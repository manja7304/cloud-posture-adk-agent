"""ADK-style tool-calling cloud posture agent."""

from __future__ import annotations

import json

from src.tools.cis_tools import check_cis_control, list_controls, format_findings


def run_agent(query: str, context: dict | None = None) -> dict:
    trace = []
    controls = json.loads(list_controls.invoke(""))
    trace.append({"tool": "list_controls", "count": len(controls)})
    target = (context or {}).get("control_id", controls[0]["id"] if controls else "CIS-1.1")
    raw = json.loads(check_cis_control.invoke(target))
    trace.append({"tool": "check_cis_control", "control_id": target, "result": raw})
    findings = json.loads(format_findings.invoke(json.dumps([raw])))
    trace.append({"tool": "format_findings", "output": findings})
    return {"answer": f"Posture check complete: {len(findings.get('findings', []))} findings", "trace": trace, "metadata": findings}
