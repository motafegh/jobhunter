"""P1.6 v12 candidate with first-class qualification evidence references.

v11 identified the right sparse qualification items, but its model-facing contract asked the
model to copy raw candidate spans while the production P1.6 evidence protocol requires evidence
reference IDs. v12 preserves the v11 semantic boundary and changes only that evidence plumbing:
every deterministic qualification item is exposed through a normal evidence reference before
inference. The accepted/public v9 path remains unchanged.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from jobhunter.analysis_service import (
    _ANALYSIS_SCHEMA,
    ANALYSIS_SCHEMA_VERSION,
    AnalysisJobResult,
    AnalysisValidationError,
    JobAnalysisService,
    _analysis_fields_for_english,
    _result,
    _validate_evidence,
)
from jobhunter.analysis_service_v11 import (
    _ENGLISH_SYSTEM_PROMPT_V11,
    _persisted_analysis_v11,
    qualification_list_spans,
    validate_v11_candidate_structured,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

ENGLISH_PROMPT_VERSION = "job-analysis-english-v12"
PROMPT_VERSION = ENGLISH_PROMPT_VERSION

_V12_RULES = """

P1.6 V12 CANDIDATE — FIRST-CLASS QUALIFICATION EVIDENCE REFERENCES:
- candidate_required_qualification_references contains JobHunter evidence-reference IDs, not raw
  employer text. Every listed ID MUST be cited by one requirement's evidence field.
- The referenced text is also present in evidence_references. Follow the normal P1.6 evidence
  protocol: cite the ID exactly; do not copy or paraphrase the referenced text into evidence.
- Evidence references whose IDs start with field:__candidate_qualification_evidence: are
  JobHunter-generated exact-source aliases. Their text is copied verbatim from the real
  description solely to make deterministic qualification items addressable. They are not an
  additional employer field and must not create facts beyond the referenced source excerpt.
- Keep the v11 decomposition rule: when a broad legacy requirement_coverage span contains
  multiple mandatory qualification references, exclude the broad coverage ID as superseded by
  exact item-level requirements rather than emitting a catch-all requirement.
"""

_ENGLISH_SYSTEM_PROMPT_V12 = _ENGLISH_SYSTEM_PROMPT_V11 + _V12_RULES


def validate_v12_candidate_structured(
    structured: dict[str, Any],
    analysis_fields: dict[str, Any],
) -> None:
    """Reuse the accepted v11 semantic checks after v12 evidence canonicalization."""

    validate_v11_candidate_structured(structured, analysis_fields)


def _persisted_analysis_v12(
    structured: dict[str, Any],
    analysis_fields: dict[str, Any],
) -> dict[str, Any]:
    """Persist the v11 granular/decomposition provenance under a new contract identity."""

    return _persisted_analysis_v11(structured, analysis_fields)


class JobAnalysisServiceV12(JobAnalysisService):
    """Persist an isolated English P1.6 v12 candidate without promoting v9 globally."""

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
            raise AnalysisValidationError(
                "Job has no current successfully parsed source version"
            )
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
                system_prompt=_ENGLISH_SYSTEM_PROMPT_V12,
                user_payload={
                    "source_job_id": source.source_job_id,
                    "analysis_mode": "english",
                    "analysis_fields": analysis_fields,
                },
                schema_name="jobhunter_job_analysis_english_v12",
                schema=_ANALYSIS_SCHEMA,
                model=self._model,
                max_tokens=self._max_tokens,
            )
            validate_v12_candidate_structured(result.structured, analysis_fields)
            analysis = _persisted_analysis_v12(result.structured, analysis_fields)
            _validate_evidence(analysis, analysis_fields)
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
                raise RuntimeError("P1.6 v12 artifact disappeared after persistence")
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
    "JobAnalysisServiceV12",
    "PROMPT_VERSION",
    "qualification_list_spans",
    "validate_v12_candidate_structured",
]
