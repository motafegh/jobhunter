#!/usr/bin/env python3
"""Offline verifier for five preselected exposed local B5 budgeted batches.

Replays original source ownership and private HTTP receipts; does not infer
unseen B5 quality, send a request, or promote employer facts.
"""

from __future__ import annotations

import hashlib
import json
import runpy
from pathlib import Path

from jobhunter.source_bound_translation_budget_b5 import B5_PHYSICAL_BUDGET_CONTRACT

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"
PILOT = BASE / "budgeted-variety-pilot-v1"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Invalid B5 budget receipt: expected JSON object")
    return value


def verify() -> dict:
    historical = runpy.run_path(str(ROOT / "scripts/verify_p16_b5_translation_batch_preflight.py"))[
        "verify"
    ]()
    if historical["status"] != "PASS_OFFLINE_BATCH_PREFLIGHT_REPLAY_NOT_MODEL_QUALITY":
        raise ValueError("B5 exposed preflight regression failed")
    scope = read(PILOT / "FROZEN_SCOPE.json")
    result = read(PILOT / "PRIVATE_RESULT.json")
    review = read(PILOT / "SOURCE_FIRST_ASSISTANT_REVIEW.json")
    sources = (
        (PILOT / "SOURCE_FIRST_ASSISTANT_REVIEW.json", "source_first_review_sha256"),
        (BASE / "B5_8_SOURCE_SNAPSHOT.sqlite3", "original_snapshot_sha256"),
        (BASE / "B5_TRANSLATION_BATCH_PREFLIGHT.json", "previous_exposed_batch_preflight_sha256"),
        (ROOT / "src/jobhunter/source_item_candidate_b2_v2.py", "B2v2_source_sha256"),
        (
            ROOT / "src/jobhunter/source_bound_translation_batch_b5.py",
            "batch_planner_source_sha256",
        ),
        (
            ROOT / "src/jobhunter/source_bound_translation_budget_b5.py",
            "budget_guard_source_sha256",
        ),
        (ROOT / "scripts/pilot_p16_b5_budget_guard_v1.py", "pilot_script_sha256"),
        (ROOT / "data/jobhunter.sqlite3", "production_database_sha256"),
        (ROOT / "corpus/manifest.json", "public_corpus_sha256"),
    )
    if any(sha(path) != scope[field] for path, field in sources):
        raise ValueError("Pilot source, transport guard or production dependency drifted")
    if (
        scope["physical_attempt_guard_contract"] != B5_PHYSICAL_BUDGET_CONTRACT
        or scope["max_physical_http_attempts"] != 7
        or scope["max_wall_seconds"] != 240.0
        or scope["max_selected_logical_batches"] != 5
        or scope["selected_original_source_items"] != 10
        or scope["model"] != "gemma-4-e2b-it"
        or scope["endpoint"] != "http://127.0.0.1:18080/v1"
        or scope["unseen_B5_evaluation"] is not False
        or scope["B6_promotion"] is not False
        or result["scope_sha256"] != sha(PILOT / "FROZEN_SCOPE.json")
        or result["new_unseen_B5"] is not False
        or result["accepted_employer_facts"] != 0
        or result["production_database_unchanged"] is not True
        or result["public_corpus_unchanged"] is not True
    ):
        raise ValueError("Frozen model budget or authority diverged")
    if (
        review["model_outputs_seen_during_review"] is not False
        or review["source_review_type"] != "assistant_exposed_original_before_new_translation"
        or review["item_count"] != 10
        or review["unseen_claim"] is not False
    ):
        raise ValueError("Source-first assistant review changed or became unseen")
    # Reconstruct the batch plan under identical source snapshots.
    pilot = runpy.run_path(str(ROOT / "scripts/pilot_p16_b5_budget_guard_v1.py"))
    batches = pilot["chosen_batches"]()
    if [b.batch_id for b in batches] != [x["batch_id"] for x in scope["batch_identity"]]:
        raise ValueError("Selected batch identities changed")
    expected_items = [
        (b.batch_id, x.source_anchor_id, x.source_span_sha256) for b in batches for x in b.items
    ]
    reviewed_items = [
        (x["batch_id"], x["source_anchor_id"], x["source_span_sha256"])
        for x in review["reviewed_source_items"]
    ]
    if reviewed_items != expected_items:
        raise ValueError("Source-first assistant review was not source-identity bound")
    captured = result["http_events"]
    budget = result["attempt_budget"]
    attempts = budget["attempts"]
    if (
        budget["contract"] != B5_PHYSICAL_BUDGET_CONTRACT
        or budget["max_http_attempts"] != 7
        or budget["wall_seconds"] != 240.0
        or len(captured) != budget["attempted_http_dispatches"]
        or len(captured) != len(attempts)
        or len(captured) != result["actual_captured_HTTP_requests"]
        or len(captured) > 7
        or result["run_elapsed_seconds"] > 245
    ):
        raise ValueError("Physical attempt accounting/ceiling mismatch")
    expected_by_content_id = {b.batch_id: {x.content_id: x for x in b.items} for b in batches}
    actual_requests_by_batch = {b.batch_id: 0 for b in batches}
    for index, (event, attempt) in enumerate(zip(captured, attempts, strict=True), start=1):
        if (
            event["ordinal"] != index
            or attempt["ordinal"] != index
            or event["url_path"] != "/v1/chat/completions"
            or event["method"] != "POST"
            or event["status_code"] != attempt["status_code"]
            or event["error_type"] != attempt["error_type"]
        ):
            raise ValueError("Attempt event receipt missing or not local translation POST")
        request_file = PILOT / event["private_request_path"]
        response_file = (
            PILOT / event["private_response_path"]
            if event["private_response_path"] is not None
            else None
        )
        if (
            not request_file.resolve().is_relative_to(PILOT.resolve())
            or sha(request_file) != event["request_sha256"]
            or (
                response_file is not None
                and (
                    not response_file.resolve().is_relative_to(PILOT.resolve())
                    or sha(response_file) != event["response_sha256"]
                )
            )
        ):
            raise ValueError("Original private HTTP evidence changed")
        sent = read(request_file)
        if (
            sent["model"] != scope["model"]
            or sent["temperature"] != 0
            or sent["stream"] is not False
            or sent["response_format"]["type"] != "json_schema"
            or sent["response_format"]["json_schema"]["strict"] is not True
        ):
            raise ValueError("Unapproved model or prompt schema")
        inputs = json.loads(sent["messages"][1]["content"])
        if inputs["source_language"] != "fa" or inputs["target_language"] != "en":
            raise ValueError("Unexpected local translation direction")
        content_ids = {x["id"] for x in inputs["items"]}
        matches = [b for b in batches if content_ids == set(expected_by_content_id[b.batch_id])]
        if len(matches) != 1:
            raise ValueError("Model request grouped unknown or unrelated source items")
        batch = matches[0]
        actual_requests_by_batch[batch.batch_id] += 1
        for row in inputs["items"]:
            original = expected_by_content_id[batch.batch_id][row["id"]]
            if row["text"] != original.exact_source_text:
                raise ValueError("Raw provider request source text was changed")
    if [x["batch_id"] for x in result["responses"]] != [b.batch_id for b in batches]:
        raise ValueError("Batch processing order/inventory changed")
    translated = unresolved = not_attempted = 0
    for entry, batch in zip(result["responses"], batches, strict=True):
        if entry["state"] in {"not_attempted_budget_exhausted", "interrupted_wall_budget"}:
            if actual_requests_by_batch[batch.batch_id] != 0:
                raise ValueError("Marked not attempted despite actual HTTP dispatch")
            if entry["source_anchor_ids"] != [x.source_anchor_id for x in batch.items]:
                raise ValueError("Missing unresolved source anchors after budget stop")
            not_attempted += len(batch.items)
            continue
        if entry["state"] != "attempted":
            raise ValueError("Unexpected B5 batch outcome")
        candidate = entry["result"]
        if candidate["batch_id"] != batch.batch_id or len(candidate["items"]) != len(batch.items):
            raise ValueError("Batch result source item count/identity mismatch")
        if actual_requests_by_batch[batch.batch_id] < 1:
            raise ValueError("Model candidate recorded without a physical HTTP request")
        if candidate["batch_request_state"] == "failed" and any(
            x["state"] != "unresolved" for x in candidate["items"]
        ):
            raise ValueError("Batch-level failure wrongly promoted an item")
        for item, source in zip(candidate["items"], batch.items, strict=True):
            if (
                item["source_anchor_id"] != source.source_anchor_id
                or item["source_span_sha256"] != source.source_span_sha256
                or item["source_strength_candidate"] != source.strength
                or item["source_category_candidate"] != source.category
                or item["meaning_review"] != "unreviewed"
                or item["target_semantic_fidelity"] != "not_established"
            ):
                raise ValueError("Model output lost source ownership or asserted fidelity")
            if item["state"] == "source_bound_translation_candidate":
                if (
                    not isinstance(item["target_text"], str)
                    or hashlib.sha256(item["target_text"].encode()).hexdigest()
                    != item["target_sha256"]
                ):
                    raise ValueError("Valid English target SHA was not established")
                translated += 1
            elif item["state"] == "unresolved":
                if item["target_text"] is not None or item["target_sha256"] is not None:
                    raise ValueError("Failed model item has a fabricated target")
                unresolved += 1
            else:
                raise ValueError("Unsupported candidate translation state")
    if translated + unresolved + not_attempted != 10:
        raise ValueError("Pilot dropped or duplicated original source items")
    extra = PILOT / "PRIVATE_ASSISTANT_MEANING_REVIEW.json"
    independent = "not_reviewed"
    if extra.exists():
        meaning = read(extra)
        if meaning.get("scope_sha256") != sha(PILOT / "FROZEN_SCOPE.json") or meaning.get(
            "result_sha256"
        ) != sha(PILOT / "PRIVATE_RESULT.json"):
            raise ValueError("Assistant meaning review was not bound to outputs")
        if (
            meaning.get("independent_blind_human") is not False
            or meaning.get("unseen_quality_claim") is not False
        ):
            raise ValueError("Assistant reviews cannot establish blind unseen accuracy")
        if (
            len(meaning.get("per_original_item", [])) != 10
            or meaning.get("pre_model_source_only_review_sha256")
            != sha(PILOT / "SOURCE_FIRST_ASSISTANT_REVIEW.json")
            or meaning.get("accepted_employer_facts") != 0
            or meaning.get("no_automatic_acceptance") is not True
        ):
            raise ValueError("Incomplete assistant review denominator or authority")
        candidates = {
            x["source_anchor_id"]: x
            for entry in result["responses"]
            if entry["state"] == "attempted"
            for x in entry["result"]["items"]
        }
        if len(candidates) != translated + unresolved:
            raise ValueError("Candidate source item identity collisions")
        reviewed = meaning["per_original_item"]
        if [x["source_anchor_id"] for x in reviewed] != [
            x["source_anchor_id"] for x in review["reviewed_source_items"]
        ]:
            raise ValueError("Assistant review not source-first inventory aligned")
        verdict_counts = {
            "assistant_supported_in_exposed_case": 0,
            "partial_material_technical_term_omission": 0,
        }
        for row in reviewed:
            candidate = candidates.get(row["source_anchor_id"])
            if (
                candidate is None
                or row["source_span_sha256"] != candidate["source_span_sha256"]
                or row["target_sha256"] != candidate["target_sha256"]
                or row["downstream_employer_fact_authority"] != "none"
                or row["independent_human_verification"] is not False
                or row["observed_verdict"] not in verdict_counts
            ):
                raise ValueError("Assistant semantic verdict not bound to exact item evidence")
            verdict_counts[row["observed_verdict"]] += 1
        if (
            verdict_counts["assistant_supported_in_exposed_case"]
            != meaning["supported_selected_items"]
            or verdict_counts["partial_material_technical_term_omission"]
            != meaning["partial_selected_items"]
            or verdict_counts
            != {
                "assistant_supported_in_exposed_case": 9,
                "partial_material_technical_term_omission": 1,
            }
        ):
            raise ValueError("Assistant meaning review omitted or inflated a material defect")
        defect = next(
            x
            for x in reviewed
            if x["observed_verdict"] == "partial_material_technical_term_omission"
        )
        original_defect = next(
            x
            for x in review["reviewed_source_items"]
            if x["source_anchor_id"] == defect["source_anchor_id"]
        )
        candidate_defect = candidates[defect["source_anchor_id"]]
        if (
            "Secure SDLC" not in original_defect["original_source_text"]
            or "Secure SDLC" in candidate_defect["target_text"]
            or not any(
                "Secure" in flag or "SDLC" in flag for flag in candidate_defect["review_flags"]
            )
        ):
            raise ValueError("Reported missing technical token is not observed in source/target")
        independent = meaning["assistant_review_summary"]
    return {
        "status": "PASS_EXPOSED_LOCAL_BUDGET_TRANSPORT_REPLAY_NOT_UNSEEN_B5",
        "source_first_assistant_anchors": 10,
        "selected_exposed_batches": 5,
        "attempt_budget_max": 7,
        "physical_attempts_observed": len(captured),
        "responses_http_completed": budget["completed_http_responses"],
        "translated_candidate_items": translated,
        "unresolved_candidate_items": unresolved,
        "not_attempted_original_items": not_attempted,
        "wall_deadline_hit": budget["wall_deadline_hit"],
        "assisted_linguistic_review": independent,
        "source_and_production_unchanged": True,
        "accepted_employer_facts": 0,
        "fresh_unseen_B5": False,
        "B6_promotion": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
