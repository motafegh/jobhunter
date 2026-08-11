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

Blueprint candidate:          role-capability-blueprint-v4
Blueprint schema:             role-capability-blueprint-v3

Review Snapshot:              job-review-snapshot-v1
```

B3 Capability is accepted for the bounded `tG9K` gate on artifact 9. B4 Blueprint is the current active gate and is not yet semantically accepted.

## 3. Permanent layer contract

```text
P1.6
→ factual substrate
→ exact employer/source-supported facts
→ conservative strength/depth/evidence

Capability Intelligence
→ auditable reasoning above P1.6
→ grouping, prerequisites/context, unknown scope
→ no loss or strengthening of accepted source truth

Role Capability Blueprint
→ human-facing professional interpretation
→ useful scope/examples/scenarios with calibrated uncertainty
```

A downstream layer never upgrades an incorrect or uncertain upstream claim into truth.

## 4. SQ-0 — Review Snapshot correctness

**Accepted.**

The normal repository-native review workflow is:

```bash
jobhunter jobs snapshot <job-id>
```

The exporter records effective analysis/capability/blueprint models, dependency identities, and current-chain flags while excluding raw responses/prompts, SQLite, secrets, and private state.

## 5. SQ-1 — P1.6 factual coverage / obligation / depth

**Accepted on `tG9K` artifact 29.**

Acceptance evidence:

- 27 requirements;
- 7 responsibilities;
- complete deterministic coverage accounting;
- Python `expert` preserved only for Python;
- `MATLAB a plus` and `C/C++ helpful` preserved as preference/optional evidence;
- individually unspecified technical-stack obligation represented as contextual;
- `Solid`, `Strong`, `Hands-on`, `Comfort`, and experience-duration depth preserved;
- education and experience included;
- exact evidence retained.

Current analysis role:

```text
gemma-4-e4b-it-ud
```

## 6. SQ-2 — Capability Intelligence calibration

**Accepted for the bounded rich `tG9K` gate on Capability artifact 9.**

Historical negative evidence remains useful:

- v4/v2 artifact 7 omitted explicit depth and over-strengthened stack/cloud/ownership;
- v5 exhausted bounded output budget and was reverted;
- v6/v3 artifact 8 proved deterministic reconciliation of linked facts but model-selected links were too incomplete and semantic overreach remained.

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
2 coherent capability profiles
no positive independence expectation
cross_capability_observations []
```

Five of the six depth facts appear inside profiles. The sixth is intentionally role-level professional experience (`three to six years`, requirement 26). This is correct partitioning, not missing depth.

Decision record:

```text
docs/experiments/2026-08-11_CAPABILITY_V7_B3_ACCEPTANCE.md
```

Freeze v7 unless downstream or heterogeneous evidence shows a repeatable correctness defect.

## 7. SQ-3 — Blueprint calibration

**Current gate: active / not yet accepted.**

Current candidate:

```text
role-capability-blueprint-v4
schema role-capability-blueprint-v3
Blueprint model gemma-4-e4b-it-ud
```

### Why v3 was rejected

Blueprint v3/v2 was tested against the fixed `tG9K` chain with both E2B and E4B.

Both models confused P1.6 requirement indices with Capability-profile indices. E4B's bounded repair correctly identified several requirement numbers but placed them into `source_depth_signals` rather than `source_requirement_indices`. Both runs also retained material semantic overreach around streaming, cloud/edge, MLOps and end-to-end architecture.

Therefore v3/v2 fails B4. Its validators remain correct and must not be weakened. Do not revive v3 with prompt patches or a larger model merely to make the LLM reproduce deterministic provenance.

### V4 deterministic/model boundary

V4 applies the Capability-v7 lesson again:

> **The model reasons; JobHunter owns provenance bookkeeping.**

Required invariants:

