from fastapi import APIRouter
from typing import List, Dict, Any
from ...remediation.workflow import remediation_manager

router = APIRouter(prefix="/investigations", tags=["Investigations"])

@router.get("/")
def list_investigations():
    return [r["investigation"] for r in remediation_manager.remediation_pipeline.values()]
