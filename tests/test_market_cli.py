from pathlib import Path

from jobhunter import app_entrypoint, market_cli


def _config(tmp_path: Path) -> Path:
    config = tmp_path / "jobhunter.toml"
    config.write_text(
        "\n".join(
            [
                "[jobhunter]",
                f'data_dir = "{tmp_path.as_posix()}"',
                f'database_path = "{(tmp_path / "jobhunter.sqlite3").as_posix()}"',
                f'evidence_dir = "{(tmp_path / "evidence").as_posix()}"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    return config


def test_market_cli_creates_target_definition_and_shows_same_state(tmp_path, capsys):
    config = _config(tmp_path)

    assert (
        market_cli.main(
            [
                "--config",
                str(config),
                "target",
                "create",
                "--slug",
                "applied-ai",
                "--name",
                "Applied AI",
            ]
        )
        == 0
    )
    assert (
        market_cli.main(
            [
                "--config",
                str(config),
                "definition",
                "create",
                "1",
                "--intent",
                "Applied AI engineering work",
                "--profile",
                "ai-focused",
            ]
        )
        == 0
    )
    assert (
        market_cli.main(
            ["--config", str(config), "show", "--definition-id", "1"]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "Target: 1" in output
    assert "Target definition: 1" in output
    assert '"membership_intent": "Applied AI engineering work"' in output
    assert '"search_profiles"' in output
    assert "ai-focused" in output


def test_main_entrypoint_routes_market_without_falling_through(monkeypatch):
    routed = []
    core_calls = []
    sync_calls = []

    monkeypatch.setattr(
        app_entrypoint,
        "market_main",
        lambda arguments: routed.append(arguments) or 0,
    )
    monkeypatch.setattr(
        app_entrypoint,
        "core_main",
        lambda arguments: core_calls.append(arguments) or 0,
    )
    monkeypatch.setattr(
        app_entrypoint,
        "_synchronize_public_corpus",
        lambda arguments: sync_calls.append(tuple(arguments)),
    )

    result = app_entrypoint.main(
        ["--config", "custom.toml", "market", "show", "--definition-id", "4"]
    )

    assert result == 0
    assert routed == [["--config", "custom.toml", "show", "--definition-id", "4"]]
    assert core_calls == []
    assert sync_calls == []


def test_market_run_refreshes_only_existing_public_projection(monkeypatch):
    sync_calls = []
    monkeypatch.setattr(app_entrypoint, "market_main", lambda arguments: 0)
    monkeypatch.setattr(app_entrypoint, "core_main", lambda arguments: 99)
    monkeypatch.setattr(
        app_entrypoint,
        "_synchronize_public_corpus",
        lambda arguments: sync_calls.append(tuple(arguments)),
    )

    result = app_entrypoint.main(["market", "run", "7"])

    assert result == 0
    assert sync_calls == [("market", "run", "7")]
    assert app_entrypoint._should_sync(["market", "run", "7"])
    assert not app_entrypoint._should_sync(["market", "target", "create"])
