"""Candidate-only section-scoped coverage from exact translated source text.

The v30 ledger remains untouched for all accepted historical artifacts.
Source headings are considered only when exact offsets can be recovered.
"""
from __future__ import annotations

import re
from typing import Any

from jobhunter.source_section_spine import SourceSection, source_sections

_OPTIONAL_TAIL_RE = re.compile(
    r"\bFamiliarity\s+with\b.{0,350}?\bis\s+an?\s+advantage,"
    r"\s*but\s+not\s+(?:a\s+)?requirement\s*\.?",
    re.IGNORECASE | re.DOTALL,
)
_NONQUALIFIED_APPLICATION_RE = re.compile(
    r"^(?:If\s+you\s+have\s+(?:a\s+)?(?:Github|GitHub|portfolio)\b|"
    r"Please\s+send\s+(?:us\s+)?your\s+(?:resume|CV)\b)",
    re.IGNORECASE,
)


def exact_scoped_sections(description: str) -> tuple[SourceSection, ...]:
    """Include only a source-explicit optional suffix under a required heading."""
    output: list[SourceSection] = []
    for section in source_sections(description):
        if section.kind != "requirements":
            output.append(section)
            continue
        match = _OPTIONAL_TAIL_RE.search(section.text)
        if match is None:
            output.append(section)
            continue
        boundary = section.start + match.start()
        required = description[section.start:boundary].rstrip()
        if required:
            stop = section.start + len(required)
            output.append(
                SourceSection(
                    kind="requirements", text=required, start=section.start,
                    end=stop, heading=section.heading,
                    heading_start=section.heading_start,
                )
            )
        preference_start = boundary
        preference_end = section.start + match.end()
        while preference_end > preference_start and description[preference_end - 1].isspace():
            preference_end -= 1
        optional_text = description[preference_start:preference_end]
        output.append(
            SourceSection(
                kind="preferred", text=optional_text, start=preference_start,
                end=preference_end, heading=optional_text,
                heading_start=preference_start,
            )
        )
        remainder_start = preference_end
        remainder = description[remainder_start:section.end].strip()
        if remainder:
            start = description.find(remainder, remainder_start, section.end)
            output.append(
                SourceSection(
                    kind="requirements", text=remainder,
                    start=start, end=start + len(remainder),
                    heading=section.heading, heading_start=section.heading_start,
                )
            )
    assert all(description[v.start:v.end] == v.text for v in output)
    return tuple(output)


def v31_requirement_plan(
    fields: dict[str, Any],
    inherited_plan: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    description = fields.get("description")
    if not isinstance(description, str):
        return {ref: dict(item) for ref, item in inherited_plan.items()}
    sections = exact_scoped_sections(description)
    explicit = [s for s in sections if s.kind in {
        "requirements", "preferred", "eligibility_middle", "eligibility_senior",
    }]
    if not explicit:
        return {ref: dict(item) for ref, item in inherited_plan.items()}
    # Remove only model-owned description references whose source spans overlap
    # an explicitly scoped section, replacing them with more precise exact refs.
    # Structured education/experience/skills are separate source fields.
    result: dict[str, dict[str, Any]] = {}
    for reference, candidate in inherited_plan.items():
        text = str(candidate.get("text") or "")
        if not reference.startswith("field:description:") or not any(
            text and (
                text in description[s.heading_start:s.end]
                or s.text in text
            ) for s in explicit
        ):
            result[reference] = dict(candidate)
    for index, section in enumerate(sections):
        if section.kind not in {
            "requirements", "preferred", "eligibility_middle", "eligibility_senior",
        }:
            continue
        ref = f"field:description:v31:section:{index}"
        hint = "preferred" if section.kind == "preferred" else "required"
        result[ref] = {
            "text": section.text,
            "source_kind": "requirement_section",
            "obligation_hint": hint,
            "allow_exclusion": section.kind not in {"eligibility_middle","eligibility_senior"},
            "obligation_context": description[section.heading_start:section.end],
            "v31_source_section_kind": section.kind,
            "v31_source_offset": section.start,
            "v31_source_end": section.end,
            "v31_boundary_inferred": section.inferred_boundary,
        }
    return result


def v31_responsibility_plan(
    fields: dict[str, Any], inherited_plan: dict[str, str]
) -> dict[str, str]:
    result = dict(inherited_plan)
    description = fields.get("description")
    if not isinstance(description, str):
        return result
    for index, section in enumerate(exact_scoped_sections(description)):
        if section.kind != "responsibilities":
            continue
        if any(
            section.text in text or text in section.text
            for text in result.values()
        ):
            continue
        result[f"field:description:v31:work:{index}"] = section.text
    return result


def v31_scoped_additional_plan(
    fields: dict[str, Any],
    inherited_plan: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    description = fields.get("description")
    if not isinstance(description, str):
        return {ref: dict(c) for ref,c in inherited_plan.items()}
    sections = exact_scoped_sections(description)
    result={}
    for ref,candidate in inherited_plan.items():
        updated=dict(candidate)
        text=str(updated.get("text") or "")
        matches=[s for s in sections if text and text in s.text]
        if len(matches)==1:
            section=matches[0]
            if section.kind=="preferred":
                updated["obligation_hint"]="preferred"
                updated["obligation_context"]=description[section.heading_start:section.end]
            if (
                section.kind in {"application", "arrangement"}
                and updated.get("allow_exclusion", False)
            ):
                updated["source_kind"]="v31_nonqualification_context"
                updated["obligation_hint"]="context_only"
        if (
            updated.get("allow_exclusion",False)
            and _NONQUALIFIED_APPLICATION_RE.match(text)
        ):
            updated["source_kind"]="v31_nonqualification_context"
            updated["obligation_hint"]="context_only"
        result[ref]=updated
    return result


__all__=[
    "exact_scoped_sections","v31_requirement_plan","v31_responsibility_plan",
    "v31_scoped_additional_plan",
]
