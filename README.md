# PQC-Migrate 🛡️⚛️
**Post-Quantum Cryptography (PQC) Static Analysis, Defensive Crypto Firewall & Agile Remediation Engine**

> [!WARNING]
> **EPISTEMIC HUMILITY STATEMENT:**
> Static cryptographic auditing does **NOT** constitute a proof of quantum security.
> PQC-Migrate is engineered as a **static-analysis, dependency blast-radius mapping, defensive policy enforcement, and risk-communication platform**, not a live-defense guarantee. It audits static algorithm selection, configuration policies, and structural coupling without ever claiming a scan "proves" quantum safety.

---

## 🏛️ System Architecture

```
                  ┌────────────────────────────────────────────────────────┐
                  │                  PQC-Migrate Platform                  │
                  └───────────────────────────┬────────────────────────────┘
                                              │
    ┌───────────────────────────┬─────────────┴─────────────┬───────────────────────────┐
    │                           │                           │                           │
    ▼                           ▼                           ▼                           ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Secure Ingestion │    │ Multi-Domain     │    │ 10-Agent         │    │ Defensive Crypto │
│ Engine           │    │ Crypto Scanners  │    │ Orchestrator     │    │ Firewall Gateway │
│ - PDF Spec Extr  │    │ - RSA/ECC/ECDSA  │    │ - DiscoveryAgent │    │ - Policy-as-Code │
│ - Safe Unpack    │    │ - AES/3DES/RC4   │    │ - EvidenceAgent  │    │ - Decision Engine│
│ - ZipBomb Shield │    │ - MD5/SHA-1/TLS  │    │ - RiskAgent      │    │ - ALLOW/WARN/    │
│ - Sandboxed Git  │    │ - PQC (ML-KEM/   │    │ - PatchAgent     │    │   REVIEW/BLOCK   │
│ - No-Execution   │    │   ML-DSA/SLH-DSA)│    │ - SandboxAgent   │    │ - WebSocket Hub  │
└──────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘
```

- **Backend Framework:** FastAPI with async execution
- **Database:** PostgreSQL (with automatic async SQLite fallback for testing/local setups)
- **Caching & Streaming:** Redis for task queueing & WebSocket telemetry broadcasting
- **Remediation Sandbox:** Isolated container environments with automated rollback
- **Data Protection:** Envelope Encryption via KMS/HSM abstraction with masked low-privilege views

---

## 🚀 Key Modules & Capabilities

### 1. Multi-Domain Cryptographic Scanner
- Detects classical asymmetric primitives broken by Shor's algorithm: **RSA (all key sizes), ECC, ECDSA, ECDH, Diffie-Hellman**.
- Detects Grover-vulnerable symmetric ciphers: **AES-128 (effective strength drops to ~64 bits), 3DES, DES, RC4**.
- Detects classically broken hashes: **MD5, SHA-1**.
- Recognizes standardized Post-Quantum Cryptography: **NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA)**.
- Audits configs: Nginx, Apache TLS cipher suites, OpenSSH `sshd_config`, Terraform KMS key specs, Dockerfiles.
- Parses X.509 certificates and flags expirations crossing the **2030 CRQC Horizon**.

### 2. 8-Tier Hierarchical Dependency Graph
Constructs and visualizes the complete cryptographic blast radius:
`Repository -> Service -> Package -> Library -> Crypto API -> Algorithm -> Certificate -> Protocol`

### 3. 10-Agent Autonomous Orchestrator
Agents communicate through structured state (`AgentBlackboardState`) with full immutable logging:
1. `DiscoveryAgent`: Discovers files, repos, services, configs, certs.
2. `EvidenceAgent`: Collects code snippets, AST locations, and certificate attributes.
3. `RiskAgent`: Evaluates Shor/Grover risk, Mosca theorem horizon, and HNDL index.
4. `DependencyAgent`: Constructs graph hierarchy and computes blast radii.
5. `MigrationAgent`: Synthesizes 4-phase NIST-aligned migration roadmap.
6. `PatchAgent`: Synthesizes agile code diff patches.
7. `SandboxAgent`: Validates patches in isolated test environments.
8. `VerificationAgent`: Verifies build output, test suites, and regression rescans.
9. `FirewallAgent`: Generates runtime policy recommendations.
10. `GovernanceAgent`: Manages approvals and compliance gates.

