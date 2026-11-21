"""Versioned, non-authoritative B2 source-structure candidate for exposed regressions.

The original B2 parser is deliberately immutable: B2/B3/B4 frozen milestones
replay with their original byte-identical candidate output. This sidecar uses
general bilingual heading and exact-source cue handling to test a successor
candidate, without changing production, B1 contracts, source versioning, model
prompts or any approved employer-fact authority.

Semantic labels remain hypotheses. An employer duty may imply a capability,
but cannot by itself establish a mandatory prior-employment requirement.
"""

from __future__ import annotations

import re
from dataclasses import replace

from jobhunter.source_eligibility_candidate_b2 import (
    EligibilityLogicResult,
    build_candidate_eligibility_logic,
)
from jobhunter.source_item_candidate_b2 import (
    _EQUIVALENT,
    _OPTION,
    _TECH_CONCEPTS,
    _TRACK,
    AlternativePathCandidate,
    B2SourceCandidate,
    DiagnosticSignal,
    SourceItemCandidate,
    WorkCapabilityCandidate,
    _classify,
    _concept_in,
    _heading_sections,
    _salary_values_materially_differ,
    _split_units,
    _trim,
    interpret_original_source_candidate,
    verify_b2_candidate,
)
from jobhunter.source_span_identity import bind_original_source_span
from jobhunter.translation_store import TranslationSourceVersion

B2V2_ENGINE = "jobhunter-p16-b2-source-structure-exposed-candidate-v2"

# These patterns describe *source document sections*, not mandatory skill names
# or rules tied to a particular employer, vacancy ID, or tool.
# Use the longest/specific phrase before any shorter historic heading.
_SECTION_PATTERNS: tuple[tuple[str, str], ...] = (
    ("work_duty", r"مسئولیت[‌\s]*های\s+(?:کلیدی|اصلی)\s*[:：]?"),
    ("work_duty", r"مسئولیت[‌\s]*ها\s*[:：]"),
    ("candidate_qualification", r"مهارت[‌\s]*ها\s+و\s+الزامات\s+فنی\s*[:：]"),
    ("candidate_qualification", r"دانش\s+و\s+مهارت[‌\s]*های\s+مورد\s+نیاز\s*[:：]?"),
    ("candidate_qualification", r"حوزه[‌\s]*های\s+تخصصی\s+و\s+مهارت[‌\s]*های\s+مورد\s*نیاز\s*[:：]?"),
    ("candidate_qualification", r"مهارت[‌\s]*های\s+مشترک\s+مورد\s+انتظار\s*[:：]?"),
    ("candidate_qualification", r"شرایط\s+و\s+الزامات\s*[:：]?"),
    ("candidate_qualification", r"سابقه\s+و\s+تجربه\s+کاری\s*[:：]?"),
    ("preferred", r"مهارت[‌\s]*های\s+زیر\s+امتیاز\s+محسوب\s+می[‌\s]*شو(?:د|ند)\s*[:：]?"),
    ("preferred", r"مزیت\s+محسوب\s+می[‌\s]*شود\s+اگر\s*[:：]?"),
    ("benefit", r"مزایای\s+همکاری\s+با\s+ما\s*[:：]?"),
    ("context", r"نکته\s+مهم\s+جذب\s+نیرو\s*[:：]?"),
    ("work_duty", r"What\s+You['’]ll\s+Work\s+On\s*[:：]?"),
    ("candidate_qualification", r"What\s+Makes\s+You\s+a\s+Great\s+Fit\s*[:：]?"),
    ("candidate_qualification", r"Technical\s+Skills\s*&\s*Requirements\s*[:：]?"),
    ("candidate_qualification", r"System\s+Design\s*&\s*Architecture\s*[:：]?"),
    ("candidate_qualification", r"AI-Assisted\s+Software\s+Development\s*[:：]?"),
    ("candidate_qualification", r"Professional\s+Requirements\s*[:：]?"),
    ("application_instruction", r"System\s+Design\s+Assessment\s*[:：]?"),
    ("work_arrangement", r"Working\s+Conditions\s*&\s*Benefits\s*[:：]?"),
    ("preferred", r"Nice\s+to\s+Have\s*[:：]?"),
    ("preferred", r"Bonus\s+Points\s*[:：]?"),
    ("benefit", r"What\s+You['’]ll\s+Get\s*[:：]?"),
    ("context", r"About\s+Us\s*[:：]?"),
    ("context", r"Built\s+for\s+Builders\s*[:：]?"),
)

