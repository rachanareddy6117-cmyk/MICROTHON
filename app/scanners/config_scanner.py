import os
import re
import uuid
from typing import List, Dict, Any
from .base import BaseScanner
from ..core.nist_standards import get_nist_recommendation

CONFIG_RULES = [
    {
        "pattern": r"(?:ssl_ciphers|SSLCipherSuite)\s+.*",
        "description": "TLS Cipher Suite configuration contains quantum-vulnerable key exchange or RSA authentication.",
        "domain": "IN_TRANSIT"
    },
    {
        "pattern": r"ssl_protocols\s+.*(?:TLSv1|TLSv1\.1|SSLv3)",
        "description": "Deprecated TLS 1.0/1.1 protocol enabled. High downgrade attack risk.",
        "domain": "IN_TRANSIT"
    },
    {
        "pattern": r"(?:HostKey.*(?:id_rsa|id_ecdsa|id_dsa)|KexAlgorithms.*(?:diffie-hellman|ecdh))",
        "description": "SSH daemon configured with quantum-vulnerable HostKey or Key Exchange.",
        "domain": "AUTHENTICATION_IDENTITY"
    },
    {
        "pattern": r"customer_master_key_spec\s*=\s*.*(?:RSA_2048|RSA_3072|RSA_4096|ECC_NIST_P256)",
        "description": "Cloud KMS asymmetric key configuration subject to Shor's algorithm.",
        "domain": "AT_REST"
    }
]

class InfrastructureConfigScanner(BaseScanner):
    def __init__(self):
        self.extensions = {".conf", ".cnf", ".yaml", ".yml", ".json", ".env", ".tf", ".toml"}
        self.special_files = {"dockerfile", "sshd_config", "nginx.conf"}

    def scan_path(self, target_path: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        findings = []
        if os.path.isfile(target_path):
            findings.extend(self._scan_file(target_path))
        else:
            for root, dirs, files in os.walk(target_path):
                dirs[:] = [d for d in dirs if d not in ["node_modules", "venv", ".venv", ".git"]]
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in self.extensions or file.lower() in self.special_files:
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

        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith("#"):
                continue
            for rule in CONFIG_RULES:
                match = re.search(rule["pattern"], line, re.IGNORECASE)
                if match:
                    recom = get_nist_recommendation("TLS")
                    findings.append({
                        "id": f"CFG-{uuid.uuid4().hex[:8].upper()}",
                        "source_type": "config",
                        "file_path": file_path,
                        "line_number": line_num,
                        "column": match.start() + 1,
                        "code_snippet": line.strip()[:140],
                        "algorithm": "Configured Protocol / Cipher Suite",
                        "key_size_or_curve": "Config-driven",
                        "category": "PROTOCOL_CONFIG",
                        "vulnerability_level": "CRITICAL_SHOR",
                        "threat_vector": rule["description"],
                        "exposure_domain": rule["domain"],
                        "nist_replacement": recom.get("primary", "Hybrid X25519+ML-KEM-768"),
                        "hybrid_pathway": "TLS 1.3 with Hybrid Post-Quantum Key Exchange",
                        "remediation_notes": "Update configuration to require TLS 1.3 and hybrid PQC key exchange.",
                        "confidence": 0.98,
                        "tags": ["config", "infrastructure"]
                    })
        return findings

config_scanner = InfrastructureConfigScanner()
