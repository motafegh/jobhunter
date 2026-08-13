#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jobhunter.p16_v13_audit import AuditError, audit_snapshot


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--snapshot", type=Path, default=None)
    args = parser.parse_args()
    path = args.snapshot or Path("review-snapshots/jobs") / f"{args.job_id}.json"
    try:
        result = audit_snapshot(path, job_id=args.job_id)
    except (AuditError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Mechanical P1.6 v13 candidate checks: FAIL: {exc}")
        return 1
    print("Mechanical P1.6 v13 candidate checks: PASS")
    print(f"Snapshot: {path.as_posix()}")
    print(f"Job: {args.job_id}")
    print(f"Artifact: {result['artifact_id']}")
    print(f"Requirements: {result['requirements']}")
    print(f"Responsibilities: {result['responsibilities']}")
    print(
        "Structured required skills covered: "
        f"{result['structured_skills']}/{result['structured_skills']}"
    )
    print(
        "Qualification-list items covered: "
        f"{result['qualification_spans']}/{result['qualification_spans']}"
    )
    print(f"Decomposed coarse coverage decisions: {result['decomposed']}")
    print(f"Coverage decisions: {result['coverage']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
