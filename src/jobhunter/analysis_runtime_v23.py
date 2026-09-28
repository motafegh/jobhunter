"""Current P1.6 v23 provider and service wiring."""

from __future__ import annotations

import re
from typing import Any

from jobhunter.analysis_runtime_v20 import _normalize, _v20_requirement_partitions
from jobhunter.analysis_runtime_v21 import V21CandidateAnalysisProvider
from jobhunter.analysis_service_v23 import JobAnalysisServiceV23
from jobhunter.config import Settings
from jobhunter.evidence_refs_v21 import _sentences, has_candidate_optionality_signal
from jobhunter.evidence_refs_v23 import build_requirement_coverage_plan_v23
from jobhunter.inference.instructor_lm_studio_v23 import (
    complete_analysis_partition_with_instructor_v23,
    persisted_v20_shape,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult


class V23CandidateAnalysisProvider(V21CandidateAnalysisProvider):
    """Keep proof preferences in their own bounded model partition."""

    def _run_once(self, **kwargs: Any) -> StructuredInferenceResult:
        kwargs = dict(kwargs)
        base_plan = self._requirement_coverage_plan(kwargs["effective_fields"])
        kwargs["additional_plan"] = _scoped_preferred_qualification_plan(
            kwargs["original_fields"],
            _remove_duplicate_residual_ownership(kwargs["additional_plan"], base_plan),
        )
        return super()._run_once(**kwargs)

    def _requirement_coverage_plan(
        self, model_fields: dict[str, Any]
    ) -> dict[str, dict[str, Any]]:
        return build_requirement_coverage_plan_v23(model_fields)

    def _requirement_partitions(
        self, plan: dict[str, dict[str, Any]]
    ) -> list[dict[str, dict[str, Any]]]:
        partitions: list[dict[str, dict[str, Any]]] = []
        for source_kind in (
            "standard", "preferred", "candidate_experience", "candidate_proof"
        ):
            subset = {
                ref: candidate
                for ref, candidate in plan.items()
                if (
                    (source_kind == "standard" and candidate.get("source_kind") not in
                     {"candidate_experience", "candidate_proof"}
                     and candidate.get("obligation_hint") != "preferred")
                    or (source_kind == "preferred"
                        and candidate.get("source_kind") not in
                        {"candidate_experience", "candidate_proof"}
                        and candidate.get("obligation_hint") == "preferred")
                    or candidate.get("source_kind") == source_kind
                )
            }
            if subset:
                partitions.extend(_v20_requirement_partitions(subset))
        return partitions

    def _complete_partition(self, **kwargs: Any) -> StructuredInferenceResult:
        result = complete_analysis_partition_with_instructor_v23(**kwargs)
        allowed = {
            _normalize(text)
            for text in kwargs["responsibility_coverage_plan"].values()
        }
        structured = dict(result.structured)
        dropped = 0
        for field in ("role_purpose", "responsibilities"):
            claims = list(structured[field])
            structured[field] = [
                claim for claim in claims
                if _normalize(str(claim["evidence"])) in allowed
            ]
            dropped += len(claims) - len(structured[field])
        if not dropped:
            return result

        request_body = dict(result.request_body)
        runtime = dict(request_body.get("runtime") or {})
        runtime["p16_v23_dropped_unassigned_work_claims"] = dropped
        request_body["runtime"] = runtime
        return StructuredInferenceResult(
            model=result.model,
            structured=structured,
            request_body=request_body,
            raw_response=result.raw_response,
            finish_reason=result.finish_reason,
        )

    def _persistable_structured(self, structured: dict[str, Any]) -> dict[str, Any]:
        return dict(persisted_v20_shape(structured))


_PREFERRED_SENTENCE_END_RE = re.compile(
    r"\b(?:is|are)\s+(?:considered\s+)?(?:an?\s+)?"
    r"(?:(?:important|valuable|strong)\s+)?(?:asset|advantage|plus)\s*[.!?]?$",
    re.I,
)
_REQUIRED_CUE_RE = re.compile(r"\b(?:essential|required|must|mandatory|necessary)\b", re.I)


def _scoped_preferred_qualification_plan(
    fields: dict[str, Any], plan: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    """Carry an unambiguous sentence-level preference to its exact list items."""

    description = fields.get("description")
    if not isinstance(description, str):
        return plan
    sentences = [
        sentence for sentence in _sentences(description)
        if _PREFERRED_SENTENCE_END_RE.search(sentence)
        and has_candidate_optionality_signal(sentence)
        and not _REQUIRED_CUE_RE.search(sentence)
    ]
    result = {reference: dict(candidate) for reference, candidate in plan.items()}
    for candidate in result.values():
        if candidate.get("source_kind") != "candidate_qualification_item":
            continue
        item = str(candidate.get("text") or "")
        parents = [sentence for sentence in sentences if item and item in sentence]
        if len(parents) != 1:
            continue
        candidate["obligation_hint"] = "preferred"
        candidate["obligation_context"] = parents[0]
    return result


def _remove_duplicate_residual_ownership(
    additional: dict[str, dict[str, Any]], base: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    """A source-exact requirement reference owns an identical residual sentence."""

    owned = {
        str(candidate.get("text") or "")
        for candidate in base.values()
        if candidate.get("source_kind") != "structured_skill"
        and candidate.get("obligation_hint") != "context_only"
        and str(candidate.get("text") or "")
    }
    return {
        reference: dict(candidate)
        for reference, candidate in additional.items()
        if not (
            candidate.get("source_kind") == "candidate_residual_sentence"
            and candidate.get("text") in owned
        )
    }


def build_v23_analysis_service(settings: Settings) -> JobAnalysisServiceV23:
    """Build the shared current English service with local failure diagnostics."""
    from jobhunter.analysis_failure_diagnostics import AnalysisFailureDiagnosticStore
    from jobhunter.analysis_runtime import _translation_service
    from jobhunter.analysis_store import AnalysisStore
    from jobhunter.translation_store import TranslationStore

    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV23(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        diagnostic_store=AnalysisFailureDiagnosticStore(settings.database_path),
        provider=V23CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )


__all__ = ["V23CandidateAnalysisProvider", "build_v23_analysis_service"]
