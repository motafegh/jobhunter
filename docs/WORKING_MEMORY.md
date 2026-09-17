# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-09-17  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current product gate:** MARKET I1-I5 ACCEPTED / I6 NEXT  
**P2.2B-B1:** CLOSED — NO-PROMOTION / DEFER  
**Parallel portfolio:** MIT complete; GitHub metadata + screenshots + release + owner mastery pending

## 1. Read this first

Current status authority:

`docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`

Current Market plan:

`docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`

Foundation decision:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

Accepted Market implementation records:

```text
docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md
docs/working-memory/2026-09-16_MARKET_I2_TARGET_SCOPED_AFFECTED_WORK_IMPLEMENTATION.md
docs/working-memory/2026-09-17_MARKET_I3_MEMBERSHIP_QUALIFICATION_IMPLEMENTATION.md
docs/working-memory/2026-09-17_MARKET_I4_IMMUTABLE_SNAPSHOT_CONSTRUCTION.md
docs/working-memory/2026-09-17_MARKET_I5_DETERMINISTIC_AGGREGATE_PROFILE.md
```

I3 real-model evidence:

`docs/experiments/2026-09-17_market-i3-real-model-acceptance/README.md`

Execution checklist:

`docs/EXECUTION_TODO.md`

Do not follow older `I1-I5 NEXT`, open-B1, or pre-foundation instructions when they conflict with these current owners.

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

> Material core-vs-adjacent boundaries belong in immutable `TargetMarketDefinitionVersion.membership_intent`; do not patch individual vacancies into the classifier prompt when the target meaning is under-specified.

---

## 3. Accepted Market increments

### I1 — domain + persistence

Accepted immutable owners for targets, definition versions, research runs, memberships, snapshots/members and aggregate profiles. Exact dependency identities and history are preserved.

Evidence: CI 1160 green through `pytest -W error`.

### I2 — target-scoped affected work

Accepted target-only source/refresh/translation/P1.6 planning with no global backlog spill. Failed refresh neither proves disappearance nor freshens evidence.

Evidence: CI 1167 green through `pytest -W error`.

### I3 — membership qualification

Accepted bounded target-relative interpretation into exactly core/adjacent/uncertain/excluded with deterministic constraints first, optional accepted P1.6, exact reuse and immutable corrections.

Implementation: `0eaf04109a57846aa6d0a920d0563f89a4dfb535`  
CI 1172: 608 passed twice.

Real-model boundary evidence:

```text
broad target       7/8 expected outcomes; tGM0 sole miss
clarified target   8/8 post-hoc boundary-calibration outcomes
```

This is supportive boundary evidence, not a population accuracy benchmark.

### I4 — immutable snapshot construction

Implementation:

```text
src/jobhunter/market_snapshot_service.py
tests/test_market_snapshot_service.py
```

Accepted:

- snapshot requires completed/completed-with-failures run;
- exact current I3 membership identities only;
- stale/superseded membership rejected;
- one source job at most once;
- semantic coverage derived as accepted/pending/missing/failed/rejected;
- failed/rejected processing state is scoped to current dependency contract;
- only core enters primary source corpus;
- historical snapshots remain immutable.

Technical evidence:

```text
head 4b5e83134202d32ee167f499c3aca9cb43478f56
CI 1182: Ruff PASS, 617 pytest PASS, 617 pytest -W error PASS
```

### I5 — deterministic aggregate profile

Acceptance owner:

`docs/working-memory/2026-09-17_MARKET_I5_DETERMINISTIC_AGGREGATE_PROFILE.md`

Implementation:

```text
src/jobhunter/market_aggregate_service.py
tests/test_market_aggregate_service.py
```

I5 builds one deterministic `market-aggregate-profile-v1` artifact from one immutable I4 snapshot only.

Accepted behavior:

- never reconstructs corpus membership from today's current state;
- source-level denominator = qualified core source postings;
- semantic denominator = core postings with accepted snapshot P1.6;
- core/adjacent/uncertain/excluded and all semantic coverage states remain explicit;
- employer breadth/concentration is derived from exact immutable source-detail `company` evidence;
- unknown employer remains unknown rather than fabricated;
- source context is deterministic over exact source-detail fields;
- only accepted-semantic core members contribute requirement/responsibility prevalence;
- one posting supports a normalized concept/responsibility at most once;
- requirement strength remains explicit as required/preferred/contextual/inferred;
- distinct-employer support and exact evidence drill-down are preserved;
- reviewed Canonical Registry mappings enrich only when reviewed no later than the snapshot timestamp;
- later Registry review cannot silently change historical aggregate replay;
- no model writes counts, shares, denominators or scores;
- repost adjustment remains explicitly not implemented;
- persisted deterministic replay is immutable/idempotent.

Warnings include small samples, incomplete semantic coverage, employer concentration, unknown employer evidence, and missing repost adjustment where applicable.

Technical evidence:

```text
head 5defb23cb769a4be7a6b0d13ea7762d35ec0f4ba
CI 1189 / 35250174702
Ruff: PASS
pytest: 622 passed
pytest -W error: 622 passed
conclusion: SUCCESS
```

---

## 4. Exact next action — I6 only

**I6 responsibility:** expose the accepted Market state/workflow through a thin browser + CLI surface using the same services and SQLite authority.

I6 must not duplicate I1-I5 business logic.

### Required I6 product surface

At minimum:

```text
list/create target identity
create/inspect immutable target definition
inspect run state/ledger
inspect exact snapshot/profile history
render latest deterministic profile
show core/source vs accepted-semantic denominators
show membership/semantic coverage counts and warnings
show requirement/responsibility evidence drill-down
```

The browser should remain the primary repeat-use workflow. CLI should expose the same services/state for automation/debugging rather than creating a second product model.

### Coordinator boundary

The first slice still needs a thin target-run coordinator. I6 may wire the already accepted services for one bounded run flow, but it must preserve the existing one-mutable-operation behavior and partial-success ledger semantics.

Do not invent a generic workflow engine.

### I6 stop lines

Do not add:

- model-generated report narrative;
- semantic role-subfamily clustering;
- repost/new-ID heuristics;
- trends/emerging/forecasting;
- personal Market→You scoring;
- Capability/Work gating;
- public `corpus/` publication;
- new vector/RAG/graph/agent infrastructure.

I7 remains responsible for the bounded real local end-to-end target run and reuse acceptance.

---

## 5. First-slice sequence

```text
I1  domain + persistence                         ACCEPTED
I2  target source eligibility / affected work   ACCEPTED
I3  membership qualification                    ACCEPTED
I4  immutable snapshot construction             ACCEPTED
I5  deterministic aggregate                     ACCEPTED
I6  browser + CLI thin workflow                 NEXT
I7  bounded real local acceptance               BLOCKED BY I6
```

---

## 6. Parallel portfolio/release state

Still pending:

```text
GitHub description/topics
real browser screenshots + privacy review
intentional v0.1.0 release
owner mastery verification
```

This does not change the I6 product frontier.
