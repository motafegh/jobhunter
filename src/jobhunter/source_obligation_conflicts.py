"""Candidate-only review flags for conflicting structured job skill authority.

Job-board skill tags are not automatically equivalent to employer-imposed
mandatory requirements. Report direct, exact-span contradictions rather than
silently overriding either original source or structured metadata.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from jobhunter.evidence_refs_v31 import exact_scoped_sections

_NONREQUIRED_RE = re.compile(
    r"\b(?:not\s+(?:an?\s+)?requirement|not\s+mandatory|"
    r"not\s+required|(?:entirely\s+)?optional)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class SourceObligationConflict:
    skill: str
    source_section_start: int
    source_section_end: int
    source_text: str
    reason: str = "structured_skill_tag_required_vs_explicit_source_nonrequired"


def structured_skill_preference_conflicts(
    fields: dict[str, Any],
) -> tuple[SourceObligationConflict, ...]:
    """Flag only exact English optional-source signals for a matching skill.

    Not a universal bilingual contradiction detector. Caller must keep this
    advisory and review the original source before promoting any obligation.
    """
    description = fields.get("description")
    skills = fields.get("skills")
    if not isinstance(description, str) or not isinstance(skills, list):
        return ()
    explicit_optional = [
        section for section in exact_scoped_sections(description)
        if section.kind == "preferred" and _NONREQUIRED_RE.search(section.text)
    ]
    results: list[SourceObligationConflict] = []
    seen: set[tuple[str, int, int]] = set()
    for skill in skills:
        if not isinstance(skill, str):
            continue
        cleaned = skill.strip()
        # Avoid matching generic one-character labels, bare short acronyms,
        # or substrings of unrelated technical product names.
        if len(cleaned) < 3 or len(cleaned) > 64:
            continue
        skill_matcher = re.compile(
            r"(?<![A-Za-z0-9])" + re.escape(cleaned) + r"s?(?![A-Za-z0-9])",
            re.IGNORECASE,
        )
        for section in explicit_optional:
            if not skill_matcher.search(section.text):
                continue
            key = (cleaned.casefold(), section.start, section.end)
            if key in seen:
                continue
            seen.add(key)
            results.append(SourceObligationConflict(
                skill=cleaned,
                source_section_start=section.start,
                source_section_end=section.end,
                source_text=section.text,
            ))
    assert all(
        description[x.source_section_start:x.source_section_end] == x.source_text
        for x in results
    )
    return tuple(results)


__all__ = ["SourceObligationConflict", "structured_skill_preference_conflicts"]
