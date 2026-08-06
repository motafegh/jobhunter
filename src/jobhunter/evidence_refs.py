"""Deterministic evidence-reference catalogs for long-form job reasoning."""

from __future__ import annotations

import re
from typing import Any

_SEGMENT_SEPARATOR_RE = re.compile(r"(?:\r?\n+|[●•▪◦]+)")


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


def _long_text_segments(text: str) -> list[str]:
    """Return exact useful sub-spans for bullet/newline-heavy source text.

    The source remains authoritative. Segments are only stable references into that source so
    models do not need to invent list indexes for concepts that live inside one long description.
    """

    if len(text) < 240 and not _SEGMENT_SEPARATOR_RE.search(text):
        return []
    pieces = [piece.strip() for piece in _SEGMENT_SEPARATOR_RE.split(text) if piece.strip()]
    if len(pieces) <= 1:
        return []
    return pieces[:80]


def build_field_evidence_catalog(fields: dict[str, Any]) -> dict[str, str]:
    """Map deterministic field/segment references to exact source text."""

    catalog: dict[str, str] = {}
    for path, text in _walk_source_strings(fields, ("field",)):
        catalog[":".join(path)] = text

    for key, value in fields.items():
        if not isinstance(value, str):
            continue
        for index, segment in enumerate(_long_text_segments(value)):
            catalog[f"field:{key}:segment:{index}"] = segment
    return catalog


def evidence_reference_payload(catalog: dict[str, str]) -> list[dict[str, str]]:
    """Return a deterministic model-facing reference list with exact text."""

    return [
        {"id": reference, "text": catalog[reference]}
        for reference in sorted(catalog)
    ]
