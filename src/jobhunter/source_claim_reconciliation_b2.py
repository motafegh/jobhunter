"""Candidate-only source links for advisory original-language job claims.

This is deliberately NOT a Persian semantic verifier, P1.6 validator, model
prompt, source classifier, or production routing service. A valid source anchor
proves *where* a claim was linked, not that the original text entails the claim.
Links may be suggested by a model or added in an explicitly exposed assistant
diagnostic; neither is an accepted employer fact or independent review.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal

from jobhunter.source_item_candidate_b2 import (
    B2SourceCandidate,
    SourceItemCandidate,
    verify_b2_candidate,
)
from jobhunter.translation_store import TranslationSourceVersion

B2_CLAIM_RECONCILIATION_CONTRACT = "jobhunter-b2-advisory-source-reconciliation-v1"
FIELDS = frozenset(
    {
        "duties",
        "requirements",
        "preferences",
        "alternatives",
        "arrangements",
        "uncertainties",
        "work_implied_capabilities",
    }
)
LinkProvenance = Literal["none", "model_suggested", "assistant_exposed_diagnostic"]
GroundingState = Literal[
    "unlinked_unknown", "linked_semantics_unreviewed", "source_candidate_disagreement"
]


@dataclass(frozen=True, slots=True)
class AdvisoryClaim:
    field: str
    index: int
    text: str
    source_anchor_ids: tuple[str, ...] = ()
    link_provenance: LinkProvenance = "none"


@dataclass(frozen=True, slots=True)
class ReconciledAdvisoryClaim:
    field: str
    index: int
    claim_sha256: str
    source_anchor_ids: tuple[str, ...]
    link_provenance: LinkProvenance
    grounding_state: GroundingState
    diagnostic_signals: tuple[str, ...]
    semantic_review: str = "unreviewed_not_established"
    authority: str = "advisory_only_no_employer_fact_promotion"


@dataclass(frozen=True, slots=True)
class ReconciledAdvisoryBatch:
    contract_version: str
    source_job_id: str
    detail_version_id: int
    source_semantic_sha256: str
    claims: tuple[ReconciledAdvisoryClaim, ...]
    authority: str = "candidate_only_no_downstream_reuse"


def advisory_claim_sha256(
    source: TranslationSourceVersion, field: str, index: int, text: str
) -> str:
    """Bind a model claim's position and exact text to its original source version."""
    payload = {
        "source_job_id": source.source_job_id,
        "detail_version_id": source.job_detail_version_id,
        "source_semantic_sha256": source.semantic_sha256,
        "field": field,
        "index": index,
        "text": text,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()


def _signals(field: str, item: SourceItemCandidate) -> tuple[str, ...]:
    """Conservative discrepancies between TWO UNREVIEWED interpretations.

    These warnings cannot decide whether an English paraphrase is linguistically
    correct. In particular, no matching technology or valid anchor establishes
    the employer's modality, duty scope, eligibility, or prior-employment policy.
    """
    kind, strength = item.category, item.employer_strength
    if field == "duties":
        return () if kind == "work_duty" else ("duty_not_established_by_source_candidate",)
    if field == "requirements":
        return (
            ()
            if kind == "candidate_qualification" and strength == "required"
            else ("mandatory_strength_not_established_by_source_candidate",)
        )
    if field == "preferences":
        return (
            ()
            if kind in {"candidate_qualification", "behavioral_expectation"}
            and strength == "preferred"
            else ("preferred_strength_not_established_by_source_candidate",)
        )
    if field == "alternatives":
        return (
            ()
            if kind == "candidate_qualification"
            else ("eligibility_alternative_not_established_by_source_candidate",)
        )
    if field == "arrangements":
        return (
            ()
            if kind in {"work_arrangement", "benefit", "compensation"}
            else ("arrangement_not_established_by_source_candidate",)
        )
    if field == "work_implied_capabilities":
        return () if kind == "work_duty" else ("work_implied_capability_without_duty_candidate",)
    return ()  # An uncertainty is allowed to remain unresolved.


def reconcile_advisory_claims(
    source: TranslationSourceVersion,
    source_candidate: B2SourceCandidate,
    claims: tuple[AdvisoryClaim, ...],
) -> ReconciledAdvisoryBatch:
    """Validate exact links and report disagreements; NEVER accept employer facts.

    An unlinked claim is not presumed false. A linked, unflagged claim is NOT
    presumed true. Source-item categories/strengths are themselves diagnostic
    heuristics, so disagreements are signals for review, not hard semantic fails.
    """
    verify_b2_candidate(source_candidate, source)
    by_id = {item.anchor.anchor_id: item for item in source_candidate.items}
    seen: set[tuple[str, int]] = set()
    output: list[ReconciledAdvisoryClaim] = []

    for claim in claims:
        if (
            claim.field not in FIELDS
            or isinstance(claim.index, bool)
            or not isinstance(claim.index, int)
            or claim.index < 0
            or not isinstance(claim.text, str)
            or not claim.text.strip()
            or not isinstance(claim.source_anchor_ids, tuple)
            or claim.link_provenance
            not in {"none", "model_suggested", "assistant_exposed_diagnostic"}
        ):
            raise ValueError("Invalid advisory claim shape or provenance")
        key = (claim.field, claim.index)
        if key in seen:
            raise ValueError("Duplicate advisory field/index identity")
        seen.add(key)
        if (bool(claim.source_anchor_ids)) != (claim.link_provenance != "none"):
            raise ValueError("Source links require explicit, matching link provenance")
        if len(set(claim.source_anchor_ids)) != len(claim.source_anchor_ids):
            raise ValueError("Duplicate source anchor in advisory claim")
        if any(anchor_id not in by_id for anchor_id in claim.source_anchor_ids):
            raise ValueError("Unknown or stale original source-item anchor")

        flags = tuple(
            sorted(
                {
                    signal
                    for anchor_id in claim.source_anchor_ids
                    for signal in _signals(claim.field, by_id[anchor_id])
                }
            )
        )
        state: GroundingState = (
            "unlinked_unknown"
            if not claim.source_anchor_ids
            else "source_candidate_disagreement"
            if flags
            else "linked_semantics_unreviewed"
        )
        output.append(
            ReconciledAdvisoryClaim(
                field=claim.field,
                index=claim.index,
                claim_sha256=advisory_claim_sha256(source, claim.field, claim.index, claim.text),
                source_anchor_ids=claim.source_anchor_ids,
                link_provenance=claim.link_provenance,
                grounding_state=state,
                diagnostic_signals=flags,
            )
        )

    return ReconciledAdvisoryBatch(
        contract_version=B2_CLAIM_RECONCILIATION_CONTRACT,
        source_job_id=source.source_job_id,
        detail_version_id=source.job_detail_version_id,
        source_semantic_sha256=source.semantic_sha256,
        claims=tuple(output),
    )
