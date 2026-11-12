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


def _section_requirement(
    description: str, section: SourceSection, start: int, end: int
) -> dict[str, Any]:
    """Source-owned exact span with no inferred additional obligation."""
    kind = section.kind
    return {
        "text": description[start:end],
        "source_kind": "requirement_section",
        "obligation_hint": "preferred" if kind == "preferred" else "required",
        "allow_exclusion": kind not in {"eligibility_middle", "eligibility_senior"},
        "obligation_context": description[section.heading_start:section.end],
        "v31_source_section_kind": kind,
        "v31_source_offset": start,
        "v31_source_end": end,
        "v31_boundary_inferred": section.inferred_boundary,
    }


def _uncovered_source_spans(
    description: str, section: SourceSection, owned: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    """Keep only missing text; never re-introduce a huge duplicate parent."""
    if not owned:
        return [(section.start, section.end)]
    spans: list[tuple[int, int]] = []
    current = section.start
    for begin, end in sorted(owned):
        if begin > current:
            spans.append((current, begin))
        current = max(current, end)
    if current < section.end:
        spans.append((current, section.end))
    remaining = []
    for begin, end in spans:
        while begin < end and (
            description[begin].isspace() or description[begin] in ",;:•"
        ):
            begin += 1
        while begin < end and (
            description[end - 1].isspace() or description[end - 1] in ",;:•"
        ):
            end -= 1
        if begin < end and any(c.isalnum() for c in description[begin:end]):
            remaining.append((begin, end))
    return remaining


def v31_requirement_plan(
    fields: dict[str, Any],
    inherited_plan: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Retain narrower v30 claims when a single explicit source section owns them.

    Replace only ambiguous heading-crossing references. Fill uncovered source
    spans individually instead of replacing a dense exact-evidence ledger with
    one unreviewable broad parent. Never delete unrelated structured fields.
    """
    description = fields.get("description")
    if not isinstance(description, str):
        return {ref: dict(item) for ref, item in inherited_plan.items()}
    sections = exact_scoped_sections(description)
    allowed = {"requirements", "preferred", "eligibility_middle", "eligibility_senior"}
    explicit = [(i, s) for i, s in enumerate(sections) if s.kind in allowed]
    if not explicit:
        return {ref: dict(item) for ref, item in inherited_plan.items()}

    result: dict[str, dict[str, Any]] = {}
    owned: dict[int, list[tuple[int, int]]] = {i: [] for i, _ in explicit}
    for reference, candidate in inherited_plan.items():
        text = str(candidate.get("text") or "")
        if not reference.startswith("field:description:") or not text:
            result[reference] = dict(candidate)
            continue
        # Only preserve a source-specific claim with one unique exact owner.
        exact = [(i, s) for i, s in explicit if s.text.count(text) == 1]
        if len(exact) == 1:
            index, section = exact[0]
            begin = section.start + section.text.index(text)
            end = begin + len(text)
            updated = dict(candidate)
            updated.update({
                "obligation_hint": (
                    "preferred" if section.kind == "preferred" else "required"
                ),
                "obligation_context": description[section.heading_start:section.end],
                "v31_source_section_kind": section.kind,
                "v31_source_offset": begin,
                "v31_source_end": end,
                "v31_boundary_inferred": section.inferred_boundary,
            })
            result[reference] = updated
            owned[index].append((begin, end))
            continue
        if any(
            s.text in text or text in description[s.heading_start:s.end]
            for _, s in explicit
        ):
            # Span crosses separate authority sections; a replacement must
            # stay inside one exact section, or its meaning is undecidable.
            continue
        result[reference] = dict(candidate)

    for index, section in explicit:
        for part, (begin, end) in enumerate(
            _uncovered_source_spans(description, section, owned[index])
        ):
            ref = f"field:description:v31:section:{index}:part:{part}"
            result[ref] = _section_requirement(description, section, begin, end)
    assert all(
        description[c["v31_source_offset"]:c["v31_source_end"]] == c["text"]
        for c in result.values() if "v31_source_offset" in c
    )
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
