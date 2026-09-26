from __future__ import annotations

import hashlib
import json
import re
import tempfile
import tomllib
import uuid
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath
from typing import Any

import pymupdf
from fastapi import UploadFile

from backend.app.config import settings
from backend.app.services.crypto_scanner import detect_crypto_usage
from backend.app.services.project_scanner import build_project_scan_result
from pqc_migrate.knowledge_repo import get_knowledge_recommendation

MAX_PDF_PAGES = 500
MAX_EXTRACTED_CHARACTERS = 2_000_000
MAX_ZIP_ENTRIES = 20_000
MAX_ZIP_EXPANDED_BYTES = 2 * 1024 * 1024 * 1024
MAX_SCANNED_FILE_BYTES = 5 * 1024 * 1024
MAX_ZIP_SCAN_BYTES = 512 * 1024 * 1024
TEXT_SUFFIXES = {
    ".c", ".cc", ".cpp", ".cs", ".go", ".h", ".hpp", ".java", ".js", ".jsx",
    ".json", ".kt", ".pem", ".properties", ".py", ".rb", ".rs", ".sh", ".sql",
    ".tf", ".toml", ".ts", ".tsx", ".xml", ".yaml", ".yml", ".txt", ".conf",
    ".cfg", ".ini", ".gradle", ".mod", ".sum", ".lock", ".md", ".sbom", ".cbom",
}
UPLOAD_SUFFIXES = {".pdf", ".zip", ".json", ".yaml", ".yml", ".crt", ".pem", ".sbom", ".cbom"} | TEXT_SUFFIXES
SECRET_MARKERS = (
    "-----BEGIN PRIVATE KEY-----",
    "-----BEGIN RSA PRIVATE KEY-----",
    "-----BEGIN EC PRIVATE KEY-----",
)
KEY_ASSIGNMENT = re.compile(
    r"(?i)\b(?:secret|private[_-]?key|api[_-]?key|password)\b\s*[:=]\s*['\"][^'\"]{8,}['\"]"
)
DEFAULT_COST_ASSUMPTIONS = {
    "hourly_rate_usd": 150.0,
    "legacy_fix_hours_per_finding": 8.0,
    "quantum_migration_hours_per_finding": 16.0,
    "crypto_review_hours_per_finding": 3.0,
}
LEGACY_ALGORITHMS = {"MD5", "SHA-1", "DES", "3DES", "RC4"}
QUANTUM_VULNERABLE_ALGORITHMS = {"RSA", "ECC", "DH"}
PQC_ALGORITHMS = {"ML-KEM", "ML-DSA", "SLH-DSA"}
LANGUAGE_SUFFIXES = {
    ".c": "C", ".cc": "C++", ".cpp": "C++", ".cs": "C#",
    ".go": "Go", ".h": "C/C++", ".hpp": "C++", ".java": "Java",
    ".js": "JavaScript", ".jsx": "JavaScript", ".kt": "Kotlin",
    ".py": "Python", ".rb": "Ruby", ".rs": "Rust", ".sh": "Shell",
    ".sql": "SQL", ".ts": "TypeScript", ".tsx": "TypeScript",
}
DEPENDENCY_MANIFESTS = {
    "package.json", "package-lock.json", "npm-shrinkwrap.json",
    "requirements.txt", "requirements-dev.txt", "pyproject.toml",
    "poetry.lock", "Pipfile", "Pipfile.lock", "go.mod", "go.sum",
    "pom.xml", "build.gradle", "build.gradle.kts", "Cargo.toml",
    "Cargo.lock", "Gemfile", "Gemfile.lock",
}


def _normalized_cost_assumptions(assumptions: dict[str, float] | None) -> dict[str, float]:
    result = DEFAULT_COST_ASSUMPTIONS | (assumptions or {})
    bounds = {
        "hourly_rate_usd": (1, 5000),
        "legacy_fix_hours_per_finding": (0, 1000),
        "quantum_migration_hours_per_finding": (0, 1000),
        "crypto_review_hours_per_finding": (0, 1000),
    }
    for name, (minimum, maximum) in bounds.items():
        value = result[name]
        if not isinstance(value, (int, float)) or not minimum <= value <= maximum:
            raise ValueError(f"{name} must be between {minimum} and {maximum}.")
        result[name] = float(value)
    return result


