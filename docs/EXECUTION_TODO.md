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
- [x] targeted `jobhunter jobs analyze <id>` command for one explicit public P1.6 job without broad orchestration.

## B. Semantic-quality gate

Do not jump to corpus-wide Phase 2.

### B1 — Review Snapshot routing

- [x] `jobhunter jobs snapshot <id>` preserves effective model/dependency identities.
- [x] current-chain flags are trustworthy.
- [x] repository-safe exclusions remain intact.

### B2 — P1.6 factual extraction

**Public/accepted P1.6 remains v9/schema v4. Dense `tG9K` v9 artifact 29 remains authoritative. V17/schema v5 is an isolated candidate whose deterministic implementation passes CI; dense live semantic acceptance is now the active gate.**

#### Accepted dense v9 baseline — `tG9K`

- [x] 27 requirements / 7 responsibilities retained.
- [x] deterministic coverage accounting accepted.
- [x] optionality preserved.
- [x] statistics/signal-processing depth `Solid` preserved.
- [x] Python `expert` remains Python-specific.
- [x] MATLAB/C++ remain preferred.
- [x] contextual stack remains contextual.
- [x] industrial AI/ML experience `Strong` preserved.
- [x] process-control/manufacturing analytics `Hands-on` preserved.
- [x] high-dimensional sensor/time-series work `Comfort` preserved.
- [x] Master's degree and 3–6 years professional experience preserved.

#### Sparse calibration history — `t4jp`

- [!] public v9 artifact `30`: structured `skills[]` coverage hole + qualification-to-responsibility leakage.
- [!] v10 artifact `31`: structured skills fixed, but coarse description coverage lost explicit neighboring qualifications.
- [!] v11: qualification spans were outside the evidence-reference protocol.
- [!] v12: first-class qualification references worked, but coarse coverage remained model-owned bookkeeping.
- [!] v13 artifact `32`: deterministic decomposition worked, but residual requirement-bearing prose and concept normalization remained wrong.
- [!] v14 artifact `33`: complete sparse mechanical PASS, but trait ontology and residual-strength semantics were wrong.
- [!] v15 artifact `34`: mechanical PASS, but empty punctuation and ability→experience typing remained.
- [x] v16 artifact `35`: bounded sparse mechanical + semantic PASS.

#### Generic semantic boundaries through v16 and inherited by v17

- [x] deterministic coverage of non-empty structured `skills[]`.
- [x] exact qualification-list item evidence.
- [x] deterministic coarse-span decomposition bookkeeping.
- [x] complete residual sentence accounting.
- [x] qualification-vs-responsibility protection.
- [x] coverage obligation separated from employer requirement strength.
- [x] schedule wording prevented from becoming technical depth.
- [x] schedule wording removed from reusable capability concepts while exact evidence remains unchanged.
- [x] valid `Ability to ...` wrapper normalization with fail-closed logistics boundary.
- [x] normalized concepts cannot retain empty grouping punctuation debris.
- [x] explicit concept-type ontology for skill/tool/knowledge/practice/domain/experience/education/other.
- [x] `experience` requires prior-applied-exposure evidence rather than mere ability wording.
- [x] one bounded correction; candidate remains fail-closed after retry exhaustion.

#### Sparse v16 acceptance

- [x] `t4jp` artifact `35`: 8 requirements / 0 responsibilities / 0 role purpose.
- [x] structured required skills 3/3.
- [x] qualification items 4/4.
- [x] residual decisions 4/4.
- [x] visual-content evidence normalized to a clean `skill` with null depth and exact evidence preserved.
- [x] Ethics/work commitment preserved as `other`.
- [x] teachability, remote-application instruction, and location/benefits/travel excluded correctly.
- [x] no fabricated responsibility or role purpose.

#### Dense-safe audit preparation

- [x] sparse-only unconditional `decomposed_requirement` assumption removed from dense audit path.
- [x] decomposition required only when qualification/residual decomposition is active.
- [x] dense-safe audit regression coverage added.
- [x] CI run 706 passed Ruff, full pytest, and warnings-as-errors.

#### Dense v16 failure — root cause now classified

- [!] v16 dense `tG9K` failed before persistence after initial generation + one Instructor validation retry.
- [x] both failed generations produced exactly 32 requirements.
- [x] generation 1 retained education but omitted mandatory `field:minimum_experience`.
- [x] generation 2 restored minimum experience but omitted mandatory `field:education`.
- [x] all six top-level structured `skills[]` surfaces were represented.
- [x] code-level diagnosis confirmed an inherited fixed 32-requirement ceiling in typed model, JSON schema, and final validator.
- [x] accepted v9 dense facts (27 requirements) plus six newly protected structured-skill source surfaces can require at least 33 distinct requirement records.
- [x] no product/domain rule justifies a 32-requirement maximum.
- [x] failure classified as a representation-capacity contract defect rather than a last-message education/minimum-experience prompt defect.

Detailed failure record:

```text
docs/working-memory/2026-08-14_P16_V16_DENSE_REGRESSION_FAILURE_AND_STATE_RECONCILIATION.md
```

#### V17 source-led-capacity correction

Candidate contract:

```text
English P1.6: job-analysis-english-v17
schema:       job-analysis-v5
branch:       agent/p16-v17-source-led-capacity
draft PR:     #5
```

