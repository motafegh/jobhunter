"""Deterministic integrity checks for derived English job projections."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from jobhunter.translation.base import TranslationError
from jobhunter.translation.projection import EnglishProjection, contains_persian

_SCALAR_FIELDS = {
    "title",
    "company",
    "job_category",
    "location",
    "employment_type",
    "minimum_experience",
    "salary",
    "gender",
    "military_service",
    "education",
}
_LONG_FIELDS = {"description", "company_description"}
_UNCHANGED_FIELDS = {"date_posted", "valid_through"}


@dataclass(frozen=True, slots=True)
class TranslationIntegrityFinding:
    """One deterministic reason an English projection is unsafe to accept."""

    code: str
    path: str
    message: str


@dataclass(frozen=True, slots=True)
class TranslationIntegrityReport:
    """Integrity result for one source/projection pair."""

    findings: tuple[TranslationIntegrityFinding, ...]

    @property
    def clean(self) -> bool:
        return not self.findings


def _shape(value: Any) -> str:
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "dict"
    if value is None:
        return "none"
    return "scalar"


def _walk_shapes(source: Any, english: Any, *, path: str, findings: list[TranslationIntegrityFinding]) -> None:
    if _shape(source) != _shape(english):
        findings.append(
            TranslationIntegrityFinding(
                code="shape_mismatch",
                path=path,
                message=f"source shape {_shape(source)!r} became {_shape(english)!r}",
            )
        )
        return
    if isinstance(source, list):
        if len(source) != len(english):
            findings.append(
                TranslationIntegrityFinding(
                    code="list_length_mismatch",
                    path=path,
                    message=f"source has {len(source)} items but English has {len(english)}",
                )
            )
            return
        for index, source_item in enumerate(source):
            _walk_shapes(
                source_item,
                english[index],
                path=f"{path}[{index}]",
                findings=findings,
            )
    elif isinstance(source, dict):
        if set(source) != set(english):
            findings.append(
                TranslationIntegrityFinding(
                    code="object_keys_mismatch",
                    path=path,
                    message="source and English object keys differ",
                )
            )
            return
        for key, source_item in source.items():
            _walk_shapes(
                source_item,
                english[key],
                path=f"{path}.{key}" if path else str(key),
                findings=findings,
            )


def _check_scalar(
    field: str,
    source: str,
    english: str,
    *,
    findings: list[TranslationIntegrityFinding],
) -> None:
    if not english.strip():
        findings.append(
            TranslationIntegrityFinding(
                code="empty_translation",
                path=field,
                message="non-empty source field became empty",
            )
        )
        return
    if "\n" in english or len(english) > max(220, len(source) * 10):
        findings.append(
            TranslationIntegrityFinding(
                code="suspicious_scalar_expansion",
                path=field,
                message=(
                    "short scalar field expanded like a paragraph; this can indicate "
                    "field-to-translation misassociation"
                ),
            )
        )
    if contains_persian(source) and contains_persian(english):
        findings.append(
            TranslationIntegrityFinding(
                code="persian_remains",
                path=field,
                message="translated scalar still contains Persian/Arabic-script text",
            )
        )


def _check_long_text(
    field: str,
    source: str,
    english: str,
    *,
    findings: list[TranslationIntegrityFinding],
) -> None:
    if not source.strip() or not english.strip():
        if source.strip() and not english.strip():
            findings.append(
                TranslationIntegrityFinding(
                    code="empty_translation",
                    path=field,
                    message="non-empty long source field became empty",
                )
            )
        return
    if len(source) >= 250 and len(english) < max(80, int(len(source) * 0.18)):
        findings.append(
            TranslationIntegrityFinding(
                code="suspicious_omission",
                path=field,
                message="English long-form text is implausibly short for the source",
            )
        )
    if len(english) > max(1200, len(source) * 5):
        findings.append(
            TranslationIntegrityFinding(
                code="suspicious_expansion",
                path=field,
                message="English long-form text is implausibly larger than the source",
            )
        )


def audit_translation_integrity(
    source_fields: dict[str, Any],
    projection: EnglishProjection,
) -> TranslationIntegrityReport:
    """Reject structural corruption without pretending to judge translation fluency."""

    english_fields = projection.fields
    findings: list[TranslationIntegrityFinding] = []
    source_projected = {
        key: value
        for key, value in source_fields.items()
        if key not in {"language", "parser_version"}
    }
    if set(source_projected) != set(english_fields):
        findings.append(
            TranslationIntegrityFinding(
                code="root_keys_mismatch",
                path="",
                message="source and English root fields differ",
            )
        )
        return TranslationIntegrityReport(findings=tuple(findings))

    _walk_shapes(source_projected, english_fields, path="", findings=findings)

    for field in _UNCHANGED_FIELDS:
        if source_projected.get(field) != english_fields.get(field):
            findings.append(
                TranslationIntegrityFinding(
                    code="stable_field_changed",
                    path=field,
                    message="date/non-translated stable field changed in English projection",
                )
            )

    for field in _SCALAR_FIELDS:
        source = source_projected.get(field)
        english = english_fields.get(field)
        if isinstance(source, str) and isinstance(english, str):
            _check_scalar(field, source, english, findings=findings)

    for field in _LONG_FIELDS:
        source = source_projected.get(field)
        english = english_fields.get(field)
        if isinstance(source, str) and isinstance(english, str):
            _check_long_text(field, source, english, findings=findings)

    for path, provenance in projection.segment_provenance.items():
        if provenance != "translated":
            continue
        value: Any = english_fields
        try:
            # Provenance paths are only used for diagnostics here; scalar top-level checks
            # already cover the source fields most vulnerable to permutation corruption.
            if "[" not in path and "." not in path:
                value = english_fields[path]
        except (KeyError, TypeError):
            continue
        if isinstance(value, str) and contains_persian(value):
            findings.append(
                TranslationIntegrityFinding(
                    code="translated_segment_not_english",
                    path=path,
                    message="translated segment still contains Persian/Arabic script",
                )
            )

    return TranslationIntegrityReport(findings=tuple(findings))


def require_translation_integrity(
    source_fields: dict[str, Any],
    projection: EnglishProjection,
) -> TranslationIntegrityReport:
    """Return a clean report or fail before a corrupt artifact can become current."""

    report = audit_translation_integrity(source_fields, projection)
    if report.clean:
        return report
    preview = "; ".join(
        f"{finding.path or '<root>'}: {finding.code}" for finding in report.findings[:6]
    )
    raise TranslationError(f"English projection failed integrity checks: {preview}")
