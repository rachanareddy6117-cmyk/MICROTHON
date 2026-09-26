import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, JSON, Integer
from ..database import Base

class AgentTask(Base):
    __tablename__ = "agent_tasks"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = Column(String(36), nullable=False)
    agent_name = Column(String(100), nullable=False)  # DiscoveryAgent, EvidenceAgent, etc.
    status = Column(String(50), default="INITIALIZED")  # INITIALIZED, RUNNING, COMPLETED, FAILED
    input_payload = Column(JSON, default=dict)
    output_payload = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

class AgentExecutionLog(Base):
    __tablename__ = "agent_execution_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String(36), nullable=False)
    agent_name = Column(String(100), nullable=False)
    step_number = Column(Integer, default=1)
    action_type = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    state_delta = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class AgentSharedState(Base):
    __tablename__ = "agent_shared_states"
    
    scan_id = Column(String(36), primary_key=True)
    blackboard_state = Column(JSON, default=dict)
    current_phase = Column(String(100), default="DISCOVERY")
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
