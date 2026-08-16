from __future__ import annotations

import json
from pathlib import Path

from jobhunter.public_corpus_cli import main


def test_status_distinguishes_discovered_jobs_from_fetched_details(
    tmp_path: Path,
    capsys,
) -> None:
    output_dir = tmp_path / "corpus"
    output_dir.mkdir()
    (output_dir / "manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "jobhunter-public-corpus-v1",
                "counts": {
                    "jobs": 2,
                    "sources": 2,
                    "english_projections": 1,
                    "p16_english": 0,
                    "p16_original": 0,
                    "capabilities": 0,
                },
                "jobs": [
                    {
                        "source_job_id": "with-detail",
                        "job_detail_version_id": 7,
                    },
                    {
                        "source_job_id": "discovered-only",
                        "job_detail_version_id": None,
                    },
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    assert main(["status", "--output-dir", str(output_dir)]) == 0

    output = capsys.readouterr().out
    assert "Known/discovered jobs: 2" in output
    assert "Fetched/parsed job details: 1" in output
    assert "English projections: 1" in output


def test_status_handles_manifest_without_job_list(tmp_path: Path, capsys) -> None:
    output_dir = tmp_path / "corpus"
    output_dir.mkdir()
    (output_dir / "manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "jobhunter-public-corpus-v1",
                "counts": {"jobs": 0},
            }
        ),
        encoding="utf-8",
    )

    assert main(["status", "--output-dir", str(output_dir)]) == 0
    assert "Fetched/parsed job details: 0" in capsys.readouterr().out
