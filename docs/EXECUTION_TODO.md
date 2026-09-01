# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-09-01  
**Active working branch:** `main`  
**Authority:** Subordinate to product/domain/source/architecture constraints, `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`, `docs/ROADMAP.md`, `docs/IMPLEMENTATION_PLAN.md`, the focused P2.2 plan, and the approved P2.2A representation amendment  
**Current focused plan:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`  
**Current controlling companion:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN_AMENDMENT_2026-09-01.md`  
**Current gate:** P2.2A Work Intelligence v2 IMPLEMENTED / REPOSITORY QUALITY GREEN / REAL-LOCAL ACCEPTANCE NEXT

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
[x] accepted/completed for stated scope
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
- [x] public corpus `jobhunter-public-corpus-v1`.
- [x] Phase 1 CLOSED.

Frozen accepted/current chains:

```text
tG9K P1.6 36 → Capability 11
t4jp P1.6 37 → Capability 12
tmBK P1.6 39 → Capability 13
t4qV P1.6 44 → Capability 14
tmyX P1.6 46 → Capability 15
```

---

## B. P2.1 Canonical Concept Registry — CLOSED / ACCEPTED

- [x] deterministic concept/alias/mapping persistence.
- [x] CLI review workflow.
- [x] browser review workflow.
- [x] bounded real-data seed.
- [x] exact provenance/currentness/idempotency/stale-dependency behavior.
- [x] repository quality acceptance.
- [-] registry publication remains unauthorized.

Accepted seed:

```text
concepts:         4
reviewed aliases: 1
claim decisions:  6
mapped:           5
unmapped:         1
```

---

## C. Utility / epistemic governance — ACCEPTED

- [x] optimize useful career intelligence per unit user time.
- [x] source fact / normalized correspondence / analytical interpretation / recommendation remain distinct.
- [x] generated/candidate remains distinct from reviewed/promoted authority.
- [x] fail hard for integrity; fail soft for interpretive uncertainty.
- [x] human review is mainly a promotion boundary.
- [x] exhaustive canonicalization is not required before useful job-level interpretation.

---

## D. P2.2 Responsibility, Work, and Role Intelligence

Approved order:

```text
P2.2A Job Work Intelligence
→ P2.2B selective responsibility/deliverable promotion
→ P2.2C responsibility-family intelligence
→ P2.2D role-archetype intelligence
```

### D1 — P2.2A Job Work Intelligence — IMPLEMENTED / ACCEPTANCE OPEN

Current identities:

```text
schema:         job-work-intelligence-v2
prompt/runtime: job-work-intelligence-v2.0
limited model:  jobhunter-deterministic-limited-work-v2
```

#### v2 representation implementation — COMPLETE

- [x] separate typed model-candidate shape from persisted assembled artifact.
- [x] model owns grouping, emphasis, confidence, bounded interpretation, candidate deliverables, and candidate role characterization.
- [x] exact accepted P1.6 responsibility/role-purpose statements are injected deterministically after candidate reference validation.
- [x] final accepted work items persist source kind + index + exact statement + copied confidence.
- [x] remove free-form `work_summary`.
- [x] remove theme/deliverable/role `summary` fields from v2.
- [x] keep optional rationale explicitly interpretive.
- [x] retain supporting requirements as context only.
- [x] retain full direct-work coverage validation.
- [x] retain impossible-reference normalization only for structurally empty source sections.
- [x] retain bounded scope-intensifier guard on model-owned interpretation.
- [x] remove dedicated second semantic authority-review model call.
- [x] normal valid direct-work generation now uses one model call.
- [x] retain at most one bounded regeneration after deterministic candidate rejection.
- [x] requirement-only jobs remain deterministic `limited` and make no model call.
- [x] validate persisted/reused v2 kind/index/exact-statement/confidence against current accepted P1.6 before display.
- [x] preserve historical v1 artifacts/attempts without reusing them as v2.
- [x] browser visibly separates candidate theme from accepted P1.6 work and optional interpretation.
- [x] CLI mirrors the same authority hierarchy.
- [x] Work Intelligence remains outside public-corpus publication.
- [x] no SQL migration required.

Implementation record:

`docs/working-memory/2026-09-01_P2_2A_V2_REPRESENTATION_IMPLEMENTATION.md`

#### Repository quality — GREEN

Implementation/CLI head:

```text
d8e7f5d0a064dcec5e662101eac67d624ff925b1
```

CI run `33548003449`:

```text
Ruff                      PASS
full pytest               PASS
pytest warnings-as-errors PASS
quality job               SUCCESS
```

- [x] candidate schema/reference regressions.
- [x] exact tG9K production-readiness statement preservation regression.
- [x] exact tmyX hardening-related role-purpose preservation regression.
- [x] persisted kind/index/statement mismatch rejection regression.
- [x] one-call normal generation regression.
- [x] bounded repair/no-second-review regression.
- [x] limited-work no-fabrication regression.
- [x] historical v1 readable/not-reused regression.
- [x] browser/CLI authority-separation regression.
- [x] no-publication browser regression.

#### Real-local semantic/product acceptance — NEXT

Historical evidence already complete:

```text
tG9K/tmyX action-authority design defect → COMPLETE
another prompt/model trial matrix         → NOT REQUIRED
```

Acceptance sequence:

- [ ] `t4qV`: generate current v2 on accepted P1.6 44.
- [ ] `t4qV`: review theme usefulness and exact accepted-work presentation.
- [ ] `tmBK`: verify deterministic `limited` result and no invented duties.
- [ ] reuse: rerun at least one unchanged current v2 job and confirm artifact reuse.
- [ ] browser: inspect same real artifacts for immediate fact/interpretation distinction.
- [ ] CLI: confirm same assembled semantics.
- [ ] decide final P2.2A semantic/product acceptance.

Interpretive policy:

```text
candidate label/rationale imperfection
→ tolerate/record when clearly interpretive and useful

factual accepted-work mismatch
→ hard integrity failure

repeatable product-quality weakness
→ smallest general repair backed by cross-job evidence

semantic relationship problem
→ do not invent deterministic verb-equivalence machinery
```

### D2 — P2.2B selective responsibility/deliverable promotion — BLOCKED

- [ ] start only after D1 acceptance.
- [ ] promote only correspondences with demonstrated downstream reuse value.
- [ ] do not optimize mapping completeness.

### D3 — P2.2C responsibility families — LATER

- [ ] candidate families may precede promotion.
- [ ] promoted families require stronger reusable evidence/review.

### D4 — P2.2D role archetypes — LATER

- [ ] job-local candidate role interpretation is allowed now.
- [ ] stable reusable archetypes require stronger cross-job/employer evidence and explicit promotion.

---

## E. Still deferred / not authorized

- [-] Work Intelligence public-corpus publication.
- [-] canonical-registry publication.
- [-] automatic taxonomy growth/promotion.
- [-] exhaustive responsibility mapping for completeness.
- [-] deterministic action-verb equivalence system.
- [-] fixed primary-theme quota.
- [-] Market v2.
- [-] personal evidence/readiness/gap scoring/recommendations.
- [-] learning-plan generation/application ranking.
- [-] autonomous application/recruiter communication.
- [-] vector/RAG/graph infrastructure without demonstrated need.
- [-] generic source/plugin framework before a real second source.
- [-] multi-model voting without measured justification.

---

## Exact next action

```text
real-local t4qV v2 generation/review
→ tmBK deterministic limited verification
→ unchanged v2 reuse verification
→ browser authority/usability inspection
→ CLI same-semantics inspection
→ P2.2A acceptance decision
→ only then P2.2B decision
```
