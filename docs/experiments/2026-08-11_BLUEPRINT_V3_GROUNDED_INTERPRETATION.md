# Blueprint v3 Grounded Interpretation Experiment

**Status:** Historical failed B4 candidate; superseded by Blueprint v4/v3  
**Date:** 2026-08-11  
**Accepted upstream chain:** English P1.6 artifact 29 → Capability artifact 9  
**Historical runtime/schema:** `role-capability-blueprint-v3` / `role-capability-blueprint-v2`

## Purpose

Blueprint v3 attempted to keep the human-facing professional interpretation layer auditable by requiring model-generated Capability/P1.6 provenance and then reconciling mechanically provable strength/depth against accepted upstream truth.

The design was materially better than the earlier freer Blueprint v2 shape, but live B4 comparison showed that it still assigned too much low-level provenance bookkeeping to the LLM.

## Historical boundary

```text
accepted P1.6 artifact 29
        ↓
accepted Capability v7 artifact 9
        ↓
model produces practitioner interpretation
with explicit upstream links / scenario basis
        ↓
JobHunter deterministic reconciliation
        ↓
Blueprint v3/v2 artifact
```

## Intended protections

### Capability-area grounding

Every Blueprint capability area carried `source_capability_indices`. The union had to cover every accepted Capability profile.

### Source-named tools

A `source_named` tool had to link accepted P1.6 requirement/responsibility indices. JobHunter then derived:

```text
source_requirement_strength
source_depth_signals
```

from accepted P1.6.

### Role-level constraints

Degree/experience constraints were injected deterministically from Capability v7 `source_truth.role_level_requirement_indices`.

For `tG9K`:

```text
25  Master's degree
26  Professional experience — three to six years
```

### Hidden requirements and scenarios

A `highly_likely` hidden requirement needed accepted upstream grounding. Scenarios declared `source_stated_workflow` or `professional_example`; practitioner-created examples could not be `highly_likely`.

## Live failure evidence

### E2B

`gemma-4-e2b-it` completed the v3 request but failed structural/provenance validation. Its bounded retry repaired some validation failures but retained source-named tools without accepted P1.6 links and confused P1.6 requirement indices with Capability-profile indices.

The semantic draft also overreached by assembling listed technologies into a stronger end-to-end MLOps/streaming/cloud/edge architecture than the vacancy established.

### E4B

A first E4B attempt was rejected before generation because the model instance had been loaded with a 4,096-token context while the prompt was about 9,521 tokens. That was an infrastructure-only failure and is not semantic evidence.

JobHunter then gained automatic LM Studio context preparation at 16,384 tokens, after which `gemma-4-e4b-it-ud` completed the same v3 request and its Instructor repair attempt.

The real E4B v3 run failed five `source_named` tool validators. More importantly, the retry correctly identified source requirement numbers but wrote them into `source_depth_signals` rather than `source_requirement_indices`. It also repeated the same namespace confusion as E2B by using P1.6 requirement indices where only Capability profile indices 0 and 1 were valid.

E4B retained material semantic overreach around:

- Spark/Kafka as necessary streaming infrastructure;
- Airflow/Prefect as required orchestration;
- AWS/GCP deployment;
- TimescaleDB/PostgreSQL runtime roles;
- MLflow/Docker deployment flow;
- edge/real-time monitoring and control feedback;
- microservices, CI/CD/model registry and regulatory/quality risks.

These were stronger than the accepted P1.6 evidence warranted.

## Decision

Blueprint v3/v2 **fails B4**.

Do not:

- weaken the validators to accept its output;
- add domain-specific prompt patches for the observed indices/tools;
- reuse the v3/v2 identity for materially changed behavior;
- promote a larger model merely to compensate for deterministic provenance work that software already knows how to perform.

The primary lesson is architectural:

> **The model reasons; JobHunter owns provenance bookkeeping.**

Blueprint v4/v3 therefore removes numeric upstream provenance from the model-facing schema and attaches Capability/P1.6 source anchors deterministically after semantic generation.

Current redesign record:

`docs/experiments/2026-08-11_BLUEPRINT_V4_DETERMINISTIC_PROVENANCE_BOUNDARY.md`

## Historical semantic lessons retained

Even though v3 is closed, these constraints remain valid:

- source optionality must survive downstream;
- explicit depth applies only to its exact source concept;
- technology list != architecture;
- cloud names do not prove cloud deployment;
- edge preference does not prove edge inference;
- practitioner-created workflows are examples, not employer topology;
- technical correctness matters more than sophisticated prose;
- sparse evidence must yield fewer strong conclusions;
- B4 requires complete semantic review, not only schema validity.
