# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-09-01
**Active working branch:** `main`  
**Authority:** Subordinate to product/domain/source/architecture constraints, `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`, `docs/ROADMAP.md` plus its 2026-08-26 amendment, `docs/IMPLEMENTATION_PLAN.md` plus its 2026-08-26 amendment, and the current focused plan  
**Current focused plan:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md` — APPROVED  
**Current gate:** P2.2A IMPLEMENTED / ACCEPTANCE OPEN / cross-job action-authority representation blocker VERIFIED / focused-plan amendment NEXT

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

Final record: `docs/working-memory/2026-08-23_P2_1D_AND_P2_1_FINAL_ACCEPTANCE.md`

---

## C. Utility / epistemic governance reorientation — ACCEPTED

- [x] useful career intelligence per unit user time is an explicit optimization target.
- [x] source fact / normalized correspondence / analytical interpretation / recommendation are distinct.
- [x] generated/candidate is distinct from reviewed/promoted authority.
- [x] fail hard for integrity; fail soft for interpretive uncertainty.
- [x] human review is mainly a promotion boundary.
- [x] Tier A integrity, Tier B promoted semantic, Tier C bounded analytical acceptance are explicit.
- [x] strict source/provenance/privacy/currentness rules remain intact.
- [x] exhaustive canonicalization is not a prerequisite for useful job-level reasoning.

Controlling companion: `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`

---

## D. P2.2 Responsibility, Work, and Role Intelligence

Focused plan: `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`

Approved order:

```text
P2.2A Job Work Intelligence v1
→ P2.2B selective responsibility/deliverable promotion
→ P2.2C responsibility-family intelligence
→ P2.2D role-archetype intelligence
```

### D1 — P2.2A Job Work Intelligence v1 — IMPLEMENTED / ACCEPTANCE OPEN

Working contract/schema:

```text
job-work-intelligence-v1
```

Current prompt/pipeline identity:

```text
job-work-intelligence-v1.3
```

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
- [x] historical artifact preservation and currentness invalidation when accepted dependencies or prompt identity change.
- [x] deterministic source-index bounds validation.
- [x] deterministic complete accepted responsibility/role-purpose coverage across themes.
- [x] deterministic no-direct-work path that does not call the model or fabricate duties.
- [x] impossible references into structurally empty source sections are normalized away without remapping references into non-empty sections.
- [x] dedicated bounded LM Studio/Instructor reasoning adapter.
- [x] one bounded service-level regeneration after a post-generation validation failure.
- [x] one final semantic authority-review pass for direct-work candidates before persistence.
- [x] authority review is model-semantic rather than a deterministic action-verb equivalence table.
- [x] authority-review output is rechecked by the same deterministic reference/coverage/scope guards.
- [x] request/raw-response provenance preserves generation, repair metadata when applicable, and authority review separately.
- [x] CLI: `jobhunter-work generate|show` and module-equivalent command.
- [x] browser route: `/jobs/<job-id>/work-intelligence`.
- [x] browser mutation remains local and does not publish Work Intelligence into `corpus/`.
- [x] final repository quality gates green on v1.3 pipeline: Ruff + 530 tests + warnings-as-errors.

Implementation record: `docs/working-memory/2026-08-26_P2_2A_JOB_WORK_INTELLIGENCE_V1_IMPLEMENTATION.md`

#### Live defect / refinement history — UNDERSTOOD

- [x] first real `t4qV` generation exposed optional structured-reference arrays in the generation schema.
- [x] structured reference arrays became required; provenance validator was not weakened.
- [x] regression proves indices mentioned only in rationale prose do not count as structured provenance.
- [x] first valid `t4qV` artifact 1 exposed repeatable unsupported `end-to-end` / `entire security stack` inflation.
- [x] v1.1 strengthened shared-evidence/scope instructions and added bounded scope-intensifier validation.
- [x] phrase normalization treats `end-to-end` and `end to end` equivalently.
- [x] first `tG9K` generation exposed a model reference to nonexistent `role_purpose[1]` while role_purpose was structurally empty.
- [x] empty-section impossible-reference normalization fixed that without weakening normal bounds validation.
- [x] `tmyX` and `tG9K` then showed repeated action-strengthening (`develop/provide → implementing`; `move toward production → deploying`).
- [x] v1.2 strengthened prompt-level action authority while rejecting deterministic verb-equivalence machinery.
- [x] v1.2 also added one bounded service-level semantic repair retry after deterministic post-generation validation rejects a draft.
- [x] real `tG9K` v1.2 artifact 5 still said direct `deploying` despite the weaker collaborative source relationship, proving prompt-only refinement insufficient.
- [x] v1.3 adds a dedicated semantic authority-review stage before persistence.
- [x] all historical artifacts remain immutable under their original prompt identities.

Key records:

```text
docs/working-memory/2026-08-26_P2_2A_T4QV_FIRST_LIVE_GENERATION_STRUCTURED_REFERENCE_FAILURE.md
docs/working-memory/2026-08-26_P2_2A_T4QV_FIRST_VALID_CANDIDATE_AND_SCOPE_REPAIR.md
docs/working-memory/2026-08-27_P2_2A_TG9K_EMPTY_ROLE_PURPOSE_REFERENCE_FAILURE_AND_REPAIR.md
docs/working-memory/2026-08-27_P2_2A_TG9K_USEFUL_CANDIDATE_AND_ACTION_AUTHORITY_V12_REFINEMENT.md
docs/working-memory/2026-08-27_P2_2A_V12_SCOPE_FAILURE_AND_BOUNDED_SEMANTIC_REPAIR_RETRY.md
docs/working-memory/2026-08-27_P2_2A_TG9K_V12_PERSISTED_ACTION_INFLATION_AND_V13_AUTHORITY_REVIEW.md
```

#### Real-local semantic/product acceptance — IN PROGRESS

Historical/live evidence so far:

```text
t4qV  artifact 2  v1.1  useful accepted candidate anchor; historical under current v1.3
tmyX  artifact 3  v1.1  useful candidate with recorded action-strengthening limitation; historical
tG9K  artifact 4  v1.1  useful grouping; showed supporting emphasis + action strengthening; historical
tG9K  artifact 5  v1.2  useful grouping; still direct deployment wording; historical
tG9K  artifacts 6-10  v1.3-v1.7 controlled action-authority evidence; historical/experimental
tmyX  artifact 11     v1.7 controlled field-review evidence; historical/experimental
```

Checkpoint record:
`docs/working-memory/2026-09-01_P2_2A_ACTION_AUTHORITY_TRIALS_AND_REPRESENTATION_REDESIGN_GATE.md`

Acceptance sequence after the representation amendment:

```text
tG9K  industrial ML / manufacturing AI                  action-authority evidence COMPLETE
tmyX  security infrastructure / Microsoft services      cross-job defect evidence COMPLETE
t4qV  network/security                                   PENDING redesigned representation
tmBK  requirements-only / no direct work evidence       PENDING redesigned representation
```

- [x] live `t4qV` and `tmyX` demonstrated that Work Intelligence materially reduces manual synthesis effort.
- [x] `tG9K` demonstrated useful heterogeneous industrial-ML grouping.
- [x] `tG9K` v1.1 produced `3 primary + 1 supporting`, resolving the concern that emphasis always collapses to all-primary. Do not add a fixed quota.
- [x] repeated action-strengthening justified a semantic authority-review stage rather than deterministic verb mappings.
- [x] run controlled `tG9K` v1.3-v1.7 action-authority trials across 2B, 4B, 12B, full-document, compact, and field-complete review protocols.
- [x] verify on `tmyX` that field-complete review still strengthened `develop/provide hardening solutions` into directly `hardening the security posture`.
- [ ] amend/approve the P2.2A representation so exact accepted direct-work statements carry factual action authority while model grouping remains candidate interpretation.
- [ ] regenerate/review `t4qV` under v1.3 for current identity without reopening already-resolved scope issues.
- [ ] generate `tmBK` and confirm deterministic `limited` behavior with no invented duties.
- [ ] rerun at least one unchanged current v1.3 job and confirm artifact reuse.
- [ ] inspect the browser Work Intelligence page on the same real artifacts.
- [ ] verify employer/P1.6 facts and JobHunter interpretation remain visually/semantically distinct.
- [ ] decide P2.2A semantic/product acceptance based on whether the view materially reduces manual reading/synthesis effort across heterogeneous anchors while preserving authority boundaries.

Interpretive policy during acceptance:

```text
bounded imperfection / harmless paraphrase
→ record or tolerate as candidate interpretation

repeatable material authority/integrity defect
→ smallest general repair + regression

semantic relationship problem
→ prefer semantic review/reasoning over brittle deterministic vocabularies

repeated product-quality weakness
→ gather cross-job evidence first, then refine semantics if justified
```

Do not introduce a deterministic action-verb equivalence system or a fixed primary-theme quota.

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
P2.2A implementation is complete; live acceptance remains open.
Current prompt/pipeline identity = job-work-intelligence-v1.3.
Historical/experimental artifacts 2-11 and all attempt records remain preserved.
→ do not run another prompt-only or model-only action-authority trial
→ amend the focused P2.2A representation plan
→ model grouping/emphasis may remain candidate interpretation
→ deterministically inject exact accepted work statements for action-bearing factual content
→ visually separate exact employer/P1.6 work from optional JobHunter interpretation
→ only then resume t4qV/tmBK/reuse/browser acceptance
→ only then decide P2.2B
```
