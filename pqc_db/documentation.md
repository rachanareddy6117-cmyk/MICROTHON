# PQC-Migrate Database Documentation

## Overview
PQC-Migrate stores security findings, crypto evidence, repository metadata, dependency graphs, migration plans, runtime policy decisions, and governance records in a PostgreSQL database designed for evidence-based cryptographic operations.

## Core design principles
- UUID-based identity for portability and distributed workloads.
- Foreign keys and explicit constraints to preserve data integrity.
- JSONB for partially structured metadata and policy payloads.
- Indexes for repository, service, algorithm, severity, confidence, status, and timestamps.
- Alembic for migration management and schema evolution.

## Primary entity groups
### Project and repository
- organizations
- projects
- repositories
- deployments
- scans
- files

### Crypto inventory
- algorithms
- libraries
- crypto_assets
- crypto_knowledge
- certificates
- services

### Findings and evidence
- findings
- finding_evidence
- blast_radius

### Graph and dependency model
- nodes
- edges
- dependencies

### Governance and operations
- agent_runs
- remediation_jobs
- sandbox_runs
- firewall_policies
- firewall_events
- exceptions
- ci_scans
- crypto_snapshots
- migration_plans
- migration_tasks
- secure_data_objects
- secure_access_logs
- evaluation_runs

## ER diagram summary
Organizations -> Projects -> Repositories -> Services -> Certificates
Repositories -> Files -> CryptoAssets -> Algorithms / Libraries
Scans -> Findings -> FindingEvidence
Findings -> BlastRadius
Repositories -> Dependencies -> Algorithms / Libraries / Certificates
Repositories -> MigrationPlans -> MigrationTasks
Organizations -> FirewallPolicies -> FirewallEvents / Exceptions

## Notes
- The database does not store plaintext secrets in operational tables.
- Secure data objects are encrypted payload wrappers and access logs are maintained separately.
- The platform stores concise reasoning summaries for agent decisions without retaining hidden chain-of-thought.
