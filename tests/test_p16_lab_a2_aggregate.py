"""Run-local A2 reconciliation and bounded repair tests."""

from __future__ import annotations

import json
from copy import deepcopy

import pytest
from test_p16_lab import root  # noqa: F401

from jobhunter.p16_lab import canonical, read_events
from jobhunter.p16_lab_a2_aggregate import aggregate, choose_repair, repair_decision
from jobhunter.p16_lab_a2_context import packet_for_case
from jobhunter.p16_lab_a2_execution import synthetic_case, verify_manifest
from jobhunter.p16_lab_a2_semantic import reconcile_response, request_scope
from jobhunter.p16_lab_provider_worker import rehearse_provider


def proposal(ref, handle, meaning="Claim", **extra):
    return {"ref": ref, "meaning": meaning, "evidence": [handle], "basis": "explicit", **extra}


def fragment(b, p, i, statements, relations=(), handles=None, whole=False):
    included = handles or [u["handle"] for u in p["units"]]
    scope = request_scope(p, b, language="L2", run_id="test", request_ordinal=i, handles=included)
    r = reconcile_response(
        p,
        b,
        scope,
        canonical({"statements": statements, "relations": list(relations)}),
        execution="completed",
    )
    return r, {"scope": scope, "primary": included, "whole_context": whole}


def setup():
    b = synthetic_case()
    return b, packet_for_case(b, "L2")


def merge(p, *pairs, repair=None):
    return aggregate(p, [r for r, _ in pairs], [q for _, q in pairs], run_id="test", repair=repair)


def test_exact_duplicates_not_text_only():
    b, p = setup()
    a = fragment(b, p, 1, [proposal("s1", "g2"), proposal("s2", "g4")])
    z = fragment(b, p, 2, [proposal("s1", "g2"), proposal("s2", "g2", strength="preferred")])
    r = merge(p, a, z)
    assert len(r["claims"]) == 3
    assert len(r["claims"][0]["origins"]) == 2
    assert len({c["aggregate_id"] for c in r["claims"]}) == 3
    assert r["authority"] == "candidate_only" and not r["whole_candidate_established"]


def test_held_duplicate_propagates_to_group_not_independent():
    b, p = setup()
    a = fragment(
        b,
        p,
        1,
        [proposal("a", "g2"), proposal("bad", "g999")],
        [{"type": "any_of", "members": ["a", "bad"], "evidence": ["g2"]}],
    )
    z = fragment(
        b,
        p,
        2,
        [
            proposal("x", "g2"),
            proposal("y", "g4", "Other path"),
            proposal("z", "g3", "Independent"),
        ],
        [{"type": "any_of", "members": ["x", "y"], "evidence": ["g2", "g4"]}],
    )
    r = merge(p, a, z)
    assert [
        c["content"]["meaning"] for c in r["claims"] if c["delivery"] == "unreviewed_proposal"
    ] == ["Independent"]
    assert r["relations"][0]["delivery"] == "withheld_dependency"
    assert r["eligibility_summary"] is None


def test_request_local_refs_never_resolve_from_other_fragment():
    b, p = setup()
    a = fragment(
        b,
        p,
        1,
        [proposal("a", "g2")],
        [{"type": "any_of", "members": ["a", "b"], "evidence": ["g2"]}],
    )
    z = fragment(b, p, 2, [proposal("b", "g4", "Unrelated")])
    r = merge(p, a, z)
    assert len(r["quarantine"]) == 1
    assert [
        c["content"]["meaning"] for c in r["claims"] if c["delivery"] == "unreviewed_proposal"
    ] == ["Unrelated"]


def test_repair_selection_and_preservation():
    b, p = setup()
    parent = fragment(b, p, 1, [proposal("a", "g2"), proposal("b", "g999", "Missing")])
    z = fragment(b, p, 2, [proposal("a", "g4", "Independent")])
    good = fragment(b, p, 3, [proposal("renamed", "g2"), proposal("b", "g2", "Missing")])
    bad = fragment(b, p, 3, [proposal("b", "g2", "Missing")])
    selection = choose_repair([parent[0], z[0]], [parent[1], z[1]], remaining_posts=1)
    assert selection["parent_ordinal"] == 1
    assert choose_repair([parent[0]], [parent[1]], remaining_posts=0) is None
    assert (
        choose_repair([parent[0]], [{**parent[1], "whole_context": True}], remaining_posts=1)
        is None
    )
    for successor, selected, count in [(good, "successor", 3), (bad, "parent", 2)]:
        decision = repair_decision(parent[0], successor[0])
        assert decision["selected"] == selected
        r = merge(p, parent, z, successor, repair={**selection, "decision": decision})
        assert len(r["fragment_revisions"]) == 3 and len(r["active_revisions"]) == 2
        assert len(r["visible_proposal_ids"]) == count
        assert r["semantic_assessment"] == "unreviewed"


