from __future__ import annotations

import json
import shutil
import sqlite3
from contextlib import closing

import httpx
import pytest

from jobhunter.p16_lab import (
    FREEZE_PATH,
    ROOT,
    Fit,
    LabStopped,
    OfflineGuard,
    OfflineRun,
    Resources,
    digest,
    inspect_journal,
    load_requirements,
)
from jobhunter.p16_lab_watchdog import supervise_offline

BASE = "http://127.0.0.1:18080"


@pytest.fixture
def root(tmp_path):
    # Copy only sealed public design dependencies into a synthetic repo.
    freeze, _ = load_requirements()
    for name in [FREEZE_PATH, *freeze["design_inputs_sha256"]]:
        dest = tmp_path / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dest)
    return tmp_path


class Clock:
    now = 100.0

    def __call__(self):
        return self.now


@pytest.fixture
def active(root):
    clock = Clock()
    run = OfflineRun(root, "test-run", clock=clock, diagnostic_only=True)
    run.start_session()
    run.start_cell(run.cells[0]["cell_id"])
    yield run, clock
    if not run.sealed:
        run.journal.close()


def request(**extra):
    return httpx.Request(
        "POST",
        BASE + "/v1/chat/completions",
        json={
            "model": "gemma-4-e4b-it-ud",
            "max_tokens": 8192,
            "messages": [{"role": "user", "content": "PRIVATE_PAYLOAD_SENTINEL"}],
            **extra,
        },
    )


def guard(active, handler=None, fit=None, resources=None):
    run, clock = active
    return OfflineGuard(
        run,
        inner=httpx.MockTransport(handler or (lambda req: httpx.Response(200, json={}))),
        fit=fit or (lambda req: Fit(digest(req.content), 200, 8192, 16384)),
        resources=resources or (lambda: Resources(clock(), 1024, 16, 16, 0)),
    )


def test_sealed_inputs_and_tamper(root):
    _, protocol = load_requirements(root)
    assert len(protocol["cells"]) == 47
    path = root / FREEZE_PATH
    path.write_bytes(path.read_bytes() + b" ")
    with pytest.raises(ValueError, match="seal"):
        load_requirements(root)


def test_design_tamper(root):
    freeze, _ = load_requirements(root)
    path = root / next(iter(freeze["design_inputs_sha256"]))
    path.write_bytes(path.read_bytes() + b"x")
    with pytest.raises(ValueError, match="design input"):
        load_requirements(root)


def test_workspace_symlink_and_reuse(root, tmp_path):
    (root / "data").symlink_to(tmp_path / "outside", target_is_directory=True)
    with pytest.raises(ValueError, match="symlink"):
        OfflineRun(root, "safe")
    (root / "data").unlink()
    run = OfflineRun(root, "safe")
    run.seal()
    with pytest.raises(FileExistsError):
        OfflineRun(root, "safe")
    with pytest.raises(ValueError):
        OfflineRun(root, "../unsafe")


def test_nested_retry_accounting_and_sticky_ninth(active):
    run, _ = active
    seen = []

    def inner(req):
        rows = [json.loads(line) for line in run.journal.path.read_text().splitlines()]
        assert rows[-1]["event"] == "reserved"
        seen.append(req)
        return httpx.Response(503, json={"error": "private"})

    g = guard(active, inner)
    for _ in range(4):
        with httpx.Client(transport=g, trust_env=False, follow_redirects=False) as client:
            for _ in range(2):
                assert client.send(request()).status_code == 503
    with pytest.raises(LabStopped, match="generation_limit"):
        g.handle_request(request())
    with pytest.raises(LabStopped):
        g.handle_request(request())
    assert len(seen) == run.gen == 8
    receipt = run.seal()
    assert receipt["stopped"] and receipt["generation_reservations"] == 8
    assert receipt["real_dispatches"] == 0
    assert "PRIVATE_PAYLOAD_SENTINEL" not in run.journal.path.read_text()


@pytest.mark.parametrize(
    "url",
    [
        "https://127.0.0.1:18080/v1/chat/completions",
        "http://localhost:18080/v1/chat/completions",
        "http://127.0.0.1:1234/v1/chat/completions",
        BASE + "/v1/embeddings",
        BASE + "/v1/chat/completions?x=1",
        "http://user@127.0.0.1:18080/v1/chat/completions",
        BASE + "/v1/chat/%63ompletions",
        BASE + "/v1/chat/completions#foo",
    ],
)
def test_endpoint_denied(active, url):
    g = guard(active, lambda req: pytest.fail("unexpected dispatch"))
    with pytest.raises(LabStopped, match="forbidden_route"):
        g.handle_request(httpx.Request("POST", url))
    assert active[0].gen == 0


