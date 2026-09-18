# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-09-18  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active branch:** `main`  
**Current product gate:** MARKET I1-I6 ACCEPTED / I7 PREPARED / LOCAL EXECUTION PENDING  
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

Prepared I7 protocol:

`docs/working-memory/2026-09-18_MARKET_I7_LOCAL_ACCEPTANCE_PROTOCOL.md`

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
I7  bounded real local acceptance           PREPARED / LOCAL EXECUTION PENDING
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

## 4. Exact next responsibility — I7

I7 is **real local acceptance**, not another architecture/implementation phase by default.

The repository-side protocol is prepared at:

`docs/working-memory/2026-09-18_MARKET_I7_LOCAL_ACCEPTANCE_PROTOCOL.md`

No real local I7 run has been claimed yet.

Use one small representative target with precise core-vs-adjacent meaning. Applied AI / ML Engineering is appropriate if its membership intent explicitly distinguishes direct AI/ML/model/agent/retrieval/system-behavior engineering from backend/platform work that primarily enables AI and from generic use of AI tools.

I7 should be executed against the owner's actual local runtime and operational SQLite, with conservative bounded budgets.

### I7 sequence

```text
1. readiness/preflight
2. create or intentionally reuse target identity
3. create/reuse one precise immutable definition version
4. preview exact target acquisition envelope
5. run one small bounded target update
6. inspect run ledger and failures
7. inspect membership outcomes/evidence
8. inspect immutable snapshot
9. inspect source vs semantic denominators
10. inspect deterministic aggregate + evidence drill-down
11. inspect browser UX and same state through CLI
12. repeat unchanged bounded run
13. verify reuse/currentness and no unrelated backlog spill
14. verify Market local-state privacy/publication boundary
15. record PASS / repair / HOLD from actual evidence
```

### Real evidence to capture

At minimum preserve:

```text
Git head
config-safe run controls (no secrets)
target + definition id/version/fingerprint
search count/request budget
candidate count
source/detail outcomes
translation reused/completed/failed counts
P1.6 current/pending/new/failed counts
membership selected/remaining/succeeded/failed + disposition counts
run status/ledger
snapshot id/member counts
core source denominator
accepted-semantic denominator
profile warnings/limitations
representative evidence drill-down paths
unchanged rerun results/reuse
SQLite integrity / foreign-key check if practical
browser screenshots only after privacy review
```

Do not commit operational SQLite, API tokens, local host paths, or private evidence dumps merely to preserve acceptance.

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
353 known/discovered jobs
43 fetched/parsed details
21 current English projections
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
