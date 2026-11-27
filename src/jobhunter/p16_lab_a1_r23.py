"""Bounded, offline-only A1 motivation and duty-boundary repair seams."""

from __future__ import annotations

import re
from typing import Any, Self

from pydantic import Field, ValidationInfo, model_validator

from jobhunter.evidence_refs import evidence_mixes_english_optionality
from jobhunter.evidence_refs_v21 import build_responsibility_coverage_plan_v21
from jobhunter.evidence_refs_v23 import build_requirement_coverage_plan_v23
from jobhunter.inference.instructor_lm_studio import _equivalent_source_excerpt
from jobhunter.inference.instructor_lm_studio_v20 import _depth_matches
from jobhunter.inference.instructor_lm_studio_v30 import (
    AnalysisRequirementV30,
    JobAnalysisResponseV30,
)
from jobhunter.p16_lab_a1_r1 import AnalysisRequirementR1

# Recognize explicit motivation syntax, not adjectives in isolation.
_MOTIVATION = re.compile(
    r"^(?:with\s+)?(?:an?\s+)?(?P<meaning>(?:(?:strong|keen|genuine)\s+)?"
    r"(?:interest\s+in|enthusiasm\s+for|motivation\s+to)\s+(?P<subject>[^.!?;]+))\.?$",
    re.I,
)
_MIXED = re.compile(
    r"\b(?:experience|proficien(?:cy|t)|mastery|knowledge|understanding|"
    r"ability|expertise|familiarity|qualification|certification|years?)\b|[,;:]",
    re.I,
)


def _motivation_meaning(text: str) -> str | None:
    match = _MOTIVATION.fullmatch(text.strip())
    if not match or _MIXED.search(match["subject"]):
        return None
    if any(
        marker.casefold().replace("-", " ") != "hands on"
        for _, _, marker in _depth_matches(match["subject"])
    ):
        return None
    return match["meaning"]


def _norm(text: str) -> str:
    return " ".join(text.split()).casefold()


def _validate_motivation(item, info: ValidationInfo) -> bool:
    """Only bypass the depth-specific checks for an exact, unmixed motivation item.

    Preserve the other V21 guards in this narrow branch; do not retype technical
    claims, infer experience, or weaken employer obligation.
    """
    if (info.context or {}).get("analysis_mode") != "english":
        return False
    exact = _equivalent_source_excerpt(item.item_excerpt, item.evidence)
    meaning = _motivation_meaning(exact) if exact is not None else None
    if meaning is None:
        return False
    if item.concept_type != "other" or _norm(item.concept) != _norm(meaning):
        raise ValueError("Motivation concept must preserve source meaning without technical typing")
    if item.requirement_type == "inferred" and not item.rationale.strip():
        raise ValueError("Inferred requirements require a concise non-empty rationale")
    if evidence_mixes_english_optionality(exact):
        raise ValueError("One item excerpt cannot mix core and optional wording")
    plan = (info.context or {}).get("requirement_coverage_plan") or {}
    preferred = any(
        isinstance(c, dict)
        and c.get("text") == item.evidence
        and c.get("obligation_hint") == "preferred"
        for c in plan.values()
    )
    if preferred and item.requirement_type != "preferred":
        raise ValueError("Preferred parent coverage requires preferred item strength")
    if item.requirement_type == "preferred" and not (
        item._has_exact_preference_signal(exact, plan)
        or (preferred and item._has_exact_preference_signal(item.evidence, plan))
    ):
        raise ValueError("Preferred item needs exact source preference in item or parent")
    if item.depth_signal is not None:
        signal = _equivalent_source_excerpt(item.depth_signal, exact)
        # Only discard a source-exact motivational adjective/head, not a
        # contradictory or invented technical-depth assertion.
        if signal is None or not re.fullmatch(
            r"(?:(?:strong|keen|genuine)(?:\s+(?:interest|enthusiasm|motivation))?"
            r"|interest|enthusiasm|motivation)",
            signal,
            re.I,
        ):
            raise ValueError("Motivation depth is not a source-exact motivation marker")
    item.item_excerpt = exact
    item.depth_signal = None
    return True


class AnalysisRequirementR2(AnalysisRequirementV30):
    @model_validator(mode="after")
    def validate_requirement_semantics(self, info: ValidationInfo) -> Self:
        if _validate_motivation(self, info):
            return self
        return super().validate_requirement_semantics(info)


class JobAnalysisResponseR2(JobAnalysisResponseV30):
    requirements: list[AnalysisRequirementR2] = Field()


class AnalysisRequirementR12(AnalysisRequirementR1):
    @model_validator(mode="after")
    def validate_requirement_semantics(self, info: ValidationInfo) -> Self:
        if _validate_motivation(self, info):
            return self
        return super().validate_requirement_semantics(info)


class JobAnalysisResponseR12(JobAnalysisResponseV30):
    requirements: list[AnalysisRequirementR12] = Field()


_SKILLS = re.compile(r"^skills\s*:\s*(?P<body>.+)$", re.I | re.S)
_SKILLS_BOUNDARY = re.compile(r"(?:^|[.!?]\s+|\n\s*)skills\s*:", re.I)
_QUAL_HEAD = re.compile(
    r"^(?:(?:strong|solid|good|practical|full|deep|basic|advanced)\s+)?"
    r"(?:familiarity|knowledge|understanding|proficiency|mastery|experience)\b",
    re.I,
)


def corrected_duty_plan(fields: dict[str, Any]) -> tuple[dict[str, str], tuple[str, ...]]:
    """Remove only a proven duplicate qualification in the supplemental duty list.

    Preserve original duty IDs and all ambiguous or unmatched items. No heading
    alone removes actual duties, and a source-exact requirement remains owed.
    """
    original = build_responsibility_coverage_plan_v21(fields)
    description = fields.get("description")
    if not isinstance(description, str):
        return original, ()
    qualification_texts = {
        c["text"]
        for c in build_requirement_coverage_plan_v23(fields).values()
        if c.get("source_kind") == "requirement_section"
        and c.get("obligation_hint") in {"required", "preferred"}
    }
    removed = []
    for ref, text in original.items():
        match = _SKILLS.fullmatch(text)
        if not ref.startswith("field:description:v21:duty:") or not match:
            continue
        body = match["body"]
        if body not in qualification_texts or not _QUAL_HEAD.match(body):
            continue
        # Do not discard mixed paragraphs with a separate work statement or
        # explicit duty cue, even when the qualification planner owns them.
        if re.search(
            r"[.!?]\s+\S|[;\n]|\b(?:you\s+will|responsible\s+for|must\s+(?:perform|deliver))\b",
            body,
            re.I,
        ):
            continue
        # Exact sentence/line heading occurrence, not an inline mention.
        if description.count(text) != 1:
            continue
        offset = description.index(text)
        if not any(m.start() <= offset < m.end() for m in _SKILLS_BOUNDARY.finditer(description)):
            continue
        removed.append(ref)
    return {ref: text for ref, text in original.items() if ref not in removed}, tuple(removed)
