from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from .agents import (
    CryptographicRiskAgent,
    DependencyAgent,
    DiscoveryAgent,
    EvidenceAgent,
    FirewallAgent,
    GovernanceAgent,
    MigrationAgent,
    PatchAgent,
    SandboxAgent,
    SecurityPolicyAgent,
    VerificationAgent,
)
from .evidence import insufficient_evidence_response, normalize_evidence
from .knowledge_repo import get_knowledge_recommendation


class PQCOrchestrator:
    def __init__(self) -> None:
        self.discovery_agent = DiscoveryAgent()
        self.evidence_agent = EvidenceAgent()
        self.risk_agent = CryptographicRiskAgent()
        self.dependency_agent = DependencyAgent()
        self.migration_agent = MigrationAgent()
        self.patch_agent = PatchAgent()
        self.sandbox_agent = SandboxAgent()
        self.verification_agent = VerificationAgent()
        self.policy_agent = SecurityPolicyAgent()
        self.firewall_agent = FirewallAgent()
        self.governance_agent = GovernanceAgent()

    def assess_finding(
        self,
        finding: str,
        evidence: Optional[List[dict]] = None,
        algorithms: Optional[List[str]] = None,
        runtime_context: Optional[Dict[str, Any]] = None,
        before: Optional[List[str]] = None,
        after: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        finding_id = f"finding-{uuid.uuid4().hex[:8]}"
        if not finding or not finding.strip():
            return insufficient_evidence_response(finding_id)

        normalized_evidence = normalize_evidence(evidence or [])
        discovery = self.discovery_agent.discover(finding, algorithms)
        evidence_result = self.evidence_agent.validate(finding, normalized_evidence, algorithms)

        if not evidence_result["valid"]:
            response = insufficient_evidence_response(finding_id)
            response["uncertainties"] = evidence_result["uncertainties"]
            response["validation"] = [
                "Collect direct evidence that ties the claim to source files, configuration, package metadata, and runtime telemetry."
            ]
            return response

        algorithms = algorithms or discovery["identified_algorithms"]
        risk_result = self.risk_agent.classify(finding, algorithms)
        dependency_result = self.dependency_agent.determine_blast_radius(runtime_context, algorithms)
        migration_result = self.migration_agent.plan(algorithms, runtime_context)
        patch = self.patch_agent.generate(algorithms)
        sandbox = self.sandbox_agent.plan()
        validation = self.verification_agent.validate(before, after)
        policy = self.policy_agent.evaluate(algorithms)
        firewall = self.firewall_agent.evaluate(runtime_context)

        recommendations = get_knowledge_recommendation(algorithms)
        confidence = round((risk_result["confidence"] + min(len(normalized_evidence) / 3, 1.0)) / 2, 2)
        approval_required = migration_result.get("approval_required", True) or policy.get("status") in {"BLOCK", "REVIEW"}

        report = {
            "finding_id": finding_id,
            "classification": risk_result["classification"],
            "confidence": confidence,
            "evidence": normalized_evidence,
            "risk": risk_result["risk"],
            "blast_radius": dependency_result["blast_radius"],
            "recommended_action": migration_result["recommended_action"],
            "patch": patch,
            "sandbox_required": sandbox["sandbox_required"],
            "validation": validation,
            "rollback": migration_result["rollback"],
            "approval_required": approval_required,
            "uncertainties": evidence_result["uncertainties"],
            "knowledge": recommendations,
            "policy": policy,
            "firewall": firewall,
        }

        self.governance_agent.record(finding_id, report)
        return report
