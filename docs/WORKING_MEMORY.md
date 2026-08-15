# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-15  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** Capability v9 source-echo-filtered dense live validation  
**Exact current point:** English P1.6 v20/v5 is fully promoted and operationally verified. Dense `tG9K` artifact 36 and sparse `t4jp` artifact 37 are current through normal public routing. Public Capability remains v7/v4; historical artifact 9 is non-current because it depends on old P1.6 artifact 29. V8 proved source-led staging mechanically (31/31 capability requirements and 8/8 responsibilities on dense `tG9K`) but was semantically rejected for downstream inflation. Four v9 live runs have failed before persistence: (1) optional profile reasoning crossed semantic boundaries, (2) inherited v8 forced-enrichment rules rejected a restrained zero-enrichment profile, (3) useful five-group planning was rejected only because non-authoritative planner prose was over-policed, and (4) a bounded profile was rejected because the model redundantly returned `source_explicit` depth/context items that JobHunter already owns deterministically. The v9 contract now keeps authoritative source truth strict, makes model enrichment optional/fail-closed, normalizes planner prose, and filters model-emitted source-truth echoes as redundancy. CI 862 passed Ruff, the full test suite, and warnings-as-errors. No v9 artifact exists yet. Next: one isolated dense v9 candidate run on `tG9K`, then mechanical + semantic review before any sparse run or public promotion.

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
parser:                             jobinja-detail-v2
translation:                        lm-studio-translation-v2
English projection:                 english-projection-v2
English P1.6 public route:          job-analysis-english-v20 / job-analysis-v5
Original P1.6 public route:         job-analysis-original-v9 / job-analysis-v4
Capability public route:            job-capability-intelligence-v7 / job-capability-intelligence-v4
Capability v8 historical candidate: job-capability-intelligence-v8 / job-capability-intelligence-v4
Capability v9 active candidate:     job-capability-intelligence-v9 / job-capability-intelligence-v5
Blueprint experimental:             role-capability-blueprint-v6 / role-capability-blueprint-v5
Review Snapshot:                    job-review-snapshot-v1
```

Public `jobhunter jobs capability` still uses v7. V8 is rejected; v9 is candidate-only until explicit live acceptance and promotion.

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

Review Snapshot selects artifacts 36 and 37 with matching English projection dependencies. Capability model-facing P1.6 strips free-form `rationale` while preserving authoritative concept/type/strength/depth/evidence/confidence; persisted P1.6 remains unchanged.

## 5. Capability history

### v7 — historical/public baseline; dense rebuild rejected

Historical accepted chain:

```text
tG9K English projection artifact 33
→ historical P1.6 artifact 29
→ Capability v7 artifact 9
```

Two rebuild attempts against promoted artifact 36 failed before persistence: broad source-link loss / invalid index, then repeated one-profile collapse with 22 capability requirements omitted. A narrow index/evidence repair passed CI 811 but did not solve the one-shot architecture failure. Do not increase retries or weaken source coverage.

### v8 — mechanical architecture proof / semantic reject

V8 changed the runtime to:

```text
accepted P1.6 source truth
→ semantic group plan
→ bounded exact source-fact assignment
→ bounded per-group reasoning
→ deterministic source-link injection
→ strict reconciliation/source truth
```

Dense `tG9K` mechanically completed:

```text
P1.6 dependency:             artifact 36
Capability requirements:     31/31 linked
Responsibilities:            8/8 linked
Profiles:                    4
Role-level requirement idx:  [31, 32]
```

This proved staged source-led reasoning solves v7's dense coverage/linkage failure. V8 is not semantically accepted because model-owned prose inflated depth, ownership/lifecycle scope, and preferred/contextual facts. Its old `5/6` metric was misleading; correct depth accounting is capability 5/5 + role-level 1 = all 6/6.

### v9 — four live failure classes, no artifact

No v9 artifact has persisted.

Live failure 1:
- profile summary added unsupported depth language;
- retry corrected summary but optional derived items used obligation/necessity language;
- whole-profile failure for one optional bad inference was too coarse;
- per-item fail-closed filtering passed CI 838.

Live failure 2:
- model returned a bounded profile with a neutral summary and no extra derived reasoning;
- inherited v8 validator rejected it because every profile was required to add derived reasoning or `unknown_scope`;
- this exposed the contradiction between `do not speculate` and `must add enrichment`.

Live failure 3:
- failure moved earlier to the group-planning stage;
- the model produced five useful structural groups for dense `tG9K`;
- the plan was rejected because non-authoritative planner prose used strength/depth/scope-flavored wording such as `requires`, `advanced`, `expertise`, `deep understanding`, `proficiency`, `necessary`, and `end-to-end`;
- this proved planner clustering and downstream semantic authority were being validated at the wrong granularity;
- no v9 artifact persisted.

Live failure 4:
- the model reached bounded profile reasoning and returned explicit `Hands-on` / `Solid` depth plus source-backed operational context;
- those items used `evidence_status="source_explicit"`;
- v9 rejected the whole profile because model-owned analytical lists allowed only derived statuses;
- this was redundant source-truth echoing, not source corruption or unsupported inference;
- no v9 artifact persisted;
- v9 now filters those echoes and lets deterministic reconciliation re-inject authoritative `source_explicit` truth.

Detailed history:

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_LIVE_FAILURES_AND_DESIGN_PAUSE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_STRICTNESS_AUDIT_AND_SIMPLIFICATION.md
```

