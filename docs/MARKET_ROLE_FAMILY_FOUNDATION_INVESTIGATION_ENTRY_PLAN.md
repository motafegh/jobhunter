# Market / Role-Family Foundation Investigation Entry Plan

**Status:** PREPARED / QUEUED BEHIND P2.2B-B1 / NOT ACTIVE YET  
**Date:** 2026-09-12  
**Branch:** `main`  
**Controlling parent:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Consolidated research input:** `docs/working-memory/2026-09-12_MARKET_RESEARCH_CONSOLIDATION_AND_DECISION_LEDGER.md`  
**Current product gate:** P2.2B-B1 remains open; this plan does not authorize the formal investigation or Market-v2 implementation before B1 closure

## 1. Purpose

This is the ready-to-use entry protocol for the formal Market / Role-Family Intelligence foundation investigation that is already owner-approved to begin after P2.2B-B1 closes.

It converts the broad investigation queue and six research passes into one bounded decision exercise with:

1. exact questions;
2. required repository/real-data evidence;
3. smallest experiments;
4. acceptance criteria;
5. implementation-authorization boundaries.

The objective is **not** to design the entire future Market system. It is to decide the smallest trustworthy first Market vertical slice and whether repository evidence is sufficient to implement it.

---

## 2. Activation condition

Do not execute this investigation while B1 remains open.

Activate immediately after one of these recorded B1 outcomes:

```text
B1 PASS
→ one reviewed responsibility concept + two accepted/current P1.6 mappings

B1 NO-PROMOTION / DEFER
→ bounded evidence insufficient or selected correspondence rejected
```

Either B1 outcome is compatible with starting Market foundation investigation.

At activation time:

1. read the final B1 decision record;
2. reconcile only the Market questions affected by that result;
3. do not require P2.2C responsibility families or P2.2D stable role archetypes before useful Market work;
4. keep candidate analytical role/work families distinct from promoted reusable taxonomy.

No second owner activation ceremony is required merely to start this already-approved investigation after B1 closure.

---

## 3. Investigation rules

### 3.1 Preserve decided research conclusions

Start from the consolidation ledger's `DECIDED` items. Reopen them only if code or real evidence materially contradicts them.

Do not repeat broad ESCO/O*NET/Cedefop/OECD/Lightcast research merely for completeness.

### 3.2 Prefer code/evidence inspection over speculative redesign

Use existing JobHunter owners first:

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

Add a new owner only where the first vertical slice has a real responsibility that no existing owner can safely represent.

### 3.3 Keep the investigation bounded

The investigation should produce decisions, small evidence tables, and at most the minimal prototypes/throwaway analyses needed to answer open questions.

It must not drift into production implementation.

### 3.4 Authority split

```text
hard integrity/currentness/count/persistence questions
→ deterministic evidence and exact tests

role relevance / candidate work-family interpretation
→ semantic evaluation with evidence and uncertainty
```

Do not convert interpretive uncertainty into an infrastructure or review blocker.

---

# 4. Exact investigation questions

## Q1 — What is the smallest first-slice target-definition contract?

Resolve:

- stable target identity fields;
- immutable definition-version fields;
- which existing search profile/pack/config references can be reused;
- which membership-intent fields must be represented independently from acquisition search terms;
- which geography/seniority/employment/freshness constraints belong in v1;
- which request/page/detail/model budgets are target/run controls rather than durable semantic identity.

Expected decision:

```text
minimal TargetMarket
minimal TargetMarketDefinitionVersion
```

Do not design every possible future target dimension.

## Q2 — How should one target run reuse acquisition and derived artifacts?

Resolve:

- existing discovery/sync entrypoint reuse;
- target-aware candidate selection without parallel source identities;
- missing vs refresh-due detail selection;
- current English projection reuse;
- accepted/current P1.6 reuse;
- whether one thin `MarketResearchService`/coordinator is sufficient;
- stage ledger and bounded budgets;
- partial-success terminal states.

Expected decision:

```text
existing services + thin target-aware coordinator
```

unless concrete evidence proves another boundary necessary.

## Q3 — Which jobs may enter a snapshot at source level?

Define deterministic source/corpus eligibility for:

- active/current source jobs;
- stale/unchecked jobs;
- explicit expiry/removal;
- failed refresh attempts;
- incomplete details;
- changed semantic source version;
- native-English vs translation-required source;
- target time/freshness window.

Critical rule:

```text
failed refresh != market disappearance
```

Expected output: one explicit source-eligibility table.

## Q4 — What evidence is sufficient for target-market membership?

Test the staged model:

```text
deterministic eligibility
→ semantic relevance when needed
```

Resolve:

- whether title + parsed source content is enough for obvious cases;
- when English projection is required;
- when accepted P1.6 materially improves classification;
- whether Capability/Work adds enough value to justify optional use;
- exact first-slice dispositions;
- evidence/reason fields;
- qualitative confidence, if useful;
- correction/review behavior;
- which dispositions enter which denominator.

Expected default vocabulary to confirm/refine:

```text
core_match
adjacent_match
uncertain
excluded
```

## Q5 — How should the first slice handle P1.6 acceptance coverage?

Resolve the operational gap between:

```text
qualified source jobs
and
qualified jobs with accepted-current P1.6
```

The investigation must answer:

- what useful source-level Market information can be shown before semantic coverage is complete;
- which aggregate sections require accepted P1.6;
- how pending/missing P1.6 backlog appears in the run/report;
- whether review prioritization can be target-aware without auto-acceptance;
- what constitutes a sufficiently useful first target run.

Do not weaken the existing P1.6 acceptance gate.

## Q6 — What is the smallest defensible repost/new-ID policy for Jobinja?

Using real or repository-safe Jobinja examples, distinguish:

```text
same logical source posting / repeated observation
repost or materially same hiring demand under a new source ID
separate requisition
uncertain near-duplicate
```

Resolve:

- evidence features used;
- whether the first slice needs model-assisted similarity at all;
- persistence location;
- representative unique-demand-unit rule;
- effect of uncertainty on denominators.

Do not build cross-source duplicate infrastructure while only Jobinja is approved.

## Q7 — What is the minimum Market persistence model?

Confirm/refine the provisional shape:

```text
TargetMarket
TargetMarketDefinitionVersion
MarketResearchRun
MarketJobMembership
MarketCorpusSnapshot + members
MarketAggregateProfile
```

For each, define:

- identity/key;
- mutability/history rule;
- exact upstream dependencies;
- reuse/currentness identity;
- minimum stored fields;
- indexes/constraints actually needed;
- migration strategy;
- what remains recomputable.

Do not add a separate storage engine.

## Q8 — What should the first deterministic aggregate profile contain?

Resolve the first useful set only:

```text
evidence/corpus quality
unique qualified postings/demand units
employer breadth/concentration
requirements by semantic type
required/preferred/contextual/inferred counts
accepted responsibilities/work evidence
explicit experience/seniority/education/context where supported
bounded evidence drill-down
```

Confirm exact denominator for every metric.

Do not introduce opaque importance scores or demand bands in v1.

## Q9 — Does the first slice need Capability or Work Intelligence as dependencies?

For each desired aggregate/report section, record:

```text
P1.6 sufficient
Capability adds material value
Work adds material value
not needed yet
```

Default assumption:

> P1.6 is the factual aggregate substrate; Capability/Work are optional enrichments and must not unnecessarily gate corpus coverage.

## Q10 — Where should semantic role-subfamily synthesis enter?

On one representative target, decide whether a deterministic aggregate alone already produces useful product value.

If not, define the smallest bounded candidate synthesis using:

```text
accepted recurring work/responsibilities
→ requirement/capability bundles
→ tools/knowledge/context
→ titles as supporting evidence
```

Do not promote candidate subfamilies into stable archetypes.

## Q11 — What browser/CLI workflow is the smallest coherent repeated-use path?

Define one shared-service workflow for:

```text
select/create target
→ preview bounds
→ run/refresh
→ inspect stage ledger
→ inspect membership/coverage
→ inspect aggregate report
→ drill down to source evidence
→ rerun and observe reuse
```

Browser remains primary. CLI remains inspection/automation/debugging.

## Q12 — What exact first-slice acceptance gate authorizes implementation completion?

Turn the existing testing strategy into an implementation-specific checklist after Q1-Q11 decisions are known.

Do not expand acceptance into later trend/personal/archetype responsibilities.

---

# 5. Required evidence

