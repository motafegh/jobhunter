from __future__ import annotations

import hashlib
import json
import runpy
import sqlite3
from pathlib import Path
from types import SimpleNamespace

import pytest
from jsonschema import Draft202012Validator

from jobhunter.source_job_understanding_b4 import (
    B4_CONTRACT_VERSION,
    build_b4_evidence_bundle,
    build_b4_model_payload,
    build_coverage_ledger,
    finalize_b4_case,
    validate_b4_model_response,
)

ROOT = Path(__file__).resolve().parents[1]


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def evidence_fixture() -> dict:
    return {
        "contract_version": B4_CONTRACT_VERSION,
        "source_version": {
            "source_job_id": "job-1",
            "job_detail_version_id": 1,
            "semantic_sha256": "a" * 64,
        },
        "posting_title": "Security Engineer",
        "items": [
            {
                "item_id": "duty-1",
                "original_text": "Develop and maintain security tooling",
                "category_candidate": "work_duty",
                "strength_candidate": "not_applicable",
                "translation": {
                    "review_state": "assistant_reviewed_exposed_cohort",
                    "target_text": "Develop and maintain security tooling",
                },
                "excluded_reason": None,
            },
            {
                "item_id": "req-1",
                "original_text": "Python experience preferred",
                "category_candidate": "candidate_qualification",
                "strength_candidate": "preferred",
                "translation": {
                    "review_state": "assistant_reviewed_exposed_cohort",
                    "target_text": "Experience with Python",
                },
                "excluded_reason": None,
            },
            {
                "item_id": "unresolved-1",
                "original_text": "Certificate or equivalent knowledge",
                "category_candidate": "candidate_qualification",
                "strength_candidate": "unresolved",
                "translation": {
                    "review_state": "assistant_reviewed_exposed_cohort",
                    "target_text": "Security certification or equivalent knowledge",
                },
                "excluded_reason": None,
            },
            {
                "item_id": "arrangement-1",
                "original_text": "Remote work possible",
                "category_candidate": "work_arrangement",
                "strength_candidate": "not_applicable",
                "translation": {
                    "review_state": "assistant_reviewed_exposed_cohort",
                    "target_text": "Remote work is possible",
                },
                "excluded_reason": None,
            },
            {
                "item_id": "context-1",
                "category_candidate": "context",
                "strength_candidate": "not_applicable",
                "translation": None,
                "excluded_reason": "context-only item excluded by B3 selection",
            },
        ],
        "eligibility_graphs": [],
        "nested_eligibility_items": [],
        "board_values": [],
        "conflicts": [],
        "brief": None,
        "analysis_outcome": "not_run",
        "downstream_authority": "none",
    }


def valid_response() -> dict:
    return {
        "role_summary": {
            "summary": (
                "The vacancy combines security-tooling development with operational security work."
            ),
            "source_item_ids": ["I01", "I02"],
        },
        "work_activities": [
            {"summary": "Develop and maintain security tooling.", "source_item_ids": ["I01"]}
        ],
        "expectation_summaries": [
            {"summary": "Python experience is presented as preferred.", "source_item_ids": ["I02"]}
        ],
        "work_implied_capabilities": [
            {
                "capability": "Security-tooling development",
                "rationale": (
                    "The assigned development work implies the ability "
                    "to design and maintain tooling."
                ),
                "source_item_ids": ["I01"],
            }
        ],
        "open_questions": [
            {
                "question": "The exact certification strength remains unclear.",
                "source_item_ids": ["I03"],
            }
        ],
    }


