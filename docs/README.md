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

Some large master documents intentionally retain historical present-tense wording from earlier checkpoints. The 2026-09-12 reconciliation supersedes those **status-only** passages without rewriting their durable product/roadmap/implementation semantics or historical chronology.

The older [`CURRENT_STATE_RECONCILIATION_2026-09-05.md`](CURRENT_STATE_RECONCILIATION_2026-09-05.md) is retained as the previous status checkpoint and is no longer the current overlay.

## 2. Current execution state

The live project state is narrower than the whole roadmap.

```text
Phase 1                      CLOSED / ACCEPTED
P2.1 Canonical Registry     CLOSED / ACCEPTED
P2.2A Work Intelligence     CLOSED / ACCEPTED
P2.2B-B1                    IN PROGRESS
                            repo evidence selection/preflight COMPLETE
                            ta9l local English + P1.6 authority gate NEXT
                            no promotion yet
P2.2C                       BLOCKED
P2.2D                       LATER

Market / Role-Family        research preparation COMPLETE
                            formal foundation investigation BLOCKED BY B1
                            implementation NOT AUTHORIZED
```

Use these files for current execution:

- [`CURRENT_STATE_RECONCILIATION_2026-09-12.md`](CURRENT_STATE_RECONCILIATION_2026-09-12.md) — current status/routing overlay for older status text.
- [`P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`](P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md) — durable P2.2 responsibility/work/role-intelligence plan; older header/current-gate wording is superseded by the current reconciliation.
- [`P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md`](P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md) — accepted P2.2A representation/authority amendment; its terminal `P2.2B not started` state is historical.
- [`P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md`](P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md) — focused active P2.2B-B1 plan; `ta9l` is already selected and the local P1.6 gate is next.
- [`EXECUTION_TODO.md`](EXECUTION_TODO.md) — current working checklist.
- [`WORKING_MEMORY.md`](WORKING_MEMORY.md) — rolling non-authoritative handoff/current-state memory.

The current product-development gate requires machine-local `ta9l` English projection/P1.6 review before any P2.2B registry promotion. Do not repeat the already-completed repository candidate scan unless `ta9l` is explicitly rejected and a new focused decision authorizes continued search.

## 3. Prepared future Market / Role-Family route

The Market / Role-Family responsibility is owner-approved but remains gated behind B1.

Current owners:

- [`MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`](MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md) — controlling future product/design direction; implementation gated.
- [`working-memory/2026-09-12_MARKET_RESEARCH_CONSOLIDATION_AND_DECISION_LEDGER.md`](working-memory/2026-09-12_MARKET_RESEARCH_CONSOLIDATION_AND_DECISION_LEDGER.md) — six research passes consolidated into `DECIDED / PROVISIONAL / OPEN / DEFERRED`.
- [`MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md`](MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_ENTRY_PLAN.md) — prepared post-B1 Q1-Q12 formal investigation protocol.

Current routing:

```text
broad remote research       COMPLETE ENOUGH / STOP
formal investigation prep  COMPLETE
formal investigation       NOT STARTED / BLOCKED BY B1
Market-v2 implementation   NOT AUTHORIZED
```

After B1 closes, the prepared formal investigation may start without another owner-activation ceremony. Implementation still requires its explicit `PASS / FIRST VERTICAL SLICE AUTHORIZED` decision.

## 4. Current technical and operational references

These documents explain implemented subsystems and normal operation. They are supporting engineering references, not higher authority than the product/domain/source/architecture stack.

| Document | Purpose |
| --- | --- |
| [`DEVELOPMENT_AND_LOCAL_SETUP.md`](DEVELOPMENT_AND_LOCAL_SETUP.md) | fresh-clone developer setup, isolated local config, optional LM Studio/Jobinja, and local-state boundaries |
| [`ACQUISITION_OPERATIONS.md`](ACQUISITION_OPERATIONS.md) | Jobinja acquisition and operational workflow |
| [`SEARCH_CONFIGURATION.md`](SEARCH_CONFIGURATION.md) | bilingual search catalog/configuration |
| [`TRANSLATION_AND_ENGLISH_CORPUS.md`](TRANSLATION_AND_ENGLISH_CORPUS.md) | translation and English-projection boundary |
| [`SEMANTIC_ANALYSIS.md`](SEMANTIC_ANALYSIS.md) | P1.6 structured factual-analysis design |
| [`CURRENT_RUNTIME_AND_VERSIONED_CODE.md`](CURRENT_RUNTIME_AND_VERSIONED_CODE.md) | current semantic runtime entrypoints, versioned dependency roles, and safe historical-code disposition |
| [`LOCAL_WEB_APP.md`](LOCAL_WEB_APP.md) | local browser application behavior and operation |
| [`demo/README.md`](demo/README.md) | reproducible public-corpus walkthrough using real accepted rich and sparse examples |
| [`../corpus/README.md`](../corpus/README.md) | deterministic repository-safe public corpus |
| [`../review-snapshots/README.md`](../review-snapshots/README.md) | selected semantic-review/acceptance exports |

