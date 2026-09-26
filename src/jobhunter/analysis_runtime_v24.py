"""Isolated v24 P1.6 runtime for exact qualification-item ownership."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from jobhunter.analysis_runtime_v23 import V23CandidateAnalysisProvider
from jobhunter.analysis_service_v24 import JobAnalysisServiceV24
from jobhunter.config import Settings
from jobhunter.evidence_refs_v23 import build_requirement_coverage_plan_v23
from jobhunter.inference.instructor_lm_studio_v24 import (
    complete_analysis_partition_with_instructor_v24,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult


def _source_words(text: str) -> Counter[str]:
    return Counter(re.findall(r"[^\W_]+", text.casefold()))


def _exact_qualification_item_plan(
    plan: dict[str, dict[str, Any]], model_fields: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    """Remove a redundant broad sentence only when exact item spans own every word.

    Older derived qualification items remain mandatory in the complete plan.
    This resolves duplicate evidence ownership before model partitioning; it does
    not create a fact, alter an obligation, or relax item validation.
    """

    values = model_fields.get("__candidate_qualification_evidence")
    if not isinstance(values, list):
        return plan
    result = dict(plan)
    for reference, parent in plan.items():
        if parent.get("source_kind") != "requirement_section":
            continue
        if not parent.get("allow_exclusion"):
            continue
        if parent.get("obligation_hint") not in (None, "required"):
            continue
        parent_text = str(parent.get("text") or "")
        children = [
            value
            for value in values
            if isinstance(value, str)
            and value.strip()
            and value.casefold() in parent_text.casefold()
        ]
        if not children:
            continue
        child_words = sum((_source_words(value) for value in children), Counter())
        if child_words and child_words == _source_words(parent_text):
            result.pop(reference)
    return result


class V24CandidateAnalysisProvider(V23CandidateAnalysisProvider):
    """Keep v23 semantic guards while giving exact items sole coverage ownership."""

    def _requirement_coverage_plan(
        self, model_fields: dict[str, Any]
    ) -> dict[str, dict[str, Any]]:
        return _exact_qualification_item_plan(
            build_requirement_coverage_plan_v23(model_fields), model_fields
        )

    def _complete_partition(self, **kwargs: Any) -> StructuredInferenceResult:
        return complete_analysis_partition_with_instructor_v24(**kwargs)


def build_v24_analysis_service(settings: Settings) -> JobAnalysisServiceV24:
    """Build candidate service; callers must use an isolated database copy."""
    from jobhunter.analysis_failure_diagnostics import AnalysisFailureDiagnosticStore
    from jobhunter.analysis_runtime import _translation_service
    from jobhunter.analysis_store import AnalysisStore
    from jobhunter.translation_store import TranslationStore

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV24(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        diagnostic_store=AnalysisFailureDiagnosticStore(settings.database_path),
        provider=V24CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )


__all__ = [
    "V24CandidateAnalysisProvider",
    "_exact_qualification_item_plan",
    "build_v24_analysis_service",
]
