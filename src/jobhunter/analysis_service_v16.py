"""P1.6 v16 candidate with clean concept normalization and experience-type guard.

v15 solved sparse coverage, residual-strength, trait ontology, and schedule/wrapper handling, but
its persisted t4jp artifact exposed two final semantic defects in one qualification: normalization
left empty punctuation and the model typed explicit ability evidence as prior experience. v16 keeps
all v15 behavior and tightens only those boundaries.
"""

from __future__ import annotations

import re
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
from jobhunter.analysis_service_v14 import _persisted_analysis_v14
from jobhunter.analysis_service_v15 import (
    _ENGLISH_SYSTEM_PROMPT_V15,
    JobAnalysisServiceV15,
    validate_v15_candidate_structured,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

ENGLISH_PROMPT_VERSION = "job-analysis-english-v16"
PROMPT_VERSION = ENGLISH_PROMPT_VERSION

_V16_RULES = """

P1.6 V16 CANDIDATE — CLEAN CONCEPTS + EXPERIENCE EVIDENCE:
- A normalized concept must be a clean reusable concept label. Removing schedule or linguistic
  wrapper text must not leave empty grouping punctuation or separator debris such as `( )`.
- concept_type=experience means prior applied exposure supported by the exact source evidence.
  Do not use experience merely because the source says a candidate has an ability to perform an
  activity. Explicit ability/proficiency to perform an activity is normally a skill unless the
  source separately states prior applied exposure.
- Keep all v15 coverage, residual-strength, concept-type, qualification-vs-duty, optionality,
  exact-evidence, and depth rules unchanged.
"""

_ENGLISH_SYSTEM_PROMPT_V16 = _ENGLISH_SYSTEM_PROMPT_V15 + _V16_RULES
_EMPTY_GROUP_RE = re.compile(r"(?:\(\s*\)|\[\s*\]|\{\s*\})")
_ABILITY_EVIDENCE_RE = re.compile(r"\bability\s+to\b", re.I)
_EXPERIENCE_EVIDENCE_RE = re.compile(
    r"\b(?:experience|experienced|years?|worked|working background|prior background)\b",
    re.I,
)


def validate_v16_candidate_structured(
    structured: dict[str, Any], analysis_fields: dict[str, Any]
) -> None:
    """Reuse v15 guards and reject malformed concepts or unsupported experience typing."""

    validate_v15_candidate_structured(structured, analysis_fields)
    requirements = structured.get("requirements") or []
    for index, item in enumerate(requirements):
        if not isinstance(item, dict):
            continue
        concept = str(item.get("concept") or "").strip()
        concept_type = str(item.get("concept_type") or "").strip()
        evidence = str(item.get("evidence") or "").strip()
        if _EMPTY_GROUP_RE.search(concept):
            raise AnalysisValidationError(
                f"P1.6 v16 requirement[{index}] concept contains empty punctuation debris"
            )
        if (
            concept_type == "experience"
            and _ABILITY_EVIDENCE_RE.search(evidence)
            and not _EXPERIENCE_EVIDENCE_RE.search(evidence)
        ):
            raise AnalysisValidationError(
                f"P1.6 v16 requirement[{index}] types explicit ability evidence as experience "
                "without prior-exposure evidence"
            )


class JobAnalysisServiceV16(JobAnalysisServiceV15):
    """Persist an isolated English P1.6 v16 candidate without promoting public v9."""

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
                system_prompt=_ENGLISH_SYSTEM_PROMPT_V16,
                user_payload={
                    "source_job_id": source.source_job_id,
                    "analysis_mode": "english",
                    "analysis_fields": analysis_fields,
                },
                schema_name="jobhunter_job_analysis_english_v16",
                schema=_ANALYSIS_SCHEMA,
                model=self._model,
                max_tokens=self._max_tokens,
            )
            validate_v16_candidate_structured(result.structured, analysis_fields)
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
                raise RuntimeError("P1.6 v16 artifact disappeared after persistence")
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
    "JobAnalysisServiceV16",
    "PROMPT_VERSION",
    "validate_v16_candidate_structured",
]
