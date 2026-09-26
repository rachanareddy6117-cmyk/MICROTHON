import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, JSON
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="analyst")  # 'security_lead', 'analyst', 'auditor', 'firewall_admin'
    is_active = Column(Boolean, default=True)
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ApiKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    key_prefix = Column(String(12), nullable=False)
    key_hash = Column(String(128), nullable=False)
    user_id = Column(String(36), nullable=False)
    role = Column(String(50), default="ci_runner")
    expires_at = Column(DateTime, nullable=True)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
