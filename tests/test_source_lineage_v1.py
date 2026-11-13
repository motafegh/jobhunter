"""Source-first bilingual evidence lineage without current P1.6 promotion."""
from __future__ import annotations

from dataclasses import replace

import pytest

from jobhunter.analysis_current import ENGLISH_PROMPT_VERSION
from jobhunter.source_bound_translation_v1 import (
    check_candidate_source_identity,
    translate_selected_spans,
)
from jobhunter.source_lineage_v1 import (
    CONTRACT_VERSION,
    align_legacy_english_field,
    original_source_spine,
)
from jobhunter.source_obligation_audit_v1 import source_skill_obligation_warnings
from jobhunter.translation.base import TranslationBatchResult, TranslationError
from jobhunter.translation_store import TranslationArtifact, TranslationSourceVersion


def _source(text: str, *, source_id: str = "fixture", version: int = 15,
            sha: str = "a" * 64, skills: list[str] | None = None
            ) -> TranslationSourceVersion:
    return TranslationSourceVersion(
        source_job_id=source_id,
        job_detail_version_id=version,
        semantic_sha256=sha,
        source_language="mixed" if any("\u0600" <= x <= "\u06ff" for x in text) else "en",
        fields={"description": text, "skills": skills or [], "language": "mixed"},
    )


def _translation(source: TranslationSourceVersion, english: str,
                 *, provenance: str = "translated"
                 ) -> TranslationArtifact:
    return TranslationArtifact(
        id=8, source_job_id=source.source_job_id,
        job_detail_version_id=source.job_detail_version_id,
        source_semantic_sha256=source.semantic_sha256,
        source_language=source.source_language,
        target_language="en",
        provider_name="lm-studio-translation-v2" if provenance == "translated"
        else "source-identity",
        provider_model="fixture" if provenance == "translated" else "native-english",
        translation_schema_version="english-projection-v2",
        fields={"description": english}, english_document=english,
        segment_provenance={"description": provenance},
        translated_segment_count=int(provenance == "translated"),
        native_segment_count=int(provenance == "native"),
        translation_sha256="b" * 64, created_at="2026-11-13T12:00:00+00:00",
    )


def _edr() -> str:
    return (
        "درباره شرکت و فعالیت‌هایش. "
        "شرح وظایف • پیاده‌سازی و پشتیبانی راهکارهای EDR "
        "• عیب‌یابی زیرساخت امنیتی سازمان "
        "• حداقل ۳ سال تجربه کاری در امنیت شبکه "
        "• تسلط بر مفاهیم Network+ و Security+ "
        "• روحیه کار تیمی مزیت محسوب می‌شود "
        "• گواهینامه تخصصی Kaspersky "
        "مزایا • بیمه تامین اجتماعی "
        "شرایط استخدام • حقوق: توافقی"
    )


def test_edr_exact_utf8_spans_preserve_local_preference_and_benefits() -> None:
    source = _source(_edr())
    spine = original_source_spine(source)
    kinds = [item.kind for item in spine.spans]
    assert kinds.count("duty_candidate") == 2
    assert kinds.count("qualification_candidate") == 3
    assert kinds.count("preferred") == 1
    assert kinds.count("benefits") == 1
    assert kinds.count("arrangement") == 1
    pref = next(x for x in spine.spans if x.kind == "preferred")
    assert pref.obligation == "preferred"
    assert pref.authority_basis == "explicit_item_preference"
    assert "مزیت محسوب می‌شود" in pref.exact_text
    assert all(
        x.obligation == "unresolved"
        for x in spine.spans if x.kind == "qualification_candidate"
    )
    assert all(
        source.fields["description"][x.start:x.end] == x.exact_text
        and source.fields["description"].encode("utf-8")[
            x.start_utf8:x.end_utf8
        ] == x.exact_text.encode("utf-8")
        for x in spine.spans
    )
    assert spine.contract_version == CONTRACT_VERSION
    assert len({x.span_id for x in spine.spans}) == len(spine.spans)


