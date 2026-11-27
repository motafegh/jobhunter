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
    run = OfflineRun(root, "test-run", clock=clock)
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
    run = OfflineRun(root, "schedule", clock=Clock())
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
    run = OfflineRun(root, "order", clock=Clock())
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
    run = OfflineRun(root, "all-cells", clock=clock)
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
