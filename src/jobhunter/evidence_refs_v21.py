"""Candidate-only exact evidence planning for the isolated P1.6 v21 contract."""

from __future__ import annotations

import re
from typing import Any

from jobhunter.evidence_refs import (
    build_requirement_coverage_plan,
    build_responsibility_coverage_plan,
    has_english_optionality_signal,
)

_APPLICATION_DIRECTIVE_RE = re.compile(
    r"^(?:to\s+apply\b[^.!?]*?\bplease\s+send\b|"
    r"interested\s+parties,?\s+please\s+send\b|"
    r"please\s+(?:do\s+not\s+)?send\s+your\s+(?:resume|cv)\b|"
    r"submit\s+(?:a|your)\s+(?:resume|cv)\b)",
    re.I,
)
_APPLICATION_SECTION_START_RE = re.compile(
    r"^(?:to\s+apply\b|interested\s+parties\b)", re.I
)
_CANDIDATE_SECTION_HEADING_RE = re.compile(
    r"(?i)(?:\(\s*)?(?P<heading>skills\s+and\s+abilities|expected\s+skills|"
    r"benefits(?:\s+(?:and\s+opportunities|of\s+collaboration))?|"
    r"tasks|job\s+description|"
    r"performance\s+indicators\s*\(kpis\)|(?:work\s+)?location)"
    r"(?:\s*:|(?<=benefits)\s+include\b)"
)
_REQUIREMENT_REENTRY_HEADINGS = {"skills and abilities", "expected skills"}
_ASTERISK_ITEM_RE = re.compile(r"(?:^|\s+)\*\s+")
_PREFERRED_GROUP_START_RE = re.compile(r"(?:points\s+considered|advantages)\s*:", re.I)
_APPLICATION_PREFERENCE_RE = re.compile(
    r"\b(?:significant|positive|strong)\s+impact\s+on\s+(?:the\s+)?"
    r"(?:resume|application|portfolio)\s+review\b",
    re.I,
)
_LIST_GERUND_RE = re.compile(
    r"(?:^include\s+|^|,\s+(?:and\s+)?)(?P<verb>[A-Za-z]+ing)\b", re.I
)
_BARE_GERUND_CHAIN_RE = re.compile(
    r"[A-Za-z]+ing(?:\s*,\s*[A-Za-z]+ing)*", re.I
)
_COLLABORATION_DUTY_RE = re.compile(
    r"^(?:close\s+)?collaboration\s+with\b[^.!?]*\bto\s+[a-z]", re.I
)
_EXPLICIT_CANDIDATE_REQUIREMENT_RE = re.compile(
    r"\b(?:we\s+need\s+someone\s+who\s+can|the\s+candidate\s+must|"
    r"you\s+must|you\s+will\s+need\s+to)\b",
    re.I,
)
_CANDIDATE_SUBJECT_RE = re.compile(
    r"\b(?:we\s+(?:are|'re)\s+looking\s+for|is\s+looking\s+to\s+attract|"
    r"role\s+is\s+suitable\s+for\s+someone|if\s+you)\b",
    re.I,
)
_CANDIDATE_QUALIFICATION_RE = re.compile(
    r"\b(?:experience|experienced|ability\s+to|able\s+to|have\s+built|"
    r"have\s+worked\s+with)\b",
    re.I,
)
_CANDIDATE_DUTY_SECTION_RE = re.compile(
    r"(?i)(?P<heading>job\s+description|tasks|responsibilities|qualifications|"
    r"requirements|skills\s+and\s+abilities|expected\s+skills|required\s+skills|"
    r"benefits(?:\s+(?:and\s+opportunities|of\s+collaboration))?|"
    r"performance\s+indicators\s*\(kpis\)|(?:work\s+)?location)\s*:"
)
_DUTY_SECTION_HEADINGS = {"job description", "tasks", "responsibilities"}


