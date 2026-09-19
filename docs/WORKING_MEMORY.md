# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-09-18  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active branch:** `main`  
**Current product gate:** MARKET I1-I6 ACCEPTED / I7 EXECUTED / HOLD — CLOSURE FOLLOW-UP NEXT  
**P2.2B-B1:** CLOSED — NO-PROMOTION / DEFER  
**Parallel portfolio:** MIT complete; GitHub metadata + screenshots + release + owner mastery pending

## 1. Read this first

Current status authority:

`docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`

Current Market plan:

`docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`

Foundation decision:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

Latest accepted increment:

`docs/working-memory/2026-09-17_MARKET_I6_BROWSER_CLI_WORKFLOW_IMPLEMENTATION.md`

Executed I7 protocol:

`docs/working-memory/2026-09-18_MARKET_I7_LOCAL_ACCEPTANCE_PROTOCOL.md`

I7 execution result:

`docs/working-memory/2026-09-18_MARKET_I7_REAL_LOCAL_ACCEPTANCE_HOLD.md`

Execution checklist:

`docs/EXECUTION_TODO.md`

I3 real-model evidence:

`docs/experiments/2026-09-17_market-i3-real-model-acceptance/README.md`

Do not follow older `I1-I6 NEXT`, open-B1, or pre-foundation instructions when they conflict with these current owners.

---

## 2. Frozen first-slice rules

```text
source = Jobinja only
search/acquisition envelope != target membership truth
membership = core_match | adjacent_match | uncertain | excluded
primary source corpus = core_match only
accepted P1.6 is not required for source-level membership
accepted-current P1.6 is required for strong semantic prevalence
pending/missing/failed/rejected P1.6 != zero demand
Capability/Work optional, not gates
repost/new-ID collapse deferred
use 'qualified source postings', not 'unique demand units'
Market state local/private by default
```

Target-definition lesson from I3 real-model evaluation:

> Material core-vs-adjacent boundaries belong in immutable `TargetMarketDefinitionVersion.membership_intent`; do not patch individual vacancies into the classifier prompt when target meaning is under-specified.

---

## 3. Accepted Market sequence

```text
I1  domain + persistence                    ACCEPTED
I2  target-scoped affected work             ACCEPTED
I3  membership qualification                ACCEPTED
I4  immutable snapshot construction         ACCEPTED
I5  deterministic aggregate profile         ACCEPTED
I6  browser + CLI thin workflow             ACCEPTED
I7  bounded real local acceptance           EXECUTED / HOLD
```

### I1

Stable target identity, immutable definition versions, run/member/snapshot/profile persistence, exact dependency identities and immutable history.

### I2

Target-only source/refresh/translation/P1.6 planning. No remaining budget may spill into unrelated global backlog. Failed refresh neither proves disappearance nor refreshes freshness.

### I3

Bounded target-relative membership with deterministic constraints first and semantic reasoning only where needed. Exactly:

```text
core_match
adjacent_match
uncertain
excluded
```

Accepted P1.6 is optional evidence, not a membership gate. Exact dependency reuse and explicit correction history are preserved.

Real-model boundary evidence:

```text
broad target       7/8 expected outcomes; tGM0 sole miss
clarified target   8/8 post-hoc boundary-calibration outcomes
```

The second result is not a general accuracy benchmark.

### I4

Terminal Market run → exact current membership identities → immutable snapshot. Semantic coverage is frozen as accepted/pending/missing/failed/rejected, and only core membership enters primary source corpus.

### I5

Deterministic profile reads one exact immutable snapshot. It keeps source/core and accepted-semantic denominators separate, uses immutable source-detail employer evidence, deduplicates concept support per posting, preserves requirement strengths and responsibility evidence, and applies Registry mappings only as-of snapshot time.

No model-authored numeric facts.

### I6

Shared implementation:

```text
src/jobhunter/market_workspace.py
src/jobhunter/market_cli.py
src/jobhunter/web/market_workspace.py
```

Primary browser surface:

```text
/market/targets
```

CLI:

```text
jobhunter market target list
jobhunter market target create
jobhunter market definition create TARGET_ID
jobhunter market show
jobhunter market preview DEFINITION_ID
jobhunter market run DEFINITION_ID
jobhunter market run-show RUN_ID
jobhunter market snapshot-show SNAPSHOT_ID
```

I6 coordinator path:

```text
immutable target definition
→ exact target search scope
→ bounded Jobinja discovery
→ bounded target-only source work
→ bounded translation
→ bounded P1.6 generation
→ bounded membership qualification
→ terminal partial-success run ledger
→ immutable snapshot
→ deterministic profile
```

Important I6 boundary:

- `membership_limit` is explicit and 0-50;
- ledger exposes eligible/selected/remaining/succeeded/failed/dispositions;
- read-only target preview does not initialize the complete model/provider runtime;
- browser uses existing one-mutable-operation `WebOperationManager`;
- CLI and browser share the same Market workspace/state owners;
- Market local tables are not exported to public corpus;
- legacy `/market` aggregate page remains available but is not the target-scoped historical authority.

During I6 integration, tests caught an accidental attempted change to accepted I5 aggregate semantics. The exact accepted I5 implementation was restored before I6 acceptance. Do not reintroduce that convenience-factory change into I5; I6 composes `MarketAggregateService` directly.

Final I6 technical evidence:

