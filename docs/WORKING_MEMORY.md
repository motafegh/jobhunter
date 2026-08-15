# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-15  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** Capability v8 source-led candidate — dense `tG9K` live run pending  
**Exact current point:** English P1.6 v20/v5 is fully promoted and operationally verified. Dense artifact 36 and sparse artifact 37 are reused through the normal public route and selected correctly by Review Snapshot. Historical Capability v7 artifact 9 is stale because it depends on old P1.6 artifact 29. Two attempts to rebuild one-shot Capability v7 against promoted artifact 36 failed without persistence, proving a stable dense grouping/coverage failure. Capability v8 source-led staged reasoning is implemented candidate-only on `main`; CI 821 passed Ruff, full pytest, and warnings-as-errors. Next: run the isolated v8 candidate on `tG9K`, then mechanically and semantically review any persisted artifact before promotion.

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
English P1.6 public route:    job-analysis-english-v20
English P1.6 schema:          job-analysis-v5
Original P1.6 public route:   job-analysis-original-v9
Original P1.6 schema:         job-analysis-v4
Capability public route:      job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4
Capability v8 candidate:      job-capability-intelligence-v8 / v4
Blueprint experimental:       role-capability-blueprint-v6 / v5
Review Snapshot:              job-review-snapshot-v1
```

Important: public `jobhunter jobs capability` still uses v7. V8 is candidate-only until live dense + sparse acceptance and an explicit promotion decision.

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
Structured skills:           3/3
Qualification-list items:    4/4
Residual coverage decisions: 4/4
Mechanical audit:            PASS
Semantic non-regression:     PASS
```

Operational promotion proof through normal public commands:

```text
tG9K → reused artifact 36 → job-analysis-english-v20 / job-analysis-v5
t4jp → reused artifact 37 → job-analysis-english-v20 / job-analysis-v5
```

Normal Review Snapshot also selected artifacts 36 and 37 with matching English projection dependencies.

The previous tG9K Capability and Blueprint artifacts remain present historically but are correctly reported as non-current because they depend on the old P1.6 chain.

Detailed P1.6 records:

```text
docs/working-memory/2026-08-14_P16_V20_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-15_P16_V20_DENSE_ARTIFACT_36_SEMANTIC_ACCEPTANCE.md
docs/working-memory/2026-08-15_P16_V20_SPARSE_ARTIFACT_37_ACCEPTANCE.md
docs/working-memory/2026-08-15_P16_V20_PUBLIC_ROUTING_IMPLEMENTED_CI_PASS.md
docs/working-memory/2026-08-15_P16_V20_PUBLIC_PROMOTION_ACCEPTANCE.md
```

## 5. P1.6 rationale boundary for downstream reasoning

One accepted sparse P1.6 item had correct authoritative fields but misleading free-form rationale prose. Downstream Capability must not treat P1.6 rationale as source authority.

The public Capability facade therefore strips `rationale` recursively from the model-facing P1.6 view while preserving the persisted artifact and authoritative concept/type/strength/depth/evidence/confidence. CI 807 passed this boundary.

V8 keeps the same boundary.

## 6. Capability v7 — historical baseline + promoted-chain failure

Historical accepted dense chain:

```text
tG9K English projection artifact 33
→ historical P1.6 v9 artifact 29
→ Capability v7 artifact 9
```

Artifact 9 remains useful historical evidence but is not current after P1.6 v20 promotion.

### Rebuild attempt 1 against P1.6 artifact 36

No artifact persisted.

- generation 1 omitted most dense capability-relevant requirement links;
- retry repaired much coverage but emitted responsibility index `9`, while valid responsibility indices are `0..7`.

A narrow v7 inference-time repair was added for mechanically impossible positive indices and exact evidence-backed link recovery. Strict whole-artifact coverage remained unchanged. CI 811 passed.

### Rebuild attempt 2

No artifact persisted.

Both generations independently collapsed the dense job into one giant capability profile. Even after retry feedback listed the missing requirement indices, the model did not restructure the answer. Final missing capability-relevant requirement indices remained:

```text
[2, 3, 4, 5, 6, 9, 10, 12, 13, 15, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 29, 30]
```

Conclusion: promoted dense P1.6 exposed a stable one-shot v7 architecture failure, not a local typo. Do not increase retries or weaken coverage validation.

Record:

```text
docs/working-memory/2026-08-15_CAPABILITY_V7_PROMOTED_P16_LINKAGE_FAILURE.md
```

## 7. Capability v8 — ACTIVE CANDIDATE

Decision: separate semantic grouping, source-fact coverage bookkeeping, and per-profile reasoning.

```text
accepted P1.6 source truth
→ compact semantic group plan
→ bounded exact source-fact assignment partitions
→ bounded reasoning per validated group
→ deterministic source-link injection
→ existing strict v7 reconciliation/source truth
→ persist only after complete validation
```

Key properties:

- group planner owns semantics, not source indices;
- capability requirements are assigned in bounded chunks of at most 8;
- every assignment partition must cover exactly its owned requirement/responsibility indices;
- only valid group IDs are allowed;
- dense assignments must use at least two groups;
- per-group reasoning sees only its assigned facts and matching evidence;
- per-group model output cannot emit source links, source-explicit strength/depth, or source-explicit duties;
- JobHunter deterministically injects source links;
- existing strict v7 reconciliation still owns source strength, explicit depth, source work activities, role-level constraints, complete source truth, independence suppression, and final coverage validation;
- persisted schema remains `job-capability-intelligence-v4`;
- candidate prompt/runtime identity is `job-capability-intelligence-v8`.

Implementation:

```text
src/jobhunter/capability_v8_models.py
src/jobhunter/capability_inference_v8.py
src/jobhunter/capability_service_v8.py
scripts/run_capability_v8_candidate.py
tests/test_capability_v8_models.py
tests/test_capability_v8_service.py
```

Deterministic gate:

```text
CI run 821
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

Detailed design record:

```text
docs/working-memory/2026-08-15_CAPABILITY_V8_SOURCE_LED_PARTITIONING.md
```

## 8. Exact next action

Run only the candidate path for dense `tG9K`:

```bash
cd ~/projects/jobhunter
git pull --ff-only origin main
python scripts/run_capability_v8_candidate.py --job-id tG9K
```

Do **not** use normal `jobhunter jobs capability tG9K` for this gate; that intentionally remains public v7.

If v8 persists, do not accept it from counts alone. Review:

- P1.6 dependency is artifact 36;
- contract v8/v4;
- all capability-relevant requirements linked;
- all 8 responsibilities linked;
- role-level requirements separate;
- all explicit depth represented through deterministic reconciliation;
- at least two coherent profiles;
- no mandatory/mastery inflation for contextual/preferred tools;
- no fabricated ownership/autonomy/leadership;
- no unsupported architecture claims;
- no generic curriculum expansion.

Then run sparse `t4jp` v8 non-regression before any public v8 promotion.

## 9. After Capability v8 bounded acceptance

Only after dense + sparse v8 acceptance:

```text
consider public Capability v8 promotion
→ align CLI/browser/Review Snapshot/current-chain lookup
→ heterogeneous Python/software role
→ network/security role
→ operations/platform/DevOps role
→ decide whether P1.6 + Capability are ready to freeze as Phase-2 input
```

Blueprint remains deferred and non-authoritative for this gate.
