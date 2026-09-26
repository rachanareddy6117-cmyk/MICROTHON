from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from typing import Dict, Any
from .scans import SCANS_STORE
from ...core.disclaimer import LIMITATIONS_DISCLOSURE

router = APIRouter(prefix="/reports", tags=["Reports & CBOM Exports"])

@router.get("/cbom/{scan_id}")
def get_cbom(scan_id: str):
    if scan_id not in SCANS_STORE:
        raise HTTPException(status_code=404, detail="Scan not found.")
    s = SCANS_STORE[scan_id]
    
    components = []
    for f in s.findings:
        components.append({
            "type": "cryptographic-asset",
            "name": f["algorithm"],
            "description": f["threat_vector"],
            "cryptoProperties": {
                "assetType": f["category"],
                "algorithmProperties": {
                    "parameterSetIdentifier": f.get("key_size_or_curve", "standard"),
                    "nistStandardReplacement": f.get("nist_replacement")
                }
            }
        })
    return JSONResponse(content={
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "disclaimer": LIMITATIONS_DISCLOSURE["warning_banner"],
        "components": components
    })
