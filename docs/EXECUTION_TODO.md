# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-09-05  
**Active working branch:** `main`  
**Authority:** Subordinate to product/domain/source/architecture constraints, `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`, `docs/ROADMAP.md`, `docs/IMPLEMENTATION_PLAN.md`, and the controlling focused P2.2 plans  
**Current-state reconciliation:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-05.md`  
**Current focused product plan:** `docs/P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md`  
**Current product gate:** P2.2B-B1 REPO EVIDENCE SELECTED / `ta9l` P1.6 ACCEPTANCE NEXT / NO PROMOTION YET  
**Parallel portfolio gate:** PR9 repository-side package complete / owner-external release actions + owner mastery pending

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

Accepted seed remains deliberately small:

```text
concepts:         4
reviewed aliases: 1
claim decisions:  6
mapped:           5
unmapped:         1
```

---

## C. Utility / epistemic governance — ACCEPTED

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

### D1 — P2.2A Job Work Intelligence — ACCEPTED / CLOSED

Current identities:

```text
schema:         job-work-intelligence-v2
prompt/runtime: job-work-intelligence-v2.0
limited model:  jobhunter-deterministic-limited-work-v2
```

- [x] exact accepted P1.6 factual work separated from model-owned interpretation.
- [x] deterministic exact-work injection and currentness validation.
- [x] one normal candidate model call; at most one bounded regeneration after deterministic rejection.
- [x] no dedicated second semantic authority-review pass.
- [x] deterministic limited path for requirement-only jobs.
- [x] browser/CLI authority separation.
- [x] repository quality green.
- [x] real-local `t4qV → tmBK → reuse → browser → CLI` acceptance passed.
- [x] P2.2A ACCEPTED / CLOSED.

Acceptance record:

`docs/working-memory/2026-09-01_P2_2A_V2_REAL_LOCAL_ACCEPTANCE.md`

### D2 — P2.2B-B1 selective responsibility promotion — IN PROGRESS / `ta9l` P1.6 GATE

Controlling focused plan:

`docs/P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md`

Repository evidence record:

`docs/working-memory/2026-09-01_P2_2B_B1_REPO_EVIDENCE_SELECTION.md`

#### Decision and boundaries

- [x] P2.2A prerequisite accepted.
- [x] authorize B1 as one bounded responsibility-promotion pilot.
- [x] reuse `jobhunter-canonical-concept-registry-v1` unchanged unless a concrete eligible pair proves a real contract gap.
- [x] target at most one reviewed responsibility concept with two exact accepted/current P1.6 responsibility mappings.
- [x] reject completeness-driven mapping.
- [x] defer deliverable promotion/schema from B1.
- [x] allow an explicit no-promotion result if evidence is insufficient.

#### Rejected candidates

- [x] reject `t4qV` responsibility[9] + `tmyX` responsibility[3]: equipment-specific documentation versus compound checklists/documentation/reports.
- [x] reject `t49W` vulnerability work + `tmyX`: remediation/priority/engineering scope differs from investigation/configuration weakness + corrective suggestions.
- [x] reject `t49N` vulnerability work + `tmyX`: vulnerability assessment + risk analysis + remediation coordination is materially compound/different.
- [x] reject `tGM0` backend/AI-integration duties + `tG9K`: different responsibility identity.
- [x] keep `tG9K` pipeline duty + `ta9l` RAG pipeline duty as a weaker alternative, not the selected candidate.

#### Bounded evidence selection — REPO SIDE COMPLETE

- [x] inspect committed current projection / fetched-job evidence for one strong recurrence.
- [x] stop the bounded scan once a stronger candidate was identified rather than scan all 353 discovered jobs.
- [x] select `ta9l` (Senior Applied AI Engineer, parsed source detail 25) as the single additional evidence-bearing P1.6 candidate.
- [x] accepted anchor: `tG9K` P1.6 36 responsibility[5] = `Design rigorous validation and monitoring for models running in an industrial setting.`
- [x] `ta9l` employer duty candidate = `Create evaluation, testing, and observability frameworks for LLM and agent performance.`
- [x] tentative identity: `responsibility:design-ai-evaluation-monitoring` / `Design AI evaluation and monitoring`.
- [x] downstream hypothesis: reusable AI/ML reliability, evaluation, and monitoring work across industrial ML and LLM/agent roles.
- [x] verify repo-side semantic shape has no unrelated ownership/lifecycle action; source-specific setting/model/testing/observability details remain source detail.

#### `ta9l` P1.6 authority gate — NEXT / LOCAL RUNTIME REQUIRED

- [ ] create/reuse current English projection for `ta9l`.
- [ ] generate English P1.6 using `job-analysis-english-v20 / job-analysis-v5`.
- [ ] semantically review the `ta9l` P1.6 artifact for acceptance.
- [ ] report exact accepted artifact ID, responsibility index, statement, evidence, and semantic-review state for the evaluation/testing/observability duty.
- [ ] if the P1.6 claim materially changes/splits the responsibility shape, re-evaluate correspondence before mutation.
- [ ] if it remains aligned, perform final two-P1.6-claim correspondence review before canonical mutation.

#### Promotion pilot — ONLY AFTER `ta9l` P1.6 ACCEPTANCE + FINAL REVIEW

- [ ] create/reuse exactly one reviewed responsibility concept.
- [ ] map exactly the two approved accepted/current P1.6 responsibility claims.
- [ ] rerun the reviewed operations and verify idempotent reuse.
- [ ] inspect current mappings/concept in CLI.
- [ ] inspect same authority/provenance in browser.
- [ ] verify stale/current behavior remains intact.
- [ ] verify no registry/P2.2 public-corpus publication occurred.
- [ ] decide B1 PASS or evidence-based NO-PROMOTION / DEFER.

### D3 — P2.2C responsibility families — BLOCKED

- [ ] do not start until B1 proves useful reusable responsibility authority or explicitly records the evidence-based reason to defer promotion.
- [ ] candidate families may precede promotion only under a separate focused decision.

### D4 — P2.2D role archetypes — LATER

- [ ] job-local candidate role interpretation already exists in P2.2A.
- [ ] stable reusable archetypes require stronger cross-job/employer evidence and explicit promotion.

---

## E. Portfolio / release readiness — PARALLEL TRACK

This track improves repository demonstrability and professional presentation without changing the P2.2 product gate.

- [x] PR0 portfolio-readiness audit.
- [x] PR1 README/public landing story.
- [x] PR2 current architecture/engineering story.
- [x] PR3 documentation information architecture.
- [x] PR4 current/historical versioned-code disposition.
- [x] PR5 bounded current-code readability/shared-web refactor.
- [x] PR6 repository-side reproducible public-corpus demo.
- [x] PR7 developer onboarding/install path.
- [x] PR8 repository/package/security/configuration hygiene.
- [x] PR9-A final repository/public consistency audit.
- [ ] PR9-B owner/external blockers: license decision, GitHub description/topics, real browser screenshots + privacy review.
- [ ] PR9-C intentional `v0.1.0` tag/GitHub release after blockers and final CI.
- [x] PR9-D release/CV/interview package prepared.
- [ ] PR9-E owner mastery verification.

Prepared package:

`docs/PORTFOLIO_RELEASE_CV_AND_INTERVIEW_PACKAGE.md`

Do not continue generic portfolio polishing after the remaining concrete blockers are closed.

---

## F. Still deferred / not authorized

- [-] Work Intelligence public-corpus publication.
- [-] canonical-registry publication.
- [-] automatic taxonomy growth/promotion.
- [-] exhaustive responsibility mapping for completeness.
- [-] P2.2B deliverable promotion until concrete repeated-value evidence exists.
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

## Exact next actions

### Product track

```text
local runtime: ta9l English projection
→ ta9l P1.6 v20 generation + semantic acceptance review
→ report exact accepted responsibility shape
→ final correspondence review against tG9K P1.6 36 responsibility[5]
→ only then canonical mutation
```

Do not accept a second new job or manufacture a promotion if `ta9l` does not preserve the selected responsibility shape.

### Portfolio/release track

```text
owner license-policy decision
→ GitHub description/topics settings action
→ real local browser screenshots + privacy review
→ final public-count/version/current-state check
→ final CI green
→ intentional v0.1.0 tag/release
→ verify tagged public surfaces
→ owner mastery verification
```

Neither track authorizes the other to bypass its gate.
