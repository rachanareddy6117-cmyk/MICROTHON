from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from pqc_db.database import SessionLocal
from pqc_db.models import (
    Algorithm,
    CryptoKnowledge,
    FirewallPolicy,
    Organization,
    Project,
    Repository,
    Scan,
    Service,
)


def seed_data() -> None:
    db: Session = SessionLocal()
    org = db.query(Organization).filter_by(slug="acme").first()
    if not org:
        org = Organization(id=uuid4(), name="Acme Security", slug="acme")
        db.add(org)
        db.flush()

    project = db.query(Project).filter_by(name="PQC Migration").first()
    if not project:
        project = Project(id=uuid4(), organization_id=org.id, name="PQC Migration", description="Migration project", status="active")
        db.add(project)
        db.flush()

    repo = db.query(Repository).filter_by(name="payments-api").first()
    if not repo:
        repo = Repository(id=uuid4(), project_id=project.id, name="payments-api", remote_url="https://example.com/payments-api", language="java", status="active")
        db.add(repo)
        db.flush()

    if not db.query(Service).filter_by(name="payments-api-gateway").first():
        db.add(Service(id=uuid4(), repository_id=repo.id, name="payments-api-gateway", environment="prod", protocol="TLS 1.2"))

    if not db.query(Algorithm).filter_by(name="RSA").first():
        db.add(Algorithm(id=uuid4(), name="RSA", family="asymmetric", status="deprecated"))
    if not db.query(Algorithm).filter_by(name="ML-KEM").first():
        db.add(Algorithm(id=uuid4(), name="ML-KEM", family="pqc", status="approved"))

    if not db.query(CryptoKnowledge).filter_by(algorithm="RSA").first():
        db.add(CryptoKnowledge(
            id=uuid4(),
            algorithm="RSA",
            family="asymmetric",
            classical_risk="high",
            quantum_risk="critical",
            implementation_risk="medium",
            known_issues="RSA and ECC are vulnerable to Shor-based attacks in a large-scale quantum threat model.",
            recommended_migration="Migrate to ML-KEM for key establishment and use PQC-aligned certificate profiles.",
            validation_requirements="Validate key sizes, certificate chains, and protocol negotiation before cutover.",
            knowledge_source="controlled-crypto-knowledge-base",
            knowledge_version="2026.09.26.v1",
            effective_date=datetime.utcnow() - timedelta(days=30),
            review_status="approved",
        ))

    if not db.query(Scan).filter_by(scan_type="baseline").first():
        db.add(Scan(id=uuid4(), repository_id=repo.id, scan_type="baseline", status="completed", summary={"status": "ok"}, created_at=datetime.utcnow()))

    if not db.query(FirewallPolicy).filter_by(policy_name="default-prod-policy").first():
        db.add(FirewallPolicy(
            id=uuid4(),
            organization_id=org.id,
            version=1,
            policy_name="default-prod-policy",
            policy_json={"tls": ["TLS 1.3"], "disallow": ["MD5", "3DES", "RC4"]},
            status="active",
            created_by=uuid4(),
            approved_by=uuid4(),
            created_at=datetime.utcnow(),
        ))

    db.commit()
    db.close()


if __name__ == "__main__":
    seed_data()
