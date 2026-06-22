#!/usr/bin/env python3
import json
from pathlib import Path
controls = [
    {"id": "CIS-1.1", "title": "S3 bucket encryption", "status": "fail", "resource": "s3://demo-logs", "remediation": "Enable SSE-KMS"},
    {"id": "CIS-2.1", "title": "MFA on root", "status": "pass", "resource": "aws-account", "remediation": "N/A"},
]
DEMO = Path(__file__).resolve().parent.parent / "demo-data"
DEMO.mkdir(parents=True, exist_ok=True)
(DEMO / "cis_controls.json").write_text(json.dumps(controls, indent=2))
print("Seeded CIS controls")
