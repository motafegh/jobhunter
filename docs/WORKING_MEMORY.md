# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-16  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** Capability v9 public promotion CLOSED; heterogeneous live semantic validation is next

## 1. Exact current point

English P1.6 v20/v5 is fully promoted and operationally verified:

```text
tG9K → P1.6 artifact 36 → ACCEPTED / CURRENT
t4jp → P1.6 artifact 37 → ACCEPTED / CURRENT
```

Capability v9 passed both opposite-end bounded semantic anchors and is now fully promoted through the normal public path:

```text
tG9K → Capability artifact 11 → ACCEPTED / CURRENT
t4jp → Capability artifact 12 → ACCEPTED WITH ACCEPTABLE DIFFERENCES / CURRENT
```

Public/current Capability contract:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

Normal `jobhunter jobs capability` commands reuse artifacts 11/12. Review Snapshot marks both artifacts current against P1.6 artifacts 36/37. Blueprint remains `blueprint_current=False`, deferred/non-authoritative, and pinned to historical Capability v7 semantics.

The next active gate is heterogeneous live semantic validation across materially different role families before treating promoted P1.6 + Capability as stable Phase-2 input.

## 2. Repository workflow rule

JobHunter uses **main-only development** by default:

```text
current work → main
next work    → main
```

Do not create a new working branch unless the user explicitly changes this rule.

## 3. Current contracts

```text
parser:                     jobinja-detail-v2
translation:                lm-studio-translation-v2
English projection:         english-projection-v2
English P1.6 public:        job-analysis-english-v20 / job-analysis-v5
Original P1.6 public:       job-analysis-original-v9 / job-analysis-v4
Capability public/current:  job-capability-intelligence-v9 / job-capability-intelligence-v5
Capability v7 historical:   job-capability-intelligence-v7 / job-capability-intelligence-v4
Capability v8 historical:   job-capability-intelligence-v8 / job-capability-intelligence-v4
Blueprint deferred:         role-capability-blueprint-v6 / role-capability-blueprint-v5
Review Snapshot:            job-review-snapshot-v1
```

## 4. P1.6 v20 — PROMOTED / CLOSED

Dense `tG9K` artifact 36:

```text
Requirements:      33
Responsibilities:  8
Role purpose:      0
Mechanical audit:  PASS
Semantic review:   PASS WITH ACCEPTABLE DIFFERENCE
```

Sparse `t4jp` artifact 37:

```text
Requirements:            8
Responsibilities:        0
Role purpose:            0
Mechanical audit:        PASS
Semantic non-regression: PASS
```

Normal P1.6 commands reuse artifacts 36/37.

## 5. Capability history

### v7 — historical baseline / promoted-chain rebuild rejected

Historical accepted artifact 9 depends on old P1.6 artifact 29. Dense rebuilds against current P1.6 failed through source-link/index loss and then one-profile collapse with 22 capability requirements omitted. Do not reopen the v7 one-shot architecture.

### v8 — staged architecture proof / semantic reject

V8 introduced:

```text
accepted P1.6 source truth
→ semantic group plan
→ bounded exact assignment
→ bounded per-group reasoning
→ deterministic source-link injection
→ strict reconciliation
```

Dense `tG9K` mechanically reached 31/31 capability requirements and 8/8 responsibilities, proving staging solved v7 coverage/linkage. V8 remained semantically rejected because model prose inflated depth, ownership/lifecycle scope, and preferred/contextual facts.

### v9 — accepted / promoted / operationally closed

Four pre-persistence live failures exposed over-enforcement and contradictions:

1. one unsafe optional inference killed the whole profile;
2. forced enrichment contradicted `do not speculate`;
3. planner prose wording was over-policed even when group structure was useful;
4. model `source_explicit` echoes were rejected even though deterministic reconciliation already owned those facts.

Final policy:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

Hard boundaries still include complete source coverage, valid indices, grounded evidence, deterministic source strength/depth/work, role-level separation, anti-collapse protection, and no persistence with incomplete authoritative truth.

## 6. Accepted/current Capability v9 artifacts

Dense artifact 11:

```text
P1.6 dependency:                        36
Capability requirements linked:         31/31
Responsibilities linked:                8/8
Capability explicit depth:              5/5
All explicit depth facts:               6/6
Role-level indices:                     [31, 32]
Disposition:                            ACCEPTED / CURRENT
```