def test_persian_inline_role_questions_and_not_mandatory_skill() -> None:
    description = (
        "در این نقش چه کار می‌کنی؟ توسعه سرویس‌های Python و API. "
        "چه چیزهایی برای ما مهم است؟ تسلط به Python. "
        "آشنایی با LLMها مزیت محسوب می‌شود، اما الزامی نیست. "
        "چرا همکاری با ما؟ یادگیری مستمر."
    )
    source = _source(description, skills=["Python", "LLM", "API"])
    spine = original_source_spine(source)
    assert any(x.kind == "duty_candidate" for x in spine.spans)
    assert any(x.kind == "qualification_candidate" for x in spine.spans)
    prefs = [x for x in spine.spans if x.obligation == "preferred"]
    assert len(prefs) == 1
    assert any(x.kind == "context" for x in spine.spans)
    warnings = source_skill_obligation_warnings(spine, source)
    assert [x.structured_skill for x in warnings] == ["LLM"]
    assert warnings[0].source_span_id == prefs[0].span_id
    assert warnings[0].disposition == "requires_source_review"


def test_tiered_eligibility_is_alternative_and_not_assumed_mandatory() -> None:
    source = _source(
        "شرایط احراز: سطح Middle: دو تا چهار سال تجربه و یک پروژه عملی "
        "سطح Senior: چهار تا هفت سال تجربه و استقرار سیستم "
        "شرایط کاری: هیبرید"
    )
    spine = original_source_spine(source)
    kinds = [x.kind for x in spine.spans]
    assert "eligibility_middle_candidate" in kinds
    assert "eligibility_senior_candidate" in kinds
    assert all(x.obligation == "unresolved" for x in spine.spans
               if x.kind.startswith("eligibility_"))
    assert "arrangement" in kinds


def test_no_headings_does_not_invent_duties_or_required_strength() -> None:
    s = _source("این شرکت در حوزه فناوری فعال است و از کار تیمی پشتیبانی می‌کند.")
    result = original_source_spine(s)
    assert len(result.spans) == 1
    assert result.spans[0].kind == "unresolved"
    assert result.spans[0].obligation == "unresolved"


def test_native_english_source_has_exact_item_identity_alignment() -> None:
    source = _source("Responsibilities: Maintain backend APIs. Required Skills: Python.")
    spine = original_source_spine(source)
    projection = _translation(source, source.fields["description"], provenance="native")
    links = align_legacy_english_field(spine, source, projection)
    assert len(links) == len(spine.spans)
    assert all(x.alignment == "native_identity" and x.review_state == "unreviewed"
               for x in links)
    assert all(x.english_exact_text is not None for x in links)
    assert all(
        source.fields["description"][link.english_start:link.english_end]
        == link.english_exact_text
        for link in links
    )


def test_existing_translated_field_does_not_claim_item_alignment() -> None:
    source = _source("شرح وظایف • پشتیبانی EDR • تسلط بر شبکه")
    spine = original_source_spine(source)
    projection = _translation(
        source, "Job Description • Support EDR • Network mastery"
    )
    links = align_legacy_english_field(spine, source, projection)
    assert links
    assert all(x.alignment == "legacy_translated_field_unaligned" for x in links)
    assert all(x.english_exact_text is None and x.english_start is None
               for x in links)


def test_stale_english_projection_and_wrong_native_provenance_rejected() -> None:
    source = _source("شرح وظایف • پشتیبانی EDR")
    spine = original_source_spine(source)
    original = _translation(source, "Job Description • EDR support")
    with pytest.raises(ValueError, match="Wrong or stale"):
        align_legacy_english_field(
            spine, source, replace(original, source_semantic_sha256="0" * 64)
        )
    with pytest.raises(ValueError, match="Native"):
        align_legacy_english_field(
            spine, source, replace(original, segment_provenance={"description": "native"})
        )
    with pytest.raises(ValueError, match="Wrong or stale"):
        align_legacy_english_field(
            spine, source, replace(original, translation_schema_version="v1")
        )


def test_original_span_identity_changes_with_semantic_version() -> None:
    original = _source(_edr())
    newer = replace(original, semantic_sha256="c" * 64)
    old_spine = original_source_spine(original)
    new_spine = original_source_spine(newer)
    assert [s.span_id for s in old_spine.spans] != [
        s.span_id for s in new_spine.spans
    ]
    assert [s.exact_text for s in old_spine.spans] == [
        s.exact_text for s in new_spine.spans
    ]