- [x] accepted/public v9/v4 path left unchanged.
- [x] candidate typed response removes the inherited 32-requirement cap.
- [x] candidate JSON schema removes `requirements.maxItems` without mutating accepted `_ANALYSIS_SCHEMA`.
- [x] candidate final validation supports item 33+ while preserving exact-evidence/depth/coverage validation.
- [x] global duplicate detection remains effective across the old 32-item boundary.
- [x] regression test proves v14 rejects 33 while v17 accepts 33 grounded unique requirements.
- [x] regression test proves duplicate after item 32 still fails.
- [x] regression test proves invented evidence after item 32 still fails.
- [x] v17 runtime preserves v15/v16 semantic normalization/validation stack.
- [x] v17 candidate runner added.
- [x] normal CI run 717 passed Ruff, full pytest, and warnings-as-errors.
- [x] temporary CI diagnostic modifications were reverted; standard CI workflow restored.

Implementation record:

```text
docs/working-memory/2026-08-14_P16_V17_SOURCE_LED_CAPACITY_IMPLEMENTATION.md
```

#### Current dense v17 live gate — `tG9K`

Run:

```bash
python scripts/run_p16_v17_candidate.py --job-id tG9K
```

- [~] run dense v17 locally against configured LM Studio/current database.
- [ ] confirm one candidate artifact persists rather than oscillating at the old 32-slot boundary.
- [ ] confirm Master's degree + `three to six years` minimum experience coexist.
- [ ] confirm all six structured `skills[]` surfaces remain represented.
- [ ] compare dense factual coverage against accepted v9 artifact 29; no silent fact loss merely to reduce count.
- [ ] verify responsibility coverage remains semantically correct.
- [ ] inspect explicit depth attachment: `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort`, `three to six years`.
- [ ] verify MATLAB/C++ remain preferred.
- [ ] verify contextual stack remains contextual where source wording requires it.
- [ ] review structured `Python` vs prose `Python (expert)` as distinct source surfaces; do not silently merge provenance/strength/depth.
- [ ] review concept-type differences only after a valid dense artifact exists.

Dense failed-output warnings from v16 remain review criteria, not accepted defects:

- [~] raw failed generations showed null `Solid`/`Strong`; final validated v17 artifact must be inspected.
- [~] structured `Python → required` can coexist with prose `Python (expert) → contextual + expert`; representation semantics remain source-surface-aware.

#### Sparse v17 non-regression — after dense artifact exists

Run:

```bash
python scripts/run_p16_v17_candidate.py --job-id t4jp
```

- [ ] compare with accepted sparse v16 artifact 35.
- [ ] ensure removing dense capacity ceiling does not increase unsupported sparse extraction.
- [ ] retain 3/3 structured skills, 4/4 qualification items, residual accounting, zero fabricated duties/purpose.

#### Current B2 decision boundary

- [x] public v9/schema v4 stays authoritative while v17 acceptance is incomplete.
- [x] sparse v16 acceptance remains valid.
- [x] v17 deterministic implementation/CI gate passed.
- [!] v17 public promotion blocked until dense semantic PASS + sparse non-regression PASS.
- [!] Capability v7 rebuild above v17 blocked until P1.6 promotion.
- [!] further heterogeneous-role progression remains gated on the dense/sparse v17 decision.

### B3 — Capability Intelligence

**Accepted for bounded `tG9K` only on Capability artifact 9 tied to accepted P1.6 v9 artifact 29.**

```text
job-capability-intelligence-v7
schema job-capability-intelligence-v4
artifact 9 on tG9K
analysis artifact 29
```

- [x] complete deterministic `source_truth`.
- [x] capability-vs-role-level P1.6 partition.
- [x] 25/25 capability-relevant requirements linked.
- [x] 7/7 responsibilities linked.
- [x] all 27 accepted requirements retained in source truth.
- [x] all six accepted explicit-depth facts retained in source truth.
- [x] two coherent profiles rather than one catch-all.
- [x] deterministic strength/depth/source-work reconciliation.
- [x] positive ownership/independence synthesis deferred.
- [x] cross-capability synthesis deferred.
- [x] repository audit + semantic review passed.

Freeze v7 unless heterogeneous evidence reveals a repeatable correctness defect. If v17 is eventually promoted, rebuild Capability v7 against that accepted analysis artifact rather than reusing artifact 9 as though it were current-chain.

### B4 — Role Capability Blueprint experiment

**Status: [-] not accepted for Phase-1 use; further Blueprint tuning deferred from the critical path.**

- [x] provenance/index failure class identified and mechanically fixed.
- [x] later contracts progressively reduced free-form authority.
- [x] v6/12B artifact 7 passed its mechanical audit and CI.
- [!] semantic review still found automated-feedback/platform/implementation assumptions not established by source.
- [x] conclusion: do not create Blueprint v7, weaken validators, or continue nearby model shopping during Phase 1.

### B5 — CI-3 heterogeneous live review — active gate

Validate:

```text
source
→ English projection
→ semantically accepted P1.6 for that job
→ Capability v7 only after P1.6 acceptance
```

Permanent workflow:

```text
snapshot current local state first
→ run matching mechanical audit
→ inspect source/projection/P1.6 semantics
→ generate Capability only after P1.6 passes
→ inspect Capability semantics
→ regenerate only a stage proved missing/stale
→ never rerun accepted upstream stages merely to create a fresh artifact
```

Current target state:

- [x] sparse/ambiguous anchor `t4jp` — P1.6 v16 bounded sparse acceptance.
- [x] rich AI/ML anchor `tG9K` — accepted v9/v7 baseline retained.
- [~] dense `tG9K` v17 candidate — deterministic implementation PASS; live semantic gate next.
- [ ] sparse `t4jp` v17 non-regression after dense v17 review.
- [ ] Python/software role — gated on v17 decision.
- [ ] network/security role — gated on v17 decision.
- [ ] operations/platform/DevOps role — gated on v17 decision.
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

Expose where applicable:

```text
requested
attempted
completed
reused
skipped intentionally
failed
remaining eligible
```

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
- [ ] record Blueprint as deferred/non-authoritative unless later evidence reopens it.

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