_NEW_HEADING = re.compile(
    "|".join(
        f"(?P<new{i}>(?<!\\w)(?:{pattern}))" for i, (_, pattern) in enumerate(_SECTION_PATTERNS)
    ),
    re.I,
)
# Original B2 headings are retained for known exposed cases. New headings take
# precedence when they overlap, avoiding double-cutting and empty phantom items.
_EXTRA_SENTENCE_GAP = re.compile(r"(?<=[.!?])(?=[A-Z][a-z])")
# Flattened HTML often erases the original list structure. Split on a
# source-visible bullet, not on a verb occurring inside a governed phrase.
_PERSIAN_ITEM_START = re.compile(
    r"(?<!\w)(?:ساخت|نوشتن|همکاری|استقرار|تجربه|سابقه|تسلط|آشنایی|توانایی)"
    r"(?=\s|‌)",
    re.I,
)
_SOURCE_BULLETS = re.compile(r"[•●▪◦·]|(?<!\w)-(?=\s)")
_SENTENCE_BREAKS = re.compile(r"(?<=[.!؟؛])\s+(?=\S)")
_WORK_BEGINS = re.compile(
    r"(?<!\w)(?:توسعه|پیاده[‌\s]*سازی|طراحی|مشارکت|تست|تهیه|"
    r"عیب[‌\s]*یابی|پشتیبانی|اتصال|مدیریت|بهینه[‌\s]*سازی)"
    r"(?=\s|‌)",
    re.I,
)
_QUAL_BEGINS = re.compile(
    r"(?<!\w)(?:آشنایی|تسلط|توانایی|داشتن|دارا\s+بودن|"
    r"روحیه|امکان\s+دورکاری|منظم|قابلیت\s+کار|"
    r"مقید\s+به|هماهنگی\s+و|علاقه[‌\s]*مند|تجربه|سابقه)"
    r"(?=\s|‌|،)",
    re.I,
)
_QUALIFICATION_OPEN = re.compile(r"^(?:تجربه|سابقه|آشنایی|تسلط|توانایی|داشتن|دارا\s+بودن)\b", re.I)
_INNER_BONUS = re.compile(
    r"(?:ترجیحاً|ترجیحا|امتیاز\s+ویژه[‌ای]*\s+محسوب\s+می[‌\s]*شود|"
    r"\b(?:bonus|nice\s+to\s+have)\b)",
    re.I,
)
_NO_PRIOR_REQUIREMENT = re.compile(r"\bno\s+[^.]{1,145}\s+(?:required|necessary)\b", re.I)
# Explicit scope negation + one-or-more choice + separately recruited specialties.
# We deliberately do not construct a validated Boolean graph from only this cue.
_NOT_ALL = re.compile(
    r"(?:لازم\s+نیست|الزامی\s+نیست|ضروری\s+نیست)"
    r"[^.؛]{0,180}?(?:تمام|همه)[^.؛]{0,120}?(?:تخصص|تسلط|حوزه)",
    re.I,
)
_ONE_OR_MORE = re.compile(r"یک\s+یا\s+چند\s+حوزه[‌\s]*", re.I)
_SEPARATELY = re.compile(r"(?:به[‌\s]*صورت\s+مجزا|جداگانه)", re.I)


def _heading_sections_v2(text: str) -> list[tuple[int, int, str, str | None]]:
    """Preserve raw character offsets while merging generic original/new headings."""
    old = _heading_sections(text)
    old_headings = [
        (start - len(heading), start, section, heading)
        for start, _end, section, heading in old
        if heading is not None
    ]
    # The baseline _heading_sections uses head.end(); derive actual offsets by
    # searching the immediate leading text rather than a content string match.
    if any(text[start:end] != heading for start, end, _sec, heading in old_headings):
        raise ValueError("Historical B2 heading identity drift")
    new_headings: list[tuple[int, int, str, str]] = []
    for match in _NEW_HEADING.finditer(text):
        index = next(i for i in range(len(_SECTION_PATTERNS)) if match.group(f"new{i}") is not None)
        new_headings.append(
            (match.start(), match.end(), _SECTION_PATTERNS[index][0], match.group())
        )
    # Prefer new, more specific headings where an original heading overlaps.
    merged = list(new_headings)
    for old_item in old_headings:
        if not any(old_item[0] < b and old_item[1] > a for a, b, _, _ in new_headings):
            merged.append(old_item)
    merged.sort(key=lambda e: (e[0], e[1]))
    if not merged:
        return [(0, len(text), "unresolved", None)]
    result: list[tuple[int, int, str, str | None]] = []
    if merged[0][0] > 0:
        result.append((0, merged[0][0], "context", None))
    for i, (_a, b, sec, header) in enumerate(merged):
        end = merged[i + 1][0] if i + 1 < len(merged) else len(text)
        if b < end:
            result.append((b, end, sec, header))
    return result


