"""B4v6 bounded, source-only decision surface and calibrated navigation evidence."""

from __future__ import annotations

import copy
import hashlib
import json
import runpy
from pathlib import Path

import pytest

from jobhunter.source_qualified_b4v5 import project_source_qualified_case
from jobhunter.source_qualified_b4v6 import (
    COMPACT_CONTRACT,
    CONDITION_LIMIT,
    DUTY_LIMIT,
    GRAPH_LIMIT,
    QUALIFICATION_LIMIT,
    build_compact_decision_view,
    render_compact_decision_views,
)

ROOT = Path(__file__).resolve().parents[1]
SCORECARD = (
    ROOT
    / "docs/working-memory/2026-11-22_p16_b4v6_compact"
    / "SAFE_EXPOSED_COMPACT_DECISION_NAVIGATION.json"
)
PRIVATE = (
    ROOT
    / "data/local-acceptance/p16-b4v6-compact-2026-11-22/v1"
    / "PRIVATE_B4V6_CANDIDATE_AND_TASK_REVIEW.json"
)


def synthetic_projection():
    # Existing B4v5 synthetic fixture is shared without importing private
    # original job data or changing the prior fixture's source interpretation.
    fixtures = runpy.run_path(str(ROOT / "tests/test_source_qualified_b4v5.py"))
    return project_source_qualified_case(fixtures["sample_case"]())


def test_bounded_candidate_preserves_source_and_never_promotes_anything():
    projection = synthetic_projection()
    before = copy.deepcopy(projection)
    view = build_compact_decision_view(projection)
    assert view["contract"] == COMPACT_CONTRACT
    assert view["source_version"] == before["source_version"]
    assert (
        view["source_drilldown"]
        and len(view["source_drilldown"]) == (view["source_qualified_item_count"])
    )
    assert view["accepted_employer_facts"] == 0
    assert view["downstream_authority"] == "none"
    assert view["b5_accepted"] is False
    assert view["b6_production_authorized"] is False
    assert projection == before
    originals = {x["source_item_id"]: x for x in projection["source_qualified_items"]}
    for item in view["source_drilldown"]:
        original = originals[item["source_item_id"]]
        assert item["original_text"] == original["original_text"]
        assert item["source_span_sha256"] == original["source_span_sha256"]
        assert item["english_reading_aid"] == original["target_text_candidate"]
        assert item["strength_candidate"] == original["strength_candidate"]


def test_compact_preview_caps_and_preserves_preference_without_mandatory_overreach():
    view = build_compact_decision_view(synthetic_projection())
    sections = view["sections"]
    assert len(sections["what_work"]["visible"]) <= DUTY_LIMIT
    assert len(sections["conditions"]["visible"]) <= CONDITION_LIMIT
    assert all(
        len(section["visible"]) <= QUALIFICATION_LIMIT
        for section in sections["capabilities"].values()
    )
    assert all(
        item["strength_candidate"] == "preferred"
        for item in sections["capabilities"]["preferred_candidate"]["visible"]
    )
    assert not any(
        item["strength_candidate"] == "required"
        for item in sections["capabilities"]["preferred_candidate"]["visible"]
    )
    assert (
        sections["capabilities"]["preferred_candidate"]["visible"][0]["source_item_id"]
        == "preferred"
    )


def test_conditional_exam_precedes_other_arrangement_and_survives_compaction():
    view = build_compact_decision_view(synthetic_projection())
    conditions = view["sections"]["conditions"]["visible"]
    assert conditions
    assert conditions[0]["source_item_id"] == "condition"
    assert conditions[0]["explicit_conditional_application"] is True


def test_unreviewed_eligibility_graph_preserved_without_inventing_child_english():
    view = build_compact_decision_view(synthetic_projection())
    graphs = view["sections"]["eligibility"]["unreviewed_candidate_graphs"]
    assert len(graphs) <= GRAPH_LIMIT
    assert len(graphs) == 1
    assert graphs[0]["root"]["kind"] in {"any_of", "all_of"}
    md = render_compact_decision_views([view])
    assert "not an accepted employer eligibility condition" in md
    assert "independent English child alignment **not established**" in md
    assert "source" in md


def test_zero_explicit_duties_cannot_turn_into_no_real_job_responsibilities():
    original = synthetic_projection()
    trimmed = copy.deepcopy(original)
    trimmed["source_qualified_items"] = [
        i for i in trimmed["source_qualified_items"] if i["category_candidate"] != "work_duty"
    ]
    trimmed["groups"].pop("work_duty", None)
    trimmed["source_item_count"] -= 1
    view = build_compact_decision_view(trimmed)
    assert view["sections"]["what_work"]["candidate_count"] == 0
    md = render_compact_decision_views([view])
    assert "does not establish that the job has no responsibilities" in md


