# JobHunter Semantic Quality Acceptance Plan

**Status:** Active bounded acceptance plan  
**Date:** 2026-08-21  
**Scope:** promoted P1.6 factual extraction, promoted Capability Intelligence, Review Snapshot current-chain verification, closed public-corpus availability, active heterogeneous semantic review, and the concluded Phase-1 Blueprint experiment  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`, `docs/ROADMAP.md`, and product/domain/source/architecture constraints.

This plan does not authorize corpus-wide Phase-2 taxonomy/Market-v2 work.

## 1. Permanent acceptance principles

Intelligence depth follows evidence density:

```text
sparse evidence
→ modest strong conclusions
→ explicit unknowns only when genuinely supported/useful

rich evidence
→ deeper work-linked decomposition
→ richer supported reasoning
```

Permanent rules:

1. **Mechanical provenance correctness and semantic calibration are separate acceptance gates.**
2. A downstream layer never becomes more authoritative than accepted upstream evidence.
3. Optional/contextual source language must not become mandatory downstream.
4. Explicit depth belongs only to the exact concept the source qualifies.
5. Deterministic source truth is authoritative; model-owned synthesis/enrichment is subordinate.
6. Optional model enrichment may be absent. Do not force speculation to satisfy schema shape.
7. Do not polish model reasoning indefinitely when repeated experiments show a layer is not stable enough for the current phase.
8. Public promotion requires bounded semantic acceptance, deterministic CI, and normal-path operational verification.
9. Once a promoted layer passes those gates, do not reopen it for harmless non-authoritative wording variation; require a repeatable correctness/provenance/contract-level defect or a changed accepted dependency.
10. Complete public job data may be versioned remotely only through an explicit repository-safe projection boundary; future private/personal state never inherits that public status automatically.
11. A mechanically completed live artifact is still a candidate until semantic review accepts it.
12. A rejected upstream artifact must not feed downstream Capability or later authority layers.

Current opposite-end accepted anchors:

```text
t4jp  sparse/ambiguous source
tG9K  rich semiconductor/industrial-ML source
```

Current heterogeneous anchor:

```text
tmBK  Python/software — active P1.6 rebuild/review
```

## 2. Current accepted/public contracts

```text
source parser:                 jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2

English P1.6 public:           job-analysis-english-v20 / job-analysis-v5
Original P1.6 public:          job-analysis-original-v9 / job-analysis-v4

Capability public/current:     job-capability-intelligence-v9 / job-capability-intelligence-v5
Review Snapshot:               job-review-snapshot-v1
Public Corpus:                 jobhunter-public-corpus-v1
```

Capability v9 public promotion is fully closed: bounded dense/sparse semantic acceptance passed, deterministic promotion CI passed, normal public commands reuse accepted artifacts 11/12, and Review Snapshot marks those exact artifacts current on P1.6 artifacts 36/37.

Historical Capability contracts remain reproducible:

```text
v7: job-capability-intelligence-v7 / job-capability-intelligence-v4
v8: job-capability-intelligence-v8 / job-capability-intelligence-v4
```

Blueprint remains experimental/deferred:

```text
role-capability-blueprint-v6 / role-capability-blueprint-v5
```

Blueprint v6 is explicitly pinned to historical Capability v7 semantics and is not current on either accepted v9 anchor. Blueprint is **not** an accepted Phase-1 decision layer.

## 3. Layer authority

Accepted Phase-1 semantic stack:

```text
source/original employer text
→ parsed source fields
→ English projection
→ accepted P1.6 factual extraction
→ accepted Capability grouping + deterministic source truth
```

Authority split inside Capability v9:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

Storage/projection boundary:

```text
local SQLite
→ operational/runtime/history authority

corpus/
→ deterministic current public repository projection

