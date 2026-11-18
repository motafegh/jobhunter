"""Tests for the private, candidate-only P1.6 B3 translation boundary."""

from __future__ import annotations

import json
import runpy
import sqlite3
import tempfile
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest

from jobhunter.source_bound_translation_b3 import (
    B3_EXCLUDED_TNHZ_APPLICATION_ANCHORS,
    B3_REQUIRED_TNDX_EXAM_ANCHORS,
    CapturingHTTPTransport,
    build_translation_review_flags,
    make_b1_source_bound_alignment,
    make_b1_unresolved_alignment,
    make_native_identity_record,
    nested_leaf_parent_relations,
    select_b3_items,
)
from jobhunter.source_eligibility_candidate_b2 import build_candidate_eligibility_logic
from jobhunter.source_item_candidate_b2 import (
    SourceItemCandidate,
    interpret_original_source_candidate,
    verify_b2_candidate,
)
from jobhunter.source_span_identity import bind_original_source_span
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ROOT = Path(__file__).resolve().parents[1]
B0 = ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
PRIVATE = ROOT / "data/local-acceptance/p16-stage-b2-2026-11-17/b2-candidate-acceptance-v5"


def _source(text: str, job_id: str = "synthetic_b3") -> TranslationSourceVersion:
    return TranslationSourceVersion(
        source_job_id=job_id,
        job_detail_version_id=1,
        semantic_sha256="a" * 64,
        source_language="fa",
        fields={"description": text},
    )


def _item(
    source: TranslationSourceVersion,
    *,
    start: int,
    end: int,
    category: str,
    anchor_id: str | None = None,
    heading: str | None = None,
) -> SourceItemCandidate:
    anchor = bind_original_source_span(source, char_start=start, char_end=end)
    if anchor_id is not None:
        anchor = replace(anchor, anchor_id=anchor_id)
    return SourceItemCandidate(
        anchor=anchor,
        category=category,  # type: ignore[arg-type]
        employer_strength="unresolved",  # type: ignore[arg-type]
        evidence_basis="original_section_context",
        heading=heading,
        qualifier="unresolved",
    )


def test_tnhz_selection_excludes_only_the_two_frozen_generic_application_items() -> None:
    source = _source("برای همکاری، رزومه را ارسال کنید. سپس تماس بگیرید.", "tNhZ")
    first = _item(
        source,
        start=0,
        end=24,
        category="application_instruction",
        anchor_id=next(iter(B3_EXCLUDED_TNHZ_APPLICATION_ANCHORS)),
    )
    second_id = next(iter(B3_EXCLUDED_TNHZ_APPLICATION_ANCHORS - {first.anchor.anchor_id}))
    second = _item(
        source,
        start=25,
        end=len(source.fields["description"]),
        category="application_instruction",
        anchor_id=second_id,
    )
    selection = select_b3_items("tNhZ", (first, second))
    assert not selection.translate_items
    assert not selection.native_identity_items
    assert {item.anchor.anchor_id for item, _ in selection.excluded_items} == (
        B3_EXCLUDED_TNHZ_APPLICATION_ANCHORS
    )
    assert {reason for _, reason in selection.excluded_items} == {"generic_application_instruction"}


def test_edr_exam_items_are_not_excluded_as_generic_application_instructions() -> None:
    source = _source("آزمون فنی برای استخدام انجام می‌شود.", "tNDx")
    items = tuple(
        _item(
            source,
            start=0,
            end=len(source.fields["description"]),
            category="application_instruction",
            anchor_id=anchor_id,
        )
        for anchor_id in B3_REQUIRED_TNDX_EXAM_ANCHORS
    )
    selection = select_b3_items("tNDx", items)
    assert {item.anchor.anchor_id for item in selection.translate_items} == (
        B3_REQUIRED_TNDX_EXAM_ANCHORS
    )
    assert not selection.excluded_items


def test_native_identity_is_exact_and_has_no_model_authority() -> None:
    source = _source("Build Python APIs", "tMps")
    item = _item(
        source,
        start=0,
        end=len(source.fields["description"]),
        category="work_duty",
    )
    record = make_native_identity_record(
        source_job_id="tMps",
        source_item_id="s_" + item.anchor.anchor_id[:40],
        item=item,
    )
    assert record["state"] == "native_identity"
    assert record["target_text"] == item.anchor.exact_text
    assert record["target_sha256"] == record["source_span_sha256"]
    assert record["model_request_count"] == 0
    assert record["provider_name"] is None


