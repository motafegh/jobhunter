"""P1.6 v19 candidate with deterministic depth/optionality boundary canonicalization."""

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
    _validate_evidence_v17,
    validate_v17_candidate_structured,
)
from jobhunter.analysis_service_v18 import (
    ANALYSIS_SCHEMA_VERSION,
    _ANALYSIS_SCHEMA_V18,
    _ENGLISH_SYSTEM_PROMPT_V18,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ENGLISH_PROMPT_VERSION = "job-analysis-english-v19"
PROMPT_VERSION = ENGLISH_PROMPT_VERSION

_V19_RULES = """

P1.6 V19 CANDIDATE — DEPTH / OPTIONALITY CANONICALIZATION:
- Preference/optionality wording such as "a plus" or "helpful" belongs in requirement_type and is
  not technical depth. JobHunter may clear such wording from depth_signal when the cited evidence
  independently proves the preferred obligation and contains no accepted depth signal.
- A normalized concept must not gain unsupported depth vocabulary. JobHunter may remove a depth
  token from the generated concept only when that token is absent from the cited exact source and
  cleanup leaves a meaningful non-generic concept. Otherwise strict validation still fails closed.
- Genuine source depth remains model-visible and must still be separated into depth_signal by the
  inherited strict validator.
- Keep every v18/v17 exact-evidence, deterministic structured-fact, structured-skill coverage,
  obligation, ontology, decomposition, responsibility, source-led-capacity, and fail-closed rule.
"""

_ENGLISH_SYSTEM_PROMPT_V19 = _ENGLISH_SYSTEM_PROMPT_V18 + _V19_RULES
_ANALYSIS_SCHEMA_V19 = deepcopy(_ANALYSIS_SCHEMA_V18)


class JobAnalysisServiceV19:
    """Persist isolated English P1.6 v19 artifacts under the v5 response schema."""

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
                system_prompt=_ENGLISH_SYSTEM_PROMPT_V19,
                user_payload={
                    "source_job_id": source.source_job_id,
                    "analysis_mode": "english",
                    "analysis_fields": analysis_fields,
                },
                schema_name="jobhunter_job_analysis_english_v19",
                schema=_ANALYSIS_SCHEMA_V19,
                model=self._model,
                max_tokens=self._max_tokens,
            )
            validate_v17_candidate_structured(result.structured, analysis_fields)
            analysis = _persisted_analysis_v14(result.structured, analysis_fields)
            _validate_evidence_v17(analysis, analysis_fields)
        except Exception as exc:
            self._record_failed_attempt(source=source, attempted_at=attempted_at, error=exc)
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
                raise RuntimeError("P1.6 v19 artifact disappeared after persistence")
            return _result(artifact, outcome="completed", analysis_mode="english")
        except Exception as exc:
            self._record_failed_attempt(source=source, attempted_at=attempted_at, error=exc)
            raise

    def analyze_job(self, source_job_id: str) -> AnalysisJobResult:
        return self.analyze_english_job(source_job_id)


__all__ = [
    "ANALYSIS_SCHEMA_VERSION",
    "ENGLISH_PROMPT_VERSION",
    "JobAnalysisServiceV19",
    "PROMPT_VERSION",
    "_ANALYSIS_SCHEMA_V19",
    "_ENGLISH_SYSTEM_PROMPT_V19",
]
