from __future__ import annotations

import uuid
from typing import Any, Dict, List
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.schemas import (
    EvaluationRunCreate,
    FirewallDecisionRequest,
    FirewallPolicyRule,
    ProjectCreate,
    RepositoryCreate,
    ScanPayload,
)
from backend.app.security import secure_headers
from backend.app.services.agent_orchestrator import AgentOrchestrator
from backend.app.services.audit import AuditLogger
from backend.app.services.crypto_scanner import detect_crypto_usage
from backend.app.services.demo_upload_samples import project_specification_pdf, software_bundle_zip
from backend.app.services.firewall import CryptoFirewallGateway
from backend.app.services.project_scanner import build_project_scan_result
from backend.app.services.repository_scanner import correlate_runtime_issue
from backend.app.services.secure_data import SecureDataModule
from backend.app.services.upload_scanner import scan_upload
from backend.app.services.sample_database import list_sample_data

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.agent_orchestrator = AgentOrchestrator()
app.state.crypto_firewall = CryptoFirewallGateway()
app.state.audit_logger = AuditLogger()
app.state.secure_data = SecureDataModule()
app.state.scan_reports = {}
app.state.firewall_policies = {}
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"


@app.middleware("http")
async def add_security_headers(request, call_next):
    if request.method == "POST" and request.url.path in {
        f"{settings.api_v1_prefix}/ingest",
        f"{settings.api_v1_prefix}/scans/upload",
    }:
        content_length = request.headers.get("content-length")
        try:
            request_size = int(content_length) if content_length else None
        except ValueError:
            return JSONResponse(status_code=400, content={"detail": "Invalid Content-Length."})
        if request_size is not None and request_size > settings.max_upload_bytes + 1024 * 1024:
            response = JSONResponse(
                status_code=413,
                content={"detail": "Upload request exceeds the configured 10 GiB limit."},
            )
            secure_headers(response)
            return response
    response = await call_next(request)
    secure_headers(response)
    return response


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get(f"{settings.api_v1_prefix}/demo/samples")
async def demo_samples() -> Dict[str, Any]:
    return list_sample_data()


@app.get(f"{settings.api_v1_prefix}/demo/sample-files/project.pdf", include_in_schema=False)
async def demo_project_sample_file() -> Response:
    return Response(
        content=project_specification_pdf(),
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="pqc-demo-project-spec.pdf"'},
    )


@app.get(f"{settings.api_v1_prefix}/demo/sample-files/software.zip", include_in_schema=False)
async def demo_software_sample_file() -> Response:
    return Response(
        content=software_bundle_zip(),
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="pqc-demo-software.zip"'},
    )


@app.get("/", include_in_schema=False)
async def frontend() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post(f"{settings.api_v1_prefix}/projects")
async def create_project(payload: ProjectCreate):
    app.state.audit_logger.record(user="analyst", agent="DiscoveryAgent", resource="project", action="create", old_state={}, new_state={"name": payload.name}, approval="approved", result="success")
    return {"id": "project-demo-1", "name": payload.name, "status": "created"}


@app.post(f"{settings.api_v1_prefix}/projects/scan")
async def scan_project(payload: dict) -> Dict[str, Any]:
    result = build_project_scan_result(payload.get("spec_text", ""))
    app.state.audit_logger.record(user="analyst", agent="DiscoveryAgent", resource="project", action="scan", old_state={}, new_state=result, approval="approved", result="success")
    return result


@app.post(f"{settings.api_v1_prefix}/repositories")
async def create_repository(payload: RepositoryCreate):
    return {"id": "repo-demo-1", "project_id": payload.project_id, "name": payload.name, "status": "registered"}


@app.post(f"{settings.api_v1_prefix}/scans")
async def create_scan(payload: ScanPayload):
    return {
        "id": str(uuid.uuid4()),
        "repository_id": payload.repository_id,
        "scan_type": payload.scan_type,
        "status": "not_queued",
        "detail": "A persistent database/worker integration is required to enqueue background scans.",
    }


@app.post(f"{settings.api_v1_prefix}/scans/crypto")
async def crypto_scan(payload: ScanPayload):
    summary = {"detected_algorithms": detect_crypto_usage(payload.summary.get("source_text", "") if payload.summary else "")}
    return {"scanner": "crypto", "status": "completed", "summary": summary}


@app.post(f"{settings.api_v1_prefix}/findings")
async def create_finding() -> Dict[str, Any]:
    raise HTTPException(status_code=501, detail="Findings are created from completed scanner evidence; manual persistence is not configured.")


@app.get(f"{settings.api_v1_prefix}/crypto-assets")
async def list_crypto_assets() -> List[Dict[str, Any]]:
    return []


@app.get(f"{settings.api_v1_prefix}/dependencies")
async def list_dependencies() -> List[Dict[str, Any]]:
    return []


@app.get(f"{settings.api_v1_prefix}/certificates")
async def list_certificates() -> List[Dict[str, Any]]:
    return []


