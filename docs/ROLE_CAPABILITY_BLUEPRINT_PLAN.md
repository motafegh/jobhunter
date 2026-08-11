# JobHunter Role Capability Blueprint Plan

**Status:** Blueprint v5/v4 implemented as active B4 candidate; live semantic acceptance open  
**Date:** 2026-08-11  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, the active Phase-1 gate, and `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`  
**Scope:** Human-facing professional interpretation above accepted P1.6 and Capability Intelligence. No corpus-wide automatic generation is authorized yet.

## 1. Purpose

JobHunter separates three semantic jobs:

```text
P1.6
→ strict factual extraction / evidence boundary

Capability Intelligence
→ auditable grouping/reasoning above P1.6

Role Capability Blueprint
→ human-facing professional interpretation
```

The Blueprint should teach the user something useful beyond rereading the vacancy while keeping two categories unmistakably separate:

```text
employer/source truth
professional interpretation
```

## 2. Current contract

Active B4 candidate:

```text
prompt/runtime: role-capability-blueprint-v5
schema:         role-capability-blueprint-v4
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
- do not reuse those identities for material redesigns.

## 3. Authority

```text
source
→ English projection
→ accepted P1.6 facts
→ accepted Capability grouping/source truth
→ Blueprint professional interpretation
```

No downstream layer overwrites upstream truth.

Mechanical linkage is not semantic certification. The v4 live result proved that a Blueprint can preserve every source index correctly and still invent employer-specific certainty in generated prose.

## 4. Why v4 was rejected

The live v4 `tG9K` artifact passed its mechanical audit but generated claims stronger than accepted P1.6 supports, including:

- real-time APC/process adjustment;
- low-latency active control loops;
- factory-floor/MES-SECS data-path topology;
- process physics as a candidate obligation;
- a specific code/training-data/hyperparameter audit-trail implementation;
- strengthened edge importance;
- ownership of the entire lifecycle.

Root cause:

1. v4 passed Capability model-derived prose downstream, where aggressive `Full-Stack ML Engineering & MLOps` reasoning could be amplified;
2. v4 still exposed broad model-owned role-shape/depth/work-product/scenario/bottom-line surfaces.

Decision record:

```text
docs/experiments/2026-08-11_BLUEPRINT_V4_SEMANTIC_FAILURE_AND_V5_BOUNDARY.md
```

## 5. V5 governing rules

Two rules are permanent:

> **JobHunter owns provenance bookkeeping.**

> **Everything the Blueprint model creates is professional inference, not employer truth.**

## 6. Model input boundary

V5 sends the model only:

```text
selected neutral role context
source-stated role purpose
role-level source constraints
accepted Capability labels
exact P1.6 requirements linked to each Capability
exact P1.6 responsibilities linked to each Capability
```

V5 intentionally does **not** send:

```text
Capability summary
Capability sub-capabilities
Capability underlying knowledge
Capability operational practices/context
other Capability-derived explanatory prose
long vacancy description duplicated after P1.6
company-description prose
```

This distinction matters: Capability v7's **grouping/source-truth boundary** is B3 accepted, but model-derived Capability prose is not automatically authoritative input to another generative layer.

## 7. Capability-order contract

The model returns exactly one `capability_interpretations` item per accepted Capability profile, in the same order.

It cannot:

- create a new Capability area;
- merge profiles;
- split profiles;
- rename authoritative Capability labels;
- emit provenance indices.

JobHunter constructs the persisted areas with authoritative:

```text
name
source_capability_index
source_capability_coverage
```

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

## 9. Model-owned interpretation contract

The v5 draft contains only:

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

### Main interpretation

Each main interpretation is persisted with deterministic strength:

```text
plausible
```

It is never treated as employer fact.

Every main interpretation requires `interpretation_uncertainty`: a concrete sentence explaining what the vacancy does not establish or what remains inferred.

### Professional considerations

A professional consideration contains:

```text
statement
interpretation_strength: plausible | speculative
uncertainty
```

Use these sparingly and only when they add role-specific professional value.

## 10. Generic language guard

Model-created interpretation is rejected when it uses unqualified employer-obligation/full-ownership language such as:

```text
mandatory
required
must
necessary
expected to
responsible for
own the entire/full/end-to-end lifecycle/stack/pipeline/system
```

Cautious negative scope such as `probably not required` remains allowed.

The guard is deliberately generic. Do not turn it into a domain-specific blacklist of semiconductor phrases.

## 11. High-risk fields removed from B4

V5 deliberately does not ask the model to generate:

```text
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

