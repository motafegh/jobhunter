# Capability v7 — promoted P1.6 linkage failure and deterministic correction

**Date:** 2026-08-15  
**Branch:** `main`  
**Status:** deterministic correction implemented and CI-pass; live rerun pending

## Context

English P1.6 v20/v5 is publicly promoted and accepted. Dense calibration job `tG9K` reuses P1.6 artifact 36 through the normal public command. Capability v7 must now be rebuilt against analysis artifact 36 instead of historical Capability artifact 9, which depends on old P1.6 artifact 29.

Before this live rebuild, the public Capability boundary was also hardened so model-facing `accepted_extraction` excludes free-form P1.6 `rationale` prose while preserving authoritative concept/type/strength/depth/evidence/confidence and artifact/dependency identity.

## Live failure

Command:

```text
jobhunter jobs capability tG9K
```

No Capability artifact persisted.

Generation 1 failed strict v7 whole-source coverage because the model created one dense profile and omitted many capability-relevant accepted P1.6 requirement indices.

Instructor retry generation 2 repaired most of that coverage by creating two profiles, but emitted:

```text
source_responsibility_indices = [2, 3, 4, 5, 6, 9]
```

Artifact 36 contains only eight responsibilities, so valid indices are `0..7`. Strict validation therefore rejected invented responsibility index `9`.

The retry output also demonstrates the underlying boundary problem: `source_requirement_indices` and `source_responsibility_indices` are provenance/bookkeeping over already-accepted P1.6 facts, but the model was being asked to manually reproduce all of that bookkeeping while also doing semantic capability grouping.

## Decision

Do **not**:

- weaken complete requirement/responsibility coverage;
- accept out-of-range indices;
- increase retry count as the primary solution;
- silently invent a replacement index for an invalid model index;
- change Capability v7 semantic contract or historical persisted artifacts.

Instead apply the same architectural rule already established during P1.6 hardening:

```text
DETERMINISTIC CODE
handles already-known structured/provenance facts
↓
LLM
handles semantic grouping and derived reasoning
↓
STRICT VALIDATOR
checks the complete result
```

## Correction

Added inference-only v7 source-link repair:

```text
src/jobhunter/capability_v7_inference_models.py
```

and routed Instructor through that response model from:

```text
src/jobhunter/capability_inference.py
```

Behavior:

1. mechanically impossible **positive** source indices are removed before the inherited strict index validator;
2. negative indices and malformed/type-invalid indices remain untouched and still fail closed;
3. after each profile's evidence is grounded/canonicalized, JobHunter adds requirement/responsibility indices whose accepted P1.6 evidence exactly matches evidence already used by that profile;
4. only capability-relevant requirements are eligible for requirement-link recovery;
5. the original v7 whole-artifact coverage validator still runs afterward;
6. missing accepted facts with no profile evidence still fail with the same omitted-coverage error;
7. dense multi-profile requirement remains unchanged;
8. reconciliation and persisted Capability v7 schema/semantics remain unchanged.

This is provenance repair, not semantic auto-classification. It does not map one invalid index to another by guess.

## Regression tests

Added:

```text
tests/test_capability_v7_inference_link_repair.py
```

Coverage includes:

- out-of-range positive responsibility index plus exact grounded evidence is repaired to the supported accepted index;
- missing coverage with no supporting profile evidence still fails;
- negative source indices still fail closed.

Updated the existing inference transport test to expect the v7 inference-specific response model. No transport/runtime semantics changed.

## Deterministic verification

GitHub Actions CI run 811 on commit:

```text
b45c11e491f343959b717b01032aa8b3eb6060eb
```

passed:

```text
Ruff                 PASS
full pytest          PASS
warnings-as-errors   PASS
```

## Current gate

The deterministic correction is accepted for rerun, but Capability v7 itself is **not yet accepted** against promoted P1.6 artifact 36.

Next action:

```text
git pull --ff-only origin main
jobhunter jobs capability tG9K
```

If a new Capability artifact persists, it must be mechanically and semantically reviewed before it becomes the accepted current Capability chain.
