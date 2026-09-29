import json
import sqlite3
import time
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from jobhunter import market_cli
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.inference.lm_studio import StructuredInferenceResult
from jobhunter.market_candidate_report import build_market_candidate_report
from jobhunter.market_models import MarketDefinitionSpec, MarketSnapshotMemberInput
from jobhunter.market_store import MarketStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore
from jobhunter.web import market_workspace as market_web
from jobhunter.web.app import create_app
from jobhunter.web.operations import WebOperationManager

_NOW = datetime(2026, 9, 29, 12, tzinfo=UTC)


class CandidateReportHarness:
    def __init__(self, tmp_path: Path) -> None:
        self.settings = Settings(
            data_dir=tmp_path / "data",
            evidence_dir=tmp_path / "data/evidence",
            database_path=tmp_path / "data/jobhunter.sqlite3",
            translation_enabled=False,
            analysis_lm_studio_model="fixture-analysis-model",
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
            slug="candidate-report",
            name="Candidate Report",
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

    def seed_job(
        self,
        source_job_id: str,
        *,
        title: str,
        responsibilities: list[dict],
        requirements: list[dict],
    ) -> MarketSnapshotMemberInput:
        posting = self.source.upsert_job(
            job=DiscoveredJobLink(
                source_job_id=source_job_id,
                company_slug="fixture",
                canonical_url=(
                    f"https://jobinja.ir/companies/fixture/jobs/{source_job_id}/role"
                ),
                observed_text=title,
            ),
            observed_at=_NOW,
        )
        detail = self.source.record_job_detail(
            job_posting_id=posting.job_posting_id,
            fetched_at=_NOW,
            requested_url=f"https://jobinja.ir/jobs/{source_job_id}",
            final_url=f"https://jobinja.ir/jobs/{source_job_id}",
            status_code=200,
            content_sha256=f"raw-{source_job_id}",
            semantic_sha256=f"semantic-{source_job_id}",
            evidence_path=Path(f"{source_job_id}.html"),
            metadata_path=Path(f"{source_job_id}.json"),
            parser_version="jobinja-detail-v2",
            parse_status="parsed",
            fields={
                "title": title,
                "description": "Fixture role description.",
                "language": "en",
            },
        )
        translation = self.translation_service.translate_job(source_job_id)
        artifact_id = self.analyses.record_artifact(
            job_detail_version_id=detail.version_id,
            translation_artifact_id=translation.artifact_id,
            model="fixture-analysis-model",
            prompt_version="fixture-prompt",
            schema_version="job-analysis-v5",
            analysis={
                "role_purpose": [],
                "responsibilities": responsibilities,
                "requirements": requirements,
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
            analysis_artifact_id=artifact_id,
            classifier_contract_version="fixture-membership-v1",
            classifier_method="model",
            classifier_identity={"provider": "fixture", "model": "fixture-membership"},
            disposition="core_match",
            reason="Fixture core match.",
            evidence_refs=("source:title",),
            confidence="high",
            created_at=_NOW,
        )
        return MarketSnapshotMemberInput(
            membership_id=membership.id,
            semantic_coverage_status="accepted",
            translation_artifact_id=translation.artifact_id,
            analysis_artifact_id=artifact_id,
        )

    def snapshot(self, *members: MarketSnapshotMemberInput) -> int:
        run = self.market.start_run(
            self.definition.id,
            controls={"fixture": True},
            started_at=_NOW,
        )
        run = self.market.finish_run(
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
            members=tuple(members),
            created_at=_NOW,
        )
        return snapshot.id


def _fixture_group(label: str, refs: list[str], *, confidence: str = "high") -> dict:
    return {
        "label": label,
        "summary": f"{label} summary",
        "why_grouped": f"{label} rationale",
        "evidence_refs": refs,
        "confidence": confidence,
        "alternatives": [],
    }


def test_candidate_report_uses_exact_snapshot_evidence_and_derives_counts(
    tmp_path: Path,
    monkeypatch,
) -> None:
    harness = CandidateReportHarness(tmp_path)
    first = harness.seed_job(
        "job-a",
        title="AI Agent Engineer",
        responsibilities=[
            {
                "statement": "Build agent workflows.",
                "evidence": "Build agent workflows.",
            },
            {
                "statement": "Operate AI services.",
                "evidence": "Operate AI services.",
            },
        ],
        requirements=[
            {
                "concept": "Python",
                "evidence": "Python is required.",
                "requirement_type": "required",
                "confidence": "high",
            }
        ],
    )
    second = harness.seed_job(
        "job-b",
        title="Speech AI Engineer",
        responsibilities=[],
        requirements=[
            {
                "concept": "Speech processing",
                "evidence": "Speech processing experience is preferred.",
                "requirement_type": "preferred",
                "confidence": "high",
            }
        ],
    )
    snapshot_id = harness.snapshot(first, second)

    monkeypatch.setattr(
        "jobhunter.market_candidate_report.ensure_lm_studio_model_context",
        lambda **kwargs: None,
    )

    def complete_structured(_self, **kwargs):
        payload = kwargs["user_payload"]
        assert payload["sample_counts"] == {
            "accepted_semantic_core_postings": 2,
            "responsibility_claims": 2,
            "requirement_claims": 2,
        }
        assert [row[0] for row in payload["claims"]] == ["C1", "C2", "C3", "C4"]
        assert kwargs["schema"]["properties"]["overall_evidence_refs"]["items"]["enum"] == [
            "C1",
            "C2",
            "C3",
            "C4",
        ]
        return StructuredInferenceResult(
            model=kwargs["model"],
            structured={
                "overall_reading": "J1 carries the main work evidence; J2 adds a niche.",
                "overall_evidence_refs": ["C1"],
                "work_clusters": [
                    _fixture_group("Agent delivery in J1", ["C1", "C2"]),
                ],
                "possible_role_subfamilies": [
                    _fixture_group("Applied AI with J1 and J2", ["C1", "C4"]),
                ],
                "limitations": ["J2 has no responsibility claims."],
            },
            request_body={},
            raw_response={},
            finish_reason="stop",
        )

    monkeypatch.setattr(
        "jobhunter.market_candidate_report.LMStudioProvider.complete_structured",
        complete_structured,
    )

    with sqlite3.connect(harness.settings.database_path) as connection:
        before = {
            table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in (
                "job_analysis_artifacts",
                "market_corpus_snapshots",
                "market_corpus_snapshot_members",
            )
        }

    report = build_market_candidate_report(harness.settings, snapshot_id)

    assert report["contract"] == "market-role-family-candidate-v3"
    assert report["source_count"] == 2
    assert report["evidence_count"] == 4
    assert "job-a" in report["overall_reading"]
    assert "job-b" in report["overall_reading"]
    assert "J1" not in report["overall_reading"]
    assert "J2" not in report["overall_reading"]

    work = report["work_clusters"][0]
    assert work["supporting_posting_count"] == 1
    assert work["supporting_source_job_ids"] == ["job-a"]
    assert work["confidence"] == "low"

    role = report["possible_role_subfamilies"][0]
    assert role["supporting_posting_count"] == 2
    assert role["supporting_source_job_ids"] == ["job-a", "job-b"]
    assert role["confidence"] == "moderate"

    assert report["responsibility_coverage"] == {
        "postings_with_work_claims": 1,
        "postings_without_work_claims": ["job-b"],
    }

    with sqlite3.connect(harness.settings.database_path) as connection:
        after = {
            table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in before
        }
        candidate_tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE '%candidate%report%'"
        ).fetchall()

    assert after == before
    assert candidate_tables == []


def test_candidate_report_rejects_snapshot_analysis_identity_mismatch(
    tmp_path: Path,
    monkeypatch,
) -> None:
    harness = CandidateReportHarness(tmp_path)
    member = harness.seed_job(
        "job-a",
        title="AI Engineer",
        responsibilities=[
            {
                "statement": "Build AI systems.",
                "evidence": "Build AI systems.",
            }
        ],
        requirements=[],
    )
    snapshot_id = harness.snapshot(member)

    original = AnalysisStore.artifact_by_id

    def mismatched_artifact(store: AnalysisStore, artifact_id: int):
        artifact = original(store, artifact_id)
        assert artifact is not None
        return replace(artifact, source_job_id="wrong-job")

    monkeypatch.setattr(AnalysisStore, "artifact_by_id", mismatched_artifact)

    with pytest.raises(ValueError, match="identity mismatch"):
        build_market_candidate_report(harness.settings, snapshot_id)


def test_candidate_report_cli_passes_model_override(monkeypatch, capsys) -> None:
    settings = object()
    calls = []
    monkeypatch.setattr(
        market_cli,
        "_load_workspace",
        lambda _config: SimpleNamespace(settings=settings),
    )
    monkeypatch.setattr(
        market_cli,
        "build_market_candidate_report",
        lambda received_settings, snapshot_id, model_override=None: calls.append(
            (received_settings, snapshot_id, model_override)
        )
        or {"snapshot_id": snapshot_id, "model": model_override},
    )

    assert market_cli.main(["candidate-report", "15", "--model", "MiMo"]) == 0

    output = json.loads(capsys.readouterr().out)
    assert calls == [(settings, 15, "MiMo")]
    assert output == {"snapshot_id": 15, "model": "MiMo"}


def test_candidate_report_browser_operation_and_rendering(
    tmp_path: Path,
    monkeypatch,
) -> None:
    settings = Settings(
        data_dir=tmp_path / "data",
        evidence_dir=tmp_path / "data/evidence",
        database_path=tmp_path / "data/jobhunter.sqlite3",
        translation_enabled=False,
    )
    operations = WebOperationManager()
    app = create_app(settings, operations=operations)
    market_web.register_market_workspace_routes(app, settings)

    evidence = {
        "source_job_id": "job-a",
        "analysis_artifact_id": 7,
        "kind": "responsibility",
        "ref": "W:job-a:0",
        "statement": "Build agent workflows.",
        "source_excerpt": "Build agent workflows.",
    }
    report = {
        "contract": "market-role-family-candidate-v3",
        "snapshot_id": 15,
        "overall_reading": "Bounded fixture interpretation.",
        "overall_evidence": [evidence],
        "model": "fixture-model",
        "source_count": 1,
        "evidence_count": 1,
        "responsibility_coverage": {
            "postings_with_work_claims": 1,
            "postings_without_work_claims": [],
        },
        "authority_note": "Candidate interpretation only.",
        "work_clusters": [
            {
                "label": "Agent delivery",
                "summary": "Build agent workflows.",
                "why_grouped": "One exact responsibility supports this candidate group.",
                "supporting_posting_count": 1,
                "supporting_source_job_ids": ["job-a"],
                "confidence": "low",
                "alternatives": [],
                "evidence": [evidence],
            }
        ],
        "possible_role_subfamilies": [],
        "scope_limitations": ["Small fixture sample."],
        "limitations": ["Interpretive output."],
    }

    monkeypatch.setattr(
        market_web,
        "build_market_candidate_report",
        lambda _settings, snapshot_id: {**report, "snapshot_id": snapshot_id},
    )
    with market_web._CANDIDATE_REPORTS_LOCK:
        market_web._CANDIDATE_REPORTS.clear()

    try:
        token = app.state.csrf_token
        with TestClient(app) as client:
            missing = client.get("/market/snapshots/15/candidate-report")
            assert missing.status_code == 404

            response = client.post(
                "/market/actions/snapshots/15/candidate-report",
                data={"csrf_token": token},
                follow_redirects=False,
            )
            assert response.status_code == 303
            operation_id = response.headers["location"].split("?", 1)[0].rsplit("/", 1)[-1]

            for _ in range(100):
                operation = operations.get(operation_id)
                assert operation is not None
                if operation.status in {"completed", "failed"}:
                    break
                time.sleep(0.01)

            assert operation.status == "completed"
            rendered = client.get("/market/snapshots/15/candidate-report")

        assert rendered.status_code == 200
        assert "Bounded fixture interpretation." in rendered.text
        assert "Agent delivery" in rendered.text
        assert "job-a" in rendered.text
        assert "Candidate interpretation only." in rendered.text
    finally:
        with market_web._CANDIDATE_REPORTS_LOCK:
            market_web._CANDIDATE_REPORTS.clear()
