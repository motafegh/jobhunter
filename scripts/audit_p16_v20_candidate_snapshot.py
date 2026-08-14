#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jobhunter.p16_v20_audit import AuditError, audit_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit isolated English P1.6 v20 candidate snapshot."
    )
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--snapshot", type=Path, default=None)
    args = parser.parse_args()
    path = args.snapshot or Path("review-snapshots/jobs") / f"{args.job_id}.json"
    try:
        result = audit_snapshot(path, job_id=args.job_id)
    except (AuditError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Mechanical P1.6 v20 candidate checks: FAIL: {exc}")
        return 1
    print("Mechanical P1.6 v20 candidate checks: PASS")
    print(f"Snapshot: {path.as_posix()}")
    print(f"Job: {args.job_id}")
    print(f"Artifact: {result['artifact_id']}")
    print(f"Requirements: {result['requirements']}")
    print(f"Responsibilities: {result['responsibilities']}")
    print(f"Role purpose statements: {result['role_purpose']}")
    structured = result["structured_skills"]
    qualifications = result["qualification_spans"]
    residuals = result["residual_spans"]
    print(f"Structured required skills covered: {structured}/{structured}")
    print(f"Qualification-list items covered: {qualifications}/{qualifications}")
    print(f"Residual coverage decisions: {residuals}/{residuals}")
    print(f"Decomposed coarse coverage decisions: {result['decomposed']}")
    print(f"Coverage decisions: {result['coverage']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
