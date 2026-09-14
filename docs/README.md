# JobHunter Documentation Map

This directory contains both **current product/engineering authority** and the project’s retained **execution, experiment, and decision history**.

The files are intentionally layered rather than treated as one flat set of equally current documents. Start here when browsing `docs/` as a developer or technical reviewer. AI assistants and contributors must still follow the controlling reading order in [`../AGENTS.md`](../AGENTS.md).

## 1. Read this first

For the current product and engineering model, use this sequence:

1. [`PRODUCT_SPECIFICATION.md`](PRODUCT_SPECIFICATION.md) — product purpose, allowed meaning, product boundaries, and intended long-term utility.
2. [`ARCHITECTURE.md`](ARCHITECTURE.md) — current implemented architecture, authority/data flow, persistence, failure semantics, and major tradeoffs.
3. [`DOMAIN_AND_ANALYSIS_MODEL.md`](DOMAIN_AND_ANALYSIS_MODEL.md) — domain entities and analytical semantics.
4. [`SOURCE_POLICY.md`](SOURCE_POLICY.md) — approved acquisition and source-authority rules.
5. [`UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`](UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md) — source fact, correspondence, interpretation, recommendation, and promotion boundaries.
6. [`ROADMAP.md`](ROADMAP.md) — strategic sequencing.
7. [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) — delivery order and implementation gates.
8. [`CURRENT_STATE_RECONCILIATION_2026-09-12.md`](CURRENT_STATE_RECONCILIATION_2026-09-12.md) — current status-only overlay for present-tense routing.

These are stable controlling or routing documents. Their root paths are kept intentionally stable because `AGENTS.md`, active plans, source comments, tests, and historical records reference them extensively.

Some large master documents intentionally retain historical present-tense wording from earlier checkpoints. The current reconciliation supersedes those **status-only** passages without rewriting durable product/roadmap/implementation semantics or historical chronology.

The older [`CURRENT_STATE_RECONCILIATION_2026-09-05.md`](CURRENT_STATE_RECONCILIATION_2026-09-05.md) is the previous status checkpoint and is no longer current.

## 2. Current execution state

```text
Phase 1                              CLOSED / ACCEPTED
P2.1 Canonical Registry             CLOSED / ACCEPTED
P2.2A Work Intelligence             CLOSED / ACCEPTED
P2.2B-B1                            CLOSED / NO-PROMOTION / DEFER
P2.2C promoted responsibility       NOT ACTIVE / NOT AUTHORIZED
P2.2D stable role archetypes        LATER

Market research                     COMPLETE ENOUGH
Market foundation investigation     PASS / COMPLETE
Market first vertical slice         AUTHORIZED / ACTIVE FRONTIER
Current exact increment             I1 domain models + SQLite persistence
Semantic report/subfamily synthesis DEFERRED FROM FIRST SLICE
```

Use these files for current execution:

- [`CURRENT_STATE_RECONCILIATION_2026-09-12.md`](CURRENT_STATE_RECONCILIATION_2026-09-12.md) — current status/routing overlay.
- [`MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`](MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md) — current controlling Market product/implementation plan.
- [`working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`](working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md) — formal `PASS / FIRST VERTICAL SLICE AUTHORIZED` decision and first-slice contract.
- [`working-memory/2026-09-12_MARKET_RESEARCH_CONSOLIDATION_AND_DECISION_LEDGER.md`](working-memory/2026-09-12_MARKET_RESEARCH_CONSOLIDATION_AND_DECISION_LEDGER.md) — prior research consolidated into `DECIDED / PROVISIONAL / OPEN / DEFERRED`.
- [`EXECUTION_TODO.md`](EXECUTION_TODO.md) — current implementation checklist.
- [`WORKING_MEMORY.md`](WORKING_MEMORY.md) — rolling handoff/current-state memory.

The exact next product action is **Market I1 — domain models + SQLite persistence**. Do not restart B1 or the foundation investigation.

## 3. Closed P2.2B and executed Market-foundation records

These remain important immediate history but are no longer the live route:

- [`P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md`](P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md) — B1 closed as `NO-PROMOTION / DEFER`; no canonical responsibility concept/mappings were created.
- [`working-memory/2026-09-14_P2_2B_B1_EXTRACTION_RECOVERY.md`](working-memory/2026-09-14_P2_2B_B1_EXTRACTION_RECOVERY.md) — exact `ta9l` local attempts, rejected artifact 47, retained coverage/depth repairs, and final defer evidence.
- [`MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md`](MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md) — executed/closed Q1–Q12 investigation protocol.

The durable P2.2 semantics remain in:

- [`P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`](P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md)
- [`P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md`](P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md)

Their older checkpoint status wording does not reopen B1/P2.2A.

## 4. Current Market first-slice boundary

Authorized first slice:

