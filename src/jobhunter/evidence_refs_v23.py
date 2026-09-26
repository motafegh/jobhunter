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
    r"significant\s+impact|prioritized\s+for\s+review)\b",
    re.I,
)
_APPLICATION_INSTRUCTION_RE = re.compile(
    r"\b(?:to\s+apply|please\s+send|submit\s+(?:a|your)\s+resume|"
    r"interested\s+parties)\b",
    re.I,
)


def _proof_sentences(bullet: str) -> list[str]:
    """Keep an explicit demonstration request with its immediately following questions."""

    sentences = _sentences(bullet)
    result: list[str] = []
    cursor = 0
    index = 0
    while index < len(sentences):
        sentence = sentences[index]
        start = bullet.find(sentence, cursor)
        if start < 0:
            raise ValueError("Proof sentence must remain an exact source substring")
        end = start + len(sentence)
        if (
            ":" in sentence and sentence.endswith("?")
            and _PROOF_CUE_RE.search(sentence)
            and _PREFERENCE_CUE_RE.search(sentence)
        ):
            while index + 1 < len(sentences) and sentences[index + 1].endswith("?"):
                index += 1
                following = sentences[index]
                following_start = bullet.find(following, end)
                if following_start < 0:
                    raise ValueError("Proof question must remain an exact source substring")
                end = following_start + len(following)
        result.append(bullet[start:end].strip())
        cursor = end
        index += 1
    return result


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
        for sentence in _proof_sentences(bullet):
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
