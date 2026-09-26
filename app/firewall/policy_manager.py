import os
import uuid
import yaml
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

DEFAULT_POLICY_YAML = """
version: 1
name: "Enterprise Post-Quantum Defensive Policy"
minimum_tls: "TLSv1.2"
minimum_rsa_key_size: 2048
blocked_algorithms:
  - "RC4"
  - "3DES"
  - "DES"
  - "MD5"
  - "EXPORT"
  - "NULL"
allowed_ciphers:
  - "TLS_AES_256_GCM_SHA384"
  - "TLS_CHACHA20_POLY1305_SHA256"
  - "ECDHE-ECDSA-AES256-GCM-SHA384"
  - "ECDHE-RSA-AES256-GCM-SHA384"
  - "X25519Kyber768Draft00"
pqc_policy: "HYBRID_PREFERRED"
approved_providers:
  - "OpenSSL_3_2"
  - "BoringSSL"
  - "oqs-provider"
"""

class FirewallPolicyManager:
    """
    Manages versioned, reviewable, auditable, and rollbackable Policy-as-Code.
    """
    def __init__(self):
        self.policy_history: List[Dict[str, Any]] = []
        self.active_exceptions: List[Dict[str, Any]] = []
        self._load_default_policy()

    def _load_default_policy(self):
        parsed = yaml.safe_load(DEFAULT_POLICY_YAML)
        parsed["id"] = "POL-V1"
        parsed["version"] = 1
        parsed["updated_at"] = datetime.now(timezone.utc).isoformat()
        parsed["updated_by"] = "initial_setup"
        self.policy_history.append(parsed)

    def get_active_policy(self) -> Dict[str, Any]:
        return self.policy_history[-1]

    def update_policy(self, new_policy_yaml: str, author: str) -> Dict[str, Any]:
        parsed = yaml.safe_load(new_policy_yaml)
        new_version = self.policy_history[-1]["version"] + 1
        parsed["id"] = f"POL-V{new_version}"
        parsed["version"] = new_version
        parsed["updated_at"] = datetime.now(timezone.utc).isoformat()
        parsed["updated_by"] = author
        self.policy_history.append(parsed)
        return parsed

    def rollback_policy(self, target_version: int, author: str) -> Dict[str, Any]:
        target = next((p for p in self.policy_history if p["version"] == target_version), None)
        if not target:
            raise ValueError(f"Policy version {target_version} does not exist.")
        
        rolled_back = target.copy()
        new_version = self.policy_history[-1]["version"] + 1
        rolled_back["id"] = f"POL-V{new_version}"
        rolled_back["version"] = new_version
        rolled_back["updated_at"] = datetime.now(timezone.utc).isoformat()
        rolled_back["updated_by"] = f"Rollback to v{target_version} by {author}"
        self.policy_history.append(rolled_back)
        return rolled_back

    def add_exception(self, endpoint: str, cipher_or_algo: str, justification: str, approver: str, days_valid: int = 30) -> Dict[str, Any]:
        exc = {
            "id": f"EXC-{uuid.uuid4().hex[:6].upper()}",
            "endpoint": endpoint,
            "allowed_cipher_or_algo": cipher_or_algo,
            "business_justification": justification,
            "approved_by": approver,
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=days_valid)).isoformat(),
            "is_active": True
        }
        self.active_exceptions.append(exc)
        return exc

    def get_active_exceptions(self, endpoint: str) -> List[Dict[str, Any]]:
        now = datetime.now(timezone.utc).isoformat()
        return [e for e in self.active_exceptions if e["is_active"] and e["expires_at"] > now and (e["endpoint"] == endpoint or e["endpoint"] == "*")]

policy_manager = FirewallPolicyManager()
