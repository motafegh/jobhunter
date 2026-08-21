from __future__ import annotations

from jobhunter import app_entrypoint
from jobhunter.public_corpus import PublicCorpusError


def test_mutating_command_synchronizes_after_success(monkeypatch) -> None:
    calls: list[tuple[str, ...]] = []
    monkeypatch.setattr(app_entrypoint, "core_main", lambda arguments: 0)
    monkeypatch.setattr(
        app_entrypoint,
        "_synchronize_public_corpus",
        lambda arguments: calls.append(tuple(arguments)),
    )

    result = app_entrypoint.main(["jobs", "capability", "tG9K"])

    assert result == 0
    assert calls == [("jobs", "capability", "tG9K")]


def test_partial_failure_still_refreshes_durable_public_state(monkeypatch) -> None:
    calls: list[tuple[str, ...]] = []
    monkeypatch.setattr(app_entrypoint, "core_main", lambda arguments: 1)
    monkeypatch.setattr(
        app_entrypoint,
        "_synchronize_public_corpus",
        lambda arguments: calls.append(tuple(arguments)),
    )

    result = app_entrypoint.main(["jobinja", "sync"])

    assert result == 1
    assert calls == [("jobinja", "sync")]


def test_read_only_command_does_not_synchronize(monkeypatch) -> None:
    calls: list[tuple[str, ...]] = []
    monkeypatch.setattr(app_entrypoint, "core_main", lambda arguments: 0)
    monkeypatch.setattr(
        app_entrypoint,
        "_synchronize_public_corpus",
        lambda arguments: calls.append(tuple(arguments)),
    )

    result = app_entrypoint.main(["jobs", "show", "tG9K"])

    assert result == 0
    assert calls == []


def test_readiness_error_does_not_synchronize(monkeypatch) -> None:
    calls: list[tuple[str, ...]] = []
    monkeypatch.setattr(app_entrypoint, "core_main", lambda arguments: 2)
    monkeypatch.setattr(
        app_entrypoint,
        "_synchronize_public_corpus",
        lambda arguments: calls.append(tuple(arguments)),
    )

    result = app_entrypoint.main(["jobs", "analyze", "missing"])

    assert result == 2
    assert calls == []


def test_projection_failure_surfaces_without_masking_durable_success(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(app_entrypoint, "core_main", lambda arguments: 0)

    def fail(_arguments) -> None:
        raise PublicCorpusError("projection failed")

    monkeypatch.setattr(app_entrypoint, "_synchronize_public_corpus", fail)

    result = app_entrypoint.main(["translations", "run", "tG9K"])

    captured = capsys.readouterr()
    assert result == 1
    assert "Public corpus synchronization failed after the local operation" in captured.err


def test_global_config_is_removed_when_detecting_mutation() -> None:
    assert app_entrypoint._should_sync(
        ["--config", "custom.toml", "jobinja", "fetch", "tG9K"]
    )
    assert app_entrypoint._should_sync(
        ["--config=custom.toml", "jobs", "capability", "tG9K"]
    )
    assert app_entrypoint._should_sync(
        ["jobs", "review-analysis", "tmBK", "accept", "--reason", "Reviewed fully"]
    )
    assert not app_entrypoint._should_sync(
        ["jobs", "review-analysis", "tmBK", "status"]
    )
    assert not app_entrypoint._should_sync(
        ["--config", "custom.toml", "jobs", "show", "tG9K"]
    )
