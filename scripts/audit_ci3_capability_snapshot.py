"""Audit the accepted P1.6 -> Capability v7 boundary for CI-3 review jobs.

Unlike the historical tG9K B3 audit, this script is intentionally job-agnostic and
ignores Role Blueprint acceptance. Blueprint may be present as experimental evidence,
but it is not part of the CI-3 mechanical gate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jobhunter.capability_v7_models import partition_source_requirements

EXPECTED_SNAPSHOT_SCHEMA = "job-review-snapshot-v1"
EXPECTED_ANALYSIS_PROMPT = "job-analysis-english-v9"
EXPECTED_ANALYSIS_SCHEMA = "job-analysis-v4"
EXPECTED_CAPABILITY_PROMPT = "job-capability-intelligence-v7"
EXPECTED_CAPABILITY_SCHEMA = "job-capability-intelligence-v4"


class AuditError(RuntimeError):
    """Raised when a mechanically checkable CI-3 invariant fails."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def _evidence_list(value: Any) -> list[str]:
    values = value if isinstance(value, list) else [value]
    return [item.strip() for item in values if isinstance(item, str) and item.strip()]


def _expected_strength(indices: list[int], requirements: list[dict[str, Any]]) -> str:
    strengths = {
        requirements[index].get("requirement_type")
        for index in indices
        if requirements[index].get("requirement_type")
    }
    strengths.discard(None)
    if not strengths:
        return "unspecified"
    if len(strengths) == 1:
        return str(next(iter(strengths)))
    return "mixed"


def _require_source_truth_matches(
    *,
    accepted: dict[str, Any],
    source_truth: dict[str, Any],
) -> tuple[list[int], list[int]]:
    requirements = accepted.get("requirements") or []
    responsibilities = accepted.get("responsibilities") or []
    purposes = accepted.get("role_purpose") or []
    _require(isinstance(requirements, list), "P1.6 requirements must be a list")
    _require(isinstance(responsibilities, list), "P1.6 responsibilities must be a list")
    _require(isinstance(purposes, list), "P1.6 role_purpose must be a list")

    capability_indices, role_level_indices = partition_source_requirements(accepted)
    _require(
        source_truth.get("capability_requirement_indices") == capability_indices,
        "source_truth capability partition does not match accepted P1.6",
    )
    _require(
        source_truth.get("role_level_requirement_indices") == role_level_indices,
        "source_truth role-level partition does not match accepted P1.6",
    )

    truth_requirements = source_truth.get("requirements") or []
    truth_responsibilities = source_truth.get("responsibilities") or []
    truth_purposes = source_truth.get("role_purpose") or []
    _require(len(truth_requirements) == len(requirements), "source_truth lost requirements")
    _require(
        len(truth_responsibilities) == len(responsibilities),
        "source_truth lost responsibilities",
    )
    _require(len(truth_purposes) == len(purposes), "source_truth lost role-purpose facts")

    for index, requirement in enumerate(requirements):
        _require(isinstance(requirement, dict), f"P1.6 requirement {index} is not an object")
        truth = truth_requirements[index]
        _require(isinstance(truth, dict), f"source_truth requirement {index} is not an object")
        _require(truth.get("index") == index, f"source_truth requirement {index} changed index")
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
        _require(
            truth.get("evidence") == _evidence_list(requirement.get("evidence")),
            f"source_truth requirement {index} changed evidence",
        )

    for index, responsibility in enumerate(responsibilities):
        _require(
            isinstance(responsibility, dict),
            f"P1.6 responsibility {index} is not an object",
        )
        truth = truth_responsibilities[index]
        _require(
            isinstance(truth, dict),
            f"source_truth responsibility {index} is not an object",
        )
        _require(
            truth.get("index") == index,
            f"source_truth responsibility {index} changed index",
        )
        for key in ("statement", "confidence"):
            _require(
                truth.get(key) == responsibility.get(key),
                f"source_truth responsibility {index} changed {key}",
            )
        _require(
            truth.get("evidence") == _evidence_list(responsibility.get("evidence")),
            f"source_truth responsibility {index} changed evidence",
        )

    for index, purpose in enumerate(purposes):
        _require(isinstance(purpose, dict), f"P1.6 role purpose {index} is not an object")
        truth = truth_purposes[index]
        _require(isinstance(truth, dict), f"source_truth role purpose {index} is not an object")
        _require(truth.get("index") == index, f"source_truth role purpose {index} changed index")
        for key in ("statement", "confidence"):
            _require(
                truth.get(key) == purpose.get(key),
                f"source_truth role purpose {index} changed {key}",
            )
        _require(
            truth.get("evidence") == _evidence_list(purpose.get("evidence")),
            f"source_truth role purpose {index} changed evidence",
        )

    return capability_indices, role_level_indices


