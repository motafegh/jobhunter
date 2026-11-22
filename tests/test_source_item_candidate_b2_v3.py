"""B2v3 general section-heading semantic boundaries and exposed regressions.

All tests are source-first: headings and spans are original source claims;
labels are unreviewed hypotheses and never confer accepted employer authority.
"""

from __future__ import annotations

import runpy
from pathlib import Path

import pytest

from jobhunter.source_eligibility_candidate_b2 import build_candidate_eligibility_logic
from jobhunter.source_item_candidate_b2 import verify_b2_candidate
from jobhunter.source_item_candidate_b2_v2 import interpret_original_source_candidate_v2
from jobhunter.source_item_candidate_b2_v3 import (
    B2V3_ENGINE,
    build_candidate_eligibility_logic_v3,
    interpret_original_source_candidate_v3,
)
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"
NEW = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-22/second-source-cohort-v1"
B0 = ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen"


def make_source(text: str) -> TranslationSourceVersion:
    return TranslationSourceVersion(
        source_job_id="synthetic-v3",
        job_detail_version_id=17,
        semantic_sha256="e" * 64,
        source_language="mixed",
        fields={"description": text},
    )


def candidate(text: str):
    source = make_source(text)
    view = interpret_original_source_candidate_v3(source)
    verify_b2_candidate(view, source)
    for unit in view.items:
        a = unit.anchor
        assert a.source_job_id == source.source_job_id
        assert text[a.char_start : a.char_end] == a.exact_text
        assert text.encode()[a.utf8_start : a.utf8_end] == a.exact_text.encode()
        assert a.semantic_sha256 == source.semantic_sha256
        assert unit.interpretation_status == "candidate_unreviewed"
    assert view.authority == "candidate_only_no_downstream_reuse"
    return view


def test_versioned_new_engine_does_not_rewrite_original_B2v2():
    assert B2V3_ENGINE.endswith("original-section-candidate-v3")
    assert interpret_original_source_candidate_v2.__module__.endswith("source_item_candidate_b2_v2")
    assert interpret_original_source_candidate_v3 is not interpret_original_source_candidate_v2


def test_flattened_persian_no_colon_roles_duties_qualifications_and_bonus():
    view = candidate(
        "ما در حال ساخت محصول هستیم. مسئولیت‌ها طراحی و توسعه سرویس‌های Python "
        "تست و پایش سرویس‌ها مهارت‌ها و توانمندی‌های موردنیاز "
        "تسلط به Python تجربه کار با SQL مهارت‌های امتیازی "
        "تجربه کار با LangGraph و Agentic AI محل شرکت: غرب تهران"
    )
    assert any(
        i.category == "work_duty" and "سرویس‌های Python" in i.anchor.exact_text for i in view.items
    )
    assert any(
        i.category == "candidate_qualification" and "تسلط به Python" in i.anchor.exact_text
        for i in view.items
    )
    assert any(
        i.category == "candidate_qualification"
        and i.employer_strength == "preferred"
        and "LangGraph" in i.anchor.exact_text
        for i in view.items
    )
    assert not any(
        i.employer_strength == "required" and "LangGraph" in i.anchor.exact_text for i in view.items
    )
    assert any(
        i.category == "work_arrangement" and "غرب تهران" in i.anchor.exact_text for i in view.items
    )


def test_phrases_about_analyzing_requirements_do_not_start_a_new_qualification_section():
    text = (
        "شرح وظایف: تحلیل نیازمندی‌ها و مشارکت در طراحی فنی و معماری نرم‌افزار. "
        "توسعه و نگهداری سرویس‌های Python. "
        "شرایط و مهارت‌های ضروری: تسلط بر Python."
    )
    view = candidate(text)
    assert any(
        i.category == "work_duty" and "تحلیل نیازمندی‌ها" in i.anchor.exact_text for i in view.items
    )
    assert any(
        i.category == "work_duty" and "توسعه و نگهداری" in i.anchor.exact_text for i in view.items
    )
    assert any(
        i.category == "candidate_qualification" and "تسلط بر Python" in i.anchor.exact_text
        for i in view.items
    )