Sparse artifact 12:

```text
P1.6 dependency:                        37
Capability requirements linked:         8/8
Responsibilities linked:                0/0
Capability explicit depth:              0/0
All explicit depth facts:               0/0
Role-level indices:                     []
Disposition:                            ACCEPTED WITH ACCEPTABLE DIFFERENCES / CURRENT
```

Sparse restraint passed: no responsibilities, role purpose, depth, experience, education, prerequisites, or model-derived duties were fabricated. Mild broadening in non-authoritative group prose was recorded rather than patched because it did not alter deterministic source truth.

## 7. Capability v9 public promotion — CLOSED

The neutral/current facade `src/jobhunter/capability_service.py` exports/builds v9/v5. CLI, browser Capability view, Review Snapshot, and other current Capability consumers follow this neutral facade.

Historical versioned modules/artifacts remain intact. Blueprint v6 is explicitly isolated by importing historical Capability v7 constants directly.

Deterministic promotion gate:

```text
CI 874
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

Final documentation/governance reconciliation also passed CI 878.

Operational verification on 2026-08-16:

```text
tG9K
normal Capability outcome: reused
contract: v9/v5
analysis artifact: 36
snapshot current=True
snapshot Capability artifact=11
snapshot analysis=36
blueprint_current=False

t4jp
normal Capability outcome: reused
contract: v9/v5
analysis artifact: 37
snapshot current=True
snapshot Capability artifact=12
snapshot analysis=37
blueprint_current=False
```

No fresh Capability generation occurred for either accepted current dependency chain.

Detailed record:

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_PUBLIC_PROMOTION.md
```

## 8. Exact current state

```text
English P1.6 tG9K artifact 36       ACCEPTED / CURRENT
English P1.6 t4jp artifact 37       ACCEPTED / CURRENT
Capability v7 artifact 9            HISTORICAL / NON-CURRENT CHAIN
Capability v8 candidate              HISTORICAL / SEMANTIC REJECT
Capability v9 artifact 11           DENSE ACCEPTED / CURRENT
Capability v9 artifact 12           SPARSE ACCEPTED / CURRENT
Capability public route              v9/v5 / OPERATIONALLY VERIFIED
Blueprint                            DEFERRED / PINNED TO HISTORICAL v7 / NON-CURRENT
Heterogeneous role review            ACTIVE NEXT GATE
Phase 2                              BLOCKED
```

## 9. Exact next action

Do not rerun `tG9K` or `t4jp` Capability unless a dependency changes or a repeatable correctness defect requires explicit re-evaluation.

Begin heterogeneous live semantic validation on materially different current jobs, in this order unless evidence suggests a better available anchor:

```text
1. Python/software role
2. network/security role
3. operations/platform/DevOps role
```

For each role:

1. confirm current source + English P1.6 chain;
2. generate/reuse public Capability v9 through the normal path;
3. audit complete source coverage/provenance;
4. inspect required/preferred/contextual strength and explicit depth calibration;
5. check for fabricated responsibilities, role constraints, prerequisites, ownership, lifecycle, architecture, or autonomy;
6. distinguish deterministic defects from acceptable model variation/local-model limitations;
7. convert repeatable deterministic defects into regression fixtures;
8. avoid v9 contract changes for harmless non-authoritative wording differences.

Only after heterogeneous acceptance should promoted P1.6 + Capability be considered stable Phase-2 input.

## 10. Relevant records

```text
docs/working-memory/2026-08-15_CAPABILITY_V7_PROMOTED_P16_LINKAGE_FAILURE.md
docs/working-memory/2026-08-15_CAPABILITY_V8_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-15_CAPABILITY_V8_LIVE_REVIEW_AND_V9_BOUNDARY.md
docs/working-memory/2026-08-15_CAPABILITY_V9_DERIVED_EXPECTATION_FILTERING.md
docs/working-memory/2026-08-15_CAPABILITY_V9_LIVE_FAILURES_AND_DESIGN_PAUSE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_STRICTNESS_AUDIT_AND_SIMPLIFICATION.md
docs/working-memory/2026-08-15_CAPABILITY_V9_DENSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_SPARSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_PUBLIC_PROMOTION.md
```
