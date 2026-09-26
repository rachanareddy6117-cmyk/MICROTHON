from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from .scans import SCANS_STORE

router = APIRouter(prefix="/agents", tags=["Agent Orchestrator & State"])

@router.get("/logs/{scan_id}")
def get_agent_logs(scan_id: str):
    if scan_id not in SCANS_STORE:
        raise HTTPException(status_code=404, detail="Scan not found.")
    return SCANS_STORE[scan_id].execution_logs
