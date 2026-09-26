from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from jobhunter.jobinja_discovery import DiscoverySummary
from jobhunter.market_aggregate_service import MarketAggregateBuildResult
from jobhunter.market_membership_service import MarketMembershipUnavailableError
from jobhunter.market_models import (
    MarketAggregateProfile,
    MarketCorpusSnapshot,
    MarketDefinitionSpec,
    MarketJobMembership,
    MarketResearchRun,
    MarketRunStatus,
    TargetMarketDefinitionVersion,
)
from jobhunter.market_snapshot_service import MarketSnapshotBuildResult
from jobhunter.market_workspace import (
    MarketRunControls,
    MarketRunCoordinator,
    MarketWorkspaceError,
    resolve_market_searches,
)
from jobhunter.search_registry import SearchCatalog, build_jobinja_keyword_url

_NOW = datetime(2026, 9, 17, 18, tzinfo=UTC)


class FakeSettings:
    def __init__(self, version="fixture-v1"):
        self.version = version

    def search_catalog(self):
        return SearchCatalog(version=self.version, packs={}, profiles={})


class FakeMarketStore:
    def __init__(self, definition, previous_ids=()):
        self.definition = definition
        self.finished = None
        self.previous_ids = previous_ids

    def latest_nonempty_snapshot_source_ids(self, definition_id):
        assert definition_id == self.definition.id
        return self.previous_ids

    def get_definition_version(self, definition_id):
        return self.definition if definition_id == self.definition.id else None

    def start_run(self, definition_id, *, controls, started_at):
        return MarketResearchRun(
            id=9,
            target_definition_version_id=definition_id,
            status="running",
            controls=controls,
            ledger={},
            started_at=started_at.isoformat(),
            completed_at=None,
            error_summary=None,
        )

    def finish_run(self, run_id, *, status, ledger, completed_at, error_summary=None):
        self.finished = MarketResearchRun(
            id=run_id,
            target_definition_version_id=self.definition.id,
            status=str(status),
            controls={},
            ledger=ledger,
            started_at=_NOW.isoformat(),
            completed_at=completed_at.isoformat(),
            error_summary=error_summary,
        )
        return self.finished


class FakePlanner:
    def __init__(self, source_ready):
        self.source_ready = source_ready
        self.calls = 0

    def plan(self, **kwargs):
        self.calls += 1
        if self.calls == 1:
            return SimpleNamespace(missing_selected=(), refresh_selected=())
        if self.calls == 2:
            return SimpleNamespace(translation_selected=())
        if self.calls == 3:
            return SimpleNamespace(analysis_selected=())
        return SimpleNamespace(
            source_ready=self.source_ready,
            ledger=lambda: {
                "source": {"candidate": len(self.source_ready), "ready": len(self.source_ready)}
            },
        )


class FakeDiscovery:
    def __init__(self, job_ids):
        self.job_ids = job_ids

    def run(self, searches):
        return DiscoverySummary(
            run_id=1,
            searches_attempted=len(searches),
            pages_fetched=1,
            unique_jobs=len(self.job_ids),
            new_jobs=0,
            known_jobs=len(self.job_ids),
            cross_search_overlaps=0,
            request_budget=10,
            requests_attempted=1,
            discovered_job_ids=self.job_ids,
            search_summaries=(),
            failures=(),
            newly_discovered=(),
        )


class NeverRun:
    def run(self, *args, **kwargs):
        raise AssertionError("This stage should not run in the fixture")

    def run_english(self, *args, **kwargs):
        raise AssertionError("This stage should not run in the fixture")


class FakeMemberships:
    def __init__(self, *, fail_job=None):
        self.fail_job = fail_job
        self.calls = []

    def qualify(self, *, target_definition_version_id, source_job_id, refresh_after_hours):
        self.calls.append(source_job_id)
        if source_job_id == self.fail_job:
            raise MarketMembershipUnavailableError("fixture model unavailable")
        membership = MarketJobMembership(
            id=100 + len(self.calls),
            target_definition_version_id=target_definition_version_id,
            source_job_id=source_job_id,
            job_detail_version_id=200 + len(self.calls),
            translation_artifact_id=None,
            analysis_artifact_id=None,
            classifier_contract_version="fixture-membership-v1",
            classifier_method="model",
            classifier_identity={"model": "fixture"},
            dependency_fingerprint=f"dep-{source_job_id}",
            disposition="core_match",
            reason="Fixture qualification.",
            evidence_refs=("source:description",),
            confidence="medium",
            supersedes_membership_id=None,
            created_at=_NOW.isoformat(),
        )
        return SimpleNamespace(membership=membership, outcome="completed")


class FakeSnapshots:
    def __init__(self):
        self.membership_ids = None

    def build_snapshot(self, *, run_id, membership_ids, refresh_after_hours):
        self.membership_ids = membership_ids
        return MarketSnapshotBuildResult(
            snapshot=MarketCorpusSnapshot(
                id=30,
                target_definition_version_id=3,
                run_id=run_id,
                snapshot_contract_version="market-corpus-snapshot-v1",
                freshness_rule="current-active",
                source_scope={},
                metadata={},
                created_at=_NOW.isoformat(),
            ),
            members=(),
        )


