"""B4v6 — compact decision-first candidate view of already source-qualified B4v5 evidence.

No new source classification, new employer requirements, provider calls, or
accepted-fact promotion. The complete original source inventory stays available
for drilldown. Default display is bounded and may be incomplete on purpose.
"""

from __future__ import annotations

from typing import Any

from jobhunter.source_qualified_b4v5 import digest_text, markdown_escape

COMPACT_CONTRACT = "jobhunter-p16-b4-compact-source-decision-candidate-v6"
DUTY_LIMIT = 3
QUALIFICATION_LIMIT = 2
CONDITION_LIMIT = 3
GRAPH_LIMIT = 4
CATEGORIES = frozenset(
    {
        "work_duty",
        "candidate_qualification",
        "behavioral_expectation",
        "work_arrangement",
        "application_instruction",
        "compensation",
        "benefit",
        "context",
        "unresolved",
    }
)
STRENGTHS = frozenset(
    {"required", "preferred", "stated_expectation", "not_applicable", "unresolved"}
)


def _check_item(item: dict[str, Any]) -> None:
    if (
        item.get("authority") != "B2_B3_source_qualified_candidate_not_accepted_fact"
        or item.get("category_candidate") not in CATEGORIES
        or item.get("strength_candidate") not in STRENGTHS
        or not isinstance(item.get("source_item_id"), str)
        or not item["source_item_id"]
        or not isinstance(item.get("original_text"), str)
        or not item["original_text"]
        or digest_text(item["original_text"]) != item.get("source_span_sha256")
    ):
        raise ValueError("B4v6 original-source evidence identity/authority mismatch")
    translated = item.get("target_text_candidate")
    if not isinstance(translated, str) or not translated:
        raise ValueError("B4v6 requires existing source-bound English reading aid")
    if item.get("b4_reviewed_terminology_overlay"):
        overlay = item["b4_reviewed_terminology_overlay"]
        if overlay.get("overlay_source_sha256") != item["source_span_sha256"] or overlay.get(
            "target_sha256"
        ) != digest_text(translated):
            raise ValueError("B4v6 reviewed terminology overlay source/target drift")


def _selected_evidence(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_item_id": item["source_item_id"],
        "source_span_sha256": item["source_span_sha256"],
        "original_text": item["original_text"],
        "english_reading_aid": item["target_text_candidate"],
        "translation_review_state": item["translation_review_state"],
        "category_candidate": item["category_candidate"],
        "strength_candidate": item["strength_candidate"],
        "qualifier_candidate": item["qualifier_candidate"],
        "explicit_conditional_application": item["is_conditional_application_statement"],
        "terminology_reviewed_overlay": bool(item["b4_reviewed_terminology_overlay"]),
        "authority": "candidate_only_not_employer_fact",
    }


def _select(items: list[dict[str, Any]], count: int) -> dict[str, Any]:
    visible = items[:count]
    return {
        "candidate_count": len(items),
        "visible": [_selected_evidence(item) for item in visible],
        "more_in_source_drilldown": len(items) - len(visible),
    }


def _node_sources(node: dict[str, Any]) -> set[str]:
    kind = node["kind"]
    if kind in {"any_of", "all_of"}:
        return set().union(*(_node_sources(child) for child in node["children"]))
    if kind == "whole_item":
        return {node["source_item_id"]}
    if kind == "original_subspan":
        if node["child_english_alignment"] != "not_established":
            raise ValueError("B4v6 cannot invent English alignment for nested original span")
        return {node["parent_source_item_id"]}
    raise ValueError("B4v6 unexpected eligibility graph branch")


