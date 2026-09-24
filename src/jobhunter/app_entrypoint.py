"""Top-level JobHunter CLI wrapper with repository public-corpus synchronization."""

from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from jobhunter.config import ConfigLoadError, Settings
from jobhunter.entrypoint import main as core_main
from jobhunter.market_cli import main as market_main
from jobhunter.public_corpus import (
    DEFAULT_PUBLIC_CORPUS_DIR,
    PublicCorpusError,
    export_public_corpus,
)

_MUTATING_PREFIXES: tuple[tuple[str, ...], ...] = (
    ("run",),
    ("jobinja", "discover"),
    ("jobinja", "fetch"),
    ("jobinja", "sync"),
    ("translations", "run"),
    ("jobs", "analyze"),
    ("jobs", "capability"),
    ("market", "run"),
)


def _config_path(arguments: Sequence[str]) -> Path | None:
    for index, argument in enumerate(arguments):
        if argument == "--config":
            if index + 1 < len(arguments):
                return Path(arguments[index + 1])
            return None
        if argument.startswith("--config="):
            return Path(argument.split("=", 1)[1])
    return None


def _command_tokens(arguments: Sequence[str]) -> tuple[str, ...]:
    tokens: list[str] = []
    skip_next = False
    for argument in arguments:
        if skip_next:
            skip_next = False
            continue
        if argument == "--config":
            skip_next = True
            continue
        if argument.startswith("--config="):
            continue
        tokens.append(argument)
    return tuple(tokens)


def _market_arguments(arguments: Sequence[str]) -> list[str] | None:
    tokens = _command_tokens(arguments)
    if not tokens or tokens[0] != "market":
        return None
    normalized: list[str] = []
    config = _config_path(arguments)
    if config is not None:
        normalized.extend(("--config", str(config)))
    normalized.extend(tokens[1:])
    return normalized


def _should_sync(arguments: Sequence[str]) -> bool:
    tokens = _command_tokens(arguments)
    if (
        len(tokens) >= 4
        and tokens[:2] == ("jobs", "review-analysis")
        and tokens[3] in {"accept", "reject"}
    ):
        return True
    return any(tokens[: len(prefix)] == prefix for prefix in _MUTATING_PREFIXES)


def _effective_analysis_model(settings: Settings) -> str | None:
    return settings.analysis_lm_studio_model or settings.lm_studio_model


def _effective_capability_model(settings: Settings) -> str | None:
    return settings.capability_lm_studio_model or settings.lm_studio_model


def _synchronize_public_corpus(arguments: Sequence[str]) -> None:
    settings = Settings.load(_config_path(arguments))
    summary = export_public_corpus(
        settings.database_path,
        output_dir=DEFAULT_PUBLIC_CORPUS_DIR,
        analysis_model=_effective_analysis_model(settings),
        capability_model=_effective_capability_model(settings),
    )
    print(
        "Public corpus synchronized: "
        f"{summary.jobs} jobs, {summary.english_projections} English projections, "
        f"{summary.english_analyses} English P1.6, {summary.capabilities} capabilities"
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Run established CLI; private diagnostics/review never synchronize public corpus."""
    arguments = list(argv if argv is not None else sys.argv[1:])
    tokens = _command_tokens(arguments)
    if tokens and tokens[0] == "diagnostics":
        from jobhunter.analysis_diagnostic_cli import main as diagnostics_main

        return diagnostics_main(tokens[1:], config_path=_config_path(arguments))
    if tokens and tokens[0] == "item-review":
        from jobhunter.analysis_item_review_cli import main as item_review_main

        return item_review_main(tokens[1:], config_path=_config_path(arguments))

    market_arguments = _market_arguments(arguments)
    result = market_main(market_arguments) if market_arguments is not None else core_main(arguments)

    # Return code 2 means argument/config/readiness failure before a valid durable
    # mutation. Return code 0 or 1 may still contain completed durable work, so the
    # corpus projection is refreshed for both.
    if result == 2 or not _should_sync(arguments):
        return result

    try:
        _synchronize_public_corpus(arguments)
    except (ConfigLoadError, ValidationError, PublicCorpusError, OSError, ValueError) as exc:
        print(
            "Public corpus synchronization failed after the local operation: "
            f"{exc}",
            file=sys.stderr,
        )
        # Never roll back or obscure an already-durable SQLite result. A previously
        # successful command becomes non-zero so repository divergence is visible;
        # an already-failed command keeps its original failure status.
        return 1 if result == 0 else result

    return result


if __name__ == "__main__":
    raise SystemExit(main())
