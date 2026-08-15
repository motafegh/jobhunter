# Capability v8 Live Review and v9 Semantic Boundary

**Date:** 2026-08-15  
**Branch:** `main`  
**Status:** v8 live mechanics PASS; v8 semantics NOT ACCEPTED; v9 candidate deterministic gate PASS

## 1. Live v8 result

The dense `tG9K` Capability v8 candidate completed against accepted English P1.6 artifact **36** using model `gemma-4-e2b-it`.

```text
Contract: job-capability-intelligence-v8 / job-capability-intelligence-v4
Capability requirements linked: 31/31
Responsibilities linked: 8/8
Role-level requirement indices: [31, 32]
Profiles: 4
```

This is the first promoted-P1.6 dense Capability run to close the complete source-link ledger mechanically. The staged source-led architecture therefore fixed the stable v7 one-shot coverage failure class.

## 2. Depth-accounting clarification

The v8 review surface reported:

```text
Explicit depth represented in profiles: 5/6
```

That is misleading rather than a missing technical-depth defect.

Accepted P1.6 artifact 36 has six explicit-depth requirements total. Five are capability-relevant technical/application depth facts and are linked into profiles. The sixth is requirement 31, the role-level `three to six years` professional-experience constraint. Requirement 32 is the Master's-degree role-level constraint.

V7/v8 inherited source-truth accounting intersected all explicit-depth indices with capability-profile links, so the deliberately separate role-level experience depth appeared falsely "unlinked".

The correct distinction is:

```text
capability explicit depth represented: 5/5
role-level explicit depth retained separately: 1
all explicit depth retained in source truth: 6/6
```

V9 changes the source-truth schema so these categories are explicit instead of conflated.

## 3. Why v8 is not semantically accepted

Although source coverage was complete, the model-owned reasoning introduced downstream inflation that P1.6 did not authorize. Representative failure classes from the live result:

- role interpretation added `advanced` ML/DL depth;
- a profile described an `end-to-end lifecycle` without source ownership evidence;
- contextual ML/DL framework facts were summarized as `proficiency` / `expertise`;
- contextual analytical tools were described as `necessitated`;
- MLOps reasoning expanded into `managing the full lifecycle`;
- preferred C/C++ was promoted into a necessary technical foundation;
- preferred industrial/edge deployment was described as a required ability/focus;
- semiconductor context was escalated to `deep domain knowledge` / `expertise`.

These are not source-link bookkeeping errors. They are semantic authority violations: downstream reasoning became more authoritative than accepted P1.6 strength/depth/scope.

Therefore:

```text
v8 mechanical coverage: PASS
v8 semantic acceptance: FAIL / NOT ACCEPTED
v8 public promotion: BLOCKED
```

The persisted v8 artifact remains historical candidate evidence and must not be rewritten or deleted merely to reuse its identity.

## 4. V9 correction

Capability v9 keeps the successful v8 staged architecture but adds a stricter semantic boundary and a new persistence identity:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

Architecture remains:

```text
accepted P1.6 source truth
→ compact semantic group plan
→ bounded exact source-fact assignment
→ bounded per-group reasoning
→ deterministic source-link injection
→ strict whole-artifact reconciliation
```

V9 adds general, non-vacancy-specific rules:

1. Ordinary model-owned prose cannot restate requirement obligation (`required`, `must`, `mandatory`, `necessary`, `prerequisite`, etc.).
2. Ordinary model-owned prose cannot invent technical depth (`advanced`, `expertise`, `proficiency`, `mastery`, `strong`, `solid`, `hands-on`, `deep`), while preserving the legitimate term `deep learning`.
3. Ordinary model-owned prose cannot infer unsupported ownership/scope (`end-to-end`, `full lifecycle`, ownership, autonomy, leadership, architecture).
4. Only the explicit `depth_signals` section may add genuinely work-implied depth reasoning.
5. A `model_inferred_prerequisite` cannot be grounded only in a preferred/contextual fact unless the same normalized concept has an independent required basis.
6. Source-truth depth accounting now separates capability depth from role-level depth.

V9 does not change accepted P1.6 artifact 36 and does not overwrite/reuse the v8 candidate artifact.

## 5. Deterministic gate

CI run **832** on the v9 candidate passed:

```text
Ruff:               PASS
full pytest:         PASS
warnings-as-errors: PASS
```

Regression tests cover:

- proper `deep learning` wording remains valid while unsupported `advanced` depth is rejected;
- ownership/lifecycle inflation is rejected;
- obligation inflation is rejected;
- preferred/contextual-only prerequisite promotion is rejected;
- role-level experience depth is separated from capability-depth coverage;
- v9 persists under a distinct prompt/schema identity;
- the v9 inference adapter supplies assigned source facts to bounded profile validation.

## 6. Current gate

Run the isolated v9 candidate on dense `tG9K` and inspect both mechanical and semantic output before any public Capability promotion.

Expected mechanical invariants:

```text
English analysis artifact: 36
Capability requirements linked: 31/31
Responsibilities linked: 8/8
Capability explicit depth represented: 5/5
All explicit depth facts retained in source truth: 6/6
Role-level explicit depth facts: 1
Role-level requirement indices: [31, 32]
```

The live semantic review must additionally confirm that model-owned reasoning no longer inflates source obligation, technical depth, ownership/lifecycle scope, or preferred/contextual facts.

Do not change the public `jobhunter jobs capability` route until this candidate is accepted.
