# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-16  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** public corpus projection implemented + CI PASS; local full-corpus backfill/publish verification pending before heterogeneous live review

## 1. Exact current point

English P1.6 v20/v5 is fully promoted and operationally verified:

```text
tG9K → P1.6 artifact 36 → ACCEPTED / CURRENT
t4jp → P1.6 artifact 37 → ACCEPTED / CURRENT
```

Capability v9 is fully promoted through the normal public path:

```text
tG9K → Capability artifact 11 → ACCEPTED / CURRENT
t4jp → Capability artifact 12 → ACCEPTED WITH ACCEPTABLE DIFFERENCES / CURRENT
```

Public/current Capability contract:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

Normal `jobhunter jobs capability` commands reuse artifacts 11/12. Review Snapshot marks both artifacts current against P1.6 artifacts 36/37. Blueprint remains `blueprint_current=False`, deferred/non-authoritative, and pinned to historical Capability v7 semantics.

Before heterogeneous review, JobHunter now has a first-class complete repository-safe public-corpus projection:

```text
local SQLite runtime authority
→ corpus/ complete current public projection
→ Git remote accessibility after intentional commit/push
```

The implementation is deterministic-green. The remaining mini-gate is one local backfill from the owner's real SQLite database, verification, commit/push, and remote inspection.

## 2. Repository workflow rule

JobHunter uses **main-only development** by default:

```text
current work → main
next work    → main
```

Do not create a new working branch unless the user explicitly changes this rule.

## 3. Current contracts

```text
parser:                     jobinja-detail-v2
translation:                lm-studio-translation-v2
English projection:         english-projection-v2
English P1.6 public:        job-analysis-english-v20 / job-analysis-v5
Original P1.6 public:       job-analysis-original-v9 / job-analysis-v4
Capability public/current:  job-capability-intelligence-v9 / job-capability-intelligence-v5
Capability v7 historical:   job-capability-intelligence-v7 / job-capability-intelligence-v4
Capability v8 historical:   job-capability-intelligence-v8 / job-capability-intelligence-v4
Blueprint deferred:         role-capability-blueprint-v6 / role-capability-blueprint-v5
Review Snapshot:            job-review-snapshot-v1
Public Corpus:              jobhunter-public-corpus-v1
```

## 4. P1.6 v20 — PROMOTED / CLOSED

Dense `tG9K` artifact 36:

```text
Requirements:      33
Responsibilities:  8
Role purpose:      0
Mechanical audit:  PASS
Semantic review:   PASS WITH ACCEPTABLE DIFFERENCE
```

Sparse `t4jp` artifact 37:

```text
Requirements:            8
Responsibilities:        0
Role purpose:            0
Mechanical audit:        PASS
Semantic non-regression: PASS
```

Normal P1.6 commands reuse artifacts 36/37.

## 5. Capability history and current state

### v7 — historical baseline / promoted-chain rebuild rejected

Historical accepted artifact 9 depends on old P1.6 artifact 29. Dense rebuilds against current P1.6 failed through source-link/index loss and then one-profile collapse with 22 capability requirements omitted. Do not reopen the v7 one-shot architecture.

### v8 — staged architecture proof / semantic reject

V8 staging mechanically reached 31/31 dense capability requirements and 8/8 responsibilities but remained semantically rejected because model prose inflated depth, ownership/lifecycle scope, and preferred/contextual facts.

### v9 — accepted / promoted / operationally closed

Final policy:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

Accepted/current artifacts:

```text
tG9K artifact 11
P1.6 dependency:                 36
Capability requirements:         31/31
Responsibilities:                8/8
Capability explicit depth:       5/5
All explicit depth:              6/6
Role-level indices:              [31, 32]
Disposition:                     ACCEPTED / CURRENT

t4jp artifact 12
P1.6 dependency:                 37
Capability requirements:         8/8
Responsibilities:                0/0
Capability explicit depth:       0/0
All explicit depth:              0/0
Role-level indices:              []
Disposition:                     ACCEPTED WITH ACCEPTABLE DIFFERENCES / CURRENT
```

