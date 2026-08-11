# Blueprint v4 Deterministic Provenance Boundary

**Status:** Historical experiment — mechanical success, B4 semantic rejection  
**Date:** 2026-08-11  
**Accepted upstream chain:** English P1.6 artifact 29 → Capability artifact 9  
**Runtime/schema tested:** `role-capability-blueprint-v4` / `role-capability-blueprint-v3`  
**Live model:** `gemma-4-e4b-it-ud`

## Why v4 existed

Blueprint v3/v2 asked the LLM to reproduce several upstream provenance namespaces:

- accepted Capability profile indices;
- P1.6 requirement indices;
- P1.6 responsibility indices;
- source-named tool links;
- source strength/depth metadata;
- scenario basis/grounding.

Both E2B and E4B confused those namespaces. The architectural response was:

> **The model should reason; JobHunter should own provenance bookkeeping.**

V4 implemented that boundary rather than weakening v3 validators or accumulating prompt patches.

## V4 boundary

```text
accepted P1.6 artifact 29
        ↓
accepted Capability v7 artifact 9
        ↓
JobHunter builds compact ordered Capability inputs
        ↓
model produces semantic interpretation draft
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

The model-facing draft contained no Capability/P1.6 numeric provenance. Persisted source anchors were reconstructed deterministically.

## What v4 proved

The live `tG9K` run completed successfully with E4B. `scripts/audit_blueprint_v4_snapshot.py` passed:

```text
Capability areas:                       2
Deterministic source requirements:      25
Deterministic source responsibilities:   7
Suggested tool examples:                 0
Role-level constraints:                  2
Hidden requirements:                     0
Professional examples:                   0
```

Therefore v4 proved that JobHunter can guarantee downstream survival of:

- accepted Capability identity and coverage;
- exact P1.6 requirement/responsibility links;
- requirement strength;
- explicit depth;
- evidence;
- role-level degree/experience constraints.

This provenance architecture remains valid and is carried forward.

## Why v4 still failed B4

Complete semantic review rejected the artifact despite the mechanical PASS.

Generated prose asserted or strongly implied employer-specific facts that accepted P1.6 does not establish:

- real-time APC/process adjustment;
- low-latency active control loops;
- factory-floor/MES-SECS-to-model topology;
- process physics as a candidate obligation;
- a specific code/training-data/hyperparameter audit trail;
- stronger edge importance based on unstated deployment topology;
- ownership of the entire lifecycle.

The failure was not missing provenance. It was **semantic amplification above correct provenance**.

## Root cause learned from v4

Two sources of amplification remained:

1. V4 passed Capability artifact 9's derived prose downstream (`summary`, `sub_capabilities`, `underlying_knowledge`, operational reasoning, etc.). The Capability grouping/source-truth boundary was accepted at B3, but its model-derived explanatory prose was not safe to treat as authoritative input to another generative layer.
2. V4 still exposed broad model-owned role-shape/depth/work-product/failure-mode/scenario/bottom-line surfaces where plausible professional knowledge could become employer-specific certainty.

Therefore a second permanent rule was added:

> **Accepted Capability grouping may flow downstream; Capability-derived prose is not automatically authoritative downstream context.**

## Decision

```text
Blueprint v4/v3 does not pass B4.
Do not publish its tG9K snapshot as an accepted review artifact.
Preserve v4 as proof of the deterministic provenance architecture.
Use a new contract identity for the semantic-boundary redesign.
```

The successor is:

```text
role-capability-blueprint-v5
schema role-capability-blueprint-v4
```

The complete failure analysis and v5 design decision are recorded in:

```text
docs/experiments/2026-08-11_BLUEPRINT_V4_SEMANTIC_FAILURE_AND_V5_BOUNDARY.md
```
