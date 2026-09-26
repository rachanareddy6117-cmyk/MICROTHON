from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pymupdf


OUTPUT = Path(__file__).resolve().parents[1] / "docs" / "PQC-Migrate-Demo-Technical-Report.pdf"
PAGE_WIDTH = 595
PAGE_HEIGHT = 842
LEFT = 58
RIGHT = 537
BOTTOM = 772
BODY_SIZE = 9.5
BODY_COLOR = (0.13, 0.20, 0.27)
NAVY = (0.035, 0.075, 0.13)
TEAL = (0.08, 0.72, 0.67)
MUTED = (0.42, 0.51, 0.58)


SECTIONS = [
    (
        "What was delivered",
        [
            "The local web demo now has a public landing and demo-role selector, first-run organization setup, a combined cryptographic inventory/findings scanner, a PDF project-risk workflow, and a project-scoped firewall policy builder.",
            "The organization profile, scan history, and role selector are stored in browser local storage. Administrator and accessor are demonstration modes only; they are not server-authenticated identities, and the UI role is not an authorization boundary.",
            "The project PDF flow extracts scope, technology, timeline, budget, vendors, dependencies, and security requirements when the document contains evidence. It reports explicit unknown or insufficient-evidence states for absent data and offers JSON and print-to-PDF exports.",
            "The crypto scanner accepts PDF, ZIP, JSON/YAML, PEM/CRT, SBOM, and CBOM inputs. Findings include candidate algorithm matches, source file and line, redacted evidence where relevant, and a SHA-256 line hash. The report can be exported as JSON, CSV, or printed to PDF.",
            "The policy center builds a project-specific policy artifact, allows preview and draft save, and groups firewall events, CI/CD guard, and secure-data status in one place. A saved draft is not enforced by a live gateway and is not a production deployment.",
            "Synthetic repository, crypto asset, finding, and firewall event records are kept in a separate SQLite sample database and shown in the Sample Data view. They are not mixed into the organization scan history.",
            "Deployment issue intake accepts a reported issue and repository reference. It does not clone the repository or invent source/dependency correlations when those relationships have not been scanned.",
        ],
    ),
    (
        "Model and analysis behavior",
        [
            "Important correction: this project has no fine-tuned or trained generative LLM. No model weights were trained, and no generative LLM API endpoint is configured for the risk-analysis or scanner workflows.",
            "The existing LocalCryptoLLM class is a local retrieval demo. It extracts PDF text with PyMuPDF, cleans the text, splits it into sentence-based chunks (250 characters with 40 characters of overlap), and embeds those chunks using the pretrained all-MiniLM-L6-v2 SentenceTransformer.",
            "The embedding vectors are normalized and indexed by FAISS IndexFlatIP. A question is embedded using the same pretrained encoder; the default top three similar reference chunks are retrieved and placed into a fixed response template. This is retrieval-augmented text assembly, not original generative reasoning or supervised training.",
            "The local demo was run against the provided crypto_flaws_and_fixes.pdf reference. It returned text about poor key management, weak padding, random number generation, and timing side channels. The run emitted a Hugging Face Hub unauthenticated-request warning while loading model weights; inference did complete. The source PDF was processed locally and was not sent as a prompt to a generative service.",
            "The upload scanner is deterministic pattern matching joined to the controlled recommendation data in pqc_migrate/knowledge_repo.py. It does not infer runtime reachability, validated financial cost, performance impact, complete certificate metadata, or dependency blast radius without dedicated evidence.",
            "Therefore the system does not claim that its advice is exhaustive, that estimates are measured, or that a system is quantum safe. Review candidate matches against current standards, implementation documentation, and organizational policy.",
        ],
    ),
    (
        "Upload safety and resource limits",
        [
            "Uploaded repository content is read as data only. ZIP entries are never extracted to the filesystem and uploaded scripts are never run. Archive names are checked for absolute paths, drive prefixes, and parent traversal.",
            "The configured upload cap is 10 GiB per file. PDF analysis is limited to 500 pages and 2,000,000 extracted characters. ZIP analysis is bounded to 20,000 entries, 2 GiB expanded size, 512 MiB of scanned text, and 5 MiB per text entry.",
            "Possible private-key blocks and credential assignments are redacted from displayed evidence. A SHA-256 hash is supplied for source-line correlation; it is not a signature or proof that a finding is valid.",
            "The application stages uploads in a temporary file and removes the staged file after processing. Production deployment still needs reverse-proxy request limits, quotas and retention controls for the upload volume, concurrency limits, background workers, and isolated scan containers.",
            "The 10 GiB application setting alone does not guarantee that a 10 GiB request can pass through a browser, proxy, hosting platform, or operating system. Those infrastructure limits must be configured and tested independently.",
        ],
    ),
    (
        "Seven-step validation",
        [
            "1. Static source checks - node --check frontend/app.js exited successfully. Pylance reported no Python syntax errors in backend/app/main.py or src/crypto_llm.py, and no diagnostics remained in those checked Python files.",
            "2. Dependency consistency - .venv Python -m pip check completed with: No broken requirements found.",
            "3. Automated tests - the full pytest suite completed with 22 passed. One non-fatal Starlette deprecation warning remains: its TestClient integration with httpx is deprecated and recommends httpx2.",
            "4. Local reference retrieval - the original PDF was passed to src/crypto_llm.py. The all-MiniLM-L6-v2 encoder loaded, the FAISS retrieval returned relevant PDF passages, and the command completed. This validates retrieval execution, not model training or answer completeness.",
            "5. Project risk PDF flow - the original PDF was uploaded in the browser and produced a REVIEW_REQUIRED report. Presently absent scope, budget, vendors, dependency, and security fields remained unknown or insufficient evidence; cost was not fabricated; the report disclosed that no generative LLM was configured.",
            "6. Cryptographic PDF scan - the original PDF was scanned in the browser. The saved scan summary contained 79 candidate evidence items across 16 observed labels: 3DES, AES, DES, DH, ECC, HMAC, MD5, ML-DSA, ML-KEM, RC4, RSA, SHA-1, SHA-2, SHA-3, SLH-DSA, and TLS. Candidate matches still require validation.",
            "7. Integrated UI and API - the landing page and both demo-role selections were exercised. The accessor Settings screen had disabled profile controls and no save action. All 18 workspace navigation views rendered with zero captured page errors. GET /api/v1/demo/samples returned HTTP 200 with 6 assets, 3 findings, 3 firewall events, and 2 repositories. A policy for Seven-step validation was saved with a UUID and explicitly remained draft/not deployed.",
        ],
    ),
    (
        "Current boundaries and production work",
        [
            "Persistence: organization setup, scan summaries, and policy drafts are not persisted to the product PostgreSQL database. Organization preferences live in this browser; firewall draft storage is local/in-memory demo state and can disappear after a restart.",
            "Identity and access: demo role selection is client-side. Add OIDC/JWT, MFA, server-side RBAC, tenant isolation, CSRF protections where applicable, and audited authorization before protecting real customer data.",
            "Integrations: GitHub/GitLab OAuth and cloning, real deployment telemetry, background job dispatch, remediation containers, KMS/HSM envelope encryption, a generative LLM, and an Envoy/OPA enforcement gateway are not configured.",
            "Analysis completeness: text matching is not a full language-semantic scanner. Certificate parsing, dynamic algorithm flow, wrapper resolution, transitive package graphs, service blast radius, and compatibility/performance tests require dedicated integrations and real repository evidence.",
            "Automation: selected report cadence is currently a saved preference, not a scheduled report job. The policy output is a reviewable draft, not an automatically deployed firewall. High-impact changes must remain approval-gated.",
            "Before production, connect persistent storage and job infrastructure; enforce proxy and worker resource limits; integrate identity, KMS/HSM, repository providers, vetted scanning and sandbox images, policy gateways, retention controls, monitoring, and disaster recovery; then repeat the adversarial suite in the target deployment environment.",
        ],
    ),
    (
        "Run the local demo",
        [
            r"From the repository root, start the app with: .venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000",
            "Open http://127.0.0.1:8000/. Select Administrator for the organization setup and policy draft demo, or Accessor for the read-only profile view. Do not use these local roles to protect real data.",
            r"Run tests with: .venv\Scripts\python.exe -m pytest -q",
            r"Check frontend syntax with: node --check frontend\app.js",
            r"Regenerate this report with: .venv\Scripts\python.exe scripts\generate_demo_report.py",
            "The report records the observed state of this local prototype. It is not a compliance attestation, a penetration-test report, or a production-readiness certification.",
        ],
    ),
]


