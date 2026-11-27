"""Fixed offline V30 provider rehearsal; never accepts a real source or transport.

The child uses trusted code with a Python audit hook, not an OS sandbox.
"""

from __future__ import annotations

import contextlib
import json
import os
import platform
import re
import socket
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import httpx

from jobhunter.p16_lab import (
    ROOT,
    LabStopped,
    OfflineGuard,
    OfflineRun,
    Resources,
    checked_path,
    digest,
    inspect_journal,
    read_events,
)
from jobhunter.p16_lab_qualification import (
    ExactFit,
    RuntimeBinding,
    guarded_synthetic_fit,
    pinned_artifacts,
)

SCENARIOS = frozenset({"success", "nested", "malformed", "unowned", "network_denied", "stall"})
BASE = "http://127.0.0.1:18080/v1"


def _child(root: Path, run_id: str, scenario: str) -> dict:
    if scenario not in SCENARIOS:
        raise ValueError("unsupported fixed scenario")
    denied = []
    blocked_import_probes = []

    def deny(event, args):
        if (
            event.startswith("socket.")
            or event.startswith("sqlite3.connect")
            or event in {"subprocess.Popen", "os.system", "os.exec", "os.posix_spawn"}
        ):
            # urllib3 catches this import-time IPv6 capability probe. Deny it
            # physically as before, but distinguish the known probe from a bypass.
            frame = sys._getframe(1)
            known_probe = False
            while frame is not None:
                if (
                    frame.f_globals.get("__name__") == "urllib3.util.connection"
                    and frame.f_code.co_name == "_has_ipv6"
                ):
                    known_probe = True
                    break
                frame = frame.f_back
            if event == "socket.__new__" and known_probe:
                blocked_import_probes.append(event)
            else:
                denied.append(event)
            raise PermissionError("offline rehearsal denied external operation")

    sys.addaudithook(deny)
    from jobhunter import analysis_runtime_v16 as rt16
    from jobhunter import analysis_runtime_v20 as rt20
    from jobhunter.analysis_runtime_v30 import V30CandidateAnalysisProvider
    from jobhunter.analysis_service import AnalysisValidationError
    from jobhunter.analysis_service_v30 import JobAnalysisServiceV30
    from jobhunter.inference import instructor_lm_studio_v20 as v20
    from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context

    # Prevent SDK user-agent platform discovery from spawning a host subprocess.
    # Synthetic header metadata only; no change to semantic messages or schema.
    platform.platform = lambda *args, **kwargs: "offline-rehearsal"
    run = OfflineRun(root, run_id, diagnostic_only=True)
    run.start_session()
    run.start_cell(run.cells[0]["cell_id"])
    model = run.models["M0"]
    attempts = {"v15": 0, "v16": 0}
    original15 = rt20.validate_v15_candidate_structured
    original16 = rt16.validate_v16_candidate_structured

    def mock(req):
        if req.method == "GET":
            models = [
                {
                    "key": model,
                    "type": "llm",
                    "loaded_instances": [{"id": model, "config": {"context_length": 16384}}],
                }
            ]
            if scenario == "unowned":
                models.append(
                    {"key": "other", "type": "llm", "loaded_instances": [{"id": "other-instance"}]}
                )
            return httpx.Response(200, json={"models": models})
        if scenario == "stall":
            time.sleep(3600)
        content = (
            "not valid JSON"
            if scenario == "malformed"
            else json.dumps(
                {
                    "role_purpose": [],
                    "responsibilities": [],
                    "requirements": [],
                    "coverage_exclusions": [],
                }
            )
        )
        return httpx.Response(
            200,
            json={
                "id": "synthetic",
                "object": "chat.completion",
                "created": 1,
                "model": model,
                "choices": [
                    {
                        "index": 0,
                        "finish_reason": "stop",
                        "message": {"role": "assistant", "content": content},
                    }
                ],
                "usage": {"prompt_tokens": 10, "completion_tokens": 10},
            },
        )

    expected = pinned_artifacts(root)
    identity = expected["M0"]

    # These are explicitly synthetic fixtures, not measured tokenizer, rights or
    # runtime evidence. The request digest is computed at the HTTP seam.
    def binding():
        return RuntimeBinding(
            model_key=model,
            artifact_sha256=identity["sha256"],
            runtime_sha256="a" * 64,
            tokenizer_sha256="b" * 64,
            effective_template_sha256="c" * 64,
            rights_receipt_sha256="d" * 64,
            instance_id=model,
            allocated_context=16384,
            lease_id=run.path.name,
            idle_confirmed=True,
            synthetic=True,
            observed_at=run.clock(),
        )

    def proof(req):
        return ExactFit(
            request_sha256=digest(req.content),
            artifact_sha256=identity["sha256"],
            runtime_sha256="a" * 64,
            tokenizer_sha256="b" * 64,
            effective_template_sha256="c" * 64,
            input_tokens=100,
            output_tokens=json.loads(req.content)["max_tokens"],
            context_tokens=16384,
            synthetic=True,
        )

    g = OfflineGuard(
        run,
        inner=httpx.MockTransport(mock),
        fit=guarded_synthetic_fit(run, expected, binding=binding, proof=proof),
        resources=lambda: Resources(run.clock(), 1024, 16, 16, 0),
    )

    def client(**kw):
        if kw.get("trust_env") is not False:
            run.stop("unexpected_client_configuration")
        return httpx.Client(**kw, transport=g, follow_redirects=False)

    def control(**kw):
        return ensure_lm_studio_model_context(**kw, transport=g)

    def validate15(structured, fields):
        original15(structured, fields)
        attempts["v15"] += 1
        if scenario == "nested" and attempts["v15"] in {1, 3}:
            raise AnalysisValidationError("synthetic V15 boundary failure")

    def validate16(structured, fields):
        original16(structured, fields)
        attempts["v16"] += 1
        if scenario == "nested" and attempts["v16"] == 1:
            raise AnalysisValidationError("synthetic V16 boundary failure")

    # Only in this disposable child; preserve actual provider, SDK and recovery chain.
    rt20.ensure_lm_studio_model_context = control
    v20.httpx = SimpleNamespace(Client=client, Timeout=httpx.Timeout)
    rt20.validate_v15_candidate_structured = validate15
    rt16.validate_v16_candidate_structured = validate16
    error = None
    try:
        if scenario == "network_denied":
            try:
                socket.socket()
            except PermissionError:
                run.stop("network_denied")
            run.stop("network_denial_not_observed")
        p = V30CandidateAnalysisProvider(
            base_url=BASE,
            configured_model=model,
            api_token=None,
            timeout_seconds=30,
            max_retries=0,
        )
        result = p.complete_structured(
            model=model,
            system_prompt=JobAnalysisServiceV30.system_prompt,
            user_payload={"analysis_fields": {"title": "Synthetic"}, "analysis_mode": "english"},
            max_tokens=8192,
            seed=17,
        )
        if denied or run.stopped:
            run.stop("unexpected_denial")
        if set(result.structured) != {
            "role_purpose",
            "responsibilities",
            "requirements",
            "coverage_exclusions",
        }:
            run.stop("unexpected_response_shape")
        run.finish_cell(idle_confirmed=True)  # only synthetic, not server evidence
    except Exception as exc:
        error = type(exc).__name__
        if not run.stopped:
            with contextlib.suppress(LabStopped):
                run.stop("provider_failed")
    report = run.seal()
    return {
        "scenario": scenario,
        "synthetic_only": True,
        "error_type": error,
        "validation_calls": attempts,
        "denied_operations": len(denied),
        "denied_event_names": sorted(set(denied)),
        "blocked_import_probe_events": sorted(set(blocked_import_probes)),
        "generation_reservations": report["generation_reservations"],
        "control_reservations": report["control_reservations"],
        "stopped": report["stopped"],
        "finished": report["simulated_cells_finished"],
        "real_dispatches": 0,
        "server_idle_established": False,
    }


