"""B5 candidate-only batching: no silent association, budget or authority changes."""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace

import httpx
import pytest

from jobhunter.source_bound_translation_b3 import select_b3_items
from jobhunter.source_bound_translation_batch_b5 import (
    B5_BATCH_PROVIDER_NAME,
    BoundedBatchLMStudioProvider,
    evaluate_batched_translation,
    plan_source_batches,
    prepare_source_batch_items,
)
from jobhunter.source_item_candidate_b2_v2 import interpret_original_source_candidate_v2
from jobhunter.translation.base import TranslationError
from jobhunter.translation.lm_studio import LMStudioTranslationProvider
from jobhunter.translation_store import TranslationSourceVersion

SAMPLE = (
    "طراحی سرویس‌های مالی ایمن و مقیاس‌پذیر",
    "توسعه پردازش‌های پس‌زمینه و صف‌های کاری",
    "پشتیبانی و بهینه‌سازی سرویس‌های شبکه",
    "مدیریت چرخه استقرار نرم‌افزار",
)


def original(text: str, job: str = "fixture") -> TranslationSourceVersion:
    return TranslationSourceVersion(
        source_job_id=job,
        job_detail_version_id=71,
        semantic_sha256="a" * 64,
        source_language="fa",
        fields={"description": text},
    )


def selected_items():
    source = original("مسئولیت‌ها: " + " · ".join(SAMPLE))
    candidate = interpret_original_source_candidate_v2(source)
    selected = select_b3_items(source.source_job_id, candidate.items)
    prepared = prepare_source_batch_items(source, selected.translate_items)
    assert len(prepared) == 4
    return prepared


def make_provider(handler):
    return BoundedBatchLMStudioProvider(
        base_url="http://127.0.0.1:18080/v1",
        configured_model="gemma-4-e2b-it",
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )


def request_items(request):
    data = json.loads(request.read())
    assert data["model"] == "gemma-4-e2b-it"
    assert data["response_format"]["type"] == "json_schema"
    assert data["response_format"]["json_schema"]["strict"] is True
    assert data["temperature"] == 0 and data["seed"] == 0
    rows = json.loads(data["messages"][1]["content"])["items"]
    for row in rows:
        assert row["id"] == hashlib.sha256(row["text"].encode()).hexdigest()[:24]
    return rows


def reply(request, rows, *, finish="stop"):
    return httpx.Response(
        200,
        request=request,
        json={
            "choices": [
                {
                    "finish_reason": finish,
                    "message": {"content": json.dumps({"translations": rows})},
                }
            ]
        },
    )


def test_planner_is_bounded_complete_and_deterministic():
    prepared = selected_items()
    first = plan_source_batches(prepared, max_batch_items=3)
    second = plan_source_batches(prepared, max_batch_items=3)
    assert first == second
    assert first.total_logical_items == 4
    assert [len(batch.items) for batch in first.batches] == [3, 1]
    assert not first.deferred_oversized
    assert [item.source_anchor_id for b in first.batches for item in b.items] == [
        item.source_anchor_id for item in prepared
    ]
    assert all(b.total_source_characters <= 1200 for b in first.batches)


def test_valid_reversed_response_associates_each_target_by_opaque_content_id():
    batch = plan_source_batches(selected_items(), max_batch_items=3).batches[0]
    calls = []

    def handler(request):
        rows = request_items(request)
        calls.append(len(rows))
        return reply(
            request,
            list(
                reversed(
                    [
                        {"id": row["id"], "translation": f"English {index + 1}"}
                        for index, row in enumerate(rows)
                    ]
                )
            ),
        )

    result = evaluate_batched_translation(batch, make_provider(handler))
    assert calls == [3]
    assert result["batch_request_state"] == "completed"
    assert result["logical_batch_invocations"] == 1
    assert result["logical_source_items_attempted"] == 3
    assert result["physical_http_completion_attempts"] == (
        "not_established_without_transport_capture"
    )
    assert [x["target_text"] for x in result["items"]] == [
        "English 1",
        "English 2",
        "English 3",
    ]
    for entry, source_item in zip(result["items"], batch.items, strict=True):
        assert entry["source_anchor_id"] == source_item.source_anchor_id
        assert entry["source_span_sha256"] == source_item.source_span_sha256
        assert entry["provider_name"] == B5_BATCH_PROVIDER_NAME
        assert entry["meaning_review"] == "unreviewed"
        assert entry["target_semantic_fidelity"] == "not_established"
        assert entry["independent_nested_leaf_alignment"] == "not_established"


@pytest.mark.parametrize("error", ["wrong_id", "duplicate_id", "missing", "extra_field"])
def test_invalid_ids_and_shapes_fail_closed_for_entire_batch(error):
    batch = plan_source_batches(selected_items(), max_batch_items=2).batches[0]

    def handler(request):
        source_rows = request_items(request)
        rows = [
            {"id": item["id"], "translation": f"English {i}"} for i, item in enumerate(source_rows)
        ]
        if error == "wrong_id":
            rows[0]["id"] = "incorrect-id"
        elif error == "duplicate_id":
            rows[1]["id"] = rows[0]["id"]
        elif error == "missing":
            rows.pop()
        else:
            rows[0]["unapproved_field"] = "invented"
        return reply(request, rows)

    result = evaluate_batched_translation(batch, make_provider(handler))
    assert result["batch_request_state"] == "failed"
    assert not result["source_item_associations_verified"]
    assert all(x["state"] == "unresolved" for x in result["items"])
    assert all(x["target_text"] is None for x in result["items"])
    assert all(x["target_sha256"] is None for x in result["items"])