```text
TargetMarket
+ immutable TargetMarketDefinitionVersion
+ MarketResearchRun
+ MarketJobMembership
+ immutable MarketCorpusSnapshot + members
+ deterministic MarketAggregateProfile
+ thin browser/CLI workflow
```

Implementation order:

```text
I1 domain + SQLite persistence
→ I2 target-scoped eligibility / affected-work planning
→ I3 membership qualification
→ I4 immutable snapshot
→ I5 deterministic aggregate profile
→ I6 browser + CLI
→ I7 bounded local real acceptance
```

Important current constraints:

- target acquisition/search vocabulary is not membership truth or canonical role taxonomy;
- accepted P1.6 is not required for source-level target membership;
- strong P1.6-backed prevalence uses only accepted-current P1.6 and an explicit semantic sub-denominator;
- pending/missing/failed P1.6 remains visible and never means zero demand;
- Capability/Work are not mandatory first-slice gates;
- automatic repost/new-ID collapse is deferred; denominator wording is `qualified source postings`, not `unique demand units`;
- semantic role-subfamily synthesis and persisted model-generated Role-Family Intelligence Report are later layers;
- Market runtime state remains local/private by default.

## 5. Current technical and operational references

| Document | Purpose |
| --- | --- |
| [`DEVELOPMENT_AND_LOCAL_SETUP.md`](DEVELOPMENT_AND_LOCAL_SETUP.md) | fresh-clone developer setup, isolated local config, optional LM Studio/Jobinja, and local-state boundaries |
| [`ACQUISITION_OPERATIONS.md`](ACQUISITION_OPERATIONS.md) | Jobinja acquisition and operational workflow |
| [`SEARCH_CONFIGURATION.md`](SEARCH_CONFIGURATION.md) | bilingual search catalog/configuration |
| [`TRANSLATION_AND_ENGLISH_CORPUS.md`](TRANSLATION_AND_ENGLISH_CORPUS.md) | translation and English-projection boundary |
| [`SEMANTIC_ANALYSIS.md`](SEMANTIC_ANALYSIS.md) | P1.6 structured factual-analysis design |
| [`CURRENT_RUNTIME_AND_VERSIONED_CODE.md`](CURRENT_RUNTIME_AND_VERSIONED_CODE.md) | current semantic runtime entrypoints, versioned dependency roles, and historical-code disposition |
| [`LOCAL_WEB_APP.md`](LOCAL_WEB_APP.md) | local browser application behavior and operation |
| [`demo/README.md`](demo/README.md) | reproducible public-corpus walkthrough |
| [`../corpus/README.md`](../corpus/README.md) | deterministic repository-safe public corpus |
| [`../review-snapshots/README.md`](../review-snapshots/README.md) | selected semantic-review/acceptance exports |

## 6. Current amendments retained beside controlling documents

The 2026-08-26 governance reorientation remains part of the current authority chain:

- [`ROADMAP_AMENDMENT_2026-08-26_UTILITY_REASONING_AND_PROMOTION.md`](ROADMAP_AMENDMENT_2026-08-26_UTILITY_REASONING_AND_PROMOTION.md)
- [`IMPLEMENTATION_PLAN_AMENDMENT_2026-08-26_REASONING_AND_PROMOTION.md`](IMPLEMENTATION_PLAN_AMENDMENT_2026-08-26_REASONING_AND_PROMOTION.md)
- [`EXECUTION_TODO_AMENDMENT_2026-08-26_UTILITY_REASONING.md`](EXECUTION_TODO_AMENDMENT_2026-08-26_UTILITY_REASONING.md)

They remain at stable paths until their durable rules are deliberately consolidated. Do not treat an amendment as a free-standing replacement for its parent.

The current-state reconciliation is narrower: it supersedes obsolete present-tense status labels, not product meaning or strategic sequencing.

## 7. Closed / historical implementation and acceptance plans

These records remain useful engineering evidence but are **not the current execution route** unless a current owner deliberately points back to a preserved invariant.

| Document | Current lifecycle |
| --- | --- |
| [`PHASE_1_JOBINJA_AUTOMATION_PLAN.md`](PHASE_1_JOBINJA_AUTOMATION_PLAN.md) | Phase-1 implementation history — closed |
| [`P1_7_REPORT_RUN_BROWSER_ACCEPTANCE_PLAN.md`](P1_7_REPORT_RUN_BROWSER_ACCEPTANCE_PLAN.md) | accepted/closed P1.7 record |
| [`SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`](SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md) | completed Phase-1 semantic-quality route |
| [`PHASE_2_CAPABILITY_INTELLIGENCE_PLAN.md`](PHASE_2_CAPABILITY_INTELLIGENCE_PLAN.md) | accepted Capability-v9 design/non-regression history |
| [`P2_1_CANONICAL_CONCEPT_REGISTRY_PLAN.md`](P2_1_CANONICAL_CONCEPT_REGISTRY_PLAN.md) | P2.1 closed/accepted implementation history |
| [`P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md`](P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md) | B1 closed/no-promotion/defer history |
| [`MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md`](MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md) | foundation protocol executed/closed |
| [`ROLE_CAPABILITY_BLUEPRINT_PLAN.md`](ROLE_CAPABILITY_BLUEPRINT_PLAN.md) | experimental Blueprint history; non-authoritative |
| [`SEMANTIC_ANALYSIS_ENGINEERING_LESSONS.md`](SEMANTIC_ANALYSIS_ENGINEERING_LESSONS.md) | engineering lessons/history |

