from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.audit import AuditLog

async def record_audit_event(
    session: AsyncSession,
    user: str,
    action: str,
    resource: str,
    agent: Optional[str] = None,
    old_state: Optional[Dict[str, Any]] = None,
    new_state: Optional[Dict[str, Any]] = None,
    approval: Optional[str] = None,
    result: str = "SUCCESS",
    client_ip: Optional[str] = None
) -> AuditLog:
    log_entry = AuditLog(
        user=user,
        agent=agent,
        timestamp=datetime.now(timezone.utc),
        resource=resource,
        action=action,
        old_state=old_state,
        new_state=new_state,
        approval=approval,
        result=result,
        client_ip=client_ip
    )
    session.add(log_entry)
    await session.commit()
    return log_entry
