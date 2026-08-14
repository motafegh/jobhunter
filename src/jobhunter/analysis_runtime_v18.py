"""Runtime wiring for P1.6 v18 deterministic structured-requirement ownership."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from jobhunter.analysis_runtime import _translation_service
from jobhunter.analysis_runtime_v14 import _ANALYSIS_CONTEXT_LENGTH
from jobhunter.analysis_runtime_v15 import _normalize_v15_schedule_concepts
from jobhunter.analysis_runtime_v17 import (
    V17CandidateAnalysisProvider,
    _complete_with_v17_response_model,
)
from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v13 import inject_decomposition_exclusions
from jobhunter.analysis_service_v15 import validate_v15_candidate_structured
from jobhunter.analysis_service_v18 import JobAnalysisServiceV18
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.evidence_refs import build_requirement_coverage_plan
from jobhunter.inference.instructor_lm_studio import _DEPTH_SIGNAL_PATTERNS
from jobhunter.inference.lm_studio import StructuredInferenceResult
from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context
from jobhunter.translation_store import TranslationStore


def _normalize(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def _v18_structured_partition(
    original_fields: dict[str, Any],
    effective_fields: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[str]]:
    """Move only mechanically representable structured facts out of model ownership.

    Education is already a credential-valued structured field. Minimum experience becomes
    deterministic only when the shared P1.6 years pattern can recover an exact extent phrase.
    Unrecognized experience wording remains model-visible and therefore still fails closed rather
    than being guessed by code.
    """

    model_fields = dict(effective_fields)
    deterministic: list[dict[str, Any]] = []
    owned_references: list[str] = []
    coverage_plan = build_requirement_coverage_plan(original_fields)

    experience = coverage_plan.get("field:minimum_experience")
    if experience is not None:
        evidence = str(experience.get("text") or "").strip()
        match = _DEPTH_SIGNAL_PATTERNS["years"].search(evidence)
        if evidence and match is not None:
            deterministic.append(
                {
                    "concept": "Professional experience",
                    "depth_signal": evidence[match.start() : match.end()],
                    "requirement_type": "required",
                    "concept_type": "experience",
                    "evidence": evidence,
                    "confidence": "high",
                    "rationale": (
                        "JobHunter deterministically materialized the structured minimum-"
                        "experience field."
                    ),
                }
            )
            model_fields.pop("minimum_experience", None)
            owned_references.append("field:minimum_experience")

    education = coverage_plan.get("field:education")
    if education is not None:
        evidence = str(education.get("text") or "").strip()
        if evidence:
            deterministic.append(
                {
                    "concept": evidence,
                    "depth_signal": None,
                    "requirement_type": "required",
                    "concept_type": "education",
                    "evidence": evidence,
                    "confidence": "high",
                    "rationale": (
                        "JobHunter deterministically materialized the structured education field."
                    ),
                }
            )
            model_fields.pop("education", None)
            owned_references.append("field:education")

    return model_fields, deterministic, owned_references


def _v18_structured_skill_coverage_plan(
    model_fields: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Give every model-visible structured skill a non-excludable exact coverage reference."""

    skills = model_fields.get("skills")
    if not isinstance(skills, list):
        return {}
    plan: dict[str, dict[str, Any]] = {}
    for index, value in enumerate(skills):
        if not isinstance(value, str) or not value.strip():
            continue
        text = value.strip()
        plan[f"field:skills:{index}"] = {
            "text": text,
            "source_kind": "structured_skill",
            "obligation_hint": "required",
            "allow_exclusion": False,
        }
    return plan


def _materialize_v18_deterministic_requirements(
    structured: dict[str, Any],
    deterministic: list[dict[str, Any]],
) -> dict[str, Any]:
    """Append deterministic structured requirements without duplicating an identical record."""

    existing = structured.get("requirements")
    if not isinstance(existing, list):
        raise AnalysisValidationError("P1.6 v18 model requirements array is malformed")
    requirements = [dict(item) if isinstance(item, dict) else item for item in existing]
    keys = {
        (
            _normalize(str(item.get("concept") or "")),
            str(item.get("requirement_type") or ""),
            _normalize(str(item.get("evidence") or "")),
        )
        for item in requirements
        if isinstance(item, dict)
    }
    for item in deterministic:
        key = (
            _normalize(str(item.get("concept") or "")),
            str(item.get("requirement_type") or ""),
            _normalize(str(item.get("evidence") or "")),
        )
        if key in keys:
            continue
        requirements.append(dict(item))
        keys.add(key)
    result = dict(structured)
    result["requirements"] = requirements
    return result


class V18CandidateAnalysisProvider(V17CandidateAnalysisProvider):
    """Keep semantic interpretation model-owned while moving obvious source facts to code."""

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

        model_fields, deterministic, deterministic_refs = _v18_structured_partition(
            original_fields,
            effective_fields,
        )
        skill_plan = _v18_structured_skill_coverage_plan(model_fields)
        merged_plan = {reference: dict(candidate) for reference, candidate in additional_plan.items()}
        for reference, candidate in skill_plan.items():
            if reference in merged_plan:
                raise AnalysisValidationError(
                    f"P1.6 v18 structured-skill coverage collides with candidate plan: {reference}"
                )
            merged_plan[reference] = dict(candidate)

        payload = dict(kwargs.get("user_payload") or {})
        payload["analysis_fields"] = model_fields
        payload["candidate_required_qualification_references"] = qualification_refs
        payload["candidate_residual_requirement_references"] = residual_refs
        payload["candidate_deterministic_requirement_references"] = deterministic_refs

        result = _complete_with_v17_response_model(
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
            additional_requirement_coverage_plan=merged_plan,
            validation_retries=1,
        )

        structured = _materialize_v18_deterministic_requirements(
            result.structured,
            deterministic,
        )
        structured, normalized_indexes = _normalize_v15_schedule_concepts(structured)
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
                "p16_v18_deterministic_structured_requirements": deterministic_refs,
                "p16_v18_structured_skill_coverage": sorted(skill_plan),
                "p16_v18_model_owned_structured_fields": sorted(
                    key
                    for key in ("minimum_experience", "education")
                    if key in model_fields
                ),
                "p16_v15_schedule_depth_normalization": True,
                "p16_v15_schedule_concept_normalization": normalized_indexes,
            }
        )
        request_body["runtime"] = runtime_payload
        return replace(result, structured=structured, request_body=request_body)


def build_v18_candidate_analysis_service(settings: Settings) -> JobAnalysisServiceV18:
    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV18(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        provider=V18CandidateAnalysisProvider(
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
    "V18CandidateAnalysisProvider",
    "_materialize_v18_deterministic_requirements",
    "_v18_structured_partition",
    "_v18_structured_skill_coverage_plan",
    "build_v18_candidate_analysis_service",
]
