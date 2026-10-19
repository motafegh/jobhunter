"""Non-authoritative P2.3A-0 deterministic profile-composition experiment.

Strategy A asks how useful accepted/current P1.6 plus reviewed Canonical Registry
identity is before introducing another semantic grouping or persistence layer.

This module is deliberately read-only:

* no Registry mutation;
* no model call;
* no profile persistence;
* no semantic grouping of pending, unmapped, or rejected claims.

Only exact claims already reviewed as ``mapped`` to the same canonical concept may
share a canonical bucket. Every other claim remains source-local. The result is an
experimental read model, not promoted P2.3 authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from jobhunter.canonical_registry import MappingDisposition
from jobhunter.canonical_registry_review import (
    CanonicalClaimReviewItem,
    CanonicalRegistryReviewReader,
)

P23A0CompositionBasis = Literal["reviewed_canonical_identity", "exact_source_claim"]


@dataclass(frozen=True, slots=True)
class P23A0CompositionBucket:
    """One deterministic Strategy-A grouping with its exact supporting claims."""

    key: str
    basis: P23A0CompositionBasis
    canonical_concept_id: str | None
    claims: tuple[CanonicalClaimReviewItem, ...]

    @property
    def claim_count(self) -> int:
        return len(self.claims)


@dataclass(frozen=True, slots=True)
class P23A0StrategyAComposition:
    """Read-only per-job Strategy-A composition and fragmentation measurements."""

    source_job_id: str
    buckets: tuple[P23A0CompositionBucket, ...]

    @property
    def claim_count(self) -> int:
        return sum(bucket.claim_count for bucket in self.buckets)

    @property
    def requirement_claim_count(self) -> int:
        return sum(
            1
            for bucket in self.buckets
            for claim in bucket.claims
            if claim.claim_kind == "requirement"
        )

    @property
    def responsibility_claim_count(self) -> int:
        return sum(
            1
            for bucket in self.buckets
            for claim in bucket.claims
            if claim.claim_kind == "responsibility"
        )

    @property
    def mapped_claim_count(self) -> int:
        return sum(
            1
            for bucket in self.buckets
            for claim in bucket.claims
            if claim.mapping_state == MappingDisposition.MAPPED.value
        )

    @property
    def canonical_bucket_count(self) -> int:
        return sum(
            bucket.basis == "reviewed_canonical_identity" for bucket in self.buckets
        )

    @property
    def source_local_bucket_count(self) -> int:
        return sum(bucket.basis == "exact_source_claim" for bucket in self.buckets)

    @property
    def deterministic_grouping_savings(self) -> int:
        """Number of exact claims collapsed only by reviewed canonical identity."""

        return self.claim_count - len(self.buckets)


def compose_p23a0_strategy_a(
    source_job_id: str,
    claims: tuple[CanonicalClaimReviewItem, ...],
) -> P23A0StrategyAComposition:
    """Compose one job without inventing semantic correspondence.

    ``mapped`` claims may share a bucket only when their immutable Registry mappings
    point at the same canonical concept. Pending/unmapped/rejected claims stay in
    distinct source-local buckets even when their wording happens to be identical.
    """

    job_id = source_job_id.strip()
    if not job_id:
        raise ValueError("source_job_id must not be empty")

    grouped: dict[
        str,
        tuple[P23A0CompositionBasis, str | None, list[CanonicalClaimReviewItem]],
    ] = {}
    seen_claims: set[tuple[int, str, int]] = set()

    for claim in claims:
        if claim.source_job_id != job_id:
            raise ValueError(
                "Strategy-A composition accepts claims from exactly one source job"
            )

        identity = (claim.analysis_artifact_id, claim.claim_kind, claim.claim_index)
        if identity in seen_claims:
            raise ValueError(f"Duplicate exact claim identity {identity!r}")
        seen_claims.add(identity)

        if claim.mapping_state == MappingDisposition.MAPPED.value:
            mapping = claim.mapping
            if mapping is None or mapping.canonical_concept_id is None:
                raise ValueError("Mapped claim is missing reviewed canonical identity")
            _validate_mapping_matches_claim(claim)
            concept_id = mapping.canonical_concept_id
            key = f"canonical:{concept_id}"
            basis: P23A0CompositionBasis = "reviewed_canonical_identity"
        else:
            concept_id = None
            key = (
                f"source:{claim.analysis_artifact_id}:"
                f"{claim.claim_kind}:{claim.claim_index}"
            )
            basis = "exact_source_claim"

        existing = grouped.get(key)
        if existing is None:
            grouped[key] = (basis, concept_id, [claim])
            continue

        existing_basis, existing_concept_id, existing_claims = existing
        if existing_basis != basis or existing_concept_id != concept_id:
            raise ValueError(f"Composition key collision for {key!r}")
        existing_claims.append(claim)

    buckets = tuple(
        P23A0CompositionBucket(
            key=key,
            basis=basis,
            canonical_concept_id=concept_id,
            claims=tuple(sorted(bucket_claims, key=_claim_sort_key)),
        )
        for key, (basis, concept_id, bucket_claims) in sorted(grouped.items())
    )
    return P23A0StrategyAComposition(source_job_id=job_id, buckets=buckets)


def compose_p23a0_strategy_a_for_job(
    reader: CanonicalRegistryReviewReader,
    source_job_id: str,
) -> P23A0StrategyAComposition:
    """Read accepted/current claims through the existing Registry review seam."""

    job_id = source_job_id.strip()
    if not job_id:
        raise ValueError("source_job_id must not be empty")
    claims = reader.list_current_claims(
        source_job_id=job_id,
        mapping_state="all",
        limit=5000,
    )
    return compose_p23a0_strategy_a(job_id, claims)


def _validate_mapping_matches_claim(claim: CanonicalClaimReviewItem) -> None:
    mapping = claim.mapping
    if mapping is None:
        raise ValueError("Mapped claim is missing Registry mapping state")
    expected = (
        claim.analysis_artifact_id,
        claim.source_job_id,
        claim.job_detail_version_id,
        claim.translation_artifact_id,
        claim.claim_kind,
        claim.claim_index,
        claim.source_text,
    )
    actual = (
        mapping.analysis_artifact_id,
        mapping.source_job_id,
        mapping.job_detail_version_id,
        mapping.translation_artifact_id,
        mapping.claim_kind,
        mapping.claim_index,
        mapping.source_text,
    )
    if actual != expected:
        raise ValueError("Registry mapping provenance does not match exact P1.6 claim")


def _claim_sort_key(claim: CanonicalClaimReviewItem) -> tuple[int, int, int]:
    kind_order = 0 if claim.claim_kind == "requirement" else 1
    return claim.analysis_artifact_id, kind_order, claim.claim_index
