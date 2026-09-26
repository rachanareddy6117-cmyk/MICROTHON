from __future__ import annotations

import argparse
import json

from pqc_migrate.orchestrator import PQCOrchestrator


def main() -> None:
    parser = argparse.ArgumentParser(description="PQC-Migrate agentic crypto assessment orchestrator")
    parser.add_argument("--finding", default="RSA certificate used in TLS handshake for a business-critical service", help="Finding to assess")
    parser.add_argument("--file", default="src/crypto/config.py", help="Source file path from evidence")
    parser.add_argument("--line", default="14", help="Source line number from evidence")
    parser.add_argument("--service", default="payments-api", help="Service identifier")
    args = parser.parse_args()

    orchestrator = PQCOrchestrator()
    report = orchestrator.assess_finding(
        finding=args.finding,
        evidence=[
            {
                "source": "scanner",
                "file_path": args.file,
                "line_number": int(args.line),
                "detail": "TLS 1.2 configuration uses RSA-based certificate path and key exchange.",
            },
            {
                "source": "package",
                "file_path": "pom.xml",
                "detail": "Dependency graph includes Spring TLS and certificate management modules.",
            },
        ],
        algorithms=["RSA", "TLS"],
        runtime_context={"service": args.service, "protocol": "TLS 1.2"},
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
