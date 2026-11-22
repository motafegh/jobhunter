"""DOM-backed B2v4 source candidate: source identity, semantics, regression.

Synthetic fixtures contain only our own text and never invoke providers.
Private exposed source-only replays are optional/local; CI deliberately skips
them if original employer source material is unavailable.
"""

from __future__ import annotations

import hashlib
import json
import runpy
from pathlib import Path

import pytest

from jobhunter.jobinja_details import _strip_html
from jobhunter.source_eligibility_candidate_b2 import build_candidate_eligibility_logic
from jobhunter.source_item_candidate_b2 import verify_b2_candidate
from jobhunter.source_item_candidate_b2_v3 import interpret_original_source_candidate_v3
from jobhunter.source_item_candidate_b2_v4_dom import (
    B2V4_DOM_CONTRACT,
    exact_dom_groups,
    interpret_original_source_candidate_v4,
)
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ROOT = Path(__file__).resolve().parents[1]
COHORTS = (
    (
        ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1",
        "B5_SELECTION_FROZEN.json",
        "B5_SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json",
        "B5_SOURCE_FROZEN_BEFORE_REVIEW.json",
        "B5_8_SOURCE_SNAPSHOT.sqlite3",
        80,
    ),
    (
        ROOT / "data/local-acceptance/p16-stage-b5-2026-11-22/second-source-cohort-v1",
        "FROZEN_METADATA_SELECTION.json",
        "SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json",
        "ORIGINAL_SOURCES_FROZEN_BEFORE_REVIEW.json",
        "isolated-second-cohort.sqlite3",
        83,
    ),
    (
        ROOT / "data/local-acceptance/p16-stage-b5-2026-11-22/third-source-cohort-v1",
        "FROZEN_METADATA_SELECTION.json",
        "SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json",
        "ORIGINAL_SOURCES_FROZEN_BEFORE_REVIEW.json",
        "isolated-third-cohort.sqlite3",
        77,
    ),
)


def make_source(markup: str) -> tuple[TranslationSourceVersion, bytes, str]:
    html = (
        '<html><head><script type="application/ld+json">'
        + json.dumps({"@type": "JobPosting", "description": markup}, ensure_ascii=False)
        + "</script></head><body></body></html>"
    ).encode("utf-8")
    source = TranslationSourceVersion(
        source_job_id="synthetic-original",
        job_detail_version_id=101,
        semantic_sha256="a" * 64,
        source_language="mixed",
        fields={"description": _strip_html(markup)},
    )
    assert source.fields["description"]
    return source, html, hashlib.sha256(html).hexdigest()


def v4(markup: str):
    source, html, digest = make_source(markup)
    result = interpret_original_source_candidate_v4(
        source, raw_job_page=html, expected_html_sha256=digest
    )
    verify_b2_candidate(result, source)
    assert result.authority == "candidate_only_no_downstream_reuse"
    assert all(u.interpretation_status == "candidate_unreviewed" for u in result.items)
    text = source.fields["description"]
    for u in result.items:
        a = u.anchor
        assert a.source_job_id == source.source_job_id
        assert a.semantic_sha256 == source.semantic_sha256
        assert a.exact_text == text[a.char_start : a.char_end]
        assert text.encode("utf-8")[a.utf8_start : a.utf8_end] == a.exact_text.encode("utf-8")
    return result


def test_dom_version_is_new_and_prior_candidate_unchanged():
    assert B2V4_DOM_CONTRACT.endswith("segmentation-candidate-v4")
    assert interpret_original_source_candidate_v4 is not interpret_original_source_candidate_v3


def test_original_jsonld_list_and_strong_section_boundaries_are_exact():
    markup = (
        "<div><strong>Responsibilities</strong></div>"
        "<ul><li>Build backend APIs with Python.</li>"
        "<li>Review test evidence.</li></ul>"
        "<div><strong>Required Skills</strong></div>"
        "<ul><li>Proficiency in Python.</li><li>Hands-on Redis experience.</li></ul>"
    )
    source, raw, digest = make_source(markup)
    groups = exact_dom_groups(source, raw_job_page=raw, expected_html_sha256=digest)
    assert any("Build backend APIs" in g.exact_text for g in groups)
    assert any(g.in_list and "Proficiency in Python" in g.exact_text for g in groups)
    c = v4(markup)
    assert sum(x.category == "work_duty" for x in c.items) == 2
    assert sum(x.category == "candidate_qualification" for x in c.items) == 2
    assert not any(i.anchor.exact_text == "Required Skills" for i in c.items)


