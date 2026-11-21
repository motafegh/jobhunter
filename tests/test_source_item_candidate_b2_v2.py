"""B2v2 non-authoritative source-structure diagnostic: positive and negative cases.

Never claim a source heading is factual eligibility authority. These fixtures
are synthetic; the real eight-source source-first review remains ignored/private.
"""

from __future__ import annotations

from pathlib import Path
from runpy import run_path

import pytest

from jobhunter.source_eligibility_candidate_b2 import build_candidate_eligibility_logic
from jobhunter.source_item_candidate_b2 import (
    interpret_original_source_candidate,
    verify_b2_candidate,
)
from jobhunter.source_item_candidate_b2_v2 import (
    B2V2_ENGINE,
    build_candidate_eligibility_logic_v2,
    interpret_original_source_candidate_v2,
)
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_B0 = (
    ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
)


def source(text: str, **fields: object) -> TranslationSourceVersion:
    return TranslationSourceVersion(
        source_job_id="fixtureB2v2",
        job_detail_version_id=91,
        semantic_sha256="a" * 64,
        source_language="mixed",
        fields={"description": text, **fields},
    )


def items(text: str, **fields: object):
    original = source(text, **fields)
    result = interpret_original_source_candidate_v2(original)
    verify_b2_candidate(result, original)
    for item in result.items:
        a = item.anchor
        assert text[a.char_start : a.char_end] == a.exact_text
        assert text.encode()[a.utf8_start : a.utf8_end] == a.exact_text.encode()
        assert a.semantic_sha256 == original.semantic_sha256
        assert a.source_job_id == original.source_job_id
    assert result.authority == "candidate_only_no_downstream_reuse"
    return result


def test_successor_parser_is_versioned_and_does_not_replace_baseline_B2():
    assert B2V2_ENGINE.endswith("exposed-candidate-v2")
    old = interpret_original_source_candidate
    assert old.__module__ == "jobhunter.source_item_candidate_b2"
    assert interpret_original_source_candidate_v2 is not old


def test_flattened_persian_duties_requirements_and_benefits_are_distinct():
    result = items(
        "برای توسعه تیم از فرد باتجربه استقبال می‌کنیم. "
        "مسئولیت‌ها: طراحی سرویس‌های Backend توسعه پردازش‌های Async "
        "همکاری با تیم DevOps "
        "مهارت‌ها و الزامات فنی: تسلط بالا به Python "
        "تجربه حرفه‌ای با Django و REST API "
        "مزایا: بیمه تکمیلی"
    )
    duties = [i.anchor.exact_text for i in result.items if i.category == "work_duty"]
    qualifications = [
        i.anchor.exact_text for i in result.items if i.category == "candidate_qualification"
    ]
    assert any("طراحی سرویس‌های Backend" in x for x in duties)
    assert any("توسعه پردازش‌های Async" in x for x in duties)
    assert any("تسلط بالا به Python" in x for x in qualifications)
    assert any("تجربه حرفه‌ای با Django" in x for x in qualifications)
    assert not any("تسلط" in x for x in duties)
    assert any(i.category == "benefit" and "بیمه" in i.anchor.exact_text for i in result.items)


def test_qualified_implementation_phrase_is_not_fabricated_as_work_duty():
    text = (
        "مسئولیت ها: طراحی و ساخت AI Agent "
        "تجربه عملی در طراحی، پیاده‌سازی و بهینه‌سازی سیستم‌های RAG "
        "تجربه کار با Python "
        "ساخت Workflow و اتوماسیون فرایندها"
    )
    result = items(text)
    candidate_qualifications = [
        i.anchor.exact_text for i in result.items if i.category == "candidate_qualification"
    ]
    assert any(
        "تجربه عملی در طراحی، پیاده‌سازی و بهینه‌سازی سیستم‌های RAG" in q
        for q in candidate_qualifications
    )
    assert not any(
        "پیاده‌سازی و بهینه‌سازی سیستم‌های RAG" in item.anchor.exact_text
        and item.category == "work_duty"
        for item in result.items
    )
    assert any(
        "ساخت Workflow" in i.anchor.exact_text and i.category == "work_duty" for i in result.items
    )


def test_persian_preferred_section_prevents_two_false_required_skills():
    result = items(
        "شرح وظایف: · شناسایی تهدیدات · تحلیل لاگ‌ها · توسعه تشخیص "
        "شرایط احراز: آشنایی با MITRE ATT&CK "
        "مهارت های زیر امتیاز محسوب می شود: "
        "توانایی تحلیل بدافزار در سطح پایه آشنایی با PowerShell و Sysinternals "
        "مزایا: بیمه تکمیلی محل کار گرم‌دره می باشد."
    )
    preferred = [
        i
        for i in result.items
        if i.category == "candidate_qualification" and i.employer_strength == "preferred"
    ]
    assert any("تحلیل بدافزار" in i.anchor.exact_text for i in preferred)
    assert any("PowerShell" in i.anchor.exact_text for i in preferred)
    assert not any(
        i.employer_strength == "required"
        for i in result.items
        if "PowerShell" in i.anchor.exact_text or "بدافزار" in i.anchor.exact_text
    )
    assert any(
        i.category == "work_arrangement" and "گرم‌دره" in i.anchor.exact_text for i in result.items
    )


