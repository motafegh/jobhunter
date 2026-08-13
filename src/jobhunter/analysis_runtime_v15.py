"""Runtime wiring for isolated English P1.6 v15 candidate."""

from __future__ import annotations

import re
from dataclasses import replace
from typing import Any

from jobhunter.analysis_runtime import _translation_service
from jobhunter.analysis_runtime_v14 import (
    _ANALYSIS_CONTEXT_LENGTH,
    V14CandidateAnalysisProvider,
    _complete_with_v14_response_model,
    _v14_candidate_evidence_view,
)
from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v13 import (
    decomposed_requirement_references,
    inject_decomposition_exclusions,
)
from jobhunter.analysis_service_v15 import (
    JobAnalysisServiceV15,
    validate_v15_candidate_structured,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.inference.lm_studio import StructuredInferenceResult
from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context
from jobhunter.translation_store import TranslationStore

_CAPABILITY_CONCEPT_TYPES = {"skill", "knowledge", "practice", "domain", "experience", "tool"}
_SCHEDULE_CONCEPT_RE = re.compile(
    r"\b(?:"
    r"full[ -]?time(?:\s*(?:and|or|/)\s*part[ -]?time)?|"
    r"part[ -]?time(?:\s*(?:and|or|/)\s*full[ -]?time)?"
    r")\b",
    re.I,
)
_GENERIC_SCHEDULE_REMAINDERS = {
    "availability",
    "employment",
    "job",
    "position",
    "role",
    "schedule",
    "work arrangement",
    "working arrangement",
    "working hours",
    "working time",
}


def _v15_candidate_evidence_view(
    analysis_fields: dict[str, Any],
) -> tuple[dict[str, Any], list[str], list[str], dict[str, dict[str, Any]]]:
    """Reuse v14 exact subcoverage but keep residual employer strength semantically neutral."""

    effective_fields, qualification_refs, residual_refs, plan = _v14_candidate_evidence_view(
        analysis_fields
    )
    neutral_plan = {reference: dict(candidate) for reference, candidate in plan.items()}
    for reference in residual_refs:
        neutral_plan[reference]["obligation_hint"] = None
    return effective_fields, qualification_refs, residual_refs, neutral_plan


def _normalize_v15_schedule_concepts(
    structured: dict[str, Any],
) -> tuple[dict[str, Any], list[int]]:
    """Strip work-schedule wording only when a meaningful capability concept remains.

    Exact evidence is never changed. Pure schedule/logistics concepts remain untouched so the
    strict v14/v15 validator still rejects them rather than manufacturing a capability.
    """

    requirements = structured.get("requirements")
    if not isinstance(requirements, list):
        return structured, []

    normalized_requirements: list[Any] = []
    changed_indexes: list[int] = []
    for index, item in enumerate(requirements):
        if not isinstance(item, dict):
            normalized_requirements.append(item)
            continue
        concept = str(item.get("concept") or "").strip()
        concept_type = str(item.get("concept_type") or "").strip()
        if (
            concept_type not in _CAPABILITY_CONCEPT_TYPES
            or not _SCHEDULE_CONCEPT_RE.search(concept)
        ):
            normalized_requirements.append(item)
            continue

        candidate = _SCHEDULE_CONCEPT_RE.sub(" ", concept)
        candidate = re.sub(r"(?:^|\s)(?:and|or)(?:\s|$)", " ", candidate, flags=re.I)
        candidate = " ".join(candidate.strip(" ,;:-/").split())
        if not candidate or candidate.casefold() in _GENERIC_SCHEDULE_REMAINDERS:
            normalized_requirements.append(item)
            continue

        normalized_item = dict(item)
        normalized_item["concept"] = candidate
        normalized_requirements.append(normalized_item)
        changed_indexes.append(index)

    if not changed_indexes:
        return structured, []
    normalized = dict(structured)
    normalized["requirements"] = normalized_requirements
    return normalized, changed_indexes


def _mark_v15_runtime(
    result: StructuredInferenceResult,
    *,
    qualification_refs: list[str],
    residual_refs: list[str],
    decomposed_refs: list[str],
) -> StructuredInferenceResult:
    request_body = dict(result.request_body)
    runtime = dict(request_body.get("runtime") or {})
    runtime.update(
        {
            "p16_v15_required_qualification_references": qualification_refs,
            "p16_v15_residual_requirement_references": residual_refs,
            "p16_v15_deterministic_decomposition_references": decomposed_refs,
            "p16_v15_residual_obligation_hints": "source_semantic",
            "p16_v15_concept_type_contract": True,
        }
    )
    request_body["runtime"] = runtime
    return replace(result, request_body=request_body)


class V15CandidateAnalysisProvider(V14CandidateAnalysisProvider):
    """Reuse v14 typed/depth boundary with v15 residual strength semantics."""

    def _run_once(
        self,
        *,
        kwargs: dict[str, Any],
        system_prompt: str,
        original_fields: dict[str, Any],
        effective_fields: dict[str, Any],
        qualification_refs: list[str],
        residual_refs: list[str],
        additional_plan: dict[str, dict[str, Any]],
        decomposed_refs: list[str],
    ) -> StructuredInferenceResult:
        selected_model = str(kwargs.get("model") or self._configured_model).strip()
        runtime = ensure_lm_studio_model_context(
            openai_base_url=self._base_url,
            model=selected_model,
            context_length=_ANALYSIS_CONTEXT_LENGTH,
            api_token=self._api_token,
            connect_timeout_seconds=min(self._timeout_seconds, 10.0),
            exclusive_llm=True,
        )
        payload = dict(kwargs.get("user_payload") or {})
        payload["analysis_fields"] = effective_fields
        payload["candidate_required_qualification_references"] = qualification_refs
        payload["candidate_residual_requirement_references"] = residual_refs

        result = _complete_with_v14_response_model(
            base_url=f"{self._base_url}/",
            api_token=self._api_token,
            timeout_seconds=self._timeout_seconds,
            network_retries=self._max_retries,
            selected_model=selected_model,
            system_prompt=system_prompt,
            user_payload=payload,
            schema=kwargs["schema"],
            max_tokens=int(kwargs.get("max_tokens") or 8192),
            seed=int(kwargs.get("seed") or 0),
            suppressed_requirement_coverage_references=decomposed_refs,
            additional_requirement_coverage_plan=additional_plan,
            validation_retries=1,
        )
        structured, normalized_indexes = _normalize_v15_schedule_concepts(result.structured)
        structured = inject_decomposition_exclusions(structured, original_fields)
        validate_v15_candidate_structured(structured, original_fields)

        request_body = dict(result.request_body)
        runtime_payload = dict(request_body.get("runtime") or {})
        runtime_payload.update(
            {
                "context_length_tokens": runtime.context_length,
                "context_action": runtime.action,
                "model_instance_id": runtime.instance_id,
                "exclusive_llm": True,
                "p16_v15_schedule_depth_normalization": True,
                "p16_v15_schedule_concept_normalization": normalized_indexes,
            }
        )
        request_body["runtime"] = runtime_payload
        return replace(result, structured=structured, request_body=request_body)

    def complete_structured(self, **kwargs: Any) -> StructuredInferenceResult:
        payload = kwargs.get("user_payload") or {}
        analysis_fields = payload.get("analysis_fields")
        if not isinstance(analysis_fields, dict):
            raise AnalysisValidationError("P1.6 v15 runtime is missing analysis_fields")

        effective_fields, qualification_refs, residual_refs, additional_plan = (
            _v15_candidate_evidence_view(analysis_fields)
        )
        decomposed_refs = decomposed_requirement_references(analysis_fields)
        try:
            result = self._run_once(
                kwargs=kwargs,
                system_prompt=str(kwargs.get("system_prompt") or ""),
                original_fields=analysis_fields,
                effective_fields=effective_fields,
                qualification_refs=qualification_refs,
                residual_refs=residual_refs,
                additional_plan=additional_plan,
                decomposed_refs=decomposed_refs,
            )
        except AnalysisValidationError as first_error:
            correction_prompt = (
                str(kwargs.get("system_prompt") or "")
                + "\n\nP1.6 V15 BOUNDED CORRECTION:\n"
                + str(first_error)
                + "\nCorrect only the violated boundary. Preserve exact evidence, mandatory "
                "qualification items, residual coverage decisions, structured required skills, "
                "source-supported requirement strength, and concept-type semantics."
            )
            result = self._run_once(
                kwargs=kwargs,
                system_prompt=correction_prompt,
                original_fields=analysis_fields,
                effective_fields=effective_fields,
                qualification_refs=qualification_refs,
                residual_refs=residual_refs,
                additional_plan=additional_plan,
                decomposed_refs=decomposed_refs,
            )
            request_body = dict(result.request_body)
            runtime = dict(request_body.get("runtime") or {})
            runtime["p16_v15_candidate_recovery"] = True
            runtime["p16_v15_first_error"] = str(first_error)
            request_body["runtime"] = runtime
            result = replace(result, request_body=request_body)

        return _mark_v15_runtime(
            result,
            qualification_refs=qualification_refs,
            residual_refs=residual_refs,
            decomposed_refs=decomposed_refs,
        )


def build_v15_candidate_analysis_service(settings: Settings) -> JobAnalysisServiceV15:
    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError(
            "No analysis model is configured. Set analysis_lm_studio_model, lm_studio_model, "
            "or an explicit translation_lm_studio_model fallback."
        )
    return JobAnalysisServiceV15(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        provider=V15CandidateAnalysisProvider(
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
    "V15CandidateAnalysisProvider",
    "_normalize_v15_schedule_concepts",
    "_v15_candidate_evidence_view",
    "build_v15_candidate_analysis_service",
]
