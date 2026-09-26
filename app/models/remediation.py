import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, JSON, Boolean, Float
from ..database import Base

class Investigation(Base):
    __tablename__ = "investigations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    finding_id = Column(String(50), nullable=False)
    status = Column(String(50), default="OPEN")  # OPEN, IN_PROGRESS, RESOLVED, DISMISSED
    assigned_agent = Column(String(100), default="InvestigationAgent")
    evidence_collected = Column(JSON, default=dict)
    risk_assessment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class FixProposal(Base):
    __tablename__ = "fix_proposals"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    finding_id = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    proposed_algorithm = Column(String(100), nullable=False)  # e.g., ML-KEM-768 or AES-256-GCM
    diff_patch = Column(Text, nullable=False)
    is_high_risk = Column(Boolean, default=False)
    requires_approval = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class RemediationPatch(Base):
    __tablename__ = "remediation_patches"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fix_proposal_id = Column(String(36), nullable=False)
    target_file = Column(String(1024), nullable=False)
    patch_content = Column(Text, nullable=False)
    reverted_content_backup = Column(Text, nullable=True)
    applied_status = Column(String(50), default="PENDING_SANDBOX")  # PENDING_SANDBOX, SANDBOX_PASSED, APPLIED, ROLLED_BACK
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class SandboxRun(Base):
    __tablename__ = "sandbox_runs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patch_id = Column(String(36), nullable=False)
    container_id = Column(String(100), nullable=True)
    build_result = Column(String(50), default="SUCCESS")  # SUCCESS, FAILED
    test_result = Column(String(50), default="PASSED")   # PASSED, FAILED
    crypto_rescan_result = Column(String(50), default="CLEAN")  # CLEAN, REGRESSION_FOUND
    performance_overhead_percent = Column(Float, default=1.5)
    compatibility_score = Column(Float, default=98.0)
    security_policy_result = Column(String(50), default="APPROVED")
    logs = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class RollbackEvent(Base):
    __tablename__ = "rollback_events"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patch_id = Column(String(36), nullable=False)
    reason = Column(Text, nullable=False)
    initiated_by = Column(String(100), default="SecurityOfficer")
    restoration_status = Column(String(50), default="RESTORED")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
