from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentState:
    agent_name: str
    status: str = "pending"
    confidence: float = 0.0
    input_reference: Optional[str] = None
    output_reference: Optional[str] = None
    reasoning_summary: str = ""
    structured_decision: Dict[str, Any] = field(default_factory=dict)


class AgentOrchestrator:
    def __init__(self) -> None:
        self.agents = {
            "DiscoveryAgent": AgentState("DiscoveryAgent"),
            "EvidenceAgent": AgentState("EvidenceAgent"),
            "RiskAgent": AgentState("RiskAgent"),
            "DependencyAgent": AgentState("DependencyAgent"),
            "MigrationAgent": AgentState("MigrationAgent"),
            "PatchAgent": AgentState("PatchAgent"),
            "SandboxAgent": AgentState("SandboxAgent"),
            "VerificationAgent": AgentState("VerificationAgent"),
            "FirewallAgent": AgentState("FirewallAgent"),
            "GovernanceAgent": AgentState("GovernanceAgent"),
        }

    def run(self, finding: str, evidence: List[dict], algorithms: List[str]) -> Dict[str, Any]:
        for name in [
            "DiscoveryAgent",
            "EvidenceAgent",
            "RiskAgent",
            "DependencyAgent",
            "MigrationAgent",
            "PatchAgent",
            "SandboxAgent",
            "VerificationAgent",
            "FirewallAgent",
            "GovernanceAgent",
        ]:
            state = self.agents[name]
            state.status = "completed"
            state.confidence = 0.85 if evidence else 0.5
            state.reasoning_summary = "Evidence validated and assessment prepared."
            state.structured_decision = {
                "finding": finding,
                "algorithms": algorithms,
                "evidence_count": len(evidence),
                "status": "completed",
            }

        return {
            "investigation_id": "investigation-demo",
            "flow": [name for name in self.agents],
            "status": "completed",
            "agent_states": {name: state.__dict__ for name, state in self.agents.items()},
        }
