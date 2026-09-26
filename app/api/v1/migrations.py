from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from .scans import SCANS_STORE

router = APIRouter(prefix="/migrations", tags=["Migration Planning"])

@router.get("/plan/{scan_id}")
def get_plan(scan_id: str):
    if scan_id not in SCANS_STORE:
        raise HTTPException(status_code=404, detail="Scan not found.")
    return SCANS_STORE[scan_id].migration_plan
