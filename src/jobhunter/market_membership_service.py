"""I3 membership qualification over fresh I2 eligibility and exact evidence identities.

This service never acquires sources, generates translations/P1.6, accepts P1.6, or
publishes Market state. Calls operate on one target candidate at a time; the later
run coordinator owns bounded batches and failure ledgers.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any

from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.market_affected_work import MarketAffectedWorkPlanner, MarketCandidateAffectedWork
from jobhunter.market_membership_inference import (
    MEMBERSHIP_SYSTEM_PROMPT,
    LMStudioMembershipProvider,
    MembershipProvider,
)
from jobhunter.market_membership_models import (
    MARKET_MEMBERSHIP_CONTRACT_VERSION,
    MARKET_MEMBERSHIP_PROMPT_VERSION,
    MarketMembershipDecision,
)
from jobhunter.market_models import MarketDefinitionSpec, MarketJobMembership
from jobhunter.market_store import MarketStore
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import build_translation_service
from jobhunter.translation_store import TranslationStore

_SOURCE_FIELDS = (
    "title",
    "description",
    "skills",
    "job_category",
    "location",
    "employment_type",
    "minimum_experience",
    "education",
    "work_arrangement",
    "seniority",
)
# Only unambiguous single structured employment values support a cheap exclusion.
# Free-form/composite values, geographic scopes, seniority, and keyword hints remain semantic.
_EMPLOYMENT_VALUES = {
    "full time": "full_time",
    "full-time": "full_time",
    "full_time": "full_time",
    "تمام وقت": "full_time",
    "part time": "part_time",
    "part-time": "part_time",
    "part_time": "part_time",
    "پاره وقت": "part_time",
}


class MarketMembershipError(ValueError):
    """Integrity or eligibility failure; must never persist as an uncertain decision."""


class MarketMembershipUnavailableError(RuntimeError):
    """Missing model configuration; distinct from interpretive uncertainty."""


@dataclass(frozen=True, slots=True)
class MarketMembershipResult:
    membership: MarketJobMembership
    outcome: str


@dataclass(frozen=True, slots=True)
class _Evidence:
    candidate: MarketCandidateAffectedWork
    target: MarketDefinitionSpec
    refs: dict[str, Any]
    translation_id: int | None
    analysis_id: int | None


def _norm(value: str) -> str:
    return " ".join(value.casefold().replace("\u200c", " ").split())


def _decision_from_constraints(evidence: _Evidence) -> MarketMembershipDecision | None:
    expected = _EMPLOYMENT_VALUES.get(_norm(evidence.target.employment_type_scope or ""))
    actual_text = evidence.refs.get("source:employment_type")
    actual = _EMPLOYMENT_VALUES.get(_norm(actual_text)) if isinstance(actual_text, str) else None
    # If the description advertises the alternative too, the structured value isn't enough.
    description = _norm(str(evidence.refs.get("source:description", "")))
    alternative_mentioned = any(
        value == expected and _norm(label) in description
        for label, value in _EMPLOYMENT_VALUES.items()
    )
    if expected and actual and actual != expected and not alternative_mentioned:
        return MarketMembershipDecision(
            disposition="excluded",
            confidence="high",
            reason=f"Structured employment type {actual_text!r} conflicts with target "
            f"employment scope {evidence.target.employment_type_scope!r}.",
            evidence_refs=["source:employment_type"],
        )
    return None


def _validate_decision(decision: MarketMembershipDecision, refs: dict[str, Any]) -> None:
    unknown = set(decision.evidence_refs) - refs.keys()
    if unknown:
        raise MarketMembershipError(f"Unknown membership evidence references: {sorted(unknown)}")
    if decision.disposition == "core_match" and not any(
        ref in {"source:description", "english:description"}
        or ref.startswith(("p16:responsibilities:", "p16:role_purpose:", "p16:requirements:"))
        for ref in decision.evidence_refs
    ):
        raise MarketMembershipError(
            "Core membership requires substantive evidence, not title/skills"
        )


class MarketMembershipService:
    def __init__(
        self,
        *,
        planner: MarketAffectedWorkPlanner,
        market_store: MarketStore,
        translation_store: TranslationStore,
        analysis_store: AnalysisStore,
        provider: MembershipProvider | None,
        clock=lambda: datetime.now(UTC),
    ) -> None:
        self._planner = planner
        self._market = market_store
        self._translations = translation_store
        self._analyses = analysis_store
        self._provider = provider
        self._clock = clock

    def _candidate(
        self,
        definition_id: int,
        job_id: str,
        refresh_after_hours: float,
    ) -> MarketCandidateAffectedWork:
        # Re-evaluate I2 at use time instead of trusting a caller's stale/forged plan flags.
        plan = self._planner.plan(
            target_definition_version_id=definition_id,
            candidate_source_job_ids=(job_id,),
            missing_limit=0,
            refresh_limit=0,
            refresh_after_hours=refresh_after_hours,
            translation_limit=0,
            analysis_limit=0,
        )
        if not plan.candidates or not plan.candidates[0].source_eligible:
            raise MarketMembershipError("Membership requires an I2 source-eligible candidate")
        return plan.candidates[0]

    def _evidence(
        self,
        definition_id: int,
        job_id: str,
        refresh_after_hours: float,
        *,
        enrich: bool,
    ) -> _Evidence:
        candidate = self._candidate(definition_id, job_id, refresh_after_hours)
        definition = self._market.get_definition_version(definition_id)
        source = self._translations.latest_source_version(job_id)
        if (
            definition is None
            or source is None
            or (source.job_detail_version_id != candidate.job_detail_version_id)
        ):
            raise MarketMembershipError("Source/target identity changed during evidence loading")
        refs = {
            f"source:{key}": source.fields[key] for key in _SOURCE_FIELDS if source.fields.get(key)
        }
        translation_id = None
        analysis_id = None
        if enrich and candidate.translation_artifact_id is not None:
            translation = self._translations.artifact_by_id(candidate.translation_artifact_id)
            if (
                translation is None
                or translation.job_detail_version_id != source.job_detail_version_id
            ):
                raise MarketMembershipError("Current translation dependency is inconsistent")
            translation_id = translation.id
            refs.update(
                {
                    f"english:{key}": translation.fields[key]
                    for key in _SOURCE_FIELDS
                    if translation.fields.get(key)
                }
            )
            if candidate.analysis_review_status == "accepted":
                analysis = self._analyses.artifact_by_id(candidate.analysis_artifact_id)
                if (
                    analysis is None
                    or analysis.semantic_review_status != "accepted"
                    or (
                        analysis.translation_artifact_id != translation_id
                        or analysis.job_detail_version_id != source.job_detail_version_id
                    )
                ):
                    raise MarketMembershipError("Accepted P1.6 dependency is inconsistent")
                analysis_id = analysis.id
                for section in ("responsibilities", "role_purpose", "requirements"):
                    for index, item in enumerate(analysis.analysis.get(section, [])):
                        refs[f"p16:{section}:{index}"] = item
        if not refs:
            raise MarketMembershipError("Parsed source has no usable membership evidence")
        return _Evidence(candidate, definition.spec, refs, translation_id, analysis_id)

    def _assert_unchanged(
        self,
        evidence: _Evidence,
        definition_id: int,
        job_id: str,
        refresh_after_hours: float,
        *,
        enrich: bool,
    ) -> None:
        current = self._evidence(definition_id, job_id, refresh_after_hours, enrich=enrich)
        if (
            current.candidate.job_detail_version_id != evidence.candidate.job_detail_version_id
            or current.translation_id != evidence.translation_id
            or current.analysis_id != evidence.analysis_id
            or current.refs != evidence.refs
        ):
            raise MarketMembershipError("Membership evidence changed during qualification; replan")

    def qualify(
        self,
        *,
        target_definition_version_id: int,
        source_job_id: str,
        refresh_after_hours: float = 24,
    ) -> MarketMembershipResult:
        evidence = self._evidence(
            target_definition_version_id,
            source_job_id,
            refresh_after_hours,
            enrich=False,
        )
        decision = _decision_from_constraints(evidence)
        enrich = decision is None
        if decision is not None:
            method = "deterministic"
            identity = {"rules": "market-membership-constraints-v1"}
        else:
            if self._provider is None:
                raise MarketMembershipUnavailableError(
                    "A membership model is required for reasoning"
                )
            evidence = self._evidence(
                target_definition_version_id,
                source_job_id,
                refresh_after_hours,
                enrich=True,
            )
            method = "model"
            identity = {
                **self._provider.identity,
                "prompt": MARKET_MEMBERSHIP_PROMPT_VERSION,
                "schema": MARKET_MEMBERSHIP_CONTRACT_VERSION,
                "prompt_sha256": hashlib.sha256(MEMBERSHIP_SYSTEM_PROMPT.encode()).hexdigest(),
            }
        dependencies = dict(
            target_definition_version_id=target_definition_version_id,
            job_detail_version_id=evidence.candidate.job_detail_version_id,
            translation_artifact_id=evidence.translation_id,
            analysis_artifact_id=evidence.analysis_id,
            classifier_contract_version=MARKET_MEMBERSHIP_CONTRACT_VERSION,
            classifier_method=method,
            classifier_identity=identity,
        )
        existing = self._market.find_reusable_membership(**dependencies)
        if existing is not None:
            self._assert_unchanged(
                evidence,
                target_definition_version_id,
                source_job_id,
                refresh_after_hours,
                enrich=enrich,
            )
            return MarketMembershipResult(existing, "reused")
        if decision is None:
            # The acquisition envelope never enters the semantic target meaning.
            target = asdict(evidence.target)
            target = {
                key: target[key]
                for key in (
                    "membership_intent",
                    "include_hints",
                    "exclude_hints",
                    "geography_scope",
                    "work_arrangement_scope",
                    "seniority_scope",
                    "employment_type_scope",
                )
            }
            payload = {"target": target, "evidence": evidence.refs}
            if len(json.dumps(payload, ensure_ascii=False)) > 32000:
                raise MarketMembershipError(
                    "Membership input exceeds 32000 characters; not truncated"
                )
            decision = MarketMembershipDecision.model_validate(
                self._provider.classify(payload).model_dump()
            )
        _validate_decision(decision, evidence.refs)
        self._assert_unchanged(
            evidence,
            target_definition_version_id,
            source_job_id,
            refresh_after_hours,
            enrich=enrich,
        )
        membership = self._market.record_membership(
            **dependencies,
            disposition=decision.disposition,
            reason=decision.reason,
            evidence_refs=tuple(decision.evidence_refs),
            confidence=decision.confidence,
            created_at=self._clock(),
        )
        return MarketMembershipResult(membership, "completed")

    def correct(
        self,
        membership_id: int,
        *,
        decision: MarketMembershipDecision,
        review_note: str,
        refresh_after_hours: float = 24,
    ) -> MarketMembershipResult:
        """Explicit reviewed correction, preserving the exact classifier/evidence lineage."""
        if not review_note.strip() or len(review_note) > 1200:
            raise MarketMembershipError("A bounded review note is required for correction")
        previous = self._market.get_membership(membership_id)
        if previous is None:
            raise LookupError(f"Unknown membership {membership_id}")
        decision = MarketMembershipDecision.model_validate(decision.model_dump())
        evidence = self._evidence(
            previous.target_definition_version_id,
            previous.source_job_id,
            refresh_after_hours,
            enrich=previous.classifier_method == "model",
        )
        if (
            evidence.candidate.job_detail_version_id,
            evidence.translation_id,
            evidence.analysis_id,
        ) != (
            previous.job_detail_version_id,
            previous.translation_artifact_id,
            previous.analysis_artifact_id,
        ):
            raise MarketMembershipError(
                "Correction requires the same current evidence dependencies"
            )
        dependencies = dict(
            target_definition_version_id=previous.target_definition_version_id,
            job_detail_version_id=previous.job_detail_version_id,
            translation_artifact_id=previous.translation_artifact_id,
            analysis_artifact_id=previous.analysis_artifact_id,
            classifier_contract_version=previous.classifier_contract_version,
            classifier_method=previous.classifier_method,
            classifier_identity=previous.classifier_identity,
        )
        latest = self._market.find_reusable_membership(**dependencies)
        if latest is None or latest.id != membership_id:
            raise MarketMembershipError(
                "Correct the latest membership decision, not superseded history"
            )
        _validate_decision(decision, evidence.refs)
        self._assert_unchanged(
            evidence,
            previous.target_definition_version_id,
            previous.source_job_id,
            refresh_after_hours,
            enrich=previous.classifier_method == "model",
        )
        corrected = self._market.record_membership(
            **dependencies,
            disposition=decision.disposition,
            reason=f"Reviewed correction: {review_note.strip()}\n{decision.reason}",
            evidence_refs=tuple(decision.evidence_refs),
            confidence=decision.confidence,
            supersedes_membership_id=membership_id,
            created_at=self._clock(),
        )
        return MarketMembershipResult(corrected, "corrected")


def build_market_membership_service(
    settings: Settings,
    *,
    membership_model: str | None = None,
) -> MarketMembershipService:
    """Compose existing currentness owners; construction makes no network/model calls.

    Use the configured analysis model by default, with an explicit role override for
    callers. Public browser/CLI orchestration remains I6 scope.
    """
    translations = TranslationStore(settings.database_path)
    analyses = AnalysisStore(settings.database_path)
    market = MarketStore(settings.database_path)
    model = membership_model or settings.effective_analysis_lm_studio_model()
    provider = (
        LMStudioMembershipProvider(
            base_url=settings.lm_studio_base_url,
            model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
        )
        if model
        else None
    )
    planner = MarketAffectedWorkPlanner(
        market_store=market,
        source_store=JobHunterStore(settings.database_path),
        observations=JobDetailObservationStore(settings.database_path),
        translation_store=translations,
        translation_service=build_translation_service(settings),
        analysis_store=analyses,
        analysis_model=settings.effective_analysis_lm_studio_model(),
    )
    return MarketMembershipService(
        planner=planner,
        market_store=market,
        translation_store=translations,
        analysis_store=analyses,
        provider=provider,
    )