The formal investigation should inspect only evidence needed to answer Q1-Q12.

## 5.1 Repository owners

At minimum inspect current versions of:

```text
src/jobhunter/search_registry.py
src/jobhunter/config.py
src/jobhunter/jobinja_discovery.py
src/jobhunter/jobinja_sync.py
src/jobhunter/jobinja_batch.py
src/jobhunter/storage.py
src/jobhunter/job_detail_observations.py
src/jobhunter/translation_store.py
src/jobhunter/translation_service.py
src/jobhunter/analysis_store.py
current P1.6 service/currentness owners
src/jobhunter/capability_store.py
current Capability service/currentness owners
current Work Intelligence store/service owners
src/jobhunter/canonical_registry.py
src/jobhunter/market_insights.py
src/jobhunter/phase1_run.py
browser operation/service wiring
CLI entrypoints
```

Inspect tests adjacent to these owners rather than reading the whole test suite indiscriminately.

## 5.2 Existing real/repository-safe evidence

Use:

- current public corpus for bounded remote case selection;
- selected accepted P1.6 anchors;
- Work Intelligence accepted behavior where relevant;
- Canonical Registry seed and final B1 result;
- current Market aggregate behavior;
- existing discovery provenance/search-effectiveness records;
- local real runtime only for questions that repository-safe evidence cannot answer.

## 5.3 Research inputs

Load the consolidation record and consult the six research records only when a specific decision needs their detail.

Do not treat external methodology as stronger authority than JobHunter's source/evidence model.

---

# 6. Smallest experiments

The investigation is complete only when the genuinely open questions have evidence. Prefer the following bounded experiments.

## E1 — Representative target-definition/search experiment

Choose **one** real target market representative of the product goal.

Recommended type:

```text
AI Security / ML Security
```

or the best equivalent current target available when the investigation begins.

Compare a very small set of existing search profile/pack/term combinations.

Record:

```text
candidates discovered
obvious relevant examples
obvious noise
important missed known examples if detectable
request/page budget
which target-definition fields were actually necessary
```

Stop when the domain-contract question is answered; do not optimize search recall indefinitely.

## E2 — Membership boundary set

Use approximately 8-12 deliberately varied real or repository-safe cases:

```text
clear core / expected title
clear core / non-obvious title
adjacent technology-overlap role
misleading keyword/title hit
sparse evidence
hybrid role
two-subfamily plausible role
genuinely uncertain role
```

Compare the lowest sufficient inputs:

```text
title/source
vs
English/source semantic text
vs
accepted P1.6
```

Only test Capability/Work if Q9 still has concrete uncertainty.

Output: evidence table + recommended first-slice membership input/contract.

## E3 — Jobinja repost/new-ID mini-set

Find only enough real candidate pairs to establish the first policy boundary.

For each pair record:

```text
employer
title
location/time
source IDs
semantic/source similarity evidence
responsibility/requirement overlap where available
disposition: same demand / separate / uncertain
```

If no credible examples are available, explicitly defer sophisticated repost adjustment and keep strong prevalence claims correspondingly limited. Do not invent fixtures as proof of real source behavior.

## E4 — P1.6 coverage/backlog simulation

Using a small synthetic/repository-safe target snapshot, model:

```text
accepted P1.6
pending P1.6
missing P1.6
translation failure
stale semantic version
```

Verify the report/run can remain useful while denominators stay honest.

This is an orchestration/product-boundary experiment, not a semantic auto-acceptance experiment.

## E5 — Minimal schema sketch and dependency walk

Before source implementation, write the smallest table/domain sketch for Q7 and manually walk these changes through it:

```text
unchanged rerun
new source semantic version
new target-definition version
new membership contract
new aggregate contract
```

Reject any schema that requires rewriting immutable history or invalidates unrelated upstream artifacts.

## E6 — First-report product sketch

Using deterministic values from the bounded case set, produce one temporary structured report/read-model sketch and answer:

- Can the user see exactly what corpus was analyzed?
- Are denominators obvious?
- Are recurring work and requirements useful without semantic narrative?
- Is evidence drill-down clear?
- Is missing semantic coverage obvious?

This is a design/prototype artifact only. Do not create production UI during the investigation.

---

# 7. Investigation acceptance criteria

