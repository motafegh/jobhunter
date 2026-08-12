import copy
import json
import subprocess
import sys
from pathlib import Path


def _snapshot() -> dict:
    purpose = {
        "statement": "Build Python automation for internal workflows.",
        "evidence": ["Build Python automation for internal workflows."],
        "confidence": "high",
    }
    requirements = [
        {
            "concept": "Python",
            "concept_type": "skill",
            "requirement_type": "contextual",
            "depth_signal": None,
            "evidence": ["Python"],
            "confidence": "high",
        },
        {
            "concept": "Professional experience",
            "concept_type": "experience",
            "requirement_type": "required",
            "depth_signal": "three years",
            "evidence": ["three years"],
            "confidence": "high",
        },
    ]
    responsibilities = [
        {
            "statement": "Build internal tooling.",
            "evidence": ["Build internal tooling."],
            "confidence": "high",
        }
    ]
    source_truth = {
        "role_purpose": [{"index": 0, **purpose}],
        "requirements": [
            {"index": index, **requirement}
            for index, requirement in enumerate(requirements)
        ],
        "responsibilities": [
            {"index": 0, **responsibilities[0]},
        ],
        "capability_requirement_indices": [0],
        "role_level_requirement_indices": [1],
        "linked_requirement_indices": [0],
        "unlinked_capability_requirement_indices": [],
        "linked_responsibility_indices": [0],
        "unlinked_responsibility_indices": [],
        "explicit_depth_requirement_indices": [1],
        "linked_explicit_depth_requirement_indices": [],
        "unlinked_explicit_depth_requirement_indices": [1],
    }
    return {
        "snapshot_schema_version": "job-review-snapshot-v1",
        "source_job_id": "job1",
        "configured_models": {
            "analysis": "analysis-model",
            "capability": "capability-model",
            "blueprint": "experimental-blueprint-model",
        },
        "status": {
            "english_projection_present": True,
            "english_analysis_present": True,
            "original_analysis_present": False,
            "capability_intelligence_present": True,
            "role_capability_blueprint_present": True,
            "translation_matches_english_analysis": True,
            "capability_is_current_chain": True,
            "blueprint_is_current_chain": True,
        },
        "source": {"source_job_id": "job1"},
        "english_projection": {
            "artifact_id": 30,
            "job_detail_version_id": 10,
        },
        "english_analysis": {
            "artifact_id": 20,
            "job_detail_version_id": 10,
            "translation_artifact_id": 30,
            "model": "analysis-model",
            "prompt_version": "job-analysis-english-v9",
            "schema_version": "job-analysis-v4",
            "analysis": {
                "role_purpose": [purpose],
                "requirements": requirements,
                "responsibilities": responsibilities,
            },
        },
        "original_analysis": None,
        "capability_intelligence": {
            "artifact_id": 40,
            "job_detail_version_id": 10,
            "translation_artifact_id": 30,
            "analysis_artifact_id": 20,
            "model": "capability-model",
            "prompt_version": "job-capability-intelligence-v7",
            "schema_version": "job-capability-intelligence-v4",
            "intelligence": {
                "capabilities": [
                    {
                        "capability_label": "Python automation",
                        "source_requirement_indices": [0],
                        "source_responsibility_indices": [0],
                        "requirement_strength": "contextual",
                        "depth_signals": [],
                        "work_activities": [
                            {
                                "statement": "Build internal tooling.",
                                "evidence_status": "source_explicit",
                            }
                        ],
                        "independence_expectation": None,
                        "sub_capabilities": [],
                        "underlying_knowledge": [],
                        "operational_practices": [],
                        "operational_context": [],
                    }
                ],
                "source_truth": source_truth,
                "cross_capability_observations": [],
            },
        },
        "role_capability_blueprint": {
            "artifact_id": 50,
            "prompt_version": "role-capability-blueprint-v6",
            "schema_version": "role-capability-blueprint-v5",
        },
    }


def _run(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "scripts/audit_ci3_capability_snapshot.py",
            "--job-id",
            "job1",
            "--snapshot",
            str(path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def test_ci3_audit_passes_and_ignores_experimental_blueprint(tmp_path: Path) -> None:
    path = tmp_path / "job1.json"
    path.write_text(json.dumps(_snapshot()), encoding="utf-8")

    result = _run(path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Mechanical CI-3 Capability checks: PASS" in result.stdout
    assert "Capability requirements linked: 1/1" in result.stdout
    assert "Responsibilities linked: 1/1" in result.stdout
    assert "Blueprint payload: present but ignored by CI-3 acceptance" in result.stdout


def test_ci3_audit_rejects_role_level_requirement_leaking_into_profile(tmp_path: Path) -> None:
    snapshot = copy.deepcopy(_snapshot())
    profile = snapshot["capability_intelligence"]["intelligence"]["capabilities"][0]
    profile["source_requirement_indices"] = [0, 1]
    source_truth = snapshot["capability_intelligence"]["intelligence"]["source_truth"]
    source_truth["linked_requirement_indices"] = [0, 1]
    source_truth["linked_explicit_depth_requirement_indices"] = [1]
    source_truth["unlinked_explicit_depth_requirement_indices"] = []
    path = tmp_path / "job1.json"
    path.write_text(json.dumps(snapshot), encoding="utf-8")

    result = _run(path)

    assert result.returncode == 1
    assert "role-level" in result.stdout
