"""B2v7: explicit standalone DOM section context over source-exact B2v6 evidence.

Post-2026-11-23 live-source exposure, opt-in only. No provider calls, accepted
employer facts, source rewording or production route changes. Do not infer
professional experience from assigned work. Heading strength is local and
cannot leak through the next independent section boundary.
"""

from __future__ import annotations

import re
from bisect import bisect_right
from dataclasses import replace

from jobhunter.source_item_candidate_b2 import (
    _TECH_CONCEPTS,
    B2SourceCandidate,
    SourceItemCandidate,
    WorkCapabilityCandidate,
    _concept_in,
    verify_b2_candidate,
)
from jobhunter.source_item_candidate_b2_v4_dom import (
    DomOriginalGroup,
    exact_dom_groups,
)
from jobhunter.source_item_candidate_b2_v5_dom import (
    _BEHAVIOR,
    _NON_REQUIRED,
    _PREFERRED,
)
from jobhunter.source_item_candidate_b2_v6_dom import interpret_original_source_candidate_v6
from jobhunter.source_span_identity import bind_original_source_span
from jobhunter.translation_store import TranslationSourceVersion

B2V7_DOM_CONTRACT = "jobhunter-p16-b2-standalone-section-semantics-candidate-v7"

# Full block titles only, never a substring inside an arbitrary responsibility.
_HEADINGS: tuple[tuple[str, str], ...] = (
    (
        "work_duty",
        r"(?:what you(?:'|’)?ll work on|"
        r"(?:key |main |primary )?responsibilit(?:y|ies)|"
        r"duties|your tasks|وظایف(?: اصلی)?|مسئولیت[‌ ]*ها)",
    ),
    (
        "required_qualification",
        r"(?:must[ -]?have|essential qualifications?|"
        r"required (?:skills|qualifications?|experience)|"
        r"mandatory requirements?|مهارت[‌ ]*های ضروری)",
    ),
    (
        "preferred_qualification",
        r"(?:nice[ -]?to[ -]?have|preferred (?:skills|qualifications?)|"
        r"bonus (?:skills|points)|مزیت[‌ ]*ها)",
    ),
    (
        "candidate_qualification",
        r"(?:requirements?|technical skills(?: & technologies)?|"
        r"qualifications?|what we(?:'|’)?re looking for|skills|"
        r"مهارت[‌ ]*ها|تخصص[‌ ]*های مورد نیاز)",
    ),
    ("benefit", r"(?:why (?:grow|join|work) with us\??|benefits?|perks?|what we offer|مزایا)"),
    (
        "context",
        r"(?:about (?:us|the company|the role)|"
        r"job description|why join us\??|درباره (?:شرکت|ما))",
    ),
    (
        "work_arrangement",
        r"(?:working conditions?|employment conditions?|"
        r"working hours?|شرایط و ساعت کاری|ساعات? کاری)",
    ),
)
_HEADING_MATCH = tuple((role, re.compile(pattern, re.I)) for role, pattern in _HEADINGS)
_ARRANGEMENT_CONTENT = re.compile(
    r"^(?:flexible (?:working hours|work schedule|hours)\b|"
    r"flexible work model\s*[:：]|working (?:hours|days)\s*[:：]|"
    r"(?:full[ -]?remote|hybrid|remote work)\b|"
    r"ساعت کاری منعطف|ساعات? کاری\s*[:：]|"
    r"امکان دورکاری|دورکاری|شرایط دورکاری)",
    re.I,
)
_EXECUTABLE_SKILL = re.compile(
    r"^(?:experience\s+(?:in|with)|strong proficiency\s+in|"
    r"proficiency\s+in|familiarity\s+with|"
    r"آشنایی\s+با|تسلط\s+بر|سابقه|تجربه)",
    re.I,
)


def _full_heading(group: DomOriginalGroup, *, next_in_list: bool) -> str | None:
    if group.in_list or len(group.exact_text) > 115:
        return None
    if not (group.in_emphasis or group.in_html_heading or next_in_list):
        return None
    title = group.exact_text.strip(" \t\r\n:：?؟").replace("ي", "ی").replace("ك", "ک")
    for role, pattern in _HEADING_MATCH:
        if pattern.fullmatch(title):
            return role
    return None


