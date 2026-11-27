"""Offline-only fixed worker supervisor exercising crash and deadline containment."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import httpx

from jobhunter.p16_lab import (
    ROOT,
    Fit,
    LabStopped,
    OfflineGuard,
    OfflineRun,
    Resources,
    canonical,
    digest,
    inspect_journal,
    publish_new,
)

# Fixed synthetic actions, not arbitrary commands or a live model worker.
SCENARIOS = frozenset({"complete", "crash", "stall"})


def supervise_offline(root: Path, run_id: str, scenario: str, timeout: float) -> dict:
    if scenario not in SCENARIOS or not 0 < timeout <= 240:
        raise ValueError("invalid synthetic worker specification")
    run = OfflineRun(root, run_id)
    run.start_session()
    run.start_cell(run.cells[0]["cell_id"])
    status = "not_started"

    def mock_dispatch(request: httpx.Request) -> httpx.Response:
        nonlocal status
        run.event("worker_started", scenario=scenario)
        start = time.monotonic()
        # The worker receives no ad, credential, server URL or arbitrary command.
        cmd = [
            sys.executable,
            "-I",
            "-B",
            "-m",
            "jobhunter.p16_lab_watchdog",
            "--synthetic-worker",
            scenario,
        ]
        remaining = run.cell_start + run.budget["wall_seconds_per_cell"] - start
        try:
            if remaining <= 0:
                run.stop("cell_deadline")
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=min(timeout, remaining),
                check=False,
                env={"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8"},
            )
            status = "completed" if result.returncode == 0 else "worker_failed"
        except subprocess.TimeoutExpired:
            # Direct child killed/reaped by subprocess.run; NOT server idle proof.
            status = "worker_timeout"
        except OSError:
            status = "worker_launch_failed"
        run.event("worker_result", status=status, elapsed=time.monotonic() - start)
        if status != "completed":
            run.stop(status)
        return httpx.Response(200, json={})

    transport = OfflineGuard(
        run,
        inner=httpx.MockTransport(mock_dispatch),
        fit=lambda req: Fit(digest(req.content), 100, 512, 16384),
        resources=lambda: Resources(run.clock(), 1024, 16, 16, 0),
    )
    request = httpx.Request(
        "POST",
        "http://127.0.0.1:18080/v1/chat/completions",
        json={
            "model": run.models["M0"],
            "max_tokens": 512,
            "messages": [{"role": "user", "content": "synthetic watchdog control"}],
        },
    )
    try:
        transport.handle_request(request)
        run.finish_cell(idle_confirmed=True)  # synthetic only, no server contacted
    except LabStopped:
        pass
    report = run.seal()
    evidence = {
        "worker_status": status,
        "synthetic_only": True,
        "server_idle_established": False,
        "receipt": report,
        "journal": inspect_journal(run.path / "dispatch.jsonl"),
    }
    publish_new(run.path / "watchdog.json", canonical(evidence))
    return evidence


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--synthetic-worker":
        scenario = sys.argv[2]
        if scenario == "complete":
            return 0
        if scenario == "crash":
            return 73
        if scenario == "stall":
            time.sleep(3600)
        return 2
    # Explicit offline-only entry, no model configuration or network support.
    if len(sys.argv) != 3 or sys.argv[2] not in SCENARIOS:
        print(
            "usage: python -m jobhunter.p16_lab_watchdog RUN_ID complete|crash|stall",
            file=sys.stderr,
        )
        return 2
    print(json.dumps(supervise_offline(ROOT, sys.argv[1], sys.argv[2], 2), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