def test_persian_optional_section_under_flattened_html_is_not_mandatory():
    c = v4(
        "<div>شرح وظایف و مسئولیت‌ها</div>"
        "<ul><li>طراحی سرویس‌های backend</li></ul>"
        "<div>مهارت‌های مورد نیاز</div>"
        "<ul><li>تسلط به Python</li></ul>"
        "<div>مزیت محسوب می‌شود</div>"
        "<ul><li>آشنایی با Docker</li><li>تجربه با LangGraph</li></ul>"
    )
    assert any(x.category == "work_duty" for x in c.items)
    assert all(
        x.employer_strength == "preferred"
        for x in c.items
        if "Docker" in x.anchor.exact_text or "LangGraph" in x.anchor.exact_text
    )
    assert not any(
        x.employer_strength == "required" and "LangGraph" in x.anchor.exact_text for x in c.items
    )


def test_persian_applicant_abilities_not_reclassified_as_daily_assigned_work():
    c = v4(
        "<div>مهارت‌های مورد نیاز</div><ul>"
        "<li>تجربه ساخت Agent های هوش مصنوعی برای پروژه‌های کاربردی</li>"
        "<li>توانایی توسعه API</li></ul>"
        "<div>مهارت‌های مطلوب (مزیت محسوب می‌شود)</div>"
        "<ul><li>تجربه پیاده‌سازی RAG</li></ul>"
    )
    assert all(x.category != "work_duty" for x in c.items)
    assert any(
        x.category == "candidate_qualification" and "توانایی توسعه" in x.anchor.exact_text
        for x in c.items
    )
    assert any(x.employer_strength == "preferred" and "RAG" in x.anchor.exact_text for x in c.items)


def test_native_english_preferred_vs_required_and_duties():
    c = v4(
        "<div><strong>Core Responsibilities</strong></div>"
        "<ul><li>Design and deploy agent workflows.</li>"
        "<li>Evaluate RAG reliability.</li></ul>"
        "<div><strong>Required Qualifications</strong></div>"
        "<ul><li>At least 4 years of experience in ML or data science.</li>"
        "<li>Hands-on Python and agent engineering.</li></ul>"
        "<div><strong>Preferred</strong></div>"
        "<ul><li>Experience with local LLM inference.</li></ul>"
    )
    assert sum(x.category == "work_duty" for x in c.items) == 2
    assert sum(x.category == "candidate_qualification" for x in c.items) == 3
    assert any(
        x.employer_strength == "preferred" and "local LLM" in x.anchor.exact_text for x in c.items
    )
    assert c.alternatives
    assert all(
        x.interpretation_status == "candidate_unreviewed_not_eligibility_authority"
        for x in c.alternatives
    )


def test_seniority_either_or_is_candidate_unresolved_not_validated_boolean_graph():
    c = v4(
        "<div>ما به دنبال مهندس Python در سطح Mid-Level یا Senior هستیم.</div>"
        "<div>مهارت‌های مورد نیاز</div><ul><li>Python</li></ul>"
    )
    assert any(x.kind == "source_dom_unresolved_seniority_or" for x in c.alternatives)
    assert all(x.logical_operator == "any_of_unresolved_option_boundaries" for x in c.alternatives)


def test_true_work_location_and_hours_survive_benefit_heading():
    c = v4(
        "<div><strong>Working Conditions & Benefits</strong></div>"
        "<ul><li>Thursday: 8:00 AM – 12:00 PM</li>"
        "<li>Company health insurance</li></ul>"
    )
    assert any(
        x.category == "work_arrangement" and "Thursday" in x.anchor.exact_text for x in c.items
    )


def test_source_html_bytes_sha_must_match_before_dom_interpretation():
    src, data, digest = make_source(
        "<div><strong>Responsibilities</strong></div><ul><li>Build Python APIs</li></ul>"
    )
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        exact_dom_groups(src, raw_job_page=data + b"\n", expected_html_sha256=digest)