def _estimate_cost(
    assets: list[dict[str, Any]],
    assumptions: dict[str, float] | None = None,
) -> dict[str, Any]:
    inputs = _normalized_cost_assumptions(assumptions)
    finding_keys: set[tuple[str, str]] = set()
    counts = {"legacy_crypto": 0, "quantum_vulnerable_public_key": 0, "crypto_review": 0}
    for asset in assets:
        for algorithm in asset["algorithms"]:
            key = (asset["file"], algorithm)
            if key in finding_keys:
                continue
            finding_keys.add(key)
            if algorithm in LEGACY_ALGORITHMS:
                counts["legacy_crypto"] += 1
            elif algorithm in QUANTUM_VULNERABLE_ALGORITHMS:
                counts["quantum_vulnerable_public_key"] += 1
            else:
                counts["crypto_review"] += 1

    hours_by_category = {
        "legacy_crypto": inputs["legacy_fix_hours_per_finding"],
        "quantum_vulnerable_public_key": inputs["quantum_migration_hours_per_finding"],
        "crypto_review": inputs["crypto_review_hours_per_finding"],
    }
    baseline_analysis_hours = 2.0
    expected_hours = baseline_analysis_hours + sum(
        counts[category] * hours_by_category[category] for category in counts
    )
    low_hours = expected_hours * 0.75
    high_hours = expected_hours * 1.5
    rate = inputs["hourly_rate_usd"]
    return {
        "status": "ESTIMATED",
        "estimate_type": "assumption-based engineering effort estimate; not a vendor quote",
        "currency": "USD",
        "total_cost_usd": round(expected_hours * rate, 2),
        "cost_range_usd": {
            "low": round(low_hours * rate, 2),
            "expected": round(expected_hours * rate, 2),
            "high": round(high_hours * rate, 2),
        },
        "estimated_hours": {
            "low": round(low_hours, 1),
            "expected": round(expected_hours, 1),
            "high": round(high_hours, 1),
        },
        "finding_counts": counts,
        "assumptions": {
            **inputs,
            "baseline_analysis_hours": baseline_analysis_hours,
            "range_method": "low = 75% and high = 150% of expected effort",
            "deduplication": "one work item per distinct source file and algorithm",
        },
        "exclusions": [
            "Vendor or license costs, infrastructure, procurement, and taxes.",
            "Measured compatibility testing, deployment, and production incident costs.",
            "The estimate is based on static candidate matches and needs engineering review.",
        ],
    }


