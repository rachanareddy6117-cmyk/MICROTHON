from fastapi import APIRouter
from typing import List, Dict, Any
from .scans import SCANS_STORE

router = APIRouter(prefix="/crypto-assets", tags=["Cryptographic Assets Inventory"])

@router.get("/")
def list_crypto_assets():
    assets = []
    for s in SCANS_STORE.values():
        for f in s.findings:
            assets.append({
                "id": f["id"],
                "name": f["algorithm"],
                "category": f["category"],
                "vulnerability": f["vulnerability_level"],
                "location": f["file_path"],
                "nist_standard_replacement": f.get("nist_replacement")
            })
    return assets
