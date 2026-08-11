# Blueprint v4 Deterministic Provenance Boundary

**Status:** Active B4 candidate; implemented on `main`, pending live semantic acceptance  
**Date:** 2026-08-11  
**Accepted upstream chain:** English P1.6 artifact 29 → Capability artifact 9  
**Candidate runtime/schema:** `role-capability-blueprint-v4` / `role-capability-blueprint-v3`  
**Blueprint model for controlled live test:** `gemma-4-e4b-it-ud`

## Why v4 exists

Blueprint v3/v2 attempted to keep its human-facing interpretation grounded by asking the LLM to reproduce several upstream provenance namespaces:

- accepted Capability profile indices;
- P1.6 requirement indices;
- P1.6 responsibility indices;
- source-named tool links;
- source strength/depth metadata;
- scenario basis/grounding.

That boundary failed with both E2B and E4B on the fixed `tG9K` chain.

The important failure was not merely malformed JSON. Both models confused P1.6 requirement indices with Capability-profile indices. E4B's bounded repair correctly reasoned that `tsfresh/sktime` came from requirement 10, PyTorch/TensorFlow from 6, Spark/Kafka from 14, Airflow/Prefect from 18, and PostgreSQL/TimescaleDB from 15/16, but placed those IDs into `source_depth_signals` rather than `source_requirement_indices`. The validators correctly rejected the result.

E4B also retained the semantic overreach v3 was intended to control: a technology list became an implied Spark/Kafka/Airflow/MLflow/Docker/cloud/edge architecture, contextual technologies were described as necessary/required, and illustrative workflow choices were stated too strongly.

The conclusion is architectural:

> **The model should reason; JobHunter should own provenance bookkeeping.**

Do not weaken v3 validators, retry v3 with prompt patches, or promote a larger model merely to compensate for a responsibility split that software can resolve exactly.

## V4 boundary

```text
accepted P1.6 artifact 29
        ↓
accepted Capability v7 artifact 9
        ↓
JobHunter builds compact ordered capability inputs
(no numeric provenance exposed to the model)
        ↓
model produces semantic interpretation draft
(exactly one interpretation per accepted Capability, in order)
        ↓
JobHunter deterministic reconciliation
        ├─ Capability identity / position / coverage
        ├─ P1.6 source requirements
        ├─ P1.6 source responsibilities
        ├─ requirement strength
        ├─ explicit depth
        ├─ evidence
        └─ role-level degree / experience constraints
        ↓
Blueprint v4/v3 artifact
```

## What the model no longer owns

The model-facing `RoleBlueprintDraft` contains no:

```text
source_capability_indices
source_requirement_indices
source_responsibility_indices
source_requirement_strength
source_depth_signals
source_role_constraints
scenario_basis
```

The model also does not rename/regroup accepted Capability profiles. It returns one `capability_interpretations` item per supplied Capability profile in the same order. JobHunter supplies the authoritative label and source links when constructing the persisted artifact.

This removes the ambiguous numeric namespaces that failed in both v3 model comparisons.

## Source facts are first-class anchors

Each persisted v4 capability area contains deterministic:

```text
source_capability_index
source_requirements[]
source_responsibilities[]
```

A source requirement preserves:

```text
requirement_index
concept
concept_type
requirement_type
depth_signal
evidence
```

These fields come from accepted upstream truth, not model reproduction.

For `tG9K`, this means contextual framework/platform requirements remain visibly contextual, preferred MATLAB/C++/edge remain preferred, Python alone carries its explicit `expert` source depth, and required industrial experience/depth remains attached to the correct source concept.

## Suggested tools are inference only

V4 removes model-created `source_named` tool records.

If a technology is employer/source-named, it is already present in deterministic `source_requirements`. The model does not need to repeat it with a provenance ID.

Model-created tools live only under:

```text
suggested_tools_or_examples
```

with relationship:

```text
likely_example
possible_example
```

They carry no source provenance and cannot be described as required/mandatory/necessary or as expert/mastery expectations.

## Hidden requirements and scenarios are structurally downgraded

