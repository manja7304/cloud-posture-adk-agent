"""Mock CIS benchmark API tools (ADK-style structured output)."""

from __future__ import annotations

import json
from pathlib import Path

from langchain_core.tools import tool

DEMO = Path(__file__).resolve().parent.parent.parent / "demo-data"


@tool
def list_controls(_: str = "") -> str:
    """List available CIS benchmark controls from mock API."""
    data = json.loads((DEMO / "cis_controls.json").read_text(encoding="utf-8"))
    return json.dumps(data)


@tool
def check_cis_control(control_id: str) -> str:
    """Check a single CIS control against mock cloud posture data."""
    controls = json.loads((DEMO / "cis_controls.json").read_text(encoding="utf-8"))
    for c in controls:
        if c["id"] == control_id:
            return json.dumps({
                "control_id": control_id,
                "status": c.get("status", "fail"),
                "resource": c.get("resource", "s3://demo-bucket"),
                "remediation": c.get("remediation", "Enable encryption"),
            })
    return json.dumps({"error": "unknown control"})


@tool
def format_findings(raw_json: str) -> str:
    """Format raw control results into structured findings JSON."""
    items = json.loads(raw_json)
    if isinstance(items, dict):
        items = [items]
    return json.dumps({
        "findings": items,
        "severity_counts": {"fail": sum(1 for i in items if i.get("status") == "fail")},
    })
