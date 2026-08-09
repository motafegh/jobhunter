# Capability v6 Deterministic Reconciliation Experiment

**Status:** Rejected after live B3 semantic review; superseded by Capability v7/v4  
**Date:** 2026-08-09  
**Accepted upstream anchor:** `tG9K` English P1.6 artifact 29  
**Live artifact:** Capability artifact 8

## Purpose

Capability v6 tested a stronger deterministic/model boundary after Capability v4 omitted explicit
depth and over-strengthened contextual stack/ownership claims.

Reserved identity:

```text
Capability prompt/runtime: job-capability-intelligence-v6
Capability schema:         job-capability-intelligence-v3
```

A historical prompt-heavy v5 experiment had already failed by exhausting the bounded output budget,
so v6 deliberately did not reuse v5.

## What v6 changed

Each capability profile supplied:

```text
source_requirement_indices
source_responsibility_indices
```

After model generation JobHunter deterministically:

- derived `requirement_strength` from linked accepted P1.6 requirement types;
- copied linked accepted P1.6 `depth_signal` values into source-explicit Capability depth entries;
- validated source indices and exact evidence grounding.

This mechanism worked correctly for facts the model actually linked.

## Live `tG9K` result

The v6 live generation completed and persisted Capability artifact 8 against accepted English P1.6
artifact 29.

Mechanical wins:

- dependency chain was correct;
- v6/v3 identity was correct;
- deterministic requirement-strength reconciliation worked;
- linked `Strong` and `Hands-on` depth signals were propagated exactly;
- stale Blueprint remained excluded from the current chain.

Semantic failures:

- only 3 of 27 accepted requirements were linked;
- only 2 of 7 accepted responsibilities were linked;
- Python `expert`, statistics `Solid`, time-series `Comfort`, and role-level duration evidence were
  therefore absent from the profile-level capability view;
- the model again inferred unsupported autonomy from partnership language;
- the model again inferred end-to-end ML lifecycle ownership from pipelines/MLOps/deployment;
- the dense role collapsed into one catch-all capability;
- exact evidence could still be semantically irrelevant to a derived claim;
- contextual tools/cloud wording was still strengthened in prose.

B3 therefore did **not** pass.

## Lesson

The v6 boundary was still too model-dependent:

```text
v6
model decides which accepted P1.6 facts survive into profile links
        ↓
JobHunter reconciles only surviving linked facts
```

That means a structurally valid artifact can still lose accepted source truth through incomplete
model linkage.

The next boundary must instead be:

```text
JobHunter preserves complete accepted P1.6 truth
        ↓
model groups and reasons above it
```

That design is Capability v7/v4 and is documented in:

```text
docs/experiments/2026-08-09_CAPABILITY_V7_SOURCE_TRUTH_BOUNDARY.md
```

Do not reuse v6 as the current Capability contract. Keep this file as historical experiment
evidence.
