"""One v25 generation/persistence ledger for heading-only duplicate residuals."""

from __future__ import annotations

import re
from typing import Any

from jobhunter.evidence_refs_v24 import persisted_qualification_plan

_QUALIFICATION_HEADING_RE = re.compile(
    r"^(?:(?:expected|desired|required|preferred)\s+"
    r"(?:competencies|qualifications|skills|abilities)\s+include|"
    r"(?:skills|competencies|qualifications)\s+and\s+"
    r"(?:abilities|skills):)\s*",
    re.I,
)


def remove_heading_duplicate_residuals(
    additional: dict[str, dict[str, Any]],
    base: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Drop a residual whose only extra words are a qualification heading."""

    result: dict[str, dict[str, Any]] = {}
    for reference, candidate in additional.items():
        text = str(candidate.get("text") or "")
        if candidate.get("source_kind") == "candidate_residual_sentence":
            body = _QUALIFICATION_HEADING_RE.sub("", text, count=1)
            if body != text and any(
                other.get("source_kind") == "requirement_section"
                and other.get("text") == body
                and candidate.get("obligation_hint") in
                (None, other.get("obligation_hint"))
                for other in base.values()
            ):
                continue
        result[reference] = dict(candidate)
    return result


def persisted_qualification_plan_v25(fields: dict[str, Any]) -> dict[str, dict[str, Any]]:
    plan = persisted_qualification_plan(fields)
    return remove_heading_duplicate_residuals(plan, plan)


__all__ = ["remove_heading_duplicate_residuals", "persisted_qualification_plan_v25"]
