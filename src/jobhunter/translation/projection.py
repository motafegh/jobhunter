"""Build complete English representations without replacing source evidence."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

TRANSLATION_SCHEMA_VERSION = "english-projection-v1"
_PERSIAN_RE = re.compile(r"[\u0600-\u06ff]")
_SOURCE_METADATA_FIELDS = {"language", "parser_version"}
_FIELD_LABELS = {
    "title": "Title",
    "company": "Company",
    "job_category": "Job category",
    "location": "Location",
    "employment_type": "Employment type",
    "minimum_experience": "Minimum experience",
    "salary": "Salary",
    "skills": "Required skill tags",
    "gender": "Gender",
    "military_service": "Military service",
    "education": "Education",
    "date_posted": "Date posted",
    "valid_through": "Valid through",
    "description": "Job description",
    "company_description": "Company description",
}
_FIELD_ORDER = tuple(_FIELD_LABELS)


@dataclass(frozen=True, slots=True)
class EnglishProjection:
    """English fields plus provenance for each text segment."""

    fields: dict[str, Any]
    document: str
    segment_provenance: dict[str, str]
    translated_segment_count: int
    native_segment_count: int
    projection_sha256: str


def contains_persian(text: str) -> bool:
    """Return whether a string contains Persian/Arabic-script code points."""

    return bool(_PERSIAN_RE.search(text))


def source_fields_for_projection(fields: dict[str, Any]) -> dict[str, Any]:
    """Remove parser metadata that does not belong in the English job document."""

    return {
        key: value
        for key, value in fields.items()
        if key not in _SOURCE_METADATA_FIELDS
    }


def _walk_strings(
    value: Any,
    *,
    path: str,
    visitor: Callable[[str, str], None],
) -> None:
    if isinstance(value, str):
        visitor(path, value)
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _walk_strings(item, path=f"{path}[{index}]", visitor=visitor)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{path}.{key}" if path else str(key)
            _walk_strings(item, path=child, visitor=visitor)


def collect_translatable_texts(fields: dict[str, Any]) -> tuple[str, ...]:
    """Collect unique Persian-containing strings in stable encounter order."""

    seen: set[str] = set()
    result: list[str] = []

    def visitor(_path: str, text: str) -> None:
        if not contains_persian(text) or text in seen:
            return
        seen.add(text)
        result.append(text)

    _walk_strings(source_fields_for_projection(fields), path="", visitor=visitor)
    return tuple(result)


def translation_required(fields: dict[str, Any]) -> bool:
    """Return whether any projected field contains Persian text."""

    return bool(collect_translatable_texts(fields))


def _project_value(
    value: Any,
    *,
    path: str,
    translations: dict[str, str],
    provenance: dict[str, str],
) -> Any:
    if isinstance(value, str):
        if contains_persian(value):
            translated = translations.get(value)
            if translated is None:
                raise ValueError(f"Missing translation for source segment at {path}")
            provenance[path] = "translated"
            return translated
        provenance[path] = "native"
        return value
    if isinstance(value, list):
        return [
            _project_value(
                item,
                path=f"{path}[{index}]",
                translations=translations,
                provenance=provenance,
            )
            for index, item in enumerate(value)
        ]
    if isinstance(value, dict):
        return {
            key: _project_value(
                item,
                path=f"{path}.{key}" if path else str(key),
                translations=translations,
                provenance=provenance,
            )
            for key, item in value.items()
        }
    return value


def _render_value(value: Any) -> str:
    if value is None:
        return "(not available)"
    if isinstance(value, list):
        return "\n".join(f"- {_render_value(item)}" for item in value) or "(not available)"
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def build_english_document(fields: dict[str, Any]) -> str:
    """Render one complete canonical English document from projected fields."""

    sections: list[str] = []
    emitted: set[str] = set()
    for key in _FIELD_ORDER:
        if key not in fields:
            continue
        emitted.add(key)
        label = _FIELD_LABELS[key]
        sections.append(f"{label}:\n{_render_value(fields[key])}")
    for key, value in fields.items():
        if key in emitted:
            continue
        label = key.replace("_", " ").title()
        sections.append(f"{label}:\n{_render_value(value)}")
    return "\n\n".join(sections)


def build_english_projection(
    fields: dict[str, Any],
    *,
    translations: dict[str, str],
) -> EnglishProjection:
    """Project one parsed source document into English with segment provenance."""

    provenance: dict[str, str] = {}
    projected = _project_value(
        source_fields_for_projection(fields),
        path="",
        translations=translations,
        provenance=provenance,
    )
    if not isinstance(projected, dict):
        raise TypeError("English projection root must remain a dictionary")
    document = build_english_document(projected)
    translated_count = sum(value == "translated" for value in provenance.values())
    native_count = sum(value == "native" for value in provenance.values())
    canonical = json.dumps(
        {
            "fields": projected,
            "segment_provenance": provenance,
            "schema": TRANSLATION_SCHEMA_VERSION,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return EnglishProjection(
        fields=projected,
        document=document,
        segment_provenance=provenance,
        translated_segment_count=translated_count,
        native_segment_count=native_count,
        projection_sha256=hashlib.sha256(canonical).hexdigest(),
    )
