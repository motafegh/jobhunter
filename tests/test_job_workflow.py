from datetime import UTC, datetime
from pathlib import Path

from jobhunter.job_workflow import JobWorkflowStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore


def _job(job_id: str, title: str) -> DiscoveredJobLink:
    return DiscoveredJobLink(
        source_job_id=job_id,
        company_slug="acme",
        canonical_url=f"https://jobinja.ir/companies/acme/jobs/{job_id}/example",
        observed_text=title,
    )


def test_job_triage_is_local_user_state(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    store.initialize()
    store.upsert_job(
        job=_job("a1", "AI Security Engineer"),
        observed_at=datetime(2026, 8, 1, tzinfo=UTC),
    )
    workflow = JobWorkflowStore(database_path)

    assert workflow.get_state("a1").triage_state == "unreviewed"
    assert workflow.set_state(("a1",), triage_state="interested") == 1
    assert workflow.get_state("a1").triage_state == "interested"


def test_priority_prefers_cross_pack_relevant_discovery_and_skips_not_relevant(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    store.initialize()
    observed_at = datetime(2026, 8, 1, tzinfo=UTC)
    run_id = store.start_run(source="jobinja", started_at=observed_at)

    a1 = store.upsert_job(job=_job("a1", "AI Security Engineer"), observed_at=observed_at)
    b1 = store.upsert_job(job=_job("b1", "General Developer"), observed_at=observed_at)
    c1 = store.upsert_job(job=_job("c1", "Python Developer"), observed_at=observed_at)

    store.record_discovery(
        run_id=run_id,
        job_posting_id=a1.job_posting_id,
        search_name="pack:ai-security :: AI Security [one]",
        page_number=1,
        discovered_at=observed_at,
    )
    store.record_discovery(
        run_id=run_id,
        job_posting_id=a1.job_posting_id,
        search_name="pack:defensive-security :: Security Engineer [two]",
        page_number=1,
        discovered_at=observed_at,
    )
    store.record_discovery(
        run_id=run_id,
        job_posting_id=b1.job_posting_id,
        search_name="pack:network-platform :: Linux [three]",
        page_number=1,
        discovered_at=observed_at,
    )
    store.record_discovery(
        run_id=run_id,
        job_posting_id=c1.job_posting_id,
        search_name="pack:python-data :: Python [four]",
        page_number=1,
        discovered_at=observed_at,
    )

    workflow = JobWorkflowStore(database_path)
    workflow.set_state(("c1",), triage_state="not_relevant")
    priorities = workflow.prioritized_missing_job_ids(limit=10)

    assert [item.source_job_id for item in priorities] == ["a1", "b1"]
    assert priorities[0].distinct_packs == 2
    assert priorities[0].score > priorities[1].score
