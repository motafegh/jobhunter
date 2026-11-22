"""Calibrated, source-first B5 diagnostic over already exposed original assertions.

Distinct from the immutable 2026-11-22 original gate. This version separates
source-span granularity, employer-role classification and optional example
lists; no model acceptance or fresh B5 promotion follows from these checks.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from typing import Any

from jobhunter.source_item_candidate_b2 import (
    B2SourceCandidate,
    SourceItemCandidate,
    verify_b2_candidate,
)

_EXPECTED = {
    "duty": "work_duty",
    "qualification": "candidate_qualification",
    "behavior": "behavioral_expectation",
    "arrangement": "work_arrangement",
}
# These review modalities explicitly describe illustrative skills/tools or
# methods. They are NOT reviewed claims of formal employer eligibility ORs.
_ILLUSTRATIVE = frozenset(
    {
        "bonus_examples_or",
        "familiarity_examples",
        "required_section_or_examples",
        "required_section_similar_options",
    }
)
# Only a reviewer-explicit choice of eligibility routes may trigger this
# strict missing-alternative check. Unknown modalities remain *unresolved*.
_EXPLICIT_ELIGIBILITY = frozenset(
    {
        "explicit_eligibility_or",
        "explicit_specialty_or",
        "explicit_required_either_or",
    }
)
_OPTIONAL = frozenset(
    {
        "nice_to_have",
        "bonus_optional",
        "explicit_preferred",
        "explicit_special_advantage",
        "preferred_education",
        "preferred_tools",
        "preferred_programming",
        "preferred_certificates",
        "preferred_degree",
        "optional_relocation",
        "explicit_not_required",
    }
)


def _overlaps(items: tuple[SourceItemCandidate, ...], start: int, end: int):
    return tuple(
        item
        for item in sorted(items, key=lambda x: x.anchor.char_start)
        if item.anchor.char_start < end and item.anchor.char_end > start
    )


def _span_cover(
    *,
    text: str,
    start: int,
    end: int,
    items: tuple[SourceItemCandidate, ...],
) -> tuple[str, tuple[SourceItemCandidate, ...]]:
    """Cover a reviewed quote by contiguous nonoverlapping evidence units.

    Boundaries between adjacent item anchors may contain only whitespace.
    All nonwhitespace bytes must be accounted for, including Persian text.
    An uncovered word, a different-category overlapping item, or an offset
    crossing genuine source content must not be counted as successful.
    """
    overlaps = _overlaps(items, start, end)
    if not overlaps:
        return "missing", ()
    cursor = start
    used: list[SourceItemCandidate] = []
    for item in overlaps:
        lo = max(start, item.anchor.char_start)
        hi = min(end, item.anchor.char_end)
        if lo > cursor and text[cursor:lo].strip():
            return "gap_in_original_source", tuple(used)
        if hi > cursor:
            used.append(item)
            cursor = hi
    if cursor < end and text[cursor:end].strip():
        return "gap_in_original_source", tuple(used)
    if not used:
        return "missing", ()
    return ("covered_one_item" if len(used) == 1 else "covered_across_items"), tuple(used)


def assess_source_anchor(
    anchor: dict[str, Any], candidate: B2SourceCandidate, original: str
) -> dict[str, Any]:
    """A selected original assertion is not automatically a hard obligation."""
    a, b = anchor["original_description_start"], anchor["original_description_end"]
    quote = anchor["original_quote"]
    if (
        not isinstance(a, int)
        or not isinstance(b, int)
        or a < 0
        or a >= b
        or b > len(original)
        or original[a:b] != quote
        or hashlib.sha256(quote.encode("utf-8")).hexdigest() != anchor["quote_sha256"]
    ):
        raise ValueError("Frozen source-first anchor text/coordinates/SHA drift")

    coverage, used = _span_cover(text=original, start=a, end=b, items=candidate.items)
    expected = _EXPECTED.get(anchor["kind"])
    roles = tuple(i.category for i in used)
    strengths = tuple(i.employer_strength for i in used)

    # A behavioral expectation may also be a broad applicant qualification;
    # that distinction is diagnostic, not a fabricated mandatory-years claim.
    compatible = bool(
        coverage.startswith("covered")
        and expected == "behavioral_expectation"
        and roles == ("candidate_qualification",)
        and strengths[0] != "required"
    )
    role_match = bool(
        coverage.startswith("covered") and expected and all(r == expected for r in roles)
    )
    optional_overstatement = bool(
        (
            anchor["modality_source_first"] in _OPTIONAL
            or anchor["kind"] in {"behavior", "arrangement"}
        )
        and any(x == "required" for x in strengths)
    )
    if anchor["kind"] == "alternative":
        modality = anchor["modality_source_first"]
        if modality in _ILLUSTRATIVE:
            alternative_type = "illustrative_options_not_eligibility_authority"
        elif modality in _EXPLICIT_ELIGIBILITY:
            alternative_type = "explicit_eligibility_disjunction_reviewed"
        else:
            alternative_type = "unresolved_not_formal_eligibility"
    else:
        alternative_type = "not_applicable"

    refs = {x.anchor.anchor_id for x in used}
    scoped_options = bool(
        refs and any(refs.intersection(alt.source_anchor_ids) for alt in candidate.alternatives)
    )
    # Graph existence in another section of the vacancy cannot satisfy
    # this anchor. A candidate-only graph must be locally source-linked.
    if alternative_type == "explicit_eligibility_disjunction_reviewed":
        alternative_status = (
            "source_scope_present_unreviewed" if scoped_options else "missing_source_scope"
        )
    elif alternative_type == "illustrative_options_not_eligibility_authority":
        alternative_status = "examples_not_mandatory_eligibility"
    elif alternative_type == "unresolved_not_formal_eligibility":
        alternative_status = "unresolved_not_auto_failed"
    else:
        alternative_status = "not_applicable"

    if not coverage.startswith("covered"):
        role_state = "source_not_fully_covered"
    elif role_match:
        role_state = "exact_role"
    elif compatible:
        role_state = "compatible_broad_qualification"
    elif expected:
        role_state = "different_role"
    else:
        role_state = "not_scored"
    # Category precision is recorded without automatically equating taxonomy
    # differences to employer-fact harm. Requiredness/OR/explicit duties remain
    # independent high-impact checks.
    critical_role_mismatch = bool(
        role_state == "different_role"
        and expected in {"work_duty", "candidate_qualification", "work_arrangement"}
    )
    duty_missed = bool(expected == "work_duty" and role_state != "exact_role")
    return {
        "anchor_id": anchor["anchor_id"],
        "coverage": coverage,
        "covered_item_count": len(used),
        "role_state": role_state,
        "candidate_roles": roles,
        "optional_or_negative_to_required": optional_overstatement,
        "explicit_duty_missing": duty_missed,
        "critical_category_mismatch": critical_role_mismatch,
        "alternative_type": alternative_type,
        "alternative_status": alternative_status,
        "hard_alternative_missing": alternative_status == "missing_source_scope",
    }


def evaluate_calibrated_gate(
    *,
    frozen: dict[str, Any],
    review: dict[str, Any],
    source_versions: dict[str, Any],
    engine: Any,
) -> dict[str, Any]:
    selection = frozen["selected_primary"]
    ids = [i["source_job_id"] for i in selection]
    if len(ids) != len(set(ids)) or not 6 <= len(ids) <= 8:
        raise ValueError("Expected six to eight unique frozen job sources")
    if ids != [i["source_job_id"] for i in review["entries"]]:
        raise ValueError("Source-first review/selection ordering drift")
    per_case = []
    for entry in review["entries"]:
        job = entry["source_job_id"]
        source = source_versions[job]
        if source.semantic_sha256 != entry["source_semantic_sha256"]:
            raise ValueError("Original semantic source SHA mismatch")
        original = source.fields["description"]
        candidate = engine(source)
        verify_b2_candidate(candidate, source)
        results = [
            assess_source_anchor(anchor, candidate, original)
            for anchor in entry["reviewed_original_anchors"]
        ]
        stats = Counter(
            {
                "reviewed_assertions": len(results),
                "role_comparable_assertions": sum(
                    anchor["kind"] in _EXPECTED for anchor in entry["reviewed_original_anchors"]
                ),
                "exact_role": sum(r["role_state"] == "exact_role" for r in results),
                "broad_qualification_compatible": sum(
                    r["role_state"] == "compatible_broad_qualification" for r in results
                ),
                "uncovered": sum(
                    r["coverage"] in {"missing", "gap_in_original_source"} for r in results
                ),
                "cross_item_covered": sum(r["coverage"] == "covered_across_items" for r in results),
                "critical_category_mismatches": sum(
                    r["critical_category_mismatch"] for r in results
                ),
                "explicit_duty_missed": sum(r["explicit_duty_missing"] for r in results),
                "false_mandatory": sum(r["optional_or_negative_to_required"] for r in results),
                "explicit_eligibility_scope_missing": sum(
                    r["hard_alternative_missing"] for r in results
                ),
                "illustrative_alternatives": sum(
                    r["alternative_type"] == "illustrative_options_not_eligibility_authority"
                    for r in results
                ),
                "unresolved_alternatives": sum(
                    r["alternative_type"] == "unresolved_not_formal_eligibility" for r in results
                ),
            }
        )
        per_case.append(
            {
                "source_job_id": job,
                "counts": dict(stats),
                "anchor_diagnostics": results,
            }
        )
    totals = {k: sum(case["counts"][k] for case in per_case) for k in per_case[0]["counts"]}
    hard_stop = any(
        totals[k]
        for k in (
            "critical_category_mismatches",
            "explicit_duty_missed",
            "false_mandatory",
            "explicit_eligibility_scope_missing",
        )
    )
    incomplete_review = bool(totals["unresolved_alternatives"] or totals["uncovered"])
    disposition = (
        "BLOCKED_REMAINING_MATERIAL_SOURCE_ERRORS"
        if hard_stop
        else (
            "INCOMPLETE_SOURCE_COVERAGE_OR_ALTERNATIVE_MEANING"
            if incomplete_review
            else "NO_SELECTED_CRITICAL_FAILURE_EXPOSED_ONLY"
        )
    )
    return {
        "contract": "jobhunter-b5-calibrated-source-gate-development-v2",
        "evaluation_scope": "exposed_only_retrospective_not_original_prospective",
        "disposition": disposition,
        "counts": totals,
        "cases": per_case,
        "B5_pass": False,
        "B6_authorized": False,
        "accepted_facts": 0,
    }
