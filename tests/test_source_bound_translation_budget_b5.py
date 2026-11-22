"""B5 physical HTTP/OS-wall-budget regression tests (no external traffic)."""

from __future__ import annotations

import hashlib
import json
import signal
import time

import httpx
import pytest

from jobhunter.source_bound_translation_batch_b5 import (
    BoundedBatchLMStudioProvider,
    evaluate_batched_translation,
    plan_source_batches,
    prepare_source_batch_items,
)
from jobhunter.source_bound_translation_budget_b5 import (
    B5AttemptBudgetExceeded,
    B5PhysicalBudget,
    B5PhysicalBudgetTransport,
    B5WallBudgetExceeded,
)
from jobhunter.source_item_candidate_b2_v2 import interpret_original_source_candidate_v2
from jobhunter.translation.base import TranslationError
from jobhunter.translation_store import TranslationSourceVersion


def sample_batch():
    text = (
        "مسئولیت‌ها: • طراحی سرویس قابل اعتماد "
        "• توسعه زیرساخت پایش "
        "• بهینه‌سازی سامانه‌های بزرگ "
        "• بررسی حوادث فنی"
    )
    source = TranslationSourceVersion(
        source_job_id="synthetic-b5",
        job_detail_version_id=101,
        semantic_sha256="c" * 64,
        source_language="fa",
        fields={"description": text},
    )
    candidate = interpret_original_source_candidate_v2(source)
    items = tuple(i for i in candidate.items if i.category == "work_duty")
    prepared = prepare_source_batch_items(source, items)
    assert len(prepared) == 4
    plan = plan_source_batches(prepared, max_batch_items=2)
    assert [len(b.items) for b in plan.batches] == [2, 2]
    return plan.batches


def echo_translation(request: httpx.Request, *, finish: str = "stop") -> httpx.Response:
    body = json.loads(request.read())
    inputs = json.loads(body["messages"][1]["content"])["items"]
    rows = [
        {"id": row["id"], "translation": f"English translation {i}"} for i, row in enumerate(inputs)
    ]
    assert all(
        row["id"] == hashlib.sha256(original["text"].encode()).hexdigest()[:24]
        for row, original in zip(rows, inputs, strict=True)
    )
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


def provider(guard: B5PhysicalBudgetTransport, *, retries: int = 0):
    return BoundedBatchLMStudioProvider(
        base_url="http://127.0.0.1:18080/v1",
        configured_model="gemma-4-e2b-it",
        transport=guard,
        max_retries=retries,
        sleep=lambda _: None,
    )


def test_each_physical_dispatch_counts_even_when_logical_request_count_is_one():
    batch = sample_batch()[0]
    seen = []

    def responder(request):
        seen.append(request)
        if len(seen) == 1:
            return echo_translation(request, finish="length")
        return echo_translation(request)

    guard = B5PhysicalBudgetTransport(
        budget=B5PhysicalBudget(max_http_attempts=2, wall_seconds=10),
        inner=httpx.MockTransport(responder),
    )
    with guard:
        done = evaluate_batched_translation(batch, provider(guard))
    assert done["batch_request_state"] == "completed"
    assert guard.attempted_http_dispatches == 2
    assert guard.completed_http_responses == 2
    assert [a["status_code"] for a in guard.safe_summary()["attempts"]] == [200, 200]


def test_truncation_recovery_is_denied_before_second_http_when_budget_is_one():
    batch = sample_batch()[0]
    count = 0

    def responder(request):
        nonlocal count
        count += 1
        return echo_translation(request, finish="length")

    guard = B5PhysicalBudgetTransport(
        budget=B5PhysicalBudget(max_http_attempts=1, wall_seconds=10),
        inner=httpx.MockTransport(responder),
    )
    with guard:
        result = evaluate_batched_translation(batch, provider(guard))
    assert count == 1
    assert guard.attempted_http_dispatches == 1
    assert guard.rejected_before_dispatch == 1
    assert result["batch_request_state"] == "failed"
    assert not result["source_item_associations_verified"]
    assert all(x["state"] == "unresolved" and x["target_text"] is None for x in result["items"])
    assert all(x["failure_code"] == B5AttemptBudgetExceeded.__name__ for x in result["items"])


