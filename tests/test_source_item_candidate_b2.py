"""Stage B2 bounded original-source candidate, not a semantic promotion."""

from __future__ import annotations

import hashlib
import shutil
from dataclasses import replace
from pathlib import Path
from runpy import run_path

import pytest

from jobhunter.source_item_candidate_b2 import (
    B2_SOURCE_CANDIDATE_CONTRACT,
    interpret_original_source_candidate,
    verify_b2_candidate,
)
from jobhunter.source_span_identity import bind_original_source_span
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ROOT = Path(__file__).resolve().parents[1]
B0 = ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"


def _source(text: str, **fields: object) -> TranslationSourceVersion:
    return TranslationSourceVersion(
        source_job_id="syntheticB2",
        job_detail_version_id=400,
        semantic_sha256="a" * 64,
        source_language="mixed",
        fields={"description": text, **fields},
    )


def _units(source: TranslationSourceVersion):
    candidate = interpret_original_source_candidate(source)
    verify_b2_candidate(candidate, source)
    return candidate


def test_frozen_identity_and_no_mandatory_past_employment_from_llm_duty() -> None:
    original = (
        "Responsibilities: Develop LLM applications. "
        "Requirements: Previous LLM work experience preferred, not required. "
        "Benefits: Equipment provided."
    )
    source = _source(original, skills=["LLM", "Python"])
    candidate = _units(source)
    assert candidate.contract_version == B2_SOURCE_CANDIDATE_CONTRACT
    assert candidate.authority == "candidate_only_no_downstream_reuse"
    assert any(x.category == "work_duty" and "LLM" in x.anchor.exact_text for x in candidate.items)
    assert any(
        x.employer_strength == "preferred"
        and x.qualifier == "negative_explicit"
        and "not required" in x.anchor.exact_text
        for x in candidate.items
    )
    assert candidate.work_capability_links
    assert {x.capability for x in candidate.work_capability_links} == {"LLM"}
    assert all(
        x.employer_prior_experience_required is None for x in candidate.work_capability_links
    )
    assert not any(
        x.category == "candidate_qualification" and x.employer_strength == "required"
        for x in candidate.items
    )
    assert any(x.kind == "board_skill_tag_vs_preferred_prose" for x in candidate.signals)
    for item in candidate.items:
        assert original[item.anchor.char_start : item.anchor.char_end] == item.anchor.exact_text
        assert original.encode("utf-8")[
            item.anchor.utf8_start : item.anchor.utf8_end
        ] == item.anchor.exact_text.encode("utf-8")


def test_work_capability_does_not_invent_framework_requirements() -> None:
    source = _source("Responsibilities: Develop and maintain LLM features.")
    c = _units(source)
    assert "LLM" in {x.capability for x in c.work_capability_links}
    assert all(
        x.capability not in {"LangChain", "Kubernetes", "vLLM"} for x in c.work_capability_links
    )
    assert all(x.employer_strength != "required" for x in c.items)


def test_required_and_optional_in_compound_source_remains_unresolved() -> None:
    source = _source("Requirements: Python required, LLM preferred.", skills=["Python", "LLM"])
    c = _units(source)
    assert any(x.category == "candidate_qualification" for x in c.items)
    assert not any(x.employer_strength == "required" for x in c.items)
    assert not any(x.employer_strength == "preferred" for x in c.items)
    assert any(x.employer_strength == "unresolved" for x in c.items)


def test_explicit_work_list_and_skills_are_not_conflated() -> None:
    source = _source(
        "Responsibilities: Design Python APIs. Develop LLM features. "
        "Requirements: Ability to review Python code.",
        skills=["Python", "LLM"],
    )
    c = _units(source)
    assert len([x for x in c.items if x.category == "work_duty"]) == 2
    assert all("Ability" not in x.anchor.exact_text for x in c.items if x.category == "work_duty")
    assert any(x.category == "candidate_qualification" for x in c.items)


def test_unknowns_and_board_source_are_kept_separate() -> None:
    source = _source(
        "Requirements: Kaspersky certificate. Experience with large government clients.",
        skills=["Kaspersky", "شرایط احراز: متن کامل شرایط استخدام ثبت آگهی"],
        minimum_experience="three years",
        employment_type="full time",
    )
    c = _units(source)
    assert not any(x.employer_strength == "required" for x in c.items)
    assert len(c.board_values) == 4
    assert any(x.classification == "possible_page_copy" for x in c.board_values)
    assert any(x.kind == "possible_page_copy_in_board_skills" for x in c.signals)
    assert all(
        x.field_json_sha256 and x.value_json_sha256 and x.selector.startswith("/")
        for x in c.board_values
    )


def test_source_version_and_anchor_tampering_are_rejected() -> None:
    source = _source("Responsibilities: Build Python APIs.")
    c = _units(source)
    for stale in (
        replace(source, semantic_sha256="b" * 64),
        replace(source, job_detail_version_id=401),
        replace(source, fields={"description": "Other text"}),
    ):
        with pytest.raises(ValueError, match="mismatch|Stale|anchor|version|field"):
            verify_b2_candidate(c, stale)
    bad = replace(c, items=(replace(c.items[0], anchor=replace(c.items[0].anchor, char_end=10)),))
    with pytest.raises(ValueError, match="anchor|offset|match"):
        verify_b2_candidate(bad, source)


