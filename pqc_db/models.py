from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from .database import Base


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String(255), nullable=False)
    slug = Column(String(120), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    role = Column(String(100), nullable=False, default="analyst")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_users_org", "organization_id"),
    )


class Project(Base):
    __tablename__ = "projects"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Repository(Base):
    __tablename__ = "repositories"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    remote_url = Column(String(500))
    language = Column(String(100))
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Deployment(Base):
    __tablename__ = "deployments"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    environment = Column(String(100), nullable=False)
    version = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Scan(Base):
    __tablename__ = "scans"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    scan_type = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    summary = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)

    __table_args__ = (
        Index("idx_scans_repository", "repository_id"),
        Index("idx_scans_status", "status"),
    )


class FileRecord(Base):
    __tablename__ = "files"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    path = Column(String(500), nullable=False)
    file_type = Column(String(100), nullable=False)
    sha256 = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_files_repository", "repository_id"),
        UniqueConstraint("repository_id", "path", name="uq_files_repository_path"),
    )


class Algorithm(Base):
    __tablename__ = "algorithms"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String(120), nullable=False, unique=True)
    family = Column(String(120), nullable=False)
    status = Column(String(50), nullable=False, default="approved")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_algorithms_name", "name"),
        Index("idx_algorithms_family", "family"),
    )


class Library(Base):
    __tablename__ = "libraries"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    name = Column(String(255), nullable=False)
    version = Column(String(120), nullable=False)
    package_manager = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=True)
    subject = Column(String(255))
    issuer = Column(String(255))
    serial_number = Column(String(255))
    expiry = Column(DateTime)
    status = Column(String(50), nullable=False, default="valid")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Service(Base):
    __tablename__ = "services"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    name = Column(String(255), nullable=False)
    environment = Column(String(100), nullable=False)
    protocol = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CryptoAsset(Base):
    __tablename__ = "crypto_assets"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"), nullable=True)
    algorithm_id = Column(UUID(as_uuid=True), ForeignKey("algorithms.id"), nullable=True)
    library_id = Column(UUID(as_uuid=True), ForeignKey("libraries.id"), nullable=True)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=True)
    role = Column(String(100), nullable=False)
    usage_type = Column(String(100), nullable=False)
    key_size = Column(Integer)
    mode = Column(String(100))
    padding = Column(String(100))
    protocol = Column(String(100))
    line_number = Column(Integer)
    confidence = Column(Numeric(4, 3), nullable=False, default=0.0)
    classification = Column(String(100), nullable=False, default="unknown")
    priority = Column(String(50), nullable=False, default="medium")
    status = Column(String(50), nullable=False, default="detected")
    detection_method = Column(String(120), nullable=False)
    first_seen = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_seen = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_crypto_assets_repo", "repository_id"),
        Index("idx_crypto_assets_algorithm", "algorithm_id"),
        Index("idx_crypto_assets_service", "service_id"),
        Index("idx_crypto_assets_classification", "classification"),
        Index("idx_crypto_assets_status", "status"),
        Index("idx_crypto_assets_confidence", "confidence"),
    )


class CryptoKnowledge(Base):
    __tablename__ = "crypto_knowledge"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    algorithm = Column(String(120), nullable=False)
    family = Column(String(120), nullable=False)
    classical_risk = Column(String(50), nullable=False)
    quantum_risk = Column(String(50), nullable=False)
    implementation_risk = Column(String(50), nullable=False)
    known_issues = Column(Text)
    recommended_migration = Column(Text)
    validation_requirements = Column(Text)
    knowledge_source = Column(String(255), nullable=False)
    knowledge_version = Column(String(80), nullable=False)
    effective_date = Column(DateTime, nullable=False)
    review_status = Column(String(50), nullable=False, default="approved")

    __table_args__ = (
        Index("idx_crypto_knowledge_algorithm", "algorithm"),
        Index("idx_crypto_knowledge_version", "knowledge_version"),
    )


class Finding(Base):
    __tablename__ = "findings"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    scan_id = Column(UUID(as_uuid=True), ForeignKey("scans.id"), nullable=False)
    crypto_asset_id = Column(UUID(as_uuid=True), ForeignKey("crypto_assets.id"), nullable=True)
    finding_type = Column(String(120), nullable=False)
    severity = Column(String(50), nullable=False)
    classification = Column(String(120), nullable=False)
    confidence = Column(Numeric(4, 3), nullable=False, default=0.0)
    evidence = Column(JSONB)
    recommendation = Column(Text)
    status = Column(String(50), nullable=False, default="open")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    resolved_at = Column(DateTime)

    __table_args__ = (
        Index("idx_findings_scan", "scan_id"),
        Index("idx_findings_severity", "severity"),
        Index("idx_findings_classification", "classification"),
        Index("idx_findings_confidence", "confidence"),
        Index("idx_findings_status", "status"),
        CheckConstraint("severity IN ('low','medium','high','critical')", name="ck_findings_severity"),
        CheckConstraint("status IN ('open','in_review','resolved','suppressed')", name="ck_findings_status"),
    )


