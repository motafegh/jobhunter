"""B2 advisory claim grounding is evidence-location, NOT semantic approval."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from jobhunter.source_claim_reconciliation_b2 import (
    B2_CLAIM_RECONCILIATION_CONTRACT,
    AdvisoryClaim,
    advisory_claim_sha256,
    reconcile_advisory_claims,
)
from jobhunter.source_item_candidate_b2 import interpret_original_source_candidate
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

B0 = (
    Path(__file__).resolve().parents[1]
    / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
)


def _source(text: str, job_id: str = "synthetic") -> TranslationSourceVersion:
    return TranslationSourceVersion(
        source_job_id=job_id,
        job_detail_version_id=99,
        semantic_sha256="a" * 64,
        source_language="mixed",
        fields={"description": text},
    )


def _link(item, field: str, text: str, index: int = 0) -> AdvisoryClaim:
    return AdvisoryClaim(
        field=field,
        index=index,
        text=text,
        source_anchor_ids=(item.anchor.anchor_id,),
        link_provenance="assistant_exposed_diagnostic",
    )


def _find(candidate, fragment: str):
    return next(item for item in candidate.items if fragment in item.anchor.exact_text)


def test_exact_source_link_is_not_a_semantic_translation_verdict() -> None:
    source = _source(
        "Responsibilities: Develop LLM features. "
        "Requirements: Knowledge of Python required. "
        "Benefits: Equipment provided."
    )
    candidate = interpret_original_source_candidate(source)
    duty = _find(candidate, "Develop LLM")
    requirement = _find(candidate, "Knowledge of Python")
    result = reconcile_advisory_claims(
        source,
        candidate,
        (
            _link(duty, "duties", "Develop LLM features."),
            _link(requirement, "requirements", "Kubernetes mandatory", 0),
            AdvisoryClaim("work_implied_capabilities", 0, "LLM engineering"),
        ),
    )
    assert result.contract_version == B2_CLAIM_RECONCILIATION_CONTRACT
    assert result.authority == "candidate_only_no_downstream_reuse"
    assert [x.grounding_state for x in result.claims] == [
        "linked_semantics_unreviewed",
        "linked_semantics_unreviewed",
        "unlinked_unknown",
    ]
    # Even a deliberately wrong paraphrase can share an exact source anchor.
    assert all(x.semantic_review == "unreviewed_not_established" for x in result.claims)
    assert all(x.authority == "advisory_only_no_employer_fact_promotion" for x in result.claims)
    assert len(result.claims[0].claim_sha256) == 64


def test_misclassified_duty_arrangement_and_strength_are_diagnostic_only() -> None:
    source = _source(
        "Responsibilities: Develop LLM features. "
        "Requirements: Knowledge of Python preferred. "
        "امکان دورکاری."
    )
    c = interpret_original_source_candidate(source)
    preferred = _find(c, "Knowledge of Python")
    arrangement = _find(c, "امکان دورکاری")
    claims = (
        _link(preferred, "requirements", "Python is mandatory"),
        _link(preferred, "preferences", "Python helpful", 0),
        _link(preferred, "duties", "Perform Python audits", 0),
        _link(arrangement, "alternatives", "Remote is an applicant eligibility path", 0),
        _link(arrangement, "arrangements", "Remote work possible", 0),
    )
    result = reconcile_advisory_claims(source, c, claims)
    assert [x.grounding_state for x in result.claims] == [
        "source_candidate_disagreement",
        "linked_semantics_unreviewed",
        "source_candidate_disagreement",
        "source_candidate_disagreement",
        "linked_semantics_unreviewed",
    ]
    assert result.claims[0].diagnostic_signals == (
        "mandatory_strength_not_established_by_source_candidate",
    )
    assert result.claims[2].diagnostic_signals == ("duty_not_established_by_source_candidate",)
    assert result.claims[3].diagnostic_signals == (
        "eligibility_alternative_not_established_by_source_candidate",
    )


def test_unresolved_qualifications_are_not_automatically_preferred() -> None:
    source = _source("Requirements: Kaspersky certificate.")
    c = interpret_original_source_candidate(source)
    item = _find(c, "Kaspersky")
    result = reconcile_advisory_claims(source, c, (_link(item, "preferences", "Preferred"),))
    assert result.claims[0].grounding_state == "source_candidate_disagreement"
    assert result.claims[0].diagnostic_signals == (
        "preferred_strength_not_established_by_source_candidate",
    )


def test_uncertainty_and_work_capability_are_not_new_employer_demands() -> None:
    source = _source(
        "Responsibilities: Develop LLM products. Requirements: Ability to maintain Python code."
    )
    c = interpret_original_source_candidate(source)
    duty = _find(c, "Develop LLM")
    ability = _find(c, "Ability to maintain")
    result = reconcile_advisory_claims(
        source,
        c,
        (
            _link(duty, "work_implied_capabilities", "LLM engineering"),
            _link(ability, "work_implied_capabilities", "Python maintenance", 1),
            AdvisoryClaim("uncertainties", 0, "Duty scope is unclear"),
        ),
    )
    assert result.claims[0].grounding_state == "linked_semantics_unreviewed"
    assert result.claims[1].diagnostic_signals == (
        "work_implied_capability_without_duty_candidate",
    )
    assert result.claims[2].grounding_state == "unlinked_unknown"


@pytest.mark.parametrize(
    "change,reason",
    [
        ({"field": "bad"}, "shape"),
        ({"index": -1}, "shape"),
        ({"index": True}, "shape"),
        ({"text": ""}, "shape"),
        ({"source_anchor_ids": ("fake",)}, "anchor"),
        ({"source_anchor_ids": ("fake", "fake")}, "anchor|Duplicate"),
        ({"link_provenance": "none"}, "provenance"),
    ],
)
def test_reject_invalid_claim_identity_or_forged_links(change, reason) -> None:
    source = _source("Responsibilities: Develop LLM features.")
    c = interpret_original_source_candidate(source)
    claim = _link(_find(c, "Develop LLM"), "duties", "Develop LLM features")
    with pytest.raises(ValueError, match=reason):
        reconcile_advisory_claims(source, c, (replace(claim, **change),))


def test_unlinked_provenance_duplicate_field_and_stale_source() -> None:
    source = _source("Responsibilities: Develop Python APIs.")
    c = interpret_original_source_candidate(source)
    x = AdvisoryClaim("duties", 0, "Develop APIs")
    with pytest.raises(ValueError, match="provenance"):
        reconcile_advisory_claims(source, c, (replace(x, link_provenance="model_suggested"),))
    with pytest.raises(ValueError, match="Duplicate"):
        reconcile_advisory_claims(source, c, (x, x))
    for stale in (
        replace(source, semantic_sha256="b" * 64),
        replace(source, fields={"description": "Tampered description"}),
    ):
        with pytest.raises(ValueError, match="identity|Stale|anchor|field"):
            reconcile_advisory_claims(stale, c, (x,))


def test_claim_fingerprint_is_source_and_text_specific() -> None:
    source = _source("Responsibilities: Develop Python APIs.")
    a = advisory_claim_sha256(source, "duties", 0, "Develop APIs")
    assert a != advisory_claim_sha256(source, "duties", 0, "Develop AI")
    assert a != advisory_claim_sha256(source, "duties", 1, "Develop APIs")
    assert a != advisory_claim_sha256(
        replace(source, source_job_id="other"), "duties", 0, "Develop APIs"
    )


def test_exposed_four_job_semantic_disagreements_remain_non_promotable() -> None:
    if not B0.is_file():
        pytest.skip("Private frozen original sources are not in public CI")
    store = TranslationStore(B0)
    cases = {j: store.latest_source_version(j) for j in ("tNhZ", "tMps", "tNDx", "tMjm")}
    assert all(cases.values())
    outputs = {}
    for job, source in cases.items():
        assert source is not None
        candidate = interpret_original_source_candidate(source)
        if job == "tNDx":
            preferred_trait = next(
                x
                for x in candidate.items
                if x.category == "behavioral_expectation" and x.employer_strength == "preferred"
            )
            unclear_qualification = next(
                x
                for x in candidate.items
                if x.category == "candidate_qualification" and x.employer_strength == "unresolved"
            )
            claims = (
                _link(preferred_trait, "requirements", "Teamwork is required"),
                _link(unclear_qualification, "preferences", "Credential preferred"),
            )
        elif job == "tMjm":
            ability = next(
                x
                for x in candidate.items
                if x.category == "candidate_qualification" and x.employer_strength == "required"
            )
            claims = (_link(ability, "duties", "New assigned activity"),)
        elif job == "tNhZ":
            arrangement = next(x for x in candidate.items if x.category == "work_arrangement")
            llm_hint = next(x for x in candidate.work_capability_links if x.capability == "LLM")
            duty = next(
                x for x in candidate.items if x.anchor.anchor_id == llm_hint.source_anchor_id
            )
            claims = (
                _link(arrangement, "alternatives", "Applicant eligibility alternatives"),
                _link(duty, "work_implied_capabilities", "LLM engineering"),
            )
        else:
            claims = (AdvisoryClaim("alternatives", 0, "Middle OR Senior"),)
        outputs[job] = reconcile_advisory_claims(source, candidate, claims)
    assert all(x.authority == "candidate_only_no_downstream_reuse" for x in outputs.values())
    assert outputs["tNDx"].claims[0].grounding_state == "source_candidate_disagreement"
    assert outputs["tNDx"].claims[1].grounding_state == "source_candidate_disagreement"
    assert outputs["tMjm"].claims[0].grounding_state == "source_candidate_disagreement"
    assert outputs["tNhZ"].claims[0].grounding_state == "source_candidate_disagreement"
    assert outputs["tNhZ"].claims[1].grounding_state == "linked_semantics_unreviewed"
    assert outputs["tMps"].claims[0].grounding_state == "unlinked_unknown"