The formal foundation investigation passes only when all of these are true:

1. The exact first-slice product question is stated in one paragraph.
2. `TargetMarket` and definition-version responsibilities are explicit and minimal.
3. Acquisition reuses existing source identity/provenance and bounded sync behavior.
4. A target-aware affected-work/reuse model is explicit.
5. Source-level snapshot eligibility is defined without treating fetch failure as disappearance.
6. Membership disposition semantics and the primary denominator are explicit.
7. The lowest sufficient semantic evidence for membership is decided from representative cases.
8. Accepted/pending/missing P1.6 coverage remains visible and authority-safe.
9. The first same-source repost/new-ID policy is either evidence-backed or explicitly deferred with corresponding report limitations.
10. The minimal persistence/schema boundary is defined with immutable history/currentness rules.
11. Every first-slice aggregate metric has an explicit denominator and deterministic owner.
12. Capability/Work dependencies are included only where their value is demonstrated.
13. Candidate subfamily synthesis is either explicitly deferred or bounded as non-canonical interpretation.
14. One coherent browser/CLI workflow is defined over shared services/state.
15. The first implementation-test matrix is explicit and bounded.
16. Publication remains local/private by default.
17. Deferred responsibilities remain outside the implementation authorization.
18. No unresolved integrity question remains that could corrupt source identity, snapshot history, denominator truth, or dependency currentness.

The investigation may still pass with semantic uncertainty. It may not pass with unresolved integrity architecture.

---

# 8. Required investigation output

Produce **one** dated working-memory decision record containing:

```text
final first-slice product scope
Q1-Q12 decisions
experiment evidence/results
accepted domain/persistence/orchestration shape
membership + denominator policy
repost disposition/policy or explicit deferral
P1.6 coverage/review-throughput handling
first aggregate contract
Capability/Work reuse decision
semantic synthesis placement decision
browser/CLI workflow
implementation order
acceptance matrix
explicit non-goals
implementation authorization decision
```

Do not create one decision file per question unless a genuinely independent experiment needs its own raw evidence record.

---

# 9. Implementation authorization boundary

## 9.1 Not authorized by this prepared plan

While B1 remains open, do **not**:

```text
start the formal Q1-Q12 investigation
create Market runtime tables/migrations
write Market-v2 services
write target-membership model prompts/contracts
modify current Market behavior
build browser Market-v2 screens
run corpus-wide Market model inference
publish Market state
start P2.2C/P2.2D as a substitute
```

## 9.2 Authorized automatically after B1 closure

The already-owner-approved next action is:

```text
execute this bounded foundation investigation
→ record one dated decision result
```

No new permission is needed merely to perform that investigation unless repository state materially changes the owner-approved direction.

## 9.3 Implementation authorization after investigation

Implementation is authorized only when the formal decision record explicitly states:

```text
FOUNDATION INVESTIGATION: PASS
FIRST VERTICAL SLICE: AUTHORIZED
```

and names the exact slice.

A likely slice is:

```text
TargetMarket + definition version
→ run
→ membership
→ immutable snapshot
→ deterministic aggregate profile
→ minimal browser/CLI inspection
```

but this remains provisional until Q1-Q12 are resolved.

If the investigation exposes a material unresolved authority/data-integrity problem, record:

```text
FOUNDATION INVESTIGATION: HOLD
```

with the smallest next evidence task. Do not start source implementation around the uncertainty.

---

# 10. Explicit first-slice non-goals

Unless the formal investigation proves one is strictly necessary for basic correctness, keep these out:

```text
longitudinal trends / `emerging`
forecasting
fixed demand-band thresholds
stable role archetypes
responsibility-family promotion for reporting
Market → You personal scoring/recommendations
salary benchmarking
second-source abstraction/plugin framework
cross-source duplicate system
external taxonomy ingestion infrastructure
vector/RAG/graph platform
agent/workflow framework
exhaustive canonicalization
automatic P1.6 acceptance
public Market corpus/export
```

---

## 11. Prepared transition state

```text
broad Market research                  COMPLETE ENOUGH
research consolidation                 COMPLETE
formal investigation entry protocol    PREPARED
formal foundation investigation         QUEUED / BLOCKED BY OPEN B1
Market-v2 implementation                NOT AUTHORIZED
```