def test_redirect_and_usage(active):
    run, _ = active
    g = guard(active, lambda req: httpx.Response(302, headers={"location": "https://x.test"}))
    with pytest.raises(LabStopped, match="redirect"):
        g.handle_request(request())
    rows = [json.loads(x) for x in run.journal.path.read_text().splitlines()]
    assert rows[-1]["status"] == 302 and rows[-1]["usage"] is None


def test_usage_unknown_and_explicit_zero(active):
    run, _ = active
    responses = iter([{}, {"usage": {"prompt_tokens": 11, "completion_tokens": 0}}])
    g = guard(active, lambda req: httpx.Response(200, json=next(responses)))
    g.handle_request(request())
    g.handle_request(request())
    rows = [json.loads(x) for x in run.journal.path.read_text().splitlines()]
    assert [x["usage"] for x in rows if x["event"] == "result"] == [
        None,
        {"prompt_tokens": 11, "completion_tokens": 0},
    ]


@pytest.mark.parametrize(
    "proof",
    [
        None,
        Fit("bad", 100, 8192, 16384),
        Fit("bound", 9000, 8192, 16384),
        Fit("bound", 100, 8193, 16384),
        Fit("bound", True, 8192, 16384),
    ],
)
def test_invalid_fit(active, proof):
    def fit(req):
        if proof is not None and proof.request_sha256 == "bound":
            return Fit(
                digest(req.content), proof.input_tokens, proof.output_tokens, proof.context_tokens
            )
        return proof

    g = guard(active, lambda req: pytest.fail("dispatch"), fit=fit)
    with pytest.raises(LabStopped, match="fit_unverified"):
        g.handle_request(request())


@pytest.mark.parametrize(
    "overrides",
    [
        {"free_vram_mib": 511},
        {"windows_available_gib": 7.9},
        {"wsl_available_gib": 7.9},
        {"swap_growth_mib": 513},
        {"thermal_or_oom": True},
        {"observed_at": 98},
        {"free_vram_mib": float("nan")},
    ],
)
def test_resource_failures(active, overrides):
    values = dict(
        observed_at=100,
        free_vram_mib=1024,
        windows_available_gib=16,
        wsl_available_gib=16,
        swap_growth_mib=0,
    )
    values.update(overrides)
    g = guard(active, lambda req: pytest.fail("dispatch"), resources=lambda: Resources(**values))
    with pytest.raises(LabStopped, match="resource_limit"):
        g.handle_request(request())


def test_unknown_resource(active):
    g = guard(active, resources=lambda: None)
    with pytest.raises(LabStopped, match="resource_unknown"):
        g.handle_request(request())


def test_control_budget(active):
    g = guard(active)
    for _ in range(16):
        assert g.handle_request(httpx.Request("GET", BASE + "/api/v1/models")).status_code == 200
    with pytest.raises(LabStopped, match="control_limit"):
        g.handle_request(httpx.Request("GET", BASE + "/api/v1/models"))


def test_elapsed_after_response_and_no_retry(active):
    _, clock = active

    def inner(req):
        clock.now += 240
        return httpx.Response(200, json={})

    g = guard(active, inner)
    with pytest.raises(LabStopped, match="cell_deadline"):
        g.handle_request(request())
    with pytest.raises(LabStopped):
        g.handle_request(request())


def test_failure_attempt_recorded(active):
    run, _ = active

    def inner(req):
        raise httpx.ReadTimeout("private exception")

    g = guard(active, inner)
    with pytest.raises(httpx.ReadTimeout):
        g.handle_request(request())
    assert run.gen == 1
    row = json.loads(run.journal.path.read_text().splitlines()[-1])
    assert row["error"] == "ReadTimeout" and row["status"] is None
    assert "private exception" not in run.journal.path.read_text()


def test_idle_unknown_stops(active):
    run, _ = active
    with pytest.raises(LabStopped, match="idle_not_confirmed"):
        run.finish_cell(idle_confirmed=False)
    assert run.seal()["simulated_cells_finished"] == 0


