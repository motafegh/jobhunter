from __future__ import annotations

import importlib.util
import json
import sqlite3
import subprocess
import sys
from contextlib import closing
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/inspect_p16_architecture.py"
spec = importlib.util.spec_from_file_location("inspect_p16_architecture", SCRIPT)
assert spec is not None and spec.loader is not None
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


def test_lexical_imports_are_not_calls():
    result = tool.scan_source(
        "analysis_current.py",
        b"from .analysis_store import AnalysisStore\n"
        b"class JobAnalysisService:\n"
        b"    def analyze_english_job(self, job):\n"
        b"        return self.service.analyze_english_job(job)\n",
    )
    assert result["internal_imports"] == ["jobhunter.analysis_store"]
    assert result["lexical_calls"] == {
        "JobAnalysisService.analyze_english_job": ["self.service.analyze_english_job"]
    }
    assert result["symbols"]["JobAnalysisService.analyze_english_job"] == 3


def test_static_inventory_and_markdown():
    result = tool.static_report()
    assert len(result["files"]) == len(tool.SCOPE)
    assert result == tool.static_report()
    md = tool.markdown(result)
    assert "Selected direct imports (not calls)" in md
    assert "not transitive closure or a dynamic call graph" in md
    assert "runtime" not in result and "schema" not in result


def test_curated_runtime_matches_effective_owners():
    result = tool.inspect_runtime()
    assert len(result["method_resolution"]) == 10
    assert len(result["mro"]) == 4
    assert (
        result["method_resolution"]["V30CandidateAnalysisProvider.complete_structured"]["owner"]
        == "V16CandidateAnalysisProvider.complete_structured"
    )
    assert (
        result["method_resolution"]["JobAnalysisServiceV30._persist_analysis"]["owner"]
        == "JobAnalysisServiceV28._persist_analysis"
    )
    requirement = result["schemas"]["AnalysisRequirementV30"]
    assert len(requirement["fields"]) == 8
    assert len(requirement["model_validators"]) == 13
    assert len(result["schemas"]["JobAnalysisResponseV30"]["model_validators"]) == 4


@pytest.fixture
def frozen(tmp_path):
    path = tmp_path / "closed.sqlite3"
    with closing(sqlite3.connect(path)) as db:
        db.executescript(
            "CREATE TABLE job_postings(id INTEGER PRIMARY KEY, private_text TEXT);"
            "CREATE TABLE job_detail_versions(id INTEGER PRIMARY KEY, job_posting_id INTEGER,"
            "FOREIGN KEY(job_posting_id) REFERENCES job_postings(id));"
            "CREATE TRIGGER example_fence BEFORE DELETE ON job_postings "
            "BEGIN SELECT RAISE(ABORT,'blocked'); END;"
            "INSERT INTO job_postings VALUES (1,'PRIVATE_ROW_SENTINEL');"
        )
        db.commit()
    return path


def test_schema_only_no_rows_and_no_mutation(frozen):
    before = frozen.read_bytes()
    result = tool.schema_report(frozen)
    assert result["tables"]["job_detail_versions"]["foreign_keys"][0]["table"] == "job_postings"
    assert result["tables"]["job_analysis_artifacts"] == {"present": False}
    assert result["triggers"] == [{"name": "example_fence", "table": "job_postings"}]
    assert "PRIVATE_ROW_SENTINEL" not in json.dumps(result)
    assert frozen.read_bytes() == before
    assert list(frozen.parent.iterdir()) == [frozen]


def test_authorizer_rejects_private_rows_and_mutations(frozen):
    with closing(sqlite3.connect(frozen)) as db:
        db.set_authorizer(tool._schema_authorizer)
        with pytest.raises(sqlite3.DatabaseError, match="prohibited|authorized"):
            db.execute("SELECT private_text FROM job_postings").fetchall()
        with pytest.raises(sqlite3.DatabaseError, match="authorized"):
            db.execute("DELETE FROM job_postings")
        assert db.execute("PRAGMA table_info(job_postings)").fetchall()


def test_schema_refuses_sidecar(frozen):
    Path(str(frozen) + "-wal").touch()
    with pytest.raises(ValueError, match="sidecars"):
        tool.schema_report(frozen)


def test_cli_refuses_non_acceptance_database(frozen):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--frozen-schema-db", str(frozen)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode != 0
    assert "data/local-acceptance" in result.stderr


@pytest.mark.parametrize(
    ("event", "args"),
    [
        ("open", ("fixture", "w", 1)),
        ("socket.connect", ()),
        ("sqlite3.connect", ()),
        ("subprocess.Popen", ()),
        ("os.remove", ()),
    ],
)
def test_worker_denies_side_effects(event, args):
    with pytest.raises(PermissionError, match="denied"):
        tool.restrict_worker(event, args)
