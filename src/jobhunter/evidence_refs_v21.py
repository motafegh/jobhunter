"""Candidate-only exact evidence planning for the isolated P1.6 v21 contract."""

from __future__ import annotations

import re
from typing import Any

from jobhunter.evidence_refs import (
    build_requirement_coverage_plan,
    build_responsibility_coverage_plan,
    has_english_optionality_signal,
)

_SENTENCE_RE = re.compile(r"[^.!?]+(?:[.!?]|$)")
_APPLICATION_DIRECTIVE_RE = re.compile(
    r"^(?:to\s+apply\b[^.!?]*?\bplease\s+send\b|"
    r"interested\s+parties,?\s+please\s+send\b|"
    r"please\s+send\s+your\s+(?:resume|cv)\b)",
    re.I,
)
_LIST_GERUND_RE = re.compile(r"(?:^include\s+|,\s+)(?P<verb>[A-Za-z]+ing)\b", re.I)
_COLLABORATION_DUTY_RE = re.compile(
    r"^(?:close\s+)?collaboration\s+with\b[^.!?]*\bto\s+[a-z]", re.I
)


def _sentences(text: str) -> list[str]:
    return [
        match.group(0).strip()
        for match in _SENTENCE_RE.finditer(text)
        if match.group(0).strip()
    ]


def build_requirement_coverage_plan_v21(
    fields: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Split only mixed-strength parent spans into exact candidate references."""

    result: dict[str, dict[str, Any]] = {}
    for reference, candidate in build_requirement_coverage_plan(fields).items():
        text = str(candidate["text"])
        sentences = _sentences(text)
        flags = [has_english_optionality_signal(sentence) for sentence in sentences]
        has_application_boundary = any(
            _APPLICATION_DIRECTIVE_RE.match(sentence) for sentence in sentences
        )
        mixes_strength = any(flags) and not all(flags)
        if len(sentences) < 2 or not (mixes_strength or has_application_boundary):
            result[reference] = dict(candidate)
            continue

        for index, sentence in enumerate(sentences):
            if _APPLICATION_DIRECTIVE_RE.match(sentence):
                break
            scoped = dict(candidate)
            scoped["text"] = sentence
            scoped["obligation_hint"] = (
                "preferred" if has_english_optionality_signal(sentence) else "required"
            )
            result[f"{reference}:sentence:{index}"] = scoped
    return result


def _gerund_list_items(sentence: str) -> list[str]:
    """Split a repeated gerund duty list while retaining coordinated verb phrases."""

    matches = list(_LIST_GERUND_RE.finditer(sentence))
    if len(matches) < 3:
        return []

    accepted = [matches[0]]
    for match in matches[1:]:
        previous = accepted[-1]
        between = sentence[previous.start("verb") : match.start()].strip(" ,")
        # "evaluating, debugging, and improving X" is one coordinated action:
        # a bare gerund before the next comma has no object and cannot stand alone.
        if len(between.split()) < 2:
            continue
        accepted.append(match)

    if len(accepted) < 3:
        return []
    items: list[str] = []
    for index, match in enumerate(accepted):
        start = 0 if index == 0 else match.start("verb")
        end = accepted[index + 1].start() if index + 1 < len(accepted) else len(sentence)
        item = sentence[start:end].strip(" ,")
        if item:
            items.append(item)
    return items


def build_responsibility_coverage_plan_v21(fields: dict[str, Any]) -> dict[str, str]:
    """Expose each explicit item in repeated duty lists to candidate coverage."""

    result: dict[str, str] = {}
    for reference, text in build_responsibility_coverage_plan(fields).items():
        sentences = _sentences(text)
        if not sentences:
            result[reference] = text
            continue
        items = _gerund_list_items(sentences[0])
        if not items:
            result[reference] = text
            continue
        for index, item in enumerate(items):
            result[f"{reference}:item:{index}"] = item
        for index, sentence in enumerate(sentences[1:], start=1):
            if _COLLABORATION_DUTY_RE.match(sentence):
                result[f"{reference}:sentence:{index}"] = sentence
                continue
            break
    return result


__all__ = [
    "build_requirement_coverage_plan_v21",
    "build_responsibility_coverage_plan_v21",
]
