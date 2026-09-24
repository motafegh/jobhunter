"""R05 A2 local diagnostic inspection and partition failure regression."""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from jobhunter import analysis_diagnostic_cli as diagnostic_cli
from jobhunter import analysis_runtime_v21 as runtime_v21
from jobhunter.analysis_failure_diagnostics import AnalysisFailureDiagnosticStore
from jobhunter.analysis_runtime_v20 import V20CandidateAnalysisProvider
from jobhunter.inference.base import InferenceResponseError


@pytest.fixture
def database(tmp_path):
    path = tmp_path / "jobhunter.sqlite3"
    with sqlite3.connect(path) as connection:
        connection.execute(
            """CREATE TABLE job_analysis_attempts (
                id INTEGER PRIMARY KEY, job_detail_version_id INTEGER,
                attempted_at TEXT, model TEXT, prompt_version TEXT,
                schema_version TEXT, outcome TEXT, error_type TEXT,
                error_message TEXT
            )"""
        )
        connection.execute(
            """INSERT INTO job_analysis_attempts VALUES
            (7, 19, '2026-09-24T18:00:00+00:00', 'local-model',
             'job-analysis-english-v21', 'job-analysis-v5', 'failed',
             'UnsafeError', 'legacy-error-marker')"""
        )
    return path


def test_cli_requires_explicit_content_option(database, monkeypatch, capsys):
    store = AnalysisFailureDiagnosticStore(database)
    error = InferenceResponseError("error-marker")
    error.last_completion = "response-marker"
    store.record_failure(attempt_id=7, error=error)
    monkeypatch.setattr(
        diagnostic_cli.Settings, "load", lambda path: SimpleNamespace(database_path=database)
    )
    assert diagnostic_cli.main(["list"], config_path=database) == 0
    output = capsys.readouterr().out
    assert "legacy-error-marker" not in output
    assert "response-marker" not in output
    assert '"diagnostics_available": true' in output
    assert diagnostic_cli.main(["show", "7"], config_path=database) == 0
    assert "response-marker" not in capsys.readouterr().out
    assert diagnostic_cli.main(
        ["show", "7", "--include-response"], config_path=database
    ) == 0
    assert "response-marker" in capsys.readouterr().out


def test_cli_unknown_failed_attempt(database, monkeypatch, capsys):
    monkeypatch.setattr(
        diagnostic_cli.Settings, "load", lambda path: SimpleNamespace(database_path=database)
    )
    assert diagnostic_cli.main(["show", "999"], config_path=database) == 2
    assert "No failed analysis attempt" in capsys.readouterr().err


def test_partition_failure_keeps_distinct_non_authoritative_records(database, monkeypatch):
    counter = 0

    def completion(**kwargs):
        nonlocal counter
        counter += 1
        if counter == 2:
            error = InferenceResponseError("invalid response")
            error.last_completion = "unusable-model-response"
            raise error
        return SimpleNamespace(structured={"requirements": [{"concept": "Linux"}]})

    def run_once(self, **kwargs):
        self._complete_partition(
            user_payload={"analysis_partition": {"index": 1, "total": 2}}
        )
        self._complete_partition(
            user_payload={"analysis_partition": {"index": 2, "total": 2}}
        )

    monkeypatch.setattr(
        runtime_v21, "complete_analysis_partition_with_instructor_v21", completion
    )
    monkeypatch.setattr(V20CandidateAnalysisProvider, "_run_once", run_once)
    provider = object.__new__(runtime_v21.V21CandidateAnalysisProvider)
    with pytest.raises(InferenceResponseError) as excinfo:
        provider._run_once()
    store = AnalysisFailureDiagnosticStore(database)
    store.record_failure(attempt_id=7, error=excinfo.value)
    rows = store.list_for_attempt(7)
    assert len(rows) == 2
    assert (rows[0].failure_stage, rows[0].partition_index) == (
        "partition_inference", 2
    )
    assert rows[0].completion_text == "unusable-model-response"
    assert rows[1].payload_kind == "model_validated_partition_structured"
    assert rows[1].partition_index == 1
    assert json.loads(rows[1].completion_text)["requirements"][0]["concept"] == "Linux"
    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT name FROM sqlite_master WHERE name = 'job_analysis_artifacts'"
        ).fetchone() is None


def test_post_partition_failure_stays_unavailable(database, monkeypatch):
    def completion(**kwargs):
        return SimpleNamespace(structured={"requirements": [{"concept": "Python"}]})

    def run_once(self, **kwargs):
        self._complete_partition(
            user_payload={"analysis_partition": {"index": 1, "total": 1}}
        )
        raise ValueError("scope failure")

    monkeypatch.setattr(
        runtime_v21, "complete_analysis_partition_with_instructor_v21", completion
    )
    monkeypatch.setattr(V20CandidateAnalysisProvider, "_run_once", run_once)
    provider = object.__new__(runtime_v21.V21CandidateAnalysisProvider)
    with pytest.raises(ValueError) as excinfo:
        provider._run_once()
    store = AnalysisFailureDiagnosticStore(database)
    store.record_failure(attempt_id=7, error=excinfo.value)
    rows = store.list_for_attempt(7)
    assert rows[0].failure_stage == "after_partition"
    assert rows[0].response_state == "unavailable"
    assert rows[1].payload_kind == "model_validated_partition_structured"


def test_expired_diagnostic_payload_is_pruned(database):
    store = AnalysisFailureDiagnosticStore(database)
    store.record_failure(attempt_id=7, error=ValueError("invalid"))
    with sqlite3.connect(database) as connection:
        older = (datetime.now(UTC) - timedelta(days=20)).isoformat()
        connection.execute(
            "UPDATE job_analysis_failure_diagnostics SET created_at = ?", (older,)
        )
    assert store.list_for_attempt(7) == ()