def _sentences(text: str) -> list[str]:
    sentences: list[str] = []
    cursor = 0
    parenthesis_depth = 0
    for index, character in enumerate(text):
        if character == "(":
            parenthesis_depth += 1
        elif character == ")":
            parenthesis_depth = max(0, parenthesis_depth - 1)
        elif character in ".!?" and parenthesis_depth == 0:
            sentence = text[cursor : index + 1].strip()
            if sentence:
                sentences.append(sentence)
            cursor = index + 1
    final = text[cursor:].strip()
    if final:
        sentences.append(final)
    return sentences


def has_candidate_optionality_signal(text: str) -> bool:
    """Recognize explicit candidate-only preference wording beyond the v20 contract."""

    return has_english_optionality_signal(text) or bool(_APPLICATION_PREFERENCE_RE.search(text))


def _candidate_requirement_chunks(text: str) -> tuple[list[str], bool]:
    """Keep exact requirement text while ending at candidate-only section boundaries."""

    matches = list(_CANDIDATE_SECTION_HEADING_RE.finditer(text))
    if not matches:
        return [text], False

    chunks: list[str] = []
    cursor = 0
    active = True
    for match in matches:
        before = text[cursor : match.start()].strip()
        if active and before:
            chunks.append(before)
        heading = " ".join(match.group("heading").casefold().split())
        active = heading in _REQUIREMENT_REENTRY_HEADINGS
        cursor = match.end()
    after = text[cursor:].strip()
    if active and after:
        chunks.append(after)
    return chunks, True


def _candidate_requirement_units(text: str) -> tuple[list[str], bool, bool]:
    chunks, section_changed = _candidate_requirement_chunks(text)
    units: list[str] = []
    list_changed = False
    for chunk in chunks:
        items = [
            item.strip()
            for item in _ASTERISK_ITEM_RE.split(chunk)
            if item.strip()
        ]
        if len(items) > 1:
            units.extend(items)
            list_changed = True
        else:
            units.extend(_sentences(chunk))
    return units, section_changed or list_changed, list_changed


def _coverage_group(reference: str) -> str:
    return re.split(r":(?:clause|sentence|item):\d+", reference, maxsplit=1)[0]


