"""P1.6 v18 candidate with deterministic ownership of mechanically known structured facts.

V17 removed the stale dense requirement ceiling and improved aggregate retry feedback. The next
live dense run showed a different failure class: the model correctly learned that education and
minimum experience were missing, but then encoded the already-known experience duration inside
both the normalized concept and ``depth_signal``. V18 stops delegating such mechanically known
structured facts to the model when JobHunter can represent them without semantic guessing.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime

from jobhunter.analysis_service import (
    AnalysisJobResult,
    AnalysisValidationError,
    _analysis_fields_for_english,
    _result,
)
from jobhunter.analysis_service_v14 import _persisted_analysis_v14
from jobhunter.analysis_service_v17 import (
    _ANALYSIS_SCHEMA_V17,
    _ENGLISH_SYSTEM_PROMPT_V17,
    ANALYSIS_SCHEMA_VERSION,
    _validate_evidence_v17,
    validate_v17_candidate_structured,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ENGLISH_PROMPT_VERSION = "job-analysis-english-v18"
PROMPT_VERSION = ENGLISH_PROMPT_VERSION

_V18_RULES = """

P1.6 V18 CANDIDATE — DETERMINISTIC STRUCTURED-FACT OWNERSHIP:
- JobHunter, not the language model, owns structured requirement facts when their representation is
  mechanically known from exact source fields. Such fields may be omitted from the model-facing
  analysis view and added back deterministically after generation with their exact provenance.
- In particular, a parseable structured minimum-experience duration is represented as concept
  "Professional experience" with the exact years phrase in depth_signal, and a structured
  education credential is represented as an education requirement using the exact field value.
- Do not reconstruct or infer a structured fact that is absent from the model-facing evidence.
- Top-level structured skills remain model-visible because concept_type can require semantic
  classification, but JobHunter supplies explicit non-excludable coverage IDs for every skill so
  none may silently disappear.
- Keep every v17/v16 exact-evidence, obligation, depth, ontology, qualification-vs-duty,
  decomposition, responsibility, source-led-capacity, and fail-closed rule unchanged.
"""

_ENGLISH_SYSTEM_PROMPT_V18 = _ENGLISH_SYSTEM_PROMPT_V17 + _V18_RULES
_ANALYSIS_SCHEMA_V18 = deepcopy(_ANALYSIS_SCHEMA_V17)


class JobAnalysisServiceV18:
    """Persist isolated English P1.6 v18 artifacts under the existing v5 response shape."""

    def __init__(
        self,
        *,
        source_store: TranslationStore,
        translation_service: TranslationService,
        analysis_store: AnalysisStore,
        provider,
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

    def _record_failed_attempt(
        self,
        *,
        source: TranslationSourceVersion,
        attempted_at: datetime,
        error: Exception,
    ) -> None:
        self._analysis_store.record_attempt(
            job_detail_version_id=source.job_detail_version_id,
            attempted_at=attempted_at,
            model=self._model,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ANALYSIS_SCHEMA_VERSION,
            outcome="failed",
            error=error,
        )

    def analyze_english_job(self, source_job_id: str) -> AnalysisJobResult:
        source = self._source_store.latest_source_version(source_job_id)
        if source is None:
            raise AnalysisValidationError("Job has no current successfully parsed source version")
        translation = self._translation_service.current_artifact(source_job_id)
        if translation is None:
            raise AnalysisValidationError(
                "Job has no current hardened English projection; translate/repair it first"
            )
        analysis_fields = _analysis_fields_for_english(translation.fields)
        attempted_at = self._clock()

        existing = self._analysis_store.find_artifact(
            job_detail_version_id=source.job_detail_version_id,
            model=self._model,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ANALYSIS_SCHEMA_VERSION,
        )
        if existing is not None:
            self._analysis_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                model=self._model,
                prompt_version=ENGLISH_PROMPT_VERSION,
                schema_version=ANALYSIS_SCHEMA_VERSION,
                outcome="reused",
                artifact_id=existing.id,
            )
            return _result(existing, outcome="reused", analysis_mode="english")

        try:
            result = self._provider.complete_structured(
                system_prompt=_ENGLISH_SYSTEM_PROMPT_V18,
                user_payload={
                    "source_job_id": source.source_job_id,
                    "analysis_mode": "english",
                    "analysis_fields": analysis_fields,
                },
                schema_name="jobhunter_job_analysis_english_v18",
                schema=_ANALYSIS_SCHEMA_V18,
                model=self._model,
                max_tokens=self._max_tokens,
            )
            validate_v17_candidate_structured(result.structured, analysis_fields)
            analysis = _persisted_analysis_v14(result.structured, analysis_fields)
            _validate_evidence_v17(analysis, analysis_fields)
        except Exception as exc:
            self._record_failed_attempt(
                source=source,
                attempted_at=attempted_at,
                error=exc,
            )
            raise

        try:
            artifact_id = self._analysis_store.record_artifact(
                job_detail_version_id=source.job_detail_version_id,
                translation_artifact_id=translation.id,
                model=result.model,
                prompt_version=ENGLISH_PROMPT_VERSION,
                schema_version=ANALYSIS_SCHEMA_VERSION,
                analysis=analysis,
                request_body=result.request_body,
                raw_response=result.raw_response,
                created_at=attempted_at,
            )
            self._analysis_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                model=self._model,
                prompt_version=ENGLISH_PROMPT_VERSION,
                schema_version=ANALYSIS_SCHEMA_VERSION,
                outcome="completed",
                artifact_id=artifact_id,
            )
            artifact = self._analysis_store.find_artifact(
                job_detail_version_id=source.job_detail_version_id,
                model=self._model,
                prompt_version=ENGLISH_PROMPT_VERSION,
                schema_version=ANALYSIS_SCHEMA_VERSION,
            )
            if artifact is None:
                raise RuntimeError("P1.6 v18 artifact disappeared after persistence")
            return _result(artifact, outcome="completed", analysis_mode="english")
        except Exception as exc:
            self._record_failed_attempt(
                source=source,
                attempted_at=attempted_at,
                error=exc,
            )
            raise

    def analyze_job(self, source_job_id: str) -> AnalysisJobResult:
        return self.analyze_english_job(source_job_id)


__all__ = [
    "ANALYSIS_SCHEMA_VERSION",
    "ENGLISH_PROMPT_VERSION",
    "JobAnalysisServiceV18",
    "PROMPT_VERSION",
    "_ANALYSIS_SCHEMA_V18",
    "_ENGLISH_SYSTEM_PROMPT_V18",
]
