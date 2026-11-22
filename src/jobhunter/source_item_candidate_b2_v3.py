"""Experimental B2v3 original-language structural recovery, *not employer authority*.

This is a compact, general bilingual heading/qualifier extension of B2v2.
It exists because two independent exposed cohorts prove narrow punctuation-
dependent deterministic sections fail on flattened ads. Old B2/v2 code,
English v30, B3 translation and accepted products are unchanged.

The output is an unreviewed candidate: original source anchors carry identity
but do not themselves establish semantic truth or mandatory qualifications.
"""

from __future__ import annotations

import re
from dataclasses import replace

from jobhunter.source_eligibility_candidate_b2 import EligibilityLogicResult
from jobhunter.source_item_candidate_b2 import (
    _TECH_CONCEPTS,
    _TRACK,
    AlternativePathCandidate,
    B2SourceCandidate,
    SourceItemCandidate,
    WorkCapabilityCandidate,
    _concept_in,
    _split_units,
    _trim,
    verify_b2_candidate,
)
from jobhunter.source_item_candidate_b2_v2 import (
    _candidate_alternatives,
    _classify_v2,
    _heading_sections_v2,
    _split_units_v2,
    build_candidate_eligibility_logic_v2,
    interpret_original_source_candidate_v2,
)
from jobhunter.source_span_identity import bind_original_source_span
from jobhunter.translation_store import TranslationSourceVersion

B2V3_ENGINE = "jobhunter-p16-b2-generic-original-section-candidate-v3"