def _builder_fixture(*, native: bool = False, corrective: bool = False):
    text = "Build security tooling" if not native else "Build security tooling"
    anchor = SimpleNamespace(
        anchor_id="anchor-1",
        field_sha256=digest(text),
        text_sha256=digest(text),
        char_start=0,
        char_end=len(text),
        exact_text=text,
    )
    item = SimpleNamespace(
        anchor=anchor,
        category="work_duty",
        employer_strength="not_applicable",
        evidence_basis="original_source_item",
        heading="Responsibilities",
        qualifier="none",
    )
    source = SimpleNamespace(
        source_job_id="job-1",
        job_detail_version_id=1,
        semantic_sha256="a" * 64,
        fields={"description": text, "title": "Security Engineer"},
    )
    candidate = SimpleNamespace(
        source_job_id="job-1",
        detail_version_id=1,
        source_semantic_sha256="a" * 64,
        source_field_sha256=digest(text),
        items=(item,),
        board_values=(),
    )
    selection = SimpleNamespace(
        translate_items=() if native else (item,),
        native_identity_items=(item,) if native else (),
        excluded_items=(),
    )
    context = {"selection": selection, "nested": []}
    item_id = "s_anchor1"
    b1_alignment = {
        "source_item_id": item_id,
        "state": "unresolved" if native else "source_bound_translation_candidate",
        "translation_sha256": None if native else digest("Build and maintain security tools"),
        "target": None
        if native
        else {"target_span": {"text_sha256": digest("Build and maintain security tools")}},
    }
    primary_text = text if native else "Build and maintain security tools"
    record = {
        "source_job_id": "job-1",
        "source_item_id": item_id,
        "source_anchor_id": "anchor-1",
        "source_semantic_sha256": "a" * 64,
        "source_span_sha256": digest(text),
        "source_char_start": 0,
        "source_char_end": len(text),
        "state": "native_identity" if native else "source_bound_translation_candidate",
        "target_text": "primary translation" if corrective else primary_text,
        "target_sha256": digest("primary translation") if corrective else digest(primary_text),
        "provider_name": "lm-studio-translation-v2",
        "provider_model": "gemma-4-e2b-it",
        "prompt_version": "translation-v2",
    }
    correction = None
    final_audit = {
        "status": "PASS",
        "production_database_written": False,
        "accepted_facts_promoted": 0,
        "unseen_generalization_established": False,
    }
    if corrective:
        corrected_text = "Build and maintain security tooling"
        correction = {
            "source_job_id": "job-1",
            "source_item_id": item_id,
            "source_anchor_id": "anchor-1",
            "selection_status": "selected_for_b1_candidate_alignment",
            "reviewer_normalized_target_text": corrected_text,
            "reviewer_normalized_target_sha256": digest(corrected_text),
        }
        final_audit["selected_corrective_target_sha256"] = digest(corrected_text)
        b1_alignment["translation_sha256"] = digest(corrected_text)
        b1_alignment["target"]["target_span"]["text_sha256"] = digest(corrected_text)
    b1_draft = {
        "source_version": {
            "source_job_id": "job-1",
            "job_detail_version_id": 1,
            "semantic_sha256": "a" * 64,
        },
        "items": [
            {
                "item_id": item_id,
                "source_ref": {
                    "kind": "original_description_span",
                    "anchor_id": "anchor-1",
                },
            }
        ],
        "alignments": [b1_alignment],
    }
    semantic_review = {
        "status": "PASS_BOUNDED_EXPOSED_COHORT_WITH_ONE_CORRECTIVE_SELECTED",
        "reviewer": "assistant_exposed_cohort_semantic_review",
        "unseen_generalization_established": False,
        "independent_holdout_count": 0,
        "critical_semantic_checks": {"source_meaning": "PASS"},
        "per_job_reviewed": {"job-1": 1},
    }
    return (
        source,
        candidate,
        context,
        b1_draft,
        [record],
        correction,
        semantic_review,
        final_audit,
    )


def test_response_schema_is_valid_json_schema():
    schema = json.loads(
        (ROOT / "docs/contracts/p16-stage-b4/job_understanding_response.schema.json").read_text()
    )
    Draft202012Validator.check_schema(schema)


def test_builder_binds_selected_translation_and_preserves_candidate_authority():
    args = _builder_fixture()
    evidence = build_b4_evidence_bundle(
        source=args[0],
        candidate=args[1],
        context=args[2],
        b1_draft=args[3],
        b3_records=args[4],
        corrective=args[5],
        semantic_review=args[6],
        final_audit=args[7],
    )
    item = evidence["items"][0]
    assert item["translation"]["target_text"] == "Build and maintain security tools"
    assert item["translation"]["review_state"] == "assistant_reviewed_exposed_cohort"
    assert evidence["authority"] == "candidate_only_no_downstream_reuse"
    assert evidence["translation_review"]["independent_blind_review"] is False


