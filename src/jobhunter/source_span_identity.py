"""Passive, exact-source span identity for future bilingual P1.6 evidence.

This module is deliberately NOT a source-section classifier, semantic
validator, translation provider, P1.6 router or persistence migration.

Its only authority is exact source text, source-version identity and a
truthful description of what legacy field-level English provenance proves.
The earlier heuristic research spine has a different contract and span IDs.
Never silently substitute its IDs for anchors produced by this module.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Literal

from jobhunter.translation.projection import contains_persian
from jobhunter.translation_store import TranslationArtifact, TranslationSourceVersion

SOURCE_SPAN_IDENTITY_CONTRACT = "jobhunter-source-span-identity-v1"
LEGACY_FIELD_ALIGNMENT_CONTRACT = "jobhunter-legacy-field-alignment-v1"
_SHA256_PATTERN = re.compile(r"[0-9a-fA-F]{64}\Z")
AlignmentState = Literal["native_english_exact", "translated_field_only_unaligned"]


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _source_field(source: TranslationSourceVersion, field: str) -> str:
    if field != "description":
        raise ValueError("Only exact employer description spans are supported")
    if (
        not source.source_job_id
        or source.job_detail_version_id <= 0
        or not _SHA256_PATTERN.fullmatch(source.semantic_sha256)
    ):
        raise ValueError("Missing or invalid source version identity")
    text = source.fields.get(field)
    if not isinstance(text, str):
        raise ValueError("Selected original source field is not text")
    return text


@dataclass(frozen=True, slots=True)
class OriginalSourceAnchor:
    contract_version: str
    anchor_id: str
    source_job_id: str
    job_detail_version_id: int
    semantic_sha256: str
    field_path: str
    field_sha256: str
    char_start: int
    char_end: int
    utf8_start: int
    utf8_end: int
    text_sha256: str
    exact_text: str


@dataclass(frozen=True, slots=True)
class LegacyFieldAlignment:
    contract_version: str
    source_anchor_id: str
    source_semantic_sha256: str
    translation_artifact_id: int
    translation_sha256: str
    state: AlignmentState
    english_char_start: int | None
    english_char_end: int | None
    english_exact_text: str | None
    semantic_review_state: str = "unreviewed"


def bind_original_source_span(
    source: TranslationSourceVersion,
    *,
    char_start: int,
    char_end: int,
    field_path: str = "description",
) -> OriginalSourceAnchor:
    """Identify the supplied exact span without guessing any semantic category.

    Both end points are Python Unicode-character offsets in the parsed source.
    Byte offsets are separately provided for hash- and UTF-8-aware consumers.
    A candidate's obligation/duty/preference interpretation is *not* inferred.
    """
    text = _source_field(source, field_path)
    if (
        isinstance(char_start, bool)
        or isinstance(char_end, bool)
        or not isinstance(char_start, int)
        or not isinstance(char_end, int)
        or char_start < 0
        or char_end <= char_start
        or char_end > len(text)
    ):
        raise ValueError("Source span offsets must be nonempty and in range")
    exact = text[char_start:char_end]
    if not exact.strip():
        raise ValueError("Source span cannot contain only whitespace")

    field_sha256 = _sha256(text)
    text_sha256 = _sha256(exact)
    seed = (
        f"{SOURCE_SPAN_IDENTITY_CONTRACT}:{source.source_job_id}:"
        f"{source.job_detail_version_id}:{source.semantic_sha256}:"
        f"{field_path}:{field_sha256}:{char_start}:{char_end}:{text_sha256}"
    )
    return OriginalSourceAnchor(
        contract_version=SOURCE_SPAN_IDENTITY_CONTRACT,
        anchor_id=_sha256(seed),
        source_job_id=source.source_job_id,
        job_detail_version_id=source.job_detail_version_id,
        semantic_sha256=source.semantic_sha256,
        field_path=field_path,
        field_sha256=field_sha256,
        char_start=char_start,
        char_end=char_end,
        utf8_start=len(text[:char_start].encode("utf-8")),
        utf8_end=len(text[:char_end].encode("utf-8")),
        text_sha256=text_sha256,
        exact_text=exact,
    )


def verify_original_source_anchor(
    anchor: OriginalSourceAnchor, source: TranslationSourceVersion
) -> None:
    """Reject tampered/stale exact spans, including alternate source versions."""
    if (
        anchor.contract_version != SOURCE_SPAN_IDENTITY_CONTRACT
        or anchor.source_job_id != source.source_job_id
        or anchor.job_detail_version_id != source.job_detail_version_id
        or anchor.semantic_sha256 != source.semantic_sha256
    ):
        raise ValueError("Source anchor version or identity is stale")
    rebuilt = bind_original_source_span(
        source, char_start=anchor.char_start, char_end=anchor.char_end,
        field_path=anchor.field_path
    )
    if rebuilt != anchor:
        raise ValueError("Source anchor content, offsets or hash do not match")


def align_legacy_english_field(
    anchor: OriginalSourceAnchor,
    source: TranslationSourceVersion,
    translation: TranslationArtifact,
) -> LegacyFieldAlignment:
    """Describe exactly what English projection v2 proves for one source anchor.

    A translated *field* never authorizes a fabricated 1-to-1 English item
    alignment. Native English fields can be aligned only when byte-exact.
    """
    verify_original_source_anchor(anchor, source)
    if (
        translation.id <= 0
        or translation.source_job_id != anchor.source_job_id
        or translation.job_detail_version_id != anchor.job_detail_version_id
        or translation.source_semantic_sha256 != anchor.semantic_sha256
        or translation.translation_schema_version != "english-projection-v2"
        or translation.target_language != "en"
        or not _SHA256_PATTERN.fullmatch(translation.translation_sha256)
    ):
        raise ValueError("English projection is not bound to the source version")
    original_field = _source_field(source, anchor.field_path)
    english_field = translation.fields.get(anchor.field_path)
    if not isinstance(english_field, str):
        raise ValueError("English projection does not contain a description field")
    provenance = translation.segment_provenance.get(anchor.field_path)
    if provenance == "native":
        if original_field != english_field or contains_persian(original_field):
            raise ValueError("Native-English provenance is not an exact identity")
        return LegacyFieldAlignment(
            contract_version=LEGACY_FIELD_ALIGNMENT_CONTRACT,
            source_anchor_id=anchor.anchor_id,
            source_semantic_sha256=anchor.semantic_sha256,
            translation_artifact_id=translation.id,
            translation_sha256=translation.translation_sha256,
            state="native_english_exact",
            english_char_start=anchor.char_start,
            english_char_end=anchor.char_end,
            english_exact_text=anchor.exact_text,
        )
    if provenance != "translated":
        raise ValueError("Translation field provenance is absent or unsupported")
    return LegacyFieldAlignment(
        contract_version=LEGACY_FIELD_ALIGNMENT_CONTRACT,
        source_anchor_id=anchor.anchor_id,
        source_semantic_sha256=anchor.semantic_sha256,
        translation_artifact_id=translation.id,
        translation_sha256=translation.translation_sha256,
        state="translated_field_only_unaligned",
        english_char_start=None,
        english_char_end=None,
        english_exact_text=None,
    )


__all__ = [
    "SOURCE_SPAN_IDENTITY_CONTRACT",
    "LEGACY_FIELD_ALIGNMENT_CONTRACT",
    "OriginalSourceAnchor",
    "LegacyFieldAlignment",
    "bind_original_source_span",
    "verify_original_source_anchor",
    "align_legacy_english_field",
]
