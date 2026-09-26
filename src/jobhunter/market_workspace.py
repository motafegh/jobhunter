"""Shared I6 Market workspace and bounded target-run coordinator.

Browser and CLI adapters use this module as one service/state boundary. It composes
accepted I1-I5 owners; it does not introduce another persistence model, semantic
classifier, report layer, or publication path.
"""

from __future__ import annotations

import json
import sqlite3
from collections import Counter
from contextlib import closing, suppress
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jobhunter.analysis_current import build_job_analysis_service
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.evidence import EvidenceStore
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.jobinja_batch import JobinjaBatchFetchService
from jobhunter.jobinja_detail_service import JobinjaDetailService
from jobhunter.jobinja_discovery import DiscoverySearch, JobinjaDiscoveryService
from jobhunter.lifecycle import LifecycleStore
from jobhunter.market_affected_work import MarketAffectedWorkPlan, MarketAffectedWorkPlanner
from jobhunter.market_aggregate_service import (
    MarketAggregateBuildResult,
    MarketAggregateService,
)
from jobhunter.market_membership_service import (
    MarketMembershipError,
    MarketMembershipUnavailableError,
    build_market_membership_service,
)
from jobhunter.market_models import (
    MarketAggregateProfile,
    MarketCorpusSnapshot,
    MarketCorpusSnapshotMember,
    MarketDefinitionSpec,
    MarketJobMembership,
    MarketResearchRun,
    MarketRunStatus,
    TargetMarket,
    TargetMarketDefinitionVersion,
)
from jobhunter.market_snapshot_service import (
    MarketSnapshotBuildResult,
    build_market_snapshot_service,
)
from jobhunter.market_store import MarketStore
from jobhunter.search_registry import expand_keyword_searches
from jobhunter.sources import JobinjaClient, canonicalize_search_url
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import build_translation_service
from jobhunter.translation_store import TranslationStore


class MarketWorkspaceError(ValueError):
    """Raised when an I6 workflow input violates the accepted Market boundary."""


@dataclass(frozen=True, slots=True)
class MarketRunControls:
    request_budget: int = 20
    search_limit: int = 20
    default_max_pages: int = 1
    missing_limit: int = 10
    refresh_limit: int = 5
    refresh_after_hours: float = 24
    translation_limit: int = 20
    analysis_limit: int = 5
    membership_limit: int = 20

    def validate(self) -> MarketRunControls:
        if not 1 <= self.request_budget <= 500:
            raise MarketWorkspaceError("request_budget must be between 1 and 500")
        if not 1 <= self.search_limit <= 500:
            raise MarketWorkspaceError("search_limit must be between 1 and 500")
        if not 1 <= self.default_max_pages <= 50:
            raise MarketWorkspaceError("default_max_pages must be between 1 and 50")
        if not 0 <= self.missing_limit <= 50:
            raise MarketWorkspaceError("missing_limit must be between 0 and 50")
        if not 0 <= self.refresh_limit <= 50:
            raise MarketWorkspaceError("refresh_limit must be between 0 and 50")
        if self.missing_limit + self.refresh_limit > 50:
            raise MarketWorkspaceError("combined detail limits may not exceed 50")
        if not 0 < self.refresh_after_hours <= 8760:
            raise MarketWorkspaceError("refresh_after_hours must be in (0, 8760]")
        if not 0 <= self.translation_limit <= 50:
            raise MarketWorkspaceError("translation_limit must be between 0 and 50")
        if not 0 <= self.analysis_limit <= 20:
            raise MarketWorkspaceError("analysis_limit must be between 0 and 20")
        if not 0 <= self.membership_limit <= 50:
            raise MarketWorkspaceError("membership_limit must be between 0 and 50")
        return self


@dataclass(frozen=True, slots=True)
class MarketScopePreview:
    definition: TargetMarketDefinitionVersion
    searches: tuple[DiscoverySearch, ...]
    controls: MarketRunControls
    candidate_plan: MarketAffectedWorkPlan | None


