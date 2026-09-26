from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List
from ...core.kms import kms_service
from ...core.security import get_current_user

router = APIRouter(prefix="/secure-data", tags=["Secure Data & KMS Envelope Encryption"])
VAULT_STORE = {}

class VaultStoreRequest(BaseModel):
    label: str
    plaintext_secret: str
    classification: str = "CONFIDENTIAL"

@router.post("/store")
def store_secret(req: VaultStoreRequest, user: dict = Depends(get_current_user)):
    """
    Encrypts plaintext with AES-256-GCM envelope encryption wrapped by KMS.
    Never stores raw private keys or raw plaintext.
    """
    enc_data = kms_service.encrypt_data(req.plaintext_secret.encode("utf-8"), req.classification)
    record_id = f"SEC-{len(VAULT_STORE) + 1}"
    record = {
        "id": record_id,
        "label": req.label,
        "classification": req.classification,
        "created_by": user["username"],
        **enc_data
    }
    VAULT_STORE[record_id] = record
    return {
        "id": record_id,
        "label": req.label,
        "cipher_algorithm": record["cipher_algorithm"],
        "kms_key_id": record["kms_key_id"],
        "masked_preview": record["masked_preview"]
    }

@router.get("/")
def list_vault_records(user: dict = Depends(get_current_user)):
    """Masked view for standard analysts."""
    is_lead = user["role"] == "security_lead"
    results = []
    for r in VAULT_STORE.values():
        results.append({
            "id": r["id"],
            "label": r["label"],
            "classification": r["classification"],
            "masked_preview": r["masked_preview"] if not is_lead else "[REDACTED UNTIL DECRYPT CALL]"
        })
    return results

@router.get("/{record_id}/decrypt")
def decrypt_secret(record_id: str, user: dict = Depends(get_current_user)):
    """Strict main-lead role-based access to decrypt envelope."""
    if user["role"] != "security_lead":
        raise HTTPException(status_code=403, detail="Decryption requires 'security_lead' role.")
    if record_id not in VAULT_STORE:
        raise HTTPException(status_code=404, detail="Record not found.")
    
    r = VAULT_STORE[record_id]
    plaintext = kms_service.decrypt_data(r, r["classification"])
    return {
        "id": record_id,
        "label": r["label"],
        "decrypted_plaintext": plaintext.decode("utf-8", errors="ignore")
    }
