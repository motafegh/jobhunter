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

A second permanent principle now applies:

> **Mechanical provenance correctness and semantic calibration are separate acceptance gates.**

A downstream artifact can be perfectly linked to upstream truth and still fail if its generated interpretation manufactures certainty.

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

Blueprint candidate:          role-capability-blueprint-v5
Blueprint schema:             role-capability-blueprint-v4

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
→ auditable grouping/reasoning above P1.6
→ source truth must survive

Role Capability Blueprint
→ human-facing professional interpretation
→ source truth displayed separately from inference
→ interpretation uncertainty must remain visible
```

A downstream layer never upgrades an incorrect, uncertain, contextual or preferred upstream claim into truth.

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
2 accepted Capability profiles
no positive independence expectation
cross_capability_observations []
```

Five of the six depth facts appear inside profiles. The sixth is intentionally role-level professional experience (`three to six years`, requirement 26).

Decision record:

```text
docs/experiments/2026-08-11_CAPABILITY_V7_B3_ACCEPTANCE.md
```

Freeze v7 unless downstream or heterogeneous evidence shows a repeatable correctness defect.

Downstream caution learned during B4: Capability **grouping and deterministic source truth** may be accepted while some Capability model-derived explanatory prose remains too aggressive to treat as authoritative input to another generative layer.

## 7. SQ-3 — Blueprint calibration

**Current gate: active / not yet accepted.**

Current candidate:

```text
role-capability-blueprint-v5
schema role-capability-blueprint-v4
Blueprint model gemma-4-e4b-it-ud
```

### Historical v3 result

Blueprint v3/v2 failed B4 with both E2B and E4B. Both models confused P1.6 requirement indices with Capability-profile indices and retained architecture/optionality overreach. Its validators remain useful negative evidence and must not be weakened.

### Historical v4 result

Blueprint v4/v3 correctly removed model-owned provenance bookkeeping. The live E4B `tG9K` run completed and its mechanical audit passed with:

```text
2 Capability areas
25 deterministic source requirements
7 deterministic source responsibilities
2 exact role-level constraints
0 suggested tools
0 hidden requirements
0 professional scenarios
```

B4 nevertheless failed semantic review because generated prose still invented or strengthened:

- real-time process adjustment;
- low-latency active control loops;
- factory-floor/MES-SECS data-path topology;
- process physics as a candidate obligation;
- a specific code/training-slice/hyperparameter audit trail;
- edge importance based on unstated topology;
- end-to-end lifecycle ownership.

This is the canonical proof that **mechanical audit PASS does not equal B4 PASS**.

### V5 deterministic/model boundary

V5 keeps v4's provenance success and reduces the model's semantic authority.

Required invariants:

1. the model receives accepted Capability labels/grouping but not Capability `summary`, `sub_capabilities`, `underlying_knowledge`, operational reasoning or other model-derived Capability prose;
2. the long vacancy/company-description prose is not redundantly supplied after accepted P1.6 establishes source facts;
3. model-facing schema contains no Capability/P1.6 numeric provenance;
4. model returns exactly one interpretation per accepted Capability profile, in source order;
5. JobHunter deterministically attaches Capability identity and complete coverage;
6. JobHunter deterministically attaches exact source role purpose, source requirements, source responsibilities, obligation strength, explicit depth, evidence and role-level constraints;
7. each main model interpretation is persisted with fixed `plausible` strength and is explicitly not employer fact;
8. every main interpretation requires a non-empty `interpretation_uncertainty` boundary;
9. professional considerations are only `plausible` or `speculative` and each requires an uncertainty sentence;
10. generic validation rejects unqualified obligation/full-ownership wording in model prose;
11. v5 has no model-generated role shape, likely-depth field, hidden requirements, tool suggestions, work-product list, scenario/topology or bottom line at B4;
12. technology list != architecture;
13. process-control/deployment/cloud/edge evidence does not prove real-time inference, low latency, active feedback, factory-floor deployment or autonomous process adjustment;
14. contextual/preferred source items remain contextual/preferred and explicit depth remains exact.

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
role-capability-blueprint-v5
role-capability-blueprint-v4
```

Run only:

```bash
jobhunter jobs blueprint tG9K
```

If a valid Blueprint artifact is produced:

```bash
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v5_snapshot.py
```

### SQ-3 mechanical gate

The v5 audit must confirm:

- English analysis artifact 29 and Capability artifact 9 remain exact upstream dependencies;
- Blueprint contract is v5/v4;
- exactly one area per accepted Capability profile, in source order with exact labels;
- `source_capability_coverage` is complete;
- exact deterministic role purpose, P1.6 requirements/responsibilities and role-level constraints survive with exact strength/depth/evidence;
- every area is mechanically `plausible` professional inference;
- every area has non-empty interpretation uncertainty;
- every professional consideration is plausible/speculative and has uncertainty;
- model prose does not contain unqualified obligation/full-ownership patterns;
- legacy v4 expansion fields are absent.

### SQ-3 semantic gate

Mechanical validity is necessary but insufficient. Reject B4 if the complete v5 artifact:

- merely paraphrases source anchors without adding useful practitioner context;
- uses uncertainty as boilerplate while still asserting employer-specific architecture/operations;
- promotes contextual/preferred frameworks/cloud/edge/MATLAB/C/C++;
- spreads Python `expert` depth to neighboring frameworks;
- assembles named technologies into one hidden company architecture;
- implies real-time/low-latency/factory-floor/active-control-loop behavior as employer fact;
- turns process/equipment physics into a candidate obligation without source support;
- converts general traceability/reproducibility/governance into one specific implementation and presents it as required;
- creates ownership/autonomy certainty not established upstream;
- loses important topology, latency, deployment, ownership, scale or exact-tool-use unknowns;
- produces generic curriculum-like professional considerations rather than role-specific interpretation.

B4 passes only when source truth and professional inference remain unmistakably separate **and** the inference is materially useful.

Records:

```text
docs/experiments/2026-08-11_BLUEPRINT_V3_GROUNDED_INTERPRETATION.md
docs/experiments/2026-08-11_BLUEPRINT_V4_DETERMINISTIC_PROVENANCE_BOUNDARY.md
docs/experiments/2026-08-11_BLUEPRINT_V4_SEMANTIC_FAILURE_AND_V5_BOUNDARY.md
```

## 8. SQ-4 — Controlled model-role comparison

The v3 E2B→E4B comparison established a contract-boundary problem, not a reason for indefinite model shopping.

For future comparisons, hold fixed:

```text
source semantic version
English projection
accepted P1.6
accepted Capability
Blueprint contract
review rubric
```

Change only the Blueprint model. Compare technical correctness, calibration, useful professional interpretation, unsupported inference, uncertainty, and usefulness per token/time.

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
