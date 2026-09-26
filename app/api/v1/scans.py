import os
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from ...agents.orchestrator import agent_engine

router = APIRouter(prefix="/scans", tags=["Scans & Agentic Execution"])
SCANS_STORE = {}

class ScanTriggerRequest(BaseModel):
    target_path: str
    repo_name: Optional[str] = "Core-Workload"

@router.post("/")
def trigger_agentic_scan(req: ScanTriggerRequest):
    if not os.path.exists(req.target_path):
        raise HTTPException(status_code=404, detail=f"Target path '{req.target_path}' does not exist.")
    
    state = agent_engine.execute_workflow(req.target_path, req.repo_name)
    SCANS_STORE[state.scan_id] = state
    return {
        "scan_id": state.scan_id,
        "status": state.current_phase,
        "total_findings": len(state.findings),
        "agility_score": state.risk_metrics.get("crypto_agility_score", 100),
        "hndl_index": state.risk_metrics.get("hndl_exposure_index", 0),
        "verification_status": state.verification_status
    }

@router.get("/")
def list_scans():
    return [
        {
            "scan_id": s.scan_id,
            "status": s.current_phase,
            "findings_count": len(s.findings),
            "agility_score": s.risk_metrics.get("crypto_agility_score")
        } for s in SCANS_STORE.values()
    ]

@router.get("/{scan_id}")
def get_scan_details(scan_id: str):
    if scan_id not in SCANS_STORE:
        raise HTTPException(status_code=404, detail="Scan ID not found.")
    return SCANS_STORE[scan_id]
