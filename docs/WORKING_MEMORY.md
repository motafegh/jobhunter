# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-15  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** Capability v9 bounded acceptance COMPLETE; public-promotion implementation is next  

## 1. Exact current point

English P1.6 v20/v5 is fully promoted and operationally verified. Dense `tG9K` P1.6 artifact 36 and sparse `t4jp` P1.6 artifact 37 are current through normal public routing.

Capability v9 has now passed the two opposite-end bounded semantic anchors:

```text
dense tG9K
P1.6 artifact 36
→ Capability v9 artifact 11
→ ACCEPTED

sparse t4jp
P1.6 artifact 37
→ Capability v9 artifact 12
→ ACCEPTED WITH ACCEPTABLE DIFFERENCES
```

Public Capability routing is **still** `job-capability-intelligence-v7 / job-capability-intelligence-v4`. V9 is now eligible for promotion work, but normal routing has not been changed yet.

Blueprint remains deferred and non-authoritative.

## 2. Repository workflow rule

JobHunter uses **main-only development** by default:

```text
current work → main
next work    → main
```

Do not create a new working branch unless the user explicitly changes this rule.

## 3. Public-current and candidate contracts

```text
parser:                             jobinja-detail-v2
translation:                        lm-studio-translation-v2
English projection:                 english-projection-v2
English P1.6 public route:          job-analysis-english-v20 / job-analysis-v5
Original P1.6 public route:         job-analysis-original-v9 / job-analysis-v4
Capability public route:            job-capability-intelligence-v7 / job-capability-intelligence-v4
Capability v8 historical candidate: job-capability-intelligence-v8 / job-capability-intelligence-v4
Capability v9 accepted candidate:   job-capability-intelligence-v9 / job-capability-intelligence-v5
Blueprint experimental:             role-capability-blueprint-v6 / role-capability-blueprint-v5
Review Snapshot:                    job-review-snapshot-v1
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

Normal P1.6 commands already reuse artifacts 36/37.

## 5. Capability history

### v7 — historical/public baseline

Historical accepted artifact 9 depends on old P1.6 artifact 29. Two attempts to rebuild the dense promoted chain under v7 failed: first through source-link/index loss, then through one-profile collapse with 22 capability requirements omitted. Do not reopen the v7 one-shot architecture.

### v8 — mechanical proof / semantic reject

V8 introduced source-led staging:

```text
accepted P1.6 source truth
→ semantic group plan
→ bounded exact assignment
→ bounded per-group reasoning
→ deterministic source-link injection
→ strict reconciliation
```

Dense `tG9K` completed mechanically with 31/31 capability requirements and 8/8 responsibilities, proving the staged architecture fixed v7 coverage/linkage. V8 was rejected semantically because model prose inflated depth, ownership/lifecycle scope, and preferred/contextual facts.

### v9 — accepted bounded candidate

V9 kept the staged architecture but corrected semantic authority. Four live pre-persistence failures exposed over-enforcement and contradictions:

1. whole-profile failure for one unsafe optional inference;
2. forced enrichment (`must add derived reasoning or unknown_scope`) contradicting `do not speculate`;
3. planner prose over-policing that rejected useful group structure;
4. model `source_explicit` echoes rejected even though deterministic reconciliation already owns those facts.

The final v9 policy is:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

Hard rules retained:

- complete capability-relevant requirement coverage;
- complete responsibility coverage;
- valid/owned source indices;
- grounded evidence only;
- dense anti-collapse protection;
- role-level education/duration-only experience separation;
- source requirement strength is deterministic;
- source-explicit depth is deterministic;
- source work activities are deterministic;
- preferred/contextual-only facts cannot independently become inferred prerequisites;
- unsupported ownership/lifecycle/autonomy/architecture analytical claims are rejected/filtered;
- incomplete authoritative source truth cannot persist.

## 6. Dense v9 acceptance — artifact 11

```text
Contract:                                  v9 / schema v5
P1.6 dependency:                           artifact 36
Capability requirements linked:            31/31
Responsibilities linked:                   8/8
Capability explicit depth represented:     5/5
All explicit depth facts retained:          6/6
Role-level requirement indices:             [31, 32]
Semantic disposition:                       ACCEPTED
```

Accepted groups:

```text
Industrial AI/ML Modeling
Sensor Data & Time-Series Analysis
Manufacturing Analytics & Optimization
ML Engineering & MLOps
```

All displayed depth/work truth is deterministic `source_explicit`. Unsafe optional model enrichment was filtered. Model-owned summaries remain non-authoritative synthesis and must not replace per-fact required/preferred/contextual truth.

Detailed record:

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_DENSE_ACCEPTANCE.md
```

