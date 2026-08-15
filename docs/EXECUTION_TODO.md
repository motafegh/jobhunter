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
- [x] v17→v20 P1.6 implementation/calibration stack consolidated into `main`.

## B. Semantic-quality gate

Do not jump to corpus-wide Phase 2.

### B1 — Review Snapshot routing

- [x] current-chain snapshot routing preserves model/dependency identities.
- [x] current-chain flags are trustworthy.
- [x] repository-safe exclusions remain intact.
- [x] public Review Snapshot distinguishes English v20/v5 from original v9/v4.

### B2 — P1.6 factual extraction — PROMOTED / CLOSED

Public-current contracts:

```text
English:  job-analysis-english-v20 / job-analysis-v5
Original: job-analysis-original-v9 / job-analysis-v4
```

Permanent boundaries:

- [x] exact source evidence/provenance.
- [x] no unsupported/invented career claims.
- [x] required/preferred/contextual strength distinct.
- [x] depth separate from obligation and normalized concept/scope.
- [x] structured skills cannot silently disappear.
- [x] exact qualification-list evidence.
- [x] complete residual/decomposed source accounting.
- [x] qualification-vs-responsibility protection.
- [x] schedule wording cannot become capability depth.
- [x] clean reusable concepts and ontology.
- [x] `experience` requires prior-applied-exposure evidence.
- [x] fail closed before persistence when complete contract is not satisfied.

Dense `tG9K` v20 artifact 36:

- [x] 33 requirements / 8 responsibilities / 0 role purpose.
- [x] mechanical audit PASS.
- [x] semantic review PASS WITH ACCEPTABLE DIFFERENCE.
- [x] all accepted dense source facts retained.
- [x] all six structured required skills retained.
- [x] education + exact 3–6 years professional experience retained.
- [x] optionality/depth/contextual stack calibrated.

Sparse `t4jp` v20 artifact 37:

- [x] 8 requirements / 0 responsibilities / 0 role purpose.
- [x] 3/3 structured skills.
- [x] 4/4 qualification-list items.
- [x] 4/4 residual decisions.
- [x] mechanical audit PASS.
- [x] semantic non-regression PASS.

Promotion closure:

- [x] public English routing aligned across targeted CLI, batch, browser, Market, Review Snapshot and Capability dependency selection.
- [x] public original-language path preserved on v9/v4.
- [x] deterministic promotion CI PASS.
- [x] normal `jobhunter jobs analyze tG9K` reuses artifact 36.
- [x] normal `jobhunter jobs analyze t4jp` reuses artifact 37.
- [x] normal Review Snapshot selects artifacts 36 and 37 with matching projection dependencies.
- [x] old Capability/Blueprint artifacts correctly reported as present-but-non-current.
- [x] operational P1.6 v20 promotion declared complete.

Key records:

```text
docs/working-memory/2026-08-15_P16_V20_DENSE_ARTIFACT_36_SEMANTIC_ACCEPTANCE.md
docs/working-memory/2026-08-15_P16_V20_SPARSE_ARTIFACT_37_ACCEPTANCE.md
docs/working-memory/2026-08-15_P16_V20_PUBLIC_PROMOTION_ACCEPTANCE.md
```

### B3 — Capability Intelligence — ACTIVE

#### Historical accepted v7 baseline

```text
historical P1.6 artifact 29
→ Capability v7 artifact 9
```

- [x] `job-capability-intelligence-v7` / schema v4 accepted for the historical bounded `tG9K` chain.
- [x] historical artifact 9 retained complete source truth for its old P1.6 dependency.
- [x] artifact 9 is now intentionally non-current because promoted P1.6 is artifact 36.

#### P1.6 rationale boundary

- [x] public Capability model-facing P1.6 view strips free-form `rationale` recursively.
- [x] persisted P1.6 artifact remains unchanged.
- [x] authoritative concept/type/strength/depth/evidence/confidence remain available.
- [x] CI 807 passed rationale-boundary regression tests.

#### Promoted-chain v7 rebuild — REJECTED FOR DENSE ONE-SHOT PATH

Attempt 1 against P1.6 artifact 36:

- [!] generation 1 omitted most capability-relevant source links.
- [!] retry invented responsibility index `9` although only `0..7` exist.
- [x] no invalid artifact persisted.
- [x] narrow positive-out-of-range/exact-evidence source-link repair implemented without weakening strict coverage.
- [x] CI 811 PASS after v7 repair.