def test_b1_translation_and_unresolved_alignments_keep_exact_target_offsets() -> None:
    target = "Teamwork is preferred, not mandatory."
    alignment = make_b1_source_bound_alignment(
        source_item_id="s_source_item",
        target_text=target,
        provider_name="lm-studio-translation-v2",
        provider_model="gemma-4-e2b-it",
        prompt_version="lm-studio-translation-v2-system-sha256:" + "b" * 64,
    )
    assert alignment["state"] == "source_bound_translation_candidate"
    assert alignment["target"]["target_span"] == {
        "char_start": 0,
        "char_end": len(target),
        "text_sha256": alignment["translation_sha256"],
    }
    unresolved = make_b1_unresolved_alignment("s_unresolved")
    assert unresolved["state"] == "unresolved"
    assert unresolved["target"] is None
    assert unresolved["translation_sha256"] is None


def test_review_flags_are_warnings_not_semantic_acceptance() -> None:
    good = build_translation_review_flags(
        "آشنایی با LLM مزیت محسوب می‌شود.",
        "Familiarity with LLM is an advantage.",
    )
    bad = build_translation_review_flags(
        "آشنایی با LLM مزیت محسوب می‌شود.",
        "LLM proficiency is required.",
    )
    assert not any("preference" in flag for flag in good)
    assert "possible_preference_to_mandatory_shift" in bad
    trait = build_translation_review_flags(
        "فردی وظیفه شناس و دقیق", "A responsible and careful person."
    )
    assert "conscientiousness_translation_needs_review" in trait


def test_nested_leafs_require_one_selected_parent_and_do_not_claim_target_offsets() -> None:
    parent = SimpleNamespace(
        anchor=SimpleNamespace(
            anchor_id="parent",
            field_path="description",
            char_start=100,
            char_end=200,
            text_sha256="a" * 64,
        )
    )
    leaf = SimpleNamespace(
        anchor_id="leaf",
        field_path="description",
        char_start=120,
        char_end=140,
        text_sha256="b" * 64,
    )
    relation = nested_leaf_parent_relations(candidate_items=(parent,), nested_leaf_anchors=(leaf,))[
        0
    ]
    assert relation["parent_anchor_id"] == "parent"
    assert relation["target_subspan_alignment"] == "not_established"


def test_capture_transport_records_bodies_but_never_auth_headers() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"ok": True}, request=request)

    capture = CapturingHTTPTransport(httpx.MockTransport(handler))
    with httpx.Client(
        base_url="http://127.0.0.1:18080/v1",
        transport=capture,
    ) as client:
        response = client.post(
            "/chat/completions",
            json={"model": "gemma-4-e2b-it", "messages": [{"content": "private source"}]},
            headers={"Authorization": "Bearer secret-token"},
        )
    assert response.json() == {"ok": True}
    assert len(capture.events) == 1
    event = capture.events[0]
    assert event.url_path == "/v1/chat/completions"
    assert b"private source" in event.request_body
    assert event.response_body == b'{"ok":true}'
    assert b"secret-token" not in event.request_body
    assert not hasattr(event, "headers")
    capture.close_inner()