def test_mixed_requirements_and_explicit_qualification_strength_are_not_mandatory_from_duties():
    view = candidate(
        "مسئولیت‌ها طراحی راهکارهای امنیتی و ارزیابی آسیب‌پذیری. "
        "مهارت‌های ضروری: آشنایی با OWASP. "
        "مهارت‌های امتیازی: تجربه کار با Docker. "
        "مهارت‌های فردی مسئولیت‌پذیری و روحیه همکاری."
    )
    assert any(i.category == "work_duty" for i in view.items)
    assert any(
        i.category == "candidate_qualification" and "OWASP" in i.anchor.exact_text
        for i in view.items
    )
    assert any(
        i.employer_strength == "preferred" and "Docker" in i.anchor.exact_text for i in view.items
    )
    assert any(
        i.category == "behavioral_expectation" and "مسئولیت‌پذیری" in i.anchor.exact_text
        for i in view.items
    )


def test_english_flattened_core_responsibilities_and_required_preferred_plus():
    view = candidate(
        "About the Role We build useful AI services. "
        "Core Responsibilities Build and maintain multi-agent systems "
        "Write and iterate prompts based on failures "
        "Monitor deployed agent behavior. "
        "Required Qualifications Strong Python with production async experience "
        "Hands-on experience with LangGraph or equivalent "
        "Preferred Familiarity with observability tools "
        "Coursework, side projects, or professional experience in NLP "
        "Requirements Familiarity with mobile languages is a plus. "
        "Nice to Have Open-source contributions."
    )
    assert any(
        i.category == "work_duty" and "multi-agent" in i.anchor.exact_text for i in view.items
    )
    assert any(
        i.category == "work_duty" and "iterate prompts" in i.anchor.exact_text for i in view.items
    )
    assert any(
        i.category == "candidate_qualification" and "Strong Python" in i.anchor.exact_text
        for i in view.items
    )
    assert any(
        i.category == "candidate_qualification"
        and i.employer_strength == "preferred"
        and "observability" in i.anchor.exact_text
        for i in view.items
    )
    assert any(
        i.category == "candidate_qualification"
        and i.employer_strength == "preferred"
        and "mobile languages" in i.anchor.exact_text
        for i in view.items
    )
    assert any(x.kind == "explicit_unresolved_option_scope" for x in view.alternatives)
    logic = build_candidate_eligibility_logic_v3(
        make_source(
            "Core Responsibilities Build APIs Required Qualifications "
            "Hands-on experience with LangGraph or equivalent"
        ),
        candidate(
            "Core Responsibilities Build APIs Required Qualifications "
            "Hands-on experience with LangGraph or equivalent"
        ),
    )
    assert logic.graphs == ()
    assert "explicit_unresolved_option_scope" in logic.unresolved_group_kinds


def test_english_leadership_and_audit_sections_are_tasks_not_candidate_qualifications():
    view = candidate(
        "Leadership & Governance Lead the audit team and coordinate work. "
        "Vulnerability Assessment & Penetration Testing "
        "Plan and oversee penetration tests. "
        "Security Control Audits Assess internal control effectiveness. "
        "Reporting, Remediation & Follow-up Track all findings to closure. "
        "Stakeholder Collaboration Coordinate with development teams. "
        "Requirements Proven experience in security assessment, "
        "penetration testing, vulnerability management, and/or auditing. "
        "Familiarity with mobile technologies is a plus."
    )
    assert sum(i.category == "work_duty" for i in view.items) >= 4
    assert any(
        i.category == "candidate_qualification" and "Proven experience" in i.anchor.exact_text
        for i in view.items
    )
    assert any(
        i.category == "candidate_qualification"
        and i.employer_strength == "preferred"
        and "is a plus" in i.anchor.exact_text
        for i in view.items
    )
    assert any(a.kind == "explicit_unresolved_option_scope" for a in view.alternatives)


def test_persian_specialty_and_one_framework_alternatives_are_unreviewed_not_eligibility_graphs():
    text = (
        "مسئولیت‌ها ساخت راهکارهای مختلف. "
        "شرایط و مهارت‌های ضروری تجربه کار با حداقل یکی از فریم‌ورک‌های پایتونی "
        "دانش عمیق در یک یا چند حوزه تخصصی."
    )
    view = candidate(text)
    groups = [x for x in view.alternatives if x.kind == "explicit_unresolved_option_scope"]
    assert groups
    assert all(x.logical_operator == "any_of_unresolved_option_boundaries" for x in groups)
    assert all(
        x.interpretation_status == "candidate_unreviewed_not_eligibility_authority" for x in groups
    )
    logic = build_candidate_eligibility_logic_v3(make_source(text), view)
    assert logic.graphs == ()
    assert "explicit_unresolved_option_scope" in logic.unresolved_group_kinds


