# JobHunter Role Capability Blueprint Plan

**Status:** Phase-1 calibration experiment concluded; implementation retained as experimental/non-authoritative  
**Date:** 2026-08-12  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md` and `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`  
**Scope:** Record the Blueprint design boundary, experiment results, and conditions for any future reopening. Corpus-wide generation is not authorized.

## 1. Purpose

JobHunter separates three semantic jobs:

```text
P1.6
→ strict factual extraction / evidence boundary

Capability Intelligence
→ auditable grouping/reasoning above P1.6

Role Capability Blueprint
→ experimental human-facing professional interpretation
```

The intended Blueprint value is useful practitioner context beyond rereading the vacancy while keeping two categories unmistakably separate:

```text
employer/source truth
professional inference
```

The Phase-1 experiment shows that the current generative approach is not reliable enough to make Blueprint an accepted decision layer.

## 2. Current implementation identity

Retained experimental implementation:

```text
prompt/runtime: role-capability-blueprint-v6
schema:         role-capability-blueprint-v5
best bounded model tested: gemma-4-12b-it-qat
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

Historical identities remain immutable evidence and must not be reused for material redesigns.

## 3. Authority boundary

```text
source
→ English projection
→ accepted P1.6 facts
→ accepted Capability grouping/source truth
→ experimental Blueprint professional context
```

No downstream layer overwrites upstream truth.

A mechanically current Blueprint artifact is not automatically semantically accepted. The `tG9K` experiment repeatedly demonstrated this distinction.

## 4. Experiment history

### V3/v2 — structural + semantic failure

E2B and E4B both confused P1.6 requirement indices with Capability-profile indices. The contract also retained streaming/cloud/edge/MLOps architecture overreach.

Lesson:

> **The model must not own provenance bookkeeping that JobHunter can derive deterministically.**

### V4/v3 — provenance success + semantic failure

V4 moved Capability/P1.6 provenance into JobHunter and passed the mechanical live audit. Generated prose still invented or strengthened real-time/low-latency control, employer topology, process physics, edge placement, specific governance implementation and end-to-end lifecycle ownership.

Lesson:

> **Correct provenance does not certify generated interpretation.**

### V5/v4 — narrower input + remaining summary failure

V5 stopped feeding Capability-derived explanatory prose downstream and removed role shape, hidden requirements, tool suggestions, work products, scenarios and bottom-line generation.

Live artifact 6 still described Area 2 as end-to-end infrastructure work, assumed telemetry streams, introduced automated training workflows and deployment-lifecycle scope while its uncertainty admitted ownership boundaries were unknown.

Lesson:

> **A single free-form positive role-summary surface can still amplify scope beyond source evidence.**

### V6/v5 + E4B — narrow contract but model failure

V6 removed free-form role-summary generation and allowed only explicitly uncertain professional considerations and unknowns.

The E4B run failed bounded Instructor validation and still introduced assumption-bearing wording.

### V6/v5 + 12B — mechanically valid, semantically still not acceptable

The controlled comparison held fixed:

```text
English projection artifact 33
P1.6 artifact 29
Capability artifact 9
Blueprint v6/v5 contract
review rubric
```

Only the Blueprint model changed to:

```text
gemma-4-12b-it-qat
```

Resulting Blueprint artifact **7** passed:

```text
scripts/audit_blueprint_v6_snapshot.py
CI
```

Mechanical result:

```text
2 Capability areas
25 deterministic source requirements
7 deterministic source responsibilities
4 professional considerations
4 important unknowns
2 role-level constraints
1 role-purpose item
```

The stronger model was materially better than E4B. It avoided the rejected v5 end-to-end/lifecycle summary behavior and produced several useful grounded considerations.

Complete semantic review still rejected the artifact because generated unknowns/considerations included assumption-bearing framing such as:

- automated APC/SPC feedback loops not established by source;
- an assumed cloud-provider/on-prem model-hosting choice;
- `raw sensor physics` as role context not stated by source;
- strict versioning of data lineage/model weights tied to unspecified quality standards.

These are milder than earlier failures but still contradict the explicit semantic boundary.

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

## 5. Phase-1 disposition

Blueprint is **not accepted for Phase-1 authoritative use**.

The implementation remains available because it is useful evidence and may support future research, but Phase 1 must not keep iterating on it.

