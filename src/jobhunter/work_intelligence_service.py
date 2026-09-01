"""P2.2A Job Work Intelligence v2 service.

Accepted/current English P1.6 remains the factual authority. The model proposes bounded job-level
grouping and interpretation; application code validates those references and deterministically
injects the exact accepted P1.6 work statements before persistence.
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
from jobhunter.work_intelligence_models import (
    AcceptedWorkItem,
    CandidateJobWorkIntelligence,
    DeliverableCandidate,
    JobWorkIntelligence,
    WorkTheme,
)
from jobhunter.work_intelligence_store import JobWorkIntelligenceArtifact, WorkIntelligenceStore

WORK_INTELLIGENCE_CONTRACT_VERSION = "job-work-intelligence-v2"
WORK_INTELLIGENCE_PROMPT_VERSION = "job-work-intelligence-v2.0"
WORK_INTELLIGENCE_SCHEMA_VERSION = WORK_INTELLIGENCE_CONTRACT_VERSION
DETERMINISTIC_LIMITED_MODEL = "jobhunter-deterministic-limited-work-v2"

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

_WORK_INTELLIGENCE_PROMPT = """You are JobHunter's Job Work Intelligence candidate interpreter.

Your job is to help a user understand how the supplied accepted work is organized. You are NOT the
authority for the factual wording of that work. JobHunter will deterministically inject the exact
accepted P1.6 statements after your structured references pass validation.

AUTHORITY
- The supplied P1.6 responsibilities and role_purpose items are accepted factual substrate.
- Use their zero-based indices to organize work; do not attempt to replace their statements.
- Requirements are supporting context only. A requirement must NEVER become a duty by itself or
  supply stronger action, ownership, autonomy, or lifecycle scope.
- Your labels, emphasis, confidence, rationales, deliverable candidates, and role interpretation
  are JobHunter analytical interpretation, not employer wording and not promoted taxonomy.
- Do not produce a general work summary or paraphrased factual work description.

WORK THEMES
- Group the direct work into a small useful set of themes, normally 2-6.
- Every supplied responsibility index and role-purpose index must appear in at least one theme.
- A work item may belong to two themes when genuinely hybrid; avoid gratuitous duplication.
- Use theme IDs theme-1, theme-2, ... and relative emphasis primary/supporting/uncertain.
- Theme labels and optional rationales may interpret the grouping, but must not be presented as
  replacement factual work statements.
- Do not invent percentages, time allocation, ownership, leadership, autonomy, or lifecycle scope.
- Do not use scope intensifiers such as `end-to-end`, `full lifecycle`, or `entire security stack`
  unless that scope is explicit in a supplied responsibility or role-purpose statement.

DELIVERABLES
- Include only outputs that are source-explicit or strongly implied by the supplied work itself.
- Do not infer deliverables from generic knowledge of a tool, title, or profession.
- Every deliverable must reference direct work. Strongly implied deliverables require a rationale.