def _item_for_explicit_section(
    item: SourceItemCandidate, role: str, heading: str
) -> SourceItemCandidate:
    """Refine only uncertain labels or an unambiguous employer-offering section.

    B2v6 already has a source-based label; keep stable duties, explicit
    preference/negative wording, work conditions, and benefits intact. This
    prevents a broad section regex from turning duties into requirements or
    optional statements into mandatory qualifications.
    """
    text = item.anchor.exact_text.strip()
    if _ARRANGEMENT_CONTENT.match(text) and item.category in {
        "benefit",
        "context",
        "unresolved",
        "work_arrangement",
        "work_duty",
    }:
        return replace(
            item,
            category="work_arrangement",
            employer_strength="not_applicable",
            evidence_basis="explicit_original_wording",
            qualifier="not_applicable",
        )
    if role == "benefit":
        # A standalone "Why Grow/Join/Work With Us" heading conveys what
        # the employer offers. In contrast, an arbitrary generic benefits
        # section must never erase an already explicit work duty/requirement.
        employer_offering = heading.strip().casefold().startswith("why ")
        if employer_offering and item.category not in {
            "work_arrangement",
            "compensation",
            "application_instruction",
        }:
            return replace(
                item,
                category="benefit",
                employer_strength="not_applicable",
                evidence_basis="original_section_context",
                qualifier="not_applicable",
            )
        return item
    if role == "work_duty":
        if item.category not in {"context", "unresolved"}:
            return item
        if _EXECUTABLE_SKILL.match(text) or _BEHAVIOR.match(text):
            return item
        return replace(
            item,
            category="work_duty",
            employer_strength="not_applicable",
            evidence_basis="original_section_context",
            qualifier="not_applicable",
        )
    if role in {"required_qualification", "preferred_qualification"}:
        if item.category not in {"candidate_qualification", "context", "unresolved"}:
            # A prior parser may have inherited the previous DUTIES heading
            # across the standalone "Must Have" heading. Repair only when
            # the item's own wording explicitly identifies a qualification;
            # never transform an action verb into mandatory paid experience.
            clearly_skill = _EXECUTABLE_SKILL.match(text) or re.search(
                r"\b(?:proficiency|knowledge|familiarity|experience|degree|skill)\b",
                text,
                re.I,
            )
            explicit_qualification_section = (
                role == "required_qualification"
                and heading.strip().casefold() in {"must have", "must-have"}
            ) or (
                role == "preferred_qualification"
                and heading.strip().casefold() in {"nice to have", "nice-to-have"}
            )
            if not (
                item.category == "work_duty" and explicit_qualification_section and clearly_skill
            ):
                return item
        # A prior explicit preference never becomes mandatory; an explicit
        # nonrequirement cannot inherit REQUIRED from its heading.
        if item.employer_strength == "preferred" and role == "required_qualification":
            return item
        if _NON_REQUIRED.search(text):
            strength, qualifier = "unresolved", "negative_explicit"
        elif _PREFERRED.search(text) or role == "preferred_qualification":
            strength, qualifier = "preferred", "positive_explicit"
        else:
            strength, qualifier = "required", "positive_explicit"
        if _BEHAVIOR.match(text):
            return replace(
                item,
                category="behavioral_expectation",
                employer_strength="stated_expectation",
                qualifier="unresolved",
                evidence_basis="explicit_original_wording",
            )
        return replace(
            item,
            category="candidate_qualification",
            employer_strength=strength,
            evidence_basis="original_section_context",
            qualifier=qualifier,
        )
    if role == "work_arrangement" and item.category in {
        "context",
        "unresolved",
        "benefit",
        "work_arrangement",
    }:
        return replace(
            item,
            category="work_arrangement",
            employer_strength="not_applicable",
            evidence_basis="original_section_context",
            qualifier="not_applicable",
        )
    # Generic headings and ordinary "context" must never overwrite sound
    # source-item classifications inherited from the earlier frozen layers.
    return item


def interpret_original_source_candidate_v7(
    source: TranslationSourceVersion,
    *,
    raw_job_page: bytes,
    expected_html_sha256: str | None = None,
) -> B2SourceCandidate:
    previous = interpret_original_source_candidate_v6(
        source, raw_job_page=raw_job_page, expected_html_sha256=expected_html_sha256
    )
    groups = exact_dom_groups(
        source, raw_job_page=raw_job_page, expected_html_sha256=expected_html_sha256
    )
    sections: list[tuple[int, str, str]] = []
    heading_spans: set[tuple[int, int]] = set()
    for i, group in enumerate(groups):
        role = _full_heading(group, next_in_list=i + 1 < len(groups) and groups[i + 1].in_list)
        if role is not None:
            sections.append((group.char_end, role, group.exact_text))
            heading_spans.add((group.char_start, group.char_end))

    boundaries = [x[0] for x in sections]
    items: list[SourceItemCandidate] = []
    for item in previous.items:
        if (item.anchor.char_start, item.anchor.char_end) in heading_spans:
            # A source-marked heading controls following content; it is never
            # itself an applicant requirement or employer fact.
            continue
        idx = bisect_right(boundaries, item.anchor.char_start) - 1
        if idx >= 0:
            _, role, heading = sections[idx]
            item = _item_for_explicit_section(item, role, heading)
            item = replace(item, heading=heading)
        items.append(item)

    # Source-specific grouping mistakes may have skipped a complete DOM list
    # bullet. Preserve it as an exact candidate and apply only an explicit,
    # standalone, source-owned section. No source-text paraphrase or inference.
    occupied = [(i.anchor.char_start, i.anchor.char_end) for i in items]
    for group in groups:
        if not group.in_list:
            continue
        if any(group.char_start < b and group.char_end > a for a, b in occupied):
            continue
        anchor = bind_original_source_span(
            source, char_start=group.char_start, char_end=group.char_end
        )
        candidate = SourceItemCandidate(
            anchor=anchor,
            category="unresolved",
            employer_strength="unresolved",
            evidence_basis="explicit_original_wording",
            qualifier="unresolved",
            heading=None,
        )
        idx = bisect_right(boundaries, group.char_start) - 1
        if idx >= 0:
            _, role, heading = sections[idx]
            candidate = replace(
                _item_for_explicit_section(candidate, role, heading), heading=heading
            )
        items.append(candidate)
        occupied.append((group.char_start, group.char_end))

    items.sort(key=lambda x: (x.anchor.char_start, x.anchor.char_end))
    valid = {item.anchor.anchor_id for item in items}
    alternatives = tuple(
        x
        for x in previous.alternatives
        if all(anchor_id in valid for anchor_id in x.source_anchor_ids)
    )
    links = tuple(
        WorkCapabilityCandidate(source_anchor_id=item.anchor.anchor_id, capability=term)
        for item in items
        if item.category == "work_duty"
        for term in _TECH_CONCEPTS
        if _concept_in(item.anchor.exact_text, term)
    )
    candidate = replace(
        previous,
        items=tuple(items),
        alternatives=alternatives,
        signals=tuple(
            x for x in previous.signals if x.source_anchor_id is None or x.source_anchor_id in valid
        ),
        work_capability_links=links,
    )
    verify_b2_candidate(candidate, source)
    return candidate