# Headings are generic source-document structure, NOT employer-specific labels
# or a mandatory-qualification wordlist. Require recognizably complete phrases,
# including some flattened examples without punctuation.
_GENERAL_HEADINGS: tuple[tuple[str, str], ...] = (
    ("work_duty", r"شرح\s+وظایف\s+و\s+مسئولیت[‌\s]*ها(?=\s|[:：])"),
    ("work_duty", r"مسئولیت[‌\s]*ها(?=\s|[:：]|$)"),
    ("work_duty", r"وظایف\s+شغلی(?=\s|[:：]|$)"),
    ("candidate_qualification", r"شرایط\s+و\s+مهارت[‌\s]*های\s+ضروری(?=\s|[:：])"),
    ("candidate_qualification", r"مهارت[‌\s]*ها\s+و\s+توانمندی[‌\s]*های\s+مورد[‌\s]*نیاز(?=\s|[:：])"),
    ("candidate_qualification", r"شرایط\s+احراز\s+و\s+مهارت[‌\s]*های\s+تخصصی(?=\s|[:：])"),
    ("candidate_qualification", r"مهارت[‌\s]*های\s+ضروری(?=\s|[:：]|$)"),
    ("candidate_qualification", r"مهارت[‌\s]*های\s+مورد\s*نیاز(?=\s|[:：]|$)"),
    ("candidate_qualification", r"مهارت[‌\s]*های\s+مهم(?=\s|[:：]|$)"),
    ("candidate_qualification", r"مهارت[‌\s]*ها(?=\s+[۱۲۳۴۵۶۷۸۹0-9][).]|\s+[•●▪◦])"),
    ("preferred", r"مهارت[‌\s]*های\s+(?:ترجیحی|امتیازی)(?=\s|[:：]|$)"),
    (
        "preferred",
        r"داشتن\s+مدارک\s+بین[‌\s]*المللی\s+زیر\s+مزیت\s+محسوب\s+می[‌\s]*شود(?=\s|[:：]|$)",
    ),
    ("behavioral_expectation", r"مهارت[‌\s]*های\s+فردی(?=\s|[:：]|$)"),
    ("behavioral_expectation", r"شایستگی[‌\s]*های\s+(?:فردی|مورد\s*نیاز)(?=\s|[:：]|$)"),
    ("behavioral_expectation", r"ویژگی[‌\s]*های\s+حرفه[‌\s]*ای\s+مورد\s+انتظار(?=\s|[:：]|$)"),
    ("behavioral_expectation", r"ویژگی[‌\s]*ها(?=\s*[:：]|\s+[•●▪◦])"),
    ("context", r"شرح\s+موقعیت\s+شغلی(?=\s|[:：]|$)"),
    ("work_arrangement", r"ساعات\s+کاری(?:\s+مؤسسه|\s+موسسه)?(?=\s|[:：]|$)"),
    ("work_arrangement", r"موقعیت\s+مکانی(?=\s|[:：]|$)"),
    ("work_arrangement", r"محل\s+فعالیت(?=\s|[:：]|$)"),
    ("work_arrangement", r"محل\s+شرکت(?=\s|[:：]|$)"),
    ("work_arrangement", r"نکات\s+مهم(?=\s|[:：]|$)"),
    ("benefit", r"مزایای\s+همکاری\s+با\s+[^.،؛]{3,90}(?=\s+امکان|\s+کار|\s+محیط)"),
    ("benefit", r"شرایط\s+شغلی\s+شرکت(?=\s|[:：]|$)"),
    ("context", r"About\s+the\s+Role(?=\s|[:：]|$)"),
    ("work_duty", r"Core\s+Responsibilities(?=\s|[:：]|$)"),
    ("work_duty", r"Leadership\s*&\s*Governance(?=\s|[:：]|$)"),
    ("work_duty", r"Vulnerability\s+Assessment\s*&\s*Penetration\s+Testing(?=\s|[:：]|$)"),
    ("work_duty", r"Security\s+Control\s+Audits(?=\s|[:：]|$)"),
    ("work_duty", r"Reporting,\s*Remediation\s*&\s*Follow[‌\s-]*up(?=\s|[:：]|$)"),
    ("work_duty", r"Stakeholder\s+Collaboration(?=\s|[:：]|$)"),
    ("candidate_qualification", r"Required\s+Qualifications(?=\s|[:：]|$)"),
    (
        "candidate_qualification",
        r"Requirements(?=\s+(?:Proven|Strong|Experience|Hands-on|Familiarity|Ability|Solid))",
    ),
    ("preferred", r"Preferred(?=\s+(?:Familiarity|Experience|Coursework|Open-source|Interest))"),
)
_NEW_HEADINGS = re.compile(
    "|".join(
        f"(?P<g{i}>(?<!\\w)(?:{pattern}))" for i, (_, pattern) in enumerate(_GENERAL_HEADINGS)
    ),
    re.I,
)
# Capture distinctive independent English bullet-like sentences lost by HTML
# flattening. Case-sensitive start words avoid splitting "experience with".
_EN_ACTION_START = re.compile(
    r"(?<!\w)(?:Build|Write|Monitor|Collaborate|Develop|Plan|Perform|Review|"
    r"Track|Ensure|Lead|Support|Assess|Identify|Provide|Coordinate|Establish|"
    r"Define|Communicate|Prepare|Escalate|Work|Analyze|Maintain|Design|Protect|"
    r"Strengthen)(?=\s+)"
)
_EN_QUAL_START = re.compile(
    r"(?<!\w)(?:Strong|Hands-on|Experience|Familiarity|Ability|Solid|"
    r"Practical|Proven|Coursework|Open-source|Interest|Good|Understanding)"
    r"(?=\s+)"
)
_EN_SENTENCE_START = re.compile(r"(?<=\.)\s+(?=[A-Z])")
_FA_WORK_ENTRY = re.compile(r"(?<!\w)(?:انجام|اجرای|ارزیابی|شناسایی|پیکربندی)(?=\s|‌)", re.I)
_SOURCE_OPTION = re.compile(
    r"(?:حداقل\s+یکی\s+از|یک\s+یا\s+چند|(?<!\w)and/or(?!\w)|"
    r"(?<!\w)or\s+(?:equivalent|another|similar)\b|"
    r"(?:frameworks?|technologies|tools?)\s+such\s+as)",
    re.I,
)
_EXPLICIT_LOCATION = re.compile(
    r"^(?:محل\s+(?:کار|شرکت|فعالیت)|موقعیت\s+مکانی|Working\s+Days|Working\s+Hours)\b",
    re.I,
)
_EXPLICIT_SCHEDULE = re.compile(
    r"(?:ساعات\s+کاری|همکاری\s+صرفاً\s+به\s+صورت\s+تمام\s+وقت|"
    r"امکان\s+دورکاری\s+و\s+پروژه[‌\s]*ای\s+وجود\s+ندارد)",
    re.I,
)
_BEHAVIOR_START = re.compile(
    r"^(?:مسئولیت[‌\s]*پذیر|روحیه|علاقه[‌\s]*مند|"
    r"پیگیری\s+بالا|توانایی\s+حل\s+مسئله|قابلیت\s+کار\s+تیمی)",
    re.I,
)


