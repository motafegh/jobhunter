# Blueprint v4 Semantic Failure and v5 Boundary

**Status:** v4/v3 mechanically successful but semantically rejected; v5/v4 active B4 candidate  
**Date:** 2026-08-11  
**Fixed upstream chain:** English projection 33 → English P1.6 artifact 29 → Capability v7/v4 artifact 9  
**v4 live model:** `gemma-4-e4b-it-ud`

## Decision

Blueprint v4/v3 is **not accepted for B4**.

The live `tG9K` artifact completed successfully and `scripts/audit_blueprint_v4_snapshot.py` passed every mechanical provenance check:

```text
Capability areas:                    2
Deterministic source requirements:   25
Deterministic source responsibilities: 7
Role-level constraints:              2
Suggested tool examples:             0
Hidden requirements:                 0
Professional examples:               0
```

That result proves the v4 deterministic provenance architecture works. It does **not** prove semantic calibration. Complete review found repeatable employer-specific certainty that the accepted source did not establish.

## What v4 got right

v4 fixed the structural failure that blocked v3:

- the model no longer emitted Capability/P1.6 numeric provenance;
- every accepted Capability profile survived in source order;
- all linked P1.6 requirements/responsibilities survived deterministically;
- requirement strength, explicit depth and evidence survived exactly;
- Master's degree and three-to-six-years experience remained exact role-level constraints;
- no model-selected source facts could disappear;
- no invalid source-named tool bookkeeping was required.

This boundary remains a permanent lesson:

> **JobHunter owns provenance; the model owns only reasoning above it.**

## Why v4 still failed B4

The live v4 prose made claims stronger than the accepted source supports. The failure classes were generic, not semiconductor-specific prompt trivia.

### 1. Real-time / low-latency control was invented

The artifact claimed data had to reach models in time for real-time APC adjustments and called low latency a primary operational concern.

Accepted P1.6 contains process-control/anomaly work, deployment context, cloud names and preferred industrial/edge deployment. Those facts do not prove real-time inference, a latency target, an active feedback loop, or autonomous process adjustment.

### 2. Employer topology was invented

The artifact described factory-floor influence and an MES/SECS-to-model control path. The source names fab systems and data concepts, but does not specify a concrete deployed data path or runtime topology.

### 3. Process physics became an unstated candidate obligation

The artifact said a practitioner must be adept at process physics. Semiconductor domain knowledge is contextual in accepted P1.6; no process/equipment-physics requirement is stated.

### 4. Governance detail was amplified beyond source

The source explicitly requires traceability/reproducibility/governance and validation discipline. v4 expanded that into a specific audit trail containing exact code version, training-data slice and hyperparameters for each decision. That is a plausible engineering implementation, not an employer-stated requirement.

### 5. Edge importance was strengthened

Industrial/edge deployment is preferred in P1.6. v4 said edge is highly valuable because critical decisions happen near equipment. The preference is source truth; the reason/topology is inference.

### 6. End-to-end ownership was invented

The bottom line said the candidate should own the entire lifecycle. Accepted P1.6 does not establish that ownership boundary.

## Root cause

The problem was not provenance reconciliation and was not solved by using the stronger E4B model.

v4 still gave the model two sources of semantic amplification:

1. **Capability derived prose** was passed downstream through `summary`, `sub_capabilities`, `underlying_knowledge`, `operational_practices`, `operational_context`, and `unknown_scope`.
2. The Blueprint schema still exposed broad free-text surfaces such as global role read/shape, depth, work products, failure modes and bottom line where plausible practitioner knowledge could become employer-specific certainty.

Capability artifact 9 was accepted for its B3 source-truth/coverage boundary, but some of its model-derived prose is intentionally aggressive. Feeding that derived prose into another generative layer compounds uncertainty.

Therefore:

> **Accepted Capability grouping may flow downstream; derived Capability prose is not automatically authoritative downstream context.**

## v5 response

A new identity is used rather than mutating v4 history:

```text
prompt: role-capability-blueprint-v5
schema: role-capability-blueprint-v4
```

### Model input is reduced to source-grounded structure

The v5 model receives only:

```text
selected neutral role context
source-stated role purpose
role-level source constraints
accepted Capability label
exact linked P1.6 requirement facts
exact linked P1.6 responsibility statements
```

It does **not** receive:

```text
Capability summary
Capability sub-capabilities
Capability underlying knowledge
Capability operational reasoning
long vacancy description duplicated after P1.6
company-description prose
```

### Every model statement is inference

v5 has no `highly_likely` model-created capability interpretation. Persisted capability interpretation strength is mechanically `plausible`.

Every main interpretation requires:

```text
practical_interpretation
interpretation_uncertainty
```

The boundary sentence must state what the vacancy does not establish or what remains inferred.

Optional professional considerations are limited to:

```text
plausible
speculative
```

and each requires its own uncertainty sentence.

### High-risk expansion surfaces are removed from B4

v5 deliberately removes model-generated:

```text
role_read
likely_role_shape
likely_depth
hidden requirements
tool recommendations
work products
operational-concern lists
scenarios
bottom_line
```

The information that is actually employer-supported remains visible separately through deterministic source anchors.

### Generic obligation guard

Model-created interpretation is rejected when it uses unqualified employer-obligation or full-ownership language such as:

```text
mandatory
required
must
necessary
expected to
responsible for
own the entire/full/end-to-end lifecycle/stack/pipeline/system
```

Cautious negative scope such as `probably not required` remains valid.

## B4 acceptance rule for v5

Mechanical validity remains necessary but insufficient.

Reject v5 if complete live review still turns professional possibilities into employer facts, including:

- real-time/low-latency control as fact;
- a specific MES/SECS/Kafka/Spark/cloud/edge topology;
- process physics as a required candidate capability without source support;
- end-to-end ownership;
- optional/contextual tools promoted to required/mastery;
- Python `expert` depth spread to neighboring frameworks;
- specific governance implementation presented as source requirement;
- vague uncertainty text that does not actually bound the interpretation.

Passing v5 should mean something narrower and more useful:

> the human gets practitioner context **and simultaneously sees exactly which parts are source truth and which parts remain interpretation**.

Only after that bounded `tG9K` gate passes should B5/CI-3 heterogeneous review begin.
