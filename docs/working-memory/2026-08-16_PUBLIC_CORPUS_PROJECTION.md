# Public Corpus Projection — Implementation Record

**Date:** 2026-08-16  
**Branch:** `main`  
**Status:** IMPLEMENTED / DETERMINISTIC CI PASS / LOCAL BACKFILL + REMOTE PUBLISH PENDING

## 1. Why this increment exists

JobHunter's complete acquired job corpus previously lived only in the local runtime database and evidence store:

```text
data/jobhunter.sqlite3
data/evidence/
```

Only two curated `review-snapshots/jobs/*.json` files were version-controlled. That prevented remote review of the full already-acquired public job pool and made heterogeneous role selection depend on local SQL access.

The repository owner explicitly wants public vacancy data and successfully completed public processing stages available both locally and remotely.

## 2. Architecture decision

Do **not** commit the live SQLite database.

Instead:

```text
SQLite
→ operational/runtime authority

corpus/
→ complete deterministic repository-safe public projection

review-snapshots/
→ selected semantic acceptance evidence
```

Public corpus contract:

```text
jobhunter-public-corpus-v1
```

This keeps Git data readable/diffable while preserving SQLite as the application's structured runtime state.

## 3. Repository layout

```text
corpus/
├── README.md
├── manifest.json
└── jobs/
    └── <source-job-id>/
        ├── source.json
        ├── english-projection.json
        ├── p16-english.json
        ├── p16-original.json
        └── capability.json
```

Every discovered Jobinja job appears in the manifest and receives `source.json`. Discovery-only jobs may have `current_detail: null`.

Optional derived files exist only when a current artifact exists for the current source dependency under the current public contract/model selection.

## 4. Exported public state

### Source

`source.json` includes:

- stable source job ID;
- company slug and canonical public URL;
- first/last seen and lifecycle state;
- current detail-version identity;
- fetch/status/hash/parser/parse metadata;
- complete deterministic `jobinja-detail-v2` fields;
- original Persian/English text as UTF-8 JSON.

Machine-local `evidence_path` and `metadata_path` are intentionally not exported.

### English projection

`english-projection.json` includes:

- translation artifact ID;
- exact source detail/hash dependency;
- source/target languages;
- provider/model/schema identity;
- translation hash/counts;
- translated fields/document;
- segment provenance.

### P1.6

`p16-english.json` and `p16-original.json` include:

- analysis artifact ID;
- source/translation dependencies;
- model/prompt/schema identity;
- durable analysis payload.

Raw request bodies and raw model protocol responses are excluded.

### Capability

`capability.json` includes:

- Capability artifact ID;
- exact source/translation/P1.6 dependencies;
- model/prompt/schema identity;
- durable Capability intelligence.

Raw request bodies and raw model protocol responses are excluded.

## 5. Manifest

`corpus/manifest.json` is the lightweight whole-corpus index. It records:

- public corpus schema;
- current P1.6/Capability contract identities;
- total jobs/stage coverage counts;
- per-job title/company/URL/lifecycle/language;
- current source version/parse status/hash;
- per-stage presence;
- current artifact IDs.

This allows remote role-family selection without opening every job file.

## 6. Current-state semantics

The repository corpus represents the **current public projection**, not a duplicate operational history database.

When a new source semantic version becomes current:

```text
source.json updates
old translation/P1.6/Capability files become stale
→ exporter removes them
→ they reappear only after current downstream stages succeed
```

Git history preserves previously committed corpus states.

The local SQLite database remains the richer operational/history authority.

## 7. Privacy and exclusion boundary

Never export into the public corpus:

```text
SQLite / WAL / SHM
raw HTML evidence
machine-local evidence paths
LM Studio request bodies
raw LM Studio responses
system prompts
secrets / API tokens
logs / debug histories
local configuration
future personal evidence/profile/application/outcome data
```

The fact that future private state may coexist in local SQLite does not authorize exporting it. Any public-corpus schema expansion requires explicit review of this boundary.

## 8. Implementation

New module:

```text
src/jobhunter/public_corpus.py
```

Core operations:

```text
export_public_corpus(...)
export_public_job(...)
verify_public_corpus(...)
```

Properties:

- deterministic sorted UTF-8 JSON;
- atomic file replacement;
- complete manifest rebuild;
- optional stale-job pruning;
- stale downstream stage removal;
- exact DB↔corpus verification;
- no network/model calls.

New standalone CLI:

```text
src/jobhunter/public_corpus_cli.py
```

Installed command:

```bash
jobhunter-corpus export
jobhunter-corpus verify
jobhunter-corpus status
```

## 9. Automatic local synchronization

`pyproject.toml` now routes the normal `jobhunter` executable through:

```text
jobhunter.app_entrypoint:main
```

The wrapper preserves the established CLI and refreshes `corpus/` after durable mutating workflows:

```text
jobhunter run
jobhunter jobinja discover
jobhunter jobinja fetch
jobhunter jobinja sync
jobhunter translations run
jobhunter jobs analyze
jobhunter jobs capability
```

Return-code behavior:

- readiness/config/argument failure (`2`) does not sync;
- success (`0`) syncs;
- partial/operational failure (`1`) also syncs because durable partial successes may exist;
- if local operation succeeded but corpus projection fails, SQLite remains durable and command becomes non-zero so divergence is visible.

No automatic Git commit/push occurs.

## 10. Browser integration

The browser's serialized `WebOperationManager` now supports an `after_success` hook.

`jobhunter-app` installs a corpus projection callback on the shared manager. This covers normal background browser operations, including the separately registered Capability route.

Order:

```text
web action
→ durable local service work
→ public corpus projection
→ operation terminal success
```

If projection fails after durable local work, the operation is visibly marked failed with a public-corpus synchronization error. Durable SQLite state is not rolled back.

## 11. Regression coverage

Tests cover:

- Persian UTF-8 source preservation;
- current source/translation/P1.6/Capability chain export;
- exact artifact/dependency identities;
- exclusion of local evidence paths;
- exclusion of raw request/model protocol fields;
- manifest stage/count accuracy;
- DB↔corpus verification PASS;
- tamper detection;
- stale downstream cleanup after source change;
- CLI mutating/read-only synchronization routing;
- synchronization failure visibility;
- browser post-operation synchronization;
- browser projection-failure visibility.

Deterministic implementation gate:

```text
CI 893
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

## 12. Operational backfill/publish gate

The code cannot populate the real repository corpus remotely because the authoritative SQLite database is local to the repository owner.

Required one-time local backfill after pulling this implementation:

```bash
cd ~/projects/jobhunter
git pull --ff-only origin main
python -m pip install -e '.[dev]'

jobhunter-corpus export
jobhunter-corpus verify
jobhunter-corpus status

git status --short
git diff -- corpus/
```

After counts/content look correct:

```bash
git add corpus/
git commit -m "data: publish JobHunter public corpus"
git push origin main
```

Then remotely verify the manifest/job directories from GitHub.

Only after that proof call the public corpus operationally available and resume heterogeneous Python/software → network/security → operations/platform/DevOps selection using the full remote dataset.
