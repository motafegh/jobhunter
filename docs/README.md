# JobHunter Documentation Map

This directory contains both **current product/engineering authority** and the project’s retained **execution, experiment, and decision history**.

The files are intentionally layered rather than treated as one flat set of equally current documents. Start here when browsing `docs/` as a developer or technical reviewer. AI assistants and contributors must still follow the controlling reading order in [`../AGENTS.md`](../AGENTS.md).

## 1. Read this first

For the current product and engineering model, use this sequence:

1. [`PRODUCT_SPECIFICATION.md`](PRODUCT_SPECIFICATION.md) — product purpose, allowed meaning, current product boundaries, and intended long-term utility.
2. [`ARCHITECTURE.md`](ARCHITECTURE.md) — current implemented architecture, authority/data flow, persistence, failure semantics, and major tradeoffs.
3. [`DOMAIN_AND_ANALYSIS_MODEL.md`](DOMAIN_AND_ANALYSIS_MODEL.md) — domain entities and analytical semantics.
4. [`SOURCE_POLICY.md`](SOURCE_POLICY.md) — approved acquisition and source-authority rules.
5. [`UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`](UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md) — source fact, correspondence, interpretation, recommendation, and promotion boundaries.
6. [`ROADMAP.md`](ROADMAP.md) — strategic sequencing.
7. [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) — delivery order and implementation gates.

These are the stable controlling documents. Their root paths are kept intentionally stable because `AGENTS.md`, active plans, source comments, tests, and historical records reference them extensively.

## 2. Current execution state

The live project state is narrower than the whole roadmap.

Current state at this documentation checkpoint:

```text
Phase 1                      CLOSED
P2.1 Canonical Registry     CLOSED / ACCEPTED
P2.2A Work Intelligence     CLOSED / ACCEPTED
P2.2B-B1                    ACTIVE / bounded selective-responsibility promotion pilot
P2.2C                       BLOCKED
```

Use these files for current execution:

- [`P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`](P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md) — controlling P2.2 responsibility/work/role-intelligence plan.
- [`P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md`](P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md) — accepted P2.2A representation amendment and current constraints.
- [`P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md`](P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md) — focused active P2.2B-B1 plan.
- [`EXECUTION_TODO.md`](EXECUTION_TODO.md) — current working checklist.
- [`WORKING_MEMORY.md`](WORKING_MEMORY.md) — rolling non-authoritative handoff/current-state memory.

The current product-development gate requires machine-local `ta9l` English projection/P1.6 review before any P2.2B registry promotion. Portfolio-readiness work may proceed independently but does not bypass that gate.

## 3. Current technical and operational references

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

## 4. Current amendments retained beside their controlling documents

The 2026-08-26 governance reorientation remains part of the current authority chain and is not merely historical notes:

- [`ROADMAP_AMENDMENT_2026-08-26_UTILITY_REASONING_AND_PROMOTION.md`](ROADMAP_AMENDMENT_2026-08-26_UTILITY_REASONING_AND_PROMOTION.md)
- [`IMPLEMENTATION_PLAN_AMENDMENT_2026-08-26_REASONING_AND_PROMOTION.md`](IMPLEMENTATION_PLAN_AMENDMENT_2026-08-26_REASONING_AND_PROMOTION.md)
- [`EXECUTION_TODO_AMENDMENT_2026-08-26_UTILITY_REASONING.md`](EXECUTION_TODO_AMENDMENT_2026-08-26_UTILITY_REASONING.md)

They stay at stable paths until their rules are deliberately consolidated into their parent documents. Do not treat an amendment as a free-standing replacement for its parent.

## 5. Closed or historical implementation/acceptance plans

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

Some older records retain header wording from the period when they were active. **Current lifecycle classification comes from the accepted project state, `AGENTS.md`, current plans, and `WORKING_MEMORY.md`; a legacy `Active` header does not reopen closed work.**

## 6. Proposal, experiment, decision, incident, and working-memory collections

These directories intentionally keep deep engineering history off the first-pass product path:

- [`proposals/`](proposals/) — candidate product/architecture ideas. Proposal presence never authorizes implementation.
- [`experiments/`](experiments/) — bounded model/contract experiments and acceptance investigations. Results may explain why current contracts exist, but experiments are not automatically current authority.
- [`decisions/`](decisions/) — durable decision records for selected architectural/semantic choices.
- [`incidents/`](incidents/) — incident/failure investigation records.
- [`working-memory/`](working-memory/) — dated implementation/handoff evidence. These are non-authoritative snapshots unless a current controlling document deliberately promotes a rule from them.

`AI_INTELLIGENCE_RAG_CONTINUAL_LEARNING_PROPOSAL.md` is a legacy root-level proposal retained at its existing path for reference stability. It is **not controlling** and should be read as proposal/history alongside `proposals/`, not as current architecture authorization.

## 7. Portfolio-readiness track

The temporary repository-quality track is separate from product feature authority:

- [`PORTFOLIO_READINESS_AND_PUBLIC_PRESENTATION_PLAN.md`](PORTFOLIO_READINESS_AND_PUBLIC_PRESENTATION_PLAN.md) — controlling portfolio-readiness sequence.
- [`PORTFOLIO_READINESS_AUDIT_2026-09-02.md`](PORTFOLIO_READINESS_AUDIT_2026-09-02.md) — frozen PR0 evidence/audit record.

This track may improve presentation, documentation, source organization, demoability, onboarding, and repository hygiene. It must not silently change accepted semantic behavior or bypass the active P2.2B product gate.

## 8. Document lifecycle labels

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

## 9. Placement rules for future documentation

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

## 10. External-reviewer route

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