"""Versioned persisted P1.6 v21 scoped-evidence service."""

from __future__ import annotations

from datetime import datetime

from jobhunter.analysis_failure_diagnostics import (
    AnalysisFailureDiagnosticStore,
    SafeFailure,
    describe_failure,
)
from jobhunter.analysis_service_v20 import (
    _ENGLISH_SYSTEM_PROMPT_V20,
    ANALYSIS_SCHEMA_VERSION,
    JobAnalysisServiceV20,
)
from jobhunter.inference.base import InferenceConnectionError, InferenceResponseError
from jobhunter.translation_store import TranslationSourceVersion

ENGLISH_PROMPT_VERSION = "job-analysis-english-v21"

_V21_RULES = """

P1.6 V21 CANDIDATE — EXACT ITEM SCOPE WITH PARENT COVERAGE:
- Every requirement must keep evidence equal to its supplied parent requirement_coverage text.
- Every requirement must also provide item_excerpt as one exact contiguous subspan of that parent
  containing the source wording for this concept. Do not paraphrase, join, or reconstruct it.
- Decide depth_signal only from item_excerpt. Supply the exact applicable marker when the item has
  one. Use null when this exact item has no accepted depth marker, even if neighboring items in the
  parent have markers. Never borrow neighboring depth.
- Keep depth wording out of concept. If the exact item starts with one source marker, JobHunter may
  materialize that one marker into depth_signal even when the generated concept uses wording such
  as "Working with X". If the concept itself starts with the same generated wrapper, JobHunter may
  also remove that wrapper and retain X as the concept.
- When one leading marker scopes a coordinated list (for example "familiarity with RAG, Embedding,
  and Vector Databases"), item_excerpt must retain that exact complete scoped phrase for every
  separately emitted concept. Do not reconstruct "familiarity with Embedding" or cite bare
  "Embedding" while claiming familiarity. The same exact group excerpt may support multiple
  concepts when the employer grammar applies the shared marker to all of them.
- Preserve obligation from the parent coverage hint. A preferred parent can supply shared
  optionality wording that is outside a narrower item_excerpt; keep that item preferred.
- item_excerpt is candidate validation evidence. JobHunter removes it before unchanged v5
  persistence; parent evidence and exact depth_signal remain the durable factual representation.
- Explicit headingless candidate-experience references may be supplied in their own partition so
  dense section decomposition and duty output cannot crowd them out. Every such supplied reference
  is a mandatory candidate qualification and must be represented; it cannot be excluded.
- When exact_item_coverage is supplied, represent every listed exact item_excerpt separately.
  Use that exact excerpt rather than the whole parent or a narrower neighboring phrase. Preserve a
  supplied required_concept_type, including experience and knowledge facts.
- Keep requirement evidence equal to exact_item_coverage.parent_reference's full supplied
  parent text. If evidence is instead the same exact unique checklist text as item_excerpt,
  JobHunter may restore its one source-proven parent; ambiguous or unknown items remain invalid.
- concept_type=experience requires prior applied exposure in the exact item_excerpt or an exact
  checklist item explicitly typed as experience. Do not turn a required capability into history.
- Keep all inherited v20 coverage, source, subject, strength, ontology, and fail-closed rules.
"""

_ENGLISH_SYSTEM_PROMPT_V21 = _ENGLISH_SYSTEM_PROMPT_V20 + _V21_RULES

__all__ = [
    "ANALYSIS_SCHEMA_VERSION",
    "JobAnalysisServiceV21",
    "ENGLISH_PROMPT_VERSION",
    "_ENGLISH_SYSTEM_PROMPT_V21",
    "_V21_RULES",
]


class JobAnalysisServiceV21(JobAnalysisServiceV20):
    """Persist scoped-evidence generation with its own identity and pending review."""

    prompt_version = ENGLISH_PROMPT_VERSION
    system_prompt = _ENGLISH_SYSTEM_PROMPT_V21
    schema_name = "jobhunter_job_analysis_english_v21"

    def __init__(
        self,
        *args,
        diagnostic_store: AnalysisFailureDiagnosticStore | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._diagnostic_store = diagnostic_store

    def _record_failed_attempt(
        self,
        *,
        source: TranslationSourceVersion,
        attempted_at: datetime,
        error: Exception,
    ) -> None:
        # Existing attempt history remains canonical. Never persist str(error):
        # Instructor may render full completions in its exception text.
        attempt_id = self._analysis_store.record_attempt(
            job_detail_version_id=source.job_detail_version_id,
            attempted_at=attempted_at,
            model=self._model,
            prompt_version=self.prompt_version,
            schema_version=ANALYSIS_SCHEMA_VERSION,
            outcome="failed",
            error=SafeFailure(describe_failure(error)),
        )
        if self._diagnostic_store is not None:
            try:
                self._diagnostic_store.record_failure(attempt_id=attempt_id, error=error)
            except Exception:
                # Private diagnostic capture is best-effort; it must not mask the
                # original failure or turn an unsuccessful attempt into an artifact.
                pass

    def analyze_english_job(self, source_job_id: str):
        try:
            return super().analyze_english_job(source_job_id)
        except InferenceConnectionError as exc:
            raise InferenceConnectionError(describe_failure(exc).message) from None
        except InferenceResponseError as exc:
            raise InferenceResponseError(describe_failure(exc).message) from None
