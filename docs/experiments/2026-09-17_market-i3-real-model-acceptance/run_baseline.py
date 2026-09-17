import json
import sqlite3
import subprocess
import time
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.config import Settings
from jobhunter.market_membership_service import build_market_membership_service
from jobhunter.market_models import MarketDefinitionSpec
from jobhunter.market_store import MarketStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore

now = datetime.now(UTC)
out = Path("data/experiments") / ("market-i3-" + now.strftime("%Y%m%dT%H%M%SZ"))
out.mkdir()
settings_source = Settings.load("jobhunter.toml")
original = settings_source.database_path.resolve()
sandbox = out / "sandbox.sqlite3"

with (
    sqlite3.connect(f"file:{original}?mode=ro", uri=True) as source,
    sqlite3.connect(sandbox) as target,
):
    source.backup(target)

settings = settings_source.model_copy(update={"database_path": sandbox})
market = MarketStore(sandbox)
target = market.create_target(
    slug="i3-acceptance-ai",
    name="Applied AI / ML Engineering",
    description="Isolated retrospective I3 acceptance.",
    created_at=now,
)
definition = market.create_definition_version(
    target.id,
    spec=MarketDefinitionSpec(
        membership_intent="Applied AI / ML engineering work",
        search_catalog_version="i3-acceptance-2026-09-17",
    ),
    created_at=now,
)

store = JobHunterStore(sandbox)
job_id = "i3-synthetic-sparse"
posting = store.upsert_job(
    job=DiscoveredJobLink(
        source_job_id=job_id,
        company_slug="synthetic-fixture",
        canonical_url=(
            "https://jobinja.ir/companies/synthetic-fixture/jobs/"
            f"{job_id}/role"
        ),
        observed_text="Technical team member",
    ),
    observed_at=now,
)
store.record_job_detail(
    job_posting_id=posting.job_posting_id,
    fetched_at=now,
    requested_url="https://jobinja.ir/jobs/i3-synthetic-sparse",
    final_url="https://jobinja.ir/jobs/i3-synthetic-sparse",
    status_code=200,
    content_sha256="synthetic-sparse",
    semantic_sha256="synthetic-sparse-v1",
    evidence_path=out / "synthetic-only.html",
    metadata_path=out / "synthetic-only.json",
    parser_version="jobinja-detail-v2",
    parse_status="parsed",
    fields={
        "title": "Technical team member",
        "description": (
            "Join our technical team. Detailed work scope will be discussed at interview."
        ),
        "language": "en",
    },
)

service = build_market_membership_service(settings)
provider = service._provider


class Recorder:
    def __init__(self):
        self.calls = 0
        self.job = None

    @property
    def identity(self):
        return provider.identity

    def classify(self, payload):
        self.calls += 1
        (out / f"{self.job}-input.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2)
        )
        decision = provider.classify(payload)
        (out / f"{self.job}-decision.json").write_text(
            decision.model_dump_json(indent=2)
        )
        return decision


recorder = Recorder()
service._provider = recorder
expected = {
    "ta9l": "core_match",
    "tG9K": "core_match",
    "tGM0": "adjacent_match",
    "t4jp": "excluded",
    "tmBK": "excluded",
    "t4qV": "excluded",
    "tmyX": "excluded",
    job_id: "uncertain",
}
report = {
    "head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    "started_at": now.isoformat(),
    "model": recorder.identity,
    "refresh_after_hours": 2160,
    "scope": "isolated historical source evidence; seven real jobs plus one synthetic sparse case",
    "results": [],
}
print("OUTPUT", out, flush=True)

for job, disposition in expected.items():
    recorder.job = job
    started = time.monotonic()
    row = {"job": job, "expected": disposition, "synthetic": job == job_id}
    try:
        evidence = service._evidence(definition.id, job, 2160, enrich=True)
        row["dependencies"] = {
            "source": evidence.candidate.job_detail_version_id,
            "translation": evidence.translation_id,
            "analysis": evidence.analysis_id,
        }
        row["evidence_characters"] = len(
            json.dumps(evidence.refs, ensure_ascii=False)
        )
        print(
            "START",
            job,
            row["dependencies"],
            "characters",
            row["evidence_characters"],
            flush=True,
        )
        result = service.qualify(
            target_definition_version_id=definition.id,
            source_job_id=job,
            refresh_after_hours=2160,
        )
        row["membership"] = asdict(result.membership)
        row["expected_match"] = result.membership.disposition == disposition
        calls = recorder.calls
        reused = service.qualify(
            target_definition_version_id=definition.id,
            source_job_id=job,
            refresh_after_hours=2160,
        )
        row["reuse_ok"] = (
            reused.outcome == "reused"
            and reused.membership.id == result.membership.id
            and calls == recorder.calls
        )
    except Exception as exc:
        row["error_type"] = type(exc).__name__
        row["error"] = str(exc)

    row["seconds"] = round(time.monotonic() - started, 2)
    report["results"].append(row)
    (out / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2)
    )
    print("RESULT", json.dumps(row, ensure_ascii=False), flush=True)

report["provider_calls"] = recorder.calls
report["completed_at"] = datetime.now(UTC).isoformat()
(out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
print("COMPLETE", out / "report.json", flush=True)
