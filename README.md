# Cloud Posture ADK Agent

![CI](https://github.com/manja7304/cloud-posture-adk-agent/actions/workflows/ci.yml/badge.svg)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue)
![Google ADK](https://img.shields.io/badge/Google_ADK-Tool_Calling-4285F4)
![LangChain](https://img.shields.io/badge/LangChain-Tools-1C3C3C)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Docker](https://img.shields.io/badge/Docker-Ollama-blue)
![CIS](https://img.shields.io/badge/CIS-Controls-blue)

> **ADK-style tool-calling agent** for CSPM — list CIS controls, check compliance posture, format structured findings JSON with severity counts. **2 CIS controls** with pass/fail over synthetic cloud fixtures.

---

## Problem Statement

Cloud security posture management (CSPM) tools flood teams with misconfiguration alerts — public S3 buckets, missing MFA on root accounts, overly permissive IAM policies — but findings arrive as unstructured text unsuitable for ticketing systems or executive dashboards. Security engineers manually reformat CSPM output for Jira and compliance reports. This agent demonstrates **structured tool-calling** that returns machine-readable findings with severity counts.

---

## Why This Architecture

Raw LLM cloud audits hallucinate control IDs and misstate pass/fail status. An **ADK-style sequential tool pipeline** (`list_controls` → `check_cis_control` → `format_findings`) invokes LangChain `@tool` functions against grounded CIS fixture data — deterministic, testable, returns `severity_counts` in metadata. Compared to polling AWS Config APIs, this pattern shows how agent tool-calling wraps CSPM checks with structured output — the same pattern Google ADK uses for cloud agents, implemented with LangChain tools for portfolio portability.

---

## Architecture

```mermaid
flowchart TB
  Engineer[Cloud Security Engineer] --> API[FastAPI :8080]
  API --> Agent[ADK-style Tool Pipeline]
  Agent --> List[list_controls]
  List --> Check[check_cis_control]
  Check --> Format[format_findings]
  List & Check --> CIS[(cis_controls.json\n2 controls)]
  Format --> Output[findings + severity_counts]
```

---

## Agent Flow

```mermaid
sequenceDiagram
  participant Eng as Cloud Engineer
  participant API as FastAPI
  participant Agent as runner.py
  participant Tools as cis_tools.py
  participant Data as cis_controls.json

  Eng->>API: POST {"query": "check posture", "context": {"control_id": "CIS-1.1"}}
  API->>Agent: run_agent()
  Agent->>Tools: list_controls()
  Tools->>Data: load 2 CIS controls
  Data-->>Tools: CIS-1.1, CIS-2.1
  Agent->>Tools: check_cis_control("CIS-1.1")
  Tools-->>Agent: status: fail (S3 encryption)
  Agent->>Tools: format_findings(results)
  Tools-->>Agent: structured JSON + severity_counts
  Agent-->>API: answer + trace + metadata
  API-->>Eng: JSON response
```

---

## Design Patterns

| Pattern | Where Used | Why | Alternative Considered |
|---------|------------|-----|------------------------|
| ADK-style Tool Calling | `cis_tools.py` `@tool` + `.invoke()` | Structured CSPM actions with typed I/O | Raw LLM cloud audit |
| Sequential Tool Pipeline | `runner.py` | list → check → format mirrors ADK agent flow | Single monolithic prompt |
| Control ID Routing | `context.control_id` | Target specific CIS check | Check all controls always |
| Structured Findings JSON | `format_findings` | Ticket-system ready output | Free-text report |
| Severity Aggregation | `severity_counts` in metadata | Executive dashboard ready | Per-finding only |

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Runtime | Python 3.11 | Agent pipeline |
| Tools | LangChain `@tool` | `list_controls`, `check_cis_control`, `format_findings` |
| API | FastAPI + Uvicorn | `POST /api/v1/agent/run` |
| LLM | Ollama llama3.2 (factory, unused in path) | Future NL explanations |
| Data | JSON | 2 CIS control fixtures |
| Quality | pytest (3 tests) + ruff | CIS-1.1 trace assertion |
| Infra | Docker Compose (app + ollama) | Port 8080 |

---

## Quickstart

```bash
cp .env.example .env
docker compose -f docker/docker-compose.yml up --build
```

```bash
curl -X POST http://localhost:8080/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{"query": "Check cloud security posture", "context": {"control_id": "CIS-1.1"}}'
```

**Expected output (abbreviated):**

```json
{
  "answer": "CIS posture check complete. 1 fail, 1 pass.",
  "trace": [
    {"tool": "list_controls", "output": {"controls": ["CIS-1.1", "CIS-2.1"]}},
    {"tool": "check_cis_control", "output": {"control_id": "CIS-1.1", "status": "fail", "finding": "S3 bucket encryption not enabled"}},
    {"tool": "format_findings", "output": {"findings": [...], "severity_counts": {"fail": 1, "pass": 1}}}
  ],
  "metadata": {"severity_counts": {"fail": 1, "pass": 1}}
}
```

---

## Demo Data

| Path | Count | Controls | Generation |
|------|-------|----------|------------|
| `demo-data/cis_controls.json` | **2 controls** | CIS-1.1 (S3 encryption, **fail**), CIS-2.1 (MFA root, **pass**) | `python scripts/seed_demo_data.py` |

---

## Evaluation & Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Unit tests | **3** | API + CIS-1.1 trace assertion |
| CIS controls | 2 | Pass/fail coverage |
| Findings format | Structured JSON | `severity_counts` in metadata |
| CI | ruff + pytest + Docker build | Mock LLM |
| P95 latency | **< 350ms** | Tool chain, no LLM |

---

## System Design Highlights

- **ADK-style tool-calling pattern** — list → check → format pipeline
- **Structured findings with severity counts** — dashboard and ticket integration ready
- **CIS control ID routing** via `context.control_id`
- **Pass/fail fixture data** — realistic CSPM narrative without cloud API keys
- **Full tool trace** on every response for audit

---

## Video Demo

[![Demo Video](https://img.shields.io/badge/Demo-YouTube-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/watch?v=PLACEHOLDER)

> Record using [`demos/RECORDING_SCRIPT.md`](demos/RECORDING_SCRIPT.md).

---

## Security & Ethics

- **Synthetic CIS fixtures only** — no live AWS/Azure API calls
- No unauthorized cloud account access
- See [SECURITY.md](SECURITY.md)

---

## Part of Cyber AI Portfolio

| # | Project | Pattern | Repo |
|:-:|---------|---------|------|
| 0 | Project Template | Shared Scaffold | [cyber-ai-project-template](https://github.com/manja7304/cyber-ai-project-template) |
| 1 | CVE Triage Agent | Tool Pipeline + LangGraph | [cyber-cve-triage-react](https://github.com/manja7304/cyber-cve-triage-react) |
| 2 | SOC Analyst Supervisor Swarm | Supervisor Router | [soc-analyst-supervisor-swarm](https://github.com/manja7304/soc-analyst-supervisor-swarm) |
| 3 | Pentest Plan-Execute Orchestrator | Plan-and-Execute + Checkpointing | [pentest-plan-execute-orchestrator](https://github.com/manja7304/pentest-plan-execute-orchestrator) |
| 4 | OWASP Agentic RAG Assistant | Agentic RAG + Self-Correction | [owasp-agentic-rag-assistant](https://github.com/manja7304/owasp-agentic-rag-assistant) |
| 5 | Secure Code Reflection Reviewer | Reflection / Self-Critique | [secure-code-reflection-reviewer](https://github.com/manja7304/secure-code-reflection-reviewer) |
| 6 | Red Team Strike Crew | Role-based Crew Pipeline | [redteam-strike-crew](https://github.com/manja7304/redteam-strike-crew) |
| 7 | GRC Evidence Collection Crew | Sequential Compliance Crew | [grc-evidence-collection-crew](https://github.com/manja7304/grc-evidence-collection-crew) |
| 8 | **Cloud Posture ADK Agent** | ADK-style Tool Calling | **you are here** |
| 9 | Threat Intel Graph RAG | Graph RAG + Hybrid Retrieval | [threat-intel-graph-rag](https://github.com/manja7304/threat-intel-graph-rag) |
| 10 | Incident Response HITL Copilot | Human-in-the-Loop + Audit Log | [incident-response-hitl-copilot](https://github.com/manja7304/incident-response-hitl-copilot) |

---

## Author

**[Manjunath KG](https://github.com/manja7304)** — AI/ML Trainee Engineer at **Ampcus Cyber**, Bengaluru.
