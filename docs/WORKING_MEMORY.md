# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-15  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current gate:** P1.6 v20 public routing implemented and deterministic CI passed; local artifact-reuse/current-chain verification pending  
**Exact current point:** dense `tG9K` v20 artifact **36** and sparse `t4jp` v20 artifact **37** passed bounded calibration. Public-current routing now resolves English P1.6 to **v20/v5** and original-language P1.6 to **v9/v4** across CLI, batch, browser, Market, Review Snapshot and Capability dependency selection. Final routing CI run **801** passed Ruff, full pytest, and warnings-as-errors. Before declaring operational promotion closed, locally verify that artifacts 36 and 37 are reused/current through the public route. Capability artifact 9 remains the accepted historical baseline tied to P1.6 artifact 29 until Capability is deliberately rebuilt after that verification.

This file is deliberately concise. Product/domain/source/architecture constraints, roadmap/implementation plans, the semantic-quality acceptance plan, and `docs/EXECUTION_TODO.md` win on conflict. Dated working-memory files preserve detailed evidence.

## 1. Repository workflow rule

JobHunter uses **main-only development** by default:

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

## 3. Public-current contracts after routing implementation

```text
parser:                       jobinja-detail-v2
translation:                  lm-studio-translation-v2
English projection:           english-projection-v2
English P1.6 public route:    job-analysis-english-v20
English P1.6 schema:          job-analysis-v5
Original P1.6 public route:   job-analysis-original-v9
Original P1.6 schema:         job-analysis-v4
Capability accepted baseline: job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4
Blueprint experimental:       role-capability-blueprint-v6
Blueprint schema:             role-capability-blueprint-v5
Review Snapshot:              job-review-snapshot-v1
```

The current English route is implemented in code, but final operational promotion closure still requires local proof that accepted artifacts 36 and 37 are current/reused under that route.

Historical accepted dense chain remains useful evidence until Capability is rebuilt:

```text
tG9K English projection artifact 33
→ historical P1.6 v9 artifact 29
→ Capability v7 artifact 9
```

## 4. V17 → V20 history consolidated on main

Historical PRs merged in order:

```text
PR #5 → v17 source-led requirement capacity
PR #6 → v18 deterministic structured requirements
PR #7 → v19 depth/optionality canonicalization
PR #8 → v20 source-led partitioning + accepted calibration evidence
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
docs/working-memory/2026-08-15_P16_V20_PUBLIC_ROUTING_IMPLEMENTED_CI_PASS.md
```

## 5. What v17 → v20 established

```text
v17 → remove arbitrary 32-requirement ceiling + aggregate dense coverage feedback
v18 → deterministic structured education/minimum experience + non-excludable structured skills
v19 → separate optionality from technical depth + expose whole-answer retry oscillation
v20 → source-led bounded partitions + exact partition scope + merge + whole-source validation
```

V20 live corrections established:

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

Artifact 37 matches accepted sparse v16 artifact 35 at the source-fact/obligation/evidence level. No duties/purpose, education/minimum-experience, or schedule-based depth were fabricated.

Ontology difference: `social networks` is `tool` in v20 versus `skill` in v16. This is defensible and does not change the source fact or obligation.

Non-gating hygiene note: the `Visual content production` requirement has correct authoritative fields (`depth_signal=null`) but one model-generated rationale inaccurately says it is “capturing scope/schedule as depth.” Treat free-form rationale as explanatory text, not authority. Capability/downstream review must not let such prose override normalized P1.6 fields/evidence.

## 8. Public-routing implementation — deterministic PASS

`src/jobhunter/analysis_current.py` is the neutral current-public facade:

```text
English → v20/v5
Original → v9/v4
```

Public routing is aligned across:

- targeted CLI;
- complete Phase-1 analysis selection/batch;
- browser generation and analysis status;
- Market current-analysis scope;
- Review Snapshot;
- Capability v7 P1.6 dependency selection.

Historical v9/v10…v20 modules retain their original identities; no circular aliasing or artifact rewriting was introduced.

Final code-level gate:

```text
main head for CI proof:       7bd77fd66ba5c12a738dad4d9333ac4eeb3c48d6
CI run 801:                   PASS
Ruff:                         PASS
full pytest:                  PASS
warnings-as-errors:           PASS
```

## 9. Current action — local reuse/current-chain verification

Pull current `main`, then use normal public commands—not candidate scripts—to prove routing against the existing local database.

Expected:

```text
tG9K English → reuse/current artifact 36 → v20/v5
t4jp English → reuse/current artifact 37 → v20/v5
```

Then export normal public Review Snapshots and verify they select those exact English artifacts.

Do **not** rebuild Capability before this proof. If either P1.6 artifact is regenerated instead of reused/current, stop and diagnose contract/source/model/dependency identity.

## 10. After local promotion verification

```text
P1.6 v20 operational promotion complete
→ rebuild/review Capability v7 against promoted P1.6 artifact 36
→ heterogeneous Python/software role
→ network/security role
→ operations/platform/DevOps role
→ decide whether P1.6 + Capability v7 are ready to freeze as Phase-2 input
```

Blueprint remains implemented but not accepted for Phase-1 decision use. Do not resume Blueprint tuning or corpus-wide Phase 2 during this gate.
