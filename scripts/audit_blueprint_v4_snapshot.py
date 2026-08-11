"""Audit the live Blueprint v4 review snapshot used for B4 acceptance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

EXPECTED_ANALYSIS_ARTIFACT_ID = 29
EXPECTED_CAPABILITY_ARTIFACT_ID = 9
EXPECTED_CAPABILITY_PROMPT = "job-capability-intelligence-v7"
EXPECTED_CAPABILITY_SCHEMA = "job-capability-intelligence-v4"
EXPECTED_BLUEPRINT_PROMPT = "role-capability-blueprint-v4"
EXPECTED_BLUEPRINT_SCHEMA = "role-capability-blueprint-v3"
DEFAULT_JOB_ID = "tG9K"
DEFAULT_SNAPSHOT = Path("review-snapshots/jobs/tG9K.json")


class AuditError(RuntimeError):
    """Raised when a mechanically checkable Blueprint v4 invariant fails."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def _indices(value: Any, *, label: str, upper: int) -> list[int]:
    _require(isinstance(value, list), f"{label} must be a list")
    result: list[int] = []
    for item in value:
        _require(isinstance(item, int), f"{label} must contain only integers")
        _require(0 <= item < upper, f"{label} contains out-of-range index {item}")
        _require(item not in result, f"{label} contains duplicate index {item}")
        result.append(item)
    return result