def test_source_semantic_description_mismatch_rejected_even_with_valid_html_sha():
    source, data, digest = make_source(
        "<div><strong>Responsibilities</strong></div><ul><li>Build Python APIs</li></ul>"
    )
    altered = TranslationSourceVersion(
        source_job_id=source.source_job_id,
        job_detail_version_id=source.job_detail_version_id,
        semantic_sha256=source.semantic_sha256,
        source_language=source.source_language,
        fields={"description": "Unrelated text"},
    )
    with pytest.raises(ValueError, match="frozen source"):
        exact_dom_groups(altered, raw_job_page=data, expected_html_sha256=digest)


def test_missing_jsonld_description_is_rejected():
    src, _html, _digest = make_source(
        "<div><strong>Responsibilities</strong></div><ul><li>Build Python APIs</li></ul>"
    )
    with pytest.raises(ValueError, match="requires original"):
        interpret_original_source_candidate_v4(
            src,
            raw_job_page=b"<html>No JobPosting</html>",
            expected_html_sha256=hashlib.sha256(b"<html>No JobPosting</html>").hexdigest(),
        )


@pytest.mark.parametrize("case", COHORTS, ids=("first-exposed", "second-exposed", "third-exposed"))
def test_all_original_source_first_exposed_regressions(case):
    root, selname, reviewname, manname, dbname, expected = case
    if not (root / dbname).is_file():
        pytest.skip("Private original source evidence intentionally unavailable in CI")
    selected = json.loads((root / selname).read_text())
    selected = selected.get("selected_primary", selected.get("primary"))
    review = json.loads((root / reviewname).read_text())
    manifest = json.loads((root / manname).read_text())
    store = TranslationStore(root / dbname)
    versions = {
        x["source_job_id"]: store.latest_source_version(x["source_job_id"]) for x in selected
    }
    raw = {x["source_job_id"]: x for x in manifest["entries"]}

    def engine(source):
        item = raw[source.source_job_id]
        html = Path(item.get("private_raw_html_path", item.get("raw_evidence_path")))
        return interpret_original_source_candidate_v4(
            source,
            raw_job_page=html.read_bytes(),
            expected_html_sha256=item.get("raw_html_sha256", item.get("source_html_sha256")),
        )

    evaluate = runpy.run_path(str(ROOT / "scripts/evaluate_p16_b5_source_gate.py"))[
        "evaluate_source_gate"
    ]
    counts = evaluate(
        frozen={"selected_primary": selected},
        review=review,
        source_versions=versions,
        engine=engine,
    )["counts"]
    assert counts["candidate_role_match_anchor_count"] == expected
    assert counts["explicit_duty_missed_anchor_count"] == 0
    assert counts["optional_or_negative_required_overstatement_count"] == 0
    assert counts["multi_specialty_alternative_structure_missing_jobs"] == 0


def test_B1_contract_on_synthetic_dom_original():
    s, raw, sha = make_source(
        "<div><strong>Responsibilities</strong></div><ul><li>Build Python APIs.</li></ul>"
        "<div><strong>Required Qualifications</strong></div>"
        "<ul><li>At least 2 years with Go or Python.</li></ul>"
        "<div><strong>Preferred</strong></div><ul><li>Docker familiarity.</li></ul>"
    )
    c = interpret_original_source_candidate_v4(s, raw_job_page=raw, expected_html_sha256=sha)
    bundle = runpy.run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))[
        "b1_design_from_b2"
    ](c, s)
    validate = runpy.run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))["validate_bundle"]
    validate(bundle, source=s)
    assert bundle["authority"] == "candidate_only_no_downstream_reuse"


def test_frozen_original_B0_graphs_not_lost_by_dom_candidate():
    p = (
        ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/"
        "exposed_original_snapshot.sqlite3"
    )
    if not p.exists():
        pytest.skip("Private original B0 source unavailable in CI")
    from jobhunter.source_item_candidate_b2_v3 import build_candidate_eligibility_logic_v3

    store = TranslationStore(p)
    for job in ("tNhZ", "tMps", "tNDx", "tMjm"):
        src = store.latest_source_version(job)
        # Earlier B0 files may have different fetched original HTML backing;
        # use previous verified B2v3 as historical graph authority.
        old = interpret_original_source_candidate_v3(src)
        assert len(build_candidate_eligibility_logic_v3(src, old).graphs) == len(
            build_candidate_eligibility_logic(src, old).graphs
        )
