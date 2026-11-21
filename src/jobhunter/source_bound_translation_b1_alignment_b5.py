"""Isolated B1 association bridge for the frozen B5 translation batch pilot.

Separate from the batch engine so the pilot source-code SHA remains immutable.
This is candidate-only B1 normalization, not validated source meaning or
employer-fact promotion. Original/translated nested-leaf subspans remain unknown.
"""

from __future__ import annotations

from typing import Any

from jobhunter.source_bound_translation_b3 import (
    make_b1_source_bound_alignment,
    make_b1_unresolved_alignment,
    sha256_text,
)
from jobhunter.source_bound_translation_batch_b5 import (
    B5_BATCH_CANDIDATE_VERSION,
    B5_BATCH_PROVIDER_NAME,
    PlannedBatch,
)
from jobhunter.translation.projection import contains_persian


def align_batch_result_to_b1(
    b1_bundle: dict[str, Any],
    batch: PlannedBatch,
    result: dict[str, Any],
) -> tuple[dict[str, Any], ...]:
    """Map each original source item to exactly one provisional B1 alignment.

    B1 source-item IDs are produced by B1, not inferred from translation
    response order or generated opaque content IDs. Unresolved results remain
    unresolved with no invented target offsets. Caller owns separate batch
    provenance receipts; none of these alignments are reviewed or promoted.
    """
    source = b1_bundle.get("source_version", {})
    if (
        source.get("source_job_id") != batch.source_job_id
        or source.get("semantic_sha256") != batch.items[0].source_semantic_sha256
        or result.get("contract") != B5_BATCH_CANDIDATE_VERSION
        or result.get("batch_id") != batch.batch_id
    ):
        raise ValueError("B1 source version and batch provenance differ")
    by_anchor: dict[str, dict[str, Any]] = {}
    for item in b1_bundle.get("items", []):
        ref = item.get("source_ref", {})
        if ref.get("kind") != "original_description_span":
            continue
        anchor = ref.get("anchor_id")
        if anchor in by_anchor:
            raise ValueError("B1 has duplicate source anchor IDs")
        by_anchor[anchor] = item
    translated = result.get("items")
    if (
        not isinstance(translated, list)
        or len(translated) != len(batch.items)
        or len({x.get("source_anchor_id") for x in translated}) != len(translated)
    ):
        raise ValueError("Batched translated item inventory is incomplete or duplicated")
    translated_by_anchor = {x["source_anchor_id"]: x for x in translated}
    if set(translated_by_anchor) != {x.source_anchor_id for x in batch.items}:
        raise ValueError("Wrong or extra source translated item in batch receipt")
    alignments = []
    for source_item in batch.items:
        b1 = by_anchor.get(source_item.source_anchor_id)
        candidate = translated_by_anchor[source_item.source_anchor_id]
        ref = b1.get("source_ref", {}) if b1 is not None else {}
        meaning = b1.get("meaning", {}) if b1 is not None else {}
        if (
            b1 is None
            or ref.get("text_sha256") != source_item.source_span_sha256
            or ref.get("field_sha256") != source_item.source_field_sha256
            or candidate.get("source_span_sha256") != source_item.source_span_sha256
            or candidate.get("source_field_sha256") != source_item.source_field_sha256
            or candidate.get("source_semantic_sha256") != source_item.source_semantic_sha256
            or candidate.get("source_job_id") != source_item.source_job_id
            or candidate.get("batch_id") != batch.batch_id
            or candidate.get("source_category_candidate") != source_item.category
            or candidate.get("source_strength_candidate") != source_item.strength
            or candidate.get("source_heading_sha256") != source_item.heading_sha256
            or meaning.get("category") != source_item.category
            or meaning.get("employer_strength") != source_item.strength
        ):
            raise ValueError("B1 source item identity or candidate strength mismatched")
        if candidate["state"] == "source_bound_translation_candidate":
            target_text = candidate.get("target_text")
            if (
                not isinstance(target_text, str)
                or not target_text.strip()
                or sha256_text(target_text) != candidate.get("target_sha256")
                or contains_persian(target_text)
                or candidate.get("target_char_start") != 0
                or candidate.get("target_char_end") != len(target_text)
                or candidate.get("provider_name") != B5_BATCH_PROVIDER_NAME
                or candidate.get("provider_model") != "gemma-4-e2b-it"
                or candidate.get("target_semantic_fidelity") != "not_established"
            ):
                raise ValueError("Target output cannot be used for a B1 candidate")
            alignment = make_b1_source_bound_alignment(
                source_item_id=b1["item_id"],
                target_text=target_text,
                provider_name=candidate["provider_name"],
                provider_model=candidate["provider_model"],
                prompt_version=B5_BATCH_CANDIDATE_VERSION,
            )
        elif candidate["state"] == "unresolved":
            if any(
                candidate.get(key) is not None
                for key in ("target_text", "target_sha256", "target_char_start", "target_char_end")
            ):
                raise ValueError("Unresolved translation cannot expose a target span")
            alignment = make_b1_unresolved_alignment(b1["item_id"])
        else:
            raise ValueError("Unrecognized candidate translation state")
        alignments.append(alignment)
    return tuple(alignments)


__all__ = ["align_batch_result_to_b1"]
