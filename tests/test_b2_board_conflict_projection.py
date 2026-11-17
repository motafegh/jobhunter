"""Focused regression tests for B2 board/source conflict preservation."""

from __future__ import annotations

import sqlite3
import sys
import tempfile
from pathlib import Path
from runpy import run_path

import pytest

from jobhunter.source_item_candidate_b2 import interpret_original_source_candidate
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

PROJECT = run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))["b1_design_from_b2"]


def _source(description: str, salary: str) -> TranslationSourceVersion:
    return TranslationSourceVersion(
        source_job_id="synthetic_salary_pair",
        job_detail_version_id=1,
        semantic_sha256="a" * 64,
        source_language="mixed",
        fields={"description": description, "salary": salary},
    )


def test_non_overlapping_same_currency_salary_values_create_unresolved_pair() -> None:
    source = _source("حقوق: حدود ۸۰ میلیون تومان", "از ۴۵,۰۰۰,۰۰۰ تومان")
    candidate = interpret_original_source_candidate(source)
    signal = next(
        item
        for item in candidate.signals
        if item.kind == "board_prose_compensation_values_materially_differ"
    )
    draft = PROJECT(candidate, source)
    conflict = next(
        item for item in draft["conflicts"] if item["type"] == "board_vs_employer_compensation"
    )
    assert signal.source_anchor_id in {item.anchor.anchor_id for item in candidate.items}
    assert signal.board_selector == "/salary"
    assert conflict["resolution"] == "preserve_both_explicit_employer_wording"
    assert conflict["item_id_a"] != conflict["item_id_b"]


def test_compatible_salary_range_and_negotiable_values_do_not_create_conflicts() -> None:
    compatible = _source("حقوق: ۳۰ تا ۵۰ میلیون تومان", "از ۳۰,۰۰۰,۰۰۰ تومان")
    negotiated = _source("حقوق: توافقی", "توافقی")
    for source in (compatible, negotiated):
        candidate = interpret_original_source_candidate(source)
        assert not any(
            item.kind == "board_prose_compensation_values_materially_differ"
            for item in candidate.signals
        )
        assert not any(
            item["type"] == "board_vs_employer_compensation"
            for item in PROJECT(candidate, source)["conflicts"]
        )


def test_all_four_frozen_board_conflict_classes_project_without_source_precedence() -> None:
    database = (
        ROOT
        / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
    )
    if not database.is_file():
        pytest.skip("Frozen B0 source snapshot is intentionally absent in CI")
    expected = {
        "tNhZ": {"board_vs_employer_strength", "board_vs_employer_arrangement"},
        "tMps": {"board_vs_employer_experience"},
        "tNDx": {"board_vs_employer_compensation"},
        "tMjm": set(),
    }
    with tempfile.TemporaryDirectory(prefix="jobhunter-b2-conflicts-") as temp:
        copied = Path(temp) / "source.sqlite3"
        with (
            sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True) as src,
            sqlite3.connect(copied) as dst,
        ):
            src.backup(dst)
        store = TranslationStore(copied)
        for job, expected_types in expected.items():
            source = store.latest_source_version(job)
            assert source is not None
            candidate = interpret_original_source_candidate(source)
            draft = PROJECT(candidate, source)
            assert {item["type"] for item in draft["conflicts"]} == expected_types
            assert all(
                item["resolution"] == "preserve_both_explicit_employer_wording"
                for item in draft["conflicts"]
            )
            if job == "tMjm":
                assert not any(item.category == "work_duty" for item in candidate.items)