@dataclass(frozen=True, slots=True)
class MarketRunResult:
    run: MarketResearchRun
    snapshot: MarketCorpusSnapshot | None
    profile: MarketAggregateProfile | None
    candidate_ids: tuple[str, ...]
    membership_ids: tuple[int, ...]
    failures: tuple[str, ...]

    @property
    def has_failures(self) -> bool:
        return bool(self.failures) or self.run.status == MarketRunStatus.COMPLETED_WITH_FAILURES


@dataclass(frozen=True, slots=True)
class MarketWorkspaceState:
    targets: tuple[TargetMarket, ...]
    selected_target: TargetMarket | None
    definitions: tuple[TargetMarketDefinitionVersion, ...]
    selected_definition: TargetMarketDefinitionVersion | None
    runs: tuple[MarketResearchRun, ...]
    memberships: tuple[MarketJobMembership, ...]
    snapshots: tuple[MarketCorpusSnapshot, ...]
    selected_snapshot: MarketCorpusSnapshot | None
    snapshot_members: tuple[MarketCorpusSnapshotMember, ...]
    profile: MarketAggregateProfile | None


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _split_texts(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value.strip() for value in values if value.strip()))


def _raw_search(item: dict[str, Any], index: int) -> DiscoverySearch:
    name = str(item.get("name") or f"target:raw:{index}").strip()
    url = canonicalize_search_url(str(item.get("url") or ""))
    raw_pages = item.get("max_pages", 1)
    if (
        isinstance(raw_pages, bool)
        or not isinstance(raw_pages, int)
        or not 1 <= raw_pages <= 50
    ):
        raise MarketWorkspaceError(
            "raw search max_pages must be an integer between 1 and 50"
        )
    if not name:
        raise MarketWorkspaceError("raw search name must not be empty")
    return DiscoverySearch(name=name, url=url, max_pages=raw_pages)


def resolve_market_searches(
    settings: Settings,
    definition: TargetMarketDefinitionVersion,
    *,
    search_limit: int,
    default_max_pages: int,
) -> tuple[DiscoverySearch, ...]:
    """Resolve only the immutable target acquisition envelope plus run controls."""

    catalog = settings.search_catalog()
    if catalog.version != definition.spec.search_catalog_version:
        raise MarketWorkspaceError(
            "Target definition search catalog version does not match the configured catalog; "
            "create a new definition version instead of silently changing acquisition meaning"
        )
    expanded = expand_keyword_searches(
        pack_names=definition.spec.search_packs,
        profile_names=definition.spec.search_profiles,
        extra_terms=definition.spec.extra_search_terms,
        default_max_pages=default_max_pages,
        catalog=catalog,
    )
    searches = [
        DiscoverySearch(name=item.name, url=item.url, max_pages=item.max_pages)
        for item in expanded
    ]
    searches.extend(
        _raw_search(item, index)
        for index, item in enumerate(definition.spec.raw_searches, start=1)
    )
    unique: dict[str, DiscoverySearch] = {}
    for search in searches:
        unique.setdefault(search.url, search)
    selected = tuple(unique.values())[:search_limit]
    if not selected:
        raise MarketWorkspaceError("Target definition resolves to no Jobinja searches")
    return selected


def _planner(
    settings: Settings,
    market: MarketStore | None = None,
) -> MarketAffectedWorkPlanner:
    translations = TranslationStore(settings.database_path)
    return MarketAffectedWorkPlanner(
        market_store=market or MarketStore(settings.database_path),
        source_store=JobHunterStore(settings.database_path),
        observations=JobDetailObservationStore(settings.database_path),
        translation_store=translations,
        translation_service=build_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        analysis_model=settings.effective_analysis_lm_studio_model(),
    )


