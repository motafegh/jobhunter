# JobHunter Role Capability Blueprint Plan

**Status:** Blueprint v6/v5 implemented as active B4 candidate; live semantic acceptance open  
**Date:** 2026-08-11  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, the active Phase-1 gate, and `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`  
**Scope:** Human-facing professional context above accepted P1.6 and Capability Intelligence. No corpus-wide automatic generation is authorized yet.

## 1. Purpose

JobHunter separates three semantic jobs:

```text
P1.6
→ strict factual extraction / evidence boundary

Capability Intelligence
→ auditable grouping/reasoning above P1.6

Role Capability Blueprint
→ human-facing professional context
```

Blueprint should add useful practitioner context beyond rereading the vacancy while keeping these unmistakably separate:

```text
employer/source truth
professional inference
```

## 2. Current contract

Active B4 candidate:

```text
prompt/runtime: role-capability-blueprint-v6
schema:         role-capability-blueprint-v5
```

Persistence identity remains:

```text
job detail version
+ exact English projection artifact
+ exact English P1.6 artifact
+ exact Capability Intelligence artifact
+ exact Blueprint model
+ Blueprint prompt version
+ Blueprint schema version
```

Historical identities remain immutable evidence:

- v3/v2 failed structural provenance and semantic calibration;
- v4/v3 passed deterministic provenance but failed live B4 semantic calibration;
- v5/v4 removed Capability-derived prose but its remaining free-form positive summary still inflated role scope;
- do not reuse those identities for material redesigns.

## 3. Authority

```text
source
→ English projection
→ accepted P1.6 facts
→ accepted Capability grouping/source truth
→ Blueprint professional context
```

No downstream layer overwrites upstream truth.

Mechanical linkage is not semantic certification. V4 proved a Blueprint can preserve every source index correctly and still invent certainty. V5 proved that even after removing most expansion surfaces, a single free-form positive interpretation paragraph can still amplify scope beyond the source.

## 4. Historical failure lessons

### V4

Live v4 `tG9K` mechanically passed but generated real-time/low-latency control, employer topology, process-physics obligation, edge placement, governance implementation and end-to-end lifecycle claims stronger than accepted P1.6.

Root cause included feeding Capability-derived explanatory prose downstream and broad model-owned Blueprint surfaces.

### V5

V5 corrected those two issues substantially but retained `practical_interpretation`.

Live artifact 6 still described Area 2 as end-to-end infrastructure work, assumed telemetry streams, introduced automated training workflows and deployment-lifecycle scope, while its uncertainty admitted ownership boundaries were unknown.

Decision:

> **Remove the free-form positive role-summary surface rather than trying to prompt it into calibration.**

Records:

```text
docs/experiments/2026-08-11_BLUEPRINT_V4_SEMANTIC_FAILURE_AND_V5_BOUNDARY.md
docs/experiments/2026-08-11_BLUEPRINT_V5_SEMANTIC_FAILURE_AND_V6_BOUNDARY.md
```

## 5. V6 governing rules

Permanent rules:

> **JobHunter owns provenance bookkeeping.**

> **Everything the Blueprint model creates is professional inference, not employer truth.**

> **Every positive model-generated statement must carry uncertainty by construction.**

## 6. Model input boundary

V6 sends only:

```text
selected neutral role context
source-stated role purpose
role-level source constraints
accepted Capability labels
exact P1.6 requirements linked to each Capability
exact P1.6 responsibilities linked to each Capability
```

V6 intentionally does **not** send:

```text
Capability summary
Capability sub-capabilities
Capability underlying knowledge
Capability operational practices/context
other Capability-derived explanatory prose
long vacancy description duplicated after P1.6
company-description prose
```

Capability v7 grouping/source truth is accepted; model-derived Capability prose is not automatically authoritative downstream input.

## 7. Capability-order contract

The model returns exactly one `capability_interpretations` item per accepted Capability profile, in the same order.

It cannot:

- create a new Capability area;
- merge profiles;
- split profiles;
- rename authoritative Capability labels;
- emit provenance indices.

JobHunter constructs persisted areas with authoritative `name`, `source_capability_index`, and complete `source_capability_coverage`.

## 8. Deterministic source anchors

JobHunter copies accepted source truth into the final Blueprint.

### Role purpose

```text
source_role_purpose[]
  statement
  evidence
```

### Capability requirements

```text
source_requirements[]
  requirement_index
  concept
  concept_type
  requirement_type
  depth_signal
  evidence
```

### Capability responsibilities

```text
source_responsibilities[]
  responsibility_index
  statement
  evidence
```

### Role-level constraints

```text
source_role_constraints[]
  requirement_index
  concept
  requirement_type
  depth_signal
  evidence
```

For current `tG9K`, expected role constraints remain Master's degree and three-to-six-years professional experience.

## 9. Model-owned v6 contract

The model-facing draft contains only:

```text
capability_interpretations[]
  professional_considerations[]
    statement
    interpretation_strength: plausible | speculative
    uncertainty
  important_unknowns[]

overall_unknowns[]
```

Every Capability requires at least one important unknown.

