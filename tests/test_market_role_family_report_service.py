from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.market_candidate_report import (
    PROMPT_VERSION,
    REPORT_CONTRACT,
    GeneratedMarketCandidateReport,
    PreparedMarketCandidateReport,
    prepare_market_candidate_report,
)
from jobhunter.market_models import MarketDefinitionSpec, MarketSnapshotMemberInput
from jobhunter.market_role_family_report_service import MarketRoleFamilyReportService
from jobhunter.market_role_family_report_store import role_family_input_fingerprint
from jobhunter.market_store import MarketStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

_NOW = datetime(2026, 10, 4, 12, tzinfo=UTC)


class RoleFamilyReportServiceHarness:
    def __init__(self, tmp_path: Path) -> None:
        self.settings = Settings(
            data_dir=tmp_path / "data",
            evidence_dir=tmp_path / "data/evidence",
            database_path=tmp_path / "data/jobhunter.sqlite3",
            translation_enabled=False,
            analysis_lm_studio_model="fixture-analysis-model",
            analysis_max_tokens=2048,
        )
        self.source = JobHunterStore(self.settings.database_path)
        self.source.initialize()
        self.market = MarketStore(self.settings.database_path)
        self.translations = TranslationStore(self.settings.database_path)
        self.analyses = AnalysisStore(self.settings.database_path)
        self.translation_service = TranslationService(
            store=self.translations,
            provider=None,
            clock=lambda: _NOW,
        )
        target = self.market.create_target(
            slug="role-family-service",
            name="Role Family Service",
            description=None,
            created_at=_NOW,
        )
        self.definition = self.market.create_definition_version(
            target.id,
            spec=MarketDefinitionSpec(
                membership_intent="Applied AI engineering work",
                search_catalog_version="fixture-v1",
            ),
            created_at=_NOW,
        )

    def snapshot(self) -> int:
        posting = self.source.upsert_job(
            job=DiscoveredJobLink(
                source_job_id="job-a",
                company_slug="fixture",
                canonical_url="https://jobinja.ir/companies/fixture/jobs/job-a/role",
                observed_text="AI Agent Engineer",
            ),
            observed_at=_NOW,
        )
        detail = self.source.record_job_detail(
            job_posting_id=posting.job_posting_id,
            fetched_at=_NOW,
            requested_url="https://jobinja.ir/jobs/job-a",
            final_url="https://jobinja.ir/jobs/job-a",
            status_code=200,
            content_sha256="raw-job-a",
            semantic_sha256="semantic-job-a",
            evidence_path=Path("job-a.html"),
            metadata_path=Path("job-a.json"),
            parser_version="jobinja-detail-v2",
            parse_status="parsed",
            fields={
                "title": "AI Agent Engineer",
                "description": "Fixture role description.",
                "language": "en",
            },
        )
        translation = self.translation_service.translate_job("job-a")
        analysis_id = self.analyses.record_artifact(
            job_detail_version_id=detail.version_id,
            translation_artifact_id=translation.artifact_id,
            model="fixture-analysis-model",
            prompt_version="fixture-prompt",
            schema_version="job-analysis-v5",
            analysis={
                "role_purpose": [],
                "responsibilities": [
                    {
                        "statement": "Build agent workflows.",
                        "evidence": "Build agent workflows.",
                    }
                ],
                "requirements": [
                    {
                        "concept": "Python",
                        "evidence": "Python is required.",
                        "requirement_type": "required",
                        "confidence": "high",
                    }
                ],
            },
            request_body={},
            raw_response={},
            created_at=_NOW,
            semantic_review_status="accepted",
        )
        membership = self.market.record_membership(
            target_definition_version_id=self.definition.id,
            job_detail_version_id=detail.version_id,
            translation_artifact_id=translation.artifact_id,
            analysis_artifact_id=analysis_id,
            classifier_contract_version="fixture-membership-v1",
            classifier_method="model",
            classifier_identity={"provider": "fixture", "model": "fixture-membership"},
            disposition="core_match",
            reason="Fixture core match.",
            evidence_refs=("source:title",),
            confidence="high",
            created_at=_NOW,
        )
        run = self.market.start_run(
            self.definition.id,
            controls={"fixture": True},
            started_at=_NOW,
        )
        self.market.finish_run(
            run.id,
            status="completed",
            ledger={"fixture": True},
            completed_at=_NOW,
        )
        snapshot = self.market.record_snapshot(
            target_definition_version_id=self.definition.id,
            run_id=run.id,
            freshness_rule="current-active",
            source_scope={"fixture": True},
            metadata={"fixture": True},
            members=(
                MarketSnapshotMemberInput(
                    membership_id=membership.id,
                    semantic_coverage_status="accepted",
                    translation_artifact_id=translation.artifact_id,
                    analysis_artifact_id=analysis_id,
                ),
            ),
            created_at=_NOW,
        )
        return snapshot.id


def _generation(
    prepared: PreparedMarketCandidateReport,
    *,
    label: str = "Agent delivery",
) -> GeneratedMarketCandidateReport:
    return GeneratedMarketCandidateReport(
        report={
            "contract": REPORT_CONTRACT,
            "prompt_version": PROMPT_VERSION,
            "snapshot_id": prepared.snapshot_id,
            "snapshot_contract": prepared.snapshot_contract,
            "target_definition_id": prepared.target_definition_id,
            "model": prepared.model,
            "work_clusters": [{"label": label}],
            "possible_role_subfamilies": [],
            "specialty_candidates": [],
            "integrity_rejection_count": 0,
            "integrity_rejections": [],
        },
        request_body={"request": label},
        raw_response={"response": label},
    )