def _detail_batch(settings: Settings) -> JobinjaBatchFetchService:
    detail = JobinjaDetailService(
        client=JobinjaClient(
            user_agent=settings.jobinja_user_agent,
            timeout_seconds=settings.jobinja_request_timeout_seconds,
            max_retries=settings.jobinja_max_retries,
        ),
        evidence_store=EvidenceStore(settings.evidence_dir),
        store=JobHunterStore(settings.database_path),
        observation_store=JobDetailObservationStore(settings.database_path),
        lifecycle_store=LifecycleStore(settings.database_path),
    )
    return JobinjaBatchFetchService(
        detail_service=detail,
        request_delay_seconds=settings.jobinja_request_delay_seconds,
    )


def _discovery(settings: Settings, *, request_budget: int) -> JobinjaDiscoveryService:
    return JobinjaDiscoveryService(
        client=JobinjaClient(
            user_agent=settings.jobinja_user_agent,
            timeout_seconds=settings.jobinja_request_timeout_seconds,
            max_retries=settings.jobinja_max_retries,
        ),
        evidence_store=EvidenceStore(settings.evidence_dir),
        store=JobHunterStore(settings.database_path),
        request_delay_seconds=settings.jobinja_request_delay_seconds,
        request_budget=request_budget,
    )


class MarketRunCoordinator:
    """Execute one bounded target-only Market refresh using accepted I1-I5 owners."""

    def __init__(
        self,
        *,
        settings: Settings,
        market_store: MarketStore,
        planner: MarketAffectedWorkPlanner,
        discovery_service: Any,
        detail_batch: Any,
        translation_service: Any,
        analysis_service: Any,
        membership_service: Any,
        snapshot_service: Any,
        aggregate_service: Any,
        clock=_utc_now,
    ) -> None:
        self._settings = settings
        self._market = market_store
        self._planner = planner
        self._discovery = discovery_service
        self._details = detail_batch
        self._translations = translation_service
        self._analyses = analysis_service
        self._memberships = membership_service
        self._snapshots = snapshot_service
        self._aggregates = aggregate_service
        self._clock = clock

    def preview(
        self,
        target_definition_version_id: int,
        *,
        controls: MarketRunControls,
        candidate_source_job_ids: tuple[str, ...] = (),
    ) -> MarketScopePreview:
        controls = controls.validate()
        definition = self._market.get_definition_version(target_definition_version_id)
        if definition is None:
            raise LookupError(
                f"Unknown Market target definition {target_definition_version_id}"
            )
        searches = resolve_market_searches(
            self._settings,
            definition,
            search_limit=controls.search_limit,
            default_max_pages=controls.default_max_pages,
        )
        plan = None
        if candidate_source_job_ids:
            plan = self._planner.plan(
                target_definition_version_id=definition.id,
                candidate_source_job_ids=candidate_source_job_ids,
                missing_limit=controls.missing_limit,
                refresh_limit=controls.refresh_limit,
                refresh_after_hours=controls.refresh_after_hours,
                translation_limit=controls.translation_limit,
                analysis_limit=controls.analysis_limit,
            )
        return MarketScopePreview(definition, searches, controls, plan)

    def run(
        self,
        target_definition_version_id: int,
        *,
        controls: MarketRunControls,
    ) -> MarketRunResult:
        controls = controls.validate()
        preview = self.preview(target_definition_version_id, controls=controls)
        run = self._market.start_run(
            target_definition_version_id,
            controls={
                **asdict(controls),
                "searches": [
                    {"name": item.name, "url": item.url, "max_pages": item.max_pages}
                    for item in preview.searches
                ],
            },
            started_at=self._clock(),
        )
        failures: list[str] = []
        membership_ids: list[int] = []
        candidate_ids: tuple[str, ...] = ()
        ledger: dict[str, Any] = {
            "target_definition_version_id": target_definition_version_id,
            "stages": {},
            "failures": [],
        }

        try:
            discovery = self._discovery.run(preview.searches)
            carried_forward_ids = self._market.latest_nonempty_snapshot_source_ids(
                target_definition_version_id
            )
            candidate_ids = tuple(dict.fromkeys(
                (*carried_forward_ids, *discovery.discovered_job_ids)
            ))
            failures.extend(f"discovery: {item}" for item in discovery.failures)
            ledger["stages"]["discovery"] = {
                "searches_attempted": discovery.searches_attempted,
                "requests_attempted": discovery.requests_attempted,
                "request_budget": discovery.request_budget,
                "pages_fetched": discovery.pages_fetched,
                "candidate_jobs": discovery.unique_jobs,
                "carried_forward_source_jobs": len(carried_forward_ids),
                "target_candidate_jobs": len(candidate_ids),
                "new_jobs": discovery.new_jobs,
                "known_jobs": discovery.known_jobs,
                "failures": len(discovery.failures),
            }

            source_plan = self._planner.plan(
                target_definition_version_id=target_definition_version_id,
                candidate_source_job_ids=candidate_ids,
                missing_limit=controls.missing_limit,
                refresh_limit=controls.refresh_limit,
                refresh_after_hours=controls.refresh_after_hours,
                translation_limit=0,
                analysis_limit=0,
            )
            source_selected = (*source_plan.missing_selected, *source_plan.refresh_selected)
            source_result = self._execute_source(source_selected)
            failures.extend(source_result["failure_messages"])
            ledger["stages"]["source_execution"] = source_result["ledger"]

            translation_plan = self._planner.plan(
                target_definition_version_id=target_definition_version_id,
                candidate_source_job_ids=candidate_ids,
                missing_limit=0,
                refresh_limit=0,
                refresh_after_hours=controls.refresh_after_hours,
                translation_limit=controls.translation_limit,
                analysis_limit=0,
            )
            translation_result = self._execute_translation(
                translation_plan.translation_selected,
                controls.translation_limit,
            )
            failures.extend(translation_result["failure_messages"])
            ledger["stages"]["translation"] = translation_result["ledger"]

            analysis_plan = self._planner.plan(
                target_definition_version_id=target_definition_version_id,
                candidate_source_job_ids=candidate_ids,
                missing_limit=0,
                refresh_limit=0,
                refresh_after_hours=controls.refresh_after_hours,
                translation_limit=0,
                analysis_limit=controls.analysis_limit,
            )
            analysis_result = self._execute_analysis(
                analysis_plan.analysis_selected,
                controls.analysis_limit,
            )
            failures.extend(analysis_result["failure_messages"])
            ledger["stages"]["analysis"] = analysis_result["ledger"]

            final_plan = self._planner.plan(
                target_definition_version_id=target_definition_version_id,
                candidate_source_job_ids=candidate_ids,
                missing_limit=0,
                refresh_limit=0,
                refresh_after_hours=controls.refresh_after_hours,
                translation_limit=0,
                analysis_limit=0,
            )
            ledger["stages"]["affected_work"] = final_plan.ledger()

            membership_stage = self._qualify_memberships(
                target_definition_version_id=target_definition_version_id,
                source_job_ids=final_plan.source_ready,
                refresh_after_hours=controls.refresh_after_hours,
                limit=controls.membership_limit,
            )
            membership_ids.extend(membership_stage["membership_ids"])
            failures.extend(membership_stage["failure_messages"])
            ledger["stages"]["membership"] = membership_stage["ledger"]
            ledger["failures"] = failures

            run = self._market.finish_run(
                run.id,
                status=(
                    MarketRunStatus.COMPLETED_WITH_FAILURES
                    if failures
                    else MarketRunStatus.COMPLETED
                ),
                ledger=ledger,
                completed_at=self._clock(),
                error_summary="\n".join(failures) if failures else None,
            )
        except Exception as exc:
            ledger["failures"] = [*failures, f"fatal:{type(exc).__name__}: {exc}"]
            with suppress(Exception):
                run = self._market.finish_run(
                    run.id,
                    status=MarketRunStatus.FAILED,
                    ledger=ledger,
                    completed_at=self._clock(),
                    error_summary=str(exc),
                )
            raise

        snapshot_result: MarketSnapshotBuildResult | None = None
        profile_result: MarketAggregateBuildResult | None = None
        try:
            snapshot_result = self._snapshots.build_snapshot(
                run_id=run.id,
                membership_ids=tuple(membership_ids),
                refresh_after_hours=controls.refresh_after_hours,
            )
            profile_result = self._aggregates.build_profile(snapshot_result.snapshot.id)
        except Exception as exc:
            failures.append(f"snapshot/profile: {type(exc).__name__}: {exc}")

        return MarketRunResult(
            run=run,
            snapshot=snapshot_result.snapshot if snapshot_result else None,
            profile=profile_result.artifact if profile_result else None,
            candidate_ids=candidate_ids,
            membership_ids=tuple(membership_ids),
            failures=tuple(failures),
        )

    def _execute_source(self, source_job_ids: tuple[str, ...]) -> dict[str, Any]:
        if not source_job_ids:
            return {
                "failure_messages": [],
                "ledger": {
                    "attempted": 0,
                    "succeeded": 0,
                    "new_versions": 0,
                    "unchanged": 0,
                    "failures": 0,
                },
            }
        result = self._details.run(source_job_ids)
        return {
            "failure_messages": [
                f"source:{item.source_job_id}: {item.error}" for item in result.failures
            ],
            "ledger": {
                "attempted": result.attempted,
                "succeeded": result.succeeded,
                "new_versions": result.new_versions,
                "unchanged": result.unchanged,
                "failures": len(result.failures),
            },
        }

    def _execute_translation(
        self,
        source_job_ids: tuple[str, ...],
        limit: int,
    ) -> dict[str, Any]:
        if not source_job_ids:
            return {
                "failure_messages": [],
                "ledger": {
                    "attempted": 0,
                    "completed": 0,
                    "reused": 0,
                    "failures": 0,
                },
            }
        result = self._translations.run(
            source_job_ids=source_job_ids,
            limit=max(1, limit),
        )
        return {
            "failure_messages": [
                f"translation:{item.source_job_id}: {item.error}"
                for item in result.failures
            ],
            "ledger": {
                "attempted": result.attempted,
                "completed": result.completed,
                "reused": result.reused,
                "failures": len(result.failures),
            },
        }

    def _execute_analysis(
        self,
        source_job_ids: tuple[str, ...],
        limit: int,
    ) -> dict[str, Any]:
        if not source_job_ids:
            return {
                "failure_messages": [],
                "ledger": {
                    "attempted": 0,
                    "completed_or_reused": 0,
                    "failures": 0,
                },
            }
        result = self._analyses.run_english(
            source_job_ids,
            limit=max(1, limit),
        )
        return {
            "failure_messages": [
                f"analysis:{item.source_job_id}: {item.error}" for item in result.failures
            ],
            "ledger": {
                "attempted": result.attempted,
                "completed_or_reused": len(result.results),
                "failures": len(result.failures),
            },
        }

    def _qualify_memberships(
        self,
        *,
        target_definition_version_id: int,
        source_job_ids: tuple[str, ...],
        refresh_after_hours: float,
        limit: int,
    ) -> dict[str, Any]:
        selected = source_job_ids[:limit]
        remaining = source_job_ids[limit:]
        membership_ids: list[int] = []
        failure_messages: list[str] = []
        dispositions: Counter[str] = Counter()
        for source_job_id in selected:
            try:
                result = self._memberships.qualify(
                    target_definition_version_id=target_definition_version_id,
                    source_job_id=source_job_id,
                    refresh_after_hours=refresh_after_hours,
                )
            except (
                MarketMembershipError,
                MarketMembershipUnavailableError,
                LookupError,
                OSError,
                RuntimeError,
                ValueError,
            ) as exc:
                failure_messages.append(f"membership:{source_job_id}: {exc}")
                continue
            membership_ids.append(result.membership.id)
            dispositions[result.membership.disposition] += 1
        return {
            "membership_ids": membership_ids,
            "failure_messages": failure_messages,
            "ledger": {
                "eligible": len(source_job_ids),
                "selected": len(selected),
                "remaining": len(remaining),
                "succeeded": len(membership_ids),
                "failed": len(failure_messages),
                "dispositions": dict(sorted(dispositions.items())),
            },
        }