def build_compact_decision_view(projection: dict[str, Any]) -> dict[str, Any]:
    if (
        projection.get("contract") != "jobhunter-p16-b4-source-qualified-projection-v5"
        or projection.get("accepted_employer_facts") != 0
        or projection.get("downstream_authority") != "none"
        or projection.get("unseen_generalization_established") is not False
        or projection["source_version"]["source_job_id"] != projection.get("source_job_id")
    ):
        raise ValueError("B4v6 cannot import a different or promoted source projection")

    items = projection["source_qualified_items"]
    ids = [item["source_item_id"] for item in items]
    if len(ids) != len(set(ids)):
        raise ValueError("B4v6 duplicate B4v5 source IDs")
    for item in items:
        _check_item(item)
    if (
        sum(len(group) for group in projection["groups"].values()) != len(items)
        or projection["source_item_count"] != len(items) + projection["excluded_source_item_count"]
    ):
        raise ValueError("B4v6 B4v5 candidate count/group drift")
    grouped = {
        category: [item["source_item_id"] for item in part]
        for category, part in projection["groups"].items()
    }
    expected = {
        category: [
            item["source_item_id"] for item in items if item["category_candidate"] == category
        ]
        for category in grouped
    }
    if grouped != expected:
        raise ValueError("B4v6 grouped inventory does not match original source order")

    duties = [item for item in items if item["category_candidate"] == "work_duty"]
    # This special ordering is generic: any terminology-corrected original
    # receives attention before unreviewed reading aids, never an invented claim.
    duties.sort(
        key=lambda item: (
            not bool(item["b4_reviewed_terminology_overlay"]),
            ids.index(item["source_item_id"]),
        )
    )

    capabilities = [
        item
        for item in items
        if item["category_candidate"] in {"candidate_qualification", "behavioral_expectation"}
    ]
    required = [item for item in capabilities if item["strength_candidate"] == "required"]
    preferred = [item for item in capabilities if item["strength_candidate"] == "preferred"]
    other = [
        item for item in capabilities if item["strength_candidate"] not in {"required", "preferred"}
    ]
    conditions = [
        item
        for item in items
        if item["category_candidate"]
        in {"application_instruction", "work_arrangement", "compensation"}
    ]
    conditions.sort(
        key=lambda item: (
            0
            if item["is_conditional_application_statement"]
            else (1 if item["category_candidate"] == "work_arrangement" else 2),
            ids.index(item["source_item_id"]),
        )
    )
    graphs = projection["eligibility_alternative_candidates"]
    if len(graphs) > GRAPH_LIMIT:
        raise ValueError("B4v6 graph cap would silently omit original eligibility evidence")
    graph_ids = [g["graph_id"] for g in graphs]
    if len(graph_ids) != len(set(graph_ids)):
        raise ValueError("B4v6 duplicate eligibility graph")
    by_id = set(ids)
    for graph in graphs:
        if graph.get("authority") != "B2_candidate_structure_not_accepted_employer_eligibility":
            raise ValueError("B4v6 eligibility authority changed")
        if not _node_sources(graph["root"]).issubset(by_id):
            raise ValueError("B4v6 graph parent source missing")
    sections = {
        "what_work": _select(duties, DUTY_LIMIT),
        "capabilities": {
            "required_candidate": _select(required, QUALIFICATION_LIMIT),
            "preferred_candidate": _select(preferred, QUALIFICATION_LIMIT),
            "other_or_unresolved_candidate": _select(other, QUALIFICATION_LIMIT),
        },
        "eligibility": {
            "candidate_graph_count": len(graphs),
            "unreviewed_candidate_graphs": graphs,
            "authority": "candidate_graph_not_employer_verified_eligibility",
        },
        "conditions": _select(conditions, CONDITION_LIMIT),
    }
    source_drilldown = [_selected_evidence(item) for item in items]
    visible_ids = [
        item["source_item_id"]
        for section in (
            sections["what_work"],
            sections["capabilities"]["required_candidate"],
            sections["capabilities"]["preferred_candidate"],
            sections["capabilities"]["other_or_unresolved_candidate"],
            sections["conditions"],
        )
        for item in section["visible"]
    ]
    if len(visible_ids) != len(set(visible_ids)):
        raise ValueError("B4v6 default preview duplicates source items")
    suppressed = projection["v4_model_claims_suppressed_due_to_translation_review"]
    corrections = projection["corrected_translation_item_ids"]
    if any(item["source_item_id"] not in by_id for item in source_drilldown) or not set(
        corrections
    ).issubset(by_id):
        raise ValueError("B4v6 source/drilldown corrections lost")
    return {
        "contract": COMPACT_CONTRACT,
        "source_job_id": projection["source_job_id"],
        "source_version": projection["source_version"],
        "source_qualified_item_count": len(items),
        "source_item_count": projection["source_item_count"],
        "excluded_source_item_count": projection["excluded_source_item_count"],
        "sections": sections,
        "default_visible_source_item_ids": visible_ids,
        "default_visible_evidence_item_count": len(visible_ids),
        "source_drilldown": source_drilldown,
        "source_drilldown_required_for_complete_job": any(
            s["more_in_source_drilldown"]
            for s in (
                sections["what_work"],
                sections["capabilities"]["required_candidate"],
                sections["capabilities"]["preferred_candidate"],
                sections["capabilities"]["other_or_unresolved_candidate"],
                sections["conditions"],
            )
        ),
        "candidate_only_unresolved_item_count": sum(
            item["category_candidate"] == "unresolved" for item in items
        ),
        "candidate_only_context_benefit_item_count": sum(
            item["category_candidate"] in {"context", "benefit"} for item in items
        ),
        "b4_model_outcome": projection["b4_analysis_outcome"],
        "b4_model_attempt_outcome": projection["b4_attempt_outcome"],
        "suppressed_prior_model_claim_count": len(suppressed),
        "suppressed_prior_model_claims": suppressed,
        "corrected_translation_item_ids": corrections,
        "metadata_conflict_candidate_count": len(projection["metadata_conflict_candidates"]),
        "source_first_nonstrengthening": True,
        "review_state": "assistant_exposed_compact_presentation_not_independently_evaluated",
        "accepted_employer_facts": 0,
        "downstream_authority": "none",
        "unseen_generalization_established": False,
        "b5_accepted": False,
        "b6_production_authorized": False,
    }


