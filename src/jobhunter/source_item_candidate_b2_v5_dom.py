"""B2v5 bounded source-DOM evidence overlay; non-authoritative.

B2v4 remains immutable after fourth prospective B5 failure. This successor
retains all of its existing original-source spans and category boundaries,
then uses standalone source-DOM section evidence to recover previously
unrecognized qualification/arrangement scope. Existing high-confidence
work duties, prior original-source graph identities and source SHA remain.

No LLM, network, production route, persistent write, or accepted fact.
"""

from __future__ import annotations

import re
from dataclasses import replace

from jobhunter.source_item_candidate_b2 import (
    _TECH_CONCEPTS,
    AlternativePathCandidate,
    B2SourceCandidate,
    SourceItemCandidate,
    WorkCapabilityCandidate,
    _concept_in,
    verify_b2_candidate,
)
from jobhunter.source_item_candidate_b2_v4_dom import (
    _is_heading,
    exact_dom_groups,
    interpret_original_source_candidate_v4,
)
from jobhunter.source_span_identity import bind_original_source_span
from jobhunter.translation_store import TranslationSourceVersion

B2V5_DOM_CONTRACT = "jobhunter-p16-b2-source-dom-evidence-overlay-candidate-v5"

# Entire original markup blocks, not vocabulary matches in arbitrary clauses.
_EXTRA_HEADINGS: tuple[tuple[str, str], ...] = (
    ("candidate_qualification", r"^(?:experience|technical skills|required skills)$"),
    ("candidate_qualification", r"^تخصص[‌\s]*های\s+مورد\s*نیاز$"),
    ("candidate_qualification", r"^شایستگی[‌\s]*های\s+تخصصی$"),
    ("candidate_qualification", r"^توانمندی[‌\s]*های\s+تخصصی$"),
    ("candidate_qualification", r"^مهارت[‌\s]*های\s+مورد\s*نیاز$"),
    ("behavioral_expectation", r"^ویژگی[‌\s]*های\s+مورد\s+انتظار$"),
    ("behavioral_expectation", r"^شایستگی[‌\s]*های\s+عمومی$"),
    ("work_arrangement", r"^شرایط\s+و\s+ساعت\s+کاری$"),
    ("work_arrangement", r"^ساعات?\s+کاری$"),
)
_ARRANGEMENT = re.compile(
    r"^(?:employment\s+type\s*:|location\s*:|time\s*:|"
    r"please\s+note\s*:\s*part.time|"
    r"part.time\s+or\s+hourly|"
    r"نوع\s+همکاری\s*:|"
    r"ساعت\s+کاری\s*:|"
    r"شرایط\s+و\s+ساعت\s+کاری|"
    r"شنبه\s+تا\s+چهارشنبه|"
    r"محدوده\s+شرکت\s*:|"
    r"محل\s+(?:فعالیت|کار|شرکت)\s*:)",
    re.I,
)
_SKILL = re.compile(
    r"^(?:داشتن|مسلط\s+به|تسلط\s+بر|آشنایی\s+با|"
    r"توانایی|مهارت\s+در|تجربه|سابقه|حداقل|"
    r"نیاز\s+به\s+حداقل|"
    r"hands.on|familiarity|proficiency|"
    r"minimum\s+\d|at\s+least\s+\d)",
    re.I,
)
_EXPLICIT_MINIMUM = re.compile(
    r"(?:نیاز\s+به\s+حداقل|حداقل\s*[۰-۹0-9]|"
    r"minimum\s*[0-9]|at\s+least\s*[0-9])",
    re.I,
)
_NON_REQUIRED = re.compile(
    r"(?:\bnot\s+(?:required|mandatory|necessary)\b|\boptional\b|"
    r"الزامی\s+نیست|ضروری\s+نیست|اجباری\s+نیست)",
    re.I,
)
_BEHAVIOR = re.compile(
    r"^(?:روحیه|مسئولیت[‌\s]*پذیری|"
    r"مسئولیت[‌\s]*پذیر|"
    r"علاقه[‌\s]*مند|توانایی\s+کار\s+تیمی)",
    re.I,
)
_PREFERRED = re.compile(
    r"(?:مزیت\s+محسوب\s+می[‌\s]*شو(?:د|ند)|"
    r"مزیت\s+محسوب\s+می[‌\s]*گردد|"
    r"امتیاز\s+(?:ویژه|مثبت)\s+دار(?:د|ند)|"
    r"nice\s+to\s+have|is\s+a\s+plus|preferred)",
    re.I,
)
_EXPLICIT_ALTERNATIVE = re.compile(
    r"(?:\band/or\b|\bor\s+equivalent\b|"
    r"(?<!\w)یا(?!\w)|"
    r"یا\s+ابزارهای\s+مشابه|"
    r"حداقل\s+یکی\s+از|"
    r"یک\s+یا\s+چند)",
    re.I,
)
_SENTENCE = re.compile(r"(?<=[.!؟؛])\s+(?=[A-Zآ-ی])")