## 5. Current amendments retained beside their controlling documents

The 2026-08-26 governance reorientation remains part of the current authority chain and is not merely historical notes:

- [`ROADMAP_AMENDMENT_2026-08-26_UTILITY_REASONING_AND_PROMOTION.md`](ROADMAP_AMENDMENT_2026-08-26_UTILITY_REASONING_AND_PROMOTION.md)
- [`IMPLEMENTATION_PLAN_AMENDMENT_2026-08-26_REASONING_AND_PROMOTION.md`](IMPLEMENTATION_PLAN_AMENDMENT_2026-08-26_REASONING_AND_PROMOTION.md)
- [`EXECUTION_TODO_AMENDMENT_2026-08-26_UTILITY_REASONING.md`](EXECUTION_TODO_AMENDMENT_2026-08-26_UTILITY_REASONING.md)

They stay at stable paths until their rules are deliberately consolidated into their parent documents. Do not treat an amendment as a free-standing replacement for its parent.

The 2026-09-12 current-state reconciliation is narrower: it supersedes obsolete present-tense status labels contradicted by later accepted evidence/current governance. It does not amend product meaning or strategic sequencing.

## 6. Closed or historical implementation/acceptance plans

These records remain useful engineering evidence, but they are **not the current execution route** unless a current controlling document explicitly points back to a preserved invariant.

| Document | Current lifecycle |
| --- | --- |
| [`PHASE_1_JOBINJA_AUTOMATION_PLAN.md`](PHASE_1_JOBINJA_AUTOMATION_PLAN.md) | Phase-1 implementation history — Phase 1 is closed |
| [`P1_7_REPORT_RUN_BROWSER_ACCEPTANCE_PLAN.md`](P1_7_REPORT_RUN_BROWSER_ACCEPTANCE_PLAN.md) | accepted/closed P1.7 acceptance record |
| [`SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`](SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md) | completed Phase-1 semantic-quality route; retained acceptance history |
| [`PHASE_2_CAPABILITY_INTELLIGENCE_PLAN.md`](PHASE_2_CAPABILITY_INTELLIGENCE_PLAN.md) | accepted Capability-v9 design/non-regression history; current architecture is summarized in `ARCHITECTURE.md` |
| [`P2_1_CANONICAL_CONCEPT_REGISTRY_PLAN.md`](P2_1_CANONICAL_CONCEPT_REGISTRY_PLAN.md) | P2.1 closed/accepted registry implementation history |
| [`ROLE_CAPABILITY_BLUEPRINT_PLAN.md`](ROLE_CAPABILITY_BLUEPRINT_PLAN.md) | experimental Blueprint research history; Blueprint is non-authoritative/currently deferred |
| [`SEMANTIC_ANALYSIS_ENGINEERING_LESSONS.md`](SEMANTIC_ANALYSIS_ENGINEERING_LESSONS.md) | engineering lessons/history, not a controlling semantic contract |

Some older records retain header/next-action wording from the period when they were active. **Current lifecycle classification comes from `AGENTS.md`, the current-state reconciliation, the active focused plan, `EXECUTION_TODO.md`, and `WORKING_MEMORY.md`; a legacy `Active` or `next` statement does not reopen closed work.**

## 7. Proposal, experiment, decision, incident, and working-memory collections

These directories intentionally keep deep engineering history off the first-pass product path:

- [`proposals/`](proposals/) — candidate product/architecture ideas. Proposal presence never authorizes implementation.
- [`experiments/`](experiments/) — bounded model/contract experiments and acceptance investigations. Results may explain why current contracts exist, but experiments are not automatically current authority.
- [`decisions/`](decisions/) — durable decision records for selected architectural/semantic choices.
- [`incidents/`](incidents/) — incident/failure investigation records.
- [`working-memory/`](working-memory/) — dated implementation/handoff evidence. These are non-authoritative snapshots unless a current controlling document deliberately promotes a rule from them.

