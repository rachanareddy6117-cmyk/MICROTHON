import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean
from ..database import Base

class CertificateInventory(Base):
    __tablename__ = "certificate_inventory"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fingerprint_sha256 = Column(String(64), unique=True, nullable=False)
    subject_dn = Column(String(512), nullable=False)
    issuer_dn = Column(String(512), nullable=False)
    public_key_algorithm = Column(String(100), nullable=False)  # RSA, ECC, Ed25519
    key_size_bits = Column(Integer, nullable=True)
    curve_name = Column(String(100), nullable=True)
    signature_algorithm = Column(String(100), nullable=False)
    serial_number = Column(String(128), nullable=False)
    
    not_valid_before = Column(DateTime, nullable=False)
    not_valid_after = Column(DateTime, nullable=False)
    is_expired = Column(Boolean, default=False)
    crosses_2030_quantum_horizon = Column(Boolean, default=False)
    is_self_signed = Column(Boolean, default=False)
    
    file_path = Column(String(1024), nullable=True)
    pqc_replacement_strategy = Column(String(255), default="Composite X.509 with ML-DSA-65")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class RevocationRecord(Base):
    __tablename__ = "revocation_records"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    certificate_fingerprint = Column(String(64), nullable=False)
    revocation_reason = Column(String(100), default="KEY_COMPROMISE_POTENTIAL")
    revocation_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    crl_distribution_point = Column(String(512), nullable=True)
