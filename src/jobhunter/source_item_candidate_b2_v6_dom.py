"""B2v6 candidate: preserve and classify unambiguous DOM evidence without new authority.

Built AFTER fourth prospective cohort exposure. B2v4/v5 and frozen receipts stay
byte-identical. A behavioral trait can be a broad qualification, but it must not
inherit a hard technical requirement; section-only unknowns remain reviewable.
"""

from __future__ import annotations

from dataclasses import replace

from jobhunter.source_item_candidate_b2 import (
    _TECH_CONCEPTS,
    B2SourceCandidate,
    SourceItemCandidate,
    WorkCapabilityCandidate,
    _concept_in,
    verify_b2_candidate,
)
from jobhunter.source_item_candidate_b2_v4_dom import exact_dom_groups
from jobhunter.source_item_candidate_b2_v5_dom import (
    _BEHAVIOR,
    interpret_original_source_candidate_v5,
)
from jobhunter.source_span_identity import bind_original_source_span
from jobhunter.translation_store import TranslationSourceVersion

B2V6_DOM_CONTRACT = "jobhunter-p16-b2-evidence-coverage-behavior-candidate-v6"


def interpret_original_source_candidate_v6(
    source: TranslationSourceVersion,
    *,
    raw_job_page: bytes,
    expected_html_sha256: str | None = None,
) -> B2SourceCandidate:
    previous = interpret_original_source_candidate_v5(
        source, raw_job_page=raw_job_page, expected_html_sha256=expected_html_sha256
    )
    modified: list[SourceItemCandidate] = []
    for item in previous.items:
        phrase = item.anchor.exact_text.lstrip(" \t\n\r·*•-")
        if (
            item.category in {"candidate_qualification", "context", "unresolved"}
            and item.employer_strength != "required"
            and _BEHAVIOR.match(phrase)
        ):
            item = replace(
                item,
                category="behavioral_expectation",
                employer_strength="stated_expectation",
                qualifier="unresolved",
                evidence_basis="explicit_original_wording",
            )
        modified.append(item)

    # False-positive headings can remove real original list content. Retain
    # such uncovered whole-list evidence as UNRESOLVED, never guess that it is
    # a required qualification, benefit, duty or applicant eligibility route.
    # Source-DOM hashes, source offsets and prior candidate spans still apply.
    spans = [(x.anchor.char_start, x.anchor.char_end) for x in modified]
    for group in exact_dom_groups(
        source, raw_job_page=raw_job_page, expected_html_sha256=expected_html_sha256
    ):
        if not group.in_list or group.in_html_heading:
            continue
        start, end = group.char_start, group.char_end
        if any(start < right and end > left for left, right in spans):
            continue
        modified.append(
            SourceItemCandidate(
                anchor=bind_original_source_span(source, char_start=start, char_end=end),
                category="unresolved",
                employer_strength="unresolved",
                evidence_basis="explicit_original_wording",
                heading=None,
                qualifier="unresolved",
            )
        )
        spans.append((start, end))

    modified.sort(key=lambda x: (x.anchor.char_start, x.anchor.char_end))
    links = tuple(
        WorkCapabilityCandidate(source_anchor_id=item.anchor.anchor_id, capability=term)
        for item in modified
        if item.category == "work_duty"
        for term in _TECH_CONCEPTS
        if _concept_in(item.anchor.exact_text, term)
    )
    candidate = replace(previous, items=tuple(modified), work_capability_links=links)
    verify_b2_candidate(candidate, source)
    return candidate


__all__ = ["B2V6_DOM_CONTRACT", "interpret_original_source_candidate_v6"]
