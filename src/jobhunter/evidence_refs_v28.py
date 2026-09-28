"""Item-level ownership for dense required residuals."""

from __future__ import annotations

from typing import Any

from jobhunter.evidence_refs_v23 import _dense_qualification_items
from jobhunter.evidence_refs_v27 import persisted_qualification_plan_v27


def require_dense_residual_items(
    plan: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Require each source-exact item when a required residual is a dense list."""

    result: dict[str, dict[str, Any]] = {}
    for reference, candidate in plan.items():
        updated = dict(candidate)
        if (
            candidate.get("source_kind") == "candidate_residual_sentence"
            and candidate.get("obligation_hint") == "required"
            and not candidate.get("allow_exclusion", True)
            and not candidate.get("required_item_excerpts")
        ):
            items = _dense_qualification_items(str(candidate.get("text") or ""), set())
            if items:
                updated["required_item_excerpts"] = items
        result[reference] = updated
    return result


def persisted_qualification_plan_v28(fields: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return require_dense_residual_items(persisted_qualification_plan_v27(fields))


__all__ = ["require_dense_residual_items", "persisted_qualification_plan_v28"]
