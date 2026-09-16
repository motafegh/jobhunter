# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-09-16  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current product gate:** MARKET I1 + I2 ACCEPTED / I3 NEXT  
**P2.2B-B1:** CLOSED — NO-PROMOTION / DEFER  
**Parallel portfolio:** MIT complete; GitHub metadata + screenshots + release + owner mastery pending

## 1. Read this first

Current status authority:

`docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`

Current Market design authority:

`docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`

Foundation decision:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

Accepted implementation records:

```text
docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md
docs/working-memory/2026-09-16_MARKET_I2_TARGET_SCOPED_AFFECTED_WORK_IMPLEMENTATION.md
```

Execution checklist:

`docs/EXECUTION_TODO.md`

Do not follow older `I1 NEXT` / `I2 NEXT`, open-B1, or pre-foundation instructions when they conflict with these current owners.

---

## 2. Frozen accepted substrate

```text
parser:                     jobinja-detail-v2
translation:                english-projection-v2 / lm-studio-translation-v2
English P1.6:               job-analysis-english-v20 / job-analysis-v5
Capability:                 job-capability-intelligence-v9 / job-capability-intelligence-v5
Canonical Registry:         jobhunter-canonical-concept-registry-v1 / P2.1 CLOSED
Work Intelligence:          job-work-intelligence-v2 / v2.0 / P2.2A CLOSED
Public Corpus:              jobhunter-public-corpus-v1
Market snapshot:            market-corpus-snapshot-v1
Market aggregate storage:   market-aggregate-profile-v1
```

Public corpus remains:

```text
353 known/discovered jobs
43 fetched/parsed details
21 current English projections
5 accepted/current English P1.6
5 accepted/current Capability
```

B1 remains closed as NO-PROMOTION / DEFER.

---

## 3. Permanent first-slice boundaries

```text
source = Jobinja only
search vocabulary != target membership truth
membership = core_match | adjacent_match | uncertain | excluded
primary corpus = core_match only
accepted P1.6 not required for source-level membership
accepted P1.6 required for strong semantic prevalence
Capability/Work optional, not gates
missing/pending/failed P1.6 != zero demand
repost/new-ID automatic collapse deferred
use 'qualified source postings', not 'unique demand units'
Market state local/private by default
```

Semantic role-subfamily synthesis, trends/forecasting, personal Market→You scoring, P2.2C/P2.2D promotion, and Market publication remain outside the first slice.

---

## 4. I1 — ACCEPTED / CLOSED

I1 established:

```text
market_targets
market_target_definition_versions
market_research_runs
market_job_memberships
market_corpus_snapshots
market_corpus_snapshot_members
market_aggregate_profiles
```

Key accepted behavior:

- stable target identity vs immutable definition versions;
- immutable exact-dependency membership history;
- immutable snapshot/member history;
- immutable deterministic aggregate-profile persistence;
- target-definition changes do not invalidate generic source/translation/P1.6 artifacts.

Final technical evidence:

```text
head: f0cded55a9887c061898d0dcab7f5e6b10300d8e
CI 1160 / 35108236384: PASS through pytest -W error
```

---

## 5. I2 — ACCEPTED / CLOSED

Implementation:

```text
src/jobhunter/job_detail_observations.py
src/jobhunter/market_affected_work.py
tests/test_market_affected_work.py
```

I2 adds one read-only target-scoped affected-work planner. It receives one immutable target definition and one already-discovered target candidate set; it never fills unused capacity from unrelated global backlog.

### Source planning

Per candidate it preserves:

```text
source identity/title/company
lifecycle
source status + selected/remaining action
current parsed detail version ID when usable
latest detail time
latest observation outcome
warnings
```

Source states:

```text
current
missing_detail
refresh_due
invalid_current_detail
expired
removed
ineligible_lifecycle
```

A source becomes eligible for I3 only when current parsed evidence exists, lifecycle is active/cautiously possibly-unavailable, and freshness is inside the current-active threshold.

### Freshness rule

I2 now distinguishes successful evidence from failed retries:

```text
latest successful parsed detail check
→ otherwise current parsed detail fetched_at
```

A failed check:

```text
does not freshen evidence
does not delete prior evidence
does not imply disappearance
```

An unchanged successful parsed check refreshes freshness without creating a new semantic version.

