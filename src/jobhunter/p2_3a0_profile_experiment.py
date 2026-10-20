"""Non-authoritative P2.3A-0 capability-profile composition experiment.

Strategy A asks how useful accepted/current P1.6 plus reviewed Canonical Registry
identity is before introducing another semantic grouping or persistence layer.

Strategy B overlays an explicitly accepted/current public Capability-v9 projection
when one already exists. Capability labels remain job-local interpretation; they
never create or replace canonical identity. Canonical identities shown inside a
Strategy-B group are inherited only from exact claims already reviewed as mapped.

This module is deliberately read-only:

* no Registry mutation;
* no model call;
* no profile persistence;
* no semantic grouping of pending, unmapped, or rejected claims;
* no inference that a Capability-v9 label is canonical identity.

The result is an experimental read model, not promoted P2.3 authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from jobhunter.canonical_registry import MappingDisposition
from jobhunter.canonical_registry_review import (
    CanonicalClaimReviewItem,
    CanonicalRegistryReviewReader,
)

P23A0CompositionBasis = Literal["reviewed_canonical_identity", "exact_source_claim"]
PUBLIC_CORPUS_SCHEMA_VERSION = "jobhunter-public-corpus-v1"
CAPABILITY_V9_PROMPT_VERSION = "job-capability-intelligence-v9"
CAPABILITY_V9_SCHEMA_VERSION = "job-capability-intelligence-v5"


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

    @property
    def claims(self) -> tuple[CanonicalClaimReviewItem, ...]:
        """Return each exact claim once in deterministic source order."""

        claims = [claim for bucket in self.buckets for claim in bucket.claims]
        return tuple(sorted(claims, key=_claim_sort_key))


@dataclass(frozen=True, slots=True)
class P23A0StrategyBGroup:
    """One accepted Capability-v9 job-local group over exact Strategy-A claims."""

    job_local_label: str
    summary: str | None
    claims: tuple[CanonicalClaimReviewItem, ...]
    canonical_concept_ids: tuple[str, ...]
    requirement_strength: str | None
    depth_signals: tuple[dict[str, Any], ...]
    work_activities: tuple[dict[str, Any], ...]
    suppressed_work_activity_count: int
    sub_capabilities: tuple[dict[str, Any], ...]
    underlying_knowledge: tuple[dict[str, Any], ...]
    operational_practices: tuple[dict[str, Any], ...]
    operational_context: tuple[dict[str, Any], ...]
    unknown_scope: tuple[dict[str, Any], ...]
    independence_expectation: Any
    overall_confidence: str | None

    @property
    def requirement_claim_count(self) -> int:
        return sum(claim.claim_kind == "requirement" for claim in self.claims)

    @property
    def responsibility_claim_count(self) -> int:
        return sum(claim.claim_kind == "responsibility" for claim in self.claims)


@dataclass(frozen=True, slots=True)
class P23A0StrategyBComposition:
    """Strategy A plus accepted Capability-v9 job-local organization."""

    base: P23A0StrategyAComposition
    capability_artifact_id: int
    capability_model: str
    groups: tuple[P23A0StrategyBGroup, ...]
    ungrouped_claims: tuple[CanonicalClaimReviewItem, ...]

    @property
    def grouped_claim_count(self) -> int:
        identities = {
            _claim_identity(claim)
            for group in self.groups
            for claim in group.claims
        }
        return len(identities)

    @property
    def canonical_concept_ids(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                {
                    concept_id
                    for group in self.groups
                    for concept_id in group.canonical_concept_ids
                }
            )
        )

    @property
    def suppressed_work_activity_count(self) -> int:
        return sum(group.suppressed_work_activity_count for group in self.groups)


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

        identity = _claim_identity(claim)
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


def compose_p23a0_strategy_b_from_public_capability(
    base: P23A0StrategyAComposition,
    public_capability: dict[str, Any],
) -> P23A0StrategyBComposition:
    """Overlay one explicit accepted/current public Capability-v9 projection.

    The public-corpus publication contract is the acceptance selector here. The
    caller must supply the committed ``capability.json`` payload, not an arbitrary
    latest database artifact. Exact dependency identities are revalidated against
    Strategy A before any job-local grouping is used.

    Capability-v9 work activities are only exposed when the same group links at
    least one exact accepted/current P1.6 responsibility. Requirement-only evidence
    may still contribute qualification/depth interpretation, but it cannot manufacture
    work that P1.6 never established. Suppression is counted explicitly for audit.
    """

    _validate_public_capability_identity(base, public_capability)
    claim_by_kind_index = {
        (claim.claim_kind, claim.claim_index): claim for claim in base.claims
    }
    intelligence = public_capability.get("intelligence")
    if not isinstance(intelligence, dict):
        raise ValueError("Public Capability-v9 projection is missing intelligence")
    profiles = intelligence.get("capabilities")
    if not isinstance(profiles, list):
        raise ValueError("Public Capability-v9 intelligence.capabilities must be a list")

    groups: list[P23A0StrategyBGroup] = []
    grouped_identities: set[tuple[int, str, int]] = set()
    for position, profile in enumerate(profiles):
        if not isinstance(profile, dict):
            raise ValueError(f"Capability-v9 group {position} must be an object")
        label = str(profile.get("capability_label") or "").strip()
        if not label:
            raise ValueError(f"Capability-v9 group {position} has no job-local label")

        linked_claims = _resolve_profile_claims(
            profile,
            claim_by_kind_index=claim_by_kind_index,
            position=position,
        )
        if not linked_claims:
            raise ValueError(f"Capability-v9 group {position} has no exact source claims")
        grouped_identities.update(_claim_identity(claim) for claim in linked_claims)

        canonical_ids = tuple(
            sorted(
                {
                    mapping.canonical_concept_id
                    for claim in linked_claims
                    if claim.mapping_state == MappingDisposition.MAPPED.value
                    and (mapping := claim.mapping) is not None
                    and mapping.canonical_concept_id is not None
                }
            )
        )
        raw_work_activities = _dict_sequence(profile, "work_activities", position)
        has_linked_responsibility = any(
            claim.claim_kind == "responsibility" for claim in linked_claims
        )
        if has_linked_responsibility:
            work_activities = raw_work_activities
            suppressed_work_activity_count = 0
        else:
            work_activities = ()
            suppressed_work_activity_count = len(raw_work_activities)

        groups.append(
            P23A0StrategyBGroup(
                job_local_label=label,
                summary=_optional_string(profile.get("summary")),
                claims=linked_claims,
                canonical_concept_ids=canonical_ids,
                requirement_strength=_optional_string(profile.get("requirement_strength")),
                depth_signals=_dict_sequence(profile, "depth_signals", position),
                work_activities=work_activities,
                suppressed_work_activity_count=suppressed_work_activity_count,
                sub_capabilities=_dict_sequence(profile, "sub_capabilities", position),
                underlying_knowledge=_dict_sequence(profile, "underlying_knowledge", position),
                operational_practices=_dict_sequence(profile, "operational_practices", position),
                operational_context=_dict_sequence(profile, "operational_context", position),
                unknown_scope=_dict_sequence(profile, "unknown_scope", position),
                independence_expectation=profile.get("independence_expectation"),
                overall_confidence=_optional_string(profile.get("overall_confidence")),
            )
        )

    ungrouped = tuple(
        claim for claim in base.claims if _claim_identity(claim) not in grouped_identities
    )
    return P23A0StrategyBComposition(
        base=base,
        capability_artifact_id=_required_int(public_capability, "artifact_id"),
        capability_model=_required_string(public_capability, "model"),
        groups=tuple(groups),
        ungrouped_claims=ungrouped,
    )


def _validate_public_capability_identity(
    base: P23A0StrategyAComposition,
    payload: dict[str, Any],
) -> None:
    if payload.get("schema_version") != PUBLIC_CORPUS_SCHEMA_VERSION:
        raise ValueError("Strategy B requires an explicit public-corpus Capability projection")
    if payload.get("stage") != "capability":
        raise ValueError("Public projection stage must be capability")
    if payload.get("prompt_version") != CAPABILITY_V9_PROMPT_VERSION:
        raise ValueError("Strategy B requires Capability-v9 prompt identity")
    if payload.get("capability_schema_version") != CAPABILITY_V9_SCHEMA_VERSION:
        raise ValueError("Strategy B requires Capability-v9 schema identity")
    if payload.get("source_job_id") != base.source_job_id:
        raise ValueError("Capability projection source job does not match Strategy A")

    claims = base.claims
    if not claims:
        raise ValueError("Strategy B requires at least one accepted/current P1.6 claim")
    dependency_identities = {
        (
            claim.analysis_artifact_id,
            claim.job_detail_version_id,
            claim.translation_artifact_id,
        )
        for claim in claims
    }
    if len(dependency_identities) != 1:
        raise ValueError("Strategy A claims do not share one exact P1.6 dependency chain")
    analysis_id, detail_id, translation_id = next(iter(dependency_identities))
    actual = (
        _required_int(payload, "analysis_artifact_id"),
        _required_int(payload, "job_detail_version_id"),
        _required_int(payload, "translation_artifact_id"),
    )
    if actual != (analysis_id, detail_id, translation_id):
        raise ValueError("Capability projection dependencies do not match Strategy A")


def _resolve_profile_claims(
    profile: dict[str, Any],
    *,
    claim_by_kind_index: dict[tuple[str, int], CanonicalClaimReviewItem],
    position: int,
) -> tuple[CanonicalClaimReviewItem, ...]:
    linked: list[CanonicalClaimReviewItem] = []
    seen: set[tuple[str, int]] = set()
    for field_name, claim_kind in (
        ("source_requirement_indices", "requirement"),
        ("source_responsibility_indices", "responsibility"),
    ):
        raw_indices = profile.get(field_name, [])
        if not isinstance(raw_indices, list):
            raise ValueError(f"Capability-v9 group {position} {field_name} must be a list")
        for raw_index in raw_indices:
            if not isinstance(raw_index, int) or isinstance(raw_index, bool) or raw_index < 0:
                raise ValueError(
                    f"Capability-v9 group {position} has invalid {field_name} index"
                )
            identity = (claim_kind, raw_index)
            if identity in seen:
                raise ValueError(
                    f"Capability-v9 group {position} repeats exact source claim {identity!r}"
                )
            seen.add(identity)
            claim = claim_by_kind_index.get(identity)
            if claim is None:
                raise ValueError(
                    f"Capability-v9 group {position} references unavailable {identity!r}"
                )
            linked.append(claim)
    return tuple(sorted(linked, key=_claim_sort_key))


def _dict_sequence(
    profile: dict[str, Any],
    field_name: str,
    position: int,
) -> tuple[dict[str, Any], ...]:
    raw = profile.get(field_name, [])
    if raw is None:
        return ()
    if not isinstance(raw, list) or any(not isinstance(item, dict) for item in raw):
        raise ValueError(f"Capability-v9 group {position} {field_name} must be a list of objects")
    return tuple(dict(item) for item in raw)


def _required_int(payload: dict[str, Any], field_name: str) -> int:
    value = payload.get(field_name)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"Public Capability projection {field_name} must be an integer")
    return value


def _required_string(payload: dict[str, Any], field_name: str) -> str:
    value = payload.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Public Capability projection {field_name} must be a non-empty string")
    return value.strip()


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Capability-v9 optional text field must be a string or null")
    return value.strip() or None


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


def _claim_identity(claim: CanonicalClaimReviewItem) -> tuple[int, str, int]:
    return claim.analysis_artifact_id, claim.claim_kind, claim.claim_index


def _claim_sort_key(claim: CanonicalClaimReviewItem) -> tuple[int, int, int]:
    kind_order = 0 if claim.claim_kind == "requirement" else 1
    return claim.analysis_artifact_id, kind_order, claim.claim_index
