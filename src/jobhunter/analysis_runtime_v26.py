"""Isolated v26 provider for source-exact mixed preference and context."""

from __future__ import annotations

import re
from typing import Any

from jobhunter.analysis_runtime_v25 import V25CandidateAnalysisProvider
from jobhunter.analysis_service_v26 import JobAnalysisServiceV26
from jobhunter.config import Settings
from jobhunter.evidence_refs_v21 import _sentences
from jobhunter.evidence_refs_v26 import split_mixed_preference_clauses

_NEGATIVE_SUITABILITY_RE = re.compile(r"\bnot\s+suitable\b", re.I)
_COMPENSATION_HEADING_RE = re.compile(
    r"^(?:salary(?:\s+and\s+benefits)?|compensation|benefits)\s*:", re.I
)


class V26CandidateAnalysisProvider(V25CandidateAnalysisProvider):
    def _requirement_coverage_plan(
        self, model_fields: dict[str, Any]
    ) -> dict[str, dict[str, Any]]:
        return split_mixed_preference_clauses(
            super()._requirement_coverage_plan(model_fields)
        )

    def _source_quoted_requirements(
        self, plan: dict[str, dict[str, Any]]
    ) -> tuple[list[str], list[dict[str, Any]]]:
        refs, claims = super()._source_quoted_requirements(plan)
        for reference, candidate in plan.items():
            if reference in refs or not reference.endswith(
                (":required_clause", ":preferred_clause")
            ):
                continue
            evidence = str(candidate.get("text") or "")
            refs.append(reference)
            claims.append(
                {
                    "concept": evidence,
                    "depth_signal": None,
                    "requirement_type": candidate["obligation_hint"],
                    "concept_type": "education" if re.search(
                        r"\b(?:degree|graduate|university)\b", evidence, re.I
                    ) else "other",
                    "evidence": evidence,
                    "confidence": "high",
                    "rationale": (
                        "Exact employer qualification clause preserves its own "
                        "obligation and alternatives."
                    ),
                }
            )
        return refs, claims

    def _source_context_exclusions(
        self, plan: dict[str, dict[str, Any]]
    ) -> tuple[list[str], list[dict[str, str]]]:
        refs: list[str] = []
        exclusions: list[dict[str, str]] = []
        for reference, candidate in plan.items():
            text = str(candidate.get("text") or "")
            if (
                candidate.get("source_kind") == "requirement_section"
                and _NEGATIVE_SUITABILITY_RE.search(text)
                and len(_sentences(text)) == 1
                and not re.search(r"\b(?:we\s+are\s+looking|must\s+have)\b", text, re.I)
            ):
                reason = (
                    "Source states an insufficiency/exclusion, not an independent "
                    "positive qualification."
                )
            elif (
                candidate.get("source_kind") == "candidate_residual_sentence"
                and _COMPENSATION_HEADING_RE.match(text)
            ):
                reason = "Source states compensation context, not candidate eligibility."
            else:
                continue
            refs.append(reference)
            exclusions.append({"evidence_reference": reference, "rationale": reason})
        return refs, exclusions


def build_v26_analysis_service(settings: Settings) -> JobAnalysisServiceV26:
    """Build isolated candidate service over a private SQLite copy."""
    from jobhunter.analysis_failure_diagnostics import AnalysisFailureDiagnosticStore
    from jobhunter.analysis_runtime import _translation_service
    from jobhunter.analysis_store import AnalysisStore
    from jobhunter.translation_store import TranslationStore

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV26(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        diagnostic_store=AnalysisFailureDiagnosticStore(settings.database_path),
        provider=V26CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )


__all__ = ["V26CandidateAnalysisProvider", "build_v26_analysis_service"]
