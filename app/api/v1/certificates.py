from fastapi import APIRouter
from typing import List, Dict, Any
from .scans import SCANS_STORE

router = APIRouter(prefix="/certificates", tags=["Certificate Inventory & Revocation"])

@router.get("/")
def list_certificates():
    certs = []
    for s in SCANS_STORE.values():
        for f in s.findings:
            if f["source_type"] == "certificate":
                certs.append(f)
    return certs