@app.get(f"{settings.api_v1_prefix}/agents")
async def list_agents() -> Dict[str, Any]:
    return {"status": "idle", "agents": [
        "DiscoveryAgent", "EvidenceAgent", "RiskAgent", "DependencyAgent",
        "MigrationAgent", "PatchAgent", "SandboxAgent", "VerificationAgent",
        "FirewallAgent", "GovernanceAgent",
    ], "active_run": None}


@app.post(f"{settings.api_v1_prefix}/investigations")
async def create_investigation() -> Dict[str, Any]:
    raise HTTPException(status_code=501, detail="Investigation persistence requires a completed finding and configured database.")


@app.post(f"{settings.api_v1_prefix}/remediations")
async def create_remediation() -> Dict[str, Any]:
    raise HTTPException(status_code=501, detail="Remediation jobs require a verified finding and configured isolated sandbox.")


@app.get(f"{settings.api_v1_prefix}/sandbox")
async def sandbox_status() -> Dict[str, Any]:
    return {"sandbox_required": True, "status": "not_configured", "production_changes_allowed": False}


@app.post(f"{settings.api_v1_prefix}/migrations")
async def create_migration_plan() -> Dict[str, Any]:
    raise HTTPException(status_code=501, detail="Migration plan persistence is not configured.")


@app.get(f"{settings.api_v1_prefix}/crypto-agility")
async def crypto_agility() -> Dict[str, Any]:
    return {"status": "INSUFFICIENT_EVIDENCE", "score": None, "evidence": [], "summary": "A repository scan and validated architecture evidence are required."}


@app.post(f"{settings.api_v1_prefix}/firewall/policies")
async def create_firewall_policy(payload: FirewallPolicyRule):
    policy_id = str(uuid.uuid4())
    record = {"id": policy_id, "status": "draft", "policy": payload.model_dump(), "deployed": False}
    app.state.firewall_policies[policy_id] = record
    app.state.audit_logger.record(user="demo-user", agent="FirewallAgent", resource="firewall_policy", action="create_draft", old_state={}, new_state=record, approval="required", result="draft")
    return record


@app.get(f"{settings.api_v1_prefix}/firewall/policies/{{policy_id}}")
async def get_firewall_policy(policy_id: str) -> Dict[str, Any]:
    policy = app.state.firewall_policies.get(policy_id)
    if policy is None:
        raise HTTPException(status_code=404, detail="Firewall policy draft was not found.")
    return policy


@app.post(f"{settings.api_v1_prefix}/firewall/events")
async def firewall_event(request: FirewallDecisionRequest):
    decision = app.state.crypto_firewall.evaluate(request.model_dump())
    app.state.audit_logger.record(user="security-lead", agent="FirewallAgent", resource="firewall_event", action="evaluate", old_state={}, new_state=request.model_dump(), approval="review" if decision["requires_approval"] else "approved", result=decision["decision"])
    return {"decision": decision["decision"], "reason": decision["reason"], "requires_approval": decision["requires_approval"]}


@app.post(f"{settings.api_v1_prefix}/ci/scan")
async def ci_scan(payload: dict) -> Dict[str, Any]:
    diff = str(payload.get("diff", payload.get("source_text", "")))
    file_name = str(payload.get("file", "not provided"))
    prohibited = {"MD5", "SHA-1", "3DES", "DES", "RC4"}
    evidence = []
    for line_number, line in enumerate(diff.splitlines(), start=1):
        if not line.startswith("+") or line.startswith("+++"):
            continue
        added_line = line[1:]
        algorithms = detect_crypto_usage(added_line)
        if algorithms:
            evidence.append({
                "file": file_name,
                "line": line_number,
                "algorithms": algorithms,
                "evidence": added_line.strip()[:500],
            })
    matched_algorithms = sorted({
        algorithm for item in evidence for algorithm in item["algorithms"]
    })
    violations = sorted(prohibited.intersection(matched_algorithms))
    decision = "BLOCK" if violations else "REVIEW" if matched_algorithms else "PASS"
    return {
        "decision": decision,
        "finding": "New cryptographic API/algorithm references were observed in added diff lines." if evidence else "No supported cryptographic pattern was observed in added diff lines.",
        "file": file_name,
        "line": evidence[0]["line"] if evidence else None,
        "algorithm": matched_algorithms,
        "policy": {"blocked_algorithms": sorted(prohibited)},
        "evidence": evidence,
        "recommended_fix": "Review the matched lines against the approved crypto policy and compatibility requirements." if evidence else "No fix recommendation; no supported match was found.",
        "limitations": ["Line numbers refer to the submitted diff, not verified repository coordinates.", "This endpoint does not compare against a persisted inventory baseline."],
    }


@app.post(f"{settings.api_v1_prefix}/secure-data")
async def create_secure_data():
    raise HTTPException(
        status_code=503,
        detail="Secure data is disabled until a production KMS/HSM and envelope-encryption storage adapter are configured.",
    )