### 4. Auto-Remediation & Sandbox Workflow
`Finding -> Investigation -> Fix Proposal -> Patch -> Sandbox -> Tests -> Rescan -> Verification -> Approval -> Deployment -> Monitoring -> Rollback`
- **Zero Automatic High-Risk Deployments:** Perimeter and TLS changes mandate manual Security Lead sign-off.
- **Rollback Engine:** Immediate one-click rollback restoring verified snapshots.

### 5. Defensive Crypto Policy Enforcement Firewall
- Enforces Policy-as-Code (YAML/JSON) with versioning, rollback, and temporary exception management.
- Evaluates handshakes and returns: `ALLOW`, `MONITOR`, `WARN`, `REVIEW`, `BLOCK`.
- Detects TLS 1.0/1.1, broken ciphers, weak RSA keys (<2048), SHA-1 signatures, and downgrade sentinels.

### 6. CI/CD Guard
Endpoint `POST /api/v1/ci/scan`:
- Analyzes newly committed pull requests or branches.
- Returns status `PASS`, `REVIEW`, or `BLOCK` with precise line-number evidence and recommended NIST PQC replacements.

### 7. Secure Data Module (Envelope Encryption)
- Encrypts sensitive secrets using **AES-256-GCM**.
- Data Encryption Keys (DEKs) wrapped by KMS Key Encryption Keys (KEKs).
- Masked views for standard analysts (`Supe*****************2026`).
- Decryption restricted exclusively to the `security_lead` role.

---

## 🔌 API Group Endpoints (`/api/v1`)

| Endpoint Group | Description |
| :--- | :--- |
| `/projects` | Manage projects and scan product specification PDFs |
| `/repositories` | Secure Git clone & safe archive ingestion |
| `/scans` | Trigger full 10-agent scans and retrieve state |
| `/findings` | Filter and query cryptographic vulnerability findings |
| `/crypto-assets` | Inventory of all discovered cryptographic components |
| `/dependencies` | 8-tier dependency graph and blast radius calculations |
| `/certificates` | X.509 certificate tracking and revocation records |
| `/agents` | Agent execution step logs and state deltas |
| `/investigations` | Finding investigation state tracking |
| `/remediations` | Fix proposal generation, approval gates, and rollbacks |
| `/sandbox` | Sandbox container runner status & validation metrics |
| `/migrations` | 4-phase NIST FIPS 203/204/205 roadmap |
| `/crypto-agility` | Cryptographic agility registry and provider factories |
| `/firewall` | Handshake inspection, active policy, exceptions & telemetry |
| `/ci` | CI/CD commit scanner (`POST /api/v1/ci/scan`) |
| `/secure-data` | KMS envelope encryption vault & role-based decryption |
| `/reports` | CycloneDX 1.6 CBOM JSON and executive reports |
| `/audit` | Immutable audit trail for all sensitive operations |
| `/evaluation` | Posture evaluation and crypto agility readiness index |
| `/ws/events` | Real-time WebSocket event streaming |

---

## 🧪 Testing & Adversarial Verification

Run the full adversarial verification suite without requiring external production credentials:
```bash
python tests/test_pqc_migrate_all.py
```
Run the REST API endpoint test suite:
```bash
python tests/test_api_endpoints.py
```

### Starting the Server
```bash
python start_server.py
```
Open **http://localhost:8000/docs** for the interactive OpenAPI Swagger UI.

### Running with Docker Compose
```bash
docker-compose up --build
```