def test_cumulative_budget_rejects_next_batch_and_does_not_promote_previous_failure():
    first, second = sample_batch()
    reached = []

    def responder(request):
        reached.append(request.url.path)
        return echo_translation(request)

    guard = B5PhysicalBudgetTransport(
        budget=B5PhysicalBudget(max_http_attempts=1, wall_seconds=10),
        inner=httpx.MockTransport(responder),
    )
    with guard:
        good = evaluate_batched_translation(first, provider(guard))
        rejected = evaluate_batched_translation(second, provider(guard))
    assert len(reached) == 1
    assert good["batch_request_state"] == "completed"
    assert rejected["batch_request_state"] == "failed"
    assert guard.attempted_http_dispatches == 1
    assert len(rejected["items"]) == 2
    assert all(x["state"] == "unresolved" for x in rejected["items"])


def test_failed_http_500_uses_attempts_and_retry_cap():
    batch = sample_batch()[0]
    calls = 0

    def responder(request):
        nonlocal calls
        calls += 1
        return httpx.Response(503, request=request, text="temporary outage")

    guard = B5PhysicalBudgetTransport(
        budget=B5PhysicalBudget(max_http_attempts=2, wall_seconds=10),
        inner=httpx.MockTransport(responder),
    )
    with guard:
        result = evaluate_batched_translation(batch, provider(guard, retries=4))
    assert calls == 2
    assert guard.attempted_http_dispatches == 2
    assert guard.rejected_before_dispatch == 1
    assert result["batch_request_state"] == "failed"
    assert all(x["target_text"] is None for x in result["items"])
    assert all(x["failure_code"] == B5AttemptBudgetExceeded.__name__ for x in result["items"])


def test_out_of_budget_model_timeout_is_a_hard_wall_clock_stop():
    batch = sample_batch()[0]
    count = 0

    def responder(request):
        nonlocal count
        count += 1
        time.sleep(1.0)
        return echo_translation(request)

    guard = B5PhysicalBudgetTransport(
        budget=B5PhysicalBudget(max_http_attempts=2, wall_seconds=0.03),
        inner=httpx.MockTransport(responder),
    )
    started = time.monotonic()
    with guard:
        result = evaluate_batched_translation(batch, provider(guard))
    elapsed = time.monotonic() - started
    assert elapsed < 0.7
    assert count == 1
    assert guard.attempted_http_dispatches == 1
    assert guard.wall_deadline_hit
    assert result["batch_request_state"] == "failed"
    assert all(x["failure_code"] == B5WallBudgetExceeded.__name__ for x in result["items"])


def test_monotonic_clock_denies_after_time_expires_between_batch_requests():
    first, second = sample_batch()
    clock = [100.0]
    count = 0

    def responder(request):
        nonlocal count
        count += 1
        clock[0] += 6
        return echo_translation(request)

    guard = B5PhysicalBudgetTransport(
        budget=B5PhysicalBudget(max_http_attempts=3, wall_seconds=5),
        inner=httpx.MockTransport(responder),
        clock=lambda: clock[0],
    )
    with guard:
        good = evaluate_batched_translation(first, provider(guard))
        denied = evaluate_batched_translation(second, provider(guard))
    assert good["batch_request_state"] == "completed"
    assert denied["batch_request_state"] == "failed"
    assert count == 1
    assert guard.wall_deadline_hit
    assert guard.rejected_before_dispatch == 1
    assert all(x["failure_code"] == B5WallBudgetExceeded.__name__ for x in denied["items"])


@pytest.mark.parametrize(
    "url,method",
    [
        ("https://127.0.0.1:18080/v1/chat/completions", "POST"),
        ("http://example.com:18080/v1/chat/completions", "POST"),
        ("http://127.0.0.1:18080/v1/models", "GET"),
        ("http://127.0.0.1:18081/v1/chat/completions", "POST"),
    ],
)
def test_nonlocal_or_wrong_endpoint_rejected_before_dispatch(url, method):
    dispatched = []

    def responder(request):
        dispatched.append(request)
        return httpx.Response(200, request=request)

    guard = B5PhysicalBudgetTransport(
        budget=B5PhysicalBudget(max_http_attempts=2, wall_seconds=10),
        inner=httpx.MockTransport(responder),
    )
    with guard, pytest.raises(TranslationError, match="only local LM Studio"):
        guard.handle_request(httpx.Request(method, url))
    assert dispatched == []
    assert guard.attempted_http_dispatches == 0
    assert guard.rejected_before_dispatch == 1


