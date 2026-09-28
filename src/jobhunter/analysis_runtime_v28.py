"""Isolated v28 provider for dense residuals and source-exact trait lists."""

from __future__ import annotations

import re
from typing import Any

from jobhunter.analysis_runtime_v27 import V27CandidateAnalysisProvider
from jobhunter.analysis_service_v28 import JobAnalysisServiceV28
from jobhunter.config import Settings
from jobhunter.evidence_refs_v28 import require_dense_residual_items

_TRAIT_CUE_RE = re.compile(
    r"\b(?:motivated|committed|creative|teamwork\s+spirit|"
    r"desire\s+to\s+learn|product\s+sense|problem[- ]solver)\b",
    re.I,
)


class V28CandidateAnalysisProvider(V27CandidateAnalysisProvider):
    def _prepare_inherited_additional_plan(
        self, plan: dict[str, dict[str, Any]]
    ) -> dict[str, dict[str, Any]]:
        return require_dense_residual_items(plan)

    def _source_quoted_requirements(
        self, plan: dict[str, dict[str, Any]]
    ) -> tuple[list[str], list[dict[str, Any]]]:
        refs, claims = super()._source_quoted_requirements(plan)
        for reference, candidate in plan.items():
            text = str(candidate.get("text") or "")
            if (
                reference in refs
                or candidate.get("source_kind") != "requirement_section"
                or candidate.get("obligation_hint") != "required"
                or candidate.get("required_item_excerpts")
                or len(text) > 125
                or text.count(",") < 2
                or not _TRAIT_CUE_RE.search(text)
            ):
                continue
            refs.append(reference)
            claims.append(
                {
                    "concept": text,
                    "depth_signal": None,
                    "requirement_type": "required",
                    "concept_type": "other",
                    "evidence": text,
                    "confidence": "high",
                    "rationale": (
                        "Exact employer candidate-trait list, without technical inference."
                    ),
                }
            )
        return refs, claims


def build_v28_analysis_service(settings: Settings) -> JobAnalysisServiceV28:
    """Build isolated candidate service over a private SQLite copy."""
    from jobhunter.analysis_failure_diagnostics import AnalysisFailureDiagnosticStore
    from jobhunter.analysis_runtime import _translation_service
    from jobhunter.analysis_store import AnalysisStore
    from jobhunter.translation_store import TranslationStore

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV28(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        diagnostic_store=AnalysisFailureDiagnosticStore(settings.database_path),
        provider=V28CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )


__all__ = ["V28CandidateAnalysisProvider", "build_v28_analysis_service"]
