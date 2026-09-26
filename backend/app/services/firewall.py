from __future__ import annotations

from typing import Any, Dict, List


ALLOWED_DECISIONS = {"ALLOW", "MONITOR", "WARN", "REVIEW", "BLOCK"}


class CryptoFirewallGateway:
    def __init__(self, policy_json: Dict[str, Any] | None = None) -> None:
        self.policy_json = policy_json or {
            "minimum_tls": "TLS 1.3",
            "allowed_ciphers": ["TLS_AES_256_GCM_SHA384"],
            "blocked_algorithms": ["MD5", "3DES", "DES", "RC4", "SHA-1"],
            "minimum_rsa_key_size": 3072,
            "certificate_requirements": {"sha2_required": True},
            "approved_providers": ["OpenSSL", "BoringSSL"],
            "pqc_policy": {"ml_kem_required": True, "ml_dsa_required": False},
            "exception_expiry": 30,
        }

    def evaluate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        tls_version = request.get("tls_version", "TLS 1.2")
        cipher = request.get("cipher", "")
        algorithm = request.get("algorithm", "")
        decision = "ALLOW"
        reason = "No policy violation detected."

        if tls_version in {"TLS 1.0", "TLS 1.1"}:
            decision = "MONITOR"
            reason = "Legacy TLS version detected; monitor and review before broader rollout."
        if cipher.lower().startswith("rc4") or algorithm in {"MD5", "3DES", "DES", "RC4", "SHA-1"}:
            decision = "BLOCK"
            reason = "Blocked algorithm detected; policy violation requires approval for exception handling."
        if decision == "ALLOW" and tls_version == "TLS 1.2":
            decision = "WARN"
            reason = "Policy is acceptable but should be upgraded toward TLS 1.3 and stronger cipher standards."

        return {
            "decision": decision,
            "reason": reason,
            "policy_snapshot": self.policy_json,
            "requires_approval": decision in {"BLOCK", "REVIEW"},
        }

    def recommend_policy(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        recommendations = []
        if telemetry.get("tls_version") in {"TLS 1.0", "TLS 1.1"}:
            recommendations.append("Disable legacy TLS versions and enforce TLS 1.3.")
        if telemetry.get("algorithm") in {"SHA-1", "MD5", "RC4"}:
            recommendations.append("Remove weak algorithms from approved provider policy.")
        return {"recommendations": recommendations, "status": "review"}