def _heading_sections_v3(text: str) -> list[tuple[int, int, str, str | None]]:
    earlier = [
        (start - len(head), start, kind, head)
        for start, _end, kind, head in _heading_sections_v2(text)
        if head is not None
    ]
    # A noun inside an existing work clause is not automatically a heading.
    # In flattened Persian, "تحلیل نیازمندی‌ها" means "analyze requirements",
    # not "start the applicant Requirements section". This is a general
    # grammatical boundary guard, not an employer-specific text exception.
    earlier = [
        unit
        for unit in earlier
        if not (
            unit[3].startswith("نیازمندی")
            and text[max(0, unit[0] - 24) : unit[0]]
            .rstrip()
            .endswith(("تحلیل", "بررسی", "شناخت", "درک"))
        )
    ]
    proposed = []
    for match in _NEW_HEADINGS.finditer(text):
        i = next(i for i in range(len(_GENERAL_HEADINGS)) if match.group(f"g{i}") is not None)
        proposed.append((match.start(), match.end(), _GENERAL_HEADINGS[i][0], match.group()))
    combined = list(proposed)
    for earlier_item in earlier:
        if not any(earlier_item[0] < b and earlier_item[1] > a for a, b, _, _ in proposed):
            combined.append(earlier_item)
    combined.sort(key=lambda x: (x[0], x[1]))
    if not combined:
        return [(0, len(text), "unresolved", None)]
    output = []
    if combined[0][0] > 0:
        output.append((0, combined[0][0], "context", None))
    for index, (_begin, end_head, role, head) in enumerate(combined):
        end = combined[index + 1][0] if index + 1 < len(combined) else len(text)
        if end_head < end:
            output.append((end_head, end, role, head))
    return output


def _split_units_v3(text: str, begin: int, end: int, role: str) -> list[tuple[int, int]]:
    initial = _split_units_v2(text, begin, end, role)
    # V2 sometimes interprets the noun phrase "team of development" or
    # "deployment processes" as the beginning of a separate imperative.
    # Rejoin only adjacent source fragments with a clearly governed noun.
    compact = []
    dangling_noun = re.compile(
        r"(?:تیم|فرآیند|فرایند|گروه|مراحل)[‌\s]*های\s*$|"
        r"(?:چرخه|کیفیت|ساختار|فرآیند|فرایند)\s*$",
        re.I,
    )
    for a, b in initial:
        if (
            compact
            and role in {"work_duty", "candidate_qualification", "preferred"}
            and dangling_noun.search(text[compact[-1][0] : compact[-1][1]])
            and not re.search(r"[.!؟؛]\s*$", text[compact[-1][0] : compact[-1][1]])
        ):
            compact[-1] = (compact[-1][0], b)
        else:
            compact.append((a, b))
    output = []
    for start, stop in compact:
        parts = {start, stop}
        if role in {"work_duty", "candidate_qualification", "preferred"}:
            matched = _EN_ACTION_START if role == "work_duty" else _EN_QUAL_START
            for mark in matched.finditer(text, start, stop):
                offset = mark.start()
                if offset - start >= 24:
                    preceding = text[max(start, offset - 8) : offset].rstrip()
                    if not preceding.endswith((",", "and", "or", "with")):
                        parts.add(offset)
            if role == "work_duty":
                for mark in _FA_WORK_ENTRY.finditer(text, start, stop):
                    if mark.start() - start >= 28:
                        before = text[max(start, mark.start() - 14) : mark.start()].rstrip()
                        if not before.endswith(("با", "در", "برای", "از", "به", "منظور")):
                            parts.add(mark.start())
            for sentence in _EN_SENTENCE_START.finditer(text, start, stop):
                parts.add(sentence.end())
        for a, b in zip(sorted(parts), sorted(parts)[1:], strict=False):
            a, b = _trim(text, a, b)
            if a < b and text[a:b] not in {"•", "●", "▪", "◦", "·", "-"}:
                output.append((a, b))
    return output


