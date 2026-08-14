"""P1.6 v20 candidate with source-led bounded semantic partitioning."""

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
from jobhunter.analysis_service_v19 import (
    _ANALYSIS_SCHEMA_V19,
    _ENGLISH_SYSTEM_PROMPT_V19,
    ANALYSIS_SCHEMA_VERSION,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ENGLISH_PROMPT_VERSION = "job-analysis-english-v20"
PROMPT_VERSION = ENGLISH_PROMPT_VERSION

_V20_RULES = """

P1.6 V20 CANDIDATE — SOURCE-LED BOUNDED SEMANTIC PARTITIONING:
- Dense source coverage is processed in independent bounded partitions. Each call must account only
  for the requirement_coverage and responsibility_coverage references supplied to that partition.
- Never repair one partition by replacing or omitting another partition's already-valid claims.
- JobHunter merges independently validated partitions and then validates the whole artifact against
  the original source-led coverage ledger.
- Keep role purpose semantically distinct from responsibilities: use role_purpose for a high-level
  statement of what the role exists to accomplish, and responsibilities for concrete duties. Do not
  move a purpose statement into responsibilities merely because both share the duty coverage ledger.
- A vague quantifier such as "some" in preferred wording like "some C / C++ helpful" is not one of
  JobHunter's accepted technical-depth signals. Preserve the exact evidence and preferred strength,
  but use depth_signal=null unless the same evidence contains an independently accepted explicit
  depth or experience-extent phrase.
- Scope/domain qualifiers describe the concept, not technical depth. For wording such as
  "industrial / edge deployment a plus", preserve "industrial / edge deployment" in the normalized
  concept and use depth_signal=null unless the source separately states an accepted depth marker.
- concept_type=experience requires explicit prior applied exposure in the cited evidence. A bare
  preferred subject/scope phrase such as "industrial / edge deployment a plus" does not by itself
  prove experience; classify the source-supported capability/domain appropriately instead.
- Keep every v19/v18/v17 exact-evidence, obligation, depth, deterministic structured-fact,
  structured-skill, ontology, decomposition, responsibility, capacity, and fail-closed rule.
"""

_ENGLISH_SYSTEM_PROMPT_V20 = _ENGLISH_SYSTEM_PROMPT_V19 + _V20_RULES
_ANALYSIS_SCHEMA_V20 = deepcopy(_ANALYSIS_SCHEMA_V19)


class JobAnalysisServiceV20:
    """Persist isolated English P1.6 v20 artifacts under the v5 response schema."""

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
                system_prompt=_ENGLISH_SYSTEM_PROMPT_V20,
                user_payload={
                    "source_job_id": source.source_job_id,
                    "analysis_mode": "english",
                    "analysis_fields": analysis_fields,
                },
                schema_name="jobhunter_job_analysis_english_v20",
                schema=_ANALYSIS_SCHEMA_V20,
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
                raise RuntimeError("P1.6 v20 artifact disappeared after persistence")
            return _result(artifact, outcome="completed", analysis_mode="english")
        except Exception as exc:
            self._record_failed_attempt(source=source, attempted_at=attempted_at, error=exc)
            raise

    def analyze_job(self, source_job_id: str) -> AnalysisJobResult:
        return self.analyze_english_job(source_job_id)


__all__ = [
    "ANALYSIS_SCHEMA_VERSION",
    "ENGLISH_PROMPT_VERSION",
    "JobAnalysisServiceV20",
    "PROMPT_VERSION",
    "_ANALYSIS_SCHEMA_V20",
    "_ENGLISH_SYSTEM_PROMPT_V20",
]
