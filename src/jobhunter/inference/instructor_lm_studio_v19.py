"""Candidate-only typed response model for P1.6 v19.

V18 moved mechanically known structured education/experience facts out of model ownership. The
next dense live run exposed a narrower normalization class inside otherwise valid semantic output:
preference words (``a plus``, ``helpful``) were placed in ``depth_signal``, and an unsupported
``expertise`` modifier was introduced into a normalized concept. V19 canonicalizes only those
mechanically provable boundary mistakes before the existing strict requirement validator runs.
"""

from __future__ import annotations

import re
from typing import Any

from pydantic import Field, ValidationInfo, model_validator

from jobhunter.evidence_refs import has_english_optionality_signal
from jobhunter.inference.instructor_lm_studio import (
    _DEPTH_SIGNAL_PATTERNS,
    _normalize,
)
from jobhunter.inference.instructor_lm_studio_v14 import AnalysisRequirementV14
from jobhunter.inference.instructor_lm_studio_v17 import JobAnalysisResponseV17

_GENERIC_CONCEPTS = {
    "domain",
    "education",
    "experience",
    "knowledge",
    "other",
    "practice",
    "skill",
    "tool",
}
_LEADING_PREPOSITION_RE = re.compile(r"^(?:in|with|of)\b\s*", re.I)
_EMPTY_GROUP_RE = re.compile(r"(?:\(\s*\)|\[\s*\]|\{\s*\})")


def _raw_evidence_text(value: dict[str, Any], info: ValidationInfo) -> str:
    """Resolve a raw model evidence ID to its supplied exact source text when available."""

    evidence = str(value.get("evidence") or "").strip()
    catalog = (info.context or {}).get("evidence_catalog") or {}
    if isinstance(catalog, dict):
        referenced = catalog.get(evidence)
        if isinstance(referenced, str) and referenced.strip():
            return referenced.strip()
    return evidence


def _has_depth_signal(text: str) -> bool:
    return any(pattern.search(text) for pattern in _DEPTH_SIGNAL_PATTERNS.values())


def _normalize_unsupported_depth_words(concept: str, evidence: str) -> str:
    """Remove model-added depth vocabulary only when the cited source does not contain it.

    This is intentionally not a general paraphraser. A depth token that is actually present in the
    source remains untouched so the inherited strict validator can require correct separation into
    ``depth_signal``. Only unsupported generated depth wording is eligible for deterministic
    removal, and cleanup is abandoned when it would leave an empty/generic concept.
    """

    candidate = concept
    changed = False
    for pattern in _DEPTH_SIGNAL_PATTERNS.values():
        if pattern.search(candidate) is None or pattern.search(evidence) is not None:
            continue
        candidate = pattern.sub(" ", candidate)
        changed = True

    if not changed:
        return concept

    candidate = _EMPTY_GROUP_RE.sub(" ", candidate)
    candidate = " ".join(candidate.strip(" ,;:-/").split())
    candidate = _LEADING_PREPOSITION_RE.sub("", candidate).strip()
    candidate = " ".join(candidate.strip(" ,;:-/").split())
    if not candidate or _normalize(candidate) in _GENERIC_CONCEPTS:
        return concept
    return candidate


class AnalysisRequirementV19(AnalysisRequirementV14):
    """Canonicalize optionality/depth leakage before inherited strict semantic validation."""

    @model_validator(mode="before")
    @classmethod
    def normalize_depth_optionality_boundary(
        cls,
        value: Any,
        info: ValidationInfo,
    ) -> Any:
        if not isinstance(value, dict):
            return value

        normalized = dict(value)
        evidence = _raw_evidence_text(value, info)

        signal = normalized.get("depth_signal")
        if (
            normalized.get("requirement_type") == "preferred"
            and isinstance(signal, str)
            and signal.strip()
            and not _has_depth_signal(signal)
            and has_english_optionality_signal(signal)
            and has_english_optionality_signal(evidence)
        ):
            normalized["depth_signal"] = None

        concept = normalized.get("concept")
        if isinstance(concept, str) and concept.strip():
            normalized["concept"] = _normalize_unsupported_depth_words(
                concept.strip(),
                evidence,
            )
        return normalized


class JobAnalysisResponseV19(JobAnalysisResponseV17):
    """V17 aggregate coverage + v19 requirement-item prevalidation canonicalization."""

    requirements: list[AnalysisRequirementV19] = Field()


__all__ = [
    "AnalysisRequirementV19",
    "JobAnalysisResponseV19",
    "_normalize_unsupported_depth_words",
]
