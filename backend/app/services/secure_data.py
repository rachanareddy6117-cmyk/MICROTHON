from __future__ import annotations

from typing import Any, Dict, List


class SecureDataModule:
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def create_record(self, *, organization_id: str, data_type: str, payload: str, classification: str) -> Dict[str, Any]:
        record = {
            "organization_id": organization_id,
            "data_type": data_type,
            "payload": payload[:10] + "***",
            "classification": classification,
            "encrypted_at_rest": True,
            "encrypted_in_transit": True,
            "role_based_access": ["admin", "security-lead"],
            "masked_view": "***",
        }
        self._store[organization_id] = record
        return record

    def access_policy(self, user_role: str) -> Dict[str, Any]:
        return {
            "user_role": user_role,
            "allowed": user_role in {"admin", "security-lead", "auditor"},
            "requires_mfa": user_role in {"admin", "security-lead"},
            "masked_view": user_role != "admin",
        }

    def list_records(self) -> List[Dict[str, Any]]:
        return list(self._store.values())
