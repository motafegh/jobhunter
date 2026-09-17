"""Thin CLI adapter over the shared I6 Market workspace service."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from pydantic import ValidationError

from jobhunter.config import ConfigLoadError, Settings
from jobhunter.market_workspace import (
    MarketRunControls,
    MarketWorkspaceError,
    MarketWorkspaceService,
    market_run_summary,
    market_state_json,
)


def _controls_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--request-budget", type=int, default=20)
    parser.add_argument("--search-limit", type=int, default=20)
    parser.add_argument("--default-max-pages", type=int, default=1)
    parser.add_argument("--missing-limit", type=int, default=10)
    parser.add_argument("--refresh-limit", type=int, default=5)
    parser.add_argument("--refresh-after-hours", type=float, default=24)
    parser.add_argument("--translation-limit", type=int, default=20)
    parser.add_argument("--analysis-limit", type=int, default=5)
    parser.add_argument("--membership-limit", type=int, default=20)


def _controls(parsed: argparse.Namespace) -> MarketRunControls:
    return MarketRunControls(
        request_budget=parsed.request_budget,
        search_limit=parsed.search_limit,
        default_max_pages=parsed.default_max_pages,
        missing_limit=parsed.missing_limit,
        refresh_limit=parsed.refresh_limit,
        refresh_after_hours=parsed.refresh_after_hours,
        translation_limit=parsed.translation_limit,
        analysis_limit=parsed.analysis_limit,
        membership_limit=parsed.membership_limit,
    ).validate()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobhunter market",
        description="Operate target-scoped Market Intelligence over local durable state.",
    )
    parser.add_argument("--config", type=Path, default=None)
    commands = parser.add_subparsers(dest="command", required=True)

    target = commands.add_parser("target", help="Create or inspect stable Market targets")
    target_commands = target.add_subparsers(dest="target_command", required=True)
    target_commands.add_parser("list", help="List local Market targets")
    create_target = target_commands.add_parser("create", help="Create a stable target identity")
    create_target.add_argument("--slug", required=True)
    create_target.add_argument("--name", required=True)
    create_target.add_argument("--description", default=None)

    definition = commands.add_parser(
        "definition",
        help="Create an immutable target-definition version",
    )
    definition_commands = definition.add_subparsers(
        dest="definition_command",
        required=True,
    )
    create_definition = definition_commands.add_parser(
        "create",
        help="Create or reuse one immutable target-definition version",
    )
    create_definition.add_argument("target_id", type=int)
    create_definition.add_argument("--intent", required=True)
    create_definition.add_argument("--profile", action="append", default=[])
    create_definition.add_argument("--pack", action="append", default=[])
    create_definition.add_argument("--term", action="append", default=[])
    create_definition.add_argument("--include-hint", action="append", default=[])
    create_definition.add_argument("--exclude-hint", action="append", default=[])
    create_definition.add_argument("--geography")
    create_definition.add_argument("--work-arrangement")
    create_definition.add_argument("--seniority")
    create_definition.add_argument("--employment-type")

    show = commands.add_parser("show", help="Inspect current target/definition/snapshot state")
    show.add_argument("--target-id", type=int)
    show.add_argument("--definition-id", type=int)
    show.add_argument("--snapshot-id", type=int)

    preview = commands.add_parser("preview", help="Preview immutable search scope and work")
    preview.add_argument("definition_id", type=int)
    preview.add_argument("--job-id", action="append", default=[])
    _controls_arguments(preview)

    run = commands.add_parser("run", help="Execute one bounded target-scoped Market run")
    run.add_argument("definition_id", type=int)
    _controls_arguments(run)

    run_show = commands.add_parser("run-show", help="Inspect one persisted Market run ledger")
    run_show.add_argument("run_id", type=int)

    snapshot_show = commands.add_parser(
        "snapshot-show",
        help="Inspect an immutable snapshot, members, and deterministic profile",
    )
    snapshot_show.add_argument("snapshot_id", type=int)
    return parser


def _load_workspace(config: Path | None) -> MarketWorkspaceService:
    settings = Settings.load(config)
    return MarketWorkspaceService(settings)


def _target_command(parsed: argparse.Namespace, workspace: MarketWorkspaceService) -> int:
    if parsed.target_command == "list":
        state = workspace.state()
        if not state.targets:
            print("No Market targets exist yet.")
            return 0
        for target in state.targets:
            print(f"{target.id}\t{target.slug}\t{target.name}")
        return 0

    target = workspace.create_target(
        slug=parsed.slug,
        name=parsed.name,
        description=parsed.description,
    )
    print(f"Target: {target.id}")
    print(f"Slug: {target.slug}")
    print(f"Name: {target.name}")
    return 0


def _definition_command(
    parsed: argparse.Namespace,
    workspace: MarketWorkspaceService,
) -> int:
    definition = workspace.create_definition(
        parsed.target_id,
        membership_intent=parsed.intent,
        search_profiles=tuple(parsed.profile),
        search_packs=tuple(parsed.pack),
        extra_search_terms=tuple(parsed.term),
        include_hints=tuple(parsed.include_hint),
        exclude_hints=tuple(parsed.exclude_hint),
        geography_scope=parsed.geography,
        work_arrangement_scope=parsed.work_arrangement,
        seniority_scope=parsed.seniority,
        employment_type_scope=parsed.employment_type,
    )
    print(f"Target definition: {definition.id}")
    print(f"Version: {definition.version_number}")
    print(f"Fingerprint: {definition.definition_fingerprint}")
    return 0


def _preview_command(parsed: argparse.Namespace, workspace: MarketWorkspaceService) -> int:
    preview = workspace.preview(
        parsed.definition_id,
        controls=_controls(parsed),
        candidate_source_job_ids=tuple(parsed.job_id),
    )
    print(f"Target definition: {preview.definition.id}")
    print(f"Searches selected: {len(preview.searches)}")
    for search in preview.searches:
        print(f"- {search.name} [max_pages={search.max_pages}] {search.url}")
    if preview.candidate_plan is not None:
        print("Affected-work ledger:")
        print(json.dumps(preview.candidate_plan.ledger(), indent=2, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    parsed = build_parser().parse_args(argv)
    try:
        workspace = _load_workspace(parsed.config)
        if parsed.command == "target":
            return _target_command(parsed, workspace)
        if parsed.command == "definition":
            return _definition_command(parsed, workspace)
        if parsed.command == "show":
            print(
                market_state_json(
                    workspace.state(
                        target_id=parsed.target_id,
                        definition_id=parsed.definition_id,
                        snapshot_id=parsed.snapshot_id,
                    )
                )
            )
            return 0
        if parsed.command == "preview":
            return _preview_command(parsed, workspace)
        if parsed.command == "run":
            result = workspace.run(parsed.definition_id, controls=_controls(parsed))
            print(market_run_summary(result))
            return 1 if result.has_failures else 0
        if parsed.command == "run-show":
            print(
                json.dumps(
                    asdict(workspace.run_by_id(parsed.run_id)),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        if parsed.command == "snapshot-show":
            snapshot, members, profile = workspace.snapshot_by_id(parsed.snapshot_id)
            print(
                json.dumps(
                    {
                        "snapshot": asdict(snapshot),
                        "members": [asdict(item) for item in members],
                        "profile": asdict(profile) if profile is not None else None,
                    },
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        raise RuntimeError(f"Unsupported Market command: {parsed.command}")
    except (ConfigLoadError, ValidationError, LookupError, MarketWorkspaceError, ValueError) as exc:
        print(f"Market command is not ready: {exc}", file=sys.stderr)
        return 2
    except (OSError, RuntimeError) as exc:
        print(f"Market command failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
