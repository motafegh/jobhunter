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

- [x] `jobhunter jobs snapshot <id>` preserves effective model/dependency identities.
- [x] current-chain flags are trustworthy.
- [x] repository-safe exclusions remain intact.

### B2 — P1.6 factual extraction

**Public/accepted P1.6 remains v9/schema v4. Dense `tG9K` v9 artifact 29 remains authoritative. Active candidate is v20/schema-v5 on `agent/p16-v20-source-led-partitioning`. First v20 live run failed in partition 1; the narrow correction is implemented and dense rerun is the active gate.**

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
- [x] depth separate from obligation and normalized concept.
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

#### Dense correction history

V17:

- [x] removed arbitrary 32-requirement ceiling.
- [x] aggregate requirement + responsibility coverage defects in one correction message.

V18:

- [x] deterministic structured minimum-experience ownership when years are mechanically parseable.
- [x] deterministic structured education ownership.
- [x] structured skills made non-excludable coverage.

V19:

- [x] `a plus` / `helpful` kept as optionality rather than technical depth.
- [x] unsupported generated depth vocabulary removable only when exact source proves it was added.
- [x] genuine source depth such as `Python (expert)` remains preserved.
- [x] dense v19 live run exposed whole-answer retry oscillation: one generation retained segment-13 facts while omitting the long stack; retry repaired the long stack but dropped segment-13 facts.

Detailed history:

```text
docs/working-memory/2026-08-14_P16_V16_DENSE_REGRESSION_FAILURE_AND_STATE_RECONCILIATION.md
docs/working-memory/2026-08-14_P16_V17_SOURCE_LED_CAPACITY_IMPLEMENTATION.md
docs/working-memory/2026-08-14_P16_V17_DENSE_COVERAGE_FEEDBACK_CORRECTION.md
docs/working-memory/2026-08-14_P16_V18_DETERMINISTIC_STRUCTURED_REQUIREMENTS.md
docs/working-memory/2026-08-14_P16_V19_DEPTH_OPTIONALITY_CANONICALIZATION.md
```

#### V20 — source-led bounded semantic partitioning

Candidate:

```text
English P1.6: job-analysis-english-v20
schema shape: job-analysis-v5
branch: agent/p16-v20-source-led-partitioning
stacked draft PR: #8
base candidate: agent/p16-v19-depth-optionality-canonicalization / PR #7
```

- [x] complete model-owned coverage ledger built before inference.
- [x] maximum 8 model-owned requirement references per partition.
- [x] core/non-excludable/required/preferred/structured-skill coverage before contextual/excludable coverage.
- [x] responsibility coverage assigned only to first partition.
- [x] every partition keeps full exact evidence catalog for grounding.
- [x] partition output restricted to assigned requirement/duty/exclusion ledger.
- [x] cross-partition leakage fails closed.
- [x] independently validated partitions merge by exact identity.
- [x] deterministic education/experience materialization occurs after merge.
- [x] inherited whole-artifact validators remain active after merge.
- [x] exact v19 oscillation shape preserved across merge in regression tests.
- [x] base implementation CI run 747 passed all gates.

Record:

```text
docs/working-memory/2026-08-14_P16_V20_SOURCE_LED_PARTITIONING.md
```

#### First dense v20 live run — partition-1 vague extent defect

- [!] no v20 artifact persisted.
- [x] source-led partitioning reached bounded partition 1.
- [x] both generations preserved MATLAB as preferred with null depth.
- [!] both generations emitted C/C++ as preferred with `depth_signal="some"` from exact evidence `some C / C++ helpful`.
- [x] shared strict depth validator correctly rejected `some` because it is not an accepted explicit technical-depth / experience-extent signal.
- [x] failure classified as a narrow inherited item-normalization gap, not a partitioning failure and not a reason to increase retries.
- [~] same live output moved the high-level segment-0 statement into responsibilities with `role_purpose=[]`; prompt now reinforces semantic purpose-vs-duty separation, but this remains a live semantic review item rather than a hardcoded rewrite.

#### V20 first-live correction

- [x] partition calls now use `AnalysisRequirementV20` / `JobAnalysisResponseV20`.
- [x] `depth_signal="some"` is cleared only when the requirement is preferred, exact evidence contains `some`, exact evidence independently proves optionality, and exact evidence contains no accepted explicit depth/experience-extent marker.
- [x] exact evidence stays unchanged; the word `some` remains reviewable in provenance.
- [x] real preferred depth such as `Strong C / C++ preferred` remains `depth_signal=Strong`.
- [x] `some C / C++` without preference is not silently repaired and remains fail-closed.
- [x] v20 prompt now explicitly distinguishes high-level role purpose from concrete responsibilities.
- [x] regression tests cover the exact live C/C++ shape, real preferred depth preservation, non-preferred fail-closed behavior, and prompt semantics.
- [x] correction implementation CI run 753 passed Ruff, full pytest, and warnings-as-errors.

Record:

```text
docs/working-memory/2026-08-14_P16_V20_FIRST_LIVE_PARTITION_CORRECTION.md
```

#### Current dense v20 live gate — `tG9K` rerun

```bash
cd ~/projects/jobhunter

git fetch origin
git switch agent/p16-v20-source-led-partitioning
git pull --ff-only origin agent/p16-v20-source-led-partitioning

python scripts/run_p16_v20_candidate.py --job-id tG9K
```

- [~] rerun dense v20 locally against configured LM Studio/current database.
- [ ] confirm one v20 artifact persists.
- [ ] confirm required `Master's degree`.
- [ ] confirm `Professional experience` + exact `three to six years` depth.
- [ ] confirm all six structured `skills[]` surfaces.
- [ ] confirm high-level role purpose is represented appropriately and concrete duty surfaces remain responsibilities.
- [ ] compare dense factual coverage against accepted v9 artifact 29; no silent fact loss.
- [ ] inspect `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort` depth attachment.
- [ ] verify MATLAB/C++ preferred with null technical depth unless independently supported.
- [ ] verify contextual stack remains contextual.
- [ ] verify semiconductor-domain concept has no unsupported expertise wording.
- [ ] preserve provenance distinction between structured Python and prose `Python (expert)`.
- [ ] review concept-type differences only after mechanical validity.

Do not run sparse `t4jp` until dense v20 mechanical + semantic PASS.

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
- [x] v17 capacity + aggregate-feedback deterministic gates passed.
- [x] v18 deterministic structured ownership gate passed.
- [x] v19 depth/optionality canonicalization gate passed.
- [x] v20 partition implementation gate passed.
- [x] v20 first-live vague-extent correction deterministic gate passed.
- [!] v20 public promotion blocked until dense semantic PASS + sparse non-regression PASS.
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

Freeze v7 unless heterogeneous evidence reveals a repeatable correctness defect. After eventual P1.6 promotion, rebuild Capability v7 against the promoted analysis artifact rather than reusing artifact 9 as though it were current-chain.

### B4 — Role Capability Blueprint experiment

**Status: [-] not accepted for Phase-1 use; further Blueprint tuning deferred.**

- [x] provenance/index failure class identified and mechanically fixed.
- [x] v6/12B artifact 7 passed mechanical audit and CI.
- [!] semantic review still found unsupported automated-feedback/platform/implementation assumptions.
- [x] do not create Blueprint v7, weaken validators, or resume nearby model shopping during this gate.

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
- [~] dense `tG9K` v20 — corrected live rerun next.
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
