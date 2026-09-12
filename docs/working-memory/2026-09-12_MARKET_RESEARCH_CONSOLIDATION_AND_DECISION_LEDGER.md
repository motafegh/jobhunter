# Market Research Consolidation and Decision Ledger

**Date:** 2026-09-12  
**Status:** PRE-INVESTIGATION CONSOLIDATION / IMPLEMENTATION NOT AUTHORIZED  
**Branch:** `main`  
**Controlling future plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Current product gate:** P2.2B-B1 remains open; the formal Market foundation investigation remains queued until B1 closes

## 1. Purpose

This record consolidates the bounded Market / Role-Family Intelligence research completed while the machine-local B1 work was postponed.

Its purpose is to prevent the later formal foundation investigation from repeating questions that have already been answered well enough at design level.

Use four states:

```text
DECIDED      strong design input; do not reopen without contradictory repository/real-data evidence
PROVISIONAL  preferred design; confirm during the formal post-B1 investigation
OPEN         requires repository/real-data evidence or a bounded experiment
DEFERRED     intentionally outside the first Market vertical slice
```

This document does not start the formal investigation, close B1, or authorize Market-v2 source implementation.

---

## 2. Research basis

Consolidated records:

```text
docs/working-memory/2026-09-07_LOCAL_RUNTIME_PAUSE_AND_REMOTE_MARKET_RESEARCH.md
docs/working-memory/2026-09-07_MARKET_TARGET_RELEVANCE_DEDUP_TREND_RESEARCH.md
docs/working-memory/2026-09-07_MARKET_REPORT_INTELLIGENCE_CONTRACT_RESEARCH.md
docs/working-memory/2026-09-07_MARKET_INCREMENTAL_ORCHESTRATION_REUSE_RESEARCH.md
docs/working-memory/2026-09-07_MARKET_PERSISTENCE_SNAPSHOT_ARTIFACT_RESEARCH.md
docs/working-memory/2026-09-08_MARKET_FIRST_SLICE_ACCEPTANCE_TESTING_STRATEGY.md
```

External reference families included ESCO, O*NET, Cedefop/JRC/ILO/OECD, Lightcast methodology references, and general state-aware build/orchestration patterns. These sources informed methodology only; none becomes JobHunter authority or a runtime dependency by default.

---

# 3. DECIDED — carry forward without rediscovery

## D1 — Market output is scoped online-job-ad intelligence, not a labour-market census

The report must expose source scope, target/search scope, processing coverage, sample size, employer breadth/concentration, duplicate policy, and important missing/stale evidence.

Do not describe a qualified Jobinja snapshot as the complete labour market.

## D2 — Stable target identity and immutable target-definition versions are separate

Use the conceptual split:

```text
TargetMarket
→ TargetMarketDefinitionVersion
```

A user-recognizable target may evolve without rewriting what an old snapshot meant.

## D3 — Acquisition envelope and market-membership meaning are separate

Permanent distinction:

```text
search vocabulary / acquisition envelope
!=
target-market membership truth
!=
canonical role taxonomy
```

Search terms optimize bounded recall. Membership must consider actual work/requirements/context.

## D4 — Market orchestration reuses existing artifact/currentness machinery

Do not create a second cache, invalidation engine, source identity model, translation pipeline, or P1.6 store.

Market should compose existing dependency identities and process only affected work:

```text
source semantic version
→ English projection
→ accepted/current P1.6
→ optional Capability / Work when actually required
→ target membership
→ snapshot
→ aggregate
```

## D5 — Eligibility and semantic relevance are staged

Use cheap deterministic eligibility for facts that are truly deterministic, then semantic reasoning only when role/work relevance requires interpretation.

Interpretive uncertainty is a soft state, not an integrity failure.

## D6 — Explicit denominators are mandatory

Never report a percentage without the denominator semantics being recoverable.

At minimum distinguish where relevant:

```text
discovered candidates
current parsed/source-eligible postings
relevance-qualified postings
accepted-current P1.6 postings
raw advertisements
approved unique-demand units
distinct employers
```

`qualified jobs` and `semantically accepted jobs` are not interchangeable.

## D7 — Raw advertisements and unique demand units are different quantities

Repeated observation of one stable source job is already one logical posting.

Future repost/new-ID handling must preserve:

```text
all source advertisements
→ explicit duplicate/repost relationship/disposition
→ approved unique-demand-unit denominator
```

Deduplication must not delete evidence.

## D8 — Point-in-time snapshots are historical authority

Old Market states must not be reconstructed from today's mutable/current database view.

A frozen snapshot must preserve exact target/version, member/source-version identities, effective membership and dedup policies, semantic coverage/dependencies, denominator semantics, and relevant warnings.

Historical snapshots remain immutable when source jobs, contracts, or target definitions later change.

