from __future__ import annotations

import hashlib
import re
import tempfile
import uuid
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

import pymupdf
from fastapi import UploadFile

from backend.app.config import settings
from backend.app.services.crypto_scanner import CRYPTO_PATTERNS, detect_crypto_usage
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
SECRET_MARKERS = (
    "-----BEGIN PRIVATE KEY-----",
    "-----BEGIN RSA PRIVATE KEY-----",
    "-----BEGIN EC PRIVATE KEY-----",
)
KEY_ASSIGNMENT = re.compile(
    r"(?i)\b(?:secret|private[_-]?key|api[_-]?key|password)\b\s*[:=]\s*['\"][^'\"]{8,}['\"]"
)


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


def _make_risk_report(text: str, assets: list[dict[str, Any]]) -> dict[str, Any]:
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
    secrets = _secret_evidence("document-or-source", text)
    return {
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
            "financial": "unknown",
            "operational": "unknown",
            "compliance": "unknown",
        },
        "project_profile": project_result["profile"],
        "algorithms": algorithms,
        "crypto_assets": assets,
        "potential_secret_findings": secrets,
        "knowledge_recommendations": recommendations,
        "cost_analysis": {
            "status": "INSUFFICIENT_EVIDENCE",
            "reason": "No validated migration estimates, rates, or cost inputs were provided.",
            "source_budget": project_result["profile"]["budget"],
        },
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


async def scan_upload(file: UploadFile) -> dict[str, Any]:
    if not file.filename:
        raise ValueError("Uploaded file is missing a name.")

    suffix = Path(file.filename).suffix.lower()
    allowed_suffixes = {".pdf", ".zip", ".json", ".yaml", ".yml", ".crt", ".pem", ".sbom", ".cbom"}
    if suffix not in allowed_suffixes:
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
                    scanned_bytes += len(raw)
                    scanned_files += 1
                source_text = "\n".join(text_parts)

        else:
            if byte_count > MAX_SCANNED_FILE_BYTES:
                raise ValueError("Individual configuration and SBOM files must be 5 MiB or smaller.")
            source_text = temp_path.read_text(encoding="utf-8", errors="replace")
            assets = _line_evidence(file.filename, source_text)
            scanned_files = 1

        report = _make_risk_report(source_text, assets)
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
