"""P2.2A Job Work Intelligence v1 service.

Strict authority stops at the accepted/current English P1.6 artifact. Above that boundary this
service produces transparent candidate interpretation, validates exact source references, and
persists the result for repeatable local UX without promoting it into canonical taxonomy.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from jobhunter.analysis_current import ENGLISH_ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisArtifact, AnalysisStore
from jobhunter.config import Settings
from jobhunter.translation_service import TranslationService, build_translation_service
from jobhunter.translation_store import TranslationStore
from jobhunter.work_intelligence_inference import (
    WorkIntelligenceInferenceProvider,
    WorkIntelligenceInferenceResult,
)
from jobhunter.work_intelligence_models import JobWorkIntelligence
from jobhunter.work_intelligence_store import JobWorkIntelligenceArtifact, WorkIntelligenceStore

WORK_INTELLIGENCE_CONTRACT_VERSION = "job-work-intelligence-v1"
WORK_INTELLIGENCE_PROMPT_VERSION = "job-work-intelligence-v1.3"
WORK_INTELLIGENCE_SCHEMA_VERSION = WORK_INTELLIGENCE_CONTRACT_VERSION
DETERMINISTIC_LIMITED_MODEL = "jobhunter-deterministic-limited-work-v1"

_SCOPE_INTENSIFIERS = (
    "end-to-end",
    "end to end",
    "full lifecycle",
    "whole lifecycle",
    "entire lifecycle",
    "complete lifecycle",
    "entire security stack",
    "whole security stack",
)

_WORK_INTELLIGENCE_PROMPT = """You are JobHunter's Job Work Intelligence interpreter.

Your job is to help a user understand what the supplied vacancy actually involves faster than
reading and mentally synthesizing every responsibility.

AUTHORITY
- The supplied P1.6 responsibilities and role_purpose items are accepted factual substrate.
- A responsibility/role_purpose `statement` defines the accepted work claim. Its `evidence` may be
  a larger shared source sentence containing neighboring clauses, examples, or equipment names.
  Do not transfer details from one neighboring clause into a different responsibility unless the
  accepted statement itself supports that scope.
- Preserve action strength and responsibility relationship from the accepted direct-work
  statements. Do not upgrade advisory, collaborative, transitional, or solution-provision wording
  into stronger execution or ownership claims. For example, `develop/provide` is not automatically
  `implement`, and `partner to move toward production` is not automatically `deploy` or own
  production deployment.
- Requirements are supporting context only. A requirement must NEVER become a duty by itself or
  supply a stronger action verb, ownership claim, or lifecycle stage than the direct-work
  statements establish.
- Your output is JobHunter interpretation, not employer wording and not promoted taxonomy.

WORK THEMES
- Group the direct work into a small useful set of themes, normally 2-6.
- Every supplied responsibility index and role-purpose index must appear in at least one theme.
- A work item may belong to two themes when genuinely hybrid; avoid gratuitous duplication.
- Use theme IDs theme-1, theme-2, ... and relative emphasis primary/supporting/uncertain.
- Do not invent percentages, time allocation, ownership, leadership, autonomy, or lifecycle scope.
- Do not use scope intensifiers such as `end-to-end`, `full lifecycle`, or `entire security stack`
  unless that scope is explicit in a supplied responsibility or role-purpose statement.

DELIVERABLES
- Include only outputs that are source-explicit or strongly implied by the supplied work itself.
- Do not infer deliverables from generic knowledge of a tool, title, or profession.

ROLE INTERPRETATION
- A candidate role label/summary is allowed when it clarifies the work composition.
- It is tentative analytical interpretation, not a canonical role archetype.
- Expose alternatives/limitations when the evidence supports more than one reading.

UNCERTAINTY
- Ambiguity should lower confidence or create alternatives/limitations, not force false certainty.
- Do not manufacture uncertainty merely to fill fields.

Use only the supplied zero-based indices as references. Do not cite or invent any other source.
"""

_SEMANTIC_REPAIR_PROMPT = """

BOUNDED SEMANTIC REPAIR
JobHunter rejected the previous candidate after structured generation because of this exact
post-generation validation error:

{error}

