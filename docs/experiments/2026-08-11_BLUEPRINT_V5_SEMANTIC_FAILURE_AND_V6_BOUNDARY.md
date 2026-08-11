# Blueprint v5 Semantic Failure and v6 Boundary

**Status:** Historical v5 experiment; v6/v5 active B4 candidate  
**Date:** 2026-08-11  
**Accepted upstream chain:** English projection 33 → English P1.6 artifact 29 → Capability v7 artifact 9  
**v5 runtime/schema tested:** `role-capability-blueprint-v5` / `role-capability-blueprint-v4`  
**v6 candidate runtime/schema:** `role-capability-blueprint-v6` / `role-capability-blueprint-v5`  
**Blueprint model:** `gemma-4-e4b-it-ud`

## What v5 fixed

Blueprint v5 kept the v4 deterministic-provenance boundary and additionally stopped sending Capability-derived explanatory prose downstream. The model received only neutral role context, accepted Capability labels, exact linked P1.6 requirement facts, exact linked responsibilities, role purpose, and role-level constraints.

V5 also removed several high-risk model-owned surfaces such as role shape, hidden requirements, tool recommendations, workflow scenarios, work-product lists, and bottom-line synthesis.

The live `tG9K` v5 artifact therefore preserved the accepted chain correctly:

```text
English analysis artifact 29
Capability artifact 9 / v7-v4
Blueprint artifact 6 / v5-v4
Blueprint model gemma-4-e4b-it-ud
```

The Review Snapshot marked the Blueprint as current-chain and CI on the published candidate passed.

## Why v5 still failed B4

The remaining free-form field was `practical_interpretation`.

Area 1 was substantially better calibrated than v4, but Area 2 still said that the function centered on designing and implementing **end-to-end infrastructure**, assumed high-volume telemetry **streams**, introduced automated training/validation workflows, and described deployment-lifecycle management. The paired uncertainty later admitted that system-ownership boundaries were unknown, so the positive interpretation and its uncertainty contradicted each other.

This is a semantic-boundary failure rather than a provenance failure.

The accepted source supports:

- robust pipelines for high-volume, high-dimensional sensor/trace/metrology data;
- rigorous validation and monitoring in an industrial setting;
- partnering to move models toward production;
- traceability, reproducibility, and governance;
- contextual Spark/Kafka, MLflow/Docker, Airflow/Prefect, cloud/edge and deployment knowledge;
- preferred industrial/edge deployment experience.

It does **not** establish:

- full/end-to-end infrastructure ownership;
- streaming rather than batch processing;
- one combined MLOps architecture;
- automated training workflows as an employer requirement;
- complete deployment-lifecycle ownership.

Therefore:

```text
Blueprint v5/v4 does not pass B4.
```

Do not accept artifact 6 as the bounded Blueprint baseline.

## V6 structural response

V6 removes the remaining free-form positive role-summary surface rather than trying to prompt it into behaving.

The model-facing v6 draft contains only:

```text
capability_interpretations[]
  professional_considerations[]
    statement
    interpretation_strength = plausible | speculative
    uncertainty
  important_unknowns[]  # at least one per Capability

overall_unknowns[]
```

The model does **not** emit:

```text
practical_interpretation
interpretation_uncertainty
area-level interpretation_strength
probably_not_required
role_read
likely_role_shape
likely_depth
hidden_requirements
suggested tools
work products
failure-mode lists
workflow scenarios
bottom_line
source provenance IDs
```

All authoritative content remains JobHunter-owned:

```text
source_role_purpose
source_role_constraints
Capability label/index/coverage
source_requirements
source_responsibilities
requirement strength
explicit depth
evidence
```

## Why this is materially safer

There is no longer a paragraph that can silently convert professional plausibility into a role-level assertion.

Every positive model-created statement is a `professional_consideration` and therefore must carry:

- `plausible` or `speculative` strength;
- an explicit uncertainty statement;
- no mandatory/required/must/necessary/expected-to/responsible-for language;
- no full/end-to-end lifecycle/stack/pipeline/system/infrastructure scope claim.

Every Capability must also contain at least one `important_unknown`.

The prompt explicitly forbids inference shortcuts such as:

```text
high-volume data -> streaming
process control -> real-time control
anomaly detection -> low latency
APC/SPC -> automated feedback loop
cloud/edge names -> deployment placement
model deployment/governance -> lifecycle ownership
```

Unknowns must not smuggle assumptions into their wording. For example, prefer:

```text
whether any automated feedback loop exists is unknown
```

over:

```text
the feedback-loop latency is unknown
```

when the source does not establish a feedback loop.

## Runtime / performance

V6 keeps automatic LM Studio context preparation at 16,384 tokens, but its output contract is substantially smaller. The Blueprint completion budget is capped at **4,096 tokens** even if the general analysis budget is larger.

This reduces unnecessary generation budget while preserving enough headroom for structured output.

## B4 acceptance rule

Mechanical v6 audit:

```bash
python scripts/audit_blueprint_v6_snapshot.py
```

A mechanical PASS remains necessary but insufficient.

B4 accepts v6 only if live semantic review confirms that:

- professional considerations add useful domain/practitioner context;
- every positive inference is clearly bounded by its uncertainty;
- contextual/preferred technology remains calibrated;
- technology lists do not become architecture;
- unknowns preserve unresolved operating-mode, deployment, ownership and interface questions;
- no source-unsupported real-time/streaming/cloud-edge/full-lifecycle assertions return;
- the layer remains useful enough to justify its existence above P1.6 + Capability.