def test_builder_uses_selected_corrective_translation_not_primary_output():
    args = _builder_fixture(corrective=True)
    evidence = build_b4_evidence_bundle(
        source=args[0],
        candidate=args[1],
        context=args[2],
        b1_draft=args[3],
        b3_records=args[4],
        corrective=args[5],
        semantic_review=args[6],
        final_audit=args[7],
    )
    translation = evidence["items"][0]["translation"]
    assert translation["target_text"] == "Build and maintain security tooling"
    assert translation["review_state"].startswith("assistant_reviewed_corrective_selected")


def test_native_identity_does_not_invent_b1_target_offsets():
    args = _builder_fixture(native=True)
    evidence = build_b4_evidence_bundle(
        source=args[0],
        candidate=args[1],
        context=args[2],
        b1_draft=args[3],
        b3_records=args[4],
        corrective=args[5],
        semantic_review=args[6],
        final_audit=args[7],
    )
    translation = evidence["items"][0]["translation"]
    assert translation["state"] == "native_english_identity"
    assert (
        translation["b1_alignment_state"]
        == "unresolved_native_identity_target_offsets_not_established"
    )
    assert translation["target_text"] == args[0].fields["description"]


def test_builder_rejects_stale_source_identity():
    args = list(_builder_fixture())
    args[1] = SimpleNamespace(**{**vars(args[1]), "source_semantic_sha256": "b" * 64})
    with pytest.raises(ValueError, match="stale"):
        build_b4_evidence_bundle(
            source=args[0],
            candidate=args[1],
            context=args[2],
            b1_draft=args[3],
            b3_records=args[4],
            corrective=args[5],
            semantic_review=args[6],
            final_audit=args[7],
        )


def test_nested_eligibility_graph_maps_child_to_parent_source_item():
    evidence = {
        "source_version": {"source_job_id": "job-1"},
        "posting_title": "AI Engineer",
        "items": [
            {
                "item_id": "parent-1",
                "original_text": "Middle or Senior track",
                "category_candidate": "candidate_qualification",
                "strength_candidate": "required",
                "qualifier_candidate": "none",
                "heading_context": None,
                "translation": {
                    "target_text": "Middle or Senior track",
                    "review_state": "assistant_reviewed_exposed_cohort",
                },
            }
        ],
        "eligibility_graphs": [
            {
                "graph_id": "middle-or-senior",
                "root_id": "tracks",
                "review_state": "candidate",
                "basis_item_ids": ["parent-1"],
                "nodes": [
                    {"id": "tracks", "operator": "any_of", "children": ["middle", "senior"]},
                    {"id": "middle", "operator": "item", "item_id": "leaf-middle"},
                    {"id": "senior", "operator": "item", "item_id": "leaf-senior"},
                ],
            }
        ],
        "nested_eligibility_items": [
            {
                "leaf_item_id": "leaf-middle",
                "parent_item_id": "parent-1",
                "source_text": "Middle track",
            },
            {
                "leaf_item_id": "leaf-senior",
                "parent_item_id": "parent-1",
                "source_text": "Senior track",
            },
        ],
    }
    payload = build_b4_model_payload(evidence)
    # Graph nodes and nested subspans remain in deterministic evidence.
    # Model should not receive uncitable graph IDs.
    assert "eligibility_graphs" not in payload
    assert "leaf-middle" not in json.dumps(payload)
    assert evidence["eligibility_graphs"][0]["nodes"][1]["item_id"] == "leaf-middle"


