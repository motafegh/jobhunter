from datetime import UTC, datetime
from pathlib import Path

from jobhunter.analysis_store import AnalysisStore
from jobhunter.market_insights import MarketInsights
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_store import TranslationStore


def _add_job_with_version(
    store: JobHunterStore,
    *,
    job_id: str,
    title: str,
    semantic: str,
    company_slug: str = "acme",
) -> int:
    observed_at = datetime(2026, 8, 1, tzinfo=UTC)
    posting = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=job_id,
            company_slug=company_slug,
            canonical_url=(
                f"https://jobinja.ir/companies/{company_slug}/jobs/{job_id}/example"
            ),
            observed_text=title,
        ),
        observed_at=observed_at,
    )
    version = store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=observed_at,
        requested_url=f"https://jobinja.ir/companies/{company_slug}/jobs/{job_id}/example",
        final_url=f"https://jobinja.ir/companies/{company_slug}/jobs/{job_id}/example",
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


def _record_analysis(
    analyses: AnalysisStore,
    *,
    version_id: int,
    requirement_type: str,
    concept: str = "Python",
) -> None:
    analyses.record_artifact(
        job_detail_version_id=version_id,
        translation_artifact_id=None,
        model="model",
        prompt_version="prompt",
        schema_version="schema",
        analysis={
            "role_purpose": [],
            "responsibilities": [
                {
                    "statement": "Build",
                    "evidence": "Example",
                    "confidence": "high",
                }
            ],
            "requirements": [
                {
                    "concept": concept,
                    "requirement_type": requirement_type,
                    "concept_type": "skill",
                    "evidence": "Example",
                    "confidence": "high",
                    "rationale": "",
                }
            ],
        },
        request_body={},
        raw_response={},
        created_at=datetime(2026, 8, 1, tzinfo=UTC),
    )


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
    TranslationStore(database_path).initialize()
    v1 = _add_job_with_version(store, job_id="a", title="Role A", semantic="one")
    v2 = _add_job_with_version(
        store,
        job_id="b",
        title="Role B",
        semantic="two",
        company_slug="beta",
    )
    analyses = AnalysisStore(database_path)
    _record_analysis(analyses, version_id=v1, requirement_type="required")
    _record_analysis(
        analyses,
        version_id=v2,
        requirement_type="preferred",
        concept="python",
    )

    summary = MarketInsights(
        database_path,
        analysis_model="model",
        analysis_prompt_version="prompt",
        analysis_schema_version="schema",
    ).market_summary()

    assert summary.discovered_jobs == 2
    assert summary.current_parsed_jobs == 2
    assert summary.analyzed_jobs == 2
    assert summary.distinct_employers == 2
    assert summary.largest_employer_jobs == 1
    assert summary.responsibility_claims == 2
    assert summary.requirement_claims == 2
    assert summary.analysis_model == "model"
    assert summary.analysis_prompt_version == "prompt"
    assert summary.analysis_schema_version == "schema"
    assert "Public Jobinja postings" in summary.source_scope
    assert "explicitly accepted current English P1.6" in summary.filter_scope
    assert "no title, location, triage, lifecycle" in summary.filter_scope
    assert "repost and cross-post near-duplicate adjustment is not implemented" in (
        summary.duplicate_adjustment
    )
    assert "strength columns are non-exclusive" in summary.duplicate_adjustment
    assert summary.sample_warning is not None
    assert "Only 2 current jobs" in summary.sample_warning
    assert summary.concentration_warning is None
    assert len(summary.requirements) == 1
    python = summary.requirements[0]
    assert python.jobs == 2
    assert python.required == 1
    assert python.preferred == 1


def test_market_summary_warns_when_one_employer_dominates_analyzed_sample(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    store.initialize()
    analyses = AnalysisStore(database_path)

    for index in range(6):
        company = "dominant" if index < 4 else f"other-{index}"
        version_id = _add_job_with_version(
            store,
            job_id=f"job-{index}",
            title=f"Role {index}",
            semantic=f"semantic-{index}",
            company_slug=company,
        )
        _record_analysis(
            analyses,
            version_id=version_id,
            requirement_type="required",
        )

    summary = MarketInsights(
        database_path,
        analysis_model="model",
        analysis_prompt_version="prompt",
        analysis_schema_version="schema",
    ).market_summary()

    assert summary.analyzed_jobs == 6
    assert summary.distinct_employers == 3
    assert summary.largest_employer_jobs == 4
    assert summary.sample_warning is not None
    assert summary.concentration_warning is not None
    assert "4 of 6 analyzed jobs" in summary.concentration_warning


def test_market_summary_reports_discovered_and_parsed_coverage_without_analysis(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    store.initialize()
    _add_job_with_version(store, job_id="parsed", title="Parsed", semantic="one")
    store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="unfetched",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/unfetched/example",
            observed_text="Unfetched",
        ),
        observed_at=datetime(2026, 8, 1, tzinfo=UTC),
    )

    summary = MarketInsights(database_path).market_summary()

    assert summary.discovered_jobs == 2
    assert summary.current_parsed_jobs == 1
    assert summary.analyzed_jobs == 0
    assert summary.distinct_employers == 0
    assert summary.sample_warning is None
    assert summary.requirements == ()
