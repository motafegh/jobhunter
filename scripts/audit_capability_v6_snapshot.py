"""Audit the live Capability v6 review snapshot used for B3 acceptance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

EXPECTED_PROMPT_VERSION = "job-capability-intelligence-v6"
EXPECTED_SCHEMA_VERSION = "job-capability-intelligence-v3"
DEFAULT_JOB_ID = "tG9K"
DEFAULT_ANALYSIS_ARTIFACT_ID = 29


class AuditError(RuntimeError):
    """Raised when the snapshot violates a mechanically checkable v6 invariant."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def _expected_strength(
    requirement_indices: list[int],
    requirements: list[dict[str, Any]],
) -> str:
    strengths = {
        requirements[index].get("requirement_type")
        for index in requirement_indices
        if requirements[index].get("requirement_type")
    }
    if not strengths:
        return "unspecified"
    if len(strengths) == 1:
        return next(iter(strengths))
    return "mixed"


def audit_snapshot(
    path: Path,
    *,
    job_id: str,
    expected_analysis_artifact_id: int,
) -> None:
    snapshot = json.loads(path.read_text(encoding="utf-8"))

    _require(snapshot.get("source_job_id") == job_id, f"Snapshot is not for {job_id!r}")

    status = snapshot.get("status") or {}
    analysis = snapshot.get("english_analysis")
    capability = snapshot.get("capability_intelligence")

    _require(isinstance(analysis, dict), "Missing English P1.6 analysis")
    _require(
        analysis.get("artifact_id") == expected_analysis_artifact_id,
        "Expected accepted P1.6 artifact "
        f"{expected_analysis_artifact_id}, got {analysis.get('artifact_id')!r}",
    )
    _require(isinstance(capability, dict), "Missing dependency-current Capability artifact")
    _require(
        capability.get("prompt_version") == EXPECTED_PROMPT_VERSION,
        f"Expected {EXPECTED_PROMPT_VERSION}, got {capability.get('prompt_version')!r}",
    )
    _require(
        capability.get("schema_version") == EXPECTED_SCHEMA_VERSION,
        f"Expected {EXPECTED_SCHEMA_VERSION}, got {capability.get('schema_version')!r}",
    )
    _require(
        status.get("capability_is_current_chain") is True,
        "Capability is not current-chain",
    )
    _require(
        snapshot.get("role_capability_blueprint") is None,
        "Blueprint must remain absent until Capability v6 passes B3",
    )
    _require(
        status.get("blueprint_is_current_chain") is False,
        "Blueprint unexpectedly belongs to the current chain",
    )

    analysis_payload = analysis.get("analysis") or {}
    requirements = analysis_payload.get("requirements") or []
    responsibilities = analysis_payload.get("responsibilities") or []
    intelligence = capability.get("intelligence") or {}
    profiles = intelligence.get("capabilities") or []

    _require(isinstance(requirements, list), "P1.6 requirements must be a list")
    _require(isinstance(responsibilities, list), "P1.6 responsibilities must be a list")
    _require(isinstance(profiles, list) and profiles, "Capability v6 contains no profiles")

    linked_requirement_indices: set[int] = set()
    explicit_depth_count = 0

    for number, profile in enumerate(profiles, start=1):
        label = profile.get("capability_label") or f"profile {number}"
        requirement_indices = profile.get("source_requirement_indices") or []
        responsibility_indices = profile.get("source_responsibility_indices") or []

        _require(
            requirement_indices or responsibility_indices,
            f"{label}: no accepted P1.6 source links",
        )
        _require(
            all(
                isinstance(index, int) and 0 <= index < len(requirements)
                for index in requirement_indices
            ),
            f"{label}: invalid requirement link",
        )
        _require(
            all(
                isinstance(index, int) and 0 <= index < len(responsibilities)
                for index in responsibility_indices
            ),
            f"{label}: invalid responsibility link",
        )

        linked_requirement_indices.update(requirement_indices)

        expected_strength = _expected_strength(requirement_indices, requirements)
        _require(
            profile.get("requirement_strength") == expected_strength,
            f"{label}: expected strength {expected_strength!r}, "
            f"got {profile.get('requirement_strength')!r}",
        )

        depth_signals = profile.get("depth_signals") or []
        explicit_depth = [
            item
            for item in depth_signals
            if item.get("evidence_status") == "source_explicit"
        ]
        expected_statements: set[str] = set()

        for index in requirement_indices:
            requirement = requirements[index]
            depth = requirement.get("depth_signal")
            concept = requirement.get("concept")
            if not isinstance(depth, str) or not depth.strip():
                continue
            if not isinstance(concept, str) or not concept.strip():
                concept = "Linked requirement"
            expected_statements.add(f"{concept} — employer-stated depth: {depth}")

        actual_statements = {
            item.get("statement")
            for item in explicit_depth
            if isinstance(item.get("statement"), str)
        }
        _require(
            actual_statements == expected_statements,
            f"{label}: deterministic source-explicit depth mismatch; "
            f"expected {sorted(expected_statements)!r}, got {sorted(actual_statements)!r}",
        )
        explicit_depth_count += len(actual_statements)

    unlinked_depth = [
        (index, item.get("concept"), item.get("depth_signal"))
        for index, item in enumerate(requirements)
        if item.get("depth_signal") and index not in linked_requirement_indices
    ]

    print("Mechanical Capability v6 checks: PASS")
    print(f"Snapshot: {path.as_posix()}")
    print(f"Capability profiles: {len(profiles)}")
    print(f"Linked P1.6 requirements: {len(linked_requirement_indices)} / {len(requirements)}")
    print(f"Deterministic explicit-depth entries: {explicit_depth_count}")

    if unlinked_depth:
        print("WARNING: explicit-depth P1.6 requirements not linked to any capability:")
        for index, concept, depth in unlinked_depth:
            print(f"  - requirement {index}: {concept!r} -> {depth!r}")
    else:
        print("All explicit-depth P1.6 requirements are linked.")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit the repository-safe Capability v6 snapshot before B3 semantic review."
    )
    parser.add_argument("--job-id", default=DEFAULT_JOB_ID)
    parser.add_argument(
        "--expected-analysis-artifact",
        type=int,
        default=DEFAULT_ANALYSIS_ARTIFACT_ID,
    )
    parser.add_argument("--snapshot", type=Path, default=None)
    return parser


def main() -> int:
    args = _parser().parse_args()
    path = args.snapshot or Path("review-snapshots/jobs") / f"{args.job_id}.json"
    try:
        audit_snapshot(
            path,
            job_id=args.job_id,
            expected_analysis_artifact_id=args.expected_analysis_artifact,
        )
    except (AuditError, OSError, json.JSONDecodeError) as exc:
        print(f"Mechanical Capability v6 checks: FAIL: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