def test_no_real_transport(active):
    with pytest.raises(TypeError, match="MockTransport"):
        OfflineGuard(active[0], inner=object(), fit=lambda req: None, resources=lambda: None)


def test_schedule_and_session_limit(root):
    run = OfflineRun(root, "schedule", clock=Clock(), diagnostic_only=True)
    try:
        run.start_session()
        for cell in run.cells[:12]:
            run.start_cell(cell["cell_id"])
            run.finish_cell(idle_confirmed=True)
        with pytest.raises(LabStopped, match="session_cell_limit"):
            run.start_cell(run.cells[12]["cell_id"])
        assert run.seal()["simulated_cells_finished"] == 12
    finally:
        run.journal.close()


def test_out_of_order(root):
    run = OfflineRun(root, "order", clock=Clock(), diagnostic_only=True)
    run.start_session()
    with pytest.raises(LabStopped, match="out_of_order"):
        run.start_cell(run.cells[1]["cell_id"])
    run.seal()


def test_torn_journal_recovery(active):
    run, _ = active
    seq = run.event("reserved", cell_id=run.cell["cell_id"], kind="generation")
    run.journal.close()
    with run.journal.path.open("ab") as file:
        file.write(b'{"seq":')
    report = inspect_journal(run.journal.path)
    assert report["outstanding_reservations"] == [seq]
    assert report["damaged_suffix"] and not report["sealed"] and not report["resume_allowed"]


@pytest.mark.parametrize(
    ("scenario", "expected", "timeout"),
    [
        ("complete", "completed", 5),
        ("crash", "worker_failed", 5),
        ("stall", "worker_timeout", 0.5),
    ],
)
def test_parent_watchdog(root, scenario, expected, timeout):
    result = supervise_offline(root, scenario, scenario, timeout)
    assert result["worker_status"] == expected
    assert result["synthetic_only"] and not result["server_idle_established"]
    assert result["receipt"]["stopped"] == (scenario != "complete")
    assert result["receipt"]["real_dispatches"] == 0


def test_receipt_missing_is_not_sealed(root):
    run = OfflineRun(root, "receipt")
    run.seal()
    assert inspect_journal(run.journal.path)["sealed"]
    (run.path / "receipt.json").unlink()
    report = inspect_journal(run.journal.path)
    assert report["journal_final_event"] and not report["sealed"]


def test_invalid_receipt_digest(root):
    run = OfflineRun(root, "corrupt")
    run.seal()
    (run.path / "receipt.json").write_text("{}")
    assert not inspect_journal(run.journal.path)["sealed"]


def test_no_retry_after_unknown_transport(active):
    g = guard(active, lambda req: (_ for _ in ()).throw(httpx.ReadTimeout("unknown")))
    with pytest.raises(httpx.ReadTimeout):
        g.handle_request(request())
    with pytest.raises(LabStopped):
        g.handle_request(request())
    assert active[0].gen == 1


def test_fit_probe_exception_is_sticky(active):
    def fail(req):
        raise ValueError("private")

    g = guard(active, fit=fail)
    with pytest.raises(LabStopped, match="fit_probe_failed"):
        g.handle_request(request())
    with pytest.raises(LabStopped):
        g.handle_request(request())
    assert active[0].gen == 0


def test_resource_probe_exception_is_sticky(active):
    def fail():
        raise ValueError("private")

    g = guard(active, resources=fail)
    with pytest.raises(LabStopped, match="resource_probe_failed"):
        g.handle_request(request())
    with pytest.raises(LabStopped):
        g.handle_request(request())
    assert active[0].gen == 0


def test_clock_regression(active):
    _, clock = active
    clock.now = 99
    with pytest.raises(LabStopped, match="invalid_clock"):
        guard(active).handle_request(request())


def test_total_active_budget(root):
    clock = Clock()
    run = OfflineRun(root, "total-time", clock=clock)
    for _ in range(4):
        run.start_session()
        clock.now += 3599
        run.finish_session()
    run.start_session()
    clock.now += 4
    with pytest.raises(LabStopped, match="total_deadline"):
        run.start_cell(run.cells[0]["cell_id"])
    run.seal()


