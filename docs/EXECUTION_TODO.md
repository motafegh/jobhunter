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

**Public/accepted P1.6 remains v9. Dense `tG9K` v9 artifact 29 is still the accepted baseline. v16 is accepted only for bounded sparse `t4jp`; dense v16 regression is currently blocked.**

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
- [!] v11: failed before persistence because qualification spans were outside the evidence-reference protocol.
- [!] v12: first-class qualification references worked, but coarse coverage still remained model-owned bookkeeping.
- [!] v13 artifact `32`: deterministic decomposition worked, but whole-span suppression hid Ethics/work commitment and one capability concept retained Ability-to/schedule wording.
- [!] v14 artifact `33`: complete mechanical sparse PASS, but behavioral/value expectation typed as skill and residual coverage mechanically forced `required`.
- [!] v15 artifact `34`: mechanical PASS, but visual-content normalization retained empty punctuation and ability evidence was mis-typed as prior experience.
- [x] v16 artifact `35`: **bounded sparse mechanical + semantic PASS**.

#### Generic candidate boundaries now implemented through v16

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

Sparse decision record:

```text
docs/working-memory/2026-08-14_P16_V16_SPARSE_ACCEPTANCE.md
```

#### Dense-safe audit preparation

- [x] remove sparse-only unconditional `decomposed_requirement` requirement from dense audit path.
- [x] require decomposition only when qualification/residual decomposition is actually active.
- [x] dense-safe audit regression coverage added.
- [x] CI run 706 passed Ruff, full pytest, and warnings-as-errors.

#### First dense v16 regression — `tG9K`

- [!] first v16 dense run failed before persistence after initial generation + one bounded retry.
- [x] both failed generations retained 1 role purpose and 7 responsibilities.
- [!] generation 1 omitted mandatory `field:minimum_experience` while retaining education.
- [!] generation 2 repaired `minimum_experience` (`three to six years`) but omitted mandatory `field:education`.
- [!] retry budget exhausted; no dense v16 artifact persisted.
- [~] classify the dense failure before any correction.

Confirmed current blocker:

```text
mandatory education + minimum_experience are individually representable,
but current dense generation/correction did not retain both simultaneously
in one JobHunter-valid response
```

Dense warning signals from failed/non-persisted output:

- [~] `Solid` statistics/signal-processing depth was lost (`null`) in both failed generations.
- [~] `Strong` industrial AI/ML experience depth was lost (`null`) in both failed generations.
- [x] `expert`, `Hands-on`, and `Comfort` survived both failed generations.
- [x] generation 2 preserved `three to six years` after correction.
- [~] all six structured `skills[]` were added as required requirements, materially expanding the dense requirement shape relative to v9.
- [~] same-concept overlap is now explicit: structured `Python → required` coexists with prose `Python (expert) → contextual`.
- [~] decide how same-concept multi-surface provenance/strength/depth should be represented without silent collapse or misleading duplication.
- [~] concept-type differences versus v9 must be reviewed deliberately if/when a dense v16 artifact persists; do not assume every ontology difference is a regression.

Detailed current resume record:

```text
docs/working-memory/2026-08-14_P16_V16_DENSE_REGRESSION_FAILURE_AND_STATE_RECONCILIATION.md
```

#### Current B2 decision boundary

- [x] public v9 stays authoritative while dense v16 is unresolved.
- [x] sparse v16 acceptance remains valid and is not invalidated by dense failure.
- [!] v16 public promotion blocked.
- [!] Capability v7 rebuild above v16 blocked.
- [!] do not advance to further heterogeneous roles until the dense P1.6 diagnosis/decision.
- [~] next action is **discussion/diagnosis**, not implementation.

Do not react only to the final `field:education` validator message. Diagnosis must consider together:

```text
mandatory structured-field coverage / correction behavior
explicit depth retention (Solid, Strong)
structured-skill + prose overlap
same-concept optionality/depth provenance
ontology differences
proper ownership of any eventual correction
```

### B3 — Capability Intelligence

**Accepted for bounded `tG9K` only on Capability artifact 9 tied to accepted P1.6 v9 artifact 29.**

Current frozen baseline:

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
- [x] all 27 accepted requirements remain in source truth.
- [x] all six accepted explicit depth facts remain in source truth.
- [x] two coherent profiles rather than one catch-all.
- [x] deterministic strength/depth/source-work reconciliation.
- [x] positive ownership/independence synthesis deferred.
- [x] cross-capability synthesis deferred.
- [x] repository audit + semantic review passed.

Decision record:

```text
docs/experiments/2026-08-11_CAPABILITY_V7_B3_ACCEPTANCE.md
```

Freeze v7 unless heterogeneous evidence reveals a repeatable correctness defect. If a new P1.6 identity is eventually promoted, rebuild Capability v7 against that accepted analysis artifact rather than reusing artifact 9 as though it were current-chain.

### B4 — Role Capability Blueprint experiment

**Status: [-] not accepted for Phase-1 use; further Blueprint tuning deferred from the Phase-1 critical path.**

- [x] provenance/index failure class identified and mechanically fixed.
- [x] later contracts progressively reduced free-form authority.
- [x] v6/12B artifact 7 passed its mechanical audit and CI.
- [!] semantic review still found automated-feedback/platform/implementation assumptions not established by source.
- [x] conclusion: do not create Blueprint v7, weaken validators, or continue nearby model shopping during Phase 1.

Best bounded experimental artifact:

```text
Blueprint artifact 7
role-capability-blueprint-v6
schema role-capability-blueprint-v5
model gemma-4-12b-it-qat
```

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

### B5 — CI-3 heterogeneous live review — active gate

Validate:

```text
source
→ English projection
→ semantically accepted P1.6 for that job
→ Capability v7 only after P1.6 acceptance
```

Blueprint remains non-gating research evidence only.

Permanent CI-3 workflow rule:

```text
snapshot current local state first
→ run the matching mechanical audit
→ inspect source/projection/P1.6 semantics
→ generate Capability only after P1.6 passes
→ inspect Capability semantics
→ regenerate only a stage proved missing/stale
→ never rerun accepted upstream stages merely to create a fresh artifact
```

Current target state:

- [x] sparse/ambiguous anchor `t4jp` — P1.6 v16 bounded sparse acceptance.
- [x] rich AI/ML anchor `tG9K` — accepted v9/v7 baseline retained.
- [!] dense `tG9K` v16 regression — failed before persistence; diagnosis active.
- [ ] Python/software role — gated on dense P1.6 decision.
- [ ] network/security role — gated on dense P1.6 decision.
- [ ] operations/platform/DevOps role — gated on dense P1.6 decision.
- [ ] verify factual coverage, optionality, depth, evidence, and Capability grouping/source truth on each after P1.6 candidate acceptance.
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