def new_page(document: pymupdf.Document, title: str, subtitle: str | None = None) -> pymupdf.Page:
    page = document.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    page.draw_rect(pymupdf.Rect(0, 0, PAGE_WIDTH, 58), color=NAVY, fill=NAVY)
    page.insert_text((LEFT, 36), "PQC-MIGRATE  /  DEMO TECHNICAL REPORT", fontsize=10, fontname="hebo", color=(1, 1, 1))
    page.insert_text((LEFT, 95), title, fontsize=21, fontname="hebo", color=NAVY)
    if subtitle:
        page.insert_text((LEFT, 119), subtitle, fontsize=9.5, fontname="helv", color=MUTED)
    return page


def wrapped_lines(text: str, max_width: float) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and pymupdf.get_text_length(candidate, fontname="helv", fontsize=BODY_SIZE) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def add_footer(page: pymupdf.Page, page_number: int, page_count: int) -> None:
    page.draw_line((LEFT, 805), (RIGHT, 805), color=(0.82, 0.87, 0.90), width=0.6)
    page.insert_text((LEFT, 823), "PQC-Migrate prototype · evidence-grounded demo · not a production security guarantee", fontsize=8, fontname="helv", color=MUTED)
    page.insert_text((RIGHT - 46, 823), f"{page_number} / {page_count}", fontsize=8, fontname="helv", color=MUTED)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = pymupdf.open()
    cover = document.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    cover.draw_rect(pymupdf.Rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT), color=NAVY, fill=NAVY)
    cover.draw_rect(pymupdf.Rect(0, 0, PAGE_WIDTH, 12), color=TEAL, fill=TEAL)
    cover.insert_text((LEFT, 115), "PQC-MIGRATE", fontsize=14, fontname="hebo", color=TEAL)
    cover.insert_textbox(
        pymupdf.Rect(LEFT, 164, RIGHT, 280),
        "Demo Runbook &\nTechnical Validation Report",
        fontsize=30,
        fontname="hebo",
        color=(1, 1, 1),
        lineheight=1.18,
    )
    cover.insert_textbox(
        pymupdf.Rect(LEFT, 310, RIGHT, 390),
        "Post-quantum migration · crypto-agility · evidence-first scanning · project-specific policy drafts",
        fontsize=13,
        fontname="helv",
        color=(0.76, 0.84, 0.88),
        lineheight=1.4,
    )
    cover.draw_line((LEFT, 435), (RIGHT, 435), color=TEAL, width=1.4)
    cover.insert_text((LEFT, 475), f"Generated: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}", fontsize=10, fontname="helv", color=(1, 1, 1))
    cover.insert_text((LEFT, 508), "Validation result: 22 tests passed; seven demo validation steps recorded.", fontsize=10, fontname="helv", color=(1, 1, 1))
    cover.insert_textbox(
        pymupdf.Rect(LEFT, 590, RIGHT, 710),
        "Important model disclosure: the current system does not contain a trained generative LLM. It includes a local PDF retrieval demo and a deterministic, evidence-based scanner. Unknown cost, performance, dependency, and runtime facts are intentionally not fabricated.",
        fontsize=11,
        fontname="helv",
        color=(0.84, 0.89, 0.91),
        lineheight=1.5,
    )

    for title, paragraphs in SECTIONS:
        page = new_page(document, title)
        y = 151
        for paragraph in paragraphs:
            bullet = paragraph[0].isdigit() and paragraph[1:3] == ". "
            prefix = "" if bullet else "• "
            lines = wrapped_lines(prefix + paragraph, RIGHT - LEFT)
            needed = len(lines) * 14 + 8
            if y + needed > BOTTOM:
                page = new_page(document, f"{title} (continued)")
                y = 151
            for line in lines:
                page.insert_text((LEFT, y), line, fontsize=BODY_SIZE, fontname="helv", color=BODY_COLOR)
                y += 14
            y += 8

    page_count = len(document)
    for number, page in enumerate(document, start=1):
        if number > 1:
            add_footer(page, number, page_count)
    document.set_metadata(
        {
            "title": "PQC-Migrate Demo Runbook and Technical Validation Report",
            "author": "PQC-Migrate",
            "subject": "Seven-step demo validation, model disclosure, security controls, and production limitations",
        }
    )
    document.save(OUTPUT, garbage=4, deflate=True)
    document.close()
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
