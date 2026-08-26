# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-08-26  
**Active working branch:** `main`  
**Authority:** Subordinate to product/domain/source/architecture constraints, `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`, `docs/ROADMAP.md` plus its 2026-08-26 amendment, `docs/IMPLEMENTATION_PLAN.md` plus its 2026-08-26 amendment, and the current focused plan  
**Current focused plan:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md` — APPROVED  
**Current gate:** P2.2A Job Work Intelligence v1 IMPLEMENTED / CI GREEN / REAL-LOCAL SEMANTIC ACCEPTANCE NEXT

Repository workflow:

```text
current work → main
next work    → main
```

Do not create a branch unless the repository owner explicitly changes this rule.

Status vocabulary:

```text
[ ] not started
[~] in progress / implemented but acceptance incomplete
[x] accepted/completed for the stated scope
[!] rejected/blocking defect
[-] deliberately deferred
```

---

## A. Accepted foundation — CLOSED

- [x] Jobinja discovery/acquisition/provenance/source-version foundation.
- [x] `jobinja-detail-v2` parser and source/lifecycle truthfulness.
- [x] `english-projection-v2` / `lm-studio-translation-v2`.
- [x] English P1.6 `job-analysis-english-v20 / job-analysis-v5`.
- [x] Capability `job-capability-intelligence-v9 / job-capability-intelligence-v5`.
- [x] heterogeneous semantic acceptance on `tmBK`, `t4qV`, and `tmyX`.
- [x] partial-success semantics and final Phase-1 CLI/browser workflow.
- [x] versioned repository-safe public corpus `jobhunter-public-corpus-v1`.
- [x] Phase 1 CLOSED.

Frozen Phase-2 factual input:

```text
tG9K P1.6 36 → Capability 11
t4jp P1.6 37 → Capability 12
tmBK P1.6 39 → Capability 13
t4qV P1.6 44 → Capability 14
tmyX P1.6 46 → Capability 15
```

Do not reopen P1.6/Capability merely for harmless non-authoritative wording variation.

Historical detail remains in `docs/WORKING_MEMORY.md`, focused plans, and `docs/working-memory/` records.

---

## B. P2.1 Canonical Concept Registry — CLOSED / ACCEPTED

- [x] deterministic concept/alias/mapping persistence.
- [x] CLI manual review workflow.
- [x] browser review workflow.
- [x] deliberately small real-data seed.
- [x] exact provenance/currentness/idempotency/stale-dependency behavior.
- [x] Ruff/full pytest/warnings-as-errors acceptance.

Accepted seed:

```text
concepts:            4
reviewed aliases:    1
claim decisions:     6
  mapped:            5
  unmapped:          1