def test_response_validator_accepts_capability_link_only_when_duty_is_cited():
    evidence = evidence_fixture()
    validated = validate_b4_model_response(valid_response(), evidence)
    capability = validated["work_implied_capabilities"][0]
    assert capability["interpretation_state"] == "derived_interpretation_candidate"
    assert capability["employer_prior_experience_status"] == "not_established_from_source"
    assert validated["source_reference_state"] == "canonical_source_item_ids_resolved"
    assert validated["role_summary"]["source_item_ids"] == ["duty-1", "req-1"]
    assert validated["work_activities"][0]["source_item_ids"] == ["duty-1"]
    assert validated["expectation_summaries"][0]["source_item_ids"] == ["req-1"]
    assert validated["open_questions"][0]["source_item_ids"] == ["unresolved-1"]
    assert validated["referenced_item_ids"] == ["duty-1", "req-1", "unresolved-1"]


def test_response_validator_rejects_capability_without_duty_reference():
    evidence = evidence_fixture()
    response = valid_response()
    response["work_implied_capabilities"][0]["source_item_ids"] = ["I02"]
    with pytest.raises(ValueError, match="explicit work-duty"):
        validate_b4_model_response(response, evidence)


def test_response_validator_rejects_arrangement_as_work_duty():
    evidence = evidence_fixture()
    response = valid_response()
    response["work_activities"][0]["source_item_ids"] = ["I04"]
    with pytest.raises(ValueError, match="explicit duty"):
        validate_b4_model_response(response, evidence)


def test_response_validator_rejects_unknown_or_excluded_item_ids():
    evidence = evidence_fixture()
    response = valid_response()
    response["role_summary"]["source_item_ids"] = ["I05"]
    with pytest.raises(ValueError, match="unknown or excluded"):
        validate_b4_model_response(response, evidence)


def test_coverage_ledger_keeps_strength_unknown_and_exclusions_separate():
    evidence = evidence_fixture()
    brief = validate_b4_model_response(valid_response(), evidence)
    ledger, counts = build_coverage_ledger(evidence, brief)
    by_id = {row["item_id"]: row for row in ledger}
    assert by_id["duty-1"]["coverage_status"] == "duty"
    assert by_id["req-1"]["coverage_status"] == "requirement"
    assert by_id["unresolved-1"]["coverage_status"] == "unresolved"
    assert by_id["arrangement-1"]["coverage_status"] == "not_summarized"
    assert by_id["context-1"]["coverage_status"] == "excluded"
    assert sum(counts.values()) == len(evidence["items"])


def test_failed_model_keeps_source_evidence_fallback():
    evidence = evidence_fixture()
    candidate = finalize_b4_case(evidence, response=None, failure_state="timed_out")
    assert candidate["analysis_outcome"] == "timed_out"
    assert candidate["brief"] is None
    assert len(candidate["items"]) == len(evidence["items"])
    assert candidate["downstream_authority"] == "none"


def test_no_duty_posting_cannot_receive_fabricated_work_activity_or_capability():
    evidence = evidence_fixture()
    evidence["items"] = [
        item for item in evidence["items"] if item["category_candidate"] != "work_duty"
    ]
    response = valid_response()
    response["role_summary"]["source_item_ids"] = ["I01"]
    response["work_activities"] = []
    response["work_implied_capabilities"] = []
    response["expectation_summaries"] = [
        {"summary": "Python experience is preferred.", "source_item_ids": ["I01"]}
    ]
    response["open_questions"] = [
        {"question": "Certification strength is unclear.", "source_item_ids": ["I02"]}
    ]
    validated = validate_b4_model_response(response, evidence)
    assert validated["work_activities"] == []
    assert validated["work_implied_capabilities"] == []


def test_baseline_reader_distinguishes_failed_v30_from_accepted_v9():
    script = runpy.run_path(str(ROOT / "scripts/run_p16_b4_job_understanding.py"))
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.executescript(
        """
        CREATE TABLE job_analysis_attempts (
            id INTEGER PRIMARY KEY, job_detail_version_id INTEGER, prompt_version TEXT,
            outcome TEXT, artifact_id INTEGER, error_type TEXT
        );
        CREATE TABLE job_analysis_artifacts (
            id INTEGER PRIMARY KEY, job_detail_version_id INTEGER, prompt_version TEXT,
            semantic_review_status TEXT
        );
        CREATE TABLE job_analysis_rejected_artifacts (
            id INTEGER PRIMARY KEY, source_job_id TEXT, job_detail_version_id INTEGER,
            prompt_version TEXT, original_artifact_id INTEGER
        );
        INSERT INTO job_analysis_attempts VALUES
            (1, 1, 'job-analysis-english-v30', 'failed', NULL, 'SafeFailure');
        INSERT INTO job_analysis_artifacts VALUES (2, 1, 'job-analysis-original-v9', 'accepted');
        """
    )
    baseline = script["baseline_for_job"](connection, "job-1", 1)
    assert baseline["v30"]["status"] == "failed_no_artifact"
    assert baseline["v9"]["status"] == "artifact_present_accepted"
    connection.close()