class FindingEvidence(Base):
    __tablename__ = "finding_evidence"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    finding_id = Column(UUID(as_uuid=True), ForeignKey("findings.id"), nullable=False)
    source_type = Column(String(80), nullable=False)
    file = Column(String(500))
    line_start = Column(Integer)
    line_end = Column(Integer)
    snippet = Column(Text)
    runtime_source = Column(Text)
    configuration_source = Column(Text)
    dependency_source = Column(Text)
    hash = Column(String(128))


class Node(Base):
    __tablename__ = "nodes"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    node_type = Column(String(80), nullable=False)
    repository = Column(String(255))
    application = Column(String(255))
    service = Column(String(255))
    package = Column(String(255))
    library = Column(String(255))
    crypto_asset = Column(String(255))
    algorithm = Column(String(255))
    certificate = Column(String(255))
    protocol = Column(String(255))
    data_asset = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Dependency(Base):
    __tablename__ = "dependencies"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=True)
    package_name = Column(String(255), nullable=False)
    library_name = Column(String(255), nullable=True)
    crypto_asset_id = Column(UUID(as_uuid=True), ForeignKey("crypto_assets.id"), nullable=True)
    algorithm_id = Column(UUID(as_uuid=True), ForeignKey("algorithms.id"), nullable=True)
    certificate_id = Column(UUID(as_uuid=True), ForeignKey("certificates.id"), nullable=True)
    protocol = Column(String(100), nullable=True)
    dependency_type = Column(String(80), nullable=False, default="DEPENDS_ON")
    dependency_depth = Column(Integer, nullable=False, default=0)
    metadata_json = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_dependencies_repository", "repository_id"),
        Index("idx_dependencies_service", "service_id"),
        Index("idx_dependencies_algorithm", "algorithm_id"),
        Index("idx_dependencies_type", "dependency_type"),
        CheckConstraint("dependency_type IN ('USES','DEPENDS_ON','CONFIGURES','CERTIFICATE_FOR','COMMUNICATES_WITH','PROVIDES','PROTECTS')", name="ck_dependencies_type"),
    )


class Edge(Base):
    __tablename__ = "edges"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    src_node_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"), nullable=False)
    dst_node_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"), nullable=False)
    relation = Column(String(80), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        CheckConstraint("relation IN ('USES','DEPENDS_ON','CONFIGURES','CERTIFICATE_FOR','COMMUNICATES_WITH','PROVIDES','PROTECTS')", name="ck_edges_relation"),
    )


class BlastRadius(Base):
    __tablename__ = "blast_radius"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    finding_id = Column(UUID(as_uuid=True), ForeignKey("findings.id"), nullable=False)
    affected_service = Column(String(255))
    affected_repository = Column(String(255))
    affected_certificate = Column(String(255))
    affected_protocol = Column(String(255))
    affected_environment = Column(String(120))
    criticality = Column(String(50), nullable=False, default="medium")
    dependency_distance = Column(Integer, nullable=False, default=0)


class AgentRun(Base):
    __tablename__ = "agent_runs"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    investigation_id = Column(UUID(as_uuid=True), nullable=False)
    agent_name = Column(String(120), nullable=False)
    agent_version = Column(String(80), nullable=False)
    input_reference = Column(String(500))
    output_reference = Column(String(500))
    status = Column(String(50), nullable=False, default="pending")
    confidence = Column(Numeric(4, 3), nullable=False, default=0.0)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)
    reasoning_summary = Column(Text)
    structured_decision = Column(JSONB)


class RemediationJob(Base):
    __tablename__ = "remediation_jobs"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    finding_id = Column(UUID(as_uuid=True), ForeignKey("findings.id"), nullable=False)
    agent_run_id = Column(UUID(as_uuid=True), ForeignKey("agent_runs.id"), nullable=True)
    type = Column(String(100), nullable=False)
    risk_level = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="queued")
    patch_reference = Column(String(500))
    sandbox_id = Column(UUID(as_uuid=True), nullable=True)
    approval_required = Column(Boolean, default=True)
    approved_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SandboxRun(Base):
    __tablename__ = "sandbox_runs"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    remediation_id = Column(UUID(as_uuid=True), ForeignKey("remediation_jobs.id"), nullable=False)
    container_reference = Column(String(255))
    commit_before = Column(String(255))
    commit_after = Column(String(255))
    build_status = Column(String(50), default="pending")
    test_status = Column(String(50), default="pending")
    crypto_scan_before = Column(JSONB)
    crypto_scan_after = Column(JSONB)
    compatibility_status = Column(String(50), default="pending")
    performance_status = Column(String(50), default="pending")
    verification_status = Column(String(50), default="pending")
    rollback_status = Column(String(50), default="pending")


