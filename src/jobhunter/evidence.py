"""Immutable local evidence writing for acquired public pages."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from jobhunter.sources import FetchedSearchPage


class EvidenceWriteError(RuntimeError):
    """Raised when an acquisition snapshot cannot be written safely."""


@dataclass(frozen=True, slots=True)
class EvidenceSnapshot:
    """References and integrity information for one saved HTTP snapshot."""

    content_path: Path
    metadata_path: Path
    content_sha256: str
    captured_at: datetime


def _safe_segment(value: str) -> str:
    ascii_part = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-._")[:40]
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:10]
    return f"{ascii_part or 'item'}-{digest}"


def _atomic_write(path: Path, content: bytes) -> None:
    temporary_path = path.with_name(f".{path.name}.tmp")
    try:
        temporary_path.write_bytes(content)
        os.replace(temporary_path, path)
    except OSError as exc:
        temporary_path.unlink(missing_ok=True)
        raise EvidenceWriteError(f"Could not write evidence file {path}: {exc}") from exc


class EvidenceStore:
    """Write raw acquisition content before downstream parsing."""

    def __init__(self, root: Path) -> None:
        self._root = root

    def write_jobinja_search_page(
        self,
        *,
        search_name: str,
        page_number: int,
        fetched_page: FetchedSearchPage,
        captured_at: datetime | None = None,
    ) -> EvidenceSnapshot:
        """Persist one raw Jobinja search page and a metadata sidecar."""

        timestamp = captured_at or datetime.now(timezone.utc)
        if timestamp.tzinfo is None:
            raise ValueError("captured_at must be timezone-aware")

        content_sha256 = hashlib.sha256(fetched_page.content).hexdigest()
        directory = self._root / "jobinja" / "search-pages" / _safe_segment(search_name)
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise EvidenceWriteError(
                f"Could not create evidence directory {directory}: {exc}"
            ) from exc

        timestamp_text = timestamp.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        stem = f"{timestamp_text}_p{page_number:04d}_{content_sha256[:12]}"
        content_path = directory / f"{stem}.html"
        metadata_path = directory / f"{stem}.json"

        metadata = {
            "source": "jobinja",
            "kind": "search_page",
            "search_name": search_name,
            "page_number": page_number,
            "captured_at": timestamp.astimezone(timezone.utc).isoformat(),
            "requested_url": fetched_page.requested_url,
            "final_url": fetched_page.final_url,
            "status_code": fetched_page.status_code,
            "headers": fetched_page.headers,
            "content_sha256": content_sha256,
            "content_bytes": len(fetched_page.content),
            "content_path": str(content_path),
        }

        _atomic_write(content_path, fetched_page.content)
        try:
            _atomic_write(
                metadata_path,
                json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True).encode(
                    "utf-8"
                ),
            )
        except EvidenceWriteError:
            content_path.unlink(missing_ok=True)
            raise

        return EvidenceSnapshot(
            content_path=content_path,
            metadata_path=metadata_path,
            content_sha256=content_sha256,
            captured_at=timestamp,
        )
