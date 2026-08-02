"""Evidence-backed local semantic analysis for current JobHunter source versions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from jobhunter.analysis_store import AnalysisArtifact, AnalysisStore
from jobhunter.inference import InferenceProviderError, LMStudioProvider
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

PROMPT_VERSION = "job-analysis-prompt-v1"
ANALYSIS_SCHEMA_VERSION = "job-analysis-v1"

_SOURCE_METADATA_FIELDS = {"language", "parser_version"}

_SYSTEM_PROMPT = """You are JobHunter's evidence-constrained job-analysis engine.
The original employer/source fields are authoritative. The English projection is only a
comprehension aid.

Extract only claims supported by the supplied employer text.
- Do not invent responsibilities, requirements, seniority, tools, or intent.
- Omit uncertain claims rather than guessing.
- Every claim must copy a short evidence excerpt VERBATIM from one original source field.
- Keep required, preferred, contextual, and inferred distinct.
- A source-explicit requirement must not be marked inferred.
- Inferred concepts require a concise rationale and still require an exact source excerpt.
- Requirement strength must be preserved. Familiarity is not proficiency; preferred is
  not required.
- Return concise normalized English statements/concepts, but evidence stays in the original
  employer language exactly as supplied.
"""

_CONFIDENCE = ["high", "medium", "low"]
_REQ_TYPES = ["required", "preferred", "contextual", "inferred"]
_CONCEPT_TYPES = [
    "tool",
    "skill",
    "knowledge",
    "practice",
    "domain",
    "experience",
    "education",
    "other",
]

_CLAIM_SCHEMA = {
    "type": "object",
    "properties": {
        "statement": {"type": "string"},
        "evidence": {"type": "string"},
        "confidence": {"type": "string", "enum": _CONFIDENCE},
    },
    "required": ["statement", "evidence", "confidence"],
    "additionalProperties": False,
}

_REQUIREMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "concept": {"type": "string"},
        "requirement_type": {"type": "string", "enum": _REQ_TYPES},
        "concept_type": {"type": "string", "enum": _CONCEPT_TYPES},
        "evidence": {"type": "string"},
        "confidence": {"type": "string", "enum": _CONFIDENCE},
        "rationale": {"type": "string"},
    },
    "required": [
        "concept",
        "requirement_type",
        "concept_type",
        "evidence",
        "confidence",
        "rationale",
    ],
    "additionalProperties": False,
}

_ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "role_purpose": {
            "type": "array",
            "maxItems": 1,
            "items": _CLAIM_SCHEMA,
        },
        "responsibilities": {
            "type": "array",
            "maxItems": 16,
            "items": _CLAIM_SCHEMA,
        },
        "requirements": {
            "type": "array",
            "maxItems": 32,
            "items": _REQUIREMENT_SCHEMA,
        },
    },
    "required": ["role_purpose", "responsibilities", "requirements"],
    "additionalProperties": False,
}


class AnalysisValidationError(ValueError):
    """Raised when model output cannot be grounded in authoritative source text."""


@dataclass(frozen=True, slots=True)
class AnalysisJobResult:
    source_job_id: str
    artifact_id: int
    outcome: str
    model: str
    responsibilities: int
    requirements: int


@dataclass(frozen=True, slots=True)
class AnalysisFailure:
    source_job_id: str
    error: str


@dataclass(frozen=True, slots=True)
class AnalysisBatchSummary:
    attempted: int
    results: tuple[AnalysisJobResult, ...]
    failures: tuple[AnalysisFailure, ...]

    @property
    def completed(self) -> int:
        return sum(item.outcome == "completed" for item in self.results)

    @property
    def reused(self) -> int:
        return sum(item.outcome == "reused" for item in self.results)


def _authoritative_source_fields(source: TranslationSourceVersion) -> dict[str, Any]:
    """Return employer/job fields only; parser metadata is never claim evidence."""

    return {
        key: value
        for key, value in source.fields.items()
        if key not in _SOURCE_METADATA_FIELDS
    }


def _iter_source_strings(value: Any):
    if isinstance(value, str):
        if value.strip():
            yield value
    elif isinstance(value, list):
        for item in value:
            yield from _iter_source_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _iter_source_strings(item)


def _normalize_evidence(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def _validate_evidence(
    analysis: dict[str, Any],
    source: TranslationSourceVersion,
) -> None:
    source_strings = tuple(
        _normalize_evidence(text)
        for text in _iter_source_strings(_authoritative_source_fields(source))
    )

    def require_excerpt(evidence: str, *, label: str) -> None:
        normalized = _normalize_evidence(evidence)
        if len(normalized) < 2:
            raise AnalysisValidationError(f"{label} has empty/too-short source evidence")
        if not any(normalized in source_text for source_text in source_strings):
            raise AnalysisValidationError(
                f"{label} evidence is not an exact excerpt of authoritative source fields"
            )

    role_purpose = analysis.get("role_purpose")
    responsibilities = analysis.get("responsibilities")
    requirements = analysis.get("requirements")
    if not all(
        isinstance(value, list)
        for value in (role_purpose, responsibilities, requirements)
    ):
        raise AnalysisValidationError("Analysis root arrays are malformed")
    if len(role_purpose) > 1 or len(responsibilities) > 16 or len(requirements) > 32:
        raise AnalysisValidationError("Analysis exceeded bounded claim counts")

    for index, claim in enumerate(role_purpose):
        if not isinstance(claim, dict):
            raise AnalysisValidationError("Role-purpose claim is malformed")
        require_excerpt(
            str(claim.get("evidence") or ""),
            label=f"role_purpose[{index}]",
        )
    for index, claim in enumerate(responsibilities):
        if not isinstance(claim, dict):
            raise AnalysisValidationError("Responsibility claim is malformed")
        require_excerpt(
            str(claim.get("evidence") or ""),
            label=f"responsibility[{index}]",
        )
    for index, item in enumerate(requirements):
        if not isinstance(item, dict):
            raise AnalysisValidationError("Requirement item is malformed")
        concept = str(item.get("concept") or "").strip()
        if not concept:
            raise AnalysisValidationError(f"requirement[{index}] has an empty concept")
        requirement_type = str(item.get("requirement_type") or "")
        if requirement_type not in _REQ_TYPES:
            raise AnalysisValidationError(
                f"requirement[{index}] has invalid requirement type"
            )
        rationale = str(item.get("rationale") or "").strip()
        if requirement_type == "inferred" and not rationale:
            raise AnalysisValidationError(
                f"requirement[{index}] inferred concept lacks rationale"
            )
        require_excerpt(
            str(item.get("evidence") or ""),
            label=f"requirement[{index}]",
        )


class JobAnalysisService:
    """Create/reuse evidence-validated analysis for current parsed job versions."""

    def __init__(
        self,
        *,
        source_store: TranslationStore,
        translation_service: TranslationService,
        analysis_store: AnalysisStore,
        provider: LMStudioProvider,
        model: str,
        max_tokens: int = 8192,
        clock=lambda: datetime.now(UTC),
    ) -> None:
        if not model.strip():
            raise ValueError("A concrete LM Studio analysis model is required")
        self._source_store = source_store
        self._translation_service = translation_service
        self._analysis_store = analysis_store
        self._provider = provider
        self._model = model.strip()
        self._max_tokens = max_tokens
        self._clock = clock

    def analyze_job(self, source_job_id: str) -> AnalysisJobResult:
        source = self._source_store.latest_source_version(source_job_id)
        if source is None:
            raise AnalysisValidationError(
                "Job has no current successfully parsed source version"
            )
        english = self._translation_service.current_artifact(source_job_id)
        if english is None:
            raise AnalysisValidationError(
                "Job has no current hardened English projection; repair/translate it first"
            )
        existing = self._analysis_store.find_artifact(
            job_detail_version_id=source.job_detail_version_id,
            model=self._model,
            prompt_version=PROMPT_VERSION,
            schema_version=ANALYSIS_SCHEMA_VERSION,
        )
        attempted_at = self._clock()
        if existing is not None:
            self._analysis_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                model=self._model,
                prompt_version=PROMPT_VERSION,
                schema_version=ANALYSIS_SCHEMA_VERSION,
                outcome="reused",
                artifact_id=existing.id,
            )
            return _result(existing, outcome="reused")

        authoritative_fields = _authoritative_source_fields(source)
        try:
            result = self._provider.complete_structured(
                system_prompt=_SYSTEM_PROMPT,
                user_payload={
                    "source_job_id": source.source_job_id,
                    "authoritative_source_fields": authoritative_fields,
                    "english_comprehension_aid": english.fields,
                },
                schema_name="jobhunter_job_analysis_v1",
                schema=_ANALYSIS_SCHEMA,
                model=self._model,
                max_tokens=self._max_tokens,
            )
            _validate_evidence(result.structured, source)
            artifact_id = self._analysis_store.record_artifact(
                job_detail_version_id=source.job_detail_version_id,
                translation_artifact_id=english.id,
                model=result.model,
                prompt_version=PROMPT_VERSION,
                schema_version=ANALYSIS_SCHEMA_VERSION,
                analysis=result.structured,
                request_body=result.request_body,
                raw_response=result.raw_response,
                created_at=attempted_at,
            )
            self._analysis_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                model=self._model,
                prompt_version=PROMPT_VERSION,
                schema_version=ANALYSIS_SCHEMA_VERSION,
                outcome="completed",
                artifact_id=artifact_id,
            )
            artifact = self._analysis_store.find_artifact(
                job_detail_version_id=source.job_detail_version_id,
                model=self._model,
                prompt_version=PROMPT_VERSION,
                schema_version=ANALYSIS_SCHEMA_VERSION,
            )
            if artifact is None:
                raise RuntimeError("Analysis artifact disappeared after persistence")
            return _result(artifact, outcome="completed")
        except Exception as exc:
            self._analysis_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                model=self._model,
                prompt_version=PROMPT_VERSION,
                schema_version=ANALYSIS_SCHEMA_VERSION,
                outcome="failed",
                error=exc,
            )
            raise

    def run(
        self,
        source_job_ids: tuple[str, ...],
        *,
        limit: int = 5,
    ) -> AnalysisBatchSummary:
        unique = tuple(
            dict.fromkeys(
                job_id.strip() for job_id in source_job_ids if job_id.strip()
            )
        )
        if not unique:
            raise ValueError("At least one job is required for analysis")
        if not 1 <= limit <= 20:
            raise ValueError("analysis limit must be between 1 and 20")
        results: list[AnalysisJobResult] = []
        failures: list[AnalysisFailure] = []
        for source_job_id in unique[:limit]:
            try:
                results.append(self.analyze_job(source_job_id))
            except (
                AnalysisValidationError,
                InferenceProviderError,
                RuntimeError,
                ValueError,
            ) as exc:
                failures.append(
                    AnalysisFailure(source_job_id=source_job_id, error=str(exc))
                )
        return AnalysisBatchSummary(
            attempted=min(len(unique), limit),
            results=tuple(results),
            failures=tuple(failures),
        )


def _result(artifact: AnalysisArtifact, *, outcome: str) -> AnalysisJobResult:
    return AnalysisJobResult(
        source_job_id=artifact.source_job_id,
        artifact_id=artifact.id,
        outcome=outcome,
        model=artifact.model,
        responsibilities=len(artifact.analysis.get("responsibilities") or []),
        requirements=len(artifact.analysis.get("requirements") or []),
    )


def format_analysis_batch_summary(summary: AnalysisBatchSummary) -> str:
    lines = [
        "Evidence-backed job analysis",
        f"Attempted: {summary.attempted}",
        f"Completed: {summary.completed}",
        f"Reused: {summary.reused}",
        f"Failures: {len(summary.failures)}",
    ]
    for result in summary.results:
        lines.append(
            f"- {result.source_job_id}: {result.outcome}, artifact {result.artifact_id}, "
            f"responsibilities={result.responsibilities}, requirements={result.requirements}, "
            f"model={result.model}"
        )
    if summary.failures:
        lines.append("Failures:")
        lines.extend(
            f"- {failure.source_job_id}: {failure.error}"
            for failure in summary.failures
        )
    return "\n".join(lines)
