#!/usr/bin/env python3
"""Revalidate the complete private B3 translation run without emitting source text."""

from __future__ import annotations

import hashlib
import json
import runpy
import sqlite3
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

from jobhunter.source_bound_translation_b3 import (
    build_translation_review_flags,
    sha256_bytes,
    sha256_text,
)
from jobhunter.source_item_candidate_b2 import (
    interpret_original_source_candidate,
    verify_b2_candidate,
)
from jobhunter.translation.projection import contains_persian
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/local-acceptance/p16-stage-b3-2026-11-18/primary-v1"
B0 = ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
B2 = ROOT / "data/local-acceptance/p16-stage-b2-2026-11-17/b2-candidate-acceptance-v5"
COHORT = ("tNhZ", "tMps", "tNDx", "tMjm")
CORRECTED_JOB = "tMjm"
CORRECTED_ANCHOR = "beeca48335d4bd92df06c563ff3593278b8c72c2960583169a7a6d0ec2be8062"
SELECTED_TARGET = "Organized, conscientious, responsible, and committed"


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    manifest = read_json(OUT / "run_manifest.json")
    safe = read_json(OUT / "SAFE_B3_METRICS.json")
    private = read_json(OUT / "PRIVATE_B3_CANDIDATES.json")
    corrective = read_json(OUT / "B3_CORRECTIVE_CANDIDATE.json")
    semantic = read_json(OUT / "B3_SEMANTIC_REVIEW.json")
    flags = read_json(OUT / "B3_REVIEW_FLAG_REASSESSMENT.json")
    audit = read_json(OUT / "B3_MECHANICAL_AUDIT.json")
    assert audit["status"] == "PASS"
    assert audit["model_completion_attempt_count"] == 64
    b1 = read_json(OUT / "B1_COMPATIBLE_DRAFTS.json")
    raw_index = read_json(OUT / "RAW_CAPTURE_INDEX.json")
    b1_validate = runpy.run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))[
        "validate_bundle"
    ]

    assert file_sha(B0) == manifest["source_database_sha256"]
    assert file_sha(B2 / "PRIVATE_B2_CANDIDATES.json") == manifest["b2_private_candidate_sha256"]
    assert (
        file_sha(ROOT / "scripts/run_p16_b3_source_bound_translation.py")
        == manifest["b3_code_fingerprints"]["runner_sha256"]
    )
    assert (
        file_sha(ROOT / "src/jobhunter/source_bound_translation_b3.py")
        == flags["reassessment_support_module_sha256"]
    )
    assert (
        flags["run_time_support_module_sha256"]
        == manifest["b3_code_fingerprints"]["support_module_sha256"]
    )

    contexts = {}
    with tempfile.TemporaryDirectory(prefix="b3-final-audit-") as temporary:
        copied = Path(temporary) / "source.sqlite3"
        with (
            sqlite3.connect("file:" + str(B0.resolve()) + "?mode=ro", uri=True) as source_db,
            sqlite3.connect(copied) as target_db,
        ):
            source_db.backup(target_db)
        store = TranslationStore(copied)
        for job in COHORT:
            source = store.latest_source_version(job)
            assert source is not None
            candidate = interpret_original_source_candidate(source)
            verify_b2_candidate(candidate, source)
            contexts[job] = (source, {item.anchor.anchor_id: item for item in candidate.items})

    records = private["items"]
    assert len(records) == 64
    assert len({(row["source_job_id"], row["source_anchor_id"]) for row in records}) == 64
    assert sum(row["state"] == "native_identity" for row in records) == 1
    assert sum(row["state"] == "source_bound_translation_candidate" for row in records) == 63
    assert sum(row["state"] == "unresolved" for row in records) == 0

    primary_tokens = Counter()
    flag_counts_v2 = Counter()
    exact_primary_requests = 0
    primary_http_attempts = 0
    for row in records:
        job = row["source_job_id"]
        item = contexts[job][1][row["source_anchor_id"]]
        anchor = item.anchor
        assert row["source_item_id"] == "s_" + anchor.anchor_id[:40]
        assert row["source_span_sha256"] == anchor.text_sha256
        assert row["source_char_start"] == anchor.char_start
        assert row["source_char_end"] == anchor.char_end

        if row["state"] == "native_identity":
            assert row["target_text"] == anchor.exact_text
            assert row["target_sha256"] == anchor.text_sha256
            assert row["model_request_count"] == 0
            continue

        assert row["target_text"] and not contains_persian(row["target_text"])
        assert row["target_sha256"] == sha256_text(row["target_text"])
        assert row["provider_model"] == "gemma-4-e2b-it"
        assert row["response_model"] == "gemma-4-e2b-it"
        assert row["model_request_count"] == 1
        assert row["http_completion_attempt_count"] == 1
        assert row["response_schema_sha256"]
        assert row["meaning_review"] in {
            "unreviewed",
            "assistant_reviewed_corrective_candidate_selected",
        }
        event = row["raw_http_events"][-1]
        request_bytes = (OUT / event["raw_request_file"]).read_bytes()
        response_bytes = (OUT / event["raw_response_file"]).read_bytes()
        assert sha256_bytes(request_bytes) == event["request_body_sha256"]
        assert sha256_bytes(response_bytes) == event["response_body_sha256"]
        request = json.loads(request_bytes)
        assert "headers" not in request and "authorization" not in request
        assert request["model"] == "gemma-4-e2b-it"
        assert request["temperature"] == 0 and request["seed"] == 0
        assert request["response_format"]["json_schema"]["name"] == "jobhunter_translation_batch_v2"
        messages = request["messages"]
        assert [message["role"] for message in messages] == ["system", "user"]
        assert sha256_text(messages[0]["content"]) == manifest["provider"]["system_prompt_sha256"]
        user = json.loads(messages[1]["content"])
        assert set(user) == {"source_language", "target_language", "items"}
        assert user["source_language"] == "fa" and user["target_language"] == "en"
        assert len(user["items"]) == 1 and set(user["items"][0]) == {"id", "text"}
        assert user["items"][0]["text"] == anchor.exact_text
        content_id = user["items"][0]["id"]
        response = json.loads(response_bytes)
        assert response["model"] == "gemma-4-e2b-it"
        assert response["choices"][0]["finish_reason"] == "stop"
        content = json.loads(response["choices"][0]["message"]["content"])
        assert len(content["translations"]) == 1
        assert content["translations"][0]["id"] == content_id
        assert content["translations"][0]["translation"].strip() == row["target_text"]
        exact_primary_requests += 1
        primary_http_attempts += row["http_completion_attempt_count"]
        usage = row.get("usage") or {}
        primary_tokens["prompt"] += usage.get("prompt_tokens") or 0
        primary_tokens["completion"] += usage.get("completion_tokens") or 0
        flag_counts_v2.update(build_translation_review_flags(anchor.exact_text, row["target_text"]))

    corrected_row = next(
        row
        for row in records
        if row["source_job_id"] == CORRECTED_JOB and row["source_anchor_id"] == CORRECTED_ANCHOR
    )
    assert corrected_row["primary_translation_review"] == "material_mistranslation_superseded"
    selected = corrected_row["selected_translation"]
    assert selected["target_text"] == SELECTED_TARGET
    assert selected["target_sha256"] == sha256_text(SELECTED_TARGET)
    assert selected["reviewer_normalization"]["applied"] is True
    assert corrected_row["selected_translation_review_flags_v2"] == []

    assert corrective["request_count"] == 1
    assert corrective["http_completion_attempt_count"] == 1
    assert corrective["provider_model"] == "gemma-4-e2b-it"
    assert corrective["response_model"] == "gemma-4-e2b-it"
    assert corrective["target_text"] == "Organized, duty-conscious, responsible, and committed"
    assert corrective["reviewer_normalized_target_text"] == SELECTED_TARGET
    assert corrective["reviewer_normalized_target_sha256"] == sha256_text(SELECTED_TARGET)
    corr_event = corrective["raw_http_events"][0]
    corr_request_bytes = (OUT / corr_event["raw_request_file"]).read_bytes()
    corr_response_bytes = (OUT / corr_event["raw_response_file"]).read_bytes()
    assert sha256_bytes(corr_request_bytes) == corrective["request_body_sha256"]
    assert sha256_bytes(corr_response_bytes) == corrective["response_body_sha256"]
    corr_request = json.loads(corr_request_bytes)
    assert "headers" not in corr_request and "authorization" not in corr_request
    assert corr_request["model"] == "gemma-4-e2b-it"
    corr_user = json.loads(corr_request["messages"][1]["content"])
    assert set(corr_user) == {"source_language", "target_language", "items", "correction_note"}
    corr_source = contexts[CORRECTED_JOB][1][CORRECTED_ANCHOR].anchor.exact_text
    assert corr_user["items"][0]["text"] == corr_source
    assert corr_user["correction_note"] == corrective["correction_note"]
    corr_response = json.loads(corr_response_bytes)
    corr_content = json.loads(corr_response["choices"][0]["message"]["content"])
    assert corr_content["translations"][0]["translation"].strip() == corrective["target_text"]

    selected_alignment = next(
        row
        for row in b1[CORRECTED_JOB]["alignments"]
        if row["source_item_id"] == corrected_row["source_item_id"]
    )
    assert selected_alignment["translation_sha256"] == sha256_text(SELECTED_TARGET)
    assert selected_alignment["target"]["target_span"]["text_sha256"] == sha256_text(
        SELECTED_TARGET
    )
    assert "assistant-review" in selected_alignment["target"]["provider_name"]
    for job in COHORT:
        b1_validate(b1[job], source=contexts[job][0])

    checkpoint = [
        json.loads(line)
        for line in (OUT / "checkpoint.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert sum(row.get("event") == "request_started" for row in checkpoint) == 63
    assert (
        sum(
            row.get("event")
            in {"request_completed", "request_failed", "request_interrupted_unknown"}
            for row in checkpoint
        )
        == 63
    )
    assert sum(row.get("event") == "corrective_request_started" for row in checkpoint) == 1
    assert sum(row.get("event") == "corrective_request_completed" for row in checkpoint) == 1
    assert len(raw_index["corrective_events"]) == 1
    assert raw_index["authorization_headers_persisted"] is False

    assert safe["aggregate"]["candidate_record_count"] == 64
    assert safe["aggregate"]["translated_candidate_count"] == 63
    assert safe["aggregate"]["native_identity_count"] == 1
    assert safe["aggregate"]["unresolved_count"] == 0
    assert safe["aggregate"]["corrective_candidate_count"] == 1
    assert safe["aggregate"]["total_source_bound_generation_requests"] == 64
    assert safe["aggregate"]["http_completion_attempt_count"] == 64
    assert safe["aggregate"]["transport_retry_count"] == 0
    assert safe["aggregate"]["truncation_recovery_count"] == 0
    assert safe["aggregate"]["prompt_tokens"] == primary_tokens["prompt"] + (
        corrective["usage"].get("prompt_tokens") or 0
    )
    assert safe["aggregate"]["completion_tokens"] == primary_tokens["completion"] + (
        corrective["usage"].get("completion_tokens") or 0
    )
    assert safe["run_status"] == "completed_with_one_corrective_candidate_selected"
    assert safe["privacy"]["authorization_headers_persisted"] is False
    assert safe["privacy"]["accepted_facts_promoted"] == 0
    assert safe["privacy"]["production_database_written"] is False

    for filename, key in (
        ("PRIVATE_B3_CANDIDATES.json", "private_candidate_output_sha256"),
        ("B1_COMPATIBLE_DRAFTS.json", "b1_compatible_drafts_sha256"),
        ("checkpoint.jsonl", "checkpoint_sha256"),
        ("RAW_CAPTURE_INDEX.json", "raw_capture_index_sha256"),
    ):
        assert file_sha(OUT / filename) == safe[key]
    assert file_sha(OUT / "B3_CORRECTIVE_CANDIDATE.json") == safe["corrective_candidate_sha256"]
    assert file_sha(OUT / "B3_SEMANTIC_REVIEW.json") == safe["semantic_review_sha256"]
    assert (
        file_sha(OUT / "B3_REVIEW_FLAG_REASSESSMENT.json")
        == safe["review_flag_reassessment_sha256"]
    )
    assert file_sha(OUT / "B3_MECHANICAL_AUDIT.json") == safe["mechanical_audit_sha256"]

    safe_text = json.dumps(safe, ensure_ascii=False)
    assert "target_text" not in safe_text and "exact_text" not in safe_text
    assert "source_heading_context" not in safe_text

    final_audit = {
        "contract": "jobhunter-p16-b3-final-audit-v1",
        "status": "PASS",
        "source_database_sha256": file_sha(B0),
        "b2_private_candidate_sha256": file_sha(B2 / "PRIVATE_B2_CANDIDATES.json"),
        "run_manifest_sha256": file_sha(OUT / "run_manifest.json"),
        "private_candidate_output_sha256": file_sha(OUT / "PRIVATE_B3_CANDIDATES.json"),
        "corrective_candidate_sha256": file_sha(OUT / "B3_CORRECTIVE_CANDIDATE.json"),
        "selected_b1_drafts_sha256": file_sha(OUT / "B1_COMPATIBLE_DRAFTS.json"),
        "safe_metrics_sha256": file_sha(OUT / "SAFE_B3_METRICS.json"),
        "semantic_review_sha256": file_sha(OUT / "B3_SEMANTIC_REVIEW.json"),
        "review_flag_reassessment_sha256": file_sha(OUT / "B3_REVIEW_FLAG_REASSESSMENT.json"),
        "mechanical_audit_sha256": file_sha(OUT / "B3_MECHANICAL_AUDIT.json"),
        "selected_corrective_target_sha256": selected["target_sha256"],
        "reviewer_normalization_applied": selected["reviewer_normalization"]["applied"],
        "run_time_b3_runner_sha256": manifest["b3_code_fingerprints"]["runner_sha256"],
        "run_time_b3_support_module_sha256": manifest["b3_code_fingerprints"][
            "support_module_sha256"
        ],
        "reassessment_support_module_sha256": flags["reassessment_support_module_sha256"],
        "corrective_runner_sha256": file_sha(
            ROOT / "scripts/run_p16_b3_single_corrective_candidate.py"
        ),
        "reconciliation_script_sha256": file_sha(
            ROOT / "scripts/reconcile_p16_b3_corrective_selection.py"
        ),
        "validator_script_sha256": file_sha(ROOT / "scripts/validate_p16_b3_translation_run.py"),
        "source_items": 78,
        "primary_persian_translation_requests": exact_primary_requests,
        "corrective_translation_requests": 1,
        "total_generation_requests": primary_http_attempts + 1,
        "native_identity_items": 1,
        "unresolved_selected_translations": 0,
        "exact_source_only_primary_requests": exact_primary_requests,
        "corrective_exact_source_plus_note_requests": 1,
        "heading_context_sent_to_model": False,
        "request_response_hashes_verified": 64,
        "b1_bundles_validated": 4,
        "nested_eligibility_leaf_count": 12,
        "nested_leaf_target_offsets": "not_established",
        "reviewed_persian_translation_count": semantic["reviewed_persian_translation_count"],
        "material_primary_translation_issue_count": semantic[
            "material_primary_translation_issue_count"
        ],
        "corrective_candidate_selected_count": semantic["selected_corrective_candidate_count"],
        "review_flag_counts_after_rule_reassessment": dict(flag_counts_v2),
        "authorization_headers_persisted": False,
        "production_database_written": False,
        "accepted_facts_promoted": 0,
        "unseen_generalization_established": False,
    }
    final_path = OUT / "B3_FINAL_AUDIT.json"
    final_path.write_text(
        json.dumps(final_audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "primary_requests": exact_primary_requests,
                "corrective_requests": 1,
                "total_requests": primary_http_attempts + 1,
                "review_flags_v2": dict(flag_counts_v2),
                "final_audit_sha256": file_sha(final_path),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
