#!/usr/bin/env python3
"""Select the single reviewed B3 corrective candidate and reconcile private outputs."""

from __future__ import annotations

import hashlib
import json
import runpy
import sqlite3
import tempfile
from pathlib import Path
from typing import Any

from jobhunter.source_bound_translation_b3 import (
    build_translation_review_flags,
    make_b1_source_bound_alignment,
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
JOB = "tMjm"
ANCHOR = "beeca48335d4bd92df06c563ff3593278b8c72c2960583169a7a6d0ec2be8062"
ITEM_ID = "s_beeca48335d4bd92df06c563ff3593278b8c72c2"
SELECTED_TEXT = "Organized, conscientious, responsible, and committed"


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    private_path = OUT / "PRIVATE_B3_CANDIDATES.json"
    b1_path = OUT / "B1_COMPATIBLE_DRAFTS.json"
    safe_path = OUT / "SAFE_B3_METRICS.json"
    audit_path = OUT / "B3_MECHANICAL_AUDIT.json"
    flags_path = OUT / "B3_REVIEW_FLAG_REASSESSMENT.json"
    corrective_path = OUT / "B3_CORRECTIVE_CANDIDATE.json"
    semantic_path = OUT / "B3_SEMANTIC_REVIEW.json"
    raw_index_path = OUT / "RAW_CAPTURE_INDEX.json"
    if semantic_path.exists():
        raise ValueError("B3 semantic reconciliation already exists; refusing to apply twice")

    safe = json.loads(safe_path.read_text(encoding="utf-8"))
    private = json.loads(private_path.read_text(encoding="utf-8"))
    b1 = json.loads(b1_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    flag_review = json.loads(flags_path.read_text(encoding="utf-8"))
    correction = json.loads(corrective_path.read_text(encoding="utf-8"))
    manifest = json.loads((OUT / "run_manifest.json").read_text(encoding="utf-8"))

    if file_sha(B0) != safe["source_database_sha256"]:
        raise ValueError("Frozen B0 source database changed")
    if file_sha(B2 / "PRIVATE_B2_CANDIDATES.json") != safe["b2_private_candidate_sha256"]:
        raise ValueError("Private B2 candidate output changed")
    if correction["source_job_id"] != JOB or correction["source_anchor_id"] != ANCHOR:
        raise ValueError("Corrective candidate is not the predeclared conscientiousness item")
    if correction["request_count"] != 1 or correction["http_completion_attempt_count"] != 1:
        raise ValueError("Corrective candidate must contain exactly one generation attempt")
    if correction["provider_model"] != manifest["provider"]["model"]:
        raise ValueError("Corrective model differs from the frozen B3 provider")
    if correction["response_model"] != manifest["provider"]["model"]:
        raise ValueError("Corrective response model differs from the frozen B3 provider")
    if contains_persian(correction["target_text"]):
        raise ValueError("Corrective candidate unexpectedly contains Persian")
    if "duty-conscious" not in correction["target_text"].casefold():
        raise ValueError("Corrective candidate no longer contains the reviewed trait correction")
    if SELECTED_TEXT != "Organized, conscientious, responsible, and committed":
        raise AssertionError("Unexpected reviewer normalization")

    with tempfile.TemporaryDirectory(prefix="b3-corrective-source-") as temporary:
        copied = Path(temporary) / "source.sqlite3"
        with (
            sqlite3.connect("file:" + str(B0.resolve()) + "?mode=ro", uri=True) as source_db,
            sqlite3.connect(copied) as target_db,
        ):
            source_db.backup(target_db)
        store = TranslationStore(copied)
        source = store.latest_source_version(JOB)
        assert source is not None
        candidate = interpret_original_source_candidate(source)
        verify_b2_candidate(candidate, source)
        item = next(x for x in candidate.items if x.anchor.anchor_id == ANCHOR)
        if item.anchor.text_sha256 != correction["source_span_sha256"]:
            raise ValueError("Corrective candidate source span hash mismatch")
        if sha256_text(item.anchor.exact_text) != correction["source_span_sha256"]:
            raise ValueError("Corrective candidate does not match exact original source text")

    raw_event = correction["raw_http_events"][0]
    request_path = OUT / raw_event["raw_request_file"]
    response_path = OUT / raw_event["raw_response_file"]
    request_bytes = request_path.read_bytes()
    response_bytes = response_path.read_bytes()
    if sha256_bytes(request_bytes) != correction["request_body_sha256"]:
        raise ValueError("Corrective raw request hash mismatch")
    if sha256_bytes(response_bytes) != correction["response_body_sha256"]:
        raise ValueError("Corrective raw response hash mismatch")
    request = json.loads(request_bytes)
    assert "headers" not in request and "authorization" not in request
    messages = request["messages"]
    assert [message["role"] for message in messages] == ["system", "user"]
    assert sha256_text(messages[0]["content"]) == manifest["provider"]["system_prompt_sha256"]
    user_payload = json.loads(messages[1]["content"])
    assert user_payload["items"][0]["text"] == item.anchor.exact_text
    assert user_payload["correction_note"] == correction["correction_note"]
    response = json.loads(response_bytes)
    content = json.loads(response["choices"][0]["message"]["content"])
    assert content["translations"][0]["translation"].strip() == correction["target_text"]

    reviewer_normalization = {
        "applied": True,
        "kind": "terminology_normalization",
        "model_text": correction["target_text"],
        "selected_text": SELECTED_TEXT,
        "edit": "duty-conscious -> conscientious",
        "reason": (
            "Conscientious is the standard idiomatic English equivalent of Persian "
            "وظیفه‌شناس in this personal-trait list; the model's duty-conscious is "
            "understandable but less idiomatic."
        ),
    }
    corrective_prompt_version = (
        "lm-studio-translation-v2-system-sha256:"
        + correction["system_prompt_sha256"]
        + "+corrective-note-v1+assistant-terminology-normalization-v1"
    )
    item_record = next(
        row
        for row in private["items"]
        if row["source_job_id"] == JOB and row["source_anchor_id"] == ANCHOR
    )
    item_record["primary_translation_review"] = "material_mistranslation_superseded"
    item_record["corrective_candidate"] = {
        "candidate_kind": correction["candidate_kind"],
        "target_text": correction["target_text"],
        "target_sha256": correction["target_sha256"],
        "provider_name": correction["provider_name"],
        "provider_model": correction["provider_model"],
        "prompt_version": (
            "lm-studio-translation-v2-system-sha256:"
            + correction["system_prompt_sha256"]
            + "+corrective-note-v1"
        ),
        "request_body_sha256": correction["request_body_sha256"],
        "response_body_sha256": correction["response_body_sha256"],
        "corrective_prompt_sha256": correction["corrective_prompt_sha256"],
        "raw_http_events": correction["raw_http_events"],
        "meaning_review": "assistant_reviewed_semantically_acceptable",
    }
    item_record["selected_translation"] = {
        "candidate_kind": "corrective_candidate_with_reviewer_normalization",
        "target_text": SELECTED_TEXT,
        "target_sha256": sha256_text(SELECTED_TEXT),
        "provider_name": "lm-studio-translation-v2+assistant-review",
        "provider_model": correction["provider_model"],
        "prompt_version": corrective_prompt_version,
        "source_model_output_sha256": correction["target_sha256"],
        "reviewer_normalization": reviewer_normalization,
        "meaning_review": "assistant_reviewed_selected",
    }
    item_record["meaning_review"] = "assistant_reviewed_corrective_candidate_selected"
    item_record["review_flags_reassessed_v2"] = build_translation_review_flags(
        item.anchor.exact_text, item_record["target_text"]
    )
    item_record["selected_translation_review_flags_v2"] = build_translation_review_flags(
        item.anchor.exact_text, SELECTED_TEXT
    )

    private["semantic_review_authority"] = (
        "assistant_reviewed_exposed_cohort_with_one_corrective_candidate_selected"
    )
    private["corrective_candidate_count"] = 1
    private["selected_corrective_candidate_count"] = 1
    private["items"] = private["items"]
    write_json(private_path, private)

    correction["reviewer_normalized_target_text"] = SELECTED_TEXT
    correction["reviewer_normalized_target_sha256"] = sha256_text(SELECTED_TEXT)
    correction["reviewer_normalization"] = reviewer_normalization
    correction["meaning_review"] = "assistant_reviewed_selected_with_terminology_normalization"
    correction["selection_status"] = "selected_for_b1_candidate_alignment"
    write_json(corrective_path, correction)

    alignment = make_b1_source_bound_alignment(
        source_item_id=ITEM_ID,
        target_text=SELECTED_TEXT,
        provider_name="lm-studio-translation-v2+assistant-review",
        provider_model=correction["provider_model"],
        prompt_version=corrective_prompt_version,
    )
    existing = b1[JOB]["alignments"]
    positions = [i for i, row in enumerate(existing) if row["source_item_id"] == ITEM_ID]
    if len(positions) != 1:
        raise ValueError("Expected exactly one B1 alignment for the corrected source item")
    existing[positions[0]] = alignment
    validator = runpy.run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))["validate_bundle"]
    validator(b1[JOB], source=source)
    write_json(b1_path, b1)

    semantic = {
        "contract": "jobhunter-p16-b3-exposed-cohort-semantic-review-v1",
        "status": "PASS_BOUNDED_EXPOSED_COHORT_WITH_ONE_CORRECTIVE_SELECTED",
        "reviewer": "assistant_exposed_cohort_semantic_review",
        "reviewed_persian_translation_count": 63,
        "native_identity_count": 1,
        "material_primary_translation_issue_count": 1,
        "corrective_candidate_count": 1,
        "selected_corrective_candidate_count": 1,
        "unresolved_translation_count": 0,
        "independent_holdout_count": 0,
        "unseen_generalization_established": False,
        "per_job_reviewed": {
            job_id: sum(row["source_job_id"] == job_id for row in private["items"])
            for job_id in ("tNhZ", "tMps", "tNDx", "tMjm")
        },
        "critical_semantic_checks": {
            "tNhZ_llm_familiarity_remains_preferred_not_mandatory": "PASS",
            "tNhZ_arrangements_and_remote_context_preserved": "PASS",
            "tMps_middle_senior_alternatives_remain_in_source_graph": "PASS",
            "tMps_one_of_domain_and_certificate_equivalence_preserved": "PASS",
            "tNDx_teamwork_remains_preferred": "PASS",
            "tNDx_kaspersky_and_customer_experience_strength_not_upgraded": "PASS",
            "tNDx_technical_entrance_exam_condition_translated": "PASS",
            "tMjm_conscientiousness_primary_mistranslation_corrected": "PASS",
            "tMjm_zero_work_duty_fabrication_preserved": "PASS",
            "headings_not_sent_as_translation_content": "PASS",
            "exact_source_anchor_identity_preserved": "PASS",
        },
        "selected_correction": {
            "source_job_id": JOB,
            "source_item_id": ITEM_ID,
            "primary_translation_sha256": item_record["target_sha256"],
            "corrective_model_output_sha256": correction["target_sha256"],
            "selected_target_sha256": sha256_text(SELECTED_TEXT),
            "reviewer_normalization": reviewer_normalization,
        },
        "minor_fluency_observations": [
            (
                "Some source list items remain grammatically literal where the Persian original "
                "is itself compressed or unpunctuated."
            ),
            (
                "These are fluency observations, not identified changes to mandatory/preferred "
                "strength, alternatives, numbers, or role meaning."
            ),
        ],
        "authority": {
            "candidate_only": True,
            "accepted_employer_facts_promoted": 0,
            "production_route_changed": False,
            "downstream_authority": "none",
        },
        "limitations": [
            "The four ads are previously exposed development cases, not a holdout.",
            "This review is not an independent accuracy or unseen-generalization claim.",
            (
                "Twelve nested eligibility leaves retain source identity but have no separate "
                "target subspan offsets."
            ),
            (
                "Candidate categories and employer-strength labels remain unreviewed as facts; "
                "their B2 uncertainty is preserved."
            ),
        ],
    }
    write_json(semantic_path, semantic)

    flag_review["corrective_candidate_selected"] = True
    flag_review["corrective_candidate_sha256"] = file_sha(corrective_path)
    flag_review["selected_target_sha256"] = sha256_text(SELECTED_TEXT)
    flag_review["selected_target_flags_v2"] = build_translation_review_flags(
        item.anchor.exact_text, SELECTED_TEXT
    )
    flag_review["primary_material_mistranslation_superseded"] = True
    write_json(flags_path, flag_review)

    checkpoint = (OUT / "checkpoint.jsonl").read_text(encoding="utf-8").splitlines()
    raw_index = json.loads(raw_index_path.read_text(encoding="utf-8"))
    raw_index["corrective_events"] = correction["raw_http_events"]
    raw_index["corrective_preflight_http_request_count"] = correction[
        "preflight_http_request_count"
    ]
    write_json(raw_index_path, raw_index)

    audit["primary_model_completion_attempt_count"] = 63
    audit["corrective_model_completion_attempt_count"] = 1
    audit["model_completion_attempt_count"] = 64
    audit["source_bound_generation_request_count"] = 64
    audit["corrective_candidate_count"] = 1
    audit["corrective_candidate_selected_count"] = 1
    audit["request_response_candidate_match_count"] = 64
    audit["corrective_source_item_id"] = ITEM_ID
    audit["corrective_target_sha256"] = correction["target_sha256"]
    audit["selected_target_sha256"] = sha256_text(SELECTED_TEXT)
    audit["reviewer_normalization_applied"] = True
    audit["unresolved_count"] = 0
    for row in audit["items"]:
        if row["job"] == JOB and row["anchor_id"] == ANCHOR:
            row["primary_translation_review"] = "material_mistranslation_superseded"
            row["corrective_candidate_selected"] = True
            row["corrective_target_sha256"] = correction["target_sha256"]
            row["selected_target_sha256"] = sha256_text(SELECTED_TEXT)
    write_json(audit_path, audit)

    safe = json.loads((OUT / "SAFE_B3_METRICS.json").read_text(encoding="utf-8"))
    safe["limits"]["planned_corrective_candidate_count"] = 0
    safe["limits"]["corrective_candidate_budget"] = 1
    safe["limits"]["corrective_candidate_count_actual"] = 1
    aggregate = safe["aggregate"]
    aggregate["corrective_candidate_count"] = 1
    aggregate["corrective_model_request_count"] = 1
    aggregate["corrective_preflight_http_request_count"] = correction[
        "preflight_http_request_count"
    ]
    aggregate["total_source_bound_generation_requests"] = 64
    aggregate["http_completion_attempt_count"] = 64
    aggregate["prompt_tokens"] = 18_462
    aggregate["completion_tokens"] = 24_496
    aggregate["corrective_prompt_tokens"] = correction["usage"].get("prompt_tokens")
    aggregate["corrective_completion_tokens"] = correction["usage"].get("completion_tokens")
    aggregate["corrective_request_started"] = 1
    aggregate["corrective_request_terminal"] = 1
    aggregate["unresolved_count"] = 0
    safe["run_status"] = "completed_with_one_corrective_candidate_selected"
    safe["meaning_review_state"] = "assistant_reviewed_exposed_cohort_with_one_corrective_selected"
    safe["private_candidate_output_sha256"] = file_sha(private_path)
    safe["b1_compatible_drafts_sha256"] = file_sha(b1_path)
    safe["checkpoint_sha256"] = file_sha(OUT / "checkpoint.jsonl")
    safe["raw_capture_index_sha256"] = file_sha(raw_index_path)
    safe["corrective_candidate_sha256"] = file_sha(corrective_path)
    safe["semantic_review_sha256"] = file_sha(semantic_path)
    safe["review_flag_reassessment_sha256"] = file_sha(flags_path)
    safe["mechanical_audit_sha256"] = file_sha(audit_path)
    safe["per_job"][JOB]["corrective_candidate_count"] = 1
    safe["b1_bundle_validation"][JOB] = "PASS_AFTER_CORRECTIVE_SELECTION"
    write_json(safe_path, safe)

    if file_sha(B0) != safe["source_database_sha256"]:
        raise ValueError("B0 source DB changed during corrective reconciliation")
    if file_sha(B2 / "PRIVATE_B2_CANDIDATES.json") != safe["b2_private_candidate_sha256"]:
        raise ValueError("B2 private candidate input changed during corrective reconciliation")

    print(
        json.dumps(
            {
                "status": semantic["status"],
                "corrective_candidate_count": 1,
                "selected_target_sha256": sha256_text(SELECTED_TEXT),
                "b1_validation": "PASS",
                "safe_metrics_sha256": file_sha(safe_path),
                "semantic_review_sha256": file_sha(semantic_path),
                "checkpoint_lines": len(checkpoint),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
