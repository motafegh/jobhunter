# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-15  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** Capability design review — implementation explicitly paused after two failed dense v9 live runs  
**Exact current point:** English P1.6 v20/v5 is fully promoted and operationally verified. Dense `tG9K` artifact 36 and sparse `t4jp` artifact 37 are current through normal public routing. Public Capability remains v7/v4, but its historical artifact 9 depends on old P1.6 artifact 29 and is non-current. V8 proved source-led staged Capability reasoning can mechanically cover dense artifact 36 (31/31 capability requirements, 8/8 responsibilities) but was semantically rejected for downstream inflation. V9 added semantic authority guardrails and corrected depth accounting, yet two dense live runs failed before persistence. The second failure exposed a contract contradiction: v9 aims not to force unsupported derived reasoning, while inherited v8 validation still requires every profile to add derived reasoning or explicit unknown scope. No v9 artifact exists. Per explicit user instruction, stop implementation and live reruns; next action is design discussion only.

This file is deliberately concise. Product/domain/source/architecture constraints, roadmap/implementation plans, `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`, and `docs/EXECUTION_TODO.md` win on conflict. Dated working-memory files preserve detailed evidence.

## 1. Repository workflow rule

JobHunter uses **main-only development** by default:

```text
current work → main
next work    → main
```

Do not create a new working branch unless the user explicitly changes this rule.

## 2. Product / architecture identity

JobHunter is a local-first personal career-intelligence application.

```text
MARKET
→ ROLE / CAPABILITY INTELLIGENCE
→ REVIEWED PERSONAL EVIDENCE
→ GAPS / CONSTRAINTS
→ LEARN / PRACTISE / BUILD / VERIFY
→ APPLICATION DECISION
→ OUTCOME
→ UPDATED EVIDENCE AND DECISIONS
↺
```

Architecture remains a local Python modular monolith with SQLite structured state, immutable evidence, FastAPI/Uvicorn/Jinja browser UI, shared CLI services, and local-first LM Studio.

Do not introduce Node/npm/React, vector/RAG, graph DB, generic plugin frameworks, agent orchestration, or similar infrastructure without demonstrated need.

## 3. Public-current contracts

```text
parser:                       jobinja-detail-v2
translation:                  lm-studio-translation-v2
English projection:           english-projection-v2
English P1.6 public route:    job-analysis-english-v20 / job-analysis-v5
Original P1.6 public route:   job-analysis-original-v9 / job-analysis-v4
Capability public route:      job-capability-intelligence-v7 / job-capability-intelligence-v4
Capability v8 historical candidate: job-capability-intelligence-v8 / job-capability-intelligence-v4
Capability v9 unaccepted candidate:  job-capability-intelligence-v9 / job-capability-intelligence-v5
Blueprint experimental:       role-capability-blueprint-v6 / role-capability-blueprint-v5
Review Snapshot:              job-review-snapshot-v1
```

