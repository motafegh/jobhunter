"""Read-only presentation context for following frozen Market evidence into jobs."""

from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, urlencode

from fastapi import HTTPException, Request

from jobhunter.config import Settings
from jobhunter.market_role_family_report_service import MarketRoleFamilyReportService
from jobhunter.market_store import MarketStore
from jobhunter.market_workspace import MarketWorkspaceService


def snapshot_jobs(database_path: Path, snapshot_id: int) -> dict[str, dict]:
    """Resolve names from the exact source/translation versions pinned by a snapshot."""

    with closing(sqlite3.connect(database_path)) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT p.source_job_id, v.id AS detail_id, v.fields_json,
                   t.translated_fields_json, sm.analysis_artifact_id,
                   (SELECT MAX(current.id) FROM job_detail_versions AS current
                    WHERE current.job_posting_id = p.id) AS current_detail_id
            FROM market_corpus_snapshot_members AS sm
            JOIN job_detail_versions AS v ON v.id = sm.job_detail_version_id
            JOIN job_postings AS p ON p.id = v.job_posting_id
            LEFT JOIN job_translation_artifacts AS t
              ON t.id = sm.translation_artifact_id AND t.job_detail_version_id = v.id
            WHERE sm.snapshot_id = ?
            ORDER BY sm.id
            """,
            (snapshot_id,),
        ).fetchall()
    jobs = {}
    for row in rows:
        source = json.loads(row["fields_json"])
        english = json.loads(row["translated_fields_json"] or "{}")
        job_id = str(row["source_job_id"])
        title = english.get("title") or source.get("title") or job_id
        company = english.get("company") or source.get("company") or ""
        jobs[job_id] = {
            "title": title,
            "company": company,
            "label": f"{title} · {company}" if company else title,
            "detail_id": row["detail_id"],
            "analysis_id": row["analysis_artifact_id"],
            "source_changed": row["detail_id"] != row["current_detail_id"],
        }
    return jobs


def market_job_url(
    job_id: str, *, snapshot_id: int, report_id: int | None = None, finding: str = ""
) -> str:
    params: dict[str, str | int] = {"from_snapshot": snapshot_id}
    if report_id is not None:
        params["from_report"] = report_id
    if finding:
        params["from_finding"] = finding
    return f"/jobs/{quote(job_id, safe='')}?{urlencode(params)}"


@dataclass(frozen=True)
class MarketJobOrigin:
    snapshot_id: int
    return_url: str
    label: str
    job: dict
    job_url: str

    @property
    def query(self) -> str:
        return self.job_url.partition("?")[2]


def job_origin(
    settings: Settings,
    job_id: str,
    *,
    snapshot_id: int | None,
    report_id: int | None,
    finding: str,
) -> MarketJobOrigin | None:
    """Accept identified local objects only; never accept an arbitrary return URL."""

    if snapshot_id is None and report_id is None:
        return None
    anchors = {"requirements", "responsibilities", "members"}
    if report_id is not None:
        report = MarketRoleFamilyReportService(settings).get_report(report_id)
        if report is None:
            raise HTTPException(404, "Originating Market report not found")
        if snapshot_id is not None and snapshot_id != report.snapshot_id:
            raise HTTPException(400, "Report and snapshot context do not match")
        snapshot_id = report.snapshot_id
        path = f"/market/reports/{report_id}"
        label = f"Back to report #{report_id}"
        anchors = {"findings"}
        for prefix, field in (
            ("observation", "overall_observations"),
            ("work", "work_clusters"),
            ("subfamily", "possible_role_subfamilies"),
            ("specialty", "specialty_candidates"),
        ):
            anchors.update(
                f"{prefix}-{index + 1}" for index in range(len(report.report.get(field, [])))
            )
    else:
        if MarketStore(settings.database_path).get_snapshot(snapshot_id) is None:
            raise HTTPException(404, "Originating Market snapshot not found")
        path = f"/market/snapshots/{snapshot_id}"
        label = f"Back to snapshot #{snapshot_id}"
    assert snapshot_id is not None
    jobs = snapshot_jobs(settings.database_path, snapshot_id)
    if job_id not in jobs:
        raise HTTPException(404, "Job does not belong to the originating Market snapshot")
    if finding and finding not in anchors:
        raise HTTPException(400, "Unknown Market finding")
    return MarketJobOrigin(
        snapshot_id=snapshot_id,
        return_url=path + (f"#{finding}" if finding else ""),
        label=label,
        job=jobs[job_id],
        job_url=market_job_url(
            job_id, snapshot_id=snapshot_id, report_id=report_id, finding=finding
        ),
    )


def request_origin(settings: Settings, job_id: str, request: Request) -> MarketJobOrigin | None:
    """Carry the same validated context into the existing job-understanding pages."""

    params = request.query_params
    try:
        snapshot_id = int(params["from_snapshot"]) if "from_snapshot" in params else None
        report_id = int(params["from_report"]) if "from_report" in params else None
    except ValueError as exc:
        raise HTTPException(422, "Market context IDs must be integers") from exc
    return job_origin(
        settings,
        job_id,
        snapshot_id=snapshot_id,
        report_id=report_id,
        finding=params.get("from_finding", ""),
    )


def overview_intelligence(settings: Settings) -> dict:
    """Reuse the existing workspace selection and accepted-report read path."""

    state = MarketWorkspaceService(settings).state()
    snapshot = state.selected_snapshot
    report = (
        MarketRoleFamilyReportService(settings).latest_accepted_report(snapshot.id)
        if snapshot is not None
        else None
    )
    return {"target": state.selected_target, "snapshot": snapshot, "report": report}
