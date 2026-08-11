"""Audit the live Blueprint v3 review snapshot used for B4 acceptance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

EXPECTED_ANALYSIS_ARTIFACT_ID = 29
EXPECTED_CAPABILITY_ARTIFACT_ID = 9
EXPECTED_CAPABILITY_PROMPT = "job-capability-intelligence-v7"
EXPECTED_CAPABILITY_SCHEMA = "job-capability-intelligence-v4"
EXPECTED_BLUEPRINT_PROMPT = "role-capability-blueprint-v3"
EXPECTED_BLUEPRINT_SCHEMA = "role-capability-blueprint-v2"
DEFAULT_JOB_ID = "tG9K"
DEFAULT_SNAPSHOT = Path("review-snapshots/jobs/tG9K.json")


class AuditError(RuntimeError):
    """Raised when a mechanically checkable Blueprint v3 invariant fails."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def _indices(value: Any, *, label: str, upper: int) -> list[int]:
    _require(isinstance(value, list), f"{label} must be a list")
    result: list[int] = []
    for item in value:
        _require(isinstance(item, int), f"{label} must contain only integers")
        _require(0 <= item < upper, f"{label} contains out-of-range index {item}")
        if item not in result:
            result.append(item)
    return result


def _expected_strength(indices: list[int], requirements: list[dict[str, Any]]) -> str:
    strengths = {
        str(requirements[index].get("requirement_type") or "").strip()
        for index in indices
        if str(requirements[index].get("requirement_type") or "").strip()
    }
    if not strengths:
        return "unspecified"
    if len(strengths) == 1:
        return next(iter(strengths))
    return "mixed"