These may be reconsidered later only if heterogeneous evidence shows a concrete user benefit and a safe representation. They are not required to prove B4.

## 12. Semantic guardrails

### Technology list != architecture

A list containing Spark, Kafka, Airflow/Prefect, MLflow, Docker, cloud platforms, databases, MES/SECS-GEM or ML frameworks does not establish one deployed system or data path.

### Process control != real-time proof

Process control, anomaly detection, manufacturing data, deployment experience, cloud names or preferred edge experience do not by themselves prove:

```text
real-time inference
low-latency control
active feedback loops
factory-floor deployment
autonomous process adjustment
```

### Domain context != unstated obligation

Semiconductor/domain knowledge may make process or equipment physics professionally useful, but it is not an employer requirement unless source-stated.

### Optionality/depth remain exact

- contextual stays contextual;
- preferred stays preferred;
- Python `expert` applies only to Python;
- explicit depth does not spread to neighboring frameworks/tools.

## 13. Artifact shape

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
interpretation_strength = plausible
practical_interpretation
interpretation_uncertainty
source_requirements[]
source_responsibilities[]
professional_considerations[]
probably_not_required[]
important_unknowns[]
```

The browser and CLI must visibly distinguish source anchors from professional inference and display the interpretation boundary adjacent to model prose.

## 14. Current implementation

Active:

```text
src/jobhunter/role_blueprint_service.py
src/jobhunter/role_blueprint_service_v5.py
src/jobhunter/role_blueprint_inference_v5.py
src/jobhunter/role_blueprint_v5_models.py
src/jobhunter/inference/lm_studio_runtime.py
scripts/audit_blueprint_v5_snapshot.py
```

Regression coverage:

```text
tests/test_role_blueprint_v5_models.py
tests/test_role_blueprint_inference_v5.py
tests/test_role_blueprint_service_v5.py
tests/test_role_blueprint_service.py
tests/test_role_blueprint_web.py
```

Historical v3/v4 implementation remains preserved for negative evidence and regression reference.

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
role-capability-blueprint-v5
role-capability-blueprint-v4
```

Run only:

```bash
jobhunter jobs blueprint tG9K
```

Do not rerun translation, P1.6 or Capability merely to test Blueprint.

If generation succeeds:

```bash
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v5_snapshot.py
```

## 16. B4 acceptance criteria

Mechanical acceptance requires:

- exact dependency identity;
- exact Capability one-to-one mapping and coverage;
- exact role purpose/requirements/responsibilities/role constraints;
- source strength/depth/evidence preservation;
- non-empty interpretation uncertainty per area;
- professional considerations only plausible/speculative with uncertainty;
- absence of legacy v4 expansion fields;
- no generic obligation/full-ownership language in model prose.

Semantic acceptance additionally requires:

1. materially useful professional interpretation beyond rereading source anchors;
2. meaningful uncertainty boundaries rather than boilerplate disclaimers;
3. no employer-specific topology/latency/ownership invention;
4. no real-time/low-latency/control-loop claim without source support;
5. no process-physics candidate obligation without source support;
6. preserved contextual/preferred/depth semantics;
7. no technology-list-to-architecture synthesis;
8. no generic curriculum dumping;
9. important unknowns preserve material uncertainty;
10. technical/domain correctness.

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
