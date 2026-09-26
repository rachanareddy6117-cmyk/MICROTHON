from fastapi import APIRouter
from typing import List, Dict, Any
from .scans import SCANS_STORE

router = APIRouter(prefix="/findings", tags=["Cryptographic Findings"])

@router.get("/")
def list_all_findings(category: str = None, vulnerability: str = None):
    all_findings = []
    for s in SCANS_STORE.values():
        for f in s.findings:
            if category and f.get("category") != category:
                continue
            if vulnerability and f.get("vulnerability_level") != vulnerability:
                continue
            all_findings.append(f)
    return all_findings
