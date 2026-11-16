"""Pure negative-contract tests for the B2 source-safe semantic decision gate."""

from __future__ import annotations

import copy
import hashlib
import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIELDS = (
    "duties",
    "requirements",
    "preferences",
    "alternatives",
    "arrangements",
    "uncertainties",
    "work_implied_capabilities",
)


@pytest.fixture
def auditor(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    return importlib.import_module("reconcile_b2_native_trials")


@pytest.fixture
def evidence(auditor):
    jobs = auditor.CASES
    blob = json.dumps({name: [] for name in FIELDS})
    digest = hashlib.sha256(blob.encode()).hexdigest()

    def trial(version, contract, prompt):
        return {
            "contract": contract,
            "source_database_sha256": auditor.SOURCE_B0_SHA,
            "model": "gemma-4-e4b-it-ud",
            "reasoning": "off",
            "authority": "research_only_no_downstream_reuse",
            "prompt_sha256": prompt,
            "cases": {
                job: {
                    "source_job_id": job,
                    "source_semantic_sha256": str(i + 1) * 64,
                    "outcome": "response",
                    "content": blob,
                    "content_sha256": digest,
                    "stats": {"reasoning_output_tokens": 0},
                    "elapsed_seconds": 4.0,
                }
                for i, job in enumerate(jobs)
            },
        }

    v2 = trial("v2", "jobhunter-b2-original-context-native-reasoning-off-v2", "a" * 64)
    v3 = trial("v3", "jobhunter-b2-original-context-native-corrective-v3", "b" * 64)
    rows = []
    for job in jobs:
        for step in range(3):
            rows.append(
                {
                    "source_job_id": job,
                    "check": f"diagnostic_{step}",
                    "v2_outcome": "fail" if step == 0 else "pass",
                    "v3_outcome": "partial" if step == 0 else "pass",
                    "rationale": "Only an exposed diagnostic observation",
                    "authority": "assistant_diagnostic_not_employer_or_independent",
                    "v2_source_semantic_sha256": v2["cases"][job]["source_semantic_sha256"],
                    "v3_source_semantic_sha256": v3["cases"][job]["source_semantic_sha256"],
                }
            )
    review = {
        "review_authority": "assistant_prior_context_exposed_not_independent_human_or_blind",
        "source_sha256": auditor.SOURCE_B0_SHA,
        "prompt_versions": {"native_v2": "a" * 64, "corrective_v3": "b" * 64},
        "semantic_acceptance": False,
        "one_corrective_trial_only": True,
        "not_generalization_accuracy": True,
        "reviewed_checks": rows,
    }
    return v2, v3, review


def test_valid_evidence_stays_candidate_only(auditor, evidence):
    v2, v3, review = evidence
    result = auditor.reconcile(v2, v3, review)
    assert result["b2_semantic_gate"] == "OPEN_NO_PROMOTION"
    assert result["accepted_employer_facts_from_model"] == 0
    assert result["downstream_authority"] == "none"
    assert result["blockers"]["semantics_not_independently_adjudicated"] is True
    assert result["assistant_checks"]["native_v2"]["fail"] == 4
    assert result["assistant_checks"]["corrective_v3"]["partial"] == 4
    assert set(result["trial_seconds"]["native_v2"]) == set(auditor.CASES)


def test_json_validity_does_not_mean_semantic_acceptance(auditor, evidence):
    v2, v3, review = evidence
    review["reviewed_checks"][0]["v2_outcome"] = "pass"
    review["reviewed_checks"][0]["v3_outcome"] = "pass"
    # Even an all-pass exposed assistant review is not independent approval.
    for row in review["reviewed_checks"]:
        row["v2_outcome"] = "pass"
        row["v3_outcome"] = "pass"
    result = auditor.reconcile(v2, v3, review)
    assert result["assistant_checks"]["corrective_v3"]["pass"] == 12
    assert result["b2_semantic_gate"] == "OPEN_NO_PROMOTION"
    assert result["blockers"]["semantics_not_independently_adjudicated"] is True
    assert result["blockers"]["material_source_interpretation_failures"] is False


@pytest.mark.parametrize(
    "mutation,error",
    [
        ("source", "snapshot"),
        ("prompt", "authority|prompt"),
        ("reviewer", "authority|prompt"),
        ("incorrect_role", "authority"),
        ("missing_case", "coverage"),
        ("raw_tamper", "altered"),
        ("reasoning", "altered|reasoning"),
        ("model_bad_structure", "seven"),
        ("duplicate_check", "Duplicated"),
        ("wrong_source_ref", "source version"),
    ],
)
def test_rejects_corrupt_or_misleading_model_evidence(auditor, evidence, mutation, error):
    v2, v3, review = copy.deepcopy(evidence)
    if mutation == "source":
        v2["source_database_sha256"] = "0" * 64
    elif mutation == "prompt":
        review["prompt_versions"]["corrective_v3"] = "0" * 64
    elif mutation == "reviewer":
        review["review_authority"] = "independent_human"
    elif mutation == "incorrect_role":
        review["reviewed_checks"][0]["authority"] = "independent_human"
    elif mutation == "missing_case":
        v3["cases"].pop(auditor.CASES[-1])
    elif mutation == "raw_tamper":
        v2["cases"][auditor.CASES[0]]["content"] = "not the hashed output"
    elif mutation == "reasoning":
        v2["cases"][auditor.CASES[0]]["stats"]["reasoning_output_tokens"] = 2
    elif mutation == "model_bad_structure":
        t = '{"duties":[]}'
        v2["cases"][auditor.CASES[0]]["content"] = t
        v2["cases"][auditor.CASES[0]]["content_sha256"] = hashlib.sha256(t.encode()).hexdigest()
    elif mutation == "duplicate_check":
        review["reviewed_checks"][0]["check"] = review["reviewed_checks"][1]["check"]
    elif mutation == "wrong_source_ref":
        review["reviewed_checks"][0]["v3_source_semantic_sha256"] = "f" * 64
    with pytest.raises(ValueError, match=error):
        auditor.reconcile(v2, v3, review)


def test_fenced_json_parses_without_claiming_fidelity(auditor):
    obj = {name: [] for name in FIELDS}
    raw = chr(96) * 3 + "json\n" + json.dumps(obj) + "\n" + chr(96) * 3
    assert auditor._parse_model_json(raw) == obj
    with pytest.raises(ValueError, match="Unclosed"):
        auditor._parse_model_json(raw[:-3])


def test_public_output_path_fence_precedes_private_file_loading(
    auditor,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "reconcile_b2_native_trials.py",
            "--v2",
            str(tmp_path / "not-here-v2.json"),
            "--v3",
            str(tmp_path / "not-here-v3.json"),
            "--review",
            str(tmp_path / "not-here-review.json"),
            "--out",
            str(tmp_path / "unsafe-report.json"),
        ],
    )
    with pytest.raises(ValueError, match="source-safe review folder"):
        auditor.main()
