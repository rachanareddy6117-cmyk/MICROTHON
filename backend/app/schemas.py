from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    source: str
    detail: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    config: Optional[str] = None
    package: Optional[str] = None
    dependency: Optional[str] = None
    certificate: Optional[str] = None
    runtime_telemetry: Optional[str] = None
    confidence: float = 0.0


class FindingAssessment(BaseModel):
    finding_id: str
    classification: str
    confidence: float
    evidence: List[EvidenceItem] = []
    risk: Dict[str, str]
    blast_radius: List[str] = []
    recommended_action: str
    patch: str
    sandbox_required: bool
    validation: List[str] = []
    rollback: List[str] = []
    approval_required: bool
    uncertainties: List[str] = []


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RepositoryCreate(BaseModel):
    project_id: str
    name: str
    remote_url: Optional[str] = None
    language: Optional[str] = None


class ScanPayload(BaseModel):
    repository_id: str
    scan_type: str = "full"
    summary: Optional[Dict[str, Any]] = None


class FirewallPolicyRule(BaseModel):
    minimum_tls: str = "TLS 1.3"
    allowed_ciphers: List[str] = ["TLS_AES_256_GCM_SHA384"]
    blocked_algorithms: List[str] = ["MD5", "3DES", "DES", "RC4", "SHA-1"]
    minimum_rsa_key_size: int = 3072
    certificate_requirements: Dict[str, Any] = {"sha2_required": True}
    approved_providers: List[str] = ["OpenSSL", "BoringSSL"]
    pqc_policy: Dict[str, Any] = {"ml_kem_required": True, "ml_dsa_required": False}
    exception_expiry: int = 30


class FirewallDecisionRequest(BaseModel):
    source: str
    destination: str
    service: str
    tls_version: str
    cipher: str
    certificate: str
    algorithm: str
    reason: Optional[str] = None
    risk: str = "medium"


class SecureDataCreate(BaseModel):
    organization_id: str
    data_type: str
    encrypted_payload: str
    encryption_metadata: Dict[str, Any]
    classification: str


class EvaluationRunCreate(BaseModel):
    dataset: str
    approach: str
    precision: float
    recall: float
    f1: float
    false_positive_rate: float
    uncertainty_detection: bool = False
    remediation_success: bool = False
    rollback_success: bool = False
