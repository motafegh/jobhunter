"""Isolated v23 provider using the v22 fail-closed source-fact response model."""

from __future__ import annotations

import re
from typing import Any, Self

from pydantic import Field, ValidationInfo, model_validator

from jobhunter.inference import instructor_lm_studio_v20 as v20
from jobhunter.inference.instructor_lm_studio import (
    AnalysisClaim,
    _equivalent_source_excerpt,
)
from jobhunter.inference.instructor_lm_studio_v20 import _depth_matches
from jobhunter.inference.instructor_lm_studio_v22 import (
    AnalysisRequirementV22,
    JobAnalysisResponseV22,
    persisted_v20_shape,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult

_PROOF_VALUE_PREFERENCE_RE = re.compile(r"\b(?:very|more)\s+valuable\b", re.I)
_ITEM_POINTS_PREFERENCE_RE = re.compile(
    r"\b(?:is|are)\s+considered\s+(?:an?\s+)?points?\.?$", re.I
)
_CONDITIONAL_WORK_RE = re.compile(
    r"\b(?:if|when|where|as)\s+(?:necessary|needed|applicable|appropriate|required)\b",
    re.I,
)
_CONDITIONAL_STATEMENT_RE = re.compile(
    r"\b(?:if|when|where|as)\s+(?:necessary|needed|applicable|appropriate|required)\b|"
    r"\b(?:optional(?:ly)?|conditional(?:ly)?|potential(?:ly)?|may)\b",
    re.I,
)
_ONE_OF_ALTERNATIVES_RE = re.compile(r"\bat\s+least\s+one\s+of\b[^.!?\n]*\bor\b", re.I)
_ALTERNATIVE_DEPTH_PREFIX_RE = re.compile(
    r"^(?:(?:general|practical|initial|basic|strong|relative)\s+)?"
    r"(?:familiarity\s+with|mastery\s+of|proficiency\s+in)\s+",
    re.I,
)


def _source_alternative_concept(item: str) -> str | None:
    """Use a short exact source item when model prose loses explicit alternatives."""

    source = item.strip(" ,.")
    if not re.search(r"\bor\b", source, re.I) or len(source) > 180 or "\n" in source:
        return None
    concept = _ALTERNATIVE_DEPTH_PREFIX_RE.sub("", source, count=1).strip()
    return concept if concept and re.search(r"\bor\b", concept, re.I) else None


class AnalysisResponsibilityV23(AnalysisClaim):
    """Keep an explicit source condition on extracted employer work."""

    @model_validator(mode="after")
    def retain_source_condition(self, info: ValidationInfo) -> Self:
        if (
            (info.context or {}).get("analysis_mode") == "english"
            and _CONDITIONAL_WORK_RE.search(self.evidence)
            and not _CONDITIONAL_STATEMENT_RE.search(self.statement)
        ):
            raise ValueError("Responsibility statement must preserve explicit source condition")
        return self


class AnalysisRequirementV23(AnalysisRequirementV22):
    """Recognize exact value preference only for versioned candidate-proof refs."""

    @model_validator(mode="before")
    @classmethod
    def preserve_source_alternatives(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        item = value.get("item_excerpt")
        if not isinstance(item, str):
            return value
        # A depth field describes an explicit degree in this exact item. Prior
        # experience and knowledge remain in the concept/evidence even when the
        # item contains no separate proficiency degree. Discard only a model
        # supplied non-degree excerpt; source and concept validation still run.
        signal = value.get("depth_signal")
        normalized = value
        if (
            isinstance(signal, str)
            and signal.strip()
            and not _depth_matches(item)
            and _equivalent_source_excerpt(signal, str(value.get("evidence") or ""))
            is not None
        ):
            normalized = {**value, "depth_signal": None}
        if (
            normalized.get("concept_type")
            in {"skill", "knowledge", "practice", "domain", "experience", "tool"}
            and re.match(r"^ability\s+to\b", str(normalized.get("concept") or ""), re.I)
        ):
            # A literal source wrapper is valid evidence, but it does not name
            # a normalized capability. Preserve the claim with an untyped label.
            normalized = {**normalized, "concept_type": "other"}
        concept = _source_alternative_concept(item)
        if concept is None or concept == normalized.get("concept"):
            return normalized
        return {**normalized, "concept": concept}

    @model_validator(mode="after")
    def retain_disjunctive_minimum(self, info: ValidationInfo) -> Self:
        if (
            (info.context or {}).get("analysis_mode") == "english"
            and self.requirement_type == "required"
            and _ONE_OF_ALTERNATIVES_RE.search(self.item_excerpt)
            and not re.search(r"\bor\b|\bat\s+least\s+one\b", self.concept, re.I)
        ):
            raise ValueError("Required concept must preserve at-least-one source alternatives")
        return self

    def _has_exact_preference_signal(self, text: str, plan: dict[str, Any]) -> bool:
        if super()._has_exact_preference_signal(text, plan):
            return True
        if text == self.item_excerpt and _ITEM_POINTS_PREFERENCE_RE.search(text):
            return True
        if any(
            isinstance(candidate, dict)
            and candidate.get("source_kind") in {
                "candidate_qualification_item", "requirement_section"
            }
            and candidate.get("obligation_hint") == "preferred"
            and candidate.get("text") == self.evidence
            and candidate.get("text") == text
            and isinstance(candidate.get("obligation_context"), str)
            and (
                candidate.get("source_kind") == "requirement_section"
                or candidate["text"] in candidate["obligation_context"]
            )
            and re.search(
                r"\b(?:important\s+asset|considered\s+an?\s+(?:asset|advantage)|"
                r"(?:an?\s+)?advantage|(?:an?\s+)?plus|score\s+is\s+given\s+for|"
                r"points?\s+(?:are\s+also\s+)?awarded\s+for|preferred|"
                r"nice[ -]to[ -]have)\b",
                candidate["obligation_context"], re.I,
            )
            for candidate in plan.values()
        ):
            return True
        return bool(
            _PROOF_VALUE_PREFERENCE_RE.search(text)
            and any(
                isinstance(candidate, dict)
                and candidate.get("source_kind") == "candidate_proof"
                and candidate.get("obligation_hint") == "preferred"
                and candidate.get("text") == self.evidence
                for candidate in plan.values()
            )
        )


class JobAnalysisResponseV23(JobAnalysisResponseV22):
    """V22 source-fact guards with scoped proof-preference recognition."""

    responsibilities: list[AnalysisResponsibilityV23] = Field(max_length=16)
    requirements: list[AnalysisRequirementV23] = Field()


def complete_analysis_partition_with_instructor_v23(
    *,
    base_url: str,
    api_token: str | None,
    timeout_seconds: float,
    network_retries: int,
    selected_model: str,
    system_prompt: str,
    user_payload: dict[str, Any],
    max_tokens: int,
    seed: int,
    requirement_coverage_plan: dict[str, dict[str, Any]],
    responsibility_coverage_plan: dict[str, str],
    validation_retries: int = 1,
) -> StructuredInferenceResult:
    additional_evidence_catalog = {
        reference: str(candidate.get("text") or "")
        for reference, candidate in requirement_coverage_plan.items()
    }
    additional_evidence_catalog.update(responsibility_coverage_plan)
    candidate_payload = dict(user_payload)
    candidate_payload["exact_item_coverage"] = [
        {
            "parent_reference": reference,
            "item_excerpt": required.get("text"),
            "required_concept_type": required.get("required_concept_type"),
        }
        for reference, candidate in requirement_coverage_plan.items()
        for required in candidate.get("required_item_excerpts") or []
        if isinstance(required, dict)
    ]
    result = v20._complete_analysis_partition_with_instructor(
        base_url=base_url,
        api_token=api_token,
        timeout_seconds=timeout_seconds,
        network_retries=network_retries,
        selected_model=selected_model,
        system_prompt=system_prompt,
        user_payload=candidate_payload,
        max_tokens=max_tokens,
        seed=seed,
        requirement_coverage_plan=requirement_coverage_plan,
        responsibility_coverage_plan=responsibility_coverage_plan,
        response_model=JobAnalysisResponseV23,
        contract_version="v23",
        validation_retries=validation_retries,
        additional_evidence_catalog=additional_evidence_catalog,
    )
    request_body = dict(result.request_body)
    runtime = dict(request_body.get("runtime") or {})
    runtime["p16_v21_item_scoped_evidence"] = True
    runtime["p16_v22_ontology_abstention"] = True
    runtime["p16_v23_candidate_proof_coverage"] = True
    request_body["runtime"] = runtime
    return StructuredInferenceResult(
        model=result.model,
        structured=result.structured,
        request_body=request_body,
        raw_response=result.raw_response,
        finish_reason=result.finish_reason,
    )


__all__ = [
    "AnalysisRequirementV23",
    "JobAnalysisResponseV23",
    "complete_analysis_partition_with_instructor_v23",
    "persisted_v20_shape",
]
