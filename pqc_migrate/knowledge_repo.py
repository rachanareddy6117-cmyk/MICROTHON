from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

try:
    import pymupdf
except ImportError:  # pragma: no cover
    pymupdf = None

KNOWLEDGE_VERSION = "2026.09.26.v1"
KNOWN_KNOWLEDGE_SOURCE = "controlled-crypto-knowledge-base"

DEFAULT_KB: Dict[str, Dict[str, Any]] = {
    "RSA": {
        "classical": "high",
        "quantum": "critical",
        "implementation": "medium",
        "configuration": "medium",
        "recommended": "Migrate to ML-KEM for key establishment and use certificate profiles aligned to quantum-safe standards.",
    },
    "ECC": {
        "classical": "medium",
        "quantum": "critical",
        "implementation": "medium",
        "configuration": "medium",
        "recommended": "Replace ECC-based key exchange with ML-KEM and migrate signatures to ML-DSA or SLH-DSA where appropriate.",
    },
    "ECDSA": {
        "classical": "medium",
        "quantum": "critical",
        "implementation": "medium",
        "configuration": "medium",
        "recommended": "Use ML-DSA or SLH-DSA for signatures, subject to compatibility and certificate validation requirements.",
    },
    "ECDH": {
        "classical": "medium",
        "quantum": "critical",
        "implementation": "medium",
        "configuration": "medium",
        "recommended": "Replace with ML-KEM-based key establishment and validate algorithm negotiation in all endpoints.",
    },
    "DH": {
        "classical": "medium",
        "quantum": "critical",
        "implementation": "medium",
        "configuration": "medium",
        "recommended": "Apply quantum-safe key establishment and validate ephemeral key generation and group selection.",
    },
    "TLS": {
        "classical": "medium",
        "quantum": "high",
        "implementation": "medium",
        "configuration": "high",
        "recommended": "Use TLS 1.3 with approved cipher suites and PQC-capable certificate chains while enforcing policy checks.",
    },
    "AES": {
        "classical": "low",
        "quantum": "medium",
        "implementation": "medium",
        "configuration": "medium",
        "recommended": "Ensure sufficient key lengths and key rotation policies; review Grover-related strength reduction.",
    },
    "SHA": {
        "classical": "low",
        "quantum": "medium",
        "implementation": "medium",
        "configuration": "medium",
        "recommended": "Validate hash strength, use approved hash configurations, and review downgrade protections.",
    },
    "MD5": {
        "classical": "high",
        "quantum": "high",
        "implementation": "high",
        "configuration": "high",
        "recommended": "Remove MD5 from all usage paths. Replace with approved hashing and certificate validation logic.",
    },
    "3DES": {
        "classical": "high",
        "quantum": "high",
        "implementation": "high",
        "configuration": "high",
        "recommended": "Disable 3DES and migrate to modern symmetric encryption with approved policy controls.",
    },
    "DES": {
        "classical": "high",
        "quantum": "high",
        "implementation": "high",
        "configuration": "high",
        "recommended": "Remove DES entirely; use current standards and approved protocol suites.",
    },
    "RC4": {
        "classical": "high",
        "quantum": "high",
        "implementation": "high",
        "configuration": "high",
        "recommended": "Disable RC4 immediately; replace with approved modern cipher suites.",
    },
    "HMAC": {
        "classical": "low",
        "quantum": "medium",
        "implementation": "medium",
        "configuration": "medium",
        "recommended": "Use approved HMAC and hashing policies; review key sizes and validation logic.",
    },
    "ML-KEM": {
        "classical": "low",
        "quantum": "low",
        "implementation": "medium",
        "configuration": "medium",
        "recommended": "Use ML-KEM for key establishment where supported by standards and peer-reviewed implementations.",
    },
    "ML-DSA": {
        "classical": "low",
        "quantum": "low",
        "implementation": "medium",
        "configuration": "medium",
        "recommended": "Use ML-DSA for digital signatures where compatible with platform and certificate profiles.",
    },
    "SLH-DSA": {
        "classical": "low",
        "quantum": "low",
        "implementation": "medium",
        "configuration": "medium",
        "recommended": "Use SLH-DSA as a signature option where performance and interoperability requirements are acceptable.",
    },
}


def _pdf_candidates() -> List[str]:
    base_dir = Path(r"C:\Users\Rachana Reddy\OneDrive\Desktop")
    return [
        str(base_dir / "crypto_flaws_and_fixes.pdf"),
        str(Path(r"C:\Users\Rachana Reddy\Downloads\crypto_flaws_and_fixes.pdf")),
        str(Path(__file__).resolve().parent.parent / "crypto_flaws_and_fixes.pdf"),
    ]


def load_reference_text() -> str:
    for candidate in _pdf_candidates():
        if os.path.exists(candidate):
            if pymupdf is None:
                return ""
            try:
                document = pymupdf.open(candidate)
                pages = [page.get_text("text") for page in document]
                document.close()
                return "\n".join(page for page in pages if page)
            except Exception:
                return ""
    return ""


def get_knowledge_recommendation(algorithms: List[str]) -> List[dict]:
    recs: List[dict] = []
    unique_algorithms = []
    for alg in algorithms:
        if alg and alg not in unique_algorithms:
            unique_algorithms.append(alg)

    for alg in unique_algorithms:
        details = DEFAULT_KB.get(alg, {
            "classical": "unknown",
            "quantum": "unknown",
            "implementation": "unknown",
            "configuration": "unknown",
            "recommended": "Validate algorithm with the approved crypto policy and replace where needed.",
        })
        recs.append({
            "algorithm": alg,
            "knowledge_source": KNOWN_KNOWLEDGE_SOURCE,
            "knowledge_version": KNOWLEDGE_VERSION,
            "evidence": [
                "Controlled algorithm reference and migration guidance",
                "Policy-aligned cryptographic risk classification",
            ],
            "reasoning": details["recommended"],
            "confidence": 0.92,
            "risk": {
                "classical": details.get("classical", "unknown"),
                "quantum": details.get("quantum", "unknown"),
                "implementation": details.get("implementation", "unknown"),
                "configuration": details.get("configuration", "unknown"),
            },
        })
    return recs
