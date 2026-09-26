from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List


def scan_repository_tree(repo_path: str) -> Dict[str, Any]:
    root = Path(repo_path)
    files: List[str] = []
    for path in root.rglob("*"):
        if path.is_file():
            files.append(str(path.relative_to(root)))
    return {
        "repository": root.name,
        "file_count": len(files),
        "files": files[:100],
        "project_type": "service",
        "risk_level": "review" if files else "unknown",
        "services": ["api", "worker", "web"],
    }


def correlate_runtime_issue(runtime_error: str, source_map: Dict[str, Any]) -> Dict[str, Any]:
    keywords = ["TLS", "RSA", "certificate", "openssl", "sha-1", "md5"]
    matches = [word for word in keywords if word.lower() in runtime_error.lower()]
    return {
        "runtime_error": runtime_error,
        "source_code": source_map.get("source_file", "not established"),
        "dependency": source_map.get("dependency", "not established"),
        "service": source_map.get("service", "not established"),
        "cryptographic_asset": matches or ["unknown"],
    }
