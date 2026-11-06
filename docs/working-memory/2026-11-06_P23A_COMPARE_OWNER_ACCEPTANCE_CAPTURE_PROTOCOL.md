# P2.3A /compare repeated-use assessment — capture protocol

**Status:** Review-only workstream; not P2.3 profile authorization or product acceptance.
**Base:** main commit `21f9d03398ad22e7cafaaa187a4d0381a4db3c75`.
**Branch:** `review/p23a-compare-usefulness-2026-11-06`.

## Goal

Test whether the existing bounded comparison view helps the owner understand
and contrast a small number of real accepted job postings, locate evidence,
and preserve factual-vs-interpretive distinctions.

This run deliberately does not acquire jobs, regenerate analyses, promote
Registry concepts, or write persistent capability profiles.

## Setup (WSL, repo root)

First check `git status --short`. If any unrelated tracked change exists,
preserve it and reconcile before switching branches. Do **not** reset, force
checkout, or blindly stash local work.

```bash
cd ~/projects/jobhunter
source .venv/bin/activate
git status --short
git fetch origin
git switch --track origin/review/p23a-compare-usefulness-2026-11-06
git pull --ff-only
```

If that branch is already checked out locally, simply use `git switch
review/p23a-compare-usefulness-2026-11-06` rather than creating another
tracking branch.

## Capture numeric evidence automatically

Use the **same populated config** as the normal application. On the
maintainer setup this was `jobhunter.toml`; substitute `config/local.toml`
only if that is the configuration containing the accepted runtime data.

```bash
python scripts/capture_p23a_comparison_review.py --config jobhunter.toml
python -m json.tool docs/working-memory/2026-11-06_p23a_compare_owner_usefulness/AUTO_METRICS.json
```

The capture makes a temporary SQLite online backup under ignored
`data/local-acceptance/`, reads its accepted/current comparison results
using the product's own shared read model, then deletes the temporary backup.
It does not persist profiles or call source/model services. It writes only:

- `AUTO_METRICS.json`: public fixed job IDs, literal filters, mechanical
  counts, availability flags, and generic error class if a scenario fails;
- `OWNER_REVIEW.md`: scenario links/questions and a template to record
  actual usability observations. Existing edits are preserved on rerun.

No titles, company names, source text, evidence excerpts, local paths, raw
model material, raw SQLite or runtime logs are exported.

## Owner visual/usefulness assessment

In another terminal, start the UI with the same configuration:

```bash
jobhunter-app --config jobhunter.toml
```

Open `http://127.0.0.1:8765/compare`, and use the four direct scenario
links in `OWNER_REVIEW.md`. For each, answer the specific question, follow
source evidence when needed, and record what helped, what failed, and which
new capability would genuinely make the workflow more useful.

Edit the review template:

```bash
code docs/working-memory/2026-11-06_p23a_compare_owner_usefulness/OWNER_REVIEW.md
```

Use `not measured` for time savings unless you actually measured the time
and can describe how. The script's automated counts are not evidence of
user comprehension, time savings, or product acceptance.

## Review and publish only the allowlisted files

Before pushing, inspect both files to ensure your **manual remarks do not
include sensitive local state**. This is a public repository.

```bash
git status --short
git diff -- docs/working-memory/2026-11-06_p23a_compare_owner_usefulness/
git add \
  docs/working-memory/2026-11-06_p23a_compare_owner_usefulness/AUTO_METRICS.json \
  docs/working-memory/2026-11-06_p23a_compare_owner_usefulness/OWNER_REVIEW.md
git diff --cached --stat
git diff --cached -- docs/working-memory/2026-11-06_p23a_compare_owner_usefulness/
git commit -m "Record owner P2.3A comparison usefulness observations"
git push -u origin review/p23a-compare-usefulness-2026-11-06
```

**Never** use `git add -A` for local acceptance evidence. Never commit
`data/`, any `*.sqlite3`, local screenshots, personal information, API
tokens, or raw source/model material. Screenshots require separate visual
privacy review before any public upload.

After pushing, review the branch evidence and then decide whether to accept
the small comparison slice, fix a specific usability defect, or authorize a
bounded follow-on semantic experiment. The evidence should not be merged
to `main` before the review disposition is recorded.
