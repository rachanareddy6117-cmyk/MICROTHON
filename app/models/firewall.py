import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, JSON, Integer, Boolean
from ..database import Base

class FirewallPolicy(Base):
    __tablename__ = "firewall_policies"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    policy_as_code_yaml = Column(Text, nullable=False)
    
    # Policy limits
    minimum_tls = Column(String(20), default="TLSv1.2")
    allowed_ciphers = Column(JSON, default=list)
    blocked_algorithms = Column(JSON, default=list)
    minimum_rsa_key_size = Column(Integer, default=2048)
    certificate_requirements = Column(JSON, default=dict)
    approved_providers = Column(JSON, default=list)
    pqc_policy = Column(String(100), default="HYBRID_PREFERRED")  # CLASSICAL_ONLY, HYBRID_PREFERRED, PQC_MANDATORY
    
    created_by = Column(String(100), default="admin")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class FirewallRule(Base):
    __tablename__ = "firewall_rules"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    policy_id = Column(String(36), nullable=False)
    name = Column(String(255), nullable=False)
    match_condition = Column(JSON, nullable=False)
    action = Column(String(20), default="WARN")  # ALLOW, MONITOR, WARN, REVIEW, BLOCK
    priority = Column(Integer, default=100)
    is_enabled = Column(Boolean, default=True)

class FirewallEvent(Base):
    __tablename__ = "firewall_events"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    client_ip = Column(String(50), nullable=True)
    endpoint = Column(String(255), nullable=False)
    negotiated_tls_version = Column(String(20), nullable=False)
    negotiated_cipher_suite = Column(String(100), nullable=False)
    peer_certificate_fingerprint = Column(String(64), nullable=True)
    rule_matched = Column(String(255), nullable=True)
    decision = Column(String(20), nullable=False)  # ALLOW, MONITOR, WARN, REVIEW, BLOCK
    reason = Column(Text, nullable=False)
    telemetry_metadata = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class PolicyException(Base):
    __tablename__ = "policy_exceptions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    endpoint = Column(String(255), nullable=False)
    allowed_cipher_or_algo = Column(String(100), nullable=False)
    business_justification = Column(Text, nullable=False)
    approved_by = Column(String(100), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