def _apply_preferred_group_scopes(
    plan: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Carry an explicit preferred-list heading across later references in its group."""

    result: dict[str, dict[str, Any]] = {}
    preferred_groups: set[str] = set()
    for reference, candidate in plan.items():
        group = _coverage_group(reference)
        text = str(candidate["text"])
        heading = _PREFERRED_GROUP_START_RE.search(text)
        if heading:
            before = text[: heading.start()].strip()
            after = text[heading.end() :].strip()
            if before:
                prefix = dict(candidate)
                prefix["text"] = before
                result[f"{reference}:required-prefix"] = prefix
            if after:
                preferred = dict(candidate)
                preferred["text"] = after
                preferred["obligation_hint"] = "preferred"
                result[f"{reference}:preferred-group"] = preferred
            preferred_groups.add(group)
            continue
        copied = dict(candidate)
        if group in preferred_groups:
            copied["obligation_hint"] = "preferred"
        result[reference] = copied
    return result


def build_requirement_coverage_plan_v21(
    fields: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Split only mixed-strength parent spans into exact candidate references."""

    result: dict[str, dict[str, Any]] = {}
    for reference, candidate in build_requirement_coverage_plan(fields).items():
        text = str(candidate["text"])
        units, boundary_changed, list_units = _candidate_requirement_units(text)
        flags = [has_candidate_optionality_signal(unit) for unit in units]
        has_application_boundary = any(
            _APPLICATION_DIRECTIVE_RE.match(unit) for unit in units
        )
        mixes_strength = any(flags) and not all(flags)
        if not boundary_changed and (
            len(units) < 2 or not (mixes_strength or has_application_boundary)
        ):
            result[reference] = dict(candidate)
            continue

        preferred_list_tail = False
        for index, sentence in enumerate(units):
            if _APPLICATION_DIRECTIVE_RE.match(sentence):
                if _APPLICATION_SECTION_START_RE.match(sentence):
                    break
                continue
            scoped = dict(candidate)
            scoped["text"] = sentence
            if list_units and has_candidate_optionality_signal(sentence):
                preferred_list_tail = True
            scoped["obligation_hint"] = (
                "preferred"
                if has_candidate_optionality_signal(sentence) or preferred_list_tail
                else "required"
            )
            if _EXPLICIT_CANDIDATE_REQUIREMENT_RE.search(sentence):
                scoped["allow_exclusion"] = False
            result[f"{reference}:sentence:{index}"] = scoped

    result = _apply_preferred_group_scopes(result)
    description = fields.get("description")
    if not isinstance(description, str):
        return result

    existing_texts = [str(candidate["text"]) for candidate in result.values()]
    for index, sentence in enumerate(_sentences(description)):
        if _APPLICATION_DIRECTIVE_RE.match(sentence):
            continue
        if not (
            _CANDIDATE_SUBJECT_RE.search(sentence)
            and _CANDIDATE_QUALIFICATION_RE.search(sentence)
        ):
            continue
        if any(
            sentence in text or (len(text) >= 40 and text in sentence)
            for text in existing_texts
        ):
            continue
        result[f"field:description:v21:candidate:{index}"] = {
            "text": sentence,
            "source_kind": "candidate_experience",
            "obligation_hint": "required",
            "allow_exclusion": False,
        }
        existing_texts.append(sentence)
    return result


def _gerund_list_items(sentence: str) -> list[str]:
    """Split a repeated gerund duty list while retaining coordinated verb phrases."""

    matches = [
        match
        for match in _LIST_GERUND_RE.finditer(sentence)
        if match.group("verb").casefold() != "including"
        and sentence[: match.start("verb")].count("(")
        == sentence[: match.start("verb")].count(")")
    ]
    if len(matches) < 3:
        return []

    accepted = [matches[0]]
    for match in matches[1:]:
        previous = accepted[-1]
        between = sentence[previous.start("verb") : match.start()].strip(" ,")
        # "evaluating, debugging, and improving X" is one coordinated action:
        # a bare gerund before the next comma has no object and cannot stand alone.
        if len(between.split()) < 2 or _BARE_GERUND_CHAIN_RE.fullmatch(between):
            continue
        accepted.append(match)

    if len(accepted) < 3:
        return []
    items: list[str] = []
    prefix = sentence[: accepted[0].start()].strip(" ,")
    if prefix:
        items.append(prefix)
    for index, match in enumerate(accepted):
        start = match.start("verb") if prefix or index > 0 else 0
        end = accepted[index + 1].start() if index + 1 < len(accepted) else len(sentence)
        item = sentence[start:end].strip(" ,")
        if item:
            items.append(item)
    return items


def _candidate_duty_sections(text: str) -> list[str]:
    matches = list(_CANDIDATE_DUTY_SECTION_RE.finditer(text))
    sections: list[str] = []
    for index, match in enumerate(matches):
        heading = " ".join(match.group("heading").casefold().split())
        if heading not in _DUTY_SECTION_HEADINGS:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.end() : end].strip()
        if section:
            sections.append(section)
    return sections


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
    description = fields.get("description")
    if not isinstance(description, str):
        return result
    existing = set(result.values())
    for section_index, section in enumerate(_candidate_duty_sections(description)):
        for sentence_index, sentence in enumerate(_sentences(section)):
            items = _gerund_list_items(sentence) or [sentence]
            for item_index, item in enumerate(items):
                if item in existing or any(item in parent for parent in existing):
                    continue
                result[
                    f"field:description:v21:duty:{section_index}:"
                    f"sentence:{sentence_index}:item:{item_index}"
                ] = item
                existing.add(item)
    return result


__all__ = [
    "build_requirement_coverage_plan_v21",
    "build_responsibility_coverage_plan_v21",
    "has_candidate_optionality_signal",
]