A model-created hidden requirement is professional inference, not employer fact. V4 permits only:

```text
plausible
speculative
```

The same rule applies to model-created workflows. The persisted field is explicitly:

```text
professional_example_scenarios
```

and JobHunter deterministically marks the basis:

```text
professional_example
```

There is no model-generated `source_stated_workflow` category in v4. If a source responsibility matters, it is already preserved as a deterministic source responsibility. This avoids asking the model to decide whether its own synthesized workflow is source-stated.

When an illustrative scenario chooses unstated topology, latency, vendor, batch/stream mode, cloud/edge placement, scale, ownership, orchestration, or feedback-loop behavior, that choice belongs in `assumptions` and must remain one possible implementation.

## Compact model input

V3 sent the full accepted extraction plus the full Capability artifact, which duplicated information and increased prompt size/namespace complexity.

V4 sends a compact projection containing:

- selected role/company context;
- role purpose;
- role-level constraints for context;
- ordered accepted Capability labels;
- source requirement facts without numeric IDs;
- source responsibility statements without numeric IDs;
- compact accepted Capability reasoning statements/status/confidence.

The raw long job description is not duplicated into the Blueprint prompt merely to recreate already accepted P1.6/Capability facts.

## Runtime context

Blueprint inference automatically prepares the selected LM Studio model with a **16,384-token context window** before generation. JobHunter reuses an already-correct load or reloads the same model when its active context is insufficient.

This is runtime preparation, not a semantic contract variable. The first E4B v3 failure at a 4,096-token load was infrastructure-only; the later E4B v3 run completed normally and provided the real negative contract evidence.

## Deterministic gate

Before live acceptance:

```bash
python -m pip install -e ".[dev]"
ruff check .
python -m pytest
python -m pytest -W error
```

Confirm the active contract:

```bash
python -c "from jobhunter.role_blueprint_service import BLUEPRINT_PROMPT_VERSION, BLUEPRINT_SCHEMA_VERSION; print(BLUEPRINT_PROMPT_VERSION); print(BLUEPRINT_SCHEMA_VERSION)"
```

Expected:

```text
role-capability-blueprint-v4
role-capability-blueprint-v3
```

## Controlled live `tG9K` B4 procedure

Keep the accepted upstream chain fixed. Do **not** rerun translation, P1.6, or Capability merely to test Blueprint.

Run only:

```bash
jobhunter jobs blueprint tG9K
```

If and only if a valid Blueprint artifact is produced:

```bash
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v4_snapshot.py
```

The mechanical audit must verify exact one-to-one Capability mapping, exact P1.6 source-anchor propagation, exact role-level constraints, absence of legacy v3 provenance fields, and bounded certainty for model-created hidden requirements/scenarios.

## Semantic B4 acceptance criteria

Mechanical correctness is necessary but not sufficient. B4 passes only if live review confirms that:

- `role_read` and `likely_role_shape` are calibrated to the vacancy rather than inflated into a broader MLOps/platform role;
- each accepted Capability receives useful practical interpretation without regrouping;
- source anchors preserve all accepted requirement strength and exact depth;
- Python `expert` depth does not spread to frameworks or neighboring tools;
- MATLAB and C/C++ remain preferred;
- cloud remains contextual and edge remains preferred rather than becoming deployment architecture;
- Spark/Kafka, databases, Airflow/Prefect, MLflow/Docker and cloud/edge are not assembled into one asserted employer stack;
- real-time, microservices, CI/CD, model registry, regulatory constraints, autonomous control loops and feedback architecture are not asserted without source support;
- professional examples are visibly hypothetical and state material assumptions;
- hidden requirements are useful, role-specific and correctly limited to plausible/speculative;
- `important_unknowns` preserve unresolved topology, latency, deployment and ownership questions;
- role-level Master's degree and three-to-six-years experience survive exactly;
- technical meanings are correct;
- the Blueprint adds useful practitioner interpretation beyond P1.6 and Capability rather than merely rewriting them.

Only complete live semantic review can accept B4.