Public `jobhunter jobs capability` still uses v7. Neither v8 nor v9 is accepted or public-current.

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
Requirements:                8
Responsibilities:            0
Role purpose:                0
Mechanical audit:            PASS
Semantic non-regression:     PASS
```

Operational public proof:

```text
tG9K → reused artifact 36 → job-analysis-english-v20 / job-analysis-v5
t4jp → reused artifact 37 → job-analysis-english-v20 / job-analysis-v5
```

Review Snapshot selects artifacts 36 and 37 with matching English projection dependencies. Historical Capability/Blueprint artifacts can remain present while correctly non-current.

The Capability model-facing P1.6 view strips free-form `rationale` while preserving authoritative concept/type/strength/depth/evidence/confidence. Persisted P1.6 remains unchanged.

## 5. Capability v7 — historical/public baseline; promoted dense rebuild rejected

Historical accepted chain:

```text
tG9K English projection artifact 33
→ historical P1.6 artifact 29
→ Capability v7 artifact 9
```

Artifact 9 is historical and non-current after P1.6 v20 promotion.

Two live rebuild attempts against artifact 36 failed before persistence:

1. broad source-link omission followed by an invented responsibility index `9` outside valid `0..7`;
2. repeated collapse of dense evidence into one oversized profile with 22 capability-relevant requirements omitted even after repair feedback.

A narrow deterministic index/evidence repair passed CI 811 but did not solve the architectural one-shot failure. Do not increase retries or weaken coverage validation.

## 6. Capability v8 — mechanical architecture proof / semantic reject

V8 changed the runtime shape to:

```text
accepted P1.6 source truth
→ semantic group plan
→ bounded exact source-fact assignment
→ bounded per-group reasoning
→ deterministic source-link injection
→ strict reconciliation/source truth
```

Dense `tG9K` completed mechanically:

```text
P1.6 dependency:             artifact 36
Capability requirements:     31/31 linked
Responsibilities:            8/8 linked
Profiles:                    4
Role-level requirement idx:  [31, 32]
```

This proves source-led staging solves v7's dense coverage/linkage failure.

V8 is **not semantically accepted**. Review found unsupported depth (`advanced`, `expertise`, `proficiency`, `deep`), ownership/lifecycle scope (`end-to-end`, `full lifecycle`), and escalation of preferred/contextual facts such as C/C++ and industrial/edge deployment.

V8's old `5/6` depth metric was also misleading. Correct accounting is:

```text
capability explicit depth: 5/5
role-level explicit depth: 1
all explicit depth retained: 6/6
```

Do not promote or overwrite the persisted v8 candidate artifact.

## 7. Capability v9 — two live failures / no artifact / implementation paused

V9 preserves the v8 staged architecture under:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

It adds general semantic authority guardrails:

- model-owned prose cannot restate source obligation;
- ordinary model-owned prose cannot add unsupported technical depth;
- model-owned prose cannot infer unsupported ownership/lifecycle/autonomy/architecture;
- preferred/contextual-only facts cannot become prerequisites without an independent required basis;
- source truth separates capability depth from role-level depth.

### Live failure 1

No artifact persisted.

- generation 1 summary used unsupported `expertise` and correctly hard-failed;
- generation 2 corrected the summary but optional derived depth statements used `necessary`, `prerequisite`, `must`, and `necessitates`;
- whole-profile rejection of one optional bad inference was judged too coarse;
- a fail-closed per-expectation filtering correction passed deterministic CI 838.

### Live failure 2

No artifact persisted.

Both generations produced a bounded MLOps/production profile with a summary and no derived expectations. Validation failed with:

```text
Capability profile reasoning must add derived reasoning or an explicit unknown boundary
```

This is inherited from `CapabilityProfileReasoningV8` and exposes the current design contradiction:

```text
v9 intent:
  do not force speculative derived intelligence;
  deterministic P1.6 facts may be enough for a bounded profile.

inherited v8 invariant:
  every profile must add derived reasoning or explicit unknown scope.
```

The earlier filtering checkpoint's statement that a profile could survive with no safe derived expectations was therefore an intended property, not an actually effective runtime property. That documentation has been explicitly corrected rather than silently rewritten.

Generation 2 also used `requires` in its summary, but the surfaced inherited-v8 failure happened before any persisted v9 artifact; do not interpret the run as a semantic pass apart from the reported error.

## 8. Current exact state

```text
English P1.6 tG9K artifact 36       ACCEPTED / CURRENT
English P1.6 t4jp artifact 37       ACCEPTED / CURRENT
Capability v7 artifact 9            HISTORICAL / NON-CURRENT
Capability v8 dense candidate       PERSISTED / MECHANICAL PASS / SEMANTIC REJECT
Capability v9 artifact              NONE PERSISTED
Capability public route             v7/v4
Capability v9 candidate             IMPLEMENTED BUT LIVE-UNACCEPTED
Blueprint                           DEFERRED / NON-AUTHORITATIVE
Heterogeneous role review           BLOCKED
Phase 2                             BLOCKED
```

## 9. Explicit pause and next action

Per user instruction:

```text
STOP implementation for now.
Do not patch v9 again.
Do not create v10.
Do not rerun Capability live generation.
Document the current point, then discuss the design together.
```

Therefore the next action is **discussion/design review only**.

The design discussion should decide what Capability is supposed to add beyond accepted P1.6 source truth, which model-owned outputs are mandatory versus optional, whether an evidence-grounded profile may legitimately contain no extra derived reasoning, and whether model-owned `depth_signals` should exist at all when source-explicit depth is already deterministic.

Detailed current record:

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_LIVE_FAILURES_AND_DESIGN_PAUSE.md
```

Other relevant records:

```text
docs/working-memory/2026-08-15_CAPABILITY_V7_PROMOTED_P16_LINKAGE_FAILURE.md
docs/working-memory/2026-08-15_CAPABILITY_V8_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-15_CAPABILITY_V8_LIVE_REVIEW_AND_V9_BOUNDARY.md
docs/working-memory/2026-08-15_CAPABILITY_V9_DERIVED_EXPECTATION_FILTERING.md
```
