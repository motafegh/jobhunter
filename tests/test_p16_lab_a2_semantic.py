"""A2 contract and structural reconciliation; authored synthetic controls only."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace

import pytest
from test_p16_lab_a2_context import fixture

from jobhunter.p16_lab import canonical, digest
from jobhunter.p16_lab_a2_context import packet_for_case
from jobhunter.p16_lab_a2_semantic import (
    Proposal,
    SemanticResponse,
    candidate_view,
    reconcile_response,
    request_scope,
)


def setup(language="L2", handles=None):
    b = fixture()
    p = packet_for_case(b, language)
    s = request_scope(
        p,
        b,
        language=language,
        run_id="authored",
        request_ordinal=1,
        handles=handles or [u["handle"] for u in p["units"]],
    )
    return p, b, s


def claim(ref="s1", evidence=None, **kw):
    return {
        "ref": ref,
        "meaning": "Ability to build APIs",
        "evidence": evidence or ["g3"],
        "basis": "inferred",
        **kw,
    }


def group(*members, **kw):
    return {"type": "eligibility_any_of", "members": list(members), "evidence": ["g3"], **kw}


def apply(inputs, statements, relations=None, execution="completed"):
    p, b, s = inputs
    raw = canonical({"statements": statements, "relations": relations or []})
    return reconcile_response(p, b, s, raw, execution=execution), raw


def visible(r):
    return {
        ref
        for c in r["claims"]
        if c["delivery"] == "unreviewed_proposal"
        for ref in c["local_refs"]
    }


def test_schema_only_four_required():
    assert set(Proposal.model_json_schema()["required"]) == {"ref", "meaning", "evidence", "basis"}
    assert SemanticResponse.model_json_schema()["required"] == ["statements"]
    assert Proposal.model_validate(claim(roles=["work", "qualification"])).roles == [
        "work",
        "qualification",
    ]


def test_independent_bad_claim_does_not_erase_valid():
    r, raw = apply(
        setup(),
        [claim(), claim("s2", ["g999"]), claim("s3", ["g4"], meaning="Independent arrangement")],
    )
    assert visible(r) == {"s1", "s3"}
    assert r["quarantine"][0]["reason"] == "unknown_or_out_of_scope_evidence"
    assert r["raw_sha256"] == digest(raw)
    assert r["semantic_assessment"] == "unreviewed"
    assert r["authority"] == "candidate_only"


@pytest.mark.parametrize(
    "bad",
    [
        {"meaning": ""},
        {"basis": "supported"},
        {"evidence": []},
        {"evidence": [1]},
        {"authority": "accepted"},
        {"ref": 1},
        {"roles": "skill"},
    ],
)
def test_invalid_item_quarantined(bad):
    r, _ = apply(setup(), [{**claim("bad"), **bad}, claim("safe")])
    assert visible(r) == {"safe"}
    assert len(r["quarantine"]) == 1


def test_duplicate_ref_quarantined_even_if_same():
    r, _ = apply(setup(), [claim(), claim(), claim("safe", ["g4"])])
    assert visible(r) == {"safe"} and len(r["quarantine"]) == 2


def test_dedup_exact_only_not_text_only():
    r, _ = apply(setup(), [claim(), claim("s2", ["g3", "g3"]), claim("s3", ["g4"])])
    assert len(r["claims"]) == 2
    assert r["claims"][0]["local_refs"] == ["s1", "s2"]
    assert r["claims"][0]["raw_indices"] == [0, 1]
    assert r["claims"][0]["normalization"][0]["raw_index"] == 1
    assert r["claims"][0]["claim_id"] != r["claims"][1]["claim_id"]


def test_nested_alternatives_are_candidate_only():
    r, _ = apply(
        setup(),
        [claim("a"), claim("b", ["g4"]), claim("c", ["g5"])],
        [group("a", "b", ref="inner"), group("inner", "c", ref="outer", type="all_of")],
    )
    assert visible(r) == {"a", "b", "c"}
    assert [len(x["claim_ids"]) for x in r["relations"]] == [2, 3]
    assert all(x["consistency"] == "resolved_candidate" for x in r["relations"])
    assert r["eligibility_summary"] is None


def test_missing_group_leaf_holds_nested_dependents():
    r, raw = apply(
        setup(),
        [
            claim("a"),
            claim("b", ["g4"]),
            claim("c", ["g5"]),
            claim("safe", ["g2"], meaning="Independent context"),
        ],
        [
            group("a", "missing", ref="inner"),
            group("inner", "b", ref="outer"),
            group("outer", "c", ref="top"),
        ],
    )
    assert visible(r) == {"safe"}
    assert len(r["quarantine"]) == 3
    assert r["raw_sha256"] == digest(raw)


@pytest.mark.parametrize(
    "relations",
    [
        [group("a", "b", evidence=["g999"])],
        [group("a", "a")],
        [group("a", "r", ref="r")],
        [group("a", "r2", ref="r1"), group("b", "r1", ref="r2")],
        [group("a", "b", ref="a")],
    ],
)
def test_broken_relation_holds_affected_claims(relations):
    r, _ = apply(setup(), [claim("a"), claim("b", ["g4"]), claim("safe", ["g2"])], relations)
    assert "safe" in visible(r)
    assert "a" not in visible(r)
    assert r["quarantine"]


def test_alias_duplicate_relation_leaf_rejected():
    r, _ = apply(setup(), [claim("a"), claim("b"), claim("safe", ["g2"])], [group("a", "b")])
    assert visible(r) == {"safe"}
    assert r["quarantine"][0]["reason"] == "duplicate_relation_leaf"


def test_unresolved_leaf_holds_whole_group():
    r, _ = apply(
        setup(),
        [claim("a", basis="unresolved"), claim("b", ["g4"]), claim("safe", ["g2"])],
        [group("a", "b")],
    )
    assert visible(r) == {"safe"}
    assert r["relations"][0]["consistency"] == "unresolved"


def test_broken_directed_relation_keeps_source_independent():
    r, _ = apply(
        setup(),
        [claim("a"), claim("b", ["g4"])],
        [{"type": "work_implies_capability", "from": "a", "to": "b", "evidence": ["g999"]}],
    )
    assert visible(r) == {"a"}


def test_directed_cycle_does_not_establish_dependencies():
    r, _ = apply(
        setup(),
        [claim("a"), claim("b", ["g4"]), claim("safe", ["g2"])],
        [
            {"type": "implies", "from": "a", "to": "b", "evidence": ["g3"]},
            {"type": "implies", "from": "b", "to": "a", "evidence": ["g4"]},
        ],
    )
    assert visible(r) == {"safe"}
    assert len(r["quarantine"]) == 2


def test_scope_restricts_handles_even_in_same_packet():
    r, _ = apply(setup(handles=["g3"]), [claim(), claim("out", ["g4"])])
    assert visible(r) == {"s1"}
    assert {u["execution"] for u in r["coverage"] if u["handle"] != "g3"} == {"not_attempted"}


@pytest.mark.parametrize(
    "raw",
    [
        b'{"statements": [], "statements": []}',
        b'{"statements": [], "authority":"accepted"}',
        b'{"statements": [NaN]}',
        b'{"statements": [1e999]}',
        b'{"statements": [{"meaning":"\\ud800"}]}',
        b"[]",
        b'{"statements": [',
    ],
)
def test_invalid_envelope_source_only(raw):
    p, b, s = setup()
    r = reconcile_response(p, b, s, raw, execution="completed")
    assert r["response_state"] == "invalid_envelope" and r["delivery"] == "source_only"
    assert not r["absence_established"]
    assert candidate_view(p, b, s, raw, r, execution="completed")["source"]["units"]


@pytest.mark.parametrize("execution", ["failed", "budget_stopped", "timeout", "not_attempted"])
def test_failed_execution_stays_failed_source_only(execution):
    p, b, s = setup()
    r = reconcile_response(p, b, s, None, execution=execution)
    assert r["execution"] == execution and r["delivery"] == "source_only"
    assert r["raw_sha256"] is None and not r["whole_candidate_established"]


def test_partial_response_does_not_override_failed_execution():
    inputs = setup(handles=["g3"])
    r, raw = apply(inputs, [claim()], execution="budget_stopped")
    v = candidate_view(*inputs, raw, r, execution="budget_stopped")
    assert v["execution"] == "budget_stopped" and v["delivery"] == "qualified_partial"
    assert v["proposals"][0]["label"] == "unreviewed_model_proposal_not_established_fact"
    assert not v["absence_established"]


def test_board_evidence_and_wrong_meaning_remain_unreviewed():
    p, b, s = setup()
    tag = next(u["handle"] for u in p["units"] if u["reference"].get("field") == "skills")
    r, raw = apply((p, b, s), [claim(evidence=[tag], meaning="Go is mandatory", basis="explicit")])
    assert r["claims"][0]["evidence_surfaces"] == ["structured_skill_tags"]
    v = candidate_view(p, b, s, raw, r, execution="completed")
    assert r["claims"][0]["content"]["meaning"] == "Go is mandatory"
    assert r["claims"][0]["delivery"] == "withheld_board_only"
    assert not v["proposals"] and v["delivery"] == "source_only"
    assert any(u["value"] == "Go" for u in v["source"]["units"])
    assert v["semantic_assessment"] == "unreviewed"


def test_field_only_never_becomes_original_child():
    p, b, s = setup("L0")
    r, raw = apply((p, b, s), [claim(evidence=["g1"])])
    v = candidate_view(p, b, s, raw, r, execution="completed")
    assert v["proposals"][0]["evidence"][0]["association"] == "verified_field_only_unaligned"
    assert v["source"]["language"] == "L2"


def test_tampered_scope_candidate_and_stale_binding_denied():
    p, b, s = setup()
    r, raw = apply((p, b, s), [claim()])
    with pytest.raises(ValueError):
        reconcile_response(p, b, {**s, "handles": ["g3"]}, raw, execution="completed")
    changed = deepcopy(r)
    changed["authority"] = "accepted"
    with pytest.raises(ValueError):
        candidate_view(p, b, s, raw, changed, execution="completed")
    with pytest.raises(ValueError):
        candidate_view(
            p,
            replace(b, source=replace(b.source, job_detail_version_id=2)),
            s,
            raw,
            r,
            execution="completed",
        )


def test_empty_response_not_absence():
    r, _ = apply(setup(), [])
    assert r["delivery"] == "source_only" and not r["absence_established"]


def test_run_identity_changes_claim_revision():
    p, b, s = setup()
    r, raw = apply((p, b, s), [claim()])
    next_scope = request_scope(
        p, b, language="L2", run_id="other", request_ordinal=1, handles=s["handles"]
    )
    nxt = reconcile_response(p, b, next_scope, raw, execution="completed")
    assert r["claims"][0]["content_sha256"] == nxt["claims"][0]["content_sha256"]
    assert r["claims"][0]["claim_id"] != nxt["claims"][0]["claim_id"]


def test_wrong_semantics_with_real_reference_are_not_mechanically_approved():
    p, b, s = setup()
    r, raw = apply(
        (p, b, s), [claim(meaning="Ten years of paid API work required", basis="explicit")]
    )
    assert r["claims"][0]["semantic_assessment"] == "unreviewed"
    v = candidate_view(p, b, s, raw, r, execution="completed")
    assert v["proposals"][0]["label"] == "unreviewed_model_proposal_not_established_fact"
    assert not v["proposals"][0]["employer_obligation_established"]


def test_mixed_board_and_prose_no_obligation_promotion():
    p, b, s = setup()
    tag = next(u["handle"] for u in p["units"] if u["reference"].get("field") == "skills")
    r, raw = apply((p, b, s), [claim(evidence=["g3", tag], strength="required")])
    assert r["claims"][0]["content"]["strength"] == "required"
    v = candidate_view(p, b, s, raw, r, execution="completed")
    assert not v["proposals"][0]["employer_obligation_established"]
    assert v["proposals"][0]["evidence"][1]["reference"]["field"] == "skills"
