"""Scoped runtime guard for the isolated P1.6 v15 candidate CLI.

The guard fixes validation ordering without changing public P1.6 or historical v14 behavior.
It is intentionally temporary candidate plumbing: normalize a linguistic ``Ability to ...``
wrapper before the existing strict v15/v14 validator, then restore the original runtime validator.
"""

from __future__ import annotations

import re
from contextlib import contextmanager
from typing import Any, Iterator

import jobhunter.analysis_runtime_v15 as runtime_v15

_CAPABILITY_TYPES = {"skill", "knowledge", "practice", "domain", "experience", "tool"}
_ABILITY_RE = re.compile(r"^ability\s+to\s+", re.I)
_GENERIC_REMAINDERS = {
    "be available",
    "be onsite",
    "be on site",
    "work",
    "work onsite",
    "work on site",
}


def normalize_ability_wrappers(structured: dict[str, Any]) -> list[int]:
    """Strip Ability-to only when a meaningful capability phrase remains.

    Exact evidence is never changed. Wrapper-only or obvious availability/logistics remnants remain
    untouched so the existing strict validator still fails closed.
    """

    requirements = structured.get("requirements")
    if not isinstance(requirements, list):
        return []

    changed: list[int] = []
    for index, item in enumerate(requirements):
        if not isinstance(item, dict):
            continue
        concept_type = str(item.get("concept_type") or "").strip()
        concept = str(item.get("concept") or "").strip()
        if concept_type not in _CAPABILITY_TYPES or not _ABILITY_RE.search(concept):
            continue

        candidate = " ".join(_ABILITY_RE.sub("", concept).strip().split())
        if len(candidate.split()) < 2 or candidate.casefold() in _GENERIC_REMAINDERS:
            continue
        item["concept"] = candidate
        changed.append(index)
    return changed


@contextmanager
def v15_ability_wrapper_guard() -> Iterator[None]:
    """Apply normalization only around the isolated candidate run."""

    original = runtime_v15.validate_v15_candidate_structured

    def guarded_validate(structured: dict[str, Any], analysis_fields: dict[str, Any]) -> None:
        normalize_ability_wrappers(structured)
        original(structured, analysis_fields)

    runtime_v15.validate_v15_candidate_structured = guarded_validate
    try:
        yield
    finally:
        runtime_v15.validate_v15_candidate_structured = original


__all__ = ["normalize_ability_wrappers", "v15_ability_wrapper_guard"]