def _classify_v3(source_text: str, section: str, heading: str | None) -> tuple[str, str, str, str]:
    stripped = source_text.strip().lstrip(":： \t")
    if section == "behavioral_expectation":
        return (
            "behavioral_expectation",
            "stated_expectation",
            "explicit_original_wording",
            "unresolved",
        )
    if section in {"context", "benefit"} and (
        _EXPLICIT_LOCATION.search(stripped) or _EXPLICIT_SCHEDULE.search(stripped)
    ):
        return "work_arrangement", "not_applicable", "explicit_original_wording", "not_applicable"
    if section == "work_arrangement" and (
        _EXPLICIT_LOCATION.search(stripped) or _EXPLICIT_SCHEDULE.search(stripped)
    ):
        return "work_arrangement", "not_applicable", "explicit_original_wording", "not_applicable"
    if section == "candidate_qualification" and re.search(
        r"(?<!\w)(?:is\s+a\s+plus|would\s+be\s+a\s+plus|"
        r"nice\s+to\s+have)(?!\w)",
        stripped,
        re.I,
    ):
        return (
            "candidate_qualification",
            "preferred",
            "explicit_original_wording",
            "positive_explicit",
        )
    if section == "preferred":
        # A preferred qualification is not an employer-required skill, even
        # when the contained text uses 'experience' or 'strong'.
        return (
            "candidate_qualification",
            "preferred",
            "explicit_original_wording",
            "positive_explicit",
        )
    if section == "candidate_qualification" and _BEHAVIOR_START.match(stripped):
        return (
            "behavioral_expectation",
            "stated_expectation",
            "explicit_original_wording",
            "unresolved",
        )
    return _classify_v2(stripped, section, heading)


def interpret_original_source_candidate_v3(
    source: TranslationSourceVersion,
) -> B2SourceCandidate:
    older = interpret_original_source_candidate_v2(source)
    text = source.fields["description"]
    units: list[SourceItemCandidate] = []
    for start, end, section, head in _heading_sections_v3(text):
        # Senior/Middle alternatives are compound AND-within-OR tracks.
        # Preserve their original contiguous item boundaries for the
        # established eligibility graph contract.
        spans = (
            _split_units(text, start, end, section)
            if head and _TRACK.search(head)
            else _split_units_v3(text, start, end, section)
        )
        for a, b in spans:
            anchor = bind_original_source_span(source, char_start=a, char_end=b)
            role, strength, basis, qualifier = _classify_v3(anchor.exact_text, section, head)
            units.append(
                SourceItemCandidate(
                    anchor=anchor,
                    category=role,
                    employer_strength=strength,
                    evidence_basis=basis,
                    heading=head,
                    qualifier=qualifier,
                )
            )
    if not units or len({x.anchor.anchor_id for x in units}) != len(units):
        raise ValueError("V3 original source has no distinct exact-bound source candidate items")
    new_ids = {x.anchor.anchor_id for x in units}
    groups = list(_candidate_alternatives(source, units))
    for item in units:
        if item.category != "candidate_qualification":
            continue
        if _SOURCE_OPTION.search(item.anchor.exact_text) and not any(
            item.anchor.anchor_id in old.source_anchor_ids for old in groups
        ):
            groups.append(
                AlternativePathCandidate(
                    source_anchor_ids=(item.anchor.anchor_id,),
                    kind="explicit_unresolved_option_scope",
                    logical_operator="any_of_unresolved_option_boundaries",
                    interpretation_status="candidate_unreviewed_not_eligibility_authority",
                )
            )
    links = [
        WorkCapabilityCandidate(source_anchor_id=unit.anchor.anchor_id, capability=term)
        for unit in units
        if unit.category == "work_duty"
        for term in _TECH_CONCEPTS
        if _concept_in(unit.anchor.exact_text, term)
    ]
    candidate = replace(
        older,
        items=tuple(units),
        signals=tuple(
            s for s in older.signals if s.source_anchor_id is None or s.source_anchor_id in new_ids
        ),
        alternatives=tuple(groups),
        work_capability_links=tuple(links),
    )
    verify_b2_candidate(candidate, source)
    return candidate


def build_candidate_eligibility_logic_v3(
    source: TranslationSourceVersion, candidate: B2SourceCandidate
) -> EligibilityLogicResult:
    previous = build_candidate_eligibility_logic_v2(source, candidate)
    unresolved = list(previous.unresolved_group_kinds)
    for group in candidate.alternatives:
        if group.kind == "explicit_unresolved_option_scope":
            unresolved.append(group.kind)
    return EligibilityLogicResult(
        graphs=previous.graphs, unresolved_group_kinds=tuple(dict.fromkeys(unresolved))
    )


__all__ = [
    "B2V3_ENGINE",
    "interpret_original_source_candidate_v3",
    "build_candidate_eligibility_logic_v3",
]
