from __future__ import annotations

from typing import Any, Dict, List, Optional

from .knowledge_repo import get_knowledge_recommendation


class DiscoveryAgent:
    def discover(self, finding: str, algorithms: Optional[List[str]] = None) -> Dict[str, Any]:
        identified = [alg for alg in (algorithms or []) if alg]
        if not identified:
            inferred = []
            for token in ["RSA", "ECC", "ECDSA", "ECDH", "DH", "TLS", "AES", "SHA", "MD5", "3DES", "DES", "RC4", "HMAC", "ML-KEM", "ML-DSA", "SLH-DSA"]:
                if token.lower() in finding.lower():
                    inferred.append(token)
            identified = inferred
        return {
            "finding": finding,
            "identified_algorithms": identified,
            "observations": [
                "Interpret scanner findings before assigning risk.",
                "Correlate result with configuration and certificate metadata."
            ],
        }


class EvidenceAgent:
    def validate(self, finding: str, evidence: List[dict], algorithms: Optional[List[str]] = None) -> Dict[str, Any]:
        normalized = [item for item in evidence if item and isinstance(item, dict)]
        if not normalized:
            return {
                "valid": False,
                "uncertainties": ["No direct evidence was provided for the finding."],
                "evidence": [],
            }
        return {
            "valid": True,
            "uncertainties": [],
            "evidence": normalized,
            "algorithms": algorithms or [],
            "evidence_quality": "sufficient" if len(normalized) >= 1 else "insufficient",
        }


class CryptographicRiskAgent:
    def classify(self, finding: str, algorithms: List[str]) -> Dict[str, Any]:
        if not algorithms:
            return {
                "classification": "configuration_risk",
                "confidence": 0.45,
                "risk": {
                    "classical": "unknown",
                    "quantum": "unknown",
                    "implementation": "unknown",
                    "configuration": "unknown",
                },
            }

        primary = algorithms[0]
        knowledge = get_knowledge_recommendation([primary])[0]
        risk = knowledge["risk"]
        classification = "implementation_risk"
        if any(k in primary for k in ["RSA", "ECC", "ECDSA", "ECDH", "DH", "TLS"]):
            classification = "quantum_risk" if risk["quantum"] in {"critical", "high"} else "classical_risk"
        if primary in {"MD5", "3DES", "DES", "RC4"}:
            classification = "classical_risk"
        if "TLS" in primary or "config" in finding.lower():
            classification = "configuration_risk"
        if "certificate" in finding.lower() or "cert" in finding.lower():
            classification = "certificate_risk"

        return {
            "classification": classification,
            "confidence": 0.9,
            "risk": risk,
        }


class DependencyAgent:
    def determine_blast_radius(self, runtime_context: Optional[Dict[str, Any]], algorithms: List[str]) -> Dict[str, Any]:
        service = (runtime_context or {}).get("service", "unknown-service")
        dependencies = [
            f"application:{service}",
            "service:gateway",
            "package:crypto-library",
            "crypto-library:provider",
            "algorithm:" + (algorithms[0] if algorithms else "unknown"),
            "certificate:validated-chain",
            "protocol:TLS",
            "data-asset:session-and-identity-data",
        ]
        return {
            "application": service,
            "blast_radius": dependencies,
            "scope": "endpoint and trust boundary affected",
        }


class MigrationAgent:
    def plan(self, algorithms: List[str], runtime_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        service = (runtime_context or {}).get("service", "unknown-service")
        recommendation = get_knowledge_recommendation(algorithms)
        recommended_algorithms = [item["algorithm"] for item in recommendation]
        return {
            "recommended_action": "Migrate the vulnerable crypto path to approved PQC-compatible mechanisms and validate compatibility in the service boundary before approval.",
            "migration_sequence": [
                "Inventory affected algorithms and certificate dependencies.",
                "Replace vulnerable handshakes or key establishment with approved standards.",
                "Validate service compatibility and certificate chains.",
                "Run sandbox regression and crypto-agility checks.",
                "Request approval for production rollout.",
            ],
            "compatibility_requirements": [
                "Validate all client and server protocol negotiation before rollout.",
                "Confirm certificate compatibility and provider support.",
                "Test performance and compatibility for service: " + service,
            ],
            "testing_requirements": [
                "Unit tests",
                "Integration tests",
                "Crypto-agility tests",
                "Certificate validation tests",
            ],
            "rollback": [
                "Restore previous crypto provider configuration.",
                "Revoke or isolate the tested environment if regression is detected.",
            ],
            "approval_required": True,
            "recommended_algorithms": recommended_algorithms,
        }


class PatchAgent:
    def generate(self, algorithms: List[str]) -> str:
        if not algorithms:
            return "No patch generated because the finding lacks sufficient evidence."
        return (
            "patch: replace vulnerable algorithm usage with standards-compliant migration path\n"
            f"- Replace {', '.join(algorithms)} with approved PQC-capable alternatives and validate certificate compatibility\n"
            "- Update protocol configuration to enforce safe negotiation and policy checks\n"
            "- Add explicit crypto-agility hooks and test coverage before deployment"
        )


class SandboxAgent:
    def plan(self) -> Dict[str, Any]:
        return {
            "sandbox_required": True,
            "checks": [
                "build",
                "unit tests",
                "integration tests",
                "crypto tests",
                "compatibility tests",
                "scanner rescan",
            ],
        }


class VerificationAgent:
    def validate(self, before: Optional[List[str]], after: Optional[List[str]]) -> List[str]:
        before_set = set(before or [])
        after_set = set(after or [])
        checks = [
            "Verify the vulnerable algorithm is removed from the active configuration.",
            "Confirm the expected replacement mechanism is present.",
            "Confirm certificate metadata remains valid after migration.",
            "Check that runtime policy does not reintroduce prohibited crypto usage.",
        ]
        if before_set.intersection(after_set):
            checks.append("A residual overlap between before/after algorithm inventory was detected; review the patch.")
        return checks


class SecurityPolicyAgent:
    def evaluate(self, algorithms: List[str]) -> Dict[str, Any]:
        if not algorithms:
            return {"status": "REVIEW", "reason": "No algorithm inventory was supplied."}
        forbidden = {"MD5", "3DES", "DES", "RC4"}
        if set(algorithms).intersection(forbidden):
            return {"status": "BLOCK", "reason": "Prohibited algorithms are present in the target configuration."}
        return {"status": "PASS", "reason": "Risk assessment stays within approved crypto policy boundaries."}


class FirewallAgent:
    def evaluate(self, runtime_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        telemetry = runtime_context or {}
        protocol = telemetry.get("protocol", "TLS")
        if protocol == "TLS 1.2":
            return {"decision": "MONITOR", "reason": "TLS 1.2 may be acceptable only when cipher suite and compatibility policy are validated."}
        return {"decision": "ALLOW", "reason": "No evident policy violation was identified in the current runtime signal."}


class GovernanceAgent:
    def record(self, finding_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "finding_id": finding_id,
            "audit_trail": [
                "Discovery performed",
                "Evidence validated",
                "Risk classified",
                "Migration plan generated",
                "Patch prepared",
                "Sandbox plan recorded",
                "Approval state recorded",
            ],
            "result": result,
        }