def rehearse_provider(root: Path, run_id: str, scenario: str, timeout: float = 20) -> dict:
    """Run the fixed child with a parent deadline; never retry an uncertain child."""
    if (
        scenario not in SCENARIOS
        or not 0 < timeout <= 240
        or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}", run_id)
    ):
        raise ValueError("invalid rehearsal specification")
    root = root.resolve(strict=True)
    path = checked_path(root, f"data/local-acceptance/p16-evolution-e3/{run_id}")
    if path.exists():
        raise FileExistsError("run ID already exists")
    cmd = [
        sys.executable,
        "-I",
        "-B",
        "-m",
        "jobhunter.p16_lab_provider_worker",
        "--child",
        str(root),
        run_id,
        scenario,
    ]
    start = time.monotonic()
    result = None
    report = None
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            check=False,
            env={"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8"},
        )
        status = "child_failed" if result.returncode else "child_completed"
        if not result.returncode:
            report = json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        status = "child_timeout"
    except (OSError, ValueError):
        status = "child_or_report_failed"
    journal = path / "dispatch.jsonl"
    inspection = inspect_journal(journal) if journal.is_file() else None
    if status == "child_completed":
        if not inspection or not inspection["sealed"] or not isinstance(report, dict):
            status = "child_receipt_unverified"
        else:
            rows = read_events(journal)
            counts = {
                kind: sum(row["event"] == "reserved" and row.get("kind") == kind for row in rows)
                for kind in ("generation", "control")
            }
            if (
                report.get("scenario") != scenario
                or report.get("real_dispatches") != 0
                or report.get("synthetic_only") is not True
                or any(
                    report.get(kind + "_reservations") != count for kind, count in counts.items()
                )
            ):
                status = "child_receipt_unverified"
    return {
        "status": status,
        "elapsed_seconds": time.monotonic() - start,
        "journal": inspection,
        "child": report if status == "child_completed" else None,
        "real_dispatch_enabled": False,
        "server_idle_established": False,
        "retry_allowed": False,
    }


def main() -> int:
    if len(sys.argv) == 5 and sys.argv[1] == "--child":
        print(json.dumps(_child(Path(sys.argv[2]), sys.argv[3], sys.argv[4])))
        return 0
    if len(sys.argv) != 3 or sys.argv[2] not in SCENARIOS:
        return 2
    print(json.dumps(rehearse_provider(ROOT, sys.argv[1], sys.argv[2]), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
