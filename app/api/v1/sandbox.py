from fastapi import APIRouter
from typing import List, Dict, Any
from ...sandbox.runner import sandbox_runner

router = APIRouter(prefix="/sandbox", tags=["Sandbox Validation"])

@router.get("/status")
def get_sandbox_status():
    return {
        "status": "READY",
        "container_isolation": "ENABLED",
        "zero_regression_scanner": "ACTIVE"
    }
