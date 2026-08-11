# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-11  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** B4 / SQ-3 Role Capability Blueprint  
**Purpose:** Resume from the real current repository state without reconstructing recent semantic-calibration work.

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

## 2. Current contracts and model roles

```text
parser:                       jobinja-detail-v2
translation:                  lm-studio-translation-v2
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

Controlled model roles:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-e4b-it-ud
```

Blueprint runtime automatically prepares the selected LM Studio model at a 16,384-token context window. Manual LM Studio context reconfiguration is not required.

## 3. Fixed `tG9K` upstream chain

```text
English projection artifact 33
→ accepted English P1.6 artifact 29
→ accepted Capability v7 artifact 9
```

Do not rerun translation, P1.6, or Capability merely to test Blueprint.

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
- two accepted Capability profiles;
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

## 4. Blueprint failure history

### v3/v2 — structural + semantic failure

Both E2B and E4B confused P1.6 requirement IDs with Capability-profile IDs. E4B's repair also placed requirement IDs into the depth field. Both retained streaming/cloud/edge/MLOps architecture overreach.

Decision:

```text
Blueprint v3/v2 fails B4.
Do not weaken validators.
Do not add model-specific prompt patches.
```

Record:

```text
docs/experiments/2026-08-11_BLUEPRINT_V3_GROUNDED_INTERPRETATION.md
```

### v4/v3 — provenance success + semantic failure

v4 moved provenance fully into JobHunter. The live E4B `tG9K` generation completed and the mechanical audit passed:

```text
Capability areas:                       2
Deterministic source requirements:      25
Deterministic source responsibilities:   7
Role-level constraints:                  2
Suggested tools:                         0
Hidden requirements:                     0
Professional scenarios:                  0
```

That result proved the deterministic provenance architecture works.

B4 still failed semantically. The generated prose claimed or strongly implied:

- real-time APC/process adjustment;
- low-latency active control loops;
- a factory-floor/MES-SECS-to-model topology;
- process physics as a candidate obligation;
- a specific code/training-slice/hyperparameter audit trail;
- strong edge importance because decisions occur near equipment;
- ownership of the entire lifecycle.

Those are not established by accepted P1.6.

Root cause:

1. v4 passed Capability artifact 9's **derived prose** downstream (`summary`, `sub_capabilities`, `underlying_knowledge`, operational reasoning, etc.);
2. v4 still exposed broad free-text Blueprint surfaces where professional knowledge could become employer-specific certainty.

Record:

```text
docs/experiments/2026-08-11_BLUEPRINT_V4_DETERMINISTIC_PROVENANCE_BOUNDARY.md
docs/experiments/2026-08-11_BLUEPRINT_V4_SEMANTIC_FAILURE_AND_V5_BOUNDARY.md
```

## 5. Current Blueprint v5 design

Two rules now govern Blueprint:

> **JobHunter owns provenance.**

> **Everything the Blueprint model creates is professional inference, not employer truth.**

### Model input

v5 receives only:

```text
selected neutral role context
source role purpose
role-level source constraints
accepted Capability label
exact linked P1.6 requirement facts
exact linked P1.6 responsibility statements
```

v5 does **not** receive:

```text
Capability summary
Capability sub-capabilities
Capability underlying knowledge
Capability operational reasoning
long source description
company-description prose
```

Accepted Capability grouping is reused; Capability-derived interpretation is not automatically treated as authoritative downstream context.

### Model output

`RoleBlueprintDraft` contains only:

```text
capability_interpretations[]
overall_unknowns[]
```

Each Capability interpretation contains:

```text
practical_interpretation
interpretation_uncertainty
professional_considerations[]
probably_not_required[]
important_unknowns[]
```

Every main interpretation is persisted with fixed strength:

```text
plausible
```

Every main interpretation must carry an `interpretation_uncertainty` sentence stating what the vacancy does not establish or what remains inferred.

Professional considerations may only be:

```text
plausible
speculative
```

and every consideration requires its own uncertainty sentence.

Generic validation rejects unqualified obligation/full-ownership wording such as `must`, `required`, `expected to`, `responsible for`, or owning the entire/full/end-to-end lifecycle/stack/pipeline/system.

Cautious negative scope such as `probably not required` is allowed.

### High-risk fields removed from B4

v5 has no model-generated:

```text
role_read
likely_role_shape
likely_depth
hidden requirements
tool recommendations
work-product list
scenario/topology generation
bottom_line
```

Source role purpose, requirements, responsibilities, obligation strength, explicit depth, evidence and role-level constraints remain visible as deterministic anchors.

## 6. Current implementation files

Active v5:

```text
src/jobhunter/role_blueprint_service.py          # public shim → v5
src/jobhunter/role_blueprint_service_v5.py
src/jobhunter/role_blueprint_inference_v5.py
src/jobhunter/role_blueprint_v5_models.py
src/jobhunter/inference/lm_studio_runtime.py
scripts/audit_blueprint_v5_snapshot.py
```

Historical v3/v4 remain preserved for negative evidence/regression reference.

V5 regression coverage includes:

```text
tests/test_role_blueprint_v5_models.py
tests/test_role_blueprint_inference_v5.py
tests/test_role_blueprint_service_v5.py
tests/test_role_blueprint_service.py
tests/test_role_blueprint_web.py
```

The CLI and browser explicitly place an interpretation boundary next to model prose and visually separate source truth from professional inference.

Standalone v5 model/service/inference coverage passed Ruff, full pytest and warnings-as-errors before activation. Final-main CI must also be green after all active-runtime/docs/UI changes.

## 7. Exact next live action

Sync and confirm the active contract:

```bash
git pull --ff-only origin main
python -c "from jobhunter.role_blueprint_service import BLUEPRINT_PROMPT_VERSION, BLUEPRINT_SCHEMA_VERSION; print(BLUEPRINT_PROMPT_VERSION); print(BLUEPRINT_SCHEMA_VERSION)"
```

Expected:

```text
role-capability-blueprint-v5
role-capability-blueprint-v4
```

Then run **only**:

```bash
jobhunter jobs blueprint tG9K
```

Do not run translation, P1.6, Capability, or full `jobhunter run` for this controlled B4 test.

If generation succeeds:

```bash
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v5_snapshot.py
```

Do not commit the locally generated v4 snapshot. The local snapshot should be replaced by the v5 candidate only after successful v5 generation.

## 8. Semantic B4 review for v5

Mechanical pass is necessary but insufficient. Review whether:

- source role purpose/constraints/requirements/responsibilities remain exact;
- every model interpretation is visibly plausible professional inference;
- every interpretation has a meaningful uncertainty boundary, not boilerplate;
- no model prose becomes an employer obligation/full-lifecycle ownership claim;
- Python `expert` does not spread to frameworks;
- contextual/preferred frameworks/cloud/edge/MATLAB/C++ remain calibrated;
- technology lists are not assembled into one company architecture;
- real-time/low-latency/factory-floor/active-control-loop claims are not asserted as employer facts;
- process/equipment physics is not turned into a candidate requirement unless source-stated;
- governance implementation details remain examples/inference rather than source truth;
- professional considerations add role-specific value rather than generic curriculum;
- per-area and whole-role unknowns preserve unresolved topology, latency, deployment, ownership and exact tool-use questions.

If B4 passes:
1. mark B4/SQ-3 accepted for bounded `tG9K`;
2. freeze v5/v4 for heterogeneous review;
3. proceed to B5/CI-3.

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
