"""Opt-in original-source brief stays read-only and never manufactures acceptance."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest

from jobhunter import app_entrypoint, source_brief_cli
from jobhunter.jobinja_details import _strip_html
from jobhunter.source_brief_cli import format_source_brief, source_brief
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore


def _original_job(tmp_path: Path) -> tuple[Path, Path]:
    db = tmp_path / "trial.sqlite3"
    body = (
        "<p><strong>Responsibilities</strong></p>"
        "<ul><li>Build Python services.</li><li>Maintain production APIs.</li></ul>"
        "<p><strong>Must Have</strong></p>"
        "<ul><li>Python proficiency.</li><li>Experience with Linux.</li></ul>"
        "<p><strong>Nice to Have</strong></p><ul><li>Familiarity with Docker.</li></ul>"
    )
    raw = (
        '<html><script type="application/ld+json">'
        + json.dumps({"@type": "JobPosting", "description": body})
        + "</script></html>"
    ).encode()
    path = tmp_path / "source.html"
    path.write_bytes(raw)
    store = JobHunterStore(db)
    store.initialize()
    posting = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="demo123",
            company_slug="example",
            canonical_url="https://jobinja.ir/companies/example/jobs/demo123/test",
            observed_text="Python Engineer",
        ),
        observed_at=datetime(2026, 11, 23, tzinfo=UTC),
    )
    store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=datetime(2026, 11, 23, tzinfo=UTC),
        requested_url="https://jobinja.ir/companies/example/jobs/demo123/test",
        final_url="https://jobinja.ir/companies/example/jobs/demo123/test",
        status_code=200,
        content_sha256=hashlib.sha256(raw).hexdigest(),
        semantic_sha256="c" * 64,
        evidence_path=path,
        metadata_path=tmp_path / "metadata.json",
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "title": "Python Engineer",
            "company": "Example Incorporated",
            "minimum_experience": "Less than 3 years",
            "description": _strip_html(body),
            "language": "en",
        },
    )
    with sqlite3.connect(db) as conn:
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    return db, path


def test_source_brief_original_drilldown_and_requiredness_are_exact(tmp_path):
    db, _ = _original_job(tmp_path)
    before = hashlib.sha256(db.read_bytes()).hexdigest()
    compact = source_brief(db, "demo123", preview_per_group=1)
    full = source_brief(db, "demo123", all_evidence=True)
    assert hashlib.sha256(db.read_bytes()).hexdigest() == before
    assert compact["candidate_only_not_accepted_employer_facts"] is True
    assert not compact["B5_independent_acceptance"]
    assert not compact["B6_production_promotion"]
    groups = {g["category"]: g for g in compact["groups"]}
    assert groups["work_duty"]["candidate_count"] == 2
    assert groups["qualification_required"]["candidate_count"] == 2
    assert groups["qualification_preferred"]["candidate_count"] == 1
    assert groups["qualification_required"]["requires_drilldown"] == 1
    assert full["groups"][1]["requires_drilldown"] == 0
    assert sum(len(g["visible"]) for g in full["groups"]) == full["extracted_source_item_count"]
    assert compact["source_metadata_verbatim"]["minimum_experience"] == "Less than 3 years"
    assert "accepted analysis" in format_source_brief(compact).lower()


def test_wrong_original_source_html_sha_fails_closed(tmp_path):
    db, path = _original_job(tmp_path)
    path.write_bytes(path.read_bytes() + b"tampered")
    with pytest.raises(ValueError, match="integrity mismatch"):
        source_brief(db, "demo123")


def test_source_brief_cli_never_triggers_automatic_corpus_export(tmp_path, monkeypatch, capsys):
    db, _ = _original_job(tmp_path)
    monkeypatch.setattr(
        source_brief_cli.Settings,
        "load",
        lambda path: SimpleNamespace(database_path=db),
    )

    def forbid_export(*args, **kwargs):
        raise AssertionError("Read-only source brief must not export corpus")

    monkeypatch.setattr(app_entrypoint, "_synchronize_public_corpus", forbid_export)
    status = app_entrypoint.main(
        [
            "--config",
            str(tmp_path / "isolated.toml"),
            "jobs",
            "source-brief",
            "demo123",
            "--json",
            "--max-per-section",
            "1",
        ]
    )
    assert status == 0
    displayed = json.loads(capsys.readouterr().out)
    assert displayed["source_job_id"] == "demo123"
    assert displayed["candidate_only_not_accepted_employer_facts"]
    assert displayed["groups"][1]["category"] == "qualification_required"


def test_missing_source_brief_refuses_implicit_fetch(tmp_path):
    db, _ = _original_job(tmp_path)
    with pytest.raises(ValueError, match="No currently parsed source"):
        source_brief(db, "unknown")
