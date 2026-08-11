# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-08-11  
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

**Status: [x] accepted for the bounded rich `tG9K` gate on Capability artifact 9.**

Historical evidence:

- [x] v4/v2 artifact 7 reviewed and rejected.
- [x] v5 output-budget experiment recorded/reverted.
- [x] v6/v3 artifact 8 generated and rejected after semantic review.
- [x] v6 proved model-selected source linkage was too weak despite correct reconciliation of linked facts.

Accepted baseline:

```text
job-capability-intelligence-v7
schema job-capability-intelligence-v4
artifact 9 on tG9K
```

Acceptance evidence:

- [x] complete deterministic `source_truth`.
- [x] capability-vs-role-level P1.6 partition.
- [x] 25/25 capability-relevant requirements linked.
- [x] 7/7 responsibilities linked.
- [x] all 27 accepted requirements remain in source truth.
- [x] all six explicit depth facts remain in source truth.
- [x] five capability-level depth facts are represented in profiles.
- [x] the sixth depth fact, `three to six years`, remains correctly role-level on requirement 26.
- [x] two coherent capability profiles rather than one coverage-driven catch-all.
- [x] deterministic requirement strength/source depth/source work activities.
- [x] positive independence/ownership synthesis deferred.
- [x] cross-capability synthesis deferred.
- [x] repository audit passed.
- [x] complete semantic review found no B3-blocking source-truth or calibration failure.
- [x] CI on the committed artifact passed.

Decision record:

```text
docs/experiments/2026-08-11_CAPABILITY_V7_B3_ACCEPTANCE.md
```

Freeze v7 unless downstream/heterogeneous evidence reveals a repeatable correctness defect.

### B4 — Role Capability Blueprint calibration / SQ-3

**Status: [~] active. v3/v2 rejected; v4/v3 mechanically passed but semantically rejected; v5/v4 also semantically rejected; v6/v5 is the active candidate.**

Historical v3 evidence:

- [x] E2B and E4B both confused P1.6 requirement IDs with Capability-profile IDs.
- [x] v3 retained streaming/cloud/edge/MLOps architecture overreach.
- [x] v3/v2 declared failed; validators preserved; no prompt-patch/model-shopping workaround adopted.

Historical v4 evidence:

- [x] v4 removed model-owned numeric provenance.
- [x] live v4 `tG9K` generation completed with E4B.
- [x] `scripts/audit_blueprint_v4_snapshot.py` passed.
- [x] v4 deterministically preserved 2 Capability areas, 25 source requirements, 7 source responsibilities and 2 role constraints.
- [x] complete B4 semantic review rejected v4 because generated prose strengthened unstated operating/architecture/ownership assumptions.
- [x] root cause isolated: v4 consumed Capability-derived prose and still exposed broad free-text expansion surfaces.

Historical v5 evidence:

- [x] v5 excluded Capability-derived prose and duplicated long vacancy text from the model input.
- [x] v5 removed role shape, hidden requirements, tool recommendations, work-product lists, scenarios and bottom-line generation.
- [x] live `tG9K` v5 artifact 6 belonged to the exact current chain and was published as review evidence.
- [x] CI on the published v5 candidate passed.
- [!] B4 semantic review still rejected Area 2 because `practical_interpretation` asserted end-to-end infrastructure, telemetry streaming, automated MLOps workflows and deployment-lifecycle scope while its uncertainty admitted ownership boundaries were unknown.
- [x] conclusion: the remaining free-form positive summary surface itself is unsafe; do not patch its wording.

Active candidate:

```text
role-capability-blueprint-v6
schema role-capability-blueprint-v5
Blueprint model gemma-4-e4b-it-ud
```

V6 deterministic/model boundary:

- [x] keep v4/v5 deterministic source provenance and exact accepted Capability grouping.
- [x] model input excludes Capability-derived explanatory prose and duplicated long source text.
- [x] model-facing schema contains no upstream numeric provenance.
- [x] no free-form `practical_interpretation` or area-level role-summary field remains.
- [x] no model-generated role shape, likely depth, hidden requirements, tool suggestions, work-product lists, topology/scenarios, probably-not-required list, or bottom line.
- [x] positive model output exists only as `professional_considerations` with `plausible|speculative` strength plus mandatory uncertainty.
- [x] every Capability requires at least one `important_unknown`.
- [x] JobHunter deterministically attaches Capability identity/coverage plus exact P1.6 requirements/responsibilities, strength, depth, evidence, role purpose and role constraints.
- [x] generic validation rejects employer-obligation wording and full/end-to-end lifecycle/stack/pipeline/system/infrastructure scope.
- [x] prompt explicitly prevents high-volume→streaming, process-control→real-time, APC/SPC→feedback-loop, cloud/edge→placement, and deployment/governance→lifecycle-ownership shortcuts.
- [x] CLI/browser show source anchors separately from explicitly uncertain professional considerations.
- [x] dedicated `scripts/audit_blueprint_v6_snapshot.py` exists.
- [x] isolated v6 model/service/inference contract passed Ruff + full pytest + warnings-as-errors before activation.
- [x] v6 completion budget is capped at 4,096 tokens; LM Studio context remains auto-managed at 16,384.

Fixed live chain:

```text
English projection artifact 33
English P1.6 artifact 29
Capability v7 artifact 9
Blueprint model gemma-4-e4b-it-ud
```

- [ ] B4.1 Pull active v6/v5 runtime and confirm contract identity.
- [ ] B4.2 Run `jobhunter jobs blueprint tG9K` without rebuilding translation/P1.6/Capability.
- [ ] B4.3 If valid, regenerate `review-snapshots/jobs/tG9K.json`.
- [ ] B4.4 Run `python scripts/audit_blueprint_v6_snapshot.py`.
- [ ] B4.5 Verify exactly two areas, one-to-one with accepted Capability profiles 0/1 and exact labels.
- [ ] B4.6 Verify deterministic requirements/responsibilities exactly match Capability 9/P1.6 truth.
- [ ] B4.7 Verify Master's + 3–6 years constraints and source role purpose are exact.
- [ ] B4.8 Verify each positive professional consideration is useful and paired with a concrete uncertainty statement.
- [ ] B4.9 Verify every Capability exposes at least one real unresolved unknown and that unknown wording does not assume absent systems.
- [ ] B4.10 Reject source-unsupported streaming/real-time/low-latency/cloud-edge placement/automated feedback/full-lifecycle claims.
- [ ] B4.11 Verify contextual/preferred frameworks/cloud/edge/MATLAB/C/C++ remain calibrated and Python `expert` does not spread.
- [ ] B4.12 Verify technology lists do not become one asserted employer architecture.
- [ ] B4.13 Accept B4 only if the bounded professional considerations add material value beyond P1.6 + Capability without manufacturing certainty.
- [-] no multi-model voting/ensemble.

Records:

```text
docs/experiments/2026-08-11_BLUEPRINT_V3_GROUNDED_INTERPRETATION.md
docs/experiments/2026-08-11_BLUEPRINT_V4_DETERMINISTIC_PROVENANCE_BOUNDARY.md
docs/experiments/2026-08-11_BLUEPRINT_V4_SEMANTIC_FAILURE_AND_V5_BOUNDARY.md
docs/experiments/2026-08-11_BLUEPRINT_V5_SEMANTIC_FAILURE_AND_V6_BOUNDARY.md
```

### B5 — CI-3 heterogeneous live review

After B4:

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
