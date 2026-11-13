"""Candidate-only original-language P1.6 evidence spine and translation lineage.

Original parsed source fields are authoritative. A current English projection v2
proves *field* association, not source-item/English-item correspondence.
Neither a heading guess nor an unreviewed translated candidate becomes a
durable employer fact.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Literal

from jobhunter.translation.projection import contains_persian
from jobhunter.translation_store import TranslationArtifact, TranslationSourceVersion

CONTRACT_VERSION = "p16-original-source-spine-v1"
SpanKind = Literal[
    "duty_candidate", "qualification_candidate", "preferred",
    "benefits", "arrangement", "application", "context", "unresolved",
    "eligibility_middle_candidate", "eligibility_senior_candidate",
]
Obligation = Literal["required", "preferred", "unresolved", "not_applicable"]
AlignmentStatus = Literal["native_identity", "legacy_translated_field_unaligned"]
_BULLET_RE = re.compile(r"[•●▪◦]\s*")
_SENTENCE_GAP_RE = re.compile(r"(?<=[.!؟؛;])\s+")
_OPTIONAL_ITEM_RE = re.compile(
    r"(?:مزیت\s+محسوب\s+می[‌\s]*شود|مزیت\s+دارد|"
    r"الزامی\s+نیست|اجباری\s+نیست|ضروری\s+نیست|"
    r"not\s+(?:a\s+)?requirement|"
    r"considered\s+an?\s+advantage)",
    re.I,
)
_EXPLICIT_REQUIRED_ITEM_RE = re.compile(
    r"(?:الزامی\s+است|ضروری\s+است|باید\s+داشته|"
    r"\b(?:must\s+have|mandatory|required)\b)",
    re.I,
)
_QUALIFICATION_START_RE = re.compile(
    r"^(?:حداقل\s*[۰-۹0-9]|"
    r"(?:تسلط|آشنایی|توانایی|مهارت|گواهینامه|مدرک|سابقه|تجربه\s+کار|روحیه\s+کار|"
    r"دارای\s+تجربه)\b|"
    r"(?:minimum\s*\d|at\s+least\s*\d|mastery\s+of|"
    r"practical\s+familiarity|ability\s+to|teamwork\s+spirit)\b)",
    re.I,
)
_HEADING_DEFINITIONS: tuple[tuple[str, str], ...] = (
    ("duty_candidate", r"شرح\s+وظایف(?=\s*[•●▪◦:]|\n)"
                       r"|شرح\s+شغل\s*:"
                       r"|مسئولیت[‌\s]*های\s+اصلی\s*:"
                       r"|مسئولیت[‌\s]*ها\s*:"
                       r"|وظایف\s+شغلی\s*:"),
    ("duty_candidate", r"در\s+این\s+نقش\s+چه\s+کار\s+می[‌\s]*کنی\s*[?؟]"),
    ("qualification_candidate", r"شرایط\s+(?:احراز|تخصصی|عمومی)\s*:"
                               r"|نیازمندی[‌\s]*ها\s*:"
                               r"|"
                               r"(?:مهارت[‌\s]*های\s+(?:ضروری|مورد\s+نیاز))\s*:"),
    ("qualification_candidate", r"چه\s+چیزهایی\s+برای\s+ما\s+مهم\s+است\s*[?؟]"),
    ("preferred", r"(?:امتیازات\s+ویژه|مهارت[‌\s]*های\s+ترجیحی|"
                  r"موارد\s+امتیازی|مواردی\s+که\s+مزیت\s+محسوب\s+می[‌\s]*شوند|"
                  r"امتیاز\s+محسوب\s+می[‌\s]*شود)\s*:"),
    ("benefits", r"(?:مزایا|مزایای\s+همکاری)(?=\s*[•●▪◦:]|\n)"),
    ("arrangement", r"شرایط\s+(?:استخدام|همکاری|کاری)\s*:?"
                    r"|"
                    r"(?:محل\s+کار|نوع\s+همکاری|حقوق)\s*:"
                    r"|حقوق\s+از\s*[۰-۹0-9]+"),
    ("application", r"نحوه\s+ارسال\s+رزومه\s*:"
                    r"|برای\s+همکاری\s*،(?=\s*رزومه)"),
    ("context", r"چرا\s+همکاری\s+با\s+ما\s*[?؟]"),
    ("eligibility_middle_candidate", r"سطح\s+(?:Middle|میانی)\s*:"),
    ("eligibility_senior_candidate", r"سطح\s+(?:Senior|ارشد)\s*:"),
    ("duty_candidate", r"(?:Main\s+)?Responsibilities\s*:"
                       r"|Job\s+Description\s*:"),
    ("qualification_candidate", r"Required\s+(?:Skills|Qualifications)\s*:"
                               r"|Requirements\s*:"),
    ("preferred", r"Preferred\s+Qualifications\s*:"
                  r"|What\s+are\s+considered\s+advantages\s*:"),
    ("benefits", r"Benefits\s*:"),
    ("arrangement", r"Working\s+Conditions\s*:"),
)
_HEADING_RE = re.compile(
    "|".join(
        f"(?P<h{index}>(?<!\\w)(?:{pattern})(?=\\s|$|[•●▪◦:]))"
        for index, (_kind, pattern) in enumerate(_HEADING_DEFINITIONS)
    ),
    re.I,
)


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class OriginalSourceSpan:
    span_id: str
    field_path: str
    start: int
    end: int
    start_utf8: int
    end_utf8: int
    exact_text: str
    text_sha256: str
    kind: SpanKind
    obligation: Obligation
    authority_basis: str
    heading_text: str | None


@dataclass(frozen=True, slots=True)
class OriginalSourceSpine:
    contract_version: str
    source_job_id: str
    detail_version_id: int
    source_semantic_sha256: str
    source_language: str
    field_path: str
    field_text_sha256: str
    spans: tuple[OriginalSourceSpan, ...]


@dataclass(frozen=True, slots=True)
class FieldTranslationLink:
    source_job_id: str
    detail_version_id: int
    source_semantic_sha256: str
    translation_artifact_id: int
    translation_sha256: str
    original_span_id: str
    alignment: AlignmentStatus
    english_start: int | None
    english_end: int | None
    english_exact_text: str | None
    review_state: str = "unreviewed"


def _trim(text: str, start: int, end: int) -> tuple[int, int]:
    while start < end and text[start].isspace():
        start += 1
    while start < end and text[end - 1].isspace():
        end -= 1
    return start, end


def _pieces(text: str, begin: int, end: int) -> list[tuple[int, int]]:
    """Return lossless source offsets, splitting bullets or explicit sentences."""
    bullets = list(_BULLET_RE.finditer(text, begin, end))
    if bullets:
        bounds = [(begin, bullets[0].start())]
        bounds.extend(
            (bullet.end(), bullets[i + 1].start() if i + 1 < len(bullets) else end)
            for i, bullet in enumerate(bullets)
        )
    else:
        gaps = list(_SENTENCE_GAP_RE.finditer(text, begin, end))
        cursor = begin
        bounds = []
        for gap in gaps:
            bounds.append((cursor, gap.start()))
            cursor = gap.end()
        bounds.append((cursor, end))
    result = [_trim(text, a, b) for a, b in bounds]
    return [(a, b) for a, b in result if a < b]


def _source_kind(text: str, inherited: SpanKind) -> tuple[SpanKind, Obligation, str]:
    # Item-local employer modality overrides any broad source heading.
    if _OPTIONAL_ITEM_RE.search(text):
        if _EXPLICIT_REQUIRED_ITEM_RE.search(text):
            return "unresolved", "unresolved", "mixed_item_modality_requires_review"
        return "preferred", "preferred", "explicit_item_preference"
    if inherited == "duty_candidate" and _QUALIFICATION_START_RE.search(text):
        return "qualification_candidate", "unresolved", "qualification_cue_unreviewed"
    if inherited == "preferred":
        return inherited, "preferred", "explicit_preferred_heading"
    if inherited.startswith("eligibility_"):
        return inherited, "unresolved", "alternative_eligibility_track_unreviewed"
    if inherited == "qualification_candidate":
        return inherited, "unresolved", "qualification_heading_unreviewed"
    if inherited in {"benefits", "arrangement", "application", "context"}:
        return inherited, "not_applicable", "explicit_nonqualification_heading"
    if inherited == "duty_candidate":
        return inherited, "not_applicable", "duty_heading_unreviewed"
    return "unresolved", "unresolved", "unclassified_source_text"


def original_source_spine(
    source: TranslationSourceVersion, *, field_path: str = "description"
) -> OriginalSourceSpine:
    """Build source-version-owned references without interpreting translations."""
    if field_path != "description":
        raise ValueError("Only the versioned employer description field is supported")
    if source.job_detail_version_id <= 0 or not re.fullmatch(
        r"[a-fA-F0-9]{64}", source.semantic_sha256
    ):
        raise ValueError("Source semantic identity must be a valid version and SHA-256")
    description = source.fields.get(field_path)
    if not isinstance(description, str):
        raise ValueError("Source description is not available as exact text")
    headings = list(_HEADING_RE.finditer(description))
    spans: list[OriginalSourceSpan] = []
    chunks: list[tuple[int, int, SpanKind, str | None]] = []
    if headings:
        chunks.append((0, headings[0].start(), "unresolved", None))
        for index, heading in enumerate(headings):
            kind = next(
                k for match_index, (k, _) in enumerate(_HEADING_DEFINITIONS)
                if heading.group(f"h{match_index}") is not None
            )
            until = headings[index + 1].start() if index + 1 < len(headings) else len(description)
            chunks.append((heading.end(), until, kind, heading.group()))
    else:
        chunks.append((0, len(description), "unresolved", None))

    field_sha = _digest(description)
    for begin, end, kind, heading in chunks:
        for start, stop in _pieces(description, begin, end):
            exact = description[start:stop]
            assigned, obligation, basis = _source_kind(exact, kind)
            unique_seed = (
                f"{CONTRACT_VERSION}:{source.job_detail_version_id}:"
                f"{source.semantic_sha256}:{field_path}:{field_sha}:"
                f"{start}:{stop}:{_digest(exact)}"
            )
            spans.append(OriginalSourceSpan(
                span_id=_digest(unique_seed)[:32],
                field_path=field_path,
                start=start,
                end=stop,
                start_utf8=len(description[:start].encode("utf-8")),
                end_utf8=len(description[:stop].encode("utf-8")),
                exact_text=exact,
                text_sha256=_digest(exact),
                kind=assigned,
                obligation=obligation,
                authority_basis=basis,
                heading_text=heading,
            ))
    if len({s.span_id for s in spans}) != len(spans):
        raise ValueError("Source span identity collision")
    if any(
        description[x.start:x.end] != x.exact_text
        or _digest(x.exact_text) != x.text_sha256
        or description.encode("utf-8")[x.start_utf8:x.end_utf8] != x.exact_text.encode("utf-8")
        for x in spans
    ):
        raise ValueError("Original source span is not exact")
    return OriginalSourceSpine(
        contract_version=CONTRACT_VERSION,
        source_job_id=source.source_job_id,
        detail_version_id=source.job_detail_version_id,
        source_semantic_sha256=source.semantic_sha256,
        source_language=source.source_language,
        field_path=field_path,
        field_text_sha256=field_sha,
        spans=tuple(spans),
    )


def align_legacy_english_field(
    spine: OriginalSourceSpine,
    source: TranslationSourceVersion,
    translation: TranslationArtifact,
) -> tuple[FieldTranslationLink, ...]:
    """Return exact native identities; explicitly abstain for legacy translation.

    The current english-projection-v2 associates the *whole description* with
    a source field. It is NOT sufficient evidence for Persian-item alignment.
    """
    if (
        spine.source_job_id != source.source_job_id
        or spine.detail_version_id != source.job_detail_version_id
        or spine.source_semantic_sha256 != source.semantic_sha256
        or translation.source_job_id != source.source_job_id
        or translation.job_detail_version_id != source.job_detail_version_id
        or translation.source_semantic_sha256 != source.semantic_sha256
        or translation.translation_schema_version != "english-projection-v2"
        or spine.field_text_sha256 != _digest(str(source.fields.get(spine.field_path)))
    ):
        raise ValueError("Wrong or stale source/translation dependency identity")
    original = source.fields.get(spine.field_path)
    english = translation.fields.get(spine.field_path)
    if not isinstance(original, str) or not isinstance(english, str):
        raise ValueError("Source/translation field is not a string")
    provenance = translation.segment_provenance.get(spine.field_path)
    if provenance not in {"native", "translated"}:
        raise ValueError("Missing translation field provenance")
    identity = provenance == "native"
    if identity and (original != english or contains_persian(original)):
        raise ValueError("Native translation provenance contradicts source identity")
    results = []
    for span in spine.spans:
        results.append(FieldTranslationLink(
            source_job_id=source.source_job_id,
            detail_version_id=source.job_detail_version_id,
            source_semantic_sha256=source.semantic_sha256,
            translation_artifact_id=translation.id,
            translation_sha256=translation.translation_sha256,
            original_span_id=span.span_id,
            alignment="native_identity" if identity else "legacy_translated_field_unaligned",
            english_start=span.start if identity else None,
            english_end=span.end if identity else None,
            english_exact_text=span.exact_text if identity else None,
        ))
    return tuple(results)


__all__ = [
    "CONTRACT_VERSION", "OriginalSourceSpan", "OriginalSourceSpine",
    "FieldTranslationLink", "original_source_spine", "align_legacy_english_field",
]
