#!/usr/bin/env python3
"""Read-only seal verifier for exposed LM Studio source-bound translation batching.

Never reissues requests, mutates old candidate artifacts, or treats successful
ID association as independent linguistic fidelity. Pilot results are private.
"""

from __future__ import annotations

import hashlib
import json
import runpy
from pathlib import Path

from jobhunter.source_bound_translation_b1_alignment_b5 import align_batch_result_to_b1
from jobhunter.source_bound_translation_b3 import select_b3_items
from jobhunter.source_bound_translation_batch_b5 import (
    B5_BATCH_CANDIDATE_VERSION,
    plan_source_batches,
    prepare_source_batch_items,
)
from jobhunter.source_item_candidate_b2_v2 import interpret_original_source_candidate_v2
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"
PILOT = BASE / "batch-pilot-v1"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError(f"Expected JSON object: {path.name}")
    return obj


def verify() -> dict:
    preflight = runpy.run_path(str(ROOT / "scripts/verify_p16_b5_translation_batch_preflight.py"))[
        "verify"
    ]()
    if preflight["status"] != "PASS_OFFLINE_BATCH_PREFLIGHT_REPLAY_NOT_MODEL_QUALITY":
        raise ValueError("Frozen offline batch planning failed its replay")

    scope = read(PILOT / "FROZEN_SCOPE.json")
    pilot = read(PILOT / "PRIVATE_RESULT.json")
    source = read(BASE / "B5_SELECTION_FROZEN.json")
    snapshot = BASE / "B5_8_SOURCE_SNAPSHOT.sqlite3"
    if (
        scope["contract"] != "p16-b5-exposed-local-translation-batch-pilot-v1"
        or scope["source_cohort"] != "previously_exposed_eight_development_jobs"
        or scope["model"] != "gemma-4-e2b-it"
        or scope["endpoint"] != "http://127.0.0.1:18080/v1"
        or scope["planned_invocations"] != 3
        or scope["max_physical_http_completion_attempts"] != 4
        or pilot["frozen_scope_sha256"] != sha(PILOT / "FROZEN_SCOPE.json")
        or scope["preflight_sha256"] != sha(BASE / "B5_TRANSLATION_BATCH_PREFLIGHT.json")
        or scope["original_snapshot_sha256"] != sha(snapshot)
        or scope["batch_code_sha256"]
        != sha(ROOT / "src/jobhunter/source_bound_translation_batch_b5.py")
        or scope["production_db_sha256"] != sha(ROOT / "data/jobhunter.sqlite3")
        or scope["corpus_sha256"] != sha(ROOT / "corpus/manifest.json")
    ):
        raise ValueError("Frozen scope, local-only boundary, or dependencies drifted")
    store = TranslationStore(snapshot)
    prepared = []
    for member in source["selected_primary"]:
        job_id = member["source_job_id"]
        original = store.latest_source_version(job_id)
        if original is None:
            raise ValueError("Original B5 job no longer available")
        b2v2 = interpret_original_source_candidate_v2(original)
        b3 = select_b3_items(job_id, b2v2.items)
        prepared.extend(prepare_source_batch_items(original, b3.translate_items))
    batches = plan_source_batches(prepared, max_batch_items=3)
    matched = [batch for batch in batches.batches if batch.batch_id == scope["batch_id"]]
    if len(matched) != 1:
        raise ValueError("Frozen source-owned batch not found in original plan")
    batch = matched[0]
    if (
        len(batch.items) != 2
        or scope["source_anchors"] != [x.source_anchor_id for x in batch.items]
        or scope["source_hashes"] != [x.source_span_sha256 for x in batch.items]
        or any(
            x.category != "candidate_qualification" or x.strength != "preferred"
            for x in batch.items
        )
    ):
        raise ValueError("Pilot source-type/optional modality changed")

    outputs = pilot["source_bound_candidate_outputs"]
    events = pilot["http_records"]
    if [x["stage"] for x in outputs] != ["batch", "single_0", "single_1"]:
        raise ValueError("Pilot did not finish three predeclared local invocations")
    if len(events) != pilot["physical_http_completion_attempts"]:
        raise ValueError("Physical HTTP events missing in pilot evidence")
    if pilot["physical_http_completion_attempts"] > scope["max_physical_http_completion_attempts"]:
        raise ValueError("Pilot exceeded physical request budget")
    if pilot["logical_invocations"] != len(outputs) or pilot["logical_invocations"] != 3:
        raise ValueError("Logical invocation count changed")

    for event in events:
        if (
            event["path"] != "/v1/chat/completions"
            or event["status"] != 200
            or event["error_type"] is not None
        ):
            raise ValueError("Unverified endpoint, HTTP failure or unsafe origin")
        request = PILOT / event["private_request_path"]
        response = PILOT / event["private_response_path"]
        if (
            not request.is_relative_to(PILOT)
            or not response.is_relative_to(PILOT)
            or sha(request) != event["request_sha256"]
            or sha(response) != event["response_sha256"]
        ):
            raise ValueError("Pilot request or response receipt drifted")
        submitted = read(request)
        if (
            submitted["model"] != scope["model"]
            or submitted["temperature"] != 0
            or submitted["response_format"]["type"] != "json_schema"
            or submitted["stream"] is not False
        ):
            raise ValueError("Prompt/model contract differs from frozen pilot")

    batch_result = outputs[0]["result"]
    if (
        outputs[0]["state"] != "returned"
        or batch_result["contract"] != B5_BATCH_CANDIDATE_VERSION
        or batch_result["batch_request_state"] != "completed"
        or batch_result["source_item_associations_verified"] is not True
        or batch_result["logical_source_items_attempted"] != 2
    ):
        raise ValueError("Batch translation source association was not established")
    entries = batch_result["items"]
    if len(entries) != 2:
        raise ValueError("Two-member batch output changed")
    # Reconstruct source-owned B1 identities from the original frozen source,
    # not from provider-returned order or generated content IDs.
    original = store.latest_source_version(batch.source_job_id)
    if original is None:
        raise ValueError("B1 source version not available")
    candidate = interpret_original_source_candidate_v2(original)
    b1_bundle = runpy.run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))[
        "b1_design_from_b2"
    ](candidate, original)
    runpy.run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))["validate_bundle"](
        b1_bundle, source=original
    )
    aligned = align_batch_result_to_b1(b1_bundle, batch, batch_result)
    if (
        len(aligned) != 2
        or any(x["state"] != "source_bound_translation_candidate" for x in aligned)
        or len({x["source_item_id"] for x in aligned}) != 2
        or b1_bundle["brief"]["downstream_authority"] != "none"
    ):
        raise ValueError("Bounded batch failed B1 item ownership or authority check")
    equal_texts = 0
    approved_cue_state = []
    for i, original in enumerate(batch.items):
        candidate = entries[i]
        individual = outputs[i + 1]["result"]
        if (
            candidate["source_anchor_id"] != original.source_anchor_id
            or candidate["source_span_sha256"] != original.source_span_sha256
            or candidate["source_strength_candidate"] != "preferred"
            or candidate["state"] != "source_bound_translation_candidate"
            or individual["source_span_sha256"] != original.source_span_sha256
            or outputs[i + 1]["state"] != "returned"
            or candidate["meaning_review"] != "unreviewed"
            or candidate["target_semantic_fidelity"] != "not_established"
        ):
            raise ValueError("Bound per-item source provenance or review authority changed")
        if candidate["target_text"] == individual["target_text"]:
            equal_texts += 1
        if (
            not candidate["target_text"]
            or not candidate["target_sha256"]
            or hashlib.sha256(candidate["target_text"].encode()).hexdigest()
            != candidate["target_sha256"]
        ):
            raise ValueError("Missing target hash or text")
        approved_cue_state.append(
            {
                "candidate_optional_strength_preserved_in_structured_sidecar": True,
                "standalone_english_text_can_prove_source_heading_modality": False,
            }
        )
    if pilot["accepted_employer_facts"] != 0 or pilot["production_database_unchanged"] is not True:
        raise ValueError("Pilot improperly promoted translated employer facts")
    review = read(PILOT / "PRIVATE_ASSISTANT_TRANSLATION_REVIEW.json")
    if (
        review["frozen_scope_sha256"] != sha(PILOT / "FROZEN_SCOPE.json")
        or review["original_pilot_result_sha256"] != sha(PILOT / "PRIVATE_RESULT.json")
        or review["source_review"] != "assistant_exposed_case_review_not_independent_blind"
        or review["preferred_heading_context_carried_into_english_target_text"] is not False
        or review["preferred_strength_retained_in_source_bound_sidecar"] is not True
        or review["new_unseen_B5_pass"] is not False
        or review["accepted_employer_facts"] != 0
        or len(review["checks"]) != 2
    ):
        raise ValueError("Pilot assistant-review authority or warning changed")
    for index, check in enumerate(review["checks"]):
        if (
            check["item_index"] != index
            or check["source_anchor_id"] != batch.items[index].source_anchor_id
            or check["source_span_sha256"] != batch.items[index].source_span_sha256
            or check["batch_target_sha256"] != entries[index]["target_sha256"]
            or check["single_target_sha256"] != outputs[index + 1]["result"]["target_sha256"]
            or check["original_source_strength_candidate"] != "preferred"
            or check["translation_meaning_supported"] is not True
        ):
            raise ValueError("Reviewed translation no longer matches frozen source and output")
    return {
        "status": "PASS_EXPOSED_BATCH_ASSOCIATION_PILOT_NO_SEMANTIC_GENERALIZATION",
        "pilot_original_source_items": 2,
        "batch_model_calls": 1,
        "single_item_control_calls": 2,
        "physical_http_completion_attempts": len(events),
        "batch_and_single_target_texts_exactly_equal": equal_texts,
        "local_model_responses_http_200": len(events),
        "successful_source_bound_target_items": 2,
        "explicit_preferred_strength_carried_in_source_metadata": 2,
        "B1_candidate_alignment_source_ids_replayed": len(aligned),
        "B1_downstream_authority": "none",
        "standalone_translation_preserves_preferred_section_context": "not_established",
        "independent_blind_linguistic_review": False,
        "assistant_exposed_item_meaning_review": "two_items_supported_with_scope_limitations",
        "private_semantic_review_sha256": sha(PILOT / "PRIVATE_ASSISTANT_TRANSLATION_REVIEW.json"),
        "correctness_on_unseen_sources": "not_established",
        "production_state_unchanged": True,
        "B5_B6_promotion": "not_authorized",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
