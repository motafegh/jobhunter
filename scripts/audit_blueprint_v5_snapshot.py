"""Audit the bounded Blueprint v5 review snapshot used for B4 acceptance."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

EXPECTED_ANALYSIS_ARTIFACT_ID = 29
EXPECTED_CAPABILITY_ARTIFACT_ID = 9
EXPECTED_CAPABILITY_PROMPT = "job-capability-intelligence-v7"
EXPECTED_CAPABILITY_SCHEMA = "job-capability-intelligence-v4"
EXPECTED_BLUEPRINT_PROMPT = "role-capability-blueprint-v5"
EXPECTED_BLUEPRINT_SCHEMA = "role-capability-blueprint-v4"
DEFAULT_JOB_ID = "tG9K"
DEFAULT_SNAPSHOT = Path("review-snapshots/jobs/tG9K.json")

_ABSOLUTE_REQUIREMENT_RE = re.compile(
    r"\b(?:mandatory|required|must|necessary|non-negotiable|has to|have to|"
    r"needs to|need to|expected to|responsible for)\b",
    re.I,
)
_NEGATED_REQUIREMENT_RE = re.compile(
    r"\b(?:not|isn't|is not|unlikely to be|probably not)\s+"
    r"(?:mandatory|required|necessary|non-negotiable)\b",
    re.I,
)
_END_TO_END_OWNERSHIP_RE = re.compile(
    r"\b(?:own|owns|owning)\s+(?:the\s+)?(?:entire|full|end-to-end)\s+"
    r"(?:lifecycle|stack|pipeline|system)\b",
    re.I,
)
_FORBIDDEN_LEGACY_KEYS = {
    "role_read",
    "likely_role_shape",
    "likely_depth",
    "why_this_matters",
    "likely_subskills",
    "suggested_tools_or_examples",
    "likely_work_products",
    "likely_failure_modes_or_operational_concerns",
    "hidden_requirements",
    "professional_example_scenarios",
    "bottom_line",
}


class AuditError(RuntimeError):
    """Raised when a mechanically checkable Blueprint v5 invariant fails."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def _evidence(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    _require(isinstance(value, list), "evidence must be a string or list")
    return [str(item).strip() for item in value if str(item).strip()]


def _uses_absolute_inference_language(value: str) -> bool:
    cleaned = _NEGATED_REQUIREMENT_RE.sub("", value)
    return bool(
        _ABSOLUTE_REQUIREMENT_RE.search(cleaned)
        or _END_TO_END_OWNERSHIP_RE.search(cleaned)
    )