def _original_and_english_lines(item: dict[str, Any]) -> list[str]:
    # No templated HTML and no ambiguous Markdown links from employer text.
    return [
        f"- English *reading aid*: {markdown_escape(item['english_reading_aid'])}",
        f"  - Original: {markdown_escape(item['original_text'])}",
        f"  - Source evidence: `{markdown_escape(item['source_item_id'])}` "
        f"(SHA-256 `{item['source_span_sha256']}`); "
        f"strength candidate: **{item['strength_candidate']}**",
    ]


def _render_section(lines: list[str], title: str, section: dict[str, Any], *, zero: str) -> None:
    if title:
        lines.append(f"### {title}")
    if not section["candidate_count"]:
        lines.extend([zero, ""])
        return
    for item in section["visible"]:
        lines.extend(_original_and_english_lines(item))
    if section["more_in_source_drilldown"]:
        lines.append(
            f"- **{section['more_in_source_drilldown']} additional source-linked candidate "
            "items in full drilldown, not assessed here.**"
        )
    lines.append("")


def _render_graph_node(node: dict[str, Any], depth: int = 0) -> list[str]:
    prefix = "  " * depth
    if node["kind"] in {"any_of", "all_of"}:
        marker = "OR" if node["kind"] == "any_of" else "AND"
        lines = [f"{prefix}- Candidate **{marker}** (not independently verified)"]
        for child in node["children"]:
            lines.extend(_render_graph_node(child, depth + 1))
        return lines
    if node["kind"] == "original_subspan":
        return [
            f"{prefix}- Original child: {markdown_escape(node['original_text'])} "
            "(independent English child alignment **not established**; "
            f"parent source `{markdown_escape(node['parent_source_item_id'])}`)"
        ]
    return [
        f"{prefix}- Original: {markdown_escape(node['original_text'])} "
        f"(source `{markdown_escape(node['source_item_id'])}`)"
    ]


def render_compact_decision_views(views: list[dict[str, Any]]) -> str:
    if len({v["source_job_id"] for v in views}) != len(views):
        raise ValueError("B4v6 duplicate source job")
    lines = [
        "# B4v6 — compact decision-first job reading (exposed research only)",
        "",
        "**Original job statements are authoritative; English is an unverified reading aid.** "
        "All categories, strength labels and eligibility paths are unaccepted candidates. "
        "Open full source drilldown before application decisions. "
        "No production facts are promoted.",
        "",
    ]
    for view in views:
        if view["contract"] != COMPACT_CONTRACT or view["accepted_employer_facts"] != 0:
            raise ValueError("B4v6 render input authority mismatch")
        sections = view["sections"]
        lines.extend([f"## {markdown_escape(view['source_job_id'])}", ""])
        _render_section(
            lines,
            "1. What would I do?",
            sections["what_work"],
            zero=(
                "No separately extracted explicit duty candidate in this source view. "
                "**This does not establish that the job has no responsibilities.**"
            ),
        )
        lines.append("### 2. What capabilities are expected?")
        lines.append("**Required candidates (not employer-verified):**")
        _render_section(
            lines,
            "",
            sections["capabilities"]["required_candidate"],
            zero="None explicitly tagged as required; unknown is not absent.",
        )
        lines.append("**Preferred/advantage candidates:**")
        _render_section(
            lines,
            "",
            sections["capabilities"]["preferred_candidate"],
            zero="No selected preferred candidate.",
        )
        lines.append("**Other, behavioral or unresolved candidates:**")
        _render_section(
            lines,
            "",
            sections["capabilities"]["other_or_unresolved_candidate"],
            zero="No additional candidate shown.",
        )
        lines.append("### 3. Are there options or alternative eligibility routes?")
        graphs = sections["eligibility"]["unreviewed_candidate_graphs"]
        if not graphs:
            lines.append(
                "No *reviewed, source-linked candidate eligibility graph* available in "
                "this view. This is not evidence that the employer has no options."
            )
        else:
            for graph in graphs:
                lines.append(
                    f"**Unreviewed source candidate** `{markdown_escape(graph['graph_id'])}`: "
                    "not an accepted employer eligibility condition."
                )
                lines.extend(_render_graph_node(graph["root"]))
        lines.append("")
        _render_section(
            lines,
            "4. What conditions should I inspect?",
            sections["conditions"],
            zero=(
                "No candidate instruction/arrangement in this first view; inspect original posting."
            ),
        )
        lines.append(
            f"**Inspection flags:** {view['default_visible_evidence_item_count']} "
            f"of {view['source_qualified_item_count']} source-qualified candidates in "
            "the default evidence view; "
            f"{view['excluded_source_item_count']} source items excluded/untranslated; "
            f"{view['candidate_only_unresolved_item_count']} unresolved-category candidates; "
            f"{view['suppressed_prior_model_claim_count']} prior model claims withheld; "
            f"B4 outcome `{markdown_escape(view['b4_model_outcome'])}`. "
            "Other source categories and all evidence remain in full drilldown. "
            "**No claims of complete job coverage, accurate translation, or user benefit.**"
        )
        lines.append("")
    return "\n".join(lines) + "\n"


__all__ = [
    "COMPACT_CONTRACT",
    "build_compact_decision_view",
    "render_compact_decision_views",
]
