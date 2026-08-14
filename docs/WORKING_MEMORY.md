# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-14  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** CI-3 heterogeneous semantic validation of P1.6 + Capability v7  
**Exact current point:** P1.6 v20 source-led partitioning is implemented and deterministic CI passes; dense `tG9K` live acceptance is the next gate.

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

No candidate artifact is public truth until its acceptance gate passes. Capability artifact 9 remains tied to analysis artifact 29.

## 3. Current candidate chain

```text
v17: agent/p16-v17-source-led-capacity                    PR #5
v18: agent/p16-v18-deterministic-structured-requirements  PR #6
v19: agent/p16-v19-depth-optionality-canonicalization     PR #7
v20: agent/p16-v20-source-led-partitioning                PR #8

active candidate:  job-analysis-english-v20
schema shape:      job-analysis-v5
public promotion:  NOT AUTHORIZED
```

Current detailed record:

```text
docs/working-memory/2026-08-14_P16_V20_SOURCE_LED_PARTITIONING.md
```

Supporting evidence trail:

```text
docs/working-memory/2026-08-14_P16_V16_DENSE_REGRESSION_FAILURE_AND_STATE_RECONCILIATION.md
docs/working-memory/2026-08-14_P16_V17_SOURCE_LED_CAPACITY_IMPLEMENTATION.md
docs/working-memory/2026-08-14_P16_V17_DENSE_COVERAGE_FEEDBACK_CORRECTION.md
docs/working-memory/2026-08-14_P16_V18_DETERMINISTIC_STRUCTURED_REQUIREMENTS.md
docs/working-memory/2026-08-14_P16_V19_DEPTH_OPTIONALITY_CANONICALIZATION.md
```

## 4. What the dense sequence established

### v17

- removed the arbitrary 32-requirement ceiling;
- aggregated dense coverage defects into one correction message;
- proved education/minimum-experience failures were unnecessary model ownership rather than a source-capacity problem.

### v18

- moved mechanically provable structured education and minimum experience to deterministic JobHunter ownership;
- kept ambiguous semantics model-owned and fail-closed;
- made every structured skill non-excludable coverage.

### v19

- kept preference/optionality (`a plus`, `helpful`) separate from technical depth;
- removed unsupported generated depth vocabulary such as `expertise` only when exact source evidence proves it was added by the model;
- preserved genuine source depth such as `Python (expert)`.

### v19 live dense result

No artifact persisted, but the previous v18 normalization failures were gone.

Generation 1 retained the four segment-13 facts:

```text
Python (expert)
SQL
MATLAB a plus
some C / C++ helpful
```

but omitted structured Python plus the long contextual stack.

Generation 2 repaired structured Python and the long contextual stack, but dropped those four already-valid segment-13 facts.

This is classified as **whole-answer retry oscillation / dense cognitive-load failure**, not a new semantic-rule defect.

## 5. Why v20 exists

V20 changes extraction granularity instead of weakening validation or asking one retry to regenerate the whole dense artifact.

```text
complete source-led coverage ledger
→ bounded independent semantic partitions
→ exact partition-scope enforcement
→ merge validated partitions
→ deterministic education/experience materialization
→ existing normalization/semantic guards
→ full original-source validation
→ persistence only if everything passes
```

### Partition rules

- maximum 8 model-owned requirement references per partition;
- core/non-excludable/required/preferred/structured-skill coverage processed first;
- contextual/excludable coverage processed in later slices;
- responsibility coverage belongs only to the first partition;
- every partition sees the full exact evidence catalog for grounding;
- every partition may emit claims only for its assigned coverage ledger;
- cross-partition requirement/duty/exclusion leakage fails closed;
- merge removes only exact duplicate identities;
- the whole merged artifact still has to satisfy the original complete source-led validators.

This prevents `fix B → forget A` behavior while preserving semantic strictness.

## 6. Strictness remains intact

V20 retains:

- exact evidence/provenance;
- no unsupported career claims;
- required/preferred/contextual separation;
- technical depth separate from obligation and normalized concept;
- deterministic structured education/minimum experience;
- structured-skill non-excludable coverage;
- source-led requirement capacity;
- qualification/residual decomposition accounting;
- responsibility coverage;
- skill/tool/knowledge/practice/domain/experience/education/other ontology;
- `experience` evidence guard;
- schedule/depth normalization;
- v19 depth/optionality canonicalization;
- duplicate protection;
- fail-closed persistence.

Partitioning is a workload/ownership change, not a weaker truth contract.

## 7. Deterministic verification

V20 implementation CI passed:

```text
run 747
Ruff: PASS
pytest: PASS
pytest -W error: PASS
```

Regression coverage proves:

- every dense coverage reference is assigned exactly once;
- every partition stays bounded;
- segment-13 facts and long contextual-stack facts survive merge together;
- structured Python and prose `Python (expert)` remain provenance-distinct;
- cross-partition leakage is rejected.

## 8. Next action — dense v20 `tG9K`

```bash
cd ~/projects/jobhunter

git fetch origin
git switch agent/p16-v20-source-led-partitioning
git pull --ff-only origin agent/p16-v20-source-led-partitioning

python scripts/run_p16_v20_candidate.py --job-id tG9K
```

Do not run `t4jp` yet.

If a v20 artifact persists, review it against accepted v9 artifact 29 and source/projection for:

- required `Master's degree`;
- `Professional experience` + exact `three to six years` depth;
- all six structured skills;
- all seven duty surfaces;
- no silent dense factual loss;
- `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort` correctly attached;
- MATLAB/C++ preferred with null technical depth unless independently supported;
- contextual technical stack retained as contextual;
- semiconductor-domain concept has no unsupported expertise wording;
- structured Python and prose `Python (expert)` remain provenance-distinct;
- concept-type differences reviewed after mechanical validity.

## 9. Sparse non-regression and promotion boundary

Only after dense v20 mechanical + semantic PASS:

```bash
python scripts/run_p16_v20_candidate.py --job-id t4jp
```

Compare against sparse v16 artifact 35.

Promotion remains blocked until:

```text
v20 deterministic CI PASS
+ dense tG9K mechanical PASS
+ dense tG9K semantic PASS
+ sparse t4jp non-regression PASS
```

Until then:

```text
public P1.6 promotion            → blocked
Capability v7 rebuild over v20  → blocked
Python/software CI-3 role       → blocked
network/security CI-3 role      → blocked
operations/platform CI-3 role   → blocked
```

After eventual P1.6 promotion, rebuild Capability v7 against the promoted P1.6 artifact rather than reusing artifact 9 as though it were current-chain.

## 10. Deferred boundaries

Blueprint remains implemented but not accepted for Phase-1 decision use. Do not create Blueprint v7 or resume nearby model shopping during this gate.

Historical fixed list ceilings outside the current requirements path (notably responsibility/coverage bounds) remain a later source-led-capacity audit unless live evidence proves they are current blockers.
