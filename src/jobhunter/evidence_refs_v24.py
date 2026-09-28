"""Exact qualification ownership shared by v24 generation and persistence."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from jobhunter.analysis_runtime_v15 import _v15_candidate_evidence_view
from jobhunter.analysis_runtime_v18 import _v18_structured_partition
from jobhunter.analysis_runtime_v20 import (
    _v20_complete_requirement_plan,
    _v20_deterministic_structured_skills,
)
from jobhunter.analysis_runtime_v23 import (
    _remove_duplicate_residual_ownership,
    _scoped_preferred_qualification_plan,
    _split_exact_section_sentences,
)
from jobhunter.analysis_service_v13 import decomposed_requirement_references
from jobhunter.evidence_refs_v23 import build_requirement_coverage_plan_v23


def _source_words(text: str) -> Counter[str]:
    return Counter(re.findall(r"[^\W_]+", text.casefold()))


def exact_qualification_item_plan(
    plan: dict[str, dict[str, Any]], model_fields: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    """Remove a redundant broad sentence only when exact items own every word."""

    values = model_fields.get("__candidate_qualification_evidence")
    if not isinstance(values, list):
        return plan
    result = dict(plan)
    for reference, parent in plan.items():
        if parent.get("source_kind") != "requirement_section":
            continue
        if not parent.get("allow_exclusion"):
            continue
        if parent.get("obligation_hint") not in (None, "required"):
            continue
        parent_text = str(parent.get("text") or "")
        children = [
            value
            for value in values
            if isinstance(value, str)
            and value.strip()
            and value.casefold() in parent_text.casefold()
        ]
        if not children:
            continue
        child_words = sum((_source_words(value) for value in children), Counter())
        if child_words and child_words == _source_words(parent_text):
            result.pop(reference)
    return result


def persisted_qualification_plan(fields: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Reconstruct the complete generation ledger from immutable source fields."""

    effective, _qualification_refs, _residual_refs, additional = (
        _v15_candidate_evidence_view(fields)
    )
    effective_base = _split_exact_section_sentences(
        exact_qualification_item_plan(
            build_requirement_coverage_plan_v23(effective), effective
        ),
        effective,
    )
    additional = _scoped_preferred_qualification_plan(
        fields, _remove_duplicate_residual_ownership(additional, effective_base)
    )
    model_fields, _deterministic, _owned = _v18_structured_partition(fields, effective)
    model_fields, _skills, _skill_refs = _v20_deterministic_structured_skills(
        model_fields
    )
    return _v20_complete_requirement_plan(
        model_fields,
        additional_plan=additional,
        decomposed_refs=decomposed_requirement_references(fields),
        base_plan=_split_exact_section_sentences(
            exact_qualification_item_plan(
                build_requirement_coverage_plan_v23(model_fields), model_fields
            ),
            model_fields,
        ),
    )


__all__ = ["exact_qualification_item_plan", "persisted_qualification_plan"]
