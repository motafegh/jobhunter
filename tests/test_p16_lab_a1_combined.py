"""Combined A1 fixed worker and private candidate envelope controls."""

from __future__ import annotations

import json
from dataclasses import replace

import pytest
from test_p16_lab import root  # noqa: F401

from jobhunter import analysis_persistence_v23 as persistence
from jobhunter.analysis_service_v30 import JobAnalysisServiceV30
from jobhunter.p16_lab import file_digest
from jobhunter.p16_lab_a1 import (
    ADAPTER,
    CONTRACT,
    PROMPT,
    A1Provider,
    reconcile,
    synthetic_input,
    verify_scoped_merge,
)
from jobhunter.p16_lab_provider_worker import rehearse_provider


@pytest.mark.parametrize(
    ("scenario", "gen", "count", "removed"),
    [
        ("a1-synthetic", 1, 2, 1),
        ("a1-motivation", 1, 1, 0),
        ("a1-missing-duty", 2, 0, 0),
    ],
)
def test_combined_a1_worker(request, scenario, gen, count, removed):
    root_path = request.getfixturevalue("root")
    result = rehearse_provider(root_path, scenario, scenario)
    assert result["status"] == "child_completed"
    child = result["child"]
    assert child["generation_reservations"] == gen
    assert child["control_reservations"] == 1
    assert child["denied_operations"] == child["real_dispatches"] == 0
    path = root_path / "data/local-acceptance/p16-evolution-e3" / scenario
    candidate = path / "a1-candidate.json"
    assert not (path / "working.sqlite3").exists()
    if not count:
        assert child["stopped"] and child["finished"] == 0
        assert child["a1_result"] is None and not candidate.exists()
        return
    assert not child["stopped"] and child["finished"] == 1
    assert child["a1_result"]["candidate_sha256"] == file_digest(candidate)
    record = json.loads(candidate.read_bytes())
    assert record["contract_version"] == CONTRACT and record["adapter"] == ADAPTER
    assert record["authority"] == "candidate_only" and record["semantic_review_status"] == "pending"
    assert record["actual_experiment_cell"] is False
    assert record["raw_response"] and record["request_body"]
    assert len(record["board_observations"]) == 1
    assert record["board_observations"][0]["value"] == "Go"
    assert record["board_observations"][0]["employer_obligation"] == "not_established"
    claims = record["analysis"]["requirements"]
    assert claims == record["normalized"]["requirements"]
    assert len(claims) == count and all(c["item_excerpt"] in c["evidence"] for c in claims)
    assert len(record["removed_duty_refs"]) == removed
    assert all(c["concept"] != "Go" for c in claims)
    if scenario == "a1-synthetic":
        assert [(c["concept"], c["depth_signal"]) for c in claims] == [
            ("Rust or Kotlin", "Strong proficiency"),
            ("distributed design", "solid understanding"),
        ]
        assert len(record["analysis"]["responsibility_coverage"]) == 1
    else:
        assert claims[0]["depth_signal"] is None
        assert claims[0]["concept"] == "Strong interest in hands-on robotics development"


def test_a1_prompt_does_not_modify_incumbent():
    old = JobAnalysisServiceV30.system_prompt
    assert "Preserve structured skills as required" in old
    assert "Preserve structured skills as required" not in PROMPT
    assert "JobHunter removes it before unchanged v5" not in PROMPT
    assert "Never borrow neighboring depth" in PROMPT
    assert JobAnalysisServiceV30.system_prompt == old


def test_a1_requires_exact_offline_transport():
    with pytest.raises(TypeError, match="offline mock guard"):
        A1Provider(None)


def test_reconciliation_rejects_duty_ledger_drift():
    from types import SimpleNamespace

    source, translation = synthetic_input()
    fields = dict(translation.fields)
    fields.pop("skills")
    provider = SimpleNamespace(duty_plans=[{}], removed_duty_refs=[()])
    old = persistence.build_responsibility_coverage_plan_v21
    with pytest.raises(ValueError, match="duty ledger mismatch"):
        reconcile({}, fields, provider)
    assert persistence.build_responsibility_coverage_plan_v21 is old
    assert replace(source, fields=fields).fields == fields


def test_scoped_merge_rejects_disappearing_or_changed_child():
    claim = {
        "concept": "Rust",
        "concept_type": "skill",
        "requirement_type": "required",
        "evidence": "Familiarity with Rust. Strong proficiency in Rust.",
        "item_excerpt": "Familiarity with Rust",
        "depth_signal": "Familiarity",
    }
    other = {
        **claim,
        "item_excerpt": "Strong proficiency in Rust",
        "depth_signal": "Strong proficiency",
    }
    verify_scoped_merge([claim, claim], [claim])
    for final in ([], [claim], [{**other, "depth_signal": None}]):
        with pytest.raises(ValueError, match="scoped merge"):
            verify_scoped_merge([claim, other], final)
