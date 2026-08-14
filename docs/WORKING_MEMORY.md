# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-15  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** P1.6 v20 promotion work after bounded dense + sparse calibration  
**Exact current point:** dense `tG9K` v20 artifact **36** passed persistence, mechanical audit, and semantic review; sparse `t4jp` v20 artifact **37** passed persistence, mechanical audit, and semantic non-regression. The complete v17→v20 implementation/calibration stack has been merged into `main`. **Public P1.6 is still v9/v4 until promotion routing is deliberately implemented and verified.** Capability artifact 9 remains tied to P1.6 artifact 29.

This file is deliberately concise. Product/domain/source/architecture constraints, roadmap/implementation plans, the semantic-quality acceptance plan, and `docs/EXECUTION_TODO.md` win on conflict. Dated working-memory files preserve detailed evidence.

## 1. Repository workflow rule

JobHunter now uses **main-only development** by default:

```text
current work → main
next work    → main
```

Do not create a new working branch or PR stack unless the user explicitly changes this rule. Historical merged PRs/branches remain evidence only; they are not active development paths.

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

## 3. Accepted/public contracts before promotion

```text
parser:                       jobinja-detail-v2
translation:                  lm-studio-translation-v2
English projection:           english-projection-v2
English P1.6 public:          job-analysis-english-v9
Original P1.6 public:         job-analysis-original-v9
P1.6 public schema:           job-analysis-v4
Capability accepted baseline: job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4
Blueprint experimental:       role-capability-blueprint-v6
Blueprint schema:             role-capability-blueprint-v5
Review Snapshot:              job-review-snapshot-v1
```

Accepted dense public chain remains until promotion:

```text
tG9K English projection artifact 33
→ P1.6 v9 artifact 29
→ Capability v7 artifact 9
```

V20 calibration passing does not itself change current public routing.

## 4. V17 → V20 history now consolidated on main

The following historical PRs have been merged into `main` in order:

```text
PR #5 → v17 source-led requirement capacity
PR #6 → v18 deterministic structured requirements
PR #7 → v19 depth/optionality canonicalization
PR #8 → v20 source-led partitioning + accepted calibration evidence
```

Current candidate/next-public English contract under promotion review:

```text
job-analysis-english-v20 / job-analysis-v5
```

Key records:

```text
docs/working-memory/2026-08-14_P16_V20_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-14_P16_V20_FIRST_LIVE_PARTITION_CORRECTION.md
docs/working-memory/2026-08-14_P16_V20_SECOND_LIVE_SCOPE_DEPTH_CORRECTION.md
docs/working-memory/2026-08-14_P16_V20_DENSE_ARTIFACT_36_PERSISTED.md
docs/working-memory/2026-08-15_P16_V20_DENSE_ARTIFACT_36_MECHANICAL_AUDIT_PASS.md
docs/working-memory/2026-08-15_P16_V20_DENSE_ARTIFACT_36_SEMANTIC_ACCEPTANCE.md
docs/working-memory/2026-08-15_P16_V20_SPARSE_ARTIFACT_37_ACCEPTANCE.md
docs/working-memory/2026-08-15_P16_V20_PROMOTION_ROUTING_DESIGN.md
```

## 5. What v17 → v20 established

```text
v17 → remove arbitrary 32-requirement ceiling + aggregate dense coverage feedback
v18 → deterministic structured education/minimum experience + non-excludable structured skills
v19 → separate optionality from technical depth + expose whole-answer retry oscillation
v20 → source-led bounded partitions + exact partition scope + merge + whole-source validation
```

V20 live corrections also established:

- `some C / C++ helpful` → preferred, `depth_signal=null`;
- `industrial / edge deployment a plus` → preferred scope in concept, not depth or fabricated experience;
- unsupported preferred `experience` fails closed without prior-applied-exposure evidence;
- role-purpose vs concrete-duty remains semantic/model-owned rather than vacancy-specific hardcoding.

## 6. Dense calibration — tG9K artifact 36 PASS

