# JobHunter Semantic Quality Acceptance Plan

**Status:** Active bounded acceptance plan  
**Date:** 2026-08-11  
**Scope:** P1.6 factual extraction, Capability Intelligence, Role Capability Blueprint, model-role comparison, and selected Review Snapshots  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`, `docs/ROADMAP.md`, and product/domain/source/architecture constraints.

This plan does not authorize corpus-wide Phase-2 taxonomy/Market-v2 work.

## 1. Permanent acceptance principle

Intelligence depth follows evidence density:

```text
sparse evidence
→ modest strong conclusions
→ explicit unknowns
→ limited architecture/tool speculation

rich evidence
→ deeper work-linked decomposition
→ richer supported interpretation
```

Current opposite-end anchors:

```text
t4jp  sparse/ambiguous source
tG9K  rich semiconductor/industrial-ML source
```

Permanent acceptance rule:

> **Mechanical provenance correctness and semantic calibration are separate acceptance gates.**

A downstream artifact can be perfectly linked to upstream truth and still fail if generated interpretation manufactures certainty.

## 2. Current contracts

```text
source parser:                 jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2

English P1.6:                 job-analysis-english-v9
Original P1.6:                job-analysis-original-v9
P1.6 schema:                  job-analysis-v4

Capability accepted baseline: job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4

Blueprint candidate:          role-capability-blueprint-v6
Blueprint schema:             role-capability-blueprint-v5

Review Snapshot:              job-review-snapshot-v1
```

B3 Capability is accepted for bounded `tG9K` on artifact 9. B4 Blueprint remains active and is not yet semantically accepted.

## 3. Permanent layer contract

```text
P1.6
→ factual substrate
→ exact employer/source-supported facts
→ conservative strength/depth/evidence

Capability Intelligence
→ auditable grouping/reasoning above P1.6
→ source truth must survive

Role Capability Blueprint
→ human-facing professional context
→ source truth displayed separately from inference
→ every positive generated inference explicitly bounded by uncertainty
```

A downstream layer never upgrades an incorrect, uncertain, contextual or preferred upstream claim into truth.

## 4. SQ-0 — Review Snapshot correctness

**Accepted.**

Normal workflow:

```bash
jobhunter jobs snapshot <job-id>
```

The exporter records effective model roles, dependency identities and current-chain flags while excluding raw responses/prompts, SQLite, secrets and private state.

## 5. SQ-1 — P1.6 factual coverage / obligation / depth

**Accepted on `tG9K` artifact 29.**

Acceptance evidence:

- 27 requirements;
- 7 responsibilities;
- complete deterministic coverage accounting;
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

## 6. SQ-2 — Capability Intelligence calibration

**Accepted for bounded rich `tG9K` on Capability artifact 9.**

Accepted v7 boundary:

```text
accepted P1.6
→ deterministic source partition
→ model semantic grouping + derived reasoning draft
→ complete-coverage validation
→ deterministic source_truth / strength / explicit depth / explicit work
→ persisted v7 artifact
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

Freeze v7 unless downstream or heterogeneous evidence shows a repeatable correctness defect.

Downstream caution learned during B4: Capability **grouping and deterministic source truth** may be accepted while Capability model-derived explanatory prose remains too aggressive to treat as authoritative input to another generative layer.

## 7. SQ-3 — Blueprint calibration

**Current gate: active / not yet accepted.**

Current candidate:

```text
role-capability-blueprint-v6
schema role-capability-blueprint-v5
Blueprint model gemma-4-e4b-it-ud
```

### Historical v3 result

V3/v2 failed B4 with E2B and E4B. Both models confused P1.6 requirement indices with Capability-profile indices and retained architecture/optionality overreach. Validators remain historical negative evidence and must not be weakened.

### Historical v4 result

V4/v3 removed model-owned provenance bookkeeping. Live E4B generation completed and mechanical audit passed with 2 Capability areas, 25 deterministic requirements, 7 deterministic responsibilities and 2 exact role constraints.

B4 still failed semantic review because model prose invented or strengthened real-time/low-latency control, employer topology, process physics, edge placement, specific governance implementation and end-to-end lifecycle ownership.

This is the canonical proof that **mechanical audit PASS does not equal B4 PASS**.

### Historical v5 result

V5/v4 excluded Capability-derived prose from model input and removed role shape, hidden requirements, tool suggestions, work products, scenarios and bottom-line generation.

Live `tG9K` Blueprint artifact **6** was current-chain, published in Review Snapshot commit `ffa690361e5cbbb755fff7bcd587d6903d5dce89`, and CI passed.

B4 still failed. Area 2's free-form `practical_interpretation` described end-to-end infrastructure, telemetry streaming, automated MLOps workflows and deployment-lifecycle scope, while its own uncertainty admitted ownership boundaries were unknown.

Therefore v5/v4 is rejected and the free-form positive role-summary surface is removed rather than prompt-patched.

### V6 deterministic/model boundary

V6 keeps the successful deterministic provenance boundary and limits the model to explicitly uncertain professional considerations and unknowns.

Required invariants:

