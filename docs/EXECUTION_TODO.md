# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-09-01  
**Active working branch:** `main`  
**Authority:** Subordinate to product/domain/source/architecture constraints, `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`, `docs/ROADMAP.md` plus its 2026-08-26 amendment, `docs/IMPLEMENTATION_PLAN.md` plus its 2026-08-26 amendment, and the current focused P2.2 plan + approved representation amendment  
**Current focused plan:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`  
**Current controlling companion:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md`  
**Current gate:** P2.2A v1 implemented / acceptance open; v2 representation APPROVED; v2 implementation NEXT

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

Frozen accepted/current chains:

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
- [x] repository quality acceptance.

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

## C. Utility / epistemic governance — ACCEPTED

- [x] useful career intelligence per unit user time is an explicit optimization target.
- [x] source fact / normalized correspondence / analytical interpretation / recommendation are distinct.
- [x] generated/candidate is distinct from reviewed/promoted authority.
- [x] fail hard for integrity; fail soft for interpretive uncertainty.
- [x] human review is mainly a promotion boundary.
- [x] strict source/provenance/privacy/currentness rules remain intact.
- [x] exhaustive canonicalization is not a prerequisite for useful job-level reasoning.

Controlling companion: `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`

---

## D. P2.2 Responsibility, Work, and Role Intelligence

Focused plan:

`docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`

Approved representation amendment:

`docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md`

Approved sequence remains:

```text
P2.2A Job Work Intelligence
→ P2.2B selective responsibility/deliverable promotion
→ P2.2C responsibility-family intelligence
→ P2.2D role-archetype intelligence
```

### D1 — P2.2A Job Work Intelligence — IMPLEMENTATION REFINEMENT / ACCEPTANCE OPEN

#### Historical/current v1 implementation — COMPLETE

Current source before v2 implementation:

```text
schema/contract: job-work-intelligence-v1
prompt/pipeline: job-work-intelligence-v1.3
```

- [x] typed candidate Work Intelligence contract.
- [x] `sufficient | limited` work-evidence state.
- [x] semantic theme grouping and relative emphasis.
- [x] exact accepted/current English P1.6 dependency resolution.
- [x] immutable candidate artifact persistence plus attempt history.
- [x] deterministic source-index/reference/coverage validation.
- [x] deterministic no-direct-work path with no fabricated duties.
- [x] bounded post-validation regeneration.
- [x] browser + CLI surfaces.
- [x] Work Intelligence remains outside public-corpus publication.
- [x] repository deterministic quality gates green on v1.3.

Historical artifacts 2-11 and all attempt/request/raw-response evidence remain immutable.

#### Cross-job action-authority investigation — COMPLETE

- [x] `t4qV` proved useful candidate work grouping.
- [x] `tG9K` proved useful heterogeneous industrial-ML grouping and non-collapsed emphasis (`3 primary + 1 supporting`).
- [x] `tmyX` and `tG9K` independently exposed action-strengthening.
- [x] v1.2 prompt refinement proved insufficient.
- [x] v1.3 dedicated semantic authority review was implemented and tested.
- [x] controlled v1.3-v1.7 trials across 2B/4B/12B/full-document/compact/field-complete review protocols were completed.
- [x] stronger/larger/free-form review did not reliably preserve action relationship/lifecycle endpoint across both jobs.
- [x] 12B review path was additionally unsuitable for normal repeated-use latency.
- [x] source restored to committed v1.3 after experimental trials; experimental code/config was not retained.

Evidence checkpoint:

`docs/working-memory/2026-09-01_P2_2A_ACTION_AUTHORITY_TRIALS_AND_REPRESENTATION_REDESIGN_GATE.md`

Do **not** run another prompt/model action-authority trial matrix.

#### Representation amendment — APPROVED

- [x] retain model candidate grouping.
- [x] retain semantic relative emphasis/confidence.
- [x] factual action authority assigned to exact accepted P1.6 responsibility/role-purpose statements.
- [x] final themes will receive exact accepted direct-work items through deterministic assembly.
- [x] model candidate response and final persisted assembled artifact are conceptually separated.
- [x] action-bearing `work_summary` removed from the required v2 representation.
- [x] `WorkTheme.summary` removed as the factual theme description.
- [x] candidate role/deliverable summaries removed from required v2 shape; optional interpretation remains explicitly candidate only where useful.
- [x] dedicated second semantic authority-review model call removed from approved v2 normal path.
- [x] no deterministic action-verb equivalence table.
- [x] no new model-routing/12B/multi-model experiment authorized.
- [x] historical v1 artifacts remain immutable.

