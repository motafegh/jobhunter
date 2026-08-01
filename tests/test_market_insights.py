from datetime import UTC, datetime
from pathlib import Path

from jobhunter.analysis_store import AnalysisStore
from jobhunter.market_insights import MarketInsights
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore


def _add_job_with_version(
    store: JobHunterStore,
    *,
    job_id: str,
    title: str,
    semantic: str,
) -> int:
    observed_at = datetime(2026, 8, 1, tzinfo=UTC)
    posting = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=job_id,
            company_slug="acme",
            canonical_url=f"https://jobinja.ir/companies/acme/jobs/{job_id}/example",
            observed_text=title,
        ),
        observed_at=observed_at,
    )
    version = store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=observed_at,
        requested_url=f"https://jobinja.ir/companies/acme/jobs/{job_id}/example",
        final_url=f"https://jobinja.ir/companies/acme/jobs/{job_id}/example",
        status_code=200,
        content_sha256=f"raw-{semantic}",
        semantic_sha256=semantic,
        evidence_path=Path(f"{job_id}.html"),
        metadata_path=Path(f"{job_id}.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "title": title,
            "description": "Example description",
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
    )
    return version.version_id


def test_search_effectiveness_counts_unique_contributions(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    store.initialize()
    observed_at = datetime(2026, 8, 1, tzinfo=UTC)
    run_id = store.start_run(source="jobinja", started_at=observed_at)
    a = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="a",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/a/example",
            observed_text="A",
        ),
        observed_at=observed_at,
    )
    b = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="b",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/b/example",
            observed_text="B",
        ),
        observed_at=observed_at,
    )
    store.record_discovery(
        run_id=run_id,
        job_posting_id=a.job_posting_id,
        search_name="search-one",
        page_number=1,
        discovered_at=observed_at,
    )
    store.record_discovery(
        run_id=run_id,
        job_posting_id=b.job_posting_id,
        search_name="search-one",
        page_number=1,
        discovered_at=observed_at,
    )
    store.record_discovery(
        run_id=run_id,
        job_posting_id=b.job_posting_id,
        search_name="search-two",
        page_number=1,
        discovered_at=observed_at,
    )

    effectiveness = MarketInsights(database_path).search_effectiveness()
    by_name = {item.search_name: item for item in effectiveness}

    assert by_name["search-one"].distinct_jobs == 2
    assert by_name["search-one"].unique_contributions == 1
    assert by_name["search-two"].distinct_jobs == 1
    assert by_name["search-two"].unique_contributions == 0


def test_market_summary_keeps_requirement_strength_separate(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    store.initialize()
    v1 = _add_job_with_version(store, job_id="a", title="Role A", semantic="one")
    v2 = _add_job_with_version(store, job_id="b", title="Role B", semantic="two")
    analyses = AnalysisStore(database_path)
    created_at = datetime(2026, 8, 1, tzinfo=UTC)

    analyses.record_artifact(
        job_detail_version_id=v1,
        translation_artifact_id=None,
        model="model",
        prompt_version="prompt",
        schema_version="schema",
        analysis={
            "role_purpose": [],
            "responsibilities": [{"statement": "Build", "evidence": "Example", "confidence": "high"}],
            "requirements": [
                {
                    "concept": "Python",
                    "requirement_type": "required",
                    "concept_type": "skill",
                    "evidence": "Example",
                    "confidence": "high",
                    "rationale": "",
                }
            ],
        },
        request_body={},
        raw_response={},
        created_at=created_at,
    )
    analyses.record_artifact(
        job_detail_version_id=v2,
        translation_artifact_id=None,
        model="model",
        prompt_version="prompt",
        schema_version="schema",
        analysis={
            "role_purpose": [],
            "responsibilities": [],
            "requirements": [
                {
                    "concept": "python",
                    "requirement_type": "preferred",
                    "concept_type": "skill",
                    "evidence": "Example",
                    "confidence": "high",
                    "rationale": "",
                }
            ],
        },
        request_body={},
        raw_response={},
        created_at=created_at,
    )

    summary = MarketInsights(database_path).market_summary()

    assert summary.analyzed_jobs == 2
    assert summary.responsibility_claims == 1
    assert summary.requirement_claims == 2
    assert len(summary.requirements) == 1
    python = summary.requirements[0]
    assert python.jobs == 2
    assert python.required == 1
    assert python.preferred == 1