def test_service_generates_once_then_reuses_exact_artifact(
    tmp_path: Path,
    monkeypatch,
) -> None:
    harness = RoleFamilyReportServiceHarness(tmp_path)
    snapshot_id = harness.snapshot()
    calls: list[PreparedMarketCandidateReport] = []

    def generate(_settings, prepared):
        calls.append(prepared)
        return _generation(prepared)

    monkeypatch.setattr(
        "jobhunter.market_role_family_report_service.generate_market_candidate_report",
        generate,
    )
    service = MarketRoleFamilyReportService(
        harness.settings,
        clock=lambda: _NOW,
    )

    first = service.generate_report(snapshot_id)
    second = service.generate_report(snapshot_id)

    assert second.id == first.id
    assert len(calls) == 1
    prepared = prepare_market_candidate_report(harness.settings, snapshot_id)
    assert first.input_fingerprint == role_family_input_fingerprint(
        prepared.candidate_input
    )
    assert first.generation_identity == prepared.generation_identity
    assert first.request_body == {"request": "Agent delivery"}
    assert first.raw_response == {"response": "Agent delivery"}
    assert [attempt.outcome for attempt in service.list_attempts(snapshot_id)] == [
        "completed",
        "reused",
    ]


def test_explicit_regeneration_persists_new_artifact_for_same_generation(
    tmp_path: Path,
    monkeypatch,
) -> None:
    harness = RoleFamilyReportServiceHarness(tmp_path)
    snapshot_id = harness.snapshot()
    calls = 0

    def generate(_settings, prepared):
        nonlocal calls
        calls += 1
        return _generation(prepared, label=f"Agent delivery {calls}")

    monkeypatch.setattr(
        "jobhunter.market_role_family_report_service.generate_market_candidate_report",
        generate,
    )
    times = iter((_NOW, _NOW, _NOW + timedelta(minutes=1), _NOW + timedelta(minutes=1)))
    service = MarketRoleFamilyReportService(
        harness.settings,
        clock=lambda: next(times),
    )

    first = service.generate_report(snapshot_id)
    second = service.generate_report(snapshot_id, regenerate=True)

    assert calls == 2
    assert first.id != second.id
    assert first.generation_fingerprint == second.generation_fingerprint
    assert first.report_sha256 != second.report_sha256
    assert service.list_reports(snapshot_id) == (second, first)
    assert [attempt.outcome for attempt in service.list_attempts(snapshot_id)] == [
        "completed",
        "completed",
    ]


def test_generation_failure_records_failed_attempt_without_report(
    tmp_path: Path,
    monkeypatch,
) -> None:
    harness = RoleFamilyReportServiceHarness(tmp_path)
    snapshot_id = harness.snapshot()

    def fail(_settings, _prepared):
        raise RuntimeError("fixture generation failure")

    monkeypatch.setattr(
        "jobhunter.market_role_family_report_service.generate_market_candidate_report",
        fail,
    )
    service = MarketRoleFamilyReportService(
        harness.settings,
        clock=lambda: _NOW,
    )

    with pytest.raises(RuntimeError, match="fixture generation failure"):
        service.generate_report(snapshot_id)

    assert service.list_reports(snapshot_id) == ()
    attempts = service.list_attempts(snapshot_id)
    assert len(attempts) == 1
    assert attempts[0].outcome == "failed"
    assert attempts[0].artifact_id is None
    assert attempts[0].error_type == "RuntimeError"


def test_generated_identity_mismatch_fails_before_persistence(
    tmp_path: Path,
    monkeypatch,
) -> None:
    harness = RoleFamilyReportServiceHarness(tmp_path)
    snapshot_id = harness.snapshot()

    def mismatch(_settings, prepared):
        generated = _generation(prepared)
        generated.report["snapshot_id"] = snapshot_id + 1
        return generated

    monkeypatch.setattr(
        "jobhunter.market_role_family_report_service.generate_market_candidate_report",
        mismatch,
    )
    service = MarketRoleFamilyReportService(
        harness.settings,
        clock=lambda: _NOW,
    )

    with pytest.raises(ValueError, match="snapshot_id does not match prepared identity"):
        service.generate_report(snapshot_id)

    assert service.list_reports(snapshot_id) == ()
    attempts = service.list_attempts(snapshot_id)
    assert len(attempts) == 1
    assert attempts[0].outcome == "failed"
    assert attempts[0].error_type == "ValueError"


def test_service_review_facade_uses_append_only_effective_state(
    tmp_path: Path,
    monkeypatch,
) -> None:
    harness = RoleFamilyReportServiceHarness(tmp_path)
    snapshot_id = harness.snapshot()
    monkeypatch.setattr(
        "jobhunter.market_role_family_report_service.generate_market_candidate_report",
        lambda _settings, prepared: _generation(prepared),
    )
    service = MarketRoleFamilyReportService(
        harness.settings,
        clock=lambda: _NOW,
    )
    report = service.generate_report(snapshot_id)

    assert service.effective_review_state(report.id) == "pending"
    assert service.latest_accepted_report(snapshot_id) is None

    service.review_report(
        report.id,
        disposition="accepted_for_bounded_use",
        note="Useful bounded interpretation.",
    )
    assert service.effective_review_state(report.id) == "accepted_for_bounded_use"
    assert service.latest_accepted_report(snapshot_id) == report

    service.review_report(
        report.id,
        disposition="rejected",
        note="Superseding owner decision.",
        reviewed_at=_NOW + timedelta(minutes=1),
    )
    assert service.effective_review_state(report.id) == "rejected"
    assert service.latest_accepted_report(snapshot_id) is None
    assert [review.disposition for review in service.list_reviews(report.id)] == [
        "accepted_for_bounded_use",
        "rejected",
    ]
