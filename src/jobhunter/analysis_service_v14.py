"""P1.6 v14 candidate with complete residual coverage and normalized capability concepts.

v13 proved deterministic coarse-span decomposition but semantic review found that suppressing the
whole coarse span could hide requirement-bearing residual prose, and one normalized concept still
mixed a capability with full-time/part-time schedule wording. v14 keeps the exact-source item
coverage and replaces each suppressed coarse span with complete candidate subcoverage: mandatory
qualification items plus exact residual sentences that must be extracted or explicitly excluded.
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
    JobAnalysisService,
    _analysis_fields_for_english,
    _result,
)
from jobhunter.analysis_service_v11 import qualification_list_spans
from jobhunter.analysis_service_v13 import (
    _ENGLISH_SYSTEM_PROMPT_V13,
    _persisted_analysis_v13,
    _validate_evidence_v13,
    decomposed_requirement_references,
    inject_decomposition_exclusions,
    validate_v13_candidate_structured,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

ENGLISH_PROMPT_VERSION = "job-analysis-english-v14"
PROMPT_VERSION = ENGLISH_PROMPT_VERSION

_SENTENCE_RE = re.compile(r"[^.!?]+(?:[.!?]|$)")
_ABILITY_WRAPPER_RE = re.compile(r"^ability\s+to\b", re.I)
_SCHEDULE_IN_CONCEPT_RE = re.compile(r"\b(?:full[ -]?time|part[ -]?time)\b", re.I)

_V14_RULES = """

P1.6 V14 CANDIDATE — COMPLETE DECOMPOSITION + CAPABILITY NORMALIZATION:
- When JobHunter decomposes a broad requirement span, candidate_required_qualification_references
  are mandatory exact qualification items and candidate_residual_requirement_references are the
  remaining exact source sentences from the same suppressed span.
- Every residual requirement reference must be either represented by a requirement or explicitly
  excluded through coverage_exclusions. Exclude residual text when it is not a candidate career
  qualification, for example teachability, benefits, location, application instructions, or work
  arrangement/logistics.
- Do not silently omit explicit employer expectations that remain in residual evidence. If a
  residual sentence states a candidate trait or qualification as important/required, preserve it.
- A normalized capability concept names the underlying skill/knowledge/practice/trait. Do not use
  the qualification wrapper 'Ability to ...' as the concept itself, and do not include full-time
  or part-time schedule wording in a capability concept. Keep the exact evidence unchanged.
- Keep all v13 exact-evidence, structured-skill, qualification-vs-duty, depth, and deterministic
  decomposition rules.
