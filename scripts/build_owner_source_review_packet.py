# ruff: noqa: E501  # self-contained inline CSS/JS keeps offline reviewer HTML portable
"""Generate a local-only, source-first owner audit package with NO model answers.

Use an immutable, isolated real-job cohort. This script creates offline HTML
that displays original employer description and separate job-board metadata,
then downloads the owner's annotations locally as JSON. There is no network
fetch, model invocation, production database write or automatic acceptance.

Run from JobHunter repository root:
  python scripts/build_owner_source_review_packet.py \
    --database data/local-acceptance/current-real-ads-2026-11-12/data/current-cohort.sqlite3 \
    --cohort data/local-acceptance/current-real-ads-2026-11-12/private-frozen-cohort.json \
    --jobs tNhZ tMps tNDx tMjm \
    --out data/local-acceptance/owner-audit-2026-11-13/packet-a
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import sqlite3
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit

from jobhunter.translation_store import TranslationStore

PACKET_VERSION = "jobhunter-owner-source-only-review-v1"
CSS = """
:root{--ink:#15263d;--muted:#54657c;--border:#cbd5e1;--accent:#2463a8;--soft:#eef4fc}
*{box-sizing:border-box}
body{font:16px/1.55 system-ui,-apple-system,'Segoe UI',sans-serif;background:#f5f7fb;color:var(--ink);
margin:0}
main{max-width:1000px;margin:2rem auto;padding:0 20px 5rem}
h1{font-size:1.9rem;margin:.2rem 0}
h2{font-size:1.45rem;margin:0 0 .5rem}
p,li{max-width:85ch}
small,.muted{color:var(--muted)}
header,article,.instructions{background:#fff;border:1px solid var(--border);
border-radius:13px;padding:24px;margin:0 0 22px;box-shadow:0 2px 10px #193f7010}
.case-index{display:inline-block;font-size:13px;font-weight:700;color:var(--accent);letter-spacing:.04em}
.meta{display:flex;gap:12px;flex-wrap:wrap;margin:.5rem 0 1rem}
.meta span{padding:4px 8px;background:var(--soft);border-radius:6px;font-size:13px}
a{color:var(--accent);overflow-wrap:anywhere}
pre.source{white-space:pre-wrap;overflow-wrap:anywhere;unicode-bidi:plaintext;direction:rtl;
font:16px/1.9 'Tahoma','Vazirmatn',sans-serif;
background:#fafbfe;border:1px solid var(--border);padding:20px;border-radius:9px;max-height:650px;overflow:auto}
.label{font-weight:700;margin:.9rem 0 .25rem}
.review-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:15px}
textarea,select,input[type=text]{width:100%;padding:12px;border:1px solid var(--border);
border-radius:7px;background:#fff;color:var(--ink);font:inherit}
textarea{min-height:100px;resize:vertical}
.field{display:block}
.field>span{display:block;font-weight:600;margin-bottom:6px}
fieldset{border:1px solid var(--border);border-radius:9px;padding:15px;margin:1rem 0}
legend{font-weight:600}
button{cursor:pointer;border:0;border-radius:9px;background:var(--accent);color:white;
font:600 16px system-ui;padding:13px 20px}
button:focus-visible,textarea:focus-visible,select:focus-visible{outline:3px solid #9cccff}
footer{position:sticky;bottom:0;background:#fff;border-top:1px solid var(--border);padding:16px;
display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:15px}
code{font-size:13px;background:#f0f3f9;padding:3px 5px;border-radius:4px;overflow-wrap:anywhere}
.note{border-left:4px solid #dbac38;padding:9px 13px;background:#fff9ec}
@media(prefers-color-scheme:dark){:root{--ink:#e1e8f4;--muted:#adb9cd;--border:#3f526b;--soft:#28384b}
body{background:#141d2a}header,article,.instructions,footer,textarea,select,input[type=text]{background:#1b2a3d}
pre.source{background:#152235}.note{background:#332b1a}code{background:#2a3a4c}}
@media print{footer{display:none}pre.source{max-height:none}article{break-before:page}body{background:white}}
"""
SCRIPT = """
'use strict';
const packet = document.body.getAttribute('data-packet');
function exportAnswers(){
  const answers = {};
  document.querySelectorAll('article[data-job-id]').forEach(card=>{
    const job=card.getAttribute('data-job-id');
    const values={};
    card.querySelectorAll('[data-answer]').forEach(control=>{
      values[control.getAttribute('data-answer')]=control.value;
    });
    answers[job]=values;
  });
  const out={
    contract:'jobhunter-owner-pass-a-response-v1',
    packet_id:packet,
    completed_at_utc:new Date().toISOString(),
    reviewer:'owner_manual_review',
    blind_phase:'A_source_only',
    model_results_exposed:false,
    answers
  };
  const file=new Blob([JSON.stringify(out,null,2)+'\\n'],{type:'application/json'});
  const link=document.createElement('a');
  const url=URL.createObjectURL(file);
  link.href=url;link.download=packet+'_PASS_A_RESPONSES.json';link.style.display='none';
  document.body.appendChild(link);link.click();link.remove();
  setTimeout(()=>URL.revokeObjectURL(url),1500);
  document.getElementById('saved').textContent='Response file generated. Save it and return the JSON for reconciliation.';
}
document.getElementById('save').addEventListener('click',exportAnswers);
"""


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _e(value: object) -> str:
    return html.escape(str(value), quote=True)


def _case_html(entry: dict, source_fields: dict, ordinal: int, count: int) -> str:
    jid = entry["job_id"]
    job = _e(jid)
    title = _e(source_fields.get("title") or entry.get("title_observed") or jid)
    original = _e(source_fields["description"])
    skills = source_fields.get("skills")
    skill_text = " | ".join(x for x in skills if isinstance(x, str)) if isinstance(skills, list) else ""
    parsed = urlsplit(str(entry.get("canonical_url") or ""))
    if (
        parsed.scheme != "https"
        or parsed.hostname != "jobinja.ir"
        or parsed.username is not None
        or parsed.password is not None
    ):
        raise ValueError("Owner-review external source URL is not an approved Jobinja page")
    meta = "".join(
        f"<span>{_e(label)}: {_e(source_fields.get(key) or 'unknown')}</span>"
        for key, label in (
            ("minimum_experience", "Board experience"),
            ("education", "Board education"),
            ("employment_type", "Board employment"),
            ("location", "Board location"),
        )
    )
    fields = (
        ("main_duties", "Which explicit duties would the employee actually perform?"),
        ("mandatory_requirements", "Which qualifications are clearly mandatory?"),
        ("preferred_optional", "Which qualifications or skills are preferred / optional?"),
        ("alternatives", "Are there alternative paths, ranges or OR conditions?"),
        ("arrangements_context", "Which terms are arrangements, application instructions or context—not technical requirements?"),
        ("unsupported_unknown", "What is ambiguous, missing, or not established by the source?"),
        ("evidence_quote", "Source evidence supporting the most important distinction (short quote)."),
        ("notes", "Other corrections or observations."),
    )
    inputs = []
    for key, label in fields:
        rows = 3 if key not in ("notes", "alternatives") else 2
        inputs.append(
            f'<label class="field"><span>{_e(label)}</span>'
            f'<textarea rows="{rows}" data-answer="{_e(key)}" '
            f'placeholder="Write your independent source assessment..."></textarea></label>'
        )
    return f"""
<article data-job-id="{job}">
  <span class="case-index">SOURCE CASE {ordinal}/{count} — {job}</span>
  <h2>{title}</h2>
  <div class="meta">{meta}</div>
  <p><strong>Archived source:</strong> <a href="{_e(entry['canonical_url'])}"
     target="_blank" rel="noopener noreferrer">View original public vacancy</a></p>
  <p><small>Frozen source SHA-256: <code>{_e(entry['semantic_sha256'])}</code>.
     Fetched at: {_e(entry['fetched_at'])}. The original below is the retained
     parsed employer description from this exact snapshot, not the live page.</small></p>
  <h3>Original employer description</h3>
  <pre class="source" dir="rtl" lang="fa">{original}</pre>
  <details><summary>Separate job-board skill tags (metadata; not automatically mandatory)</summary>
    <p dir="auto">{_e(skill_text or '(none listed)')}</p></details>
  <p class="note">Judge independently from the original wording. Do not assume a title,
     a site skill tag, or nearby text makes a skill mandatory.</p>
  <fieldset><legend>Your source-only assessment</legend>
    <label class="field"><span>How confidently can you interpret this posting?</span>
      <select data-answer="confidence">
      <option value="">Choose...</option>
      <option value="clear">Clear source evidence</option>
      <option value="partly_unclear">Partly unclear</option>
      <option value="cannot_determine">Cannot determine from source</option>
      </select></label>
    <div class="review-grid">{''.join(inputs)}</div>
  </fieldset>
</article>"""


def build_packet(
    database: Path, cohort_file: Path, jobs: tuple[str, ...], packet_id: str
) -> tuple[bytes, dict]:
    """Create a self-contained, blind Pass A HTML in memory, before writing."""
    entries = json.loads(cohort_file.read_text())
    by_id = {e["job_id"]: e for e in entries}
    if len(by_id) != len(entries) or not 1 <= len(jobs) <= 5:
        raise ValueError("Review packet must select one to five unique source cases")
    if len(jobs) != len(set(jobs)) or any(j not in by_id for j in jobs):
        raise ValueError("Unknown or duplicate review case")
    with tempfile.TemporaryDirectory(prefix="jobhunter-owner-blind-") as directory:
        snap = Path(directory) / "cohort.sqlite3"
        with (
            sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True) as source,
            sqlite3.connect(snap) as copied,
        ):
            source.backup(copied)
            if copied.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("Source integrity failed")
            if copied.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("Source foreign keys failed")
        store = TranslationStore(snap)
        cases = []
        fragments = []
        for i, job in enumerate(jobs, start=1):
            entry = by_id[job]
            source = store.latest_source_version(job)
            if (
                source is None
                or source.job_detail_version_id != entry["detail_id"]
                or source.semantic_sha256 != entry["semantic_sha256"]
            ):
                raise ValueError("Current parsed detail version does not match source freeze")
            fields = source.fields
            if not isinstance(fields.get("description"), str):
                raise ValueError("Original description is missing")
            fragments.append(_case_html(entry, fields, i, len(jobs)))
            cases.append({
                "job_id": job,
                "source_url": entry["canonical_url"],
                "fetched_at_utc": entry["fetched_at"],
                "source_semantic_sha256": source.semantic_sha256,
                "source_detail_version_id": source.job_detail_version_id,
                "description_sha256": _sha(fields["description"].encode("utf-8")),
                "exposed_development_case": True,
                "pass_a_model_output_included": False,
            })
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>JobHunter — independent source-only review</title>
<style>{CSS}</style></head>
<body data-packet="{_e(packet_id)}"><main>
<header><div class="case-index">JOBHUNTER • OWNER AUDIT • PASS A</div>
<h1>Original-source review</h1>
<p>This package contains <strong>only retained original Persian vacancies</strong>
and distinct job-board metadata. It intentionally contains no JobHunter analysis,
translation, assistant verdict, grading key or expected answer.</p>
<p><strong>Procedure:</strong> Read the original employer text. Write your own account
of the actual duties, required and optional qualifications, alternatives and
unknowns. Use source wording as evidence. You can leave fields blank or choose
Cannot determine. When finished, select <strong>Save Pass A responses</strong> and
share the downloaded JSON for a frozen independent review.</p>
<p class="note">Do not open the model-comparison packet until your Pass A response
has been saved. This is an exposed development case, not a protected holdout.</p>
<small>Packet: {_e(packet_id)} · Generated from immutable source snapshots · No cloud/model
calls · No automatic promotion</small>
</header>
{''.join(fragments)}
</main><footer>
<button type="button" id="save">Save Pass A responses (JSON)</button>
<span class="muted" id="saved" aria-live="polite">Offline file. No answers are sent to a server.</span>
</footer>
<script>{SCRIPT}</script></body></html>
"""
    result = page.encode("utf-8")
    manifest = {
        "contract": PACKET_VERSION,
        "packet_id": packet_id,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "case_count": len(cases),
        "source_only_html_sha256": _sha(result),
        "blind_phase": "A_source_only",
        "model_output_included": False,
        "pass_b": "withheld_until_pass_a_frozen",
        "human_review_completed": False,
        "review_answers_file_expected": packet_id + "_PASS_A_RESPONSES.json",
        "privacy": "local_only_original_job_text_not_committed",
        "cases": cases,
    }
    return result, manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True, type=Path)
    parser.add_argument("--cohort", required=True, type=Path)
    parser.add_argument("--jobs", required=True, nargs="+")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--packet-id", default="JH-OWNER-A1-20261113")
    args = parser.parse_args()
    root = Path.cwd().resolve()
    if not (root / "AGENTS.md").is_file():
        raise RuntimeError("Run from JobHunter repository root")
    output = args.out.resolve()
    if not output.is_relative_to(root / "data/local-acceptance"):
        raise ValueError("Review packet raw source must stay inside ignored local data")
    if output.exists():
        raise FileExistsError("Refusing to overwrite a prior review packet")
    if not args.packet_id.isascii() or not all(c.isalnum() or c == "-" for c in args.packet_id):
        raise ValueError("Invalid packet identity")
    page, manifest = build_packet(
        args.database, args.cohort, tuple(args.jobs), args.packet_id
    )
    output.mkdir(parents=True)
    (output / "PASS_A_SOURCE_ONLY.html").write_bytes(page)
    (output / "PACKET_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
    (output / "README.txt").write_text(
        "JobHunter independent owner review — Pass A only.\n"
        "Open PASS_A_SOURCE_ONLY.html offline in your browser.\n"
        "Read the original Persian postings, answer the source-only questions,\n"
        "and click Save Pass A responses (JSON). Return the resulting JSON.\n"
        "The model-comparison pass will be made available only after Pass A is saved.\n"
        "Neither a candidate verdict nor automatic approval is included.\n"
    )
    print("local_review_packet:", output.relative_to(root))
    print("cases:", len(manifest["cases"]))
    print("pass_b:", manifest["pass_b"])
    print("original_text_committed:", False)


if __name__ == "__main__":
    main()
