"""Exact qualification ownership shared by v24 generation and persistence."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from jobhunter.analysis_service_v11 import qualification_list_spans
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
    """Reconstruct the same exact-item ownership from immutable source fields."""

    return exact_qualification_item_plan(
        build_requirement_coverage_plan_v23(fields),
        {"__candidate_qualification_evidence": qualification_list_spans(fields)},
    )


__all__ = ["exact_qualification_item_plan", "persisted_qualification_plan"]
