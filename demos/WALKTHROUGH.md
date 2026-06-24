# Demo Walkthrough — Cloud Posture ADK Agent

**Pattern:** Google ADK Tool Calling  
**Captured:** 2026-06-24 with `USE_MOCK_LLM=true` (no Docker/Ollama required)

---

## Prerequisites

```bash
cp .env.example .env   # optional for mock demo
pip install -r requirements.txt
```

---

## Step 1 — One-command demo

```bash
export USE_MOCK_LLM=true
python scripts/run_demo.py
```

This runs the same FastAPI `TestClient` path as CI — real code, real JSON output.

### Step 2 — Agent API call

```bash
curl -X POST http://localhost:8080/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{"query": "check posture", "context": {"control_id": "CIS-1.1"}}'
```

Or offline (no server):

```bash
USE_MOCK_LLM=true python scripts/run_demo.py
```

**Request (`demos/captured/request.json`):**

```json
{
  "query": "check posture",
  "context": {
    "control_id": "CIS-1.1"
  }
}
```

**Response (`demos/captured/response.json`):**

```json
{
  "answer": "Posture check complete: 1 findings",
  "trace": [
    {
      "tool": "list_controls",
      "count": 2
    },
    {
      "tool": "check_cis_control",
      "control_id": "CIS-1.1",
      "result": {
        "control_id": "CIS-1.1",
        "status": "fail",
        "resource": "s3://demo-logs",
        "remediation": "Enable SSE-KMS"
      }
    },
    {
      "tool": "format_findings",
      "output": {
        "findings": [
          {
            "control_id": "CIS-1.1",
            "status": "fail",
            "resource": "s3://demo-logs",
            "remediation": "Enable SSE-KMS"
          }
        ],
        "severity_counts": {
          "fail": 1
        }
      }
    }
  ],
  "metadata": {
    "findings": [
      {
        "control_id": "CIS-1.1",
        "status": "fail",
        "resource": "s3://demo-logs",
        "remediation": "Enable SSE-KMS"
      }
    ],
    "severity_counts": {
      "fail": 1
    }
  }
}
```

### Step 3 — Agent trace excerpt

```json
[
  {
    "tool": "list_controls",
    "count": 2
  },
  {
    "tool": "check_cis_control",
    "control_id": "CIS-1.1",
    "result": {
      "control_id": "CIS-1.1",
      "status": "fail",
      "resource": "s3://demo-logs",
      "remediation": "Enable SSE-KMS"
    }
  }
]
```

---

## Architecture callout (2-min video)

> Google ADK-style tool-calling agent scanning CIS controls against synthetic cloud posture fixtures.

Highlight in your recording:

1. **Problem → pattern** — why this agent architecture fits the security domain
2. **Tool/trace output** — show structured JSON, not just the final answer
3. **`docs/architecture.md`** — Mermaid diagram for the close

---

## Artifacts

| File | Description |
|------|-------------|
| [`demos/captured/request.json`](captured/request.json) | API request payload |
| [`demos/captured/response.json`](captured/response.json) | Live captured response |
| [`demos/captured/trace.json`](captured/trace.json) | Agent trace array |
| [`demos/captured/terminal-session.txt`](captured/terminal-session.txt) | Terminal replay for Loom |

---

## Record your video

```bash
python scripts/run_demo.py
```

Use [`demos/RECORDING_SCRIPT.md`](RECORDING_SCRIPT.md) for shot list and narration cues.
