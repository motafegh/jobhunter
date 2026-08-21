"""Deterministic evidence-reference catalogs for long-form job reasoning."""

from __future__ import annotations

import re
from typing import Any

_SEGMENT_SEPARATOR_RE = re.compile(r"(?:\r?\n+|[●•▪◦]+)")
_SECTION_HEADING_RE = re.compile(
    r"(?i)(?:^|\s+)"
    r"(?:preferred\s+(?:qualifications|requirements|skills)|nice[ -]to[ -]have|"
    r"required\s+(?:qualifications|requirements|skills)|"
    r"you(?:'|’)ll\s+stand\s+out\s+if|"
    r"(?:this|the)\s+(?:position|role)\s+(?:will\s+be|is)\s+responsible\s+for|"
    r"you\s+will\s+be\s+responsible\s+for|"
    r"what\s+you(?:'|’)ll\s+do|what\s+we(?:'|’)re\s+looking\s+for|"
    r"technical\s+skill\s+stack|key\s+responsibilities|"
    r"responsibilities(?=\s*(?::|-|include\b))|"
    r"requirements(?=\s*(?::|-))|"
    r"qualifications(?=\s*(?::|-|include\b))|"
    r"specialized\s+competencies|skills(?=\s*(?::|-)|\s+in\b))"
    r"\s*:?(?=\s|$)"
)
_CLAUSE_SEPARATOR_RE = re.compile(r";\s+")
_PARENTHETICAL_DEPTH_RE = re.compile(
    r"\((?:expert|proficient|advanced|intermediate|basic|beginner)\)", re.I
)
_OPTIONALITY_RE = re.compile(
    r"\b(?:preferred|preference|plus|helpful|advantage|nice[ -]to[ -]have|optional)\b",
    re.I,
)
_GLOBAL_UNSPECIFIED_RE = re.compile(
    r"\b(?:do\s+not|don['’]t)\s+expect\s+(?:you\s+to\s+have\s+)?every\b|"
    r"\bnot\s+every\s+(?:single\s+)?(?:item|tool|technology|skill)\b",
    re.I,
)
_CANDIDATE_EXPERIENCE_RE = re.compile(
    r"\bwe\s+(?:are|'re)\s+(?:looking\s+for|seeking)\b"
    r".*\bwith\s+experience\s+(?:in|with)\b",
    re.I,
)
_CANDIDATE_DUTY_RE = re.compile(
    r"\bwe\s+(?:are|'re)\s+(?:looking\s+for|seeking)\b.+\bto\s+[a-z]",
    re.I,
)
_NON_REQUIREMENT_VALUES = {
    "it doesn't matter",
    "doesn't matter",
    "not important",
    "not required",
    "unspecified",
}


def _walk_source_strings(value: Any, path: tuple[str, ...]):
    if isinstance(value, str):
        text = value.strip()
        if text:
            yield path, text
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk_source_strings(item, (*path, str(index)))
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _walk_source_strings(item, (*path, str(key)))


def _split_section_headings(piece: str) -> list[str]:
    """Split exact source text around common vacancy headings, omitting heading tokens."""

    matches = list(_SECTION_HEADING_RE.finditer(piece))
    if not matches:
        return [piece.strip()] if piece.strip() else []

    segments: list[str] = []
    cursor = 0
    for match in matches:
        before = piece[cursor : match.start()].strip()
        if before:
            segments.append(before)
        cursor = match.end()
    after = piece[cursor:].strip()
    if after:
        segments.append(after)
    return segments


def _heading_kind(heading: str) -> str | None:
    normalized = " ".join(heading.casefold().replace("’", "'").split()).strip(":")
    if normalized in {
        "what you'll do",
        "key responsibilities",
        "responsibilities",
        "this position will be responsible for",
        "this position is responsible for",
        "the position will be responsible for",
        "the position is responsible for",
        "this role will be responsible for",
        "this role is responsible for",
        "the role will be responsible for",
        "the role is responsible for",
        "you will be responsible for",
    }:
        return "responsibilities"
    if normalized == "technical skill stack":
        return "technical_stack"
    if normalized in {
        "preferred qualifications",
        "preferred requirements",
        "preferred skills",
        "nice to have",
        "nice-to-have",
        "you'll stand out if",
    }:
        return "preferred_requirements"
    if normalized in {
        "what we're looking for",
        "required qualifications",
        "required requirements",
        "required skills",
        "requirements",
        "qualifications",
        "specialized competencies",
        "skills",
    }:
        return "requirements"
    return None


