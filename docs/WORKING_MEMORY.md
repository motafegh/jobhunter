# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-23
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** Phase 1 CLOSED; P2.1A/B/C ACCEPTED; P2.1D small reviewed seed next

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
tmBK → Capability artifact 13 → HETEROGENEOUS PYTHON/SOFTWARE ACCEPTED / CURRENT
t4qV → Capability artifact 14 → HETEROGENEOUS NETWORK/SECURITY ACCEPTED / CURRENT
tmyX → Capability artifact 15 → HETEROGENEOUS OPERATIONS/PLATFORM ACCEPTED / CURRENT
```

Normal Capability commands reuse artifacts 11/12 on P1.6 artifacts 36/37. Review Snapshot marks both exact chains current. Blueprint remains `blueprint_current=False`, deferred/non-authoritative, and pinned to historical Capability v7 semantics.

The complete repository-safe public corpus is implemented, populated from the real local database, verified, remotely inspected, and operationally closed. Current projection export excludes preserved historical English v1 artifacts.

Heterogeneous Python/software validation is closed on `tmBK`: P1.6 artifact 39 was explicitly accepted after complete source review, and Capability artifact 13 passed 16/16 requirement, 0/0 responsibility, and 7/7 explicit-depth review.

Network/security `t4qV` is closed on P1.6 44 → Capability 14 after general structured-skill, preferred-heading, experience-bound, responsibility, candidate-experience, and credential-ontology fixes. Operations/platform `tmyX` is closed on P1.6 46 → Capability 15 after general heading-boundary, pre-heading duty, and non-depth ability/skill fixes. `t49N` was blocked before P1.6 for a material English field-association defect.

Phase 2 is active only through `docs/P2_1_CANONICAL_CONCEPT_REGISTRY_PLAN.md`. P2.1A deterministic persistence, P2.1B manual CLI review, and P2.1C browser review are accepted. The next bounded increment is P2.1D: a deliberately small, human/semantic-reviewed seed from the five accepted P1.6 chains, followed by idempotency/stale-dependency acceptance. P2.1 is not closed yet.

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
Canonical Registry:         jobhunter-canonical-concept-registry-v1
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

Capability public promotion is operationally closed and the accepted P1.6 v20/v5 + Capability v9/v5 stack is frozen as the Phase-2 source-truth input unless a repeatable material defect or dependency change explicitly reopens it.

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
Known/discovered Jobinja jobs: 353
Fetched/parsed job details:     43
Current English projections:    20
English P1.6:                    5
Original P1.6:                   0
Capabilities:                    5
Per-job stage files:           383
Corpus size:                  ~3.7 MiB
```

Important interpretation:

```text
353 known/discovered jobs != 353 fully fetched advertisements
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
9. Canonical-registry review state is not part of the public corpus unless a later explicit privacy/source review authorizes a repository-safe projection.

## 7. Heterogeneous live review — CLOSED

Order:

```text
1. Python/software          ← accepted: tmBK 39 → 13
2. network/security         ← accepted: t4qV 44 → 14
3. operations/platform      ← accepted: tmyX 46 → 15
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

The acceptance boundary is now enforced in persistence and every authoritative consumer. Fresh English v20 output is stored as `pending`; only explicit review acceptance makes it eligible for Capability, Market, accepted dashboard counts, or `corpus/`. Review rejection archives the full local candidate and clears its current unique identity for a corrected rebuild. Existing accepted anchors 36/37 migrate as accepted. V20 also owns a copied depth-signal registry, so importing it cannot mutate historical validators.

### Exact next local action

P2.1A, P2.1B, and P2.1C are accepted. Do not rerun accepted heterogeneous anchors merely for wording variation. Execute P2.1D only: inspect exact accepted/current P1.6 claims from all five accepted chains, choose a deliberately small cross-role seed, human/semantic-review every concept/alias/mapping decision, include the required alias + ambiguous/unmapped + responsibility + education/credential-or-experience case, then prove rerun/idempotency and stale-dependency behavior. Do not bulk-map the accepted corpus or begin Market v2.

