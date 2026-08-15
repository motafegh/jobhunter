# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-15  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** Capability v9 guarded source-led candidate — dense `tG9K` live run pending  
**Exact current point:** English P1.6 v20/v5 is fully promoted and operationally verified. Dense artifact 36 and sparse artifact 37 are current through normal public routing. Historical/public Capability v7 remains the accepted baseline contract but cannot reliably rebuild dense artifact 36 with its one-shot generation architecture. Capability v8 proved the staged source-led architecture mechanically by completing `tG9K` with 31/31 capability requirements and 8/8 responsibilities, but semantic review found downstream depth/obligation/ownership inflation, so v8 is not accepted. Capability v9 preserves the v8 staged architecture, adds general semantic authority guardrails, separates role-level depth from capability-depth accounting, persists under a new v9/v5 identity, and passed deterministic CI 832. Next: run the isolated v9 candidate on `tG9K` and review it before any public promotion.

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
Capability v9 active candidate:     job-capability-intelligence-v9 / job-capability-intelligence-v5
Blueprint experimental:       role-capability-blueprint-v6 / role-capability-blueprint-v5
Review Snapshot:              job-review-snapshot-v1
```

Important: public `jobhunter jobs capability` still uses v7. V8 and v9 are candidate/history paths only until explicit acceptance and promotion.

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

Review Snapshot also selects artifacts 36 and 37 with matching English projection dependencies. Historical Capability/Blueprint artifacts remain present but correctly non-current.

The public Capability model-facing P1.6 view strips free-form `rationale` recursively while preserving authoritative concept/type/strength/depth/evidence/confidence. Persisted P1.6 remains unchanged.

Key records:

```text
docs/working-memory/2026-08-15_P16_V20_DENSE_ARTIFACT_36_SEMANTIC_ACCEPTANCE.md
docs/working-memory/2026-08-15_P16_V20_SPARSE_ARTIFACT_37_ACCEPTANCE.md
docs/working-memory/2026-08-15_P16_V20_PUBLIC_PROMOTION_ACCEPTANCE.md
```

## 5. Capability v7 — historical accepted baseline; promoted dense rebuild rejected

Historical accepted chain:

```text
tG9K English projection artifact 33
→ historical P1.6 v9 artifact 29
→ Capability v7 artifact 9
```

Artifact 9 remains useful historical evidence but is stale after P1.6 v20 promotion.

Two live v7 rebuild attempts against artifact 36 failed before persistence:

1. first run: broad source-link omission; retry then invented responsibility index `9` outside valid `0..7`;
2. second run: both generations collapsed dense evidence into one giant profile and omitted the same large requirement ledger even after explicit retry feedback.

A narrow deterministic index/evidence repair passed CI 811 but could not solve the architectural one-shot failure. Do not increase retries or weaken coverage validation.

Record:

```text
docs/working-memory/2026-08-15_CAPABILITY_V7_PROMOTED_P16_LINKAGE_FAILURE.md
```

## 6. Capability v8 — staged architecture mechanically proved, semantically rejected

V8 separated semantic grouping from source coverage bookkeeping:

```text
accepted P1.6 source truth
→ compact semantic group plan
→ bounded exact source-fact assignment partitions
→ bounded per-group reasoning
→ deterministic source-link injection
→ strict v7 reconciliation/source truth
```

Deterministic CI 821 passed.

Dense live `tG9K` then completed:

```text
Contract:                    job-capability-intelligence-v8 / v4
English P1.6 artifact:       36
Capability requirements:     31/31 linked
Responsibilities:            8/8 linked
Profiles:                    4
Role-level requirement idx:  [31, 32]
```

This proves the source-led staged architecture solved the v7 dense coverage failure.

However v8 is **not semantically accepted**. Review found generalized downstream inflation such as:

- unsupported `advanced` / `expertise` / `proficiency` depth in model-owned prose;
- unsupported `end-to-end` / `full lifecycle` ownership or scope;
- contextual tools described as necessary/required analytical foundations;
- preferred C/C++ promoted into a prerequisite foundation;
- preferred industrial/edge deployment escalated into a required ability/focus;
- semiconductor domain context escalated into unsupported `deep` expertise.

The v8 `5/6 explicit depth represented` line was also misleading rather than a missing source fact: five capability-relevant explicit depths were correctly linked, while the sixth explicit depth is role-level `three to six years` professional experience and was deliberately kept outside capability profiles.

Correct accounting is:

```text
capability explicit depth: 5/5
role-level explicit depth: 1
all explicit depth retained: 6/6
```

Do not promote v8 and do not rewrite/delete its persisted candidate artifact.

Records:

```text
docs/working-memory/2026-08-15_CAPABILITY_V8_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-15_CAPABILITY_V8_LIVE_REVIEW_AND_V9_BOUNDARY.md
```

## 7. Capability v9 — ACTIVE CANDIDATE

V9 deliberately preserves the successful v8 staged architecture while changing semantic authority and persistence identity:

```text
job-capability-intelligence-v9 / job-capability-intelligence-v5
```

General v9 boundaries:

- ordinary model-owned prose cannot restate requirement obligation (`required`, `must`, `mandatory`, `necessary`, `prerequisite`, etc.);
- ordinary model-owned prose cannot add technical depth (`advanced`, `expertise`, `proficiency`, `mastery`, `strong`, `solid`, `hands-on`, `deep`), while legitimate `deep learning` remains allowed;
- ordinary model-owned prose cannot infer `end-to-end`, `full lifecycle`, ownership, autonomy, leadership, or architecture;
- only `depth_signals` may add bounded work-implied depth reasoning;
- `model_inferred_prerequisite` cannot rest on a preferred/contextual-only source fact unless that same concept has an independent required basis;
- source-truth accounting separates capability explicit depth from role-level explicit depth;
- v9 uses a new prompt/schema identity, so the persisted v8 candidate cannot be silently reused as v9.

Implementation:

```text
src/jobhunter/capability_v9_models.py
src/jobhunter/capability_service_v9.py
scripts/run_capability_v9_candidate.py
tests/test_capability_v9_boundary.py
```

Deterministic gate:

```text
CI run 832
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

## 8. Exact next action

Run only the isolated v9 candidate for dense `tG9K`:

```bash
cd ~/projects/jobhunter
git pull --ff-only origin main
python scripts/run_capability_v9_candidate.py --job-id tG9K
```

Do **not** use normal `jobhunter jobs capability tG9K`; public Capability intentionally remains v7.

Expected mechanical invariants:

```text
new v9 artifact identity
English analysis artifact: 36
Capability requirements linked: 31/31
Responsibilities linked: 8/8
Capability explicit depth represented: 5/5
All explicit depth facts retained in source truth: 6/6
Role-level explicit depth facts: 1
Role-level requirement indices: [31, 32]
```

Then review semantics, not counts alone. V9 must show no model-owned obligation inflation, no unsupported depth inflation, no ownership/lifecycle inflation, and no preferred/contextual fact promoted into a prerequisite.

Only after dense semantic acceptance should sparse `t4jp` v9 non-regression run. Public promotion remains a separate later decision.

## 9. After Capability bounded acceptance

```text
dense v9 semantic acceptance
→ sparse t4jp v9 non-regression
→ decide whether v9 is fit for public Capability promotion
→ only then align public CLI/browser/Review Snapshot/current-chain lookup
→ heterogeneous Python/software role
→ network/security role
→ operations/platform/DevOps role
→ decide whether P1.6 + Capability are ready to freeze as Phase-2 input
```

Blueprint remains deferred and non-authoritative for this gate.
