# JobHunter Review Snapshots

`review-snapshots/` contains deliberately exported, reviewable JSON snapshots of selected Jobinja
jobs. These files are **not** the JobHunter SQLite database and are not runtime inputs.

## Why this exists

The live database stays local and ignored by Git because it is binary, changes frequently, may
later contain private/personal state, and is awkward to diff or review. A review snapshot instead
captures the current logical intelligence chain in stable UTF-8 JSON so another reviewer or AI
assistant can inspect quality directly from the repository.

## Create or refresh one snapshot

```bash
source .venv/bin/activate
jobhunter jobs snapshot tG9K
```

The standalone `jobhunter-review-snapshot tG9K` entry point is also available.

Default output:

```text
review-snapshots/jobs/tG9K.json
```

Then review the diff and intentionally publish it:

```bash
git diff -- review-snapshots/jobs/tG9K.json
git add review-snapshots/jobs/tG9K.json
git commit -m "review: update tG9K intelligence snapshot"
git push origin main
```

After that, a repository reviewer can inspect the complete selected chain without asking for a
manual copy/paste of the browser pages.

## Included

A snapshot may contain the current:

- public Jobinja source fields and source-version provenance;
- English projection and translation identity/provenance;
- English P1.6 semantic analysis;
- original-language semantic analysis when it exists;
- Capability Intelligence when it matches the current English-analysis dependency;
- Role Capability Blueprint when it matches the current Capability Intelligence dependency;
- model, prompt/schema version, artifact ID, timestamp, and dependency IDs needed for audit.

## Deliberately excluded

Snapshots do not export:

- SQLite/WAL/SHM files;
- raw HTML contents;
- LM Studio raw responses;
- model request bodies/system prompts;
- API tokens or local configuration;
- operation histories/debug logs;
- candidate/private personal data or future user notes.

The JobHunter repository is public. Only commit snapshots whose source material is appropriate to
publish. The current exporter is intentionally scoped to public Jobinja job records and derived
analysis of those records.

## Dependency status

The `status` object is important. A stale Capability or Blueprint artifact is not exported as if it
were current. For example, after a new English-analysis contract is introduced, regenerate the
English analysis and Capability/Blueprint before expecting all `*_is_current_chain` fields to be
true.
