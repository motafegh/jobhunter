"""Versioned B2v4 candidate: preserve HTML list/section structure before flattening.

The original Jobinja JSON-LD description is structured HTML, while parsed
P1 source v2 normalizes it into one immutable text string. This bounded
source-owned candidate reconstructs that exact string from HTML TEXT NODES,
then labels only original spans using source-visible DOM boundaries. It refuses
stale/unmatched evidence. Generic heading cues remain advisory.

B2/B2v2/B2v3/public v30/v9 and all production stores remain unchanged.
This is not an authorization to accept a model-generated employer fact.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, replace
from html.parser import HTMLParser

from jobhunter.jobinja_details import _clean, _jobposting_json, _PageCollector, _strip_html
from jobhunter.source_item_candidate_b2 import (
    _TECH_CONCEPTS,
    AlternativePathCandidate,
    B2SourceCandidate,
    SourceItemCandidate,
    WorkCapabilityCandidate,
    _concept_in,
    verify_b2_candidate,
)
from jobhunter.source_item_candidate_b2_v3 import (
    _classify_v3,
    build_candidate_eligibility_logic_v3,
    interpret_original_source_candidate_v3,
)
from jobhunter.source_span_identity import bind_original_source_span
from jobhunter.translation_store import TranslationSourceVersion

B2V4_DOM_CONTRACT = "jobhunter-p16-b2-original-dom-segmentation-candidate-v4"
_BLOCKS = frozenset({"div", "p", "li", "ul", "ol", "br", "h1", "h2", "h3", "h4", "h5", "h6"})
_H = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
_SENIORITY_SCOPE = re.compile(r"(?:Mid[ -]?Level|Middle|میانی)\s+(?:یا|or)\s+(?:Senior|ارشد)", re.I)
_OPTION = re.compile(
    r"(?<!\w)(?:or|and/or)(?!\w)|"
    r"(?<!\w)یا(?!\w)|"
    r"(?:حداقل\s+یکی\s+از|یک\s+یا\s+چند|"
    r"یا\s+ابزارهای\s+مشابه|یا\s+فریم[‌\s]*ورک[‌\s]*های\s+مشابه)",
    re.I,
)
_PREFERRED_EXPLICIT = re.compile(
    r"(?:مزیت\s+محسوب\s+می[‌\s]*شود|"
    r"امتیاز\s+(?:مثبت|ویژه)|"
    r"nice\s+to\s+have|"
    r"is\s+a\s+plus|"
    r"bonus\s+points|"
    r"preferred|"
    r"ترجیحاً)",
    re.I,
)
_NEGATED_MANDATORY = re.compile(
    r"(?:الزامی\s+نیست|"
    r"ضروری\s+نیست|"
    r"اجباری\s+نیست|"
    r"not\s+required|"
    r"not\s+mandatory)",
    re.I,
)
_ARRANGEMENT_START = re.compile(
    r"^(?:محل\s+(?:کار|شرکت|فعالیت)|نوع\s+همکاری|"
    r"ساعات\s+کاری|"
    r"پوزیشن\s+بصورت\s+حضوری|"
    r"همکاری\s+صرفاً\s+به\s+صورت|"
    r"working\s+(?:hours|days)|"
    r"(?:Thursday|Friday|Saturday|Sunday|Monday|Tuesday|Wednesday)\s*:|"
    r"remote\s+work)",
    re.I,
)
_COMPENSATION_START = re.compile(r"^(?:حقوق|salary)\s*[:：]", re.I)
_BEHAVIORAL_OPEN = re.compile(
    r"^(?:مسئولیت[‌\s]*پذیر|علاقه[‌\s]*مند|"
    r"توانایی\s+کار\s+تیمی|روحیه\s+(?:یادگیری|کنجکاوی|کار\s+تیمی))",
    re.I,
)


@dataclass(frozen=True, slots=True)
class DomOriginalNode:
    text: str
    char_start: int
    char_end: int
    group: int
    in_list: bool
    in_emphasis: bool
    in_html_heading: bool


@dataclass(frozen=True, slots=True)
class DomOriginalGroup:
    char_start: int
    char_end: int
    exact_text: str
    in_list: bool
    in_emphasis: bool
    in_html_heading: bool


class _SourceDOM(HTMLParser):
    """Record only ordered HTML text nodes plus structural group boundaries."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._stack: list[str] = []
        self._group = 0
        self.nodes: list[tuple[int, str, bool, bool, bool]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        t = tag.casefold()
        if t in _BLOCKS:
            self._group += 1
        if t not in {"br", "hr", "img", "input", "meta", "link", "wbr"}:
            self._stack.append(t)

    def handle_endtag(self, tag: str) -> None:
        t = tag.casefold()
        if t in _BLOCKS:
            self._group += 1
        if t in self._stack:
            # HTML source may be imperfectly nested: close the current tag
            # and all open descendants without assigning imagined DOM nodes.
            self._stack = self._stack[: len(self._stack) - 1 - self._stack[::-1].index(t)]

    def handle_data(self, data: str) -> None:
        content = _clean(data)
        if not content:
            return
        self.nodes.append(
            (
                self._group,
                content,
                "li" in self._stack,
                "strong" in self._stack or "b" in self._stack,
                bool(_H.intersection(self._stack)),
            )
        )


def _source_description_html(raw_job_page: bytes) -> str:
    c = _PageCollector()
    c.feed(raw_job_page.decode("utf-8"))
    c.close()
    job = _jobposting_json(c)
    if not isinstance(job, dict) or not isinstance(job.get("description"), str):
        raise ValueError("B2v4 DOM candidate requires original JobPosting HTML description")
    return job["description"]


def exact_dom_groups(
    source: TranslationSourceVersion,
    *,
    raw_job_page: bytes,
    expected_html_sha256: str | None = None,
) -> tuple[DomOriginalGroup, ...]:
    """Verify *entire* raw HTML and exact normalized original-source span cover."""
    if (
        expected_html_sha256 is not None
        and hashlib.sha256(raw_job_page).hexdigest() != expected_html_sha256
    ):
        raise ValueError("B2v4 raw original HTML fingerprint mismatch")
    description = source.fields.get("description")
    if not isinstance(description, str) or not description.strip():
        raise ValueError("Missing frozen original description")
    markup = _source_description_html(raw_job_page)
    if _strip_html(markup) != description:
        raise ValueError("Original HTML normalized description is not the frozen source")
    collector = _SourceDOM()
    collector.feed(markup)
    collector.close()
    if not collector.nodes:
        raise ValueError("No DOM text nodes in preserved original description")
    # This is EXACTLY the existing v2 _PageCollector normalization: a
    # whitespace separator is inserted after every HTML data node.
    flat = " ".join(node[1] for node in collector.nodes)
    if flat != description:
        raise ValueError("DOM text nodes cannot exactly reproduce source-v2 description")
    nodes: list[DomOriginalNode] = []
    cursor = 0
    for group_id, piece, in_list, emphasis, header in collector.nodes:
        end = cursor + len(piece)
        nodes.append(
            DomOriginalNode(
                text=piece,
                char_start=cursor,
                char_end=end,
                group=group_id,
                in_list=in_list,
                in_emphasis=emphasis,
                in_html_heading=header,
            )
        )
        cursor = end + 1
    if cursor - 1 != len(description):
        raise ValueError("DOM source span accounting inconsistent with original text")
    grouped: list[DomOriginalGroup] = []
    run: list[DomOriginalNode] = []

    def flush() -> None:
        if not run:
            return
        first, last = run[0], run[-1]
        start, end = first.char_start, last.char_end
        exact = description[start:end]
        if exact != " ".join(x.text for x in run):
            raise ValueError("Grouped DOM text is not exact source-owned original substring")
        grouped.append(
            DomOriginalGroup(
                char_start=start,
                char_end=end,
                exact_text=exact,
                in_list=any(x.in_list for x in run),
                in_emphasis=any(x.in_emphasis for x in run),
                in_html_heading=any(x.in_html_heading for x in run),
            )
        )

    for node in nodes:
        if run and node.group != run[0].group:
            flush()
            run = []
        run.append(node)
    flush()
    if len({(x.char_start, x.char_end) for x in grouped}) != len(grouped):
        raise ValueError("DOM segmentation duplicated an original span")
    if any(a.char_end >= b.char_start for a, b in zip(grouped, grouped[1:], strict=False)):
        raise ValueError("DOM segmentation has overlapping source spans")
    return tuple(grouped)


def _fold(value: str) -> str:
    """Minimal orthography normalization for heading-role lexemes only."""
    return (
        value.casefold()
        .replace("‌", "")
        .replace("ي", "ی")
        .replace("ك", "ک")
        .replace(":", " ")
        .replace("：", " ")
        .strip()
    )


def _heading_role(text: str) -> str | None:
    """Classify standalone *source-marked headings*, never skill-name labels."""
    t = _fold(text)
    if len(t) > 135 or not t:
        return None
    if any(
        x in t
        for x in (
            "nice to have",
            "preferred",
            "bonus",
            "مزیت",
            "امتیاز",
            "مطلوب",
            "ترجیح",
        )
    ):
        return "preferred"
    if any(
        x in t
        for x in (
            "soft skills",
            "mindset",
            "شایستگیهای فردی",
            "مهارتهای فردی",
            "توانمندیهای عمومی",
            "ویژگیهای فردی",
            "ویژگیهای حرفه",
        )
    ):
        return "behavioral_expectation"
    if any(x in t for x in ("benefits", "perks", "مزایا", "بیمه و")):
        return "benefit"
    if any(
        x in t
        for x in (
            "شرایط همکاری",
            "working conditions",
            "نوع همکاری",
            "ساعات کاری",
            "employment conditions",
            "موقعیت مکانی",
        )
    ):
        return "work_arrangement"
    if any(
        x in t
        for x in (
            "responsibilit",
            "duties",
            "tasks",
            "وظایف",
            "مسئولیت",
        )
    ):
        return "work_duty"
    if any(
        x in t
        for x in (
            "required",
            "qualification",
            "requirements",
            "skills",
            "شرایط احراز",
            "مهارت",
            "توانمندی",
            "دانش و ",
            "الزامات",
            "تخصصی",
        )
    ):
        return "candidate_qualification"
    if any(x in t for x in ("about the role", "درباره موقعیت", "شرح موقعیت")):
        return "context"
    return None


def _is_heading(group: DomOriginalGroup, *, next_in_list: bool) -> str | None:
    role = _heading_role(group.exact_text)
    if role is None:
        return None
    # A heading is a standalone block from source markup or the parent of
    # ensuing list items. A clause *mentioning* requirements must not open
    # a new applicant-skills section in the middle of a duty.
    if (
        group.in_html_heading
        or (group.in_emphasis and len(group.exact_text) <= 115)
        or (not group.in_list and next_in_list and len(group.exact_text) <= 115)
        or (not group.in_list and len(group.exact_text) <= 60)
    ):
        return role
    return None


def _label_item(
    group: DomOriginalGroup,
    role: str,
    heading: str | None,
) -> tuple[str, str, str, str]:
    t = group.exact_text.strip()
    if _COMPENSATION_START.match(t):
        return "compensation", "not_applicable", "explicit_original_wording", "not_applicable"
    if _ARRANGEMENT_START.match(t):
        return "work_arrangement", "not_applicable", "explicit_original_wording", "not_applicable"
    if _BEHAVIORAL_OPEN.match(t):
        return (
            "behavioral_expectation",
            "stated_expectation",
            "explicit_original_wording",
            "unresolved",
        )
    if role == "work_duty" and _PREFERRED_EXPLICIT.search(t):
        return (
            "candidate_qualification",
            "preferred",
            "explicit_original_wording",
            "positive_explicit",
        )
    if role == "work_arrangement" and "حقوق:" in t[:18]:
        return "compensation", "not_applicable", "explicit_original_wording", "not_applicable"
    if role == "work_duty":
        # An explicit applicant-skill cue may appear among tasks; don't
        # transform it into a fabricated employee duty.
        if re.match(
            r"^(?:تسلط|آشنایی|تجربه|سابقه|توانایی|"
            r"hands-on experience|proficiency|familiarity|ability to)\b",
            t,
            re.I,
        ):
            return "candidate_qualification", "unresolved", "original_section_context", "unresolved"
        return "work_duty", "not_applicable", "original_section_context", "not_applicable"
    if role == "candidate_qualification":
        if _PREFERRED_EXPLICIT.search(t):
            return (
                "candidate_qualification",
                "preferred",
                "explicit_original_wording",
                "positive_explicit",
            )
        if _NEGATED_MANDATORY.search(t):
            return (
                "candidate_qualification",
                "unresolved",
                "explicit_original_wording",
                "negative_explicit",
            )
        category, strength, basis, qual = _classify_v3(t, role, heading)
        # A literal REQUIRED section establishes its own scope; a generic
        # skills section (or merely "important") does not. Optional/negative
        # item wording above always overrides section strength.
        if (
            category == "candidate_qualification"
            and strength == "unresolved"
            and heading is not None
            and re.search(r"(?<!\w)required(?!\w)|مهارت[‌\s]*های\s+ضروری", heading, re.I)
        ):
            return category, "required", "original_section_context", "positive_explicit"
        return category, strength, basis, qual
    if role == "preferred":
        return (
            "candidate_qualification",
            "preferred",
            "original_section_context",
            "positive_explicit",
        )
    if role == "behavioral_expectation":
        return (
            "behavioral_expectation",
            "stated_expectation",
            "original_section_context",
            "unresolved",
        )
    if role == "work_arrangement":
        return "work_arrangement", "not_applicable", "original_section_context", "not_applicable"
    if role == "benefit":
        return "benefit", "not_applicable", "original_section_context", "not_applicable"
    if role == "context":
        return "context", "not_applicable", "original_section_context", "not_applicable"
    # A meaning-bearing original clause without known section remains
    # an unresolved candidate (never a guessed hard requirement/duty).
    return _classify_v3(t, "unresolved", heading)


def interpret_original_source_candidate_v4(
    source: TranslationSourceVersion,
    *,
    raw_job_page: bytes,
    expected_html_sha256: str | None = None,
) -> B2SourceCandidate:
    """Versioned DOM candidate, never a production source of accepted facts."""
    previous = interpret_original_source_candidate_v3(source)
    groups = exact_dom_groups(
        source,
        raw_job_page=raw_job_page,
        expected_html_sha256=expected_html_sha256,
    )
    text = source.fields["description"]
    current_role = "context"
    heading: str | None = None
    items: list[SourceItemCandidate] = []
    alternatives: list[AlternativePathCandidate] = []
    for index, group in enumerate(groups):
        next_in_list = index + 1 < len(groups) and groups[index + 1].in_list
        section = _is_heading(group, next_in_list=next_in_list)
        if section is not None:
            heading, current_role = group.exact_text, section
            continue
        anchor = bind_original_source_span(
            source,
            char_start=group.char_start,
            char_end=group.char_end,
        )
        category, strength, basis, qualifier = _label_item(group, current_role, heading)
        item = SourceItemCandidate(
            anchor=anchor,
            category=category,
            employer_strength=strength,
            evidence_basis=basis,
            qualifier=qualifier,
            heading=heading,
        )
        items.append(item)
        if category == "candidate_qualification" and _OPTION.search(anchor.exact_text):
            alternatives.append(
                AlternativePathCandidate(
                    source_anchor_ids=(anchor.anchor_id,),
                    kind="source_dom_explicit_unresolved_option_scope",
                    logical_operator="any_of_unresolved_option_boundaries",
                    interpretation_status="candidate_unreviewed_not_eligibility_authority",
                )
            )
    if not items:
        raise ValueError("DOM source segmentation yielded no evidence-qualified original items")
    # If the DOM has no recognized work section but the already-proven B2v3
    # source parser has an explicit named duty section, preserve its complete
    # source anchors rather than suppressing every task. Likewise never drop
    # an existing compound-source AND/OR graph known to B1.
    old_graphs = build_candidate_eligibility_logic_v3(source, previous).graphs
    if old_graphs or (
        not any(x.category == "work_duty" for x in items)
        and any(x.category == "work_duty" and x.heading for x in previous.items)
    ):
        return previous
    # An explicitly either-level seniority role may appear in an introductory
    # paragraph, not a qualification bullet. Preserve an unresolved signal,
    # not a fabricated AND/OR applicant graph or mandatory years claim.
    for match in _SENIORITY_SCOPE.finditer(text):
        containing = [
            x
            for x in items
            if x.anchor.char_start <= match.start() and x.anchor.char_end >= match.end()
        ]
        if len(containing) == 1 and not any(
            containing[0].anchor.anchor_id in x.source_anchor_ids for x in alternatives
        ):
            alternatives.append(
                AlternativePathCandidate(
                    source_anchor_ids=(containing[0].anchor.anchor_id,),
                    kind="source_dom_unresolved_seniority_or",
                    logical_operator="any_of_unresolved_option_boundaries",
                    interpretation_status="candidate_unreviewed_not_eligibility_authority",
                )
            )
    ids = {x.anchor.anchor_id for x in items}
    links = tuple(
        WorkCapabilityCandidate(source_anchor_id=x.anchor.anchor_id, capability=term)
        for x in items
        if x.category == "work_duty"
        for term in _TECH_CONCEPTS
        if _concept_in(x.anchor.exact_text, term)
    )
    view = replace(
        previous,
        items=tuple(items),
        signals=tuple(
            s for s in previous.signals if s.source_anchor_id is None or s.source_anchor_id in ids
        ),
        alternatives=tuple(alternatives),
        work_capability_links=links,
    )
    verify_b2_candidate(view, source)
    for item in view.items:
        a = item.anchor
        if text[a.char_start : a.char_end] != a.exact_text:
            raise ValueError("Bound DOM candidate lost exact original quote")
    return view


__all__ = [
    "B2V4_DOM_CONTRACT",
    "DomOriginalGroup",
    "exact_dom_groups",
    "interpret_original_source_candidate_v4",
]
