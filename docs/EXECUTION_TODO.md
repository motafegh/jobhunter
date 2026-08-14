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
- [x] v17→v20 implementation/calibration stack consolidated into `main` through merged PRs #5–#8.

## B. Semantic-quality gate

Do not jump to corpus-wide Phase 2.

### B1 — Review Snapshot routing

- [x] current-chain snapshot routing preserves model/dependency identities.
- [x] current-chain flags are trustworthy.
- [x] repository-safe exclusions remain intact.

### B2 — P1.6 factual extraction

**V20 dense + sparse bounded calibration is complete and all implementation/history is now on `main`. Public/accepted P1.6 remains v9/schema-v4 until explicit promotion routing is implemented and verified. Active gate: P1.6 v20 promotion implementation on `main`.**

#### Accepted public baseline before promotion

Dense `tG9K` v9 artifact 29:

- [x] 27 requirements / 7 responsibilities / 1 role purpose.
- [x] optionality/depth/contextual stack calibrated.
- [x] education and 3–6 years professional experience retained.

Sparse `t4jp` v16 artifact 35 remains the historical sparse calibration baseline.

#### Permanent semantic boundaries

- [x] exact source evidence/provenance.
- [x] no unsupported/invented career claims.
- [x] required/preferred/contextual strength distinct.
- [x] depth separate from obligation and normalized concept/scope.
- [x] structured `skills[]` cannot silently disappear.
- [x] exact qualification-list evidence.
- [x] deterministic coarse-span decomposition bookkeeping.
- [x] complete residual sentence accounting.
- [x] qualification-vs-responsibility protection.
- [x] schedule wording cannot become capability depth.
- [x] clean reusable concepts.
- [x] ontology: skill/tool/knowledge/practice/domain/experience/education/other.
- [x] `experience` requires prior-applied-exposure evidence.
- [x] fail closed before persistence when complete contract is not satisfied.

#### V17 → V20 correction chain

- [x] v17 removed arbitrary 32-requirement ceiling.
- [x] v17 aggregated dense coverage defects.
- [x] v18 deterministic structured minimum experience + education.
- [x] v18 structured skills non-excludable.
- [x] v19 optionality/depth separation + genuine source depth preservation.
- [x] v19 exposed dense whole-answer retry oscillation.
- [x] v20 bounded source-led partitions (max 8 model-owned refs).
- [x] v20 exact partition-scope enforcement + independent merge.
- [x] v20 `some C / C++ helpful` → preferred + null depth.
- [x] v20 `industrial / edge deployment` → scope, not depth/unsupported experience.
- [x] v20 preferred `experience` requires prior-exposure evidence.
- [x] historical PR #5 merged to main.
- [x] historical PR #6 merged to main.
- [x] historical PR #7 merged to main.
- [x] historical PR #8 merged to main.

Detailed v20 records:

```text
docs/working-memory/2026-08-14_P16_V20_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-14_P16_V20_FIRST_LIVE_PARTITION_CORRECTION.md
docs/working-memory/2026-08-14_P16_V20_SECOND_LIVE_SCOPE_DEPTH_CORRECTION.md
docs/working-memory/2026-08-14_P16_V20_DENSE_ARTIFACT_36_PERSISTED.md
docs/working-memory/2026-08-15_P16_V20_DENSE_ARTIFACT_36_MECHANICAL_AUDIT_PASS.md
docs/working-memory/2026-08-15_P16_V20_DENSE_ARTIFACT_36_SEMANTIC_ACCEPTANCE.md
docs/working-memory/2026-08-15_P16_V20_SPARSE_ARTIFACT_37_ACCEPTANCE.md
docs/working-memory/2026-08-15_P16_V20_PROMOTION_ROUTING_DESIGN.md
```

#### Dense v20 `tG9K` artifact 36 — PASS

```text
Requirements:      33
Responsibilities:  8
Role purpose:      0
Mechanical audit:  PASS
Semantic review:   PASS WITH ACCEPTABLE DIFFERENCE
```

- [x] all 27 accepted v9 source-derived requirements retained.
- [x] all six structured required skills added/retained.
- [x] Master's degree and exact 3–6 year professional-experience depth correct.
- [x] `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort` correct.
- [x] MATLAB/C++ preferred + null depth.
- [x] industrial/edge deployment preferred scope + null depth, no fabricated experience.
- [x] contextual stack remains contextual.
- [x] no silent dense factual loss.
- [x] 8-vs-7 duty count explained and accepted: v20 treats the opening concrete `Build and validate...` action as responsibility rather than v9 role purpose.

#### Sparse v20 `t4jp` artifact 37 — PASS

```text
Requirements:                8
Responsibilities:            0
Role purpose:                0
Structured skills:           3/3
Qualification-list items:    4/4
Residual coverage decisions: 4/4
Decomposed coarse decisions: 1
Mechanical audit:            PASS
Semantic non-regression:     PASS
```

