from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional


@dataclass
class EvidenceItem:
    source: str
    detail: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    config: Optional[str] = None
    package: Optional[str] = None
    dependency: Optional[str] = None
    certificate: Optional[str] = None
    runtime_telemetry: Optional[str] = None
    confidence: float = 0.0

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "detail": self.detail,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "config": self.config,
            "package": self.package,
            "dependency": self.dependency,
            "certificate": self.certificate,
            "runtime_telemetry": self.runtime_telemetry,
            "confidence": self.confidence,
        }


def normalize_evidence(items: Iterable[dict[str, Any]]) -> List[dict[str, Any]]:
    return [EvidenceItem(**item).to_dict() for item in items if item]


def insufficient_evidence_response(finding_id: str) -> dict:
    return {
        "finding_id": finding_id,
        "classification": "INSUFFICIENT_EVIDENCE",
        "confidence": 0.0,
        "evidence": [],
        "risk": {
            "classical": "unknown",
            "quantum": "unknown",
            "implementation": "unknown",
            "configuration": "unknown",
        },
        "blast_radius": [],
        "recommended_action": "REQUEST_ADDITIONAL_EVIDENCE",
        "patch": "No patch generated. More evidence is required before remediation can proceed.",
        "sandbox_required": True,
        "validation": ["Collect source file, dependency metadata, certificate metadata, and runtime telemetry."],
        "rollback": ["Do not change production until evidence is confirmed."],
        "approval_required": True,
        "uncertainties": ["Evidence is insufficient to classify the issue with confidence."],
    }