@app.post(f"{settings.api_v1_prefix}/secure-data/access")
async def secure_data_access() -> Dict[str, Any]:
    raise HTTPException(
        status_code=503,
        detail="Secure data access is disabled until server-side identity and KMS-backed authorization are configured.",
    )


@app.get(f"{settings.api_v1_prefix}/reports")
async def reports() -> Dict[str, Any]:
    return {"summary": {"open_findings": 0, "approved_remediations": 0, "firewall_actions": 0}, "source": "No persisted organization database is configured."}


@app.get(f"{settings.api_v1_prefix}/audit")
async def audit_log() -> List[Dict[str, Any]]:
    return app.state.audit_logger.list_recent(limit=10)


@app.post(f"{settings.api_v1_prefix}/evaluation")
async def create_evaluation(payload: EvaluationRunCreate):
    return {"id": str(uuid.uuid4()), "approach": payload.approach, "status": "received_not_persisted"}


@app.post(f"{settings.api_v1_prefix}/ingest")
@app.post(f"{settings.api_v1_prefix}/scans/upload")
async def ingest_artifact(
    file: UploadFile = File(...),
    hourly_rate_usd: float = Form(default=150, ge=1, le=5000),
    legacy_fix_hours_per_finding: float = Form(default=8, ge=0, le=1000),
    quantum_migration_hours_per_finding: float = Form(default=16, ge=0, le=1000),
    crypto_review_hours_per_finding: float = Form(default=3, ge=0, le=1000),
):
    try:
        result = await scan_upload(file, {
            "hourly_rate_usd": hourly_rate_usd,
            "legacy_fix_hours_per_finding": legacy_fix_hours_per_finding,
            "quantum_migration_hours_per_finding": quantum_migration_hours_per_finding,
            "crypto_review_hours_per_finding": crypto_review_hours_per_finding,
        })
        result["hash"] = result["sha256"]
        result["profile"] = result["report"]["project_profile"]
        result["assessment_status"] = result["report"]["classification"]
        app.state.scan_reports[result["scan_id"]] = result
        if len(app.state.scan_reports) > 100:
            del app.state.scan_reports[next(iter(app.state.scan_reports))]
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post(f"{settings.api_v1_prefix}/deployments/report-issue")
async def report_deployment_issue(payload: dict) -> Dict[str, Any]:
    issue = str(payload.get("issue", "")).strip()
    repository_url = str(payload.get("repository_url", "")).strip()
    if not issue:
        raise HTTPException(status_code=422, detail="A deployment issue description is required.")
    if repository_url and not repository_url.startswith(("https://github.com/", "https://gitlab.com/")):
        raise HTTPException(status_code=422, detail="Repository URL must use GitHub or GitLab HTTPS.")
    correlations = correlate_runtime_issue(issue, {
        "repository_url": repository_url or "not provided",
        "source_file": "not established",
        "dependency": "not established",
        "service": str(payload.get("service", "not specified")),
    })
    app.state.audit_logger.record(
        user=str(payload.get("reporter", "participant")),
        agent="DeploymentHealth",
        resource="deployment_issue",
        action="report",
        old_state={},
        new_state={"repository_url": repository_url, "issue": issue[:2000]},
        approval="not_required",
        result="received",
    )
    return {
        "status": "received",
        "issue_id": str(uuid.uuid4()),
        "repository_url": repository_url or None,
        "correlation": correlations,
        "uncertainties": [
            "No repository connector is configured to verify source locations.",
            "Deployment telemetry was not supplied; dependency and service relationships remain unverified.",
        ],
    }


@app.post(f"{settings.api_v1_prefix}/projects/{{project_id}}/risk")
async def project_risk(project_id: str, payload: dict) -> Dict[str, Any]:
    check = build_project_scan_result(str(payload.get("spec_text", "")))
    return {"project_id": project_id, **check}


@app.post(f"{settings.api_v1_prefix}/deployments/scan")
async def deployment_scan(payload: dict) -> Dict[str, Any]:
    runtime_error = str(payload.get("runtime_error", "")).strip()
    if not runtime_error:
        raise HTTPException(status_code=422, detail="A runtime issue or deployment log excerpt is required.")
    return {
        "deployment_id": payload.get("deployment_id", "not provided"),
        "status": "review",
        "runtime_error": runtime_error,
        "correlation": correlate_runtime_issue(runtime_error, {
            "source_file": "not established",
            "dependency": "not established",
            "service": str(payload.get("service", "not established")),
        }),
        "uncertainties": ["No deployment telemetry connector was used.", "Source file and dependency were not verified."],
    }


@app.websocket("/ws/events")
async def ws_events(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json({"type": "scan_status", "status": "running", "message": "Crypto analysis in progress"})
            break
    except WebSocketDisconnect:
        pass


@app.get("/api/v1/firewall")
async def firewall_summary() -> Dict[str, Any]:
    return {"status": "ok", "decisions": ["ALLOW", "MONITOR", "WARN", "REVIEW", "BLOCK"]}


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