def _dependency_names(manifest_name: str, content: str) -> list[str]:
    try:
        if manifest_name == "package.json":
            package = json.loads(content)
            sections = ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies")
            return sorted({name for section in sections for name in package.get(section, {})})
        if manifest_name in {"package-lock.json", "npm-shrinkwrap.json"}:
            package_lock = json.loads(content)
            packages = package_lock.get("packages", {})
            from_package_paths = {
                match.group(1)
                for path in packages
                if (match := re.search(r"(?:^|/)node_modules/(.+)$", path))
            }
            return sorted(from_package_paths or package_lock.get("dependencies", {}))
        if manifest_name in {"pyproject.toml", "Cargo.toml"}:
            parsed = tomllib.loads(content)
            if manifest_name == "Cargo.toml":
                return sorted(parsed.get("dependencies", {}))
            project = parsed.get("project", {})
            names = {dependency.split(";", 1)[0].split("[", 1)[0].split()[0] for dependency in project.get("dependencies", [])}
            poetry = parsed.get("tool", {}).get("poetry", {}).get("dependencies", {})
            names.update(name for name in poetry if name.lower() != "python")
            return sorted(names)
        if manifest_name in {"poetry.lock", "Cargo.lock"}:
            parsed = tomllib.loads(content)
            return sorted({
                package["name"]
                for package in parsed.get("package", [])
                if isinstance(package, dict) and package.get("name")
            })
        if manifest_name == "pom.xml":
            root = ET.fromstring(content)
            namespace = {"m": "http://maven.apache.org/POM/4.0.0"}
            found = root.findall(".//m:dependency/m:artifactId", namespace)
            return sorted({element.text.strip() for element in found if element.text})
        if manifest_name.startswith("requirements") or manifest_name in {"Pipfile", "Pipfile.lock"}:
            if manifest_name == "Pipfile":
                parsed = tomllib.loads(content)
                return sorted(set(parsed.get("packages", {})) | set(parsed.get("dev-packages", {})))
            if manifest_name == "Pipfile.lock":
                parsed = json.loads(content)
                return sorted(set(parsed.get("default", {})) | set(parsed.get("develop", {})))
            return sorted({
                match.group(1)
                for line in content.splitlines()
                if (match := re.match(r"\s*([A-Za-z0-9_.-]+)\s*(?:[<>=!~;\[]|$)", line))
                and not line.lstrip().startswith("#")
            })
        if manifest_name == "go.mod":
            return sorted({
                match.group(1)
                for line in content.splitlines()
                if (match := re.match(r"\s*(?:require\s+)?([A-Za-z0-9._~/-]+\.[A-Za-z0-9._~/-]+)\s+v[\w.+-]+", line))
            })
        if manifest_name in {"build.gradle", "build.gradle.kts"}:
            return sorted(set(re.findall(
                r"""(?:implementation|api|runtimeOnly|compileOnly)\s*\(?\s*["']([^:"']+):[^:"']+:[^"']+["']""",
                content,
            )))
        if manifest_name in {"Gemfile", "Gemfile.lock"}:
            return sorted(set(re.findall(r"""^\s*gem\s+["']([^"']+)["']""", content, flags=re.MULTILINE)))
    except (json.JSONDecodeError, tomllib.TOMLDecodeError, ET.ParseError, AttributeError, TypeError, IndexError):
        return []
    return []


def _software_analysis(
    files: list[tuple[str, str]],
    assets: list[dict[str, Any]],
    secrets: list[dict[str, Any]],
) -> dict[str, Any]:
    languages: dict[str, int] = {}
    manifests: list[dict[str, Any]] = []
    packages_by_name: dict[str, str] = {}
    total_lines = 0
    for path, text in files:
        suffix = Path(path).suffix.lower()
        if language := LANGUAGE_SUFFIXES.get(suffix):
            languages[language] = languages.get(language, 0) + 1
        total_lines += len(text.splitlines())
        file_name = Path(path).name
        if file_name in DEPENDENCY_MANIFESTS or file_name.startswith("requirements"):
            dependencies = _dependency_names(file_name, text)
            manifests.append({"file": path, "dependency_count": len(dependencies)})
            for dependency in dependencies:
                packages_by_name.setdefault(dependency, path)
    return {
        "status": "static_analysis_complete",
        "source_files_analyzed": len(files),
        "total_text_lines_analyzed": total_lines,
        "languages_detected": languages,
        "package_manifests": manifests,
        "dependencies_identified": len(packages_by_name),
        "dependency_names": sorted(packages_by_name)[:500],
        "crypto_candidate_matches": len(assets),
        "potential_secret_findings": len(secrets),
        "dependency_vulnerability_status": "NOT_CHECKED_NO_ADVISORY_FEED_CONFIGURED",
        "build_and_tests": "NOT_RUN; uploaded software is never executed",
        "limitations": [
            "Dependency names are read from supported text manifests; versions and transitive resolution are not verified.",
            "Known-vulnerability matching needs a configured, current advisory database.",
            "Static crypto matches do not prove code paths are reachable at runtime.",
        ],
    }


def _safe_archive_name(name: str) -> str | None:
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or any(part in {"..", ""} for part in path.parts):
        return None
    if re.match(r"^[a-zA-Z]:", normalized):
        return None
    return path.as_posix()


def _line_evidence(source_name: str, text: str) -> list[dict[str, Any]]:
    assets: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        algorithms = detect_crypto_usage(line)
        if algorithms:
            is_sensitive = (
                any(marker in line for marker in SECRET_MARKERS)
                or KEY_ASSIGNMENT.search(line) is not None
            )
            assets.append({
                "file": source_name,
                "line": line_number,
                "algorithms": algorithms,
                "evidence": (
                    "[REDACTED: possible secret material]"
                    if is_sensitive
                    else line.strip()[:500]
                ),
                "evidence_hash": hashlib.sha256(line.encode("utf-8")).hexdigest(),
            })
        if len(assets) >= 5000:
            break
    return assets


