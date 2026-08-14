# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-08-15  
**Authority:** Subordinate to product/domain/source/architecture constraints, `docs/ROADMAP.md`, `docs/IMPLEMENTATION_PLAN.md`, and `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`  
**Current focused plan:** `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`

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
- [x] targeted `jobhunter jobs analyze <id>` command for one explicit public P1.6 job.

## B. Semantic-quality gate

Do not jump to corpus-wide Phase 2.

### B1 — Review Snapshot routing

- [x] current-chain snapshot routing preserves model/dependency identities.
- [x] current-chain flags are trustworthy.
- [x] repository-safe exclusions remain intact.

### B2 — P1.6 factual extraction

**Public/accepted P1.6 remains v9/schema v4. Dense `tG9K` v20 artifact 36 passed persistence, mechanical audit, and semantic review. Active candidate remains v20/schema-v5 on `agent/p16-v20-source-led-partitioning`. The active gate is now sparse `t4jp` v20 non-regression.**

#### Accepted baselines

Dense `tG9K` v9 artifact 29:

- [x] 27 requirements / 7 responsibilities / 1 role purpose.
- [x] optionality preserved.
- [x] `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort` preserved.
- [x] MATLAB/C++ preferred.
- [x] contextual stack contextual.
- [x] Master's degree and 3–6 years professional experience retained.

Sparse `t4jp` v16 artifact 35:

- [x] 8 requirements / 0 responsibilities / 0 role purpose.
- [x] structured required skills 3/3.
- [x] qualification items 4/4.
- [x] residual decisions 4/4.
- [x] no fabricated duty/purpose.

#### Permanent semantic boundaries

- [x] exact source evidence/provenance.
- [x] no unsupported/invented career claims.
- [x] required/preferred/contextual strength kept distinct.
- [x] depth separate from obligation and normalized concept/scope.
- [x] structured `skills[]` cannot silently disappear.
- [x] exact qualification-list item evidence.
- [x] deterministic coarse-span decomposition bookkeeping.
- [x] complete residual sentence accounting.
- [x] qualification-vs-responsibility protection.
- [x] schedule wording cannot become capability depth.
- [x] clean reusable concepts.
- [x] ontology: skill/tool/knowledge/practice/domain/experience/education/other.
- [x] `experience` requires prior-applied-exposure evidence.
- [x] fail closed before persistence when the complete contract is not satisfied.

#### V17 → V20 correction chain

- [x] v17 removed arbitrary 32-requirement ceiling.
- [x] v17 aggregated dense coverage defects for bounded retry feedback.
- [x] v18 deterministically owns parseable structured minimum experience and education.
- [x] v18 makes structured skills non-excludable.
- [x] v19 separates optionality from technical depth and protects genuine source depth.
- [x] v19 dense run identified whole-answer retry oscillation.
- [x] v20 uses bounded source-led partitions (max 8 model-owned refs).
- [x] v20 enforces partition scope and merges independently-valid partitions.
- [x] v20 preserves `some C / C++ helpful` as preferred + null depth.
- [x] v20 preserves `industrial / edge deployment` as scope, not technical depth.
- [x] v20 refuses unsupported preferred `experience` without prior-exposure evidence.

Detailed records:

```text
docs/working-memory/2026-08-14_P16_V16_DENSE_REGRESSION_FAILURE_AND_STATE_RECONCILIATION.md
docs/working-memory/2026-08-14_P16_V17_SOURCE_LED_CAPACITY_IMPLEMENTATION.md
docs/working-memory/2026-08-14_P16_V17_DENSE_COVERAGE_FEEDBACK_CORRECTION.md
docs/working-memory/2026-08-14_P16_V18_DETERMINISTIC_STRUCTURED_REQUIREMENTS.md
docs/working-memory/2026-08-14_P16_V19_DEPTH_OPTIONALITY_CANONICALIZATION.md
docs/working-memory/2026-08-14_P16_V20_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-14_P16_V20_FIRST_LIVE_PARTITION_CORRECTION.md
docs/working-memory/2026-08-14_P16_V20_SECOND_LIVE_SCOPE_DEPTH_CORRECTION.md
docs/working-memory/2026-08-14_P16_V20_DENSE_ARTIFACT_36_PERSISTED.md
docs/working-memory/2026-08-15_P16_V20_DENSE_ARTIFACT_36_MECHANICAL_AUDIT_PASS.md
docs/working-memory/2026-08-15_P16_V20_DENSE_ARTIFACT_36_SEMANTIC_ACCEPTANCE.md
```