class FakeAggregates:
    def build_profile(self, snapshot_id):
        artifact = MarketAggregateProfile(
            id=40,
            snapshot_id=snapshot_id,
            aggregate_contract_version="market-aggregate-profile-v1",
            profile_sha256="fixture-profile",
            profile={},
            created_at=_NOW.isoformat(),
        )
        return MarketAggregateBuildResult(artifact=artifact, profile={})


def _definition(*, catalog_version="fixture-v1"):
    return TargetMarketDefinitionVersion(
        id=3,
        target_market_id=1,
        version_number=1,
        definition_fingerprint="fixture-definition",
        spec=MarketDefinitionSpec(
            membership_intent="Applied AI engineering work",
            search_catalog_version=catalog_version,
            raw_searches=(
                {
                    "name": "fixture-ai",
                    "url": build_jobinja_keyword_url("AI Engineer"),
                    "max_pages": 1,
                },
            ),
        ),
        created_at=_NOW.isoformat(),
    )


def _coordinator(job_ids, *, fail_job=None, previous_ids=()):
    definition = _definition()
    market = FakeMarketStore(definition, previous_ids)
    memberships = FakeMemberships(fail_job=fail_job)
    snapshots = FakeSnapshots()
    source_ready = tuple(dict.fromkeys((*previous_ids, *job_ids)))
    coordinator = MarketRunCoordinator(
        settings=FakeSettings(),
        market_store=market,
        planner=FakePlanner(source_ready),
        discovery_service=FakeDiscovery(job_ids),
        detail_batch=NeverRun(),
        translation_service=NeverRun(),
        analysis_service=NeverRun(),
        membership_service=memberships,
        snapshot_service=snapshots,
        aggregate_service=FakeAggregates(),
        clock=lambda: _NOW,
    )
    return coordinator, market, memberships, snapshots


def test_market_run_bounds_membership_work_and_records_remaining():
    coordinator, market, memberships, snapshots = _coordinator(("a", "b", "c", "d"))

    result = coordinator.run(
        3,
        controls=MarketRunControls(
            missing_limit=0,
            refresh_limit=0,
            translation_limit=0,
            analysis_limit=0,
            membership_limit=2,
        ),
    )

    assert memberships.calls == ["a", "b"]
    assert len(result.membership_ids) == 2
    assert snapshots.membership_ids == result.membership_ids
    assert result.run.status == MarketRunStatus.COMPLETED
    assert market.finished.ledger["stages"]["membership"] == {
        "eligible": 4,
        "selected": 2,
        "remaining": 2,
        "succeeded": 2,
        "failed": 0,
        "dispositions": {"core_match": 2},
    }


def test_market_run_preserves_partial_success_when_one_membership_fails():
    coordinator, market, memberships, snapshots = _coordinator(
        ("a", "b", "c"),
        fail_job="b",
    )

    result = coordinator.run(
        3,
        controls=MarketRunControls(
            missing_limit=0,
            refresh_limit=0,
            translation_limit=0,
            analysis_limit=0,
            membership_limit=3,
        ),
    )

    assert memberships.calls == ["a", "b", "c"]
    assert len(result.membership_ids) == 2
    assert snapshots.membership_ids == result.membership_ids
    assert result.has_failures is True
    assert result.run.status == MarketRunStatus.COMPLETED_WITH_FAILURES
    assert market.finished.ledger["stages"]["membership"]["failed"] == 1
    assert any(value.startswith("membership:b:") for value in result.failures)


def test_market_run_carries_forward_prior_members_when_search_pages_shift():
    coordinator, market, memberships, snapshots = _coordinator(
        ("new", "old-b"), previous_ids=("old-a", "old-b"),
    )

    result = coordinator.run(
        3,
        controls=MarketRunControls(
            missing_limit=0, refresh_limit=0, translation_limit=0,
            analysis_limit=0, membership_limit=3,
        ),
    )

    assert result.candidate_ids == ("old-a", "old-b", "new")
    assert memberships.calls == ["old-a", "old-b", "new"]
    assert snapshots.membership_ids == result.membership_ids
    discovery = market.finished.ledger["stages"]["discovery"]
    assert discovery["candidate_jobs"] == 2
    assert discovery["carried_forward_source_jobs"] == 2
    assert discovery["target_candidate_jobs"] == 3


def test_market_run_controls_reject_unbounded_membership_budget():
    with pytest.raises(MarketWorkspaceError, match="membership_limit"):
        MarketRunControls(membership_limit=51).validate()


def test_market_search_resolution_rejects_catalog_drift():
    with pytest.raises(MarketWorkspaceError, match="catalog version"):
        resolve_market_searches(
            FakeSettings(version="fixture-v2"),
            _definition(catalog_version="fixture-v1"),
            search_limit=10,
            default_max_pages=1,
        )
