from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from ...firewall.engine import CryptoFirewallDecisionEngine, HandshakeMetadata
from ...firewall.policy_manager import policy_manager
from ...firewall.recommendations import recommendation_engine

router = APIRouter(prefix="/firewall", tags=["Crypto Firewall Gateway"])
firewall_engine = CryptoFirewallDecisionEngine(policy_manager)

class PolicyUpdateRequest(BaseModel):
    policy_yaml: str
    author: str = "security_admin"

class ExceptionRequest(BaseModel):
    endpoint: str
    cipher_or_algo: str
    justification: str
    approver: str = "security_lead"
    days_valid: int = 30

@router.post("/inspect")
def inspect_handshake(meta: HandshakeMetadata):
    return firewall_engine.evaluate_handshake(meta)

@router.get("/policies/active")
def get_active_policy():
    return policy_manager.get_active_policy()

@router.post("/policies/update")
def update_policy(req: PolicyUpdateRequest):
    return policy_manager.update_policy(req.policy_yaml, req.author)

@router.post("/policies/rollback/{version}")
def rollback_policy(version: int, author: str = "security_admin"):
    try:
        return policy_manager.rollback_policy(version, author)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/exceptions")
def create_exception(req: ExceptionRequest):
    return policy_manager.add_exception(req.endpoint, req.cipher_or_algo, req.justification, req.approver, req.days_valid)

@router.get("/events")
def get_firewall_events():
    return firewall_engine.events_history

@router.get("/recommendations")
def get_recommendations():
    return recommendation_engine.generate_recommendations(firewall_engine.events_history)
