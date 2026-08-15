# JobHunter Semantic Quality Acceptance Plan

**Status:** Active bounded acceptance plan  
**Date:** 2026-08-15  
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

Capability public code route: job-capability-intelligence-v9 / job-capability-intelligence-v5
Review Snapshot:              job-review-snapshot-v1
```

Capability v9 public-promotion implementation has deterministic CI acceptance. Local normal-path operational verification is still pending before the promotion is called fully closed.

Historical Capability contracts remain reproducible:

```text
v7: job-capability-intelligence-v7 / job-capability-intelligence-v4
v8: job-capability-intelligence-v8 / job-capability-intelligence-v4
```

Blueprint remains experimental/deferred:

```text
role-capability-blueprint-v6 / role-capability-blueprint-v5
```

Blueprint v6 is explicitly pinned to historical Capability v7 during the Capability v9 promotion. Blueprint is **not** an accepted Phase-1 decision layer.

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

**Status: accepted foundation; Capability v9 operational recheck pending.**

Normal workflow:

```bash
jobhunter jobs snapshot <job-id>
```

The exporter records dependency/model identities and current-chain status while excluding raw model prompts/responses, SQLite, secrets, logs, and future private state.

Current promotion verification must prove:

- `tG9K` snapshot selects Capability artifact 11 as current on P1.6 artifact 36;
- `t4jp` snapshot selects Capability artifact 12 as current on P1.6 artifact 37;
- contract is v9/v5;
- historical v7/v8 remain non-current;
- Blueprint is not silently rebased on v9.

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

**Status: v9 bounded semantic acceptance COMPLETE; public code promotion CI PASS; operational verification pending.**

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
Blueprint v6                      → remains pinned to historical v7
```

Deterministic promotion gate:

```text
CI 874
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

Operational close requires normal commands to reuse artifacts 11/12 and snapshots to mark those exact v9 artifacts current.

Decision records:

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_DENSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_SPARSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_PUBLIC_PROMOTION.md
```

## 7. SQ-3 — Blueprint experiment disposition

**Status: concluded for Phase 1 / not accepted / further tuning deferred.**

The Blueprint experiment demonstrated that even mechanically valid professional interpretation could smuggle assumptions about architecture, topology, automation, platforms, or ownership.

Phase-1 decision:

- do not create a new Blueprint version during the Capability promotion;
- do not weaken Blueprint validators;
- do not promote Blueprint into Market/personal/recommendation truth;
- keep historical Blueprint artifacts as experimental evidence;
- keep Blueprint v6 pinned to historical v7 dependency semantics until a separate explicit reopening decision.

## 8. SQ-4 — Capability v9 operational promotion verification — ACTIVE

Run:

```bash
jobhunter jobs capability tG9K
jobhunter jobs capability t4jp

jobhunter jobs snapshot tG9K
jobhunter jobs snapshot t4jp
```

Acceptance criteria:

```text
tG9K capability → artifact 11 → reused → v9/v5 → P1.6 36
t4jp capability → artifact 12 → reused → v9/v5 → P1.6 37
```

Snapshots must mark those exact artifacts current. No fresh Capability generation should occur for unchanged accepted dependencies.

After this proof, mark Capability v9 public promotion closed.

## 9. SQ-5 — Heterogeneous live semantic acceptance — NEXT

After operational promotion closes, validate materially different jobs:

```text
Python/software
network/security
operations/platform/DevOps
```

For each role:

1. verify current P1.6 dependency and source truth;
2. verify Capability coverage/provenance;
3. review source optionality and depth calibration;
4. ensure no fabricated responsibilities, role constraints, ownership, or architecture;
5. distinguish repeatable deterministic defects from local-model limitations;
6. convert repeatable deterministic defects into fixtures;
7. preserve acceptable model variation when authoritative source truth remains correct.

Only after heterogeneous acceptance should promoted P1.6 + Capability be considered stable Phase-2 input.

## 10. Phase-2 gate

Do not begin corpus-wide Phase 2 until:

```text
P1.6 promotion closed
+ Capability v9 operational promotion closed
+ heterogeneous semantic review accepted
+ remaining Phase-1 workflow/source/market truthfulness gates closed
```

Blueprint remains non-authoritative unless separately reopened by evidence and explicit decision.
