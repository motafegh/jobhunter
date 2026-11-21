"""Regression tests for B5 original-source/unchanged-B2 early stop gate."""

from __future__ import annotations

import hashlib

# The diagnostic is a standalone script, not a production module.
import runpy
from pathlib import Path
from types import SimpleNamespace

import pytest

from jobhunter import source_item_candidate_b2
from jobhunter.source_item_candidate_b2 import interpret_original_source_candidate

ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(ROOT / "scripts/evaluate_p16_b5_source_gate.py"))
match_source_anchor = MODULE["match_source_anchor"]
evaluate_source_gate = MODULE["evaluate_source_gate"]


def record(
    *,
    job_id: str = "job-1",
    kind: str = "duty",
    modality: str = "stated",
    quote: str = "Review code for security",
    candidate_category: str = "work_duty",
    candidate_strength: str = "not_applicable",
) -> tuple[dict, SimpleNamespace, SimpleNamespace]:
    anchor = {
        "anchor_id": f"{job_id}-SO-01",
        "original_description_start": 0,
        "original_description_end": len(quote),
        "original_quote": quote,
        "quote_sha256": hashlib.sha256(quote.encode()).hexdigest(),
        "kind": kind,
        "modality_source_first": modality,
    }
    item = SimpleNamespace(
        anchor=SimpleNamespace(char_start=0, char_end=len(quote), anchor_id="a"),
        category=candidate_category,
        employer_strength=candidate_strength,
    )
    candidate = SimpleNamespace(
        items=[item],
        alternatives=[],
        authority="candidate_only_no_downstream_reuse",
    )
    source = SimpleNamespace(semantic_sha256="a" * 64)
    return anchor, candidate, source


def test_exact_original_span_and_source_role_are_both_required():
    anchor, candidate, _ = record()
    result = match_source_anchor(anchor, candidate)
    assert result["span_present_within_one_candidate"] is True
    assert result["candidate_semantic_role_match"] is True
    assert result["optional_or_negative_strengthened_to_required"] is False


def test_candidate_parse_mechanical_success_does_not_imply_semantic_success():
    anchor, candidate, _ = record(candidate_category="context")
    result = match_source_anchor(anchor, candidate)
    assert result["span_present_within_one_candidate"] is True
    assert result["candidate_semantic_role_match"] is False
    assert result["verdict_state"] == "covered_category_mismatch"


@pytest.mark.parametrize(
    "modality", ["explicit_preferred", "nice_to_have", "bonus_optional", "explicit_not_required"]
)
def test_optional_or_negated_original_cannot_be_strengthened_to_required(modality: str):
    anchor, candidate, _ = record(
        kind="qualification",
        modality=modality,
        candidate_category="candidate_qualification",
        candidate_strength="required",
    )
    result = match_source_anchor(anchor, candidate)
    assert result["candidate_semantic_role_match"] is True
    assert result["optional_or_negative_strengthened_to_required"] is True


def test_tampered_original_quote_hash_fails_closed():
    anchor, candidate, _ = record()
    anchor["quote_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="SHA"):
        match_source_anchor(anchor, candidate)


def test_b2_split_across_reviewed_source_span_is_uncovered_not_falsely_matched():
    anchor, candidate, _ = record()
    candidate.items[0].anchor.char_end = 10
    result = match_source_anchor(anchor, candidate)
    assert result["span_present_within_one_candidate"] is False
    assert result["candidate_semantic_role_match"] is None


def test_six_job_source_first_cohort_blocks_missing_explicit_duty(monkeypatch):
    # runpy returns a mapping separate from the function's executable globals.
    script_globals = evaluate_source_gate.__globals__
    monkeypatch.setitem(
        script_globals,
        "verify_b2_candidate",
        lambda candidate, source: None,
    )
    monkeypatch.setitem(
        script_globals,
        "build_candidate_eligibility_logic",
        lambda source, candidate: SimpleNamespace(graphs=[]),
    )
    entries, versions, candidates, selected = [], {}, {}, []
    for i in range(6):
        job = f"job-{i}"
        anchor, candidate, source = record(
            job_id=job,
            candidate_category="unresolved" if i == 1 else "work_duty",
        )
        entries.append(
            {
                "source_job_id": job,
                "source_semantic_sha256": source.semantic_sha256,
                "reviewed_original_anchors": [anchor],
            }
        )
        versions[job] = source
        candidates[job] = candidate
        selected.append({"source_job_id": job})
    verdict = evaluate_source_gate(
        frozen={"selected_primary": selected},
        review={"entries": entries},
        source_versions=versions,
        engine=lambda s: candidates[next(job for job, source in versions.items() if source is s)],
    )
    assert verdict["disposition"] == "BLOCKED_UPSTREAM_SOURCE_SEMANTICS"
    assert verdict["counts"]["explicit_duty_missed_anchor_count"] == 1
    assert verdict["counts"]["job_count_with_critical_structural_or_category_gaps"] == 1
    assert verdict["new_b3_translation_requests"] == 0
    assert verdict["new_b4_analysis_requests"] == 0
    assert verdict["accepted_facts_promoted"] == 0
    assert verdict["exhaustive_source_statement_denominator"] is False


def test_source_first_selection_order_change_rejected():
    anchor, candidate, source = record()
    with pytest.raises(ValueError, match="order"):
        evaluate_source_gate(
            frozen={"selected_primary": [{"source_job_id": "different"}] * 6},
            review={
                "entries": [
                    {
                        "source_job_id": "job-1",
                        "source_semantic_sha256": source.semantic_sha256,
                        "reviewed_original_anchors": [anchor],
                    }
                ]
            },
            source_versions={"job-1": source},
            engine=lambda _s: candidate,
        )


def test_B2_parser_function_is_not_redefined_for_B5_holdout():
    assert (
        interpret_original_source_candidate
        is source_item_candidate_b2.interpret_original_source_candidate
    )