def audit_snapshot(path: Path, *, job_id: str) -> None:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    _require(
        snapshot.get("snapshot_schema_version") == EXPECTED_SNAPSHOT_SCHEMA,
        f"Expected snapshot schema {EXPECTED_SNAPSHOT_SCHEMA}",
    )
    _require(snapshot.get("source_job_id") == job_id, f"Snapshot is not for {job_id!r}")

    status = snapshot.get("status") or {}
    _require(status.get("english_projection_present") is True, "English projection is missing")
    _require(status.get("english_analysis_present") is True, "English P1.6 analysis is missing")
    _require(
        status.get("translation_matches_english_analysis") is True,
        "English projection does not match the selected English analysis",
    )
    _require(
        status.get("capability_intelligence_present") is True,
        "Capability Intelligence is missing for the configured contract/model",
    )
    _require(
        status.get("capability_is_current_chain") is True,
        "Capability Intelligence is not on the selected current dependency chain",
    )

    configured_models = snapshot.get("configured_models") or {}
    analysis = snapshot.get("english_analysis")
    capability = snapshot.get("capability_intelligence")
    translation = snapshot.get("english_projection")
    _require(isinstance(analysis, dict), "Missing English P1.6 payload")
    _require(isinstance(capability, dict), "Missing current Capability payload")
    _require(isinstance(translation, dict), "Missing English projection payload")

    _require(
        analysis.get("prompt_version") == EXPECTED_ANALYSIS_PROMPT,
        f"Expected P1.6 prompt {EXPECTED_ANALYSIS_PROMPT}, got {analysis.get('prompt_version')!r}",
    )
    _require(
        analysis.get("schema_version") == EXPECTED_ANALYSIS_SCHEMA,
        f"Expected P1.6 schema {EXPECTED_ANALYSIS_SCHEMA}, got {analysis.get('schema_version')!r}",
    )
    _require(
        capability.get("prompt_version") == EXPECTED_CAPABILITY_PROMPT,
        "Capability prompt is not the accepted v7 contract",
    )
    _require(
        capability.get("schema_version") == EXPECTED_CAPABILITY_SCHEMA,
        "Capability schema is not the accepted v4 contract",
    )
    _require(
        analysis.get("model") == configured_models.get("analysis"),
        "English P1.6 artifact model does not match configured analysis model",
    )
    _require(
        capability.get("model") == configured_models.get("capability"),
        "Capability artifact model does not match configured capability model",
    )
    _require(
        analysis.get("translation_artifact_id") == translation.get("artifact_id"),
        "English analysis references a different translation artifact",
    )
    _require(
        capability.get("analysis_artifact_id") == analysis.get("artifact_id"),
        "Capability references a different English analysis artifact",
    )
    _require(
        capability.get("translation_artifact_id") == translation.get("artifact_id"),
        "Capability references a different English projection artifact",
    )
    _require(
        capability.get("job_detail_version_id") == analysis.get("job_detail_version_id"),
        "Capability and English analysis use different source versions",
    )

    accepted = analysis.get("analysis") or {}
    intelligence = capability.get("intelligence") or {}
    source_truth = intelligence.get("source_truth")
    profiles = intelligence.get("capabilities") or []
    _require(isinstance(accepted, dict), "P1.6 analysis payload is invalid")
    _require(isinstance(intelligence, dict), "Capability intelligence payload is invalid")
    _require(isinstance(source_truth, dict), "Capability v7 source_truth is missing")
    _require(isinstance(profiles, list), "Capability profiles must be a list")

    requirements = accepted.get("requirements") or []
    responsibilities = accepted.get("responsibilities") or []
    _require(isinstance(requirements, list), "P1.6 requirements must be a list")
    _require(isinstance(responsibilities, list), "P1.6 responsibilities must be a list")

    capability_indices, role_level_indices = _require_source_truth_matches(
        accepted=accepted,
        source_truth=source_truth,
    )

    if capability_indices or responsibilities:
        _require(bool(profiles), "Capability v7 contains no profiles for capability/work evidence")
    if len(requirements) >= 12 and len(responsibilities) >= 5:
        _require(len(profiles) >= 2, "Dense source collapsed into fewer than two profiles")

    capability_index_set = set(capability_indices)
    role_level_set = set(role_level_indices)
    linked_requirements: set[int] = set()
    linked_responsibilities: set[int] = set()
    linked_explicit_depth: set[int] = set()

    for number, profile in enumerate(profiles, start=1):
        _require(isinstance(profile, dict), f"Capability profile {number} is not an object")
        label = str(profile.get("capability_label") or f"profile {number}")
        req_links = profile.get("source_requirement_indices") or []
        resp_links = profile.get("source_responsibility_indices") or []
        _require(isinstance(req_links, list), f"{label}: requirement links are not a list")
        _require(isinstance(resp_links, list), f"{label}: responsibility links are not a list")
        _require(req_links or resp_links, f"{label}: no accepted P1.6 source links")
        _require(
            all(isinstance(index, int) and index in capability_index_set for index in req_links),
            f"{label}: requirement links include invalid or role-level indices",
        )
        _require(
            not (set(req_links) & role_level_set),
            f"{label}: role-level requirements leaked into Capability grouping",
        )
        _require(
            all(
                isinstance(index, int) and 0 <= index < len(responsibilities)
                for index in resp_links
            ),
            f"{label}: invalid responsibility links",
        )
        linked_requirements.update(req_links)
        linked_responsibilities.update(resp_links)

        _require(
            profile.get("requirement_strength") == _expected_strength(req_links, requirements),
            f"{label}: deterministic requirement strength mismatch",
        )

        expected_depth = {
            f"{requirements[index]['concept']} — employer-stated depth: "
            f"{requirements[index]['depth_signal']}"
            for index in req_links
            if requirements[index].get("depth_signal")
        }
        actual_depth = {
            item.get("statement")
            for item in profile.get("depth_signals") or []
            if isinstance(item, dict) and item.get("evidence_status") == "source_explicit"
        }
        _require(actual_depth == expected_depth, f"{label}: source-explicit depth mismatch")
        linked_explicit_depth.update(
            index for index in req_links if requirements[index].get("depth_signal")
        )

        expected_work = {
            responsibilities[index]["statement"]
            for index in resp_links
            if isinstance(responsibilities[index], dict)
            and responsibilities[index].get("statement")
        }
        actual_work = {
            item.get("statement")
            for item in profile.get("work_activities") or []
            if isinstance(item, dict) and item.get("evidence_status") == "source_explicit"
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
                    not isinstance(item, dict) or item.get("evidence_status") != "source_explicit"
                    for item in profile.get(section) or []
                ),
                f"{label}: model source_explicit item survived in {section}",
            )

    _require(
        capability_index_set <= linked_requirements,
        "Capability-relevant P1.6 requirements are not fully linked",
    )
    _require(
        linked_responsibilities == set(range(len(responsibilities))),
        "P1.6 responsibilities are not fully linked",
    )
    _require(
        set(source_truth.get("linked_requirement_indices") or []) == linked_requirements,
        "source_truth linked requirement accounting disagrees with profiles",
    )
    _require(
        source_truth.get("unlinked_capability_requirement_indices") == [],
        "source_truth reports unlinked capability requirements",
    )
    _require(
        set(source_truth.get("linked_responsibility_indices") or [])
        == linked_responsibilities,
        "source_truth linked responsibility accounting disagrees with profiles",
    )
    _require(
        source_truth.get("unlinked_responsibility_indices") == [],
        "source_truth reports unlinked responsibilities",
    )

    explicit_depth = {
        index for index, requirement in enumerate(requirements)
        if isinstance(requirement, dict) and requirement.get("depth_signal")
    }
    _require(
        set(source_truth.get("explicit_depth_requirement_indices") or []) == explicit_depth,
        "source_truth explicit-depth accounting is incomplete",
    )
    _require(
        set(source_truth.get("linked_explicit_depth_requirement_indices") or [])
        == linked_explicit_depth,
        "source_truth linked-depth accounting disagrees with profiles",
    )
    _require(
        set(source_truth.get("unlinked_explicit_depth_requirement_indices") or [])
        == explicit_depth - linked_explicit_depth,
        "source_truth unlinked-depth accounting disagrees with role-level partition",
    )
    _require(
        intelligence.get("cross_capability_observations") == [],
        "Capability v7 must not persist cross-capability synthesis",
    )

    density = (
        "dense"
        if len(requirements) >= 12 and len(responsibilities) >= 5
        else "sparse/moderate"
    )
    print("Mechanical CI-3 Capability checks: PASS")
    print(f"Snapshot: {path.as_posix()}")
    print(f"Job: {job_id}")
    print(f"P1.6 artifact: {analysis.get('artifact_id')}")
    print(f"Capability artifact: {capability.get('artifact_id')}")
    print(f"Evidence density: {density}")
    print(f"Requirements: {len(requirements)}")
    print(f"Responsibilities: {len(responsibilities)}")
    print(f"Capability profiles: {len(profiles)}")
    print(
        "Capability requirements linked: "
        f"{len(capability_index_set & linked_requirements)}/{len(capability_indices)}"
    )
    print(
        "Responsibilities linked: "
        f"{len(linked_responsibilities)}/{len(responsibilities)}"
    )
    print(f"Explicit depth facts: {len(explicit_depth)}")
    print(f"Role-level requirement indices: {role_level_indices}")
    if snapshot.get("role_capability_blueprint") is not None:
        print("Blueprint payload: present but ignored by CI-3 acceptance")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the current accepted P1.6 v9/v4 -> Capability v7/v4 boundary "
            "for one heterogeneous CI-3 review job."
        )
    )
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--snapshot", type=Path, default=None)
    args = parser.parse_args()
    path = args.snapshot or Path("review-snapshots/jobs") / f"{args.job_id}.json"
    try:
        audit_snapshot(path, job_id=args.job_id)
    except (AuditError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Mechanical CI-3 Capability checks: FAIL: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
