"""Bounded read models for comparing current accepted job evidence."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from jobhunter.canonical_registry import CanonicalRegistryStore
from jobhunter.canonical_registry_review import (
    CanonicalClaimReviewItem,
    build_canonical_registry_review_reader,
)
from jobhunter.capability_service import CAPABILITY_PROMPT_VERSION, CAPABILITY_SCHEMA_VERSION
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.config import Settings
from jobhunter.p2_3a0_profile_experiment import (
    P23A0StrategyBGroup,
    compose_p23a0_strategy_a,
    compose_p23a0_strategy_b_from_current_capability,
)
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import build_translation_service


def claim_key(claim: CanonicalClaimReviewItem) -> tuple[int, str, int]:
    return claim.analysis_artifact_id, claim.claim_kind, claim.claim_index


def claim_anchor(claim: CanonicalClaimReviewItem) -> str:
    return f"claim-{claim.analysis_artifact_id}-{claim.claim_kind}-{claim.claim_index}"


@dataclass(frozen=True)
class ComparisonOption:
    source_job_id: str
    title: str
    company: str


@dataclass(frozen=True)
class ComparisonGroup:
    interpretation: P23A0StrategyBGroup
    matching_claims: tuple[CanonicalClaimReviewItem, ...]
    shared_claim_count: int


@dataclass(frozen=True)
class ComparisonJob:
    option: ComparisonOption
    claims: tuple[CanonicalClaimReviewItem, ...]
    matching_claims: tuple[CanonicalClaimReviewItem, ...]
    groups: tuple[ComparisonGroup, ...]
    grouping_notice: str
    capability_artifact_id: int | None

    @property
    def requirements(self) -> tuple[CanonicalClaimReviewItem, ...]:
        return tuple(c for c in self.matching_claims if c.claim_kind == "requirement")

    @property
    def responsibilities(self) -> tuple[CanonicalClaimReviewItem, ...]:
        return tuple(c for c in self.matching_claims if c.claim_kind == "responsibility")

    @property
    def total_responsibilities(self) -> int:
        return sum(c.claim_kind == "responsibility" for c in self.claims)


@dataclass(frozen=True)
class JobComparison:
    options: tuple[ComparisonOption, ...]
    jobs: tuple[ComparisonJob, ...]
    canonical_labels: dict[str, str]
    query: str


def build_job_comparison(
    settings: Settings, job_ids: tuple[str, ...], query: str = "",
) -> JobComparison:
    """Read accepted facts once; optional grouping never changes the claim denominator.

    The query is a literal, case-insensitive phrase in exact accepted claim wording.
    Broad evidence spans remain inspectable, but cannot make neighboring claims
    match a capability that their own wording never mentions.
    """

    selected = tuple(dict.fromkeys(job_id for job_id in job_ids if job_id))
    if len(job_ids) > 3:
        raise ValueError("Choose at most three jobs")
    if len(query) > 120:
        raise ValueError("Use at most 120 characters for the wording filter")
    query = " ".join(query.split())
    current_claims = (
        build_canonical_registry_review_reader(settings).list_current_claims(
            mapping_state="all", limit=5000,
        )
        if settings.effective_analysis_lm_studio_model() else ()
    )
    if len(current_claims) == 5000:
        raise ValueError("The accepted claim set exceeds this bounded comparison view")
    claims_by_job: dict[str, list[CanonicalClaimReviewItem]] = {}
    for claim in current_claims:
        claims_by_job.setdefault(claim.source_job_id, []).append(claim)

    source = JobHunterStore(settings.database_path)
    source.initialize()
    translation_service = build_translation_service(settings)
    options: dict[str, ComparisonOption] = {}
    for job_id in dict.fromkeys((*claims_by_job, *selected)):
        posting = source.get_job(job_id)
        if posting is None:
            raise LookupError(f"Job {job_id} is not in the local catalog")
        detail = source.get_latest_job_detail(job_id)
        translation = translation_service.current_artifact(job_id)
        fields = dict(detail.fields) if detail else {}
        if translation is not None:
            fields.update(translation.fields)
        options[job_id] = ComparisonOption(
            source_job_id=job_id,
            title=fields.get("title") or posting.title_observed or job_id,
            company=fields.get("company") or posting.company_slug,
        )

    capability_store = CapabilityIntelligenceStore(settings.database_path)
    jobs = tuple(
        _comparison_job(
            settings, options[job_id], tuple(claims_by_job.get(job_id, ())),
            query, capability_store,
        )
        for job_id in selected
    )
    registry = CanonicalRegistryStore(settings.database_path)
    concept_ids = {
        c.mapping.canonical_concept_id
        for job in jobs for c in job.matching_claims
        if c.mapping is not None and c.mapping.canonical_concept_id is not None
    }
    labels = {}
    for concept_id in concept_ids:
        concept = registry.get_concept(concept_id)
        if concept is not None:
            labels[concept_id] = concept.preferred_label
    return JobComparison(
        options=tuple(sorted(options.values(), key=lambda item: (item.title, item.source_job_id))),
        jobs=jobs, canonical_labels=labels, query=query,
    )


def _comparison_job(
    settings: Settings,
    option: ComparisonOption,
    claims: tuple[CanonicalClaimReviewItem, ...],
    query: str,
    capability_store: CapabilityIntelligenceStore,
) -> ComparisonJob:
    needle = query.casefold()
    matching = tuple(
        c for c in claims
        if not needle or needle in c.source_text.casefold()
    )
    grouping = None
    notice = "No current Capability grouping is available; exact accepted facts remain usable."
    if claims:
        artifact = capability_store.latest_current(
            option.source_job_id,
            model=settings.effective_capability_lm_studio_model(),
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        if artifact is not None:
            try:
                grouping = compose_p23a0_strategy_b_from_current_capability(
                    compose_p23a0_strategy_a(option.source_job_id, claims), artifact,
                )
                notice = "Existing capability labels are job-local interpretation."
            except ValueError:
                # Reject the affected overlay, retaining independently qualified facts.
                notice = (
                    "The existing Capability grouping could not be validated against these "
                    "current facts. Its interpretation is withheld; exact facts remain available."
                )
    matching_keys = {claim_key(c) for c in matching}
    groups = ()
    if grouping is not None:
        memberships = Counter(claim_key(c) for g in grouping.groups for c in g.claims)
        groups = tuple(
            ComparisonGroup(
                interpretation=group,
                matching_claims=tuple(c for c in group.claims if claim_key(c) in matching_keys),
                shared_claim_count=sum(memberships[claim_key(c)] > 1 for c in group.claims),
            )
            for group in grouping.groups
            if any(claim_key(c) in matching_keys for c in group.claims)
        )
    return ComparisonJob(
        option=option, claims=claims, matching_claims=matching, groups=groups,
        grouping_notice=notice,
        capability_artifact_id=grouping.capability_artifact_id if grouping else None,
    )
