"""Source novelty means original-text uniqueness, not merely job-ID uniqueness."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from jobhunter.source_novelty import (
    compare_exact_original_descriptions,
    novelty_report,
)
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore


def _seed(path: Path, jid: str, description: str) -> None:
    store = JobHunterStore(path)
    store.initialize()
    posting = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=jid,
            company_slug="example",
            canonical_url=f"https://jobinja.ir/companies/example/jobs/{jid}/example",
            observed_text="Example",
        ),
        observed_at=datetime(2026, 11, 23, tzinfo=UTC),
    )
    store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=datetime(2026, 11, 23, tzinfo=UTC),
        requested_url=f"https://jobinja.ir/companies/example/jobs/{jid}/example",
        final_url=f"https://jobinja.ir/companies/example/jobs/{jid}/example",
        status_code=200,
        content_sha256="a" * 64,
        semantic_sha256="b" * 64,
        evidence_path=Path("private-original.html"),
        metadata_path=Path("private-metadata.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={"description": description, "title": "Example"},
    )


def test_identical_description_is_duplicate_even_with_different_job_id(tmp_path):
    archive = tmp_path / "prior.sqlite3"
    current = tmp_path / "current.sqlite3"
    _seed(archive, "old-one", "Design and develop Python APIs.")
    _seed(current, "new-other-id", "Design and develop Python APIs.")
    result = compare_exact_original_descriptions(current, ["new-other-id"], [archive])[0]
    assert result.exact_description_found_in_archive
    assert result.duplicate_under_different_job_id
    assert result.archived_matching_job_ids == ("old-one",)


def test_same_job_id_with_different_source_description_is_distinct_relative_to_archive(tmp_path):
    archive = tmp_path / "prior.sqlite3"
    current = tmp_path / "current.sqlite3"
    _seed(archive, "same-job", "Build APIs.")
    _seed(current, "same-job", "Audit security controls.")
    result = compare_exact_original_descriptions(current, ["same-job"], [archive])[0]
    assert not result.exact_description_found_in_archive
    assert not result.duplicate_under_different_job_id


def test_exact_source_novelty_refuses_missing_archives_and_missing_candidates(tmp_path):
    current = tmp_path / "current.sqlite3"
    _seed(current, "one", "Build APIs.")
    with pytest.raises(FileNotFoundError):
        compare_exact_original_descriptions(current, ["one"], [tmp_path / "not-here.sqlite3"])
    with pytest.raises(ValueError, match="lacks a parsed original"):
        compare_exact_original_descriptions(current, ["missing"], [current])
    with pytest.raises(ValueError, match="At least one archived"):
        compare_exact_original_descriptions(current, ["one"], [])


def test_local_report_contains_only_hash_and_identifiers_not_employer_text(tmp_path):
    archive = tmp_path / "prior.sqlite3"
    current = tmp_path / "current.sqlite3"
    _seed(archive, "old", "Private original description")
    _seed(current, "new", "Private original description")
    report = novelty_report(current, ["new"], [archive])
    text = json.dumps(report)
    assert report["independent_new_source_certified"] is False
    assert report["all_distinct_within_supplied_archives"] is False
    assert "Private original description" not in text
    assert "original_description_sha256" in text