Approved new identities:

```text
schema/contract: job-work-intelligence-v2
prompt/runtime:  job-work-intelligence-v2.0
```

Controlling amendment:

`docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md`

#### v2 implementation — NEXT

Expected bounded implementation surface:

```text
src/jobhunter/work_intelligence_models.py
src/jobhunter/work_intelligence_service.py
src/jobhunter/work_intelligence_inference.py        # only as required by candidate schema/review removal
src/jobhunter/web/work_intelligence.py              # only if context assembly changes
src/jobhunter/web/templates/work_intelligence.html
src/jobhunter/work_intelligence_cli.py              # rendering/formatter as needed
focused Work Intelligence tests
```

Implementation checklist:

- [ ] define typed v2 model-candidate shape that carries semantic grouping decisions and source indices but does not author factual direct-work statements.
- [ ] define final assembled v2 artifact shape with deterministic `AcceptedWorkItem` identity (`kind`, `index`, exact accepted P1.6 `statement`, copied confidence when available).
- [ ] preserve `sufficient | limited` behavior.
- [ ] preserve semantic theme labels/emphasis/confidence.
- [ ] resolve candidate responsibility/role-purpose indices into exact accepted work items only after deterministic reference/coverage validation.
- [ ] prevent kind/index/statement drift by construction.
- [ ] remove required action-bearing `work_summary` / theme factual summary fields from v2.
- [ ] keep optional rationale/interpretation explicitly candidate and structurally separate.
- [ ] remove dedicated second model semantic authority-review call from normal successful path.
- [ ] preserve at most one bounded regeneration after deterministic candidate validation rejects a draft.
- [ ] keep current dependency/currentness/reference/coverage/schema/publication protections.
- [ ] keep requirement-only `tmBK` deterministic limited/no-model behavior.
- [ ] keep existing small unsupported scope-intensifier guard only as a bounded candidate-prose safety check; do not expand it into paraphrase machinery.
- [ ] update browser to show exact accepted P1.6 work inside each theme rather than only raw indices.
- [ ] update CLI to render the same assembled authority split.
- [ ] preserve historical v1 readability/history and ensure v1 is not reused as current v2.
- [ ] do not create a DB migration unless an actual table-level requirement is discovered.

#### v2 deterministic regression requirements

- [ ] exact P1.6 direct-work statements survive unchanged into final `AcceptedWorkItem` values.
- [ ] source kind/index and statement cannot disagree.
- [ ] stronger model interpretation cannot replace factual accepted work wording.
- [ ] every accepted responsibility/role-purpose remains covered across themes.
- [ ] invalid references still fail.
- [ ] requirement-only evidence cannot create work.
- [ ] normal valid direct-work generation performs one model call, not generation + authority review.
- [ ] bounded regeneration remains bounded.
- [ ] historical v1 artifacts remain historical.
- [ ] current v2 rerun reuses the same artifact identity.
- [ ] browser/CLI clearly distinguish accepted P1.6 work from JobHunter interpretation.
- [ ] Work Intelligence remains excluded from public-corpus publication.

Use known relationships as regression evidence without launching another live trial matrix:

```text
tG9K:
Partner with the semiconductor technical lead and engineering to move models toward production.

tmyX:
...develop and provide security requirements, Best Practices, and hardening solutions.
```

#### Post-implementation semantic/product acceptance

After focused deterministic v2 quality is green:

```text
1. t4qV — redesigned real direct-work generation/review
2. tmBK — deterministic limited-work verification
3. unchanged current v2 artifact — reuse verification
4. browser — real authority-boundary/usability inspection
5. CLI — same assembled semantics
6. P2.2A acceptance decision
7. only then P2.2B decision
```

`tG9K`/`tmyX` action-authority evidence is already complete; do not require another model experiment to prove the same defect.

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
implement job-work-intelligence-v2 candidate-vs-assembled representation
→ remove dedicated second model authority-review call
→ deterministically inject exact accepted P1.6 direct-work statements
→ update browser/CLI authority presentation
→ add focused v2 representation/authority regressions
→ run focused repository quality gates
→ resume t4qV / tmBK / reuse / browser acceptance
→ decide P2.2A acceptance
→ only then decide P2.2B
```