def test_clone_verified_snapshot(root):
    from jobhunter.p16_lab import SNAPSHOTS, file_digest

    source = root / SNAPSHOTS["accepted"]
    source.parent.mkdir(parents=True)
    with closing(sqlite3.connect(source)) as db:
        db.execute("CREATE TABLE sample(id INTEGER PRIMARY KEY)")
        db.commit()
    before = file_digest(source)
    run = OfflineRun(root, "clone")
    # Synthetic fixture only: production constructor pins actual expected hashes.
    run.snapshot_hashes = {"accepted": before}
    run.start_session()
    clone = run.clone_snapshot("accepted")
    assert clone.parent == run.path
    assert file_digest(clone) == file_digest(source) == before
    run.seal()


@pytest.mark.parametrize("case", ["digest", "wal", "symlink", "unknown"])
def test_clone_refuses_invalid_snapshot(root, case):
    from jobhunter.p16_lab import SNAPSHOTS

    source = root / SNAPSHOTS["accepted"]
    source.parent.mkdir(parents=True)
    if case == "symlink":
        source.symlink_to(root / FREEZE_PATH)
    else:
        source.write_bytes(b"not a snapshot")
    if case == "wal":
        source.with_name(source.name + "-wal").write_bytes(b"pending")
    run = OfflineRun(root, "invalid-clone")
    run.start_session()
    with pytest.raises(LabStopped, match="snapshot"):
        run.clone_snapshot("production" if case == "unknown" else "accepted")
    assert not (run.path / "accepted.sqlite3").exists()
    run.seal()


def test_full_schedule_simulated_diagnostic_reservations(root):
    clock = Clock()
    run = OfflineRun(root, "all-cells", clock=clock, diagnostic_only=True)
    g = guard((run, clock))
    for i, cell in enumerate(run.cells):
        if i % 12 == 0:
            if i:
                run.finish_session()
            run.start_session()
        run.start_cell(cell["cell_id"])
        for _ in range(8):
            g.handle_request(request(model=run.models[cell["model_role"]]))
        for _ in range(16):
            g.handle_request(httpx.Request("GET", BASE + "/api/v1/models"))
        run.finish_cell(idle_confirmed=True)
    run.finish_session()
    report = run.seal()
    assert report["simulated_cells_finished"] == 47
    assert report["generation_reservations"] == 376
    assert report["control_reservations"] == 752
    assert report["real_dispatches"] == 0
    assert not report["remaining_cell_ids"]
    assert inspect_journal(run.journal.path)["sealed"]


def fit_for_body(req):
    return Fit(digest(req.content), 200, json.loads(req.content)["max_tokens"], 16384)


def preflight(run, clock, role, *, blocked=False):
    run.start_preflight(role)
    g = guard((run, clock), fit=fit_for_body)
    for _ in range(2):
        g.handle_request(request(model=run.models[role], max_tokens=512))
    run.finish_preflight(
        outcome="blocked" if blocked else "qualified",
        idle_confirmed=True,
        blocker="technical" if blocked else None,
    )


def test_preflight_required(root):
    run = OfflineRun(root, "no-preflight")
    run.start_session()
    with pytest.raises(LabStopped, match="preflight_required"):
        run.start_cell(run.cells[0]["cell_id"])
    run.seal()


def test_preflight_caps(root):
    clock = Clock()
    run = OfflineRun(root, "preflight-cap", clock=clock)
    run.start_session()
    run.start_preflight("M0")
    g = guard((run, clock), fit=fit_for_body)
    for _ in range(2):
        g.handle_request(request(max_tokens=512))
    with pytest.raises(LabStopped, match="generation_limit"):
        g.handle_request(request(max_tokens=512))
    receipt = run.seal()
    assert receipt["preflight_generation_reservations"] == 2
    assert receipt["diagnostic_generation_reservations"] == 0


@pytest.mark.parametrize("kind", ["output", "time", "order", "idle", "probes", "failed"])
def test_preflight_negative(root, kind):
    clock = Clock()
    run = OfflineRun(root, "negative-" + kind, clock=clock)
    run.start_session()
    with pytest.raises(LabStopped):
        if kind == "order":
            run.start_preflight("M2")
        else:
            run.start_preflight("M0")
            g = guard((run, clock), fit=fit_for_body)
            if kind == "output":
                g.handle_request(request(max_tokens=513))
            elif kind == "time":
                clock.now += 180
                g.handle_request(request(max_tokens=512))
            elif kind == "failed":
                g = guard((run, clock), handler=lambda req: httpx.Response(503), fit=fit_for_body)
                for _ in range(2):
                    g.handle_request(request(max_tokens=512))
                run.finish_preflight(outcome="qualified", idle_confirmed=True)
            else:
                run.finish_preflight(outcome="qualified", idle_confirmed=kind != "idle")
    assert run.seal()["stopped"]


