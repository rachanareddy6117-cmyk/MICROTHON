import os
import base64
import secrets
from typing import Tuple, Dict, Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from ..config import settings

class EnvelopeEncryptionService:
    """
    Implements production Envelope Encryption for sensitive data.
    - Generates 256-bit AES Data Encryption Keys (DEKs).
    - Encrypts payload with AES-256-GCM.
    - Wraps DEK using Master Key Encryption Key (KEK).
    - Generates safe masked representations for low-privilege access.
    - Never stores raw keys.
    """
    def __init__(self):
        # Simulated or hardware KMS master key (32 bytes)
        raw_master = bytes.fromhex(settings.KMS_MASTER_KEY_HEX)
        if len(raw_master) != 32:
            raw_master = raw_master.ljust(32, b"\x00")[:32]
        self.master_kek = raw_master
        self.kms_key_id = settings.KMS_MASTER_KEY_ID

    def encrypt_data(self, plaintext: bytes, classification: str = "CONFIDENTIAL") -> Dict[str, str]:
        # 1. Generate ephemeral DEK (32 bytes = 256 bits)
        dek = secrets.token_bytes(32)
        nonce_iv = secrets.token_bytes(12)
        
        # 2. Encrypt payload with DEK using AES-256-GCM
        aesgcm_dek = AESGCM(dek)
        ciphertext_and_tag = aesgcm_dek.encrypt(nonce_iv, plaintext, associated_data=classification.encode())
        
        ciphertext = ciphertext_and_tag[:-16]
        tag = ciphertext_and_tag[-16:]
        
        # 3. Wrap DEK with Master KEK
        kek_iv = secrets.token_bytes(12)
        aesgcm_kek = AESGCM(self.master_kek)
        wrapped_dek_full = aesgcm_kek.encrypt(kek_iv, dek, associated_data=b"DEK_WRAP")
        wrapped_dek_blob = kek_iv + wrapped_dek_full

        # 4. Generate masked preview (e.g. for API keys or certificates)
        pt_str = plaintext.decode("utf-8", errors="ignore")
        if len(pt_str) > 8:
            masked = pt_str[:4] + "*" * (len(pt_str) - 8) + pt_str[-4:]
        else:
            masked = "********"

        return {
            "encrypted_data_base64": base64.b64encode(ciphertext).decode(),
            "encrypted_dek_base64": base64.b64encode(wrapped_dek_blob).decode(),
            "nonce_iv_base64": base64.b64encode(nonce_iv).decode(),
            "tag_mac_base64": base64.b64encode(tag).decode(),
            "kms_key_id": self.kms_key_id,
            "cipher_algorithm": "AES-256-GCM",
            "masked_preview": masked
        }

    def decrypt_data(self, enc_dict: Dict[str, str], classification: str = "CONFIDENTIAL") -> bytes:
        ciphertext = base64.b64decode(enc_dict["encrypted_data_base64"])
        wrapped_dek_blob = base64.b64decode(enc_dict["encrypted_dek_base64"])
        nonce_iv = base64.b64decode(enc_dict["nonce_iv_base64"])
        tag = base64.b64decode(enc_dict["tag_mac_base64"])

        # 1. Unwrap DEK using Master KEK
        kek_iv = wrapped_dek_blob[:12]
        wrapped_dek = wrapped_dek_blob[12:]
        aesgcm_kek = AESGCM(self.master_kek)
        dek = aesgcm_kek.decrypt(kek_iv, wrapped_dek, associated_data=b"DEK_WRAP")

        # 2. Decrypt data using DEK
        aesgcm_dek = AESGCM(dek)
        plaintext = aesgcm_dek.decrypt(nonce_iv, ciphertext + tag, associated_data=classification.encode())
        return plaintext

kms_service = EnvelopeEncryptionService()
