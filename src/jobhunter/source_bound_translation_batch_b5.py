"""B5 candidate-only bounded source-item translation batching.

An opt-in sidecar around the established LM Studio v2 structured provider.
The original provider intentionally isolates text chunks. This class changes
only its request chunking, under explicit per-request item/character caps;
its JSON response schema, content-derived IDs and ID/order validation remain
the existing, tested implementation.

Batch membership never makes translation meaning automatically reviewed. A
failed request leaves ALL members unresolved with individual original-source
identities; there is no silent retry, item rescheduling or fallback reuse.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

from jobhunter.source_bound_translation_b3 import (
    build_translation_review_flags,
    sha256_text,
)
from jobhunter.source_item_candidate_b2 import SourceItemCandidate
from jobhunter.source_span_identity import verify_original_source_anchor
from jobhunter.translation.base import TranslationError
from jobhunter.translation.lm_studio import LMStudioTranslationProvider
from jobhunter.translation.projection import contains_persian
from jobhunter.translation_store import TranslationSourceVersion

B5_BATCH_CANDIDATE_VERSION = "jobhunter-p16-b5-translation-batching-candidate-v1"
B5_BATCH_PROVIDER_NAME = "lm-studio-translation-b5-bounded-batch-candidate-v1"
MAX_BATCH_ITEMS = 4
MAX_BATCH_CHARACTERS = 1_200
MAX_SINGLE_ITEM_CHARACTERS = 1_200


def _sha_object(data: Any) -> str:
    return hashlib.sha256(
        json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


@dataclass(frozen=True, slots=True)
class BatchSourceItem:
    source_job_id: str
    source_anchor_id: str
    source_semantic_sha256: str
    source_field_sha256: str
    source_span_sha256: str
    exact_source_text: str
    category: str
    strength: str
    heading: str | None

    @property
    def heading_sha256(self) -> str | None:
        return sha256_text(self.heading) if self.heading is not None else None

    @property
    def content_id(self) -> str:
        # The established LM Studio schema derives exactly this ID from text.
        return self.source_span_sha256[:24]


@dataclass(frozen=True, slots=True)
class PlannedBatch:
    batch_id: str
    source_job_id: str
    items: tuple[BatchSourceItem, ...]
    total_source_characters: int
    candidate_version: str = B5_BATCH_CANDIDATE_VERSION


@dataclass(frozen=True, slots=True)
class TranslationBatchPlan:
    batches: tuple[PlannedBatch, ...]
    deferred_oversized: tuple[BatchSourceItem, ...]
    total_logical_items: int
    max_batch_items: int
    max_batch_characters: int
    plan_sha256: str


def prepare_source_batch_items(
    source: TranslationSourceVersion,
    items: Sequence[SourceItemCandidate],
) -> tuple[BatchSourceItem, ...]:
    """Prove original-source ownership before any translation planning."""
    prepared: list[BatchSourceItem] = []
    seen: set[str] = set()
    for item in items:
        original = item.anchor
        verify_original_source_anchor(original, source)
        if original.anchor_id in seen:
            raise ValueError("Duplicate original source anchor cannot be batched")
        if original.source_job_id != source.source_job_id:
            raise ValueError("Source anchor belongs to another job")
        if not contains_persian(original.exact_text):
            raise ValueError("Batched translation requires Persian-script source items")
        if not original.exact_text.strip():
            raise ValueError("Empty source item cannot be translated")
        if original.text_sha256 != sha256_text(original.exact_text):
            raise ValueError("Source original item text digest mismatch")
        seen.add(original.anchor_id)
        prepared.append(
            BatchSourceItem(
                source_job_id=source.source_job_id,
                source_anchor_id=original.anchor_id,
                source_semantic_sha256=source.semantic_sha256,
                source_field_sha256=original.field_sha256,
                source_span_sha256=original.text_sha256,
                exact_source_text=original.exact_text,
                category=item.category,
                strength=item.employer_strength,
                heading=item.heading,
            )
        )
    return tuple(prepared)


def plan_source_batches(
    items: Sequence[BatchSourceItem],
    *,
    max_batch_items: int = MAX_BATCH_ITEMS,
    max_batch_characters: int = MAX_BATCH_CHARACTERS,
) -> TranslationBatchPlan:
    """Stable, source-ordered batch plan; never co-batch disparate obligations.

    Same employer source and semantic version, category, strength and original
    section heading are required. Duplicate source text is NOT co-batched:
    content-derived IDs alone cannot distinguish equal text inside one request.
    Oversized items remain explicit deferred work, not silently truncated.
    """
    if not 1 <= max_batch_items <= MAX_BATCH_ITEMS:
        raise ValueError("max_batch_items must be between 1 and 4")
    if not 1 <= max_batch_characters <= MAX_BATCH_CHARACTERS:
        raise ValueError("max_batch_characters exceeds bounded candidate ceiling")
    prepared = tuple(items)
    batches: list[PlannedBatch] = []
    deferred: list[BatchSourceItem] = []
    current: list[BatchSourceItem] = []
    running_chars = 0
    seen_anchors: set[str] = set()

    def flush() -> None:
        nonlocal running_chars
        if not current:
            return
        item_refs = [
            {
                "source_anchor_id": item.source_anchor_id,
                "source_span_sha256": item.source_span_sha256,
                "source_semantic_sha256": item.source_semantic_sha256,
                "source_field_sha256": item.source_field_sha256,
                "candidate_category": item.category,
                "candidate_strength": item.strength,
                "source_heading_sha256": item.heading_sha256,
            }
            for item in current
        ]
        batch_id = _sha_object(
            {
                "contract": B5_BATCH_CANDIDATE_VERSION,
                "source_job_id": current[0].source_job_id,
                "items": item_refs,
            }
        )
        batches.append(
            PlannedBatch(
                batch_id=batch_id,
                source_job_id=current[0].source_job_id,
                items=tuple(current),
                total_source_characters=running_chars,
            )
        )
        current.clear()
        running_chars = 0

    for item in prepared:
        if item.source_anchor_id in seen_anchors:
            raise ValueError("Cannot batch a source anchor twice")
        seen_anchors.add(item.source_anchor_id)
        if item.source_span_sha256 != sha256_text(item.exact_source_text):
            raise ValueError("Source hash mismatch in batched item")
        if len(item.exact_source_text) > MAX_SINGLE_ITEM_CHARACTERS:
            flush()
            deferred.append(item)
            continue
        if len(item.exact_source_text) > max_batch_characters:
            flush()
            deferred.append(item)
            continue
        current_key = (
            (
                current[0].source_job_id,
                current[0].source_semantic_sha256,
                current[0].category,
                current[0].strength,
                current[0].heading_sha256,
            )
            if current
            else None
        )
        next_key = (
            item.source_job_id,
            item.source_semantic_sha256,
            item.category,
            item.strength,
            item.heading_sha256,
        )
        # The provider uses only the first 24 source SHA digits for its IDs.
        content_ids = {existing.content_id for existing in current}
        if current and (
            current_key != next_key
            or len(current) >= max_batch_items
            or running_chars + len(item.exact_source_text) > max_batch_characters
            or item.content_id in content_ids
        ):
            flush()
        current.append(item)
        running_chars += len(item.exact_source_text)
    flush()
    if len({b.batch_id for b in batches}) != len(batches):
        raise ValueError("Duplicate batch ID across planned requests")
    flattened = tuple(item for batch in batches for item in batch.items)
    # Planning can interleave deferred oversized originals, so compare sets,
    # not concatenated order, for completeness.
    if (
        len(flattened) + len(deferred) != len(prepared)
        or {x.source_anchor_id for x in flattened + tuple(deferred)} != seen_anchors
    ):
        raise ValueError("Batch planner lost or duplicated source evidence")
    manifest = {
        "candidate_version": B5_BATCH_CANDIDATE_VERSION,
        "max_batch_items": max_batch_items,
        "max_batch_characters": max_batch_characters,
        "logical_item_count": len(prepared),
        "batches": [
            {
                "batch_id": batch.batch_id,
                "source_job_id": batch.source_job_id,
                "source_anchors": [item.source_anchor_id for item in batch.items],
                "source_spans": [item.source_span_sha256 for item in batch.items],
                "item_categories": [item.category for item in batch.items],
                "item_strengths": [item.strength for item in batch.items],
                "item_heading_hashes": [item.heading_sha256 for item in batch.items],
                "total_chars": batch.total_source_characters,
            }
            for batch in batches
        ],
        "deferred_oversized_anchors": [item.source_anchor_id for item in deferred],
    }
    return TranslationBatchPlan(
        batches=tuple(batches),
        deferred_oversized=tuple(deferred),
        total_logical_items=len(prepared),
        max_batch_items=max_batch_items,
        max_batch_characters=max_batch_characters,
        plan_sha256=_sha_object(manifest),
    )


class BoundedBatchLMStudioProvider(LMStudioTranslationProvider):
    """Opt-in small-batch provider; the installed v2 provider stays unchanged."""

    def __init__(self, *, base_url: str, configured_model: str | None, **kwargs: Any) -> None:
        parsed = urlparse(base_url)
        if (
            parsed.scheme != "http"
            or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
            or parsed.path.rstrip("/") != "/v1"
            or configured_model != "gemma-4-e2b-it"
        ):
            raise ValueError("B5 batch pilot is restricted to local LM Studio and frozen Gemma E2B")
        super().__init__(base_url=base_url, configured_model=configured_model, **kwargs)

    @property
    def name(self) -> str:
        return B5_BATCH_PROVIDER_NAME

    def _request_chunks(self, texts: tuple[str, ...]) -> tuple[tuple[str, ...], ...]:
        if not 1 <= len(texts) <= MAX_BATCH_ITEMS:
            raise TranslationError("B5 batch requires 1-4 source items")
        if sum(len(text) for text in texts) > MAX_BATCH_CHARACTERS:
            raise TranslationError("B5 batch character ceiling exceeded")
        content_ids = [sha256_text(text)[:24] for text in texts]
        if len(content_ids) != len(set(content_ids)):
            raise TranslationError("Repeated text/content ID in single B5 request")
        return (texts,)


def evaluate_batched_translation(
    batch: PlannedBatch,
    provider: BoundedBatchLMStudioProvider,
) -> dict[str, Any]:
    """Execute one planned batch, preserving failure and per-item candidate state.

    A transport/JSON/schema/cardinality error makes every member unresolved.
    No silent per-item retrials. A valid response is associated via strict
    content-derived IDs, not returned array position alone; semantic quality
    still requires source-first review. Never claim batch success as review.
    """
    if (
        not 1 <= len(batch.items) <= MAX_BATCH_ITEMS
        or sum(len(i.exact_source_text) for i in batch.items) != batch.total_source_characters
        or batch.total_source_characters > MAX_BATCH_CHARACTERS
        or any(i.source_job_id != batch.source_job_id for i in batch.items)
    ):
        raise ValueError("Invalid batch provenance, cardinality, or character bound")
    expected = plan_source_batches(
        batch.items,
        max_batch_items=len(batch.items),
        max_batch_characters=batch.total_source_characters,
    )
    if len(expected.batches) != 1 or expected.batches[0].batch_id != batch.batch_id:
        raise ValueError("Input item order or source context differs from frozen batch")
    texts = tuple(item.exact_source_text for item in batch.items)
    completed = None
    error_code: str | None = None
    try:
        completed = provider.translate_texts(texts, source_language="fa", target_language="en")
        if len(completed.texts) != len(batch.items):
            raise TranslationError("B5 source-bound response cardinality mismatch")
    except (TranslationError, ValueError) as exc:
        error_code = type(exc).__name__
        # Do not expose raw provider text or source content in error records.
        completed = None
    records = []
    for index, item in enumerate(batch.items):
        value = completed.texts[index].strip() if completed else ""
        valid_english = bool(value) and not contains_persian(value)
        state = (
            "source_bound_translation_candidate"
            if completed is not None and valid_english
            else "unresolved"
        )
        records.append(
            {
                "source_job_id": item.source_job_id,
                "source_anchor_id": item.source_anchor_id,
                "source_semantic_sha256": item.source_semantic_sha256,
                "source_field_sha256": item.source_field_sha256,
                "source_span_sha256": item.source_span_sha256,
                "source_heading_sha256": item.heading_sha256,
                "source_category_candidate": item.category,
                "source_strength_candidate": item.strength,
                "batch_id": batch.batch_id,
                "batch_member_index": index,
                "batch_member_count": len(batch.items),
                "source_content_id": item.content_id,
                "state": state,
                "target_text": value if valid_english else None,
                "target_sha256": sha256_text(value) if valid_english else None,
                "target_char_start": 0 if valid_english else None,
                "target_char_end": len(value) if valid_english else None,
                "provider_name": provider.name,
                "provider_model": provider.model if completed else None,
                "target_language": "en",
                "meaning_review": "unreviewed",
                "target_semantic_fidelity": "not_established",
                "independent_nested_leaf_alignment": "not_established",
                "review_flags": list(build_translation_review_flags(item.exact_source_text, value))
                if valid_english
                else [],
                "failure_code": (
                    None
                    if valid_english
                    else (
                        "persian_script_remains_or_blank" if completed is not None else error_code
                    )
                ),
            }
        )
    return {
        "contract": B5_BATCH_CANDIDATE_VERSION,
        "batch_id": batch.batch_id,
        "source_job_id": batch.source_job_id,
        "logical_batch_invocations": 1,
        "physical_http_completion_attempts": "not_established_without_transport_capture",
        "logical_source_items_attempted": len(batch.items),
        "batch_request_state": "completed" if completed else "failed",
        "source_item_associations_verified": bool(completed),
        "meaning_review": "unreviewed",
        "items": records,
    }


__all__ = [
    "B5_BATCH_CANDIDATE_VERSION",
    "B5_BATCH_PROVIDER_NAME",
    "MAX_BATCH_ITEMS",
    "MAX_BATCH_CHARACTERS",
    "BatchSourceItem",
    "PlannedBatch",
    "TranslationBatchPlan",
    "prepare_source_batch_items",
    "plan_source_batches",
    "BoundedBatchLMStudioProvider",
    "evaluate_batched_translation",
]
