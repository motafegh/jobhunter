"""First bounded A1 repair seam: preserve exact compound qualification scopes.

Experimental schema only; no production registration or general source parser.
The model still owns the meaning. A mechanically unique source/subject match
allows source-exact recovery, otherwise the compound item remains unresolved.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Self

from pydantic import Field, ValidationInfo, model_validator

from jobhunter.inference.instructor_lm_studio import _equivalent_source_excerpt
from jobhunter.inference.instructor_lm_studio_v19 import _raw_evidence_text
from jobhunter.inference.instructor_lm_studio_v20 import _depth_matches
from jobhunter.inference.instructor_lm_studio_v23 import AnalysisRequirementV23
from jobhunter.inference.instructor_lm_studio_v30 import (
    AnalysisRequirementV30,
    JobAnalysisResponseV30,
)

# Only explicit degree-headed clauses with a mechanically recoverable subject.
# Do not infer the meaning of arbitrary conjunctions or split an OR group.
_HEAD = (
    r"(?P<degree>(?:(?:strong|solid|relative|initial|basic|general|advanced|"
    r"sufficient|deep)\s+)?(?:proficiency|understanding|knowledge|mastery|familiarity))"
    r"\s+(?P<prep>in|of|with)\s+"
)
_LEAD = re.compile(r"^" + _HEAD, re.I)
_JOIN = re.compile(r",\s+(?:(?:with|and)\s+)?(?:an?\s+)?(?=" + _HEAD + ")", re.I)
_OR = re.compile(r"\bor\b", re.I)


@dataclass(frozen=True, slots=True)
class ScopedDegree:
    item: str
    degree: str
    subject: str
    head: str
    prep: str


def _normalized(text: str) -> str:
    return " ".join(text.split()).casefold()


def _single_scope(text: str) -> ScopedDegree | None:
    match = _LEAD.match(text)
    if match is None:
        return None
    degree = match["degree"]
    subject = text[match.end() :].strip(" ,.;")
    # At least one incumbent-recognized explicit marker, and no second
    # degree in the subject. Multiword markers in the one head are one degree.
    if not subject or not _depth_matches(degree) or _depth_matches(subject):
        return None
    return ScopedDegree(text.strip(" ,.;"), degree, subject, degree.split()[-1], match["prep"])


def _compound_scopes(text: str) -> tuple[ScopedDegree, ...]:
    if not _OR.search(text):
        return ()
    joins = list(_JOIN.finditer(text))
    if len(joins) != 1:
        return ()
    join = joins[0]
    first = _single_scope(text[: join.start()])
    second = _single_scope(text[join.end() :])
    if first is None or second is None:
        return ()
    return first, second


def _parent_scopes(text: str) -> tuple[ScopedDegree, ...]:
    # The evidence ledger can own a whole section, rather than only one
    # sentence. Recognize sentence-contained compounds; keep exact substrings.
    return tuple(
        scope
        for sentence in re.split(r"(?<=[.!?])\s+|\n+", text)
        for scope in _compound_scopes(sentence.strip())
    )


def _subject_matches(concept: str, scope: ScopedDegree) -> bool:
    # Exact match, or the model's source-supported degree/subject wrapper.
    # Never add missing alternatives or substitute another subject.
    return _normalized(concept) in {
        _normalized(scope.subject),
        _normalized(f"{scope.head} {scope.prep} {scope.subject}"),
        _normalized(f"{scope.degree} {scope.prep} {scope.subject}"),
    }


def _signal_matches(signal: object, scope: ScopedDegree) -> bool:
    if signal is None:
        return True
    if not isinstance(signal, str) or not signal.strip():
        return False
    return _normalized(signal) in {
        _normalized(scope.degree),
        _normalized(scope.item),
        *(_normalized(marker) for _, _, marker in _depth_matches(scope.degree)),
    }


class AnalysisRequirementR1(AnalysisRequirementV30):
    """V30 requirement with the bounded R1 normalization/degree repair only."""

    @model_validator(mode="before")
    @classmethod
    def preserve_source_alternatives(cls, value: Any, info: ValidationInfo) -> Any:
        if not isinstance(value, dict) or (info.context or {}).get("analysis_mode") != "english":
            return AnalysisRequirementV23.preserve_source_alternatives(value)
        item = value.get("item_excerpt")
        concept = value.get("concept")
        if not isinstance(item, str) or not isinstance(concept, str):
            return AnalysisRequirementV23.preserve_source_alternatives(value)
        parent = _raw_evidence_text(value, info)
        canonical = _equivalent_source_excerpt(item, parent)
        if canonical is None:
            return AnalysisRequirementV23.preserve_source_alternatives(value)
        scopes = _compound_scopes(canonical)
        if scopes:
            matches = [scope for scope in scopes if _subject_matches(concept, scope)]
            if len(matches) != 1 or not _signal_matches(value.get("depth_signal"), matches[0]):
                raise ValueError("Compound alternative has unresolved subject or degree scope")
            scope = matches[0]
            if (
                sum(_normalized(s.item) == _normalized(scope.item) for s in _parent_scopes(parent))
                != 1
            ):
                raise ValueError("Compound alternative parent scope is not unique")
            exact = _equivalent_source_excerpt(scope.item, parent)
            if exact is None:
                raise ValueError("Compound alternative child is not exact source evidence")
            # Keep the original parent reference, all other fields and OR topology.
            return {
                **value,
                "concept": scope.subject,
                "item_excerpt": exact,
                "depth_signal": scope.degree,
            }
        # If the model already supplied a scoped child of a recognized compound,
        # prevent the old rewrite from replacing its concept with the broad parent.
        parent_scopes = _parent_scopes(parent)
        matches = [
            scope
            for scope in parent_scopes
            if _normalized(scope.item) == _normalized(canonical.strip(" ,.;"))
        ]
        if len(matches) > 1:
            raise ValueError("Compound alternative parent scope is not unique")
        if len(matches) == 1:
            scope = matches[0]
            if not _subject_matches(concept, scope) or not _signal_matches(
                value.get("depth_signal"), scope
            ):
                raise ValueError("Compound alternative child has unresolved subject or degree")
            return {
                **value,
                "concept": scope.subject,
                "item_excerpt": canonical,
                "depth_signal": scope.degree,
            }
        return AnalysisRequirementV23.preserve_source_alternatives(value)

    @model_validator(mode="after")
    def validate_requirement_semantics(self, info: ValidationInfo) -> Self:
        # Restrict the full-degree repair to exact children of a recognized
        # compound alternative parent. Keep every other incumbent validator.
        if (info.context or {}).get("analysis_mode") == "english":
            scopes = _parent_scopes(self.evidence)
            matches = [
                scope
                for scope in scopes
                if _normalized(scope.item) == _normalized(self.item_excerpt.strip(" ,.;"))
                and _normalized(scope.subject) == _normalized(self.concept)
            ]
            if len(matches) == 1:
                scope = matches[0]
                if not _signal_matches(self.depth_signal, scope):
                    raise ValueError("Compound alternative degree is outside the child scope")
                # The inherited validator treats separate lexical matches as
                # separate levels. Validate a single source marker using every
                # existing rule, then retain the complete exact degree phrase.
                self.depth_signal = _depth_matches(scope.degree)[0][2]
                validated = super().validate_requirement_semantics(info)
                validated.depth_signal = scope.degree
                return validated
        return super().validate_requirement_semantics(info)


class JobAnalysisResponseR1(JobAnalysisResponseV30):
    requirements: list[AnalysisRequirementR1] = Field()
