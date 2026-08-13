"""P1.6 v15 candidate with neutral residual strength and explicit concept-type semantics.

v14 achieved complete sparse-source coverage but its live t4jp artifact exposed two remaining
semantic issues: a behavioral/value expectation was typed as a skill, and candidate residual
coverage was mechanically marked required regardless of source wording. v15 preserves v14's
complete decomposition, exact evidence, responsibility boundary, concept normalization, and
schedule/depth handling while tightening only those two boundaries.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from jobhunter.analysis_service import (
    _ANALYSIS_SCHEMA,
    ANALYSIS_SCHEMA_VERSION,
    AnalysisJobResult,
    AnalysisValidationError,
    _analysis_fields_for_english,
    _result,
)
from jobhunter.analysis_service_v13 import _validate_evidence_v13
from jobhunter.analysis_service_v14 import (
    _ENGLISH_SYSTEM_PROMPT_V14,
    JobAnalysisServiceV14,
    _persisted_analysis_v14,
    validate_v14_candidate_structured,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

ENGLISH_PROMPT_VERSION = "job-analysis-english-v15"
PROMPT_VERSION = ENGLISH_PROMPT_VERSION

_V15_RULES = """

P1.6 V15 CANDIDATE — CONCEPT TYPE + RESIDUAL STRENGTH:
- Coverage obligation and employer requirement strength are separate. A residual coverage item must
  be accounted for, but do not assume it is required merely because JobHunter surfaced it for
  review. Determine required/preferred/contextual only from the exact source wording.
- concept_type must describe what kind of concept the employer is expressing, not how strongly the
  employer wants it.
- Use skill for an ability/proficiency to perform a task or activity; tool for a named technology or
  instrument; knowledge for subject-matter understanding; practice for a method/discipline; domain
  for an industry/problem area; experience for prior applied exposure; education for credentials.
- Use other for explicit candidate traits, values, behavioral expectations, or professional
  qualities that do not fit the technical/capability categories above. Do not label such a trait as
  skill merely because the employer considers it important or required.
- Keep all v14 complete-decomposition, exact-evidence, qualification-vs-duty, normalized-concept,
  optionality, and depth rules unchanged.
"""

_ENGLISH_SYSTEM_PROMPT_V15 = _ENGLISH_SYSTEM_PROMPT_V14 + _V15_RULES


def validate_v15_candidate_structured(
    structured: dict[str, Any], analysis_fields: dict[str, Any]
) -> None:
    """Reuse v14 mechanical/semantic guards; v15 type semantics remain model-judged and reviewed."""

    validate_v14_candidate_structured(structured, analysis_fields)


class JobAnalysisServiceV15(JobAnalysisServiceV14):
    """Persist an isolated English P1.6 v15 candidate without promoting public v9."""

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
        super().__init__(
            source_store=source_store,
            translation_service=translation_service,
            analysis_store=analysis_store,
            provider=provider,
            model=model,
            max_tokens=max_tokens,
            clock=clock,
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
                system_prompt=_ENGLISH_SYSTEM_PROMPT_V15,
                user_payload={
                    "source_job_id": source.source_job_id,
                    "analysis_mode": "english",
                    "analysis_fields": analysis_fields,
                },
                schema_name="jobhunter_job_analysis_english_v15",
                schema=_ANALYSIS_SCHEMA,
                model=self._model,
                max_tokens=self._max_tokens,
            )
            validate_v15_candidate_structured(result.structured, analysis_fields)
            analysis = _persisted_analysis_v14(result.structured, analysis_fields)
            _validate_evidence_v13(analysis, analysis_fields)
        except Exception as exc:
            self._record_failed_attempt(
                source=source,
                attempted_at=attempted_at,
                prompt_version=ENGLISH_PROMPT_VERSION,
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
                raise RuntimeError("P1.6 v15 artifact disappeared after persistence")
            return _result(artifact, outcome="completed", analysis_mode="english")
        except Exception as exc:
            self._record_failed_attempt(
                source=source,
                attempted_at=attempted_at,
                prompt_version=ENGLISH_PROMPT_VERSION,
                error=exc,
            )
            raise

    def analyze_job(self, source_job_id: str) -> AnalysisJobResult:
        return self.analyze_english_job(source_job_id)


__all__ = [
    "ANALYSIS_SCHEMA_VERSION",
    "ENGLISH_PROMPT_VERSION",
    "JobAnalysisServiceV15",
    "PROMPT_VERSION",
    "validate_v15_candidate_structured",
]
