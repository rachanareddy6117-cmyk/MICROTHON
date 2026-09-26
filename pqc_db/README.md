# PQC-Migrate Database

This package defines the PostgreSQL schema for the PQC-Migrate platform.

## Components
- `database.py`: engine and session factory
- `models.py`: SQLAlchemy ORM models
- `seed.py`: baseline seed data
- `queries.py`: sample analytical queries
- `alembic/`: migration scripts

## Database notes
- PostgreSQL is required.
- UUID primary keys are used throughout.
- JSONB is used where structured metadata is needed.
- Indexes are created for risk, classification, service, repository, severity, and timestamps.
- Alembic provides migration management.

## Example migration
```bash
alembic upgrade head
```

## Initialize seed data
```bash
python -m pqc_db.seed
```

## ER diagram summary
The model includes:
- Organizations → Projects → Repositories → Deployments
- Repositories → Scans → Findings → Evidence
- Repositories → Files → CryptoAssets → Algorithms / Libraries / Services / Certificates
- Security and governance tables for firewall policies, exceptions, audits, and evaluations
- Graph tables for dependency relationships and blast radius
