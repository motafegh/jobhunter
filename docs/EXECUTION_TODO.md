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

### B3 — Capability Intelligence — ACTIVE DESIGN GATE / IMPLEMENTATION PAUSED

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
- [x] stop iterative mutation of public/historical v7 for this dense case.

#### Capability v8 source-led candidate — MECHANICAL PASS / SEMANTIC REJECT

Architecture proof:

```text
accepted P1.6 source truth
→ compact semantic group plan
→ bounded exact source-fact assignment
→ bounded per-group reasoning
→ deterministic source-link injection
→ strict reconciliation/source truth
```

- [x] group semantics separated from source-index bookkeeping.
- [x] bounded assignment and exact owned-source coverage enforced.
- [x] per-group reasoning receives only assigned facts + matching evidence.
- [x] JobHunter owns final source links, source strength, explicit depth and source work activities.
- [x] P1.6 rationale excluded from model-facing payloads.
- [x] CI 821: Ruff PASS / full pytest PASS / warnings-as-errors PASS.
- [x] dense `tG9K` completed against P1.6 artifact 36.
- [x] 31/31 capability requirements linked.
- [x] 8/8 responsibilities linked.
- [x] four profiles generated.
- [x] role-level requirement indices remained `[31, 32]`.
- [x] source-led architecture solved v7 dense linkage/coverage failure mechanically.
- [!] unsupported depth inflation appeared in model-owned prose.
- [!] unsupported ownership/lifecycle scope appeared in model-owned prose.
- [!] contextual/preferred facts were promoted into stronger prerequisite/required interpretations.
- [!] preferred C/C++ was treated as a technical foundation.
- [!] preferred industrial/edge deployment was escalated beyond source optionality.
- [!] v8 is NOT semantically accepted and MUST NOT be publicly promoted.
- [x] persisted v8 candidate remains historical evidence; do not overwrite/delete it.

Depth accounting:

- [x] five capability-relevant explicit depth facts are linked: 5/5.
- [x] one additional explicit depth is role-level 3–6 years professional experience.
- [x] all six explicit depth facts remain in source truth.

#### Capability v9 guarded source-led candidate — TWO LIVE FAILURES / NO ARTIFACT

Contract:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

Implemented boundaries:

- [x] ordinary model-owned prose cannot restate source obligation.
- [x] ordinary model-owned prose cannot add unsupported technical depth.
- [x] ordinary model-owned prose cannot infer unsupported ownership/lifecycle/autonomy/architecture.
- [x] preferred/contextual-only facts cannot independently justify model-inferred prerequisites.
- [x] source truth separates capability explicit depth from role-level explicit depth.
- [x] v9 uses a distinct persistence identity from v8.
- [x] CI 832 passed initial v9 deterministic gate.

Live failure 1:

- [!] generation 1 summary added unsupported `expertise` and hard-failed as intended.
- [!] generation 2 optional derived depth statements used `necessary`, `prerequisite`, `must`, and `necessitates`.
- [x] no v9 artifact persisted.
- [x] per-expectation fail-closed filtering correction implemented.
- [x] CI 838 passed Ruff / full pytest / warnings-as-errors for that correction.

Live failure 2:

- [!] both generations returned a bounded MLOps/production profile with summary + no derived reasoning.
- [!] inherited v8 validator rejected both with `Capability profile reasoning must add derived reasoning or an explicit unknown boundary`.
- [x] no v9 artifact persisted.
- [!] this exposes a design contradiction: v9 aims not to force speculative enrichment, while inherited v8 still requires every profile to add derived reasoning or unknown scope.
- [!] previous documentation claiming a v9 profile could survive with no safe derived expectations was an intended property but not an effective runtime property; documentation has been corrected explicitly.
- [~] Capability semantic contract requires design discussion before any further implementation.

#### Explicit pause

Per user instruction:

- [-] do not patch v9 again yet.
- [-] do not create v10.
- [-] do not rerun dense Capability generation.
- [-] do not run sparse `t4jp` Capability validation.
- [-] do not change public Capability routing.
- [~] discuss what Capability should add beyond accepted P1.6 source truth.
- [~] decide whether a profile may validly contain only neutral grouping + deterministic source facts.
- [~] decide whether derived reasoning is mandatory, optional, or should become explicit unknown when absent.
- [~] decide whether model-owned `depth_signals` are valuable now that source-explicit depth is deterministic.
- [~] decide which Capability outputs are authoritative source-derived facts vs optional model enrichment.

**Current exact next action:** design discussion only. There is intentionally no shell command to run.

Detailed current record:

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_LIVE_FAILURES_AND_DESIGN_PAUSE.md
```

Supporting records:

```text
docs/working-memory/2026-08-15_CAPABILITY_V7_PROMOTED_P16_LINKAGE_FAILURE.md
docs/working-memory/2026-08-15_CAPABILITY_V8_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-15_CAPABILITY_V8_LIVE_REVIEW_AND_V9_BOUNDARY.md
docs/working-memory/2026-08-15_CAPABILITY_V9_DERIVED_EXPECTATION_FILTERING.md
```

### B4 — Role Capability Blueprint experiment

**Status: [-] not accepted for Phase-1 use; tuning deferred.**

- [x] deterministic provenance failure class fixed historically.
- [x] historical v6/12B artifact 7 passed mechanical audit and CI.
- [!] semantic review still found unsupported assumptions.
- [x] do not resume Blueprint tuning during the Capability gate.

### B5 — Heterogeneous live review

Blocked until Capability design/acceptance resumes.

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