During Phase 1:

- do not create Blueprint v7;
- do not weaken v6 validators;
- do not add vacancy/domain-specific prompt patches;
- do not continue adjacent local-model shopping;
- do not use Blueprint output in Market aggregation;
- do not use Blueprint output as personal readiness evidence;
- do not use Blueprint output as automatic recommendation/application truth;
- do not treat current-chain status as semantic acceptance.

Blueprint may be inspected as **non-gating experimental evidence** only.

## 6. V6 deterministic boundary worth preserving

Although v6 is not accepted as an authoritative product layer, its deterministic architecture remains the strongest Blueprint design achieved in the experiment.

### Model input

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
Capability operational prose
long duplicated vacancy description
company-description prose
```

### JobHunter-owned persisted source anchors

```text
source_role_purpose[]
source_capability_coverage[]
source_role_constraints[]
capability_areas[].source_requirements[]
capability_areas[].source_responsibilities[]
```

Requirement strength, explicit depth, evidence, Capability identity and source coverage remain deterministic.

### Model-owned v6 surface

```text
capability_interpretations[]
  professional_considerations[]
    statement
    interpretation_strength: plausible | speculative
    uncertainty
  important_unknowns[]

overall_unknowns[]
```

There is no model-generated:

```text
practical_interpretation
role shape
likely depth
hidden requirements
tool recommendations
work-product lists
failure-mode lists
end-to-end scenarios
runtime topology
probably-not-required list
bottom line
source provenance IDs
```

This boundary should be preserved as historical engineering knowledge even if a future Blueprint redesign uses a different representation.

## 7. Permanent inference lessons

### Technology list != architecture

Spark, Kafka, Airflow/Prefect, MLflow, Docker, cloud platforms, databases, MES/SECS-GEM and ML frameworks do not establish one deployed system or data path.

### High-volume != streaming

High-volume/high-dimensional data does not establish streaming rather than batch or mixed operation.

### Process control != real-time proof

Process control, anomaly detection or APC/SPC terminology do not by themselves establish real-time inference, low latency, or an automated feedback loop.

### Cloud/edge names != placement

Cloud platform names and preferred industrial/edge experience do not prove where an employer deploys models.

### Deployment/governance != lifecycle ownership

Model deployment, traceability, reproducibility and governance do not prove one person owns the full ML/MLOps lifecycle.

### Unknowns can smuggle assumptions

Questions can overreach too. An unknown is not automatically safe merely because it is phrased as uncertainty.

For example, asking for *the* cloud provider presumes cloud deployment; asking about *the* feedback-loop latency presumes a feedback loop. The safe representation must preserve the possibility that the system/choice does not exist at all.

### Optionality/depth remain exact

- contextual stays contextual;
- preferred stays preferred;
- Python `expert` applies only to Python;
- explicit depth does not spread to neighboring tools.

## 8. Runtime / implementation retained

Current implementation:

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

Current experimental Blueprint model:

```text
gemma-4-12b-it-qat
```

Runtime automatically prepares the model at an 8,192-token context and uses exclusive LLM loading so other loaded LLM instances are unloaded before the Blueprint model is prepared; embedding models are left alone.

V6 completion budget remains bounded to 4,096 tokens.

The browser explicitly marks Blueprint as experimental/non-authoritative.

## 9. Reopen criteria

Do not reopen Blueprint merely because another prompt wording or nearby local model is available.

A future reopening requires at least one material change to the problem, for example:

- heterogeneous evidence reveals a concrete user-value question P1.6 + Capability cannot answer;
- a materially stronger/different inference approach is available;
- deterministic or retrieval-backed professional knowledge can bound interpretation better;
- a reviewed human-in-the-loop representation can separate source facts, professional examples and employer-specific claims safely;
- later canonical Phase-2 structures provide stronger grounding than single-job generation.

A reopened design must use a new prompt/schema identity and must not silently mutate v6/v5.

## 10. Current next work

Blueprint calibration is no longer the active gate.

Proceed with heterogeneous validation of:

```text
source
→ English projection
→ P1.6
→ Capability v7
```

Blueprint may be observed only as research evidence during that review.

The current selected `tG9K` snapshot intentionally preserves artifact 7 as rejected experimental evidence while P1.6 artifact 29 and Capability artifact 9 remain accepted bounded anchors.