class FirewallPolicy(Base):
    __tablename__ = "firewall_policies"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    policy_name = Column(String(255), nullable=False)
    policy_json = Column(JSONB, nullable=False)
    status = Column(String(50), nullable=False, default="draft")
    created_by = Column(UUID(as_uuid=True), nullable=False)
    approved_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        CheckConstraint("status IN ('draft','approved','active','deprecated')", name="ck_firewall_policy_status"),
    )


class FirewallEvent(Base):
    __tablename__ = "firewall_events"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    policy_id = Column(UUID(as_uuid=True), ForeignKey("firewall_policies.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    source = Column(String(255))
    destination = Column(String(255))
    service = Column(String(255))
    tls_version = Column(String(50))
    cipher = Column(String(200))
    certificate = Column(String(255))
    algorithm = Column(String(120))
    decision = Column(String(50), nullable=False)
    reason = Column(Text)
    risk = Column(String(50), nullable=False, default="medium")
    agent_analysis_id = Column(UUID(as_uuid=True), nullable=True)

    __table_args__ = (
        CheckConstraint("decision IN ('ALLOW','MONITOR','WARN','REVIEW','BLOCK')", name="ck_firewall_decision"),
        Index("idx_firewall_events_timestamp", "timestamp"),
        Index("idx_firewall_events_service", "service"),
    )


class FirewallException(Base):
    __tablename__ = "exceptions"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    policy_id = Column(UUID(as_uuid=True), ForeignKey("firewall_policies.id"), nullable=False)
    resource = Column(String(255), nullable=False)
    reason = Column(Text, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    approved_by = Column(UUID(as_uuid=True), nullable=True)
    expires_at = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False, default="active")

    __table_args__ = (
        CheckConstraint("status IN ('active','expired','revoked')", name="ck_exception_status"),
        CheckConstraint("expires_at > created_at", name="ck_exception_expiry"),
    )


class CiScan(Base):
    __tablename__ = "ci_scans"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    commit_hash = Column(String(120), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    new_crypto_count = Column(Integer, default=0)
    policy_violation_count = Column(Integer, default=0)
    decision = Column(String(20), nullable=False, default="REVIEW")


class CryptoSnapshot(Base):
    __tablename__ = "crypto_snapshots"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    scan_id = Column(UUID(as_uuid=True), ForeignKey("scans.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    asset_count = Column(Integer, default=0)
    algorithm_summary = Column(JSONB)
    risk_summary = Column(JSONB)
    migration_progress = Column(JSONB)


class MigrationPlan(Base):
    __tablename__ = "migration_plans"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    status = Column(String(50), nullable=False, default="draft")
    created_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class MigrationTask(Base):
    __tablename__ = "migration_tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    migration_plan_id = Column(UUID(as_uuid=True), ForeignKey("migration_plans.id"), nullable=False)
    finding_id = Column(UUID(as_uuid=True), ForeignKey("findings.id"), nullable=False)
    phase = Column(String(80), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(String(50), nullable=False, default="medium")
    status = Column(String(50), nullable=False, default="pending")
    dependencies = Column(JSONB, default=list)
    validation = Column(JSONB, default=list)
    rollback = Column(JSONB, default=list)

    __table_args__ = (
        CheckConstraint("status IN ('pending','in_progress','blocked','done')", name="ck_migration_task_status"),
    )


class SecureDataObject(Base):
    __tablename__ = "secure_data_objects"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    data_type = Column(String(120), nullable=False)
    encrypted_payload = Column(Text, nullable=False)
    encryption_metadata = Column(JSONB, nullable=False)
    classification = Column(String(80), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SecureAccessLog(Base):
    __tablename__ = "secure_access_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    object_id = Column(UUID(as_uuid=True), ForeignKey("secure_data_objects.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    result = Column(String(50), nullable=False)


class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    dataset = Column(String(255), nullable=False)
    approach = Column(String(50), nullable=False)
    precision = Column(Numeric(5, 4), nullable=False, default=0.0)
    recall = Column(Numeric(5, 4), nullable=False, default=0.0)
    f1 = Column(Numeric(5, 4), nullable=False, default=0.0)
    false_positive_rate = Column(Numeric(5, 4), nullable=False, default=0.0)
    uncertainty_detection = Column(Boolean, default=False)
    remediation_success = Column(Boolean, default=False)
    rollback_success = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Investigation(Base):
    __tablename__ = "investigations"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), nullable=False, default="open")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