1. model-facing Blueprint schema contains no Capability/P1.6 numeric provenance;
2. model returns exactly one interpretation per accepted Capability profile, in source order;
3. JobHunter deterministically attaches exact Capability identity and complete coverage;
4. JobHunter deterministically attaches each Capability profile's source requirements and responsibilities;
5. source requirement strength, explicit depth and evidence come from accepted upstream truth;
6. source-named technologies are represented by deterministic source requirements, not model-created `source_named` records;
7. model-created suggested tools are only `likely_example` or `possible_example`, carry no source provenance, and cannot be required/mandatory/necessary or expert/mastery claims;
8. role-level degree/experience constraints are copied from Capability source truth;
9. hidden requirements are only plausible/speculative;
10. model-created workflows are explicitly `professional_example_scenarios` and only plausible/speculative;
11. JobHunter injects `scenario_basis = professional_example`;
12. material unstated architecture/topology/latency/vendor/batch-stream/cloud-edge/scale/ownership/orchestration/feedback choices remain assumptions;
13. technology list != architecture.

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
role-capability-blueprint-v4
role-capability-blueprint-v3
```

Run only:

```bash
jobhunter jobs blueprint tG9K
```

If a valid Blueprint artifact is produced:

```bash
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v4_snapshot.py
```

### SQ-3 mechanical gate

The v4 audit must confirm:

- English analysis artifact 29 and Capability artifact 9 remain the exact upstream dependencies;
- Blueprint contract is v4/v3;
- persisted Blueprint contains exactly one area per accepted Capability profile in the same order and with the exact label;
- `source_capability_coverage` is complete;
- each area carries exact deterministic P1.6 source requirements and responsibilities matching Capability artifact 9 links;
- source concept/type/strength/depth/evidence remains exact;
- role-level constraints remain exact;
- suggested tools contain no source provenance fields;
- hidden requirements are only plausible/speculative;
- professional examples are only plausible/speculative and carry deterministic `professional_example` basis;
- legacy v3 provenance/scenario fields are absent.

### SQ-3 semantic gate

Mechanical validity is necessary but insufficient. Reject B4 if the complete artifact:

- simply paraphrases P1.6/Capability instead of adding professional value;
- inflates the role into a broader MLOps/platform identity without support;
- promotes contextual/preferred frameworks/cloud/edge/MATLAB/C/C++;
- spreads Python `expert` depth to neighboring frameworks;
- assembles named technologies into one claimed hidden company architecture;
- labels illustrative workflows as employer topology;
- hides assumptions about latency/topology/vendor/batch-stream/cloud-edge/ownership;
- asserts real-time, microservices, CI/CD, model registry, regulatory constraints, autonomous feedback or control loops without support;
- invents generic hidden requirements/curriculum;
- misuses technical tools/protocols/platforms;
- amplifies broad Capability wording into ownership/autonomy certainty;
- fails to preserve important unknowns.

B4 passes only when the human-facing explanation is materially useful, technically sound, and calibrated.

Records:

```text
docs/experiments/2026-08-11_BLUEPRINT_V3_GROUNDED_INTERPRETATION.md
docs/experiments/2026-08-11_BLUEPRINT_V4_DETERMINISTIC_PROVENANCE_BOUNDARY.md
```

## 8. SQ-4 — Controlled model-role comparison

The v3 E2B→E4B comparison is complete and established a contract-boundary problem rather than a reason to continue model shopping.

For future model comparisons, hold fixed:

```text
source semantic version
English projection
accepted P1.6
accepted Capability
Blueprint contract
review rubric
```

Change only the Blueprint model. Compare technical correctness, calibration, useful professional interpretation, unsupported inference, uncertainty, and usefulness per token/time.

Do not compare another model during the first v4 live run. No multi-model voting/ensemble.

## 9. SQ-5 / CI-3 — heterogeneous live acceptance

After B4, review materially different jobs:

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

Record factual false positives/negatives, strength/depth mistakes, evidence mismatch, capability decomposition/status mistakes, unsupported prerequisites, missing unknowns, Blueprint technical/certainty mistakes, and model limitations separately from deterministic defects.

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