Capability public promotion is operationally closed. No fresh Capability generation occurred during normal-path verification.

Detailed record:

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_PUBLIC_PROMOTION.md
```

## 6. Public corpus projection — IMPLEMENTED / LOCAL BACKFILL PENDING

Problem solved:

```text
before:
full fetched/processed public job corpus → local SQLite only
GitHub → only selected tG9K/t4jp review snapshots

after implementation:
SQLite → runtime authority
corpus/ → complete repository-safe current public projection
review-snapshots/ → curated acceptance evidence
```

Contract:

```text
jobhunter-public-corpus-v1
```

Layout:

```text
corpus/manifest.json
corpus/jobs/<job-id>/source.json
corpus/jobs/<job-id>/english-projection.json
corpus/jobs/<job-id>/p16-english.json
corpus/jobs/<job-id>/p16-original.json
corpus/jobs/<job-id>/capability.json
```

Behavior:

- every discovered Jobinja job appears in the manifest and gets `source.json`;
- original Persian/English parsed vacancy fields remain UTF-8;
- current translation/P1.6/Capability artifact and dependency identities are exported;
- raw model requests/responses, raw HTML, local evidence paths, secrets/logs/config, and future personal/private state are excluded;
- source change removes stale downstream stage files until rebuilt;
- full DB↔corpus verification is deterministic;
- normal mutating CLI commands synchronize after durable local work;
- completed browser background operations synchronize through the shared operation manager;
- projection failure is surfaced but does not roll back SQLite;
- JobHunter never auto-commits or auto-pushes Git.

Commands:

```bash
jobhunter-corpus export
jobhunter-corpus verify
jobhunter-corpus status
```

Implementation gate:

```text
CI 893
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

Detailed record:

```text
docs/working-memory/2026-08-16_PUBLIC_CORPUS_PROJECTION.md
```

## 7. Exact current state

```text
English P1.6 tG9K artifact 36       ACCEPTED / CURRENT
English P1.6 t4jp artifact 37       ACCEPTED / CURRENT
Capability v7 artifact 9            HISTORICAL / NON-CURRENT CHAIN
Capability v8 candidate              HISTORICAL / SEMANTIC REJECT
Capability v9 artifact 11           DENSE ACCEPTED / CURRENT
Capability v9 artifact 12           SPARSE ACCEPTED / CURRENT
Capability public route              v9/v5 / OPERATIONALLY VERIFIED
Blueprint                            DEFERRED / PINNED TO HISTORICAL v7 / NON-CURRENT
Public corpus implementation         COMPLETE / CI PASS
Public corpus real local backfill    PENDING
Public corpus remote publish proof   PENDING
Heterogeneous role review            NEXT AFTER CORPUS PUBLISH PROOF
Phase 2                              BLOCKED
```

## 8. Exact next action

The real corpus cannot be populated remotely because `data/jobhunter.sqlite3` exists only on the repository owner's machine.

Pull and reinstall once so the new console entrypoints are registered, then backfill:

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

Review the printed counts and corpus diff. If correct:

```bash
git add corpus/
git commit -m "data: publish JobHunter public corpus"
git push origin main
```

Then remotely inspect `corpus/manifest.json` and job directories and mark public-corpus operational availability closed.

After that, choose heterogeneous live roles from the complete remote corpus:

```text
1. Python/software
2. network/security
3. operations/platform/DevOps
```

Do not rerun `tG9K` or `t4jp` Capability unless a dependency changes or a repeatable correctness defect requires explicit re-evaluation.

## 9. Relevant records

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_DENSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_SPARSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_PUBLIC_PROMOTION.md
docs/working-memory/2026-08-16_PUBLIC_CORPUS_PROJECTION.md
corpus/README.md
```