def _evidence(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    _require(isinstance(value, list), "evidence must be a string or list")
    return [str(item).strip() for item in value if str(item).strip()]


def _audit_source_requirement(
    item: dict[str, Any],
    requirement: dict[str, Any],
    *,
    expected_index: int,
) -> None:
    _require(
        item.get("requirement_index") == expected_index,
        f"Source requirement index mismatch for {expected_index}",
    )
    for field in ("concept", "concept_type", "requirement_type", "depth_signal"):
        _require(
            item.get(field) == requirement.get(field),
            f"Source requirement {expected_index} drifted field {field}",
        )
    _require(
        _evidence(item.get("evidence")) == _evidence(requirement.get("evidence")),
        f"Source requirement {expected_index} evidence drift",
    )


def _audit_source_responsibility(
    item: dict[str, Any],
    responsibility: dict[str, Any],
    *,
    expected_index: int,
) -> None:
    _require(
        item.get("responsibility_index") == expected_index,
        f"Source responsibility index mismatch for {expected_index}",
    )
    _require(
        item.get("statement") == responsibility.get("statement"),
        f"Source responsibility {expected_index} statement drift",
    )
    _require(
        _evidence(item.get("evidence")) == _evidence(responsibility.get("evidence")),
        f"Source responsibility {expected_index} evidence drift",
    )


def audit(snapshot: dict[str, Any], *, job_id: str) -> dict[str, int]:
    _require(snapshot.get("source_job_id") == job_id, "Snapshot job identity mismatch")
    status = snapshot.get("status") or {}
    _require(status.get("capability_is_current_chain") is True, "Capability is not current chain")
    _require(status.get("blueprint_is_current_chain") is True, "Blueprint is not current chain")

    analysis = snapshot.get("english_analysis")
    capability = snapshot.get("capability_intelligence")
    blueprint_artifact = snapshot.get("role_capability_blueprint")
    _require(isinstance(analysis, dict), "English analysis is missing")
    _require(isinstance(capability, dict), "Capability artifact is missing")
    _require(isinstance(blueprint_artifact, dict), "Blueprint artifact is missing")

    _require(
        analysis.get("artifact_id") == EXPECTED_ANALYSIS_ARTIFACT_ID,
        f"Expected English analysis artifact {EXPECTED_ANALYSIS_ARTIFACT_ID}",
    )
    _require(
        capability.get("artifact_id") == EXPECTED_CAPABILITY_ARTIFACT_ID,
        f"Expected Capability artifact {EXPECTED_CAPABILITY_ARTIFACT_ID}",
    )
    _require(
        capability.get("prompt_version") == EXPECTED_CAPABILITY_PROMPT,
        "Capability prompt contract mismatch",
    )
    _require(
        capability.get("schema_version") == EXPECTED_CAPABILITY_SCHEMA,
        "Capability schema contract mismatch",
    )
    _require(
        blueprint_artifact.get("capability_artifact_id") == EXPECTED_CAPABILITY_ARTIFACT_ID,
        "Blueprint does not depend on accepted Capability artifact 9",
    )
    _require(
        blueprint_artifact.get("analysis_artifact_id") == EXPECTED_ANALYSIS_ARTIFACT_ID,
        "Blueprint does not depend on accepted English analysis artifact 29",
    )
    _require(
        blueprint_artifact.get("prompt_version") == EXPECTED_BLUEPRINT_PROMPT,
        "Blueprint prompt contract mismatch",
    )
    _require(
        blueprint_artifact.get("schema_version") == EXPECTED_BLUEPRINT_SCHEMA,
        "Blueprint schema contract mismatch",
    )

    intelligence = capability.get("intelligence") or {}
    profiles = intelligence.get("capabilities") or []
    source_truth = intelligence.get("source_truth") or {}
    requirements = source_truth.get("requirements") or []
    responsibilities = source_truth.get("responsibilities") or []
    _require(isinstance(profiles, list) and profiles, "Accepted Capability has no profiles")
    _require(isinstance(requirements, list) and requirements, "Source truth requirements missing")
    _require(isinstance(responsibilities, list), "Source truth responsibilities must be a list")

    blueprint = blueprint_artifact.get("blueprint") or {}
    _require(isinstance(blueprint, dict), "Blueprint payload is not an object")
    areas = blueprint.get("capability_areas") or []
    _require(isinstance(areas, list), "Blueprint capability_areas must be a list")
    _require(
        len(areas) == len(profiles),
        "Blueprint v4 must persist exactly one area per accepted Capability profile",
    )

    expected_coverage = list(range(len(profiles)))
    coverage = _indices(
        blueprint.get("source_capability_coverage") or [],
        label="source_capability_coverage",
        upper=len(profiles),
    )
    _require(coverage == expected_coverage, "Blueprint capability coverage mismatch")

    source_requirements = 0
    source_responsibilities = 0
    suggested_tools = 0
    for position, (area, profile) in enumerate(zip(areas, profiles, strict=True)):
        _require(isinstance(area, dict), f"Blueprint area {position} is not an object")
        _require(isinstance(profile, dict), f"Capability profile {position} is not an object")
        _require(
            area.get("source_capability_index") == position,
            f"Blueprint area {position} is not attached to Capability {position}",
        )
        _require(
            area.get("name") == profile.get("capability_label"),
            f"Blueprint area {position} renamed the accepted Capability",
        )
        _require(
            "source_capability_indices" not in area,
            "Legacy v3 source_capability_indices leaked into v4 area",
        )

        expected_req = _indices(
            profile.get("source_requirement_indices") or [],
            label=f"Capability {position} requirement links",
            upper=len(requirements),
        )
        persisted_req = area.get("source_requirements") or []
        _require(
            len(persisted_req) == len(expected_req),
            f"Capability {position} source requirement count mismatch",
        )
        for persisted, req_index in zip(persisted_req, expected_req, strict=True):
            _require(isinstance(persisted, dict), "Persisted source requirement is not an object")
            requirement = requirements[req_index]
            _require(isinstance(requirement, dict), "Capability source requirement is invalid")
            _audit_source_requirement(persisted, requirement, expected_index=req_index)
            source_requirements += 1

        expected_resp = _indices(
            profile.get("source_responsibility_indices") or [],
            label=f"Capability {position} responsibility links",
            upper=len(responsibilities),
        )
        persisted_resp = area.get("source_responsibilities") or []
        _require(
            len(persisted_resp) == len(expected_resp),
            f"Capability {position} source responsibility count mismatch",
        )
        for persisted, resp_index in zip(persisted_resp, expected_resp, strict=True):
            _require(
                isinstance(persisted, dict),
                "Persisted source responsibility is not an object",
            )
            responsibility = responsibilities[resp_index]
            _require(isinstance(responsibility, dict), "Capability responsibility is invalid")
            _audit_source_responsibility(
                persisted,
                responsibility,
                expected_index=resp_index,
            )
            source_responsibilities += 1

        for tool in area.get("suggested_tools_or_examples") or []:
            _require(isinstance(tool, dict), "Suggested tool is not an object")
            _require(
                tool.get("relationship") in {"likely_example", "possible_example"},
                "Blueprint v4 suggested tool has invalid relationship",
            )
            forbidden = {
                "source_requirement_indices",
                "source_responsibility_indices",
                "source_requirement_strength",
                "source_depth_signals",
            }
            _require(
                forbidden.isdisjoint(tool),
                "Model-created suggested tool contains legacy source provenance fields",
            )
            suggested_tools += 1

    role_indices = _indices(
        source_truth.get("role_level_requirement_indices") or [],
        label="role-level requirement links",
        upper=len(requirements),
    )
    constraints = blueprint.get("source_role_constraints") or []
    _require(
        len(constraints) == len(role_indices),
        "Blueprint role constraint count mismatch",
    )
    for persisted, req_index in zip(constraints, role_indices, strict=True):
        _require(isinstance(persisted, dict), "Role constraint is not an object")
        requirement = requirements[req_index]
        _require(isinstance(requirement, dict), "Role-level source requirement is invalid")
        _require(persisted.get("requirement_index") == req_index, "Role constraint index drift")
        for field in ("concept", "requirement_type", "depth_signal"):
            _require(
                persisted.get(field) == requirement.get(field),
                f"Role constraint {req_index} drifted field {field}",
            )
        _require(
            _evidence(persisted.get("evidence")) == _evidence(requirement.get("evidence")),
            f"Role constraint {req_index} evidence drift",
        )

    hidden = blueprint.get("hidden_requirements") or []
    for item in hidden:
        _require(isinstance(item, dict), "Hidden requirement is not an object")
        _require(
            item.get("interpretation_strength") in {"plausible", "speculative"},
            "Blueprint v4 hidden requirement has invalid certainty",
        )
        _require(
            "source_capability_indices" not in item
            and "source_responsibility_indices" not in item,
            "Blueprint v4 hidden requirement contains legacy provenance bookkeeping",
        )

    _require(
        "likely_end_to_end_scenarios" not in blueprint,
        "Legacy v3 likely_end_to_end_scenarios field leaked into v4 Blueprint",
    )
    scenarios = blueprint.get("professional_example_scenarios") or []
    for item in scenarios:
        _require(isinstance(item, dict), "Professional scenario is not an object")
        _require(
            item.get("scenario_basis") == "professional_example",
            "Blueprint v4 scenario basis must be professional_example",
        )
        _require(
            item.get("interpretation_strength") in {"plausible", "speculative"},
            "Blueprint v4 professional scenario has invalid certainty",
        )
        _require(
            "source_capability_indices" not in item
            and "source_responsibility_indices" not in item,
            "Blueprint v4 professional scenario contains legacy provenance bookkeeping",
        )

    return {
        "areas": len(areas),
        "source_requirements": source_requirements,
        "source_responsibilities": source_responsibilities,
        "suggested_tools": suggested_tools,
        "role_constraints": len(constraints),
        "hidden_requirements": len(hidden),
        "professional_examples": len(scenarios),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--job-id", default=DEFAULT_JOB_ID)
    args = parser.parse_args()

    try:
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        counts = audit(snapshot, job_id=args.job_id)
    except (OSError, json.JSONDecodeError, AuditError) as exc:
        print(f"Mechanical Blueprint v4 checks: FAIL\n{exc}")
        return 1

    print("Mechanical Blueprint v4 checks: PASS")
    print(f"Snapshot: {args.snapshot}")
    print(f"Capability areas: {counts['areas']}")
    print(f"Deterministic source requirements: {counts['source_requirements']}")
    print(f"Deterministic source responsibilities: {counts['source_responsibilities']}")
    print(f"Suggested tool examples: {counts['suggested_tools']}")
    print(f"Role-level constraints: {counts['role_constraints']}")
    print(f"Hidden requirements: {counts['hidden_requirements']}")
    print(f"Professional examples: {counts['professional_examples']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