def test_clean_checkpoint_preserves_budget_and_fallback(root):
    clock = Clock()
    r = OfflineRun(root, "checkpoint", clock=clock)
    r.start_session()
    preflight(r, clock, "M0")
    preflight(r, clock, "M1", blocked=True)
    preflight(r, clock, "M2")
    clock.now += 11
    r.finish_session()
    r.pause()
    with pytest.raises(LabStopped):
        r.start_session()
    # Different monotonic epoch is safe at a clean boundary.
    clock.now = 1
    r = OfflineRun.resume(root, "checkpoint", clock=clock)
    assert r.gen == r.preflight_gen == 6
    assert r.active_elapsed == 11
    assert r.models["challenger"] == r.models["M2"]
    with pytest.raises((ValueError, BlockingIOError)):
        OfflineRun.resume(root, "checkpoint")
    r.start_session()
    g = guard((r, clock), fit=fit_for_body)
    for cell in r.cells[:6]:
        r.start_cell(cell["cell_id"])
        g.handle_request(request(model=r.models[cell["model_role"]]))
        r.finish_cell(idle_confirmed=True)
    r.finish_session()
    r.pause()
    r = OfflineRun.resume(root, "checkpoint", clock=clock)
    assert r.gen == 12 and r.next_index == 6 and r.diagnostic_gen == 6
    receipt = r.seal()
    assert receipt["preflight_results"] == {"M0": "qualified", "M1": "blocked", "M2": "qualified"}
    assert receipt["generation_reservations"] == 12


@pytest.mark.parametrize("kind", ["torn", "manifest", "prefix", "active", "sealed"])
def test_resume_denies_invalid_state(root, kind):
    r = OfflineRun(root, "resume-" + kind, diagnostic_only=True)
    if kind == "active":
        r.start_session()
        r.start_cell(r.cells[0]["cell_id"])
        r.journal.close()
    elif kind == "sealed":
        r.seal()
    else:
        r.start_session()
        r.finish_session()
        r.pause()
        if kind == "torn":
            with r.journal.path.open("ab") as f:
                f.write(b"broken")
        elif kind == "manifest":
            p = r.path / "manifest.json"
            p.write_bytes(p.read_bytes() + b" ")
        else:
            p = r.journal.path
            p.write_bytes(
                p.read_bytes().replace(
                    b'"mode":"offline_simulation"', b'"mode":"offline_modified"', 1
                )
            )
    with pytest.raises((ValueError, KeyError, BlockingIOError)):
        OfflineRun.resume(root, "resume-" + kind)


def test_full_budget_with_preflight_and_checkpoints(root):
    clock = Clock()
    r = OfflineRun(root, "full-caps", clock=clock)
    r.start_session()
    for role in ("M0", "M1", "M2"):
        r.start_preflight(role)
        g = guard((r, clock), fit=fit_for_body)
        for _ in range(2):
            g.handle_request(request(model=r.models[role], max_tokens=512))
        for _ in range(16):
            g.handle_request(httpx.Request("GET", BASE + "/api/v1/models"))
        r.finish_preflight(
            outcome="blocked" if role == "M1" else "qualified",
            idle_confirmed=True,
            blocker="rights" if role == "M1" else None,
        )
    for i, cell in enumerate(r.cells):
        if i and i % 12 == 0:
            r.finish_session()
            r.pause()
            r = OfflineRun.resume(root, "full-caps", clock=clock)
            r.start_session()
        if cell["conditional_interaction"] and r.conditional_eligible is None:
            r.decide_interaction(eligible=True)
        r.start_cell(cell["cell_id"])
        g = guard((r, clock), fit=fit_for_body)
        for _ in range(8):
            g.handle_request(request(model=r.models[cell["model_role"]]))
        for _ in range(16):
            g.handle_request(httpx.Request("GET", BASE + "/api/v1/models"))
        r.finish_cell(idle_confirmed=True)
    r.finish_session()
    receipt = r.seal()
    assert receipt["generation_reservations"] == 382
    assert receipt["control_reservations"] == 800
    assert receipt["preflight_generation_reservations"] == 6
    assert receipt["diagnostic_generation_reservations"] == 376
    assert receipt["simulated_cells_finished"] == 47


