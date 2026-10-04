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
from jobhunter.market_candidate_report import (
    GeneratedMarketCandidateReport,
    build_market_candidate_report,
)
from jobhunter.market_models import MarketDefinitionSpec, MarketSnapshotMemberInput
from jobhunter.market_role_family_report_service import MarketRoleFamilyReportService
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


def _fixture_point(text: str, refs: list[str]) -> dict:
    return {"text": text, "evidence_refs": refs}


def _fixture_group(
    label: str,
    refs: list[str],
    *,
    confidence: str = "high",
    alternatives: list[dict] | None = None,
) -> dict:
    return {
        "label": label,
        "interpretation_points": [_fixture_point(f"{label} interpretation", refs)],
        "confidence": confidence,
        "alternatives": alternatives or [],
    }


def _seed_two_job_snapshot(tmp_path: Path) -> tuple[CandidateReportHarness, int]:
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
    return harness, harness.snapshot(first, second)


def test_candidate_report_uses_exact_snapshot_evidence_and_derives_counts(
    tmp_path: Path,
    monkeypatch,
) -> None:
    harness, snapshot_id = _seed_two_job_snapshot(tmp_path)

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
        assert payload["source_aliases"] == ["J1", "J2"]
        assert [row[0] for row in payload["claims"]] == ["C1", "C2", "C3", "C4"]
        schema = kwargs["schema"]
        assert schema["properties"]["overall_observations"]["items"]["properties"][
            "evidence_refs"
        ]["items"]["enum"] == ["C1", "C2", "C3", "C4"]
        return StructuredInferenceResult(
            model=kwargs["model"],
            structured={
                "overall_observations": [
                    _fixture_point("J1 carries the main work evidence.", ["C1"]),
                    _fixture_point("J2 adds a speech specialty signal.", ["C4"]),
                ],
                "work_clusters": [
                    _fixture_group(
                        "Agent delivery",
                        ["C1", "C2"],
                        alternatives=[{"label": "Agent operations", "evidence_refs": ["C2"]}],
                    ),
                    _fixture_group("Speech specialty", ["C4"]),
                ],
                "possible_role_subfamilies": [
                    _fixture_group("Applied AI across J1 and J2", ["C1", "C4"]),
                    _fixture_group("Speech AI specialist", ["C4"]),
                ],
                "limitations": ["Small sample limits generalization."],
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

    assert report["contract"] == "market-role-family-candidate-v6"
    assert report["prompt_version"] == "market-role-family-candidate-prompt-v6"
    assert report["source_count"] == 2
    assert report["available_evidence_count"] == 4
    assert report["available_responsibility_claim_count"] == 2
    assert report["available_requirement_claim_count"] == 2
    assert report["cited_evidence_count"] == 3
    assert report["overall_supporting_source_job_ids"] == ["job-a", "job-b"]
    assert [item["text"] for item in report["overall_observations"]] == [
        "job-a carries the main work evidence.",
        "job-b adds a speech specialty signal.",
    ]

    agent_work = report["work_clusters"][0]
    assert agent_work["supporting_posting_count"] == 1
    assert agent_work["supporting_source_job_ids"] == ["job-a"]
    assert agent_work["confidence"] == "low"
    assert agent_work["support_basis"] == "responsibility_supported_work"
    assert agent_work["candidate_scope"] == "single_posting_specialty_or_outlier"
    assert agent_work["alternatives"][0]["evidence_refs"] == ["W:job-a:1"]

    speech_work = report["work_clusters"][1]
    assert speech_work["support_basis"] == "requirement_derived_specialty"
    assert speech_work["candidate_scope"] == "single_posting_specialty_or_outlier"

    role = report["possible_role_subfamilies"][0]
    assert role["supporting_posting_count"] == 2
    assert role["supporting_source_job_ids"] == ["job-a", "job-b"]
    assert role["confidence"] == "moderate"

    assert report["specialty_candidates"][0]["label"] == "Speech AI specialist"
    assert report["specialty_candidates"][0]["supporting_source_job_ids"] == ["job-b"]
    assert report["responsibility_coverage"] == {
        "postings_with_work_claims": 1,
        "postings_without_work_claims": ["job-b"],
    }
    assert report["integrity_rejection_count"] == 0
    assert report["integrity_rejections"] == []

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


def test_candidate_report_normalizes_declared_compact_citations(
    tmp_path: Path,
    monkeypatch,
) -> None:
    harness, snapshot_id = _seed_two_job_snapshot(tmp_path)
    monkeypatch.setattr(
        "jobhunter.market_candidate_report.ensure_lm_studio_model_context",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        "jobhunter.market_candidate_report.LMStudioProvider.complete_structured",
        lambda _self, **kwargs: StructuredInferenceResult(
            model=kwargs["model"],
            structured={
                "overall_observations": [
                    _fixture_point(
                        "J1 carries supported agent work (C1, C2).",
                        ["C1", "C2"],
                    ),
                ],
                "work_clusters": [
                    {
                        "label": "Agent delivery",
                        "interpretation_points": [
                            _fixture_point(
                                "The work combines workflow construction (C1) "
                                "and service operation (C2).",
                                ["C1", "C2"],
                            ),
                        ],
                        "confidence": "high",
                        "alternatives": [
                            {
                                "label": "Agent operations (C2)",
                                "evidence_refs": ["C2"],
                            }
                        ],
                    }
                ],
                "possible_role_subfamilies": [],
                "limitations": [],
            },
            request_body={},
            raw_response={},
            finish_reason="stop",
        ),
    )

    report = build_market_candidate_report(harness.settings, snapshot_id)

    assert [item["text"] for item in report["overall_observations"]] == [
        "job-a carries supported agent work."
    ]
    assert report["work_clusters"][0]["interpretation_points"][0]["text"] == (
        "The work combines workflow construction and service operation."
    )
    assert report["work_clusters"][0]["alternatives"][0]["label"] == "Agent operations"
    assert report["integrity_rejection_count"] == 0
    assert report["integrity_rejections"] == []


@pytest.mark.parametrize(
    ("text", "refs", "expected_code"),
    [
        (
            "J1 work cites C2 even though only C1 is declared.",
            ["C1"],
            "compact_evidence_id_without_matching_ref",
        ),
        (
            "J2 is a speech specialist.",
            ["C1"],
            "source_alias_without_matching_evidence",
        ),
    ],
)
def test_candidate_report_soft_filters_semantically_untraceable_prose(
    tmp_path: Path,
    monkeypatch,
    text: str,
    refs: list[str],
    expected_code: str,
) -> None:
    harness, snapshot_id = _seed_two_job_snapshot(tmp_path)
    monkeypatch.setattr(
        "jobhunter.market_candidate_report.ensure_lm_studio_model_context",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        "jobhunter.market_candidate_report.LMStudioProvider.complete_structured",
        lambda _self, **kwargs: StructuredInferenceResult(
            model=kwargs["model"],
            structured={
                "overall_observations": [
                    _fixture_point("J1 carries supported work.", ["C1"]),
                    _fixture_point(text, refs),
                ],
                "work_clusters": [],
                "possible_role_subfamilies": [],
                "limitations": [],
            },
            request_body={},
            raw_response={},
            finish_reason="stop",
        ),
    )

    report = build_market_candidate_report(harness.settings, snapshot_id)

    assert [item["text"] for item in report["overall_observations"]] == [
        "job-a carries supported work."
    ]
    assert report["integrity_rejection_count"] == 1
    assert report["integrity_rejections"] == [
        {
            "path": "overall_observations[1]",
            "code": expected_code,
        }
    ]


def test_candidate_report_filters_bad_alternative_without_dropping_group(
    tmp_path: Path,
    monkeypatch,
) -> None:
    harness, snapshot_id = _seed_two_job_snapshot(tmp_path)
    monkeypatch.setattr(
        "jobhunter.market_candidate_report.ensure_lm_studio_model_context",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        "jobhunter.market_candidate_report.LMStudioProvider.complete_structured",
        lambda _self, **kwargs: StructuredInferenceResult(
            model=kwargs["model"],
            structured={
                "overall_observations": [
                    _fixture_point("J1 carries supported work.", ["C1"]),
                ],
                "work_clusters": [
                    _fixture_group(
                        "Agent delivery",
                        ["C1"],
                        alternatives=[
                            {"label": "J2 specialist", "evidence_refs": ["C1"]},
                            {"label": "Agent workflow delivery", "evidence_refs": ["C1"]},
                        ],
                    )
                ],
                "possible_role_subfamilies": [],
                "limitations": ["J2 has no responsibility claims."],
            },
            request_body={},
            raw_response={},
            finish_reason="stop",
        ),
    )

    report = build_market_candidate_report(harness.settings, snapshot_id)

    assert report["work_clusters"][0]["label"] == "Agent delivery"
    assert [item["label"] for item in report["work_clusters"][0]["alternatives"]] == [
        "Agent workflow delivery"
    ]
    assert report["limitations"] == []
    assert report["integrity_rejection_count"] == 2
    assert report["integrity_rejections"] == [
        {
            "path": "work_clusters[0].alternatives[0]",
            "code": "source_alias_without_matching_evidence",
        },
        {
            "path": "limitations[0]",
            "code": "uncited_source_alias_in_limitation",
        },
    ]


def test_candidate_report_fails_if_no_integrity_safe_interpretation_survives(
    tmp_path: Path,
    monkeypatch,
) -> None:
    harness, snapshot_id = _seed_two_job_snapshot(tmp_path)
    monkeypatch.setattr(
        "jobhunter.market_candidate_report.ensure_lm_studio_model_context",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        "jobhunter.market_candidate_report.LMStudioProvider.complete_structured",
        lambda _self, **kwargs: StructuredInferenceResult(
            model=kwargs["model"],
            structured={
                "overall_observations": [
                    _fixture_point("J2 unsupported here.", ["C1"]),
                ],
                "work_clusters": [],
                "possible_role_subfamilies": [],
                "limitations": [],
            },
            request_body={},
            raw_response={},
            finish_reason="stop",
        ),
    )

    with pytest.raises(ValueError, match="no integrity-safe interpretation"):
        build_market_candidate_report(harness.settings, snapshot_id)


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


def test_candidate_report_cli_uses_durable_service(monkeypatch, capsys) -> None:
    settings = object()
    calls = []
    artifact = SimpleNamespace(
        id=9,
        snapshot_id=15,
        report_contract_version="market-role-family-intelligence-report-v1",
        candidate_contract_version="market-role-family-candidate-v6",
        prompt_version="market-role-family-candidate-prompt-v6",
        model="MiMo",
        generation_identity={"provider": "lm-studio", "model": "MiMo"},
        input_fingerprint="input-hash",
        generation_fingerprint="generation-hash",
        report_sha256="report-hash",
        created_at="2026-10-04T12:00:00+00:00",
        report={"snapshot_id": 15, "model": "MiMo"},
    )

    class FakeReportService:
        def __init__(self, received_settings):
            assert received_settings is settings

        def generate_report(
            self,
            snapshot_id,
            *,
            model_override=None,
            regenerate=False,
        ):
            calls.append((snapshot_id, model_override, regenerate))
            return artifact

        def effective_review_state(self, report_id):
            assert report_id == artifact.id
            return "pending"

    monkeypatch.setattr(
        market_cli,
        "_load_workspace",
        lambda _config: SimpleNamespace(settings=settings),
    )
    monkeypatch.setattr(
        market_cli,
        "MarketRoleFamilyReportService",
        FakeReportService,
    )

    assert (
        market_cli.main(
            ["candidate-report", "15", "--model", "MiMo", "--regenerate"]
        )
        == 0
    )

    output = json.loads(capsys.readouterr().out)
    assert calls == [(15, "MiMo", True)]
    assert output["id"] == 9
    assert output["snapshot_id"] == 15
    assert output["review_state"] == "pending"
    assert output["report"] == {"snapshot_id": 15, "model": "MiMo"}
    assert "request_body" not in output
    assert "raw_response" not in output


def test_candidate_report_browser_cli_durable_workflow_and_restart(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    harness, snapshot_id = _seed_two_job_snapshot(tmp_path)
    operations = WebOperationManager()
    app = create_app(harness.settings, operations=operations)
    market_web.register_market_workspace_routes(app, harness.settings)

    generation_calls = []

    def generate(_settings, prepared):
        generation_calls.append(prepared)
        evidence = prepared.evidence["W:job-a:0"]
        point = {
            "text": "Bounded fixture interpretation.",
            "evidence_refs": ["W:job-a:0"],
            "evidence": [evidence],
            "evidence_count": 1,
            "supporting_posting_count": 1,
            "supporting_source_job_ids": ["job-a"],
        }
        group = {
            "label": "Agent delivery",
            "interpretation_points": [{**point, "text": "Build agent workflows."}],
            "evidence_refs": ["W:job-a:0"],
            "evidence": [evidence],
            "evidence_count": 1,
            "supporting_posting_count": 1,
            "supporting_source_job_ids": ["job-a"],
            "confidence": "low",
            "alternatives": [],
            "support_basis": "responsibility_supported_work",
            "candidate_scope": "single_posting_specialty_or_outlier",
        }
        return GeneratedMarketCandidateReport(
            report={
                "contract": "market-role-family-candidate-v6",
                "prompt_version": "market-role-family-candidate-prompt-v6",
                "snapshot_id": prepared.snapshot_id,
                "snapshot_contract": prepared.snapshot_contract,
                "target_definition_id": prepared.target_definition_id,
                "model": prepared.model,
                "overall_observations": [point],
                "overall_supporting_source_job_ids": ["job-a"],
                "source_count": 2,
                "available_evidence_count": 4,
                "available_responsibility_claim_count": 2,
                "available_requirement_claim_count": 2,
                "cited_evidence_count": 1,
                "responsibility_coverage": {
                    "postings_with_work_claims": 1,
                    "postings_without_work_claims": ["job-b"],
                },
                "authority_note": "Candidate interpretation only.",
                "work_clusters": [group],
                "possible_role_subfamilies": [],
                "specialty_candidates": [],
                "scope_limitations": ["Small fixture sample."],
                "limitations": ["Interpretive output."],
                "integrity_rejection_count": 0,
                "integrity_rejections": [],
                "sources": list(prepared.sources.values()),
            },
            request_body={"private_request_marker": True},
            raw_response={"private_raw_marker": True},
        )

    monkeypatch.setattr(
        "jobhunter.market_role_family_report_service.generate_market_candidate_report",
        generate,
    )

    token = app.state.csrf_token
    with TestClient(app) as client:
        snapshot_page = client.get(f"/market/snapshots/{snapshot_id}")
        assert snapshot_page.status_code == 200
        assert "Generate role-family report" in snapshot_page.text
        assert "No durable interpretation" in snapshot_page.text

        response = client.post(
            f"/market/actions/snapshots/{snapshot_id}/candidate-report",
            data={"csrf_token": token, "regenerate": "false"},
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

        service = MarketRoleFamilyReportService(harness.settings)
        artifacts = service.list_reports(snapshot_id)
        assert len(artifacts) == 1
        artifact = artifacts[0]
        assert len(generation_calls) == 1

        rendered = client.get(f"/market/reports/{artifact.id}")
        assert rendered.status_code == 200
        assert "Bounded fixture interpretation." in rendered.text
        assert "Agent delivery" in rendered.text
        assert "Ready for your review" in rendered.text
        assert "Evidence used" in rendered.text
        assert "private_request_marker" not in rendered.text
        assert "private_raw_marker" not in rendered.text

        compatibility = client.get(
            f"/market/snapshots/{snapshot_id}/candidate-report",
            follow_redirects=False,
        )
        assert compatibility.status_code == 303
        assert compatibility.headers["location"] == f"/market/reports/{artifact.id}"

        reuse_response = client.post(
            f"/market/actions/snapshots/{snapshot_id}/candidate-report",
            data={"csrf_token": token, "regenerate": "false"},
            follow_redirects=False,
        )
        reuse_operation_id = (
            reuse_response.headers["location"].split("?", 1)[0].rsplit("/", 1)[-1]
        )
        for _ in range(100):
            reuse_operation = operations.get(reuse_operation_id)
            assert reuse_operation is not None
            if reuse_operation.status in {"completed", "failed"}:
                break
            time.sleep(0.01)

        assert reuse_operation.status == "completed"
        assert len(generation_calls) == 1
        assert len(service.list_reports(snapshot_id)) == 1
        assert [attempt.outcome for attempt in service.list_attempts(snapshot_id)] == [
            "completed",
            "reused",
        ]

    monkeypatch.setattr(
        market_cli,
        "_load_workspace",
        lambda _config: SimpleNamespace(settings=harness.settings),
    )
    assert market_cli.main(["role-report", "list", str(snapshot_id)]) == 0
    listed = json.loads(capsys.readouterr().out)
    assert listed[0]["id"] == artifact.id
    assert listed[0]["review_state"] == "pending"

    assert market_cli.main(["role-report", "show", str(artifact.id)]) == 0
    shown = json.loads(capsys.readouterr().out)
    assert shown["id"] == artifact.id
    assert shown["report"]["work_clusters"][0]["label"] == "Agent delivery"
    assert "request_body" not in shown
    assert "raw_response" not in shown

    assert (
        market_cli.main(
            [
                "role-report",
                "review",
                str(artifact.id),
                "--disposition",
                "accepted_for_bounded_use",
                "--note",
                "Useful bounded interpretation.",
            ]
        )
        == 0
    )
    reviewed = json.loads(capsys.readouterr().out)
    assert reviewed["effective_review_state"] == "accepted_for_bounded_use"

    fresh_operations = WebOperationManager()
    fresh_app = create_app(harness.settings, operations=fresh_operations)
    market_web.register_market_workspace_routes(fresh_app, harness.settings)
    with TestClient(fresh_app) as fresh_client:
        after_restart = fresh_client.get(f"/market/reports/{artifact.id}")
        assert after_restart.status_code == 200
        assert "Accepted for bounded use" in after_restart.text
        assert "Useful bounded interpretation." in after_restart.text

        snapshot_after_restart = fresh_client.get(
            f"/market/snapshots/{snapshot_id}"
        )
        assert snapshot_after_restart.status_code == 200
        assert f"Report #{artifact.id}" in snapshot_after_restart.text
        assert "accepted for bounded use" in snapshot_after_restart.text.lower()

