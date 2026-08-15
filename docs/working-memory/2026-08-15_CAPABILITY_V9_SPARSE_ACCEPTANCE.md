# Capability v9 Sparse Acceptance

**Date:** 2026-08-15  
**Branch:** `main`  
**Status:** sparse `t4jp` Capability v9 ACCEPTED WITH ACCEPTABLE DIFFERENCES; v9 dense+sparse gate complete; public promotion not yet performed

## 1. Accepted live artifact

The isolated Capability v9 candidate completed successfully for sparse job `t4jp` and persisted:

```text
Capability artifact:          12
Capability model:             gemma-4-e2b-it
Capability contract:          job-capability-intelligence-v9
Capability schema:            job-capability-intelligence-v5
English P1.6 dependency:      artifact 37
```

The accepted sparse P1.6 anchor contains exactly eight required requirements, zero responsibilities, zero role purpose, and no explicit depth. This matches the earlier bounded sparse semantic acceptance record.

## 2. Mechanical acceptance

Observed live result:

```text
Capability requirements linked:        8/8
Responsibilities linked:               0/0
Capability explicit depth represented: 0/0
All explicit depth facts retained:      0/0
Role-level explicit depth facts:        0
Role-level requirement indices:         []
```

Mechanical disposition: **PASS**.

No responsibility, role purpose, experience duration, education constraint, or depth signal was invented.

## 3. Sparse capability grouping

The persisted artifact contains five bounded groups:

```text
1. Artificial Intelligence & Content Generation
2. Visual Media Production
3. Digital Presence & Design
4. Content Strategy & Tools
5. Professional Conduct
```

Source links remain complete across the eight sparse P1.6 requirements. Requirement 3 (`Content creation with AI`) is used in two semantically related groups; no source fact is omitted.

## 4. Semantic review

### 4.1 Restraint and source truth

The sparse run exhibits the required restraint:

- all eight accepted sparse requirements remain linked;
- no responsibilities are fabricated from qualification wording;
- no role purpose is invented;
- no technical/professional depth is invented;
- no role-level constraint is invented;
- all displayed group strengths remain `required`, matching the accepted sparse P1.6 facts;
- there are no surviving model-derived depth/work/prerequisite sections;
- planner prose normalization and source-echo filtering occurred without changing authoritative source truth.

This is the important opposite-end proof relative to dense `tG9K`: v9 can preserve rich deterministic source truth on a dense vacancy while also accepting a sparse vacancy without forcing extra analytical enrichment.

### 4.2 Acceptable differences

Two model-owned synthesis phrases are broader than the exact sparse source wording:

1. `Content Strategy & Tools` is broader than the underlying linked facts `Social networks` + `Content creation with AI`.
2. The `Digital Presence & Design` summary says `managing online platforms`, while the directly assigned source fact is `Website design`.

These are classified as **acceptable differences**, not authoritative defects, because:

- they occur only in non-authoritative capability labels/summaries;
- deterministic P1.6 source truth remains complete and unchanged;
- they do not create required/preferred/contextual strength changes;
- they do not add depth, prerequisites, duties, ownership, experience, or education;
- downstream consumers must not substitute summary prose for per-fact source truth.

If future heterogeneous evidence shows that sparse group labels routinely drift into materially new capabilities, that should be treated as a repeatable semantic defect. This one bounded sparse artifact does not justify another v9 contract patch.

## 5. Sparse acceptance decision

```text
P1.6 dependency artifact 37:       PASS
Requirement coverage 8/8:          PASS
Responsibilities 0/0:              PASS
No role-purpose invention:         PASS
No depth invention:                PASS
No role-level invention:           PASS
Source strength preservation:      PASS
Sparse restraint:                  PASS
Semantic grouping:                 PASS WITH ACCEPTABLE DIFFERENCES
```

Decision:

**Capability v9 artifact 12 is ACCEPTED WITH ACCEPTABLE DIFFERENCES for bounded sparse `t4jp`.**

## 6. Dense + sparse v9 disposition

Accepted opposite-end anchors are now:

```text
dense tG9K  → P1.6 artifact 36 → Capability v9 artifact 11 → ACCEPTED
sparse t4jp → P1.6 artifact 37 → Capability v9 artifact 12 → ACCEPTED WITH ACCEPTABLE DIFFERENCES
```

The Capability v9 bounded acceptance gate is therefore complete.

This makes `job-capability-intelligence-v9 / job-capability-intelligence-v5` **eligible for public promotion work**, but this record does not itself change public routing. Public `jobhunter jobs capability` remains v7/v4 until the promotion implementation and operational verification are completed.

## 7. Next gate

Promotion work should align the neutral/current Capability facade and all normal consumers with v9/v5 while preserving historical v7/v8 modules/artifacts. At minimum verify:

- CLI normal Capability command selects/reuses v9 artifacts 11/12;
- batch/browser/Review Snapshot/current-chain dependency selection agrees;
- current-chain flags identify v9/v5 artifacts correctly;
- no historical v7/v8 artifact is rewritten or deleted;
- normal commands reuse existing accepted artifacts rather than regenerating them;
- full deterministic CI passes;
- bounded operational checks for both `tG9K` and `t4jp` pass after promotion.

Blueprint remains deferred/non-authoritative and is not part of Capability promotion.