1. model receives accepted Capability labels/grouping but no Capability-derived explanatory prose;
2. long vacancy/company-description prose is not redundantly supplied after accepted P1.6 establishes source facts;
3. model-facing schema contains no Capability/P1.6 numeric provenance;
4. model returns exactly one item per accepted Capability profile in source order;
5. JobHunter deterministically attaches Capability identity/coverage;
6. JobHunter deterministically attaches exact source role purpose, requirements, responsibilities, obligation strength, explicit depth, evidence and role-level constraints;
7. there is no free-form `practical_interpretation`, role-shape, likely-depth, hidden-requirement, tool-suggestion, work-product, scenario/topology, probably-not-required or bottom-line output;
8. every positive generated statement exists only in `professional_considerations`;
9. each professional consideration is `plausible` or `speculative` and must have a concrete uncertainty sentence;
10. every Capability must include at least one `important_unknown`;
11. generic validation rejects employer-obligation wording and full/end-to-end lifecycle/stack/pipeline/system/infrastructure scope;
12. high-volume data != streaming;
13. process control/anomaly detection != real-time or low latency;
14. APC/SPC != automated feedback loop;
15. cloud/edge names != deployment placement;
16. deployment/governance != lifecycle ownership;
17. unknown wording must not itself presume an unstated system;
18. contextual/preferred source items and exact depth remain authoritative.

### Fixed `tG9K` B4 chain

```text
English projection artifact 33
English P1.6 artifact 29
Capability v7 artifact 9
Blueprint model gemma-4-e4b-it-ud
```

Do not rebuild translation, P1.6 or Capability for this test.

Confirm active contract:

```bash
python -c "from jobhunter.role_blueprint_service import BLUEPRINT_PROMPT_VERSION, BLUEPRINT_SCHEMA_VERSION; print(BLUEPRINT_PROMPT_VERSION); print(BLUEPRINT_SCHEMA_VERSION)"
```

Expected:

```text
role-capability-blueprint-v6
role-capability-blueprint-v5
```

Run only:

```bash
jobhunter jobs blueprint tG9K
```

If valid:

```bash
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v6_snapshot.py
```

### SQ-3 mechanical gate

The v6 audit must confirm:

- English analysis artifact 29 and Capability artifact 9 remain exact upstream dependencies;
- Blueprint contract is v6/v5;
- exactly one area per accepted Capability profile, in source order with exact labels;
- `source_capability_coverage` is complete;
- exact deterministic role purpose, P1.6 requirements/responsibilities and role constraints survive with exact strength/depth/evidence;
- v5 free-form area fields are absent;
- every Capability has at least one non-empty important unknown;
- every professional consideration is plausible/speculative and carries non-empty uncertainty;
- generated consideration statements contain no mechanically detectable employer-obligation/full-scope wording;
- older expansion fields remain absent.

### SQ-3 semantic gate

Mechanical validity is necessary but insufficient. Reject B4 if the complete v6 artifact:

- merely restates source anchors without useful practitioner value;
- uses uncertainty as boilerplate while still implying employer-specific architecture/operations;
- promotes contextual/preferred frameworks/cloud/edge/MATLAB/C/C++;
- spreads Python `expert` depth;
- assembles named technologies into one company architecture;
- implies streaming/real-time/low-latency/factory-floor/automated-feedback behavior without source support;
- invents cloud/edge placement or full lifecycle ownership;
- creates generic curriculum rather than role-specific professional context;
- writes unknowns that presume a stream, feedback loop, topology or platform not established by source;
- provides so little value that the Blueprint layer is not justified above P1.6 + Capability.

B4 passes only when source truth and professional inference remain unmistakably separate **and** the bounded inference is materially useful.

Records:

```text
docs/experiments/2026-08-11_BLUEPRINT_V3_GROUNDED_INTERPRETATION.md
docs/experiments/2026-08-11_BLUEPRINT_V4_DETERMINISTIC_PROVENANCE_BOUNDARY.md
docs/experiments/2026-08-11_BLUEPRINT_V4_SEMANTIC_FAILURE_AND_V5_BOUNDARY.md
docs/experiments/2026-08-11_BLUEPRINT_V5_SEMANTIC_FAILURE_AND_V6_BOUNDARY.md
```

## 8. SQ-4 — Controlled model-role comparison

The v3 E2B→E4B comparison established a contract-boundary problem, not a reason for indefinite model shopping.

For future comparisons, hold fixed source semantic version, English projection, accepted P1.6, accepted Capability, Blueprint contract and review rubric. Change only the Blueprint model.

No multi-model voting/ensemble.

## 9. SQ-5 / CI-3 — heterogeneous live acceptance

After bounded B4 acceptance, review materially different jobs:

1. `t4jp` sparse/ambiguous;
2. `tG9K` rich AI/ML;
3. Python/software;
4. network/security;
5. operations/platform/DevOps.

For each selected case inspect:

```text
source
→ English
→ P1.6
→ Capability
→ Blueprint
```

Record factual false positives/negatives, strength/depth mistakes, evidence mismatch, capability decomposition/status mistakes, missing unknowns, Blueprint technical/certainty mistakes, and model limitations separately from deterministic defects.

## 10. Stop rule

Do not polish semantic reasoning indefinitely.

Once the bounded semantic slice is accepted across heterogeneous evidence, stop expanding it and return to Phase-1 closure:

```text
Market truthfulness/sampling
→ source/lifecycle acceptance
→ partial-success semantics
→ P1.7 report/run/browser acceptance
→ Phase-1 closure
```

Only after Phase-1 closure begin corpus-wide Phase 2.