def test_board_tag_mutation_and_bogus_disqualifier_rejected() -> None:
    source = _source("Requirements: LLM is an advantage.", skills=["LLM"])
    c = _units(source)
    bad = replace(c, board_values=(replace(c.board_values[0], value="Kubernetes"),))
    with pytest.raises(ValueError, match="tampered"):
        verify_b2_candidate(bad, source)
    assert c.work_capability_links == ()


def test_current_public_analyzer_unchanged() -> None:
    import jobhunter.analysis_current as current

    assert "build_v30_analysis_service" in current.__dict__
    assert not hasattr(current, "build_b2_source_candidate_service")


def test_real_exposed_source_diagnostics_on_private_copy(tmp_path: Path) -> None:
    if not B0.exists():
        pytest.skip("Private B0 source is intentionally not available in public CI")
    before = hashlib.sha256(B0.read_bytes()).hexdigest()
    db = tmp_path / "exposed_copy.sqlite3"
    shutil.copy2(B0, db)
    store = TranslationStore(db)
    cases = {}
    for job in ("tNhZ", "tMps", "tNDx", "tMjm"):
        source = store.latest_source_version(job)
        assert source is not None
        cases[job] = _units(source)
    assert hashlib.sha256(B0.read_bytes()).hexdigest() == before
    n = cases["tNhZ"]
    assert len([x for x in n.items if x.category == "work_duty"]) == 6
    assert any(x.employer_strength == "preferred" and "LLM" in x.anchor.exact_text for x in n.items)
    assert any(x.kind == "board_skill_tag_vs_preferred_prose" for x in n.signals)
    assert any(x.kind == "board_employment_mode_may_hide_prose_alternative" for x in n.signals)
    assert any(x.capability == "LLM" for x in n.work_capability_links)
    assert all(x.employer_prior_experience_required is None for x in n.work_capability_links)

    m = cases["tMps"]
    assert len([x for x in m.alternatives if x.kind == "seniority_tracks"]) == 1
    assert (
        len(next(x for x in m.alternatives if x.kind == "seniority_tracks").source_anchor_ids) == 2
    )
    assert any(x.kind == "one_of_technical_domains" for x in m.alternatives)
    assert any(x.kind == "possible_page_copy_in_board_skills" for x in m.signals)
    assert any(
        x.kind == "board_experience_range_may_hide_seniority_alternatives" for x in m.signals
    )

    d = cases["tNDx"]
    assert len([x for x in d.items if x.category == "work_duty"]) == 5
    assert any(
        x.employer_strength == "preferred" and "روحیه" in x.anchor.exact_text for x in d.items
    )
    for word in ("Kaspersky", "دولتی"):
        assert any(
            word in x.anchor.exact_text and x.employer_strength == "unresolved"
            for x in d.items
            if x.category == "candidate_qualification"
        )
    assert any(x.kind == "certificate_or_equivalent_knowledge" for x in d.alternatives)
    assert not any(
        x.category == "work_arrangement" and "ریموت" in x.anchor.exact_text for x in d.items
    )
    assert any(
        x.category == "application_instruction" and "آزمون فنی" in x.anchor.exact_text
        for x in d.items
    )

    q = cases["tMjm"]
    assert not any(x.category == "work_duty" for x in q.items)
    assert any(
        x.category == "candidate_qualification" and "OWASP" in x.anchor.exact_text for x in q.items
    )
    assert any(
        x.category == "work_arrangement" and "دورکاری" in x.anchor.exact_text for x in q.items
    )
    assert any(
        x.category == "behavioral_expectation" and "وظیفه شناس" in x.anchor.exact_text
        for x in q.items
    )
    assert any(
        x.category == "compensation" and x.anchor.exact_text.startswith("30") for x in q.items
    )
    assert all(x.authority == "candidate_only_no_downstream_reuse" for x in cases.values())


def test_anchor_sha_reuse_matches_stage_a() -> None:
    source = _source("Responsibilities: Build Python APIs.")
    c = _units(source)
    for item in c.items:
        a = bind_original_source_span(
            source, char_start=item.anchor.char_start, char_end=item.anchor.char_end
        )
        assert item.anchor.anchor_id == a.anchor_id


def test_no_false_disqualification_when_employer_source_has_no_qualifications() -> None:
    c = _units(_source("Responsibilities: Maintain Python APIs."))
    assert c.work_capability_links
    assert all(x.employer_strength != "required" for x in c.items)


def test_generic_source_benefit_vs_requirement() -> None:
    c = _units(_source("Benefits: Health insurance. Requirements: Python knowledge."))
    assert any(x.category == "benefit" for x in c.items)
    assert any(x.category == "candidate_qualification" for x in c.items)
    assert not any(x.category == "work_duty" for x in c.items)


