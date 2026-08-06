"""Deterministic evidence-reference catalogs for long-form job reasoning."""

from __future__ import annotations

import re
from typing import Any

_SEGMENT_SEPARATOR_RE = re.compile(r"(?:\r?\n+|[●•▪◦]+)")
_SECTION_HEADING_RE = re.compile(
    r"(?i)(?:^|\s+)"
    r"(?:what\s+you(?:'|’)ll\s+do|what\s+we(?:'|’)re\s+looking\s+for|"
    r"technical\s+skill\s+stack|key\s+responsibilities|responsibilities|"
    r"requirements|qualifications|specialized\s+competencies|skills)"
    r"\s*:?(?=\s|$)"
)
_CLAUSE_SEPARATOR_RE = re.compile(r";\s+")


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


def _long_text_segments(text: str) -> list[str]:
    """Return exact useful sub-spans for bullet/newline/heading-heavy source text.

    The source remains authoritative. Segments are only stable references into that source so
    models do not need to invent list indexes for concepts that live inside one long description.
    """

    if (
        len(text) < 240
        and not _SEGMENT_SEPARATOR_RE.search(text)
        and not _SECTION_HEADING_RE.search(text)
    ):
        return []

    pieces: list[str] = []
    for raw_piece in _SEGMENT_SEPARATOR_RE.split(text):
        pieces.extend(_split_section_headings(raw_piece))
    return [piece for piece in pieces if piece][:80]


def _segment_clauses(segment: str) -> list[str]:
    """Expose exact semicolon clauses when a single source bullet mixes requirement strength."""

    clauses = [piece.strip() for piece in _CLAUSE_SEPARATOR_RE.split(segment) if piece.strip()]
    if len(clauses) <= 1:
        return []
    return clauses[:16]


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
                catalog[f"{segment_ref}:clause:{clause_index}"] = clause
    return catalog


def evidence_reference_payload(catalog: dict[str, str]) -> list[dict[str, str]]:
    """Return a deterministic model-facing reference list with exact text."""

    return [
        {"id": reference, "text": catalog[reference]}
        for reference in sorted(catalog)
    ]
