"""Isolated CLI and browser must never prune/overwrite tracked repo corpus."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from jobhunter import app_entrypoint
from jobhunter.public_corpus import (
    DEFAULT_PUBLIC_CORPUS_DIR,
    automatic_corpus_destination,
)
from jobhunter.web import launcher


def test_canonical_default_database_retains_repository_corpus(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert automatic_corpus_destination(Path("data/jobhunter.sqlite3")) == DEFAULT_PUBLIC_CORPUS_DIR


def test_alternate_database_isolated_export_even_in_repo_subdirectory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    alternate = tmp_path / "data/local-acceptance/trial/isolated.sqlite3"
    output = automatic_corpus_destination(alternate)
    assert output == alternate.parent / "public-corpus"
    assert output.resolve() != DEFAULT_PUBLIC_CORPUS_DIR.resolve()


def test_cli_auto_sync_uses_isolated_destination_for_nondefault_database(tmp_path, monkeypatch):
    alternate = tmp_path / "trial/data/job.sqlite3"
    calls = []
    settings = SimpleNamespace(
        database_path=alternate,
        analysis_lm_studio_model="analysis-model",
        capability_lm_studio_model="capability-model",
        lm_studio_model=None,
    )
    monkeypatch.setattr(app_entrypoint.Settings, "load", lambda path: settings)

    def export(db, *, output_dir, **kwargs):
        calls.append((db, output_dir))
        return SimpleNamespace(jobs=0, english_projections=0, english_analyses=0, capabilities=0)

    monkeypatch.setattr(app_entrypoint, "export_public_corpus", export)
    app_entrypoint._synchronize_public_corpus(["--config", str(tmp_path / "trial/isolated.toml")])
    assert calls == [(alternate, alternate.parent / "public-corpus")]


def test_browser_auto_sync_uses_isolated_destination(tmp_path, monkeypatch):
    alternate = tmp_path / "trial/data/job.sqlite3"
    captured = []
    monkeypatch.setattr(
        launcher,
        "export_public_corpus",
        lambda db, *, output_dir, **kwargs: captured.append((db, output_dir)),
    )
    settings = SimpleNamespace(
        database_path=alternate,
        analysis_lm_studio_model="analysis-model",
        capability_lm_studio_model="capability-model",
        lm_studio_model=None,
    )
    launcher._synchronize_public_corpus(settings)
    assert captured == [(alternate, alternate.parent / "public-corpus")]
