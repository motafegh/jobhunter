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

### B3 — Capability Intelligence — ACTIVE V9 LIVE GATE

#### Historical/public v7 baseline

```text
historical P1.6 artifact 29
→ Capability v7 artifact 9
```

- [x] `job-capability-intelligence-v7` / schema v4 remains the historical/public accepted baseline.
- [x] artifact 9 is intentionally non-current because current P1.6 is artifact 36.
- [x] public Capability model-facing P1.6 view strips free-form rationale while preserving authoritative semantic fields.

#### Promoted-chain v7 rebuild — REJECTED DENSE ONE-SHOT PATH

- [!] attempt 1 omitted most source links; retry invented responsibility index 9 outside valid 0..7.
- [x] invalid output did not persist.
- [x] narrow deterministic index/evidence repair implemented; CI 811 PASS.
- [!] attempt 2 collapsed dense evidence into one giant profile and omitted 22 capability-relevant requirements even after retry feedback.
- [x] classify as stable one-shot architecture failure rather than isolated index noise.
- [x] do not increase retries.
- [x] do not weaken whole-artifact coverage validation.

#### Capability v8 source-led candidate — MECHANICAL PASS / SEMANTIC REJECT

- [x] source-led group-plan → bounded assignment → bounded profile architecture implemented.
- [x] dense `tG9K` completed against P1.6 artifact 36.
- [x] 31/31 capability requirements linked.
- [x] 8/8 responsibilities linked.
- [x] four profiles generated.
- [x] role-level indices `[31, 32]` remained separate.
- [x] source-led architecture solved v7 dense linkage/coverage failure mechanically.
- [!] v8 model prose inflated depth, ownership/lifecycle scope, and contextual/preferred facts.
- [!] v8 is NOT semantically accepted and MUST NOT be publicly promoted.
- [x] persisted v8 candidate remains historical evidence; do not overwrite/delete it.
- [x] correct depth accounting: capability 5/5 + role-level 1 = all 6/6.

#### Capability v9 live failure history — FOUR FAILURES / NO ARTIFACT

- [!] live failure 1: model profile summary/derived items crossed semantic authority boundaries.
- [x] no v9 artifact persisted.
- [x] per-item fail-closed filtering implemented; CI 838 PASS.
- [!] live failure 2: model returned neutral profile with no derived reasoning and inherited v8 forced-enrichment validator rejected it.
- [x] no v9 artifact persisted.
- [x] identified direct contradiction: `do not speculate` vs `must add derived reasoning or unknown scope`.
- [!] live failure 3: useful five-group dense plan was rejected before assignment because non-authoritative planner prose used words such as `requires`, `advanced`, `expertise`, `deep`, `proficiency`, `necessary`, and `end-to-end`.
- [x] no v9 artifact persisted.
- [x] classify failure 3 as planner prose over-enforcement, not source-coverage or grouping-structure failure.
- [!] live failure 4: bounded profile reasoning echoed source-owned `Hands-on` / `Solid` depth and source-backed operational context using `evidence_status="source_explicit"`; v9 rejected the whole profile because model-owned lists allowed only derived statuses.
- [x] no v9 artifact persisted.
- [x] classify failure 4 as redundant source-truth echo over-enforcement, not hallucination or source corruption.
- [x] model-emitted `source_explicit` analytical items are now filtered as redundancy; deterministic reconciliation remains the sole source-explicit authority.

#### Capability v9 strictness audit + simplification — IMPLEMENTED / DETERMINISTIC PASS

Contract remains candidate-only:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

Truth-protection rules retained:

- [x] complete capability-relevant requirement coverage remains mandatory.
- [x] complete responsibility coverage remains mandatory.
- [x] valid owned indices remain mandatory.
- [x] evidence grounding remains mandatory.
- [x] dense multi-group protection remains mandatory.
- [x] group IDs and normalized labels remain structurally distinct.
- [x] role-level education / duration-only experience separation remains mandatory.
- [x] source requirement strength remains deterministic.
- [x] source-explicit depth remains deterministic.
- [x] source work activities remain deterministic.
- [x] preferred/contextual-only facts still cannot independently justify inferred prerequisites.
- [x] unsupported ownership/lifecycle/autonomy/architecture analytical claims remain blocked.
- [x] incomplete authoritative source truth still fails before persistence.

Contradictory / unnecessary strictness removed or narrowed:

- [x] REMOVE v9 requirement that every profile must add derived reasoning or unknown scope.
- [x] REMOVE forced `unknown_scope` filler when no genuine unknown claim exists.
- [x] MAKE model-derived depth/sub-capability/knowledge/practice/context enrichment optional.
- [x] REPLACE whole-profile failure for one unsafe optional inference with item-level fail-closed filtering.
- [x] REPLACE inflated profile-summary retry with fallback to normalized group summary.
- [x] REMOVE duplicate hard-coded v8 revalidation after provider has already validated a v9 stage.
- [x] preserve historical v8 fallback validation for fake/legacy providers and historical v8 behavior.
- [x] NARROW prerequisite wording rule: explicit `model_inferred_prerequisite` may use necessity/prerequisite language.
- [x] KEEP inferred-prerequisite statement from masquerading as employer `required/must/mandatory`.
- [x] ALLOW inferred-prerequisite rationale to accurately refer to a required source fact.
- [x] KEEP preferred/contextual-only prerequisite inflation blocked by source-strength evidence logic.
- [x] v9 final profile/draft contract permits zero optional model enrichment.
- [x] trusted deterministic reconciliation still injects source strength/depth/work truth.
- [x] any internal compatibility bridge is removed before v9 persistence.
- [x] REPLACE planner prose lexical hard-failure with deterministic normalization.
- [x] preserve useful planner group IDs/boundaries when only planner wording overreaches.
- [x] remove claim-like strength/depth/scope modifiers from planner labels while preserving legitimate `Deep Learning`.
- [x] replace inflated planner summaries with `This capability area covers <label>.`.
- [x] replace inflated role interpretation with neutral synthesis of normalized group labels.
- [x] record planner normalization as deterministic uncertainty.
- [x] KEEP duplicate/collapsed normalized labels, invalid IDs/group counts, and dense structural collapse as hard failures.
- [x] FILTER model-emitted `source_explicit` analytical items as redundant/misplaced rather than failing the bounded profile.
- [x] KEEP deterministic reconciliation as the only authority that injects accepted source-explicit depth/work/source truth.
- [x] preserve the pre-filter v9 implementation in `capability_v9_models_core.py`; keep the public v9 model module as a thin inference-boundary wrapper.

Regression proofs:

- [x] zero-enrichment profile succeeds under v9.
- [x] zero-enrichment profile still fails under historical v8.
- [x] zero-enrichment final v9 artifact survives deterministic reconciliation.
- [x] deterministic required strength and source-explicit depth remain present.
- [x] preferred-only inferred prerequisite is filtered.
- [x] required-grounded inferred prerequisite can use prerequisite language.
- [x] typed v9 response is not accidentally revalidated as v8.
- [x] inflated planner prose normalizes instead of retrying.
- [x] exact five-group structure from live failure 3 survives planner normalization.
- [x] legitimate `Deep Learning` terminology survives label normalization.
- [x] source-explicit depth/context echoes are filtered without failing profile reasoning.
- [x] accepted source-explicit truth is still injected deterministically downstream.

Deterministic gates:

- [x] CI 849 Ruff PASS.
- [x] CI 849 full pytest PASS — 434 tests.
- [x] CI 849 warnings-as-errors PASS.
- [x] CI 855 Ruff PASS.
- [x] CI 855 full pytest PASS — 435 tests.
- [x] CI 855 warnings-as-errors PASS.
- [x] CI 862 Ruff PASS.
- [x] CI 862 full pytest PASS.
- [x] CI 862 warnings-as-errors PASS.
- [x] CI 864 final reconciled documentation head PASS.

Live acceptance still pending:

- [~] rerun isolated dense `tG9K` v9 candidate against P1.6 artifact 36 after source-echo filtering.
- [ ] verify new v9 artifact identity/dependency if persisted.
- [ ] verify 31/31 capability requirements linked.
- [ ] verify 8/8 responsibilities linked.
- [ ] verify capability explicit depth 5/5 and all depth 6/6.
- [ ] verify role-level indices `[31, 32]` remain separate.
- [ ] full semantic review: no source-strength/depth/ownership/lifecycle inflation.
- [ ] verify preferred/contextual facts are not promoted.
- [ ] accept zero optional enrichment as valid when a profile has nothing defensible to add.
- [ ] verify planner normalization remains non-authoritative and does not alter source truth.
- [ ] verify model-emitted source-explicit echoes are absent from accepted model-owned enrichment and represented only through deterministic source truth.
- [ ] only after dense acceptance run sparse `t4jp` v9 non-regression.
- [ ] only after dense + sparse acceptance decide whether v9 is suitable for public promotion.

**Next exact command:**

```bash
cd ~/projects/jobhunter
git pull --ff-only origin main
python scripts/run_capability_v9_candidate.py --job-id tG9K
```

Do not use normal `jobhunter jobs capability`; public routing intentionally remains v7.

Key current record:

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_STRICTNESS_AUDIT_AND_SIMPLIFICATION.md
```

Supporting history:

```text
docs/working-memory/2026-08-15_CAPABILITY_V7_PROMOTED_P16_LINKAGE_FAILURE.md
docs/working-memory/2026-08-15_CAPABILITY_V8_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-15_CAPABILITY_V8_LIVE_REVIEW_AND_V9_BOUNDARY.md
docs/working-memory/2026-08-15_CAPABILITY_V9_DERIVED_EXPECTATION_FILTERING.md
docs/working-memory/2026-08-15_CAPABILITY_V9_LIVE_FAILURES_AND_DESIGN_PAUSE.md
```

### B4 — Role Capability Blueprint experiment

**Status: [-] not accepted for Phase-1 use; tuning deferred.**

- [x] deterministic provenance failure class fixed historically.
- [x] historical v6/12B artifact 7 passed mechanical audit and CI.
- [!] semantic review still found unsupported assumptions.
- [x] do not resume Blueprint tuning during the Capability gate.

### B5 — Heterogeneous live review

Blocked until Capability candidate acceptance/promotion decision.

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
