# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-21  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** public corpus OPERATIONALLY CLOSED; heterogeneous live semantic validation ACTIVE; Python/software anchor `tmBK` awaiting rebuilt P1.6 review

## 1. Exact current point

English P1.6 v20/v5 is promoted/current and operationally verified on the accepted opposite-end anchors:

```text
tG9K → P1.6 artifact 36 → ACCEPTED / CURRENT
t4jp → P1.6 artifact 37 → ACCEPTED / CURRENT
```

Capability v9/v5 is promoted/current through the normal public path:

```text
tG9K → Capability artifact 11 → ACCEPTED / CURRENT
t4jp → Capability artifact 12 → ACCEPTED WITH ACCEPTABLE DIFFERENCES / CURRENT
```

Normal Capability commands reuse artifacts 11/12 on P1.6 artifacts 36/37. Review Snapshot marks both exact chains current. Blueprint remains `blueprint_current=False`, deferred/non-authoritative, and pinned to historical Capability v7 semantics.

The complete repository-safe public corpus is implemented, populated from the real local database, verified, committed, remotely inspected, and operationally closed.

Heterogeneous validation is now active. The first Python/software anchor is `tmBK` (Python Developer, source detail 44, English projection artifact 38). Its first persisted P1.6 artifact 38 was mechanically valid but semantically rejected because a deterministic depth canonicalizer propagated the first `Mastery` marker across unrelated `Familiarity`/`Sufficient knowledge` concepts. The rejected artifact must not feed Capability.

After that rejection, additional live rebuild attempts exposed two adjacent deterministic boundaries: `effectively use AI` is application wording rather than technical depth, and a positively represented coverage reference must not also remain redundantly excluded. Those cases are now hardened with regression tests on `main`. The next local action is a clean `tmBK` P1.6 rebuild under the current head followed by full semantic review.

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

## 4. P1.6 v20 — PROMOTED / PUBLIC CONTRACT CLOSED

Dense accepted `tG9K` artifact 36:

```text
Requirements:      33
Responsibilities:  8
Role purpose:      0
Mechanical audit:  PASS
Semantic review:   PASS WITH ACCEPTABLE DIFFERENCE
```

Sparse accepted `t4jp` artifact 37:

```text
Requirements:            8
Responsibilities:        0
Role purpose:            0
Mechanical audit:        PASS
Semantic non-regression: PASS
```

Normal P1.6 commands reuse artifacts 36/37.

The promoted contract may still receive deterministic implementation hardening when heterogeneous live evidence exposes a repeatable material defect. Do not create a new version for harmless model wording variation.

## 5. Capability history and current state

### v7 — historical baseline / promoted-chain rebuild rejected

Historical accepted artifact 9 depends on old P1.6 artifact 29. Dense promoted-chain rebuilds exposed source-link/index loss and then one-profile collapse with many capability requirements omitted. Do not reopen the v7 one-shot architecture.

### v8 — staged architecture proof / semantic reject

V8 staging mechanically reached complete dense requirement/responsibility coverage but remained semantically rejected because model prose inflated depth, ownership/lifecycle scope, and preferred/contextual facts.

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

Capability public promotion is operationally closed. Heterogeneous validation remains necessary before the promoted P1.6 + Capability stack is frozen as Phase-2 input.

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

