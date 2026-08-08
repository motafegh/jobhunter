# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-08-08  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`, `docs/ROADMAP.md`, and product/domain/source/architecture constraints  
**Current focused plan:** `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`

This file is the **current operational checklist**, not a historical backlog. Older completed/obsolete checklist items were removed during the 2026-08-08 reconciliation so the next conversation does not restart already-completed work.

Status vocabulary:

```text
[ ] not started
[~] in progress / implemented but acceptance incomplete
[x] completed/accepted for the stated bounded scope
[!] blocking defect before dependent work
[-] deliberately deferred
```

---

# A. Repository/state reconciliation

## A1 — Documentation and handoff

- [x] A1.1 Reconcile the active semantic-analysis documentation with `job-analysis-english-v4` / `job-analysis-original-v4`.
- [x] A1.2 Reconcile Capability Intelligence documentation with `job-capability-intelligence-v4` and schema v2.
- [x] A1.3 Reconcile Role Capability Blueprint documentation with prompt v2 / schema v1.
- [x] A1.4 Add `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md` as the focused current quality plan subordinate to the Phase-1/master gates.
- [x] A1.5 Reconcile the Review Snapshot / independent-model decision with the integrated CLI and first real `tG9K` snapshot findings.
- [x] A1.6 Reconcile README, AGENTS, Architecture, master/Phase-1 plan, Local Web App, and Review Snapshot entry-point/current-state text with the current implementation.
- [x] A1.7 Add `docs/WORKING_MEMORY.md` as the rolling non-authoritative handoff for the next conversation.
- [x] A1.8 Final stale-reference sweep completed across current/entry-point docs; historical incident/lesson records may retain historical version numbers when clearly historical.
- [x] A1.9 Audit `PRODUCT_SPECIFICATION.md`, `DOMAIN_AND_ANALYSIS_MODEL.md`, `SOURCE_POLICY.md`, and `ROADMAP.md`; leave them unchanged because their strategic/product/source invariants remain compatible with the reconciled execution state.

**A1 accepted:** a fresh conversation can follow repository docs without being told to implement v2/v3 contracts that are no longer current.

---

# B. Current semantic-quality gate

This is the immediate build/acceptance sequence. Do not jump to corpus-wide Phase 2.

## B0 — Current implemented baseline

- [x] B0.1 Hardened `english-projection-v2` exists and current `tG9K` translation artifact is dependency-linked.
- [x] B0.2 P1.6 v4 long-posting extraction/evidence-reference path is implemented.
- [x] B0.3 Capability Intelligence v4 evidence-reference/dependency path is implemented.
- [x] B0.4 Capability invalid-extra evidence cleanup is implemented when valid grounding remains.
- [x] B0.5 `unknown_or_unsupported` invalid-only evidence cleanup is implemented without weakening supported claims.
- [x] B0.6 Role Capability Blueprint v2 is implemented.
- [x] B0.7 Dedicated analysis/capability/blueprint model configuration exists.
- [x] B0.8 Review Snapshot v1 export exists.
- [x] B0.9 First real review snapshot `review-snapshots/jobs/tG9K.json` is committed and reviewable from GitHub.
- [x] B0.10 `tG9K` completed current P1.6 → Capability → Blueprint successfully after the evidence-normalization fixes.

Notes:

- The repository has observed successful deterministic test runs during this work, including the earlier 250-pass suite, but the final accepted head for the next tranche still requires the normal Ruff/pytest/warnings gate after new code changes.
- Do not infer that Phase 1 is closed merely because this bounded semantic chain runs.

---

## B1 — Fix Review Snapshot effective-model routing

**Priority: first code task in the next implementation session.**

- [!] B1.1 `jobhunter jobs snapshot <id>` currently calls `write_review_snapshot()` without the effective model-role arguments.
- [ ] B1.2 Pass `settings.effective_analysis_lm_studio_model()`.
- [ ] B1.3 Pass `settings.effective_capability_lm_studio_model()`.
- [ ] B1.4 Pass `settings.effective_blueprint_lm_studio_model()`.
- [ ] B1.5 Update `tests/test_review_snapshot_entrypoint.py` so integrated CLI routing verifies all three model roles.
- [ ] B1.6 Run focused snapshot/model-routing tests.
- [ ] B1.7 Run `ruff check .`, full `pytest`, and `pytest -W error`.
- [ ] B1.8 Regenerate `tG9K` snapshot and confirm `configured_models` contains the effective role models rather than null values.
- [ ] B1.9 Confirm `translation_matches_english_analysis`, `capability_is_current_chain`, and `blueprint_is_current_chain` remain true.

