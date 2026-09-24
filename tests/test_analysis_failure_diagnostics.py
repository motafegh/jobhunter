"""Local-only R05 failure-diagnostic regression tests."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from jobhunter.analysis_failure_diagnostics import (
    AnalysisFailureDiagnosticStore,
    SafeFailure,
    describe_failure,
)
from jobhunter.analysis_service_v20 import JobAnalysisServiceV20
from jobhunter.analysis_service_v21 import JobAnalysisServiceV21
from jobhunter.inference.base import InferenceConnectionError, InferenceResponseError


@pytest.fixture
def diagnostic_database(tmp_path):
    path = tmp_path / "diagnostic.sqlite3"
    with sqlite3.connect(path) as connection:
        connection.execute("CREATE TABLE job_analysis_attempts (id INTEGER PRIMARY KEY)")
        connection.execute("INSERT INTO job_analysis_attempts(id) VALUES (7)")
    return path


def _completion(content: str):
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))])


def test_public_error_does_not_interpolate_provider_exception():
    marker = "TEST_ONLY_SENSITIVE_VALUE"

    class UnsafeError(InferenceResponseError):
        def __str__(self):
            raise AssertionError("provider exception must not be stringified")

    description = describe_failure(UnsafeError(marker))
    assert description.code == "inference_response_failed"
    assert marker not in str(SafeFailure(description))
    assert describe_failure(InferenceConnectionError(marker)).code == "inference_connection_failed"


def test_retry_completion_is_private_attempt_linked_diagnostic(diagnostic_database):
    marker = "TEST_ONLY_SENSITIVE_VALUE"
    nested = RuntimeError("retry failed")
    nested.failed_attempts = [
        SimpleNamespace(attempt_number=1, completion=_completion(marker))
    ]
    failure = InferenceResponseError("untrusted error text")
    failure.__cause__ = nested
    store = AnalysisFailureDiagnosticStore(diagnostic_database)
    ids = store.record_failure(attempt_id=7, error=failure)
    assert len(ids) == 1
    record = store.list_for_attempt(7)[0]
    assert record.response_state == "available"
    assert record.retry_number == 1
    assert record.completion_text == marker
    with sqlite3.connect(diagnostic_database) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
    assert "job_analysis_artifacts" not in tables


def test_missing_and_oversize_completion_are_explicit(diagnostic_database):
    store = AnalysisFailureDiagnosticStore(diagnostic_database)
    store.record_failure(attempt_id=7, error=InferenceConnectionError("no response"))
    oversized = RuntimeError("invalid output")
    oversized.last_completion = _completion("x" * (128 * 1024 + 1))
    store.record_failure(attempt_id=7, error=oversized)
    rows = store.list_for_attempt(7)
    assert [row.response_state for row in rows] == ["unavailable", "oversize"]
    assert all(row.completion_text is None for row in rows)


def test_diagnostics_require_real_attempt_and_known_stage(diagnostic_database):
    store = AnalysisFailureDiagnosticStore(diagnostic_database)
    with pytest.raises(ValueError, match="attempt_id"):
        store.record_failure(attempt_id=0, error=ValueError("invalid"))
    with pytest.raises(ValueError, match="stage"):
        store.record_failure(attempt_id=7, error=ValueError("invalid"), failure_stage="accepted")
    with pytest.raises(sqlite3.IntegrityError):
        store.record_failure(attempt_id=77, error=ValueError("invalid"))


def test_v21_records_sanitized_failure_and_links_diagnostics():
    recorded = []
    captures = []

    class AttemptStore:
        def record_attempt(self, **kwargs):
            recorded.append(kwargs)
            return 89

    class DiagnosticStore:
        def record_failure(self, **kwargs):
            captures.append(kwargs)

    service = object.__new__(JobAnalysisServiceV21)
    service._analysis_store = AttemptStore()
    service._diagnostic_store = DiagnosticStore()
    service._model = "local-model"
    original = InferenceResponseError("TEST_ONLY_SENSITIVE_VALUE")
    service._record_failed_attempt(
        source=SimpleNamespace(job_detail_version_id=41),
        attempted_at=datetime(2026, 9, 24, tzinfo=UTC),
        error=original,
    )
    assert recorded[0]["outcome"] == "failed"
    assert recorded[0]["prompt_version"] == "job-analysis-english-v21"
    assert "TEST_ONLY_SENSITIVE_VALUE" not in str(recorded[0]["error"])
    assert captures == [{"attempt_id": 89, "error": original}]


def test_diagnostic_write_is_best_effort():
    class AttemptStore:
        def record_attempt(self, **kwargs):
            return 89

    class BrokenDiagnostics:
        def record_failure(self, **kwargs):
            raise sqlite3.OperationalError("test failure")

    service = object.__new__(JobAnalysisServiceV21)
    service._analysis_store = AttemptStore()
    service._diagnostic_store = BrokenDiagnostics()
    service._model = "local-model"
    service._record_failed_attempt(
        source=SimpleNamespace(job_detail_version_id=41),
        attempted_at=datetime(2026, 9, 24, tzinfo=UTC),
        error=InferenceResponseError("test response failure"),
    )


def test_v21_surfaces_safe_inference_failure(monkeypatch):
    def fail(self, source_job_id):
        raise InferenceResponseError("TEST_ONLY_SENSITIVE_VALUE")

    monkeypatch.setattr(JobAnalysisServiceV20, "analyze_english_job", fail)
    service = object.__new__(JobAnalysisServiceV21)
    with pytest.raises(InferenceResponseError) as excinfo:
        service.analyze_english_job("job-id")
    assert "TEST_ONLY_SENSITIVE_VALUE" not in str(excinfo.value)