def test_b1_design_projection_is_candidate_only_and_reference_valid() -> None:
    b1_design_from_b2 = run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))[
        "b1_design_from_b2"
    ]
    validate_bundle = run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))["validate_bundle"]

    source = _source(
        "Responsibilities: Develop LLM applications. "
        "Requirements: LLM experience preferred, not required.",
        skills=["LLM"],
    )
    candidate = _units(source)
    draft = b1_design_from_b2(candidate, source)
    validate_bundle(draft, source=source)
    assert draft["authority"] == "candidate_only_no_downstream_reuse"
    assert draft["review_events"] == []
    assert draft["brief"]["analysis_outcome"] == "not_run"
    assert draft["brief"]["downstream_authority"] == "none"
    assert draft["alignments"] == []
    assert len(draft["conflicts"]) == 1
    assert draft["conflicts"][0]["resolution"] == "unresolved"
    assert all(x["semantic_review"] == "candidate_unreviewed" for x in draft["items"])


def test_b1_design_real_alternative_paths_remain_candidate_only(tmp_path: Path) -> None:
    b1_design_from_b2 = run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))[
        "b1_design_from_b2"
    ]
    validate_bundle = run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))["validate_bundle"]

    if not B0.exists():
        pytest.skip("Private B0 source is intentionally not available in clean CI")
    copied = tmp_path / "frozen.sqlite3"
    shutil.copy2(B0, copied)
    store = TranslationStore(copied)
    for job in ("tNhZ", "tMps", "tNDx", "tMjm"):
        source = store.latest_source_version(job)
        assert source is not None
        candidate = _units(source)
        draft = b1_design_from_b2(candidate, source)
        validate_bundle(draft, source=source)
        assert draft["brief"]["selected_item_ids"] == []
        assert draft["review_events"] == []
        if job == "tMps":
            assert len(draft["eligibility_graphs"]) == 1
            assert draft["eligibility_graphs"][0]["nodes"][0]["operator"] == "any_of"
            assert any(x.kind == "one_of_technical_domains" for x in candidate.alternatives)
        elif job == "tNDx":
            assert len(draft["eligibility_graphs"]) == 1
            assert draft["eligibility_graphs"][0]["graph_id"] == (
                "candidate_certificate_or_knowledge"
            )
            assert any(
                x.kind == "certificate_or_equivalent_knowledge" for x in candidate.alternatives
            )
        elif job == "tNhZ":
            assert any(x["type"] == "board_vs_employer_strength" for x in draft["conflicts"])


def test_diagnostic_is_local_only_and_bounded(tmp_path: Path) -> None:
    diagnose = run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))["diagnose"]

    invalid_database = tmp_path / "does_not_exist.sqlite3"
    with pytest.raises(ValueError, match="ignored local data"):
        diagnose(invalid_database, ("tNhZ",), tmp_path / "public")
    with pytest.raises(ValueError, match="distinct source IDs"):
        diagnose(
            invalid_database,
            tuple(f"job{i}" for i in range(9)),
            ROOT / "data/local-acceptance/b2-test-invalid",
        )


def test_work_tied_to_capability_without_mandatory_professional_history() -> None:
    source = _source("Responsibilities: Design Python APIs and maintain services.")
    result = _units(source)
    assert any(x.capability == "Python" for x in result.work_capability_links)
    assert any(x.capability == "API" for x in result.work_capability_links)
    assert all(x.employer_strength != "required" for x in result.items)
    assert all(x.employer_prior_experience_required is None for x in result.work_capability_links)


def test_explicit_persian_optional_cue_outweighs_requirements_heading() -> None:
    source = _source(
        "نیازمندی‌ها • آشنایی با LLM مزیت محسوب می‌شود، اما الزامی نیست.",
        skills=["LLM"],
    )
    c = _units(source)
    assert any(
        x.category == "candidate_qualification"
        and x.employer_strength == "preferred"
        and x.qualifier == "negative_explicit"
        for x in c.items
    )
    assert not any(x.employer_strength == "required" for x in c.items)


def test_multi_clause_mixed_modality_is_not_forced_into_one_requirement() -> None:
    source = _source("Requirements: Python must have, LLM is preferred.", skills=["Python"])
    c = _units(source)
    assert any(x.employer_strength == "unresolved" for x in c.items)
    assert not any(x.employer_strength == "required" for x in c.items)


def test_source_version_changed_board_field_is_rejected() -> None:
    source = _source("Responsibilities: Build Python APIs.", skills=["Python"])
    c = _units(source)
    updated = replace(
        source, fields={"description": source.fields["description"], "skills": ["LLM"]}
    )
    with pytest.raises(ValueError, match="Stale board field"):
        verify_b2_candidate(c, updated)


def test_negative_only_skill_is_nonmandatory_not_automatically_preferred() -> None:
    result = _units(_source("Requirements: Previous LLM experience not required."))
    assert any(
        x.category == "candidate_qualification"
        and x.employer_strength == "unresolved"
        and x.qualifier == "negative_explicit"
        for x in result.items
    )
    assert not any(x.employer_strength == "required" for x in result.items)
    assert not any(x.employer_strength == "preferred" for x in result.items)
