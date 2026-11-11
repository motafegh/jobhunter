"""Read-only P2.3B candidate briefs over already-qualified factual job evidence.

This is not a persistent profile, canonical equivalence engine, inference provider,
or employer requirement generator. It reuses the bounded comparison read owner.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Literal
from urllib.parse import quote

from jobhunter.canonical_registry_review import CanonicalClaimReviewItem
from jobhunter.config import Settings
from jobhunter.job_comparison import ComparisonJob, build_job_comparison, claim_anchor

CandidateStatus = Literal[
    "strongly_implied_by_work", "model_inferred_prerequisite", "unknown_or_unsupported"
]
CandidateConfidence = Literal["low", "medium", "high"]
_ALTERNATIVE_RE = re.compile(r"\b(?:or|and/or)\b", re.IGNORECASE)
_JSON_FENCE = re.compile(r"^\s*```(?:json)?\s*(\{.*\})\s*```\s*$", re.S | re.I)


def decode_candidate_json(raw: str) -> dict:
    """Accept only a JSON object or one complete fenced object, never prose extraction."""
    match = _JSON_FENCE.fullmatch(raw)
    result = json.loads(match.group(1) if match else raw)
    if not isinstance(result, dict):
        raise ValueError("Model candidate must be a JSON object")
    return result


@dataclass(frozen=True, slots=True)
class FactReference:
    """One accepted/current P1.6 claim, never authored by an inference model."""

    ref: str
    claim_kind: str
    statement: str
    evidence: str | None
    strength: str | None
    explicit_depth: str | None
    concept_id: str | None
    job_source_url: str
    exact_claim_url: str
    potential_alternatives: bool


@dataclass(frozen=True, slots=True)
class EvidenceQuestion:
    """Candidate interview/project verification task, not an employer obligation."""

    kind: str
    question: str
    supporting_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ProposedInterpretation:
    """Optional author/model proposal, never accepted as a source fact."""

    text: str
    status: CandidateStatus
    confidence: CandidateConfidence
    supporting_refs: tuple[str, ...]
    rationale: str


@dataclass(frozen=True, slots=True)
class CapabilityExpectationBrief:
    contract: str
    source_job_id: str
    capability_phrase: str
    accepted_claim_count: int
    matched_claim_count: int
    source_requirements: tuple[FactReference, ...]
    source_responsibilities: tuple[FactReference, ...]
    questions: tuple[EvidenceQuestion, ...]
    current_capability_artifact_id: int | None
    grouping_notice: str
    limitation: str

    @property
    def all_facts(self) -> tuple[FactReference, ...]:
        return (*self.source_requirements, *self.source_responsibilities)


def _fact(claim: CanonicalClaimReviewItem, job_id: str) -> FactReference:
    return FactReference(
        ref=f"{claim.analysis_artifact_id}:{claim.claim_kind}:{claim.claim_index}",
        claim_kind=claim.claim_kind,
        statement=claim.source_text,
        evidence=claim.evidence,
        strength=claim.strength,
        explicit_depth=claim.depth_signal,
        concept_id=(
            claim.mapping.canonical_concept_id if claim.mapping is not None else None
        ),
        job_source_url=f"/jobs/{quote(job_id, safe='')}#english-analysis",
        exact_claim_url=(
            f"/compare?job={quote(job_id, safe='')}#{claim_anchor(claim)}"
        ),
        potential_alternatives=(
            claim.claim_kind == "requirement" and
            bool(_ALTERNATIVE_RE.search(claim.source_text))
        ),
    )


def compose_expectation_brief(job: ComparisonJob, phrase: str) -> CapabilityExpectationBrief:
    """Compose an honest question-oriented baseline without new semantic claims.

    Claim-level 'required' never proves a mentioned alternative mandatory.
    Missing matching duties never proves that the work is absent from the role.
    """

    if not phrase or not phrase.strip() or len(phrase) > 120:
        raise ValueError("Choose a nonempty capability phrase of at most 120 characters")
    phrase = " ".join(phrase.split())
    if not job.claims:
        raise ValueError("No accepted/current P1.6 evidence for the selected job")
    matches = tuple(
        c for c in job.claims if phrase.casefold() in c.source_text.casefold()
    )
    requirements = tuple(
        _fact(c, job.option.source_job_id) for c in matches if c.claim_kind == "requirement"
    )
    responsibilities = tuple(
        _fact(c, job.option.source_job_id)
        for c in matches if c.claim_kind == "responsibility"
    )
    questions: list[EvidenceQuestion] = []
    for claim in requirements:
        questions.append(EvidenceQuestion(
            kind="qualification_demonstration",
            question=(
                "What concrete project or work evidence demonstrates this exact "
                "qualification, and which parts have you personally performed?"
            ),
            supporting_refs=(claim.ref,),
        ))
        if claim.potential_alternatives:
            questions.append(EvidenceQuestion(
                kind="alternative_scope",
                question=(
                    "Does the employer require this particular capability, or does "
                    "one of the alternatives in the statement also satisfy the condition?"
                ),
                supporting_refs=(claim.ref,),
            ))
    for claim in responsibilities:
        questions.append(EvidenceQuestion(
            kind="direct_work_demonstration",
            question=(
                "What technically concrete example could demonstrate the "
                "explicitly described work, without assuming unstated ownership or scale?"
            ),
            supporting_refs=(claim.ref,),
        ))
    if not responsibilities:
        questions.append(EvidenceQuestion(
            kind="missing_work_scope",
            question=(
                "Which duties, if any, involve this capability? No directly stated "
                "duty matches this phrase in the current accepted claim wording."
            ),
            supporting_refs=tuple(c.ref for c in requirements),
        ))
    questions.append(EvidenceQuestion(
        kind="technical_scope",
        question=(
            "What technical scope, independence, deployment conditions, and "
            "performance expectations would need to be verified rather than assumed?"
        ),
        supporting_refs=tuple(c.ref for c in (*requirements, *responsibilities)),
    ))
    return CapabilityExpectationBrief(
        contract="job-capability-expectation-candidate-v0",
        source_job_id=job.option.source_job_id,
        capability_phrase=phrase,
        accepted_claim_count=len(job.claims),
        matched_claim_count=len(matches),
        source_requirements=requirements,
        source_responsibilities=responsibilities,
        questions=tuple(questions),
        current_capability_artifact_id=job.capability_artifact_id,
        grouping_notice=job.grouping_notice,
        limitation=(
            "Only literal accepted-claim wording is selected. Claim strength applies "
            "to the entire statement, not necessarily each listed alternative. "
            "These questions are candidate guidance, not employer-stated requirements. "
            "Unmatched work, independence and technical scope remain unassessed."
        ),
    )


def build_capability_expectation_brief(
    settings: Settings, source_job_id: str, phrase: str,
) -> CapabilityExpectationBrief:
    """Read the same current accepted facts as /compare, with no source/model call."""

    comparison = build_job_comparison(settings, (source_job_id,), phrase)
    if not comparison.jobs:
        raise LookupError(f"Job {source_job_id} has no comparison selection")
    return compose_expectation_brief(comparison.jobs[0], phrase)


def validate_interpretation_proposals(
    brief: CapabilityExpectationBrief,
    proposed: tuple[ProposedInterpretation, ...],
) -> tuple[ProposedInterpretation, ...]:
    """Validate candidate provenance/strength boundaries, not semantic correctness.

    Accepted facts remain owned by P1.6. Proposed work implications need direct
    job work, and inferred prerequisites need independent required qualification
    support, not an alternative-only or preferred basis.
    """
    if len(proposed) > 8:
        raise ValueError("No more than eight candidate interpretations")
    owned = {f.ref: f for f in brief.all_facts}
    for item in proposed:
        if not item.text.strip() or not item.rationale.strip():
            raise ValueError("Candidate interpretation and rationale cannot be empty")
        if len(item.text) > 600 or len(item.rationale) > 500:
            raise ValueError("Candidate interpretation exceeds bounded text limits")
        if len(item.supporting_refs) > 10:
            raise ValueError("Candidate cites too many selected claims")
        if item.status not in (
            "strongly_implied_by_work", "model_inferred_prerequisite",
            "unknown_or_unsupported",
        ) or item.confidence not in ("low", "medium", "high"):
            raise ValueError("Unsupported candidate evidence status/confidence")
        if len(item.supporting_refs) != len(set(item.supporting_refs)):
            raise ValueError("Duplicate supporting source references")
        if any(ref not in owned for ref in item.supporting_refs):
            raise ValueError("Candidate cites an unselected or stale source claim")
        refs = [owned[ref] for ref in item.supporting_refs]
        if item.status == "strongly_implied_by_work" and not any(
            ref.claim_kind == "responsibility" for ref in refs
        ):
            raise ValueError("Work implication requires directly supported work")
        if item.status == "model_inferred_prerequisite" and not any(
            ref.claim_kind == "requirement"
            and ref.strength == "required"
            and not ref.potential_alternatives
            for ref in refs
        ):
            raise ValueError(
                "A model prerequisite needs a non-alternative required claim"
            )
    return proposed


def format_expectation_brief(brief: CapabilityExpectationBrief) -> str:
    """Human-readable local candidate report; includes exact accepted job wording."""

    lines = [
        f"# Candidate capability expectations — {brief.source_job_id}: {brief.capability_phrase}",
        "",
        f"Contract: {brief.contract} (non-authoritative / read-only)",
        f"Matched accepted claims: {brief.matched_claim_count} / {brief.accepted_claim_count}",
        f"Current Capability v9 overlay: {brief.current_capability_artifact_id or 'unavailable'}",
        "",
        "## Employer qualifications (exact accepted wording)",
    ]
    if not brief.source_requirements:
        lines.append("No matching qualification claim; this is not evidence of no demand.")
    for fact in brief.source_requirements:
        lines.extend([
            f"- [{fact.ref}] {fact.statement}",
            f"  - Claim strength: {fact.strength or 'unestablished'}; "
            f"explicit depth: {fact.explicit_depth or 'not established'}",
            "  - Potential alternatives: " + (
                "review required" if fact.potential_alternatives else "not mechanically flagged"
            ),
            f"  - Exact claim: {fact.exact_claim_url}",
            f"  - Source: {fact.job_source_url}",
        ])
    lines.extend(["", "## Directly stated work (exact accepted wording)"])
    if not brief.source_responsibilities:
        lines.append("No matching direct duty; do not infer one from qualifications.")
    for fact in brief.source_responsibilities:
        lines.extend([
            f"- [{fact.ref}] {fact.statement}",
            f"  - Exact claim: {fact.exact_claim_url}",
            f"  - Source: {fact.job_source_url}",
            f"  - Reviewed concept: {fact.concept_id or 'not mapped'}",
        ])
    lines.extend(["", "## Questions to verify (candidate guidance, not job claims)"])
    for question in brief.questions:
        lines.append(
            f"- {question.question} "
            f"[basis: {', '.join(question.supporting_refs) or 'scope unknown'}]"
        )
    lines.extend(["", "## Boundaries", brief.limitation, brief.grouping_notice, ""])
    return "\n".join(lines)
