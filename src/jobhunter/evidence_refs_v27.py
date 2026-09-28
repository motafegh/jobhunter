"""Inherit exact required parent obligation for residual source qualifications."""

from __future__ import annotations

from typing import Any

from jobhunter.analysis_runtime_v15 import _v15_candidate_evidence_view
from jobhunter.evidence_refs_v23 import build_requirement_coverage_plan_v23
from jobhunter.evidence_refs_v26 import persisted_qualification_plan_v26


def inherit_decomposed_required_residuals(
    plan: dict[str, dict[str, Any]],
    original_base: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """A residual inside a removed required parent remains a required source fact."""

    result: dict[str, dict[str, Any]] = {}
    for reference, candidate in plan.items():
        if (
            candidate.get("source_kind") != "candidate_residual_sentence"
            or candidate.get("obligation_hint") not in (None, "required")
        ):
            result[reference] = dict(candidate)
            continue
        text = str(candidate.get("text") or "")
        parents = [
            parent for parent_ref, parent in original_base.items()
            if parent_ref not in plan
            and parent.get("source_kind") == "requirement_section"
            and parent.get("obligation_hint") == "required"
            and text
            and text in str(parent.get("text") or "")
        ]
        result[reference] = (
            {**candidate, "obligation_hint": "required", "allow_exclusion": False}
            if parents else dict(candidate)
        )
    return result


def persisted_qualification_plan_v27(fields: dict[str, Any]) -> dict[str, dict[str, Any]]:
    effective, _, _, _ = _v15_candidate_evidence_view(fields)
    original_base = build_requirement_coverage_plan_v23(effective)
    return inherit_decomposed_required_residuals(
        persisted_qualification_plan_v26(fields), original_base
    )


__all__ = ["inherit_decomposed_required_residuals", "persisted_qualification_plan_v27"]