`AI_INTELLIGENCE_RAG_CONTINUAL_LEARNING_PROPOSAL.md` is a legacy root-level proposal retained at its existing path for reference stability. It is **not controlling** and should be read as proposal/history alongside `proposals/`, not as current architecture authorization.

## 8. Portfolio-readiness track

The temporary repository-quality track is separate from product feature authority:

- [`PORTFOLIO_READINESS_AND_PUBLIC_PRESENTATION_PLAN.md`](PORTFOLIO_READINESS_AND_PUBLIC_PRESENTATION_PLAN.md) — portfolio-readiness sequence/history.
- [`PORTFOLIO_READINESS_AUDIT_2026-09-02.md`](PORTFOLIO_READINESS_AUDIT_2026-09-02.md) — frozen PR0 evidence/audit record.
- [`PORTFOLIO_RELEASE_CV_AND_INTERVIEW_PACKAGE.md`](PORTFOLIO_RELEASE_CV_AND_INTERVIEW_PACKAGE.md) — prepared PR9 release/CV/interview/mastery package.
- [`PORTFOLIO_RELEASE_STATE_AMENDMENT_2026-09-06_MIT_LICENSE.md`](PORTFOLIO_RELEASE_STATE_AMENDMENT_2026-09-06_MIT_LICENSE.md) — current release-state amendment; MIT decision/application complete.
- [`working-memory/2026-09-06_PR9_MIT_LICENSE_DECISION_AND_RELEASE_PROGRESS.md`](working-memory/2026-09-06_PR9_MIT_LICENSE_DECISION_AND_RELEASE_PROGRESS.md) — dated release-progress evidence.

Current portfolio status:

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

Any older portfolio-plan/package wording that says licensing is absent, undecided, or awaiting owner choice is status-only historical text superseded by the MIT release-state amendment.

This track may improve presentation, documentation, source organization, demoability, onboarding, and repository hygiene. It must not silently change accepted semantic behavior or bypass the active P2.2B product gate. Further generic portfolio polishing should stop; remaining work should close only concrete PR9 blockers/mastery items.

## 9. Document lifecycle labels

Use these meanings when adding or reviewing documentation:

```text
CURRENT / CONTROLLING
Defines present product, architecture, policy, roadmap, or authorized execution.

CURRENT / SUPPORTING
Explains an implemented subsystem or operation but is subordinate to controlling docs.

ACTIVE PLAN
Controls a currently authorized bounded implementation/evaluation increment.

ROLLING STATE
Current handoff/checklist state; intentionally changes frequently and is not permanent authority.

CLOSED / ACCEPTED
Preserved plan or acceptance record whose implementation gate is complete.

HISTORICAL / EXPERIMENTAL
Useful evidence of evolution, failure, learning, or research; not current authority.

PROPOSAL
Candidate idea only; never self-authorizing.
```

## 10. Placement rules for future documentation

To prevent `docs/` from becoming flat and ambiguous again:

- keep only stable controlling documents, current supporting subsystem guides, active top-level plans, and a small number of repository-wide audit/track documents at `docs/` root;
- put reproducible reviewer/demo walkthroughs under `demo/`;
- put model/contract investigations in `experiments/`;
- put dated execution/handoff evidence in `working-memory/`;
- put candidate product/architecture ideas in `proposals/`;
- put durable selected decisions in `decisions/`;
- put incident investigations in `incidents/`;
- do not create a new document when an existing current owner can be updated safely;
- do not move widely referenced controlling files merely to make the directory visually tidy;
- if a future move is justified, update all repository references and verify links in the same bounded change.

## 11. External-reviewer route

A reviewer who wants increasing depth should normally follow:

```text
README.md
→ demo/README.md for a concrete accepted evidence chain
→ PRODUCT_SPECIFICATION.md
→ ARCHITECTURE.md
→ DEVELOPMENT_AND_LOCAL_SETUP.md when cloning/running locally
→ DOMAIN_AND_ANALYSIS_MODEL.md / SOURCE_POLICY.md
→ current subsystem or active-plan docs as needed
→ decisions / experiments / working-memory only for deeper historical evidence
```

This keeps JobHunter’s engineering history available without forcing a recruiter or new developer to reconstruct the project chronology before understanding the current system.