def _expected_depth(indices: list[int], requirements: list[dict[str, Any]]) -> list[str]:
    return [
        str(requirements[index]["depth_signal"]).strip()
        for index in indices
        if requirements[index].get("depth_signal")
    ]


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
    capability_profiles = intelligence.get("capabilities") or []
    source_truth = intelligence.get("source_truth") or {}
    requirements = source_truth.get("requirements") or []
    responsibilities = source_truth.get("responsibilities") or []
    _require(capability_profiles, "Accepted Capability has no profiles")
    _require(requirements, "Capability source truth has no requirements")

    blueprint = blueprint_artifact.get("blueprint") or {}
    areas = blueprint.get("capability_areas") or []
    _require(areas, "Blueprint contains no capability areas")

    expected_capabilities = list(range(len(capability_profiles)))
    declared_coverage = _indices(
        blueprint.get("source_capability_coverage") or [],
        label="source_capability_coverage",
        upper=len(capability_profiles),
    )
    _require(
        declared_coverage == expected_capabilities,
        f"Blueprint capability coverage mismatch: {declared_coverage} != {expected_capabilities}",
    )

    area_coverage: set[int] = set()
    source_named_tools = 0
    inferred_tools = 0
    for area_index, area in enumerate(areas):
        links = _indices(
            area.get("source_capability_indices") or [],
            label=f"area {area_index} capability links",
            upper=len(capability_profiles),
        )
        _require(links, f"Blueprint area {area_index} has no Capability grounding")
        area_coverage.update(links)
        for tool_index, tool in enumerate(area.get("likely_tools_or_examples") or []):
            relationship = tool.get("relationship")
            requirement_links = _indices(
                tool.get("source_requirement_indices") or [],
                label=f"area {area_index} tool {tool_index} requirement links",
                upper=len(requirements),
            )
            responsibility_links = _indices(
                tool.get("source_responsibility_indices") or [],
                label=f"area {area_index} tool {tool_index} responsibility links",
                upper=len(responsibilities),
            )
            if relationship == "source_named":
                source_named_tools += 1
                _require(
                    bool(requirement_links or responsibility_links),
                    f"Source-named tool {tool.get('name')!r} has no P1.6 grounding",
                )
                expected_strength = _expected_strength(requirement_links, requirements)
                _require(
                    tool.get("source_requirement_strength") == expected_strength,
                    f"Source-named tool {tool.get('name')!r} has incorrect strength",
                )
                expected_depth = _expected_depth(requirement_links, requirements)
                _require(
                    (tool.get("source_depth_signals") or []) == expected_depth,
                    f"Source-named tool {tool.get('name')!r} has incorrect depth propagation",
                )
            else:
                inferred_tools += 1
                _require(not requirement_links, "Inferred tool contains P1.6 requirement links")
                _require(not responsibility_links, "Inferred tool contains P1.6 responsibility links")
                _require(
                    tool.get("source_requirement_strength") == "unspecified",
                    "Inferred tool carries source requirement strength",
                )
                _require(not (tool.get("source_depth_signals") or []), "Inferred tool carries source depth")

    _require(
        sorted(area_coverage) == expected_capabilities,
        "Union of Blueprint area links does not cover every accepted Capability profile",
    )

    role_indices = _indices(
        source_truth.get("role_level_requirement_indices") or [],
        label="Capability role-level requirement indices",
        upper=len(requirements),
    )
    constraints = blueprint.get("source_role_constraints") or []
    constraint_indices = [item.get("requirement_index") for item in constraints]
    _require(
        constraint_indices == role_indices,
        f"Blueprint role constraints mismatch: {constraint_indices} != {role_indices}",
    )
    for constraint, requirement_index in zip(constraints, role_indices, strict=True):
        requirement = requirements[requirement_index]
        _require(constraint.get("concept") == requirement.get("concept"), "Role constraint concept drift")
        _require(
            constraint.get("requirement_type") == requirement.get("requirement_type"),
            "Role constraint strength drift",
        )
        _require(
            constraint.get("depth_signal") == requirement.get("depth_signal"),
            "Role constraint depth drift",
        )

    for item in blueprint.get("hidden_requirements") or []:
        if item.get("interpretation_strength") == "highly_likely":
            capability_links = _indices(
                item.get("source_capability_indices") or [],
                label="hidden requirement capability links",
                upper=len(capability_profiles),
            )
            responsibility_links = _indices(
                item.get("source_responsibility_indices") or [],
                label="hidden requirement responsibility links",
                upper=len(responsibilities),
            )
            _require(
                bool(capability_links or responsibility_links),
                "Highly-likely hidden requirement has no accepted upstream grounding",
            )

    professional_examples = 0
    source_workflows = 0
    for scenario in blueprint.get("likely_end_to_end_scenarios") or []:
        basis = scenario.get("scenario_basis")
        if basis == "professional_example":
            professional_examples += 1
            _require(
                scenario.get("interpretation_strength") != "highly_likely",
                "Professional example scenario is incorrectly highly_likely",
            )
        elif basis == "source_stated_workflow":
            source_workflows += 1
            links = _indices(
                scenario.get("source_responsibility_indices") or [],
                label="source workflow responsibility links",
                upper=len(responsibilities),
            )
            _require(links, "Source-stated workflow has no responsibility grounding")
        else:
            raise AuditError(f"Unknown scenario_basis: {basis!r}")
        if scenario.get("interpretation_strength") == "highly_likely":
            _require(
                not (scenario.get("assumptions") or []),
                "Highly-likely scenario depends on unresolved assumptions",
            )

    return {
        "areas": len(areas),
        "source_named_tools": source_named_tools,
        "inferred_tools": inferred_tools,
        "professional_examples": professional_examples,
        "source_workflows": source_workflows,
        "role_constraints": len(constraints),
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
        print(f"Mechanical Blueprint v3 checks: FAIL\n{exc}")
        return 1

    print("Mechanical Blueprint v3 checks: PASS")
    print(f"Snapshot: {args.snapshot}")
    print(f"Capability areas: {counts['areas']}")
    print(f"Source-named tools: {counts['source_named_tools']}")
    print(f"Inferred tool examples: {counts['inferred_tools']}")
    print(f"Professional-example scenarios: {counts['professional_examples']}")
    print(f"Source-stated workflows: {counts['source_workflows']}")
    print(f"Role-level constraints preserved: {counts['role_constraints']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
