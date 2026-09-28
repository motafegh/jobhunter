"""Isolated v25 provider: keep source siblings within one bounded model call."""

from __future__ import annotations

import re
from typing import Any

from jobhunter.analysis_runtime_v23 import _filter_unassigned_partition_claims
from jobhunter.analysis_runtime_v24 import V24CandidateAnalysisProvider
from jobhunter.analysis_service_v25 import JobAnalysisServiceV25
from jobhunter.config import Settings
from jobhunter.inference.instructor_lm_studio_v24 import (
    complete_analysis_partition_with_instructor_v24,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult

_SENTENCE_REF_RE = re.compile(r"^(.*):sentence:\d+$")
_PARTITION_SIZE = 8


def _v25_requirement_partitions(
    plan: dict[str, dict[str, Any]],
    *,
    partition_size: int = _PARTITION_SIZE,
) -> list[dict[str, dict[str, Any]]]:
    """Pack adjacent source sentences atomically without mixing semantic buckets."""

    if partition_size < 1:
        raise ValueError("partition_size must be positive")
    buckets: dict[tuple[str, str], list[list[str]]] = {}
    for reference, candidate in plan.items():
        source_kind = str(candidate.get("source_kind") or "")
        if source_kind in {"candidate_experience", "candidate_proof"}:
            kind = source_kind
        elif candidate.get("obligation_hint") == "preferred":
            kind = "preferred"
        else:
            kind = "standard"
        core = (
            not bool(candidate.get("allow_exclusion", False))
            or candidate.get("obligation_hint") in {"required", "preferred"}
            or source_kind == "structured_skill"
        )
        key = (kind, "core" if core else "contextual")
        groups = buckets.setdefault(key, [])
        match = _SENTENCE_REF_RE.match(reference)
        if match and groups and _SENTENCE_REF_RE.match(groups[-1][-1]):
            last_parent = _SENTENCE_REF_RE.match(groups[-1][-1]).group(1)
            if last_parent == match.group(1):
                groups[-1].append(reference)
                continue
        groups.append([reference])

    partitions: list[dict[str, dict[str, Any]]] = []
    for kind in ("standard", "preferred", "candidate_experience", "candidate_proof"):
        for tier in ("core", "contextual"):
            current: list[str] = []
            for group in buckets.get((kind, tier), []):
                if len(group) > partition_size:
                    if current:
                        partitions.append({ref: dict(plan[ref]) for ref in current})
                        current = []
                    for offset in range(0, len(group), partition_size):
                        chunk = group[offset : offset + partition_size]
                        partitions.append({ref: dict(plan[ref]) for ref in chunk})
                    continue
                if current and len(current) + len(group) > partition_size:
                    partitions.append({ref: dict(plan[ref]) for ref in current})
                    current = []
                current.extend(group)
            if current:
                partitions.append({ref: dict(plan[ref]) for ref in current})
    return partitions


class V25CandidateAnalysisProvider(V24CandidateAnalysisProvider):
    def _requirement_partitions(
        self, plan: dict[str, dict[str, Any]]
    ) -> list[dict[str, dict[str, Any]]]:
        return _v25_requirement_partitions(plan)

    def _complete_partition(self, **kwargs: Any) -> StructuredInferenceResult:
        scoped_refs = list(kwargs["requirement_coverage_plan"])
        scoped_refs.extend(kwargs["responsibility_coverage_plan"])
        result = complete_analysis_partition_with_instructor_v24(
            **kwargs,
            contract_version="v25",
            model_evidence_references=scoped_refs,
        )
        return _filter_unassigned_partition_claims(
            result,
            requirement_plan=kwargs["requirement_coverage_plan"],
            responsibility_plan=kwargs["responsibility_coverage_plan"],
        )


def build_v25_analysis_service(settings: Settings) -> JobAnalysisServiceV25:
    """Build candidate service; callers must use an isolated database copy."""
    from jobhunter.analysis_failure_diagnostics import AnalysisFailureDiagnosticStore
    from jobhunter.analysis_runtime import _translation_service
    from jobhunter.analysis_store import AnalysisStore
    from jobhunter.translation_store import TranslationStore

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV25(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        diagnostic_store=AnalysisFailureDiagnosticStore(settings.database_path),
        provider=V25CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )


__all__ = ["V25CandidateAnalysisProvider", "build_v25_analysis_service"]