def test_source_hash_tampering_rejected_in_preview():
    projection = synthetic_projection()
    broken = copy.deepcopy(projection)
    broken["source_qualified_items"][0]["original_text"] += " injected"
    with pytest.raises(ValueError, match="identity/authority mismatch"):
        build_compact_decision_view(broken)


def test_accepted_employer_claim_promotion_rejected():
    projection = synthetic_projection()
    projection["accepted_employer_facts"] = 1
    with pytest.raises(ValueError, match="different or promoted"):
        build_compact_decision_view(projection)


def test_unaligned_eligibility_child_alignment_fabrication_is_rejected():
    projection = synthetic_projection()
    graph = projection["eligibility_alternative_candidates"][0]

    # Mutate a private synthetic copy to ensure even a claimed English offset
    # cannot sneak into the source-first compact view.
    def corrupt(node):
        if node["kind"] == "original_subspan":
            node["child_english_alignment"] = "invented_alignment"
            return True
        return any(corrupt(child) for child in node.get("children", []))

    assert corrupt(graph["root"])
    with pytest.raises(ValueError, match="cannot invent English alignment"):
        build_compact_decision_view(projection)


def test_untrusted_employer_markdown_is_escaped_in_compact_renderer():
    projection = synthetic_projection()
    changed = copy.deepcopy(projection)
    item = changed["source_qualified_items"][0]
    item["original_text"] = "unsafe [click](https://malicious.example) <script>boom</script>"
    item["source_span_sha256"] = hashlib.sha256(item["original_text"].encode()).hexdigest()
    for original in changed["groups"][item["category_candidate"]]:
        if original["source_item_id"] == item["source_item_id"]:
            original["original_text"] = item["original_text"]
            original["source_span_sha256"] = item["source_span_sha256"]
    if item["b4_reviewed_terminology_overlay"]:
        pytest.skip("Use a synthetic item without an existing terminology overlay")
    view = build_compact_decision_view(changed)
    rendered = render_compact_decision_views([view])
    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered
    assert "](https://malicious.example)" not in rendered


def test_no_unknown_or_unrelated_source_graph_can_be_silently_accepted():
    projection = synthetic_projection()
    bad = copy.deepcopy(projection)
    bad["eligibility_alternative_candidates"][0]["authority"] = "accepted_employer_eligibility"
    with pytest.raises(ValueError, match="eligibility authority changed"):
        build_compact_decision_view(bad)


def test_public_aggregate_is_safe_and_scoped():
    record = json.loads(SCORECARD.read_text(encoding="utf-8"))
    assert record["contract"] == "jobhunter-p16-b4v6-compact-usefulness-exposed-v1"
    assert record["status"] == "PASS_EXPOSED_COMPACT_PRESENTATION_ENGINEERING_NOT_USER_BENEFIT"
    assert record["frozen_protocol_preimplementation_commit"] == "e830c3c"
    assert record["case_count"] == 4
    assert record["predeclared_task_count"] == 9
    assert record["original_B4v5_source_qualified_items"] == 64
    assert record["B4v6_immediately_visible_source_items"] < 64
    assert record["B4v6_full_drilldown_source_items"] == 64
    assert record["B4v6_markdown_chars"] < record["B4v5_markdown_chars"]
    assert record["task_all_original_evidence_available"] is True
    assert record["existing_v30_valid_same_source_artifact_count"] == 0
    assert record["new_model_http_requests"] == record["new_source_requests"] == 0
    assert record["new_accepted_employer_facts"] == 0
    assert record["B5_independent_generalization_accepted"] is False
    assert record["B6_production_promotion_authorized"] is False
    assert record["user_time_saved_measured"] is False
    assert record["blind_independent_human_review"] is False
    for path, expected in record["code_sha256"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
    safe_json = SCORECARD.read_text(encoding="utf-8")
    assert "original_text" not in safe_json
    assert "source_item_id" not in safe_json
    assert "private_raw_html_path" not in safe_json
    assert "tNhZ" not in safe_json
    assert not any("\u0600" <= character <= "\u06ff" for character in safe_json)


def test_private_exposed_replay_is_read_only_and_hash_stable():
    if not PRIVATE.is_file():
        pytest.skip("Private original B4v5 source projection absent on clean CI")
    verify = runpy.run_path(str(ROOT / "scripts/evaluate_p16_b4v6_compact_usefulness.py"))[
        "verify"
    ]()
    assert verify["status"] == "PASS_EXPOSED_COMPACT_PRESENTATION_ENGINEERING_NOT_USER_BENEFIT"
    assert verify["predeclared_task_count"] == 9
    assert verify["B5_independent_generalization_accepted"] is False