@pytest.mark.parametrize(
    "text",
    [
        "شرح وظایف: هماهنگی و بررسی نتیجه. مهارت‌های ضروری: Python.",
        "تجربه تحلیل تهدید و تأیید کار با تیم‌ها.",
        "Requirements and risks are reviewed by the team.",
        "مسئولیت‌ها مدیریت پروژه و تحویل به تیم توسعه.",
    ],
)
def test_unrelated_connectors_do_not_create_fabricated_or_eligibility(text):
    view = candidate(text)
    assert not any(x.kind == "explicit_unresolved_option_scope" for x in view.alternatives)


def test_scope_and_negative_source_qualifier_stay_uncertain_until_review():
    view = candidate(
        "شرایط و مهارت‌های ضروری: Python. "
        "مهارت‌های ترجیحی: Docker. "
        "نکات مهم: همکاری صرفاً به صورت تمام وقت است و امکان دورکاری و پروژه‌ای وجود ندارد."
    )
    assert not any(
        i.employer_strength == "required" and "Docker" in i.anchor.exact_text for i in view.items
    )
    assert any(
        i.category == "work_arrangement" and "دورکاری" in i.anchor.exact_text for i in view.items
    )


@pytest.mark.parametrize("job", ["tNhZ", "tMps", "tNDx", "tMjm"])
def test_historical_B0_development_cases_preserve_duty_and_graph_contract(job):
    p = B0 / "exposed_original_snapshot.sqlite3"
    if not p.exists():
        pytest.skip("Private original B0 source snapshot intentionally unavailable in CI")
    src = TranslationStore(p).latest_source_version(job)
    prior = interpret_original_source_candidate_v2(src)
    new = interpret_original_source_candidate_v3(src)
    prev_logic = build_candidate_eligibility_logic(src, prior)
    next_logic = build_candidate_eligibility_logic_v3(src, new)
    assert sum(x.category == "work_duty" for x in prior.items) == sum(
        x.category == "work_duty" for x in new.items
    )
    assert {g.graph_id for g in prev_logic.graphs} == {g.graph_id for g in next_logic.graphs}


@pytest.mark.parametrize(
    ("p", "select", "review", "snapshot", "expected_matches", "expected_missed"),
    [
        (
            OLD,
            "B5_SELECTION_FROZEN.json",
            "B5_SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json",
            "B5_8_SOURCE_SNAPSHOT.sqlite3",
            82,
            0,
        ),
        (
            NEW,
            "FROZEN_METADATA_SELECTION.json",
            "SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json",
            "isolated-second-cohort.sqlite3",
            79,
            0,
        ),
    ],
)
def test_two_exposed_eight_case_original_source_regressions(
    p, select, review, snapshot, expected_matches, expected_missed
):
    if not (p / snapshot).exists():
        pytest.skip("Original employer data and source-first reviews are private")
    selected = __import__("json").loads((p / select).read_text())
    rows = selected.get("selected_primary", selected.get("primary"))
    sealed = __import__("json").loads((p / review).read_text())
    store = TranslationStore(p / snapshot)
    versions = {
        item["source_job_id"]: store.latest_source_version(item["source_job_id"]) for item in rows
    }
    evaluate = runpy.run_path(str(ROOT / "scripts/evaluate_p16_b5_source_gate.py"))[
        "evaluate_source_gate"
    ]
    result = evaluate(
        frozen={"selected_primary": rows},
        review=sealed,
        source_versions=versions,
        engine=interpret_original_source_candidate_v3,
    )
    assert result["counts"]["candidate_role_match_anchor_count"] == expected_matches
    assert result["counts"]["explicit_duty_missed_anchor_count"] == expected_missed
    assert result["counts"]["optional_or_negative_required_overstatement_count"] == 0
    assert result["counts"]["multi_specialty_alternative_structure_missing_jobs"] == 0


def test_new_parser_remains_compatible_with_B1_candidate_anchor_contract():
    src = make_source(
        "مسئولیت‌ها طراحی API و کار با تیم فنی. مهارت‌های ضروری: Python. مهارت‌های امتیازی: Docker."
    )
    view = interpret_original_source_candidate_v3(src)
    bundle = runpy.run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))[
        "b1_design_from_b2"
    ](view, src)
    validate = runpy.run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))["validate_bundle"]
    validate(bundle, source=src)
    assert bundle["authority"] == "candidate_only_no_downstream_reuse"
    assert bundle["brief"]["downstream_authority"] == "none"
