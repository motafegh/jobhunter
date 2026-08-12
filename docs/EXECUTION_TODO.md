# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-08-12  
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

## B. Semantic-quality gate

Do not jump to corpus-wide Phase 2.

### B1 — Review Snapshot routing

- [x] `jobhunter jobs snapshot <id>` preserves effective model/dependency identities.
- [x] current-chain flags are trustworthy.
- [x] repository-safe exclusions remain intact.

### B2 — P1.6 factual extraction

**Accepted for dense `tG9K` on artifact 29.**

- [x] 27 requirements / 7 responsibilities retained.
- [x] deterministic coverage accounting.
- [x] optionality preserved.
- [x] Python `expert` remains Python-specific.
- [x] MATLAB/C++ remain preferred.
- [x] contextual stack remains contextual.
- [x] explicit depth and 3–6 years experience preserved.

### B3 — Capability Intelligence

**Accepted for bounded `tG9K` on Capability artifact 9.**

Current frozen baseline:

```text
job-capability-intelligence-v7
schema job-capability-intelligence-v4
artifact 9 on tG9K
```

- [x] complete deterministic `source_truth`.
- [x] capability-vs-role-level P1.6 partition.
- [x] 25/25 capability-relevant requirements linked.
- [x] 7/7 responsibilities linked.
- [x] all 27 accepted requirements remain in source truth.
- [x] all six explicit depth facts remain in source truth.
- [x] two coherent profiles rather than one catch-all.
- [x] deterministic strength/depth/source-work reconciliation.
- [x] positive ownership/independence synthesis deferred.
- [x] cross-capability synthesis deferred.
- [x] repository audit + semantic review passed.

Decision record:

```text
docs/experiments/2026-08-11_CAPABILITY_V7_B3_ACCEPTANCE.md
```

Freeze v7 unless heterogeneous evidence reveals a repeatable correctness defect.

### B4 — Role Capability Blueprint experiment

**Status: [-] not accepted for Phase-1 use; further Blueprint tuning deferred from the Phase-1 critical path.**

The bounded experiment has now tested v3→v6 across E2B, E4B and 12B local models.

Key evidence:

- [x] v3/v2 showed model-owned provenance/index bookkeeping was unsafe.
- [x] v4/v3 fixed deterministic provenance but broad generated prose still invented employer-specific operating/topology/ownership claims.
- [x] v5/v4 removed Capability-derived prose and most expansion surfaces, but free-form interpretation still inflated end-to-end/streaming/lifecycle scope.
- [x] v6/v5 removed free-form role-summary interpretation and limited generation to bounded professional considerations + unknowns.
- [!] v6/E4B still failed structured repair and introduced unstated assumptions.
- [x] controlled v6/12B comparison kept P1.6 29, Capability 9, v6/v5 and rubric fixed; only Blueprint model changed.
- [x] v6/12B artifact 7 passed `scripts/audit_blueprint_v6_snapshot.py` and CI.
- [!] complete semantic review still found unknowns/considerations that smuggled automated-feedback/platform/implementation assumptions not established by source.
- [x] conclusion: do not create Blueprint v7, do not weaken validators, and do not continue nearby model shopping during Phase 1.

Best bounded experimental artifact:

```text
Blueprint artifact 7
role-capability-blueprint-v6
schema role-capability-blueprint-v5
model gemma-4-12b-it-qat
review snapshot commit 671bd6e3c43555c631958531671a0f1be9726554
```

This artifact is **review evidence, not an accepted decision layer**.

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

Reopen Blueprint only when a materially different grounding/inference approach or a demonstrated user-value gap justifies it. Do not reopen merely for another prompt version or adjacent local model.

### B5 — CI-3 heterogeneous live review — active next gate

Validate the layers that have actually passed bounded acceptance:

```text
source
→ English projection
→ P1.6
→ Capability v7
```

Blueprint may be observed as non-gating research evidence only.

Target materially different roles:

- [ ] sparse/ambiguous anchor (`t4jp`);
- [x] rich AI/ML anchor (`tG9K`) as dense baseline;
- [ ] Python/software role;
- [ ] network/security role;
- [ ] operations/platform/DevOps role;
- [ ] verify factual coverage, obligation strength, depth, evidence and Capability grouping/source truth on each;
- [ ] convert repeatable deterministic defects into fixtures;
- [ ] record model limitations separately from deterministic defects;
- [ ] decide whether P1.6 + Capability v7 is good enough to freeze as Phase-2 input.

## C. Phase-1 closure after heterogeneous semantic acceptance

### C1 — Market truthfulness
- [ ] analyzed-current sample size visible;
- [ ] source/filter/contract scope recoverable;
- [ ] small-sample/concentration warnings;
- [ ] coverage metrics separate from semantic certification.

### C2 — Source/lifecycle
- [ ] network/429/5xx/challenge/auth failure != expired/removed;
- [ ] cautious 404/410/repeated-missing lifecycle handling;
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

- [ ] browser/CLI summaries agree;
- [ ] earlier durable success survives later failure;
- [ ] no-eligible-work != attempted-and-failed.

### C4 — P1.7 final workflow
- [ ] final per-job report/provenance;
- [ ] ready-job queue;
- [ ] combined current-corpus report;
- [ ] `jobhunter run` deterministic acceptance;
- [ ] browser equivalent acceptance;
- [ ] rerun/idempotency proof;
- [ ] bounded live end-to-end Phase-1 acceptance.

### C5 — Phase-1 closure
- [ ] acceptance summary with exact corpus/sample/contracts/bounds;
- [ ] reconcile final accepted docs;
- [ ] freeze accepted P1.6 + Capability starting contract for Phase 2;
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
