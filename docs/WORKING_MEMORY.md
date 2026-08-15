# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-15  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** Capability v9 public promotion implemented + CI PASS; local operational verification pending

## 1. Exact current point

English P1.6 v20/v5 is fully promoted and operationally verified:

```text
tG9K → P1.6 artifact 36 → ACCEPTED / CURRENT
t4jp → P1.6 artifact 37 → ACCEPTED / CURRENT
```

Capability v9 passed both opposite-end bounded semantic anchors:

```text
tG9K → Capability artifact 11 → ACCEPTED
t4jp → Capability artifact 12 → ACCEPTED WITH ACCEPTABLE DIFFERENCES
```

The public/current Capability facade has now been promoted in code to:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

Deterministic promotion CI passed. The remaining gate is local operational verification that normal commands reuse artifacts 11/12 and Review Snapshot marks the v9 chain current.

Blueprint remains deferred/non-authoritative and is explicitly pinned to historical Capability v7 so this promotion does not silently rebase Blueprint.

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

Dense `tG9K` mechanically reached 31/31 capability requirements and 8/8 responsibilities, proving the staging architecture solved v7 coverage/linkage. V8 remained semantically rejected because model prose inflated depth, ownership/lifecycle scope, and preferred/contextual facts.

### v9 — accepted and promoted in code

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

## 6. Accepted Capability v9 artifacts

Dense artifact 11:

```text
P1.6 dependency:                        36
Capability requirements linked:         31/31
Responsibilities linked:                8/8
Capability explicit depth:              5/5
All explicit depth facts:               6/6
Role-level indices:                     [31, 32]
Disposition:                            ACCEPTED
```

Sparse artifact 12:

```text
P1.6 dependency:                        37
Capability requirements linked:         8/8
Responsibilities linked:                0/0
Capability explicit depth:              0/0
All explicit depth facts:               0/0
Role-level indices:                     []
Disposition:                            ACCEPTED WITH ACCEPTABLE DIFFERENCES
```

Sparse restraint passed: no responsibilities, role purpose, depth, experience, education, prerequisites, or model-derived duties were fabricated. Mild broadening in non-authoritative group prose was recorded rather than patched because it did not alter deterministic source truth.

## 7. Capability v9 public promotion implementation

The neutral/current facade `src/jobhunter/capability_service.py` now exports/builds v9/v5. Existing public consumers already depend on this neutral facade, so the switch aligns:

```text
CLI
browser Capability view
Review Snapshot current-chain selection
other current Capability consumers
```

Historical versioned modules/artifacts remain intact.

Blueprint v6 is intentionally isolated by importing Capability v7 contract constants directly. A compare against the pre-promotion Blueprint file confirmed that isolation is only a one-line dependency import change; no Blueprint prompt/schema/inference/persistence logic changed.

Promotion regression coverage locks:

- current Capability prompt/schema = v9/v5;
- current service uses the v9 boundary;
- current formatter is the v9 formatter;
- deferred Blueprint v6 remains pinned to v7.

The old current-service tests were migrated from a one-shot v7 fake-provider fixture to deterministic staged v9 responses while preserving the actual invariants: exact P1.6 dependency, deterministic source truth, persistence/reuse, and fail-closed invalid output.

Deterministic promotion gate:

```text
CI 874
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

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
Capability v9 artifact 11           DENSE ACCEPTED
Capability v9 artifact 12           SPARSE ACCEPTED WITH ACCEPTABLE DIFFERENCES
Capability public code route         v9/v5 / CI PASS
Capability operational promotion     VERIFICATION PENDING
Blueprint                            DEFERRED / PINNED TO HISTORICAL v7
Heterogeneous role review            NEXT AFTER OPERATIONAL VERIFICATION
Phase 2                              BLOCKED
```

## 9. Exact next action

Do not generate new Capability candidates for `tG9K` or `t4jp`.

Pull `main`, then verify the normal public path:

```bash
jobhunter jobs capability tG9K
jobhunter jobs capability t4jp

jobhunter jobs snapshot tG9K
jobhunter jobs snapshot t4jp
```

Expected:

```text
tG9K → reuse Capability artifact 11 → v9/v5 → P1.6 artifact 36
t4jp → reuse Capability artifact 12 → v9/v5 → P1.6 artifact 37
```

Review Snapshot must identify those Capability artifacts as current for their dependency chains. Blueprint must remain deferred and must not be silently regenerated/rebased on v9.

Only after this operational proof mark Capability v9 promotion closed and resume heterogeneous Python/software, network/security, and operations/platform/DevOps live review before broader Phase-2 use.

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