"""

_ENGLISH_SYSTEM_PROMPT_V14 = _ENGLISH_SYSTEM_PROMPT_V13 + _V14_RULES


def residual_requirement_spans(analysis_fields: dict[str, Any]) -> list[str]:
    """Return exact residual sentences after the final detected qualification-list item.

    This candidate helper activates only when deterministic qualification-list decomposition is
    present. The returned text is exact source text from the same description; it is not inferred
    or normalized. Residual sentences are model-classified as requirement vs. non-requirement.
    """

    description = analysis_fields.get("description")
    if not isinstance(description, str):
        return []
    spans = qualification_list_spans(analysis_fields)
    if len(spans) < 2:
        return []

    cursor = 0
    last_end: int | None = None
    for span in spans:
        position = description.find(span, cursor)
        if position < 0:
            # The first item may include a recognized heading token removed by legacy section
            # segmentation. Continue locating later exact items; decomposition is still bounded
            # by the last exact qualification occurrence we can prove.
            continue
        last_end = position + len(span)
        cursor = last_end
    if last_end is None:
        return []

    tail = description[last_end:]
    leading = len(tail) - len(tail.lstrip(" \t\r\n,;:-"))
    tail = tail[leading:]
    if not tail:
        return []

    return [
        match.group(0).strip()
        for match in _SENTENCE_RE.finditer(tail)
        if match.group(0).strip()
    ][:32]


def _normalize(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def validate_v14_candidate_structured(
    structured: dict[str, Any], analysis_fields: dict[str, Any]
) -> None:
    """Validate v13 semantics plus normalized capability concepts."""

    validate_v13_candidate_structured(structured, analysis_fields)
    for index, item in enumerate(structured.get("requirements") or []):
        if not isinstance(item, dict):
            continue
        concept = str(item.get("concept") or "").strip()
        concept_type = str(item.get("concept_type") or "")
        if concept_type in {"skill", "knowledge", "practice", "domain", "experience", "tool"}:
            if _ABILITY_WRAPPER_RE.search(concept):
                raise AnalysisValidationError(
                    f"P1.6 v14 requirement[{index}] concept keeps an 'Ability to ...' wrapper; "
                    "normalize to the underlying capability noun phrase"
                )
            if _SCHEDULE_IN_CONCEPT_RE.search(concept):
                raise AnalysisValidationError(
                    f"P1.6 v14 requirement[{index}] concept mixes capability with full-time/"
                    "part-time schedule wording"
                )


def _persisted_analysis_v14(
    structured: dict[str, Any], analysis_fields: dict[str, Any]
) -> dict[str, Any]:
    """Persist v13 provenance plus complete residual requirement accounting."""

    residuals = residual_requirement_spans(analysis_fields)
    residual_refs = {
        f"field:__candidate_residual_requirement_evidence:{index}": text
        for index, text in enumerate(residuals)
    }
    original_exclusions = []
    residual_exclusions: dict[str, dict[str, Any]] = {}
    for item in structured.get("coverage_exclusions") or []:
        if not isinstance(item, dict):
            continue
        reference = str(item.get("evidence_reference") or "").strip()
        if reference in residual_refs:
            residual_exclusions[reference] = item
        else:
            original_exclusions.append(dict(item))

    base_structured = dict(structured)
    base_structured["coverage_exclusions"] = original_exclusions
    analysis = _persisted_analysis_v13(base_structured, analysis_fields)
    coverage = analysis.setdefault("coverage", [])
    requirements_by_evidence = {
        _normalize(str(item.get("evidence") or ""))
        for item in analysis.get("requirements") or []
        if isinstance(item, dict)
    }

    for reference, evidence in residual_refs.items():
        if _normalize(evidence) in requirements_by_evidence:
            disposition = "extracted_requirement"
            rationale = "A persisted requirement cites this exact residual coverage input."
        else:
            exclusion = residual_exclusions.get(reference)
            if exclusion is None:
                raise AnalysisValidationError(
                    f"Unaccounted v14 residual requirement coverage reference: {reference!r}"
                )
            disposition = "excluded_non_requirement"
            rationale = str(exclusion.get("rationale") or "")
        coverage.append(
            {
                "evidence": evidence,
                "disposition": disposition,
                "rationale": rationale,
            }
        )
    return analysis


class JobAnalysisServiceV14(JobAnalysisService):
    """Persist an isolated English P1.6 v14 candidate without promoting public v9."""

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
                system_prompt=_ENGLISH_SYSTEM_PROMPT_V14,
                user_payload={
                    "source_job_id": source.source_job_id,
                    "analysis_mode": "english",
                    "analysis_fields": analysis_fields,
                },
                schema_name="jobhunter_job_analysis_english_v14",
                schema=_ANALYSIS_SCHEMA,
                model=self._model,
                max_tokens=self._max_tokens,
            )
            validate_v14_candidate_structured(result.structured, analysis_fields)
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
                raise RuntimeError("P1.6 v14 artifact disappeared after persistence")
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
    "JobAnalysisServiceV14",
    "PROMPT_VERSION",
    "decomposed_requirement_references",
    "inject_decomposition_exclusions",
    "qualification_list_spans",
    "residual_requirement_spans",
    "validate_v14_candidate_structured",
]