**Acceptance:** the normal integrated snapshot command is safe for future multi-model comparisons.

---

## B2 — P1.6 factual coverage / obligation / depth hardening (SQ-1)

P1.6 is the factual substrate. Fix this before downstream quality tuning.

### B2.1 Coverage accounting

- [ ] Identify a deterministic/structured way to ensure meaningful requirement-bearing long-description segments are either extracted or explainably excluded.
- [ ] Do **not** introduce a forced minimum claim count.
- [ ] Use `tG9K` as the first regression/acceptance example for explicit omitted families.

Known `tG9K` omissions to verify after the fix:

- [ ] Data & statistics: pandas / NumPy / SciPy / statsmodels / PCA / PLS.
- [ ] Industrial statistics: SPC / DOE / capability analysis / Bayesian methods.
- [ ] Fab data systems: MES / SECS-GEM / equipment/metrology/trace.
- [ ] Cloud providers / edge wording.
- [ ] `MATLAB a plus`.
- [ ] `some C / C++ helpful`.
- [ ] structured 3–6 years experience and Master's degree when semantically appropriate.

### B2.2 Obligation and depth

- [ ] Preserve `Python (expert)` as Python-specific depth.
- [ ] Do not propagate `expert` to all ML frameworks.
- [ ] Preserve `MATLAB a plus` as optional/preference evidence.
- [ ] Preserve `C/C++ helpful` as optional/helpful evidence.
- [ ] Preserve global `we don't expect every single item` without turning every stack item required or preferred.
- [ ] Evaluate whether the current P1.6 `required/preferred/contextual/inferred` enum can truthfully encode reviewed mixed/unspecified cases.
- [ ] Add `mixed`/`unspecified` only if reviewed examples prove the current contract is insufficient; version the prompt/schema as required by the resulting contract change.

### B2.3 Validation

- [ ] Add deterministic regression fixtures for the actual generic failure classes.
- [ ] Re-run `tG9K` English analysis only after the contract changes.
- [ ] Review the full P1.6 output before rebuilding Capability.
- [ ] Preserve exact evidence and artifact versioning/reuse behavior.

**Acceptance:** `tG9K` factual extraction is materially complete for its explicit requirements and does not inflate optionality/depth.

---

## B3 — Capability Intelligence calibration (SQ-2)

Start only after B2's P1.6 substrate is accepted for `tG9K`.

- [ ] B3.1 Ensure material explicit depth/seniority/experience evidence can populate `depth_signals`.
- [ ] B3.2 Prevent `requirement_strength` from systematically becoming stronger than accepted P1.6/source evidence.
- [ ] B3.3 Preserve optional cloud/edge wording as optional/uncertain context rather than high-confidence role topology.
- [ ] B3.4 Reduce capability-area leakage (for example MLOps uncertainty attached to a time-series capability without reason).
- [ ] B3.5 Keep invalid-extra evidence normalization deterministic.
- [ ] B3.6 Keep supported invalid-only evidence fail-closed.
- [ ] B3.7 Keep unknown-scope evidence-empty normalization valid.
- [ ] B3.8 Do not add semiconductor-specific validators.
- [ ] B3.9 Rebuild `tG9K` Capability after the accepted P1.6 change.
- [ ] B3.10 Review usefulness, evidence statuses, depth, requirement strength, unknown scope, and decomposition.

**Acceptance:** Capability is materially more useful than P1.6 without systematic over-strengthening or generic curriculum expansion.

---

## B4 — Blueprint calibration and dedicated-model comparison (SQ-3/SQ-4)

- [ ] B4.1 Confirm the Blueprint preserves accepted upstream optionality/unknowns.
- [ ] B4.2 Treat a technology list as evidence of available/desired technologies, not an architecture specification.
- [ ] B4.3 Prevent `highly_likely` scenarios from contradicting explicit unresolved unknowns.
- [ ] B4.4 Keep possible/likely example tools non-mandatory unless the source independently requires them.
- [ ] B4.5 Prefer general certainty/technical-correctness rules over domain-specific prompt patches.
- [ ] B4.6 Review the regenerated `tG9K` Blueprint under the current Gemma model.
- [ ] B4.7 Select one stronger local reasoning model candidate if Gemma still shows expert-judgment limitations.
- [ ] B4.8 Keep source, English projection, accepted P1.6, prompt/schema, and review rubric fixed for the model comparison.
- [ ] B4.9 Compare technical correctness, calibration, scenario realism, unsupported inference, and usefulness.
- [ ] B4.10 Configure a dedicated Capability/Blueprint model only if the evidence supports the choice.
- [-] B4.11 Do not build multi-model voting/ensembles.