A legacy `Active`, `next`, or old gate statement does not reopen closed work. Current lifecycle comes from `AGENTS.md`, the current-state reconciliation, current Market plan/decision, `EXECUTION_TODO.md`, and `WORKING_MEMORY.md`.

## 8. Proposal, experiment, decision, incident, and working-memory collections

- [`proposals/`](proposals/) — candidate product/architecture ideas; never self-authorizing.
- [`experiments/`](experiments/) — bounded model/contract investigations; evidence, not automatic authority.
- [`decisions/`](decisions/) — durable decision records.
- [`incidents/`](incidents/) — failure/incident investigations.
- [`working-memory/`](working-memory/) — dated execution/handoff evidence; subordinate unless deliberately promoted by current authority.

`AI_INTELLIGENCE_RAG_CONTINUAL_LEARNING_PROPOSAL.md` remains a legacy root-level proposal for reference stability and is not current architecture authorization.

## 9. Portfolio-readiness track

The repository-quality/release track is parallel to product feature authority.

Current portfolio state:

```text
PR0–PR8    complete / repository-side complete as recorded
PR9-A      final repository/public audit complete
PR9-B      MIT license complete
           GitHub description/topics pending
           real browser screenshots + privacy review pending
PR9-C      intentional v0.1.0 release pending
PR9-D      CV/interview package complete
PR9-E      owner mastery prepared / not verified
```

Relevant owners:

- [`PORTFOLIO_READINESS_AND_PUBLIC_PRESENTATION_PLAN.md`](PORTFOLIO_READINESS_AND_PUBLIC_PRESENTATION_PLAN.md)
- [`PORTFOLIO_READINESS_AUDIT_2026-09-02.md`](PORTFOLIO_READINESS_AUDIT_2026-09-02.md)
- [`PORTFOLIO_RELEASE_CV_AND_INTERVIEW_PACKAGE.md`](PORTFOLIO_RELEASE_CV_AND_INTERVIEW_PACKAGE.md)
- [`PORTFOLIO_RELEASE_STATE_AMENDMENT_2026-09-06_MIT_LICENSE.md`](PORTFOLIO_RELEASE_STATE_AMENDMENT_2026-09-06_MIT_LICENSE.md)

Portfolio work must not silently broaden the authorized Market slice or alter accepted semantic contracts.

## 10. Document lifecycle labels

```text
CURRENT / CONTROLLING
Defines present product, architecture, policy, roadmap, or authorized execution.

CURRENT / SUPPORTING
Explains an implemented subsystem or operation but is subordinate to controlling docs.

ACTIVE PLAN
Controls a currently authorized bounded implementation/evaluation increment.

ROLLING STATE
Current handoff/checklist state; intentionally changes frequently.

CLOSED / ACCEPTED
Preserved plan/acceptance record whose gate is complete.

HISTORICAL / EXPERIMENTAL
Useful evolution/failure/research evidence; not current authority.

PROPOSAL
Candidate idea only; never self-authorizing.
```

## 11. Placement rules

- keep stable controlling docs, current supporting guides, active plans, and a small number of repository-wide tracks at `docs/` root;
- put reproducible demo walkthroughs under `demo/`;
- put model/contract experiments in `experiments/`;
- put dated execution/handoff evidence in `working-memory/`;
- put candidate ideas in `proposals/`;
- put durable selected decisions in `decisions/`;
- put incident investigations in `incidents/`;
- update an existing current owner rather than creating a duplicate document when practical;
- do not move widely referenced controlling files merely for visual tidiness;
- if a move is justified, update all references and verify links in the same bounded change.

## 12. External-reviewer route

```text
README.md
→ demo/README.md
→ PRODUCT_SPECIFICATION.md
→ ARCHITECTURE.md
→ DEVELOPMENT_AND_LOCAL_SETUP.md when cloning/running
→ DOMAIN_AND_ANALYSIS_MODEL.md / SOURCE_POLICY.md
→ current Market plan/decision or subsystem docs as needed
→ decisions / experiments / working-memory for deeper history
```

This keeps JobHunter’s engineering history available without forcing a reviewer to reconstruct chronology before understanding the current system.