### Translation / P1.6 planning

Only source-ready target candidates may consume downstream budget.

Translation states:

```text
blocked_source
current
needed_selected
needed_remaining
unavailable_provider
```

P1.6 states:

```text
blocked_source
blocked_translation
current_accepted
current_pending_review
needed_selected
needed_remaining
unavailable_model
```

Exact current translation/P1.6 artifacts are reused. Pending current P1.6 remains pending review rather than being regenerated. A new semantic source version naturally invalidates old downstream currentness without deleting history.

### I2 regression boundary

Tests explicitly prove:

- missing-detail budget cannot spill into unrelated global backlog;
- refresh budget cannot spill into unrelated global backlog;
- translation/P1.6 budget cannot spill into unrelated global backlog;
- target work can remain `remaining` even when unrelated global work exists;
- failed refresh != disappearance;
- lifecycle removed/expired exclusion remains deterministic;
- exact dependency reuse/currentness is preserved.

Final technical evidence:

```text
head: 2ada4e92207f694bb5b7a4cba8c17108a67a4863
CI 1167 / 35123454023
Ruff: PASS
pytest: PASS
pytest -W error: PASS
```

I2 is planning-only. Actual target discovery/source/model execution and persisted run-stage failures will be integrated later into the thin Market coordinator; I2 itself makes no network/model calls.

---

## 6. Exact next action — I3 only

I3 responsibility:

**Membership qualification contract + service.**

I3 must consume only I2 source-eligible candidates and decide one of:

```text
core_match
adjacent_match
uncertain
excluded
```

### Required I3 shape

```text
1. deterministic target constraints
2. bounded semantic role/work relevance only when deterministic evidence is insufficient
3. persist/reuse exact MarketJobMembership dependency identity
```

Minimum factual evidence boundary:

```text
current parsed source detail + title
+ current English projection when needed for language/semantic reasoning
+ accepted-current P1.6 opportunistically when available
```

Accepted P1.6 must **not** become a prerequisite. Capability and Work remain optional and must not become gates.

### Representative boundary cases already authorized for fake/fixture tests

For the Applied AI / ML Engineering representative target:

```text
ta9l  → clear core source evidence despite no accepted P1.6
tG9K  → clear core with accepted P1.6 support
tGM0  → adjacent backend/AI-platform role
t4jp  → excluded AI-title false positive / content-production center
tmBK  → excluded Python/backend with AI-usage qualification only
t4qV  → excluded network security
tmyX  → excluded infrastructure security
```

Add a sparse/borderline fixture where `uncertain` is the correct successful output.

### I3 must prove

- title/keyword equality cannot by itself create `core_match`;
- deterministic exclusions/constraints happen before model calls;
- model output is bounded to the four dispositions + short reason/evidence refs;
- `uncertain` is valid success, not a failure/retry trigger;
- exact target/source/classifier/translation/P1.6 dependencies drive reuse;
- changed source/target/classifier dependencies prevent stale membership reuse;
- exact reruns reuse membership;
- reviewed corrections supersede rather than overwrite history;
- no Registry/P2.2C/P2.2D promotion side effect.

---

## 7. First-slice sequence

```text
I1  domain + persistence                         ACCEPTED
I2  target source eligibility / affected work   ACCEPTED
I3  membership qualification                    NEXT
I4  snapshot construction                       BLOCKED BY I3
I5  deterministic aggregate                     BLOCKED BY I4
I6  browser + CLI                               BLOCKED BY I5
I7  bounded real local acceptance               BLOCKED BY I6
```

---

## 8. Stop lines during I3

Do not:

- implement snapshot construction or aggregate calculation early;
- build browser/report UI;
- auto-accept P1.6;
- make Capability/Work mandatory;
- invent repost similarity thresholds;
- promote membership to Canonical Registry/P2.2C/P2.2D;
- add trends/emerging/forecasting;
- add personal readiness/gap/scoring/recommendations;
- publish Market state to `corpus/`;
- add generic workflow/vector/RAG/graph/agent infrastructure.

---

## 9. Parallel portfolio/release state

Still pending:

```text
GitHub description/topics
real browser screenshots + privacy review
intentional v0.1.0 release
owner mastery verification
```

This does not change the I3 product frontier.
