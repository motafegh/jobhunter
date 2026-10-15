import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from test_market_candidate_report import _seed_two_job_snapshot
from test_market_role_family_report_store import _record_report

from jobhunter.market_role_family_report_store import MarketRoleFamilyReportStore
from jobhunter.web.intelligence_navigation import job_origin, market_job_url, snapshot_jobs
from jobhunter.web.launcher import build_runtime_app


def _dump(path):
    with sqlite3.connect(path) as connection:
        # Existing stores lazily initialize empty tables on first read. Check domain
        # rows, including sequences, rather than treating schema initialization as data.
        return tuple(sorted(row for row in connection.iterdump() if row.startswith("INSERT")))


def test_frozen_labels_and_navigation_survive_a_new_job_version(tmp_path: Path):
    harness, snapshot_id = _seed_two_job_snapshot(tmp_path)
    original = snapshot_jobs(harness.settings.database_path, snapshot_id)
    posting = harness.source.get_job("job-a")
    harness.source.record_job_detail(
        job_posting_id=posting.id,
        fetched_at=datetime(2026, 10, 15, tzinfo=UTC),
        requested_url=posting.canonical_url,
        final_url=posting.canonical_url,
        status_code=200,
        content_sha256="changed-content",
        semantic_sha256="changed-semantic",
        evidence_path=Path("changed.html"),
        metadata_path=Path("changed.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={"title": "A completely different role", "company": "New company"},
    )
    after = snapshot_jobs(harness.settings.database_path, snapshot_id)
    assert after["job-a"]["label"] == original["job-a"]["label"]
    assert after["job-a"]["source_changed"] is True
    app = build_runtime_app(harness.settings)
    before = _dump(harness.settings.database_path)
    with TestClient(app) as client:
        page = client.get(
            market_job_url("job-a", snapshot_id=snapshot_id, finding="responsibilities")
        )
        assert page.status_code == 200
        assert "A completely different role" in page.text
        assert "AI Agent Engineer" in page.text
        assert "The source has changed since that snapshot" in page.text
        assert f"/market/snapshots/{snapshot_id}#responsibilities" in page.text
        snapshot = client.get(f"/market/snapshots/{snapshot_id}")
        assert snapshot.status_code == 200
        assert "AI Agent Engineer" in snapshot.text
        assert "A completely different role" not in snapshot.text
        assert "from_snapshot=" in snapshot.text
    assert before == _dump(harness.settings.database_path)


def test_report_context_validates_membership_snapshot_and_finding(tmp_path: Path):
    harness, snapshot_id = _seed_two_job_snapshot(tmp_path)
    report = _record_report(
        MarketRoleFamilyReportStore(harness.settings.database_path), snapshot_id
    )
    origin = job_origin(
        harness.settings, "job-a", snapshot_id=snapshot_id, report_id=report.id, finding="work-1"
    )
    assert origin.return_url == f"/market/reports/{report.id}#work-1"
    assert parse_qs(urlsplit(origin.job_url).query)["from_report"] == [str(report.id)]
    cases = [
        ("job-a", snapshot_id + 100, report.id, "work-1", 400),
        ("unknown-job", snapshot_id, report.id, "work-1", 404),
        ("job-a", snapshot_id, report.id, "//external.example", 400),
        ("job-a", snapshot_id, report.id, "work-99", 400),
        ("job-a", snapshot_id, report.id + 100, "", 404),
        ("job-a", snapshot_id + 100, None, "", 404),
    ]
    for job_id, selected_snapshot, selected_report, finding, status in cases:
        with pytest.raises(HTTPException) as exc:
            job_origin(
                harness.settings,
                job_id,
                snapshot_id=selected_snapshot,
                report_id=selected_report,
                finding=finding,
            )
        assert exc.value.status_code == status


def test_job_subpages_keep_validated_market_context(tmp_path: Path):
    harness, snapshot_id = _seed_two_job_snapshot(tmp_path)
    with TestClient(build_runtime_app(harness.settings)) as client:
        for page in ["work-intelligence", "capability-intelligence"]:
            response = client.get(
                f"/jobs/job-a/{page}?from_snapshot={snapshot_id}&from_finding=requirements"
            )
            assert response.status_code == 200
            assert f"/market/snapshots/{snapshot_id}#requirements" in response.text
            assert f"from_snapshot={snapshot_id}" in response.text
            invalid = client.get(f"/jobs/job-a/{page}?from_snapshot=bad")
            assert invalid.status_code == 422


def test_overview_uses_existing_intelligence_without_generation(tmp_path: Path, monkeypatch):
    harness, snapshot_id = _seed_two_job_snapshot(tmp_path)

    def forbidden(*args, **kwargs):
        raise AssertionError("Viewing existing intelligence must not generate a report")

    monkeypatch.setattr(
        "jobhunter.market_role_family_report_service.generate_market_candidate_report", forbidden
    )
    app = build_runtime_app(harness.settings)
    before = _dump(harness.settings.database_path)
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert f"/market/snapshots/{snapshot_id}" in response.text
        assert response.text.index("Open Market intelligence") < response.text.index(
            "Run full workflow"
        )
        assert "Skip to content" in response.text
        assert 'aria-current="page"' in response.text
    assert before == _dump(harness.settings.database_path)