```text
Contract:          job-analysis-english-v20 / job-analysis-v5
Requirements:      33
Responsibilities:  8
Role purpose:      0
Mechanical audit:  PASS
Semantic review:   PASS WITH ACCEPTABLE DIFFERENCE
```

Artifact 36 preserves all 27 accepted dense v9 source-derived requirements and adds all six structured required skills, giving 33 total. It preserves Master's degree, exact `three to six years` professional-experience depth, `Strong`, `Hands-on`, `Comfort`, `Solid`, and Python `expert`; MATLAB/C++ remain preferred with null depth; contextual stack remains contextual; industrial/edge deployment has correct scope and no fabricated experience.

The 8-vs-7 responsibility difference is fully explained by the opening `Build and validate ML/AI models...` source bullet. V9 classified it as role purpose; v20 classifies it as a concrete responsibility. The other seven duty surfaces are unchanged. This was accepted because the source sentence is itself a concrete imperative under `What you'll do` and no meaning is lost.

## 7. Sparse calibration — t4jp artifact 37 PASS

```text
Contract:                    job-analysis-english-v20 / job-analysis-v5
Requirements:                8
Responsibilities:            0
Role purpose:                0
Structured skills:           3/3
Qualification-list items:    4/4
Residual coverage decisions: 4/4
Decomposed coarse decisions: 1
Mechanical audit:            PASS
Semantic non-regression:     PASS
```

Artifact 37 matches accepted sparse v16 artifact 35 at the source-fact/obligation/evidence level:

- all 3 structured required skills retained;
- all 4 exact qualification-list items retained;
- `Ethics and work commitment` retained;
- `the work is teachable`, remote-application instruction, and location/benefits sentence remain excluded;
- no responsibilities or role purpose fabricated;
- no education/minimum-experience requirement fabricated from `it doesn't matter`;
- schedule wording `full-time and part-time` does not enter concept or depth.

Ontology difference: `social networks` is `tool` in v20 versus `skill` in v16. This is defensible and does not change the source fact or obligation.

Non-gating hygiene note: the `Visual content production` requirement has correct authoritative fields (`depth_signal=null`) but one model-generated rationale inaccurately says it is “capturing scope/schedule as depth.” Treat free-form rationale as explanatory text, not authority. Capability/downstream review must not let such prose override normalized P1.6 fields/evidence.

## 8. V20 calibration boundary — satisfied

```text
v20 deterministic CI PASS
+ dense tG9K 36 persistence PASS
+ dense tG9K 36 mechanical PASS
+ dense tG9K 36 semantic PASS
+ sparse t4jp 37 persistence PASS
+ sparse t4jp 37 mechanical PASS
+ sparse t4jp 37 semantic non-regression PASS
```

This authorizes **P1.6 v20 promotion work**. It does not itself perform promotion.

## 9. Current action — promotion implementation on main

The promotion-routing design is recorded in:

```text
docs/working-memory/2026-08-15_P16_V20_PROMOTION_ROUTING_DESIGN.md
```

Promotion must:

- make the public English path use v20/v5;
- preserve the still-valid original-language v9/v4 path unless separately revalidated;
- keep exact current-artifact/dependency routing correct;
- avoid circular imports between historical v9 modules and v20 modules;
- align targeted CLI, complete Phase-1 batch, browser, Review Snapshot, Market and Capability dependency selection;
- preserve historical artifact/module reproducibility;
- add promotion regression tests;
- pass Ruff, full pytest, and warnings-as-errors;
- only then rebuild Capability v7 against the promoted English P1.6 dependency.

All implementation for this gate proceeds directly on `main`.

## 10. After promotion

```text
promoted English P1.6 v20/v5
→ rebuild/review Capability v7 against promoted P1.6
→ heterogeneous Python/software role
→ network/security role
→ operations/platform/DevOps role
→ decide whether P1.6 + Capability v7 are ready to freeze as Phase-2 input
```

Blueprint remains implemented but not accepted for Phase-1 decision use. Do not resume Blueprint tuning or corpus-wide Phase 2 during this gate.