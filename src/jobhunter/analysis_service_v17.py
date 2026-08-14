"""P1.6 v17 candidate with source-led requirement capacity.

v16 passed the sparse semantic gate but the dense tG9K regression exposed an inherited contract
collision: accepted dense facts plus structured ``skills[]`` coverage can require more than the
legacy 32 requirement slots. v17 changes only representation capacity. It preserves v16 factual,
coverage, strength, depth, concept-type, and responsibility semantics.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from typing import Any

from jobhunter.analysis_service import (
    _ANALYSIS_SCHEMA,
    AnalysisJobResult,
    AnalysisValidationError,
    _analysis_fields_for_english,
    _result,
)
from jobhunter.analysis_service_v13 import _validate_evidence_v13
from jobhunter.analysis_service_v14 import _persisted_analysis_v14
from jobhunter.analysis_service_v16 import (
    _ENGLISH_SYSTEM_PROMPT_V16,
    JobAnalysisServiceV16,
    validate_v16_candidate_structured,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ENGLISH_PROMPT_VERSION = "job-analysis-english-v17"
PROMPT_VERSION = ENGLISH_PROMPT_VERSION
ANALYSIS_SCHEMA_VERSION = "job-analysis-v5"

_V17_RULES = """

P1.6 V17 CANDIDATE — SOURCE-LED REQUIREMENT CAPACITY:
- The number of requirement records follows supported source assertions and required coverage; it
  is not a quota and has no fixed 32-item semantic ceiling.
- Do not omit, merge, weaken, or exclude a valid source assertion merely to reduce the requirement
  count. Distinct source surfaces remain distinct when their evidence or semantics differ.
- Keep all v16 exact-evidence, coverage, structured-skill, qualification-vs-duty, optionality,
  depth, concept-normalization, and concept-type rules unchanged.
"""

_ENGLISH_SYSTEM_PROMPT_V17 = _ENGLISH_SYSTEM_PROMPT_V16 + _V17_RULES

_ANALYSIS_SCHEMA_V17 = deepcopy(_ANALYSIS_SCHEMA)
_ANALYSIS_SCHEMA_V17["properties"]["requirements"].pop("maxItems", None)

_LEGACY_FINAL_GUARD_REQUIREMENT_BATCH = 32


def _normalize(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def _validate_evidence_v17(
    analysis: dict[str, Any], analysis_fields: dict[str, Any]
) -> None:
    """Reuse the accepted independent guard without inheriting its old cardinality ceiling.

    The accepted v9/v4 guard remains unchanged and still rejects more than 32 requirements. V17
    validates the same persisted artifact in bounded requirement batches, then separately proves
    global requirement uniqueness so duplicates cannot hide across batch boundaries.
    """

    requirements = analysis.get("requirements")
    if not isinstance(requirements, list):
        raise AnalysisValidationError("Analysis requirements array is malformed")

    seen: set[tuple[str, str, str]] = set()
    for index, item in enumerate(requirements):
        if not isinstance(item, dict):
            raise AnalysisValidationError(f"requirement[{index}] is malformed")
        key = (
            _normalize(str(item.get("concept") or "")),
            str(item.get("requirement_type") or ""),
            _normalize(str(item.get("evidence") or "")),
        )
        if key in seen:
            raise AnalysisValidationError(
                f"requirement[{index}] duplicates an earlier requirement claim"
            )
        seen.add(key)

    if not requirements:
        _validate_evidence_v13(analysis, analysis_fields)
        return

    for start in range(0, len(requirements), _LEGACY_FINAL_GUARD_REQUIREMENT_BATCH):
        validation_slice = dict(analysis)
        validation_slice["requirements"] = requirements[
            start : start + _LEGACY_FINAL_GUARD_REQUIREMENT_BATCH
        ]
        _validate_evidence_v13(validation_slice, analysis_fields)


def validate_v17_candidate_structured(
    structured: dict[str, Any], analysis_fields: dict[str, Any]
) -> None:
    """V17 intentionally changes only capacity; all v16 semantic guards remain authoritative."""

    validate_v16_candidate_structured(structured, analysis_fields)


class JobAnalysisServiceV17(JobAnalysisServiceV16):
    """Persist isolated English P1.6 v17 artifacts under the new v5 schema identity."""

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

    def _record_failed_attempt(
        self,
        *,
        source: TranslationSourceVersion,
        attempted_at: datetime,
        prompt_version: str,
        error: Exception,
    ) -> None:
        self._analysis_store.record_attempt(
            job_detail_version_id=source.job_detail_version_id,
            attempted_at=attempted_at,
            model=self._model,
            prompt_version=prompt_version,
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
                system_prompt=_ENGLISH_SYSTEM_PROMPT_V17,
                user_payload={
                    "source_job_id": source.source_job_id,
                    "analysis_mode": "english",
                    "analysis_fields": analysis_fields,
                },
                schema_name="jobhunter_job_analysis_english_v17",
                schema=_ANALYSIS_SCHEMA_V17,
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
                raise RuntimeError("P1.6 v17 artifact disappeared after persistence")
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
    "JobAnalysisServiceV17",
    "PROMPT_VERSION",
    "_ANALYSIS_SCHEMA_V17",
    "_ENGLISH_SYSTEM_PROMPT_V17",
    "_validate_evidence_v17",
    "validate_v17_candidate_structured",
]
