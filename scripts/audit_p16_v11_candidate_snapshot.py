#!/usr/bin/env python3
"""Mechanical audit for the isolated English P1.6 v11 candidate snapshot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION
from jobhunter.analysis_service_v11 import ENGLISH_PROMPT_VERSION, qualification_list_spans


class AuditError(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def _normalize(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def audit_snapshot(path: Path, *, job_id: str) -> None:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    _require(snapshot.get("source_job_id") == job_id, f"Snapshot is not for {job_id!r}")

    status = snapshot.get("status") or {}
    _require(status.get("english_projection_present") is True, "English projection is missing")
    _require(status.get("english_analysis_present") is True, "English P1.6 candidate is missing")
    _require(
        status.get("translation_matches_english_analysis") is True,
        "English projection does not match P1.6 v11 candidate",
    )

    projection = snapshot.get("english_projection")
    analysis = snapshot.get("english_analysis")
    _require(isinstance(projection, dict), "English projection payload is missing")
    _require(isinstance(analysis, dict), "English analysis payload is missing")
    _require(
        analysis.get("prompt_version") == ENGLISH_PROMPT_VERSION,
        f"Expected {ENGLISH_PROMPT_VERSION}, got {analysis.get('prompt_version')!r}",
    )
    _require(
        analysis.get("schema_version") == ANALYSIS_SCHEMA_VERSION,
        f"Expected schema {ANALYSIS_SCHEMA_VERSION}",
    )
    _require(
        analysis.get("translation_artifact_id") == projection.get("artifact_id"),
        "P1.6 v11 candidate references a different English projection",
    )

    payload = analysis.get("analysis") or {}
    requirements = payload.get("requirements") or []
    responsibilities = payload.get("responsibilities") or []
    coverage = payload.get("coverage") or []
    _require(isinstance(requirements, list), "requirements must be a list")
    _require(isinstance(responsibilities, list), "responsibilities must be a list")
    _require(isinstance(coverage, list), "coverage must be a list")

    fields = projection.get("fields") or {}
    skills = fields.get("skills") or []
    _require(isinstance(skills, list), "projection skills must be a list")
    structured_skills = [
        item.strip() for item in skills if isinstance(item, str) and item.strip()
    ]
    qualification_spans = qualification_list_spans(fields)

    requirements_by_evidence: dict[str, list[dict[str, Any]]] = {}
    for item in requirements:
        _require(isinstance(item, dict), "requirement item is malformed")
        evidence = str(item.get("evidence") or "")
        requirements_by_evidence.setdefault(_normalize(evidence), []).append(item)

    for skill in structured_skills:
        matches = requirements_by_evidence.get(_normalize(skill), [])
        _require(bool(matches), f"Structured skill is missing from requirements: {skill!r}")
        _require(
            any(item.get("requirement_type") == "required" for item in matches),
            f"Structured skill did not preserve required strength: {skill!r}",
        )

    for span in qualification_spans:
        _require(
            _normalize(span) in requirements_by_evidence,
            f"Qualification-list item is missing from requirements: {span!r}",
        )

    coverage_by_evidence = {
        _normalize(str(item.get("evidence") or "")): item
        for item in coverage
        if isinstance(item, dict)
    }
    for expected in [*structured_skills, *qualification_spans]:
        decision = coverage_by_evidence.get(_normalize(expected))
        _require(
            bool(decision and decision.get("disposition") == "extracted_requirement"),
            f"Missing deterministic extracted-requirement coverage: {expected!r}",
        )

    requirement_evidence = set(requirements_by_evidence)
    qualification_evidence = {_normalize(item) for item in qualification_spans}
    for index, item in enumerate(responsibilities):
        _require(isinstance(item, dict), f"responsibility[{index}] is malformed")
        statement = _normalize(str(item.get("statement") or ""))
        evidence = _normalize(str(item.get("evidence") or ""))
        _require(
            evidence not in requirement_evidence,
            f"responsibility[{index}] reuses exact qualification evidence",
        )
        _require(
            evidence not in qualification_evidence,
            f"responsibility[{index}] uses qualification-list evidence as work",
        )
        _require(
            not (statement and f"ability to {statement}" in evidence),
            f"responsibility[{index}] paraphrases ability-to qualification wording",
        )

    print("Mechanical P1.6 v11 candidate checks: PASS")
    print(f"Snapshot: {path.as_posix()}")
    print(f"Job: {job_id}")
    print(f"Artifact: {analysis.get('artifact_id')}")
    print(f"Requirements: {len(requirements)}")
    print(f"Responsibilities: {len(responsibilities)}")
    print(f"Structured required skills covered: {len(structured_skills)}/{len(structured_skills)}")
    print(f"Qualification-list items covered: {len(qualification_spans)}/{len(qualification_spans)}")
    print(f"Coverage decisions: {len(coverage)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit one isolated English P1.6 v11 candidate snapshot."
    )
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--snapshot", type=Path, default=None)
    args = parser.parse_args()
    path = args.snapshot or Path("review-snapshots/jobs") / f"{args.job_id}.json"
    try:
        audit_snapshot(path, job_id=args.job_id)
    except (AuditError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Mechanical P1.6 v11 candidate checks: FAIL: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
