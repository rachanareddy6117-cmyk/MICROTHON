from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(prefix="/audit", tags=["Immutable Audit Trail"])
AUDIT_TRAIL = []

def record_audit(user: str, action: str, resource: str, result: str = "SUCCESS"):
    from datetime import datetime, timezone
    AUDIT_TRAIL.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": user,
        "action": action,
        "resource": resource,
        "result": result
    })

@router.get("/")
def get_audit_trail():
    return AUDIT_TRAIL