class StubTranslator:
    name = "bounded-test-translator"
    model = "test-model"

    def __init__(self, texts: list[str]) -> None:
        self._texts = iter(texts)
        self.calls: list[tuple[str, ...]] = []

    def translate_texts(self, texts, *, source_language, target_language):
        assert source_language == "fa" and target_language == "en"
        assert len(texts) == 1
        self.calls.append(texts)
        return TranslationBatchResult(
            texts=(next(self._texts),), detected_languages=("fa",)
        )


def test_source_bound_translation_one_request_per_span_and_review_pending() -> None:
    s = _source("شرح وظایف • پشتیبانی EDR • آشنایی با LLMها الزامی نیست.")
    spine = original_source_spine(s)
    chosen = tuple(x.span_id for x in spine.spans if x.kind != "unresolved")
    assert len(chosen) == 2
    translator = StubTranslator([
        "Support EDR systems",
        "Familiarity with LLMs is not required.",
    ])
    candidates = translate_selected_spans(
        spine, provider=translator, selected_span_ids=chosen
    )
    assert len(translator.calls) == 2
    assert all(len(call) == 1 for call in translator.calls)
    assert candidates[0].original_span_id == chosen[0]
    assert candidates[1].status == "source_bound_unreviewed"
    assert candidates[1].review_flags == ()
    check_candidate_source_identity(spine, candidates)


def test_translation_without_explicit_not_required_cue_flags_review() -> None:
    s = _source("چه چیزهایی برای ما مهم است؟ آشنایی با LLMها الزامی نیست.")
    spine = original_source_spine(s)
    span = next(x for x in spine.spans if "LLM" in x.exact_text)
    candidates = translate_selected_spans(
        spine, provider=StubTranslator(["LLM proficiency is mandatory."]),
        selected_span_ids=(span.span_id,),
    )
    assert candidates[0].review_flags == ("explicit_not_required_cue_not_preserved",)
    check_candidate_source_identity(spine, candidates)
    assert candidates[0].status == "source_bound_unreviewed"


def test_translated_candidate_tamper_and_staleness_rejected() -> None:
    s = _source("شرح وظایف • پشتیبانی EDR")
    spine = original_source_spine(s)
    span = next(x for x in spine.spans if "EDR" in x.exact_text)
    c = translate_selected_spans(
        spine, provider=StubTranslator(["Support EDR"]),
        selected_span_ids=(span.span_id,),
    )
    with pytest.raises(ValueError, match="not bound"):
        check_candidate_source_identity(
            spine, (replace(c[0], translated_text="Support SQL"),)
        )
    with pytest.raises(ValueError, match="not bound"):
        check_candidate_source_identity(
            original_source_spine(replace(s, semantic_sha256="c" * 64)), c
        )


def test_candidate_selection_and_provider_fail_closed() -> None:
    source = _source("شرح وظایف • پیاده‌سازی EDR")
    spine = original_source_spine(source)
    span = next(x for x in spine.spans if "EDR" in x.exact_text)
    with pytest.raises(ValueError, match="Duplicate"):
        translate_selected_spans(
            spine, provider=StubTranslator([]),
            selected_span_ids=(span.span_id, span.span_id),
        )
    with pytest.raises(ValueError, match="does not belong"):
        translate_selected_spans(
            spine, provider=StubTranslator([]),
            selected_span_ids=("other",),
        )
    with pytest.raises(ValueError, match="provider"):
        translate_selected_spans(
            spine, provider=None, selected_span_ids=(span.span_id,),
        )
    with pytest.raises(TranslationError, match="Persian"):
        translate_selected_spans(
            spine, provider=StubTranslator(["پشتیبانی EDR"]),
            selected_span_ids=(span.span_id,),
        )


def test_public_current_english_route_remains_v30() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v30"


