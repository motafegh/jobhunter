# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-08-14  
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

**Public/accepted P1.6 remains v9/schema v4. Dense `tG9K` v9 artifact 29 remains authoritative. Active candidate is v20/schema-v5 on `agent/p16-v20-source-led-partitioning`. Dense v20 artifact 36 has now persisted with 33 requirements / 8 responsibilities. Active gate is artifact 36 mechanical snapshot audit + semantic review. Do not run sparse `t4jp` yet.**

#### Accepted baselines

Dense `tG9K` v9 artifact 29:

- [x] 27 requirements / 7 responsibilities.
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

#### Dense correction chain

V17:

- [x] removed arbitrary 32-requirement ceiling.
- [x] aggregate requirement/responsibility coverage defects into one bounded correction.

V18:

- [x] deterministic parseable structured minimum experience.
- [x] deterministic structured education.
- [x] structured skills non-excludable.

V19:

- [x] optionality separated from technical depth.
- [x] unsupported generated depth vocabulary guarded.
- [x] genuine source depth preserved.
- [x] dense whole-answer retry oscillation identified.

V20:

- [x] source-led bounded requirement partitions (max 8 model-owned refs).
- [x] exact partition-scope enforcement.
- [x] independent partition merge by exact identity.
- [x] deterministic structured facts materialized after merge.
- [x] inherited whole-artifact validators retained.
- [x] `some C / C++ helpful` corrected to preferred + null depth in the proven case.
- [x] `industrial / edge deployment` scope kept in concept rather than technical depth.
- [x] unsupported preferred `experience` remains fail-closed without prior-exposure evidence.
- [x] role-purpose versus concrete-duty distinction remains semantic/model-owned.

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
```

#### Dense v20 artifact 36 — current gate

Persisted local result:

```text
Artifact: 36
Contract: job-analysis-english-v20 / job-analysis-v5
Requirements: 33
Responsibilities: 8
```

- [x] one dense v20 artifact persisted.
- [x] complete v20 generation/partition/merge/validation/persistence path passed.
- [x] v20-specific snapshot exporter implemented.
- [x] v20-specific mechanical snapshot auditor implemented.
- [x] review-tool regression binds audit to v20 prompt/schema identity.
- [x] review-tool CI passed Ruff + full pytest + warnings-as-errors.
- [~] export artifact 36 review snapshot.
- [ ] run v20 mechanical snapshot audit.
- [ ] inspect required `Master's degree`.
- [ ] inspect `Professional experience` + exact `three to six years` depth.
- [ ] inspect all six structured `skills[]` surfaces.
- [ ] inspect high-level role purpose versus concrete responsibilities.
- [ ] explain/accept/reject 8 responsibilities versus accepted v9 baseline 7.
- [ ] compare dense factual coverage against accepted v9 artifact 29 and source/projection; no silent fact loss.
- [ ] inspect `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort` depth attachment.
- [ ] verify MATLAB/C++ preferred with null technical depth unless independently supported.
- [ ] verify `industrial / edge deployment` retains scope without fabricated depth or experience.
- [ ] verify contextual stack remains contextual.
- [ ] verify semiconductor-domain concept has no unsupported expertise wording.
- [ ] preserve provenance distinction between structured Python and prose `Python (expert)`.
- [ ] review concept-type differences for semantic defensibility.

Local review commands:

```bash
cd ~/projects/jobhunter

git pull --ff-only origin agent/p16-v20-source-led-partitioning

python scripts/export_p16_v20_candidate_snapshot.py --job-id tG9K
python scripts/audit_p16_v20_candidate_snapshot.py --job-id tG9K
```

Review file:

```text
review-snapshots/jobs/tG9K.json
```

Do **not** run sparse `t4jp` until artifact 36 mechanical + semantic PASS.

#### Sparse v20 non-regression — only after dense PASS

```bash
python scripts/run_p16_v20_candidate.py --job-id t4jp
```

- [ ] compare with accepted sparse v16 artifact 35.
- [ ] ensure partitioning/deterministic ownership does not create sparse over-extraction.
- [ ] retain structured skills, qualification/residual accounting, and zero fabricated duties/purpose.

#### Current B2 decision boundary

- [x] public v9/schema v4 stays authoritative.
- [x] sparse v16 acceptance remains valid.
- [x] v17-v20 deterministic correction gates passed.
- [x] dense v20 artifact 36 mechanically persisted.
- [!] v20 public promotion blocked until artifact 36 semantic PASS + sparse non-regression PASS.
- [!] Capability v7 rebuild above v20 blocked until P1.6 promotion.
- [!] heterogeneous-role progression blocked until dense/sparse v20 decision.

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

- [x] sparse `t4jp` — v16 bounded acceptance.
- [x] rich AI/ML `tG9K` — accepted v9/v7 baseline retained.
- [~] dense `tG9K` v20 artifact 36 — mechanical + semantic review now.
- [ ] sparse `t4jp` v20 non-regression after dense PASS.
- [ ] Python/software role — gated on v20 decision.
- [ ] network/security role — gated on v20 decision.
- [ ] operations/platform/DevOps role — gated on v20 decision.
- [ ] convert repeatable deterministic defects into fixtures.
- [ ] record model limitations separately from deterministic defects.
- [ ] decide whether P1.6 + Capability v7 is good enough to freeze as Phase-2 input.

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
