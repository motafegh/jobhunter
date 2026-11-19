"""P1.6 B4v5: source-qualified vacancy projection over frozen B4 candidate evidence.

This read-only presentation layer does not call an LLM, mutate B2/B3/v30/v9,
convert candidate labels into employer facts, or infer item-level translated
offsets for nested alternative spans.
"""

from __future__ import annotations

import hashlib
import html
import json
from typing import Any


def digest_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json_sha(value: Any) -> str:
    return digest_text(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def apply_reviewed_translation_overlay(
    *, candidate: dict[str, Any], correction: dict[str, Any] | None
) -> dict[str, dict[str, Any]]:
    """Validate an item-specific translation revision without modifying B3."""
    if correction is None:
        return {}
    version = candidate["source_version"]
    if correction.get("source_job_id") != version["source_job_id"]:
        raise ValueError("Reviewed translation overlay has different source job identity")
    item_matches = [
        item for item in candidate["items"] if item["item_id"] == correction.get("source_item_id")
    ]
    if len(item_matches) != 1:
        raise ValueError("Reviewed translation overlay source item is missing or duplicated")
    item = item_matches[0]
    original = item["translation"]
    if original is None or item["excluded_reason"] is not None:
        raise ValueError("Reviewed translation overlay cannot target an excluded source item")
    expected = {
        "source_span_sha256": item["source_span_sha256"],
        "original_target_sha256": original["target_sha256"],
        "source_semantic_sha256": version["semantic_sha256"],
    }
    for key, value in expected.items():
        if correction.get(key) != value:
            raise ValueError(f"Reviewed translation overlay identity mismatch: {key}")
    source_token = correction.get("source_token")
    wrong = correction.get("old_target_token")
    replacement = correction.get("reviewed_target_token")
    reviewed = correction.get("reviewed_target_text")
    if not all(
        isinstance(text, str) and text for text in (source_token, wrong, replacement, reviewed)
    ):
        raise ValueError("Reviewed translation overlay has blank revision metadata")
    if correction.get("reviewer") != "assistant_original_source_terminology_review":
        raise ValueError("Reviewed translation overlay has unknown review authority")
    if source_token not in item["original_text"]:
        raise ValueError("Reviewed source token is not contained in the original quote")
    if original["target_text"].count(wrong) != 1:
        raise ValueError("Candidate target does not contain exactly one specified wrong token")
    if original["target_text"].replace(wrong, replacement, 1) != reviewed:
        raise ValueError("Review changed more than the declared terminology token")
    if digest_text(reviewed) != correction.get("reviewed_target_sha256"):
        raise ValueError("Reviewed target hash mismatch")
    if reviewed == original["target_text"]:
        raise ValueError("Reviewed overlay is not a material revision")
    return {
        item["item_id"]: {
            "target_text": reviewed,
            "target_sha256": correction["reviewed_target_sha256"],
            "b3_original_target_sha256": original["target_sha256"],
            "review_state": "assistant_reviewed_original_source_terminology_overlay",
            "overlay_source_sha256": item["source_span_sha256"],
            "reviewer": correction["reviewer"],
            "source_token": source_token,
        }
    }


def project_eligibility_graph(
    graph: dict[str, Any],
    *,
    source_by_id: dict[str, dict[str, Any]],
    nested_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Make B2's OR/AND graph readable without translating nested source spans."""
    nodes = {node["id"]: node for node in graph["nodes"]}
    if len(nodes) != len(graph["nodes"]):
        raise ValueError("Eligibility graph contains duplicate node IDs")

    def branch(node_id: str, active: frozenset[str]) -> dict[str, Any]:
        if node_id not in nodes or node_id in active:
            raise ValueError("Eligibility graph has unknown nodes or cycles")
        node = nodes[node_id]
        op = node["operator"]
        if op in {"any_of", "all_of"}:
            children = node.get("children", [])
            if not children:
                raise ValueError("Eligibility operator lacks branches")
            return {
                "kind": op,
                "node_label": node_id,
                "children": [branch(child, active | {node_id}) for child in children],
            }
        if op != "item":
            raise ValueError("Unexpected eligibility graph operator")
        source_id = node["item_id"]
        nested = nested_by_id.get(source_id)
        if nested is not None:
            if nested["target_subspan_alignment"] != "not_established":
                raise ValueError("Nested eligibility child unexpectedly has translated offset")
            if digest_text(nested["source_text"]) != nested["leaf_text_sha256"]:
                raise ValueError("Nested original-language source span SHA does not match")
            parent_id = nested["parent_item_id"]
            if parent_id not in source_by_id:
                raise ValueError("Nested eligibility parent is missing")
            return {
                "kind": "original_subspan",
                "node_label": node_id,
                "source_item_id": source_id,
                "original_text": nested["source_text"],
                "parent_source_item_id": parent_id,
                "parent_english_candidate": source_by_id[parent_id]["target_text_candidate"],
                "child_english_alignment": "not_established",
            }
        if source_id not in source_by_id:
            raise ValueError("Eligibility graph references an unknown source item")
        item = source_by_id[source_id]
        return {
            "kind": "whole_item",
            "node_label": node_id,
            "source_item_id": source_id,
            "original_text": item["original_text"],
            "english_candidate": item["target_text_candidate"],
        }

    root = branch(graph["root_id"], frozenset())
    if root["kind"] not in {"any_of", "all_of"}:
        raise ValueError("Eligibility graph root must be an operator")
    return {
        "graph_id": graph["graph_id"],
        "review_state": graph.get("review_state"),
        "root": root,
        "authority": "B2_candidate_structure_not_accepted_employer_eligibility",
    }


def project_source_qualified_case(
    case: dict[str, Any], *, correction: dict[str, Any] | None = None
) -> dict[str, Any]:
    evidence = case["candidate"]
    job_id = case["source_job_id"]
    if evidence["source_version"]["source_job_id"] != job_id:
        raise ValueError("B4 case identity changed")
    overlays = apply_reviewed_translation_overlay(candidate=evidence, correction=correction)
    qualified: list[dict[str, Any]] = []
    candidates_by_id: dict[str, dict[str, Any]] = {}
    for item in evidence["items"]:
        if item["item_id"] in candidates_by_id:
            raise ValueError("Duplicate B4 item IDs")
        entry = None
        translation = item["translation"]
        if translation is not None:
            checked_overlay = overlays.get(item["item_id"])
            entry = {
                "source_item_id": item["item_id"],
                "category_candidate": item["category_candidate"],
                "strength_candidate": item["strength_candidate"],
                "qualifier_candidate": item["qualifier_candidate"],
                "evidence_basis_candidate": item["evidence_basis_candidate"],
                "original_text": item["original_text"],
                "source_span_sha256": item["source_span_sha256"],
                "target_text_candidate": (
                    checked_overlay["target_text"]
                    if checked_overlay
                    else translation["target_text"]
                ),
                "b3_selected_target_sha256": translation["target_sha256"],
                "translation_review_state": (
                    checked_overlay["review_state"]
                    if checked_overlay
                    else translation["review_state"]
                ),
                "b4_reviewed_terminology_overlay": checked_overlay,
                "authority": "B2_B3_source_qualified_candidate_not_accepted_fact",
            }
            qualified.append(entry)
        candidates_by_id[item["item_id"]] = (
            entry
            if entry
            else {
                "source_item_id": item["item_id"],
                "original_text": item["original_text"],
                "category_candidate": item["category_candidate"],
                "excluded_reason": item["excluded_reason"],
                "target_text_candidate": None,
            }
        )

    graph_data = []
    nested = {item["leaf_item_id"]: item for item in evidence["nested_eligibility_items"]}
    if len(nested) != len(evidence["nested_eligibility_items"]):
        raise ValueError("Duplicate nested eligibility leaves")
    for graph in evidence["eligibility_graphs"]:
        graph_data.append(
            project_eligibility_graph(graph, source_by_id=candidates_by_id, nested_by_id=nested)
        )

    linked_alternative_parents = set()
    for nested_item in nested.values():
        linked_alternative_parents.add(nested_item["parent_item_id"])
    for item in qualified:
        item["in_eligibility_alternative_candidate"] = (
            item["source_item_id"] in linked_alternative_parents
        )
        item["is_conditional_application_statement"] = (
            item["category_candidate"] == "application_instruction"
            and item["evidence_basis_candidate"] == "explicit_original_wording"
        )
    groups: dict[str, list[dict[str, Any]]] = {}
    for item in qualified:
        groups.setdefault(item["category_candidate"], []).append(item)

    # V4 model interpretation has never been semantically accepted. Its claims
    # citing a reviewed translation error cannot be shown alongside a corrected
    # original-source item.
    model = evidence["brief"]
    suppressed = []
    visible_model: dict[str, Any] | None = None
    if model is not None:
        visible_model = {"role_summary": model["role_summary"]}
        if set(model["role_summary"]["source_item_ids"]) & set(overlays):
            suppressed.append("role_summary")
            visible_model["role_summary"] = None
        for section in (
            "work_activities",
            "expectation_summaries",
            "work_implied_capabilities",
            "open_questions",
        ):
            visible = []
            for idx, claim in enumerate(model[section]):
                if set(claim["source_item_ids"]) & set(overlays):
                    suppressed.append(f"{section}[{idx}]")
                else:
                    visible.append(claim)
            visible_model[section] = visible

    return {
        "contract": "jobhunter-p16-b4-source-qualified-projection-v5",
        "source_job_id": job_id,
        "source_version": evidence["source_version"],
        "b4_analysis_outcome": evidence["analysis_outcome"],
        "b4_attempt_outcome": case["attempt_outcome"],
        "source_qualified_items": qualified,
        "source_item_count": len(evidence["items"]),
        "excluded_source_item_count": len(evidence["items"]) - len(qualified),
        "groups": groups,
        "eligibility_alternative_candidates": graph_data,
        "metadata_conflict_candidates": evidence["conflicts"],
        "board_metadata_value_count": len(evidence["board_values"]),
        "corrected_translation_item_ids": sorted(overlays),
        "v4_model_candidates": visible_model,
        "v4_model_claims_suppressed_due_to_translation_review": suppressed,
        "review_state": "assistant_exposed_source_qualified_projection_not_independent",
        "accepted_employer_facts": 0,
        "downstream_authority": "none",
        "unseen_generalization_established": False,
    }


def markdown_escape(value: str) -> str:
    result = html.escape(value, quote=False)
    for ch in ("\\", "\x60", "*", "_", "[", "]", "(", ")", "#", "+", "-", ".", "!", "|", "{", "}"):
        result = result.replace(ch, "\\" + ch)
    return result.replace("\n", " ")


def _graph_lines(node: dict[str, Any], depth: int = 0) -> list[str]:
    pad = "  " * depth
    if node["kind"] in {"any_of", "all_of"}:
        relation = "ONE OF (OR)" if node["kind"] == "any_of" else "ALL OF (AND)"
        lines = [f"{pad}- **{relation}** — {markdown_escape(node['node_label'])}"]
        for child in node["children"]:
            lines.extend(_graph_lines(child, depth + 1))
        return lines
    if node["kind"] == "original_subspan":
        return [
            f"{pad}- {markdown_escape(node['original_text'])} "
            f"(original source subspan: {node['source_item_id']}; "
            f"parent: {node['parent_source_item_id']}; "
            "independent English child alignment NOT ESTABLISHED)"
        ]
    return [
        f"{pad}- {markdown_escape(node['english_candidate'])} (source: {node['source_item_id']})"
    ]


def render_source_qualified_briefs(projections: list[dict[str, Any]]) -> str:
    lines = [
        "# B4 v5 — source-qualified job understanding (four exposed development ads)",
        "",
        "Research-only: B2 categories/strength are candidates, not accepted employer facts. "
        "B3 translations are reading aids; original-language quotes remain authoritative. "
        "Model interpretations remain non-authoritative.",
        "",
    ]
    for projection in projections:
        lines.extend(
            [
                f"## {projection['source_job_id']}",
                "",
                f"**Previous B4 outcome:** {projection['b4_analysis_outcome']}. "
                "Selected source facts remain visible, including any omitted "
                "or rejected by the model.",
                "",
            ]
        )
        groups = projection["groups"]
        duty_count = len(groups.get("work_duty", []))
        qualification_count = len(groups.get("candidate_qualification", []))
        behavioral_count = len(groups.get("behavioral_expectation", []))
        lines.extend(
            [
                "### At a glance — original-source-qualified candidates",
                f"- Explicit duty statements: **{duty_count}** "
                "(no duties means do not infer a task list)",
                f"- Applicant qualification items: **{qualification_count}**; "
                f"behavioral expectation items: **{behavioral_count}**",
            ]
        )
        if projection["eligibility_alternative_candidates"]:
            for graph in projection["eligibility_alternative_candidates"]:
                root = graph["root"]
                branch_names = ", ".join(
                    markdown_escape(child["node_label"]) for child in root["children"]
                )
                lines.append(
                    f"- **Eligibility path candidate: ONE OF (OR)** {branch_names}. "
                    "Do not combine the alternative branches into cumulative requirements."
                )
        selected = [
            item
            for item in projection["source_qualified_items"]
            if item["strength_candidate"] == "preferred"
            or item["in_eligibility_alternative_candidate"]
            or item["is_conditional_application_statement"]
            or item["b4_reviewed_terminology_overlay"]
        ]
        if not selected:
            selected = groups.get("candidate_qualification", [])[:3]
        if selected:
            lines.append("- **Important source-qualified details:**")
            for item in selected[:7]:
                label = markdown_escape(item["strength_candidate"])
                lines.append(
                    f"  - {markdown_escape(item['target_text_candidate'])} "
                    f"(B2 strength: {label}; source: {item['source_item_id']})"
                )
            if len(selected) > 7:
                lines.append(f"  - {len(selected) - 7} additional source items indexed below")
        lines.append("")
        sections = (
            ("work_duty", "Explicit work-duty candidates"),
            ("candidate_qualification", "Source-qualified applicant capabilities/requirements"),
            ("behavioral_expectation", "Behavioral expectations"),
            ("application_instruction", "Application and acceptance conditions"),
            ("work_arrangement", "Work arrangement"),
            ("compensation", "Compensation"),
            ("benefit", "Benefits"),
        )
        for category, title in sections:
            items = projection["groups"].get(category, [])
            if not items:
                continue
            lines.append(f"### {title}")
            for item in items:
                role = (
                    "; alternative-track source candidate, not cumulative"
                    if item["in_eligibility_alternative_candidate"]
                    else ""
                )
                original = markdown_escape(item["original_text"])
                translation = markdown_escape(item["target_text_candidate"])
                label = markdown_escape(item["strength_candidate"])
                lines.extend(
                    [
                        f"- **{translation}** (source: {item['source_item_id']}; "
                        f"B2 strength candidate: {label}{role})",
                        f"  - Original: {original}",
                    ]
                )
                if item["b4_reviewed_terminology_overlay"]:
                    lines.append(
                        "  - **Reviewed candidate terminology correction**: "
                        "prior B3 translation retained unchanged for audit"
                    )
            lines.append("")
        graphs = projection["eligibility_alternative_candidates"]
        if graphs:
            lines.extend(
                [
                    "### Alternative eligibility paths (B2 graph candidates)",
                    "These represent source-qualified OR/AND paths, not cumulative requirements or "
                    "accepted employer policy. Original nested spans are displayed without "
                    "inventing independent English child translations.",
                ]
            )
            for graph in graphs:
                lines.append(f"**{markdown_escape(graph['graph_id'])}:**")
                lines.extend(_graph_lines(graph["root"]))
                lines.append("")
        if projection["v4_model_candidates"] is not None:
            model = projection["v4_model_candidates"]
            if model["role_summary"]:
                lines.extend(
                    [
                        "### Earlier model interpretation (unapproved)",
                        markdown_escape(model["role_summary"]["summary"]),
                        "",
                    ]
                )
            if projection["v4_model_claims_suppressed_due_to_translation_review"]:
                lines.append(
                    "The previous model response contained references to a revised translation. "
                    "Those generated claims were withheld from this source-first projection."
                )
                lines.append("")
        else:
            lines.extend(
                [
                    "No validated earlier model interpretation. Source-owned items above "
                    "remain available without inventing work responsibilities.",
                    "",
                ]
            )
        lines.extend(["---", ""])
    return "\n".join(lines)