def test_repair_cannot_drop_resolved_relation():
    b, p = setup()
    statements = [proposal("a", "g2"), proposal("b", "g4", "Other")]
    relation = {"type": "any_of", "members": ["a", "b"], "evidence": ["g2", "g4"]}
    parent = fragment(b, p, 1, [*statements, proposal("bad", "g999")], [relation])
    good = fragment(b, p, 2, [*statements, proposal("new", "g3", "New")], [relation])
    wrong = fragment(
        b, p, 2, [*statements, proposal("new", "g3", "New")], [{**relation, "type": "all_of"}]
    )
    assert repair_decision(parent[0], good[0])["selected"] == "successor"
    assert repair_decision(parent[0], wrong[0])["selected"] == "parent"


def test_tampered_fragment_and_foreign_request_rejected():
    b, p = setup()
    a = fragment(b, p, 1, [proposal("a", "g2")])
    bad = deepcopy(a[0])
    bad["claims"][0]["content"]["meaning"] = "tampered"
    with pytest.raises(ValueError, match="identity"):
        merge(p, (bad, a[1]))
    with pytest.raises(ValueError, match="identity"):
        aggregate(p, [a[0]], [a[1]], run_id="foreign")


def test_no_attempt_is_not_absence():
    _, p = setup()
    r = merge(p)
    assert all(not c["attempts"] for c in r["coverage"])
    assert r["delivery"] == "source_only" and not r["absence_established"]


@pytest.mark.parametrize(
    "scenario,gen,visible,selection",
    [
        ("a2-shared", 2, 3, None),
        ("a2-repair", 3, 3, "successor"),
        ("a2-repair-loss", 3, 2, "parent"),
        ("a2-repair-overflow", 2, 2, None),
    ],
)
def test_guarded_aggregation_and_repair(request, scenario, gen, visible, selection):
    root_path = request.getfixturevalue("root")
    result = rehearse_provider(root_path, scenario, scenario)
    assert result["status"] == "child_completed" and result["journal"]["sealed"]
    child = result["child"]
    summary = child["a2_result"]
    assert child["generation_reservations"] == gen and child["control_reservations"] == 1
    assert summary["visible_proposals"] == visible
    assert child["denied_operations"] == child["real_dispatches"] == 0
    path = root_path / "data/local-acceptance/p16-evolution-e3" / scenario
    rows = read_events(path / "dispatch.jsonl")
    assert verify_manifest(path, summary, rows)
    r = json.loads((path / "a2-aggregate.json").read_bytes())
    assert len(r["fragment_revisions"]) == gen
    if selection:
        assert r["repair"]["decision"]["selected"] == selection
        assert len(r["active_revisions"]) == 2
    elif scenario == "a2-repair-overflow":
        assert any(e["event"] == "a2_repair_blocked" for e in rows)
        assert r["quarantine"]
    else:
        assert len([c for c in r["claims"] if len(c["origins"]) == 2]) == 1
    (path / "a2-aggregate.json").write_bytes(b"{}")
    assert not verify_manifest(path, summary, rows)


def test_explicit_unresolved_relation_holds_members():
    b, p = setup()
    a = fragment(
        b,
        p,
        1,
        [proposal("a", "g2"), proposal("b", "g4", "Other"), proposal("safe", "g3", "Independent")],
        [{"type": "unresolved", "members": ["a", "b"], "evidence": ["g2", "g4"]}],
    )
    r = merge(p, a)
    assert [
        c["content"]["meaning"] for c in r["claims"] if c["delivery"] == "unreviewed_proposal"
    ] == ["Independent"]


def test_repair_cannot_erase_broken_relation_and_add_unrelated_claim():
    b, p = setup()
    parent = fragment(
        b,
        p,
        1,
        [proposal("a", "g2")],
        [{"type": "any_of", "members": ["a", "missing"], "evidence": ["g2"]}],
    )
    successor = fragment(b, p, 2, [proposal("new", "g3", "Unrelated")])
    assert repair_decision(parent[0], successor[0])["selected"] == "parent"
