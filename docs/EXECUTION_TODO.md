# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-08-15  
**Active working branch:** `main`  
**Authority:** Subordinate to product/domain/source/architecture constraints, `docs/ROADMAP.md`, `docs/IMPLEMENTATION_PLAN.md`, and `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`  
**Current focused plan:** `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`

Repository workflow rule:

```text
All current and next JobHunter implementation work proceeds directly on main.
Do not create a new working branch unless the user explicitly changes this rule.
```

Status vocabulary:

```text
[ ] not started
[~] in progress / implemented but acceptance incomplete
[x] completed/accepted for the stated bounded scope
[!] rejected / blocking defect for the stated candidate
[-] deliberately deferred
```

## A. Accepted foundation

- [x] Jobinja acquisition/provenance/source-version foundation.
- [x] `jobinja-detail-v2`.
- [x] `english-projection-v2` / `lm-studio-translation-v2`.
- [x] local browser + CLI shared services.
- [x] independent analysis/capability/blueprint model roles.
- [x] Review Snapshot v1 and current-chain routing.
- [x] deterministic CI gate: Ruff + full pytest + warnings-as-errors.
- [x] targeted `jobhunter jobs analyze <id>` command.
- [x] P1.6 v20 implementation/calibration stack consolidated into `main`.

## B. Semantic-quality gate

Do not jump to corpus-wide Phase 2.

### B1 — Review Snapshot routing

- [x] current-chain snapshot routing preserves model/dependency identities.
- [x] current-chain flags are trustworthy.
- [x] repository-safe exclusions remain intact.
- [x] public Review Snapshot distinguishes English v20/v5 from original v9/v4.
- [~] operationally verify Review Snapshot now selects Capability v9/v5 artifacts 11/12 after promotion.

### B2 — P1.6 factual extraction — PROMOTED / CLOSED

Public-current contracts:

```text
English:  job-analysis-english-v20 / job-analysis-v5
Original: job-analysis-original-v9 / job-analysis-v4
```

- [x] dense `tG9K` artifact 36: 33 requirements / 8 responsibilities / 0 role purpose.
- [x] dense mechanical audit PASS.
- [x] dense semantic review PASS WITH ACCEPTABLE DIFFERENCE.
- [x] sparse `t4jp` artifact 37: 8 requirements / 0 responsibilities / 0 role purpose.
- [x] sparse mechanical audit PASS.
- [x] sparse semantic non-regression PASS.
- [x] exact source evidence/provenance and complete source accounting.
- [x] required/preferred/contextual strength distinct from depth.
- [x] structured skills cannot silently disappear.
- [x] qualification-vs-duty protection.
- [x] schedule wording cannot become capability depth.
- [x] `experience` requires prior-applied-exposure evidence.
- [x] public English routing aligned across CLI, batch, browser, Market, Review Snapshot and Capability dependency selection.
- [x] public original-language path remains v9/v4.
- [x] normal `jobhunter jobs analyze tG9K` reuses artifact 36.
- [x] normal `jobhunter jobs analyze t4jp` reuses artifact 37.
- [x] normal Review Snapshot selects artifacts 36/37 with matching projection dependencies.
- [x] operational P1.6 v20 promotion complete.

### B3 — Capability Intelligence — V9 PUBLIC PROMOTION OPERATIONAL GATE

Current public code contract:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

#### Historical evidence

- [x] Capability v7 artifact 9 preserved as historical evidence tied to old P1.6 artifact 29.
- [!] v7 promoted-chain dense rebuild rejected: source-link/index loss then stable one-profile collapse.
- [x] do not reopen the v7 one-shot architecture.
- [x] Capability v8 source-led staging mechanically proved 31/31 dense requirement coverage and 8/8 responsibilities.
- [!] v8 semantic candidate rejected for depth/ownership/lifecycle and optionality inflation.
- [x] historical v7/v8 modules/artifacts remain preserved.

#### Capability v9 semantic contract — ACCEPTED

Final policy:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

Truth-protection rules retained:

- [x] complete capability-relevant requirement coverage.
- [x] complete responsibility coverage.
- [x] valid owned indices.
- [x] grounded evidence only.
- [x] dense anti-collapse protection.
- [x] role-level education / duration-only experience separation.
- [x] deterministic source requirement strength.
- [x] deterministic source-explicit depth.
- [x] deterministic source work activities.
- [x] preferred/contextual-only facts cannot independently justify inferred prerequisites.
- [x] unsupported ownership/lifecycle/autonomy/architecture analytical claims are blocked/filtered.
- [x] incomplete authoritative source truth cannot persist.

Over-enforcement removed/narrowed:

- [x] zero optional model enrichment is valid.
- [x] forced `unknown_scope` filler removed.
- [x] one unsafe optional item is filtered instead of killing a profile.
- [x] inflated profile summary falls back to normalized group summary.
- [x] planner prose overreach normalizes rather than retrying useful clustering.
- [x] redundant model `source_explicit` echoes are filtered; deterministic reconciliation remains authoritative.
- [x] prerequisite wording rules distinguish explicit inference from employer-stated obligation.

#### Dense v9 acceptance — COMPLETE

- [x] artifact 11 depends on P1.6 artifact 36.
- [x] 31/31 capability requirements linked.
- [x] 8/8 responsibilities linked.
- [x] capability explicit depth 5/5.
- [x] all explicit depth 6/6.
- [x] role-level indices `[31, 32]` separate.
- [x] semantic review PASS.

