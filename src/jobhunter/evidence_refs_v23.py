"""Isolated exact source coverage for explicit candidate work-demonstration preferences."""

from __future__ import annotations

import re
from typing import Any

from jobhunter.evidence_refs_v21 import _sentences, build_requirement_coverage_plan_v21

_PROOF_CUE_RE = re.compile(
    r"\b(?:samples?\s+of\s+work|sample\s+projects?|real-world\s+sample|"
    r"real\s+project|github\s+repository|(?:online\s+)?demo|portfolio|"
    r"(?:agents?|projects?)\s+you\s+have\s+previously\s+built)\b",
    re.I,
)
_PREFERENCE_CUE_RE = re.compile(
    r"\b(?:huge\s+plus|plus\s+if|very\s+valuable|more\s+valuable|"
    r"significant\s+impact|prioritized\s+for\s+review|"
    r"having\s+at\s+least\s+one\s+real-world\s+sample)\b",
    re.I,
)
_APPLICATION_INSTRUCTION_RE = re.compile(
    r"\b(?:to\s+apply|please\s+send|submit\s+(?:a|your)\s+resume|"
    r"interested\s+parties)\b",
    re.I,
)


def build_requirement_coverage_plan_v23(
    fields: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Add only explicit preferred proof; retain all v21 source and skill rules."""

    plan = build_requirement_coverage_plan_v21(fields)
    description = fields.get("description")
    if not isinstance(description, str):
        return plan

    existing = [str(item["text"]) for item in plan.values()]
    index = 0
    for bullet in description.split("•"):
        for sentence in _sentences(bullet):
            text = sentence.strip()
            if not (
                _PROOF_CUE_RE.search(text)
                and _PREFERENCE_CUE_RE.search(text)
                and not _APPLICATION_INSTRUCTION_RE.search(text)
            ):
                continue
            if any(text in covered for covered in existing):
                continue
            plan[f"field:description:v23:proof:{index}"] = {
                "text": text,
                "source_kind": "candidate_proof",
                "obligation_hint": "preferred",
                "allow_exclusion": False,
                "required_item_excerpts": [
                    {"text": text, "required_concept_type": None}
                ],
            }
            existing.append(text)
            index += 1
    return plan


__all__ = ["build_requirement_coverage_plan_v23"]
