from __future__ import annotations

import json

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION
from jobhunter.analysis_service_v16 import ENGLISH_PROMPT_VERSION
from jobhunter.p16_v16_audit import audit_snapshot


def test_v16_audit_does_not_require_sparse_decomposition_for_dense_role(tmp_path) -> None:
    path = tmp_path / "dense.json"
    snapshot = {
        "source_job_id": "dense",
        "english_projection": {
            "artifact_id": 1,
            "fields": {
                "description": "Build robust pipelines for industrial ML workloads.",
                "skills": [],
            },
        },
        "english_analysis": {
            "artifact_id": 2,
            "translation_artifact_id": 1,
            "prompt_version": ENGLISH_PROMPT_VERSION,
            "schema_version": ANALYSIS_SCHEMA_VERSION,
            "analysis": {
                "role_purpose": [],
                "responsibilities": [],
                "requirements": [
                    {
                        "concept": "Industrial ML pipelines",
                        "concept_type": "skill",
                        "requirement_type": "required",
                        "depth_signal": None,
                        "evidence": "Build robust pipelines for industrial ML workloads.",
                        "confidence": "high",
                        "rationale": "Explicit source evidence.",
                    }
                ],
                "coverage": [],
            },
        },
    }
    path.write_text(json.dumps(snapshot), encoding="utf-8")

    result = audit_snapshot(path, job_id="dense")

    assert result["decomposed"] == 0
    assert result["requirements"] == 1