def _assert_no_legacy_keys(value: Any, *, path: str = "blueprint") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _require(
                key not in _FORBIDDEN_LEGACY_KEYS,
                f"legacy v4 key remains at {path}.{key}",
            )
            _assert_no_legacy_keys(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _assert_no_legacy_keys(item, path=f"{path}[{index}]")


def _check_source_requirement(
    actual: dict[str, Any],
    expected: dict[str, Any],
    *,
    expected_index: int,
) -> None:
    _require(actual.get("requirement_index") == expected_index, "requirement index mismatch")
    for key in ("concept", "concept_type", "requirement_type", "depth_signal"):
        _require(
            actual.get(key) == expected.get(key),
            f"requirement {expected_index} {key} mismatch",
        )
    _require(
        _evidence(actual.get("evidence")) == _evidence(expected.get("evidence")),
        f"requirement {expected_index} evidence mismatch",
    )


def _check_source_responsibility(
    actual: dict[str, Any],
    expected: dict[str, Any],
    *,
    expected_index: int,
) -> None:
    _require(
        actual.get("responsibility_index") == expected_index,
        "responsibility index mismatch",
    )
    _require(
        actual.get("statement") == expected.get("statement"),
        f"responsibility {expected_index} statement mismatch",
    )
    _require(
        _evidence(actual.get("evidence")) == _evidence(expected.get("evidence")),
        f"responsibility {expected_index} evidence mismatch",
    )


def audit_snapshot(path: Path, *, job_id: str = DEFAULT_JOB_ID) -> dict[str, int]:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    _require(snapshot.get("source_job_id") == job_id, "unexpected source job ID")
    status = snapshot.get("status") or {}
    _require(status.get("capability_is_current_chain") is True, "Capability is not current chain")
    _require(status.get("blueprint_is_current_chain") is True, "Blueprint is not current chain")

    analysis_payload = snapshot.get("english_analysis") or {}
    capability_payload = snapshot.get("capability_intelligence") or {}
    blueprint_payload = snapshot.get("role_capability_blueprint") or {}

    _require(
        analysis_payload.get("artifact_id") == EXPECTED_ANALYSIS_ARTIFACT_ID,
        "unexpected English P1.6 artifact",
    )
    _require(
        capability_payload.get("artifact_id") == EXPECTED_CAPABILITY_ARTIFACT_ID,
        "unexpected Capability artifact",
    )
    _require(
        capability_payload.get("prompt_version") == EXPECTED_CAPABILITY_PROMPT,
        "unexpected Capability prompt",
    )
    _require(
        capability_payload.get("schema_version") == EXPECTED_CAPABILITY_SCHEMA,
        "unexpected Capability schema",
    )
    _require(
        blueprint_payload.get("capability_artifact_id") == EXPECTED_CAPABILITY_ARTIFACT_ID,
        "Blueprint does not depend on accepted Capability artifact 9",
    )
    _require(
        blueprint_payload.get("prompt_version") == EXPECTED_BLUEPRINT_PROMPT,
        "unexpected Blueprint prompt",
    )
    _require(
        blueprint_payload.get("schema_version") == EXPECTED_BLUEPRINT_SCHEMA,
        "unexpected Blueprint schema",
    )

    accepted = analysis_payload.get("analysis") or {}
    capability = capability_payload.get("intelligence") or {}
    blueprint = blueprint_payload.get("blueprint") or {}
    _assert_no_legacy_keys(blueprint)

    requirements = list(accepted.get("requirements") or [])
    responsibilities = list(accepted.get("responsibilities") or [])
    capability_profiles = list(capability.get("capabilities") or [])
    source_truth = capability.get("source_truth") or {}
    areas = list(blueprint.get("capability_areas") or [])

    _require(len(areas) == len(capability_profiles), "Capability area count mismatch")
    _require(
        blueprint.get("source_capability_coverage") == list(range(len(capability_profiles))),
        "Capability coverage is not deterministic source order",
    )

    expected_purpose = [
        {
            "statement": str(item.get("statement") or ""),
            "evidence": _evidence(item.get("evidence")),
        }
        for item in accepted.get("role_purpose") or []
        if isinstance(item, dict) and str(item.get("statement") or "").strip()
    ]
    actual_purpose = list(blueprint.get("source_role_purpose") or [])
    _require(len(actual_purpose) == len(expected_purpose), "role purpose count mismatch")
    for actual, expected in zip(actual_purpose, expected_purpose, strict=True):
        _require(actual.get("statement") == expected["statement"], "role purpose mismatch")
        _require(
            _evidence(actual.get("evidence")) == expected["evidence"],
            "purpose evidence mismatch",
        )

    role_indices = list(source_truth.get("role_level_requirement_indices") or [])
    constraints = list(blueprint.get("source_role_constraints") or [])
    _require(len(constraints) == len(role_indices), "role constraint count mismatch")
    for actual, requirement_index in zip(constraints, role_indices, strict=True):
        expected = requirements[requirement_index]
        _require(actual.get("requirement_index") == requirement_index, "constraint index mismatch")
        _require(actual.get("concept") == expected.get("concept"), "constraint concept mismatch")
        _require(
            actual.get("requirement_type") == expected.get("requirement_type"),
            "constraint strength mismatch",
        )
        _require(
            actual.get("depth_signal") == expected.get("depth_signal"),
            "constraint depth mismatch",
        )
        _require(
            _evidence(actual.get("evidence")) == _evidence(expected.get("evidence")),
            "constraint evidence mismatch",
        )

    total_requirements = 0
    total_responsibilities = 0
    considerations = 0
    for capability_index, (area, profile) in enumerate(
        zip(areas, capability_profiles, strict=True)
    ):
        _require(
            area.get("source_capability_index") == capability_index,
            "capability link mismatch",
        )
        _require(
            area.get("name") == profile.get("capability_label"),
            "capability label mismatch",
        )
        _require(
            area.get("interpretation_strength") == "plausible",
            "v5 capability interpretation must be mechanically plausible",
        )
        interpretation = str(area.get("practical_interpretation") or "")
        _require(bool(interpretation.strip()), "missing practical interpretation")
        _require(
            not _uses_absolute_inference_language(interpretation),
            "practical interpretation claims employer obligation/full ownership",
        )

        expected_requirement_indices = list(profile.get("source_requirement_indices") or [])
        actual_requirements = list(area.get("source_requirements") or [])
        _require(
            len(actual_requirements) == len(expected_requirement_indices),
            f"Capability {capability_index} requirement count mismatch",
        )
        for actual, requirement_index in zip(
            actual_requirements,
            expected_requirement_indices,
            strict=True,
        ):
            _check_source_requirement(
                actual,
                requirements[requirement_index],
                expected_index=requirement_index,
            )
        total_requirements += len(actual_requirements)

        expected_responsibility_indices = list(profile.get("source_responsibility_indices") or [])
        actual_responsibilities = list(area.get("source_responsibilities") or [])
        _require(
            len(actual_responsibilities) == len(expected_responsibility_indices),
            f"Capability {capability_index} responsibility count mismatch",
        )
        for actual, responsibility_index in zip(
            actual_responsibilities,
            expected_responsibility_indices,
            strict=True,
        ):
            _check_source_responsibility(
                actual,
                responsibilities[responsibility_index],
                expected_index=responsibility_index,
            )
        total_responsibilities += len(actual_responsibilities)

        for item in area.get("professional_considerations") or []:
            _require(
                item.get("interpretation_strength") in {"plausible", "speculative"},
                "invalid professional consideration strength",
            )
            _require(bool(str(item.get("uncertainty") or "").strip()), "missing uncertainty")
            statement = str(item.get("statement") or "")
            _require(bool(statement.strip()), "missing professional consideration statement")
            _require(
                not _uses_absolute_inference_language(statement),
                "professional consideration claims employer obligation/full ownership",
            )
            considerations += 1

    return {
        "capability_areas": len(areas),
        "deterministic_source_requirements": total_requirements,
        "deterministic_source_responsibilities": total_responsibilities,
        "professional_considerations": considerations,
        "role_level_constraints": len(constraints),
        "role_purpose_items": len(actual_purpose),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit the bounded Blueprint v5 review snapshot")
    parser.add_argument("snapshot", nargs="?", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--job-id", default=DEFAULT_JOB_ID)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        result = audit_snapshot(args.snapshot, job_id=args.job_id)
    except (AuditError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Mechanical Blueprint v5 checks: FAIL\n{exc}")
        return 1

    print("Mechanical Blueprint v5 checks: PASS")
    print(f"Snapshot: {args.snapshot}")
    print(f"Capability areas: {result['capability_areas']}")
    print(
        "Deterministic source requirements: "
        f"{result['deterministic_source_requirements']}"
    )
    print(
        "Deterministic source responsibilities: "
        f"{result['deterministic_source_responsibilities']}"
    )
    print(f"Professional considerations: {result['professional_considerations']}")
    print(f"Role-level constraints: {result['role_level_constraints']}")
    print(f"Role-purpose items: {result['role_purpose_items']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