#### Dense v20 artifact 36 — bounded PASS

```text
Artifact:          36
Contract:          job-analysis-english-v20 / job-analysis-v5
Requirements:      33
Responsibilities:  8
Role purpose:      0
Mechanical audit:  PASS
Semantic review:   PASS WITH ACCEPTABLE DIFFERENCE
```

- [x] dense v20 artifact persisted.
- [x] complete generation/partition/merge/validation/persistence path passed.
- [x] v20-specific snapshot export/audit passed.
- [x] required `Master's degree` retained.
- [x] `Professional experience` retains exact `three to six years` depth.
- [x] all six structured skills retained.
- [x] all 27 accepted dense v9 source-derived requirements retained; 33 total = 27 + 6 structured skills.
- [x] no silent dense factual loss.
- [x] `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort` retained correctly.
- [x] MATLAB/C++ preferred with null technical depth.
- [x] `industrial / edge deployment` remains preferred scope with null depth and no fabricated experience.
- [x] contextual technical stack remains contextual.
- [x] semiconductor-domain concept contains no unsupported expertise wording.
- [x] structured Python and prose `Python (expert)` remain provenance-distinct.
- [x] concept-type differences are semantically defensible.
- [x] 8-vs-7 responsibility difference explained: v20 treats the opening `Build and validate ML/AI models...` bullet as a concrete responsibility; v9 used it as role purpose. Exact meaning remains represented, so this is accepted rather than blocking.

#### Sparse v20 non-regression — ACTIVE GATE

Run only:

```bash
cd ~/projects/jobhunter

git pull --ff-only origin agent/p16-v20-source-led-partitioning
python scripts/run_p16_v20_candidate.py --job-id t4jp
```

Acceptance target against sparse v16 artifact 35:

- [~] run sparse v20 locally against configured LM Studio/current database.
- [ ] one sparse v20 artifact persists.
- [ ] 3/3 structured required skills represented.
- [ ] 4/4 qualification items represented.
- [ ] complete residual coverage decisions.
- [ ] 0 responsibilities.
- [ ] 0 role purpose.
- [ ] no fabricated duty/purpose.
- [ ] no deterministic over-extraction.
- [ ] export/audit/review sparse v20 artifact after persistence.

#### Current B2 decision boundary

- [x] public v9/schema v4 stays authoritative until promotion.
- [x] sparse v16 acceptance remains valid baseline.
- [x] v17-v20 deterministic correction gates passed.
- [x] dense v20 artifact 36 persistence PASS.
- [x] dense v20 artifact 36 mechanical audit PASS.
- [x] dense v20 artifact 36 semantic PASS with acceptable classification difference.
- [!] v20 public promotion blocked until sparse v20 non-regression PASS.
- [!] Capability v7 rebuild above v20 blocked until P1.6 promotion.
- [!] heterogeneous-role progression blocked until sparse v20 decision.
- [!] candidate PR merge blocked until sparse v20 decision and promotion decision.

### B3 — Capability Intelligence

**Accepted only for bounded `tG9K` on Capability artifact 9 tied to accepted P1.6 v9 artifact 29.**

- [x] `job-capability-intelligence-v7` / schema v4 accepted for bounded tG9K.
- [x] complete deterministic source truth.
- [x] 25/25 capability-relevant requirements linked.
- [x] 7/7 responsibilities linked.
- [x] all 27 accepted requirements retained in source truth.
- [x] all six accepted explicit-depth facts retained.
- [x] two coherent capability profiles.

Freeze v7 until a promoted P1.6 artifact exists. Then rebuild Capability v7 against the promoted P1.6 dependency rather than treating artifact 9 as current-chain.

### B4 — Role Capability Blueprint experiment

**Status: [-] not accepted for Phase-1 use; further Blueprint tuning deferred.**

- [x] provenance/index failure class identified and mechanically fixed.
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

- [x] rich AI/ML `tG9K` v20 dense bounded acceptance.
- [~] sparse `t4jp` v20 non-regression.
- [ ] Python/software role — gated on sparse v20 decision/promotion.
- [ ] network/security role — gated on sparse v20 decision/promotion.
- [ ] operations/platform/DevOps role — gated on sparse v20 decision/promotion.
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
