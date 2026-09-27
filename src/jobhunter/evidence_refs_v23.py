"""Isolated exact source coverage for explicit candidate work-demonstration preferences."""

from __future__ import annotations

import re
from typing import Any

from jobhunter.analysis_service_v11 import qualification_list_spans
from jobhunter.evidence_refs import (
    _SECTION_HEADING_RE,
    _heading_kind,
    has_english_optionality_signal,
)
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
_QUALIFICATION_ITEM_START_RE = re.compile(
    r"(?:^|,\s+)(?P<item>(?:(?:practical|real-world|professional|hands-on|"
    r"specialized|proficient|a\s+good|a\s+relevant)\s+)?"
    r"(?:experience|understanding|familiarity|mastery|proficiency|ability|knowledge|"
    r"educational\s+background)\b|(?:and\s+)?the\s+ability\b|"
    r"(?:and\s+)?a\s+relevant\s+educational\s+background\b)",
    re.I,
)
_EXPLICIT_EXPERIENCE_ITEM_RE = re.compile(
    r"^(?:(?:practical|real-world|professional|hands-on)\s+)?experience\b", re.I
)


_PREFERRED_LIST_PREFIX_RE = re.compile(
    r"^(?:points?\s+(?:are\s+also\s+)?awarded|score\s+is\s+given)\s+for\s+",
    re.I,
)


def _dense_qualification_items(
    text: str, derived_qualifications: set[str]
) -> list[dict[str, str | None]]:
    """Require each exact item in a dense source qualification list."""

    prefix = _PREFERRED_LIST_PREFIX_RE.match(text)
    scope = text[prefix.end() :] if prefix else text
    matches = list(_QUALIFICATION_ITEM_START_RE.finditer(scope))
    if len(matches) < 3:
        return []
    items: list[dict[str, str | None]] = []
    for index, match in enumerate(matches):
        start = match.start("item")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(scope)
        item = scope[start:end].strip(" ,.")
        if item.casefold() in derived_qualifications:
            continue
        items.append({
            "text": item,
            "required_concept_type": (
                "experience" if _EXPLICIT_EXPERIENCE_ITEM_RE.match(item) else None
            ),
        })
    return items if len(items) >= 2 else []


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

    headings = list(_SECTION_HEADING_RE.finditer(description))
    derived_qualifications = {
        value.strip().casefold() for value in qualification_list_spans(fields)
    }
    for candidate in plan.values():
        if (
            candidate.get("source_kind") == "requirement_section"
            and not candidate.get("required_item_excerpts")
        ):
            items = _dense_qualification_items(
                str(candidate.get("text") or ""), derived_qualifications
            )
            if items:
                candidate["required_item_excerpts"] = items
        if (
            candidate.get("source_kind") != "requirement_section"
            or candidate.get("obligation_hint") != "preferred"
        ):
            continue
        text = str(candidate.get("text") or "")
        if not text or has_english_optionality_signal(text):
            continue
        positions = [match.start() for match in re.finditer(re.escape(text), description)]
        if len(positions) != 1:
            continue
        prior = [heading for heading in headings if heading.end() <= positions[0]]
        if prior and _heading_kind(prior[-1].group(0).strip()) == "preferred_requirements":
            candidate["obligation_context"] = prior[-1].group(0).strip()

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
