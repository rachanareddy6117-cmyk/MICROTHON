import os
import re
import ast
import uuid
from typing import List, Dict, Any
from .base import BaseScanner
from ..core.nist_standards import get_nist_recommendation

# Rules matching RSA, ECC, ECDSA, ECDH, DH, AES, 3DES, DES, RC4, MD5, SHA-1, SHA-2, SHA-3, HMAC, TLS, ML-KEM, ML-DSA, SLH-DSA
CRYPTO_RULES = [
    # 1. RSA
    {
        "pattern": r"(?:RSA\.generate|rsa\.generate_private_key|generateKeyPair.*rsa|KeyPairGenerator\.getInstance.*RSA|crypto\.createSign.*RSA|RSA_generate_key|from cryptography\.hazmat\.primitives\.asymmetric import rsa)",
        "algorithm": "RSA",
        "category": "ASYMMETRIC_ENCRYPTION",
        "level": "CRITICAL_SHOR",
        "threat": "Polynomially broken by Shor's algorithm on a Cryptanalytically Relevant Quantum Computer (CRQC).",
        "domain": "IN_TRANSIT"
    },
    # 2. ECC / ECDSA / ECDH
    {
        "pattern": r"(?:ec\.generate_private_key|KeyPairGenerator\.getInstance.*EC|crypto\.generateKeyPair.*ec|namedCurve.*(?:secp256k1|prime256v1|p256|p384)|createECDH)",
        "algorithm": "ECC / ECDSA",
        "category": "DIGITAL_SIGNATURE",
        "level": "CRITICAL_SHOR",
        "threat": "Elliptic curve discrete logarithms are solved in polynomial time via Shor's algorithm.",
        "domain": "AUTHENTICATION_IDENTITY"
    },
    # 3. Diffie-Hellman / DH
    {
        "pattern": r"(?:createDiffieHellman|DH_generate_parameters|dhparam|from cryptography\.hazmat\.primitives\.asymmetric import dh|dh\.generate_parameters)",
        "algorithm": "Diffie-Hellman",
        "category": "KEY_EXCHANGE",
        "level": "CRITICAL_SHOR",
        "threat": "Classical discrete logarithms broken by Shor. Severe Harvest Now, Decrypt Later (HNDL) risk.",
        "domain": "IN_TRANSIT"
    },
    # 4. Weak / Legacy Symmetric: 3DES, DES, RC4, Blowfish
    {
        "pattern": r"\b(?:3DES|DES3|DES-EDE3|DES|RC4|blowfish)\b",
        "algorithm": "Legacy Symmetric Cipher (3DES/DES/RC4)",
        "category": "SYMMETRIC_CIPHER",
        "level": "MEDIUM_DEPRECATED",
        "threat": "Classically broken or weak. Highly insecure.",
        "domain": "AT_REST"
    },
    # 5. Grover-Vulnerable AES-128
    {
        "pattern": r"\b(?:aes-128-cbc|aes-128-gcm|AES128|AES\.MODE_CBC|AES\.MODE_ECB)\b",
        "algorithm": "AES-128",
        "category": "SYMMETRIC_CIPHER",
        "level": "HIGH_GROVER",
        "threat": "Grover's algorithm halves effective brute-force complexity to ~64 bits. Upgrade to AES-256.",
        "domain": "AT_REST"
    },
    # 6. Hashes & MACs: MD5, SHA-1, SHA-2, SHA-3, HMAC
    {
        "pattern": r"(?:hashlib\.(?:md5|sha1)|crypto\.createHash.*(?:md5|sha1)|MessageDigest\.getInstance.*(?:MD5|SHA-1))",
        "algorithm": "Legacy Hash (MD5 / SHA-1)",
        "category": "HASH_FUNCTION",
        "level": "MEDIUM_DEPRECATED",
        "threat": "Collision resistance broken classically and accelerated by quantum algorithms.",
        "domain": "AUTHENTICATION_IDENTITY"
    },
    {
        "pattern": r"(?:hashlib\.sha256|hashlib\.sha384|hashlib\.sha512|hashlib\.sha3_|crypto\.createHmac)",
        "algorithm": "SHA-2 / SHA-3 / HMAC",
        "category": "HASH_FUNCTION",
        "level": "PQC_RESISTANT",
        "threat": "Quantum resistant hash functions. Maintain output lengths >= 256 bits.",
        "domain": "AUTHENTICATION_IDENTITY"
    },
    # 7. Post-Quantum Cryptography (ML-KEM, ML-DSA, SLH-DSA, Kyber, Dilithium)
    {
        "pattern": r"\b(?:ML-KEM|ML-DSA|SLH-DSA|crystals-kyber|crystals-dilithium|pqcrypto|oqs)\b",
        "algorithm": "Standardized PQC (FIPS 203/204/205)",
        "category": "PQC_STANDARDIZED",
        "level": "PQC_RESISTANT",
        "threat": "NIST Post-Quantum Cryptography standard. Ensure implementation side-channel resilience.",
        "domain": "IN_TRANSIT"
    },
    # 8. Hardcoded Private Keys & Secrets
    {
        "pattern": r"(?:-----BEGIN (?:RSA )?PRIVATE KEY-----|private_key\s*=\s*['\"][A-Za-z0-9+/=]{40,})",
        "algorithm": "Hardcoded Private Key Material",
        "category": "HARDCODED_SECRET",
        "level": "CRITICAL_SHOR",
        "threat": "Static secret embedded directly in codebase. Immediate security compromise.",
        "domain": "AUTHENTICATION_IDENTITY"
    }
]

