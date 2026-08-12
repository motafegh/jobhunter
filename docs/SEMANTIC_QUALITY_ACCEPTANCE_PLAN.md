# JobHunter Semantic Quality Acceptance Plan

**Status:** Active bounded acceptance plan  
**Date:** 2026-08-12  
**Scope:** P1.6 factual extraction, Capability Intelligence, heterogeneous semantic review, selected Review Snapshots, and the concluded Phase-1 Blueprint experiment  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`, `docs/ROADMAP.md`, and product/domain/source/architecture constraints.

This plan does not authorize corpus-wide Phase-2 taxonomy/Market-v2 work.

## 1. Permanent acceptance principles

Intelligence depth follows evidence density:

```text
sparse evidence
→ modest strong conclusions
→ explicit unknowns

rich evidence
→ deeper work-linked decomposition
→ richer supported reasoning
```

Permanent rules:

1. **Mechanical provenance correctness and semantic calibration are separate acceptance gates.**
2. A downstream layer never becomes more authoritative than accepted upstream evidence.
3. Optional/contextual source language must not become mandatory downstream.
4. Explicit depth belongs only to the exact concept the source qualifies.
5. Do not polish model reasoning indefinitely when repeated experiments show the layer is not stable enough for the current phase.

Current opposite-end anchors:

```text
t4jp  sparse/ambiguous source
tG9K  rich semiconductor/industrial-ML source
```

## 2. Current accepted contracts

```text
source parser:                 jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2

English P1.6:                 job-analysis-english-v9
Original P1.6:                job-analysis-original-v9
P1.6 schema:                  job-analysis-v4

Capability accepted baseline: job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4

Review Snapshot:              job-review-snapshot-v1
```

Blueprint implementation remains available experimentally at:

```text
role-capability-blueprint-v6
schema role-capability-blueprint-v5
best bounded model tested: gemma-4-12b-it-qat
```

Blueprint is **not an accepted Phase-1 decision layer**.

## 3. Layer authority

Accepted Phase-1 semantic stack:

```text
source/original employer text
→ parsed source fields
→ English projection
→ P1.6 factual extraction
→ Capability grouping + deterministic source truth
```

Experimental only:

```text
accepted P1.6 + Capability
→ Blueprint professional interpretation
```

Blueprint output must not feed Market, personal readiness, automatic recommendations, or other authoritative Phase-1 decisions.

## 4. SQ-0 — Review Snapshot correctness

**Accepted.**

Normal workflow:

```bash
jobhunter jobs snapshot <job-id>
```

The exporter records dependency/model identities and current-chain status while excluding raw model prompts/responses, SQLite, secrets, logs and future private state.

## 5. SQ-1 — P1.6 factual coverage / obligation / depth

**Accepted on dense `tG9K` artifact 29.**

Acceptance evidence:

- 27 requirements;
- 7 responsibilities;
- deterministic coverage accounting;
- Python `expert` preserved only for Python;
- MATLAB/C++ preference retained;
- contextual stack remains contextual;
- `Solid`, `Strong`, `Hands-on`, `Comfort`, and experience-duration depth preserved;
- education and experience included;
- exact evidence retained.

Current analysis model:

```text
gemma-4-e4b-it-ud
```

This bounded acceptance still requires heterogeneous confirmation before promotion to broader Phase-2 use.

## 6. SQ-2 — Capability Intelligence calibration

**Accepted for bounded rich `tG9K` on Capability artifact 9.**

Accepted v7 boundary:

```text
accepted P1.6
→ deterministic source partition
→ model semantic grouping + derived reasoning draft
→ complete-coverage validation
→ deterministic source_truth / strength / explicit depth / explicit work
→ persisted Capability v7
```

`tG9K` acceptance evidence:

```text
P1.6 artifact 29
Capability artifact 9
25/25 capability-relevant requirements linked
7/7 responsibilities linked
27/27 requirements retained in source truth
6/6 explicit depth facts retained in source truth
role-level requirement indices [25, 26]
2 accepted Capability profiles
no positive independence expectation
cross_capability_observations []
```

Freeze v7 unless heterogeneous evidence shows a repeatable correctness defect.

Important downstream lesson: accepted Capability **grouping and deterministic source truth** may be reused, but Capability model-derived explanatory prose is not automatically authoritative input to another generative layer.

Decision record:

```text
docs/experiments/2026-08-11_CAPABILITY_V7_B3_ACCEPTANCE.md
```

## 7. SQ-3 — Blueprint experiment disposition

**Status: concluded for Phase 1 / not accepted / further tuning deferred.**

The Blueprint experiment tested multiple contract boundaries and local models:

```text
v3/v2 + E2B/E4B
→ provenance namespace confusion + architecture/optionality overreach

