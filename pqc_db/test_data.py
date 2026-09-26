from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from pqc_db.database import SessionLocal
from pqc_db.models import (
    Algorithm,
    Certificate,
    CryptoKnowledge,
    FirewallPolicy,
    Organization,
    Project,
    Repository,
    Scan,
    Service,
)


def seed_test_data() -> None:
    db: Session = SessionLocal()

    org = db.query(Organization).filter_by(slug="demo-org").first()
    if not org:
        org = Organization(id=uuid4(), name="Demo Org", slug="demo-org")
        db.add(org)

    project = db.query(Project).filter_by(name="Demo Migration").first()
    if not project:
        project = Project(id=uuid4(), organization_id=org.id, name="Demo Migration", description="Demo project", status="active")
        db.add(project)

    repo = db.query(Repository).filter_by(name="demo-service").first()
    if not repo:
        repo = Repository(id=uuid4(), project_id=project.id, name="demo-service", remote_url="https://example.com/demo-service", language="python", status="active")
        db.add(repo)

    service = db.query(Service).filter_by(name="demo-api").first()
    if not service:
        service = Service(id=uuid4(), repository_id=repo.id, name="demo-api", environment="prod", protocol="TLS 1.2")
        db.add(service)

    cert = db.query(Certificate).filter_by(subject="demo-api.internal").first()
    if not cert:
        cert = Certificate(id=uuid4(), service_id=service.id, subject="demo-api.internal", issuer="Demo CA", serial_number="ABC123", expiry=datetime.utcnow() + timedelta(days=365), status="valid")
        db.add(cert)

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
            known_issues="Legacy RSA key exchange and certificate chains are vulnerable under quantum attacks.",
            recommended_migration="Use ML-KEM and PQC-aware certificate profiles.",
            validation_requirements="Validate compatibility and certificate chain trust.",
            knowledge_source="controlled-crypto-knowledge-base",
            knowledge_version="2026.09.26.v1",
            effective_date=datetime.utcnow(),
            review_status="approved",
        ))

    if not db.query(Scan).filter_by(scan_type="demo-scan").first():
        db.add(Scan(id=uuid4(), repository_id=repo.id, scan_type="demo-scan", status="completed", summary={"count": 2}, created_at=datetime.utcnow()))

    if not db.query(FirewallPolicy).filter_by(policy_name="demo-prod-policy").first():
        db.add(FirewallPolicy(
            id=uuid4(),
            organization_id=org.id,
            version=1,
            policy_name="demo-prod-policy",
            policy_json={"allow": ["TLS 1.3"], "block": ["MD5", "3DES"]},
            status="active",
            created_by=uuid4(),
            approved_by=uuid4(),
            created_at=datetime.utcnow(),
        ))

    db.commit()
    db.close()


if __name__ == "__main__":
    seed_test_data()
