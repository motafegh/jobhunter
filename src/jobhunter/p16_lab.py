"""Offline-only foundation for the P1.6 AI Lab. No production routing or real transport."""

from __future__ import annotations

import fcntl
import hashlib
import json
import math
import os
import re
import shutil
import sqlite3
import sys
import threading
import time
from collections.abc import Callable
from contextlib import closing
from dataclasses import dataclass
from importlib.metadata import version
from pathlib import Path
from typing import Any

import httpx

FREEZE_PATH = "docs/working-memory/2026-11-27_p16_e2_freeze/E3_REQUIREMENTS_FREEZE.json"
FREEZE_SHA = "e687bac59e54ed4e137e67a0944325aaecc56149e17c5da8612ef18b0fee8df4"
PROTOCOL_PATH = "docs/working-memory/2026-11-26_p16_e2/EXPERIMENT_PROTOCOL_DRAFT.json"
CONTRACT = "p16-e3-lab-receipt-v1"
SNAPSHOTS = {
    "accepted": (
        "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/configured_local_snapshot.sqlite3"
    ),
    "exposed": (
        "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
    ),
    "nov23": "data/local-acceptance/2026-11-23-fresh-e2e-manual-audit/data/current-cohort.sqlite3",
}
ROOT = Path(__file__).resolve().parents[2]