@pytest.mark.parametrize("max_http_attempts,wall_seconds", [(0, 10), (9, 10), (1, 0), (1, 901)])
def test_unbounded_or_invalid_session_policy_is_refused(max_http_attempts, wall_seconds):
    with pytest.raises(ValueError):
        B5PhysicalBudget(max_http_attempts=max_http_attempts, wall_seconds=wall_seconds)


def test_request_without_active_budget_session_rejected():
    guard = B5PhysicalBudgetTransport(
        budget=B5PhysicalBudget(max_http_attempts=1, wall_seconds=2),
        inner=httpx.MockTransport(lambda req: pytest.fail("never send HTTP")),
    )
    with pytest.raises(RuntimeError, match="active hard-deadline"):
        guard.handle_request(httpx.Request("POST", "http://127.0.0.1:18080/v1/chat/completions"))
    assert guard.attempted_http_dispatches == 0


def test_single_use_budget_guard_cannot_be_reentered():
    guard = B5PhysicalBudgetTransport(
        budget=B5PhysicalBudget(max_http_attempts=1, wall_seconds=1),
        inner=httpx.MockTransport(lambda req: pytest.fail("never send HTTP")),
    )
    with guard:
        pass
    with pytest.raises(ValueError, match="single-use"), guard:
        pass


def test_transport_exception_retries_consume_physical_attempts_without_unsafe_reuse():
    batch = sample_batch()[0]
    count = 0

    def responder(request):
        nonlocal count
        count += 1
        raise httpx.ConnectTimeout("no local model connection", request=request)

    guard = B5PhysicalBudgetTransport(
        budget=B5PhysicalBudget(max_http_attempts=2, wall_seconds=10),
        inner=httpx.MockTransport(responder),
    )
    with guard:
        result = evaluate_batched_translation(batch, provider(guard, retries=5))
    assert count == 2
    assert guard.attempted_http_dispatches == 2
    assert guard.completed_http_responses == 0
    assert guard.rejected_before_dispatch == 1
    assert result["batch_request_state"] == "failed"
    assert all(x["state"] == "unresolved" for x in result["items"])
    assert all(x["target_sha256"] is None for x in result["items"])


def test_budget_restores_prior_signal_handler_even_on_exception():
    previous = signal.getsignal(signal.SIGALRM)
    guard = B5PhysicalBudgetTransport(
        budget=B5PhysicalBudget(max_http_attempts=1, wall_seconds=10),
        inner=httpx.MockTransport(lambda _r: pytest.fail("no HTTP")),
    )
    with pytest.raises(RuntimeError, match="synthetic failed workflow"), guard:
        raise RuntimeError("synthetic failed workflow")
    assert signal.getsignal(signal.SIGALRM) is previous
    assert signal.getitimer(signal.ITIMER_REAL)[0] == 0
    assert guard.attempted_http_dispatches == 0


def test_guarded_budget_receipt_contains_no_model_source_or_target_text():
    batch = sample_batch()[0]
    guard = B5PhysicalBudgetTransport(
        budget=B5PhysicalBudget(max_http_attempts=1, wall_seconds=10),
        inner=httpx.MockTransport(echo_translation),
    )
    with guard:
        result = evaluate_batched_translation(batch, provider(guard))
    assert result["batch_request_state"] == "completed"
    receipt = guard.safe_summary()
    encoded = json.dumps(receipt, ensure_ascii=False)
    assert '"request_body"' not in encoded and '"target_text"' not in encoded
    assert '"source_text"' not in encoded and '"response_body"' not in encoded
    assert batch.items[0].exact_source_text not in encoded
    assert result["items"][0]["target_text"] not in encoded
    assert receipt["attempted_http_dispatches"] == 1
    assert receipt["no_payload_retained"] is True
