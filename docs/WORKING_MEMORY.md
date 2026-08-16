# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-16  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** public corpus OPERATIONALLY CLOSED; heterogeneous live semantic validation is active next

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

The complete repository-safe public-corpus projection is now implemented, populated from the real local database, verified, committed, remotely inspected, and operationally closed.

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

## 6. Public corpus — IMPLEMENTED / POPULATED / OPERATIONALLY CLOSED

Architecture:

```text
local SQLite
→ runtime/history authority

corpus/
→ complete current repository-safe projection of known public Jobinja state

review-snapshots/
→ curated semantic-review evidence
```

Contract:

```text
jobhunter-public-corpus-v1
```

Real corpus coverage after backfill from `data/jobhunter.sqlite3`:

```text
Known/discovered Jobinja jobs: 344
Fetched/parsed job details:     43
English projections:            33
English P1.6:                    2
Original P1.6:                   0
Capabilities:                    2
Per-job stage files:           381
Corpus size:                  ~3.6 MiB
```

Important interpretation:

```text
344 known/discovered jobs
!=
344 fully fetched advertisements
```

A discovery-only job remains a valid corpus identity with `current_detail: null`. Only the 43 entries with fetched/parsed current detail are eligible for downstream semantic-review selection.

Public-safety scan over actual corpus data passed: no raw model request/response protocol, evidence paths, SQLite paths, `/home/` paths, `/mnt/c/` paths, secrets, or future private state were exported.

Accepted anchor dependency proof:

```text
tG9K
source detail:       40
translation:         33
P1.6:                36
Capability:          11
Capability → P1.6:   36
Capability → trans:  33

t4jp
source detail:       41
translation:         34
P1.6:                37
Capability:          12
Capability → P1.6:   37
Capability → trans:  34
```

Full corpus publication commit:

```text
15dbfa3636bbf7118de79683beec3e7ac4a6359d
data: publish complete public job corpus
```

Remote GitHub inspection confirmed the manifest, job directories, contracts, and accepted anchors. Publication CI 902 passed Ruff, full pytest, and warnings-as-errors.

The CLI was then hardened so corpus coverage reports `Known/discovered jobs` and `Fetched/parsed job details` separately. Hardening head `91f1d7edc1cebd2fd8c1fb01b4e2b04163807153` passed CI 904. This was reporting-only; no corpus data regeneration was required.

Permanent corpus rules:

1. SQLite remains runtime/history authority.
2. `corpus/` is the version-controlled current public projection.
3. Discovery-only identities and fetched/parsed details remain explicitly distinguishable.
4. Mutating JobHunter workflows refresh the local corpus only after durable success.
5. `jobhunter-corpus verify` is the deterministic DB↔corpus integrity gate.
6. Git commit/push remains explicit and is never part of runtime correctness.
7. Future personal/private evidence must never enter the public corpus.
8. Remote corpus inspection can now drive role selection and later public-data analysis without local SQLite access.

Detailed closure record:

```text
docs/working-memory/2026-08-16_PUBLIC_CORPUS_OPERATIONAL_CLOSURE.md
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
Public corpus                        OPERATIONALLY CLOSED / REMOTELY AVAILABLE
Known/discovered jobs                344
Fetched/parsed detail jobs           43
English projection jobs              33
Current P1.6 jobs                      2
Current Capability jobs                2
Heterogeneous role review            ACTIVE NEXT GATE
Phase 2                              BLOCKED
```

## 8. Exact next action

Use the remote corpus to choose materially different **fetched/parsed** jobs for heterogeneous live semantic validation:

```text
1. Python/software role
2. network/security role
3. operations/platform/DevOps role
```

For each role:

1. select a job with non-null current detail from the repository corpus;
2. inspect original source fields and current English projection state;
3. generate/reuse current English P1.6 v20 through the normal path;
4. generate/reuse current Capability v9 through the normal path;
5. review factual coverage, provenance, strength, depth, role-level constraints, grouping, and source truth;
6. reject fabricated responsibilities, prerequisites, ownership, lifecycle, architecture, autonomy, or mandatory strength;
7. distinguish repeatable deterministic defects from acceptable model variation/local-model limitations;
8. convert repeatable deterministic defects into tests;
9. avoid contract changes for harmless non-authoritative wording differences.

Do not rerun `tG9K` or `t4jp` Capability unless a dependency changes or a repeatable correctness defect requires explicit re-evaluation.

## 9. Relevant records

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_DENSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_SPARSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_PUBLIC_PROMOTION.md
docs/working-memory/2026-08-16_PUBLIC_CORPUS_PROJECTION.md
docs/working-memory/2026-08-16_PUBLIC_CORPUS_OPERATIONAL_CLOSURE.md
corpus/README.md
```