def _split_units_v2(text: str, start: int, end: int, section: str) -> list[tuple[int, int]]:
    """Split at visible bullets/sentences and only safe, ungoverned list cues.

    Do not separate 'experience in design, implementation ...' or
    'log analysis for identifying threats' at an internal verbal noun. Exact
    offset and original wording are preserved; the semantic label stays candidate.
    """
    fixed_cuts = {start, end}
    for marker in _SOURCE_BULLETS.finditer(text, start, end):
        fixed_cuts.update((marker.start(), marker.end()))
    for gap in _SENTENCE_BREAKS.finditer(text, start, end):
        fixed_cuts.update((gap.start(), gap.end()))
    for gap in _EXTRA_SENTENCE_GAP.finditer(text, start, end):
        fixed_cuts.add(gap.start())
    result: list[tuple[int, int]] = []
    if section in {"benefit", "context", "work_arrangement"}:
        # Work locations or explicitly optional remote arrangements can follow
        # an unpunctuated benefits list in flattened source HTML.
        for marker in re.finditer(
            r"(?<!\w)(?:محل\s+کار\s+|Remote\s+Work:|Relocation\s+Support:)", text[start:end], re.I
        ):
            if marker.start() > 0:
                fixed_cuts.add(start + marker.start())
    for segment_start, segment_end in zip(sorted(fixed_cuts), sorted(fixed_cuts)[1:], strict=False):
        segment_start, segment_end = _trim(text, segment_start, segment_end)
        if segment_start >= segment_end or text[segment_start:segment_end] in (
            "•",
            "●",
            "▪",
            "◦",
            "·",
            "-",
        ):
            continue
        cuts = {segment_start, segment_end}
        if section in {"work_duty", "candidate_qualification", "preferred"}:
            # A qualification starting with 'experience ...' governs its
            # internal verbs; avoid inventing separate assigned work.
            cue_patterns = (
                (_QUAL_BEGINS, _PERSIAN_ITEM_START)
                if section == "preferred"
                else (
                    (_WORK_BEGINS, _QUAL_BEGINS, _PERSIAN_ITEM_START)
                    if section == "work_duty"
                    else (_QUAL_BEGINS, _PERSIAN_ITEM_START)
                )
            )
            matches = sorted(
                {
                    m.start(): m.group()
                    for pattern in cue_patterns
                    for m in pattern.finditer(text, segment_start, segment_end)
                }.items()
            )
            currently_qualified = bool(_QUALIFICATION_OPEN.match(text[segment_start:segment_end]))
            for at, match_text in matches:
                if at - segment_start < 22:
                    continue
                left = text[max(segment_start, at - 25) : at].strip()
                if left.endswith(
                    (
                        "و",
                        "در",
                        "با",
                        "از",
                        "به",
                        "برای",
                        "شامل",
                        "منظور",
                        "طراحی،",
                        "مکانیزم‌های",
                        "سازوکارهای",
                    )
                ):
                    continue
                is_qualification = bool(_QUAL_BEGINS.fullmatch(match_text))
                if currently_qualified and not is_qualification:
                    # A list that opens with "Experience designing, implementing"
                    # must remain one qualification. A later independently
                    # phrased "Design/build ..." duty must still be recognized.
                    last_cut = max(c for c in cuts if c < at)
                    prefix = text[last_cut:at].strip()
                    governed_phrase = bool(
                        re.match(r"^(?:تجربه|سابقه)\b", prefix, re.I)
                        and re.search(r"(?<!\w)(?:در|از|با)(?!\w)", prefix)
                    )
                    if governed_phrase:
                        continue
                # A new qualification entry can end a previous qualification;
                # a new work item can end a work item. Do not impose exclusivity
                # on the underlying capability relationships.
                cuts.add(at)
                currently_qualified = is_qualification
        pieces = sorted(cuts)
        for a, b in zip(pieces, pieces[1:], strict=False):
            a, b = _trim(text, a, b)
            if a < b:
                result.append((a, b))
    return result


