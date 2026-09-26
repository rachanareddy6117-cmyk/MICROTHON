import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from ...scanners.crypto_scanner import crypto_scanner

router = APIRouter(prefix="/ci", tags=["CI/CD Guard"])

class CIScanRequest(BaseModel):
    repository_path: str
    commit_sha: str = "HEAD"
    branch: str = "main"

@router.post("/scan")
def ci_scan(req: CIScanRequest):
    """
    CI/CD Guard endpoint:
    Detects newly introduced crypto in commits/PRs.
    Returns: PASS, REVIEW, or BLOCK.
    """
    if not os.path.exists(req.repository_path):
        raise HTTPException(status_code=404, detail="Repository path not found.")

    findings = crypto_scanner.scan_path(req.repository_path)
    
    # Decision logic
    has_hardcoded_keys = any(f["category"] == "HARDCODED_SECRET" for f in findings)
    has_deprecated = any(f["vulnerability_level"] == "MEDIUM_DEPRECATED" for f in findings)
    has_shor_critical = any(f["vulnerability_level"] == "CRITICAL_SHOR" for f in findings)

    decision = "PASS"
    policy_violation = "Compliant with baseline PQC policy."

    if has_hardcoded_keys:
        decision = "BLOCK"
        policy_violation = "Hardcoded private cryptographic keys detected in code commit!"
    elif has_deprecated:
        decision = "BLOCK"
        policy_violation = "Classically broken crypto (MD5/SHA-1/3DES) introduced!"
    elif has_shor_critical:
        decision = "REVIEW"
        policy_violation = "Classical asymmetric primitives (RSA/ECDSA) detected. Review against PQC agility guidelines."

    details = []
    for f in findings:
        details.append({
            "finding_id": f["id"],
            "file": f["file_path"],
            "line": f["line_number"],
            "algorithm": f["algorithm"],
            "policy": f["vulnerability_level"],
            "evidence": f["code_snippet"],
            "recommended_fix": f.get("nist_replacement", "Use agility registry provider")
        })

    return {
        "status": decision,
        "policy_message": policy_violation,
        "total_crypto_detected": len(findings),
        "details": details
    }