- [x] sparse v20 artifact persisted.
- [x] 3/3 structured required skills represented.
- [x] 4/4 qualification items represented.
- [x] 4/4 residual decisions accounted.
- [x] 0 responsibilities.
- [x] 0 role purpose.
- [x] no fabricated duty/purpose.
- [x] no education/minimum-experience fabrication from `it doesn't matter`.
- [x] no schedule wording in concept/depth.
- [x] no deterministic over-extraction.
- [x] semantic comparison against v16 artifact 35 passed.
- [x] `social networks` ontology difference (`tool` vs prior `skill`) accepted as defensible with unchanged fact/evidence/strength.
- [x] model rationale hygiene issue recorded separately: one correct `Visual content production` claim has `depth_signal=null` but rationale inaccurately mentions capturing schedule as depth. Do not treat free-form rationale as authoritative semantics.

#### V20 calibration boundary

- [x] v20 deterministic CI PASS.
- [x] dense tG9K persistence PASS.
- [x] dense tG9K mechanical PASS.
- [x] dense tG9K semantic PASS.
- [x] sparse t4jp persistence PASS.
- [x] sparse t4jp mechanical PASS.
- [x] sparse t4jp semantic non-regression PASS.
- [x] full v17→v20 stack merged to `main`.

#### P1.6 v20 promotion — ACTIVE GATE ON MAIN

Promotion is authorized for implementation/review, but **not yet completed**.

- [x] inspect public routing impact and record promotion design.
- [x] choose minimal architecture direction: keep historical v9 module semantics and introduce a neutral current-public facade instead of circular aliasing.
- [ ] implement current-public facade for mode-specific English v20/v5 and original v9/v4 routing.
- [ ] make targeted English analysis use v20/v5.
- [ ] preserve targeted original-language analysis on v9/v4.
- [ ] provide a public English batch surface compatible with Phase-1 partial-failure behavior.
- [ ] align `phase1_run.py` eligibility/current-artifact/Market routing to v20/v5.
- [ ] align browser analysis and Market/current-analysis routing to v20/v5.
- [ ] align Review Snapshot to English v20/v5 and original v9/v4 independently.
- [ ] align Capability v7 dependency selection to current English v20/v5.
- [ ] ensure free-form P1.6 rationale cannot override normalized source truth downstream.
- [ ] preserve old artifact/history/module reproducibility and avoid circular imports.
- [ ] add/update promotion regression tests.
- [ ] Ruff PASS.
- [ ] full pytest PASS.
- [ ] warnings-as-errors PASS.
- [ ] verify accepted v20 artifacts 36 and 37 remain current/reusable after promotion.
- [ ] update public contract docs only after implementation is proven.

### B3 — Capability Intelligence

**Accepted bounded baseline:** Capability v7 artifact 9 tied to P1.6 v9 artifact 29.

- [x] `job-capability-intelligence-v7` / schema v4 accepted for bounded tG9K.
- [x] complete deterministic source truth.
- [x] 25/25 capability-relevant requirements linked.
- [x] 7/7 responsibilities linked.
- [x] all 27 requirements retained in source truth.
- [x] all six explicit-depth facts retained.
- [x] two coherent capability profiles.
- [!] do not rebuild Capability against v20 until P1.6 promotion routing is complete.
- [ ] after promotion, rebuild/review Capability v7 against promoted P1.6 dependency.
- [ ] ensure model-generated P1.6 rationale does not override normalized source truth/strength/depth/evidence.

### B4 — Role Capability Blueprint experiment

**Status: [-] not accepted for Phase-1 use; further tuning deferred.**

- [x] deterministic provenance failure class fixed.
- [x] v6/12B artifact 7 passed mechanical audit and CI.
- [!] semantic review still found unsupported assumptions.
- [x] do not create Blueprint v7 or resume nearby model shopping during this gate.

### B5 — CI-3 heterogeneous live review

Permanent workflow:

```text
snapshot current local state first
→ run matching mechanical audit
→ inspect source/projection/P1.6 semantics
→ generate Capability only after P1.6 passes
→ inspect Capability semantics
→ regenerate only a stage proved missing/stale
```

Current targets:

- [x] rich AI/ML `tG9K` v20 bounded acceptance.
- [x] sparse `t4jp` v20 bounded non-regression.
- [ ] Python/software role — after P1.6 promotion + Capability dependency rebuild.
- [ ] network/security role — after P1.6 promotion + Capability dependency rebuild.
- [ ] operations/platform/DevOps role — after P1.6 promotion + Capability dependency rebuild.
- [ ] convert repeatable deterministic defects into fixtures.
- [ ] record model limitations separately from deterministic defects.
- [ ] decide whether promoted P1.6 + Capability v7 is good enough to freeze as Phase-2 input.

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