"""Runtime wiring for P1.6 v20 source-led coverage partitioning."""

from __future__ import annotations

from typing import Any

from jobhunter.analysis_runtime import _translation_service
from jobhunter.analysis_runtime_v14 import _ANALYSIS_CONTEXT_LENGTH
from jobhunter.analysis_runtime_v15 import _normalize_v15_schedule_concepts
from jobhunter.analysis_runtime_v18 import (
    _materialize_v18_deterministic_requirements,
    _v18_structured_partition,
    _v18_structured_skill_coverage_plan,
)
from jobhunter.analysis_runtime_v19 import V19CandidateAnalysisProvider
from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v13 import inject_decomposition_exclusions
from jobhunter.analysis_service_v15 import validate_v15_candidate_structured
from jobhunter.analysis_service_v20 import JobAnalysisServiceV20
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.evidence_refs import (
    build_requirement_coverage_plan,
    build_responsibility_coverage_plan,
)
from jobhunter.inference.instructor_lm_studio_v20 import (
    complete_analysis_partition_with_instructor_v20,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult
from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context
from jobhunter.translation_store import TranslationStore

_PARTITION_SIZE = 8


def _normalize(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def _v20_complete_requirement_plan(
    model_fields: dict[str, Any],
    *,
    additional_plan: dict[str, dict[str, Any]],
    skill_plan: dict[str, dict[str, Any]],
    decomposed_refs: list[str],
) -> dict[str, dict[str, Any]]:
    """Build the exact model-owned coverage ledger before partitioning it."""

    plan = {
        reference: dict(candidate)
        for reference, candidate in build_requirement_coverage_plan(model_fields).items()
    }
    for reference in decomposed_refs:
        candidate = plan.get(reference)
        if candidate is None:
            continue
        if not bool(candidate.get("allow_exclusion", False)):
            raise AnalysisValidationError(
                f"P1.6 v20 cannot suppress non-excludable decomposed coverage: {reference}"
            )
        del plan[reference]

    for source_plan, label in ((additional_plan, "candidate"), (skill_plan, "skill")):
        for reference, candidate in source_plan.items():
            if reference in plan:
                raise AnalysisValidationError(
                    f"P1.6 v20 {label} coverage collides with existing plan: {reference}"
                )
            plan[reference] = dict(candidate)
    return plan


def _chunks(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def _v20_requirement_partitions(
    plan: dict[str, dict[str, Any]],
    *,
    partition_size: int = _PARTITION_SIZE,
) -> list[dict[str, dict[str, Any]]]:
    """Split dense coverage into bounded semantic units without changing source obligations."""

    if partition_size < 1:
        raise ValueError("partition_size must be positive")
    core: list[str] = []
    contextual: list[str] = []
    for reference, candidate in plan.items():
        hint = candidate.get("obligation_hint")
        source_kind = candidate.get("source_kind")
        non_excludable = not bool(candidate.get("allow_exclusion", False))
        if non_excludable or hint in {"required", "preferred"} or source_kind == "structured_skill":
            core.append(reference)
        else:
            contextual.append(reference)

    partitions: list[dict[str, dict[str, Any]]] = []
    for group in [*_chunks(core, partition_size), *_chunks(contextual, partition_size)]:
        partitions.append({reference: dict(plan[reference]) for reference in group})
    return partitions


def _partition_prompt(base_prompt: str, *, index: int, total: int) -> str:
    return (
        base_prompt
        + "\n\nP1.6 V20 SOURCE-LED PARTITION "
        + f"{index}/{total}:\n"
        + "This call owns ONLY the evidence references listed in requirement_coverage and "
        + "responsibility_coverage. Extract/account for every supplied reference, but do not "
        + "re-extract requirements, duties, or role purpose from evidence outside this partition. "
        + "When responsibility_coverage is empty, return role_purpose=[] and responsibilities=[]. "
        + "When a requirement reference is genuinely not a qualification and exclusion is allowed, "
        + "use coverage_exclusions rather than inventing a requirement. Preserve every inherited "
        + "exact-evidence, strength, depth, ontology, and fail-closed rule."
    )


def _assert_partition_scope(
    structured: dict[str, Any],
    *,
    requirement_plan: dict[str, dict[str, Any]],
    responsibility_plan: dict[str, str],
) -> None:
    """Reject cross-partition leakage so one slice cannot overwrite another slice's decisions."""

    allowed_requirements = {
        _normalize(str(candidate.get("text") or ""))
        for candidate in requirement_plan.values()
    }
    requirements = structured.get("requirements")
    if not isinstance(requirements, list):
        raise AnalysisValidationError("P1.6 v20 partition requirements array is malformed")
    leaked_requirements = sorted(
        {
            str(item.get("evidence") or "")
            for item in requirements
            if isinstance(item, dict)
            and _normalize(str(item.get("evidence") or "")) not in allowed_requirements
        }
    )
    if leaked_requirements:
        raise AnalysisValidationError(
            "P1.6 v20 partition emitted requirement evidence outside its assigned ledger: "
            + repr(leaked_requirements)
        )

    allowed_responsibilities = {_normalize(text) for text in responsibility_plan.values()}
    leaked_responsibilities: set[str] = set()
    for key in ("role_purpose", "responsibilities"):
        values = structured.get(key)
        if not isinstance(values, list):
            raise AnalysisValidationError(f"P1.6 v20 partition {key} array is malformed")
        for item in values:
            if not isinstance(item, dict):
                continue
            evidence = str(item.get("evidence") or "")
            if _normalize(evidence) not in allowed_responsibilities:
                leaked_responsibilities.add(evidence)
    if leaked_responsibilities:
        raise AnalysisValidationError(
            "P1.6 v20 partition emitted duty evidence outside its assigned ledger: "
            + repr(sorted(leaked_responsibilities))
        )

    exclusions = structured.get("coverage_exclusions")
    if not isinstance(exclusions, list):
        raise AnalysisValidationError("P1.6 v20 partition coverage_exclusions array is malformed")
    allowed_exclusion_refs = set(requirement_plan)
    leaked_exclusions = sorted(
        {
            str(item.get("evidence_reference") or "")
            for item in exclusions
            if isinstance(item, dict)
            and str(item.get("evidence_reference") or "") not in allowed_exclusion_refs
        }
    )
    if leaked_exclusions:
        raise AnalysisValidationError(
            "P1.6 v20 partition emitted exclusions outside its assigned ledger: "
            + repr(leaked_exclusions)
        )


def _merge_partition_structured(parts: list[dict[str, Any]]) -> dict[str, Any]:
    """Union independently valid partitions while removing only exact duplicate records."""

    merged: dict[str, list[Any]] = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [],
        "coverage_exclusions": [],
    }
    seen: dict[str, set[tuple[str, ...]]] = {key: set() for key in merged}

    for part in parts:
        for key in merged:
            values = part.get(key)
            if not isinstance(values, list):
                raise AnalysisValidationError(f"P1.6 v20 partition {key} array is malformed")
            for item in values:
                if not isinstance(item, dict):
                    merged[key].append(item)
                    continue
                if key in {"role_purpose", "responsibilities"}:
                    identity = (
                        _normalize(str(item.get("statement") or "")),
                        _normalize(str(item.get("evidence") or "")),
                    )
                elif key == "requirements":
                    identity = (
                        _normalize(str(item.get("concept") or "")),
                        str(item.get("requirement_type") or ""),
                        _normalize(str(item.get("evidence") or "")),
                    )
                else:
                    identity = (str(item.get("evidence_reference") or ""),)
                if identity in seen[key]:
                    continue
                seen[key].add(identity)
                merged[key].append(dict(item))
    return merged


class V20CandidateAnalysisProvider(V19CandidateAnalysisProvider):
    """Extract dense source-led coverage in bounded independent semantic partitions."""

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
        complete_plan = _v20_complete_requirement_plan(
            model_fields,
            additional_plan=additional_plan,
            skill_plan=skill_plan,
            decomposed_refs=decomposed_refs,
        )
        requirement_partitions = _v20_requirement_partitions(complete_plan)
        responsibility_plan = build_responsibility_coverage_plan(model_fields)
        if not requirement_partitions:
            requirement_partitions = [{}]

        payload_base = dict(kwargs.get("user_payload") or {})
        payload_base["analysis_fields"] = model_fields
        payload_base["candidate_deterministic_requirement_references"] = deterministic_refs

        structured_parts: list[dict[str, Any]] = []
        request_parts: list[dict[str, Any]] = []
        raw_parts: list[dict[str, Any]] = []
        finish_reasons: list[str] = []
        total = len(requirement_partitions)

        for offset, partition in enumerate(requirement_partitions):
            index = offset + 1
            partition_responsibilities = responsibility_plan if index == 1 else {}
            partition_refs = set(partition)
            payload = dict(payload_base)
            payload["candidate_required_qualification_references"] = [
                reference for reference in qualification_refs if reference in partition_refs
            ]
            payload["candidate_residual_requirement_references"] = [
                reference for reference in residual_refs if reference in partition_refs
            ]
            payload["analysis_partition"] = {
                "index": index,
                "total": total,
                "requirement_references": list(partition),
                "responsibility_references": list(partition_responsibilities),
            }

            result = complete_analysis_partition_with_instructor_v20(
                base_url=f"{self._base_url}/",
                api_token=self._api_token,
                timeout_seconds=self._timeout_seconds,
                network_retries=self._max_retries,
                selected_model=selected_model,
                system_prompt=_partition_prompt(system_prompt, index=index, total=total),
                user_payload=payload,
                max_tokens=int(kwargs.get("max_tokens") or 8192),
                seed=int(kwargs.get("seed") or 0) + offset,
                requirement_coverage_plan=partition,
                responsibility_coverage_plan=partition_responsibilities,
                validation_retries=1,
            )
            _assert_partition_scope(
                result.structured,
                requirement_plan=partition,
                responsibility_plan=partition_responsibilities,
            )
            structured_parts.append(result.structured)
            request_parts.append(result.request_body)
            raw_parts.append(result.raw_response)
            if result.finish_reason:
                finish_reasons.append(result.finish_reason)

        structured = _merge_partition_structured(structured_parts)
        structured = _materialize_v18_deterministic_requirements(structured, deterministic)
        structured, normalized_indexes = _normalize_v15_schedule_concepts(structured)
        structured = inject_decomposition_exclusions(structured, original_fields)
        validate_v15_candidate_structured(structured, original_fields)

        request_body = {
            "model": selected_model,
            "partition_requests": request_parts,
            "runtime": {
                "context_length_tokens": runtime.context_length,
                "context_action": runtime.action,
                "model_instance_id": runtime.instance_id,
                "exclusive_llm": True,
                "p16_v17_source_led_requirement_capacity": True,
                "p16_v18_deterministic_structured_requirements": deterministic_refs,
                "p16_v18_structured_skill_coverage": sorted(skill_plan),
                "p16_v19_depth_optionality_prevalidation": True,
                "p16_v20_source_led_partitioning": True,
                "p16_v20_partition_size": _PARTITION_SIZE,
                "p16_v20_partition_count": total,
                "p16_v20_partition_refs": [list(partition) for partition in requirement_partitions],
                "p16_v15_schedule_depth_normalization": True,
                "p16_v15_schedule_concept_normalization": normalized_indexes,
            },
        }
        return StructuredInferenceResult(
            model=selected_model,
            structured=structured,
            request_body=request_body,
            raw_response={"partitions": raw_parts},
            finish_reason=",".join(finish_reasons) if finish_reasons else None,
        )


def build_v20_candidate_analysis_service(settings: Settings) -> JobAnalysisServiceV20:
    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    return JobAnalysisServiceV20(
        source_store=TranslationStore(settings.database_path),
        translation_service=_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        provider=V20CandidateAnalysisProvider(
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
    "V20CandidateAnalysisProvider",
    "_PARTITION_SIZE",
    "_assert_partition_scope",
    "_merge_partition_structured",
    "_v20_complete_requirement_plan",
    "_v20_requirement_partitions",
    "build_v20_candidate_analysis_service",
]
