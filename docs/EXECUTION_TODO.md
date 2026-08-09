# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-08-09  
**Authority:** Subordinate to product/domain/source/architecture constraints, `docs/ROADMAP.md`, `docs/IMPLEMENTATION_PLAN.md`, and `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`  
**Current focused plan:** `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`

Status vocabulary:

```text
[ ] not started
[~] in progress / implemented but acceptance incomplete
[x] completed/accepted for the stated bounded scope
[!] blocking defect
[-] deliberately deferred
```

## A. Accepted foundation / reconciliation

- [x] Jobinja acquisition/provenance/source-version foundation.
- [x] `jobinja-detail-v2`.
- [x] `english-projection-v2` / `lm-studio-translation-v2`.
- [x] local browser + CLI shared services.
- [x] independent analysis/capability/blueprint model roles.
- [x] Review Snapshot v1 and effective-model routing.
- [x] current entry-point/handoff documentation exists.
- [x] normal deterministic CI gate is Ruff + full pytest + warnings-as-errors.

## B. Current semantic-quality gate

Do not jump to corpus-wide Phase 2.

### B1 — Review Snapshot routing

- [x] Integrated `jobhunter jobs snapshot <id>` passes all effective model roles.
- [x] Current-chain dependency flags are trustworthy.
- [x] Snapshot exclusions remain intact.

### B2 — P1.6 factual coverage / obligation / depth

**Accepted for `tG9K` on artifact 29.**

- [x] 27 requirements / 7 responsibilities retained.
- [x] deterministic coverage accounting.
- [x] explicit optionality preserved.
- [x] Python-specific `expert` depth preserved.
- [x] `MATLAB a plus` and `C/C++ helpful` remain optional/preferred.
- [x] contextual stack items are not individually upgraded to required.
- [x] education and 3–6 years experience participate.
- [x] no forced minimum claim count.

### B3 — Capability Intelligence calibration / SQ-2

**Status: [~] active. B3 is not accepted.**

Historical evidence:

- [x] v4/v2 artifact 7 reviewed and rejected.
- [x] v5 output-budget experiment recorded/reverted.
- [x] v6/v3 artifact 8 generated and reviewed.
- [x] v6 mechanical reconciliation proved useful.
- [x] v6 semantic result rejected because model-selected source links lost most P1.6 coverage and repeated ownership/autonomy/optionality failures.

Current candidate:

```text
job-capability-intelligence-v7
schema job-capability-intelligence-v4
```

Implementation:

- [x] complete deterministic `source_truth`.
- [x] capability-vs-role-level P1.6 partition.
- [x] hard coverage of all capability-relevant requirements.
- [x] hard coverage of all responsibilities.
- [x] dense-source multi-profile guard.
- [x] deterministic requirement strength.
- [x] deterministic source-explicit depth.
- [x] deterministic source-explicit work activities.
- [x] positive independence/ownership inference deferred.
- [x] cross-capability synthesis deferred.
- [x] v7 repository audit script.
- [x] deterministic regression coverage.
- [x] Ruff/full pytest/warnings-as-errors green on current v7 implementation.

Live acceptance still required:

- [ ] B3.1 Run v7 against fixed `tG9K` P1.6 artifact 29 with current E2B Capability model.
- [ ] B3.2 Regenerate `review-snapshots/jobs/tG9K.json`.
- [ ] B3.3 Run `python scripts/audit_capability_v7_snapshot.py`.
- [ ] B3.4 Verify 25/25 capability-relevant requirements linked and 7/7 responsibilities linked.
- [ ] B3.5 Verify `source_truth` retains all 27 requirements, all 7 responsibilities, and all explicit depth.
- [ ] B3.6 Verify >=2 coherent capability profiles rather than coverage-driven catch-all grouping.
- [ ] B3.7 Verify contextual/preferred tools are not promoted to mandatory/mastery in prose.
- [ ] B3.8 Verify cloud/edge does not become required deployment architecture.
- [ ] B3.9 Verify evidence relevance; exact evidence alone is insufficient if semantically unrelated.
- [ ] B3.10 Verify derived prerequisites are technically useful, not generic curriculum.
- [ ] B3.11 Verify no ownership/autonomy overreach survives elsewhere.
- [ ] B3.12 Accept B3 only if the complete artifact is materially more useful than P1.6 and correctly calibrated.

If the model cannot satisfy v7 coverage within the bounded call, diagnose the exact failure. Prefer bounded partitioning/output reduction or controlled model comparison over more prompt patching.

### B4 — Blueprint calibration / SQ-3 and model comparison if needed

Blocked until B3 passes.

- [ ] Preserve accepted upstream optionality/unknowns.
- [ ] technology list != architecture.
- [ ] `highly_likely` must not contradict unresolved unknowns.
- [ ] examples remain non-mandatory unless source requires them.
- [ ] review regenerated `tG9K` Blueprint.
- [ ] compare one stronger reasoning model only if evidence warrants it.
- [-] no multi-model voting/ensemble.

### B5 — CI-3 heterogeneous live review

After B3/B4:

- [ ] sparse/ambiguous anchor (`t4jp`);
- [ ] rich AI/ML anchor (`tG9K`);
- [ ] Python/software role;
- [ ] network/security role;
- [ ] operations/platform/DevOps role;
- [ ] review source → English → P1.6 → Capability → Blueprint;
- [ ] convert repeatable deterministic failures into fixtures;
- [ ] record model limitations separately from deterministic defects.

## C. Phase-1 closure after semantic acceptance

### C1 — Market truthfulness
- [ ] analyzed-current sample size visible;
- [ ] source/filter/contract scope recoverable;
- [ ] small-sample/concentration warnings;
- [ ] coverage metrics remain separate from semantic certification.

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
- [ ] freeze accepted P1.6 starting contract for Phase 2;
- [ ] record unresolved non-capabilities.

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