Generate one fresh candidate from the same supplied evidence. Correct the cited boundary while
preserving useful supported grouping. Do not weaken, guess, clamp, or omit structured source
references. Do not invent new duties, stronger action ownership, lifecycle scope, or unsupported
source details. This is the only post-validation semantic repair attempt.
"""

_AUTHORITY_REVIEW_PROMPT = """You are JobHunter's final semantic authority reviewer for one
candidate Job Work Intelligence document.

The draft has already been generated from accepted P1.6 work evidence and has passed structural
reference checks. Your task is NOT to redesign the grouping. Audit the draft specifically for
semantic authority inflation, then return the full corrected JobWorkIntelligence document.

REVIEW BOUNDARY
- Accepted responsibility and role-purpose `statement` values are the direct-work authority.
- Supporting requirements are context only and cannot create a duty or strengthen an action.
- Preserve the draft's useful theme boundaries, theme IDs, emphasis, confidence, and structured
  references unless a wording correction itself requires a minimal adjustment.
- Prefer minimal prose rewrites over regrouping.
- Do not add new duties, deliverables, role interpretations, lifecycle stages, ownership, or scope.
- Do not turn advisory, collaborative, transitional, or solution-provision wording into stronger
  execution claims.
- `develop/provide` must not silently become `implement`.
- `partner/collaborate to move models toward production` must not silently become direct
  `deploying models` or ownership of production deployment.
- Requirements such as `model deployment` may clarify the domain but cannot override the weaker
  direct-work relationship.
- Remove or soften unsupported words such as ownership/lifecycle intensifiers when direct work
  does not establish them.
- If the draft is already bounded, preserve it rather than rewriting for style.