def test_frozen_exposed_cohort_selection_is_exactly_64_items_and_63_requests() -> None:
    if not B0.is_file() or not (PRIVATE / "PRIVATE_B2_CANDIDATES.json").is_file():
        pytest.skip("Private B0/B2 acceptance data is intentionally absent in CI")

    with tempfile.TemporaryDirectory(prefix="jobhunter-b3-selection-") as temp:
        copied = Path(temp) / "source.sqlite3"
        with (
            sqlite3.connect(B0.resolve().as_uri() + "?mode=ro", uri=True) as source_db,
            sqlite3.connect(copied) as target_db,
        ):
            source_db.backup(target_db)
        store = TranslationStore(copied)
        private = json.loads((PRIVATE / "PRIVATE_B2_CANDIDATES.json").read_text(encoding="utf-8"))
        totals = {
            "translate": 0,
            "native": 0,
            "excluded": 0,
            "context": 0,
            "generic": 0,
            "nested_leaves": 0,
        }
        for job_id in ("tNhZ", "tMps", "tNDx", "tMjm"):
            source = store.latest_source_version(job_id)
            assert source is not None
            candidate = interpret_original_source_candidate(source)
            verify_b2_candidate(candidate, source)
            assert len(private[job_id]["original_candidate"]["items"]) == len(candidate.items)
            selection = select_b3_items(job_id, candidate.items)
            logic = build_candidate_eligibility_logic(source, candidate)
            leaves = [leaf.anchor for graph in logic.graphs for leaf in graph.leaves]
            relations = nested_leaf_parent_relations(
                candidate_items=selection.translate_items,
                nested_leaf_anchors=leaves,
            )
            totals["nested_leaves"] += len(relations)
            totals["translate"] += len(selection.translate_items)
            totals["native"] += len(selection.native_identity_items)
            totals["excluded"] += len(selection.excluded_items)
            totals["context"] += sum(
                reason == "context_only" for _, reason in selection.excluded_items
            )
            totals["generic"] += sum(
                reason == "generic_application_instruction"
                for _, reason in selection.excluded_items
            )
            if job_id == "tNDx":
                selected_ids = {item.anchor.anchor_id for item in selection.translate_items}
                assert selected_ids >= B3_REQUIRED_TNDX_EXAM_ANCHORS

        assert totals == {
            "translate": 63,
            "native": 1,
            "excluded": 14,
            "context": 12,
            "generic": 2,
            "nested_leaves": 12,
        }


def test_local_model_preflight_captures_endpoint_without_persisting_auth_header(
    tmp_path: Path,
) -> None:
    runner = runpy.run_path(str(ROOT / "scripts/run_p16_b3_source_bound_translation.py"))
    verify = runner["verify_local_model"]

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/models"
        assert request.headers["Authorization"] == "Bearer local-secret"
        return httpx.Response(
            200,
            json={"data": [{"id": "gemma-4-e2b-it"}]},
            request=request,
        )

    capture = CapturingHTTPTransport(httpx.MockTransport(handler))
    settings = SimpleNamespace(
        lm_studio_base_url="http://127.0.0.1:1234/v1",
        lm_studio_api_token="local-secret",
    )
    records = verify(
        settings=settings,
        expected_model="gemma-4-e2b-it",
        capture=capture,
        output_dir=tmp_path,
    )
    assert len(records) == 1
    assert records[0]["response_status"] == 200
    request_file = tmp_path / records[0]["raw_request_file"]
    response_file = tmp_path / records[0]["raw_response_file"]
    assert request_file.read_bytes() == b""
    assert b"gemma-4-e2b-it" in response_file.read_bytes()
    assert b"local-secret" not in request_file.read_bytes()
    assert b"local-secret" not in response_file.read_bytes()
    capture.close_inner()


def test_review_flag_lexical_boundaries_avoid_persian_substring_false_positives() -> None:
    flags = build_translation_review_flags(
        "پیاده‌سازی منطق بازار و نیازهای کسب‌وکار",
        "Implementation of market logic and business needs.",
    )
    assert "alternative_or_equivalence_cue_not_obvious" not in flags
    assert "negation_cue_not_obvious" not in flags

    preference = build_translation_review_flags(
        "آشنایی با LLM مزیت محسوب می‌شود، اما الزامی نیست.",
        "Familiarity with LLM is an advantage, but it is not mandatory.",
    )
    assert "possible_preference_to_mandatory_shift" not in preference

    penetration_testing = build_translation_review_flags(
        "آزمون نفوذ وب و تست برنامه‌های کاربردی",
        "Web penetration testing and application testing.",
    )
    assert "entrance_exam_term_not_obvious" not in penetration_testing


def test_negation_diagnostic_does_not_confuse_positive_required_with_negative_cues() -> None:
    preserved = build_translation_review_flags(
        "توانایی انجام کار بدون نیاز به نظارت دائم",
        "Ability to work without constant supervision.",
    )
    reversed = build_translation_review_flags(
        "این مورد الزامی نیست",
        "This item is mandatory.",
    )
    optional = build_translation_review_flags(
        "این مورد الزامی نیست",
        "This item is optional.",
    )
    assert "negation_cue_not_obvious" not in preserved
    assert "negation_cue_not_obvious" in reversed
    assert "negation_cue_not_obvious" not in optional
