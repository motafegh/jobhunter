# Market / Role-Family Foundation Investigation Entry Plan

**Status:** EXECUTED / CLOSED — FOUNDATION PASS / FIRST VERTICAL SLICE AUTHORIZED  
**Original date:** 2026-09-12  
**Executed:** 2026-09-14  
**Branch:** `main`  
**Controlling parent:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Research input:** `docs/working-memory/2026-09-12_MARKET_RESEARCH_CONSOLIDATION_AND_DECISION_LEDGER.md`  
**Final decision:** `docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

## 1. Lifecycle / execution result

This file was the prepared entry protocol for the formal Market / Role-Family foundation investigation. Its activation condition was satisfied when P2.2B-B1 closed as **NO-PROMOTION / DEFER** on 2026-09-14.

The protocol has now been executed.

Final result:

```text
FOUNDATION INVESTIGATION: PASS
FIRST VERTICAL SLICE: AUTHORIZED
```

The current next action is **not another investigation**. It is implementation increment **I1 — Market domain models + SQLite persistence**, under the exact scope and stop lines recorded in the final decision.

This file remains a closed protocol/evidence record. The final decision owns current Q1–Q12 answers and implementation authorization.

---

## 2. Original investigation purpose

The protocol existed to convert six bounded research passes into one evidence-based decision exercise covering:

1. exact first-slice questions;
2. required repository/real-data evidence;
3. smallest experiments;
4. acceptance criteria;
5. implementation-authorization boundaries.

It deliberately prohibited production Market implementation until the foundation result explicitly said:

```text
FOUNDATION INVESTIGATION: PASS
FIRST VERTICAL SLICE: AUTHORIZED
```

That condition is now satisfied by the September 14 decision record.

---

## 3. Investigation principles that remain useful implementation history

### Preserve prior research decisions

The investigation started from the consolidation ledger's `DECIDED` items and reopened them only where repository/real evidence materially required it.

Broad ESCO/O*NET/Cedefop/OECD/Lightcast research was not repeated merely for completeness.

### Prefer existing owners

The protocol required auditing/reusing:

```text
search/config/acquisition
source identity/version/lifecycle
translation
accepted P1.6
Capability
Work Intelligence
Canonical Registry
current Market read model
browser operations
CLI
SQLite migration/store patterns
```

The final decision confirmed a thin extension of these owners rather than a parallel platform.

### Keep authority split explicit

```text
hard integrity/currentness/count/persistence
→ deterministic application evidence/tests

