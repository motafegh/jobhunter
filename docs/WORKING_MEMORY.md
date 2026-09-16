# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-09-16  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current product gate:** MARKET I1 ACCEPTED / I2 NEXT  
**P2.2B-B1:** CLOSED — NO-PROMOTION / DEFER  
**Parallel portfolio:** MIT complete; GitHub metadata + screenshots + release + owner mastery pending

## 1. Read this first

Current status authority:

`docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`

Current Market design authority:

`docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`

Foundation result:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

Latest implementation/acceptance record:

`docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md`

Execution checklist:

`docs/EXECUTION_TODO.md`

Do not follow older `I1 NEXT`, open-B1, or pre-foundation instructions when they conflict with these current owners.

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
Blueprint:                  historical / experimental / non-authoritative
```

Accepted/current P1.6 → Capability anchors:

```text
tG9K 36 → 11
t4jp 37 → 12
tmBK 39 → 13
t4qV 44 → 14
tmyX 46 → 15
```

Public corpus remains:

```text
353 known/discovered jobs
43 fetched/parsed details
21 current English projections
5 accepted/current English P1.6
5 accepted/current Capability
```

B1 is closed as NO-PROMOTION / DEFER. Do not repeat the `ta9l` extraction/model matrix merely to force responsibility promotion.

---

## 3. Market foundation state

Formal decision:

```text
FOUNDATION INVESTIGATION: PASS
FIRST VERTICAL SLICE: AUTHORIZED
```

Authorized first slice:

```text
TargetMarket
+ immutable TargetMarketDefinitionVersion
+ thin target-aware MarketResearchRun coordinator
+ MarketJobMembership
+ immutable MarketCorpusSnapshot + members
+ deterministic MarketAggregateProfile
+ thin browser/CLI workflow
```

Permanent first-slice boundaries:

- Jobinja remains the only approved recurring source.
- search/acquisition recall is not target membership truth.
- `core_match / adjacent_match / uncertain / excluded` remain distinct.
- primary target corpus is core only.
- accepted P1.6 is not required for source-level membership.
- accepted P1.6 is required for strong semantic prevalence statistics.
- Capability and Work are optional enrichments, not gates.
- missing/pending/failed P1.6 is not zero demand.
- automatic repost/new-ID collapse remains deferred; say `qualified source postings`, not `unique demand units`.
- semantic role-subfamily synthesis, trends and personal intelligence remain outside the first slice.
- Market state remains local/private by default.

---

## 4. I1 domain + SQLite persistence — ACCEPTED / CLOSED

Implementation:

```text
src/jobhunter/market_models.py
src/jobhunter/market_store.py
tests/test_market_store.py
tests/test_market_i1_invalidation.py
```

I1 established these durable runtime/history boundaries:

```text
market_targets
market_target_definition_versions
market_research_runs
market_job_memberships
market_corpus_snapshots
market_corpus_snapshot_members
market_aggregate_profiles
```

### Accepted I1 behavior

- `TargetMarket` is stable identity; display metadata may evolve.
- definition versions are canonicalized, fingerprinted and immutable.
- same normalized definition reuses its version; semantic changes create a new version.
- target-definition changes do not invalidate generic source/translation/P1.6 artifacts.
- research runs preserve exact target definition, controls and a partial-success ledger.
- membership reuse is keyed by exact target/source/classifier/artifact dependency identity.
- membership decisions are immutable; correction creates a new superseding record.
- membership may consume P1.6 only when it is from the exact chain and accepted.
- snapshot/member history is immutable.
- snapshot semantic coverage records `accepted / pending / missing / failed / rejected` separately.
- only `core_match` is persisted as primary-corpus inclusion at the I1 state layer.
- aggregate-profile persistence is immutable and deterministic over exact snapshot + contract.
- conflicting deterministic replay for the same snapshot/contract is an integrity failure.

Contracts introduced:

```text
market-corpus-snapshot-v1
market-aggregate-profile-v1
```

Final I1 technical evidence:

```text
code/test head: f0cded55a9887c061898d0dcab7f5e6b10300d8e
CI: 1160 / 35108236384
Ruff: PASS
pytest: PASS
pytest -W error: PASS
```

I1 does not yet make a real target run, decide lifecycle eligibility, classify target membership, calculate the aggregate profile, or expose a browser/CLI Market workflow.

---

## 5. Exact next action — I2 only

I2 responsibility:

**Target-scoped source eligibility + affected-work planning.**

The problem to solve is narrower than full Market orchestration:

> Given one immutable target definition and the existing JobHunter source/runtime state, determine exactly which target candidates are source-eligible and which target-scoped source/translation/P1.6 work is missing or stale—without spilling run budget into unrelated global backlog and without confusing refresh failure with disappearance.

### I2 must inspect/reuse

At minimum:

```text
search_registry.py / config search definitions
jobinja_discovery.py
jobinja_sync.py
jobinja_batch.py
job_catalog.py
job_detail_observations.py
lifecycle.py
storage.py
translation_service.py / translation_store.py
analysis currentness/store/service owners
phase1_run.py as orchestration precedent only
market_models.py / market_store.py from I1
```

### I2 must decide/implement

- one target-scoped candidate/source-state representation;
- deterministic source eligibility from current parsed source + lifecycle/freshness evidence;
- target-only missing-detail selection;
- target-only refresh-due selection;
- target-only translation affected-work selection;
- target-only P1.6 affected-work selection;
- exact reuse state for already-current artifacts;
- explicit unavailable/failure/remaining counts suitable for the later Market run ledger;
- no semantic target-membership inference yet.

### I2 critical regression boundary

Existing global Phase-1 helpers may use preferred IDs and then fill remaining budget from the global backlog. That behavior is useful for global maintenance but **must not be reused blindly for a target Market run**.

I2 should prove target runs cannot consume unrelated jobs merely because budget remains.

### Lifecycle rule

```text
failed refresh != disappearance
```

Network/rate-limit/challenge/auth/server failures remain non-destructive evidence. `expired` / confirmed `removed` state is different from a failed check.

---

## 6. First-slice sequence after I1

```text
I1  domain + persistence                         ACCEPTED
I2  target source eligibility / affected work   NEXT
I3  membership qualification                    BLOCKED BY I2
I4  snapshot construction                       BLOCKED BY I3
I5  deterministic aggregate                     BLOCKED BY I4
I6  browser + CLI                               BLOCKED BY I5
I7  bounded real local acceptance               BLOCKED BY I6
```

Do not jump to I3/I4/I5 because I1 already contains their persistence records. Persistence capability is not the same as accepted service behavior.

---

## 7. Stop lines

Do not during I2:

- implement semantic `core/adjacent/uncertain/excluded` classification;
- assemble production Market snapshots;
- calculate final Market aggregates;
- build browser/report UI;
- auto-accept P1.6;
- make Capability/Work corpus-wide gates;
- invent repost similarity thresholds;
- start P2.2C/P2.2D promotion;
- add trends/emerging/forecasting;
- add personal readiness/gap/scoring/recommendations;
- publish Market state to `corpus/`;
- add generic workflow/vector/RAG/graph/agent infrastructure.

---

## 8. Parallel portfolio/release state

Still pending:

```text
GitHub description/topics
real browser screenshots + privacy review
intentional v0.1.0 release
owner mastery verification
```

This parallel track does not change the I2 product frontier.
