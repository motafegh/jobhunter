"""Calibrated source-evaluation behavior: syntax, scope and obligations independent."""

from __future__ import annotations

import hashlib
import json
import runpy
from dataclasses import replace
from pathlib import Path

import pytest

from jobhunter.jobinja_details import _strip_html
from jobhunter.source_gate_evaluation_v2 import (
    assess_source_anchor,
    evaluate_calibrated_gate,
)
from jobhunter.source_item_candidate_b2_v4_dom import interpret_original_source_candidate_v4
from jobhunter.source_item_candidate_b2_v6_dom import (
    B2V6_DOM_CONTRACT,
    interpret_original_source_candidate_v6,
)
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ROOT = Path(__file__).resolve().parents[1]


def source_and_candidate(markup: str, *, version: str = "v6"):
    raw = (
        '<html><head><script type="application/ld+json">'
        + json.dumps({"@type": "JobPosting", "description": markup}, ensure_ascii=False)
        + "</script></head></html>"
    ).encode()
    source = TranslationSourceVersion(
        source_job_id="test-v6",
        job_detail_version_id=15,
        semantic_sha256="a" * 64,
        source_language="mixed",
        fields={"description": _strip_html(markup)},
    )
    engine = (
        interpret_original_source_candidate_v6
        if version == "v6"
        else interpret_original_source_candidate_v4
    )
    result = engine(source, raw_job_page=raw)
    return source, result


def anchor(original: str, phrase: str, *, kind: str, modality: str = "explicit_work"):
    start = original.index(phrase)
    return {
        "anchor_id": "synthetic",
        "original_description_start": start,
        "original_description_end": start + len(phrase),
        "original_quote": phrase,
        "quote_sha256": hashlib.sha256(phrase.encode()).hexdigest(),
        "kind": kind,
        "modality_source_first": modality,
    }


def test_adjacent_distinct_work_bullets_are_covered_without_merged_parser_item():
    s, c = source_and_candidate(
        "<div>Key Responsibilities</div>"
        "<ul><li>Build secure APIs.</li><li>Audit deployment configuration.</li></ul>",
        version="v4",
    )
    phrase = "Build secure APIs. Audit deployment configuration."
    result = assess_source_anchor(
        anchor(s.fields["description"], phrase, kind="duty"), c, s.fields["description"]
    )
    assert result["coverage"] == "covered_across_items"
    assert result["covered_item_count"] == 2
    assert result["role_state"] == "exact_role"
    assert result["explicit_duty_missing"] is False


def test_real_missing_nonwhitespace_text_cannot_be_hidden_by_multi_item_tiling():
    s, c = source_and_candidate(
        "<div>Key Responsibilities</div><ul><li>Build APIs.</li><li>Audit services.</li></ul>",
        version="v4",
    )
    assert len(c.items) >= 2
    missing = replace(c, items=c.items[:-1])
    phrase = "Build APIs. Audit services."
    verdict = assess_source_anchor(
        anchor(s.fields["description"], phrase, kind="duty"), missing, s.fields["description"]
    )
    assert verdict["coverage"] == "gap_in_original_source"
    assert verdict["explicit_duty_missing"] is True


def test_example_list_without_employer_eligibility_or_does_not_trigger_hard_stop():
    s, c = source_and_candidate(
        "<div>Technical Skills</div>"
        "<ul><li>Familiarity with Agile methodologies (Scrum, Kanban).</li></ul>",
        version="v4",
    )
    a = anchor(
        s.fields["description"],
        "Scrum, Kanban",
        kind="alternative",
        modality="familiarity_examples",
    )
    result = assess_source_anchor(a, c, s.fields["description"])
    assert result["alternative_status"] == "examples_not_mandatory_eligibility"
    assert result["hard_alternative_missing"] is False
    assert not c.alternatives


