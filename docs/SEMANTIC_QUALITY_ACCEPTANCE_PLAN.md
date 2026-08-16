# JobHunter Semantic Quality Acceptance Plan

**Status:** Active bounded acceptance plan  
**Date:** 2026-08-16  
**Scope:** P1.6 factual extraction, Capability Intelligence, Review Snapshot current-chain verification, heterogeneous semantic review, and the concluded Phase-1 Blueprint experiment  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`, `docs/ROADMAP.md`, and product/domain/source/architecture constraints.

This plan does not authorize corpus-wide Phase-2 taxonomy/Market-v2 work.

## 1. Permanent acceptance principles

Intelligence depth follows evidence density:

```text
sparse evidence
→ modest strong conclusions
→ explicit unknowns only when genuinely supported/useful

rich evidence
→ deeper work-linked decomposition
→ richer supported reasoning
```

Permanent rules:

1. **Mechanical provenance correctness and semantic calibration are separate acceptance gates.**
2. A downstream layer never becomes more authoritative than accepted upstream evidence.
3. Optional/contextual source language must not become mandatory downstream.
4. Explicit depth belongs only to the exact concept the source qualifies.
5. Deterministic source truth is authoritative; model-owned synthesis/enrichment is subordinate.
6. Optional model enrichment may be absent. Do not force speculation to satisfy schema shape.
7. Do not polish model reasoning indefinitely when repeated experiments show a layer is not stable enough for the current phase.
8. Public promotion requires bounded semantic acceptance, deterministic CI, and normal-path operational verification.
9. Once a promoted layer passes those gates, do not reopen it for harmless non-authoritative wording variation; require a repeatable correctness/provenance or contract-level defect.

Current opposite-end anchors:

```text
t4jp  sparse/ambiguous source
tG9K  rich semiconductor/industrial-ML source
```

## 2. Current accepted/public contracts

```text
source parser:                 jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2

English P1.6 public:           job-analysis-english-v20 / job-analysis-v5
Original P1.6 public:          job-analysis-original-v9 / job-analysis-v4

Capability public/current:     job-capability-intelligence-v9 / job-capability-intelligence-v5
Review Snapshot:               job-review-snapshot-v1
```

Capability v9 public promotion is fully closed: bounded dense/sparse semantic acceptance passed, deterministic promotion CI passed, normal public commands reuse accepted artifacts 11/12, and Review Snapshot marks those exact artifacts current on P1.6 artifacts 36/37.

Historical Capability contracts remain reproducible:

```text
v7: job-capability-intelligence-v7 / job-capability-intelligence-v4
v8: job-capability-intelligence-v8 / job-capability-intelligence-v4
```

Blueprint remains experimental/deferred:

```text
role-capability-blueprint-v6 / role-capability-blueprint-v5
```

Blueprint v6 is explicitly pinned to historical Capability v7 semantics and is not current on either accepted v9 anchor. Blueprint is **not** an accepted Phase-1 decision layer.

## 3. Layer authority

Accepted Phase-1 semantic stack:

```text
source/original employer text
→ parsed source fields
→ English projection
→ accepted P1.6 factual extraction
→ accepted Capability grouping + deterministic source truth
```

Authority split inside Capability v9:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

Experimental only:

```text
accepted P1.6 + historical Blueprint-compatible Capability
→ Blueprint professional interpretation
```

Blueprint output must not feed Market, personal readiness, automatic recommendations, or other authoritative Phase-1 decisions.

## 4. SQ-0 — Review Snapshot correctness

**Status: ACCEPTED / CURRENT-CHAIN VERIFIED.**

Normal workflow:

```bash
jobhunter jobs snapshot <job-id>
```

The exporter records dependency/model identities and current-chain status while excluding raw model prompts/responses, SQLite, secrets, logs, and future private state.

Capability v9 promotion verification proved:

```text
tG9K
capability_is_current_chain=True
Capability artifact=11
analysis artifact=36
contract=v9/v5
blueprint_is_current_chain=False