## D9 — Numeric aggregation is application-owned and deterministic

Counts, shares, distinct-employer support, strength distributions, concentration, denominator bookkeeping, and approved duplicate adjustment are deterministic responsibilities.

Models may interpret aggregate facts; they must not author or repair numeric prevalence.

## D10 — Report dimensions remain semantically separate

Do not flatten the market into one `top skills` list.

The report should keep useful separation among:

```text
responsibilities / work
technologies / tools / platforms / languages
applied technical capabilities
knowledge areas
practices / methods
professional capabilities
experience / seniority
education / credentials
work arrangement / context
```

A tool mention is not automatically an applied capability. Knowledge is not automatically demonstrated work.

## D11 — Vacancy-specific requirement strength remains JobHunter semantics

Keep P1.6:

```text
required | preferred | contextual | inferred
```

Do not equate these with external occupation-taxonomy semantics such as ESCO `essential/optional`.

## D12 — Candidate role subfamilies should be work-led, not title-led

Candidate subfamily reasoning should primarily use recurring accepted responsibilities/work and requirement/capability bundles. Titles are supporting evidence.

Candidate subfamilies remain analytical interpretation and do not silently become canonical archetypes.

## D13 — Candidate interpretation does not require canonical promotion

Use the existing epistemic rule:

```text
candidate analytical interpretation
!=
reviewed/promoted reusable taxonomy
```

Human review is mainly a promotion boundary. The first useful report must not wait for exhaustive canonical responsibility/family/archetype promotion.

## D14 — The first Market vertical slice is intentionally narrow

Preferred smallest useful durable slice:

```text
TargetMarket + immutable definition version
→ MarketResearchRun
→ MarketJobMembership
→ MarketCorpusSnapshot
→ deterministic MarketAggregateProfile
```

A persisted model-generated `RoleFamilyIntelligenceReport` becomes necessary only when semantic report/subfamily synthesis is introduced.

## D15 — Persistence references upstream authority rather than copying it

Market records should point to exact existing source/translation/P1.6/other artifact identities rather than duplicate complete upstream payloads into Market tables/JSON.

Keep SQLite as the runtime/history store.

## D16 — Partial success and affected-work visibility are product requirements

A Market run should expose enough stage ledger information to distinguish, where applicable:

```text
requested
eligible
attempted
completed
reused
failed
pending/review-needed
remaining
```

One failed source/model operation must not erase successful durable work.

## D17 — P1.6 acceptance remains an authority boundary

Fresh P1.6 artifacts remain `pending` until accepted under the existing contract.

The Market layer must expose separate counts for:

```text
qualified source jobs
qualified jobs with accepted-current P1.6
qualified jobs with pending P1.6
qualified jobs missing P1.6
```

Do not weaken P1.6 acceptance merely to increase Market coverage.

## D18 — First-slice test philosophy is already defined

Use three evidence tiers:

```text
Tier 1: compact synthetic deterministic mini-market
Tier 2: curated repository-safe semantic boundary cases
Tier 3: bounded real local target run
```

Exact invariants get exact assertions. Semantic tests protect dangerous authority/boundary failures and tolerate safe prose/label variation.

## D19 — Initial external taxonomies are references, not dependencies

ESCO/O*NET may later help with optional crosswalks, aliases, comparison, or validation.

Do not force a target into one external occupation code and do not add external-taxonomy infrastructure before a concrete first-slice need is demonstrated.

## D20 — Market state remains local by default

Do not publish Market/Work/Registry/personal state into `corpus/` without a separate privacy/publication decision.

---

# 4. PROVISIONAL — confirm, do not redesign from zero

## P1 — Membership dispositions

Preferred initial vocabulary:

```text
core_match
adjacent_match
uncertain
excluded
```

Confirm exact semantics and persistence naming during the formal audit.

## P2 — Primary denominator policy

Strong current hypothesis:

```text
primary semantic prevalence → approved core members with accepted-current P1.6
reported separately         → adjacent / uncertain / incomplete semantic coverage
```

Confirm against real target cases rather than treating this as universal by fiat.

## P3 — Exact `TargetMarketDefinitionVersion` fields

The stable conceptual split is decided, but the precise first-slice fields remain to be confirmed from existing search/config owners and one representative target.

## P4 — Membership semantic input

Confirm the lowest sufficient evidence for target relevance:

- title + parsed source fields;
- English projection when needed;
- accepted P1.6 when available/necessary;
- optional Work/Capability only if they add measured value.

Do not make Capability/Work corpus-wide prerequisites without evidence.

## P5 — Duplicate/repost persistence boundary

Confirm the smallest representation:

```text
reusable duplicate/repost artifact
vs
snapshot/run-scoped grouping result
```

Avoid a global duplicate ontology unless repeated reuse justifies it.

