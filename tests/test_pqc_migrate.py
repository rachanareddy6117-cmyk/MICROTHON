from __future__ import annotations

import json

from pqc_migrate.orchestrator import PQCOrchestrator


def test_knowledge_repo_contains_standardized_pqc_algorithms():
    repo = __import__("pqc_migrate.knowledge_repo", fromlist=["get_knowledge_recommendation"]).get_knowledge_recommendation
    result = repo(["ML-KEM", "ML-DSA", "SLH-DSA"])
    assert len(result) >= 3
    assert all(item["knowledge_source"] for item in result)
    assert all(item["knowledge_version"] for item in result)


def test_orchestrator_returns_structured_report_for_valid_evidence():
    orchestrator = PQCOrchestrator()
    report = orchestrator.assess_finding(
        finding="RSA certificate used in TLS handshake for business-critical service",
        evidence=[
            {"source": "scanner", "file_path": "src/crypto/config.py", "line_number": 14, "detail": "TLS 1.2 with RSA key exchange"},
            {"source": "package", "file_path": "pom.xml", "detail": "spring-boot-starter-tomcat"},
        ],
        algorithms=["RSA", "TLS"],
        runtime_context={"service": "payments-api", "protocol": "TLS"},
    )

    assert report["classification"] in {"classical_risk", "quantum_risk", "implementation_risk", "configuration_risk", "dependency_risk", "certificate_risk"}
    assert report["confidence"] >= 0.5
    assert isinstance(report["evidence"], list)
    assert "recommended_action" in report
    assert "patch" in report
    assert report["sandbox_required"] is True


def test_orchestrator_returns_insufficient_evidence_when_empty():
    orchestrator = PQCOrchestrator()
    report = orchestrator.assess_finding(finding="Unclear issue without evidence", evidence=[], algorithms=[], runtime_context={})
    assert report["classification"] == "INSUFFICIENT_EVIDENCE"
    assert report["recommended_action"] == "REQUEST_ADDITIONAL_EVIDENCE"
    assert report["approval_required"] is True
    assert "INSUFFICIENT_EVIDENCE" in json.dumps(report)