```text
technical head: 4076bb731b3485aa99fbdf63bf73a96dc7a5773b
CI:             1210 / 35263630011
entrypoint:     PASS
Ruff:           PASS
pytest:         632 passed
pytest -W error 632 passed
```

---

## 4. Exact next responsibility — I7 HOLD closure follow-up

I7 real-local execution occurred on the owner's operational runtime.

Protocol:

`docs/working-memory/2026-09-18_MARKET_I7_LOCAL_ACCEPTANCE_PROTOCOL.md`

Sanitized result:

`docs/working-memory/2026-09-18_MARKET_I7_REAL_LOCAL_ACCEPTANCE_HOLD.md`

Key evidence:

```text
run 1: completed_with_failures
snapshot/profile: created
core source postings: 6
accepted-semantic core postings: 0

run 2: completed_with_failures
candidate jobs: 52
discovery: 5 searches / 5 requests / 5 pages / 0 new IDs
source execution: 6 attempted / 6 succeeded / 5 new versions / 1 unchanged
translation: 4 attempted / 2 completed / 2 failed
final current translation reuse: 9
P1.6: 2 attempted / 1 completed-or-reused / 1 failed
final P1.6 state: 0 accepted / 1 pending-review
membership: 12 eligible / 8 selected / 8 succeeded / 0 failed
dispositions: 6 core / 1 adjacent / 1 excluded
CI 1246: SUCCESS
```

The runs proved useful target-scoped progression, currentness/reuse, honest partial-success handling,
membership separation, source-vs-semantic denominator honesty, and Market-publication privacy.

During I7, browser inspection exposed presentation gaps in target forms, membership reason/evidence,
and frozen aggregate evidence. The local agent repaired those surfaces, added a regression test proving
historical snapshot evidence survives later source changes, and the final pushed head passed CI.

Decision: **HOLD**. The live source corpus had no accepted-semantic core member, so the real workflow
could not exercise accepted-P1.6 requirement/responsibility drill-down. The handoff also did not retain
the final post-rerun snapshot/profile immutability comparison or a post-run SQLite integrity result.

Next work is narrow:

```text
review the pending P1.6 artifact normally
→ accept only if it is semantically valid; otherwise preserve rejection/pending evidence
→ establish at least one accepted-current P1.6 core member without weakening the contract
→ verify live semantic aggregate/evidence drill-down through CLI + browser
→ verify second snapshot/profile and first snapshot/profile immutability
→ verify post-run SQLite integrity/foreign keys + privacy
→ PASS only if all remaining checks succeed
```

No new Market architecture or later-scope feature is authorized by this HOLD.

---

### 2026-09-19 closure follow-up

Definition fingerprint and snapshot/profile 2 were recovered. Snapshot 1, its members
and profile exactly match both retained pre-rerun JSON captures. Operational SQLite
integrity/foreign-key and corpus privacy checks passed. Those evidence gaps are closed.

Pending `t7ck` P1.6 artifact 48 has material coverage/optionality/qualification-to-duty
errors and must not be accepted. Owner rejection decision remains pending. An isolated
replay exposed a foreign-key failure when rejecting a candidate referenced by snapshot 2.
A bounded `AnalysisStore` repair now retains rejected historical payloads while excluding
them from current/reuse selection and allowing replacements. Real-database-copy replay,
Ruff, dependency consistency, and all 636 tests with warnings-as-errors passed. Operational
review state remains unchanged; the repair is local/uncommitted.

The remaining gate is a valid accepted-semantic core artifact and real CLI/browser
semantic drill-down on a new snapshot, followed by post-mutation integrity/privacy checks.
Details are appended to `docs/working-memory/2026-09-18_MARKET_I7_REAL_LOCAL_ACCEPTANCE_HOLD.md`.

---

## 5. I7 decision rule

Possible outcomes:

```text
PASS
→ first Market vertical slice can close

BOUNDED REPAIR
→ identify exact owning layer (I2/I3/I4/I5/I6), repair only that defect,
  rerun deterministic CI + relevant real acceptance

HOLD
→ keep slice open when evidence is insufficient or local/provider/source conditions
  prevent a defensible conclusion
```

Do not force PASS because I1-I6 repository tests are green.

---

## 6. I7 stop lines

Do not during I7:

- add role-subfamily synthesis;
- add trends/emerging/forecasting;
- add Market → You/personal scoring;
- auto-accept P1.6;
- make Capability or Work mandatory;
- invent repost-dedup thresholds;
- publish local Market tables to `corpus/`;
- reopen B1/P2.2C/P2.2D;
- introduce another workflow/currentness/persistence layer;
- weaken deterministic tests to accommodate a live model result.

If live evidence exposes a real defect, preserve the evidence and repair the smallest owning boundary.

---

## 7. Public corpus / local-state boundary

Repository-safe public corpus baseline remains:

```text
394 known/discovered jobs
51 fetched/parsed details
27 current English projections
5 accepted/current English P1.6
5 accepted/current Capability
```

`market run` may create upstream English/P1.6 artifacts, so the existing public-corpus wrapper may refresh those already-governed projections. It must not publish:

```text
Market target definitions
Market research runs
Market memberships
Market snapshots
Market aggregate profiles
```

unless a later explicit publication decision authorizes that.

---

## 8. Parallel portfolio/release

Still pending:

```text
GitHub description/topics
real browser screenshots + privacy review
intentional v0.1.0 tag/release
owner mastery verification
```

These do not change the I7 product frontier.
