"""Validate draft Stage B1 evidence-contract examples; not a production analysis route.

Only structural and referential checks are possible on public source-safe JSON.
An optional exact original-source object can additionally prove span/metadata
identity; this does NOT prove semantic classification or translation fidelity.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from jobhunter.source_span_identity import (
    align_legacy_english_field,
    bind_original_source_span,
    verify_original_source_anchor,
)
from jobhunter.translation_store import TranslationArtifact, TranslationSourceVersion

_SCHEMA = (
    Path(__file__).resolve().parents[1]
    / "docs/contracts/p16-stage-b1/source_evidence_bundle.schema.json"
)


def _digest(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def _assert(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def _selected_value(source: TranslationSourceVersion, selector: str) -> Any:
    # JSON Pointer over the *original* parsed fields; no object-key evaluation.
    parts = selector.split("/")[1:]
    result: Any = source.fields
    for token in parts:
        # RFC 6901: only ~0 and ~1 escapes are valid, not arbitrary "~n".
        _assert(not re.search(r"~(?![01])", token), "Invalid JSON Pointer escape")
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(result, dict):
            _assert(token in result, "Unknown structured board selector")
            result = result[token]
        elif isinstance(result, list):
            _assert(
                token == "0"
                or (token.isascii() and token.isdecimal() and not token.startswith("0")),
                "Noncanonical structured list selector",
            )
            index = int(token)
            _assert(0 <= index < len(result), "Structured list selector out of range")
            result = result[index]
        else:
            raise ValueError("Structured selector traverses scalar value")
    return result


def _validate_nodes(
    nodes: dict[str, dict[str, Any]],
    root_id: str,
    items: dict[str, dict[str, Any]],
) -> None:
    visited: set[str] = set()
    active: set[str] = set()

    def check_node(nid: str) -> None:
        _assert(nid in nodes, "Unknown alternative eligibility child")
        _assert(nid not in active, "Cycle in eligibility AND/OR graph")
        if nid in visited:
            return
        active.add(nid)
        node = nodes[nid]
        if node["operator"] == "item":
            iid = node["item_id"]
            _assert(iid in items, "Alternative eligibility leaf has unknown source")
            _assert(
                items[iid]["meaning"]["category"] == "candidate_qualification",
                "Only candidate qualifications may be eligibility leaves",
            )
            _assert(
                items[iid]["source_ref"]["kind"] == "original_description_span",
                "Board metadata alone cannot define employer eligibility",
            )
            _assert(
                items[iid]["meaning"]["employer_strength"] == "required",
                "Eligibility leaf must represent a source-required qualification",
            )
            _assert(
                items[iid]["meaning"]["scope"] in {"alternative_path", "chosen_option"},
                "Alternative graph leaf must not become unconditional requirement",
            )
        else:
            for child in node["children"]:
                check_node(child)
        active.remove(nid)
        visited.add(nid)

    check_node(root_id)
    _assert(set(nodes) == visited, "Unreachable eligibility graph nodes")


def evaluate_eligibility_truth_table(
    graph: dict[str, Any], satisfied_item_ids: set[str]
) -> bool:
    """Pure Boolean design-proof helper, NOT an applicant matcher.

    Requires the caller to validate the bundle graph first. This evaluates
    only the stated AND/OR topology on synthetic truth assignments.
    """
    nodes = {x["id"]: x for x in graph["nodes"]}

    def value(nid: str) -> bool:
        node = nodes[nid]
        if node["operator"] == "item":
            return node["item_id"] in satisfied_item_ids
        if node["operator"] == "all_of":
            return all(value(child) for child in node["children"])
        return any(value(child) for child in node["children"])

    return value(graph["root_id"])


def validate_bundle(
    bundle: dict[str, Any],
    *,
    source: TranslationSourceVersion | None = None,
    translation: TranslationArtifact | None = None,
) -> None:
    """Reject broken draft identities/relations without assigning employer truth."""
    schema = json.loads(_SCHEMA.read_text())
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors(bundle))
    if errors:
        raise ValueError(f"B1 schema violation: {errors[0].message}")

    version = bundle["source_version"]
    items: dict[str, dict[str, Any]] = {}
    for item in bundle["items"]:
        iid = item["item_id"]
        _assert(iid not in items, "Duplicate item identifier")
        items[iid] = item
        ref, meaning = item["source_ref"], item["meaning"]
        cat, strength, basis, qualifier, scope = (
            meaning["category"],
            meaning["employer_strength"],
            meaning["basis"],
            meaning["qualifier_status"],
            meaning["scope"],
        )
        if strength != "required":
            _assert(
                scope in {"standalone", "not_applicable"},
                "Alternative-path scope must belong to source-required qualification",
            )
        if scope in {"alternative_path", "chosen_option"}:
            _assert(
                cat == "candidate_qualification" and strength == "required",
                "Conditional eligibility scope cannot be a global employer demand",
            )

        if ref["kind"] == "structured_board_value":
            _assert(
                ref["selector"] == "/" + ref["field_path"]
                or ref["selector"].startswith("/" + ref["field_path"] + "/"),
                "Board field reference does not match selector",
            )
            _assert(
                basis == "board_metadata_only",
                "Board field cannot masquerade as original employer prose",
            )
            _assert(
                strength in {"not_applicable", "unresolved"},
                "Board metadata cannot independently establish employer obligation",
            )
            _assert(
                qualifier in {"unresolved", "not_applicable"},
                "Board tags cannot prove a mandatory or optional source cue",
            )
            _assert(
                scope == "not_applicable",
                "Board tags cannot create an employer qualification scope",
            )
        else:
            _assert(
                ref["char_end"] > ref["char_start"],
                "Original text offset range is invalid",
            )
            _assert(
                basis != "board_metadata_only",
                "Original description span cannot be labeled board-only",
            )
            _assert(
                ref["kind"] == "original_description_span",
                "Unknown original source reference kind",
            )

        if cat not in {"candidate_qualification", "behavioral_expectation"}:
            _assert(
                strength in {"not_applicable", "unresolved"},
                "Employer obligation on nonqualification category",
            )
        if cat != "behavioral_expectation":
            _assert(
                strength != "stated_expectation",
                "Stated behavioral expectation only applies to behavior",
            )
        _assert(
            not (strength == "required" and qualifier == "negative_explicit"),
            "Negative explicit source wording cannot support required employer skill",
        )
        _assert(
            not (
                strength == "required"
                and basis in {"candidate_semantic_inference", "unresolved"}
            ),
            "Inferred/unknown semantics cannot claim explicit employer requirement",
        )
        if source is not None:
            _assert(
                source.source_job_id == version["source_job_id"]
                and source.job_detail_version_id == version["job_detail_version_id"]
                and source.semantic_sha256 == version["semantic_sha256"],
                "Stale original source version",
            )
            if ref["kind"] == "original_description_span":
                anchor = bind_original_source_span(
                    source, char_start=ref["char_start"], char_end=ref["char_end"]
                )
                verify_original_source_anchor(anchor, source)
                _assert(
                    anchor.anchor_id == ref["anchor_id"]
                    and anchor.field_sha256 == ref["field_sha256"]
                    and anchor.text_sha256 == ref["text_sha256"],
                    "Original source anchor does not match exact source text",
                )
            else:
                _assert(
                    ref["field_path"] in source.fields,
                    "Board field absent from parsed source",
                )
                _assert(
                    _digest(source.fields[ref["field_path"]])
                    == ref["field_json_sha256"],
                    "Board field digest is stale",
                )
                _assert(
                    _digest(_selected_value(source, ref["selector"]))
                    == ref["selected_value_json_sha256"],
                    "Selected board value digest does not match",
                )
                _assert(
                    (
                        ref["selector"] == "/" + ref["field_path"]
                        or ref["selector"].startswith("/" + ref["field_path"] + "/")
                    ),
                    "Board JSON selector points outside declared field",
                )

    if translation is not None:
        _assert(source is not None, "Need original source to verify translation identity")
        _assert(
            translation.source_job_id == version["source_job_id"]
            and translation.job_detail_version_id == version["job_detail_version_id"]
            and translation.source_semantic_sha256 == version["semantic_sha256"],
            "Translation bound to another source version",
        )

    align_keys: set[tuple[str, str, str | None]] = set()
    for alignment in bundle["alignments"]:
        iid, state, target = (
            alignment["source_item_id"],
            alignment["state"],
            alignment["target"],
        )
        _assert(iid in items, "Alignment refers to unknown source item")
        ref = items[iid]["source_ref"]
        _assert(
            ref["kind"] == "original_description_span",
            "Board field cannot be aligned as an employer-description item",
        )
        key = (iid, state, target["translation_sha256"] if target else None)
        _assert(key not in align_keys, "Duplicate source-to-translation relation")
        align_keys.add(key)
        if state in {"legacy_field_only_unaligned", "unresolved"}:
            _assert(target is None, "Unaligned evidence cannot invent English offsets")
        if state == "legacy_field_only_unaligned":
            _assert(
                alignment["translation_artifact_id"] is not None
                and alignment["translation_sha256"] is not None
                and alignment["meaning_review"] == "unreviewed",
                "Legacy field alignment does not prove item meaning",
            )
        if state in {"native_english_exact", "source_bound_translation_candidate"}:
            _assert(target is not None, "Exact/bound alignment must reference target")
            _assert(
                target["target_span"]["char_end"] > target["target_span"]["char_start"],
                "Target span offsets are invalid",
            )
            wanted = (
                "native_exact_v2"
                if state == "native_english_exact"
                else "source_bound_item_output"
            )
            _assert(
                target["target_kind"] == wanted,
                "Alignment state does not match its target authority",
            )
            _assert(
                target["translation_sha256"] == alignment["translation_sha256"],
                "Alignment and translation output SHA mismatch",
            )
            if state == "source_bound_translation_candidate":
                _assert(
                    alignment["translation_artifact_id"] is None,
                    "Unpersisted source-bound candidate cannot claim existing translation ID",
                )
        if state == "native_english_exact":
            _assert(
                target["translation_artifact_id"]
                == alignment["translation_artifact_id"],
                "Native projection artifact dependency mismatch",
            )
        if state == "semantic_mismatch":
            _assert(target is not None, "Mismatched translation needs an exact target")
            _assert(
                alignment["meaning_review"] == "contradicted",
                "Semantic mismatch must not be marked reviewed-equivalent",
            )
        if translation is not None and state in {
            "legacy_field_only_unaligned", "native_english_exact"
        }:
            _assert(
                alignment["translation_artifact_id"] == translation.id
                and alignment["translation_sha256"] == translation.translation_sha256,
                "Legacy projection dependency mismatch",
            )
            assert source is not None
            a = bind_original_source_span(
                source, char_start=ref["char_start"], char_end=ref["char_end"]
            )
            legacy = align_legacy_english_field(a, source, translation)
            expected_legacy = (
                "translated_field_only_unaligned"
                if state == "legacy_field_only_unaligned"
                else "native_english_exact"
            )
            _assert(
                legacy.state == expected_legacy,
                "Claimed alignment state not supported by translation v2",
            )
            if state == "native_english_exact":
                target_span = target["target_span"]
                _assert(
                    target_span["char_start"] == legacy.english_char_start
                    and target_span["char_end"] == legacy.english_char_end
                    and target_span["text_sha256"] == ref["text_sha256"],
                    "Native-English exact target identity not preserved",
                )

    all_graph_ids: set[str] = set()
    graph_referenced_items: set[str] = set()
    for graph in bundle["eligibility_graphs"]:
        gid = graph["graph_id"]
        _assert(gid not in all_graph_ids, "Duplicate eligibility graph ID")
        all_graph_ids.add(gid)
        for basis in graph["basis_item_ids"]:
            graph_referenced_items.add(basis)
            _assert(basis in items, "Alternative group lacks qualifier source item")
            _assert(
                items[basis]["source_ref"]["kind"] == "original_description_span",
                "Alternative group qualifier requires original source",
            )
        nodes: dict[str, dict[str, Any]] = {}
        for node in graph["nodes"]:
            nid = node["id"]
            _assert(nid not in nodes, "Duplicate eligibility graph node ID")
            nodes[nid] = node
        _assert(graph["root_id"] in nodes, "Missing eligibility root")
        _validate_nodes(nodes, graph["root_id"], items)
        graph_referenced_items.update(
            node["item_id"] for node in nodes.values() if node["operator"] == "item"
        )
    for iid, item in items.items():
        if item["meaning"]["scope"] in {"alternative_path", "chosen_option"}:
            _assert(
                iid in graph_referenced_items,
                "Conditional source requirement needs explicit eligibility group ownership",
            )

    for c in bundle["conflicts"]:
        _assert(
            c["item_id_a"] in items and c["item_id_b"] in items,
            "Conflict references unknown source item",
        )
        _assert(c["item_id_a"] != c["item_id_b"], "Self-conflict is invalid")
        if c["type"].startswith("board_vs_employer"):
            kinds = {
                items[c[k]]["source_ref"]["kind"]
                for k in ("item_id_a", "item_id_b")
            }
            _assert(
                kinds == {"original_description_span", "structured_board_value"},
                "Board-vs-prose conflict must preserve each original source",
            )

    review_ids: set[str] = set()
    review_dimensions: dict[str, tuple[str, str]] = {}
    independent_items: set[str] = set()
    assistant_checked_items: set[str] = set()
    for e in bundle["review_events"]:
        event_id = e["event_id"]
        _assert(event_id not in review_ids, "Duplicate append-only review event ID")
        _assert(e["item_id"] in items, "Review event refers to unknown item")
        reviewer, finding, dimension = (
            e["reviewer_kind"],
            e["finding"],
            e["dimension"],
        )
        if reviewer == "assistant_prior_context_exposed":
            _assert(
                finding != "independently_checked",
                "Assistant review cannot impersonate independent review",
            )
        if finding == "assistant_checked":
            _assert(
                reviewer == "assistant_prior_context_exposed",
                "Assistant-check status requires accurate assistant reviewer provenance",
            )
            if dimension == "semantic_classification":
                assistant_checked_items.add(e["item_id"])
        if finding == "independently_checked":
            _assert(
                reviewer in {"owner", "independent_human"},
                "Independent check requires independent reviewer provenance",
            )
            if dimension == "semantic_classification":
                independent_items.add(e["item_id"])
        if dimension == "downstream_authorization":
            _assert(
                finding == "not_authorized",
                "B1 draft events cannot promote durable authority",
            )
        expected_evidence = items[e["item_id"]]["source_ref"]
        evidence_sha = (
            expected_evidence["text_sha256"]
            if expected_evidence["kind"] == "original_description_span"
            else expected_evidence["selected_value_json_sha256"]
        )
        _assert(
            e["evidence_digest"] == evidence_sha,
            "Review event must cite exact item evidence digest",
        )
        if dimension == "original_source_integrity" and finding == "valid":
            _assert(
                reviewer == "deterministic_verifier",
                "Original source validity needs deterministic verifier",
            )
        previous_id = e["previous_event_id"]
        if previous_id is not None:
            _assert(
                previous_id in review_ids,
                "Review event predecessor must already exist",
            )
            _assert(
                review_dimensions[previous_id] == (e["item_id"], dimension),
                "Review event cannot replace a different item/dimension",
            )
        review_ids.add(event_id)
        review_dimensions[event_id] = (e["item_id"], dimension)

    for iid, item in items.items():
        if item["semantic_review"] == "independent_source_checked":
            _assert(
                iid in independent_items,
                "Independent item state must have independent review event",
            )
        if item["semantic_review"] == "assistant_checked_context_exposed":
            _assert(
                iid in assistant_checked_items,
                "Assistant-checked item needs explicit provenance-bearing review event",
            )

    brief = bundle["brief"]
    selected = set(brief["selected_item_ids"])
    unknown = set(brief["unresolved_item_ids"])
    _assert(
        not (selected & unknown), "Selected factual items cannot be unresolved"
    )
    _assert(
        (selected | unknown) <= set(items),
        "Candidate brief refers to missing source items",
    )
    for iid in selected:
        item = items[iid]
        _assert(
            item["source_ref"]["kind"] == "original_description_span",
            "Brief cannot promote board metadata to employer-fact item",
        )
        _assert(
            item["meaning"]["category"] != "unresolved"
            and item["meaning"]["employer_strength"] != "unresolved",
            "Unresolved source claims must remain outside qualified brief",
        )
        _assert(
            item["semantic_review"] != "rejected",
            "Rejected item cannot become a factual brief claim",
        )
    for iid in unknown:
        _assert(
            items[iid]["meaning"]["employer_strength"] == "unresolved"
            or items[iid]["meaning"]["category"] == "unresolved",
            "Unknown slot requires an unresolved item",
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundles", nargs="+", type=Path)
    args = parser.parse_args()
    for filename in args.bundles:
        document = json.loads(filename.read_text())
        validate_bundle(document)
        print("B1_DRAFT_SCHEMA_AND_GRAPH_VALID", filename)