Exact heterogeneous records:

- `docs/working-memory/2026-08-21_T4QV_NETWORK_SECURITY_P16_REJECTIONS.md`
- `docs/working-memory/2026-08-21_TMYX_OPERATIONS_PLATFORM_ACCEPTANCE.md`
- `docs/working-memory/2026-08-23_PARTIAL_SUCCESS_SEMANTICS_ACCEPTANCE.md`

Closed Phase-1 plan and evidence:

- `docs/P1_7_REPORT_RUN_BROWSER_ACCEPTANCE_PLAN.md`
- `docs/working-memory/2026-08-23_P1_7_AND_PHASE_1_CLOSURE.md`

Active focused Phase-2 plan and acceptance records:

- `docs/P2_1_CANONICAL_CONCEPT_REGISTRY_PLAN.md`
- `docs/working-memory/2026-08-23_P2_1A_REGISTRY_FOUNDATION.md`
- `docs/working-memory/2026-08-23_P2_1B_MANUAL_CLI_ACCEPTANCE.md`
- `docs/working-memory/2026-08-23_P2_1C_REGISTRY_BROWSER_ACCEPTANCE.md`

## 8. Exact current state

```text
English P1.6 tG9K artifact 36       ACCEPTED / CURRENT
English P1.6 t4jp artifact 37       ACCEPTED / CURRENT
English P1.6 tmBK artifact 39       PYTHON/SOFTWARE ACCEPTED / CURRENT
English P1.6 t4qV artifact 44       NETWORK/SECURITY ACCEPTED / CURRENT
English P1.6 tmyX artifact 46       OPERATIONS/PLATFORM ACCEPTED / CURRENT
Capability v7 artifact 9            HISTORICAL / NON-CURRENT CHAIN
Capability v8 candidate              HISTORICAL / SEMANTIC REJECT
Capability v9 artifact 11           DENSE ACCEPTED / CURRENT
Capability v9 artifact 12           SPARSE ACCEPTED / CURRENT
Capability v9 artifact 13           PYTHON/SOFTWARE ACCEPTED / CURRENT
Capability v9 artifact 14           NETWORK/SECURITY ACCEPTED / CURRENT
Capability v9 artifact 15           OPERATIONS/PLATFORM ACCEPTED / CURRENT
Capability public route             v9/v5 / OPERATIONALLY VERIFIED
Blueprint                           DEFERRED / PINNED TO HISTORICAL v7 / NON-CURRENT
Canonical registry contract         v1 / ACCEPTED FOUNDATION
P2.1A deterministic persistence     ACCEPTED
P2.1B manual CLI                    ACCEPTED
P2.1C browser review                ACCEPTED
P2.1D small reviewed seed           ACTIVE NEXT / NOT YET ACCEPTED
P2.1 overall                        OPEN
Public corpus                       OPERATIONALLY CLOSED / REMOTELY AVAILABLE
Known/discovered jobs               353
Fetched/parsed detail jobs          43
Current English projections         20
Current local corpus P1.6             5
Current local corpus Capability       5
Heterogeneous Python/software       ACCEPTED — tmBK 39 → 13
Heterogeneous network/security      ACCEPTED — t4qV 44 → 14
Heterogeneous operations/platform  ACCEPTED — tmyX 46 → 15
```

## 9. Phase-2 progression

The accepted Phase-1 stack now feeds the bounded registry path:

```text
freeze promoted P1.6 v20 + Capability v9 as Phase-2 input
→ P2.1A registry persistence ACCEPTED
→ P2.1B manual CLI review ACCEPTED
→ P2.1C browser review ACCEPTED
→ P2.1D small cross-role seed + acceptance ACTIVE
→ only after P2.1 closure: later focused Phase-2 aggregation work
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
docs/working-memory/2026-08-23_P2_1B_MANUAL_CLI_ACCEPTANCE.md
docs/working-memory/2026-08-23_P2_1C_REGISTRY_BROWSER_ACCEPTANCE.md
corpus/README.md
```