Return only the corrected full structured JobWorkIntelligence document using the supplied
zero-based references.
"""


class WorkIntelligenceError(ValueError):
    """Raised when P2.2A cannot safely produce or persist Work Intelligence."""


@dataclass(frozen=True, slots=True)
class WorkIntelligenceResult:
    source_job_id: str
    artifact_id: int
    outcome: str
    model: str
    evidence_status: str
    work_theme_count: int


def _source_evidence(item: dict[str, Any]) -> list[str]:
    raw = item.get("evidence")
    values = raw if isinstance(raw, list) else [raw]
    return [value.strip() for value in values if isinstance(value, str) and value.strip()]


def _work_fact(index: int, item: Any, *, section: str) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise WorkIntelligenceError(f"Accepted P1.6 {section}[{index}] is not an object")
    statement = item.get("statement")
    if not isinstance(statement, str) or not statement.strip():
        raise WorkIntelligenceError(
            f"Accepted P1.6 {section}[{index}] has no usable statement"
        )
    return {
        "index": index,
        "statement": statement.strip(),
        "evidence": _source_evidence(item),
        "confidence": item.get("confidence"),
    }


def _requirement_fact(index: int, item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise WorkIntelligenceError(f"Accepted P1.6 requirement[{index}] is not an object")
    concept = item.get("concept")
    if not isinstance(concept, str) or not concept.strip():
        raise WorkIntelligenceError(
            f"Accepted P1.6 requirement[{index}] has no usable concept"
        )
    return {
        "index": index,
        "concept": concept.strip(),
        "concept_type": item.get("concept_type"),
        "requirement_type": item.get("requirement_type"),
        "depth_signal": item.get("depth_signal"),
        "evidence": _source_evidence(item),
        "confidence": item.get("confidence"),
    }


def _limited_intelligence() -> JobWorkIntelligence:
    return JobWorkIntelligence(
        evidence_status="limited",
        work_summary=(
            "The accepted job analysis contains no direct responsibility or role-purpose evidence, "
            "so JobHunter will not invent duties from qualifications alone."
        ),
        work_themes=[],
        deliverables=[],
        role_interpretation=None,
        limitations=[
            "Direct work structure is unavailable from the accepted vacancy evidence; requirements "
            "can describe candidate expectations but are not treated as job duties."
        ],
    )


def _normalized_semantic_text(value: str) -> str:
    return " ".join(
        value.casefold().replace("–", " ").replace("—", " ").replace("-", " ").split()
    )


def _direct_work_statement_text(responsibilities: list[Any], role_purpose: list[Any]) -> str:
    statements: list[str] = []
    for item in [*responsibilities, *role_purpose]:
        if isinstance(item, dict):
            statement = item.get("statement")
            if isinstance(statement, str) and statement.strip():
                statements.append(statement)
    return _normalized_semantic_text(" ".join(statements))


def _candidate_scope_text(intelligence: JobWorkIntelligence) -> str:
    values = [intelligence.work_summary]
    for theme in intelligence.work_themes:
        values.extend([theme.label, theme.summary])
    for deliverable in intelligence.deliverables:
        values.extend([deliverable.label, deliverable.summary])
    if intelligence.role_interpretation is not None:
        values.extend(
            [
                intelligence.role_interpretation.label,
                intelligence.role_interpretation.summary,
            ]
        )
    return _normalized_semantic_text(" ".join(values))


def _validate_scope_language(
    intelligence: JobWorkIntelligence,
    *,
    responsibilities: list[Any],
    role_purpose: list[Any],
) -> None:
    """Reject unsupported lifecycle/scope amplification without constraining normal semantics."""

    source_text = _direct_work_statement_text(responsibilities, role_purpose)
    candidate_text = _candidate_scope_text(intelligence)
    unsupported = [
        phrase
        for phrase in _SCOPE_INTENSIFIERS
        if _normalized_semantic_text(phrase) in candidate_text
        and _normalized_semantic_text(phrase) not in source_text
    ]
    if unsupported:
        raise WorkIntelligenceError(
            "Work Intelligence introduced unsupported lifecycle/scope intensifier(s): "
            + ", ".join(sorted(set(unsupported)))
        )


class WorkIntelligenceService:
    """Build or reuse one candidate Work Intelligence artifact above accepted English P1.6."""

    def __init__(
        self,
        *,
        source_store: TranslationStore,
        analysis_store: AnalysisStore,
        work_store: WorkIntelligenceStore,
        translation_service: TranslationService,
        analysis_model: str,
        work_model: str | None,
        provider: WorkIntelligenceInferenceProvider | None,
        max_tokens: int = 8192,
        clock=lambda: datetime.now(UTC),
    ) -> None:
        if not analysis_model.strip():
            raise ValueError("A concrete accepted English P1.6 analysis model is required")
        if not 1 <= max_tokens <= 32768:
            raise ValueError("max_tokens must be between 1 and 32768")
        self._source_store = source_store
        self._analysis_store = analysis_store
        self._work_store = work_store
        self._translation_service = translation_service
        self._analysis_model = analysis_model.strip()
        self._work_model = work_model.strip() if work_model else None
        self._provider = provider
        self._max_tokens = max_tokens
        self._clock = clock

    def _current_p16(self, source_job_id: str) -> AnalysisArtifact:
        source = self._source_store.latest_source_version(source_job_id)
        if source is None:
            raise WorkIntelligenceError("Job has no current successfully parsed source version")
        translation = self._translation_service.current_artifact(source_job_id)
        if translation is None:
            raise WorkIntelligenceError(
                "Job has no configured current English projection; translate/repair it first"
            )
        analysis = self._analysis_store.find_artifact(
            job_detail_version_id=source.job_detail_version_id,
            translation_artifact_id=translation.id,
            require_translation_dependency=True,
            model=self._analysis_model,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        )
        if analysis is None or analysis.semantic_review_status != "accepted":
            raise WorkIntelligenceError(
                "Job has no semantically accepted current English P1.6 analysis"
            )
        if analysis.job_detail_version_id != source.job_detail_version_id:
            raise WorkIntelligenceError("Accepted English P1.6 is stale for the current source")
        if analysis.translation_artifact_id != translation.id:
            raise WorkIntelligenceError(
                "Accepted English P1.6 does not depend on the current English projection"
            )
        return analysis

    @staticmethod
    def _sections(analysis: AnalysisArtifact) -> tuple[list[Any], list[Any], list[Any]]:
        value = analysis.analysis
        responsibilities = value.get("responsibilities") or []
        role_purpose = value.get("role_purpose") or []
        requirements = value.get("requirements") or []
        if not isinstance(responsibilities, list):
            raise WorkIntelligenceError("Accepted P1.6 responsibilities are not a list")
        if not isinstance(role_purpose, list):
            raise WorkIntelligenceError("Accepted P1.6 role_purpose is not a list")
        if not isinstance(requirements, list):
            raise WorkIntelligenceError("Accepted P1.6 requirements are not a list")
        return responsibilities, role_purpose, requirements

    @staticmethod
    def _validate_references(
        intelligence: JobWorkIntelligence,
        *,
        responsibility_count: int,
        role_purpose_count: int,
        requirement_count: int,
    ) -> None:
        def validate(values: list[int], count: int, label: str) -> None:
            invalid = [value for value in values if value >= count]
            if invalid:
                raise WorkIntelligenceError(
                    f"Work Intelligence references missing {label} indices: {invalid}"
                )

        # When a source section is structurally empty, there is no possible semantic target for a
        # model-emitted reference into that section. Removing only those impossible references is a
        # deterministic normalization, not a semantic remap. References into non-empty sections
        # are never clamped, guessed, or reassigned; ordinary bounds validation still rejects them.
        covered_responsibilities: set[int] = set()
        covered_purpose: set[int] = set()
        for theme in intelligence.work_themes:
            if responsibility_count == 0:
                theme.responsibility_indices.clear()
            if role_purpose_count == 0:
                theme.role_purpose_indices.clear()
            if requirement_count == 0:
                theme.supporting_requirement_indices.clear()
            if not theme.responsibility_indices and not theme.role_purpose_indices:
                raise WorkIntelligenceError(
                    "Work theme has no valid direct work references after removing references to "
                    "absent source sections"
                )
            validate(theme.responsibility_indices, responsibility_count, "responsibility")
            validate(theme.role_purpose_indices, role_purpose_count, "role-purpose")
            validate(theme.supporting_requirement_indices, requirement_count, "requirement")
            covered_responsibilities.update(theme.responsibility_indices)
            covered_purpose.update(theme.role_purpose_indices)
        for deliverable in intelligence.deliverables:
            if responsibility_count == 0:
                deliverable.responsibility_indices.clear()
            if role_purpose_count == 0:
                deliverable.role_purpose_indices.clear()
            if not deliverable.responsibility_indices and not deliverable.role_purpose_indices:
                raise WorkIntelligenceError(
                    "Deliverable has no valid direct work references after removing references to "
                    "absent source sections"
                )
            validate(deliverable.responsibility_indices, responsibility_count, "responsibility")
            validate(deliverable.role_purpose_indices, role_purpose_count, "role-purpose")

        if intelligence.evidence_status == "sufficient":
            expected_responsibilities = set(range(responsibility_count))
            expected_purpose = set(range(role_purpose_count))
            missing_responsibilities = sorted(
                expected_responsibilities - covered_responsibilities
            )
            missing_purpose = sorted(expected_purpose - covered_purpose)
            if missing_responsibilities or missing_purpose:
                raise WorkIntelligenceError(
                    "Work themes omitted accepted direct work evidence: "
                    f"responsibilities={missing_responsibilities}, "
                    f"role_purpose={missing_purpose}"
                )

    @staticmethod
    def _document_from_inference(
        inference: WorkIntelligenceInferenceResult,
    ) -> JobWorkIntelligence:
        if inference.validated_model is not None:
            if not isinstance(inference.validated_model, JobWorkIntelligence):
                raise WorkIntelligenceError(
                    "Work Intelligence provider returned an incompatible validated model"
                )
            document = inference.validated_model
        else:
            document = JobWorkIntelligence.model_validate(inference.intelligence)
        if document.evidence_status != "sufficient":
            raise WorkIntelligenceError(
                "Direct accepted work evidence requires evidence_status='sufficient'"
            )
        return document

    def _validate_generated_document(
        self,
        document: JobWorkIntelligence,
        *,
        responsibilities: list[Any],
        role_purpose: list[Any],
        requirements: list[Any],
    ) -> None:
        self._validate_references(
            document,
            responsibility_count=len(responsibilities),
            role_purpose_count=len(role_purpose),
            requirement_count=len(requirements),
        )
        _validate_scope_language(
            document,
            responsibilities=responsibilities,
            role_purpose=role_purpose,
        )

    def _authority_review_candidate(
        self,
        *,
        document: JobWorkIntelligence,
        user_payload: dict[str, Any],
        responsibilities: list[Any],
        role_purpose: list[Any],
        requirements: list[Any],
        generation_request_body: dict[str, Any],
        generation_raw_response: dict[str, Any],
    ) -> tuple[JobWorkIntelligence, dict[str, Any], dict[str, Any]]:
        """Run one semantic authority audit before persisting a direct-work candidate."""

        if self._provider is None:
            raise WorkIntelligenceError("Work Intelligence provider is unavailable")

        review_payload = {
            "source_job_id": user_payload.get("source_job_id"),
            "analysis_artifact_id": user_payload.get("analysis_artifact_id"),
            "responsibilities": user_payload.get("responsibilities", []),
            "role_purpose": user_payload.get("role_purpose", []),
            "supporting_requirements": user_payload.get("supporting_requirements", []),
            "candidate": document.model_dump(mode="json"),
        }
        inference = self._provider.complete(
            response_model=JobWorkIntelligence,
            system_prompt=_AUTHORITY_REVIEW_PROMPT,
            user_payload=review_payload,
            max_tokens=min(self._max_tokens, 4096),
            seed=1,
        )
        reviewed = self._document_from_inference(inference)
        self._validate_generated_document(
            reviewed,
            responsibilities=responsibilities,
            role_purpose=role_purpose,
            requirements=requirements,
        )
        return (
            reviewed,
            {
                "generation": generation_request_body,
                "authority_review": inference.request_body,
            },
            {
                "generation": generation_raw_response,
                "authority_review": inference.raw_response,
            },
        )

    def _generate_with_semantic_repair(
        self,
        *,
        user_payload: dict[str, Any],
        responsibilities: list[Any],
        role_purpose: list[Any],
        requirements: list[Any],
    ) -> tuple[JobWorkIntelligence, dict[str, Any], dict[str, Any]]:
        """Generate, repair one validation failure, then run one semantic authority review."""

        if self._provider is None:
            raise WorkIntelligenceError("Work Intelligence provider is unavailable")

        first_error: WorkIntelligenceError | None = None
        first_request_body: dict[str, Any] | None = None
        first_raw_response: dict[str, Any] | None = None
        system_prompt = _WORK_INTELLIGENCE_PROMPT

        for repair_attempt in range(2):
            inference = self._provider.complete(
                response_model=JobWorkIntelligence,
                system_prompt=system_prompt,
                user_payload=user_payload,
                max_tokens=min(self._max_tokens, 4096),
                seed=0,
            )
            document = self._document_from_inference(inference)
            try:
                self._validate_generated_document(
                    document,
                    responsibilities=responsibilities,
                    role_purpose=role_purpose,
                    requirements=requirements,
                )
            except WorkIntelligenceError as exc:
                if repair_attempt == 1:
                    raise
                first_error = exc
                first_request_body = inference.request_body
                first_raw_response = inference.raw_response
                system_prompt = _WORK_INTELLIGENCE_PROMPT + _SEMANTIC_REPAIR_PROMPT.format(
                    error=str(exc)
                )
                continue

            generation_request_body = inference.request_body
            generation_raw_response = inference.raw_response
            if first_error is not None:
                generation_request_body = dict(inference.request_body)
                generation_request_body["semantic_repair"] = {
                    "attempts": 1,
                    "trigger": str(first_error),
                    "initial_request_body": first_request_body,
                }
                generation_raw_response = {
                    "semantic_repair": {
                        "attempts": 1,
                        "trigger": str(first_error),
                        "initial_raw_response": first_raw_response,
                        "final_raw_response": inference.raw_response,
                    }
                }

            return self._authority_review_candidate(
                document=document,
                user_payload=user_payload,
                responsibilities=responsibilities,
                role_purpose=role_purpose,
                requirements=requirements,
                generation_request_body=generation_request_body,
                generation_raw_response=generation_raw_response,
            )

        raise WorkIntelligenceError("Bounded semantic repair exhausted without a candidate")

    def _identity_for(self, analysis: AnalysisArtifact) -> tuple[str, bool]:
        responsibilities, role_purpose, _ = self._sections(analysis)
        has_direct_work = bool(responsibilities or role_purpose)
        if not has_direct_work:
            return DETERMINISTIC_LIMITED_MODEL, False
        if not self._work_model or self._provider is None:
            raise WorkIntelligenceError(
                "Direct work evidence exists but no Work Intelligence LM Studio model is configured"
            )
        return self._work_model, True

    def current_artifact(self, source_job_id: str) -> JobWorkIntelligenceArtifact | None:
        """Return an artifact only when it depends on the exact current accepted P1.6 artifact."""

        try:
            analysis = self._current_p16(source_job_id)
            model, _ = self._identity_for(analysis)
        except WorkIntelligenceError:
            return None
        return self._work_store.find_artifact(
            analysis_artifact_id=analysis.id,
            model=model,
            prompt_version=WORK_INTELLIGENCE_PROMPT_VERSION,
            schema_version=WORK_INTELLIGENCE_SCHEMA_VERSION,
        )

    def analyze_job(self, source_job_id: str) -> WorkIntelligenceResult:
        source_job_id = source_job_id.strip()
        if not source_job_id:
            raise WorkIntelligenceError("source_job_id must not be empty")
        analysis = self._current_p16(source_job_id)
        responsibilities, role_purpose, requirements = self._sections(analysis)
        model, use_model = self._identity_for(analysis)
        attempted_at = self._clock()

        existing = self._work_store.find_artifact(
            analysis_artifact_id=analysis.id,
            model=model,
            prompt_version=WORK_INTELLIGENCE_PROMPT_VERSION,
            schema_version=WORK_INTELLIGENCE_SCHEMA_VERSION,
        )
        if existing is not None:
            self._work_store.record_attempt(
                analysis_artifact_id=analysis.id,
                attempted_at=attempted_at,
                model=model,
                prompt_version=WORK_INTELLIGENCE_PROMPT_VERSION,
                schema_version=WORK_INTELLIGENCE_SCHEMA_VERSION,
                outcome="reused",
                artifact_id=existing.id,
            )
            document = JobWorkIntelligence.model_validate(existing.intelligence)
            return WorkIntelligenceResult(
                source_job_id=source_job_id,
                artifact_id=existing.id,
                outcome="reused",
                model=existing.model,
                evidence_status=document.evidence_status,
                work_theme_count=len(document.work_themes),
            )

        try:
            if not use_model:
                document = _limited_intelligence()
                request_body = {
                    "contract": WORK_INTELLIGENCE_CONTRACT_VERSION,
                    "mode": "deterministic-limited-work-boundary",
                    "analysis_artifact_id": analysis.id,
                }
                raw_response = {"deterministic": True, "reason": "no_direct_work_evidence"}
                self._validate_generated_document(
                    document,
                    responsibilities=responsibilities,
                    role_purpose=role_purpose,
                    requirements=requirements,
                )
            else:
                user_payload = {
                    "source_job_id": source_job_id,
                    "analysis_artifact_id": analysis.id,
                    "responsibilities": [
                        _work_fact(index, item, section="responsibility")
                        for index, item in enumerate(responsibilities)
                    ],
                    "role_purpose": [
                        _work_fact(index, item, section="role_purpose")
                        for index, item in enumerate(role_purpose)
                    ],
                    "supporting_requirements": [
                        _requirement_fact(index, item)
                        for index, item in enumerate(requirements)
                    ],
                }
                document, request_body, raw_response = self._generate_with_semantic_repair(
                    user_payload=user_payload,
                    responsibilities=responsibilities,
                    role_purpose=role_purpose,
                    requirements=requirements,
                )

            artifact_id = self._work_store.record_artifact(
                analysis_artifact_id=analysis.id,
                model=model,
                prompt_version=WORK_INTELLIGENCE_PROMPT_VERSION,
                schema_version=WORK_INTELLIGENCE_SCHEMA_VERSION,
                intelligence=document.model_dump(mode="json"),
                request_body=request_body,
                raw_response=raw_response,
                created_at=attempted_at,
            )
            self._work_store.record_attempt(
                analysis_artifact_id=analysis.id,
                attempted_at=attempted_at,
                model=model,
                prompt_version=WORK_INTELLIGENCE_PROMPT_VERSION,
                schema_version=WORK_INTELLIGENCE_SCHEMA_VERSION,
                outcome="completed",
                artifact_id=artifact_id,
            )
        except Exception as exc:
            self._work_store.record_attempt(
                analysis_artifact_id=analysis.id,
                attempted_at=attempted_at,
                model=model,
                prompt_version=WORK_INTELLIGENCE_PROMPT_VERSION,
                schema_version=WORK_INTELLIGENCE_SCHEMA_VERSION,
                outcome="failed",
                error=exc,
            )
            raise

        return WorkIntelligenceResult(
            source_job_id=source_job_id,
            artifact_id=artifact_id,
            outcome="completed",
            model=model,
            evidence_status=document.evidence_status,
            work_theme_count=len(document.work_themes),
        )


def build_work_intelligence_service(settings: Settings) -> WorkIntelligenceService:
    """Build the current P2.2A service without making Work Intelligence canonical authority."""

    analysis_model = settings.effective_analysis_lm_studio_model()
    if not analysis_model:
        raise ValueError("No analysis model is configured for accepted English P1.6")

    # P2.2A currently uses the stronger accepted analysis reasoning role for both generation and
    # its final semantic authority review. Real-local evidence showed that the smaller Capability
    # model produced useful grouping but repeatedly preserved action-authority inflation even after
    # an explicit review pass. Model identity is already part of artifact currentness, so existing
    # 2B artifacts remain immutable history and are not reused as current 4B results.
    work_model = analysis_model
    provider = None
    if work_model:
        provider = WorkIntelligenceInferenceProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=work_model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            network_retries=settings.inference_max_retries,
            validation_retries=1,
        )
    return WorkIntelligenceService(
        source_store=TranslationStore(settings.database_path),
        analysis_store=AnalysisStore(settings.database_path),
        work_store=WorkIntelligenceStore(settings.database_path),
        translation_service=build_translation_service(settings),
        analysis_model=analysis_model,
        work_model=work_model,
        provider=provider,
        max_tokens=settings.analysis_max_tokens,
    )


def format_work_intelligence(artifact: JobWorkIntelligenceArtifact) -> str:
    document = JobWorkIntelligence.model_validate(artifact.intelligence)
    lines = [
        f"Job Work Intelligence: {artifact.source_job_id}",
        f"State: {artifact.semantic_state} / {document.evidence_status}",
        f"Model: {artifact.model}",
        f"P1.6 dependency: artifact {artifact.analysis_artifact_id}",
        "",
        document.work_summary,
    ]
    if document.work_themes:
        lines.append("\nWork themes:")
        for theme in document.work_themes:
            lines.append(
                f"- {theme.label} [{theme.emphasis}, {theme.confidence}] — {theme.summary}"
            )
    if document.deliverables:
        lines.append("\nLikely deliverables:")
        for item in document.deliverables:
            lines.append(f"- {item.label} [{item.status}, {item.confidence}] — {item.summary}")
    if document.role_interpretation is not None:
        role = document.role_interpretation
        lines.extend(
            [
                "\nCandidate role interpretation:",
                f"- {role.label} [{role.confidence}] — {role.summary}",
            ]
        )
    if document.limitations:
        lines.append("\nLimitations:")
        lines.extend(f"- {item}" for item in document.limitations)
    return "\n".join(lines)


__all__ = [
    "DETERMINISTIC_LIMITED_MODEL",
    "WORK_INTELLIGENCE_CONTRACT_VERSION",
    "WORK_INTELLIGENCE_PROMPT_VERSION",
    "WORK_INTELLIGENCE_SCHEMA_VERSION",
    "WorkIntelligenceError",
    "WorkIntelligenceResult",
    "WorkIntelligenceService",
    "build_work_intelligence_service",
    "format_work_intelligence",
]