def _inferred_qualification_status(phrase: str) -> tuple[str, str]:
    """A minimum never overrides explicit preferred or nonrequired wording."""
    if _PREFERRED.search(phrase):
        return "preferred", "positive_explicit"
    if _NON_REQUIRED.search(phrase):
        return "unresolved", "unresolved"
    if _EXPLICIT_MINIMUM.search(phrase):
        return "required", "unresolved"
    return "unresolved", "unresolved"


def _clean_heading(t: str) -> str:
    return t.strip(" \t:：").replace("ي", "ی").replace("ك", "ک").casefold()


def _role_heading(t: str) -> str | None:
    if not t or len(t) > 110 or t.lstrip().startswith(("·", "*", "-", "•")):
        return None
    value = _clean_heading(t)
    for role, regex in _EXTRA_HEADINGS:
        if re.fullmatch(regex, value, re.I):
            return role
    return None


def _label_overlay(item: SourceItemCandidate, role: str | None) -> SourceItemCandidate:
    source_text = item.anchor.exact_text
    phrase = source_text.lstrip(" \t\n\r·*•-")
    if not phrase:
        return item
    if (
        item.category == "candidate_qualification"
        and item.employer_strength == "required"
        and _NON_REQUIRED.search(phrase)
    ):
        # A flat-heading predecessor must not override explicit non-obligation.
        return replace(
            item,
            employer_strength="unresolved",
            qualifier="unresolved",
            evidence_basis="explicit_original_wording",
        )
    if _ARRANGEMENT.match(phrase) or (
        item.category == "context" and re.search(r"please\s+note\s*:\s*part.time", phrase, re.I)
    ):
        return replace(
            item,
            category="work_arrangement",
            employer_strength="not_applicable",
            evidence_basis="explicit_original_wording",
            qualifier="not_applicable",
        )
    if _BEHAVIOR.match(phrase) and item.category in {
        "context",
        "work_duty",
        "candidate_qualification",
        "benefit",
    }:
        # A duty that begins with an imperative about *doing teamwork* is
        # not the same as a trait statement; the restricted stem ensures
        # this is a stated interpersonal expectation.
        return replace(
            item,
            category="behavioral_expectation",
            employer_strength="stated_expectation",
            evidence_basis="explicit_original_wording",
            qualifier="unresolved",
        )
    if role == "candidate_qualification" and item.category in {
        "context",
        "work_duty",
        "unresolved",
        "benefit",
    }:
        strength, qualifier = _inferred_qualification_status(phrase)
        return replace(
            item,
            category="candidate_qualification",
            employer_strength=strength,
            evidence_basis="original_section_context",
            qualifier=qualifier,
        )
    if (
        role == "behavioral_expectation"
        and item.category
        in {
            "context",
            "candidate_qualification",
            "benefit",
        }
        and not _EXPLICIT_MINIMUM.search(phrase)
    ):
        return replace(
            item,
            category="behavioral_expectation",
            employer_strength="stated_expectation",
            evidence_basis="original_section_context",
            qualifier="unresolved",
        )
    if role == "work_arrangement" and item.category in {
        "context",
        "candidate_qualification",
        "benefit",
    }:
        return replace(
            item,
            category="work_arrangement",
            employer_strength="not_applicable",
            evidence_basis="original_section_context",
            qualifier="not_applicable",
        )
    if item.category == "context" and (_SKILL.match(phrase) or _EXPLICIT_MINIMUM.search(phrase)):
        strength, qualifier = _inferred_qualification_status(phrase)
        return replace(
            item,
            category="candidate_qualification",
            employer_strength=strength,
            evidence_basis="explicit_original_wording",
            qualifier=qualifier,
        )
    if item.category == "candidate_qualification" and _PREFERRED.search(phrase):
        return replace(
            item,
            employer_strength="preferred",
            evidence_basis="explicit_original_wording",
            qualifier="positive_explicit",
        )
    return item


