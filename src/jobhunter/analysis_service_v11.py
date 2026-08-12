"""P1.6 v11 candidate with sparse qualification-list coverage.

v10 fixed structured ``skills[]`` coverage and qualification-vs-duty leakage. v11 keeps
those boundaries and additionally makes comma-separated qualification lists reviewable at
item granularity. The accepted/public v9 path remains unchanged until heterogeneous
acceptance promotes a newer contract.
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
    _validate_evidence,
)
from jobhunter.analysis_service_v10 import (
    _ENGLISH_SYSTEM_PROMPT_V10,
    _normalize,
    _persisted_analysis_v10,
    validate_v10_candidate_structured,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

ENGLISH_PROMPT_VERSION = "job-analysis-english-v11"
PROMPT_VERSION = ENGLISH_PROMPT_VERSION

_QUALIFICATION_START_RE = re.compile(
    r"^(?:skills?\s+in|ability\s+to|knowledge\s+of|experience\s+(?:with|in)|"
    r"familiarity\s+with|proficiency\s+(?:in|with)|proficient\s+(?:in|with)|"
    r"expertise\s+in|competenc(?:e|y)\s+in|creativity\s+in|understanding\s+of)\b",
    re.I,
)
_FINITE_OR_DIRECTIVE_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|being|has|have|had|must|should|will|would|"
    r"can|could|may|might|please|do|does|did)\b",
    re.I,
)
_SENTENCE_RE = re.compile(r"[^.!?]+(?:[.!?]|$)")

_V11_RULES = """

P1.6 V11 CANDIDATE — QUALIFICATION-LIST GRANULARITY:
- candidate_required_qualification_spans contains exact source excerpts from a sentence that
  clearly begins as a qualification list. Every listed span MUST be represented by its own
  requirement citing that exact span as evidence.
- Do not satisfy one qualification-list item by citing a neighboring item or the whole paragraph.
- Preserve the actual source meaning. A structured skill tag and a narrower description phrase
  are separate facts when they are not semantically equivalent (for example a broad technology
  tag versus using that technology for a particular kind of work).
- Bare short noun phrases that continue an explicit comma-separated qualification list are still
  qualification items; do not drop them merely because the qualification marker appears only in
  the first item.
"""

_ENGLISH_SYSTEM_PROMPT_V11 = _ENGLISH_SYSTEM_PROMPT_V10 + _V11_RULES


def _looks_like_list_continuation(clause: str) -> bool:
    """Return whether a comma clause plausibly continues an explicit qualification list."""

    text = clause.strip().strip(".;")
    if not text:
        return False
    if _QUALIFICATION_START_RE.search(text):
        return True
    # Short noun/adjective phrases are common continuation items ("SQL", "website design").
    # Stop when prose becomes a finite clause/directive rather than a list item.
    tokens = text.split()
    return len(tokens) <= 12 and _FINITE_OR_DIRECTIVE_RE.search(text) is None


def qualification_list_spans(fields: dict[str, Any]) -> list[str]:
    """Extract exact comma-separated qualification items from clearly introduced lists.

    This intentionally does not try to classify arbitrary prose. A sentence only becomes a
    candidate list when its first comma-delimited clause starts with an explicit qualification
    marker. Subsequent short non-finite clauses are treated as list continuations until prose
    resumes. Exact source text is preserved for evidence/provenance.
    """

    description = fields.get("description")
    if not isinstance(description, str) or "," not in description:
        return []

    result: list[str] = []
    for sentence_match in _SENTENCE_RE.finditer(description):
        sentence = sentence_match.group(0).strip()
        sentence_body = sentence.rstrip(".!?").strip()
        clauses = [part.strip() for part in sentence_body.split(",") if part.strip()]
        if len(clauses) < 2 or _QUALIFICATION_START_RE.search(clauses[0]) is None:
            continue
        for index, clause in enumerate(clauses):
            if index > 0 and not _looks_like_list_continuation(clause):
                break
            result.append(clause)
    return result


def validate_v11_candidate_structured(
    structured: dict[str, Any],
    analysis_fields: dict[str, Any],
) -> None:
    """Validate v10 boundaries plus exact item-level qualification-list coverage."""

    validate_v10_candidate_structured(structured, analysis_fields)
    requirements = structured.get("requirements") or []
    responsibilities = structured.get("responsibilities") or []

    requirements_by_evidence = {
        _normalize(str(item.get("evidence") or ""))
        for item in requirements
        if isinstance(item, dict)
    }
    spans = qualification_list_spans(analysis_fields)
    missing = [span for span in spans if _normalize(span) not in requirements_by_evidence]
    if missing:
        raise AnalysisValidationError(
            "P1.6 v11 omitted explicit qualification-list items: " + " | ".join(missing)
        )

    span_evidence = {_normalize(span) for span in spans}
    for index, item in enumerate(responsibilities):
        if not isinstance(item, dict):
            continue
        evidence = _normalize(str(item.get("evidence") or ""))
        if evidence in span_evidence:
            raise AnalysisValidationError(
                f"P1.6 v11 responsibility[{index}] uses qualification-list evidence as work"
            )


def _persisted_analysis_v11(
    structured: dict[str, Any],
    analysis_fields: dict[str, Any],
) -> dict[str, Any]:
    """Persist v10 accounting plus exact qualification-list coverage decisions."""

    analysis = _persisted_analysis_v10(structured, analysis_fields)
    coverage = analysis.setdefault("coverage", [])
    requirements = analysis.get("requirements") or []
    requirement_evidence = {
        _normalize(str(item.get("evidence") or ""))
        for item in requirements
        if isinstance(item, dict)
    }
    covered = {
        _normalize(str(item.get("evidence") or ""))
        for item in coverage
        if isinstance(item, dict)
    }
    for span in qualification_list_spans(analysis_fields):
        normalized = _normalize(span)
        if normalized not in requirement_evidence:
            raise AnalysisValidationError(
                f"Qualification-list item disappeared before v11 persistence: {span!r}"
            )
        if normalized in covered:
            continue
        coverage.append(
            {
                "evidence": span,
                "disposition": "extracted_requirement",
                "rationale": "P1.6 v11 deterministic qualification-list coverage.",
            }
        )
        covered.add(normalized)
    return analysis


class JobAnalysisServiceV11(JobAnalysisService):
    """Persist an isolated English P1.6 v11 candidate without promoting v9 globally."""

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
            spans = qualification_list_spans(analysis_fields)
            result = self._provider.complete_structured(
                system_prompt=_ENGLISH_SYSTEM_PROMPT_V11,
                user_payload={
                    "source_job_id": source.source_job_id,
                    "analysis_mode": "english",
                    "analysis_fields": analysis_fields,
                    "candidate_required_qualification_spans": spans,
                },
                schema_name="jobhunter_job_analysis_english_v11",
                schema=_ANALYSIS_SCHEMA,
                model=self._model,
                max_tokens=self._max_tokens,
            )
            validate_v11_candidate_structured(result.structured, analysis_fields)
            analysis = _persisted_analysis_v11(result.structured, analysis_fields)
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
                raise RuntimeError("P1.6 v11 artifact disappeared after persistence")
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
    "JobAnalysisServiceV11",
    "PROMPT_VERSION",
    "qualification_list_spans",
    "validate_v11_candidate_structured",
]
