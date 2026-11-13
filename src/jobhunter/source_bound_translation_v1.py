"""Isolated per-source-span translation candidates with durable source identity.

Unlike the existing whole-description English projection v2, these one-to-one
calls bind each translated output to an exact original-source field span.
Translation association is mechanically proven; semantics remain unreviewed.
No public translation artifact, P1.6 artifact, or accepted state is mutated.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Literal

from jobhunter.source_lineage_v1 import OriginalSourceSpine
from jobhunter.translation.base import TranslationError, TranslationProvider
from jobhunter.translation.projection import contains_persian

TRANSLATION_CANDIDATE_CONTRACT = "p16-source-bound-translation-candidate-v1"
CandidateStatus = Literal["native_identity", "source_bound_unreviewed"]


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


_SOURCE_NEGATED_REQUIREMENT_RE = re.compile(
    r"(?:الزامی\s+نیست|اجباری\s+نیست|ضروری\s+نیست|"
    r"not\s+(?:a\s+)?requirement|not\s+required)",
    re.I,
)
_ENGLISH_NEGATED_REQUIREMENT_RE = re.compile(
    r"\b(?:not\s+(?:an?\s+)?requirement|not\s+required|"
    r"not\s+mandatory|optional|is\s+not\s+essential)\b",
    re.I,
)
_SOURCE_PREFERENCE_RE = re.compile(
    r"(?:مزیت\s+محسوب\s+می[‌\s]*شود|"
    r"مزیت\s+دارد|considered\s+an?\s+advantage)",
    re.I,
)
_ENGLISH_PREFERENCE_RE = re.compile(
    r"\b(?:advantage|advantageous|preferred|bonus|"
    r"nice[- ]to[- ]have|not\s+required|not\s+mandatory|optional)\b",
    re.I,
)
_ENGLISH_MANDATORY_ASSERTION_RE = re.compile(
    r"\b(?:is\s+(?:required|mandatory|essential)|must\s+have)\b",
    re.I,
)


@dataclass(frozen=True, slots=True)
class BoundTranslationCandidate:
    contract_version: str
    original_source_job_id: str
    original_detail_version_id: int
    original_semantic_sha256: str
    original_field_sha256: str
    original_span_id: str
    original_span_sha256: str
    provider_name: str
    provider_model: str
    translated_text: str
    translated_sha256: str
    status: CandidateStatus
    review_flags: tuple[str, ...]


def _modality_review_flags(original: str, english: str) -> tuple[str, ...]:
    # Lexical guard is deliberately *not* a linguistic verification service.
    # It can detect a lost explicit negative cue and withhold promotion; a
    # positive result cannot prove full fidelity.
    flags: list[str] = []
    source_negated = bool(_SOURCE_NEGATED_REQUIREMENT_RE.search(original))
    english_negated = bool(_ENGLISH_NEGATED_REQUIREMENT_RE.search(english))
    if source_negated and not english_negated:
        flags.append("explicit_not_required_cue_not_preserved")
    if _SOURCE_PREFERENCE_RE.search(original):
        if not _ENGLISH_PREFERENCE_RE.search(english):
            flags.append("explicit_preference_cue_not_preserved")
        if _ENGLISH_MANDATORY_ASSERTION_RE.search(english) and not english_negated:
            flags.append("possible_preference_to_mandatory_strengthening")
    return tuple(flags)


def translate_selected_spans(
    spine: OriginalSourceSpine,
    *,
    provider: TranslationProvider | None,
    selected_span_ids: tuple[str, ...],
    max_segments: int = 4,
    max_source_characters: int = 1600,
) -> tuple[BoundTranslationCandidate, ...]:
    """Translate exact source spans individually and retain review-only status.

    Stable source version IDs and checksums must be verified by the caller
    against a current, successfully parsed source *before* invoking this API.
    A transient model failure raises; no partial output is promoted.
    """
    if spine.contract_version != "p16-original-source-spine-v1":
        raise ValueError("Unsupported original source spine identity")
    if not 1 <= max_segments <= 20 or not 1 <= max_source_characters <= 12000:
        raise ValueError("Invalid bounded translation limits")
    if not 1 <= len(selected_span_ids) <= max_segments:
        raise ValueError("Selection exceeds the bounded translation budget")
    indexed = {span.span_id: span for span in spine.spans}
    if len(selected_span_ids) != len(set(selected_span_ids)):
        raise ValueError("Duplicate source span selection is not allowed")
    if any(span_id not in indexed for span_id in selected_span_ids):
        raise ValueError("Selected span does not belong to exact source version")
    selected = [indexed[span_id] for span_id in selected_span_ids]
    if any(len(span.exact_text) > max_source_characters for span in selected):
        raise ValueError("Source span exceeds bounded translation input length")
    if provider is None and any(contains_persian(s.exact_text) for s in selected):
        raise ValueError("A local translation provider is required for Persian source")
    results: list[BoundTranslationCandidate] = []
    for span in selected:
        if not contains_persian(span.exact_text):
            text = span.exact_text
            provider_name, provider_model = "source-identity", "native-english"
            status: CandidateStatus = "native_identity"
        else:
            assert provider is not None
            batch = provider.translate_texts(
                (span.exact_text,), source_language="fa", target_language="en"
            )
            if len(batch.texts) != 1:
                raise TranslationError("Bound translation did not return exactly one item")
            text = batch.texts[0]
            if not isinstance(text, str) or not text.strip():
                raise TranslationError("Bound translation is empty or malformed")
            if contains_persian(text):
                raise TranslationError("Bound English translation still contains Persian script")
            if len(text) > max(220, len(span.exact_text) * 8):
                raise TranslationError("Bound English translation expanded unreasonably")
            provider_name, provider_model = provider.name, provider.model
            status = "source_bound_unreviewed"
        results.append(BoundTranslationCandidate(
            contract_version=TRANSLATION_CANDIDATE_CONTRACT,
            original_source_job_id=spine.source_job_id,
            original_detail_version_id=spine.detail_version_id,
            original_semantic_sha256=spine.source_semantic_sha256,
            original_field_sha256=spine.field_text_sha256,
            original_span_id=span.span_id,
            original_span_sha256=span.text_sha256,
            provider_name=provider_name,
            provider_model=provider_model,
            translated_text=text,
            translated_sha256=_sha(text),
            status=status,
            review_flags=_modality_review_flags(span.exact_text, text),
        ))
    return tuple(results)


def check_candidate_source_identity(
    spine: OriginalSourceSpine, candidates: tuple[BoundTranslationCandidate, ...]
) -> None:
    """Refuse detached, forged or stale candidate claims."""
    known = {s.span_id: s for s in spine.spans}
    if len(candidates) != len({s.original_span_id for s in candidates}):
        raise ValueError("Duplicate translated source IDs")
    for candidate in candidates:
        span = known.get(candidate.original_span_id)
        if (
            candidate.contract_version != TRANSLATION_CANDIDATE_CONTRACT
            or candidate.original_source_job_id != spine.source_job_id
            or candidate.original_detail_version_id != spine.detail_version_id
            or candidate.original_semantic_sha256 != spine.source_semantic_sha256
            or candidate.original_field_sha256 != spine.field_text_sha256
            or span is None
            or candidate.original_span_sha256 != span.text_sha256
            or candidate.translated_sha256 != _sha(candidate.translated_text)
            or candidate.status not in {"native_identity", "source_bound_unreviewed"}
        ):
            raise ValueError("Translated candidate is not bound to this source version")
        if candidate.status == "native_identity" and (
            candidate.translated_text != span.exact_text
            or contains_persian(span.exact_text)
        ):
            raise ValueError("Forged native source identity translation")


__all__ = [
    "TRANSLATION_CANDIDATE_CONTRACT", "BoundTranslationCandidate",
    "translate_selected_spans", "check_candidate_source_identity",
]
