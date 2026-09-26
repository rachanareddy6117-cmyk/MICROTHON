# PQC-Migrate

PQC-Migrate is an evidence-first post-quantum cryptography migration and crypto-agility platform prototype.

## Run the local web demo

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/`. Select either **Administrator** or **Accessor (read-only)**. Administrator setup collects organization name, location, industry, security contact, initial project, and report cadence. In this prototype, the role and organization profile are stored only in browser local storage. These demo roles are not real authentication, and their UI permissions are not server authorization.

## Current scanner workflow

1. Open **Risk Analysis & Scanner** for a PDF project specification.
2. Open **Cryptographic Scanner** for PDF, ZIP, configuration, certificate, SBOM, or CBOM content.
3. Start the scan and review the report. Candidate algorithm matches include line evidence and a line hash. Suspected key material is redacted.
4. Review the risk dimensions and total USD engineering estimate. Rate and estimated hours per finding are editable before scanning; the displayed low/expected/high values are estimates, not quotes.
5. For software ZIPs, review detected source files, languages, supported package manifests, dependency names, cryptographic references, and possible secret markers. The scan is static; it does not execute code or run builds.
6. Export the full analysis as JSON, CSV, or a printable PDF.
7. Use **Policy Center** to create a project-scoped firewall policy draft. Drafts are not deployed to a network gateway.

The scanner offers **Load sample project PDF** and **Load sample software ZIP** buttons. These synthetic files contain no real credentials or customer data and are designed to demonstrate risk scoring, the cost estimate, static inventory, dependency names, and evidence exports.

Cost estimates use a 2-hour baseline plus editable expected effort per distinct file/algorithm match (default blended labor rate USD 150/hour, with legacy crypto 8 hours, classical public-key migration 16 hours, and other crypto review 3 hours per finding). The range is 75%–150% of expected effort. Licenses, vendor costs, infrastructure, testing, compatibility, and deployment are excluded. Dependency names are inventory only; no vulnerability advisory feed is configured.

The upload limit is 10 GiB per file. PDF analysis limits pages and extracted text. ZIP files are inspected in place without extracting or executing entries; their expanded scan scope is separately bounded. An installation should use a dedicated upload volume with storage quotas and a reverse-proxy body-size limit.

## Docker Compose

Set `POSTGRES_PASSWORD` in the shell or in an untracked `.env` file before starting the stack. Do not commit production credentials.

```powershell
$env:POSTGRES_PASSWORD = "use-a-local-development-password"
docker compose up --build
```

The compose stack provides PostgreSQL and Redis containers, but the current demo API workflows still do not persist scan results or policy drafts to PostgreSQL.

## Evidence and model behavior

The current upload scanner is deterministic: it parses bounded text, finds configured cryptographic patterns, and joins findings to the controlled, versioned recommendation table in `pqc_migrate/knowledge_repo.py`. Missing project fields remain unknown. Cost impact, performance, compliance conclusions, runtime reachability, and dependency blast radius are not inferred without measurement or supporting evidence.

The existing `src/crypto_llm.py` is **not a trained generative LLM**. It loads the pretrained `all-MiniLM-L6-v2` SentenceTransformer to embed reference-document chunks, retrieves the nearest chunks with FAISS, and places the retrieved text into a fixed response template. It does not fine-tune or train model weights, and no generative LLM endpoint is configured for the new risk report. The local retrieval demo does not send the source PDF to a model service.

The retrieved crypto guidance is kept as controlled local content; it is not a substitute for reviewed standards, organizational policy, or cryptographic expertise. All findings are assessments, not guarantees of quantum safety.

## Sample data and organization data

- Synthetic assets, findings, repository examples, and firewall events are seeded in a separate SQLite database at `backend/data/pqc_demo_samples.sqlite3`.
- The **Sample Data** page reads only that database. Synthetic records are not displayed in the organization dashboard.
- The database can be located elsewhere with `PQC_SAMPLE_DB_PATH`.
- The product PostgreSQL schema and migrations are separate; this backend demo does not yet persist organization scans, onboarding profiles, or policies to PostgreSQL.

## API surfaces available in this demo

- `GET /health`
- `POST /api/v1/scans/upload` (also available at `/api/v1/ingest`)
- `POST /api/v1/projects/scan`
- `POST /api/v1/deployments/report-issue`
- `POST /api/v1/deployments/scan`
- `POST /api/v1/ci/scan`
- `POST /api/v1/firewall/policies` and `GET /api/v1/firewall/policies/{policy_id}`
- `POST /api/v1/firewall/events`
- `GET /api/v1/demo/samples`
- `GET /api/v1/demo/sample-files/project.pdf`
- `GET /api/v1/demo/sample-files/software.zip`
- `GET /api/v1/audit`
- `WS /ws/events`

GitHub/GitLab cloning, real OIDC/MFA and server-enforced RBAC, PostgreSQL persistence, KMS/HSM, shared cross-device organization profiles, background worker dispatch, sandbox container execution, Envoy/OPA deployment, and production CI webhooks require their respective integrations. Unsupported data views return empty, unknown, or explicit unavailable states rather than fabricated organization records.

## Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
node --check frontend\app.js
```

See [the demo technical report](./docs/PQC-Migrate-Demo-Technical-Report.pdf) for the model explanation, security limits, seven-step validation results, and production integration checklist. Regenerate it with:

```powershell
.\.venv\Scripts\python.exe scripts\generate_demo_report.py
```

For a one-page overview of project tools and software, see [the tech-stack PDF](./docs/PQC-Migrate-Tech-Stack.pdf).
