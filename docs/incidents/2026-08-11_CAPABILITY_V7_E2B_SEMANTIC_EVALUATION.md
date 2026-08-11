# Capability v7 E2B Semantic Evaluation

**Status:** B3 semantic acceptance failed on E2B; v7 structural/source-truth boundary retained  
**Date:** 2026-08-11  
**Live review commit:** `97e78bc5447e57cbf3d93d18b812ce3e27f5c5b0`  
**Accepted upstream anchor:** `tG9K` English P1.6 artifact 29  
**Capability contract:** `job-capability-intelligence-v7` / `job-capability-intelligence-v4`  
**Capability model:** `gemma-4-e2b-it`

## Decision

Do **not** accept B3 on the E2B result.

The v7 architecture materially fixes the previous source-loss/provenance problem and should be retained. The remaining failure is semantic synthesis by the current E2B capability model. The next action is a controlled same-contract comparison using the already-available E4B model as the Capability role while holding source, English projection, accepted P1.6 artifact, v7 prompt/schema, deterministic reconciliation, and review rubric fixed.

Do not add another prompt-patch collection before that comparison.

## What passed

The live v7 artifact is mechanically and structurally much stronger than v6:

- `tG9K` remained anchored to accepted English P1.6 artifact 29;
- Capability artifact 9 used v7/v4 and `gemma-4-e2b-it`;
- all 25 capability-relevant requirements were linked (`25/25`);
- all 7 responsibilities were linked (`7/7`);
- complete accepted P1.6 requirements/responsibilities are preserved in JobHunter-owned `source_truth`;
- six explicit depth facts are preserved in `source_truth`;
- five capability-level explicit depth facts are deterministically projected into profiles;
- professional experience (`three to six years`) remains preserved as a role-level requirement instead of disappearing;
- dense-source decomposition produced two capability profiles instead of the v6 one-profile collapse;
- positive `independence_expectation` is absent;
- `cross_capability_observations` is empty;
- source-explicit work activities are deterministically reconstructed;
- the repository-native v7 audit passed;
- Blueprint remains outside the current chain;
- push CI for review commit `97e78bc` passed.

This means v7 successfully removes the model's authority to decide whether accepted upstream facts survive downstream.

## Why B3 still fails semantically

### 1. Contextual frameworks are still upgraded to mastery

The accepted P1.6 framework group is contextual:

```text
ML & deep learning: scikit-learn, PyTorch, TensorFlow, XGBoost / LightGBM
requirement_type = contextual
```

The v7 E2B result nevertheless emits:

```text
Programming & Core ML Implementation
Why: Requires expert Python skills and mastery of core ML/DL frameworks (PyTorch, TensorFlow, etc.).
```

Only Python has explicit `expert` depth. The framework group does not. This reproduces a primary v4/v6 B3 failure class and directly violates the v7 calibration rule that contextual/preferred tools are not automatically mastery-level.

### 2. Cloud/edge context is strengthened into actual deployment topology

Accepted P1.6 distinguishes:

```text
Cloud & edge: AWS, GCP, or Azure               -> contextual
industrial / edge deployment a plus           -> preferred
```

The v7 E2B profile summary says:

```text
production deployment on cloud/edge infrastructure
```

and the profile is labeled:

```text
Full-Stack ML Engineering & MLOps
```

This is stronger than the accepted source substrate. Model deployment is contextual; cloud is contextual; industrial/edge deployment is explicitly a plus. The artifact may discuss deployment considerations, but it cannot present cloud/edge production deployment as the actual role topology.

### 3. Contextual fab-system knowledge is phrased as required

Accepted P1.6 records MES / SECS-GEM / equipment-metrology-trace knowledge as contextual. The v7 E2B derived claim states:

```text
Industrial Data Systems Knowledge
Why: Requires familiarity with MES, SECS/GEM, and equipment trace data.
```

`Requires familiarity` upgrades a contextual source fact into mandatory prose. Deterministic `requirement_strength = mixed` does not neutralize this semantic strengthening inside derived text.

### 4. End-to-end/full-stack framing is still too strong

The second capability summary says:

```text
Proficiency in the end-to-end lifecycle of ML projects
```

The source supports robust pipelines, validation/monitoring, moving models toward production, governance, MLOps technologies, and model deployment. It does not explicitly establish full lifecycle ownership or a broad full-stack engineering mandate.

v7 correctly prevents a persisted autonomy/ownership field, but the same overreach can still leak into capability labels and summary prose. That is a model-semantic problem that deterministic source retention alone cannot solve.

### 5. Unknown-scope use remains weak

Both profiles persist empty `unknown_scope` arrays even though the source contains obvious unresolved boundaries, including exact depth for most contextual stack entries, actual cloud/edge deployment topology, exact MLOps depth, and division of implementation responsibility with engineering.

Top-level `uncertainties` partially recognizes tool depth, but the profile-level reasoning surface is still more confident than the evidence warrants.

## Improvements relative to v6

The v7 E2B result should not be treated as equivalent to v6 failure.

v6 failed both structurally and semantically: it lost most accepted P1.6 facts, omitted several explicit depth signals, collapsed the role into one profile, inferred autonomy/end-to-end ownership, and allowed source coverage to depend on model linkage.

v7 fixes those structural defects. The remaining problem is narrower: E2B still writes over-strengthened semantic prose despite receiving the complete source substrate and explicit calibration instructions.

That narrower failure is useful because it makes the next experiment diagnostic rather than another architecture guess.

## Next controlled experiment

Use E4B only for the Capability model while holding everything else fixed:

```text
source job/detail version       fixed
English projection artifact 33 fixed
English P1.6 artifact 29        fixed
Capability prompt v7            fixed
Capability schema v4            fixed
deterministic reconciliation    fixed
audit/rubric                     fixed
Capability model                E2B -> E4B only
```

Evaluate whether E4B removes the E2B failure classes:

- no mastery claim for contextual framework lists;
- no required cloud/edge topology from contextual/preferred evidence;
- no `requires` language that upgrades contextual source facts;
- no unsupported full-stack/end-to-end ownership framing;
- coherent decomposition rather than catch-all stack grouping;
- useful unknown-scope boundaries;
- derived prerequisites remain technically useful and directly grounded.

If E4B passes, configure E4B as the dedicated Capability model and proceed with B3 acceptance evidence. If E4B repeats the same material errors, do not keep prompt-patching; revisit the model-facing semantic output contract or use a more capable reasoning model before Blueprint calibration.
