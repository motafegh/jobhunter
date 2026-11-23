"""Versioned B2v7 heading-scoped candidate, source-first and non-authoritative."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

import pytest

from jobhunter.jobinja_details import _strip_html
from jobhunter.source_item_candidate_b2 import verify_b2_candidate
from jobhunter.source_item_candidate_b2_v7_dom import (
    B2V7_DOM_CONTRACT,
    interpret_original_source_candidate_v7,
)
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "data/local-acceptance/2026-11-23-fresh-e2e-manual-audit"


def _candidate(html: str):
    raw = (
        '<html><head><script type="application/ld+json">'
        + json.dumps({"@type": "JobPosting", "description": html}, ensure_ascii=False)
        + "</script></head></html>"
    ).encode()
    source = TranslationSourceVersion(
        source_job_id="synthetic-v7",
        job_detail_version_id=22,
        semantic_sha256="7" * 64,
        source_language="mixed",
        fields={"description": _strip_html(html)},
    )
    result = interpret_original_source_candidate_v7(
        source,
        raw_job_page=raw,
        expected_html_sha256=hashlib.sha256(raw).hexdigest(),
    )
    verify_b2_candidate(result, source)
    for item in result.items:
        a = item.anchor
        assert source.fields["description"][a.char_start : a.char_end] == a.exact_text
        assert (
            source.fields["description"].encode()[a.utf8_start : a.utf8_end]
            == a.exact_text.encode()
        )
    return result


def test_standalone_work_and_benefit_headings_do_not_contaminate_each_other():
    c = _candidate(
        "<p><strong>What You'll Work On</strong></p>"
        "<ul><li>Build scalable services</li><li>Review infrastructure</li></ul>"
        "<p><strong>Key Responsibilities</strong></p>"
        "<ul><li>Monitor API reliability</li></ul>"
        "<p><strong>Why Grow With Us?</strong></p>"
        "<ul><li>Mentorship and growth</li>"
        "<li><strong>Technical Ownership: Learn from experienced engineers</strong></li></ul>"
        "<p><strong>Benefits</strong></p>"
        "<ul><li>Flexible Work Model: Hybrid with remote options</li></ul>"
    )
    assert len([x for x in c.items if x.category == "work_duty"]) == 3
    assert any(x.category == "benefit" and "Mentorship" in x.anchor.exact_text for x in c.items)
    assert any(
        x.category == "benefit" and "Technical Ownership" in x.anchor.exact_text for x in c.items
    )
    assert any(
        x.category == "work_arrangement" and "Hybrid" in x.anchor.exact_text for x in c.items
    )


def test_must_have_is_scope_not_a_spurious_required_qualifier():
    c = _candidate(
        "<p><strong>Requirements</strong></p>"
        "<p><strong>Must Have</strong></p>"
        "<ul><li>Familiarity with Python</li><li>Degree in Computer Engineering</li></ul>"
        "<p><strong>Nice to Have</strong></p>"
        "<ul><li>Experience with VoIP</li></ul>"
    )
    assert not any(i.anchor.exact_text == "Must Have" for i in c.items)
    req = [x for x in c.items if x.employer_strength == "required"]
    assert len(req) == 2
    assert all(i.category == "candidate_qualification" for i in req)
    preferred = [x for x in c.items if x.employer_strength == "preferred"]
    assert len(preferred) == 1
    assert preferred[0].anchor.exact_text == "Experience with VoIP"


def test_negative_and_optional_item_never_turn_mandatory_from_section():
    c = _candidate(
        "<p><strong>Must Have</strong></p>"
        "<ul><li>Python skill</li><li>Degree is not required</li>"
        "<li>Optional tool knowledge</li></ul>"
    )
    assert len([i for i in c.items if i.employer_strength == "required"]) == 1
    assert all(
        i.employer_strength != "required"
        for i in c.items
        if "not required" in i.anchor.exact_text or "Optional" in i.anchor.exact_text
    )


def test_heading_words_inside_list_items_do_not_poison_following_conditions():
    c = _candidate(
        "<p><strong>Benefits</strong></p>"
        "<ul><li><strong>Responsibilities: Learn in a mentorship program</strong></li>"
        "<li>Flexible working hours</li></ul>"
    )
    # The existing B2v6 label for the first bullet is preserved to avoid
    # cross-cohort regressions. The next benefit/condition must not inherit
    # an invented required-duty section from that emphasized list bullet.
    assert any(
        "Flexible working hours" in i.anchor.exact_text and i.category == "work_arrangement"
        for i in c.items
    )


def test_generic_skill_section_is_not_equal_to_required_professional_experience():
    c = _candidate(
        "<p><strong>Technical Skills</strong></p>"
        "<ul><li>Familiarity with ISO 27001</li><li>Ability to design dashboards</li></ul>"
    )
    assert all(i.employer_strength != "required" for i in c.items)
    assert all(i.category == "candidate_qualification" for i in c.items)


def test_live_source_evidence_replay_after_exposure():
    if not (PRIVATE / "data/current-cohort.sqlite3").is_file():
        pytest.skip("Private Nov 23 original-source cohort unavailable in CI")
    db = PRIVATE / "data/current-cohort.sqlite3"
    expected = {"tdIF": (15, 0), "td0u": (6, 5), "td0r": (6, 0)}
    with sqlite3.connect(db) as conn:
        store = TranslationStore(db)
        for jid, (duties, must_have) in expected.items():
            src = store.latest_source_version(jid)
            rec = conn.execute(
                "select evidence_path,content_sha256 from job_detail_versions where id=?",
                (src.job_detail_version_id,),
            ).fetchone()
            out = interpret_original_source_candidate_v7(
                src,
                raw_job_page=Path(rec[0]).read_bytes(),
                expected_html_sha256=rec[1],
            )
            verify_b2_candidate(out, src)
            assert sum(i.category == "work_duty" for i in out.items) == duties
            if must_have:
                assert (
                    sum(
                        i.employer_strength == "required"
                        and i.category == "candidate_qualification"
                        for i in out.items
                    )
                    == must_have
                )
                assert all(i.anchor.exact_text != "Must Have" for i in out.items)
            if jid == "td0r":
                assert any(
                    "ساعت کاری منعطف" in i.anchor.exact_text and i.category == "work_arrangement"
                    for i in out.items
                )
    assert B2V7_DOM_CONTRACT.endswith("-v7")