## 6. Capability v9 strictness audit — IMPLEMENTED / CI PASS

The governing distinction is now:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

### Hard rules retained

- complete capability-relevant P1.6 requirement coverage;
- complete responsibility coverage;
- valid/owned source indices;
- grounded evidence only;
- dense jobs cannot collapse all evidence into one group;
- group IDs and normalized labels must remain structurally distinct;
- education / duration-only experience remain role-level constraints;
- requirement strength is deterministic and source-owned;
- source-explicit depth is deterministic and source-owned;
- preferred/contextual-only facts cannot independently become inferred prerequisites;
- unsupported ownership/lifecycle/autonomy/architecture analytical claims are rejected/filtered;
- incomplete authoritative source truth cannot persist.

### Contradictory/unnecessary rules removed or narrowed for v9

1. **Mandatory derived reasoning removed.** A profile may validly contain neutral grouping + deterministic source facts and zero model-derived enrichment.
2. **Forced `unknown_scope` filler removed.** No fake unknown is required merely to satisfy shape.
3. **Duplicate hard-coded v8 revalidation removed.** The staged engine preserves the provider's already-validated version-specific Pydantic model; legacy/fake providers still use fallback validation.
4. **One bad optional inference no longer kills the whole profile.** Unsafe derived items are filtered individually.
5. **Inflated profile summary uses safe fallback.** V9 falls back to the normalized group summary and records the replacement instead of spending a retry.
6. **Prerequisite language rule narrowed.** `model_inferred_prerequisite` may use `necessary/prerequisite` language as explicit inference; its statement still cannot masquerade as employer `required/must/mandatory`. Rationale may accurately refer to a required source fact. Preferred/contextual-only grounding remains blocked.
7. **Derived depth is optional.** Source-explicit depth is already deterministic; no extra model depth is required.
8. **Planner prose lexical hard-failure removed.** Useful group structure is retained while claim-like planner wording is normalized deterministically. Inflated summaries become `This capability area covers <label>.`; inflated role interpretation becomes a neutral synthesis of the normalized group labels. Genuine terms such as `Deep Learning` are preserved. Structural grouping defects still fail hard.
9. **Model-emitted `source_explicit` analytical items no longer fail the profile.** They are filtered as redundant/misplaced model output. Deterministic reconciliation remains the only authority that injects accepted source-explicit depth/work/source facts.

Historical v7/v8 behavior is preserved. V9 uses its own final profile/draft contract and version-specific reconciler while reusing deterministic v7 reconciliation internally. Any compatibility bridge used for historical reconciliation is removed before v9 persistence.

