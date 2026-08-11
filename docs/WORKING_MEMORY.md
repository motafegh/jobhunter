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

Blueprint candidate:          role-capability-blueprint-v6
Blueprint schema:             role-capability-blueprint-v5

Review Snapshot:              job-review-snapshot-v1
```

Controlled model roles:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-e4b-it-ud
```

Blueprint runtime automatically prepares the selected LM Studio model at a 16,384-token context window. V6 caps the smaller structured completion at 4,096 tokens. Manual LM Studio context reconfiguration is not required.

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

### v4/v3 — provenance success + semantic failure

V4 moved provenance fully into JobHunter. The live E4B `tG9K` generation completed and the mechanical audit passed: 2 Capability areas, 25 deterministic source requirements, 7 deterministic source responsibilities and 2 role-level constraints.

That proved the deterministic provenance architecture works. B4 still failed because generated prose claimed or strongly implied real-time/low-latency control, factory-floor/data-path topology, process physics, stronger edge placement, specific governance implementation and entire-lifecycle ownership.

Root cause:

1. v4 passed Capability artifact 9's model-derived explanatory prose downstream;
2. v4 still exposed broad free-text Blueprint expansion surfaces.

### v5/v4 — narrower input, remaining summary failure

V5 stopped sending Capability-derived prose downstream and removed role shape, hidden requirements, tool suggestions, work products, scenarios and bottom-line generation.

Live `tG9K` v5 artifact **6** was a valid current-chain artifact and was committed in review snapshot commit `ffa690361e5cbbb755fff7bcd587d6903d5dce89`. CI passed.

B4 still failed semantically. Area 2's remaining free-form `practical_interpretation` said the function centered on end-to-end ML infrastructure, high-volume telemetry streams, automated model-training workflows and deployment-lifecycle management, while its own uncertainty admitted the system-ownership boundary was unknown.

Conclusion:

```text
Blueprint v5/v4 fails B4.
The remaining free-form positive role-summary surface is the defect.
Do not patch individual semiconductor/MLOps phrases.
```

Records:

```text
docs/experiments/2026-08-11_BLUEPRINT_V3_GROUNDED_INTERPRETATION.md
docs/experiments/2026-08-11_BLUEPRINT_V4_DETERMINISTIC_PROVENANCE_BOUNDARY.md
docs/experiments/2026-08-11_BLUEPRINT_V4_SEMANTIC_FAILURE_AND_V5_BOUNDARY.md
docs/experiments/2026-08-11_BLUEPRINT_V5_SEMANTIC_FAILURE_AND_V6_BOUNDARY.md
```

## 5. Current Blueprint v6 design

Permanent rules:

> **JobHunter owns provenance.**

> **Everything the Blueprint model creates is professional inference, not employer truth.**

> **There is no free-form positive role-summary surface in v6.**

### Model input

V6 receives only:

```text
selected neutral role context
source role purpose
role-level source constraints
accepted Capability label
exact linked P1.6 requirement facts
exact linked P1.6 responsibility statements
```

It does **not** receive Capability summaries/sub-capabilities/underlying knowledge/operational reasoning, the long source description, or company-description prose.

### Model output

The v6 `RoleBlueprintDraft` contains only:

```text
capability_interpretations[]
  professional_considerations[]
    statement
    interpretation_strength = plausible | speculative
    uncertainty
  important_unknowns[]  # at least one

overall_unknowns[]
```

No model-generated:

```text
practical_interpretation
interpretation_uncertainty
area-level interpretation_strength
probably_not_required
role_read
likely_role_shape
likely_depth
hidden requirements
tool recommendations
work-product lists
scenario/topology generation
bottom_line
source provenance IDs
```

Every positive model-created statement therefore carries uncertainty by construction. Every Capability must contain at least one important unknown.

Generic validation rejects employer-obligation wording and full/end-to-end lifecycle/stack/pipeline/system/infrastructure scope.

The prompt explicitly blocks inference shortcuts:

```text
high-volume data → streaming
process control → real-time control
anomaly detection → low latency
APC/SPC → automated feedback loop
cloud/edge names → deployment placement
deployment/governance → lifecycle ownership
```

Unknowns may not smuggle those assumptions in indirectly.

### Deterministic persisted source anchors

JobHunter still attaches exact:

```text
source role purpose
source role constraints
Capability identity/index/coverage
source requirements
source responsibilities
requirement strength
explicit depth
evidence
```

The accepted P1.6 and Capability chain remains authoritative.

## 6. Current implementation files

Active v6:

```text
src/jobhunter/role_blueprint_service.py          # public shim → v6
src/jobhunter/role_blueprint_service_v6.py
src/jobhunter/role_blueprint_inference_v6.py
src/jobhunter/role_blueprint_v6_models.py
src/jobhunter/inference/lm_studio_runtime.py
scripts/audit_blueprint_v6_snapshot.py
```

Historical v3/v4/v5 implementations remain preserved for negative evidence/regression reference.

V6 regression coverage includes:

```text
tests/test_role_blueprint_v6_models.py
tests/test_role_blueprint_inference_v6.py
tests/test_role_blueprint_service_v6.py
tests/test_role_blueprint_service.py
tests/test_role_blueprint_web.py
```

The CLI/browser surface shows deterministic source anchors first and only explicitly uncertain professional considerations/unknowns after them.

The isolated v6 model/service/inference boundary passed Ruff, full pytest and warnings-as-errors before public activation. Final-main CI must be green after all current-runtime/docs/UI changes.

`*.egg-info/` is now ignored so editable installs do not dirty normal Git status. Existing local generated metadata may be deleted safely.

## 7. Exact next live action

Sync, clean generated metadata if present, and confirm the active contract:

```bash
git pull --ff-only origin main
rm -rf src/jobhunter_local.egg-info
python -c "from jobhunter.role_blueprint_service import BLUEPRINT_PROMPT_VERSION, BLUEPRINT_SCHEMA_VERSION; print(BLUEPRINT_PROMPT_VERSION); print(BLUEPRINT_SCHEMA_VERSION)"
```

Expected:

```text
role-capability-blueprint-v6
role-capability-blueprint-v5
```

Then run **only**:

```bash
jobhunter jobs blueprint tG9K
```

Do not run translation, P1.6, Capability, or full `jobhunter run` for this controlled B4 test.

If generation succeeds:

```bash
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v6_snapshot.py
```

The current committed snapshot contains rejected v5 artifact 6 as review evidence. Replace it only with the newly generated v6 candidate.

## 8. Semantic B4 review for v6

Mechanical pass is necessary but insufficient. Review whether:

- source role purpose/constraints/requirements/responsibilities remain exact;
- each professional consideration adds real practitioner value rather than simply rewriting source facts;
- every positive consideration is visibly plausible/speculative and has a meaningful uncertainty sentence;
- every Capability exposes at least one real unresolved unknown;
- unknown wording does not assume a stream, feedback loop, cloud/edge placement, topology, ownership model or other unstated system;
- Python `expert` does not spread to frameworks;
- contextual/preferred frameworks/cloud/edge/MATLAB/C++ remain calibrated;
- technology lists are not assembled into one employer architecture;
- streaming/real-time/low-latency/factory-floor/active-control-loop/full-lifecycle claims do not return without source support;
- the layer remains useful enough to justify Blueprint above P1.6 + Capability.

If B4 passes:
1. mark B4/SQ-3 accepted for bounded `tG9K`;
2. freeze v6/v5 for heterogeneous review;
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
