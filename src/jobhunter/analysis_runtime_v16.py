"""Runtime adapter for isolated English P1.6 v16 candidate."""
from __future__ import annotations

import re
from dataclasses import replace
from typing import Any

from jobhunter.analysis_runtime import _translation_service
from jobhunter.analysis_runtime_v15 import V15CandidateAnalysisProvider
from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v16 import JobAnalysisServiceV16, validate_v16_candidate_structured
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.p16_v15_runtime_guard import v15_ability_wrapper_guard
from jobhunter.translation_store import TranslationStore

_EMPTY_GROUP_RE = re.compile(r"(?:\(\s*\)|\[\s*\]|\{\s*\})")


def _clean_v16_concepts(structured: dict[str, Any]) -> tuple[dict[str, Any], list[int]]:
    requirements = structured.get("requirements")
    if not isinstance(requirements, list):
        return structured, []
    changed: list[int] = []
    normalized = []
    for index, item in enumerate(requirements):
        if not isinstance(item, dict):
            normalized.append(item)
            continue
        concept = str(item.get("concept") or "").strip()
        candidate = " ".join(_EMPTY_GROUP_RE.sub(" ", concept).strip(" ,;:-/").split())
        if candidate and candidate != concept:
            item = dict(item)
            item["concept"] = candidate
            changed.append(index)
        normalized.append(item)
    if not changed:
        return structured, []
    result = dict(structured)
    result["requirements"] = normalized
    return result, changed


class V16CandidateAnalysisProvider(V15CandidateAnalysisProvider):
    def _attempt(self, kwargs: dict[str, Any], system_prompt: str):
        attempt_kwargs = dict(kwargs)
        attempt_kwargs["system_prompt"] = system_prompt
        with v15_ability_wrapper_guard():
            result = super().complete_structured(**attempt_kwargs)
        structured, changed = _clean_v16_concepts(result.structured)
        fields = (kwargs.get("user_payload") or {}).get("analysis_fields")
        if not isinstance(fields, dict):
            raise AnalysisValidationError("P1.6 v16 runtime is missing analysis_fields")
        validate_v16_candidate_structured(structured, fields)
        body = dict(result.request_body)
        runtime = dict(body.get("runtime") or {})
        runtime["p16_v16_clean_concept_normalization"] = changed
        runtime["p16_v16_experience_evidence_guard"] = True
        body["runtime"] = runtime
        return replace(result, structured=structured, request_body=body)

    def complete_structured(self, **kwargs: Any):
        prompt = str(kwargs.get("system_prompt") or "")
        try:
            return self._attempt(kwargs, prompt)
        except AnalysisValidationError as first_error:
            correction = (
                prompt
                + "\n\nP1.6 V16 BOUNDED CORRECTION:\n"
                + str(first_error)
                + "\nCorrect only that concept normalization/type boundary; preserve all evidence, "
                "coverage, strength, depth, and responsibility decisions."
            )
            result = self._attempt(kwargs, correction)
            body = dict(result.request_body)
            runtime = dict(body.get("runtime") or {})
            runtime["p16_v16_candidate_recovery"] = True
            runtime["p16_v16_first_error"] = str(first_error)
            body["runtime"] = runtime
            return replace(result, request_body=body)


def build_v16_candidate_analysis_service(settings: Settings) -> JobAnalysisServiceV16:
    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV16(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        provider=V16CandidateAnalysisProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            max_retries=settings.inference_max_retries,
        ),
        model=model,
        max_tokens=settings.analysis_max_tokens,
    )
