"""Passive P1.6 source identity contract: no heuristic or route promotion."""

from __future__ import annotations

from dataclasses import replace

import pytest

from jobhunter.analysis_current import ENGLISH_PROMPT_VERSION
from jobhunter.source_span_identity import (
    LEGACY_FIELD_ALIGNMENT_CONTRACT,
    SOURCE_SPAN_IDENTITY_CONTRACT,
    align_legacy_english_field,
    bind_original_source_span,
    verify_original_source_anchor,
)
from jobhunter.translation_store import TranslationArtifact, TranslationSourceVersion


def _source(
    text: str, *, job: str = "tFixture", version: int = 13,
    digest: str = "a" * 64,
) -> TranslationSourceVersion:
    return TranslationSourceVersion(
        source_job_id=job,
        job_detail_version_id=version,
        semantic_sha256=digest,
        source_language="mixed",
        fields={"description": text, "skills": ["LLM"]},
    )


def _english(
    source: TranslationSourceVersion,
    description: str, *,
    provenance: str = "translated",
) -> TranslationArtifact:
    return TranslationArtifact(
        id=44,
        source_job_id=source.source_job_id,
        job_detail_version_id=source.job_detail_version_id,
        source_semantic_sha256=source.semantic_sha256,
        source_language=source.source_language,
        target_language="en",
        provider_name="fixture",
        provider_model="fixture",
        translation_schema_version="english-projection-v2",
        fields={"description": description},
        english_document=description,
        segment_provenance={"description": provenance},
        translated_segment_count=int(provenance == "translated"),
        native_segment_count=int(provenance == "native"),
        translation_sha256="b" * 64,
        created_at="2026-11-13T00:00:00+00:00",
    )


def test_unicode_source_offsets_hashes_and_version_identity() -> None:
    text = "شرح وظایف • پشتیبانی EDR • همکاری تیمی مزیت محسوب می‌شود."
    source = _source(text)
    start = text.index("همکاری تیمی")
    end = text.index(".", start)
    anchor = bind_original_source_span(source, char_start=start, char_end=end)
    assert anchor.contract_version == SOURCE_SPAN_IDENTITY_CONTRACT
    assert anchor.exact_text == "همکاری تیمی مزیت محسوب می‌شود"
    assert anchor.utf8_start > anchor.char_start
    assert text.encode("utf-8")[anchor.utf8_start:anchor.utf8_end] == (
        anchor.exact_text.encode("utf-8")
    )
    assert len(anchor.anchor_id) == 64
    verify_original_source_anchor(anchor, source)
    assert bind_original_source_span(
        source, char_start=start, char_end=end
    ) == anchor
    assert (
        bind_original_source_span(source, char_start=0, char_end=end).anchor_id
        != anchor.anchor_id
    )


@pytest.mark.parametrize(
    "start,end",
    [(-1, 2), (0, 0), (4, 3), (0, 99), (True, 3), (1, False), ("1", 2)],
)
def test_invalid_range_rejected(start, end) -> None:
    with pytest.raises(ValueError, match="offsets"):
        bind_original_source_span(_source("hello"), char_start=start, char_end=end)


def test_empty_or_nontext_source_cannot_be_bound() -> None:
    with pytest.raises(ValueError, match="whitespace"):
        bind_original_source_span(_source("  "), char_start=0, char_end=2)
    source = replace(_source("abc"), fields={"description": None})
    with pytest.raises(ValueError, match="not text"):
        bind_original_source_span(source, char_start=0, char_end=1)
    with pytest.raises(ValueError, match="description"):
        bind_original_source_span(_source("abc"), char_start=0, char_end=1,
                                  field_path="skills")


def test_invalid_source_identity_rejected() -> None:
    for source in (
        _source("test", digest="bad"),
        _source("test", version=0),
        _source("test", job=""),
    ):
        with pytest.raises(ValueError, match="identity"):
            bind_original_source_span(source, char_start=0, char_end=3)


def test_tamper_or_stale_source_refused() -> None:
    source = _source("مدرک یا تجربه")
    anchor = bind_original_source_span(source, char_start=0, char_end=5)
    for corrupted in (
        replace(anchor, exact_text="incorrect"),
        replace(anchor, char_start=1),
        replace(anchor, anchor_id="0" * 64),
        replace(anchor, utf8_end=123),
    ):
        with pytest.raises(ValueError, match="anchor"):
            verify_original_source_anchor(corrupted, source)
    for stale_source in (
        replace(source, job_detail_version_id=14),
        replace(source, semantic_sha256="f" * 64),
        replace(source, fields={"description": "other source"}),
    ):
        with pytest.raises(ValueError, match="anchor"):
            verify_original_source_anchor(anchor, stale_source)


def test_persian_translation_v2_remains_unaligned_even_when_strings_match() -> None:
    text = "آشنایی با LLM مزیت محسوب می‌شود"
    source = _source(text)
    anchor = bind_original_source_span(source, char_start=0, char_end=len(text))
    translation = _english(source, text, provenance="translated")
    aligned = align_legacy_english_field(anchor, source, translation)
    assert aligned.contract_version == LEGACY_FIELD_ALIGNMENT_CONTRACT
    assert aligned.state == "translated_field_only_unaligned"
    assert aligned.english_char_start is None
    assert aligned.english_char_end is None
    assert aligned.english_exact_text is None
    assert aligned.semantic_review_state == "unreviewed"


def test_native_english_identity_only_when_exact() -> None:
    source = _source("Python backend API work.")
    anchor = bind_original_source_span(source, char_start=0, char_end=6)
    translation = _english(source, "Python backend API work.", provenance="native")
    result = align_legacy_english_field(anchor, source, translation)
    assert result.state == "native_english_exact"
    assert (result.english_char_start, result.english_char_end) == (0, 6)
    assert result.english_exact_text == "Python"

    for wrong_translation in (
        replace(translation, fields={"description": "Changed."}),
        replace(translation, segment_provenance={"description": "translated"}),
    ):
        if wrong_translation.segment_provenance["description"] == "native":
            with pytest.raises(ValueError, match="Native-English"):
                align_legacy_english_field(anchor, source, wrong_translation)
        else:
            assert (
                align_legacy_english_field(anchor, source, wrong_translation).state
                == "translated_field_only_unaligned"
            )


def test_native_persian_cannot_be_misrepresented_as_identity() -> None:
    original = _source("کارشناسی امنیت")
    anchor = bind_original_source_span(
        original, char_start=0, char_end=len(original.fields["description"])
    )
    translation = _english(original, original.fields["description"], provenance="native")
    with pytest.raises(ValueError, match="Native-English"):
        align_legacy_english_field(anchor, original, translation)


def test_stale_translation_and_invalid_provenance_rejected() -> None:
    source = _source("شرح وظایف • پشتیبانی")
    anchor = bind_original_source_span(source, char_start=0, char_end=4)
    projection = _english(source, "Description: support")
    for wrong in (
        replace(projection, source_job_id="other"),
        replace(projection, job_detail_version_id=999),
        replace(projection, source_semantic_sha256="f" * 64),
        replace(projection, translation_schema_version="v3"),
        replace(projection, target_language="fa"),
        replace(projection, translation_sha256="bad"),
        replace(projection, id=0),
    ):
        with pytest.raises(ValueError, match="projection"):
            align_legacy_english_field(anchor, source, wrong)
    with pytest.raises(ValueError, match="provenance"):
        align_legacy_english_field(
            anchor, source, replace(projection, segment_provenance={"description": "unknown"})
        )


def test_pure_identity_module_does_not_change_public_analysis() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v30"