review-snapshots/
→ selected semantic acceptance evidence
```

Experimental only:

```text
accepted P1.6 + historical Blueprint-compatible Capability
→ Blueprint professional interpretation
```

Blueprint output must not feed Market, personal readiness, automatic recommendations, or other authoritative Phase-1 decisions.

## 4. SQ-0 — Review Snapshot correctness

**Status: ACCEPTED / CURRENT-CHAIN VERIFIED.**

Normal workflow:

```bash
jobhunter jobs snapshot <job-id>
```

Capability v9 promotion verification proved:

```text
tG9K
capability_is_current_chain=True
Capability artifact=11
analysis artifact=36
contract=v9/v5
blueprint_is_current_chain=False

t4jp
capability_is_current_chain=True
Capability artifact=12
analysis artifact=37
contract=v9/v5
blueprint_is_current_chain=False
```

Current-chain status proves dependency currentness, not semantic acceptance.

## 5. SQ-1 — P1.6 factual coverage / obligation / depth

**Status: PROMOTED / CLOSED AS PUBLIC CONTRACT; HETEROGENEOUS NON-REGRESSION ACTIVE.**

Dense accepted anchor:

```text
job:                       tG9K
English P1.6 artifact:     36
contract:                  job-analysis-english-v20 / job-analysis-v5
requirements:              33
responsibilities:          8
role purpose:              0
semantic disposition:      PASS WITH ACCEPTABLE DIFFERENCE
```

Sparse accepted anchor:

```text
job:                       t4jp
English P1.6 artifact:     37
contract:                  job-analysis-english-v20 / job-analysis-v5
requirements:              8
responsibilities:          0
role purpose:              0
semantic disposition:      PASS
```

Accepted P1.6 invariants include complete source accounting; required/preferred/contextual optionality; exact concept-scoped depth; education/experience preservation; structured-skill survival; qualification-vs-duty protection; and fail-closed unsupported evidence.

Normal public P1.6 routing reuses artifacts 36/37.

Heterogeneous review may still reveal repeatable deterministic implementation defects within v20. Fix those with narrowly scoped deterministic behavior and regression tests when the public semantic contract itself remains unchanged. Do not create a new version merely for every vacancy-specific model variation.

## 6. SQ-2 — Capability Intelligence calibration

**Status: PROMOTED / OPERATIONALLY CLOSED; HETEROGENEOUS NON-REGRESSION ACTIVE.**

Accepted dense anchor:

```text
job:                              tG9K
P1.6 artifact:                    36
Capability artifact:              11
contract:                         job-capability-intelligence-v9 / job-capability-intelligence-v5
capability requirements linked:   31/31
responsibilities linked:          8/8
capability explicit depth:        5/5
all explicit depth:               6/6
role-level indices:               [31, 32]
semantic disposition:             ACCEPTED
current public chain:             YES
```

Accepted sparse anchor:

```text
job:                              t4jp
P1.6 artifact:                    37
Capability artifact:              12
contract:                         job-capability-intelligence-v9 / job-capability-intelligence-v5
capability requirements linked:   8/8
responsibilities linked:          0/0
explicit depth:                   0/0
role-level indices:               []
semantic disposition:             ACCEPTED WITH ACCEPTABLE DIFFERENCES
current public chain:             YES
```

V9 acceptance rules include complete coverage/provenance, dense anti-collapse, deterministic source strength/depth/work, role-level separation, optionality protection, filtering of unsupported ownership/lifecycle/autonomy/architecture claims, optional model enrichment, and fail-closed incomplete source truth.

Operational proof:

```text
normal tG9K Capability → reused artifact 11 → P1.6 36
normal t4jp Capability → reused artifact 12 → P1.6 37
snapshots → exact artifacts current
fresh Capability generation → none
Blueprint current → false on both anchors
```

Do not reopen Capability v9 for harmless non-authoritative wording differences.

## 7. SQ-3 — Blueprint experiment disposition

**Status: CONCLUDED FOR PHASE 1 / NOT ACCEPTED / FURTHER TUNING DEFERRED.**

Phase-1 decision:

- do not create a new Blueprint version during the heterogeneous semantic gate;
- do not weaken Blueprint validators;
- do not promote Blueprint into Market/personal/recommendation truth;
- keep historical Blueprint artifacts as experimental evidence;
- keep Blueprint v6 pinned to historical v7 dependency semantics until a separate explicit reopening decision.

## 8. SQ-4 — Capability v9 operational promotion verification

**Status: CLOSED.**

Verified on the normal public path:

```text
tG9K capability → artifact 11 → reused → v9/v5 → P1.6 36
t4jp capability → artifact 12 → reused → v9/v5 → P1.6 37
```

Review Snapshot verified the exact current chains and `blueprint_current=False` for both anchors. No fresh Capability generation occurred during promotion verification.

## 9. SQ-5 — Versioned public-corpus operational availability

**Status: OPERATIONALLY CLOSED / REMOTELY AVAILABLE.**

Contract:

```text
jobhunter-public-corpus-v1
```

Accepted invariants:

- complete current Jobinja identity set represented in the manifest;
- original public parsed Persian/English vacancy content preserved as UTF-8 JSON when current detail exists;
- discovery-only identities remain explicit with `current_detail: null`;
- current translation/P1.6/Capability artifacts use exact current dependencies/contracts;
- stale downstream files disappear after source changes until rebuilt;
- raw model protocol/request bodies, raw HTML, machine-local paths, secrets/logs/config, and future private/personal state are excluded;
- DB↔corpus verification is deterministic;
- CLI/browser durable operations synchronize locally after durable work;
- projection failure is visible and cannot roll back SQLite;
- publishing to Git remains intentional, not automatic.

Real operational proof:

```text
Known/discovered jobs:       344
Fetched/parsed job details:   43
English projections:          33
English P1.6:                  2
Original P1.6:                 0
Capabilities:                  2
```

The real local DB was exported and verified; corpus safety checks passed; accepted tG9K/t4jp dependency chains were verified; the corpus was committed/pushed; remote manifest/job inspection succeeded; publication CI passed; and CLI terminology was hardened so `Known/discovered jobs` cannot be confused with fetched/parsed detail coverage.

Important interpretation:

```text
344 known/discovered jobs != 344 complete advertisements
```

Only jobs with a current fetched/parsed detail are eligible for heterogeneous semantic-review selection.

Decision records:

```text
docs/working-memory/2026-08-16_PUBLIC_CORPUS_PROJECTION.md
docs/working-memory/2026-08-16_PUBLIC_CORPUS_OPERATIONAL_CLOSURE.md
corpus/README.md
```

## 10. SQ-6 — Heterogeneous live semantic acceptance

**Status: ACTIVE.**

Use materially different current fetched/parsed jobs:

```text
1. Python/software
2. network/security
3. operations/platform/DevOps
```

### SQ-6A — Python/software — active anchor `tmBK`

Current upstream chain:

```text
job:                       tmBK — Python Developer
source detail version:     44
English projection:        artifact 38
translation contract:      lm-studio-translation-v2 / english-projection-v2
P1.6 contract:             job-analysis-english-v20 / job-analysis-v5
analysis model:            gemma-4-e4b-it-ud
```

Why `tmBK` is useful:

- materially different from the industrial-ML dense anchor;
- ordinary backend/software requirements;
- multiple explicit technical depth levels in one source segment;
- structured source skills plus narrative requirements;
- soft/behavioral requirements;
- no genuine explicit responsibility section, which tests qualification-vs-duty restraint.

A separate Python candidate, `tI1n`, was blocked before P1.6 because manual source-vs-English review found a material translation error. Do not compensate for bad translation downstream; treat it as translation-quality evidence.

#### `tmBK` live incidents already converted into deterministic protections

1. **`Sufficient knowledge` depth vocabulary gap**
   - source explicitly uses `Sufficient knowledge of Object-Oriented concepts, modular design`;
   - v20 initially rejected the phrase because the accepted depth registry lacked it;
   - v20 now accepts `sufficient knowledge` while plain `knowledge` remains non-depth;
   - regression coverage added.

2. **Multi-signal depth propagation defect**
   - one evidence segment contains `Mastery`, `Familiarity`, and `Sufficient knowledge` for different concepts;
   - the old canonicalizer validated the supplied signal but returned the first marker in the whole evidence block, incorrectly propagating `Mastery`;
   - first persisted `tmBK` analysis artifact 38 therefore assigned `Mastery` to Linux, SQL/NoSQL, OOP/modular design, and locking/concurrency/transactions;
   - artifact 38 is semantically rejected and must not feed Capability;
   - current v20 canonicalizes from the item-specific supplied source phrase and fails closed when multi-level evidence lacks item-specific depth;
   - regression coverage added; CI passed.

3. **Non-depth effective-application wording**
   - a subsequent rebuild attempt used `Ability to effectively use (AI) ...` as `depth_signal`;
   - this phrase describes how the ability is applied, not a technical proficiency level;
   - v20 now clears that exact signal only when the evidence contains no genuine accepted depth marker;
   - if real depth exists in the same evidence, validation still fails closed instead of guessing;
   - regression coverage added; CI passed.

4. **Contradictory coverage exclusion bookkeeping**
   - model output could positively extract a coverage reference and simultaneously place the exact same reference in `coverage_exclusions`;
   - v20 now removes only the redundant exclusion when the reference is already positively represented;
   - genuine exclusions remain untouched;
   - regression coverage added; CI passed.

#### Current exact `tmBK` acceptance sequence

```text
synchronize local main to current head
→ rerun `jobhunter jobs analyze tmBK`
→ inspect complete persisted P1.6 artifact
→ verify all depth-sensitive requirements
→ verify AI usage has depth=null
→ verify no fabricated responsibilities
→ verify soft requirements remain requirements rather than duties
→ verify complete/non-contradictory coverage
→ accept P1.6 only if source truth is correct
→ only then run `jobhunter jobs capability tmBK`
```

Expected depth-sensitive semantics from the employer source:

```text
Python/Django                         Mastery
DRF/FastAPI                           Mastery
Git                                   Familiarity
Linux                                 Familiarity
SQL/NoSQL                             Familiarity
OOP + modular design                  Sufficient knowledge
Database locking/concurrency/tx       Familiarity
AI usage for software development     no technical depth signal
```

Do not run Capability before `tmBK` P1.6 acceptance.

### SQ-6B — network/security — pending

Select a materially different fetched/parsed role after Python/software closes. Review protocol/security-tool/incident/monitoring/certification/operational-duty semantics without importing generic security expectations.

### SQ-6C — operations/platform/DevOps — pending

Select a materially different fetched/parsed role after network/security. Stress CI/CD, Linux/cloud/container/orchestration/monitoring/availability/incident/production/ownership language while preventing unsupported architecture/lifecycle/autonomy inflation.

### Per-role acceptance procedure

For each role:

1. verify source detail and English projection quality first;
2. run/reuse current English P1.6 through the normal public path;
3. manually accept P1.6 source truth before Capability;
4. run/reuse Capability v9 through the normal public path;
5. verify complete requirement/responsibility coverage and source provenance;
6. review required/preferred/contextual optionality and explicit depth calibration;
7. ensure no fabricated responsibilities, role constraints, prerequisites, ownership, lifecycle, architecture, autonomy, or mandatory strength;
8. distinguish repeatable deterministic defects from local-model limitations or harmless non-authoritative variation;
9. convert repeatable deterministic defects into regression fixtures;
10. preserve acceptable model variation when authoritative source truth remains correct;
11. do not change the v9 contract merely to cosmetically normalize prose.

Only after heterogeneous acceptance should promoted P1.6 + Capability be considered stable/frozen Phase-2 input.

## 11. Phase-2 gate

Do not begin corpus-wide Phase 2 until:

```text
P1.6 promotion closed
+ Capability v9 promotion closed
+ public corpus operationally closed
+ heterogeneous semantic review accepted
+ remaining Phase-1 workflow/source/market truthfulness gates closed
```

Blueprint remains non-authoritative unless separately reopened by evidence and explicit decision.