def test_baseline_reader_does_not_count_rejected_v30_as_valid_artifact():
    script = runpy.run_path(str(ROOT / "scripts/run_p16_b4_job_understanding.py"))
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.executescript(
        """
        CREATE TABLE job_analysis_attempts (
            id INTEGER PRIMARY KEY, job_detail_version_id INTEGER, prompt_version TEXT,
            outcome TEXT, artifact_id INTEGER, error_type TEXT
        );
        CREATE TABLE job_analysis_artifacts (
            id INTEGER PRIMARY KEY, job_detail_version_id INTEGER, prompt_version TEXT,
            semantic_review_status TEXT
        );
        CREATE TABLE job_analysis_rejected_artifacts (
            id INTEGER PRIMARY KEY, source_job_id TEXT, job_detail_version_id INTEGER,
            prompt_version TEXT, original_artifact_id INTEGER
        );
        INSERT INTO job_analysis_attempts VALUES
            (1, 1, 'job-analysis-english-v30', 'completed', NULL, NULL);
        INSERT INTO job_analysis_rejected_artifacts VALUES
            (3, 'job-1', 1, 'job-analysis-english-v30', NULL);
        """
    )
    baseline = script["baseline_for_job"](connection, "job-1", 1)
    assert baseline["v30"]["status"] == "rejected_candidate_no_valid_artifact"
    assert baseline["v30"]["valid_artifact_ids"] == []
    connection.close()


def test_b4_model_payload_uses_reviewed_translation_not_raw_original_or_board_metadata():
    from jobhunter.source_job_understanding_b4 import build_b4_model_payload

    evidence = evidence_fixture()
    evidence["items"][0]["original_text"] = "PRIVATE ORIGINAL SOURCE TEXT"
    evidence["board_values"] = [{"value": "BOARD-ONLY-VALUE"}]
    payload = build_b4_model_payload(evidence)
    serialized = json.dumps(payload, ensure_ascii=False)
    assert "PRIVATE ORIGINAL SOURCE TEXT" not in serialized
    assert "BOARD-ONLY-VALUE" not in serialized
    assert payload["source_items"][0]["text"] == "Develop and maintain security tooling"


def test_native_response_extractor_uses_only_final_message_content():
    script = runpy.run_path(str(ROOT / "scripts/run_p16_b4_job_understanding.py"))
    response = {
        "output": [
            {"type": "reasoning", "content": "ignored non-final channel"},
            {"type": "message", "content": '{"role_summary": {}}'},
        ],
        "reasoning_content": "ignored non-final payload",
    }
    answer, count = script["extract_final_message"](response)
    assert answer == '{"role_summary": {}}'
    assert count == 1
    metadata = script["response_metadata"](
        model="local-test",
        status_code=200,
        answer=answer,
        message_count=count,
        response_sha="a" * 64,
    )
    assert metadata["reasoning_content_persisted"] is False
    assert "reasoning_content" not in metadata
    assert "ignored non-final payload" not in json.dumps(metadata)