class ComprehensiveCryptoScanner(BaseScanner):
    def __init__(self):
        self.code_extensions = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".java", ".c", ".cpp", ".rs", ".cs"}

    def scan_path(self, target_path: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        findings = []
        if os.path.isfile(target_path):
            findings.extend(self._scan_file(target_path))
        else:
            for root, dirs, files in os.walk(target_path):
                dirs[:] = [d for d in dirs if d not in ["node_modules", "venv", ".venv", ".git", "__pycache__"]]
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in self.code_extensions:
                        file_path = os.path.join(root, file)
                        findings.extend(self._scan_file(file_path))
        return findings

    def _scan_file(self, file_path: str) -> List[Dict[str, Any]]:
        findings = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            return findings

        # Run AST analysis for Python files
        if file_path.endswith(".py"):
            findings.extend(self._scan_python_ast("".join(lines), file_path))

        for line_num, line in enumerate(lines, 1):
            for rule in CRYPTO_RULES:
                match = re.search(rule["pattern"], line, re.IGNORECASE)
                if match:
                    algo = rule["algorithm"]
                    # Deduplicate with AST
                    if any(f["file_path"] == file_path and f["line_number"] == line_num and f["algorithm"] == algo for f in findings):
                        continue

                    recom = get_nist_recommendation(algo)
                    finding_id = f"FIND-{uuid.uuid4().hex[:8].upper()}"

                    findings.append({
                        "id": finding_id,
                        "source_type": "code",
                        "file_path": file_path,
                        "line_number": line_num,
                        "column": match.start() + 1,
                        "code_snippet": line.strip()[:140],
                        "algorithm": algo,
                        "key_size_or_curve": self._extract_key_hint(line),
                        "category": rule["category"],
                        "vulnerability_level": rule["level"],
                        "threat_vector": rule["threat"],
                        "exposure_domain": rule["domain"],
                        "nist_replacement": recom.get("primary", "FIPS 203/204 Standard"),
                        "hybrid_pathway": recom.get("hybrid"),
                        "remediation_notes": f"Detected via code static analysis: {line.strip()[:60]}",
                        "confidence": 0.95,
                        "tags": ["code-analysis", os.path.splitext(file_path)[1].lower()]
                    })
        return findings

    def _scan_python_ast(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        findings = []
        try:
            tree = ast.parse(content, filename=file_path)
        except SyntaxError:
            return findings

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                if "cryptography.hazmat.primitives.asymmetric" in mod:
                    for alias in node.names:
                        if alias.name in ["rsa", "dsa", "ec", "dh", "x25519"]:
                            algo = alias.name.upper()
                            recom = get_nist_recommendation(algo)
                            findings.append({
                                "id": f"FIND-AST-{uuid.uuid4().hex[:8].upper()}",
                                "source_type": "code",
                                "file_path": file_path,
                                "line_number": node.lineno,
                                "column": node.col_offset,
                                "code_snippet": f"from {mod} import {alias.name}",
                                "algorithm": algo,
                                "key_size_or_curve": "Imported primitive",
                                "category": "ASYMMETRIC_ENCRYPTION",
                                "vulnerability_level": "CRITICAL_SHOR",
                                "threat_vector": "Direct import of classical asymmetric primitive broken by Shor's algorithm.",
                                "exposure_domain": "IN_TRANSIT",
                                "nist_replacement": recom.get("primary", "FIPS 203/204 Standard"),
                                "hybrid_pathway": recom.get("hybrid"),
                                "remediation_notes": "Decouple algorithm import behind a crypto-agility abstraction interface.",
                                "confidence": 1.0,
                                "tags": ["ast-analysis", "python"]
                            })
        return findings

    def _extract_key_hint(self, line: str) -> str:
        digits = re.findall(r"\b(512|1024|2048|3072|4096|128|256|384)\b", line)
        if digits:
            return f"{digits[0]} bits"
        curves = re.findall(r"(secp256k1|prime256v1|p256|p384)", line, re.IGNORECASE)
        if curves:
            return curves[0]
        return "Standard parameters"

crypto_scanner = ComprehensiveCryptoScanner()
