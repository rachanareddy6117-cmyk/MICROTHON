import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Repository(Base):
    __tablename__ = "repositories"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True)
    name = Column(String(255), nullable=False)
    git_url = Column(String(512), nullable=True)
    default_branch = Column(String(100), default="main")
    source_type = Column(String(50), default="git")  # 'git', 'zip_upload', 'local_folder'
    local_path = Column(String(1024), nullable=True)
    is_sandboxed = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    project = relationship("Project", back_populates="repositories")
    deployment_logs = relationship("DeploymentLog", back_populates="repository", cascade="all, delete-orphan")

class DeploymentLog(Base):
    __tablename__ = "deployment_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    repository_id = Column(String(36), ForeignKey("repositories.id"), nullable=False)
    environment = Column(String(50), default="production")  # production, staging, dev
    log_content = Column(Text, nullable=False)
    has_crypto_error = Column(Boolean, default=False)
    detected_errors = Column(JSON, default=list)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    repository = relationship("Repository", back_populates="deployment_logs")

class RuntimeErrorCorrelation(Base):
    __tablename__ = "runtime_error_correlations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    deployment_log_id = Column(String(36), ForeignKey("deployment_logs.id"), nullable=False)
    runtime_error_signature = Column(String(255), nullable=False)
    source_file = Column(String(512), nullable=True)
    line_number = Column(String(50), nullable=True)
    crypto_primitive_id = Column(String(100), nullable=True)
    service_name = Column(String(100), nullable=True)
    correlation_confidence = Column(String(20), default="HIGH")
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
