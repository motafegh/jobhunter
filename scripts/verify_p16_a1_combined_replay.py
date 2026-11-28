"""Combined R1/R2/R3 retained and original counterfactual controls; no model calls."""

from __future__ import annotations

import json

from verify_p16_a1_r1_replay import REPLAY, REPLAY_SHA, outcome

from jobhunter.inference.instructor_lm_studio_v30 import (
    AnalysisRequirementV30,
    JobAnalysisResponseV30,
)
from jobhunter.p16_lab import ROOT, checked_path, file_digest, load_requirements
from jobhunter.p16_lab_a1_r1 import _compound_scopes
from jobhunter.p16_lab_a1_r23 import (
    AnalysisRequirementR12,
    JobAnalysisResponseR12,
    _motivation_meaning,
    corrected_duty_plan,
)

COUNTERFACTUALS = (
    "data/local-acceptance/p16-evolution-e1-2026-11-24/PRIVATE_E1_4_5_COUNTERFACTUALS.json"
)
COUNTERFACTUAL_SHA = "97c9cb1ccc32e643ec1458197a8ea10fd8ff0533f38bac6256f73fc4a622bfa2"


def corrected(ctx):
    plan, removed = corrected_duty_plan(ctx["analysis_fields"])
    if not ctx["responsibility_coverage_plan"]:
        return ctx, ()
    if set(ctx["responsibility_coverage_plan"]) - set(plan) != set(removed):
        raise ValueError("unexpected retained duty ledger difference")
    return {**ctx, "responsibility_coverage_plan": plan}, removed