def test_script_remains_in_one_output_does_not_make_it_english():
    batch = plan_source_batches(selected_items(), max_batch_items=2).batches[0]

    def handler(request):
        rows = request_items(request)
        return reply(
            request,
            [
                {"id": rows[0]["id"], "translation": "Secure APIs"},
                {"id": rows[1]["id"], "translation": "هنوز فارسی"},
            ],
        )

    result = evaluate_batched_translation(batch, make_provider(handler))
    assert [entry["state"] for entry in result["items"]] == [
        "source_bound_translation_candidate",
        "unresolved",
    ]
    assert result["items"][1]["target_text"] is None
    assert result["items"][1]["failure_code"] == "persian_script_remains_or_blank"


def test_truncated_batch_retries_boundedly_but_is_not_certified():
    batch = plan_source_batches(selected_items(), max_batch_items=2).batches[0]
    budgets = []

    def handler(request):
        body = json.loads(request.read())
        budgets.append(body["max_tokens"])
        entries = request_items(request)
        if len(budgets) == 1:
            return reply(request, [], finish="length")
        return reply(
            request,
            [{"id": row["id"], "translation": f"English {i}"} for i, row in enumerate(entries)],
        )

    result = evaluate_batched_translation(batch, make_provider(handler))
    assert budgets == [4096, 8192]
    assert all(x["state"] == "source_bound_translation_candidate" for x in result["items"])
    assert result["physical_http_completion_attempts"] == (
        "not_established_without_transport_capture"
    )


def test_duplicate_content_across_distinct_anchors_is_not_cobatched():
    a, b = selected_items()[:2]
    duplicate = replace(
        b,
        exact_source_text=a.exact_source_text,
        source_span_sha256=a.source_span_sha256,
    )
    plan = plan_source_batches((a, duplicate))
    assert [len(b.items) for b in plan.batches] == [1, 1]


def test_duplicate_anchor_rejected_and_oversized_deferred_without_dropping():
    a = selected_items()[0]
    with pytest.raises(ValueError, match="anchor twice"):
        plan_source_batches((a, a))
    text = "آزمون آزمایشی " * 180
    too_long = replace(
        a,
        source_anchor_id="f" * 64,
        exact_source_text=text,
        source_span_sha256=hashlib.sha256(text.encode()).hexdigest(),
    )
    plan = plan_source_batches((a, too_long))
    assert plan.total_logical_items == 2
    assert len(plan.batches) == 1
    assert plan.deferred_oversized == (too_long,)


def test_different_employer_role_strength_or_heading_cannot_cobatch():
    a, b, c, d = selected_items()
    unique = (
        a,
        replace(b, strength="preferred"),
        replace(c, source_job_id="other-employer"),
        replace(d, heading="Other section"),
    )
    plan = plan_source_batches(unique)
    assert len(plan.batches) == 4


def test_direct_provider_overlimit_checks_without_http_calls():
    provider = make_provider(lambda _request: pytest.fail("must not send HTTP"))
    with pytest.raises(TranslationError, match="1-4"):
        provider.translate_texts(
            tuple("آزمایش " + str(x) for x in range(5)), source_language="fa", target_language="en"
        )
    with pytest.raises(TranslationError, match="Repeated text"):
        provider.translate_texts(("متن", "متن"), source_language="fa", target_language="en")
    with pytest.raises(TranslationError, match="character ceiling"):
        provider.translate_texts(("متن" * 450,), source_language="fa", target_language="en")


def test_existing_provider_remains_one_item_per_request():
    sizes = []

    def handler(request):
        rows = request_items(request)
        sizes.append(len(rows))
        return reply(request, [{"id": rows[0]["id"], "translation": "English"}])

    old = LMStudioTranslationProvider(
        base_url="http://127.0.0.1:18080/v1",
        configured_model="gemma-4-e2b-it",
        transport=httpx.MockTransport(handler),
        max_retries=0,
    )
    result = old.translate_texts(
        ("متن الف", "متن ب", "متن ج"),
        source_language="fa",
        target_language="en",
    )
    assert len(result.texts) == 3
    assert sizes == [1, 1, 1]
    assert old.name == "lm-studio-translation-v2"


def test_invalid_batch_identity_rejected_before_provider():
    batch = plan_source_batches(selected_items(), max_batch_items=2).batches[0]
    with pytest.raises(ValueError, match="frozen batch"):
        evaluate_batched_translation(
            replace(batch, batch_id="0" * 64),
            make_provider(lambda _request: pytest.fail("no HTTP")),
        )


def test_original_source_anchor_identity_checked_before_planning():
    original_source = original("مسئولیت‌ها: طراحی سامانه ایمن")
    c = interpret_original_source_candidate_v2(original_source)
    selected = select_b3_items(original_source.source_job_id, c.items)
    tampered = replace(
        selected.translate_items[0],
        anchor=replace(selected.translate_items[0].anchor, exact_text="fake"),
    )
    with pytest.raises(ValueError):
        prepare_source_batch_items(original_source, (tampered,))
