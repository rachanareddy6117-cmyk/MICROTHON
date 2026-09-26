from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from ...remediation.workflow import remediation_manager

router = APIRouter(prefix="/remediations", tags=["Auto Remediation & Approval"])

class RemediationTriggerRequest(BaseModel):
    finding: Dict[str, Any]
    target_repo_dir: str

class ApprovalRequest(BaseModel):
    remediation_id: str
    approver: str = "security_lead"

class RollbackRequest(BaseModel):
    remediation_id: str
    reason: str
    operator: str = "security_lead"

@router.get("/")
def list_remediations():
    return list(remediation_manager.remediation_pipeline.values())

@router.post("/initiate")
def initiate_remediation(req: RemediationTriggerRequest):
    return remediation_manager.initiate_remediation(req.finding, req.target_repo_dir)

@router.post("/approve")
def approve_remediation(req: ApprovalRequest):
    try:
        return remediation_manager.approve_and_deploy(req.remediation_id, req.approver)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/rollback")
def rollback_remediation(req: RollbackRequest):
    try:
        return remediation_manager.execute_rollback(req.remediation_id, req.reason, req.operator)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