Accepted publication baseline:

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
344 known/discovered jobs != 344 fully fetched advertisements
```

A discovery-only job remains a valid corpus identity with `current_detail: null`. Only the 43 entries with fetched/parsed current detail are eligible for downstream semantic-review selection.

Public-safety scan over actual corpus data passed: no raw model request/response protocol, evidence paths, SQLite paths, machine-local paths, secrets, or future private state were exported.

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

Remote GitHub inspection confirmed the manifest, job directories, contracts, and accepted anchors. Coverage reporting was subsequently hardened so `Known/discovered jobs` and `Fetched/parsed job details` are separate.

Permanent corpus rules:

1. SQLite remains runtime/history authority.
2. `corpus/` is the version-controlled current public projection.
3. Discovery-only identities and fetched/parsed details remain explicitly distinguishable.
4. Mutating JobHunter workflows refresh the local corpus only after durable success.
5. `jobhunter-corpus verify` is the deterministic DB↔corpus integrity gate.
6. Git commit/push remains explicit and is never part of runtime correctness.
7. Future personal/private evidence must never enter the public corpus.
8. Remote corpus inspection can drive role selection and later public-data analysis without local SQLite access.

## 7. Heterogeneous live review — ACTIVE

Order:

```text
1. Python/software          ← active: tmBK
2. network/security
3. operations/platform/DevOps
```

### `tmBK` upstream

```text
job:                       tmBK — Python Developer
source detail version:     44
English projection:        artifact 38
translation contract:      lm-studio-translation-v2 / english-projection-v2
P1.6 contract:             job-analysis-english-v20 / job-analysis-v5
analysis model:            gemma-4-e4b-it-ud
```

The source contains multiple different explicit depth levels in one dense requirement segment:

```text
Mastery of Python/Django
Mastery of DRF/FastAPI
Familiarity with Git
Familiarity with Linux
Familiarity with SQL/NoSQL
Sufficient knowledge of OOP/modular design
Familiarity with locking/concurrency/transaction management
```

It also contains soft/behavioral requirements and no genuine explicit responsibility section, making it a useful qualification-vs-duty test.

A separate Python candidate, `tI1n`, was blocked before P1.6 because its English projection materially mistranslated an application requirement. Upstream translation defects are not repaired by downstream factual extraction.

### `tmBK` deterministic incidents and fixes

1. **Sufficient-knowledge vocabulary** — fixed; plain `knowledge` remains non-depth.
2. **Multi-signal canonicalization** — first persisted P1.6 artifact 38 rejected because `Mastery` spread to Linux/SQL/OOP/locking concepts; fixed by item-specific depth canonicalization + fail-closed missing-item-depth behavior; regression coverage added; CI 911 passed.
3. **Effective-application wording** — later rebuild output used `Ability to effectively use AI ...` as depth; fixed by clearing that exact non-depth phrase only when its evidence contains no real depth; fail-closed preserved otherwise; regression coverage added; CI 914 passed.
4. **Redundant coverage exclusion** — model output could extract and exclude the same coverage reference; fixed by removing only contradictory duplicate exclusions for already represented references; regression coverage added; CI 916 passed.

Rejected P1.6 artifact 38:

```text
mechanically generated:       yes
semantically accepted:        no
allowed for Capability:       no
Capability downstream:        none
published as accepted corpus: no
```

The rejected artifact was retired from local current analysis state before the later rebuild attempt. The later failed rebuild persisted no replacement artifact, so the current corpus/database returned to the two accepted P1.6 anchors before the next rebuild.

### Exact next local action

After pulling current `main`:

```bash
jobhunter jobs analyze tmBK
```

Then manually inspect the complete persisted P1.6 artifact before any Capability run.

Expected source-calibrated depth semantics:

```text
Python/Django                         Mastery
DRF/FastAPI                           Mastery
Git                                   Familiarity
Linux                                 Familiarity
SQL/NoSQL                             Familiarity
OOP + modular design                  Sufficient knowledge
Database locking/concurrency/tx       Familiarity
AI usage                              no technical depth
```

Also verify:

- responsibilities remain empty unless supported by genuine duty evidence;
- soft requirements remain requirements rather than fabricated duties;
- structured skills remain present;
- source strength is not inflated;
- coverage is complete and non-contradictory.

Only after semantic P1.6 acceptance:

```bash
jobhunter jobs capability tmBK
```

Then audit complete source coverage/provenance, grouping, deterministic source strength/depth/work, role-level separation, and absence of fabricated prerequisites/ownership/lifecycle/architecture/autonomy.

## 8. Exact current state

```text
English P1.6 tG9K artifact 36       ACCEPTED / CURRENT
English P1.6 t4jp artifact 37       ACCEPTED / CURRENT
Capability v7 artifact 9            HISTORICAL / NON-CURRENT CHAIN
Capability v8 candidate              HISTORICAL / SEMANTIC REJECT
Capability v9 artifact 11           DENSE ACCEPTED / CURRENT
Capability v9 artifact 12           SPARSE ACCEPTED / CURRENT
Capability public route             v9/v5 / OPERATIONALLY VERIFIED
Blueprint                           DEFERRED / PINNED TO HISTORICAL v7 / NON-CURRENT
Public corpus                       OPERATIONALLY CLOSED / REMOTELY AVAILABLE
Known/discovered jobs               344
Fetched/parsed detail jobs          43
Published English projections       33
Published accepted/current P1.6      2
Published accepted/current Capability 2
Heterogeneous Python/software       ACTIVE — tmBK rebuild/review
Heterogeneous network/security      PENDING
Heterogeneous operations/DevOps     PENDING
Phase 2                             BLOCKED
```

## 9. After heterogeneous acceptance

If Python/software, network/security, and operations/platform/DevOps all pass without unresolved repeatable material defects:

```text
freeze promoted P1.6 v20 + Capability v9 as Phase-2 input
→ Market truthfulness/sampling
→ source/lifecycle acceptance
→ partial-success semantics
→ P1.7 report/run/browser acceptance
→ Phase-1 closure
→ only then corpus-wide Phase 2
```

Do not rerun `tG9K` or `t4jp` Capability unless a dependency changes or a repeatable correctness defect requires explicit re-evaluation.

## 10. Relevant records

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_DENSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_SPARSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_PUBLIC_PROMOTION.md
docs/working-memory/2026-08-16_PUBLIC_CORPUS_PROJECTION.md
docs/working-memory/2026-08-16_PUBLIC_CORPUS_OPERATIONAL_CLOSURE.md
docs/working-memory/2026-08-17_TMBK_P16_MULTI_SIGNAL_DEPTH_REJECTION.md
corpus/README.md
```
