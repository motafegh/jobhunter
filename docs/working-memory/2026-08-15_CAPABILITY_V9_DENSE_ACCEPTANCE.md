# Capability v9 Dense Acceptance

**Date:** 2026-08-15  
**Branch:** `main`  
**Status:** dense `tG9K` Capability v9 ACCEPTED; sparse non-regression and public promotion still pending

## 1. Accepted live artifact

The isolated Capability v9 candidate completed successfully for dense job `tG9K` and persisted a new artifact:

```text
Capability artifact:          11
Capability model:             gemma-4-e2b-it
Capability contract:          job-capability-intelligence-v9
Capability schema:            job-capability-intelligence-v5
English P1.6 dependency:      artifact 36
```

This is the first Capability candidate built from promoted English P1.6 artifact 36 that passes both the complete deterministic source-truth gate and the bounded dense semantic review.

## 2. Mechanical acceptance

Observed live result:

```text
Capability requirements linked:            31/31
Responsibilities linked:                   8/8
Capability explicit depth represented:     5/5
All explicit depth facts retained:          6/6
Role-level explicit depth facts:            1
Role-level requirement indices:             [31, 32]
```

Role-level constraints remained separate:

```text
[31] Professional experience | required | depth=three to six years
[32] Master's degree         | required | depth=none
```

Mechanical disposition: **PASS**.

The staged architecture therefore now has live evidence for the full dense chain:

```text
accepted P1.6 source truth
→ semantic group plan
→ bounded exact source-fact assignment
→ bounded per-group reasoning
→ deterministic source-link injection
→ strict final reconciliation
→ persisted v9 artifact
```

## 3. Accepted capability grouping

The persisted dense artifact contains four coherent capability areas:

```text
1. Industrial AI/ML Modeling
2. Sensor Data & Time-Series Analysis
3. Manufacturing Analytics & Optimization
4. ML Engineering & MLOps
```

Role interpretation:

```text
The role combines Industrial AI/ML Modeling, Sensor Data & Time-Series Analysis,
Manufacturing Analytics & Optimization, and ML Engineering & MLOps.
```

The dense job no longer collapses into one catch-all capability profile.

## 4. Semantic acceptance

### 4.1 Source-owned strength/depth remain authoritative

All persisted displayed depth signals are `source_explicit` and state that they were deterministically propagated from accepted P1.6 requirements. Representative preserved facts include:

```text
Strong    → applying AI/ML to semiconductor/comparable industrial data
Comfort   → high-dimensional time-series/sensor/metrology data and noise
Solid     → statistics and signal-processing fundamentals
Hands-on  → process control/manufacturing analytics/yield/fault-anomaly work
expert    → Python
```

No model-derived depth statement survived as authoritative source depth.

### 4.2 Source responsibilities remain deterministic

All displayed work activities are `source_explicit` and deterministically propagated from accepted P1.6 responsibilities, including:

- building and validating ML/AI models on semiconductor process/equipment/manufacturing data;
- yield optimization, APC/SPC, FDC, and anomaly-detection work;
- handling high-volume/high-dimensional sensor/trace/metrology data;
- robust pipeline work;
- problem framing with the technical team;
- rigorous validation and monitoring in an industrial setting;
- partnering to move models toward production;
- traceability, reproducibility, and governance.

No unsupported ownership, autonomy, leadership, or full-lifecycle claim survived as authoritative work truth.

### 4.3 Optional model enrichment behaved fail-closed

The live artifact records that JobHunter:

- normalized non-authoritative planner prose when it crossed strength/depth/scope wording boundaries;
- filtered redundant/misplaced `source_explicit` model echoes;
- replaced one model-expanded profile summary with the validated group summary;
- discarded optional model-derived expectations that crossed v9 semantic guardrails.

This is the intended v9 behavior:

```text
bad optional inference         → filter
redundant source-truth echo    → filter
planner prose inflation        → normalize
no optional enrichment         → valid
authoritative source defect    → fail closed
```

The completed artifact demonstrates that v9 can preserve useful grouping while refusing unsafe optional elaboration.

### 4.4 Preferred/contextual facts were not promoted into authoritative requirement strength

The final profiles report `Strength: mixed` where groups contain facts of different source strengths. The accepted authoritative requirement strength remains in deterministic source truth; no surviving model-owned statement declares preferred/contextual facts to be employer-required.

This corrects the key semantic failure class observed in v8.

## 5. Non-blocking observation

Some model-owned capability summaries synthesize linked source facts using active phrasing such as `applying Deep Learning` or `deploy ... models`.

These summaries are accepted for this bounded dense artifact because:

1. they do not assert `required`, `must`, `mandatory`, invented depth, ownership, or lifecycle breadth;
2. the underlying linked source facts support those topics/scope;
3. the profile is explicitly shown as `Strength: mixed` where applicable;
4. authoritative source strength/depth/work remains separate and deterministic.

However, these summaries remain **non-authoritative synthesis**. Future UI/reporting should not treat them as substitutes for per-fact required/preferred/contextual source truth.

This is an observation, not a blocker for dense acceptance.

## 6. Dense acceptance decision

```text
Mechanical provenance / coverage:    PASS
Role-level separation:                PASS
Source-explicit depth preservation:   PASS
Source responsibility preservation:  PASS
No authoritative strength inflation: PASS
No unsupported ownership inflation:  PASS
Optional-enrichment fail-closed path: PASS
Dense semantic grouping:              PASS
```

Decision:

**Capability v9 artifact 11 is ACCEPTED for bounded dense `tG9K`.**

This does **not** yet authorize public promotion.

## 7. Next gate

Run the isolated sparse candidate against accepted sparse P1.6 artifact 37:

```bash
cd ~/projects/jobhunter
git pull --ff-only origin main
python scripts/run_capability_v9_candidate.py --job-id t4jp
```

Sparse acceptance must verify restraint:

- dependency on P1.6 artifact 37;
- all capability-relevant sparse requirements linked;
- no fabricated responsibilities;
- no role-purpose invention;
- no strength/depth promotion;
- no forced capability proliferation;
- zero optional enrichment is acceptable;
- contextual/ambiguous source facts remain contextual/ambiguous rather than becoming prerequisites.

Only after sparse non-regression should JobHunter decide whether Capability v9 is ready to replace public v7 routing.