## P6 — Semantic membership review/correction UX

Obvious low-risk candidate interpretation should not require manual approval. Borderline cases should remain inspectable/correctable where useful.

The exact review state/UI remains to be designed.

## P7 — Persisted semantic report timing

The first deterministic slice may render directly from `MarketAggregateProfile`. Persist `RoleFamilyIntelligenceReport` once semantic synthesis exists and its nondeterministic output must be recoverable exactly.

## P8 — First-slice semantic qualification placement

If deterministic/source eligibility alone cannot produce a useful representative target corpus, include bounded semantic relevance in the first slice. Otherwise add it immediately after the deterministic substrate.

---

# 5. OPEN — requires evidence, code audit, or bounded experiment

## O1 — Real acquisition recall/noise for a representative target

Test existing search profiles/packs and bounded search vocabulary against one representative target.

Questions:

- Does existing search configuration provide adequate candidate recall?
- How much obvious noise appears?
- Which target fields genuinely need a new domain object rather than config reuse?

## O2 — Membership qualification quality

Build/evaluate a compact representative set containing clear core, adjacent, misleading keyword/title, sparse, hybrid, and genuinely uncertain cases.

Evaluate:

- title-only failure avoidance;
- evidence-grounded reasons;
- false confident inclusion/exclusion;
- useful use of `uncertain`;
- whether accepted P1.6 materially improves the decision enough to justify dependency.

Do not optimize for a fake single accuracy number on a tiny sample.

## O3 — Same-source repost/new-ID policy on real Jobinja evidence

Find a bounded set of real candidate repost/near-duplicate examples and determine which observable features justify:

```text
same demand unit
separate requisition
uncertain relationship
```

No opaque global similarity threshold should become authority without evidence.

## O4 — P1.6 review throughput at Market scale

The existing accepted-only boundary is correct, but a useful Market target may contain many pending/missing P1.6 jobs.

Investigate the operational product question:

> How can JobHunter provide useful partial Market intelligence while preserving accepted-only strong semantic statistics and making review backlog explicit?

Do not solve this by auto-acceptance.

## O5 — Minimal first-slice persistence/schema fit

Audit existing SQLite owners/migration patterns and prove the smallest relational shape for target/version/run/membership/snapshot/profile without introducing redundant authority or generic framework abstractions.

## O6 — Market-run orchestration wiring

Audit `phase1_run`, sync, translation, P1.6, browser operations and CLI entrypoints to decide whether Market should compose existing services directly or needs one thin target-aware coordinator.

The default hypothesis is one thin coordinator, not a workflow framework.

## O7 — Real product usefulness of the deterministic first report

On one bounded local target, verify whether the initial report actually answers useful questions such as:

```text
What work recurs?
What requirements recur and at what strength?
How broad is employer support?
What evidence is missing or incomplete?
```

This product check decides whether semantic narrative/subfamily synthesis belongs in the same increment or the next one.

---

# 6. DEFERRED — outside the first vertical slice

Do not pull these into the first implementation simply because the future product may need them:

```text
longitudinal trend claims until comparable snapshots exist
`emerging` labels until multiple comparable windows support them
forecasting / predictive labour-market claims
fixed core/common/specialized demand thresholds before evidence justifies them
stable reusable role-archetype promotion
responsibility-family promotion merely to make the report work
Market → You personal readiness/gap/scoring/recommendations
salary benchmarking without adequate source coverage
second-source generic plugin architecture
cross-source duplicate machinery before a second source exists
external-taxonomy ingestion/crosswalk infrastructure without a concrete need
vector/RAG/graph infrastructure
agent orchestration framework
exhaustive canonical mapping
automatic P1.6 acceptance
public Market corpus/export without separate privacy/publication approval
```

---

## 7. Transition rule after B1 closure

When P2.2B-B1 closes:

1. re-read the final B1 decision and reconcile any effect on responsibility correspondence/family reuse;
2. load this consolidation record plus `docs/MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md`;
3. run the bounded formal foundation investigation only;
4. produce one dated investigation decision record resolving the remaining provisional/open items needed for the first slice;
5. authorize implementation only if that investigation yields a coherent minimal vertical slice and explicit acceptance boundaries.

Do not perform a second broad external-research cycle unless a concrete unresolved question actually requires it.

---

## 8. Current consolidated state

```text
Market broad design research          COMPLETE ENOUGH / STOP
Market decision consolidation         COMPLETE
formal foundation investigation       QUEUED BEHIND B1 / NOT STARTED
Market source implementation          NOT AUTHORIZED
first implementation slice            DEFINED PROVISIONALLY / NOT AUTHORIZED
local B1 execution                    STILL REQUIRED WHEN OWNER RUNTIME ACCESS RETURNS
```
