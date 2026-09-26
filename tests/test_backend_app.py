from fastapi.testclient import TestClient
import pymupdf

from backend.app.main import app
from backend.app.services.crypto_scanner import detect_crypto_usage
from backend.app.services.project_scanner import extract_project_risk

client = TestClient(app)


def test_health_endpoint():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_frontend_and_static_assets_are_served():
    response = client.get('/')
    assert response.status_code == 200
    assert "PQC-Migrate" in response.text
    assert "fonts.googleapis.com" not in response.text
    assert "style-src 'self' 'unsafe-inline'" in response.headers["content-security-policy"]

    assets_response = client.get('/static/app.js')
    assert assets_response.status_code == 200
    assert "renderDashboard" in assets_response.text


def test_project_scan_does_not_invent_missing_fields():
    response = client.post('/api/v1/projects/scan', json={'spec_text': ''})
    assert response.status_code == 200
    result = response.json()
    assert result['status'] == 'insufficient_evidence'
    assert result['profile']['scope'] == 'unknown'
    assert result['profile']['technology'] == []
    assert result['profile']['vendors'] == []


def test_pdf_ingestion_extracts_project_fields_without_executing_content():
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text(
        (72, 72),
        "Scope: Payments API migration\n"
        "Technology: Java, TLS\n"
        "Timeline: Q4\n"
        "Budget: medium\n"
        "Vendors: OpenSSL\n"
        "Dependencies: Redis\n"
        "Security requirements: TLS 1.3",
    )
    pdf_bytes = document.tobytes()
    document.close()

    response = client.post(
        "/api/v1/ingest",
        files={"file": ("project.pdf", pdf_bytes, "application/pdf")},
    )

    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "completed"
    assert result["profile"]["scope"] == "Payments API migration"
    assert result["profile"]["technology"] == ["Java", "TLS"]
    assert result["profile"]["dependencies"] == ["Redis"]
    assert result["report"]["cost_analysis"]["status"] == "ESTIMATED"
    assert result["report"]["cost_analysis"]["currency"] == "USD"
    assert result["report"]["cost_analysis"]["cost_range_usd"]["expected"] > 0


def test_zip_scanner_reports_algorithm_evidence_and_redacts_secret_material():
    import io
    import zipfile

    bundle = io.BytesIO()
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "src/crypto.py",
            'cipher = "AES-128-CBC"\n'
            'private_key = "-----BEGIN RSA PRIVATE KEY----- supersecretvalue"\n'
            'signature = "SHA-1"\n'
            'kem = "ML-KEM-768"\n',
        )

    response = client.post(
        "/api/v1/scans/upload",
        files={"file": ("source.zip", bundle.getvalue(), "application/zip")},
    )
    assert response.status_code == 200
    report = response.json()["report"]
    assert {"AES", "RSA", "SHA-1", "ML-KEM"} <= set(report["algorithms"])
    assert report["potential_secret_findings"]
    serialized = response.text
    assert "supersecretvalue" not in serialized
    assert "[REDACTED: possible secret material]" in serialized
    assert report["llm_status"]["configured"] is False


def test_software_zip_returns_static_inventory_cost_and_never_executes_code():
    import io
    import zipfile

    bundle = io.BytesIO()
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("requirements.txt", "cryptography==42.0.0\nrequests>=2.0\n")
        archive.writestr(
            "src/crypto.py",
            'digest = hashlib.md5(payload)\n'
            'key_type = "RSA-2048"\n'
            'cipher = "AES-256-GCM"\n'
            'private_key = "supersecretvalue"\n'
            'raise RuntimeError("must not execute")\n',
        )

    response = client.post(
        "/api/v1/scans/upload",
        files={"file": ("software.zip", bundle.getvalue(), "application/zip")},
        data={
            "hourly_rate_usd": "200",
            "legacy_fix_hours_per_finding": "2",
            "quantum_migration_hours_per_finding": "4",
            "crypto_review_hours_per_finding": "1",
        },
    )

    assert response.status_code == 200
    report = response.json()["report"]
    software = report["software_analysis"]
    assert software["source_files_analyzed"] == 2
    assert software["dependencies_identified"] == 2
    assert set(software["dependency_names"]) == {"cryptography", "requests"}
    assert software["dependency_vulnerability_status"] == "NOT_CHECKED_NO_ADVISORY_FEED_CONFIGURED"
    assert software["build_and_tests"] == "NOT_RUN; uploaded software is never executed"
    assert "RuntimeError" not in response.text
    assert "supersecretvalue" not in response.text
    cost = report["cost_analysis"]
    assert cost["assumptions"]["hourly_rate_usd"] == 200
    assert cost["finding_counts"]["legacy_crypto"] == 1
    assert cost["finding_counts"]["quantum_vulnerable_public_key"] == 1
    assert cost["finding_counts"]["crypto_review"] == 1
    assert cost["total_cost_usd"] == 1800
    assert cost["cost_range_usd"]["expected"] == 1800


def test_zip_scanner_rejects_path_traversal_without_extracting():
    import io
    import zipfile

    bundle = io.BytesIO()
    with zipfile.ZipFile(bundle, "w") as archive:
        archive.writestr("../../outside.py", "RSA")

    response = client.post(
        "/api/v1/scans/upload",
        files={"file": ("unsafe.zip", bundle.getvalue(), "application/zip")},
    )
    assert response.status_code == 400
    assert "unsafe path" in response.json()["detail"]