def _classify_v2(exact: str, section: str, heading: str | None) -> tuple[str, str, str, str]:
    """Prevent required coercion when explicit optional/negative evidence exists."""
    line = exact.strip()
    if line.startswith(
        (
            "Remote Work:",
            "Relocation Support:",
            "Working Days:",
            "Working Hours:",
            "Employment Type:",
            "Thursday:",
            "محل کار:",
            "محل کار ",
        )
    ) and section in {"benefit", "work_arrangement", "preferred", "context"}:
        return "work_arrangement", "not_applicable", "explicit_original_wording", "not_applicable"
    # Interpersonal traits remain distinct from technical qualifications,
    # without preventing useful links between job duties and capabilities.
    if re.match(
        r"^(?:علاقه[‌\s]*مند\s+به|توانایی\s+کار\s+تیمی|"
        r"روحیه\s+(?:کنجکاوی|همکاری|تیمی))(?=\s|،|$)",
        line,
        re.I,
    ):
        return (
            "behavioral_expectation",
            "stated_expectation",
            "explicit_original_wording",
            "unresolved",
        )
    if _NO_PRIOR_REQUIREMENT.search(line):
        if section in {"candidate_qualification", "preferred"}:
            return (
                "candidate_qualification",
                "unresolved",
                "explicit_original_wording",
                "negative_explicit",
            )
        return "unresolved", "unresolved", "explicit_original_wording", "negative_explicit"
    if (
        _INNER_BONUS.search(line)
        and section in {"candidate_qualification", "preferred", "work_duty"}
        and re.search(r"(?:ترجیحاً|ترجیحا|امتیاز\s+ویژه)", line, re.I)
    ):
        return (
            "candidate_qualification",
            "preferred",
            "explicit_original_wording",
            "positive_explicit",
        )
    # English "No research publications ... required" should not accidentally
    # become a duty or a mandatory requirement, even when an old heading is broad.
    return _classify(line, section, heading)


def _candidate_alternatives(
    source: TranslationSourceVersion, units: list[SourceItemCandidate]
) -> tuple[AlternativePathCandidate, ...]:
    alternatives: list[AlternativePathCandidate] = []
    track_refs = [
        item.anchor.anchor_id
        for item in units
        if item.category == "candidate_qualification"
        and item.heading
        and _TRACK.search(item.heading)
    ]
    if len(track_refs) >= 2:
        alternatives.append(
            AlternativePathCandidate(
                source_anchor_ids=tuple(dict.fromkeys(track_refs)),
                kind="seniority_tracks",
                logical_operator="any_of",
            )
        )
    for item in units:
        if item.category != "candidate_qualification":
            continue
        if _EQUIVALENT.search(item.anchor.exact_text):
            alternatives.append(
                AlternativePathCandidate(
                    source_anchor_ids=(item.anchor.anchor_id,),
                    kind="certificate_or_equivalent_knowledge",
                    logical_operator="any_of_within_source_clause",
                )
            )
        elif _OPTION.search(item.anchor.exact_text):
            alternatives.append(
                AlternativePathCandidate(
                    source_anchor_ids=(item.anchor.anchor_id,),
                    kind="one_of_technical_domains",
                    logical_operator="any_of_within_source_clause",
                )
            )
    text = source.fields["description"]
    # Do not say that every listed track is necessary when the original
    # explicitly says that one or more separately recruited specialties suffice.
    # An exact source group warns about OR scope, not automatically an applicant
    # eligibility tree: individual specialty boundaries are still unverified.
    all_not = _NOT_ALL.search(text)
    one_or_more = _ONE_OR_MORE.search(text)
    separate = _SEPARATELY.search(text)
    if all_not and one_or_more and separate:
        matching = [
            unit.anchor.anchor_id
            for unit in units
            if any(
                unit.anchor.char_start <= at < unit.anchor.char_end
                for at in (all_not.start(), one_or_more.start(), separate.start())
            )
        ]
        if matching:
            alternatives.append(
                AlternativePathCandidate(
                    source_anchor_ids=tuple(dict.fromkeys(matching)),
                    kind="one_or_more_separately_hired_specialties",
                    logical_operator="any_of_unresolved_option_boundaries",
                    interpretation_status="candidate_unreviewed_not_eligibility_authority",
                )
            )
    return tuple(alternatives)


