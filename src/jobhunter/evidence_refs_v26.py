"""Exact mixed-strength qualification ownership for the isolated v26 candidate."""

from __future__ import annotations

import re
from typing import Any

from jobhunter.evidence_refs_v25 import persisted_qualification_plan_v25

_PREFERRED_CLAUSE_RE = re.compile(r",\s+(?=preferably\b)", re.I)


def split_mixed_preference_clauses(
    plan: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Give exact required/preferred source clauses separate coverage owners."""

    result: dict[str, dict[str, Any]] = {}
    for reference, candidate in plan.items():
        text = str(candidate.get("text") or "")
        match = _PREFERRED_CLAUSE_RE.search(text)
        if (
            candidate.get("source_kind") != "requirement_section"
            or candidate.get("obligation_hint") != "required"
            or candidate.get("required_item_excerpts")
            or match is None
        ):
            result[reference] = dict(candidate)
            continue
        required = text[: match.start()]
        preferred = text[match.end() :]
        if not required or not preferred or not preferred.lower().startswith("preferably "):
            result[reference] = dict(candidate)
            continue
        result[f"{reference}:required_clause"] = {
            **candidate,
            "text": required,
            "obligation_context": text,
        }
        result[f"{reference}:preferred_clause"] = {
            **candidate,
            "text": preferred,
            "obligation_hint": "preferred",
            "obligation_context": text,
        }
    return result


def persisted_qualification_plan_v26(fields: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return split_mixed_preference_clauses(persisted_qualification_plan_v25(fields))


__all__ = ["split_mixed_preference_clauses", "persisted_qualification_plan_v26"]