role relevance / semantic interpretation
→ bounded semantic evaluation with evidence and uncertainty
```

Interpretive uncertainty is not an infrastructure failure.

---

# 4. Q1–Q12 protocol and resolved outcome pointer

The original protocol asked the following questions. Their authoritative answers now live in the final decision record.

## Q1 — Smallest target-definition contract

Resolve stable `TargetMarket` identity versus immutable `TargetMarketDefinitionVersion`, acquisition references, membership intent, target constraints, and run-only budgets.

**Resolved:** stable target + immutable definition version; operational budgets belong to `MarketResearchRun` rather than silently changing semantic target identity.

## Q2 — Target-run reuse and orchestration

Resolve how one target run composes existing discovery/sync, source currentness, translation, P1.6, bounded budgets and partial-success state.

**Resolved:** one thin target-aware coordinator over existing owners; target-scoped affected-work queues are required so bounded budget does not spill into unrelated global backlog.

## Q3 — Source-level snapshot eligibility

Resolve lifecycle/currentness/fetch-failure/freshness behavior.

**Resolved:** successfully parsed current source evidence is required; failed refresh is not disappearance; expired/removed postings stay historical but leave the active primary corpus; weak/retryable availability failures retain prior evidence subject to freshness/warnings.

## Q4 — Target-market membership evidence

Resolve deterministic eligibility, semantic relevance, evidence dependencies and dispositions.

**Resolved:**

```text
core_match
adjacent_match
uncertain
excluded
```

Current parsed source + title/English evidence can establish source-level membership. Accepted P1.6 is optional stronger evidence, not a membership prerequisite. Capability/Work are not first-slice gates.

## Q5 — P1.6 acceptance coverage

Resolve how a useful Market view survives incomplete accepted-semantic coverage without weakening P1.6 authority.

**Resolved:** source-level core membership and accepted-P1.6 semantic prevalence use separate explicit denominators. Accepted/pending/missing/failed/rejected processing state remains visible. Missing analysis never becomes zero demand.

## Q6 — Jobinja repost/new-ID policy

Resolve the smallest defensible same-demand policy from real evidence.

**Resolved for v1:** automatic new-ID collapse is deferred because the investigation did not establish a defensible real pair set. Use `qualified source postings`, disclose the limitation, and do not claim `unique demand units`.

## Q7 — Minimum persistence model

Resolve identity, mutability, history, dependency and recomputation rules.

**Resolved conceptual first-slice owners:**

```text
market_targets
market_target_definition_versions
market_research_runs
market_job_memberships
market_corpus_snapshots
market_corpus_snapshot_members
market_aggregate_profiles
```

SQLite remains the runtime/history store. Definition versions, snapshots and profiles are immutable history artifacts.

## Q8 — First deterministic aggregate profile

Resolve evidence-quality header, requirement/work metrics, denominators, employer breadth and drill-down.

**Resolved:** deterministic profile over the frozen target snapshot with explicit source and accepted-P1.6 denominators, employer concentration, requirement type/strength support and evidence drill-down. No opaque demand score/bands/trends.

## Q9 — Capability / Work dependency

**Resolved:** neither is mandatory in the first slice. Reviewed Registry mappings may enrich where available; unmapped evidence remains valid.

## Q10 — Semantic role-subfamily synthesis

**Resolved:** defer from the first slice. First prove the deterministic target corpus/profile. Any later synthesis is candidate/non-canonical and should operate at report/aggregate level rather than generating one narrative per job.

## Q11 — Browser/CLI repeated-use workflow

**Resolved:** browser remains primary and reuses the existing one-mutable-operation pattern; CLI exposes the same services/state for inspection/automation/debugging. Market runtime state remains local by default.

## Q12 — First-slice acceptance gate

**Resolved:** exact deterministic/store/service/semantic-boundary/browser/CLI invariants are recorded in the final decision. A bounded real local target run remains required before implementation closure.

---

# 5. Evidence owners inspected by the executed investigation

The investigation inspected the current responsibilities needed for its decisions, including:

```text
src/jobhunter/search_registry.py
src/jobhunter/config.py
src/jobhunter/jobinja_sync.py
src/jobhunter/job_detail_observations.py
src/jobhunter/lifecycle.py
src/jobhunter/storage.py
src/jobhunter/translation_service.py
src/jobhunter/analysis_store.py
src/jobhunter/phase1_run.py
src/jobhunter/market_insights.py
src/jobhunter/work_intelligence_service.py
src/jobhunter/canonical_registry.py
src/jobhunter/web/operations.py
src/jobhunter/cli.py
```

Adjacent tests and representative public-corpus jobs/P1.6 artifacts were inspected rather than reading the repository indiscriminately.

The final decision records the evidence boundary: no new live Jobinja acquisition run was performed during this formal audit, so search-recall optimization is an implementation-acceptance concern rather than a fabricated investigation result.

---

# 6. Executed bounded experiments/evidence

## E1 — Target/search contract

Existing bilingual/versioned search profiles/packs plus current config were sufficient to establish the target/acquisition contract. Live recall/noise optimization remains a bounded real-run acceptance task.

## E2 — Membership boundary set

Representative repository-safe cases demonstrated:

```text
ta9l  → clear Applied-AI core despite missing accepted P1.6
tG9K  → clear Applied-ML core with accepted rich P1.6
tGM0  → adjacent backend/AI-platform work
t4jp  → misleading AI title; content-production role
tmBK  → Python/backend role with AI-usage qualification only
t4qV  → network-security role
tmyX  → Microsoft infrastructure-security role
```

This established that title-only classification is unsafe and accepted P1.6 should not gate source-level membership.

## E3 — Repost/new-ID evidence

No credible bounded real pair set was established. Per protocol, automatic repost adjustment was explicitly deferred rather than simulated into authority.

## E4 — P1.6 coverage/backlog

Current analysis-store semantics plus the real B1 `ta9l` result proved the need to distinguish accepted/pending/missing/failed/rejected semantic coverage from source-level target membership.

## E5 — Schema/dependency walk

The proposed relational responsibilities survived unchanged rerun, new source version, new target definition, new membership contract and new aggregate contract without requiring historical rewrites or unrelated upstream invalidation.

## E6 — Deterministic report/read-model

Current `MarketInsights` already proves deterministic requirement-strength counts, employer concentration/sample warnings and explicit scope/duplicate disclosures. The target-scoped first profile extends those responsibilities over a frozen membership snapshot.

---

# 7. Acceptance criteria result

The investigation passed because it resolved the integrity architecture needed before implementation:

- explicit first-slice product question;
- stable target and immutable definition-version responsibilities;
- existing source identity/provenance reuse;
- target-scoped affected-work model;
- source eligibility without treating fetch failure as disappearance;
- explicit membership states and primary denominator;
- lowest sufficient membership evidence;
- explicit accepted/pending/missing P1.6 coverage;
- repost policy explicitly deferred with claim limitations;
- bounded SQLite persistence shape;
- explicit deterministic metric denominators;
- Capability/Work included only when later evidence demonstrates value;
- subfamily synthesis deferred from v1;
- coherent browser/CLI workflow;
- bounded implementation test matrix;
- local/private publication boundary;
- no unresolved integrity issue that would corrupt identity, history, denominator truth or currentness.

Semantic uncertainty remains allowed. Integrity ambiguity does not.

---

# 8. Implementation authorization

The final decision authorizes this exact slice:

```text
TargetMarket
+ TargetMarketDefinitionVersion
+ MarketResearchRun
+ MarketJobMembership
+ MarketCorpusSnapshot + members
+ MarketAggregateProfile
+ minimal browser/CLI workflow
```

Implementation sequence:

```text
I1 domain models + SQLite persistence
→ I2 target-scoped source eligibility / affected-work planning
→ I3 membership qualification
→ I4 immutable snapshot
→ I5 deterministic aggregate profile
→ I6 browser + CLI workflow
→ I7 bounded real local acceptance
```

The current next action is **I1**.

---

# 9. Non-goals that remain outside the authorization

```text
longitudinal trends / `emerging`
forecasting
fixed demand bands
stable role archetypes
responsibility-family promotion for reporting
semantic role-subfamily synthesis in v1
persisted model-generated Role-Family Intelligence Report in v1
Market → You scoring/recommendations
salary benchmarking
second-source plugin abstraction
cross-source duplicate system
external-taxonomy ingestion infrastructure
vector/RAG/graph platform
agent/workflow framework
exhaustive canonicalization
automatic P1.6 acceptance
public Market corpus/export
```

---

## 10. Closed transition state

```text
broad Market research                  COMPLETE ENOUGH
research consolidation                 COMPLETE
foundation investigation protocol      EXECUTED / CLOSED
foundation investigation               PASS
first vertical slice                   AUTHORIZED
current next action                    I1 DOMAIN + SQLITE PERSISTENCE
```

For implementation details, use the final foundation decision rather than reopening this protocol.
