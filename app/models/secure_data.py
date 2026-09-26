import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey
from ..database import Base

class EncryptedVaultRecord(Base):
    __tablename__ = "encrypted_vault_records"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    record_label = Column(String(255), nullable=False)
    data_classification = Column(String(50), default="CONFIDENTIAL")  # CONFIDENTIAL, RESTRICTED, PUBLIC
    
    # Envelope encryption fields: never store raw plaintext or raw keys
    encrypted_data_base64 = Column(Text, nullable=False)
    encrypted_dek_base64 = Column(Text, nullable=False)  # Data Encryption Key wrapped by KMS KEK
    nonce_iv_base64 = Column(String(64), nullable=False)
    tag_mac_base64 = Column(String(64), nullable=False)
    kms_key_id = Column(String(100), nullable=False)
    cipher_algorithm = Column(String(50), default="AES-256-GCM")
    
    # Masked representation for low-privilege viewers
    masked_preview = Column(String(255), default="************")
    
    created_by = Column(String(100), default="system")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class KmsKeyEnvelope(Base):
    __tablename__ = "kms_key_envelopes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    key_alias = Column(String(100), unique=True, nullable=False)
    kms_provider = Column(String(50), default="local_simulated")
    key_status = Column(String(20), default="ACTIVE")
    algorithm = Column(String(50), default="AES-256-GCM")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
