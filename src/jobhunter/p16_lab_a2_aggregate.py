"""A2 run-local fragment aggregation and bounded repair selection.

Never infer semantic equivalence or resolve a reference across request namespaces.
"""

from __future__ import annotations

from collections import defaultdict

from jobhunter.p16_lab import canonical, digest


def _identity(value):
    return digest(canonical(value))


def _relation_signature(record, relation):
    # Keep ordered/nested topology, not merely the unordered set of leaves.
    claims = {ref: c["content_sha256"] for c in record["claims"] for ref in c["local_refs"]}
    groups = {r["local_ref"]: r for r in record["relations"] if r["local_ref"] is not None}

    def node(ref, trail):
        if ref in claims:
            return {"claim": claims[ref]}
        if ref in trail or ref not in groups:
            return {"unresolved_local_ref": ref}
        return shape(groups[ref], trail | {ref})

    def shape(r, trail):
        content = r["content"]
        result = {k: v for k, v in content.items() if k not in {"ref", "members", "from", "to"}}
        if "members" in content:
            result["members"] = [node(ref, trail) for ref in content["members"]]
        else:
            result["from"] = node(content["from"], trail)
            result["to"] = node(content["to"], trail)
        return result

    return _identity(shape(relation, set()))


def choose_repair(records, requests, *, remaining_posts):
    """First concrete recoverable parsed defect, one bounded repair for this run.

    No retry of malformed whole response, uncertain transport, board-only proposal,
    missing coverage without an identified defect, or merely low-quality meaning.
    """
    if remaining_posts <= 0 or len(records) != len(requests):
        return None
    if any(r["execution"] != "completed" for r in records):
        return None
    for record, request in zip(records, requests, strict=True):
        if record["scope"] != request["scope"]:
            raise ValueError("fragment scope mismatch")
        # Avoid blanket retries of whole advertisement; only a partition with
        # concrete bad references / relation structure is recoverable here.
        if request.get("whole_context") or not record["quarantine"]:
            continue
        if not request["primary"]:
            continue
        return {
            "parent_ordinal": record["scope"]["request_ordinal"],
            "parent_revision_sha256": record["revision_sha256"],
            "primary": list(request["primary"]),
            "issues": [
                {k: q[k] for k in ("kind", "index", "ref", "reason")} for q in record["quarantine"]
            ],
        }
    return None


def repair_decision(parent, successor):
    """Conservative replacement: preserve every previously valid claim/relation.

    No semantic scoring, new claim promotion, or deletion of original record.
    """
    if (
        parent["scope"]["run_id"] != successor["scope"]["run_id"]
        or parent["scope"]["packet_sha256"] != successor["scope"]["packet_sha256"]
        or parent["scope"]["handles"] != successor["scope"]["handles"]
        or parent["scope"]["request_ordinal"] >= successor["scope"]["request_ordinal"]
    ):
        raise ValueError("repair scope mismatch")
    old = {c["content_sha256"] for c in parent["claims"] if c["delivery"] == "unreviewed_proposal"}
    new = {
        c["content_sha256"] for c in successor["claims"] if c["delivery"] == "unreviewed_proposal"
    }
    old_rel = {
        _relation_signature(parent, r)
        for r in parent["relations"]
        if r["consistency"] == "resolved_candidate"
    }
    new_rel = {
        _relation_signature(successor, r)
        for r in successor["relations"]
        if r["consistency"] == "resolved_candidate"
    }
    improved = (
        successor["execution"] == "completed"
        and successor["response_state"] == "parsed"
        and bool(parent["quarantine"])
        and not successor["quarantine"]
        and not any(c["delivery"] == "withheld_dependency" for c in successor["claims"])
        and old <= new
        and old_rel <= new_rel
        and (bool(new - old) or bool(new_rel - old_rel))
        and (
            not any(q["kind"] == "relation" for q in parent["quarantine"])
            or bool(new_rel - old_rel)
        )
    )
    return {
        "parent_revision_sha256": parent["revision_sha256"],
        "successor_revision_sha256": successor["revision_sha256"],
        "selected": "successor" if improved else "parent",
        "reason": "structural_defect_removed_preserving_prior_proposals"
        if improved
        else "repair_not_demonstrably_preserving",
        "semantic_assessment": "unreviewed",
    }