def test_mixed_explicit_required_and_optional_cues_abstain() -> None:
    text = (
        "شرایط احراز: آشنایی با Python الزامی است؛ "
        "آشنایی با LLM مزیت محسوب می‌شود اما الزامی نیست."
    )
    s = _source(text)
    spine = original_source_spine(s)
    assert any(x.kind == "qualification_candidate" for x in spine.spans)
    assert any(x.kind == "preferred" for x in spine.spans)
    compound = _source(
        "شرایط احراز: آشنایی با Python الزامی است و "
        "LLM مزیت محسوب می‌شود اما الزامی نیست."
    )
    compound_spine = original_source_spine(compound)
    assert any(
        x.authority_basis == "mixed_item_modality_requires_review"
        and x.obligation == "unresolved"
        for x in compound_spine.spans
    )


def test_generic_job_description_intro_is_not_duty_evidence() -> None:
    source = _source(
        "شرح شغل و وظایف شرکت برای توسعه تیم فنی نیرو می‌خواهد. "
        "شرایط تخصصی: آشنایی با امنیت اطلاعات "
        "شرایط عمومی: همکاری تیمی حقوق از 30 میلیون تومان"
    )
    spine = original_source_spine(source)
    assert not any(x.kind == "duty_candidate" for x in spine.spans)
    assert any(x.kind == "qualification_candidate" for x in spine.spans)
    assert any(x.kind == "arrangement" for x in spine.spans)


def test_local_model_url_prevents_external_translations() -> None:
    from pathlib import Path
    from runpy import run_path

    local_lm_studio_url = run_path(str(
        Path(__file__).resolve().parents[1]
        / "scripts/translate_p16_original_span_v1.py"
    ))["local_lm_studio_url"]

    assert local_lm_studio_url("http://127.0.0.1:18080/v1") == (
        "http://127.0.0.1:18080/v1"
    )
    assert local_lm_studio_url("http://[::1]:1234/v1") == (
        "http://[::1]:1234/v1"
    )
    for url in (
        "https://127.0.0.1:18080/v1",
        "http://example.com/v1",
        "http://127.0.0.1:18080/api",
        "http://me:secret@127.0.0.1:18080/v1",
        "http://127.0.0.1:18080/v1?next=https://example.com",
    ):
        with pytest.raises(ValueError, match="loopback"):
            local_lm_studio_url(url)


def test_duplicate_job_ids_are_reconciled_before_audit() -> None:
    from pathlib import Path
    from runpy import run_path

    _unique_job_ids = run_path(str(
        Path(__file__).resolve().parents[1]
        / "scripts/audit_p16_source_lineage_v1.py"
    ))["_unique_job_ids"]

    assert _unique_job_ids([" tNhZ ", "tNhZ", "tNDx"]) == ("tNhZ", "tNDx")
    with pytest.raises(ValueError):
        _unique_job_ids([])
    with pytest.raises(ValueError):
        _unique_job_ids(["not-a-id"])
    with pytest.raises(ValueError):
        _unique_job_ids(["tNhZ"] * 0)


def test_explicit_persian_advantage_cannot_be_silently_promoted_to_required() -> None:
    source = _source("شرح وظایف • روحیه تیمی مزیت محسوب می‌شود")
    spine = original_source_spine(source)
    item = next(x for x in spine.spans if x.kind == "preferred")
    result = translate_selected_spans(
        spine,
        provider=StubTranslator(["Teamwork is mandatory."]),
        selected_span_ids=(item.span_id,),
    )
    assert "explicit_preference_cue_not_preserved" in result[0].review_flags
    assert "possible_preference_to_mandatory_strengthening" in result[0].review_flags
    assert result[0].status == "source_bound_unreviewed"


def test_source_bound_summary_status_parser_fails_closed() -> None:
    from pathlib import Path
    from runpy import run_path

    parse = run_path(str(
        Path(__file__).resolve().parents[1]
        / "scripts/summarize_p16_source_bound_trials_v1.py"
    ))["_parse_status"]
    assert parse("source_job_id=tNDx\nexit_code=0\n") == {
        "source_job_id": "tNDx", "exit_code": "0"
    }
    with pytest.raises(ValueError, match="Malformed"):
        parse("not key value")
    with pytest.raises(ValueError, match="Duplicate"):
        parse("exit_code=0\nexit_code=1\n")
