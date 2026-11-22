"""B2v5 DOM evidence overlay: synthetic non-regressions and optional private replay."""

from __future__ import annotations

import hashlib
import json
import runpy
from pathlib import Path

import pytest

from jobhunter.jobinja_details import _strip_html
from jobhunter.source_item_candidate_b2_v4_dom import (
    interpret_original_source_candidate_v4,
)
from jobhunter.source_item_candidate_b2_v5_dom import (
    B2V5_DOM_CONTRACT,
    interpret_original_source_candidate_v5,
)
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ROOT = Path(__file__).resolve().parents[1]
FROZEN_COHORTS = (
    (
        "first",
        "p16-stage-b5-2026-11-21/acquisition-v1",
        "B5_SELECTION_FROZEN.json",
        "B5_SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json",
        "B5_SOURCE_FROZEN_BEFORE_REVIEW.json",
        "B5_8_SOURCE_SNAPSHOT.sqlite3",
        83,
        0,
    ),
    (
        "second",
        "p16-stage-b5-2026-11-22/second-source-cohort-v1",
        "FROZEN_METADATA_SELECTION.json",
        "SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json",
        "ORIGINAL_SOURCES_FROZEN_BEFORE_REVIEW.json",
        "isolated-second-cohort.sqlite3",
        84,
        0,
    ),
    (
        "third",
        "p16-stage-b5-2026-11-22/third-source-cohort-v1",
        "FROZEN_METADATA_SELECTION.json",
        "SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json",
        "ORIGINAL_SOURCES_FROZEN_BEFORE_REVIEW.json",
        "isolated-third-cohort.sqlite3",
        78,
        0,
    ),
    (
        "fourth",
        "p16-stage-b5-2026-11-22/fourth-source-cohort-v1",
        "FROZEN_METADATA_SELECTION.json",
        "SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json",
        "ORIGINAL_SOURCES_FROZEN_BEFORE_REVIEW.json",
        "isolated-fourth-cohort.sqlite3",
        71,
        1,
    ),
)


def fixture(markup: str):
    html = (
        '<html><head><script type="application/ld+json">'
        + json.dumps({"@type": "JobPosting", "description": markup}, ensure_ascii=False)
        + "</script></head></html>"
    ).encode()
    source = TranslationSourceVersion(
        source_job_id="synthetic-v5",
        job_detail_version_id=33,
        semantic_sha256="8" * 64,
        source_language="mixed",
        fields={"description": _strip_html(markup)},
    )
    return source, html


def candidates(markup: str):
    source, raw = fixture(markup)
    prior = interpret_original_source_candidate_v4(source, raw_job_page=raw)
    new = interpret_original_source_candidate_v5(source, raw_job_page=raw)
    assert new.authority == "candidate_only_no_downstream_reuse"
    assert all(i.interpretation_status == "candidate_unreviewed" for i in new.items)
    for item in new.items:
        a = item.anchor
        assert source.fields["description"][a.char_start : a.char_end] == a.exact_text
        assert source.fields["description"].encode()[a.utf8_start : a.utf8_end] == (
            a.exact_text.encode()
        )
        assert a.semantic_sha256 == source.semantic_sha256
    return prior, new


def test_versioned_dom_evidence_overlay_never_modifies_frozen_dom():
    assert B2V5_DOM_CONTRACT.endswith("overlay-candidate-v5")
    assert interpret_original_source_candidate_v5 is not interpret_original_source_candidate_v4


def test_distinct_requirements_heading_overrides_context_without_losing_duty_items():
    previous, view = candidates(
        "<div>تخصص‌های مورد نیاز:</div>"
        "<p>آشنایی با Network Security</p><p>تسلط بر Python</p>"
        "<div>وظایف اصلی:</div>"
        "<p>ارزیابی امنیتی زیرساخت</p><p>نوشتن گزارش فنی</p>"
    )
    assert any(
        i.category == "candidate_qualification" and "Python" in i.anchor.exact_text
        for i in view.items
    )
    assert any(
        i.category == "work_duty" and "ارزیابی امنیتی" in i.anchor.exact_text for i in view.items
    )
    assert len([i for i in view.items if i.category == "work_duty"]) >= len(
        [i for i in previous.items if i.category == "work_duty"]
    )


def test_english_experience_heading_and_employer_location_are_not_duties():
    _, view = candidates(
        "<p>Employment Type: remote</p><p>Location: Tehran</p>"
        "<div>Key Responsibilities</div>"
        "<p>Build fast APIs.</p><div>Experience</div>"
        "<p>Minimum 5 years of experience with Node.js.</p>"
        "<div>Technical Skills</div><p>Strong JavaScript knowledge.</p>"
    )
    assert any(
        i.category == "work_arrangement" and "remote" in i.anchor.exact_text for i in view.items
    )
    assert any(
        i.category == "candidate_qualification" and "Minimum 5 years" in i.anchor.exact_text
        for i in view.items
    )


def test_false_responsibility_heading_with_personal_trait_does_not_create_duties():
    _, view = candidates(
        "<div>مهارت‌های مورد نیاز</div>"
        "<p>تجربه نرم‌افزار</p>"
        "<p>· مسئولیت‌پذیری و روحیه کار تیمی</p>"
        "<p>· علاقه‌مند به یادگیری و توسعه فردی</p>"
    )
    assert not any(i.category == "work_duty" and "روحیه" in i.anchor.exact_text for i in view.items)


