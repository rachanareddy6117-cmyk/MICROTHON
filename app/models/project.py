import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner = Column(String(100), default="security_lead")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Specification metadata extracted from PDF / documentation
    scope = Column(Text, nullable=True)
    technology_stack = Column(JSON, default=list)
    budget = Column(String(100), nullable=True)
    timeline = Column(String(100), nullable=True)
    vendors = Column(JSON, default=list)
    identified_risks = Column(JSON, default=list)
    
    # Relationships
    repositories = relationship("Repository", back_populates="project", cascade="all, delete-orphan")
    scans = relationship("ScanJob", back_populates="project", cascade="all, delete-orphan")

class ProjectRiskAnalysis(Base):
    __tablename__ = "project_risk_analyses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    source_filename = Column(String(255), nullable=False)
    extracted_text_preview = Column(Text, nullable=True)
    quantum_risk_index = Column(Float, default=0.0)
    hndl_exposure_level = Column(String(50), default="UNKNOWN")
    governance_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