t4jp
capability_is_current_chain=True
Capability artifact=12
analysis artifact=37
contract=v9/v5
blueprint_is_current_chain=False
```

This closes the Capability-era Review Snapshot recheck.

## 5. SQ-1 — P1.6 factual coverage / obligation / depth

**Status: PROMOTED / CLOSED.**

Dense accepted anchor:

```text
job:                       tG9K
English P1.6 artifact:     36
contract:                  job-analysis-english-v20 / job-analysis-v5
requirements:              33
responsibilities:          8
role purpose:              0
semantic disposition:      PASS WITH ACCEPTABLE DIFFERENCE
```

Sparse accepted anchor:

```text
job:                       t4jp
English P1.6 artifact:     37
contract:                  job-analysis-english-v20 / job-analysis-v5
requirements:              8
responsibilities:          0
role purpose:              0
semantic disposition:      PASS
```

Accepted P1.6 invariants include:

- complete deterministic source accounting;
- required/preferred/contextual optionality preserved;
- explicit depth separated from obligation strength;
- Python `expert` remains Python-specific;
- `Strong`, `Hands-on`, `Comfort`, `Solid`, and experience-duration depth preserved where stated;
- MATLAB/C++ remain preferred where stated;
- contextual framework/cloud/tool facts remain contextual;
- education and experience constraints preserved;
- qualification wording does not fabricate responsibilities;
- schedule wording does not become capability depth or prior experience.

Normal public P1.6 routing reuses artifacts 36/37.

## 6. SQ-2 — Capability Intelligence calibration

**Status: PROMOTED / OPERATIONALLY CLOSED.**

Accepted dense anchor:

```text
job:                              tG9K
P1.6 artifact:                    36
Capability artifact:              11
contract:                         job-capability-intelligence-v9 / job-capability-intelligence-v5
capability requirements linked:   31/31
responsibilities linked:          8/8
capability explicit depth:        5/5
all explicit depth:               6/6
role-level indices:               [31, 32]
semantic disposition:             ACCEPTED
current public chain:             YES
```

Accepted sparse anchor:

```text
job:                              t4jp
P1.6 artifact:                    37
Capability artifact:              12
contract:                         job-capability-intelligence-v9 / job-capability-intelligence-v5
capability requirements linked:   8/8
responsibilities linked:          0/0
explicit depth:                   0/0
role-level indices:               []
semantic disposition:             ACCEPTED WITH ACCEPTABLE DIFFERENCES
current public chain:             YES
```

V9 acceptance rules:

- complete capability-relevant requirement and responsibility coverage is mandatory;
- source indices/evidence must be valid and grounded;
- dense jobs cannot collapse all source truth into one group;
- requirement strength, source-explicit depth, and source work activities are deterministic;
- education/duration-only experience remain role-level constraints;
- preferred/contextual-only facts cannot independently become inferred prerequisites;
- unsupported ownership/lifecycle/autonomy/architecture claims are rejected/filtered;
- unsafe optional model items are filtered rather than promoted;
- planner-only wording may normalize without discarding useful grouping structure;
- redundant model `source_explicit` echoes are discarded and re-injected only by deterministic reconciliation;
- zero optional model enrichment is valid;
- incomplete authoritative source truth cannot persist.

Promotion implementation:

```text
neutral/current Capability facade → v9/v5
CLI/browser/Review Snapshot       → follow neutral facade
Blueprint v6                      → pinned to historical v7
```

Deterministic promotion gate:

```text
CI 874
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

Operational proof:

```text
normal tG9K Capability → reused artifact 11 → P1.6 36
normal t4jp Capability → reused artifact 12 → P1.6 37
snapshots → exact artifacts current
fresh Capability generation → none
Blueprint current → false on both anchors
```

Decision records:

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_DENSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_SPARSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_PUBLIC_PROMOTION.md
```

Do not reopen Capability v9 for harmless non-authoritative wording differences. Reopen only if heterogeneous evidence shows a repeatable deterministic/provenance defect, authoritative optionality/depth corruption, fabricated authoritative content, or another contract-level failure.

## 7. SQ-3 — Blueprint experiment disposition

**Status: concluded for Phase 1 / not accepted / further tuning deferred.**

The Blueprint experiment demonstrated that even mechanically valid professional interpretation could smuggle assumptions about architecture, topology, automation, platforms, or ownership.

Phase-1 decision:

- do not create a new Blueprint version during the heterogeneous semantic gate;
- do not weaken Blueprint validators;
- do not promote Blueprint into Market/personal/recommendation truth;
- keep historical Blueprint artifacts as experimental evidence;
- keep Blueprint v6 pinned to historical v7 dependency semantics until a separate explicit reopening decision.

## 8. SQ-4 — Capability v9 operational promotion verification — CLOSED

Verified on the normal public path:

```text
tG9K capability → artifact 11 → reused → v9/v5 → P1.6 36
t4jp capability → artifact 12 → reused → v9/v5 → P1.6 37
```

Review Snapshot verified the exact current chains and `blueprint_current=False` for both anchors. No fresh Capability generation occurred.

## 9. SQ-5 — Heterogeneous live semantic acceptance — ACTIVE NEXT GATE

Validate materially different current jobs:

```text
Python/software
network/security
operations/platform/DevOps
```

For each role:

1. confirm the current source record and accepted/current English P1.6 dependency;
2. run/reuse Capability v9 through the **normal public path**, not a candidate script;
3. verify complete requirement/responsibility coverage and source provenance;
4. review required/preferred/contextual optionality and explicit depth calibration;
5. ensure no fabricated responsibilities, role constraints, prerequisites, ownership, lifecycle, architecture, autonomy, or mandatory strength;
6. distinguish repeatable deterministic defects from local-model limitations or harmless non-authoritative variation;
7. convert repeatable deterministic defects into regression fixtures;
8. preserve acceptable model variation when authoritative source truth remains correct;
9. do not change the v9 contract merely to cosmetically normalize prose.

Only after heterogeneous acceptance should promoted P1.6 + Capability be considered stable Phase-2 input.

## 10. Phase-2 gate

Do not begin corpus-wide Phase 2 until:

```text
P1.6 promotion closed
+ Capability v9 promotion closed
+ heterogeneous semantic review accepted
+ remaining Phase-1 workflow/source/market truthfulness gates closed
```

Blueprint remains non-authoritative unless separately reopened by evidence and explicit decision.