def test_item_example_is_not_a_claim_all_named_tools_mandatory():
    _, view = candidates(
        "<div>مهارت‌های مورد نیاز</div>"
        "<p>تجربه کار با فریم‌ورک‌هایی مانند LangChain یا ابزارهای مشابه</p>"
        "<div>مزیت محسوب می‌شود</div><p>تجربه RAG</p>"
    )
    assert any(
        i.employer_strength != "required" and "LangChain" in i.anchor.exact_text for i in view.items
    )
    assert all(
        a.interpretation_status == "candidate_unreviewed_not_eligibility_authority"
        for a in view.alternatives
    )


def test_source_html_byte_sha_verification_always_applies_before_overlay():
    src, raw = fixture("<div>مهارت‌های مورد نیاز</div><p>تسلط بر Python</p>")
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        interpret_original_source_candidate_v5(
            src,
            raw_job_page=raw + b" ",
            expected_html_sha256=hashlib.sha256(raw).hexdigest(),
        )


@pytest.mark.parametrize("cohort", FROZEN_COHORTS, ids=[x[0] for x in FROZEN_COHORTS])
def test_source_first_exposed_regression_cohorts_remain_candidate_only(cohort):
    _, path, selection, review_file, manifest_file, snapshot, matches, misses = cohort
    p = ROOT / "data/local-acceptance" / path
    if not (p / snapshot).exists():
        pytest.skip("Private original source/evaluator data unavailable in CI")
    sel = json.loads((p / selection).read_text())
    chosen = sel.get("selected_primary", sel.get("primary"))
    review = json.loads((p / review_file).read_text())
    manifest = json.loads((p / manifest_file).read_text())
    raw = {x["source_job_id"]: x for x in manifest["entries"]}
    store = TranslationStore(p / snapshot)
    versions = {a["source_job_id"]: store.latest_source_version(a["source_job_id"]) for a in chosen}
    if cohort[0] == "fourth":
        supplementary = json.loads(
            (p / "SOURCE_FIRST_EXPLICIT_OR_SUPPLEMENT_SEALED.json").read_text()
        )
        for item in supplementary["alternative_anchors"]:
            ref = next(x for x in review["entries"] if x["source_job_id"] == item["source_job_id"])
            ref["reviewed_original_anchors"].append(
                {k: v for k, v in item.items() if k != "source_job_id"}
            )

    def engine(src):
        rec = raw[src.source_job_id]
        path = Path(rec.get("private_raw_html_path", rec.get("raw_evidence_path")))
        return interpret_original_source_candidate_v5(
            src,
            raw_job_page=path.read_bytes(),
            expected_html_sha256=rec.get("raw_html_sha256", rec.get("source_html_sha256")),
        )

    result = runpy.run_path(str(ROOT / "scripts/evaluate_p16_b5_source_gate.py"))[
        "evaluate_source_gate"
    ](
        frozen={"selected_primary": chosen},
        review=review,
        source_versions=versions,
        engine=engine,
    )
    count = result["counts"]
    assert count["candidate_role_match_anchor_count"] == matches
    assert count["explicit_duty_missed_anchor_count"] == misses
    assert count["optional_or_negative_required_overstatement_count"] == 0


def test_synthetic_B1_anchor_contract_preserved_with_overlay():
    src, raw = fixture(
        "<div>تخصص‌های مورد نیاز:</div><p>آشنایی با Python</p>"
        "<div>وظایف اصلی:</div><p>ساخت API امن</p>"
    )
    candidate = interpret_original_source_candidate_v5(src, raw_job_page=raw)
    bundle = runpy.run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))[
        "b1_design_from_b2"
    ](candidate, src)
    validate = runpy.run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))["validate_bundle"]
    validate(bundle, source=src)


@pytest.mark.parametrize(
    ("wording", "expected"),
    [
        ("Minimum 3 years of Python experience is preferred", "preferred"),
        ("Minimum 3 years of Python experience is not required", "unresolved"),
        ("Minimum 3 years of Python experience is optional", "unresolved"),
        ("Minimum 3 years of Python experience required", "required"),
    ],
)
def test_recovered_minimum_never_overrides_explicit_nonmandatory_wording(wording, expected):
    _, view = candidates(
        "<div>Key Responsibilities</div><p>Build secure APIs.</p>"
        "<div>Technical Skills</div><p>" + wording + "</p>"
    )
    matching = [
        item
        for item in view.items
        if "Minimum 3 years" in item.anchor.exact_text
        and item.category == "candidate_qualification"
    ]
    assert matching, "The original statement must remain source-linked"
    assert all(item.employer_strength == expected for item in matching)


def test_public_safe_fourth_failure_scorecard_matches_frozen_candidate_code():
    path = ROOT / (
        "docs/working-memory/2026-11-22_p16_b5_fourth/SAFE_FOURTH_B5_FAILURE_AND_B2V5_EXPOSED.json"
    )
    record = json.loads(path.read_text(encoding="utf-8"))
    for key, file in (
        ("B2v4_frozen_candidate", ROOT / "src/jobhunter/source_item_candidate_b2_v4_dom.py"),
        ("B2v5_exposed_candidate", ROOT / "src/jobhunter/source_item_candidate_b2_v5_dom.py"),
    ):
        assert record["sha256"][key] == hashlib.sha256(file.read_bytes()).hexdigest()
    assert record["fourth_prospective"]["source_gate"] == ("FAILED_STOP_BEFORE_TRANSLATION_OR_V30")
    assert record["fourth_prospective"]["role_matched"] == 56
    assert record["exposed_cohorts"][3]["B2v5_role_matched"] == 71
    assert record["exposed_cohorts"][3]["B2v5_missed_explicit_duties"] == 1
    assert record["exposed_cohorts"][3]["B2v5_missing_alternative_jobs"] == 1
    assert record["b1_candidate_bundle_validations_passed"] == 32
    assert record["B5_pass"] is False
    assert record["B6_promotion_authorized"] is False
    assert record["new_accepted_employer_facts"] == 0