def verify(root=ROOT):
    load_requirements(root)
    source = checked_path(root, REPLAY)
    prior = checked_path(root, COUNTERFACTUALS)
    assert file_digest(source) == REPLAY_SHA and file_digest(prior) == COUNTERFACTUAL_SHA
    cases = json.loads(source.read_bytes())
    historical = json.loads(prior.read_bytes())
    rows = []
    recovered = {"compound": 0, "motivation": 0}
    for case in cases:
        for row in case["replays"]:
            matches = row["replays"]
            assert len(matches) == 1
            ctx = case["captures"][matches[0]["partition"] - 1]["context"]
            new_ctx, removed = corrected(ctx)
            old, old_errors = outcome(JobAnalysisResponseV30, row["raw"], ctx)
            new, new_errors = outcome(JobAnalysisResponseR12, row["raw"], new_ctx)
            targets = []
            for i, item in enumerate(row["raw"]["requirements"]):
                before, _ = outcome(AnalysisRequirementV30, item, ctx)
                after, _ = outcome(AnalysisRequirementR12, item, new_ctx)
                if before is not None or after is None:
                    continue
                scopes = _compound_scopes(item["item_excerpt"])
                if scopes:
                    matching = [
                        x for x in scopes if x.subject.casefold() == after.concept.casefold()
                    ]
                    assert len(matching) == 1
                    assert after.depth_signal == matching[0].degree
                    assert after.item_excerpt == matching[0].item
                    kind = "compound"
                else:
                    assert _motivation_meaning(item["item_excerpt"]) is not None
                    assert after.concept == item["concept"] and after.depth_signal is None
                    kind = "motivation"
                assert after.evidence == ctx["evidence_catalog"][item["evidence"]]
                assert after.requirement_type == item["requirement_type"]
                recovered[kind] += 1
                targets.append({"index": i, "kind": kind})
            rows.append(
                {
                    "recovered_items": targets,
                    "diagnostic": row["diagnostic"],
                    "before_valid": old is not None,
                    "after_valid": new is not None,
                    "removed_duties": len(removed),
                    "before_errors": old_errors,
                    "after_errors": new_errors,
                }
            )
    assert recovered == {"compound": 4, "motivation": 2}
    assert len(rows) == 6 and not any(r["before_valid"] for r in rows)
    assert [r["diagnostic"] for r in rows if r["after_valid"]] == [6]
    checks = {}

    def test(name, cls, raw, ctx, expected, exact_depth=None, check_depth=False):
        value, errors = outcome(cls, raw, ctx)
        assert (value is not None) == expected, name
        if check_depth:
            assert value.depth_signal == exact_depth, name
        checks[name] = {
            "historical_valid": historical[name]["pass"],
            "combined_valid": expected,
            "errors": errors,
            "depth_checked": check_depth,
        }

    backend, ai, sec = cases
    ctx = backend["captures"][0]["context"]
    a, b = backend["replays"][1]["raw"]["requirements"][:2]
    qa = {
        **a,
        "item_excerpt": "Strong proficiency in Python or Go",
        "depth_signal": "Strong proficiency",
        "concept": "Python or Go",
    }
    qb = {
        **b,
        "item_excerpt": "solid understanding of software engineering principles",
        "depth_signal": "solid understanding",
        "concept": "Software engineering principles",
    }
    test(
        "backend_narrowed_complete_degree",
        AnalysisRequirementR12,
        qa,
        ctx,
        True,
        "Strong proficiency",
        True,
    )
    test(
        "backend_narrowed_solid_item",
        AnalysisRequirementR12,
        qb,
        ctx,
        True,
        "solid understanding",
        True,
    )
    test(
        "backend_narrowed_lossy_degree_token",
        AnalysisRequirementR12,
        {**qa, "depth_signal": "proficiency"},
        ctx,
        True,
        "Strong proficiency",
        True,
    )
    test(
        "backend_borrowed_other_subject_degree",
        AnalysisRequirementR12,
        {**qa, "depth_signal": "solid"},
        ctx,
        False,
    )
    test(
        "backend_invented_evidence",
        AnalysisRequirementR12,
        {**qa, "depth_signal": "proficiency", "evidence": "field:nonexistent:77"},
        ctx,
        False,
    )
    f = backend["replays"][0]["raw"]["requirements"][6]
    test(
        "backend_familiarity_move_to_separate_field",
        AnalysisRequirementR12,
        {**f, "concept": f["concept"].removeprefix("Familiarity with ")},
        ctx,
        True,
    )
    for i in (3, 4, 5):
        q = backend["replays"][0]["raw"]["requirements"][i]
        name = f"backend_nonrecognized_degree_null_{i}"
        test(name, AnalysisRequirementR12, {**q, "depth_signal": None}, ctx, True, None, True)
        checks[name]["known_semantic_loss_control"] = True
    ctx2 = ai["captures"][1]["context"]
    q = ai["replays"][0]["raw"]["requirements"][1]
    test("ai_motivation_original_null", AnalysisRequirementR12, q, ctx2, True, None, True)
    neutral = {**q, "concept": "Interest in practical product and software-service development"}
    test("ai_motivation_neutral_concept_null", AnalysisRequirementR12, neutral, ctx2, False)
    test(
        "ai_motivation_misleading_lexical_degree",
        AnalysisRequirementR12,
        {**neutral, "depth_signal": "strong"},
        ctx2,
        False,
    )
    ctx3 = sec["captures"][0]["context"]
    raw = sec["replays"][1]["raw"]
    alt, removed = corrected(ctx3)
    assert len(removed) == 1
    test("security_original_full_response", JobAnalysisResponseR12, raw, ctx3, False)
    test("security_counterfactual_remove_false_duty", JobAnalysisResponseR12, raw, alt, True)
    test(
        "security_negative_control_missing_real_duty",
        JobAnalysisResponseR12,
        {**raw, "responsibilities": raw["responsibilities"][1:]},
        alt,
        False,
    )
    assert set(checks) == set(historical) and len(checks) == 15
    assert file_digest(source) == REPLAY_SHA and file_digest(prior) == COUNTERFACTUAL_SHA
    return {
        "authority": "offline_diagnostic_only",
        "retained": rows,
        "recovered_items": recovered,
        "counterfactuals": checks,
        "real_model_calls": 0,
        "limitations": [
            "R4 separate original board checks, not replayed as employer claims",
            "Three null-depth controls still pass with known semantic loss",
            "Partition results, not whole job semantic acceptance",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
