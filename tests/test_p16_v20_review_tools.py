from __future__ import annotations

import json
from pathlib import Path

import pytest

from jobhunter.analysis_service_v20 import ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.p16_v20_audit import AuditError, audit_snapshot


def _write_snapshot(path: Path, *, prompt_version: str = ENGLISH_PROMPT_VERSION) -> None:
    payload = {
        "source_job_id": "tG9K",
        "english_projection": {
            "artifact_id": 33,
            "fields": {"description": "", "skills": []},
        },
        "english_analysis": {
            "artifact_id": 36,
            "translation_artifact_id": 33,
            "prompt_version": prompt_version,
            "schema_version": ANALYSIS_SCHEMA_VERSION,
            "analysis": {
                "role_purpose": [],
                "responsibilities": [],
                "requirements": [],
                "coverage": [],
            },
        },
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_v20_review_audit_binds_to_v20_contract(tmp_path: Path) -> None:
    path = tmp_path / "tG9K.json"
    _write_snapshot(path)

    result = audit_snapshot(path, job_id="tG9K")

    assert result["artifact_id"] == 36
    assert result["requirements"] == 0
    assert result["responsibilities"] == 0
    assert result["role_purpose"] == 0


def test_v20_review_audit_rejects_wrong_prompt_contract(tmp_path: Path) -> None:
    path = tmp_path / "tG9K.json"
    _write_snapshot(path, prompt_version="job-analysis-english-v16")

    with pytest.raises(AuditError, match="Wrong P1.6 candidate contract"):
        audit_snapshot(path, job_id="tG9K")