class LabStopped(RuntimeError):
    """No further dispatch is allowed in the affected run."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode()


def file_digest(path: Path) -> str:
    with path.open("rb") as file:
        h = hashlib.sha256()
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            h.update(chunk)
        return h.hexdigest()


def checked_path(root: Path, relative: str) -> Path:
    """Reject symlinks and traversal in trusted local workspace paths, not a sandbox."""
    parts = Path(relative).parts
    if not parts or Path(relative).is_absolute() or any(p in ("..", ".") for p in parts):
        raise ValueError("invalid relative path")
    root = root.resolve(strict=True)
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise ValueError("symlink forbidden")
    if not path.resolve().is_relative_to(root):
        raise ValueError("path escapes root")
    return path


def load_requirements(root: Path = ROOT) -> tuple[dict, dict]:
    """Validate pinned requirements and all immutable design inputs, no private reads."""
    freeze_bytes = checked_path(root, FREEZE_PATH).read_bytes()
    if digest(freeze_bytes) != FREEZE_SHA:
        raise ValueError("requirements seal mismatch")
    freeze = json.loads(freeze_bytes)
    for rel, expected in freeze["design_inputs_sha256"].items():
        if file_digest(checked_path(root, rel)) != expected:
            raise ValueError("design input mismatch")
    protocol = json.loads(checked_path(root, PROTOCOL_PATH).read_bytes())
    if protocol["budget"] != freeze["budget"]:
        raise ValueError("budget mismatch")
    return freeze, protocol


def execution_identity() -> dict:
    """Bind offline continuation to checkout source bytes and key installed versions.

    Not a full dependency lock or attestation of loaded modules/native runtime.
    """
    source = ROOT / "src/jobhunter"
    files = {str(p.relative_to(ROOT)): file_digest(p) for p in sorted(source.rglob("*.py"))}
    files["pyproject.toml"] = file_digest(ROOT / "pyproject.toml")
    return {
        "contract": "p16-offline-execution-identity-v1",
        "source_tree_sha256": digest(canonical(files)),
        "source_files": len(files),
        "python": sys.version,
        "packages": {
            name: version(name)
            for name in (
                "httpx",
                "httpcore",
                "openai",
                "instructor",
                "pydantic",
                "pydantic-core",
                "tenacity",
                "jsonschema",
            )
        },
    }


def verify_private_copies(path: Path, rows: list[dict], expected: dict) -> None:
    """Match named clone events and immutable copies; no DB initialization."""
    cloned = {}
    for row in rows:
        if row["event"] == "snapshot_cloned":
            name = row["snapshot"]
            if name in cloned or name not in expected or row["sha256"] != expected[name]:
                raise ValueError("snapshot event mismatch")
            cloned[name] = row["sha256"]
    for name in SNAPSHOTS:
        copy = checked_path(path, f"{name}.sqlite3")
        if name in cloned:
            if not copy.is_file() or file_digest(copy) != cloned[name]:
                raise ValueError("private copy mismatch")
            for suffix in ("-wal", "-journal", "-shm"):
                if Path(str(copy) + suffix).exists():
                    raise ValueError("private copy sidecar")
        elif copy.exists():
            raise ValueError("unrecorded private copy")


def sync_directory(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def publish_new(path: Path, data: bytes) -> None:
    """Atomic no-overwrite publication on a local POSIX filesystem."""
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as file:
        file.write(data)
        file.flush()
        os.fsync(file.fileno())
    os.link(temp, path)
    temp.unlink()
    sync_directory(path.parent)


class Journal:
    """Single writer, append-only fsynced events. Never logs payloads or exception text."""

    def __init__(self, path: Path):
        self.path = path
        self._file = path.open("xb")
        fcntl.flock(self._file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        self._seq = 0
        sync_directory(path.parent)

    @classmethod
    def reopen_checkpoint(cls, path: Path) -> tuple[Journal, list[dict]]:
        journal = cls.__new__(cls)
        journal.path = path
        journal._file = path.open("r+b")
        try:
            fcntl.flock(journal._file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            rows = read_events(path)
            if not rows or rows[-1]["event"] != "session_checkpoint":
                raise ValueError("no clean session checkpoint")
            if rows[-1].get("prefix_sha256") != digest(
                b"".join(canonical(row) for row in rows[:-1])
            ):
                raise ValueError("checkpoint prefix mismatch")
            if any(row["event"] in {"stopped", "run_sealed"} for row in rows):
                raise ValueError("terminal journal")
            journal._seq = len(rows)
            journal._file.seek(0, os.SEEK_END)
            return journal, rows
        except BaseException:
            journal.close()
            raise

    def append(self, event: str, **fields: Any) -> int:
        seq = self._seq + 1
        self._file.write(canonical({"seq": seq, "event": event, **fields}))
        self._file.flush()
        os.fsync(self._file.fileno())
        self._seq = seq
        return seq

    def close(self) -> None:
        self._file.close()


def read_events(path: Path) -> list[dict]:
    data = path.read_bytes()
    if not data.endswith(b"\n"):
        raise ValueError("torn journal")
    rows = [json.loads(line) for line in data.splitlines()]
    pending = set()
    for i, row in enumerate(rows, 1):
        if row["seq"] != i:
            raise ValueError("invalid journal sequence")
        if row["event"] == "reserved":
            pending.add(i)
        elif row["event"] == "result":
            pending.remove(row["reservation"])
    if pending:
        raise ValueError("outstanding reservation")
    return rows


def inspect_journal(path: Path) -> dict:
    """Read-only recovery; torn/malformed suffix is not a successful completion."""
    events = []
    damaged = False
    pending = set()
    for line in path.read_bytes().splitlines(keepends=True):
        try:
            if not line.endswith(b"\n"):
                raise ValueError("torn event")
            row = json.loads(line)
            if row["seq"] != len(events) + 1:
                raise ValueError("event order")
            if row["event"] == "reserved":
                pending.add(row["seq"])
            elif row["event"] == "result":
                pending.remove(row["reservation"])
            events.append(row)
        except (ValueError, KeyError, TypeError):
            damaged = True
            break
    final_event = bool(
        events and events[-1]["event"] == "run_sealed" and not damaged and not pending
    )
    receipt = path.with_name("receipt.json")
    published = (
        final_event
        and receipt.is_file()
        and file_digest(receipt) == events[-1].get("receipt_sha256")
    )
    return {
        "valid_events": len(events),
        "outstanding_reservations": sorted(pending),
        "damaged_suffix": damaged,
        "journal_final_event": final_event,
        "sealed": bool(published),
        "resume_allowed": False,
    }


@dataclass(frozen=True, slots=True)
class Fit:
    """Synthetic proof bound to exact request bytes; real tokenizer proof not yet implemented."""

    request_sha256: str
    input_tokens: int
    output_tokens: int
    context_tokens: int


@dataclass(frozen=True, slots=True)
class Resources:
    observed_at: float
    free_vram_mib: int
    windows_available_gib: float
    wsl_available_gib: float
    swap_growth_mib: int
    thermal_or_oom: bool = False


class OfflineRun:
    """Offline simulation of the sealed schedule; clean session checkpoint continuation only.

    All calls use an explicit MockTransport. Real model/control calls are not implemented.
    This owns counters across cells/sessions; any stop is sticky. No concurrent dispatch.
    """

    def __init__(
        self,
        root: Path,
        run_id: str,
        *,
        clock: Callable[[], float] = time.monotonic,
        diagnostic_only: bool = False,
    ):
        if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}", run_id):
            raise ValueError("invalid run ID")
        freeze, protocol = load_requirements(root)
        self.root = root.resolve(strict=True)
        self.snapshot_hashes = freeze["frozen_snapshot_sha256"]
        self.execution = execution_identity()
        self.diagnostic_only = diagnostic_only
        self.preflight_results: dict[str, str] = {}
        self.preflight_gen = self.preflight_control = 0
        self.diagnostic_gen = self.diagnostic_control = 0
        self.skipped_cells: list[str] = []
        self.conditional_eligible: bool | None = None
        self.paused = False
        self.budget = freeze["budget"]
        self.cells = tuple(protocol["cells"])
        self.models = {**protocol["model_roles"], "challenger": protocol["model_roles"]["M1"]}
        # Offline default only; actual challenger selection needs preflight evidence.
        path = checked_path(root, "data/local-acceptance/p16-evolution-e3")
        path.mkdir(parents=True, exist_ok=True)
        self.path = checked_path(root, f"data/local-acceptance/p16-evolution-e3/{run_id}")
        self.path.mkdir(mode=0o700, exist_ok=False)
        sync_directory(path)
        publish_new(
            self.path / "manifest.json",
            canonical(
                {
                    "contract": CONTRACT,
                    "mode": "offline_simulation",
                    "authority": "candidate_only",
                    "requirements_sha256": FREEZE_SHA,
                    "run_id": run_id,
                    "cells": self.cells,
                    "budget": self.budget,
                    "real_dispatch_enabled": False,
                    "simulated_challenger": "M1",
                    "diagnostic_only": diagnostic_only,
                    "execution_identity": self.execution,
                }
            ),
        )
        self.journal = Journal(self.path / "dispatch.jsonl")
        self.clock = clock
        self.started = clock()
        self.last_clock = self.started
        self.owner_thread = threading.get_ident()
        self.session_start: float | None = None
        self.active_elapsed = 0.0
        self.session_cells = 0
        self.next_index = 0
        self.cell: dict | None = None
        self.cell_start = 0.0
        self.gen = self.control = self.cell_gen = self.cell_control = 0
        self.context_reserved = self.output_reserved = 0
        self.stopped = False
        self.sealed = False
        self.in_flight = False
        self.journal.append(
            "run_started",
            mode="offline_simulation",
            manifest_sha256=file_digest(self.path / "manifest.json"),
        )

    def clone_snapshot(self, name: str) -> Path:
        """Prepare exact closed private copy; caller guarantees no active snapshot writers."""
        self.check_time()
        if self.cell is not None or self.next_index or name not in SNAPSHOTS:
            self.stop("invalid_snapshot_request")
        try:
            source = checked_path(self.root, SNAPSHOTS[name])
            expected = self.snapshot_hashes[name]
            dest = checked_path(self.path, f"{name}.sqlite3")
            temp = dest.with_suffix(".copy.tmp")
            if dest.exists() or temp.exists():
                raise ValueError("copy already exists")

            def check_source():
                # Retained frozen WAL may exist but must have no pending frames.
                for suffix in ("-wal", "-journal"):
                    sidecar = Path(str(source) + suffix)
                    if sidecar.is_symlink() or (sidecar.exists() and sidecar.stat().st_size):
                        raise ValueError("unclosed source snapshot")
                if file_digest(source) != expected:
                    raise ValueError("source digest mismatch")

            check_source()
            with source.open("rb") as src, temp.open("xb") as dst:
                shutil.copyfileobj(src, dst, length=1024 * 1024)
                dst.flush()
                os.fsync(dst.fileno())
            check_source()
            if file_digest(temp) != expected:
                raise ValueError("copy digest mismatch")
            with closing(sqlite3.connect(temp.as_uri() + "?mode=ro&immutable=1", uri=True)) as db:
                db.execute("PRAGMA query_only=ON")
                if db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                    raise ValueError("copy integrity")
                if db.execute("PRAGMA foreign_key_check").fetchone() is not None:
                    raise ValueError("copy foreign keys")
            self.check_time()
            os.link(temp, dest)
            temp.unlink()
            sync_directory(self.path)
            self.event("snapshot_cloned", snapshot=name, sha256=expected)
            return dest
        except LabStopped:
            raise
        except Exception:
            self.stop("snapshot_copy_failed")

    def event(self, name: str, **fields: Any) -> int:
        try:
            return self.journal.append(name, **fields)
        except BaseException:
            self.stopped = True
            raise

    def stop(self, reason: str) -> None:
        if not self.stopped and not self.sealed:
            self.stopped = True
            self.event("stopped", reason=reason)
        raise LabStopped(reason)

    def require_open(self) -> None:
        if threading.get_ident() != self.owner_thread:
            raise LabStopped("single owner thread required")
        if self.stopped or self.sealed or self.paused:
            raise LabStopped("run not open")

    def check_time(self) -> None:
        self.require_open()
        if self.session_start is None:
            self.stop("no_active_session")
        now = self.clock()
        elapsed = now - self.session_start
        if not math.isfinite(elapsed) or elapsed < 0 or now < self.last_clock:
            self.stop("invalid_clock")
        self.last_clock = now
        if elapsed >= self.budget["active_seconds_per_session_cap"]:
            self.stop("session_deadline")
        if self.active_elapsed + elapsed >= self.budget["active_total_seconds_cap"]:
            self.stop("total_deadline")
        if self.cell is not None and now - self.cell_start >= self.unit_wall_limit:
            self.stop("cell_deadline")

    def start_session(self) -> None:
        self.require_open()
        if self.session_start is not None or self.cell is not None:
            self.stop("session_already_active")
        if self.active_elapsed >= self.budget["active_total_seconds_cap"]:
            self.stop("total_deadline")
        self.session_start = self.clock()
        self.session_cells = 0
        self.event("session_started")

    def finish_session(self) -> None:
        self.check_time()
        if self.cell is not None:
            self.stop("cell_still_open")
        assert self.session_start is not None
        self.active_elapsed += self.clock() - self.session_start
        self.session_start = None
        self.event("session_finished", active_seconds=self.active_elapsed)

    @property
    def is_preflight(self) -> bool:
        return self.cell is not None and self.cell.get("phase") == "preflight"

    @property
    def unit_wall_limit(self) -> int:
        key = "preflight_seconds_per_model" if self.is_preflight else "wall_seconds_per_cell"
        return self.budget[key]

    def _begin_unit(self, unit: dict) -> None:
        self.cell = unit
        self.cell_start = self.clock()
        self.cell_gen = self.cell_control = self.cell_success = 0
        self.context_reserved = self.output_reserved = 0

    def start_preflight(self, role: str) -> None:
        self.check_time()
        if (
            self.diagnostic_only
            or self.cell is not None
            or self.next_index
            or role in self.preflight_results
        ):
            self.stop("invalid_preflight_transition")
        expected = (
            "M0"
            if not self.preflight_results
            else "M1"
            if self.preflight_results == {"M0": "qualified"}
            else "M2"
            if self.preflight_results == {"M0": "qualified", "M1": "blocked"}
            else None
        )
        if role != expected:
            self.stop("invalid_preflight_order")
        self._begin_unit({"cell_id": "preflight-" + role, "model_role": role, "phase": "preflight"})
        self.event("preflight_started", role=role)

    def finish_preflight(
        self, *, outcome: str, idle_confirmed: bool, blocker: str | None = None
    ) -> None:
        self.check_time()
        if not self.is_preflight or self.in_flight or idle_confirmed is not True:
            self.stop("preflight_idle_or_state")
        role = self.cell["model_role"]
        if outcome == "qualified":
            if self.cell_gen != 2 or self.cell_success != 2 or blocker is not None:
                self.stop("preflight_probes_required")
        elif outcome == "blocked":
            if blocker not in {"technical", "rights"}:
                self.stop("invalid_preflight_blocker")
        else:
            self.stop("invalid_preflight_outcome")
        self.preflight_results[role] = outcome
        self.event(
            "preflight_finished",
            role=role,
            outcome=outcome,
            blocker=blocker,
            generation=self.cell_gen,
            control=self.cell_control,
        )
        self.cell = None
        if role == "M0" and outcome == "blocked":
            self.stop("baseline_preflight_blocked")
        if role == "M2" and outcome == "blocked":
            self.stop("no_qualified_challenger")
        if role == "M2" and outcome == "qualified":
            self.models["challenger"] = self.models["M2"]

    def _preflight_ready(self) -> bool:
        return self.diagnostic_only or (
            self.preflight_results.get("M0") == "qualified"
            and (
                self.preflight_results.get("M1") == "qualified"
                or self.preflight_results.get("M2") == "qualified"
            )
        )

    def decide_interaction(self, *, eligible: bool) -> None:
        self.check_time()
        if (
            self.cell is not None
            or self.conditional_eligible is not None
            or self.next_index >= len(self.cells)
            or not self.cells[self.next_index]["conditional_interaction"]
        ):
            self.stop("invalid_interaction_decision")
        self.conditional_eligible = eligible
        self.event("interaction_decided", eligible=eligible)

    def skip_interaction(self, cell_id: str) -> None:
        self.check_time()
        if (
            self.cell is not None
            or self.conditional_eligible is not False
            or self.next_index >= len(self.cells)
            or self.cells[self.next_index]["cell_id"] != cell_id
            or not self.cells[self.next_index]["conditional_interaction"]
        ):
            self.stop("invalid_interaction_skip")
        self.event("cell_skipped", cell_id=cell_id, reason="synthetic_a2_not_viable")
        self.skipped_cells.append(cell_id)
        self.next_index += 1

    def start_cell(self, cell_id: str) -> None:
        self.check_time()
        if self.cell is not None or self.next_index >= len(self.cells):
            self.stop("invalid_cell_transition")
        if not self._preflight_ready():
            self.stop("preflight_required")
        if self.session_cells >= self.budget["diagnostic_cells_per_session_cap"]:
            self.stop("session_cell_limit")
        cell = self.cells[self.next_index]
        if cell_id != cell["cell_id"]:
            self.stop("out_of_order_cell")
        if (
            not self.diagnostic_only
            and cell["conditional_interaction"]
            and self.conditional_eligible is not True
        ):
            self.stop("interaction_not_authorized")
        self._begin_unit(cell)
        self.session_cells += 1
        self.event("cell_started", cell_id=cell_id)

    def finish_cell(self, *, idle_confirmed: bool) -> None:
        self.check_time()
        if self.cell is None or self.is_preflight or self.in_flight or idle_confirmed is not True:
            self.stop("idle_not_confirmed")
        self.event(
            "cell_finished",
            cell_id=self.cell["cell_id"],
            generation=self.cell_gen,
            control=self.cell_control,
            outcome="simulation_only",
        )
        self.cell = None
        self.next_index += 1

    def pause(self) -> None:
        """Only explicitly finished sessions may continue in another process."""
        self.require_open()
        if self.session_start is not None or self.cell is not None or self.in_flight:
            self.stop("unsafe_checkpoint")
        try:
            if execution_identity() != self.execution:
                raise ValueError("execution identity changed")
            verify_private_copies(self.path, read_events(self.journal.path), self.snapshot_hashes)
        except Exception:
            self.stop("checkpoint_identity_mismatch")
        self.event(
            "session_checkpoint",
            active_seconds=self.active_elapsed,
            prefix_sha256=file_digest(self.journal.path),
        )
        self.journal.close()
        self.paused = True

    @classmethod
    def resume(cls, root: Path, run_id: str, *, clock: Callable[[], float] = time.monotonic):
        if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}", run_id):
            raise ValueError("invalid run ID")
        freeze, protocol = load_requirements(root)
        path = checked_path(root, f"data/local-acceptance/p16-evolution-e3/{run_id}")
        journal, rows = Journal.reopen_checkpoint(checked_path(path, "dispatch.jsonl"))
        try:
            manifest = json.loads(checked_path(path, "manifest.json").read_bytes())
            if (
                rows[0]["event"] != "run_started"
                or rows[0].get("manifest_sha256") != file_digest(path / "manifest.json")
                or manifest["requirements_sha256"] != FREEZE_SHA
                or manifest["cells"] != protocol["cells"]
                or manifest["budget"] != freeze["budget"]
                or manifest["run_id"] != run_id
                or manifest["real_dispatch_enabled"] is not False
                or type(manifest["diagnostic_only"]) is not bool
                or manifest.get("execution_identity") != execution_identity()
                or (path / "receipt.json").exists()
            ):
                raise ValueError("checkpoint manifest mismatch")
            verify_private_copies(path, rows, freeze["frozen_snapshot_sha256"])
            r = cls.__new__(cls)
            r.execution = manifest["execution_identity"]
            r.root, r.path, r.journal = root.resolve(strict=True), path, journal
            r.snapshot_hashes, r.budget = freeze["frozen_snapshot_sha256"], freeze["budget"]
            r.cells = tuple(protocol["cells"])
            r.models = {**protocol["model_roles"], "challenger": protocol["model_roles"]["M1"]}
            r.diagnostic_only = manifest["diagnostic_only"]
            r.preflight_results = {}
            r.skipped_cells = []
            r.conditional_eligible = None
            r.gen = r.control = r.preflight_gen = r.preflight_control = 0
            r.diagnostic_gen = r.diagnostic_control = r.next_index = 0
            r.active_elapsed = 0.0
            active_session = False
            active_unit = None
            for row in rows[1:]:
                event = row["event"]
                if event == "session_started":
                    if active_session:
                        raise ValueError("nested session")
                    active_session = True
                elif event in {"cell_started", "preflight_started"}:
                    if not active_session or active_unit is not None:
                        raise ValueError("invalid unit start")
                    active_unit = (event, row.get("cell_id", row.get("role")))
                elif event == "reserved":
                    if active_unit is None:
                        raise ValueError("reservation outside unit")
                    phase, kind = row["phase"], row["kind"]
                    expected = (
                        "preflight" if active_unit[0] == "preflight_started" else "diagnostic"
                    )
                    if phase != expected or kind not in {"generation", "control"}:
                        raise ValueError("invalid reservation")
                    if kind == "generation":
                        r.gen += 1
                        if phase == "preflight":
                            r.preflight_gen += 1
                        else:
                            r.diagnostic_gen += 1
                    else:
                        r.control += 1
                        if phase == "preflight":
                            r.preflight_control += 1
                        else:
                            r.diagnostic_control += 1
                elif event == "preflight_finished":
                    role = row["role"]
                    if active_unit != ("preflight_started", role) or role in r.preflight_results:
                        raise ValueError("invalid preflight finish")
                    r.preflight_results[role] = row["outcome"]
                    active_unit = None
                elif event in {"cell_finished", "cell_skipped"}:
                    cell_id = row["cell_id"]
                    if r.next_index >= len(r.cells) or r.cells[r.next_index]["cell_id"] != cell_id:
                        raise ValueError("invalid cell order")
                    if event == "cell_finished":
                        if active_unit != ("cell_started", cell_id):
                            raise ValueError("invalid cell finish")
                        active_unit = None
                    else:
                        if active_unit is not None:
                            raise ValueError("invalid cell skip")
                        r.skipped_cells.append(cell_id)
                    r.next_index += 1
                elif event == "interaction_decided":
                    if r.conditional_eligible is not None:
                        raise ValueError("duplicate interaction decision")
                    r.conditional_eligible = row["eligible"]
                elif event == "session_finished":
                    elapsed = row["active_seconds"]
                    if (
                        not active_session
                        or active_unit is not None
                        or not math.isfinite(elapsed)
                        or elapsed < r.active_elapsed
                    ):
                        raise ValueError("invalid session finish")
                    r.active_elapsed = elapsed
                    active_session = False
                elif event == "session_checkpoint":
                    if active_session or active_unit is not None:
                        raise ValueError("unsafe checkpoint")
                    if row["active_seconds"] != r.active_elapsed:
                        raise ValueError("checkpoint elapsed mismatch")
            if (
                active_session
                or active_unit is not None
                or r.gen > r.budget["all_generation_post_cap"]
                or r.control > r.budget["all_control_http_cap"]
                or r.diagnostic_gen > r.budget["diagnostic_generation_post_cap"]
                or r.preflight_gen > 6
                or r.active_elapsed >= r.budget["active_total_seconds_cap"]
            ):
                raise ValueError("checkpoint limit")
            if r.preflight_results.get("M2") == "qualified":
                r.models["challenger"] = r.models["M2"]
            r.clock = clock
            r.started = r.last_clock = clock()
            r.owner_thread = threading.get_ident()
            r.session_start = None
            r.session_cells = 0
            r.cell = None
            r.cell_start = 0.0
            r.cell_gen = r.cell_control = r.cell_success = 0
            r.context_reserved = r.output_reserved = 0
            r.stopped = r.sealed = r.in_flight = r.paused = False
            r.event("run_resumed")
            return r
        except BaseException:
            journal.close()
            raise

    def seal(self) -> dict:
        if self.sealed or self.paused:
            raise LabStopped("already sealed or paused")
        if threading.get_ident() != self.owner_thread or self.in_flight:
            raise LabStopped("unsafe seal")
        if self.cell is not None and not self.stopped:
            self.stop("unfinished_cell")
        if self.session_start is not None:
            elapsed = self.clock() - self.session_start
            if (
                not math.isfinite(elapsed)
                or elapsed < 0
                or elapsed >= self.budget["active_seconds_per_session_cap"]
                or self.active_elapsed + elapsed >= self.budget["active_total_seconds_cap"]
            ):
                self.stopped = True
                self.event("stopped", reason="seal_deadline_or_clock")
            if math.isfinite(elapsed) and elapsed >= 0:
                self.active_elapsed += elapsed
            self.session_start = None
        report = {
            "contract": CONTRACT,
            "mode": "offline_simulation",
            "authority": "candidate_only",
            "execution_identity": self.execution,
            "generation_reservations": self.gen,
            "control_reservations": self.control,
            "stopped": self.stopped,
            "active_seconds": self.active_elapsed,
            "simulated_cells_finished": self.next_index - len(self.skipped_cells),
            "skipped_cell_ids": self.skipped_cells,
            "preflight_results": self.preflight_results,
            "preflight_generation_reservations": self.preflight_gen,
            "preflight_control_reservations": self.preflight_control,
            "diagnostic_generation_reservations": self.diagnostic_gen,
            "diagnostic_control_reservations": self.diagnostic_control,
            "remaining_cell_ids": [c["cell_id"] for c in self.cells[self.next_index :]],
            "real_dispatches": 0,
            "resume_allowed": False,
            "active_unit": self.cell["cell_id"] if self.cell else None,
            "active_unit_outcome": "stopped" if self.cell and self.stopped else None,
        }
        self.event("run_sealed", stopped=self.stopped, receipt_sha256=digest(canonical(report)))
        self.journal.close()
        self.sealed = True
        publish_new(self.path / "receipt.json", canonical(report))
        return report


GEN_ROUTE = ("POST", "/v1/chat/completions")
CONTROL_ROUTES = {
    ("GET", "/api/v1/models"),
    ("POST", "/api/v1/models/load"),
    ("POST", "/api/v1/models/unload"),
}


class OfflineGuard(httpx.BaseTransport):
    """Transport seam at physical request boundary. No real transport can be supplied."""

    def __init__(
        self,
        run: OfflineRun,
        *,
        inner: httpx.MockTransport,
        fit: Callable[[httpx.Request], Fit | None],
        resources: Callable[[], Resources | None],
        owned_instances: frozenset[str] = frozenset(),
    ):
        if type(inner) is not httpx.MockTransport:
            raise TypeError("offline runner requires exact MockTransport")
        self.run = run
        self.inner = inner
        self.fit = fit
        self.resources = resources
        self.owned_instances = owned_instances

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        r = self.run
        r.check_time()
        if r.cell is None or r.in_flight:
            r.stop("no_cell_or_concurrent_dispatch")
        url = request.url
        route = (request.method, url.path)
        if (
            url.scheme != "http"
            or url.host != "127.0.0.1"
            or url.port != 18080
            or url.username
            or url.password
            or url.query
            or url.fragment
            or url.raw_path != url.path.encode()
            or route not in CONTROL_ROUTES | {GEN_ROUTE}
        ):
            r.stop("forbidden_route")
        try:
            sample = self.resources()
        except Exception:
            r.stop("resource_probe_failed")
        if not isinstance(sample, Resources):
            r.stop("resource_unknown")
        assert sample is not None
        values = (
            sample.observed_at,
            sample.free_vram_mib,
            sample.windows_available_gib,
            sample.wsl_available_gib,
            sample.swap_growth_mib,
        )
        b = r.budget
        if (
            not all(math.isfinite(x) for x in values)
            or not 0 <= r.clock() - sample.observed_at <= b["memory_poll_target_seconds"]
            or sample.free_vram_mib < b["minimum_free_vram_mib"]
            or sample.windows_available_gib < b["minimum_windows_available_gib"]
            or sample.wsl_available_gib < b["minimum_wsl_available_gib"]
            or sample.swap_growth_mib > b["max_swap_growth_mib"]
            or sample.thermal_or_oom
        ):
            r.stop("resource_limit")
        generation = route == GEN_ROUTE
        reservation = {}
        if generation:
            unit_cap = (
                b["preflight_posts_per_model"]
                if r.is_preflight
                else b["generation_post_cap_per_cell"]
            )
            phase_gen = r.preflight_gen if r.is_preflight else r.diagnostic_gen
            phase_cap = (
                b["preflight_model_cap"] * b["preflight_posts_per_model"]
                if r.is_preflight
                else b["diagnostic_generation_post_cap"]
            )
            if (
                r.cell_gen >= unit_cap
                or phase_gen >= phase_cap
                or r.gen >= b["all_generation_post_cap"]
            ):
                r.stop("generation_limit")
            try:
                proof = self.fit(request)
            except LabStopped:
                raise
            except Exception:
                r.stop("fit_probe_failed")
            try:
                body = json.loads(request.content)
            except (ValueError, httpx.RequestNotRead):
                r.stop("invalid_generation_body")
            output_cap = (
                b["preflight_output_cap_per_post"]
                if r.is_preflight
                else b["requested_output_tokens_per_call"]
            )
            if (
                not isinstance(body, dict)
                or not isinstance(proof, Fit)
                or proof.request_sha256 != digest(request.content)
                or body.get("model") != r.models.get(r.cell["model_role"])
                or body.get("stream", False) is not False
                or any(
                    type(x) is not int
                    for x in (proof.input_tokens, proof.output_tokens, proof.context_tokens)
                )
                or not proof.input_tokens > 0
                or not 0 < proof.output_tokens <= output_cap
                or body.get("max_tokens") != proof.output_tokens
                or proof.context_tokens != b["requested_context_tokens"]
                or proof.input_tokens + proof.output_tokens > proof.context_tokens
            ):
                r.stop("fit_unverified")
            if (
                r.context_reserved + proof.context_tokens > b["max_context_reservations_per_cell"]
                or r.output_reserved + proof.output_tokens > b["max_output_reservations_per_cell"]
            ):
                r.stop("reservation_limit")
            reservation = {"context": proof.context_tokens, "output": proof.output_tokens}
        else:
            if (
                r.cell_control >= b["control_cap_per_cell_or_preflight_model"]
                or r.control >= b["all_control_http_cap"]
            ):
                r.stop("control_limit")
            if route[0] == "POST":
                try:
                    control_body = json.loads(request.content)
                except (ValueError, httpx.RequestNotRead):
                    r.stop("invalid_control_body")
                if not isinstance(control_body, dict):
                    r.stop("invalid_control_body")
                if route[1].endswith("/unload"):
                    instance = control_body.get("instance_id")
                    if not isinstance(instance, str) or instance not in self.owned_instances:
                        r.stop("unowned_instance")
                elif (
                    control_body.get("model") != r.models.get(r.cell["model_role"])
                    or control_body.get("context_length") != b["requested_context_tokens"]
                ):
                    r.stop("invalid_model_load")
        r.check_time()
        if not 0 <= r.clock() - sample.observed_at <= b["memory_poll_target_seconds"]:
            r.stop("resource_sample_expired")
        seq = r.event(
            "reserved",
            cell_id=r.cell["cell_id"],
            kind="generation" if generation else "control",
            phase="preflight" if r.is_preflight else "diagnostic",
            route=route[1],
            **reservation,
        )
        if generation:
            r.gen += 1
            if r.is_preflight:
                r.preflight_gen += 1
            else:
                r.diagnostic_gen += 1
            r.cell_gen += 1
            r.context_reserved += reservation["context"]
            r.output_reserved += reservation["output"]
        else:
            r.control += 1
            if r.is_preflight:
                r.preflight_control += 1
            else:
                r.diagnostic_control += 1
            r.cell_control += 1
        r.in_flight = True
        started = r.clock()
        mock_dispatched = False
        status = None
        usage = None
        error = None
        try:
            r.check_time()
            if not 0 <= r.clock() - sample.observed_at <= b["memory_poll_target_seconds"]:
                r.stop("resource_sample_expired")
            mock_dispatched = True
            response = self.inner.handle_request(request)
            response.read()
            status = response.status_code
            if generation and 200 <= status < 300:
                r.cell_success += 1
            if generation:
                try:
                    raw = response.json().get("usage")
                    if isinstance(raw, dict):
                        usage = {
                            k: raw[k]
                            for k in ("prompt_tokens", "completion_tokens")
                            if type(raw.get(k)) is int and raw[k] >= 0
                        } or None
                except (ValueError, AttributeError):
                    pass
            if 300 <= status < 400:
                r.stop("redirect_forbidden")
            r.check_time()
            return response
        except BaseException as exc:
            error = type(exc).__name__
            # Unknown transport completion must not permit a retry or next cell.
            if not r.stopped:
                r.stopped = True
                r.event("stopped", reason="transport_outcome_unknown")
            raise
        finally:
            r.in_flight = False
            r.event(
                "result",
                reservation=seq,
                status=status,
                usage=usage,
                error=error,
                mock_dispatched=mock_dispatched,
                elapsed_seconds=r.clock() - started,
            )

    def close(self) -> None:
        # Nested clients do not own the shared run.
        pass
