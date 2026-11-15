"""B2 original-source item and board-metadata diagnostic candidate.

The input is an already-frozen parsed employer description. Candidate
classifications do not turn source text into accepted employer facts, and
board tags never establish employer-required skills. No provider, database,
network, translation, acceptance or downstream code is invoked here.

This intentionally small, context-preserving parser favors original spans,
recognizable headings and list structure over forced micro-classifications.
More ambiguous text remains candidate/unresolved for later semantic review.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Literal

from jobhunter.source_span_identity import (
    OriginalSourceAnchor,
    bind_original_source_span,
    verify_original_source_anchor,
)
from jobhunter.translation_store import TranslationSourceVersion

B2_SOURCE_CANDIDATE_CONTRACT = "jobhunter-b2-original-source-candidate-v1"

Category = Literal[
    "work_duty",
    "candidate_qualification",
    "behavioral_expectation",
    "work_arrangement",
    "compensation",
    "benefit",
    "application_instruction",
    "context",
    "unresolved",
]
Strength = Literal["required", "preferred", "stated_expectation", "not_applicable", "unresolved"]

# Structural headings, not employer obligation proofs. Keep the original
# passage intact when segmentation is not reliably supported by punctuation.
_HEADING_PATTERNS: tuple[tuple[str, str], ...] = (
    ("context", r"درباره\s+[^\s]{2,35}(?=\s+شرکت|\s+ما\b)"),
    ("work_duty", r"در\s+این\s+نقش\s+چه\s+کار\s+می[‌\s]*کنی\s*[؟?]"),
    ("candidate_qualification", r"چه\s+چیزهایی\s+برای\s+ما\s+مهم\s+است\s*[؟?]"),
    ("work_duty", r"شرح\s+وظایف(?=\s*[•●▪◦:]|\s+[^\s])"),
    ("work_duty", r"شرح\s+شغل(?:\s+و\s+وظایف)?\s*[:：]?"),
    ("work_duty", r"مسئولیت[‌\s]*های\s+اصلی\s*[:：]"),
    ("candidate_qualification", r"نیازمندی[‌\s]*ها(?=\s*[•●▪◦:]|\s+[^\s])"),
    ("candidate_qualification", r"مهارت[‌\s]*های\s+مورد\s+نیاز\s*[:：]"),
    ("candidate_qualification", r"شرایط\s+(?:احراز|تخصصی|عمومی)\s*[:：]"),
    ("candidate_qualification", r"سطح\s+(?:Middle|Senior|میانی|ارشد)\s*[:：]"),
    ("preferred", r"مواردی\s+که\s+مزیت\s+محسوب\s+می[‌\s]*شوند\s*[:：]"),
    ("preferred", r"مهارت[‌\s]*های\s+ترجیحی\s*[:：]"),
    ("benefit", r"مزایا(?=\s*[•●▪◦:]|\s+[^\s])"),
    ("work_arrangement", r"شرایط\s+(?:کاری|استخدام|همکاری)\s*[:：]?"),
    ("work_arrangement", r"نوع\s+همکاری\s*[:：]"),
    ("work_arrangement", r"محل\s+کار\s*[:：]"),
    ("compensation", r"حقوق\s*[:：]"),
    ("compensation", r"حقوق\s+از(?=\s*[۰-۹0-9])"),
    ("application_instruction", r"برای\s+همکاری\s*[،,]"),
    ("context", r"چرا\s+همکاری\s+با\s+ما\s*[؟?]"),
    (
        "work_duty",
        r"(?:Main\s+)?Responsibilities\s*:",
    ),
    (
        "candidate_qualification",
        r"(?:Required\s+)?(?:Qualifications|Requirements)\s*:",
    ),
    (
        "preferred",
        r"Preferred\s+Qualifications\s*:",
    ),
    (
        "benefit",
        r"Benefits\s*:",
    ),
)
_HEADING_RE = re.compile(
    "|".join(
        f"(?P<h{i}>(?<!\\w)(?:{pattern}))" for i, (_, pattern) in enumerate(_HEADING_PATTERNS)
    ),
    re.I,
)
_BULLET_RE = re.compile(r"[•●▪◦]|(?<!\w)-(?=\s)", re.U)
_SENTENCE_RE = re.compile(r"(?<=[.!؟؛])\s+(?=\S)")
_PREFERENCE = re.compile(
    r"مزیت\s+محسوب\s+می[‌\s]*شو(?:د|ند)|مزیت\s+دارد|"
    r"الزامی\s+نیست|اجباری\s+نیست|ضروری\s+نیست|"
    r"(?:not\s+(?:strictly\s+)?mandatory|not\s+required|preferred|an?\s+advantage)",
    re.I,
)
_POSITIVE_PREFERENCE = re.compile(r"مزیت\s+محسوب|مزیت\s+دارد|preferred|an?\s+advantage", re.I)
_NEGATIVE = re.compile(
    r"(?:الزامی|اجباری|ضروری)\s+نیست|not\s+(?:strictly\s+)?mandatory|not\s+required",
    re.I,
)
_REQUIRED = re.compile(
    r"(?<!\w)(?:حداقل|الزامی\s+است|ضروری\s+است|باید|"
    r"must\s+have|required|mandatory)(?!\w)",
    re.I,
)
_QUALIFICATION_CUE = re.compile(
    r"^(?:آشنایی|تسلط|توانایی|مهارت|حداقل|دارا\s+بودن|داشتن|"
    r"گواهینامه|تجربه|سابقه|knowledge\s+of|ability\s+to)",
    re.I,
)
_BEHAVIOR = re.compile(
    r"^(?:روحیه|داشتن\s+روحیه|منظم|وظیفه\s*شناس|مسئولیت\s*پذیر|قابلیت\s+کار\s+تیمی|"
    r"مقید\s+به|هماهنگی\s+و|علاقه\s*مند)",
    re.I,
)
_ARRANGEMENT = re.compile(
    r"(?:امکان\s+دورکاری|"
    r"(?:کار|همکاری)\s+به\s+صورت\s+(?:هیبرید|تمام\s*وقت|پاره\s*وقت)|"
    r"(?:نوع\s+همکاری|محل\s+کار)\s*:|"
    r"remote\s+work\s+(?:available|possible))",
    re.I,
)
_COMPENSATION = re.compile(r"^(?:حقوق\s*(?:[:：]|از)|salary\s*(?:[:：]|from))", re.I)
_TRACK = re.compile(r"سطح\s+(Middle|Senior|میانی|ارشد)\s*[:：]", re.I)
_EQUIVALENT = re.compile(
    r"(?:گواهینامه\s+یا\s+دانش\s+معادل|certificate\s+or\s+equivalent\s+knowledge)", re.I
)
_OPTION = re.compile(r"یکی\s+از\s+حوزه[‌\s]*های\s+", re.I)
_WORK_START = re.compile(
    r"(?<!\w)(?:توسعه|پیاده[‌\s]*سازی|طراحی|مشارکت|تست|تهیه|"
    r"عیب[‌\s]*یابی|پشتیبانی|اتصال|مدیریت|بهینه[‌\s]*سازی)(?=\s|‌)",
    re.I,
)
_QUAL_START = re.compile(
    r"(?<!\w)(?:آشنایی|تسلط|توانایی|داشتن|دارا\s+بودن|"
    r"روحیه|امکان\s+دورکاری|منظم|قابلیت\s+کار|"
    r"مقید\s+به|هماهنگی\s+و|علاقه[‌\s]*مند)(?=\s|‌|،)",
    re.I,
)
_TECH_CONCEPTS = ("Python", "LLM", "RAG", "API", "EDR", "Docker", "Kubernetes")
_BOARD_FIELDS = (
    "skills",
    "minimum_experience",
    "education",
    "employment_type",
    "salary",
    "location",
    "job_category",
    "gender",
    "military_service",
)


def _digest(data: Any) -> str:
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _trim(text: str, a: int, b: int) -> tuple[int, int]:
    while a < b and text[a].isspace():
        a += 1
    while b > a and text[b - 1].isspace():
        b -= 1
    return a, b


@dataclass(frozen=True, slots=True)
class SourceItemCandidate:
    anchor: OriginalSourceAnchor
    category: Category
    employer_strength: Strength
    evidence_basis: str
    heading: str | None
    qualifier: str
    interpretation_status: str = "candidate_unreviewed"


@dataclass(frozen=True, slots=True)
class BoardValueCandidate:
    field_path: str
    selector: str
    field_json_sha256: str
    value_json_sha256: str
    value: Any
    classification: str  # metadata, skill_tag, possible_page_copy


@dataclass(frozen=True, slots=True)
class DiagnosticSignal:
    kind: str
    source_anchor_id: str | None
    board_selector: str | None
    interpretation: str


@dataclass(frozen=True, slots=True)
class AlternativePathCandidate:
    source_anchor_ids: tuple[str, ...]
    kind: str
    logical_operator: str
    interpretation_status: str = "unreviewed"


@dataclass(frozen=True, slots=True)
class WorkCapabilityCandidate:
    source_anchor_id: str
    capability: str
    evidence_state: str = "strongly_implied_by_work_candidate"
    employer_prior_experience_required: bool | None = None


@dataclass(frozen=True, slots=True)
class B2SourceCandidate:
    contract_version: str
    source_job_id: str
    detail_version_id: int
    source_semantic_sha256: str
    source_field_sha256: str
    items: tuple[SourceItemCandidate, ...]
    board_values: tuple[BoardValueCandidate, ...]
    alternatives: tuple[AlternativePathCandidate, ...]
    signals: tuple[DiagnosticSignal, ...]
    work_capability_links: tuple[WorkCapabilityCandidate, ...]
    authority: str = "candidate_only_no_downstream_reuse"


def _heading_sections(description: str) -> list[tuple[int, int, str, str | None]]:
    headings = list(_HEADING_RE.finditer(description))
    if not headings:
        return [(0, len(description), "unresolved", None)]
    output = [(0, headings[0].start(), "context", None)]
    for index, head in enumerate(headings):
        group = next(i for i in range(len(_HEADING_PATTERNS)) if head.group(f"h{i}") is not None)
        end = headings[index + 1].start() if index + 1 < len(headings) else len(description)
        kind = _HEADING_PATTERNS[group][0]
        output.append((head.end(), end, kind, head.group()))
    return output


def _split_units(text: str, start: int, end: int, section: str) -> list[tuple[int, int]]:
    """Split only at explicit markers and conservative source-visible cues."""
    cuts = {start, end}
    for marker in _BULLET_RE.finditer(text, start, end):
        cuts.update((marker.start(), marker.end()))
    for gap in _SENTENCE_RE.finditer(text, start, end):
        cuts.update((gap.start(), gap.end()))
    # The Jobinja parsed description can flatten each list into one line.
    # In that case recognizable list-entry openings can be *candidate* cuts.
    cues = (
        _WORK_START
        if section == "work_duty"
        else (_QUAL_START if section in {"candidate_qualification", "preferred"} else None)
    )
    if cues is not None:
        for match in cues.finditer(text, start, end):
            at = match.start()
            left = text[max(start, at - 20) : at].rstrip()
            # Do not split coordinated actions or governed qualification phrases.
            if left.endswith(("و", "در", "به", "با", "از", "یکی", "داشتن", "به همراه", "شامل")):
                continue
            if at - start >= 22:
                cuts.add(at)
    ordered = sorted(cuts)
    result = []
    for a, b in zip(ordered, ordered[1:], strict=False):
        a, b = _trim(text, a, b)
        if a < b and text[a:b] not in ("•", "●", "▪", "◦", "-"):
            result.append((a, b))
    return result


def _classify(text: str, section: str, heading: str | None) -> tuple[Category, Strength, str, str]:
    line = text.strip()
    if not line:
        return "unresolved", "unresolved", "unresolved", "unresolved"
    if _ARRANGEMENT.search(line) and (
        line.startswith(("امکان", "کار به صورت", "همکاری به صورت", "نوع همکاری", "محل کار"))
        or section == "work_arrangement"
    ):
        return "work_arrangement", "not_applicable", "explicit_original_wording", "not_applicable"
    if line.startswith(("پذیرش نهایی", "ارسال رزومه")):
        return (
            "application_instruction",
            "not_applicable",
            "explicit_original_wording",
            "not_applicable",
        )
    if _COMPENSATION.search(line) or section == "compensation":
        return "compensation", "not_applicable", "explicit_original_wording", "not_applicable"
    if section == "benefit":
        return "benefit", "not_applicable", "original_section_context", "not_applicable"
    if section == "application_instruction":
        return (
            "application_instruction",
            "not_applicable",
            "original_section_context",
            "not_applicable",
        )
    if section == "context":
        return "context", "not_applicable", "original_section_context", "not_applicable"

    pref = bool(_PREFERENCE.search(line))
    # Optional wording like "not required" contains the word "required".
    # Check actual required cues after removing preference/negative cues.
    required = bool(_REQUIRED.search(_PREFERENCE.sub(" ", line)))
    mixed = pref and required
    if mixed and (
        section in {"candidate_qualification", "preferred"} or _QUALIFICATION_CUE.match(line)
    ):
        return "candidate_qualification", "unresolved", "unresolved", "unresolved"
    if _BEHAVIOR.search(line):
        if pref:
            return (
                "behavioral_expectation",
                "preferred" if _POSITIVE_PREFERENCE.search(line) else "unresolved",
                "explicit_original_wording",
                "negative_explicit" if _NEGATIVE.search(line) else "positive_explicit",
            )
        return (
            "behavioral_expectation",
            "stated_expectation",
            "original_section_context",
            "unresolved",
        )
    if section == "work_duty" and not _QUALIFICATION_CUE.match(line):
        # A generic vacancy-introduction sentence under a "job description"
        # heading is not necessarily an employee's assigned responsibility.
        if line.startswith(("شرکت ", "ما در ", "We are hiring", "Our company")):
            return "context", "not_applicable", "original_section_context", "not_applicable"
        return "work_duty", "not_applicable", "original_section_context", "not_applicable"
    if section in {"candidate_qualification", "preferred"} or _QUALIFICATION_CUE.match(line):
        if pref:
            # Negative-only evidence establishes non-mandatory, not necessarily preferred.
            return (
                "candidate_qualification",
                "preferred" if _POSITIVE_PREFERENCE.search(line) else "unresolved",
                "explicit_original_wording",
                "negative_explicit" if _NEGATIVE.search(line) else "positive_explicit",
            )
        if required:
            return (
                "candidate_qualification",
                "required",
                "explicit_original_wording",
                "positive_explicit",
            )
        if section == "preferred":
            return (
                "candidate_qualification",
                "preferred",
                "original_section_context",
                "positive_explicit",
            )
        # Inherited heading and a capability cue support a requirement *candidate*,
        # but no forced employer-required label for bare nouns/unclear examples.
        if (
            re.match(r"^(?:تسلط|آشنایی|توانایی|دارا\s+بودن|حداقل|داشتن)\b", line)
            and heading
            and any(w in heading for w in ("نیازمندی", "تخصصی", "احراز", "مورد نیاز"))
        ):
            return "candidate_qualification", "required", "original_section_context", "unresolved"
        return "candidate_qualification", "unresolved", "unresolved", "unresolved"
    if section == "work_arrangement":
        return "work_arrangement", "not_applicable", "original_section_context", "not_applicable"
    return "unresolved", "unresolved", "unresolved", "unresolved"


def _board_values(source: TranslationSourceVersion) -> tuple[BoardValueCandidate, ...]:
    result: list[BoardValueCandidate] = []
    for name in _BOARD_FIELDS:
        if name not in source.fields or source.fields[name] is None:
            continue
        field = source.fields[name]
        for index, value in enumerate(field) if isinstance(field, list) else ((None, field),):
            if not isinstance(value, (str, int, float, bool)):
                continue
            selector = f"/{name}" + (f"/{index}" if index is not None else "")
            copy = (
                name == "skills"
                and isinstance(value, str)
                and (
                    len(value) > 160
                    or any(
                        cue in value
                        for cue in ("شرایط احراز", "شرایط کاری", "مزیت محسوب", "ثبت آگهی")
                    )
                )
            )
            result.append(
                BoardValueCandidate(
                    field_path=name,
                    selector=selector,
                    field_json_sha256=_digest(field),
                    value_json_sha256=_digest(value),
                    value=value,
                    classification="possible_page_copy"
                    if copy
                    else ("skill_tag" if name == "skills" else "metadata"),
                )
            )
    return tuple(result)


def _concept_in(text: str, term: str) -> bool:
    # Literal matching is only evidence of a mention, not a normalized ontology.
    return bool(re.search(r"(?<![a-zA-Z])" + re.escape(term) + r"s?(?![a-zA-Z])", text, re.I))


def interpret_original_source_candidate(source: TranslationSourceVersion) -> B2SourceCandidate:
    """Pure, non-production source candidate. Does not assert semantic acceptance."""
    text = source.fields.get("description")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("B2 needs a nonempty parsed original description")
    # Use Stage A to validate source version and original field semantics.
    full = bind_original_source_span(source, char_start=0, char_end=len(text))
    verify_original_source_anchor(full, source)
    units: list[SourceItemCandidate] = []
    for start, end, section, heading in _heading_sections(text):
        for a, b in _split_units(text, start, end, section):
            anchor = bind_original_source_span(source, char_start=a, char_end=b)
            category, strength, basis, qualifier = _classify(anchor.exact_text, section, heading)
            units.append(
                SourceItemCandidate(
                    anchor=anchor,
                    category=category,
                    employer_strength=strength,
                    evidence_basis=basis,
                    qualifier=qualifier,
                    heading=heading,
                )
            )
    boards = _board_values(source)
    signals: list[DiagnosticSignal] = []
    for board in boards:
        if board.classification == "possible_page_copy":
            signals.append(
                DiagnosticSignal(
                    "possible_page_copy_in_board_skills",
                    None,
                    board.selector,
                    "Board field contains a long/section-like phrase, not verified as one skill",
                )
            )
        if board.classification != "skill_tag" or not isinstance(board.value, str):
            continue
        for unit in units:
            if (
                unit.category == "candidate_qualification"
                and unit.employer_strength == "preferred"
                and _concept_in(unit.anchor.exact_text, board.value.strip())
                and len(board.value) <= 48
            ):
                signals.append(
                    DiagnosticSignal(
                        "board_skill_tag_vs_preferred_prose",
                        unit.anchor.anchor_id,
                        board.selector,
                        "Board skill tag does not override original optional employer wording",
                    )
                )
                break

    # A structured board value can be narrower than the employer's stated
    # alternatives. Signal the potential loss of scope; it is NOT a proven
    # contradiction or an authorization to overwrite either source.
    for board in boards:
        if board.field_path != "employment_type" or not isinstance(board.value, str):
            continue
        normalized_tag = re.sub(r"[\s‌]+", "", board.value).casefold()
        for unit in units:
            if unit.category != "work_arrangement":
                continue
            original = re.sub(r"[\s‌]+", "", unit.anchor.exact_text).casefold()
            if normalized_tag and normalized_tag in original and "یا" in original:
                signals.append(
                    DiagnosticSignal(
                        "board_employment_mode_may_hide_prose_alternative",
                        unit.anchor.anchor_id,
                        board.selector,
                        "Board employment value may omit a source-stated work-mode alternative",
                    )
                )
                break

    hints: list[WorkCapabilityCandidate] = []
    for unit in units:
        if unit.category != "work_duty":
            continue
        for concept in _TECH_CONCEPTS:
            if _concept_in(unit.anchor.exact_text, concept):
                hints.append(
                    WorkCapabilityCandidate(
                        source_anchor_id=unit.anchor.anchor_id,
                        capability=concept,
                    )
                )
    alternatives: list[AlternativePathCandidate] = []
    # Preserve original alternatives as candidate groups, without fabricating a
    # globally mandatory skill list or forcing item-level Boolean execution.
    track_refs: list[str] = []
    for unit in units:
        if (
            unit.category == "candidate_qualification"
            and unit.heading
            and _TRACK.search(unit.heading)
        ):
            track_refs.append(unit.anchor.anchor_id)
    if len(track_refs) >= 2:
        alternatives.append(
            AlternativePathCandidate(
                source_anchor_ids=tuple(dict.fromkeys(track_refs)),
                kind="seniority_tracks",
                logical_operator="any_of",
            )
        )
    for unit in units:
        if unit.category != "candidate_qualification":
            continue
        if _EQUIVALENT.search(unit.anchor.exact_text):
            alternatives.append(
                AlternativePathCandidate(
                    source_anchor_ids=(unit.anchor.anchor_id,),
                    kind="certificate_or_equivalent_knowledge",
                    logical_operator="any_of_within_source_clause",
                )
            )
        elif _OPTION.search(unit.anchor.exact_text):
            alternatives.append(
                AlternativePathCandidate(
                    source_anchor_ids=(unit.anchor.anchor_id,),
                    kind="one_of_technical_domains",
                    logical_operator="any_of_within_source_clause",
                )
            )
    if any(group.kind == "seniority_tracks" for group in alternatives):
        for board in boards:
            if board.field_path == "minimum_experience":
                signals.append(
                    DiagnosticSignal(
                        "board_experience_range_may_hide_seniority_alternatives",
                        track_refs[0],
                        board.selector,
                        "Board experience summary cannot substitute for source-alternative paths",
                    )
                )
                break
    return B2SourceCandidate(
        contract_version=B2_SOURCE_CANDIDATE_CONTRACT,
        source_job_id=source.source_job_id,
        detail_version_id=source.job_detail_version_id,
        source_semantic_sha256=source.semantic_sha256,
        source_field_sha256=full.field_sha256,
        items=tuple(units),
        board_values=boards,
        alternatives=tuple(alternatives),
        signals=tuple(signals),
        work_capability_links=tuple(hints),
    )


def verify_b2_candidate(candidate: B2SourceCandidate, source: TranslationSourceVersion) -> None:
    """Integrity fence only; classification truth requires separate evaluation."""
    if (
        candidate.contract_version != B2_SOURCE_CANDIDATE_CONTRACT
        or candidate.authority != "candidate_only_no_downstream_reuse"
        or candidate.source_job_id != source.source_job_id
        or candidate.detail_version_id != source.job_detail_version_id
        or candidate.source_semantic_sha256 != source.semantic_sha256
    ):
        raise ValueError("B2 candidate identity or authority mismatch")
    description = source.fields.get("description")
    if not isinstance(description, str):
        raise ValueError("Missing original source")
    if candidate.source_field_sha256 != hashlib.sha256(description.encode("utf-8")).hexdigest():
        raise ValueError("Stale original source field")
    ids = set()
    for item in candidate.items:
        verify_original_source_anchor(item.anchor, source)
        if item.anchor.anchor_id in ids:
            raise ValueError("Duplicate original source item")
        ids.add(item.anchor.anchor_id)
        if item.employer_strength == "required" and item.category != "candidate_qualification":
            raise ValueError("Invalid category for employer-required candidate")
        if item.employer_strength == "required" and item.evidence_basis not in {
            "explicit_original_wording",
            "original_section_context",
        }:
            raise ValueError("Unproven required employer condition")
    for board in candidate.board_values:
        field = source.fields[board.field_path]
        selector = board.selector
        expected = f"/{board.field_path}"
        if not (selector == expected or selector.startswith(expected + "/")):
            raise ValueError("Board selector is not under its field")
        if _digest(field) != board.field_json_sha256:
            raise ValueError("Stale board field")
        if isinstance(field, list):
            _, _, ix = selector.rpartition("/")
            if not ix.isascii() or not ix.isdecimal() or str(int(ix)) != ix:
                raise ValueError("Invalid board array selector")
            value = field[int(ix)]
        elif selector == expected:
            value = field
        else:
            raise ValueError("Bad scalar board selector")
        if _digest(value) != board.value_json_sha256 or value != board.value:
            raise ValueError("Stale or tampered selected board value")
    for hint in candidate.work_capability_links:
        if hint.source_anchor_id not in ids:
            raise ValueError("Capability hint not linked to a source item")
        if hint.employer_prior_experience_required is not None:
            raise ValueError("Work-implied capability cannot establish employer experience policy")
    for group in candidate.alternatives:
        if not set(group.source_anchor_ids) <= ids:
            raise ValueError("Alternative refers to unknown source item")
    for signal in candidate.signals:
        if signal.source_anchor_id is not None and signal.source_anchor_id not in ids:
            raise ValueError("Signal refers to unknown source item")
        if signal.board_selector is not None and not any(
            b.selector == signal.board_selector for b in candidate.board_values
        ):
            raise ValueError("Signal refers to unknown board field")


__all__ = [
    "B2_SOURCE_CANDIDATE_CONTRACT",
    "B2SourceCandidate",
    "SourceItemCandidate",
    "BoardValueCandidate",
    "DiagnosticSignal",
    "AlternativePathCandidate",
    "WorkCapabilityCandidate",
    "interpret_original_source_candidate",
    "verify_b2_candidate",
]
