"""init pqc schema

Revision ID: 20260926_init_pqc_schema
Revises:
Create Date: 2026-09-26 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260926_init_pqc_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "repositories",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("remote_url", sa.String(length=500), nullable=True),
        sa.Column("language", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("idx_users_org", "users", ["organization_id"], unique=False)
    op.create_table(
        "deployments",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("repository_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("environment", sa.String(length=100), nullable=False),
        sa.Column("version", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "scans",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("repository_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("scan_type", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("summary", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_scans_repository", "scans", ["repository_id"], unique=False)
    op.create_index("idx_scans_status", "scans", ["status"], unique=False)
    op.create_table(
        "files",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("repository_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("path", sa.String(length=500), nullable=False),
        sa.Column("file_type", sa.String(length=100), nullable=False),
        sa.Column("sha256", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("repository_id", "path", name="uq_files_repository_path"),
    )
    op.create_index("idx_files_repository", "files", ["repository_id"], unique=False)
    op.create_table(
        "algorithms",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("family", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("idx_algorithms_name", "algorithms", ["name"], unique=False)
    op.create_index("idx_algorithms_family", "algorithms", ["family"], unique=False)
    op.create_table(
        "libraries",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("repository_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=120), nullable=False),
        sa.Column("package_manager", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "services",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("repository_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("environment", sa.String(length=100), nullable=False),
        sa.Column("protocol", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "certificates",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("issuer", sa.String(length=255), nullable=True),
        sa.Column("serial_number", sa.String(length=255), nullable=True),
        sa.Column("expiry", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "crypto_assets",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("repository_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("file_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("algorithm_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("library_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("role", sa.String(length=100), nullable=False),
        sa.Column("usage_type", sa.String(length=100), nullable=False),
        sa.Column("key_size", sa.Integer(), nullable=True),
        sa.Column("mode", sa.String(length=100), nullable=True),
        sa.Column("padding", sa.String(length=100), nullable=True),
        sa.Column("protocol", sa.String(length=100), nullable=True),
        sa.Column("line_number", sa.Integer(), nullable=True),
        sa.Column("confidence", sa.Numeric(precision=4, scale=3), nullable=False),
        sa.Column("classification", sa.String(length=100), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("detection_method", sa.String(length=120), nullable=False),
        sa.Column("first_seen", sa.DateTime(), nullable=False),
        sa.Column("last_seen", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["algorithm_id"], ["algorithms.id"]),
        sa.ForeignKeyConstraint(["file_id"], ["files.id"]),
        sa.ForeignKeyConstraint(["library_id"], ["libraries.id"]),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_crypto_assets_repo", "crypto_assets", ["repository_id"], unique=False)
    op.create_index("idx_crypto_assets_algorithm", "crypto_assets", ["algorithm_id"], unique=False)
    op.create_index("idx_crypto_assets_service", "crypto_assets", ["service_id"], unique=False)
    op.create_index("idx_crypto_assets_classification", "crypto_assets", ["classification"], unique=False)
    op.create_index("idx_crypto_assets_status", "crypto_assets", ["status"], unique=False)
    op.create_index("idx_crypto_assets_confidence", "crypto_assets", ["confidence"], unique=False)
    op.create_table(
        "crypto_knowledge",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("algorithm", sa.String(length=120), nullable=False),
        sa.Column("family", sa.String(length=120), nullable=False),
        sa.Column("classical_risk", sa.String(length=50), nullable=False),
        sa.Column("quantum_risk", sa.String(length=50), nullable=False),
        sa.Column("implementation_risk", sa.String(length=50), nullable=False),
        sa.Column("known_issues", sa.Text(), nullable=True),
        sa.Column("recommended_migration", sa.Text(), nullable=True),
        sa.Column("validation_requirements", sa.Text(), nullable=True),
        sa.Column("knowledge_source", sa.String(length=255), nullable=False),
        sa.Column("knowledge_version", sa.String(length=80), nullable=False),
        sa.Column("effective_date", sa.DateTime(), nullable=False),
        sa.Column("review_status", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_crypto_knowledge_algorithm", "crypto_knowledge", ["algorithm"], unique=False)
    op.create_index("idx_crypto_knowledge_version", "crypto_knowledge", ["knowledge_version"], unique=False)
    op.create_table(
        "findings",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("crypto_asset_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("finding_type", sa.String(length=120), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("classification", sa.String(length=120), nullable=False),
        sa.Column("confidence", sa.Numeric(precision=4, scale=3), nullable=False),
        sa.Column("evidence", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("recommendation", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["crypto_asset_id"], ["crypto_assets.id"]),
        sa.ForeignKeyConstraint(["scan_id"], ["scans.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_findings_scan", "findings", ["scan_id"], unique=False)
    op.create_index("idx_findings_severity", "findings", ["severity"], unique=False)
    op.create_index("idx_findings_classification", "findings", ["classification"], unique=False)
    op.create_index("idx_findings_confidence", "findings", ["confidence"], unique=False)
    op.create_index("idx_findings_status", "findings", ["status"], unique=False)
    op.create_table(
        "finding_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("finding_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_type", sa.String(length=80), nullable=False),
        sa.Column("file", sa.String(length=500), nullable=True),
        sa.Column("line_start", sa.Integer(), nullable=True),
        sa.Column("line_end", sa.Integer(), nullable=True),
        sa.Column("snippet", sa.Text(), nullable=True),
        sa.Column("runtime_source", sa.Text(), nullable=True),
        sa.Column("configuration_source", sa.Text(), nullable=True),
        sa.Column("dependency_source", sa.Text(), nullable=True),
        sa.Column("hash", sa.String(length=128), nullable=True),
        sa.ForeignKeyConstraint(["finding_id"], ["findings.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "nodes",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("node_type", sa.String(length=80), nullable=False),
        sa.Column("repository", sa.String(length=255), nullable=True),
        sa.Column("application", sa.String(length=255), nullable=True),
        sa.Column("service", sa.String(length=255), nullable=True),
        sa.Column("package", sa.String(length=255), nullable=True),
        sa.Column("library", sa.String(length=255), nullable=True),
        sa.Column("crypto_asset", sa.String(length=255), nullable=True),
        sa.Column("algorithm", sa.String(length=255), nullable=True),
        sa.Column("certificate", sa.String(length=255), nullable=True),
        sa.Column("protocol", sa.String(length=255), nullable=True),
        sa.Column("data_asset", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "dependencies",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("repository_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("package_name", sa.String(length=255), nullable=False),
        sa.Column("library_name", sa.String(length=255), nullable=True),
        sa.Column("crypto_asset_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("algorithm_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("certificate_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("protocol", sa.String(length=100), nullable=True),
        sa.Column("dependency_type", sa.String(length=80), nullable=False),
        sa.Column("dependency_depth", sa.Integer(), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["algorithm_id"], ["algorithms.id"]),
        sa.ForeignKeyConstraint(["certificate_id"], ["certificates.id"]),
        sa.ForeignKeyConstraint(["crypto_asset_id"], ["crypto_assets.id"]),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_dependencies_repository", "dependencies", ["repository_id"], unique=False)
    op.create_index("idx_dependencies_service", "dependencies", ["service_id"], unique=False)
    op.create_index("idx_dependencies_algorithm", "dependencies", ["algorithm_id"], unique=False)
    op.create_index("idx_dependencies_type", "dependencies", ["dependency_type"], unique=False)
    op.create_table(
        "edges",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("src_node_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dst_node_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("relation", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["src_node_id"], ["nodes.id"]),
        sa.ForeignKeyConstraint(["dst_node_id"], ["nodes.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "blast_radius",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("finding_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("affected_service", sa.String(length=255), nullable=True),
        sa.Column("affected_repository", sa.String(length=255), nullable=True),
        sa.Column("affected_certificate", sa.String(length=255), nullable=True),
        sa.Column("affected_protocol", sa.String(length=255), nullable=True),
        sa.Column("affected_environment", sa.String(length=120), nullable=True),
        sa.Column("criticality", sa.String(length=50), nullable=False),
        sa.Column("dependency_distance", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["finding_id"], ["findings.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "agent_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("investigation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("agent_name", sa.String(length=120), nullable=False),
        sa.Column("agent_version", sa.String(length=80), nullable=False),
        sa.Column("input_reference", sa.String(length=500), nullable=True),
        sa.Column("output_reference", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("confidence", sa.Numeric(precision=4, scale=3), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("reasoning_summary", sa.Text(), nullable=True),
        sa.Column("structured_decision", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "remediation_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("finding_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("agent_run_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("type", sa.String(length=100), nullable=False),
        sa.Column("risk_level", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("patch_reference", sa.String(length=500), nullable=True),
        sa.Column("sandbox_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("approval_required", sa.Boolean(), nullable=True),
        sa.Column("approved_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_run_id"], ["agent_runs.id"]),
        sa.ForeignKeyConstraint(["finding_id"], ["findings.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sandbox_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("remediation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("container_reference", sa.String(length=255), nullable=True),
        sa.Column("commit_before", sa.String(length=255), nullable=True),
        sa.Column("commit_after", sa.String(length=255), nullable=True),
        sa.Column("build_status", sa.String(length=50), nullable=True),
        sa.Column("test_status", sa.String(length=50), nullable=True),
        sa.Column("crypto_scan_before", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("crypto_scan_after", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("compatibility_status", sa.String(length=50), nullable=True),
        sa.Column("performance_status", sa.String(length=50), nullable=True),
        sa.Column("verification_status", sa.String(length=50), nullable=True),
        sa.Column("rollback_status", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(["remediation_id"], ["remediation_jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "firewall_policies",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("policy_name", sa.String(length=255), nullable=False),
        sa.Column("policy_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("approved_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "firewall_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("policy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=True),
        sa.Column("destination", sa.String(length=255), nullable=True),
        sa.Column("service", sa.String(length=255), nullable=True),
        sa.Column("tls_version", sa.String(length=50), nullable=True),
        sa.Column("cipher", sa.String(length=200), nullable=True),
        sa.Column("certificate", sa.String(length=255), nullable=True),
        sa.Column("algorithm", sa.String(length=120), nullable=True),
        sa.Column("decision", sa.String(length=50), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("risk", sa.String(length=50), nullable=False),
        sa.Column("agent_analysis_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["policy_id"], ["firewall_policies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_firewall_events_timestamp", "firewall_events", ["timestamp"], unique=False)
    op.create_index("idx_firewall_events_service", "firewall_events", ["service"], unique=False)
    op.create_table(
        "exceptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("policy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("resource", sa.String(length=255), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("approved_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(["policy_id"], ["firewall_policies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "ci_scans",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("repository_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("commit_hash", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("new_crypto_count", sa.Integer(), nullable=True),
        sa.Column("policy_violation_count", sa.Integer(), nullable=True),
        sa.Column("decision", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "crypto_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("repository_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("asset_count", sa.Integer(), nullable=True),
        sa.Column("algorithm_summary", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("risk_summary", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("migration_progress", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
        sa.ForeignKeyConstraint(["scan_id"], ["scans.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "migration_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("repository_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "migration_tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("migration_plan_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("finding_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("phase", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("priority", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("dependencies", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("validation", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("rollback", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(["finding_id"], ["findings.id"]),
        sa.ForeignKeyConstraint(["migration_plan_id"], ["migration_plans.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "secure_data_objects",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("data_type", sa.String(length=120), nullable=False),
        sa.Column("encrypted_payload", sa.Text(), nullable=False),
        sa.Column("encryption_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("classification", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "secure_access_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("object_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("result", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(["object_id"], ["secure_data_objects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "evaluation_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("dataset", sa.String(length=255), nullable=False),
        sa.Column("approach", sa.String(length=50), nullable=False),
        sa.Column("precision", sa.Numeric(precision=5, scale=4), nullable=False),
        sa.Column("recall", sa.Numeric(precision=5, scale=4), nullable=False),
        sa.Column("f1", sa.Numeric(precision=5, scale=4), nullable=False),
        sa.Column("false_positive_rate", sa.Numeric(precision=5, scale=4), nullable=False),
        sa.Column("uncertainty_detection", sa.Boolean(), nullable=True),
        sa.Column("remediation_success", sa.Boolean(), nullable=True),
        sa.Column("rollback_success", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "investigations",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("repository_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("investigations")
    op.drop_table("evaluation_runs")
    op.drop_table("secure_access_logs")
    op.drop_table("secure_data_objects")
    op.drop_table("migration_tasks")
    op.drop_table("migration_plans")
    op.drop_table("crypto_snapshots")
    op.drop_table("ci_scans")
    op.drop_table("exceptions")
    op.drop_table("firewall_events")
    op.drop_table("firewall_policies")
    op.drop_table("sandbox_runs")
    op.drop_table("remediation_jobs")
    op.drop_table("agent_runs")
    op.drop_table("blast_radius")
    op.drop_table("edges")
    op.drop_table("dependencies")
    op.drop_table("nodes")
    op.drop_table("finding_evidence")
    op.drop_table("findings")
    op.drop_table("crypto_knowledge")
    op.drop_table("crypto_assets")
    op.drop_table("certificates")
    op.drop_table("services")
    op.drop_table("libraries")
    op.drop_table("algorithms")
    op.drop_table("files")
    op.drop_table("scans")
    op.drop_table("deployments")
    op.drop_table("users")
    op.drop_table("repositories")
    op.drop_table("projects")
    op.drop_table("organizations")
