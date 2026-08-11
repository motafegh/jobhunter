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

Blueprint candidate:          role-capability-blueprint-v4
Blueprint schema:             role-capability-blueprint-v3

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

## 4. Blueprint v3 failure and decision

Blueprint v3/v2 asked the model to reproduce several numeric provenance namespaces and then reconciled source strength/depth deterministically.

Controlled live evidence:

- E2B completed generation but failed provenance validation, confused P1.6 requirement indices with Capability-profile indices, and overreached semantically.
- The first E4B attempt failed only because the LM Studio instance was loaded at 4,096 context for a ~9,521-token prompt. Automatic 16,384 context preparation was then implemented and verified.
- E4B subsequently completed both the initial generation and Instructor repair attempt, but still failed the v3 contract.
- E4B correctly reasoned that source tools mapped to requirements such as 10, 6, 14, 18 and 15/16, but wrote those IDs into `source_depth_signals` instead of `source_requirement_indices`.
- E4B also repeated the Capability/P1.6 namespace confusion and retained streaming/cloud/edge/MLOps architecture overreach.

Decision:

```text
Blueprint v3/v2 fails B4.
Do not weaken validators.
Do not add prompt patches.
Do not model-shop to 12B to compensate for deterministic bookkeeping.
```

Historical record:

```text
docs/experiments/2026-08-11_BLUEPRINT_V3_GROUNDED_INTERPRETATION.md
```

## 5. Current Blueprint v4 design

Architectural rule:

> **The model reasons; JobHunter owns provenance bookkeeping.**

Current v4 boundary:

```text
accepted P1.6 + accepted Capability v7
→ JobHunter builds compact ordered capability inputs
→ model emits semantic interpretation only
→ JobHunter deterministically attaches all upstream provenance/source anchors
→ Blueprint v4/v3 artifact
```

### Model-facing draft

The LLM does **not** emit:

```text
Capability indices
P1.6 requirement indices
P1.6 responsibility indices
source strength
source depth
role constraints
scenario basis
```

It returns exactly one `capability_interpretations` item per accepted Capability profile, in source order. It cannot regroup, merge, split, or rename accepted Capability profiles.

### Deterministic persisted source anchors

Each persisted Blueprint area receives:

```text
source_capability_index
source_requirements[]
source_responsibilities[]
```

Source requirements preserve exact:

```text
requirement_index
concept
concept_type
requirement_type
depth_signal
evidence
```

Role-level degree/experience constraints are injected from Capability `source_truth`.

### Suggested tools

Employer/source-named technologies remain visible through deterministic source requirements. The model only creates:

```text
suggested_tools_or_examples
```

with `likely_example` or `possible_example`. Suggested tools carry no source provenance and cannot be mandatory/required/necessary or inherit expert/mastery depth.

### Hidden requirements and workflow examples

Model-created hidden requirements are only `plausible` or `speculative`.

Model-created workflows are stored as:

```text
professional_example_scenarios
```

They are only `plausible` or `speculative`, and JobHunter injects `scenario_basis = professional_example` deterministically. Unstated topology/latency/vendor/batch-stream/cloud-edge/scale/ownership/orchestration/feedback-loop choices belong in explicit assumptions.

Current design record:

```text
docs/experiments/2026-08-11_BLUEPRINT_V4_DETERMINISTIC_PROVENANCE_BOUNDARY.md
```

## 6. Current implementation files

Active v4:

```text
src/jobhunter/role_blueprint_service.py          # public shim → v4
src/jobhunter/role_blueprint_service_v4.py
src/jobhunter/role_blueprint_inference_v4.py
src/jobhunter/role_blueprint_v4_models.py
src/jobhunter/inference/lm_studio_runtime.py
scripts/audit_blueprint_v4_snapshot.py
```

Historical v3 remains preserved:

```text
src/jobhunter/role_blueprint_service_v3.py
src/jobhunter/role_blueprint_inference.py
src/jobhunter/role_blueprint_models.py
scripts/audit_blueprint_v3_snapshot.py
```

V4 regression coverage includes:

```text
tests/test_role_blueprint_v4_models.py
tests/test_role_blueprint_inference_v4.py
tests/test_role_blueprint_service_v4.py
tests/test_role_blueprint_service.py
tests/test_lm_studio_runtime.py
```

The browser template now shows deterministic employer/source anchors separately from practitioner-created examples and labels model-created workflows as professional examples rather than employer architecture.

## 7. Exact next live action

First sync and confirm the active contract:

```bash
git pull --ff-only origin main
python -c "from jobhunter.role_blueprint_service import BLUEPRINT_PROMPT_VERSION, BLUEPRINT_SCHEMA_VERSION; print(BLUEPRINT_PROMPT_VERSION); print(BLUEPRINT_SCHEMA_VERSION)"
```

Expected:

```text
role-capability-blueprint-v4
role-capability-blueprint-v3
```

Then run **only**:

```bash
jobhunter jobs blueprint tG9K
```

Do not run:

```text
translation again
Analyze English / P1.6 again
Capability again
full jobhunter run
```

If Blueprint generation fails, preserve the failed attempt and inspect the exact validation/output/model error. Do not fabricate or commit an empty snapshot.

If generation succeeds:

```bash
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v4_snapshot.py
```

The mechanical audit must confirm:

- English analysis artifact 29;
- Capability artifact 9 / v7/v4 current chain;
- Blueprint v4/v3 depends on Capability 9 and P1.6 29;
- exactly one Blueprint area per accepted Capability profile, in the same order and with the exact accepted label;
- deterministic source requirements exactly match each Capability profile's P1.6 links, including strength/depth/evidence;
- deterministic source responsibilities exactly match the accepted links;
- role-level constraints match source truth;
- suggested tools contain no legacy source provenance fields;
- hidden requirements are only plausible/speculative;
- professional example scenarios are only plausible/speculative and carry deterministic `professional_example` basis;
- legacy v3 provenance/scenario fields are absent.

A mechanical pass is necessary but not sufficient.

## 8. Semantic B4 review after a valid v4 artifact

Review whether:

- the Blueprint adds useful practitioner interpretation rather than paraphrasing P1.6/Capability;
- role shape is calibrated and does not inflate the vacancy into a broader MLOps/platform identity;
- Python alone carries explicit expert source depth unless another concept has independent depth evidence;
- contextual/preferred frameworks, cloud/edge, MATLAB, and C/C++ remain calibrated;
- a technology list is not assembled into a hidden company architecture;
- Spark/Kafka, databases, Airflow/Prefect, MLflow/Docker and cloud/edge remain separate source facts unless an illustrative scenario clearly labels assumptions;
- professional examples are technically coherent and visibly hypothetical;
- real-time, microservices, CI/CD, model registry, regulatory constraints and control loops are not asserted without support;
- hidden requirements are role-specific and useful, not generic curriculum;
- important unknowns preserve real architecture/operational uncertainty;
- tools/protocols/platforms retain normal technical meaning;
- the model does not amplify broad Capability wording into ownership/autonomy claims.

If B4 passes:
1. mark B4/SQ-3 accepted for the bounded `tG9K` gate;
2. freeze Blueprint v4/v3 for the next heterogeneous review tranche;
3. continue B5/CI-3 with sparse, Python/software, network/security, and operations/platform roles.

If v4 still fails semantically, diagnose the failure at the correct layer. Do not immediately change upstream artifacts, model, prompt, and schema together.

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