## 7. Sparse v9 acceptance — artifact 12

```text
Contract:                                  v9 / schema v5
P1.6 dependency:                           artifact 37
Capability requirements linked:            8/8
Responsibilities linked:                   0/0
Capability explicit depth represented:     0/0
All explicit depth facts retained:          0/0
Role-level requirement indices:             []
Semantic disposition:                       ACCEPTED WITH ACCEPTABLE DIFFERENCES
```

Accepted groups:

```text
Artificial Intelligence & Content Generation
Visual Media Production
Digital Presence & Design
Content Strategy & Tools
Professional Conduct
```

Sparse restraint passed: no responsibilities, role purpose, depth, experience, education, prerequisites, or model-derived work were fabricated.

Two mild non-authoritative synthesis differences are recorded rather than patched:

- `Content Strategy & Tools` is broader than exact source wording;
- the website-design summary mentions `managing online platforms` although that is not an explicit assigned source fact.

They do not alter deterministic source truth, strength, depth, duties, or role-level constraints and therefore are not blockers for bounded sparse acceptance.

Detailed record:

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_SPARSE_ACCEPTANCE.md
```

## 8. Deterministic implementation gates

Relevant v9 gates passed:

```text
CI 849  simplified contract                  PASS
CI 855  planner normalization                PASS
CI 862  source-echo filtering                PASS
CI 864  reconciled source-echo state         PASS
CI 866  dense acceptance documentation       PASS
```

Each authoritative implementation gate passed Ruff, full pytest, and warnings-as-errors.

## 9. Exact current state

```text
English P1.6 tG9K artifact 36       ACCEPTED / CURRENT
English P1.6 t4jp artifact 37       ACCEPTED / CURRENT
Capability v7 artifact 9            HISTORICAL / PUBLIC ROUTE / NON-CURRENT CHAIN
Capability v8 dense candidate       HISTORICAL / SEMANTIC REJECT
Capability v9 artifact 11           DENSE ACCEPTED
Capability v9 artifact 12           SPARSE ACCEPTED WITH ACCEPTABLE DIFFERENCES
Capability public route             STILL v7/v4
Capability v9                       BOUNDED ACCEPTANCE COMPLETE / PROMOTION ELIGIBLE
Blueprint                           DEFERRED / NON-AUTHORITATIVE
Heterogeneous role review           NEXT AFTER PROMOTION/OPERATIONAL VERIFICATION
Phase 2                             BLOCKED
```

## 10. Exact next action

Do **not** rerun dense or sparse candidates and do **not** patch v9 based only on the accepted non-authoritative wording differences.

Next work is the controlled public Capability promotion:

```text
accepted v9/v5 candidate
→ align neutral/current Capability facade
→ align CLI + batch + browser + Review Snapshot/current-chain selection
→ preserve historical v7/v8 modules/artifacts
→ deterministic CI
→ operationally verify normal commands reuse artifacts 11 and 12
```

Promotion must not touch Blueprint routing.

After promotion verification, resume heterogeneous live review on materially different Python/software, network/security, and operations/platform/DevOps jobs before broader Phase-2 use.

## 11. Relevant records

```text
docs/working-memory/2026-08-15_CAPABILITY_V7_PROMOTED_P16_LINKAGE_FAILURE.md
docs/working-memory/2026-08-15_CAPABILITY_V8_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-15_CAPABILITY_V8_LIVE_REVIEW_AND_V9_BOUNDARY.md
docs/working-memory/2026-08-15_CAPABILITY_V9_DERIVED_EXPECTATION_FILTERING.md
docs/working-memory/2026-08-15_CAPABILITY_V9_LIVE_FAILURES_AND_DESIGN_PAUSE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_STRICTNESS_AUDIT_AND_SIMPLIFICATION.md
docs/working-memory/2026-08-15_CAPABILITY_V9_DENSE_ACCEPTANCE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_SPARSE_ACCEPTANCE.md
```
