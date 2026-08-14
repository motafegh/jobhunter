from __future__ import annotations

from jobhunter.analysis_current import (
    ANALYSIS_SCHEMA_VERSION,
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
    ORIGINAL_ANALYSIS_SCHEMA_VERSION,
    ORIGINAL_PROMPT_VERSION,
    JobAnalysisService,
)
from jobhunter.analysis_service import AnalysisJobResult, AnalysisValidationError


class _FakeEnglishService:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def analyze_english_job(self, source_job_id: str) -> AnalysisJobResult:
        self.calls.append(source_job_id)
        if source_job_id == "bad":
            raise AnalysisValidationError("invalid english candidate")
        return AnalysisJobResult(
            source_job_id=source_job_id,
            artifact_id=20,
            outcome="completed",
            model="english-model",
            responsibilities=2,
            requirements=3,
            analysis_mode="english",
        )


class _FakeOriginalService:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def analyze_original_job(self, source_job_id: str) -> AnalysisJobResult:
        self.calls.append(source_job_id)
        return AnalysisJobResult(
            source_job_id=source_job_id,
            artifact_id=9,
            outcome="reused",
            model="original-model",
            responsibilities=1,
            requirements=2,
            analysis_mode="original",
        )


def _service() -> tuple[JobAnalysisService, _FakeEnglishService, _FakeOriginalService]:
    english = _FakeEnglishService()
    original = _FakeOriginalService()
    service = JobAnalysisService(english_service=english, original_service=original)  # type: ignore[arg-type]
    return service, english, original


def test_current_contract_is_english_v20_and_original_v9() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v20"
    assert ENGLISH_ANALYSIS_SCHEMA_VERSION == "job-analysis-v5"
    assert ANALYSIS_SCHEMA_VERSION == ENGLISH_ANALYSIS_SCHEMA_VERSION
    assert ORIGINAL_PROMPT_VERSION == "job-analysis-original-v9"
    assert ORIGINAL_ANALYSIS_SCHEMA_VERSION == "job-analysis-v4"


def test_current_service_routes_modes_independently() -> None:
    service, english, original = _service()

    english_result = service.analyze_english_job("dense")
    original_result = service.analyze_original_job("dense")

    assert english_result.analysis_mode == "english"
    assert original_result.analysis_mode == "original"
    assert english.calls == ["dense"]
    assert original.calls == ["dense"]


def test_current_english_batch_preserves_partial_failure_semantics() -> None:
    service, english, _ = _service()

    summary = service.run(("one", "bad", "one", "two"), limit=3)

    assert summary.analysis_mode == "english"
    assert summary.attempted == 3
    assert [item.source_job_id for item in summary.results] == ["one", "two"]
    assert [item.source_job_id for item in summary.failures] == ["bad"]
    assert english.calls == ["one", "bad", "two"]


def test_current_original_batch_uses_original_service() -> None:
    service, _, original = _service()

    summary = service.run_original(("one", "two"), limit=2)

    assert summary.analysis_mode == "original"
    assert summary.attempted == 2
    assert summary.reused == 2
    assert original.calls == ["one", "two"]
