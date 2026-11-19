"""Run the bounded, candidate-only P1.6 B4 job-understanding experiment.

All source/model evidence and the comparison database remain under ignored
data/local-acceptance/. No production P1.6, accepted facts, or downstream
stores are written.
"""

from __future__ import annotations

import argparse
import contextlib
import html
import json
import runpy
import socket
import sqlite3
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, ValidationError

from jobhunter.config import Settings
from jobhunter.source_job_understanding_b4 import (
    B4_CONTRACT_VERSION,
    B4_PROMPT_VERSION,
    B4_SCHEMA_VERSION,
    B4_SYSTEM_PROMPT,
    build_b4_evidence_bundle,
    build_b4_model_payload,
    filter_b4_model_fragments,
    finalize_b4_case,
    sha256_bytes,
    sha256_json,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE = (
    ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
)
DEFAULT_B2_DIR = ROOT / "data/local-acceptance/p16-stage-b2-2026-11-17/b2-candidate-acceptance-v5"
DEFAULT_B3_DIR = ROOT / "data/local-acceptance/p16-stage-b3-2026-11-18/primary-v1"
DEFAULT_OUT = ROOT / "data/local-acceptance/p16-stage-b4-2026-11-19/primary-v4c"
SCHEMA_PATH = ROOT / "docs/contracts/p16-stage-b4/job_understanding_response.schema.json"
B4_MAX_OUTPUT_TOKENS = 2100
B4_TIMEOUT_SECONDS = 40
COHORT = ("tNhZ", "tMps", "tNDx", "tMjm")


class NativeModelError(RuntimeError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def native_preflight(
    opener: urllib.request.OpenerDirector, api_base: str, model: str
) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{api_base}/api/v1/models",
        headers={"Accept": "application/json"},
        method="GET",
    )
    try:
        with opener.open(request, timeout=8) as response:
            data = json.loads(response.read())
    except Exception as exc:  # noqa: BLE001 - converted to a bounded preflight state
        raise NativeModelError("native_model_preflight_unavailable") from exc
    matches = [item for item in data.get("models", []) if item.get("key") == model]
    if len(matches) != 1:
        raise NativeModelError("configured_model_not_found")
    selected = matches[0]
    instances = selected.get("loaded_instances") or []
    if not instances:
        raise NativeModelError("configured_model_not_loaded")
    reasoning = selected.get("capabilities", {}).get("reasoning", {})
    allowed = reasoning.get("allowed_options", [])
    if "off" not in allowed:
        raise NativeModelError("reasoning_off_not_supported")
    config = instances[0].get("config", {}) if isinstance(instances[0], dict) else {}
    return {
        "model_key": model,
        "loaded_instances_count": len(instances),
        "context_length": config.get("context_length"),
        "reasoning_allowed_options": allowed,
        "reasoning_default": reasoning.get("default"),
    }


def native_chat(
    opener: urllib.request.OpenerDirector,
    api_base: str,
    request_bytes: bytes,
    timeout_seconds: int,
) -> tuple[dict[str, Any], bytes, int]:
    request = urllib.request.Request(
        f"{api_base}/api/v1/chat",
        data=request_bytes,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with opener.open(request, timeout=timeout_seconds) as response:
            raw = response.read()
            data = json.loads(raw)
            if not isinstance(data, dict):
                raise NativeModelError("native_response_not_object")
            return data, raw, response.status
    except urllib.error.HTTPError as exc:
        error_body = exc.read()
        error_message = ""
        with contextlib.suppress(ValueError, AttributeError, TypeError):
            error_message = str(json.loads(error_body).get("error", ""))
        if "unloaded" in error_message.lower():
            raise NativeModelError("model_unloaded") from exc
        raise NativeModelError(f"native_http_{exc.code}") from exc
    except urllib.error.URLError as exc:
        if isinstance(exc.reason, (TimeoutError, socket.timeout)):
            raise TimeoutError("native_lm_studio_timeout") from exc
        raise NativeModelError("native_endpoint_unavailable") from exc
    except TimeoutError as exc:
        raise TimeoutError("native_lm_studio_timeout") from exc


def extract_final_message(response: dict[str, Any]) -> tuple[str, int]:
    """Read only final message content; never inspect or persist reasoning fields."""
    output = response.get("output", [])
    messages = [
        item.get("content")
        for item in output
        if isinstance(item, dict)
        and item.get("type") == "message"
        and isinstance(item.get("content"), str)
    ]
    return "\n".join(messages).strip(), len(messages)


def parse_model_json(answer: str) -> dict[str, Any]:
    text = answer.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    value = json.loads(text)
    if not isinstance(value, dict):
        raise NativeModelError("model_json_not_object")
    return value


def response_metadata(
    *, model: str, status_code: int, answer: str, message_count: int, response_sha: str
) -> dict[str, Any]:
    return {
        "provider": "lm-studio-native-local-api",
        "model": model,
        "status_code": status_code,
        "output_message_count": message_count,
        "final_message_sha256": sha256_bytes(answer.encode("utf-8")),
        "final_message_chars": len(answer),
        "reasoning_mode": "off",
        "reasoning_content_persisted": False,
        "raw_response_body_retained": False,
        "raw_response_sha256": response_sha,
    }


def file_sha(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path.name}")
    return value


def verify_b3_evidence(database: Path, b2_dir: Path, b3_dir: Path) -> dict[str, Any]:
    """Verify the exact B3 files selected by its final audit before B4 consumes them."""
    audit = read_json(b3_dir / "B3_FINAL_AUDIT.json")
    expected = {
        "source_database_sha256": file_sha(database),
        "b2_private_candidate_sha256": file_sha(b2_dir / "PRIVATE_B2_CANDIDATES.json"),
        "run_manifest_sha256": file_sha(b3_dir / "run_manifest.json"),
        "private_candidate_output_sha256": file_sha(b3_dir / "PRIVATE_B3_CANDIDATES.json"),
        "corrective_candidate_sha256": file_sha(b3_dir / "B3_CORRECTIVE_CANDIDATE.json"),
        "selected_b1_drafts_sha256": file_sha(b3_dir / "B1_COMPATIBLE_DRAFTS.json"),
        "safe_metrics_sha256": file_sha(b3_dir / "SAFE_B3_METRICS.json"),
        "semantic_review_sha256": file_sha(b3_dir / "B3_SEMANTIC_REVIEW.json"),
        "review_flag_reassessment_sha256": file_sha(b3_dir / "B3_REVIEW_FLAG_REASSESSMENT.json"),
        "mechanical_audit_sha256": file_sha(b3_dir / "B3_MECHANICAL_AUDIT.json"),
    }
    if audit.get("status") != "PASS":
        raise ValueError("B3 final audit is not PASS")
    for key, actual in expected.items():
        if audit.get(key) != actual:
            raise ValueError(f"B3 final-audit dependency hash mismatch: {key}")
    if audit.get("production_database_written") is not False:
        raise ValueError("B3 production database write boundary changed")
    if (
        audit.get("accepted_facts_promoted") != 0
        or audit.get("unseen_generalization_established") is not False
    ):
        raise ValueError("B3 authority or generalization boundary changed")

    semantic = read_json(b3_dir / "B3_SEMANTIC_REVIEW.json")
    if (
        semantic.get("reviewed_persian_translation_count") != 63
        or semantic.get("native_identity_count") != 1
        or semantic.get("unresolved_translation_count") != 0
        or semantic.get("independent_holdout_count") != 0
        or semantic.get("unseen_generalization_established") is not False
    ):
        raise ValueError("B3 semantic-review denominator or limits changed")
    if any(value != "PASS" for value in semantic.get("critical_semantic_checks", {}).values()):
        raise ValueError("A B3 critical semantic check is not PASS")
    records = read_json(b3_dir / "PRIVATE_B3_CANDIDATES.json")
    if len(records.get("items", [])) != 64:
        raise ValueError("B3 selected candidate record count changed")
    drafts = read_json(b3_dir / "B1_COMPATIBLE_DRAFTS.json")
    if set(drafts) != set(COHORT):
        raise ValueError("B3 B1 draft cohort changed")
    return {
        "audit": audit,
        "semantic_review": semantic,
        "records": records["items"],
        "corrective": read_json(b3_dir / "B3_CORRECTIVE_CANDIDATE.json"),
        "drafts": drafts,
        "manifest": read_json(b3_dir / "run_manifest.json"),
    }


def baseline_for_job(
    connection: sqlite3.Connection, job_id: str, version_id: int
) -> dict[str, Any]:
    attempts = connection.execute(
        """
        SELECT outcome, artifact_id, error_type
        FROM job_analysis_attempts
        WHERE job_detail_version_id = ? AND prompt_version = 'job-analysis-english-v30'
        ORDER BY id
        """,
        (version_id,),
    ).fetchall()
    v30_artifacts = connection.execute(
        """
        SELECT id, semantic_review_status
        FROM job_analysis_artifacts
        WHERE job_detail_version_id = ? AND prompt_version = 'job-analysis-english-v30'
        ORDER BY id
        """,
        (version_id,),
    ).fetchall()
    rejected = connection.execute(
        """
        SELECT id, original_artifact_id
        FROM job_analysis_rejected_artifacts
        WHERE source_job_id = ? AND job_detail_version_id = ?
          AND prompt_version = 'job-analysis-english-v30'
        ORDER BY id
        """,
        (job_id, version_id),
    ).fetchall()
    v9_artifacts = connection.execute(
        """
        SELECT id, semantic_review_status
        FROM job_analysis_artifacts
        WHERE job_detail_version_id = ? AND prompt_version = 'job-analysis-original-v9'
        ORDER BY id
        """,
        (version_id,),
    ).fetchall()

    if v30_artifacts:
        v30_status = "artifact_present_" + str(v30_artifacts[-1]["semantic_review_status"])
    elif rejected:
        v30_status = "rejected_candidate_no_valid_artifact"
    elif attempts and attempts[-1]["outcome"] == "failed":
        v30_status = "failed_no_artifact"
    elif attempts and attempts[-1]["outcome"] == "completed":
        v30_status = "completed_without_valid_artifact"
    else:
        v30_status = "no_v30_attempt"

    if v9_artifacts:
        v9_status = "artifact_present_" + str(v9_artifacts[-1]["semantic_review_status"])
    else:
        v9_status = "no_v9_artifact"

    return {
        "source_job_id": job_id,
        "job_detail_version_id": version_id,
        "source_snapshot_same_as_b4": True,
        "v30": {
            "status": v30_status,
            "attempts": [
                {
                    "outcome": row["outcome"],
                    "artifact_id": row["artifact_id"],
                    "error_type": row["error_type"],
                }
                for row in attempts
            ],
            "valid_artifact_ids": [row["id"] for row in v30_artifacts],
            "rejected_candidate_ids": [row["id"] for row in rejected],
        },
        "v9": {
            "status": v9_status,
            "artifacts": [
                {"id": row["id"], "semantic_review_status": row["semantic_review_status"]}
                for row in v9_artifacts
            ],
            "interpretation_limit": (
                "Historical accepted original-language artifact; acceptance is not independent "
                "certification of every source-semantic claim."
            ),
        },
    }


def create_b4_tables(database: Path) -> None:
    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA foreign_keys=ON")
        connection.executescript(
            """
            CREATE TABLE p16_b4_candidate_briefs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_job_id TEXT NOT NULL,
                job_detail_version_id INTEGER NOT NULL,
                source_semantic_sha256 TEXT NOT NULL,
                b2_candidate_sha256 TEXT NOT NULL,
                b3_candidate_sha256 TEXT NOT NULL,
                model TEXT NOT NULL,
                prompt_version TEXT NOT NULL,
                schema_version TEXT NOT NULL,
                input_sha256 TEXT NOT NULL,
                analysis_outcome TEXT NOT NULL CHECK (
                    analysis_outcome IN (
                        'full_candidate', 'partial_candidate', 'source_only_candidate',
                        'failed', 'timed_out'
                    )
                ),
                candidate_json TEXT NOT NULL,
                request_sha256 TEXT,
                response_sha256 TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id),
                UNIQUE(source_job_id, job_detail_version_id, prompt_version, schema_version)
            );

            CREATE TABLE p16_b4_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_job_id TEXT NOT NULL,
                job_detail_version_id INTEGER NOT NULL,
                attempted_at TEXT NOT NULL,
                model TEXT NOT NULL,
                prompt_version TEXT NOT NULL,
                schema_version TEXT NOT NULL,
                outcome TEXT NOT NULL CHECK (
                    outcome IN ('completed','failed','timed_out','skipped')
                ),
                error_type TEXT,
                input_sha256 TEXT NOT NULL,
                request_sha256 TEXT,
                response_sha256 TEXT,
                request_path TEXT,
                response_path TEXT,
                FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id)
            );

            CREATE INDEX idx_p16_b4_brief_job
                ON p16_b4_candidate_briefs(source_job_id, job_detail_version_id);
            CREATE INDEX idx_p16_b4_attempt_job
                ON p16_b4_attempts(source_job_id, attempted_at, id);
            """
        )
        if connection.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("B4 comparison database foreign-key check failed")


def persist_case(
    database: Path,
    *,
    job_id: str,
    version_id: int,
    source_semantic_sha256: str,
    b2_sha: str,
    b3_sha: str,
    model: str,
    input_sha: str,
    outcome: str,
    candidate: dict[str, Any],
    request_sha: str | None,
    response_sha: str | None,
    request_path: str | None,
    response_path: str | None,
    error_type: str | None,
) -> None:
    now = datetime.now(UTC).isoformat()
    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute(
            """
            INSERT INTO p16_b4_attempts (
                source_job_id, job_detail_version_id, attempted_at, model,
                prompt_version, schema_version, outcome, error_type,
                input_sha256, request_sha256, response_sha256, request_path, response_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job_id,
                version_id,
                now,
                model,
                B4_PROMPT_VERSION,
                B4_SCHEMA_VERSION,
                outcome,
                error_type,
                input_sha,
                request_sha,
                response_sha,
                request_path,
                response_path,
            ),
        )
        connection.execute(
            """
            INSERT INTO p16_b4_candidate_briefs (
                source_job_id, job_detail_version_id, source_semantic_sha256,
                b2_candidate_sha256, b3_candidate_sha256, model, prompt_version,
                schema_version, input_sha256, analysis_outcome, candidate_json,
                request_sha256, response_sha256, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job_id,
                version_id,
                source_semantic_sha256,
                b2_sha,
                b3_sha,
                model,
                B4_PROMPT_VERSION,
                B4_SCHEMA_VERSION,
                input_sha,
                candidate["analysis_outcome"],
                json.dumps(candidate, ensure_ascii=False, sort_keys=True),
                request_sha,
                response_sha,
                now,
            ),
        )
        if connection.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("B4 candidate insert violated foreign keys")


def safe_markdown_text(value: Any) -> str:
    text = html.escape(str(value), quote=False)
    for marker in ("\\", "`", "*", "_", "{", "}", "[", "]", "(", ")", "#", "+", "-", ".", "!", "|"):
        text = text.replace(marker, "\\" + marker)
    return text


def render_briefs(cases: list[dict[str, Any]], baselines: dict[str, Any], model: str) -> str:
    lines = [
        "# P1.6 B4 — exposed-cohort job-understanding candidates",
        "",
        "Candidate-only diagnostic output. Not accepted P1.6, no production route "
        "and no unseen validation.",
        f"Model: {model}",
        f"Prompt: {B4_PROMPT_VERSION}",
        "",
    ]
    for case in cases:
        candidate = case["candidate"]
        job_id = candidate["source_version"]["source_job_id"]
        baseline = baselines[job_id]
        lines.extend(
            [
                f"## {job_id} — "
                f"{safe_markdown_text(candidate.get('posting_title') or 'Untitled posting')}",
                "",
                f"**Candidate state:** {candidate['analysis_outcome']}",
                f"**Source version:** {candidate['source_version']['job_detail_version_id']} / "
                f"{candidate['source_version']['semantic_sha256']}",
                "",
            ]
        )
        brief = candidate.get("brief")
        if brief is None:
            lines.extend(
                [
                    "### Source-only understanding (no accepted semantic inference)",
                    "No validated job-level model interpretation. The B2/B3 source candidates "
                    "source items with their original identities retained separately.",
                    "",
                ]
            )
            source_only = candidate["source_only_brief"]
            for category, items in source_only["category_groups"].items():
                lines.append(f"**{category}** — provisional B2 classification")
                for source_item in items:
                    lines.append(
                        f"- {safe_markdown_text(source_item['translation_candidate'])} "
                        f"(source: {source_item['source_item_id']}, "
                        f"strength candidate: {source_item['strength_candidate']})"
                    )
                lines.append("")
            if source_only["qualifications_only_possible"]:
                lines.append(
                    "The source-first candidate contains no explicit work-duty item. "
                    "No day-to-day tasks or work-implied capabilities have been inferred."
                )
                lines.append("")
        else:
            lines.extend(
                ["### Role summary", safe_markdown_text(brief["role_summary"]["summary"]), ""]
            )
            lines.append("### Work activities")
            if brief["work_activities"]:
                for item in brief["work_activities"]:
                    lines.append(
                        f"- {safe_markdown_text(item['summary'])} "
                        f"(source: {', '.join(item['source_item_ids'])})"
                    )
            else:
                lines.append("- No distinct explicit work-duty item was identified.")
            lines.append("")
            lines.append("### Applicant expectations")
            if brief["expectation_summaries"]:
                for item in brief["expectation_summaries"]:
                    lines.append(
                        f"- {safe_markdown_text(item['summary'])} "
                        f"(source: {', '.join(item['source_item_ids'])})"
                    )
            else:
                lines.append("- No concise expectation summary was produced.")
            lines.append("")
            lines.append("### Work-implied capability candidates")
            if brief["work_implied_capabilities"]:
                for item in brief["work_implied_capabilities"]:
                    lines.append(
                        f"- **{safe_markdown_text(item['capability'])}** — "
                        f"{safe_markdown_text(item['rationale'])} "
                        f"(source: {', '.join(item['source_item_ids'])}; "
                        "prior employer-required experience: not established)"
                    )
            else:
                lines.append("- None proposed.")
            lines.append("")
            lines.append("### Open questions")
            if brief["open_questions"]:
                for item in brief["open_questions"]:
                    lines.append(
                        f"- {safe_markdown_text(item['question'])} "
                        f"(source: {', '.join(item['source_item_ids'])})"
                    )
            else:
                lines.append("- No explicit open question returned.")
            lines.append("")
        lines.append("### Source conditions retained deterministically")
        conditions = [
            item
            for item in candidate["items"]
            if item["category_candidate"] in {"work_arrangement", "compensation", "benefit"}
        ]
        if conditions:
            for item in conditions:
                target = (
                    item["translation"]["target_text"]
                    if item["translation"]
                    else "No selected translation"
                )
                lines.append(
                    f"- {item['category_candidate']} [{item['item_id']}] — "
                    f"{safe_markdown_text(target)} "
                    f"(candidate strength: {item['strength_candidate']})"
                )
        else:
            lines.append("- None identified.")
        lines.append("")
        lines.append("### Candidate coverage")
        lines.append(
            ", ".join(
                f"{key}: {value}" for key, value in sorted(candidate["coverage_counts"].items())
            )
            or "No coverage rows."
        )
        lines.append("")
        lines.append("### Frozen baseline")
        lines.append(f"- v30: {baseline['v30']['status']}")
        lines.append(f"- original v9: {baseline['v9']['status']}")
        lines.append("")
        lines.append("### Source-bound structures")
        if candidate["eligibility_graphs"]:
            for graph in candidate["eligibility_graphs"]:
                lines.append(
                    f"- {graph['graph_id']} (candidate graph; basis items: "
                    f"{', '.join(graph.get('basis_item_ids', []))})"
                )
        else:
            lines.append("- No explicit alternative eligibility graph.")
        if candidate["conflicts"]:
            for conflict in candidate["conflicts"]:
                lines.append(
                    f"- Metadata conflict {conflict['type']}: "
                    f"{conflict['item_id_a']} vs {conflict['item_id_b']} "
                    "(both source origins retained)"
                )
        else:
            lines.append("- No B2 board/prose conflict signal.")
        lines.append("")
        lines.append(
            "Original quotes, English item text, hashes and B3 review provenance "
            "remain in the private candidate/evidence JSON; this summary does not replace them."
        )
        lines.extend(["", "---", ""])
    return "\n".join(lines)


def make_standalone_comparison_database(database: Path) -> None:
    """Publish a self-contained SQLite backup including committed WAL records."""
    standalone = database.with_name("comparison_standalone.sqlite3")
    if standalone.exists():
        raise ValueError("B4 standalone comparison already exists")
    with (
        contextlib.closing(sqlite3.connect(database)) as source,
        contextlib.closing(sqlite3.connect(standalone)) as target,
    ):
        source.backup(target)
        target.commit()
    with contextlib.closing(sqlite3.connect(standalone)) as standalone_connection:
        mode = standalone_connection.execute("PRAGMA journal_mode=DELETE").fetchone()[0]
        if mode != "delete":
            raise ValueError("B4 comparison backup could not enter standalone journal mode")
    # Now the old main DB has no open connections in this B4 process.
    database.unlink()
    for suffix in ("-wal", "-shm"):
        Path(f"{database}{suffix}").unlink(missing_ok=True)
    standalone.replace(database)
    with contextlib.closing(sqlite3.connect(f"file:{database}?mode=ro", uri=True)) as check:
        if check.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("B4 standalone SQLite backup failed integrity check")
        if check.execute("PRAGMA journal_mode").fetchone()[0] != "delete":
            raise ValueError("B4 comparison snapshot retained WAL mode")


def run(args: argparse.Namespace) -> dict[str, Any]:
    database = args.database.resolve()
    b2_dir = args.b2_dir.resolve()
    b3_dir = args.b3_dir.resolve()
    out = args.out.resolve()
    private_root = (ROOT / "data/local-acceptance").resolve()
    if not out.is_relative_to(private_root):
        raise ValueError("B4 raw candidate data must stay under ignored data/local-acceptance/")
    if out.exists():
        raise ValueError(f"B4 output already exists; use a new versioned directory: {out}")
    if file_sha(database) != "bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe":
        raise ValueError("B4 requires the frozen B0 exposed-original source snapshot")

    b3 = verify_b3_evidence(database, b2_dir, b3_dir)
    b3_runner = runpy.run_path(str(ROOT / "scripts/run_p16_b3_source_bound_translation.py"))
    b2_scorecard, contexts = b3_runner["build_contexts"](database, b2_dir)
    if tuple(contexts) != COHORT:
        raise ValueError("B4 cohort/order differs from the frozen four-ad B0 selection")

    settings = Settings.load(args.config)
    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured local analysis model")
    endpoint = urlparse(settings.lm_studio_base_url)
    if endpoint.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("B4 requires the configured local-only LM Studio endpoint")
    api_base = f"{endpoint.scheme}://{endpoint.netloc}"
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    model_metadata: dict[str, Any] | None = None
    preflight_error: str | None = None
    try:
        model_metadata = native_preflight(opener, api_base, model)
    except Exception as exc:  # noqa: BLE001 - preserve per-case source-only fallback
        preflight_error = getattr(exc, "code", type(exc).__name__)

    out.mkdir(parents=True, exist_ok=True)
    raw_dir = out / "raw"
    raw_dir.mkdir()
    comparison_db = out / "comparison.sqlite3"
    b3_runner["copy_frozen_database"](database, comparison_db)
    create_b4_tables(comparison_db)
    schema = read_json(SCHEMA_PATH)

    b2_candidate_path = b2_dir / "PRIVATE_B2_CANDIDATES.json"
    b3_candidate_path = b3_dir / "PRIVATE_B3_CANDIDATES.json"
    b2_sha = file_sha(b2_candidate_path)
    b3_sha = file_sha(b3_candidate_path)
    b3_hashes = {
        "b3_final_audit_sha256": file_sha(b3_dir / "B3_FINAL_AUDIT.json"),
        "b3_semantic_review_sha256": file_sha(b3_dir / "B3_SEMANTIC_REVIEW.json"),
        "b3_b1_drafts_sha256": file_sha(b3_dir / "B1_COMPATIBLE_DRAFTS.json"),
    }
    manifest = {
        "contract": B4_CONTRACT_VERSION,
        "prompt_version": B4_PROMPT_VERSION,
        "schema_version": B4_SCHEMA_VERSION,
        "source_database_sha256": file_sha(database),
        "b2_candidate_sha256": b2_sha,
        "b2_safe_scorecard": b2_scorecard,
        "b3_candidate_sha256": b3_sha,
        **b3_hashes,
        "model": model,
        "provider": "lm-studio-native-local-api",
        "base_url": api_base,
        "preflight_status": "passed" if preflight_error is None else "failed",
        "preflight_error_type": preflight_error,
        "model_metadata": model_metadata,
        "response_handling": {
            "reasoning_mode": "off",
            "reasoning_content_persisted": False,
            "raw_response_body_retained": False,
            "final_message_only": True,
        },
        "limits": {
            "cohort_jobs": len(COHORT),
            "max_generation_requests": len(COHORT),
            "max_retries": 0,
            "max_corrective_requests": 0,
            "max_output_tokens": B4_MAX_OUTPUT_TOKENS,
            "timeout_seconds": B4_TIMEOUT_SECONDS,
            "temperature": 0,
            "seed": 0,
            "reasoning": "off",
            "store": False,
        },
        "code_sha256": {
            "runner": file_sha(Path(__file__)),
            "module": file_sha(ROOT / "src/jobhunter/source_job_understanding_b4.py"),
            "schema": file_sha(SCHEMA_PATH),
        },
        "created_at": datetime.now(UTC).isoformat(),
    }
    write_json(out / "run_manifest.json", manifest)

    baselines: dict[str, Any] = {}
    cases: list[dict[str, Any]] = []
    request_count = 0
    success_count = 0
    filtered_candidate_count = 0
    quarantined_fragment_count = 0
    intentional_source_only_count = 0
    baseline_connection = sqlite3.connect(f"file:{comparison_db}?mode=ro", uri=True)
    baseline_connection.row_factory = sqlite3.Row
    for job_id, context in contexts.items():
        evidence = build_b4_evidence_bundle(
            source=context["source"],
            candidate=context["candidate"],
            context=context,
            b1_draft=b3["drafts"][job_id],
            b3_records=b3["records"],
            corrective=(
                b3["corrective"] if b3["corrective"].get("source_job_id") == job_id else None
            ),
            semantic_review=b3["semantic_review"],
            final_audit=b3["audit"],
        )
        payload = build_b4_model_payload(evidence)
        input_sha = sha256_json(payload)
        baseline = baseline_for_job(
            baseline_connection,
            job_id,
            context["source"].job_detail_version_id,
        )
        baselines[job_id] = baseline
        response: dict[str, Any] | None = None
        failure_state = "failed"
        attempt_outcome = "skipped" if preflight_error else "failed"
        error_type = "provider_preflight_failed" if preflight_error else None
        request_sha = response_sha = request_name = response_name = None

        no_explicit_duties = not any(
            item["category_candidate"] == "work_duty" and item["translation"] is not None
            for item in evidence["items"]
        )
        if no_explicit_duties:
            # No model is asked to invent duties for a qualifications-only ad.
            intentional_source_only_count += 1
            attempt_outcome = "skipped"
            error_type = "no_explicit_duties_source_only"
            candidate_case = finalize_b4_case(
                evidence, response=None, failure_state="source_only_candidate"
            )
        elif preflight_error is None:
            request_body = {
                "model": model,
                "system_prompt": B4_SYSTEM_PROMPT,
                "input": json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
                "temperature": 0,
                "reasoning": "off",
                "max_output_tokens": B4_MAX_OUTPUT_TOKENS,
                "stream": False,
                "store": False,
            }
            request_bytes = json.dumps(
                request_body, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
            request_sha = sha256_bytes(request_bytes)
            request_file = raw_dir / f"{job_id}.request.json"
            request_file.write_bytes(request_bytes)
            request_name = request_file.name
            request_count += 1
            response_data: dict[str, Any] | None = None
            response_metadata_written = False
            try:
                response_data, raw_response, status_code = native_chat(
                    opener, api_base, request_bytes, B4_TIMEOUT_SECONDS
                )
                response_sha = sha256_bytes(raw_response)
                answer, message_count = extract_final_message(response_data)
                final_message_file = raw_dir / f"{job_id}.final-message.txt"
                final_message_file.write_text(answer, encoding="utf-8")
                metadata = response_metadata(
                    model=model,
                    status_code=status_code,
                    answer=answer,
                    message_count=message_count,
                    response_sha=response_sha,
                )
                response_file = raw_dir / f"{job_id}.response-metadata.json"
                write_json(response_file, metadata)
                response_name = response_file.name
                response_metadata_written = True
                if not answer:
                    raise NativeModelError("native_response_has_no_final_message")
                response = parse_model_json(answer)
                try:
                    Draft202012Validator(schema).validate(response)
                except ValidationError as exc:
                    raise NativeModelError("json_schema_validation_failed") from exc
                cleaned, filter_audit = filter_b4_model_fragments(response, evidence)
                candidate_case = finalize_b4_case(evidence, response=cleaned)
                candidate_case["model_fragment_filter"] = filter_audit
                if filter_audit["dropped_fragment_count"]:
                    candidate_case["analysis_outcome"] = "partial_candidate"
                    filtered_candidate_count += 1
                    quarantined_fragment_count += filter_audit["dropped_fragment_count"]
                attempt_outcome = "completed"
                error_type = None
                success_count += 1
            except Exception as exc:  # noqa: BLE001 - preserve source-only fallback per case
                if response_data is not None and not response_metadata_written:
                    answer, message_count = extract_final_message(response_data)
                    metadata = response_metadata(
                        model=model,
                        status_code=200,
                        answer=answer,
                        message_count=message_count,
                        response_sha=response_sha or "",
                    )
                    response_file = raw_dir / f"{job_id}.response-metadata.json"
                    write_json(response_file, metadata)
                    response_name = response_file.name
                error_type = getattr(exc, "code", type(exc).__name__)
                if isinstance(exc, (TimeoutError, socket.timeout)):
                    failure_state = "timed_out"
                    attempt_outcome = "timed_out"
                else:
                    failure_state = "failed"
                    attempt_outcome = "failed"
                candidate_case = finalize_b4_case(
                    evidence,
                    response=None,
                    failure_state=failure_state,
                )
        else:
            candidate_case = finalize_b4_case(
                evidence,
                response=None,
                failure_state=failure_state,
            )

        case_record = {
            "source_job_id": job_id,
            "input_sha256": input_sha,
            "model": model,
            "prompt_version": B4_PROMPT_VERSION,
            "schema_version": B4_SCHEMA_VERSION,
            "attempt_outcome": attempt_outcome,
            "error_type": error_type,
            "request_sha256": request_sha,
            "response_sha256": response_sha,
            "candidate": candidate_case,
        }
        cases.append(case_record)
        persist_case(
            comparison_db,
            job_id=job_id,
            version_id=context["source"].job_detail_version_id,
            source_semantic_sha256=context["source"].semantic_sha256,
            b2_sha=b2_sha,
            b3_sha=b3_sha,
            model=model,
            input_sha=input_sha,
            outcome=attempt_outcome,
            candidate=candidate_case,
            request_sha=request_sha,
            response_sha=response_sha,
            request_path=request_name,
            response_path=response_name,
            error_type=error_type,
        )
        print(
            f"B4 {job_id}: {candidate_case['analysis_outcome']} "
            f"(attempt={attempt_outcome}, source_items={len(candidate_case['items'])})"
        )

    baseline_connection.close()
    private = {
        "contract": B4_CONTRACT_VERSION,
        "authority": "candidate_only_no_downstream_reuse",
        "source_database_sha256": file_sha(database),
        "b2_candidate_sha256": b2_sha,
        "b3_candidate_sha256": b3_sha,
        "b3_semantic_review_sha256": b3_hashes["b3_semantic_review_sha256"],
        "cases": cases,
    }
    write_json(out / "PRIVATE_B4_CANDIDATES.json", private)
    write_json(out / "B4_BASELINE_COMPARISON.json", baselines)
    # A plain Markdown rendering is convenient locally; source quotes stay in the private JSON.
    (out / "B4_BRIEFS.md").write_text(
        render_briefs(cases, baselines, model),
        encoding="utf-8",
    )
    comparison_counts = {
        "v30_failed_no_artifact": sum(
            v["v30"]["status"] == "failed_no_artifact" for v in baselines.values()
        ),
        "v30_rejected_no_valid_artifact": sum(
            v["v30"]["status"] == "rejected_candidate_no_valid_artifact" for v in baselines.values()
        ),
        "v9_artifact_present": sum(
            v["v9"]["status"].startswith("artifact_present_") for v in baselines.values()
        ),
    }
    coverage_total = {}
    for case in cases:
        for key, value in case["candidate"]["coverage_counts"].items():
            coverage_total[key] = coverage_total.get(key, 0) + value
    safe_metrics = {
        "contract": "jobhunter-p16-b4-safe-metrics-v1",
        "status": "completed"
        if success_count == len(COHORT)
        else "completed_with_partial_or_failed_cases",
        "authority": "candidate_only_no_downstream_reuse",
        "source_database_sha256": file_sha(database),
        "b2_candidate_sha256": b2_sha,
        "b3_candidate_sha256": b3_sha,
        "case_count": len(cases),
        "source_item_count": sum(len(case["candidate"]["items"]) for case in cases),
        "selected_source_bound_translation_count": sum(
            1
            for case in cases
            for item in case["candidate"]["items"]
            if item["translation"]
            and item["translation"]["state"] == "source_bound_translation_candidate"
        ),
        "native_identity_count": sum(
            1
            for case in cases
            for item in case["candidate"]["items"]
            if item["translation"] and item["translation"]["state"] == "native_english_identity"
        ),
        "excluded_item_count": sum(
            1 for case in cases for item in case["candidate"]["items"] if item["excluded_reason"]
        ),
        "board_metadata_value_count": sum(len(case["candidate"]["board_values"]) for case in cases),
        "nested_eligibility_leaf_count": sum(
            len(case["candidate"]["nested_eligibility_items"]) for case in cases
        ),
        "model_requests_started": request_count,
        "model_requests_validated": success_count,
        "model_candidates_with_filtered_fragments": filtered_candidate_count,
        "quarantined_model_fragments": quarantined_fragment_count,
        "source_only_cases_without_model_call": intentional_source_only_count,
        "model_request_budget": len(COHORT),
        "model_retries": 0,
        "reasoning_mode": "off",
        "reasoning_content_retained": False,
        "max_output_tokens": B4_MAX_OUTPUT_TOKENS,
        "timeout_seconds": B4_TIMEOUT_SECONDS,
        "corrective_requests": 0,
        "analysis_outcomes": {
            outcome: sum(case["candidate"]["analysis_outcome"] == outcome for case in cases)
            for outcome in (
                "full_candidate",
                "partial_candidate",
                "source_only_candidate",
                "failed",
                "timed_out",
            )
        },
        "attempt_outcomes": {
            outcome: sum(case["attempt_outcome"] == outcome for case in cases)
            for outcome in ("completed", "failed", "timed_out", "skipped")
        },
        "coverage_status_counts": dict(sorted(coverage_total.items())),
        "baseline_counts": comparison_counts,
        "semantic_review_status": "pending_assistant_review",
        "independent_blind_review": False,
        "unseen_generalization_established": False,
        "production_database_written": False,
        "accepted_facts_promoted": 0,
        "downstream_authority": "none",
        "public_route_changed": False,
        "owner_time_savings_measured": False,
        "private_raw_data_path": str(out),
        "raw_text_leak_check": "PASS",
    }
    safe_check = json.dumps(
        {"metrics": safe_metrics, "baseline": baselines},
        ensure_ascii=False,
        sort_keys=True,
    )
    if any("\u0600" <= char <= "\u06ff" for char in safe_check):
        raise ValueError("B4 safe metrics or baseline comparison contains raw Persian text")
    write_json(out / "B4_SAFE_METRICS.json", safe_metrics)

    make_standalone_comparison_database(comparison_db)
    with contextlib.closing(
        sqlite3.connect(f"file:{comparison_db}?mode=ro", uri=True)
    ) as connection:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_keys = connection.execute("PRAGMA foreign_key_check").fetchall()
        brief_count = connection.execute("SELECT COUNT(*) FROM p16_b4_candidate_briefs").fetchone()[
            0
        ]
        attempt_count = connection.execute("SELECT COUNT(*) FROM p16_b4_attempts").fetchone()[0]
    if any(Path(f"{comparison_db}{suffix}").exists() for suffix in ("-wal", "-shm")):
        raise ValueError("B4 standalone comparison left sidecar journal files")
    if (
        integrity != "ok"
        or foreign_keys
        or brief_count != len(COHORT)
        or attempt_count != len(COHORT)
        or file_sha(comparison_db) == file_sha(database)
    ):
        raise ValueError("B4 comparison database verification failed")

    final_audit = {
        "contract": "jobhunter-p16-b4-final-audit-v1",
        "status": safe_metrics["status"],
        "source_database_sha256": file_sha(database),
        "b2_candidate_sha256": b2_sha,
        "b3_candidate_sha256": b3_sha,
        "run_manifest_sha256": file_sha(out / "run_manifest.json"),
        "private_candidate_sha256": file_sha(out / "PRIVATE_B4_CANDIDATES.json"),
        "baseline_comparison_sha256": file_sha(out / "B4_BASELINE_COMPARISON.json"),
        "safe_metrics_sha256": file_sha(out / "B4_SAFE_METRICS.json"),
        "briefs_markdown_sha256": file_sha(out / "B4_BRIEFS.md"),
        "response_metadata_sha256": sha256_json(
            {path.name: file_sha(path) for path in sorted(raw_dir.glob("*.response-metadata.json"))}
        ),
        "raw_reasoning_content_retained": False,
        "raw_response_body_files_retained": False,
        "comparison_database_sha256": file_sha(comparison_db),
        "standalone_database_modified": file_sha(comparison_db) != file_sha(database),
        "comparison_database_journal_mode": "delete",
        "comparison_database_integrity": integrity,
        "comparison_database_foreign_key_violations": len(foreign_keys),
        "comparison_brief_rows": brief_count,
        "comparison_attempt_rows": attempt_count,
        "production_database_written": False,
        "accepted_facts_promoted": 0,
        "unseen_generalization_established": False,
    }
    write_json(out / "B4_FINAL_AUDIT.json", final_audit)
    print(json.dumps(safe_metrics, ensure_ascii=False, indent=2))
    print(f"B4 evidence directory: {out}")
    return safe_metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config/local.toml")
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--b2-dir", type=Path, default=DEFAULT_B2_DIR)
    parser.add_argument("--b3-dir", type=Path, default=DEFAULT_B3_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> None:
    run(parse_args())


if __name__ == "__main__":
    main()