def test_sample_data_is_served_from_isolated_sample_database():
    response = client.get("/api/v1/demo/samples")
    assert response.status_code == 200
    body = response.json()
    assert "isolated SQLite sample database" == body["database"]
    assert body["crypto_assets"]
    assert "not production data" in body["notice"]


def test_downloadable_demo_inputs_produce_pdf_cost_and_software_analysis():
    project = client.get("/api/v1/demo/sample-files/project.pdf")
    assert project.status_code == 200
    assert project.headers["content-type"].startswith("application/pdf")
    project_scan = client.post(
        "/api/v1/scans/upload",
        files={"file": ("pqc-demo-project-spec.pdf", project.content, "application/pdf")},
    )
    assert project_scan.status_code == 200
    project_report = project_scan.json()["report"]
    assert project_report["project_profile"]["scope"] != "unknown"
    assert project_report["risk"]["quantum"] in {"high", "critical"}
    assert project_report["cost_analysis"]["total_cost_usd"] > 0

    software = client.get("/api/v1/demo/sample-files/software.zip")
    assert software.status_code == 200
    assert software.headers["content-type"].startswith("application/zip")
    software_scan = client.post(
        "/api/v1/scans/upload",
        files={"file": ("pqc-demo-software.zip", software.content, "application/zip")},
    )
    assert software_scan.status_code == 200
    report = software_scan.json()["report"]
    assert report["software_analysis"]["source_files_analyzed"] >= 4
    assert report["software_analysis"]["dependencies_identified"] >= 4
    assert report["cost_analysis"]["total_cost_usd"] > 0
    assert "DEMO_ONLY_NOT_A_REAL_SECRET" not in software_scan.text
    assert "scanner must not execute" not in software_scan.text


def test_firewall_policy_creates_a_reviewable_undepoyed_draft():
    payload = {
        "minimum_tls": "TLS 1.3",
        "allowed_ciphers": ["TLS_AES_256_GCM_SHA384"],
        "blocked_algorithms": ["MD5", "SHA-1"],
        "minimum_rsa_key_size": 3072,
        "approved_providers": ["OpenSSL"],
        "exception_expiry": 30,
    }
    response = client.post("/api/v1/firewall/policies", json=payload)
    assert response.status_code == 200
    draft = response.json()
    assert draft["status"] == "draft"
    assert draft["deployed"] is False
    fetched = client.get(f"/api/v1/firewall/policies/{draft['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["policy"]["minimum_tls"] == "TLS 1.3"


def test_deployment_issue_correlation_does_not_invent_source_or_dependencies():
    response = client.post(
        "/api/v1/deployments/report-issue",
        json={
            "issue": "TLS handshake errors after certificate renewal",
            "repository_url": "https://github.com/example/project",
            "service": "edge-api",
        },
    )
    assert response.status_code == 200
    correlation = response.json()["correlation"]
    assert correlation["source_code"] == "not established"
    assert correlation["dependency"] == "not established"
    assert correlation["service"] == "edge-api"


def test_ci_guard_detects_added_sha1_and_passes_non_crypto_diff():
    block = client.post(
        "/api/v1/ci/scan",
        json={"file": "app.py", "diff": "+digest = hashlib.sha1(payload).digest()"},
    )
    assert block.status_code == 200
    assert block.json()["decision"] == "BLOCK"
    assert block.json()["evidence"][0]["line"] == 1
    assert "sha1" in block.json()["evidence"][0]["evidence"].lower()

    passed = client.post("/api/v1/ci/scan", json={"diff": "+print('hello')"})
    assert passed.status_code == 200
    assert passed.json()["decision"] == "PASS"
    assert passed.json()["evidence"] == []


def test_secure_data_fails_closed_without_kms_integration():
    response = client.post(
        "/api/v1/secure-data",
        json={
            "organization_id": "org",
            "data_type": "report",
            "encrypted_payload": "ciphertext",
            "encryption_metadata": {},
            "classification": "internal",
        },
    )
    assert response.status_code == 503


def test_websocket_stream_emits_scan_status():
    with client.websocket_connect("/ws/events") as websocket:
        event = websocket.receive_json()
    assert event["type"] == "scan_status"
    assert event["status"] == "running"


def test_firewall_rejects_weak_crypto():
    response = client.post(
        '/api/v1/firewall/events',
        json={
            'source': 'gateway',
            'destination': 'payments',
            'service': 'payments-api',
            'tls_version': 'TLS 1.0',
            'cipher': 'RC4-SHA',
            'certificate': 'sha1-rsa',
            'algorithm': 'RSA',
            'reason': 'legacy',
            'risk': 'high',
        },
    )
    assert response.status_code == 200
    assert response.json()['decision'] in {'MONITOR', 'BLOCK', 'WARN'}


def test_crypto_scanner_detects_algorithms():
    text = 'RSA key exchange with SHA-1 signature and TLS 1.2 protocol, plus AES-128 and RC4.'
    algorithms = detect_crypto_usage(text)
    assert 'RSA' in algorithms
    assert 'SHA-1' in algorithms
    assert 'AES' in algorithms


def test_project_scanner_extracts_spec_fields():
    spec = '''
    Scope: Payments API migration
    Technology: Java, TLS, Redis
    Budget: medium
    Timeline: Q4
    Vendors: OpenSSL, Spring
    Risks: RSA certificate usage, legacy TLS policy
    '''
    profile = extract_project_risk(spec)
    assert profile['scope'] == 'Payments API migration'
    assert 'Java' in profile['technology']
    assert profile['budget'] == 'medium'