#### Sparse v9 acceptance — COMPLETE

- [x] artifact 12 depends on P1.6 artifact 37.
- [x] 8/8 requirements linked.
- [x] 0/0 responsibilities.
- [x] 0/0 explicit depth.
- [x] no fabricated role purpose, role-level constraints, duties, prerequisites, or depth.
- [x] semantic disposition PASS WITH ACCEPTABLE DIFFERENCES.

#### Public-promotion implementation — COMPLETE / CI PASS

- [x] neutral/current `capability_service.py` promotes v9/v5.
- [x] CLI/browser/Review Snapshot follow the neutral current facade.
- [x] current formatter is v9 formatter.
- [x] current builder uses staged v9 service.
- [x] neutral facade preserves model/provider inspection surface.
- [x] current-service tests migrated from obsolete one-shot v7 fake-provider shape to deterministic v9 staged fixture.
- [x] exact P1.6 dependency/reuse/fail-closed assertions preserved.
- [x] deferred Blueprint v6 pinned explicitly to historical Capability v7 constants.
- [x] compare proved Blueprint isolation is only a one-line dependency import change.
- [x] historical v7/v8/v9 modules remain available.
- [x] CI 874 Ruff PASS.
- [x] CI 874 full pytest PASS.
- [x] CI 874 warnings-as-errors PASS.

#### Operational promotion verification — CURRENT NEXT GATE

- [ ] pull latest `main` locally.
- [ ] normal `jobhunter jobs capability tG9K` reuses artifact 11 under v9/v5.
- [ ] normal `jobhunter jobs capability t4jp` reuses artifact 12 under v9/v5.
- [ ] normal `jobhunter jobs snapshot tG9K` marks Capability artifact 11 current on P1.6 artifact 36.
- [ ] normal `jobhunter jobs snapshot t4jp` marks Capability artifact 12 current on P1.6 artifact 37.
- [ ] verify no new Capability generation occurs for these accepted current dependencies.
- [ ] verify Blueprint remains deferred/pinned and is not silently rebuilt/rebased on v9.
- [ ] after proof, mark Capability v9 public promotion operationally CLOSED.

**Next exact commands:**

```bash
cd ~/projects/jobhunter
git pull --ff-only origin main

jobhunter jobs capability tG9K
jobhunter jobs capability t4jp

jobhunter jobs snapshot tG9K
jobhunter jobs snapshot t4jp
```

Key current records:

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_DENSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_SPARSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_PUBLIC_PROMOTION.md
```

### B4 — Role Capability Blueprint experiment

**Status: [-] not accepted for Phase-1 use; tuning deferred.**

- [x] historical v6/12B artifact 7 remains experimental evidence.
- [!] semantic review found unsupported assumptions.
- [x] Blueprint v6 is pinned to historical v7 during Capability v9 promotion.
- [x] do not resume Blueprint tuning during this gate.

### B5 — Heterogeneous live review

Blocked only until Capability v9 operational-promotion verification closes.

- [ ] Python/software role.
- [ ] network/security role.
- [ ] operations/platform/DevOps role.
- [ ] convert repeatable deterministic defects into fixtures.
- [ ] record model limitations separately from deterministic defects.
- [ ] decide whether promoted P1.6 + promoted Capability are good enough to freeze as Phase-2 input.

## C. Phase-1 closure after heterogeneous semantic acceptance

### C1 — Market truthfulness

- [ ] analyzed-current sample size visible.
- [ ] source/filter/contract scope recoverable.
- [ ] small-sample/concentration warnings.
- [ ] coverage metrics separate from semantic certification.

### C2 — Source/lifecycle

- [ ] network/429/5xx/challenge/auth failure != expired/removed.
- [ ] cautious 404/410/repeated-missing lifecycle handling.
- [ ] last-successful / consecutive-failure summaries accepted.

### C3 — Partial-success truthfulness

- [ ] expose requested / attempted / completed / reused / skipped / failed / remaining eligible.
- [ ] browser/CLI summaries agree.
- [ ] earlier durable success survives later failure.
- [ ] no-eligible-work != attempted-and-failed.

### C4 — P1.7 final workflow

- [ ] final per-job report/provenance.
- [ ] ready-job queue.
- [ ] combined current-corpus report.
- [ ] `jobhunter run` deterministic acceptance.
- [ ] browser equivalent acceptance.
- [ ] rerun/idempotency proof.
- [ ] bounded live end-to-end Phase-1 acceptance.

### C5 — Phase-1 closure

- [ ] acceptance summary with exact corpus/sample/contracts/bounds.
- [ ] reconcile final accepted docs.
- [ ] freeze accepted P1.6 + Capability starting contract for Phase 2.
- [ ] keep Blueprint deferred/non-authoritative unless later evidence reopens it.

## D. Phase 2 — gated

Do not begin until Phase-1 closure.

```text
canonical concept registry
→ reviewed aliases/mappings
→ responsibilities/deliverables
→ corpus-scale capability requirement profiles
→ role archetypes
→ Market v2
→ later personal evidence/gap intelligence
```

Still deferred: automatic taxonomy growth, corpus-wide Blueprint generation, personal readiness scoring, learning-plan generation, application ranking, autonomous applications, vector/RAG infrastructure, generic plugin framework, and multi-model voting.