def test_explicit_eligibility_requires_a_source_local_option_not_other_vacancy_section():
    s, c = source_and_candidate(
        "<div>Requirements</div>"
        "<p>Equivalent certification pathway is accepted.</p>"
        "<p>Knowledge of Python or Go is useful.</p>",
        version="v4",
    )
    a = anchor(
        s.fields["description"],
        "Equivalent certification pathway is accepted.",
        kind="alternative",
        modality="explicit_eligibility_or",
    )
    result = assess_source_anchor(a, c, s.fields["description"])
    assert result["alternative_type"] == "explicit_eligibility_disjunction_reviewed"
    assert result["alternative_status"] == "missing_source_scope"
    assert result["hard_alternative_missing"] is True


def test_unknown_option_modality_stays_unresolved_not_certified_or_absent():
    s, c = source_and_candidate(
        "<div>Technical Skills</div><p>Familiarity with CI tools.</p>", version="v4"
    )
    result = assess_source_anchor(
        anchor(s.fields["description"], "CI tools", kind="alternative", modality="not_reviewed"),
        c,
        s.fields["description"],
    )
    assert result["alternative_status"] == "unresolved_not_auto_failed"


def test_behavioral_as_broad_nonmandatory_qualification_is_not_critical_mismatch():
    s, c = source_and_candidate(
        "<div>Technical Skills</div><p>Ability to work with others.</p>", version="v4"
    )
    result = assess_source_anchor(
        anchor(
            s.fields["description"],
            "Ability to work with others.",
            kind="behavior",
            modality="stated_trait",
        ),
        c,
        s.fields["description"],
    )
    # Depending on previous section-role rules, this must never fabricate a
    # mandatory previous-employment condition.
    assert result["optional_or_negative_to_required"] is False
    if result["candidate_roles"] == ("candidate_qualification",):
        assert result["role_state"] == "compatible_broad_qualification"
        assert result["critical_category_mismatch"] is False


def test_negative_requiredness_is_hard_failure_even_if_category_matches():
    s, c = source_and_candidate(
        "<div>Technical Skills</div><p>Minimum 5 years required.</p><p>Knowledge of Python.</p>",
        version="v4",
    )
    # This deliberately simulates conflicting reviewer evidence, to verify
    # that category matching does not defeat explicit optionality safeguards.
    # Force an unsupported mandatory classification on the *reviewed item*.
    # A required strength on some other item cannot trigger this assertion.
    selected = next(i for i in c.items if "Knowledge of Python." in i.anchor.exact_text)
    forced = replace(
        c,
        items=tuple(
            replace(i, employer_strength="required") if i is selected else i for i in c.items
        ),
    )
    result = assess_source_anchor(
        anchor(
            s.fields["description"],
            "Knowledge of Python.",
            kind="qualification",
            modality="explicit_preferred",
        ),
        forced,
        s.fields["description"],
    )
    assert result["optional_or_negative_to_required"] is True


def test_frozen_quote_and_coordinates_are_required():
    s, c = source_and_candidate(
        "<div>Key Responsibilities</div><p>Build secure APIs.</p>", version="v4"
    )
    a = anchor(s.fields["description"], "Build secure APIs.", kind="duty")
    a["original_description_start"] += 1
    with pytest.raises(ValueError, match="coordinates/SHA drift"):
        assess_source_anchor(a, c, s.fields["description"])


def test_b2v6_version_isolated_and_trait_recovered_without_mandatory_experience():
    assert B2V6_DOM_CONTRACT.endswith("-v6")
    s, c = source_and_candidate(
        "<div>مهارت‌های مورد نیاز</div>"
        "<p>تجربه کار با Docker</p>"
        "<p>· مسئولیت‌پذیری و روحیه کار تیمی</p>"
    )
    traits = [i for i in c.items if "روحیه کار تیمی" in i.anchor.exact_text]
    assert len(traits) == 1
    assert traits[0].category == "behavioral_expectation"
    assert traits[0].employer_strength == "stated_expectation"


def test_b2v6_false_heading_item_recovers_as_uncertain_source_evidence():
    _, c = source_and_candidate(
        "<div>Benefits</div>"
        "<ul><li>Competitive compensation.</li>"
        "<li><strong>Performance-based bonuses.</strong></li></ul>"
    )
    bonuses = [i for i in c.items if "Performance-based bonuses" in i.anchor.exact_text]
    assert len(bonuses) == 1
    assert bonuses[0].category != "candidate_qualification"
    assert bonuses[0].employer_strength != "required"