def _secret_evidence(source_name: str, text: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(marker in line for marker in SECRET_MARKERS) or KEY_ASSIGNMENT.search(line):
            results.append({
                "file": source_name,
                "line": line_number,
                "type": "potential_hardcoded_secret",
                "evidence": "[REDACTED: possible secret material]",
                "evidence_hash": hashlib.sha256(line.encode("utf-8")).hexdigest(),
            })
            if len(results) >= 1000:
                break
    return results


def _make_risk_report(
    text: str,
    assets: list[dict[str, Any]],
    software_files: list[tuple[str, str]],
    cost_assumptions: dict[str, float] | None = None,
) -> dict[str, Any]:
    algorithms = sorted({
        algorithm
        for asset in assets
        for algorithm in asset["algorithms"]
    })
    knowledge_aliases = {
        "SHA-1": "SHA",
        "SHA-2": "SHA",
        "SHA-3": "SHA",
        "AES": "AES",
    }
    knowledge_algorithms = list(dict.fromkeys(
        knowledge_aliases.get(algorithm, algorithm) for algorithm in algorithms
    ))
    recommendations = get_knowledge_recommendation(knowledge_algorithms)
    risk_levels = [recommendation["risk"] for recommendation in recommendations]
    severity_order = {"unknown": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}

    def highest_risk(key: str) -> str:
        return max(
            (risk.get(key, "unknown") for risk in risk_levels),
            key=lambda value: severity_order.get(value, 0),
            default="unknown",
        )

    project_result = build_project_scan_result(text)
    secrets = [
        secret
        for source_name, source_text in (
            software_files if software_files else [("document-or-source", text)]
        )
        for secret in _secret_evidence(source_name, source_text)
    ]
    report = {
        "assessment_type": "evidence-based cryptographic risk assessment",
        "classification": (
            "INSUFFICIENT_EVIDENCE"
            if not algorithms and not secrets and not project_result["profile"]["risks"]
            else "REVIEW_REQUIRED"
        ),
        "risk": {
            "classical": highest_risk("classical"),
            "quantum": highest_risk("quantum"),
            "implementation": highest_risk("implementation"),
            "configuration": highest_risk("configuration"),
            "financial": "see cost estimate",
            "operational": "unknown",
            "compliance": "unknown",
        },
        "project_profile": project_result["profile"],
        "algorithms": algorithms,
        "crypto_assets": assets,
        "potential_secret_findings": secrets,
        "knowledge_recommendations": recommendations,
        "cost_analysis": _estimate_cost(assets, cost_assumptions),
        "efficiency_analysis": {
            "status": "NOT_MEASURED",
            "finding_count": len(assets),
            "reason": "Performance and delivery efficiency require measured baseline and post-change telemetry.",
        },
        "confidence": 0.0 if not assets else 0.8,
        "uncertainties": [
            "Text matching identifies candidate crypto usage; it does not prove runtime reachability.",
            "Certificate cryptographic metadata and dependency relationships require dedicated parsers or scanner evidence.",
            "Cost and performance impact are not estimated without organization-provided inputs and measurements.",
        ],
        "llm_status": {
            "configured": False,
            "reason": "No generative LLM endpoint is configured; output uses deterministic scanning and the controlled knowledge repository.",
        },
    }
    if software_files:
        report["software_analysis"] = _software_analysis(software_files, assets, secrets)
    return report


async def scan_upload(
    file: UploadFile,
    cost_assumptions: dict[str, float] | None = None,
) -> dict[str, Any]:
    if not file.filename:
        raise ValueError("Uploaded file is missing a name.")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in UPLOAD_SUFFIXES:
        raise ValueError("Unsupported type. Upload a PDF, ZIP, configuration, certificate, SBOM, or CBOM file.")

    scan_id = str(uuid.uuid4())
    digest = hashlib.sha256()
    byte_count = 0
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(prefix="pqc-scan-", suffix=suffix, delete=False) as staged:
            temp_path = Path(staged.name)
            while chunk := await file.read(1024 * 1024):
                byte_count += len(chunk)
                if byte_count > settings.max_upload_bytes:
                    raise ValueError("Upload exceeds the 10 GiB limit.")
                digest.update(chunk)
                staged.write(chunk)

        assets: list[dict[str, Any]] = []
        source_text = ""
        scanned_files = 0
        software_files: list[tuple[str, str]] = []

        if suffix == ".pdf":
            with pymupdf.open(temp_path) as document:
                if document.page_count > MAX_PDF_PAGES:
                    raise ValueError(f"PDF exceeds the {MAX_PDF_PAGES}-page analysis limit.")
                pages: list[str] = []
                character_count = 0
                for page in document:
                    page_text = page.get_text("text")
                    character_count += len(page_text)
                    if character_count > MAX_EXTRACTED_CHARACTERS:
                        raise ValueError("Extracted PDF text exceeds the analysis limit.")
                    pages.append(page_text)
                source_text = "\n".join(pages)
                assets = _line_evidence(file.filename, source_text)
                scanned_files = document.page_count

        elif suffix == ".zip":
            with zipfile.ZipFile(temp_path) as archive:
                entries = archive.infolist()
                if len(entries) > MAX_ZIP_ENTRIES:
                    raise ValueError(f"ZIP exceeds the {MAX_ZIP_ENTRIES}-entry limit.")
                total_expanded = 0
                scanned_bytes = 0
                text_parts: list[str] = []
                for info in entries:
                    safe_name = _safe_archive_name(info.filename)
                    if safe_name is None:
                        raise ValueError("ZIP contains an unsafe path.")
                    if info.is_dir():
                        continue
                    if (info.external_attr >> 16) & 0o170000 == 0o120000:
                        raise ValueError("ZIP contains a symbolic link.")
                    total_expanded += info.file_size
                    if total_expanded > MAX_ZIP_EXPANDED_BYTES:
                        raise ValueError("ZIP expanded contents exceed the 2 GiB scan limit.")
                    if info.file_size > MAX_SCANNED_FILE_BYTES or Path(safe_name).suffix.lower() not in TEXT_SUFFIXES:
                        continue
                    if info.compress_size and info.file_size / info.compress_size > 1000:
                        raise ValueError("ZIP contains an entry with an unsafe compression ratio.")
                    if scanned_bytes + info.file_size > MAX_ZIP_SCAN_BYTES:
                        break
                    with archive.open(info, "r") as source:
                        raw = source.read(MAX_SCANNED_FILE_BYTES + 1)
                    if len(raw) > MAX_SCANNED_FILE_BYTES:
                        continue
                    text = raw.decode("utf-8", errors="replace")
                    text_parts.append(text)
                    assets.extend(_line_evidence(safe_name, text))
                    software_files.append((safe_name, text))
                    scanned_bytes += len(raw)
                    scanned_files += 1
                source_text = "\n".join(text_parts)

        else:
            if byte_count > MAX_SCANNED_FILE_BYTES:
                raise ValueError("Individual configuration and SBOM files must be 5 MiB or smaller.")
            source_text = temp_path.read_text(encoding="utf-8", errors="replace")
            assets = _line_evidence(file.filename, source_text)
            scanned_files = 1
            if suffix != ".pdf":
                software_files.append((file.filename, source_text))

        report = _make_risk_report(source_text, assets, software_files, cost_assumptions)
        return {
            "scan_id": scan_id,
            "status": "completed" if source_text.strip() else "insufficient_evidence",
            "filename": Path(file.filename).name,
            "bytes_received": byte_count,
            "sha256": digest.hexdigest(),
            "scanned_files_or_pages": scanned_files,
            "report": report,
        }
    except zipfile.BadZipFile as exc:
        raise ValueError("The uploaded ZIP file is invalid.") from exc
    except pymupdf.FileDataError as exc:
        raise ValueError("The uploaded PDF file is invalid or cannot be parsed.") from exc
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        await file.close()