**Acceptance:** Blueprint is useful professional interpretation without routinely inventing one architecture from a broad stack list.

---

## B5 — CI-3 representative live review (SQ-5)

Current accepted review anchors:

```text
t4jp  sparse/ambiguous AI-content posting
tG9K  rich semiconductor/industrial-ML posting
```

Add materially different examples:

- [ ] B5.1 Python/software role.
- [ ] B5.2 network/security role.
- [ ] B5.3 operations/platform/DevOps role.
- [ ] B5.4 Prefer multiple companies and varied description length/language/requirement density.
- [ ] B5.5 For each job, review source → English → P1.6 → Capability → Blueprint.
- [ ] B5.6 Generate/update a Review Snapshot for selected acceptance examples.
- [ ] B5.7 Record P1.6 false positives/negatives and strength/depth mistakes.
- [ ] B5.8 Record Capability evidence-status/decomposition/unknown-scope mistakes.
- [ ] B5.9 Record Blueprint technical/over-inference/certainty mistakes.
- [ ] B5.10 Convert repeatable deterministic failures into fixtures.
- [ ] B5.11 Record model-capability limitations separately from deterministic defects.

**Acceptance:** heterogeneous reviewed evidence is good enough to promote/freeze the bounded semantic contracts or clearly identifies one final contract/model revision.

---

# C. Phase-1 closure after semantic acceptance

Do not spend indefinite time polishing Capability/Blueprint after B5 passes.

## C1 — Market truthfulness

- [ ] Exact analyzed-current sample size visible.
- [ ] Source/filter scope recoverable.
- [ ] Current analysis contract identity recoverable.
- [ ] Required/preferred/contextual/inferred counts remain semantically honest.
- [ ] Small-sample warning.
- [ ] Employer/role concentration warning where appropriate.
- [ ] Coverage metrics remain separate from semantic-quality certification.

## C2 — Source/lifecycle acceptance

- [ ] network failure != expired/removed.
- [ ] 429 != empty/removed.
- [ ] 500/502/503/504 != expired.
- [ ] challenge/auth/access != missing job.
- [ ] first 404/410 remains cautious.
- [ ] repeated strong missing evidence follows the defined lifecycle rule.
- [ ] last-successful/consecutive-failure summaries are accepted.

## C3 — Operation/partial-success truthfulness

For multi-stage work preserve:

```text
requested
attempted
completed
reused
skipped intentionally
failed
remaining eligible
```

- [ ] Browser and CLI summaries agree.
- [ ] Earlier durable success survives later-stage failure.
- [ ] `no eligible work` remains distinct from `attempt failed`.

## C4 — P1.7 final run/reporting

- [ ] Finalize per-job report/provenance surface.
- [ ] Ready-job analysis queue.
- [ ] Combined current-corpus report.
- [ ] `jobhunter run` deterministic end-to-end acceptance.
- [ ] browser equivalent acceptance over the same services.
- [ ] rerun/idempotency proof.
- [ ] bounded live end-to-end Phase-1 acceptance.

## C5 — Phase-1 closure

- [ ] Acceptance summary with exact corpus/sample/contracts/bounds.
- [ ] Reconcile README/product/architecture/current-state docs to accepted reality.
- [ ] Freeze/identify accepted P1.6 starting contract for Phase 2.
- [ ] Mark unresolved non-capabilities explicitly.

---

# D. Phase 2 — gated

Do **not** begin until Phase-1 closure.

Then continue the master/roadmap sequence:

```text
canonical concept registry
→ reviewed alias/mapping
→ canonical responsibilities/deliverables
→ job capability requirement profiles at corpus scale
→ role archetypes
→ Market v2
→ later personal evidence/gap intelligence
```

Still deferred:

- automatic taxonomy growth;
- corpus-wide Blueprint generation;
- personal readiness scoring;
- learning-plan generation;
- application ranking;
- autonomous applications;
- vector/RAG infrastructure;
- generic plugin framework;
- multi-model voting.