def _split_segment_text(text: str) -> list[str]:
    return [piece.strip() for piece in _SEGMENT_SEPARATOR_RE.split(text) if piece.strip()]


def _long_text_segments_with_sections(text: str) -> list[tuple[str, str | None]]:
    """Return exact long-text segments together with the nearest recognized section kind."""

    if (
        len(text) < 240
        and not _SEGMENT_SEPARATOR_RE.search(text)
        and not _SECTION_HEADING_RE.search(text)
    ):
        return []

    matches = list(_SECTION_HEADING_RE.finditer(text))
    if not matches:
        return [(piece, None) for piece in _split_segment_text(text)][:80]

    segments: list[tuple[str, str | None]] = []
    cursor = 0
    section_kind: str | None = None
    for match in matches:
        for piece in _split_segment_text(text[cursor : match.start()]):
            segments.append((piece, section_kind))
        section_kind = _heading_kind(match.group(0).strip())
        # Optionality must remain in the exact evidence span so downstream validators can
        # independently verify that preferred strength came from the employer source.
        cursor = match.start() if section_kind == "preferred_requirements" else match.end()
    for piece in _split_segment_text(text[cursor:]):
        segments.append((piece, section_kind))
    return segments[:80]


def _long_text_segments(text: str) -> list[str]:
    """Return exact useful sub-spans for bullet/newline/heading-heavy source text.

    The source remains authoritative. Segments are only stable references into that source so
    models do not need to invent list indexes for concepts that live inside one long description.
    """

    return [segment for segment, _section_kind in _long_text_segments_with_sections(text)]


def _segment_clauses(segment: str) -> list[str]:
    """Expose exact semicolon clauses when a single source bullet mixes requirement strength."""

    clauses = [piece.strip() for piece in _CLAUSE_SEPARATOR_RE.split(segment) if piece.strip()]
    if len(clauses) <= 1:
        return []
    return clauses[:16]


def _depth_scoped_items(text: str) -> list[str]:
    """Expose exact list items when a parenthetical depth applies to only one neighbor."""

    if not _PARENTHETICAL_DEPTH_RE.search(text) or ":" not in text:
        return []
    remainder = text.split(":", 1)[1].strip()
    if not remainder:
        return []

    parts: list[str] = []
    cursor = 0
    depth = 0
    for match in re.finditer(r"\(|\)|\s+and\s+", remainder, re.I):
        token = match.group(0)
        if token == "(":
            depth += 1
        elif token == ")":
            depth = max(0, depth - 1)
        elif depth == 0:
            part = remainder[cursor : match.start()].strip()
            if part:
                parts.append(part)
            cursor = match.end()
    final = remainder[cursor:].strip().rstrip(".")
    if final:
        parts.append(final)
    return parts[:8] if len(parts) > 1 else []


def has_english_optionality_signal(text: str) -> bool:
    """Return whether exact English text contains an explicit optionality/preference signal."""

    return bool(_OPTIONALITY_RE.search(text))


def evidence_mixes_english_optionality(evidence: str) -> bool:
    """Return whether semicolon clauses combine optional and non-optional wording."""

    clauses = _segment_clauses(evidence)
    if len(clauses) < 2:
        return False
    optional_flags = [has_english_optionality_signal(clause) for clause in clauses]
    return any(optional_flags) and not all(optional_flags)