The large v9 implementation before source-echo filtering is preserved byte-for-byte in `src/jobhunter/capability_v9_models_core.py`; the public `capability_v9_models.py` is now a thin boundary wrapper that re-exports the v9 contract and overrides only inference-facing redundant/misplaced status handling.

Regression proofs include:

- zero-enrichment profile valid under v9;
- same zero-enrichment profile still invalid under historical v8;
- final v9 reconciliation succeeds with zero model enrichment and injects deterministic source strength/depth;
- preferred-only inferred prerequisite remains filtered;
- required-grounded inferred prerequisite can use prerequisite language;
- typed v9 stage output is not accidentally revalidated as v8;
- planner prose inflation normalizes instead of retrying;
- exact five-group structure from live failure 3 survives normalization;
- `Deep Learning` remains preserved as a legitimate term;
- source-explicit depth/context echoes from the model are filtered without failing the bounded profile;
- deterministic reconciliation remains responsible for final accepted source-explicit truth.

Deterministic gates:

```text
CI run 849
Ruff:               PASS
full pytest:        PASS (434 tests)
warnings-as-errors: PASS

CI run 855
Ruff:               PASS
full pytest:        PASS (435 tests)
warnings-as-errors: PASS

CI run 862
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

Detailed audit:

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_STRICTNESS_AUDIT_AND_SIMPLIFICATION.md
```

## 7. Exact current state

```text
English P1.6 tG9K artifact 36       ACCEPTED / CURRENT
English P1.6 t4jp artifact 37       ACCEPTED / CURRENT
Capability v7 artifact 9            HISTORICAL / NON-CURRENT
Capability v8 dense candidate       PERSISTED / MECHANICAL PASS / SEMANTIC REJECT
Capability v9 artifact              NONE PERSISTED
Capability public route             v7/v4
Capability v9 candidate             SOURCE-ECHO-FILTERED / DETERMINISTIC PASS / LIVE PENDING
Blueprint                           DEFERRED / NON-AUTHORITATIVE
Heterogeneous role review           BLOCKED UNTIL CAPABILITY ACCEPTANCE
Phase 2                             BLOCKED
```

## 8. Exact next action

Run only the isolated dense v9 candidate:

```bash
cd ~/projects/jobhunter
git pull --ff-only origin main
python scripts/run_capability_v9_candidate.py --job-id tG9K
```

Do not use normal `jobhunter jobs capability tG9K`; the public route intentionally remains v7.

A successful run is not accepted from counts alone. Review must verify:

- dependency on P1.6 artifact 36;
- complete 31/31 capability requirement linkage;
- complete 8/8 responsibility linkage;
- capability explicit depth 5/5;
- all explicit depth retained 6/6;
- role-level indices `[31, 32]` remain separate;
- no source-strength inflation;
- no unsupported depth/ownership/lifecycle inflation;
- preferred/contextual facts are not promoted;
- zero optional enrichment, if present for a profile, is treated as valid rather than failure;
- any planner normalization remains non-authoritative and does not alter source truth;
- any model-emitted source-explicit echoes are absent from accepted model-owned enrichment and represented only through deterministic source truth.

Only after dense semantic acceptance should sparse `t4jp` v9 non-regression run. Public promotion is a separate later decision.

## 9. Relevant records

```text
docs/working-memory/2026-08-15_CAPABILITY_V7_PROMOTED_P16_LINKAGE_FAILURE.md
docs/working-memory/2026-08-15_CAPABILITY_V8_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-15_CAPABILITY_V8_LIVE_REVIEW_AND_V9_BOUNDARY.md
docs/working-memory/2026-08-15_CAPABILITY_V9_DERIVED_EXPECTATION_FILTERING.md
docs/working-memory/2026-08-15_CAPABILITY_V9_LIVE_FAILURES_AND_DESIGN_PAUSE.md
docs/working-memory/2026-08-15_CAPABILITY_V9_STRICTNESS_AUDIT_AND_SIMPLIFICATION.md
```

Blueprint remains deferred and non-authoritative for this gate.
