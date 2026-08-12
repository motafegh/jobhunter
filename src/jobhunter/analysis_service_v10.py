"""P1.6 v10 candidate for heterogeneous sparse-source acceptance.

This module intentionally leaves the accepted v9 production path untouched while CI-3
validates a stricter factual contract against sparse postings.  Promotion to the public
analysis service is a separate acceptance decision.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from jobhunter.analysis_service import (
    _ANALYSIS_SCHEMA,
    _ENGLISH_SYSTEM_PROMPT,
    ANALYSIS_SCHEMA_VERSION,
    AnalysisJobResult,
    AnalysisValidationError,
    JobAnalysisService,
    _analysis_fields_for_english,
    _persisted_analysis,
    _result,
    _validate_evidence,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

ENGLISH_PROMPT_VERSION = "job-analysis-english-v10"
PROMPT_VERSION = ENGLISH_PROMPT_VERSION

_V10_RULES = """

P1.6 V10 CANDIDATE — SPARSE / STRUCTURED-SKILL BOUNDARY:
- The top-level skills array is an explicit structured job requirement surface. Every non-empty
  skills item MUST be represented by a requirement that cites that exact skills item as evidence.
  Do not omit a structured skill merely because related wording also appears in description text.
- Preserve structured skills as required unless the exact structured skill evidence itself states
  otherwise. Do not weaken them to contextual just because a nearby prose sentence is ambiguous.
- Qualification wording such as "ability to X", "skill(s) in X", "knowledge of X",
  "experience with X", or "familiarity with X" belongs under requirements unless the source
  independently frames X as an employee duty/action.
- Do not convert availability, employment arrangement, teachability, location, benefits, or
  candidate traits into responsibilities.
- A responsibility must have duty evidence that is narrower than qualification evidence. If the
  same exact source span is already being used as a requirement and no narrower duty excerpt
  exists, omit the responsibility rather than paraphrasing the qualification into a verb phrase.
"""

_ENGLISH_SYSTEM_PROMPT_V10 = _ENGLISH_SYSTEM_PROMPT + _V10_RULES


def _normalize(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def _structured_skills(fields: dict[str, Any]) -> list[str]:
    value = fields.get("skills")
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def validate_v10_candidate_structured(
    structured: dict[str, Any],
    analysis_fields: dict[str, Any],
) -> None:
    """Validate v10-only sparse/structured-skill semantics before persistence.

    This is intentionally additional to the existing Instructor/Pydantic v9 checks.  It
    does not mutate model output; it either proves the candidate obeyed the v10 boundary or
    fails closed so the bounded candidate provider can request one correction.
    """

    requirements = structured.get("requirements") or []
    responsibilities = structured.get("responsibilities") or []
    if not isinstance(requirements, list) or not isinstance(responsibilities, list):
        raise AnalysisValidationError("P1.6 v10 candidate arrays are malformed")

    requirements_by_evidence: dict[str, list[dict[str, Any]]] = {}
    for item in requirements:
        if not isinstance(item, dict):
            raise AnalysisValidationError("P1.6 v10 requirement item is malformed")
        evidence = item.get("evidence")
        if isinstance(evidence, str) and evidence.strip():
            requirements_by_evidence.setdefault(_normalize(evidence), []).append(item)

    missing_skills: list[str] = []
    wrong_strength: list[str] = []
    for skill in _structured_skills(analysis_fields):
        matches = requirements_by_evidence.get(_normalize(skill), [])
        if not matches:
            missing_skills.append(skill)
            continue
        if not any(item.get("requirement_type") == "required" for item in matches):
            wrong_strength.append(skill)
    if missing_skills:
        raise AnalysisValidationError(
            "P1.6 v10 omitted structured required skills: " + ", ".join(missing_skills)
        )
    if wrong_strength:
        raise AnalysisValidationError(
            "P1.6 v10 changed structured-skill obligation away from required: "
            + ", ".join(wrong_strength)
        )

    requirement_evidence = set(requirements_by_evidence)
    for index, item in enumerate(responsibilities):
        if not isinstance(item, dict):
            raise AnalysisValidationError("P1.6 v10 responsibility item is malformed")
        statement = str(item.get("statement") or "").strip()
        evidence = str(item.get("evidence") or "").strip()
        normalized_statement = _normalize(statement)
        normalized_evidence = _normalize(evidence)
        if normalized_evidence in requirement_evidence:
            raise AnalysisValidationError(
                f"P1.6 v10 responsibility[{index}] reuses exact qualification evidence; "
                "cite a narrower explicit duty span or omit the responsibility"
            )
        if normalized_statement and f"ability to {normalized_statement}" in normalized_evidence:
            raise AnalysisValidationError(
                f"P1.6 v10 responsibility[{index}] paraphrases 'ability to ...' qualification "
                "wording as employee work"
            )
        if normalized_evidence.startswith(
            (
                "ability to ",
                "skill in ",
                "skills in ",
                "knowledge of ",
                "experience with ",
                "familiarity with ",
            )
        ):
            raise AnalysisValidationError(
                f"P1.6 v10 responsibility[{index}] is grounded in qualification wording"
            )


def _persisted_analysis_v10(
    structured: dict[str, Any],
    analysis_fields: dict[str, Any],
) -> dict[str, Any]:
    """Persist v9 coverage plus deterministic accounting for structured required skills."""

    analysis = _persisted_analysis(structured, analysis_fields)
    coverage = analysis.setdefault("coverage", [])
    covered = {
        _normalize(str(item.get("evidence") or ""))
        for item in coverage
        if isinstance(item, dict)
    }
    requirement_evidence = {
        _normalize(str(item.get("evidence") or ""))
        for item in analysis.get("requirements") or []
        if isinstance(item, dict)
    }
    for skill in _structured_skills(analysis_fields):
        normalized = _normalize(skill)
        if normalized not in requirement_evidence:
            raise AnalysisValidationError(
                f"Structured skill disappeared before v10 persistence: {skill!r}"
            )
        if normalized in covered:
            continue
        coverage.append(
            {
                "evidence": skill,
                "disposition": "extracted_requirement",
                "rationale": "P1.6 v10 deterministic structured required-skill coverage.",
            }
        )
        covered.add(normalized)
    return analysis


class JobAnalysisServiceV10(JobAnalysisService):
    """Persist an isolated English P1.6 v10 candidate without promoting v9 globally."""

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
                system_prompt=_ENGLISH_SYSTEM_PROMPT_V10,
                user_payload={
                    "source_job_id": source.source_job_id,
                    "analysis_mode": "english",
                    "analysis_fields": analysis_fields,
                },
                schema_name="jobhunter_job_analysis_english_v10",
                schema=_ANALYSIS_SCHEMA,
                model=self._model,
                max_tokens=self._max_tokens,
            )
            validate_v10_candidate_structured(result.structured, analysis_fields)
            analysis = _persisted_analysis_v10(result.structured, analysis_fields)
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
                raise RuntimeError("P1.6 v10 artifact disappeared after persistence")
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
    "JobAnalysisServiceV10",
    "PROMPT_VERSION",
    "validate_v10_candidate_structured",
]
