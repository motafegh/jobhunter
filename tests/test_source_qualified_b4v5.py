"""B4v5 source-projection tests: source integrity, alternative eligibility and corrections."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from jobhunter.source_qualified_b4v5 import (
    apply_reviewed_translation_overlay,
    markdown_escape,
    project_source_qualified_case,
    render_source_qualified_briefs,
)

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / "data/local-acceptance/p16-stage-b4-2026-11-19/primary-v4c"
REVIEW = ROOT / (
    "data/local-acceptance/p16-stage-b4-2026-11-19/reviewed-terminology-correction-v5.json"
)


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def sample_case() -> dict:
    text = "Use the فدک system to help customers"
    english = "Use the FDC ticketing system to help customers"
    items = [
        {
            "item_id": "duty",
            "original_text": text,
            "source_span_sha256": sha(text),
            "category_candidate": "work_duty",
            "strength_candidate": "not_applicable",
            "qualifier_candidate": "not_applicable",
            "evidence_basis_candidate": "explicit_original_wording",
            "excluded_reason": None,
            "translation": {
                "target_text": english,
                "target_sha256": sha(english),
                "review_state": "assistant_reviewed_exposed_cohort",
            },
        },
        {
            "item_id": "middle",
            "original_text": "2–4 years or 4–7 years",
            "source_span_sha256": sha("2–4 years or 4–7 years"),
            "category_candidate": "candidate_qualification",
            "strength_candidate": "required",
            "qualifier_candidate": "positive_explicit",
            "evidence_basis_candidate": "explicit_original_wording",
            "excluded_reason": None,
            "translation": {
                "target_text": "Middle track: 2–4 years OR Senior track: 4–7 years",
                "target_sha256": sha("Middle track: 2–4 years OR Senior track: 4–7 years"),
                "review_state": "assistant_reviewed_exposed_cohort",
            },
        },
        {
            "item_id": "preferred",
            "original_text": "LLM familiarity is a plus but not mandatory",
            "source_span_sha256": sha("LLM familiarity is a plus but not mandatory"),
            "category_candidate": "candidate_qualification",
            "strength_candidate": "preferred",
            "qualifier_candidate": "negative_explicit",
            "evidence_basis_candidate": "explicit_original_wording",
            "excluded_reason": None,
            "translation": {
                "target_text": "LLM familiarity is a plus but not mandatory",
                "target_sha256": sha("LLM familiarity is a plus but not mandatory"),
                "review_state": "native_english_exact_identity",
            },
        },
        {
            "item_id": "condition",
            "original_text": "Passing a technical exam is a condition",
            "source_span_sha256": sha("Passing a technical exam is a condition"),
            "category_candidate": "application_instruction",
            "strength_candidate": "not_applicable",
            "qualifier_candidate": "not_applicable",
            "evidence_basis_candidate": "explicit_original_wording",
            "excluded_reason": None,
            "translation": {
                "target_text": "Passing a technical exam is a condition",
                "target_sha256": sha("Passing a technical exam is a condition"),
                "review_state": "assistant_reviewed_exposed_cohort",
            },
        },
        {
            "item_id": "context",
            "original_text": "About employer",
            "category_candidate": "context",
            "strength_candidate": "not_applicable",
            "excluded_reason": "context_only",
            "translation": None,
        },
    ]
    child_text = "2–4 years"
    nested = {
        "leaf_item_id": "middle_child",
        "parent_item_id": "middle",
        "source_text": child_text,
        "leaf_text_sha256": sha(child_text),
        "target_subspan_alignment": "not_established",
    }
    return {
        "source_job_id": "testjob",
        "attempt_outcome": "completed",
        "candidate": {
            "source_version": {"source_job_id": "testjob", "semantic_sha256": "a" * 64},
            "analysis_outcome": "partial_candidate",
            "items": items,
            "nested_eligibility_items": [nested],
            "eligibility_graphs": [
                {
                    "graph_id": "test_middle_or_senior",
                    "review_state": "candidate",
                    "root_id": "root",
                    "nodes": [
                        {"id": "root", "operator": "any_of", "children": ["m", "s"]},
                        {"id": "m", "operator": "item", "item_id": "middle_child"},
                        {"id": "s", "operator": "item", "item_id": "middle"},
                    ],
                }
            ],
            "conflicts": [],
            "board_values": [],
            "brief": {
                "role_summary": {
                    "summary": "Help customers via FDC.",
                    "source_item_ids": ["duty"],
                },
                "work_activities": [
                    {
                        "summary": "Work with FDC",
                        "source_item_ids": ["duty"],
                    }
                ],
                "expectation_summaries": [],
                "work_implied_capabilities": [],
                "open_questions": [],
            },
        },
    }


def sample_correction() -> dict:
    c = sample_case()
    item = c["candidate"]["items"][0]
    revised = item["translation"]["target_text"].replace("FDC", "Fadak")
    return {
        "source_job_id": "testjob",
        "source_item_id": "duty",
        "source_semantic_sha256": "a" * 64,
        "source_span_sha256": item["source_span_sha256"],
        "original_target_sha256": item["translation"]["target_sha256"],
        "source_token": "فدک",
        "old_target_token": "FDC",
        "reviewed_target_token": "Fadak",
        "reviewed_target_text": revised,
        "reviewed_target_sha256": sha(revised),
        "reviewer": "assistant_original_source_terminology_review",
    }


def test_source_projection_preserves_preferred_negative_and_conditional_terms():
    projection = project_source_qualified_case(sample_case())
    assert projection["source_item_count"] == 5
    assert len(projection["source_qualified_items"]) == 4
    assert projection["excluded_source_item_count"] == 1
    preferred = projection["groups"]["candidate_qualification"][1]
    assert preferred["strength_candidate"] == "preferred"
    assert preferred["qualifier_candidate"] == "negative_explicit"
    assert "not mandatory" in preferred["target_text_candidate"]
    condition = projection["groups"]["application_instruction"][0]
    assert condition["is_conditional_application_statement"]
    assert condition["authority"] == "B2_B3_source_qualified_candidate_not_accepted_fact"
    assert projection["accepted_employer_facts"] == 0


def test_alternatives_remain_structured_not_flattened_to_cumulative_requirement():
    projection = project_source_qualified_case(sample_case())
    graph = projection["eligibility_alternative_candidates"][0]
    assert graph["root"]["kind"] == "any_of"
    assert len(graph["root"]["children"]) == 2
    assert graph["root"]["children"][0]["kind"] == "original_subspan"
    assert graph["root"]["children"][0]["child_english_alignment"] == "not_established"
    assert graph["root"]["children"][0]["original_text"] == "2–4 years"
    assert projection["groups"]["candidate_qualification"][0][
        "in_eligibility_alternative_candidate"
    ]
    result = render_source_qualified_briefs([projection])
    assert "ONE OF (OR)" in result
    assert "not cumulative" in result
    assert "At a glance" in result
    assert "LLM familiarity is a plus but not mandatory" in result
    assert "Passing a technical exam is a condition" in result


def test_translation_overlay_revises_one_provenance_bound_term_without_b3_mutation():
    case = sample_case()
    before = json.dumps(case, ensure_ascii=False, sort_keys=True)
    review = sample_correction()
    projection = project_source_qualified_case(case, correction=review)
    corrected = projection["groups"]["work_duty"][0]
    assert "Fadak" in corrected["target_text_candidate"]
    assert "FDC" not in corrected["target_text_candidate"]
    assert corrected["b3_selected_target_sha256"] == sha(
        "Use the FDC ticketing system to help customers"
    )
    assert projection["corrected_translation_item_ids"] == ["duty"]
    assert set(projection["v4_model_claims_suppressed_due_to_translation_review"]) == {
        "role_summary",
        "work_activities[0]",
    }
    assert json.dumps(case, ensure_ascii=False, sort_keys=True) == before


@pytest.mark.parametrize(
    "change",
    [
        {"source_span_sha256": "0" * 64},
        {"original_target_sha256": "0" * 64},
        {"source_token": "not in original"},
        {"old_target_token": "FDO"},
        {"reviewed_target_text": "Invent a whole new job responsibility"},
        {"reviewer": "unknown"},
        {"source_job_id": "other_job"},
    ],
)
def test_translation_review_rejects_unowned_or_broadened_corrections(change):
    c = sample_case()["candidate"]
    review = sample_correction()
    review.update(change)
    with pytest.raises(ValueError):
        apply_reviewed_translation_overlay(candidate=c, correction=review)


def test_malformed_graph_cycle_and_missing_nested_parent_are_blocked():
    case = sample_case()
    bad = copy.deepcopy(case)
    bad["candidate"]["eligibility_graphs"][0]["nodes"][1] = {
        "id": "m",
        "operator": "any_of",
        "children": ["root"],
    }
    with pytest.raises(ValueError, match="cycles"):
        project_source_qualified_case(bad)
    bad2 = copy.deepcopy(case)
    bad2["candidate"]["nested_eligibility_items"][0]["parent_item_id"] = "missing"
    with pytest.raises(ValueError, match="parent"):
        project_source_qualified_case(bad2)


def test_source_markdown_is_escaped_not_executable():
    assert "&lt;script&gt;" in markdown_escape("<script>alert(1)</script>")
    assert markdown_escape("[click](https://bad.example)") != "[click](https://bad.example)"


@pytest.mark.skipif(
    not (PRIOR / "PRIVATE_B4_CANDIDATES.json").exists() or not REVIEW.exists(),
    reason="Private frozen B4 review data are intentionally absent in clean CI",
)
def test_four_frozen_cases_have_complete_source_qualified_projection():
    prior = json.loads((PRIOR / "PRIVATE_B4_CANDIDATES.json").read_text())
    review = json.loads(REVIEW.read_text())["corrections"][0]
    projections = [
        project_source_qualified_case(
            case, correction=review if case["source_job_id"] == "tNDx" else None
        )
        for case in prior["cases"]
    ]
    assert sum(len(p["source_qualified_items"]) for p in projections) == 64
    assert sum(p["excluded_source_item_count"] for p in projections) == 14
    assert [p["source_job_id"] for p in projections] == ["tNhZ", "tMps", "tNDx", "tMjm"]
    assert sum(len(p["eligibility_alternative_candidates"]) for p in projections) == 2
    assert len(projections[1]["eligibility_alternative_candidates"][0]["root"]["children"]) == 2
    assert projections[2]["corrected_translation_item_ids"] == [
        "s_ae62e5aa14da3bfe232413c7ca6d01907c2878b1"
    ]
    assert len(projections[3]["groups"].get("work_duty", [])) == 0
    assert projections[3]["v4_model_candidates"] is None
    assert (
        projections[0]["groups"]["candidate_qualification"][-1]["strength_candidate"] == "preferred"
    )
