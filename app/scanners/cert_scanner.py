import os
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, ec, dsa, ed25519
from .base import BaseScanner
from ..core.nist_standards import get_nist_recommendation

class X509CertificateScanner(BaseScanner):
    def __init__(self):
        self.cert_extensions = {".crt", ".pem", ".cer", ".der", ".key", ".pub", ".csr"}

    def scan_path(self, target_path: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        findings = []
        if os.path.isfile(target_path):
            findings.extend(self._scan_file(target_path))
        else:
            for root, dirs, files in os.walk(target_path):
                dirs[:] = [d for d in dirs if d not in ["node_modules", "venv", ".venv", ".git"]]
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in self.cert_extensions or "cert" in file.lower() or "id_rsa" in file.lower():
                        file_path = os.path.join(root, file)
                        findings.extend(self._scan_file(file_path))
        return findings

    def _scan_file(self, file_path: str) -> List[Dict[str, Any]]:
        findings = []
        try:
            with open(file_path, "rb") as f:
                data = f.read()
        except Exception:
            return findings

        # Check for X.509 Certificate
        cert = None
        try:
            cert = x509.load_pem_x509_certificate(data, default_backend())
        except Exception:
            try:
                cert = x509.load_der_x509_certificate(data, default_backend())
            except Exception:
                pass

        if cert:
            pub_key = cert.public_key()
            algo = "RSA" if isinstance(pub_key, rsa.RSAPublicKey) else ("ECC" if isinstance(pub_key, ec.EllipticCurvePublicKey) else "Classical")
            key_size = pub_key.key_size if hasattr(pub_key, "key_size") else 2048

            try:
                not_after = cert.not_valid_after_utc
            except AttributeError:
                not_after = cert.not_valid_after.replace(tzinfo=timezone.utc)

            crosses_2030 = not_after > datetime(2030, 1, 1, tzinfo=timezone.utc)
            horizon_note = " Validity crosses 2030 CRQC Horizon!" if crosses_2030 else ""

            recom = get_nist_recommendation(algo)
            findings.append({
                "id": f"CERT-{uuid.uuid4().hex[:8].upper()}",
                "source_type": "certificate",
                "file_path": file_path,
                "line_number": 1,
                "column": 1,
                "code_snippet": f"Subject: {cert.subject.rfc4514_string()[:80]}",
                "algorithm": f"X.509 ({algo})",
                "key_size_or_curve": f"{key_size} bits",
                "category": "CERTIFICATE",
                "vulnerability_level": "CRITICAL_SHOR",
                "threat_vector": f"Public key authentication broken by Shor's algorithm.{horizon_note}",
                "exposure_domain": "IN_TRANSIT",
                "nist_replacement": recom.get("primary", "Composite X.509 with ML-DSA-65"),
                "hybrid_pathway": "Composite Certificate (IETF LAMPS)",
                "remediation_notes": f"Serial: {cert.serial_number} | Valid until: {not_after.strftime('%Y-%m-%d')}",
                "confidence": 1.0,
                "tags": ["x509", "pki", "certificate"]
            })
            return findings

        # Check for Private Key PEM
        text = data.decode("utf-8", errors="ignore")
        if "PRIVATE KEY" in text:
            algo = "RSA Private Key" if "RSA" in text else "Asymmetric Private Key"
            findings.append({
                "id": f"KEY-{uuid.uuid4().hex[:8].upper()}",
                "source_type": "certificate",
                "file_path": file_path,
                "line_number": 1,
                "column": 1,
                "code_snippet": text.strip()[:100],
                "algorithm": algo,
                "key_size_or_curve": "Stored Key File",
                "category": "CERTIFICATE",
                "vulnerability_level": "CRITICAL_SHOR",
                "threat_vector": "Stored classical private key vulnerable to factorization under Shor's algorithm.",
                "exposure_domain": "AUTHENTICATION_IDENTITY",
                "nist_replacement": "FIPS 204: ML-DSA-65 or FIPS 203: ML-KEM-768",
                "hybrid_pathway": "Dual keypairs",
                "remediation_notes": "Rotate stored private key to hybrid or post-quantum keypair.",
                "confidence": 1.0,
                "tags": ["private-key", "pem"]
            })

        return findings

cert_scanner = X509CertificateScanner()