v4/v3 + E4B
→ deterministic provenance fixed; broad model prose still invented operating/topology/ownership claims

v5/v4 + E4B
→ Capability-derived prose removed; free-form interpretation still inflated end-to-end/streaming/lifecycle scope

v6/v5 + E4B
→ narrow bounded contract; structured repair failed and assumptions remained

v6/v5 + gemma-4-12b-it-qat
→ mechanically valid and materially better; semantic boundary still violated by assumption-bearing unknowns/considerations
```

### Best bounded Blueprint evidence

```text
job tG9K
Blueprint artifact 7
P1.6 artifact 29
Capability artifact 9
prompt role-capability-blueprint-v6
schema role-capability-blueprint-v5
model gemma-4-12b-it-qat
snapshot commit 671bd6e3c43555c631958531671a0f1be9726554
```

Mechanical audit passed with:

```text
2 Capability areas
25 deterministic source requirements
7 deterministic source responsibilities
4 professional considerations
4 important unknowns
2 role-level constraints
1 role-purpose item
```

CI also passed.

### Why it is still not accepted

The explicit v6 semantic rubric rejects generated statements or unknowns that smuggle unstated architecture, feedback loops, platforms, or implementation obligations.

The 12B artifact still contained examples such as:

- asking whether automated APC/SPC feedback loops are operational although source does not establish an automated feedback-loop architecture;
- asking which cloud provider or on-prem platform is currently used, implicitly assuming a deployment choice exists;
- introducing `raw sensor physics` as part of the role interpretation;
- mapping traceability/governance into strict versioning of data lineage/model weights and unspecified quality standards.

These are milder than prior failures, but accepting them would contradict the project’s own semantic boundary.

### Phase-1 decision

Do **not**:

- create Blueprint v7 during Phase 1;
- weaken v6 validators;
- add vacancy/domain-specific prompt patches;
- continue adjacent local-model shopping;
- promote Blueprint artifacts into accepted Market/personal/recommendation truth.

Keep Blueprint v6/v5 code and artifact 7 as experimental evidence. Reopen only when a materially different grounding/inference approach or a demonstrated user-value gap justifies it.

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

## 8. SQ-4 / CI-3 — heterogeneous live semantic acceptance — active

This is now the active semantic gate.

Validate the stack that has actually passed bounded acceptance:

```text
source
→ English projection
→ P1.6
→ Capability v7
```

Blueprint may be observed during review only as non-gating research evidence.

Use materially different jobs where possible:

1. `t4jp` sparse/ambiguous source;
2. `tG9K` rich AI/ML industrial baseline;
3. Python/software role;
4. network/security role;
5. operations/platform/DevOps role.

For each selected case inspect:

### P1.6

- factual false positives/negatives;
- responsibility vs candidate-qualification classification;
- requirement strength;
- optional/contextual wording;
- explicit depth attachment;
- education/experience preservation;
- evidence relevance and exactness;
- dense-source coverage vs sparse-source restraint.

### Capability v7

- complete capability-relevant requirement coverage;
- complete responsibility coverage;
- coherent grouping rather than catch-all profiles;
- role-level requirement partition;
- deterministic source truth;
- source strength/depth/work reconciliation;
- no unsupported ownership/autonomy inference;
- no contextual/preferred tool promotion;
- model-derived prose not treated as more authoritative than source truth.

### Engineering follow-up

- convert repeatable deterministic defects into fixtures/tests;
- distinguish model limitations from deterministic bugs;
- change the frozen v7 contract only for a repeatable material correctness defect;
- avoid role-specific prompt patch collections.

## 9. SQ-5 — heterogeneous acceptance decision

The bounded semantic stack is ready to freeze/promote as Phase-2 input only when heterogeneous evidence shows that:

- P1.6 remains conservative on sparse sources and complete enough on dense ones;
- obligation strength and explicit depth remain calibrated across role families;
- evidence remains trustworthy;
- Capability source truth remains complete;
- Capability grouping remains professionally coherent across materially different roles;
- no repeatable deterministic defect remains unresolved;
- observed model limitations are documented and acceptable for the intended Phase-2 use.

If a selected role fails, fix only the general failure class and rerun the affected bounded sample.

## 10. Stop rule

Do not polish semantic reasoning indefinitely.

Once P1.6 + Capability v7 are accepted across the heterogeneous bounded sample, return to Phase-1 closure:

```text
Market truthfulness/sampling
→ source/lifecycle acceptance
→ partial-success semantics
→ P1.7 report/run/browser acceptance
→ Phase-1 closure
```

Only after Phase-1 closure begin corpus-wide Phase 2.