def _meaningful_structured_requirement(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    normalized = " ".join(value.casefold().replace("’", "'").split())
    return bool(normalized and normalized not in _NON_REQUIREMENT_VALUES)


def build_requirement_coverage_plan(fields: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Identify explicit requirement-bearing evidence that P1.6 must account for.

    This is deliberately narrower than the complete evidence catalog. It covers structured
    experience/education plus text under recognized requirement/qualification/skill headings.
    The model still decides semantic normalization, but it may not silently skip these inputs.
    """

    plan: dict[str, dict[str, Any]] = {}
    for key in ("minimum_experience", "education"):
        value = fields.get(key)
        if _meaningful_structured_requirement(value):
            plan[f"field:{key}"] = {
                "text": value.strip(),
                "source_kind": "structured_field",
                "obligation_hint": "required",
                "allow_exclusion": False,
            }

    description = fields.get("description")
    if not isinstance(description, str):
        return plan

    segments = _long_text_segments_with_sections(description)
    requirement_segments = [
        (index, segment, section_kind)
        for index, (segment, section_kind) in enumerate(segments)
        if section_kind in {"requirements", "preferred_requirements", "technical_stack"}
        or (section_kind is None and _CANDIDATE_EXPERIENCE_RE.search(segment))
    ]
    has_global_unspecified = any(
        _GLOBAL_UNSPECIFIED_RE.search(segment)
        for _index, segment, section_kind in requirement_segments
        if section_kind == "technical_stack"
    )

    for index, segment, section_kind in requirement_segments:
        segment_ref = f"field:description:segment:{index}"
        if _GLOBAL_UNSPECIFIED_RE.search(segment):
            plan[segment_ref] = {
                "text": segment,
                "source_kind": "section_modifier",
                "obligation_hint": "context_only",
                "allow_exclusion": False,
            }
            continue

        clauses = _segment_clauses(segment)
        references = (
            [
                (f"{segment_ref}:clause:{clause_index}", clause)
                for clause_index, clause in enumerate(clauses)
            ]
            if clauses
            else [(segment_ref, segment)]
        )
        for reference, text in references:
            items = _depth_scoped_items(text)
            item_references = (
                [
                    (f"{reference}:item:{item_index}", item)
                    for item_index, item in enumerate(items)
                ]
                if items
                else [(reference, text)]
            )
            for item_reference, item_text in item_references:
                if (
                    section_kind == "preferred_requirements"
                    or has_english_optionality_signal(item_text)
                ):
                    obligation_hint = "preferred"
                elif section_kind == "technical_stack" and has_global_unspecified:
                    obligation_hint = "contextual"
                else:
                    obligation_hint = "required"
                plan[item_reference] = {
                    "text": item_text,
                    "source_kind": (
                        "candidate_experience"
                        if section_kind is None
                        else "requirement_section"
                    ),
                    "obligation_hint": obligation_hint,
                    "allow_exclusion": section_kind is not None,
                }
    return plan


def build_responsibility_coverage_plan(fields: dict[str, Any]) -> dict[str, str]:
    """Identify exact duty spans that role purpose/responsibilities must account for."""

    description = fields.get("description")
    if not isinstance(description, str):
        return {}
    plan: dict[str, str] = {}
    for index, (segment, section_kind) in enumerate(
        _long_text_segments_with_sections(description)
    ):
        if section_kind != "responsibilities" and not (
            section_kind is None and _CANDIDATE_DUTY_RE.search(segment)
        ):
            continue
        segment_ref = f"field:description:segment:{index}"
        clauses = _segment_clauses(segment)
        references = (
            [
                (f"{segment_ref}:clause:{clause_index}", clause)
                for clause_index, clause in enumerate(clauses)
            ]
            if clauses
            else [(segment_ref, segment)]
        )
        plan.update(references)
    return plan


def responsibility_coverage_payload(plan: dict[str, str]) -> list[dict[str, str]]:
    """Return the non-duplicative model-facing duty checklist."""

    return [{"id": reference} for reference in sorted(plan)]


def requirement_coverage_payload(
    plan: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return a deterministic model-facing coverage checklist."""

    return [
        {
            "id": reference,
            "source_kind": plan[reference]["source_kind"],
            "obligation_hint": plan[reference]["obligation_hint"],
            "allow_exclusion": plan[reference]["allow_exclusion"],
        }
        for reference in sorted(plan)
    ]


def build_field_evidence_catalog(fields: dict[str, Any]) -> dict[str, str]:
    """Map deterministic field/segment/clause references to exact source text."""

    catalog: dict[str, str] = {}
    for path, text in _walk_source_strings(fields, ("field",)):
        catalog[":".join(path)] = text

    for key, value in fields.items():
        if not isinstance(value, str):
            continue
        for index, segment in enumerate(_long_text_segments(value)):
            segment_ref = f"field:{key}:segment:{index}"
            catalog[segment_ref] = segment
            for clause_index, clause in enumerate(_segment_clauses(segment)):
                clause_ref = f"{segment_ref}:clause:{clause_index}"
                catalog[clause_ref] = clause
                for item_index, item in enumerate(_depth_scoped_items(clause)):
                    catalog[f"{clause_ref}:item:{item_index}"] = item
            for item_index, item in enumerate(_depth_scoped_items(segment)):
                catalog[f"{segment_ref}:item:{item_index}"] = item
    return catalog


def evidence_reference_payload(catalog: dict[str, str]) -> list[dict[str, str]]:
    """Return a deterministic model-facing reference list with exact text."""

    return [
        {"id": reference, "text": catalog[reference]}
        for reference in sorted(catalog)
    ]