def test_english_job_section_roles_negation_and_bonus_are_preserved():
    result = items(
        "About Us We build software for researchers. "
        "What You'll Work On Build Docker-based evaluation environments. "
        "Develop synthetic data pipelines. "
        "What Makes You a Great Fit "
        "Experience building reliable production systems. "
        "No research publications or model-training experience required. "
        "Bonus Points Hands-on experience with LLM APIs. "
        "What You'll Get Remote Work: Work remotely. "
        "Relocation Support: Optional relocation assistance."
    )
    assert any(
        i.category == "work_duty" and "Docker-based evaluation environments" in i.anchor.exact_text
        for i in result.items
    )
    assert any(
        i.category == "candidate_qualification" and "production systems" in i.anchor.exact_text
        for i in result.items
    )
    assert any(
        "research publications" in i.anchor.exact_text
        and i.employer_strength != "required"
        and i.qualifier == "negative_explicit"
        for i in result.items
    )
    assert any(
        i.employer_strength == "preferred" and "LLM APIs" in i.anchor.exact_text
        for i in result.items
    )
    assert any(
        i.category == "work_arrangement" and "Remote" in i.anchor.exact_text for i in result.items
    )


def test_duty_named_framework_does_not_become_mandatory_prior_experience():
    result = items(
        "مسئولیت‌های کلیدی طراحی و پیاده‌سازی Agent ها با استفاده "
        "از فریم‌ورک‌های مدرن مانند LangChain. "
        "دانش و مهارت‌های مورد نیاز: تسلط بر Python."
    )
    assert any(
        i.category == "work_duty" and "مانند LangChain" in i.anchor.exact_text for i in result.items
    )
    assert not any(
        i.category == "candidate_qualification"
        and i.employer_strength == "required"
        and "LangChain" in i.anchor.exact_text
        for i in result.items
    )


def test_one_or_more_specialties_are_provisional_without_invented_or_graph():
    text = (
        "حوزه‌های تخصصی و مهارت‌های موردنیاز "
        "۱. ارزیابی امنیت وب و API "
        "۲. ارزیابی امنیت موبایل "
        "۳. بررسی سورس‌کد "
        "متقاضی لازم نیست در تمام زمینه‌های ذکرشده تخصص داشته باشد، "
        "داشتن دانش عمیق و تجربه در یک یا چند حوزه تخصصی اولویت دارد. "
        "نکته مهم جذب نیرو برای حوزه‌های تخصصی مختلف به‌صورت مجزا انجام می‌شود."
    )
    src = source(text)
    candidate = interpret_original_source_candidate_v2(src)
    verify_b2_candidate(candidate, src)
    group = [
        a for a in candidate.alternatives if a.kind == "one_or_more_separately_hired_specialties"
    ]
    assert len(group) == 1
    assert group[0].logical_operator == "any_of_unresolved_option_boundaries"
    assert group[0].interpretation_status == "candidate_unreviewed_not_eligibility_authority"
    assert set(group[0].source_anchor_ids) <= {i.anchor.anchor_id for i in candidate.items}
    logic = build_candidate_eligibility_logic_v2(src, candidate)
    assert logic.graphs == ()
    assert group[0].kind in logic.unresolved_group_kinds


@pytest.mark.parametrize(
    "text",
    [
        "حوزه‌های تخصصی و مهارت‌های موردنیاز مهارت در شبکه و امنیت لازم است.",
        "لازم نیست در تمام حوزه‌های تخصص داشته باشید اما باید همه ابزارهای لازم را بشناسید.",
        "در یک یا چند حوزه تجربه عملی دارید. شرایط همکاری به صورت مجزا تعیین می‌شود.",
        "همه نقش‌ها به صورت جداگانه بررسی می‌شوند و هر فرد باید در تمام موارد مهارت داشته باشد.",
    ],
)
def test_ambiguous_or_unrelated_choice_words_do_not_produce_alternative(text):
    src = source(text)
    candidate = interpret_original_source_candidate_v2(src)
    assert not any(
        a.kind == "one_or_more_separately_hired_specialties" for a in candidate.alternatives
    )


def test_required_and_preferred_in_compound_remain_unresolved():
    result = items("Requirements: Python required, LLM preferred.")
    assert all(
        i.employer_strength != "required"
        for i in result.items
        if i.category == "candidate_qualification"
    )
    assert any(i.employer_strength == "unresolved" for i in result.items)


@pytest.mark.parametrize(
    ("job", "expected_graph", "expected_duties"),
    [
        ("tNhZ", 0, 6),
        ("tMps", 1, 11),
        ("tNDx", 1, 5),
        ("tMjm", 0, 0),
    ],
)
def test_previous_exposed_B0_candidate_graphs_are_preserved(
    job: str, expected_graph: int, expected_duties: int
):
    if not PRIVATE_B0.exists():
        pytest.skip("Private B0 source snapshot intentionally absent from CI")
    src = TranslationStore(PRIVATE_B0).latest_source_version(job)
    assert src is not None
    previous = interpret_original_source_candidate(src)
    candidate = interpret_original_source_candidate_v2(src)
    logic = build_candidate_eligibility_logic_v2(src, candidate)
    assert len(logic.graphs) == expected_graph
    assert sum(i.category == "work_duty" for i in candidate.items) == expected_duties
    assert {g.graph_id for g in logic.graphs} == {
        g.graph_id for g in build_candidate_eligibility_logic(src, previous).graphs
    }
    assert previous.authority == candidate.authority


def test_new_candidate_preserves_existing_B1_draft_provenance_contract():
    src = source(
        "مسئولیت‌ها: طراحی و نگهداری APIها. "
        "مهارت‌ها و الزامات فنی: تسلط به Python. "
        "مزایا: بیمه تکمیلی",
        skills=["Python"],
    )
    candidate = interpret_original_source_candidate_v2(src)
    b1 = run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))["b1_design_from_b2"]
    validate = run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))["validate_bundle"]
    draft = b1(candidate, src)
    validate(draft, source=src)
    assert draft["authority"] == "candidate_only_no_downstream_reuse"
    assert draft["review_events"] == []
    assert draft["brief"]["downstream_authority"] == "none"
