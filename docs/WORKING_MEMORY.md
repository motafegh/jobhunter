# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-15  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** CI-3 heterogeneous semantic validation of P1.6 + Capability v7  
**Exact current point:** dense `tG9K` P1.6 v20 artifact **36** passed persistence, the v20-specific mechanical snapshot audit, and full semantic review with one acceptable purpose-vs-duty classification difference. The next authorized gate is **sparse `t4jp` v20 non-regression**. Public P1.6 remains v9/v4; no promotion, Capability rebuild, heterogeneous-role progression, or candidate merge yet.

This file is deliberately concise. Product/domain/source/architecture constraints, roadmap/implementation plans, the semantic-quality acceptance plan, and `docs/EXECUTION_TODO.md` win on conflict. Dated working-memory files preserve the detailed evidence trail.

## 1. Product / architecture identity

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

## 2. Accepted/public contracts remain frozen

```text
parser:                       jobinja-detail-v2
translation:                  lm-studio-translation-v2
English projection:           english-projection-v2
English P1.6 accepted/public: job-analysis-english-v9
Original P1.6:                job-analysis-original-v9
P1.6 accepted schema:         job-analysis-v4
Capability accepted baseline: job-capability-intelligence-v7
Capability schema:            job-capability-intelligence-v4
Blueprint experimental:       role-capability-blueprint-v6
Blueprint schema:             role-capability-blueprint-v5
Review Snapshot:              job-review-snapshot-v1
```

Accepted dense chain remains:

```text
tG9K English projection artifact 33
→ P1.6 v9 artifact 29
→ Capability v7 artifact 9
```

Sparse calibration anchor remains `t4jp` P1.6 v16 artifact 35.

No candidate artifact is public truth until the full promotion gate passes. Capability artifact 9 remains tied to analysis artifact 29.

## 3. Current candidate chain

```text
v17: agent/p16-v17-source-led-capacity                    PR #5
v18: agent/p16-v18-deterministic-structured-requirements  PR #6
v19: agent/p16-v19-depth-optionality-canonicalization     PR #7
v20: agent/p16-v20-source-led-partitioning                PR #8

active candidate:   job-analysis-english-v20
schema shape:       job-analysis-v5
dense artifact:     tG9K artifact 36
dense gate:         PASS
public promotion:   NOT AUTHORIZED
```

Current v20 records:

```text
docs/working-memory/2026-08-14_P16_V20_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-14_P16_V20_FIRST_LIVE_PARTITION_CORRECTION.md
docs/working-memory/2026-08-14_P16_V20_SECOND_LIVE_SCOPE_DEPTH_CORRECTION.md
docs/working-memory/2026-08-14_P16_V20_DENSE_ARTIFACT_36_PERSISTED.md
docs/working-memory/2026-08-15_P16_V20_DENSE_ARTIFACT_36_MECHANICAL_AUDIT_PASS.md
docs/working-memory/2026-08-15_P16_V20_DENSE_ARTIFACT_36_SEMANTIC_ACCEPTANCE.md
```

Earlier dense correction history remains in the v16-v19 dated records.

## 4. What v17 → v20 established

### v17

- removed the arbitrary 32-requirement ceiling;
- aggregated dense coverage defects into one correction message;
- exposed unnecessary model ownership of mechanically known structured facts.

### v18

- moved parseable structured education and minimum experience to deterministic JobHunter ownership;
- kept ambiguous semantics model-owned/fail-closed;
- made structured skills non-excludable coverage.

### v19

- separated optionality from technical depth;
- removed unsupported generated depth vocabulary only when exact source evidence proves it was model-added;
- preserved genuine source depth;
- exposed dense whole-answer retry oscillation.

### v20

Changed extraction granularity instead of weakening validation:

```text
complete source-led coverage ledger
→ bounded independent semantic partitions
→ exact partition-scope enforcement
→ merge validated partitions
→ deterministic structured facts
→ inherited normalization/semantic guards
→ full original-source validation
→ persistence only if everything passes
```

Each model-owned requirement partition is bounded to at most 8 references. Cross-partition requirement/duty/exclusion leakage fails closed.

Live corrections established:

- `some C / C++ helpful` → preferred, null technical depth, exact evidence preserved;
- `industrial / edge deployment a plus` → scope belongs in concept, not depth;
- unsupported preferred `experience` remains fail-closed unless evidence states prior applied exposure;
- role purpose versus responsibility remains a semantic classification rather than a tG9K-specific hardcoded rewrite.

## 5. Dense v20 artifact 36 — accepted bounded calibration

Persisted result:

```text
Artifact:          36
Contract:          job-analysis-english-v20 / job-analysis-v5
Model:             gemma-4-e4b-it-ud
Requirements:      33
Responsibilities:  8
Role purpose:      0
```

Mechanical snapshot audit:

```text
PASS
structured skills: 6/6
coverage decisions: 34
```

Semantic verdict:

```text
PASS WITH ACCEPTABLE DIFFERENCE
```

### Requirement coverage

Artifact 36 preserves all 27 accepted dense v9 source-derived requirements and adds the six structured required skills that v9 omitted:

```text
Artificial Intelligence
Python
Microsoft Office
Machine learning
Linux
Git
```

Therefore:

```text
27 accepted source-derived requirements
+ 6 structured required skills
= 33 v20 requirements
```

No accepted dense factual requirement was silently lost.

### Required/depth facts

Correctly retained:

- `Master's degree` required;
- `Professional experience` with exact `three to six years` depth;
- `Strong` AI/ML industrial/manufacturing experience;
- `Hands-on` process-control/manufacturing-analytics/yield/anomaly work;
- `Comfort` with high-dimensional time-series/sensor/metrology data;
- `Solid` statistics/signal-processing fundamentals;
- prose `Python (expert)` with `expert` depth.

Correct optionality:

```text
MATLAB a plus              → preferred, depth=null
some C / C++ helpful       → preferred, depth=null
industrial / edge deployment a plus
                           → preferred, depth=null, no fabricated experience
```

The long technical stack remains contextual under the employer's global stack modifier.

### Ontology

V20's ontology differences from v9 are defensible and generally more specific: concrete technologies are often `tool`, semiconductor subject matter is `domain`, model deployment is `skill`, and unsupported deployment `experience` is no longer invented. Structured Python and prose `Python (expert)` remain provenance-distinct.

### 8 responsibilities vs v9's 7 + role purpose

No duty was duplicated or lost. Both versions split the source semicolon line into two atomic duties:

```text
Handle high-volume, high-dimensional sensor / trace and metrology data
build robust pipelines.
```

The count difference is entirely the opening source bullet:

```text
Build and validate ML/AI models on semiconductor process, equipment, and manufacturing data.
```

V9 classified it as role purpose. V20 classifies it as a responsibility. Because it is itself a concrete imperative action under `What you'll do`, the v20 classification is semantically defensible. Meaning is preserved, so this is accepted rather than treated as a blocker.

Dense `tG9K` v20 is therefore accepted for this bounded calibration case.

## 6. Current action — sparse v20 non-regression

The next authorized live command is:

```bash
python scripts/run_p16_v20_candidate.py --job-id t4jp
```

Compare the resulting sparse v20 artifact against accepted sparse v16 artifact 35. Sparse acceptance target:

- 3/3 structured required skills;
- 4/4 qualification items;
- complete residual accounting;
- 0 responsibilities;
- 0 role purpose;
- no fabricated duty/purpose;
- no deterministic over-extraction.

If sparse v20 persists, export/audit/review it before any promotion decision.

## 7. Promotion boundary

Promotion still requires:

```text
v20 deterministic CI PASS
+ dense tG9K persistence PASS
+ dense tG9K mechanical audit PASS
+ dense tG9K semantic PASS
+ sparse t4jp v20 non-regression PASS
```

Until sparse passes:

```text
public P1.6 promotion            → blocked
Capability v7 rebuild over v20  → blocked
Python/software CI-3 role       → blocked
network/security CI-3 role      → blocked
operations/platform CI-3 role   → blocked
candidate PR merge              → blocked
```

After eventual P1.6 promotion, rebuild Capability v7 against the promoted P1.6 artifact rather than treating artifact 9 as current-chain.

## 8. Deferred boundaries

Blueprint remains implemented but not accepted for Phase-1 decision use. Do not create Blueprint v7 or resume nearby model shopping during this gate.

Historical fixed list ceilings outside the current requirements path remain a later source-led-capacity audit unless live evidence proves they are current blockers.
