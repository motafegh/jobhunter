# JobHunter Role Capability Blueprint Plan

**Status:** Phase-1 experiment concluded; retained experimental/non-authoritative; pinned to historical Capability v7 semantics  
**Date:** 2026-08-21  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md` and `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`  
**Scope:** Record the Blueprint design boundary, experiment results, and conditions for any future reopening. Corpus-wide generation and authoritative use are not authorized.

## 1. Purpose

JobHunter separates three semantic jobs:

```text
P1.6
→ strict factual extraction / evidence boundary

Capability Intelligence
→ auditable grouping/reasoning above accepted P1.6

Role Capability Blueprint
→ experimental human-facing professional interpretation
```

The intended Blueprint value was practitioner context beyond rereading the vacancy while keeping two categories unmistakably separate:

```text
employer/source truth
professional inference
```

The Phase-1 experiment showed that the current generative approach is not reliable enough to make Blueprint an accepted decision layer.

## 2. Retained experimental identity

```text
prompt/runtime: role-capability-blueprint-v6
schema:         role-capability-blueprint-v5
best bounded model tested: gemma-4-12b-it-qat
```

Blueprint v6 is intentionally **not rebased onto current Capability v9**. It remains pinned to the historical Capability v7 dependency semantics used by the experiment.

Persistence identity preserves:

```text
job detail version
+ exact English projection artifact
+ exact English P1.6 artifact
+ exact historical Blueprint-compatible Capability artifact
+ exact Blueprint model
+ Blueprint prompt version
+ Blueprint schema version
```

Historical identities remain immutable evidence and must not be silently reused for a material redesign.

## 3. Authority boundary

Current accepted public chain:

```text
source
→ English projection
→ accepted/current P1.6 v20 facts
→ accepted/current Capability v9 grouping/source truth
```

Blueprint sits **outside** that current accepted authority chain during Phase 1:

```text
historical Blueprint-compatible P1.6/Capability chain
→ experimental Blueprint v6 professional context
```

No downstream layer overwrites upstream truth. A mechanically current/dependency-matching Blueprint artifact is not automatically semantically accepted.

## 4. Experiment history

### V3/v2 — structural + semantic failure

E2B and E4B confused P1.6 requirement indices with Capability-profile indices. The contract also retained streaming/cloud/edge/MLOps architecture overreach.

Lesson:

> The model must not own provenance bookkeeping that JobHunter can derive deterministically.

### V4/v3 — provenance success + semantic failure

V4 moved Capability/P1.6 provenance into JobHunter and passed mechanical live audit. Generated prose still invented or strengthened real-time/low-latency control, employer topology, process physics, edge placement, specific governance implementation and end-to-end lifecycle ownership.

Lesson:

> Correct provenance does not certify generated interpretation.

### V5/v4 — narrower input + remaining summary failure

V5 stopped feeding Capability-derived explanatory prose downstream and removed several high-risk generated surfaces. Live artifact 6 still described end-to-end infrastructure work, assumed telemetry streams, introduced automated training workflows and deployment-lifecycle scope while its own uncertainty admitted ownership boundaries were unknown.

Lesson:

> A free-form positive role-summary surface can amplify scope beyond source evidence.

### V6/v5 + E4B — narrow contract but model failure

V6 removed free-form role-summary generation and allowed only explicitly uncertain professional considerations and unknowns. E4B still failed bounded validation and produced assumption-bearing wording.

### V6/v5 + 12B — mechanically valid, semantically rejected

The controlled comparison held the historical source/English/P1.6/Capability chain, Blueprint contract and review rubric fixed while changing only the Blueprint model to `gemma-4-12b-it-qat`.

Artifact 7 passed mechanical audit/CI and was materially better than the smaller model, but complete semantic review still rejected assumption-bearing framing such as:

- automated APC/SPC feedback loops not established by source;
- assumed cloud-provider/on-prem model-hosting choice;
- `raw sensor physics` as role context not stated by source;
- strict versioning of data lineage/model weights tied to unspecified quality standards.

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

## 5. Phase-1 disposition

Blueprint is **not accepted for Phase-1 authoritative use**.

During Phase 1:

- do not create Blueprint v7;
- do not weaken v6 validators;
- do not add vacancy/domain-specific prompt patches;
- do not continue adjacent local-model shopping;
- do not use Blueprint output in Market aggregation;
- do not use Blueprint output as personal readiness evidence;
- do not use Blueprint output as automatic recommendation/application truth;
- do not treat current-chain/dependency status as semantic acceptance;
- do not rebase Blueprint v6 onto Capability v9 merely because v9 is current.

Blueprint may be inspected only as non-gating experimental evidence.

## 6. V6 deterministic boundary worth preserving

Although v6 is not an authoritative product layer, its strongest engineering lesson is the deterministic separation between source anchors and generated interpretation.

V6 model input was narrowed to neutral role context plus exact source-grounded facts associated with the historical accepted Capability chain.

JobHunter-owned source anchors included source role purpose, capability coverage, role constraints, source requirements and source responsibilities.

The model-owned surface was reduced to bounded professional considerations and important unknowns.

This architecture remains useful historical engineering knowledge even if a future Blueprint redesign uses a different representation.

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

Questions/unknowns can overreach too. Asking for *the* cloud provider presumes cloud deployment; asking about *the* feedback-loop latency presumes a feedback loop. Safe uncertainty must preserve the possibility that the assumed system/choice does not exist.

### Optionality/depth remain exact

Contextual stays contextual; preferred stays preferred; explicit depth stays scoped to the exact concept.

## 8. Runtime / implementation retained

Current retained implementation includes:

```text
src/jobhunter/role_blueprint_service.py
src/jobhunter/role_blueprint_service_v6.py
src/jobhunter/role_blueprint_inference_v6.py
src/jobhunter/role_blueprint_v6_models.py
src/jobhunter/inference/lm_studio_runtime.py
scripts/audit_blueprint_v6_snapshot.py
```

Regression coverage for Blueprint remains preserved. The browser must label Blueprint experimental/non-authoritative.

## 9. Reopen criteria

Do not reopen Blueprint merely because another prompt wording or nearby local model is available.

A future reopening requires a material change, for example:

- heterogeneous evidence reveals a concrete user-value question P1.6 + Capability cannot answer;
- a materially stronger/different inference approach becomes available;
- deterministic/retrieval-backed professional knowledge can bound interpretation better;
- a reviewed human-in-the-loop representation can safely separate source facts, professional examples and employer-specific claims;
- later canonical Phase-2 structures provide stronger grounding than single-job generation.

A reopened design must use a new prompt/schema identity and must not silently mutate v6/v5.

## 10. Current next work

Blueprint is **not** the active gate.

Current accepted/public semantic work proceeds through:

```text
source
→ English projection
→ P1.6 v20/v5
→ Capability v9/v5
```

Heterogeneous validation order:

```text
Python/software          ← tmBK accepted: P1.6 39 → Capability 13
network/security         ← t4qV accepted: P1.6 44 → Capability 14
operations/platform      ← tmyX accepted: P1.6 46 → Capability 15
```

Blueprint may be observed only as historical/research evidence. Do not generate or tune Blueprint as part of the current heterogeneous acceptance path.
