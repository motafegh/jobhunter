# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-11  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** B4 / SQ-3 Role Capability Blueprint  
**Purpose:** Resume from the real current repository state without reconstructing the recent semantic-calibration work.

This file is not a controlling specification. Higher-authority product/domain/source/architecture, roadmap, implementation, Phase-1, focused acceptance, and TODO documents win on conflict.

## 1. Product / architecture identity

JobHunter is a local-first personal career-intelligence application.

```text
MARKET
→ ROLE / CAPABILITY INTELLIGENCE
→ REVIEWED PERSONAL EVIDENCE
→ GAPS / CONSTRAINTS
→ LEARN / PRACTISE / BUILD / VERIFY
→ APPLICATION DECISION
→ OUTCOME
→ UPDATED EVIDENCE AND DECISIONS
↺
```

Architecture remains a local Python modular monolith with SQLite structured state, immutable evidence, FastAPI/Uvicorn/Jinja browser UI, shared CLI services, and local-first LM Studio. Do not introduce Node/npm/React, vector/RAG, graph DB, generic plugin frameworks, or agent orchestration without demonstrated need.

## 2. Current contracts

```text
parser:                       jobinja-detail-v2
translation:                  lm-studio-translation-v2
English projection:           english-projection-v2

English P1.6:                 job-analysis-english-v9
Original P1.6:                job-analysis-original-v9
P1.6 schema:                  job-analysis-v4

Capability accepted baseline: job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4

Blueprint candidate:          role-capability-blueprint-v3
Blueprint schema:             role-capability-blueprint-v2

Review Snapshot:              job-review-snapshot-v1
```

