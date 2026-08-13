"""P1.6 v13 candidate with deterministic coarse-coverage decomposition.

v12 proved that the model can preserve the sparse qualification facts once they are exposed as
first-class evidence references. Its remaining failure was mechanical: the generic Instructor
coverage layer still required the model to account for one coarse requirement span that JobHunter
had already decomposed into exact qualification items. v13 moves that bookkeeping back to
JobHunter while leaving the accepted/public v9 path unchanged.
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
from jobhunter.evidence_refs import build_requirement_coverage_plan
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

ENGLISH_PROMPT_VERSION = "job-analysis-english-v13"
PROMPT_VERSION = ENGLISH_PROMPT_VERSION

_V13_RULES = """

P1.6 V13 CANDIDATE — FIRST-CLASS QUALIFICATION REFERENCES + DETERMINISTIC DECOMPOSITION:
- candidate_required_qualification_references contains JobHunter evidence-reference IDs, not raw
  employer text. Every listed ID MUST be cited by one requirement's evidence field.
- The referenced text is also present in evidence_references. Follow the normal P1.6 evidence
  protocol: cite the ID exactly; do not copy or paraphrase the referenced text into evidence.
- Evidence IDs beginning with field:__candidate_qualification_evidence: are JobHunter-generated
  exact-source aliases copied verbatim from the real description solely to make deterministic
  qualification items addressable. They are not new employer facts.
- JobHunter may omit a broad legacy requirement_coverage item when it has mechanically proven
  that the same source span is decomposed into multiple mandatory item-level qualification
  references. Do not recreate that coarse paragraph as a catch-all requirement.
- Do not add a coverage_exclusion merely to satisfy bookkeeping for a deterministically decomposed
  span. JobHunter owns and persists that decomposition provenance after semantic generation.
- Preserve structured required skills, qualification-vs-duty separation, source obligation
  strength, and exact evidence. Qualification wording is not technical depth.
"""

_ENGLISH_SYSTEM_PROMPT_V13 = _ENGLISH_SYSTEM_PROMPT_V11 + _V13_RULES


def _normalize(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def _span_count(evidence: str, spans: list[str]) -> int:
    normalized = _normalize(evidence)
    return sum(1 for span in spans if _normalize(span) in normalized)


def decomposed_requirement_references(analysis_fields: dict[str, Any]) -> list[str]:
    """Return coarse coverage IDs mechanically superseded by exact qualification items."""

    spans = qualification_list_spans(analysis_fields)
    if len(spans) < 2:
        return []
    plan = build_requirement_coverage_plan(analysis_fields)
    return [
        reference
        for reference, candidate in plan.items()
        if candidate.get("allow_exclusion", False)
        and _span_count(str(candidate.get("text") or ""), spans) >= 2
    ]


def inject_decomposition_exclusions(
    structured: dict[str, Any],
    analysis_fields: dict[str, Any],
) -> dict[str, Any]:
    """Attach deterministic bookkeeping required by legacy persistence, not by the model."""

    result = dict(structured)
    exclusions = [
        dict(item)
        for item in (structured.get("coverage_exclusions") or [])
        if isinstance(item, dict)
    ]
    existing = {
        str(item.get("evidence_reference") or "").strip()
        for item in exclusions
    }
    for reference in decomposed_requirement_references(analysis_fields):
        if reference in existing:
            continue
        exclusions.append(
            {
                "evidence_reference": reference,
                "rationale": (
                    "JobHunter deterministically decomposed this coarse requirement span into "
                    "exact item-level qualification requirements."
                ),
            }
        )
    result["coverage_exclusions"] = exclusions
    return result


def validate_v13_candidate_structured(
    structured: dict[str, Any],
    analysis_fields: dict[str, Any],
) -> None:
    """Validate granular semantics plus deterministic decomposition bookkeeping."""

    validate_v11_candidate_structured(structured, analysis_fields)
    required = set(decomposed_requirement_references(analysis_fields))
    exclusions = {
        str(item.get("evidence_reference") or "").strip()
        for item in (structured.get("coverage_exclusions") or [])
        if isinstance(item, dict)
    }
    missing = sorted(required - exclusions)
    if missing:
        raise AnalysisValidationError(
            "P1.6 v13 is missing deterministic decomposition bookkeeping: "
            + ", ".join(missing)
        )


def _persisted_analysis_v13(
    structured: dict[str, Any],
    analysis_fields: dict[str, Any],
) -> dict[str, Any]:
    """Persist v11 item coverage and truthful decomposed_requirement provenance."""

    return _persisted_analysis_v11(structured, analysis_fields)


class JobAnalysisServiceV13(JobAnalysisService):
    """Persist an isolated English P1.6 v13 candidate without promoting v9 globally."""

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
                system_prompt=_ENGLISH_SYSTEM_PROMPT_V13,
                user_payload={
                    "source_job_id": source.source_job_id,
                    "analysis_mode": "english",
                    "analysis_fields": analysis_fields,
                },
                schema_name="jobhunter_job_analysis_english_v13",
                schema=_ANALYSIS_SCHEMA,
                model=self._model,
                max_tokens=self._max_tokens,
            )
            structured = inject_decomposition_exclusions(result.structured, analysis_fields)
            validate_v13_candidate_structured(structured, analysis_fields)
            analysis = _persisted_analysis_v13(structured, analysis_fields)
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
                raise RuntimeError("P1.6 v13 artifact disappeared after persistence")
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
    "JobAnalysisServiceV13",
    "PROMPT_VERSION",
    "decomposed_requirement_references",
    "inject_decomposition_exclusions",
    "qualification_list_spans",
    "validate_v13_candidate_structured",
]