def test_b2v6_source_byte_drift_rejected():
    raw = (
        b'<html><head><script type="application/ld+json">'
        b'{"@type":"JobPosting","description":"<p>Hello.</p>"}'
        b"</script></head></html>"
    )
    s = TranslationSourceVersion(
        source_job_id="hash-check",
        job_detail_version_id=1,
        semantic_sha256="a" * 64,
        source_language="en",
        fields={"description": "Hello."},
    )
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        interpret_original_source_candidate_v6(
            s, raw_job_page=raw + b" ", expected_html_sha256=hashlib.sha256(raw).hexdigest()
        )


def test_sealed_calibrated_fourth_scorecard_is_source_safe_and_nonpromotion():
    p = ROOT / (
        "docs/working-memory/2026-11-22_p16_b5_calibrated/SAFE_EXPOSED_SOURCE_GATE_CALIBRATION.json"
    )
    record = json.loads(p.read_text(encoding="utf-8"))
    assert record["contract"] == "jobhunter-p16-b5-exposed-calibrated-gate-v2"
    assert record["status"] == "PASS_EXPOSED_METHOD_REPAIR_NO_B5_ACCEPTANCE"
    assert record["original_B2v4_source_gate_failed"] is True
    assert record["source_jobs"] == 8
    assert record["selected_original_source_assertions"] == 80
    assert record["b1_candidate_contract_validations"] == 8
    assert record["review_independent_human"] is False
    assert record["new_model_requests"] == record["new_source_requests"] == 0
    assert record["new_accepted_employer_facts"] == 0
    assert record["B5_accepted"] is False
    assert record["B6_promotion_authorized"] is False
    assert record["independent_generalization_established"] is False
    candidates = record["candidates"]
    old = candidates["B2v4_frozen_prospective"]["counts"]
    v5 = candidates["B2v5_exposed"]["counts"]
    v6 = candidates["B2v6_exposed"]["counts"]
    assert (old["exact_role"], old["critical_category_mismatches"]) == (57, 12)
    assert v5["exact_role"] == 72
    assert v6["exact_role"] == v6["role_comparable_assertions"] == 73
    assert v6["explicit_duty_missed"] == 0
    assert v6["cross_item_covered"] == 1
    assert v6["explicit_eligibility_scope_missing"] == 0
    assert v6["illustrative_alternatives"] == 4
    assert v6["false_mandatory"] == 0
    assert v6["uncovered"] == 0
    for path, expected_hash in record["code_sha256"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected_hash
    # The production SQLite database is private and intentionally absent
    # from a clean CI checkout. Verify its SHA when local evidence exists;
    # otherwise preserve the recorded receipt without inventing local bytes.
    production_db = ROOT / "data/jobhunter.sqlite3"
    assert len(record["production_database_sha256"]) == 64
    if production_db.is_file():
        assert (
            hashlib.sha256(production_db.read_bytes()).hexdigest()
            == record["production_database_sha256"]
        )
    manifest = ROOT / "corpus/manifest.json"
    if manifest.is_file():
        assert (
            hashlib.sha256(manifest.read_bytes()).hexdigest()
            == record["public_corpus_manifest_sha256"]
        )
    else:
        assert len(record["public_corpus_manifest_sha256"]) == 64
    safe = p.read_text(encoding="utf-8")
    assert not any("\u0600" <= char <= "\u06ff" for char in safe)
    assert "original_quote" not in safe
    assert "private_raw_html_path" not in safe
    assert "https://jobinja" not in safe


def test_private_original_and_calibrated_receipts_replay_without_promotion():
    f = ROOT / (
        "data/local-acceptance/p16-b5-calibrated-2026-11-22/PRIVATE_EXPOSED_CALIBRATED_DETAILS.json"
    )
    if not f.exists():
        pytest.skip("Private source evidence unavailable on a fresh checkout")
    old_verify = runpy.run_path(str(ROOT / "scripts/verify_p16_b5_fourth_source_gate.py"))[
        "verify"
    ]()
    assert old_verify["explicit_duties_missed"] == 1
    assert old_verify["unrepresented_alternatives_jobs"] == 1
    new_verify = runpy.run_path(str(ROOT / "scripts/verify_p16_b5_fourth_calibrated_gate.py"))[
        "verify"
    ]()
    assert new_verify["status"] == "PASS_EXPOSED_METHOD_REPAIR_NO_B5_ACCEPTANCE"
    assert new_verify["B5_accepted"] is False
    assert new_verify["B6_authorized"] is False


@pytest.mark.parametrize(
    ("name", "expected_exact", "expected_critical", "expected_unknown_alts"),
    [
        ("first", 83, 1, 3),
        ("second", 84, 0, 4),
        ("third", 78, 0, 4),
        ("fourth", 73, 0, 0),
    ],
)
def test_all_four_exposed_cohorts_v6_calibrated_and_b1_contract(
    name, expected_exact, expected_critical, expected_unknown_alts
):
    cohorts = runpy.run_path(str(ROOT / "tests/test_source_item_candidate_b2_v5_dom.py"))[
        "FROZEN_COHORTS"
    ]
    cohort = next(x for x in cohorts if x[0] == name)
    _, rel, sel, review_file, man, snapshot, *_ = cohort
    p = ROOT / "data/local-acceptance" / rel
    if not (p / snapshot).exists():
        pytest.skip("Private frozen cohort unavailable in CI")
    selection = json.loads((p / sel).read_text(encoding="utf-8"))
    selected = selection.get("selected_primary", selection.get("primary"))
    review = json.loads((p / review_file).read_text(encoding="utf-8"))
    manifest = json.loads((p / man).read_text(encoding="utf-8"))
    raw = {item["source_job_id"]: item for item in manifest["entries"]}
    store = TranslationStore(p / snapshot)
    versions = {
        item["source_job_id"]: store.latest_source_version(item["source_job_id"])
        for item in selected
    }
    if name == "fourth":
        supplement = json.loads(
            (p / "SOURCE_FIRST_EXPLICIT_OR_SUPPLEMENT_SEALED.json").read_text(encoding="utf-8")
        )
        for extra in supplement["alternative_anchors"]:
            record = next(
                x for x in review["entries"] if x["source_job_id"] == extra["source_job_id"]
            )
            record["reviewed_original_anchors"].append(
                {k: v for k, v in extra.items() if k != "source_job_id"}
            )

    def engine(source):
        entry = raw[source.source_job_id]
        return interpret_original_source_candidate_v6(
            source,
            raw_job_page=Path(
                entry.get("private_raw_html_path", entry.get("raw_evidence_path"))
            ).read_bytes(),
            expected_html_sha256=entry.get("raw_html_sha256", entry.get("source_html_sha256")),
        )

    result = evaluate_calibrated_gate(
        frozen={"selected_primary": selected},
        review=review,
        source_versions=versions,
        engine=engine,
    )
    c = result["counts"]
    assert c["exact_role"] == expected_exact
    assert c["critical_category_mismatches"] == expected_critical
    assert c["unresolved_alternatives"] == expected_unknown_alts
    assert c["explicit_duty_missed"] == 0
    assert c["false_mandatory"] == 0
    assert c["explicit_eligibility_scope_missing"] == 0
    assert result["B5_pass"] is False
    b1_design = runpy.run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))[
        "b1_design_from_b2"
    ]
    validate = runpy.run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))["validate_bundle"]
    for source in versions.values():
        validate(b1_design(engine(source), source), source=source)


def test_safe_scorecard_on_clean_checkout_without_private_production_db(monkeypatch):
    """Exercise the actual clean-CI path without changing the local database."""
    real_is_file = Path.is_file
    private_db = ROOT / "data/jobhunter.sqlite3"

    def is_file_without_private_db(path):
        if path == private_db:
            return False
        return real_is_file(path)

    monkeypatch.setattr(Path, "is_file", is_file_without_private_db)
    test_sealed_calibrated_fourth_scorecard_is_source_safe_and_nonpromotion()