class MarketWorkspaceService:
    """Shared read/write facade used by I6 CLI and browser adapters."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.store = MarketStore(settings.database_path)
        self._database_path = settings.database_path

    def create_target(
        self,
        *,
        slug: str,
        name: str,
        description: str | None,
    ) -> TargetMarket:
        return self.store.create_target(
            slug=slug,
            name=name,
            description=description,
            created_at=_utc_now(),
        )

    def create_definition(
        self,
        target_market_id: int,
        *,
        membership_intent: str,
        search_profiles: tuple[str, ...] = (),
        search_packs: tuple[str, ...] = (),
        extra_search_terms: tuple[str, ...] = (),
        raw_searches: tuple[dict[str, Any], ...] = (),
        include_hints: tuple[str, ...] = (),
        exclude_hints: tuple[str, ...] = (),
        geography_scope: str | None = None,
        work_arrangement_scope: str | None = None,
        seniority_scope: str | None = None,
        employment_type_scope: str | None = None,
    ) -> TargetMarketDefinitionVersion:
        intent = " ".join(membership_intent.split())
        if not intent:
            raise MarketWorkspaceError("membership_intent must not be empty")
        catalog = self.settings.search_catalog()
        spec = MarketDefinitionSpec(
            membership_intent=intent,
            search_catalog_version=catalog.version,
            search_profiles=_split_texts(search_profiles),
            search_packs=_split_texts(search_packs),
            extra_search_terms=_split_texts(extra_search_terms),
            raw_searches=raw_searches,
            include_hints=_split_texts(include_hints),
            exclude_hints=_split_texts(exclude_hints),
            geography_scope=(geography_scope or "").strip() or None,
            work_arrangement_scope=(work_arrangement_scope or "").strip() or None,
            seniority_scope=(seniority_scope or "").strip() or None,
            employment_type_scope=(employment_type_scope or "").strip() or None,
        )
        provisional = TargetMarketDefinitionVersion(
            id=-1,
            target_market_id=target_market_id,
            version_number=-1,
            definition_fingerprint="validation-only",
            spec=spec,
            created_at="",
        )
        resolve_market_searches(
            self.settings,
            provisional,
            search_limit=500,
            default_max_pages=1,
        )
        return self.store.create_definition_version(
            target_market_id,
            spec=spec,
            created_at=_utc_now(),
        )

    def preview(
        self,
        definition_id: int,
        *,
        controls: MarketRunControls,
        candidate_source_job_ids: tuple[str, ...] = (),
    ) -> MarketScopePreview:
        controls = controls.validate()
        definition = self.store.get_definition_version(definition_id)
        if definition is None:
            raise LookupError(f"Unknown Market target definition {definition_id}")
        searches = resolve_market_searches(
            self.settings,
            definition,
            search_limit=controls.search_limit,
            default_max_pages=controls.default_max_pages,
        )
        plan = None
        if candidate_source_job_ids:
            plan = _planner(self.settings, self.store).plan(
                target_definition_version_id=definition.id,
                candidate_source_job_ids=candidate_source_job_ids,
                missing_limit=controls.missing_limit,
                refresh_limit=controls.refresh_limit,
                refresh_after_hours=controls.refresh_after_hours,
                translation_limit=controls.translation_limit,
                analysis_limit=controls.analysis_limit,
            )
        return MarketScopePreview(definition, searches, controls, plan)

    def run(
        self,
        definition_id: int,
        *,
        controls: MarketRunControls,
    ) -> MarketRunResult:
        coordinator = build_market_run_coordinator_with_budget(
            self.settings,
            request_budget=controls.request_budget,
        )
        return coordinator.run(definition_id, controls=controls)

    def state(
        self,
        *,
        target_id: int | None = None,
        definition_id: int | None = None,
        snapshot_id: int | None = None,
    ) -> MarketWorkspaceState:
        explicit_target = target_id is not None
        targets = tuple(
            item
            for value in self._ids("market_targets")
            if (item := self.store.get_target(value)) is not None
        )
        selected_target = self.store.get_target(target_id) if target_id is not None else None
        if explicit_target and selected_target is None:
            raise LookupError(f"Unknown Market target {target_id}")

        selected_snapshot = None
        if snapshot_id is not None:
            selected_snapshot = self.store.get_snapshot(snapshot_id)
            if selected_snapshot is None:
                raise LookupError(f"Unknown Market snapshot {snapshot_id}")
            if (
                definition_id is not None
                and definition_id != selected_snapshot.target_definition_version_id
            ):
                raise MarketWorkspaceError(
                    "snapshot_id and definition_id name different Market definitions"
                )
            definition_id = selected_snapshot.target_definition_version_id

        selected_definition = None
        if definition_id is not None:
            selected_definition = self.store.get_definition_version(definition_id)
            if selected_definition is None:
                raise LookupError(f"Unknown Market target definition {definition_id}")
            if (
                explicit_target
                and selected_target is not None
                and selected_target.id != selected_definition.target_market_id
            ):
                raise MarketWorkspaceError(
                    "target_id and definition_id name different Market targets"
                )
            selected_target = self.store.get_target(selected_definition.target_market_id)

        if selected_target is None and targets:
            selected_target = targets[0]

        definitions: tuple[TargetMarketDefinitionVersion, ...] = ()
        if selected_target is not None:
            definitions = tuple(
                item
                for value in self._ids(
                    "market_target_definition_versions",
                    where="target_market_id = ?",
                    params=(selected_target.id,),
                )
                if (item := self.store.get_definition_version(value)) is not None
            )
            if selected_definition is None and definitions:
                selected_definition = definitions[0]

        runs: tuple[MarketResearchRun, ...] = ()
        memberships: tuple[MarketJobMembership, ...] = ()
        snapshots: tuple[MarketCorpusSnapshot, ...] = ()
        if selected_definition is not None:
            runs = tuple(
                item
                for value in self._ids(
                    "market_research_runs",
                    where="target_definition_version_id = ?",
                    params=(selected_definition.id,),
                )
                if (item := self.store.get_run(value)) is not None
            )
            memberships = tuple(
                item
                for value in self._ids(
                    "market_job_memberships",
                    where="target_definition_version_id = ?",
                    params=(selected_definition.id,),
                )
                if (item := self.store.get_membership(value)) is not None
            )
            snapshots = tuple(
                item
                for value in self._ids(
                    "market_corpus_snapshots",
                    where="target_definition_version_id = ?",
                    params=(selected_definition.id,),
                )
                if (item := self.store.get_snapshot(value)) is not None
            )

        if selected_snapshot is None and snapshots:
            selected_snapshot = snapshots[0]
        if (
            selected_snapshot is not None
            and selected_definition is not None
            and selected_snapshot.target_definition_version_id != selected_definition.id
        ):
            raise MarketWorkspaceError(
                "Selected snapshot does not belong to the selected Market definition"
            )

        members = (
            self.store.list_snapshot_members(selected_snapshot.id)
            if selected_snapshot is not None
            else ()
        )
        profile = self._profile_for_snapshot(selected_snapshot.id) if selected_snapshot else None
        return MarketWorkspaceState(
            targets=targets,
            selected_target=selected_target,
            definitions=definitions,
            selected_definition=selected_definition,
            runs=runs,
            memberships=memberships,
            snapshots=snapshots,
            selected_snapshot=selected_snapshot,
            snapshot_members=members,
            profile=profile,
        )

    def run_by_id(self, run_id: int) -> MarketResearchRun:
        run = self.store.get_run(run_id)
        if run is None:
            raise LookupError(f"Unknown Market run {run_id}")
        return run

    def snapshot_by_id(
        self,
        snapshot_id: int,
    ) -> tuple[
        MarketCorpusSnapshot,
        tuple[MarketCorpusSnapshotMember, ...],
        MarketAggregateProfile | None,
    ]:
        snapshot = self.store.get_snapshot(snapshot_id)
        if snapshot is None:
            raise LookupError(f"Unknown Market snapshot {snapshot_id}")
        return (
            snapshot,
            self.store.list_snapshot_members(snapshot_id),
            self._profile_for_snapshot(snapshot_id),
        )

    def _profile_for_snapshot(self, snapshot_id: int) -> MarketAggregateProfile | None:
        ids = self._ids(
            "market_aggregate_profiles",
            where="snapshot_id = ?",
            params=(snapshot_id,),
        )
        return self.store.get_aggregate_profile(ids[0]) if ids else None

    def _ids(
        self,
        table: str,
        *,
        where: str = "",
        params: tuple[Any, ...] = (),
    ) -> tuple[int, ...]:
        allowed = {
            "market_targets",
            "market_target_definition_versions",
            "market_research_runs",
            "market_job_memberships",
            "market_corpus_snapshots",
            "market_aggregate_profiles",
        }
        if table not in allowed:
            raise RuntimeError("Unsupported Market workspace table")
        self.store.initialize()
        clause = f" WHERE {where}" if where else ""
        database_path = Path(self._database_path).resolve()
        with closing(sqlite3.connect(f"file:{database_path}?mode=ro", uri=True)) as connection:
            rows = connection.execute(
                f"SELECT id FROM {table}{clause} ORDER BY id DESC",
                params,
            ).fetchall()
        return tuple(int(row[0]) for row in rows)


def build_market_run_coordinator_with_budget(
    settings: Settings,
    *,
    request_budget: int,
) -> MarketRunCoordinator:
    market = MarketStore(settings.database_path)
    return MarketRunCoordinator(
        settings=settings,
        market_store=market,
        planner=_planner(settings, market),
        discovery_service=_discovery(settings, request_budget=request_budget),
        detail_batch=_detail_batch(settings),
        translation_service=build_translation_service(settings),
        analysis_service=build_job_analysis_service(settings),
        membership_service=build_market_membership_service(settings),
        snapshot_service=build_market_snapshot_service(settings),
        aggregate_service=MarketAggregateService(
            database_path=settings.database_path,
            market_store=market,
            analysis_store=AnalysisStore(settings.database_path),
        ),
    )


def market_run_summary(result: MarketRunResult) -> str:
    lines = [
        f"Market run {result.run.id}: {result.run.status}",
        f"Target definition: {result.run.target_definition_version_id}",
        f"Candidates: {len(result.candidate_ids)}",
        f"Qualified memberships: {len(result.membership_ids)}",
        f"Snapshot: {result.snapshot.id if result.snapshot else 'not created'}",
        f"Aggregate profile: {result.profile.id if result.profile else 'not created'}",
        f"Failures: {len(result.failures)}",
    ]
    if result.failures:
        lines.append("Failure details:")
        lines.extend(f"- {value}" for value in result.failures)
    return "\n".join(lines)


def market_state_json(state: MarketWorkspaceState) -> str:
    def convert(value: Any) -> Any:
        if hasattr(value, "__dataclass_fields__"):
            return asdict(value)
        return value

    payload = {
        "targets": [convert(item) for item in state.targets],
        "selected_target": convert(state.selected_target),
        "definitions": [convert(item) for item in state.definitions],
        "selected_definition": convert(state.selected_definition),
        "runs": [convert(item) for item in state.runs],
        "memberships": [convert(item) for item in state.memberships],
        "snapshots": [convert(item) for item in state.snapshots],
        "selected_snapshot": convert(state.selected_snapshot),
        "snapshot_members": [convert(item) for item in state.snapshot_members],
        "profile": convert(state.profile),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
