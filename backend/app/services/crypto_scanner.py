from __future__ import annotations

import re
from typing import Any, Dict, List

CRYPTO_PATTERNS = {
    "RSA": [r"\bRSA\b", r"\bRsa\b", r"\bPKCS#1\b"],
    "ECC": [r"\bECC\b", r"\bECDSA\b", r"\bECDH\b", r"\bsecp256r1\b", r"\bsecp384r1\b"],
    "DH": [r"\bDH\b", r"\bDiffie-Hellman\b"],
    "AES": [r"\bAES\b", r"\bAES-128\b", r"\bAES-256\b"],
    "3DES": [r"\b3DES\b", r"\bTripleDES\b"],
    "DES": [r"\bDES\b"],
    "RC4": [r"\bRC4\b"],
    "MD5": [r"\bMD5\b"],
    "SHA-1": [r"\bSHA-1\b", r"\bSHA1\b"],
    "SHA-2": [r"\bSHA-256\b", r"\bSHA-384\b", r"\bSHA-512\b"],
    "SHA-3": [r"\bSHA3\b", r"\bSHA-3\b"],
    "HMAC": [r"\bHMAC\b"],
    "TLS": [r"\bTLS\b", r"\bSSL\b"],
    "ML-KEM": [r"\bML-KEM\b", r"\bKyber\b"],
    "ML-DSA": [r"\bML-DSA\b", r"\bDilithium\b"],
    "SLH-DSA": [r"\bSLH-DSA\b", r"\bSPHINCS\b"],
}


def detect_crypto_usage(text: str) -> List[str]:
    findings: List[str] = []
    for algorithm, patterns in CRYPTO_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                findings.append(algorithm)
                break
    return sorted(set(findings))


def build_crypto_asset_record(file_path: str, line_number: int, snippet: str) -> Dict[str, Any]:
    algorithms = detect_crypto_usage(snippet)
    return {
        "file_path": file_path,
        "line_number": line_number,
        "snippet": snippet,
        "algorithms": algorithms,
        "classification": "unknown",
        "confidence": 0.8 if algorithms else 0.0,
        "status": "detected" if algorithms else "unknown",
    }


def extract_security_summary(repo_files: List[str]) -> Dict[str, Any]:
    all_algorithms: List[str] = []
    for path in repo_files:
        with open(path, "r", errors="ignore") as handle:
            content = handle.read()
            all_algorithms.extend(detect_crypto_usage(content))
    return {
        "detected_algorithms": sorted(set(all_algorithms)),
        "file_count": len(repo_files),
        "risk_level": "review" if all_algorithms else "pass",
    }
