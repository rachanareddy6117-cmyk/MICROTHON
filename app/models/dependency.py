import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, JSON, Float, Integer
from ..database import Base

class DependencyNode(Base):
    __tablename__ = "dependency_nodes"
    
    id = Column(String(255), primary_key=True)
    label = Column(String(255), nullable=False)
    node_type = Column(String(50), nullable=False)  # repository, service, package, library, crypto_api, algorithm, certificate, protocol
    category = Column(String(100), nullable=True)
    vulnerability_tag = Column(String(50), nullable=True)
    metadata_json = Column(JSON, default=dict)

class DependencyEdge(Base):
    __tablename__ = "dependency_edges"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String(255), nullable=False)
    target = Column(String(255), nullable=False)
    relation = Column(String(100), default="depends_on")

class BlastRadiusRecord(Base):
    __tablename__ = "blast_radius_records"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    finding_id = Column(String(50), nullable=False)
    algorithm = Column(String(100), nullable=False)
    location = Column(String(1024), nullable=False)
    direct_dependents_count = Column(Integer, default=0)
    transitive_impacted_count = Column(Integer, default=0)
    transitive_impacted_files = Column(JSON, default=list)
    criticality_score = Column(Float, default=0.0)
    operational_impact = Column(String(100), default="Perimeter / In-Transit")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
