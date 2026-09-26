import os
import sys
from starlette.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

def test_api_endpoints():
    print("\n========================================================")
    print("VERIFYING PQC-MIGRATE REST API ENDPOINTS")
    print("========================================================")

    # 1. Health endpoint
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "HEALTHY"
    print("[PASSED] GET /health")

    # 2. Crypto Agility Registry
    res = client.get("/api/v1/crypto-agility/registry")
    assert res.status_code == 200
    assert "ML-KEM-768" in res.json()["key_encapsulation"]
    print("[PASSED] GET /api/v1/crypto-agility/registry")

    # 3. Defensive Crypto Firewall Inspection
    firewall_payload = {
        "client_ip": "192.168.1.100",
        "endpoint": "/api/v1/transactions",
        "tls_version": "TLSv1.0",
        "cipher_suite": "RC4-SHA",
        "public_key_bits": 1024
    }
    res = client.post("/api/v1/firewall/inspect", json=firewall_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["decision"] == "BLOCK"
    print(f"[PASSED] POST /api/v1/firewall/inspect -> Blocked legacy TLS 1.0 (Decision: {data['decision']})")

    # 4. CI/CD Guard
    adv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "adversarial_repo")
    ci_payload = {
        "repository_path": adv_dir,
        "commit_sha": "abc1234",
        "branch": "feature/crypto"
    }
    res = client.post("/api/v1/ci/scan", json=ci_payload)
    assert res.status_code == 200
    ci_data = res.json()
    assert ci_data["status"] in ["REVIEW", "BLOCK"]
    print(f"[PASSED] POST /api/v1/ci/scan -> Status: {ci_data['status']} ({ci_data['total_crypto_detected']} primitives detected)")

    # 5. Secure Data Envelope Encryption
    sec_payload = {
        "label": "Master Root CA Private Key",
        "plaintext_secret": "SuperSecretCertificateAuthorityKeyBytes2026",
        "classification": "CONFIDENTIAL"
    }
    res = client.post("/api/v1/secure-data/store", json=sec_payload)
    assert res.status_code == 200
    sec_data = res.json()
    assert sec_data["cipher_algorithm"] == "AES-256-GCM"
    assert sec_data["masked_preview"] != sec_payload["plaintext_secret"]
    print(f"[PASSED] POST /api/v1/secure-data/store -> KMS Envelope Encrypted (Masked: {sec_data['masked_preview']})")

    # 6. Evaluation Posture Metrics
    res = client.get("/api/v1/evaluation/metrics")
    assert res.status_code == 200
    print(f"[PASSED] GET /api/v1/evaluation/metrics -> {res.json()['cryptographic_agility_index']}/100")

    print("\n========================================================")
    print("[SUCCESS] ALL REST API ENDPOINTS VERIFIED!")
    print("========================================================\n")

if __name__ == "__main__":
    test_api_endpoints()