def aggregate(packet, records, requests, *, run_id, repair=None):
    """Aggregate independently verified fragments within one exact source packet.

    Exact content and evidence equality permits grouping, not claim-ID replacement.
    Relation-bearing claims stay separate; matching held scope conservatively
    withholds duplicates and connected group leaves across fragments.
    """
    if len(records) > len(requests) or len(requests) > 8:
        raise ValueError("invalid fragment cardinality")
    handles = [u["handle"] for u in packet["units"]]
    all_revisions = []
    for i, (record, request) in enumerate(zip(records, requests, strict=False), 1):
        scope = record["scope"]
        if (
            scope != request["scope"]
            or scope["run_id"] != run_id
            or scope["packet_sha256"] != packet["packet_sha256"]
            or scope["request_ordinal"] != i
            or scope["language"] != packet["language"]
            or not set(scope["handles"]) <= set(handles)
            or record["authority"] != "candidate_only"
            or record["revision_sha256"]
            != _identity({k: v for k, v in record.items() if k != "revision_sha256"})
        ):
            raise ValueError("invalid fragment identity")
        all_revisions.append(record["revision_sha256"])
    active = list(records)
    if repair is not None:
        parent_index = repair["parent_ordinal"] - 1
        if not 0 <= parent_index < len(records) - 1:
            raise ValueError("invalid repair parent")
        parent, successor = records[parent_index], records[-1]
        if repair["decision"] != repair_decision(parent, successor):
            raise ValueError("repair decision mismatch")
        active.pop(-1)
        if repair["decision"]["selected"] == "successor":
            active[parent_index] = successor
    entries = []
    relation_members = set()
    relations = []
    for r in active:
        for rel in r["relations"]:
            relation_members.update(rel["claim_ids"])
            relations.append({"revision_sha256": r["revision_sha256"], "relation": rel})
        for c in r["claims"]:
            entries.append((r, c))
    # Match exact normalized content (including exact evidence list and qualifiers).
    # A held interpretation cannot become visible through a duplicate alias.
    held = {c["content_sha256"] for _, c in entries if c["delivery"] != "unreviewed_proposal"}
    by_id = {c["claim_id"]: c for _, c in entries}
    changed = True
    while changed:
        before = set(held)
        for item in relations:
            rel = item["relation"]
            leaves = [by_id[i]["content_sha256"] for i in rel["claim_ids"]]
            if rel["consistency"] != "resolved_candidate" or held.intersection(leaves):
                if "members" in rel["content"]:
                    held.update(leaves)
                else:
                    # Directed links are ordered source then target.
                    held.add(leaves[-1])
        changed = before != held
    grouped = {}
    for r, c in entries:
        key = c["claim_id"] if c["claim_id"] in relation_members else c["content_sha256"]
        item = grouped.setdefault(
            key,
            {
                "content": c["content"],
                "content_sha256": c["content_sha256"],
                "origins": [],
                "relation_bound": c["claim_id"] in relation_members,
                "association": c["association"],
                "delivery": "withheld_dependency"
                if c["content_sha256"] in held
                else "unreviewed_proposal",
                "semantic_assessment": "unreviewed",
                "authority": "candidate_only",
            },
        )
        item["origins"].append(
            {
                "claim_id": c["claim_id"],
                "revision_sha256": r["revision_sha256"],
                "request_ordinal": r["scope"]["request_ordinal"],
            }
        )
    claims = list(grouped.values())
    for c in claims:
        c["aggregate_id"] = _identity([run_id, packet["packet_sha256"], c["origins"]])
    for item in relations:
        rel = item["relation"]
        item["delivery"] = (
            "withheld_dependency"
            if (
                rel["consistency"] != "resolved_candidate"
                or any(by_id[i]["content_sha256"] in held for i in rel["claim_ids"])
            )
            else "unreviewed_relation"
        )
    visible = [c for c in claims if c["delivery"] == "unreviewed_proposal"]
    covered = {h for c in visible for h in c["content"]["evidence"]}
    attempts = defaultdict(list)
    for r in records:
        for h in r["scope"]["handles"]:
            attempts[h].append(
                {"ordinal": r["scope"]["request_ordinal"], "execution": r["execution"]}
            )
    coverage = [
        {
            "handle": h,
            "attempts": attempts[h],
            "coverage": "linked_candidate" if h in covered else "unresolved",
            "material_meaning_coverage": "unreviewed",
        }
        for h in handles
    ]
    result = {
        "contract": "p16-e3-candidate-envelope-v1",
        "kind": "run_fragment_aggregate",
        "packet_sha256": packet["packet_sha256"],
        "run_id": run_id,
        "fragment_revisions": all_revisions,
        "active_revisions": [r["revision_sha256"] for r in active],
        "repair": repair,
        "claims": claims,
        "relations": relations,
        "coverage": coverage,
        "quarantine": [
            {"revision_sha256": r["revision_sha256"], **q} for r in active for q in r["quarantine"]
        ],
        "visible_proposal_ids": [c["aggregate_id"] for c in visible],
        "delivery": "qualified_partial" if visible else "source_only",
        "whole_candidate_established": False,
        "absence_established": False,
        "semantic_assessment": "unreviewed",
        "authority": "candidate_only",
        "eligibility_summary": None,
        "actual_experiment_cell": False,
    }
    return {**result, "aggregate_sha256": _identity(result)}
