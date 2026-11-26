"""Bounded P1.6 developer inspection; not a call graph or semantic evaluator."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import inspect
import json
import os
import sqlite3
import subprocess
import sys
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "jobhunter"
SCOPE = (
    "app_entrypoint.py",
    "entrypoint.py",
    "analysis_current.py",
    "analysis_runtime.py",
    "analysis_service.py",
    "jobinja_detail_service.py",
    "translation_service.py",
    "translation_store.py",
    "translation/projection.py",
    "analysis_runtime_v20.py",
    "inference/lm_studio_runtime.py",
    "inference/instructor_lm_studio_v24.py",
    "inference/instructor_lm_studio_v20.py",
    "inference/instructor_lm_studio_v23.py",
    "analysis_runtime_v23.py",
    "analysis_persistence_v23.py",
    "analysis_store.py",
    "analysis_failure_diagnostics.py",
    "analysis_item_review.py",
    "source_span_identity.py",
    "source_item_candidate_b2_v7_dom.py",
    "source_bound_translation_b3.py",
    "source_job_understanding_b4.py",
    "source_qualified_b4v5.py",
    "source_qualified_b4v6.py",
    "source_brief_cli.py",
    "capability_service_v8.py",
    "work_intelligence_service.py",
    "canonical_registry_review.py",
    "public_corpus.py",
    "web/app.py",
    # Additional explicit method-ownership and schema seams, not transitive closure.
    "analysis_runtime_v30.py",
    "analysis_runtime_v29.py",
    "analysis_runtime_v27.py",
    "analysis_runtime_v26.py",
    "analysis_runtime_v25.py",
    "analysis_runtime_v21.py",
    "analysis_runtime_v16.py",
    "analysis_runtime_v15.py",
    "analysis_service_v30.py",
    "analysis_service_v28.py",
    "analysis_service_v21.py",
    "analysis_service_v20.py",
    "inference/instructor_lm_studio_v30.py",
)
CLASSES = (
    (
        "analysis_service_v30",
        "JobAnalysisServiceV30",
        (
            "analyze_english_job",
            "_persist_analysis",
            "_record_failed_attempt",
        ),
    ),
    (
        "analysis_runtime_v30",
        "V30CandidateAnalysisProvider",
        (
            "complete_structured",
            "_run_once",
            "_requirement_coverage_plan",
            "_responsibility_coverage_plan",
            "_requirement_partitions",
            "_complete_partition",
            "_persistable_structured",
        ),
    ),
    ("inference.instructor_lm_studio_v30", "JobAnalysisResponseV30", ()),
    ("inference.instructor_lm_studio_v30", "AnalysisRequirementV30", ()),
)
TABLES = (
    "job_postings",
    "job_detail_versions",
    "job_translation_artifacts",
    "job_analysis_artifacts",
    "job_analysis_attempts",
    "job_analysis_item_review_sessions",
    "job_analysis_item_review_events",
)
CALL_TARGETS = (
    ("analysis_runtime_v30.py", "V30CandidateAnalysisProvider._complete_partition"),
    ("analysis_runtime_v16.py", "V16CandidateAnalysisProvider.complete_structured"),
    ("analysis_runtime_v15.py", "V15CandidateAnalysisProvider.complete_structured"),
    ("analysis_current.py", "JobAnalysisService.analyze_english_job"),
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def module_name(rel: str) -> str:
    return "jobhunter." + rel.removesuffix(".py").replace("/", ".")


def scan_source(rel: str, data: bytes) -> dict:
    """Lexical facts only; local imports are included, not execution claims."""
    tree = ast.parse(data)
    definitions = {}
    call_targets = {}
    imports = set()

    def walk(nodes, prefix=""):
        for node in nodes:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix + node.name
                definitions[name] = node.lineno
                if isinstance(node, ast.ClassDef):
                    walk(node.body, name + ".")
                if (rel, name) in CALL_TARGETS:
                    call_targets[name] = sorted(
                        {ast.unparse(n.func) for n in ast.walk(node) if isinstance(n, ast.Call)}
                    )

    walk(tree.body)
    package = module_name(rel).rsplit(".", 1)[0]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(a.name for a in node.names if a.name.startswith("jobhunter."))
        elif isinstance(node, ast.ImportFrom):
            name = node.module or ""
            if node.level:
                name = importlib.util.resolve_name("." * node.level + name, package)
            if name.startswith("jobhunter."):
                imports.add(name)
            elif name == "jobhunter":
                imports.update("jobhunter." + a.name for a in node.names if a.name != "*")
    return {
        "sha256": digest(data),
        "symbols": definitions,
        "internal_imports": sorted(imports),
        "lexical_calls": call_targets,
    }


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args],
        text=True,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
        timeout=10,
    ).strip()


def static_report() -> dict:
    files = {"src/jobhunter/" + rel: scan_source(rel, (SRC / rel).read_bytes()) for rel in SCOPE}
    return {
        "contract": "p16-architecture-inspection-v1",
        "revision": git("rev-parse", "HEAD"),
        "inspected_source_dirty": bool(git("status", "--porcelain", "--", *files)),
        "files": files,
        "limitations": [
            "Curated scope, not transitive closure or a dynamic call graph.",
            "Imports and lexical calls do not establish actual execution or authority.",
            "Runtime introspection is optional, curated, and not a live inference trace.",
            "Schema metadata describes a supplied frozen snapshot, not current live state.",
            "No semantic correctness, completeness or promotion claim.",
        ],
    }


def restrict_worker(event, args):
    """Defense in depth for the reviewed introspection worker, not an OS sandbox."""
    if event == "open":
        _, _, flags = args
        if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
            raise PermissionError("inspection worker: file write denied")
    if event.startswith(("socket.", "subprocess.", "sqlite3.", "ctypes.")) or event in {
        "os.system",
        "os.exec",
        "os.spawn",
        "os.fork",
        "os.posix_spawn",
        "os.remove",
        "os.rename",
        "os.mkdir",
        "os.rmdir",
        "os.chmod",
        "os.chown",
        "os.link",
        "os.symlink",
        "os.truncate",
        "os.utime",
    }:
        raise PermissionError("inspection worker: side effect denied: " + event)


def runtime_report() -> dict:
    """Called only inside the isolated, allowlisted worker (no service instances)."""
    sys.dont_write_bytecode = True
    sys.addaudithook(restrict_worker)
    owners = {}
    mro = {}
    schemas = {}
    for module, name, methods in CLASSES:
        cls = getattr(importlib.import_module("jobhunter." + module), name)
        mro[name] = [c.__name__ for c in cls.__mro__]
        for method in methods:
            func = getattr(cls, method)
            path = Path(inspect.getsourcefile(func)).resolve().relative_to(ROOT)
            owners[name + "." + method] = {
                "owner": func.__qualname__,
                "file": str(path),
                "line": inspect.getsourcelines(func)[1],
                "sha256": digest(path.read_bytes()),
            }
        if not methods:
            schema = cls.model_json_schema()
            decorators = cls.__pydantic_decorators__
            schemas[name] = {
                "fields": sorted(schema.get("properties", {})),
                "required": sorted(schema.get("required", [])),
                "schema_sha256": digest(json.dumps(schema, sort_keys=True).encode()),
                "model_validators": {
                    k: {"owner": v.func.__qualname__, "mode": v.info.mode}
                    for k, v in decorators.model_validators.items()
                },
                "field_validators": sorted(decorators.field_validators),
            }
    return {"method_resolution": owners, "mro": mro, "schemas": schemas}


def inspect_runtime() -> dict:
    # Minimal child environment; no provider credentials/config passed.
    env = {"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8"}
    if os.name == "nt" and "SYSTEMROOT" in os.environ:
        env["SYSTEMROOT"] = os.environ["SYSTEMROOT"]
    result = subprocess.run(
        [sys.executable, "-I", "-B", str(Path(__file__).resolve()), "--runtime-worker"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise RuntimeError("curated runtime inspection failed; use static/manual fallback")
    return json.loads(result.stdout)


def _schema_authorizer(action, arg1, arg2, database, source):
    if action == sqlite3.SQLITE_SELECT:
        return sqlite3.SQLITE_OK
    if action == sqlite3.SQLITE_READ and arg1 in {"sqlite_master", "sqlite_schema"}:
        return sqlite3.SQLITE_OK
    if (
        action == sqlite3.SQLITE_PRAGMA
        and arg1 in {"table_info", "foreign_key_list"}
        and arg2 in TABLES
    ):
        return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY


def schema_report(path: Path) -> dict:
    """Only schema metadata from a closed, explicitly frozen file; no row reads."""
    path = path.resolve(strict=True)
    if not path.is_file() or any(
        Path(str(path) + suffix).exists() for suffix in ("-wal", "-shm", "-journal")
    ):
        raise ValueError("require a closed frozen SQLite file without sidecars")
    before = path.stat()
    with closing(sqlite3.connect(path.as_uri() + "?mode=ro&immutable=1", uri=True)) as db:
        db.execute("PRAGMA query_only=ON")

        db.set_authorizer(_schema_authorizer)
        tables = {}
        for name in TABLES:
            exists = db.execute(
                "SELECT 1 FROM sqlite_schema WHERE type='table' AND name=?", (name,)
            ).fetchone()
            if not exists:
                tables[name] = {"present": False}
                continue
            cols = db.execute(f"PRAGMA table_info({name})").fetchall()
            fks = db.execute(f"PRAGMA foreign_key_list({name})").fetchall()
            tables[name] = {
                "present": True,
                "columns": [
                    {"name": c[1], "type": c[2], "not_null": bool(c[3]), "pk_order": c[5]}
                    for c in cols
                ],
                "foreign_keys": [
                    {"id": f[0], "seq": f[1], "table": f[2], "from": f[3], "to": f[4]} for f in fks
                ],
            }
        triggers = db.execute(
            "SELECT name,tbl_name FROM sqlite_schema WHERE type='trigger' ORDER BY name"
        ).fetchall()
        result = {
            "tables": tables,
            "triggers": [
                {"name": name, "table": table} for name, table in triggers if table in TABLES
            ],
        }

    after = path.stat()
    if (before.st_size, before.st_mtime_ns, before.st_ino) != (
        after.st_size,
        after.st_mtime_ns,
        after.st_ino,
    ) or any(Path(str(path) + suffix).exists() for suffix in ("-wal", "-shm", "-journal")):
        raise ValueError("frozen schema snapshot changed during inspection")
    return result


def markdown(report: dict) -> str:
    lines = [
        "# P1.6 curated architecture inspection",
        "",
        "Revision: `" + report["revision"] + "`",
        f"Inspected sources dirty: {report['inspected_source_dirty']}",
        "",
        "## Limits",
        *("- " + x for x in report["limitations"]),
        "",
        "## Static source inventory",
        "",
        "| File | Symbols | SHA-256 |",
        "| --- | ---: | --- |",
    ]
    for path, info in report["files"].items():
        lines.append(f"| `{path}` | {len(info['symbols'])} | `{info['sha256'][:12]}` |")
    # A deliberately small import-only diagram; not the DOC.2 runtime flow.
    subset = (
        "analysis_current.py",
        "analysis_runtime_v30.py",
        "analysis_runtime_v29.py",
        "analysis_service_v30.py",
        "analysis_runtime.py",
        "analysis_service.py",
    )
    nodes = {module_name(rel): f"n{i}" for i, rel in enumerate(subset)}
    lines += ["", "## Selected direct imports (not calls)", "", "```mermaid", "flowchart LR"]
    for mod, node in nodes.items():
        lines.append(f'  {node}["{mod.removeprefix("jobhunter.")}"]')
    for rel in subset:
        for target in report["files"]["src/jobhunter/" + rel]["internal_imports"]:
            if target in nodes:
                lines.append(f"  {nodes[module_name(rel)]} -.->|imports| {nodes[target]}")
    lines += ["```", ""]
    if "runtime" in report:
        lines += [
            "## Resolved method owners",
            "",
            "| Requested | Actual owner | File |",
            "| --- | --- | --- |",
        ]
        for name, v in report["runtime"]["method_resolution"].items():
            lines.append(f"| `{name}` | `{v['owner']}` | `{v['file']}:{v['line']}` |")
        lines += ["", "## Schema summaries", ""]
        for name, v in report["runtime"]["schemas"].items():
            lines.append(
                f"- {name}: {len(v['fields'])} fields; "
                f"{len(v['model_validators'])} model validators."
            )
    if "schema" in report:
        lines += ["", "## Frozen schema dependencies", ""]
        for name, v in report["schema"]["tables"].items():
            if not v["present"]:
                lines.append(f"- {name}: absent from snapshot.")
            else:
                for f in v["foreign_keys"]:
                    lines.append(f"- {name}.{f['from']} -> {f['table']}.{f['to']}")
        lines += ["", "Trigger names only; SQL semantics and selector logic require review."]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--runtime", action="store_true", help="curated class introspection")
    parser.add_argument("--frozen-schema-db", type=Path, help="closed local-acceptance snapshot")
    parser.add_argument("--runtime-worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.runtime_worker:
        print(json.dumps(runtime_report(), sort_keys=True))
        return 0
    report = static_report()
    if args.runtime:
        report["runtime"] = inspect_runtime()
    if args.frozen_schema_db:
        path = args.frozen_schema_db.resolve(strict=True)
        if not path.is_relative_to((ROOT / "data/local-acceptance").resolve()):
            parser.error("schema inspection requires a frozen snapshot in data/local-acceptance")
        report["schema"] = schema_report(path)
    print(
        markdown(report)
        if args.format == "markdown"
        else json.dumps(report, indent=2, sort_keys=True),
        end="" if args.format == "markdown" else "\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