def test_conditional_skip_receipt(root):
    clock = Clock()
    r = OfflineRun(root, "skip-interaction", clock=clock)
    r.start_session()
    preflight(r, clock, "M0")
    preflight(r, clock, "M1")
    for i, cell in enumerate(r.cells):
        if i and i % 12 == 0:
            r.finish_session()
            r.start_session()
        if cell["conditional_interaction"]:
            if r.conditional_eligible is None:
                r.decide_interaction(eligible=False)
            r.skip_interaction(cell["cell_id"])
            continue
        r.start_cell(cell["cell_id"])
        r.finish_cell(idle_confirmed=True)
    r.finish_session()
    receipt = r.seal()
    assert receipt["simulated_cells_finished"] == 42
    assert len(receipt["skipped_cell_ids"]) == 5
    assert not receipt["remaining_cell_ids"]


def test_actual_native_control_helper_injected(active):
    from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context

    run, _ = active
    model = run.models["M0"]
    seen = []

    def handler(req):
        seen.append(req.url.path)
        if req.method == "GET":
            return httpx.Response(
                200, json={"models": [{"key": model, "type": "llm", "loaded_instances": []}]}
            )
        return httpx.Response(
            200, json={"instance_id": model, "load_config": {"context_length": 16384}}
        )

    g = guard(active, handler)
    state = ensure_lm_studio_model_context(
        openai_base_url=BASE + "/v1", model=model, context_length=16384, transport=g
    )
    assert state.instance_id == model
    assert seen == ["/api/v1/models", "/api/v1/models/load"]
    assert run.control == 2


def test_native_exclusive_unowned_unload_blocked(active):
    from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context

    r, _ = active
    model = r.models["M0"]
    seen = []

    def handler(req):
        seen.append(req.url.path)
        return httpx.Response(
            200,
            json={
                "models": [
                    {"key": model, "type": "llm", "loaded_instances": []},
                    {"key": "other", "type": "llm", "loaded_instances": [{"id": "user-model"}]},
                ]
            },
        )

    g = guard(active, handler)
    with pytest.raises(LabStopped, match="unowned_instance"):
        ensure_lm_studio_model_context(
            openai_base_url=BASE + "/v1",
            model=model,
            context_length=16384,
            transport=g,
            exclusive_llm=True,
        )
    assert seen == ["/api/v1/models"]
    assert r.control == 1


def test_actual_instructor_boundary_fake_http(active, monkeypatch):
    from types import SimpleNamespace

    from pydantic import BaseModel

    from jobhunter.inference import instructor_lm_studio_v20 as v20

    class SyntheticResponse(BaseModel):
        text: str

    replies = iter(["not valid JSON", '{"text":"synthetic"}'])
    seen = []

    def handler(req):
        seen.append(json.loads(req.content))
        return httpx.Response(
            200,
            json={
                "id": "synthetic",
                "object": "chat.completion",
                "created": 1,
                "model": active[0].models["M0"],
                "choices": [
                    {
                        "index": 0,
                        "finish_reason": "stop",
                        "message": {"role": "assistant", "content": next(replies)},
                    }
                ],
                "usage": {"prompt_tokens": 20, "completion_tokens": 5},
            },
        )

    g = guard(active, handler, fit=fit_for_body)

    def client(**kwargs):
        assert kwargs["trust_env"] is False
        return httpx.Client(**kwargs, transport=g, follow_redirects=False)

    # Substitute only the module's httpx reference, not global httpx.Client.
    monkeypatch.setattr(v20, "httpx", SimpleNamespace(Client=client, Timeout=httpx.Timeout))
    result = v20._complete_analysis_partition_with_instructor(
        base_url=BASE + "/v1",
        api_token=None,
        timeout_seconds=30,
        network_retries=0,
        selected_model=active[0].models["M0"],
        system_prompt="synthetic",
        user_payload={"analysis_fields": {"title": "Synthetic"}, "analysis_mode": "english"},
        max_tokens=8192,
        seed=17,
        requirement_coverage_plan={},
        responsibility_coverage_plan={},
        response_model=SyntheticResponse,
        contract_version="synthetic",
        validation_retries=2,
    )
    assert result.structured == {"text": "synthetic"}
    assert len(seen) == active[0].gen == 2
