from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class AuditEntry:
    user: str
    agent: str
    timestamp: str
    resource: str
    action: str
    old_state: Dict[str, Any]
    new_state: Dict[str, Any]
    approval: str
    result: str


class AuditLogger:
    def __init__(self) -> None:
        self.entries: List[AuditEntry] = []

    def record(
        self,
        *,
        user: str,
        agent: str,
        resource: str,
        action: str,
        old_state: Dict[str, Any] | None = None,
        new_state: Dict[str, Any] | None = None,
        approval: str = "pending",
        result: str = "success",
    ) -> AuditEntry:
        entry = AuditEntry(
            user=user,
            agent=agent,
            timestamp=datetime.now(timezone.utc).isoformat(),
            resource=resource,
            action=action,
            old_state=old_state or {},
            new_state=new_state or {},
            approval=approval,
            result=result,
        )
        self.entries.append(entry)
        return entry

    def list_recent(self, limit: int = 20) -> List[Dict[str, Any]]:
        return [entry.__dict__ for entry in self.entries[-limit:]]