The model does **not** generate:

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
failure-mode lists
end-to-end scenarios
runtime topology
bottom_line
```

### Professional considerations

A consideration exists only when it adds real practitioner value and always includes:

```text
statement
interpretation_strength = plausible | speculative
uncertainty
```

No generated positive statement is allowed to stand alone as an unlabeled role-level conclusion.

## 10. Generic language guard

Model-created consideration text is rejected when it uses unqualified employer-obligation wording or full-scope claims such as:

```text
mandatory
required
must
necessary
expected to
responsible for
full/end-to-end lifecycle
full/end-to-end stack
full/end-to-end pipeline
full/end-to-end system
full/end-to-end infrastructure
```

The guard is deliberately generic. Do not turn it into a semiconductor-specific blacklist.

## 11. Semantic inference guards

### Technology list != architecture

A list containing Spark, Kafka, Airflow/Prefect, MLflow, Docker, cloud platforms, databases, MES/SECS-GEM or ML frameworks does not establish one deployed system or data path.

### High-volume != streaming

High-volume/high-dimensional data does not establish streaming rather than batch or mixed operation.

### Process control != real-time proof

Process control, anomaly detection or APC/SPC terminology do not by themselves establish real-time inference, low-latency control, or an automated feedback loop.

### Cloud/edge names != placement

Cloud platform names and preferred industrial/edge experience do not prove where this employer deploys models.

### Deployment/governance != lifecycle ownership

Model deployment, traceability, reproducibility and governance do not prove one person owns the full ML/MLOps lifecycle.

### Unknowns cannot smuggle assumptions

When a system is not source-established, write:

```text
whether any automated feedback loop exists is unknown
```

not:

```text
the feedback-loop latency is unknown
```

### Optionality/depth remain exact

- contextual stays contextual;
- preferred stays preferred;
- Python `expert` applies only to Python;
- explicit depth does not spread to neighboring tools.

## 12. Persisted artifact shape

Persisted `RoleCapabilityBlueprint` contains:

```text
source_role_purpose[]
source_capability_coverage[]
source_role_constraints[]
capability_areas[]
overall_unknowns[]
```

Each area contains:

```text
name
source_capability_index
source_requirements[]
source_responsibilities[]
professional_considerations[]
important_unknowns[]
```

The browser and CLI visibly distinguish deterministic source anchors from professional considerations and their uncertainty.

## 13. Runtime / performance boundary

Blueprint runtime automatically prepares the selected LM Studio instance at a 16,384-token context window.

Because v6 has a much smaller output contract, its completion budget is capped at:

```text
4,096 tokens
```

This is intentionally lower than the general analysis maximum and avoids unnecessary generation cost while leaving ample structured-output headroom.

## 14. Current implementation

Active:

```text
src/jobhunter/role_blueprint_service.py
src/jobhunter/role_blueprint_service_v6.py
src/jobhunter/role_blueprint_inference_v6.py
src/jobhunter/role_blueprint_v6_models.py
src/jobhunter/inference/lm_studio_runtime.py
scripts/audit_blueprint_v6_snapshot.py
```

Regression coverage:

```text
tests/test_role_blueprint_v6_models.py
tests/test_role_blueprint_inference_v6.py
tests/test_role_blueprint_service_v6.py
tests/test_role_blueprint_service.py
tests/test_role_blueprint_web.py
```

Historical v3/v4/v5 implementation remains preserved for negative evidence and regression reference.

## 15. Current live B4 gate

Fixed chain:

```text
English projection artifact 33
English P1.6 artifact 29
Capability v7 artifact 9
Blueprint model gemma-4-e4b-it-ud
```

Confirm:

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

Do not rerun translation, P1.6 or Capability merely to test Blueprint.

If generation succeeds:

```bash
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v6_snapshot.py
```

## 16. B4 acceptance criteria

Mechanical acceptance requires:

- exact dependency identity;
- exact Capability one-to-one mapping and coverage;
- exact role purpose/requirements/responsibilities/role constraints;
- source strength/depth/evidence preservation;
- absence of v5 free-form area-summary fields;
- at least one important unknown per Capability;
- professional considerations only plausible/speculative with non-empty uncertainty;
- no mechanically detectable employer-obligation/full-scope wording;
- absence of older expansion fields.

Semantic acceptance additionally requires:

1. considerations add materially useful professional context beyond rereading source anchors;
2. uncertainty is substantive rather than boilerplate;
3. no employer-specific topology/latency/ownership invention;
4. no streaming/real-time/low-latency/control-loop claim without source support;
5. no cloud/edge placement invention;
6. preserved contextual/preferred/depth semantics;
7. no technology-list-to-architecture synthesis;
8. unknowns do not presume unstated systems;
9. no generic curriculum dumping;
10. technical/domain correctness;
11. enough incremental value to justify retaining Blueprint above P1.6 + Capability.

A mechanical PASS does not accept B4.

## 17. Non-goals

Do not build yet:

- corpus-wide Blueprint generation;
- personal fit/readiness scoring;
- learning-plan generation;
- application ranking;
- model voting/ensembles;
- vector/RAG infrastructure;
- domain-specific prompt patch collections;
- automatic architecture generation presented as employer truth.
