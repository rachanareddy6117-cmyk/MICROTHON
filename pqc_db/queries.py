from __future__ import annotations

from sqlalchemy import text

from pqc_db.database import SessionLocal


def get_risk_by_algorithm() -> list[dict]:
    with SessionLocal() as session:
        rows = session.execute(text("""
            SELECT a.name, ck.quantum_risk, ck.classical_risk
            FROM crypto_knowledge ck
            JOIN algorithms a ON lower(a.name) = lower(ck.algorithm)
            ORDER BY ck.quantum_risk DESC
        """")).fetchall()
        return [dict(row._mapping) for row in rows]


def get_findings_by_severity() -> list[dict]:
    with SessionLocal() as session:
        rows = session.execute(text("""
            SELECT severity, COUNT(*) AS count
            FROM findings
            GROUP BY severity
        """")).fetchall()
        return [dict(row._mapping) for row in rows]


def get_crypto_assets_for_service(service_name: str) -> list[dict]:
    with SessionLocal() as session:
        rows = session.execute(text("""
            SELECT ca.role, ca.protocol, alg.name AS algorithm, ca.classification
            FROM crypto_assets ca
            JOIN services s ON s.id = ca.service_id
            LEFT JOIN algorithms alg ON alg.id = ca.algorithm_id
            WHERE s.name = :service_name
        """), {"service_name": service_name}).fetchall()
        return [dict(row._mapping) for row in rows]


def get_recent_firewall_events() -> list[dict]:
    with SessionLocal() as session:
        rows = session.execute(text("""
            SELECT service, tls_version, cipher, decision, reason, risk
            FROM firewall_events
            ORDER BY timestamp DESC
            LIMIT 20
        """)).fetchall()
        return [dict(row._mapping) for row in rows]