Controlled model roles:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-e2b-it
```

## 3. Fixed `tG9K` upstream chain

```text
English projection artifact 33
→ accepted English P1.6 artifact 29
→ accepted Capability v7 artifact 9
```

Do not rerun P1.6 or Capability merely to test Blueprint.

Artifact 29 is B2/SQ-1 accepted:

- 27 requirements;
- 7 responsibilities;
- complete deterministic coverage accounting;
- optionality preserved;
- Python-specific `expert` depth preserved;
- education and 3–6 years experience present.

Artifact 9 is B3/SQ-2 accepted for the bounded rich `tG9K` gate:

- 25/25 capability-relevant requirements linked;
- 7/7 responsibilities linked;
- two coherent capability profiles;
- all 27 requirements preserved in deterministic source truth;
- all six explicit depth facts preserved;
- requirements 25/26 remain role-level;
- no positive independence expectation;
- no cross-capability synthesis.

The CLI showing five of six explicit depths inside profiles is intentional: requirement 26 (`Professional experience — three to six years`) is role-level and must not be forced into a capability profile.

B3 decision:

```text
docs/experiments/2026-08-11_CAPABILITY_V7_B3_ACCEPTANCE.md
```

## 4. Capability history relevant to later review

- v4/v2 artifact 7: rejected; depth omitted, contextual stack/cloud strengthened, ownership overreach, evidence leakage.
- v5: historical failed output-budget experiment; do not reuse identity.
- v6/v3 artifact 8: rejected; deterministic reconciliation worked only for model-selected links, but model linked too little and repeated autonomy/ownership/optionality failures.
- v7/v4 artifact 9: accepted bounded B3 baseline. Freeze unless downstream or heterogeneous evidence exposes a repeatable correctness problem.

## 5. Current B4 Blueprint v3 design

Blueprint remains the human-facing professional interpretation layer. v3 adds a stronger deterministic/model boundary without turning it into another factual extraction layer.

### Capability grounding

Every Blueprint capability area carries `source_capability_indices`. The union of all areas must cover every accepted Capability profile.

For current `tG9K`, accepted Capability indices are:

```text
0  Advanced ML/Statistical Modeling for Industrial Data
1  Full-Stack ML Engineering & MLOps
```

The Blueprint may reorganize/explain those areas, but it cannot silently ignore one or add a generic ungrounded curriculum area.

### Source-named tools

A `source_named` tool must link accepted P1.6 requirement/responsibility indices.

JobHunter deterministically derives:

```text
source_requirement_strength
source_depth_signals
```

This prevents Python `expert` from spreading to PyTorch/TensorFlow/XGBoost/etc. and prevents contextual/preferred tools from silently becoming mandatory.

`likely_example` / `possible_example` tools have no P1.6 source links, source strength, or source depth.

### Role-level constraints

JobHunter deterministically copies Capability source-truth role-level requirements into Blueprint.

Expected `tG9K` constraints:

```text
25  Master's degree                         required
26  Professional experience                required; three to six years
```

### Hidden requirements

A `highly_likely` hidden requirement must link accepted Capability work and/or responsibilities. It is still interpretation, not employer fact.

### Scenario basis

Every scenario declares:

```text
source_stated_workflow
professional_example
```

A practitioner-created `professional_example` cannot be `highly_likely`. Unstated topology, latency, vendor, batch/stream mode, cloud/edge placement, scale, or ownership assumptions must remain explicit. A highly-likely scenario cannot depend on unresolved assumptions.

## 6. Current implementation files

```text
src/jobhunter/role_blueprint_models.py
src/jobhunter/role_blueprint_service.py
src/jobhunter/role_blueprint_service_v3.py
src/jobhunter/role_blueprint_inference.py
scripts/audit_blueprint_v3_snapshot.py
```

Regression coverage includes:

```text
tests/test_role_blueprint_models.py
tests/test_role_blueprint_service.py
tests/test_role_blueprint_inference.py
tests/test_role_blueprint_evidence_shape.py
```

B4 experiment:

```text
docs/experiments/2026-08-11_BLUEPRINT_V3_GROUNDED_INTERPRETATION.md
```

## 7. Exact next action

Keep accepted upstream artifacts and model roles fixed.

Run locally:

```bash
jobhunter jobs blueprint tG9K
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v3_snapshot.py
```

Do not run:

```text
Analyze English / P1.6 again
Capability again
full jobhunter run
```

for this controlled B4 test.

If Blueprint generation fails, preserve the failed attempt and inspect the exact validation/output/model error. Do not fabricate or commit an empty snapshot.

If generation succeeds, the mechanical audit must confirm:

- English analysis artifact 29;
- Capability artifact 9 / v7/v4 current chain;
- Blueprint v3/v2 depends on Capability 9;
- all accepted Capability profiles are covered;
- source-named tools have valid P1.6 links and deterministic strength/depth;
- inferred tools carry no source strength/depth;
- role-level constraints match source truth;
- professional-example scenarios are not highly likely;
- source-stated workflows link accepted responsibilities;
- highly-likely scenarios have no unresolved assumptions.

A mechanical pass is necessary but not sufficient.

## 8. Semantic review after the live push

Review whether:

- the Blueprint adds useful practitioner interpretation rather than paraphrasing P1.6/Capability;
- capability-area organization is coherent;
- Python alone carries explicit expert depth unless another tool has independent depth evidence;
- contextual/preferred frameworks, cloud/edge, MATLAB, and C/C++ remain calibrated;
- a technology list is not assembled into a hidden company architecture;
- professional-example workflows are technically coherent and visibly hypothetical;
- source-stated/high-confidence workflows do not contradict unresolved unknowns;
- hidden requirements are useful and grounded rather than generic curriculum;
- tools/protocols/platforms retain normal technical meaning;
- important unknowns preserve real architecture/operational uncertainty;
- the model does not amplify broad Capability wording into ownership/autonomy claims.

### Decision after review

If B4 passes:
1. mark B4/SQ-3 accepted for the bounded `tG9K` gate;
2. freeze Blueprint v3/v2 for the next heterogeneous review tranche;
3. continue B5/CI-3 with sparse, Python/software, network/security, and operations/platform roles.

If B4 is mechanically correct but E2B remains semantically weak:
1. keep source/P1.6/Capability/prompt/schema/rubric fixed;
2. compare one stronger Blueprint reasoning model;
3. compare correctness/calibration rather than eloquence;
4. do not build multi-model voting.

If B4 exposes a repeatable deterministic defect, fix the correct layer and rerun the same bounded case before heterogeneous expansion.

## 9. Phase sequence after B4

```text
B5/CI-3 heterogeneous review
→ Market truthfulness
→ source/lifecycle acceptance
→ partial-success semantics
→ P1.7 final report/run/browser acceptance
→ Phase-1 closure
→ only then corpus-wide Phase 2
```