def test_native_model_preflight_requires_loaded_model_and_reasoning_off():
    script = runpy.run_path(str(ROOT / "scripts/run_p16_b4_job_understanding.py"))

    class FakeResponse:
        status = 200

        def __init__(self, payload):
            self.payload = json.dumps(payload).encode()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return self.payload

    class FakeOpener:
        def __init__(self, payload):
            self.payload = payload

        def open(self, request, timeout):
            return FakeResponse(self.payload)

    payload = {
        "models": [
            {
                "key": "local-model",
                "loaded_instances": [{"config": {"context_length": 4096}}],
                "capabilities": {"reasoning": {"allowed_options": ["off", "on"], "default": "on"}},
            }
        ]
    }
    result = script["native_preflight"](
        FakeOpener(payload), "http://127.0.0.1:18080", "local-model"
    )
    assert result["context_length"] == 4096
    assert "off" in result["reasoning_allowed_options"]
    payload["models"][0]["loaded_instances"] = []
    with pytest.raises(Exception, match="configured_model_not_loaded"):
        script["native_preflight"](FakeOpener(payload), "http://127.0.0.1:18080", "local-model")


def test_source_only_brief_uses_exact_translated_items_without_inventing_duties():
    from jobhunter.source_job_understanding_b4 import build_source_only_brief

    evidence = evidence_fixture()
    evidence["items"] = [
        item for item in evidence["items"] if item["category_candidate"] != "work_duty"
    ]
    brief = build_source_only_brief(evidence)
    assert brief["duty_candidate_count"] == 0
    assert brief["qualifications_only_possible"] is True
    assert brief["category_groups"]["candidate_qualification"][0]["source_item_id"] == "req-1"
    assert (
        brief["category_groups"]["candidate_qualification"][0]["translation_candidate"]
        == "Experience with Python"
    )
    assert brief["downstream_authority"] == "none"


def test_b4_brief_renderer_escapes_untrusted_source_text():
    script = runpy.run_path(str(ROOT / "scripts/run_p16_b4_job_understanding.py"))
    escape = script["safe_markdown_text"]
    assert "<script>" not in escape("<script>alert('x')</script>")
    assert "&lt;script&gt;" in escape("<script>alert('x')</script>")
    assert escape("[fake](http://bad)") != "[fake](http://bad)"


def test_filter_quarantines_misclassified_arrangements_without_losing_valid_work():
    from jobhunter.source_job_understanding_b4 import filter_b4_model_fragments

    evidence = evidence_fixture()
    response = valid_response()
    response["expectation_summaries"].append(
        {"summary": "Remote work is possible.", "source_item_ids": ["I04"]}
    )
    response["work_implied_capabilities"].append(
        {
            "capability": "Knowledge of Python",
            "rationale": "A qualification is not automatically an implied work duty.",
            "source_item_ids": ["I02"],
        }
    )
    filtered, audit = filter_b4_model_fragments(response, evidence)
    assert audit["dropped_fragment_count"] == 2
    assert {row["section"] for row in audit["dropped_fragments"]} == {
        "expectation_summaries",
        "work_implied_capabilities",
    }
    assert len(filtered["work_activities"]) == 1
    assert len(filtered["expectation_summaries"]) == 1
    assert len(filtered["work_implied_capabilities"]) == 1
    validated = validate_b4_model_response(filtered, evidence)
    assert validated["work_activities"][0]["source_item_ids"] == ["duty-1"]
    assert validated["work_implied_capabilities"][0]["source_item_ids"] == ["duty-1"]
    assert validated["source_reference_state"] == "canonical_source_item_ids_resolved"


def test_standalone_comparison_backup_includes_committed_wal_rows(tmp_path):
    script = runpy.run_path(str(ROOT / "scripts/run_p16_b4_job_understanding.py"))
    database = tmp_path / "comparison.sqlite3"
    connection = sqlite3.connect(database)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("CREATE TABLE evidence (source_id TEXT PRIMARY KEY)")
    connection.execute("INSERT INTO evidence VALUES ('source-1')")
    connection.commit()
    connection.close()
    script["make_standalone_comparison_database"](database)
    with sqlite3.connect(database) as restored:
        assert restored.execute("SELECT source_id FROM evidence").fetchall() == [("source-1",)]
        assert restored.execute("PRAGMA journal_mode").fetchone()[0] == "delete"
        assert restored.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert not Path(str(database) + "-wal").exists()
    assert not Path(str(database) + "-shm").exists()