def interpret_original_source_candidate_v2(source: TranslationSourceVersion) -> B2SourceCandidate:
    """Return candidate-only structure with original B2 dataclasses/authority.

    Existing B2 code and frozen model/prompt outputs are untouched.
    """
    historical = interpret_original_source_candidate(source)
    text = source.fields["description"]
    units = []
    for start, end, section, heading in _heading_sections_v2(text):
        # Explicit nested seniority tracks are compound eligibility paths;
        # do not split their required-years conjunction into fragments.
        spans = (
            _split_units(text, start, end, section)
            if heading and _TRACK.search(heading)
            else _split_units_v2(text, start, end, section)
        )
        for a, b in spans:
            anchor = bind_original_source_span(source, char_start=a, char_end=b)
            category, strength, basis, qualifier = _classify_v2(anchor.exact_text, section, heading)
            units.append(
                SourceItemCandidate(
                    anchor=anchor,
                    category=category,
                    employer_strength=strength,
                    evidence_basis=basis,
                    heading=heading,
                    qualifier=qualifier,
                )
            )
    ids = {x.anchor.anchor_id for x in units}
    if not units or len(ids) != len(units):
        raise ValueError("Source-item segmentation missing or duplicate exact anchors")
    hints = [
        WorkCapabilityCandidate(source_anchor_id=item.anchor.anchor_id, capability=term)
        for item in units
        if item.category == "work_duty"
        for term in _TECH_CONCEPTS
        if _concept_in(item.anchor.exact_text, term)
    ]
    # Preserve only old diagnostic signals with source IDs surviving unchanged.
    signals = [
        s for s in historical.signals if s.source_anchor_id is None or s.source_anchor_id in ids
    ]
    # Re-emit simple optional metadata disagreement and salary mismatch against
    # the new units, never treat board tags as employer obligations.
    for board in historical.board_values:
        if (
            board.classification == "skill_tag"
            and isinstance(board.value, str)
            and len(board.value) <= 48
        ):
            for unit in units:
                if (
                    unit.category == "candidate_qualification"
                    and unit.employer_strength == "preferred"
                    and _concept_in(unit.anchor.exact_text, board.value.strip())
                ):
                    signals.append(
                        DiagnosticSignal(
                            "board_skill_tag_vs_preferred_prose",
                            unit.anchor.anchor_id,
                            board.selector,
                            "Board tag does not override employer optionality",
                        )
                    )
                    break
        if board.field_path == "salary" and isinstance(board.value, str):
            for unit in units:
                if unit.category == "compensation" and _salary_values_materially_differ(
                    board.value, unit.anchor.exact_text
                ):
                    signals.append(
                        DiagnosticSignal(
                            "board_prose_compensation_values_materially_differ",
                            unit.anchor.anchor_id,
                            board.selector,
                            "Values differ; preserve both sources without choosing a winner",
                        )
                    )
    distinct_signals = tuple(dict.fromkeys(signals))
    candidate = replace(
        historical,
        items=tuple(units),
        signals=distinct_signals,
        alternatives=_candidate_alternatives(source, units),
        work_capability_links=tuple(hints),
    )
    verify_b2_candidate(candidate, source)
    return candidate


def build_candidate_eligibility_logic_v2(
    source: TranslationSourceVersion, candidate: B2SourceCandidate
) -> EligibilityLogicResult:
    """Preserve proven B2 OR graphs and expose *unresolved* specialty choices.

    Never manufacture track nodes from a list of possible fields or tools.
    A source may explicitly say 'one or more specialties' while the precise
    track-specific qualifications remain unverified; the scope signal should
    survive without becoming a validated applicant-eligibility graph.
    """
    known = build_candidate_eligibility_logic(source, candidate)
    unresolved = list(known.unresolved_group_kinds)
    for group in candidate.alternatives:
        if group.kind == "one_or_more_separately_hired_specialties":
            unresolved.append(group.kind)
    return EligibilityLogicResult(
        graphs=known.graphs,
        unresolved_group_kinds=tuple(dict.fromkeys(unresolved)),
    )


__all__ = [
    "B2V2_ENGINE",
    "interpret_original_source_candidate_v2",
    "build_candidate_eligibility_logic_v2",
]
