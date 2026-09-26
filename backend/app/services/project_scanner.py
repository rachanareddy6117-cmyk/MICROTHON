from __future__ import annotations

import re
from typing import Any, Dict, List


def extract_project_risk(spec_text: str) -> Dict[str, Any]:
    text = spec_text or ""
    scope = re.search(r"scope[:\s]+([^\n]+)", text, re.IGNORECASE)
    technology = re.findall(r"technology[:\s]+([^\n]+)", text, flags=re.IGNORECASE)
    budget = re.search(r"budget[:\s]+([^\n]+)", text, re.IGNORECASE)
    timeline = re.search(r"timeline[:\s]+([^\n]+)", text, re.IGNORECASE)
    vendors = re.findall(r"vendor(?:s)?[:\s]+([^\n]+)", text, re.IGNORECASE)
    risks = re.findall(r"risk(?:s)?[:\s]+([^\n]+)", text, re.IGNORECASE)
    dependencies = re.findall(r"dependenc(?:y|ies)[:\s]+([^\n]+)", text, re.IGNORECASE)
    security_requirements = re.findall(
        r"security requirements?[:\s]+([^\n]+)", text, re.IGNORECASE
    )

    return {
        "scope": scope.group(1).strip() if scope else "unknown",
        "technology": [item.strip() for item in technology[0].split(",")] if technology else [],
        "budget": budget.group(1).strip() if budget else "unknown",
        "timeline": timeline.group(1).strip() if timeline else "unknown",
        "vendors": [item.strip() for vendor in vendors for item in vendor.split(",")] if vendors else [],
        "dependencies": [item.strip() for dependency in dependencies for item in dependency.split(",")] if dependencies else [],
        "security_requirements": [
            item.strip()
            for requirement in security_requirements
            for item in requirement.split(",")
        ] if security_requirements else [],
        "risks": [item.strip() for risk in risks for item in risk.split(",")] if risks else [],
    }


def build_project_scan_result(spec_text: str) -> Dict[str, Any]:
    profile = extract_project_risk(spec_text)
    risk_score = 0
    if "RSA" in " ".join(profile["risks"]).upper() or "legacy" in " ".join(profile["risks"]).lower():
        risk_score += 30
    if "certificate" in " ".join(profile["risks"]).lower():
        risk_score += 20
    return {
        "risk_score": min(risk_score, 100),
        "profile": profile,
        "status": (
            "insufficient_evidence"
            if not any(value not in ("unknown", [], None) for value in profile.values())
            else "review" if risk_score >= 30 else "ok"
        ),
    }
