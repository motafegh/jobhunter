"""Audit the live Capability v7 review snapshot used for B3 acceptance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

EXPECTED_PROMPT_VERSION = "job-capability-intelligence-v7"
EXPECTED_SCHEMA_VERSION = "job-capability-intelligence-v4"
DEFAULT_JOB_ID = "tG9K"
DEFAULT_ANALYSIS_ARTIFACT_ID = 29


class AuditError(RuntimeError):
    """Raised when a mechanically checkable v7 invariant fails."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def _expected_strength(indices: list[int], requirements: list[dict[str, Any]]) -> str:
    strengths = {
        requirements[index]["requirement_type"]
        for index in indices
        if requirements[index].get("requirement_type")
    }
    if not strengths:
        return "unspecified"
    if len(strengths) == 1:
        return next(iter(strengths))
    return "mixed"


def _role_level(requirement: dict[str, Any]) -> bool:
    concept_type = str(requirement.get("concept_type") or "").casefold()
    if concept_type == "education":
        return True
    if concept_type != "experience":
        return False
    depth = str(requirement.get("depth_signal") or "").casefold()
    evidence = str(requirement.get("evidence") or "").casefold()
    return "year" in depth or "year" in evidence


def audit_snapshot(path: Path, *, job_id: str, analysis_artifact_id: int) -> None:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    _require(snapshot.get("source_job_id") == job_id, f"Snapshot is not for {job_id!r}")

    status = snapshot.get("status") or {}
    analysis = snapshot.get("english_analysis")
    capability = snapshot.get("capability_intelligence")
    _require(isinstance(analysis, dict), "Missing English P1.6 analysis")
    _require(
        analysis.get("artifact_id") == analysis_artifact_id,
        f"Expected P1.6 artifact {analysis_artifact_id}, got {analysis.get('artifact_id')!r}",
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
    _require(status.get("capability_is_current_chain") is True, "Capability is not current-chain")
    _require(
        status.get("blueprint_is_current_chain") is False,
        "Blueprint unexpectedly belongs to the current chain",
    )
    _require(
        snapshot.get("role_capability_blueprint") is None,
        "Blueprint payload must remain absent until B3 passes",
    )

    accepted = analysis.get("analysis") or {}
    requirements = accepted.get("requirements") or []
    responsibilities = accepted.get("responsibilities") or []
    role_purpose = accepted.get("role_purpose") or []
    intelligence = capability.get("intelligence") or {}
    profiles = intelligence.get("capabilities") or []
    source_truth = intelligence.get("source_truth")

    _require(isinstance(requirements, list), "P1.6 requirements must be a list")
    _require(isinstance(responsibilities, list), "P1.6 responsibilities must be a list")
    _require(isinstance(role_purpose, list), "P1.6 role_purpose must be a list")
    _require(isinstance(profiles, list) and profiles, "Capability v7 contains no profiles")
    _require(isinstance(source_truth, dict), "Capability v7 source_truth is missing")
    if len(requirements) >= 12 and len(responsibilities) >= 5:
        _require(len(profiles) >= 2, "Dense source collapsed into fewer than two profiles")

    role_level = [
        index for index, requirement in enumerate(requirements) if _role_level(requirement)
    ]
    capability_requirement_indices = [
        index for index in range(len(requirements)) if index not in role_level
    ]
    _require(
        source_truth.get("role_level_requirement_indices") == role_level,
        "source_truth role-level partition does not match accepted P1.6",
    )
    _require(
        source_truth.get("capability_requirement_indices") == capability_requirement_indices,
        "source_truth capability partition does not match accepted P1.6",
    )

    truth_requirements = source_truth.get("requirements") or []
    truth_responsibilities = source_truth.get("responsibilities") or []
    truth_purpose = source_truth.get("role_purpose") or []
    _require(len(truth_requirements) == len(requirements), "source_truth lost requirements")
    _require(
        len(truth_responsibilities) == len(responsibilities),
        "source_truth lost responsibilities",
    )
    _require(len(truth_purpose) == len(role_purpose), "source_truth lost role-purpose facts")

    for index, requirement in enumerate(requirements):
        truth = truth_requirements[index]
        for key in (
            "concept",
            "concept_type",
            "requirement_type",
            "depth_signal",
            "confidence",
        ):
            _require(
                truth.get(key) == requirement.get(key),
                f"source_truth requirement {index} changed {key}",
            )
        expected_evidence = requirement.get("evidence")
        expected_evidence = (
            expected_evidence if isinstance(expected_evidence, list) else [expected_evidence]
        )
        expected_evidence = [item for item in expected_evidence if isinstance(item, str) and item]
        _require(
            truth.get("evidence") == expected_evidence,
            f"source_truth requirement {index} changed evidence",
        )

    linked_requirements: set[int] = set()
    linked_responsibilities: set[int] = set()
    profile_depth_indices: set[int] = set()

    for number, profile in enumerate(profiles, start=1):
        label = profile.get("capability_label") or f"profile {number}"
        req_links = profile.get("source_requirement_indices") or []
        resp_links = profile.get("source_responsibility_indices") or []
        _require(req_links or resp_links, f"{label}: no accepted P1.6 source links")
        _require(
            all(isinstance(i, int) and 0 <= i < len(requirements) for i in req_links),
            f"{label}: invalid requirement link",
        )
        _require(
            all(isinstance(i, int) and 0 <= i < len(responsibilities) for i in resp_links),
            f"{label}: invalid responsibility link",
        )
        linked_requirements.update(req_links)
        linked_responsibilities.update(resp_links)

        _require(
            profile.get("requirement_strength") == _expected_strength(req_links, requirements),
            f"{label}: deterministic requirement strength mismatch",
        )

        expected_depth = {
            f"{requirements[i]['concept']} — employer-stated depth: "
            f"{requirements[i]['depth_signal']}"
            for i in req_links
            if requirements[i].get("depth_signal")
        }
        actual_depth = {
            item.get("statement")
            for item in profile.get("depth_signals") or []
            if item.get("evidence_status") == "source_explicit"
        }
        _require(actual_depth == expected_depth, f"{label}: source-explicit depth mismatch")
        profile_depth_indices.update(
            i for i in req_links if requirements[i].get("depth_signal")
        )

        expected_work = {
            responsibilities[i]["statement"]
            for i in resp_links
            if responsibilities[i].get("statement")
        }
        actual_work = {
            item.get("statement")
            for item in profile.get("work_activities") or []
            if item.get("evidence_status") == "source_explicit"
        }
        _require(actual_work == expected_work, f"{label}: source-explicit work mismatch")

        _require(
            profile.get("independence_expectation") is None,
            f"{label}: positive independence/ownership survived v7 reconciliation",
        )
        for section in (
            "sub_capabilities",
            "underlying_knowledge",
            "operational_practices",
            "operational_context",
        ):
            _require(
                all(
                    item.get("evidence_status") != "source_explicit"
                    for item in profile.get(section) or []
                ),
                f"{label}: model source_explicit item survived in {section}",
            )

    _require(
        set(capability_requirement_indices) <= linked_requirements,
        "Capability-relevant P1.6 requirements are not fully linked",
    )
    _require(
        linked_responsibilities == set(range(len(responsibilities))),
        "P1.6 responsibilities are not fully linked",
    )
    _require(
        source_truth.get("unlinked_capability_requirement_indices") == [],
        "source_truth reports unlinked capability requirements",
    )
    _require(
        source_truth.get("unlinked_responsibility_indices") == [],
        "source_truth reports unlinked responsibilities",
    )

    explicit_depth = {
        index for index, requirement in enumerate(requirements) if requirement.get("depth_signal")
    }
    _require(
        set(source_truth.get("explicit_depth_requirement_indices") or []) == explicit_depth,
        "source_truth explicit-depth accounting is incomplete",
    )
    _require(
        set(source_truth.get("linked_explicit_depth_requirement_indices") or [])
        == profile_depth_indices,
        "source_truth linked-depth accounting disagrees with profiles",
    )
    _require(
        intelligence.get("cross_capability_observations") == [],
        "Capability v7 must not persist cross-capability synthesis",
    )

    print("Mechanical Capability v7 checks: PASS")
    print(f"Snapshot: {path.as_posix()}")
    print(f"Capability profiles: {len(profiles)}")
    print(
        "Capability requirements linked: "
        f"{len(set(capability_requirement_indices) & linked_requirements)}"
        f"/{len(capability_requirement_indices)}"
    )
    print(
        "Responsibilities linked: "
        f"{len(linked_responsibilities)}/{len(responsibilities)}"
    )
    print(f"Explicit depth facts in source truth: {len(explicit_depth)}")
    print(f"Role-level requirement indices: {role_level}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit the Capability v7 source-truth boundary before B3 semantic review."
    )
    parser.add_argument("--job-id", default=DEFAULT_JOB_ID)
    parser.add_argument(
        "--expected-analysis-artifact",
        type=int,
        default=DEFAULT_ANALYSIS_ARTIFACT_ID,
    )
    parser.add_argument("--snapshot", type=Path, default=None)
    args = parser.parse_args()
    path = args.snapshot or Path("review-snapshots/jobs") / f"{args.job_id}.json"
    try:
        audit_snapshot(
            path,
            job_id=args.job_id,
            analysis_artifact_id=args.expected_analysis_artifact,
        )
    except (AuditError, OSError, json.JSONDecodeError) as exc:
        print(f"Mechanical Capability v7 checks: FAIL: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
