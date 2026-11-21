"""B5 batched source-item-to-B1 association, without semantic promotion."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from runpy import run_path

import httpx
import pytest

from jobhunter.source_bound_translation_b1_alignment_b5 import align_batch_result_to_b1
from jobhunter.source_bound_translation_b3 import select_b3_items
from jobhunter.source_bound_translation_batch_b5 import (
    BoundedBatchLMStudioProvider,
    evaluate_batched_translation,
    plan_source_batches,
    prepare_source_batch_items,
)
from jobhunter.source_item_candidate_b2_v2 import interpret_original_source_candidate_v2
from jobhunter.translation_store import TranslationSourceVersion

ROOT = Path(__file__).resolve().parents[1]


def fixture():
    source = TranslationSourceVersion(
        source_job_id="fixture_alignment",
        job_detail_version_id=14,
        semantic_sha256="a" * 64,
        source_language="fa",
        fields={"description": ("مهارت‌های ترجیحی: آشنایی با Python · تجربه با ابزارهای Docker")},
    )
    candidate = interpret_original_source_candidate_v2(source)
    selection = select_b3_items(source.source_job_id, candidate.items)
    prepared = prepare_source_batch_items(source, selection.translate_items)
    assert len(prepared) == 2
    assert all(i.strength == "preferred" for i in prepared)
    batch = plan_source_batches(prepared).batches[0]
    b1 = run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))["b1_design_from_b2"](
        candidate, source
    )
    validate = run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))["validate_bundle"]
    validate(b1, source=source)
    return source, b1, batch, validate


def valid_result(batch):
    def handler(request):
        payload = json.loads(request.read())
        items = json.loads(payload["messages"][1]["content"])["items"]
        return httpx.Response(
            200,
            request=request,
            json={
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "content": json.dumps(
                                {
                                    "translations": [
                                        {
                                            "id": x["id"],
                                            "translation": f"English meaning {index + 1}",
                                        }
                                        for index, x in enumerate(items)
                                    ]
                                }
                            )
                        },
                    }
                ]
            },
        )

    provider = BoundedBatchLMStudioProvider(
        base_url="http://127.0.0.1:18080/v1",
        configured_model="gemma-4-e2b-it",
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )
    return evaluate_batched_translation(batch, provider)


def test_two_batch_outputs_join_distinct_original_B1_source_ids():
    original, b1, batch, validate = fixture()
    translation = valid_result(batch)
    aligned = align_batch_result_to_b1(b1, batch, translation)
    assert len(aligned) == 2
    ids = {
        item["source_ref"]["anchor_id"]: item["item_id"]
        for item in b1["items"]
        if item["source_ref"]["kind"] == "original_description_span"
    }
    assert [x["source_item_id"] for x in aligned] == [ids[i.source_anchor_id] for i in batch.items]
    assert all(x["state"] == "source_bound_translation_candidate" for x in aligned)
    assert all(x["meaning_review"] == "unreviewed" for x in aligned)
    assert all(x["target"]["target_kind"] == "source_bound_item_output" for x in aligned)
    assert all(x["target"]["target_span"]["char_start"] == 0 for x in aligned)
    assert all(x["target"]["provider_name"].endswith("candidate-v1") for x in aligned)
    checked = deepcopy(b1)
    checked["alignments"] = list(aligned)
    validate(checked, source=original)
    assert checked["authority"] == "candidate_only_no_downstream_reuse"
    assert checked["review_events"] == []
    assert checked["brief"]["downstream_authority"] == "none"


def test_unresolved_member_has_no_invented_target_offsets():
    original, b1, batch, validate = fixture()
    received = valid_result(batch)
    received["items"][1]["state"] = "unresolved"
    received["items"][1]["target_text"] = None
    received["items"][1]["target_sha256"] = None
    received["items"][1]["target_char_start"] = None
    received["items"][1]["target_char_end"] = None
    aligned = align_batch_result_to_b1(b1, batch, received)
    assert aligned[0]["state"] == "source_bound_translation_candidate"
    assert aligned[1]["state"] == "unresolved"
    assert aligned[1]["target"] is None
    checked = deepcopy(b1)
    checked["alignments"] = list(aligned)
    validate(checked, source=original)


@pytest.mark.parametrize(
    "field, value",
    [
        ("source_span_sha256", "0" * 64),
        ("source_semantic_sha256", "0" * 64),
        ("source_field_sha256", "0" * 64),
        ("target_sha256", "0" * 64),
    ],
)
def test_tampered_source_or_target_digest_rejected(field, value):
    _, b1, batch, _ = fixture()
    received = valid_result(batch)
    received["items"][0][field] = value
    with pytest.raises(ValueError):
        align_batch_result_to_b1(b1, batch, received)


def test_false_required_original_B1_strength_rejected():
    _, b1, batch, _ = fixture()
    received = valid_result(batch)
    altered = deepcopy(b1)
    relevant = next(
        row
        for row in altered["items"]
        if row["source_ref"].get("anchor_id") == batch.items[0].source_anchor_id
    )
    relevant["meaning"]["employer_strength"] = "required"
    with pytest.raises(ValueError, match="strength"):
        align_batch_result_to_b1(altered, batch, received)


def test_duplicate_or_foreign_response_source_id_rejected():
    _, b1, batch, _ = fixture()
    received = valid_result(batch)
    received["items"][1]["source_anchor_id"] = "z" * 64
    with pytest.raises(ValueError, match="Wrong or extra"):
        align_batch_result_to_b1(b1, batch, received)


def test_missing_response_member_fails_closed():
    _, b1, batch, _ = fixture()
    received = valid_result(batch)
    received["items"] = received["items"][:1]
    with pytest.raises(ValueError, match="inventory"):
        align_batch_result_to_b1(b1, batch, received)
