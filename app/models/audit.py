import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, JSON
from ..database import Base

class AuditLog(Base):
    """
    Immutable audit trail for all security, cryptographic, and remediation operations.
    """
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user = Column(String(100), nullable=False)
    agent = Column(String(100), nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    resource = Column(String(255), nullable=False)
    action = Column(String(100), nullable=False)
    old_state = Column(JSON, nullable=True)
    new_state = Column(JSON, nullable=True)
    approval = Column(String(100), nullable=True)
    result = Column(String(50), default="SUCCESS")
    client_ip = Column(String(50), nullable=True)