ROLE INTERPRETATION
- A concise candidate role label is allowed when it clarifies the work composition.
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
        # Preserve the accepted P1.6 statement exactly. It is also the value later injected into
        # the persisted artifact; the model sees it for reasoning but never authors its replacement.
        "statement": statement,
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
        work_themes=[],
        deliverables=[],
        role_interpretation=None,
        limitations=[
            "The accepted job analysis contains no direct responsibility or role-purpose evidence, "
            "so JobHunter will not invent duties from qualifications alone."
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


def _candidate_scope_text(intelligence: CandidateJobWorkIntelligence) -> str:
    values: list[str] = []
    for theme in intelligence.work_themes:
        values.append(theme.label)
        if theme.rationale:
            values.append(theme.rationale)
    for deliverable in intelligence.deliverables:
        values.append(deliverable.label)
        if deliverable.rationale:
            values.append(deliverable.rationale)
    if intelligence.role_interpretation is not None:
        role = intelligence.role_interpretation
        values.append(role.label)
        values.extend(role.alternatives)
        values.extend(role.limitations)
    values.extend(intelligence.limitations)
    return _normalized_semantic_text(" ".join(values))


def _validate_scope_language(
    intelligence: CandidateJobWorkIntelligence,
    *,
    responsibilities: list[Any],
    role_purpose: list[Any],
) -> None:
    """Reject explicit unsupported scope intensifiers in model-owned candidate interpretation."""

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


def _accepted_confidence(item: dict[str, Any]) -> str | None:
    value = item.get("confidence")
    return value if value in {"high", "medium", "low"} else None


def _accepted_work_item(
    *,
    kind: str,
    index: int,
    responsibilities: list[Any],
    role_purpose: list[Any],
) -> AcceptedWorkItem:
    source = responsibilities if kind == "responsibility" else role_purpose
    label = "responsibility" if kind == "responsibility" else "role_purpose"
    if index < 0 or index >= len(source):
        raise WorkIntelligenceError(f"Cannot assemble missing accepted {label}[{index}]")
    item = source[index]
    if not isinstance(item, dict):
        raise WorkIntelligenceError(f"Accepted P1.6 {label}[{index}] is not an object")
    statement = item.get("statement")
    if not isinstance(statement, str) or not statement.strip():
        raise WorkIntelligenceError(f"Accepted P1.6 {label}[{index}] has no usable statement")
    return AcceptedWorkItem(
        kind=kind,
        index=index,
        statement=statement,
        confidence=_accepted_confidence(item),
    )


def _accepted_work_items(
    *,
    responsibility_indices: list[int],
    role_purpose_indices: list[int],
    responsibilities: list[Any],
    role_purpose: list[Any],
) -> list[AcceptedWorkItem]:
    return [
        *[
            _accepted_work_item(
                kind="responsibility",
                index=index,
                responsibilities=responsibilities,
                role_purpose=role_purpose,
            )
            for index in responsibility_indices
        ],
        *[
            _accepted_work_item(
                kind="role_purpose",
                index=index,
                responsibilities=responsibilities,
                role_purpose=role_purpose,
            )
            for index in role_purpose_indices
        ],
    ]


def _assemble_document(
    candidate: CandidateJobWorkIntelligence,
    *,
    responsibilities: list[Any],
    role_purpose: list[Any],
) -> JobWorkIntelligence:
    """Combine model-owned structure with exact accepted P1.6 work by deterministic reference."""

    if candidate.evidence_status != "sufficient":
        raise WorkIntelligenceError(
            "Direct accepted work evidence requires evidence_status='sufficient'"
        )

    themes = [
        WorkTheme(
            theme_id=theme.theme_id,
            label=theme.label,
            emphasis=theme.emphasis,
            confidence=theme.confidence,
            accepted_work_items=_accepted_work_items(
                responsibility_indices=theme.responsibility_indices,
                role_purpose_indices=theme.role_purpose_indices,
                responsibilities=responsibilities,
                role_purpose=role_purpose,
            ),
            supporting_requirement_indices=theme.supporting_requirement_indices,
            rationale=theme.rationale,
        )
        for theme in candidate.work_themes
    ]
    deliverables = [
        DeliverableCandidate(
            label=item.label,
            status=item.status,
            confidence=item.confidence,
            accepted_work_items=_accepted_work_items(
                responsibility_indices=item.responsibility_indices,
                role_purpose_indices=item.role_purpose_indices,
                responsibilities=responsibilities,
                role_purpose=role_purpose,
            ),
            rationale=item.rationale,
        )
        for item in candidate.deliverables
    ]
    return JobWorkIntelligence(
        evidence_status=candidate.evidence_status,
        work_themes=themes,
        deliverables=deliverables,
        role_interpretation=candidate.role_interpretation,
        limitations=candidate.limitations,
    )


class WorkIntelligenceService:
    """Build or reuse one v2 candidate artifact above accepted English P1.6."""

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
        intelligence: CandidateJobWorkIntelligence,
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

        # A reference into a structurally empty section has no possible semantic target. Removing
        # only those impossible references is deterministic normalization, not semantic remapping.
        # References into non-empty sections are never clamped, guessed, or reassigned.
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
            validate(
                deliverable.responsibility_indices,
                responsibility_count,
                "responsibility",
            )
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
    def _candidate_from_inference(
        inference: WorkIntelligenceInferenceResult,
    ) -> CandidateJobWorkIntelligence:
        if inference.validated_model is not None:
            if not isinstance(inference.validated_model, CandidateJobWorkIntelligence):
                raise WorkIntelligenceError(
                    "Work Intelligence provider returned an incompatible validated model"
                )
            candidate = inference.validated_model
        else:
            candidate = CandidateJobWorkIntelligence.model_validate(inference.intelligence)
        if candidate.evidence_status != "sufficient":
            raise WorkIntelligenceError(
                "Direct accepted work evidence requires evidence_status='sufficient'"
            )
        return candidate

    def _validate_generated_candidate(
        self,
        candidate: CandidateJobWorkIntelligence,
        *,
        responsibilities: list[Any],
        role_purpose: list[Any],
        requirements: list[Any],
    ) -> None:
        self._validate_references(
            candidate,
            responsibility_count=len(responsibilities),
            role_purpose_count=len(role_purpose),
            requirement_count=len(requirements),
        )
        _validate_scope_language(
            candidate,
            responsibilities=responsibilities,
            role_purpose=role_purpose,
        )

    @staticmethod
    def _validate_assembled_document(
        document: JobWorkIntelligence,
        *,
        responsibilities: list[Any],
        role_purpose: list[Any],
        requirement_count: int,
    ) -> None:
        """Verify persisted factual items still exactly match their accepted P1.6 dependency."""

        if document.evidence_status == "limited":
            if responsibilities or role_purpose:
                raise WorkIntelligenceError(
                    "Limited Work Intelligence cannot represent accepted direct work evidence"
                )
            return

        expected = {
            *[("responsibility", index) for index in range(len(responsibilities))],
            *[("role_purpose", index) for index in range(len(role_purpose))],
        }
        covered: set[tuple[str, int]] = set()

        def validate_item(item: AcceptedWorkItem) -> None:
            source = responsibilities if item.kind == "responsibility" else role_purpose
            if item.index >= len(source):
                raise WorkIntelligenceError(
                    f"Persisted Work Intelligence references missing {item.kind}[{item.index}]"
                )
            raw = source[item.index]
            if not isinstance(raw, dict):
                raise WorkIntelligenceError(
                    f"Accepted P1.6 {item.kind}[{item.index}] is not an object"
                )
            statement = raw.get("statement")
            if not isinstance(statement, str) or item.statement != statement:
                raise WorkIntelligenceError(
                    "Persisted accepted work statement does not exactly match P1.6 "
                    f"{item.kind}[{item.index}]"
                )
            expected_confidence = _accepted_confidence(raw)
            if item.confidence != expected_confidence:
                raise WorkIntelligenceError(
                    "Persisted accepted work confidence does not match P1.6 "
                    f"{item.kind}[{item.index}]"
                )

        for theme in document.work_themes:
            invalid_requirements = [
                index
                for index in theme.supporting_requirement_indices
                if index >= requirement_count
            ]
            if invalid_requirements:
                raise WorkIntelligenceError(
                    "Persisted Work Intelligence references missing requirement indices: "
                    f"{invalid_requirements}"
                )
            for item in theme.accepted_work_items:
                validate_item(item)
                covered.add((item.kind, item.index))

        for deliverable in document.deliverables:
            for item in deliverable.accepted_work_items:
                validate_item(item)

        missing = expected - covered
        if missing:
            missing_responsibilities = sorted(
                index for kind, index in missing if kind == "responsibility"
            )
            missing_purpose = sorted(
                index for kind, index in missing if kind == "role_purpose"
            )
            raise WorkIntelligenceError(
                "Persisted work themes omitted accepted direct work evidence: "
                f"responsibilities={missing_responsibilities}, "
                f"role_purpose={missing_purpose}"
            )

    def _generate_with_semantic_repair(
        self,
        *,
        user_payload: dict[str, Any],
        responsibilities: list[Any],
        role_purpose: list[Any],
        requirements: list[Any],
    ) -> tuple[CandidateJobWorkIntelligence, dict[str, Any], dict[str, Any]]:
        """Generate one candidate, with at most one repair after deterministic rejection."""

        if self._provider is None:
            raise WorkIntelligenceError("Work Intelligence provider is unavailable")

        first_error: WorkIntelligenceError | None = None
        first_request_body: dict[str, Any] | None = None
        first_raw_response: dict[str, Any] | None = None
        system_prompt = _WORK_INTELLIGENCE_PROMPT

        for repair_attempt in range(2):
            inference = self._provider.complete(
                response_model=CandidateJobWorkIntelligence,
                system_prompt=system_prompt,
                user_payload=user_payload,
                max_tokens=min(self._max_tokens, 4096),
                seed=0,
            )
            candidate = self._candidate_from_inference(inference)
            try:
                self._validate_generated_candidate(
                    candidate,
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

            request_body = inference.request_body
            raw_response = inference.raw_response
            if first_error is not None:
                request_body = dict(inference.request_body)
                request_body["semantic_repair"] = {
                    "attempts": 1,
                    "trigger": str(first_error),
                    "initial_request_body": first_request_body,
                }
                raw_response = {
                    "semantic_repair": {
                        "attempts": 1,
                        "trigger": str(first_error),
                        "initial_raw_response": first_raw_response,
                        "final_raw_response": inference.raw_response,
                    }
                }
            return candidate, request_body, raw_response

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
        """Return only the v2 artifact on the exact current accepted P1.6 dependency."""

        try:
            analysis = self._current_p16(source_job_id)
            responsibilities, role_purpose, requirements = self._sections(analysis)
            model, _ = self._identity_for(analysis)
        except WorkIntelligenceError:
            return None
        artifact = self._work_store.find_artifact(
            analysis_artifact_id=analysis.id,
            model=model,
            prompt_version=WORK_INTELLIGENCE_PROMPT_VERSION,
            schema_version=WORK_INTELLIGENCE_SCHEMA_VERSION,
        )
        if artifact is None:
            return None
        document = JobWorkIntelligence.model_validate(artifact.intelligence)
        self._validate_assembled_document(
            document,
            responsibilities=responsibilities,
            role_purpose=role_purpose,
            requirement_count=len(requirements),
        )
        return artifact

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
            document = JobWorkIntelligence.model_validate(existing.intelligence)
            self._validate_assembled_document(
                document,
                responsibilities=responsibilities,
                role_purpose=role_purpose,
                requirement_count=len(requirements),
            )
            self._work_store.record_attempt(
                analysis_artifact_id=analysis.id,
                attempted_at=attempted_at,
                model=model,
                prompt_version=WORK_INTELLIGENCE_PROMPT_VERSION,
                schema_version=WORK_INTELLIGENCE_SCHEMA_VERSION,
                outcome="reused",
                artifact_id=existing.id,
            )
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
                candidate, request_body, raw_response = self._generate_with_semantic_repair(
                    user_payload=user_payload,
                    responsibilities=responsibilities,
                    role_purpose=role_purpose,
                    requirements=requirements,
                )
                document = _assemble_document(
                    candidate,
                    responsibilities=responsibilities,
                    role_purpose=role_purpose,
                )

            self._validate_assembled_document(
                document,
                responsibilities=responsibilities,
                role_purpose=role_purpose,
                requirement_count=len(requirements),
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
    """Build the current P2.2A v2 service without promoting candidate interpretation."""

    analysis_model = settings.effective_analysis_lm_studio_model()
    if not analysis_model:
        raise ValueError("No analysis model is configured for accepted English P1.6")

    # Keep the accepted analysis reasoning model for the single bounded candidate-generation role.
    # The v2 representation no longer asks a second model pass to establish factual action
    # authority; exact accepted P1.6 work is injected deterministically after candidate validation.
    work_model = analysis_model
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
    """Render the same v2 fact-versus-interpretation hierarchy used by the browser."""

    document = JobWorkIntelligence.model_validate(artifact.intelligence)
    lines = [
        f"Job Work Intelligence: {artifact.source_job_id}",
        f"State: {artifact.semantic_state} / {document.evidence_status}",
        f"Model: {artifact.model}",
        f"P1.6 dependency: artifact {artifact.analysis_artifact_id}",
    ]

    if document.work_themes:
        lines.append("\nWork themes:")
        for theme in document.work_themes:
            lines.append(f"- {theme.label} [{theme.emphasis}, {theme.confidence}]")
            lines.append("  JobHunter candidate theme")
            lines.append("  Accepted P1.6 work:")
            for item in theme.accepted_work_items:
                source_label = (
                    "responsibility" if item.kind == "responsibility" else "role purpose"
                )
                confidence = f", {item.confidence}" if item.confidence else ""
                lines.append(
                    f"  * [{source_label} {item.index}{confidence}] {item.statement}"
                )
            if theme.rationale:
                lines.append(f"  JobHunter interpretation: {theme.rationale}")
            if theme.supporting_requirement_indices:
                lines.append(
                    "  Supporting requirement indices: "
                    + ", ".join(str(value) for value in theme.supporting_requirement_indices)
                )

    if document.deliverables:
        lines.append("\nCandidate deliverables:")
        for item in document.deliverables:
            lines.append(f"- {item.label} [{item.status}, {item.confidence}]")
            lines.append("  Accepted P1.6 work support:")
            for work in item.accepted_work_items:
                source_label = (
                    "responsibility" if work.kind == "responsibility" else "role purpose"
                )
                lines.append(f"  * [{source_label} {work.index}] {work.statement}")
            if item.rationale:
                lines.append(f"  JobHunter interpretation: {item.rationale}")

    if document.role_interpretation is not None:
        role = document.role_interpretation
        lines.extend(
            [
                "\nCandidate role interpretation:",
                f"- {role.label} [{role.confidence}]",
                "  Supporting themes: " + ", ".join(role.supporting_theme_ids),
            ]
        )
        if role.alternatives:
            lines.append("  Alternatives: " + "; ".join(role.alternatives))
        if role.limitations:
            lines.append("  Role limits: " + "; ".join(role.limitations))

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