registry publication NOT AUTHORIZED
```

Final record:

`docs/working-memory/2026-08-23_P2_1D_AND_P2_1_FINAL_ACCEPTANCE.md`

---

## C. Utility / epistemic governance reorientation — ACCEPTED

- [x] make useful career intelligence per unit user time an explicit optimization target.
- [x] distinguish source fact / normalized correspondence / analytical interpretation / recommendation.
- [x] distinguish generated/candidate from reviewed/promoted authority.
- [x] fail hard for integrity; fail soft for interpretive uncertainty.
- [x] make human review primarily a promotion boundary.
- [x] define Tier A integrity, Tier B promoted semantic, Tier C bounded analytical acceptance.
- [x] preserve strict source/provenance/privacy/currentness rules.
- [x] prevent exhaustive canonicalization from becoming a prerequisite for useful job-level reasoning.

Controlling companion:

`docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`

---

## D. P2.2 Responsibility, Work, and Role Intelligence

Focused plan:

`docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`

Approved order:

```text
P2.2A Job Work Intelligence v1
→ P2.2B selective responsibility/deliverable promotion
→ P2.2C responsibility-family intelligence
→ P2.2D role-archetype intelligence
```

### D1 — P2.2A Job Work Intelligence v1 — IMPLEMENTED / ACCEPTANCE OPEN

Working contract:

`job-work-intelligence-v1`

#### Implementation — COMPLETE

- [x] typed candidate Work Intelligence contract.
- [x] `sufficient | limited` work-evidence state.
- [x] `primary | supporting | uncertain` relative emphasis instead of fake percentages.
- [x] `source_explicit | strongly_implied_by_work` deliverable status.
- [x] candidate role interpretation with confidence/alternatives/limitations.
- [x] work themes require direct responsibility or role-purpose support.
- [x] supporting requirements cannot create duties by themselves.
- [x] exact accepted/current English P1.6 dependency resolution.
- [x] immutable candidate artifact persistence plus attempt history.
- [x] historical artifact preservation and currentness invalidation when P1.6 changes.
- [x] deterministic source-index bounds validation.
- [x] deterministic complete accepted responsibility/role-purpose coverage across themes.
- [x] deterministic no-direct-work path that does not call the model or fabricate duties.
- [x] dedicated bounded LM Studio/Instructor reasoning adapter.
- [x] Work Intelligence keeps separate prompt/schema/artifact identity from Capability.
- [x] initial implementation reuses the existing configured capability-model fallback chain rather than adding premature configuration.
- [x] CLI: `jobhunter-work generate|show`.
- [x] browser route: `/jobs/<job-id>/work-intelligence`.
- [x] accepted job-detail pages link to Work Intelligence.
- [x] browser clearly distinguishes accepted facts from JobHunter candidate interpretation.
- [x] browser mutation does not use `WebOperationManager` and therefore does not publish/refresh Work Intelligence into `corpus/`.
- [x] focused deterministic/browser regression coverage.

Implementation record:

`docs/working-memory/2026-08-26_P2_2A_JOB_WORK_INTELLIGENCE_V1_IMPLEMENTATION.md`

#### Repository quality — PASS

CI run `32996495178`, implementation head `c77635c63ec3140146315980fb0c80522b03d0cf`:

- [x] Ruff PASS.
- [x] full pytest PASS.
- [x] warnings-as-errors pytest PASS.

Do not invent a test count; the retrieved CI evidence established successful steps, not their console count.

#### Real-local semantic/product acceptance — NEXT

Use the real current local database and configured local model:

```text
tG9K  responsibility-rich industrial ML / manufacturing AI
t4qV  responsibility-rich network/security
tmyX  responsibility-rich security infrastructure / Microsoft services
tmBK  requirements-only / no direct work evidence boundary
```

- [ ] pull the current `main` implementation locally.
- [ ] ensure editable install exposes the new `jobhunter-work` entrypoint if needed.
- [ ] generate `tG9K` Work Intelligence and review usefulness/coverage/restraint.
- [ ] generate `t4qV` Work Intelligence and review usefulness/coverage/restraint.
- [ ] generate `tmyX` Work Intelligence and review usefulness/coverage/restraint.
- [ ] generate `tmBK` and confirm deterministic `limited` behavior with no invented duties.
- [ ] rerun at least one unchanged job and confirm artifact reuse.
- [ ] inspect the browser Work Intelligence page on the same real artifacts.
- [ ] verify employer/P1.6 facts and JobHunter interpretation remain visually/semantically distinct.
- [ ] record any model limitation as analytical limitation unless it violates an integrity contract.
- [ ] convert only repeatable integrity defects into deterministic fixes/tests.
- [ ] decide P2.2A semantic/product acceptance based on whether the view materially reduces manual reading/synthesis effort.

### D2 — P2.2B selective responsibility/deliverable promotion — BLOCKED ON D1 ACCEPTANCE

- [ ] decide which candidate semantics actually deserve reusable promotion based on observed P2.2A value.
- [ ] normalize only where downstream reuse justifies it.
- [ ] do not pursue mapping percentage/completeness as an objective.

### D3 — P2.2C responsibility-family intelligence — LATER

- [ ] candidate families may be useful before promotion.
- [ ] promoted reusable families require stronger evidence/review.

### D4 — P2.2D role-archetype intelligence — LATER

- [ ] candidate job-local role interpretation may exist early.
- [ ] stable reusable archetypes require stronger cross-job/employer evidence and explicit promotion.

---

## E. Still deferred / not authorized

- [-] Work Intelligence public-corpus publication.
- [-] canonical-registry publication.
- [-] automatic taxonomy growth/promotion.
- [-] exhaustive responsibility mapping merely for completeness.
- [-] fixed title-first role taxonomy.
- [-] Market v2 before the applicable promoted canonical substrate is ready.
- [-] durable personal evidence/readiness/gap scoring/recommendations.
- [-] learning-plan generation and application ranking.
- [-] autonomous applications/recruiter communication.
- [-] vector/RAG/graph infrastructure without demonstrated product need.
- [-] generic source/plugin framework before a real second source.
- [-] multi-model voting without measured justification.

---

## Exact next action

```text
P2.2A implementation is complete and repository CI is green.
→ perform real-local semantic/product acceptance on tG9K, t4qV, tmyX, tmBK
→ fix only evidence-backed defects if found
→ close P2.2A only after usefulness + authority-boundary review
→ then decide P2.2B from what P2.2A actually taught us
```