Attempt 2:

- [!] both generations collapsed dense `tG9K` into one giant capability profile.
- [!] retry knew the missing requirement ledger but still failed to restructure.
- [!] final missing capability-relevant indices remained `[2, 3, 4, 5, 6, 9, 10, 12, 13, 15, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 29, 30]`.
- [x] no invalid artifact persisted.
- [x] classify this as stable one-shot architecture failure, not isolated index noise.
- [x] do not increase retries.
- [x] do not loosen final coverage validation.
- [x] stop iterative mutation of historical/public v7 semantics for this dense input.

Record:

```text
docs/working-memory/2026-08-15_CAPABILITY_V7_PROMOTED_P16_LINKAGE_FAILURE.md
```

#### Capability v8 source-led candidate — IMPLEMENTED / LIVE ACCEPTANCE PENDING

Architecture:

```text
accepted P1.6 source truth
→ compact semantic capability-group plan
→ bounded exact source-fact assignment partitions
→ bounded per-group reasoning
→ deterministic source-link injection
→ existing strict v7 reconciliation/source truth
→ persist only after complete validation
```

Implementation:

- [x] `CapabilityGroupPlanV8` separates group semantics from source-index bookkeeping.
- [x] dense group plan requires at least two groups.
- [x] capability requirements partition in chunks of at most 8.
- [x] responsibilities distributed into bounded assignment partitions exactly once.
- [x] every assignment partition must cover exactly its owned requirement/responsibility indices.
- [x] assignments may use only known group IDs.
- [x] each source fact may map to at most two groups.
- [x] dense final assignment must use at least two groups.
- [x] per-group reasoning receives only assigned facts + matching evidence references.
- [x] per-group model output owns no source links, source-explicit strength/depth, or source-explicit duties.
- [x] JobHunter injects validated source links deterministically.
- [x] existing v7 reconciliation still derives strength, explicit depth, source work activities, role-level constraints and complete source truth.
- [x] P1.6 rationale remains excluded from model-facing payloads.
- [x] persisted schema remains v4; candidate prompt identity is `job-capability-intelligence-v8`.
- [x] isolated candidate runner added: `scripts/run_capability_v8_candidate.py`.
- [x] model/partition/service tests added.
- [x] Ruff PASS — CI 821.
- [x] full pytest PASS — CI 821.
- [x] warnings-as-errors PASS — CI 821.
- [~] run dense `tG9K` v8 candidate against promoted P1.6 artifact 36.
- [ ] if persisted, perform mechanical source-truth/dependency audit.
- [ ] perform full semantic review of dense capability grouping/reasoning.
- [ ] verify no contextual/preferred-tool strength inflation.
- [ ] verify no ownership/autonomy/leadership fabrication.
- [ ] verify no unsupported architecture or generic curriculum expansion.
- [ ] run sparse `t4jp` v8 non-regression only after dense acceptance.
- [ ] consider public Capability v8 promotion only after dense + sparse acceptance.

Detailed v8 record:

```text
docs/working-memory/2026-08-15_CAPABILITY_V8_SOURCE_LED_PARTITIONING.md
```

**Next exact command:**

```bash
cd ~/projects/jobhunter
git pull --ff-only origin main
python scripts/run_capability_v8_candidate.py --job-id tG9K
```

Do not use normal `jobhunter jobs capability` for this candidate gate; the public route intentionally remains v7.

### B4 — Role Capability Blueprint experiment

**Status: [-] not accepted for Phase-1 use; tuning deferred.**

- [x] deterministic provenance failure class fixed historically.
- [x] v6/12B artifact 7 passed mechanical audit and CI historically.
- [!] semantic review still found unsupported assumptions.
- [x] do not resume Blueprint tuning during the Capability gate.

### B5 — Heterogeneous live review

Do not begin until Capability candidate acceptance/promotion decision.

Future targets:

- [ ] Python/software role.
- [ ] network/security role.
- [ ] operations/platform/DevOps role.
- [ ] convert repeatable deterministic defects into fixtures.
- [ ] record model limitations separately from deterministic defects.
- [ ] decide whether promoted P1.6 + accepted Capability are good enough to freeze as Phase-2 input.

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
