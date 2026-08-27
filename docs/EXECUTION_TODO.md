# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-08-27  
**Active working branch:** `main`  
**Authority:** Subordinate to product/domain/source/architecture constraints, `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`, `docs/ROADMAP.md` plus its 2026-08-26 amendment, `docs/IMPLEMENTATION_PLAN.md` plus its 2026-08-26 amendment, and the current focused plan  
**Current focused plan:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md` — APPROVED  
**Current gate:** P2.2A Job Work Intelligence v1 IMPLEMENTED / LIVE SEMANTIC-PRODUCT ACCEPTANCE IN PROGRESS / `tG9K` NEXT

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

Current prompt identity:

```text
job-work-intelligence-v1.1
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
- [x] dedicated bounded LM Studio/Instructor reasoning adapter.
- [x] CLI: `jobhunter-work generate|show` and module-equivalent command.
- [x] browser route: `/jobs/<job-id>/work-intelligence`.
- [x] browser mutation remains local and does not publish Work Intelligence into `corpus/`.
- [x] repository quality gates passed for the implementation and subsequent structured-reference/scope-boundary repairs.

Implementation record: `docs/working-memory/2026-08-26_P2_2A_JOB_WORK_INTELLIGENCE_V1_IMPLEMENTATION.md`

#### Live defect history — UNDERSTOOD / REPAIRED

- [x] first real `t4qV` generation exposed optional structured-reference arrays in the generation schema.
- [x] structured reference arrays became required; provenance validator was not weakened.
- [x] regression proves indices mentioned only in rationale prose do not count as structured provenance.
- [x] first valid `t4qV` artifact 1 exposed repeatable unsupported `end-to-end` / `entire security stack` inflation.
- [x] prompt identity bumped to `job-work-intelligence-v1.1` and shared-evidence/action-scope instructions strengthened.
- [x] bounded scope-intensifier guard added without constraining ordinary semantic grouping.
- [x] phrase normalization treats `end-to-end` and `end to end` equivalently.
- [x] historical artifact 1 remains preserved under the previous prompt identity.

Records:

```text
docs/working-memory/2026-08-26_P2_2A_T4QV_FIRST_LIVE_GENERATION_STRUCTURED_REFERENCE_FAILURE.md
docs/working-memory/2026-08-26_P2_2A_T4QV_FIRST_VALID_CANDIDATE_AND_SCOPE_REPAIR.md
```

#### Real-local semantic/product acceptance — IN PROGRESS

Acceptance anchors:

```text
t4qV  network/security                                  artifact 2  ACCEPTED candidate anchor
tmyX  security infrastructure / Microsoft services      artifact 3  ACCEPTED candidate anchor with recorded limitation
tG9K  industrial ML / manufacturing AI                  NEXT
tmBK  requirements-only / no direct work evidence       PENDING
```

- [x] pull and exercise the real local P2.2A path.
- [x] generate/review `t4qV` under v1.1 after repairs.
- [x] accept `t4qV` artifact 2 as useful, bounded candidate product intelligence.
- [x] generate/review `tmyX` artifact 3.
- [x] accept `tmyX` artifact 3 as useful bounded candidate intelligence with a recorded non-promoted action-verb limitation (`develop/provide` → summary `implementing`).
- [~] all generated themes were `primary` on both `t4qV` and `tmyX`; this is a product-quality watch item, not yet a deterministic defect. Use `tG9K` as the next independent check.
- [ ] generate `tG9K` Work Intelligence and review usefulness/coverage/restraint plus the emphasis pattern.
- [ ] generate `tmBK` and confirm deterministic `limited` behavior with no invented duties.
- [ ] rerun at least one unchanged current job and confirm artifact reuse.
- [ ] inspect the browser Work Intelligence page on the same real artifacts.
- [ ] verify employer/P1.6 facts and JobHunter interpretation remain visually/semantically distinct.
- [ ] decide P2.2A semantic/product acceptance based on whether the view materially reduces manual reading/synthesis effort across the heterogeneous anchors.

Accepted/live records:

```text
docs/working-memory/2026-08-27_P2_2A_T4QV_V11_SEMANTIC_PRODUCT_ANCHOR_ACCEPTED.md
docs/working-memory/2026-08-27_P2_2A_TMYX_SEMANTIC_PRODUCT_ANCHOR_ACCEPTED_WITH_LIMITATION.md
```

Interpretive policy during acceptance:

```text
bounded imperfection / harmless paraphrase
→ record or tolerate as candidate interpretation

repeatable material authority/integrity defect
→ smallest general repair + regression

repeated product-quality weakness
→ gather cross-job evidence, then refine semantics if justified
```

Do not introduce a deterministic action-verb equivalence system or a fixed primary-theme quota from the current evidence.

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
P2.2A implementation is complete.
t4qV artifact 2 and tmyX artifact 3 are accepted candidate product anchors.
→ generate/review tG9K next
→ use it to test heterogeneous ML grouping and whether the all-primary emphasis pattern repeats
→ then test tmBK limited-work behavior
→ then artifact reuse + browser UX
→ close P2.2A only after usefulness + authority-boundary review
→ only then decide P2.2B
```
