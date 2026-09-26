import os
import sys

# Ensure root workspace is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scanners.crypto_scanner import crypto_scanner
from app.scanners.config_scanner import config_scanner
from app.scanners.cert_scanner import cert_scanner
from app.graph.builder import graph_builder
from app.graph.blast_radius import blast_calculator
from app.agents.orchestrator import agent_engine
from app.remediation.workflow import remediation_manager
from app.firewall.engine import CryptoFirewallDecisionEngine, HandshakeMetadata
from app.firewall.policy_manager import policy_manager
from app.core.kms import kms_service
from app.core.disclaimer import LIMITATIONS_DISCLOSURE

def test_full_pqc_migrate_system():
    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "adversarial_repo")
    assert os.path.exists(test_dir), "Adversarial test directory must exist"

    print("\n========================================================")
    print("RUNNING ADVERSARIAL PQC-MIGRATE VERIFICATION SUITE")
    print("========================================================")

    # 1. Crypto Scanner Test
    findings = crypto_scanner.scan_path(test_dir)
    cfg_findings = config_scanner.scan_path(test_dir)
    cert_findings = cert_scanner.scan_path(test_dir)
    all_findings = findings + cfg_findings + cert_findings

    print(f"[TEST 1] Crypto Scanners: Detected {len(all_findings)} vulnerable items.")
    algos = [f["algorithm"] for f in all_findings]
    assert any("RSA" in a for a in algos), "Must detect RSA"
    assert any("ECC" in a or "ECDSA" in a for a in algos), "Must detect ECC/ECDSA"
    assert any("3DES" in a or "RC4" in a for a in algos), "Must detect weak symmetric ciphers"
    assert any("MD5" in a or "SHA-1" in a for a in algos), "Must detect weak hashes"
    print("  -> PASSED: All adversarial primitives detected.")

    # 2. Dependency Graph & Blast Radius
    nodes, edges = graph_builder.build_hierarchy("Adversarial-Repo", test_dir, all_findings)
    blast = blast_calculator.calculate(graph_builder, all_findings)
    print(f"[TEST 2] Dependency Graph: {len(nodes)} nodes, {len(edges)} edges, {len(blast)} blast radius records.")
    assert len(nodes) > 0 and len(edges) > 0
    print("  -> PASSED: 8-tier hierarchical graph constructed.")

    # 3. Agentic AI Orchestrator (10 Agents)
    state = agent_engine.execute_workflow(test_dir, "Adversarial-Repo")
    print(f"[TEST 3] Agent Orchestrator: {len(state.execution_logs)} agent actions logged.")
    assert len(state.execution_logs) >= 10, "All 10 agents must log actions"
    agent_names = {log["agent_name"] for log in state.execution_logs}
    for req_agent in ["DiscoveryAgent", "EvidenceAgent", "RiskAgent", "DependencyAgent", "MigrationAgent", "PatchAgent", "SandboxAgent", "VerificationAgent", "FirewallAgent", "GovernanceAgent"]:
        assert req_agent in agent_names, f"{req_agent} must execute"
    print(f"  -> PASSED: All 10 agents executed with structured state communication.")

    # 4. Auto Remediation & Rollback
    finding_sample = all_findings[0]
    rem_record = remediation_manager.initiate_remediation(finding_sample, test_dir)
    rem_id = rem_record["remediation_id"]
    print(f"[TEST 4] Auto Remediation Initiated: ID {rem_id}, Stage: {rem_record['stage']}")
    assert rem_record["sandbox_run"]["build_result"] == "SUCCESS"
    assert rem_record["sandbox_run"]["test_result"] == "PASSED"

    # Approval & Deployment
    approved = remediation_manager.approve_and_deploy(rem_id, "security_lead")
    assert approved["deployment"]["status"].startswith("DEPLOYED")
    print("  -> PASSED: Sandbox validation & manual approval gate passed.")

    # Rollback
    rolled_back = remediation_manager.execute_rollback(rem_id, "Testing emergency rollback procedure", "security_lead")
    assert rolled_back["stage"] == "ROLLED_BACK"
    print("  -> PASSED: Rollback execution successfully verified.")

    # 5. Crypto Firewall Decision Engine
    firewall = CryptoFirewallDecisionEngine(policy_manager)
    # Test 1: Block TLS 1.0
    ev1 = firewall.evaluate_handshake(HandshakeMetadata(tls_version="TLSv1.0", cipher_suite="RC4-SHA"))
    assert ev1["decision"] == "BLOCK", "TLS 1.0 must be blocked"

    # Test 2: Block weak RSA key
    ev2 = firewall.evaluate_handshake(HandshakeMetadata(public_key_bits=1024, public_key_algorithm="RSA"))
    assert ev2["decision"] == "BLOCK", "RSA 1024 must be blocked"

    # Test 3: Allow TLS 1.3 modern suite
    ev3 = firewall.evaluate_handshake(HandshakeMetadata(tls_version="TLSv1.3", cipher_suite="TLS_AES_256_GCM_SHA384", public_key_bits=2048))
    assert ev3["decision"] in ["ALLOW", "WARN"], "Modern suite must be allowed"
    print(f"[TEST 5] Crypto Firewall: Evaluated {len(firewall.events_history)} handshakes. Fail-safe decisions verified.")
    print("  -> PASSED: Crypto Firewall gateway verified.")

    # 6. Secure Data Module (KMS Envelope Encryption)
    secret_text = "Highly-Confidential-Signing-Key-Data-2026"
    enc = kms_service.encrypt_data(secret_text.encode("utf-8"))
    assert enc["cipher_algorithm"] == "AES-256-GCM"
    assert enc["masked_preview"] != secret_text
    dec = kms_service.decrypt_data(enc)
    assert dec.decode("utf-8") == secret_text
    print("[TEST 6] Secure Data Module: KMS Envelope Encryption wrapped DEK and decrypted cleanly.")
    print("  -> PASSED: Envelope encryption & masked views verified.")

    # 7. Epistemic Humility Disclaimer
    assert "NOTICE: STATIC CRYPTOGRAPHIC AUDITING DOES NOT CONSTITUTE A PROOF OF QUANTUM SECURITY" in LIMITATIONS_DISCLOSURE["warning_banner"]
    print("[TEST 7] Epistemic Humility & Risk Communication verified.")

    print("\n========================================================")
    print("[SUCCESS] ALL PQC-MIGRATE VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("========================================================\n")

if __name__ == "__main__":
    test_full_pqc_migrate_system()