def _source_scope(
    source: TranslationSourceVersion,
    *,
    raw_job_page: bytes,
    expected_html_sha256: str | None,
) -> tuple[list[tuple[int, str]], tuple]:
    groups = exact_dom_groups(
        source,
        raw_job_page=raw_job_page,
        expected_html_sha256=expected_html_sha256,
    )
    sections = []
    for index, group in enumerate(groups):
        kind = _role_heading(group.exact_text)
        stripped = group.exact_text.lstrip(" \t\n\r")
        if (
            kind is None
            and not stripped.startswith(("·", "*", "-", "•"))
            and not _SKILL.match(stripped)
            and len(stripped) <= 105
        ):
            kind = _is_heading(
                group,
                next_in_list=(index + 1 < len(groups) and groups[index + 1].in_list),
            )
        if kind is not None:
            sections.append((group.char_end, kind))
    return sections, groups


def interpret_original_source_candidate_v5(
    source: TranslationSourceVersion,
    *,
    raw_job_page: bytes,
    expected_html_sha256: str | None = None,
) -> B2SourceCandidate:
    prior = interpret_original_source_candidate_v4(
        source,
        raw_job_page=raw_job_page,
        expected_html_sha256=expected_html_sha256,
    )
    sections, groups = _source_scope(
        source,
        raw_job_page=raw_job_page,
        expected_html_sha256=expected_html_sha256,
    )
    modified = []
    for item in prior.items:
        applicable = [role for end, role in sections if end <= item.anchor.char_start]
        section = applicable[-1] if applicable else None
        modified.append(_label_overlay(item, section))

    # If B2v4 mistakenly treated a full qualification/schedule item as a
    # heading and omitted it, recover only an ENTIRE DOM group that is
    # NOT a recognized title and is disjoint from existing source items.
    intervals = [(i.anchor.char_start, i.anchor.char_end) for i in modified]
    for group in groups:
        if _role_heading(group.exact_text) is not None:
            continue
        a, b = group.char_start, group.char_end
        if any(a < end and b > start for start, end in intervals):
            continue
        text = group.exact_text
        phrase = text.lstrip(" \t\n\r·*•-")
        if not (_SKILL.match(phrase) or _ARRANGEMENT.match(phrase) or _BEHAVIOR.match(phrase)):
            continue
        marker = bind_original_source_span(source, char_start=a, char_end=b)
        found = SourceItemCandidate(
            anchor=marker,
            category="unresolved",
            employer_strength="unresolved",
            evidence_basis="explicit_original_wording",
            heading=None,
            qualifier="unresolved",
        )
        active = [role for end, role in sections if end <= a]
        modified.append(_label_overlay(found, active[-1] if active else None))
        intervals.append((a, b))

    modified.sort(key=lambda item: (item.anchor.char_start, item.anchor.char_end))
    identities = {item.anchor.anchor_id for item in modified}
    alternatives = [
        alt for alt in prior.alternatives if all(ref in identities for ref in alt.source_anchor_ids)
    ]
    for item in modified:
        if item.category != "candidate_qualification":
            continue
        if _EXPLICIT_ALTERNATIVE.search(item.anchor.exact_text) and not any(
            item.anchor.anchor_id in alt.source_anchor_ids for alt in alternatives
        ):
            alternatives.append(
                AlternativePathCandidate(
                    source_anchor_ids=(item.anchor.anchor_id,),
                    kind="source_dom_v5_unresolved_options",
                    logical_operator="any_of_unresolved_option_boundaries",
                    interpretation_status="candidate_unreviewed_not_eligibility_authority",
                )
            )
    links = tuple(
        WorkCapabilityCandidate(source_anchor_id=item.anchor.anchor_id, capability=term)
        for item in modified
        if item.category == "work_duty"
        for term in _TECH_CONCEPTS
        if _concept_in(item.anchor.exact_text, term)
    )
    result = replace(
        prior,
        items=tuple(modified),
        alternatives=tuple(alternatives),
        signals=tuple(
            x
            for x in prior.signals
            if x.source_anchor_id is None or x.source_anchor_id in identities
        ),
        work_capability_links=links,
    )
    verify_b2_candidate(result, source)
    return result


__all__ = ["B2V5_DOM_CONTRACT", "interpret_original_source_candidate_v5"]
