import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, JSON, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class ScanJob(Base):
    __tablename__ = "scan_jobs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True)
    repository_id = Column(String(36), ForeignKey("repositories.id"), nullable=True)
    scan_type = Column(String(50), default="FULL")  # FULL, CI_GUARD, CERT_ONLY, CONFIG_ONLY
    status = Column(String(50), default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED
    total_files_scanned = Column(Integer, default=0)
    crypto_agility_score = Column(Float, default=100.0)
    hndl_exposure_index = Column(Float, default=0.0)
    summary_counts = Column(JSON, default=dict)
    limitations_disclosure = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
    
    project = relationship("Project", back_populates="scans")
    findings = relationship("Finding", back_populates="scan_job", cascade="all, delete-orphan")

class Finding(Base):
    __tablename__ = "findings"
    
    id = Column(String(50), primary_key=True)
    scan_job_id = Column(String(36), ForeignKey("scan_jobs.id"), nullable=False)
    source_type = Column(String(50), nullable=False)  # code, config, certificate, deployment
    file_path = Column(String(1024), nullable=False)
    line_number = Column(Integer, nullable=True)
    column = Column(Integer, nullable=True)
    code_snippet = Column(Text, nullable=True)
    
    algorithm = Column(String(100), nullable=False)
    key_size_or_curve = Column(String(100), nullable=True)
    category = Column(String(100), nullable=False)  # ASYMMETRIC_ENCRYPTION, DIGITAL_SIGNATURE, etc.
    vulnerability_level = Column(String(50), nullable=False)  # CRITICAL_SHOR, HIGH_GROVER, MEDIUM_DEPRECATED
    threat_vector = Column(Text, nullable=False)
    exposure_domain = Column(String(50), nullable=False)  # IN_TRANSIT, AT_REST, AUTHENTICATION_IDENTITY
    
    nist_replacement = Column(String(255), nullable=False)
    hybrid_pathway = Column(String(255), nullable=True)
    remediation_notes = Column(Text, nullable=True)
    confidence = Column(Float, default=1.0)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    scan_job = relationship("ScanJob", back_populates="findings")

class CryptoAsset(Base):
    __tablename__ = "crypto_assets"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    asset_type = Column(String(50), nullable=False)  # algorithm, certificate, key, protocol
    parameter_set = Column(String(100), nullable=True)
    quantum_vulnerability = Column(String(50), nullable=False)
    location_reference = Column(String(1024), nullable=False)
    service_boundary = Column(String(100), default="default_service")
    is_active = Column(String(20), default="YES")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
