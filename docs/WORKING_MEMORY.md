# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-14  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** CI-3 heterogeneous semantic validation of P1.6 + Capability v7  
**Exact current point:** dense `tG9K` P1.6 v20 finally persisted as artifact **36** with 33 requirements and 8 responsibilities. Mechanical generation/persistence passed. V20-specific snapshot export/audit tooling is implemented and CI passes. Next gate is **mechanical snapshot audit + full semantic review of artifact 36**. Do not run sparse `t4jp` yet.

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

Accepted dense chain:

```text
tG9K English projection artifact 33
→ P1.6 v9 artifact 29
→ Capability v7 artifact 9
```

Sparse calibration anchor: `t4jp` P1.6 v16 artifact 35.

No candidate artifact is public truth until its acceptance gate passes. Capability artifact 9 remains tied to analysis artifact 29.

## 3. Current candidate chain

```text
v17: agent/p16-v17-source-led-capacity                    PR #5
v18: agent/p16-v18-deterministic-structured-requirements  PR #6
v19: agent/p16-v19-depth-optionality-canonicalization     PR #7
v20: agent/p16-v20-source-led-partitioning                PR #8

active candidate:  job-analysis-english-v20
schema shape:      job-analysis-v5
candidate artifact: tG9K artifact 36
public promotion:  NOT AUTHORIZED
```

Current v20 records:

```text
docs/working-memory/2026-08-14_P16_V20_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-14_P16_V20_FIRST_LIVE_PARTITION_CORRECTION.md
docs/working-memory/2026-08-14_P16_V20_SECOND_LIVE_SCOPE_DEPTH_CORRECTION.md
docs/working-memory/2026-08-14_P16_V20_DENSE_ARTIFACT_36_PERSISTED.md
```

Earlier dense correction trail remains in the dated v16-v19 records.

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

- separated optionality (`a plus`, `helpful`) from technical depth;
- removed unsupported generated depth vocabulary only when exact source evidence proves it was model-added;
- preserved genuine source depth;
- exposed whole-answer retry oscillation on dense coverage.

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

Live corrections also established:

- `some C / C++ helpful` → preferred, null technical depth, exact evidence preserved;
- `industrial / edge deployment a plus` → scope belongs in concept, not depth;
- unsupported preferred `experience` remains fail-closed unless exact evidence states prior applied exposure;
- high-level role purpose vs concrete responsibilities remains a semantic review boundary, not a tG9K-specific deterministic rewrite.

## 5. First persisted dense v20 artifact

Latest local run:

```text
Outcome: completed
English P1.6 v20 candidate for tG9K
Artifact: 36
Model: gemma-4-e4b-it-ud
Contract: job-analysis-english-v20 / job-analysis-v5
Responsibilities: 8
Requirements: 33
```

This proves the current v20 path can complete generation, partition validation, merge, deterministic materialization, inherited normalization, full source-led validation, and persistence.

It does **not** yet prove semantic acceptance.

Immediate review signal:

```text
accepted v9 responsibilities: 7
v20 artifact 36 responsibilities: 8
```

Therefore purpose-vs-duty classification must be reviewed explicitly; counts are not an acceptance criterion by themselves.

## 6. V20 review tooling

V20-specific review tools now exist and are bound to `job-analysis-english-v20 / job-analysis-v5`:

```bash
python scripts/export_p16_v20_candidate_snapshot.py --job-id tG9K
python scripts/audit_p16_v20_candidate_snapshot.py --job-id tG9K
```

The exporter selects the current v20 artifact and its exact English-projection dependency. The auditor checks the v20 prompt/schema identity, projection dependency, structured-skill/qualification/residual coverage accounting, decomposition, concept hygiene, schedule/depth rules, and unsupported ability→experience typing.

Review-tool CI passed Ruff, full pytest, and pytest with warnings as errors.

## 7. Current action — artifact 36 review

On the local machine:

```bash
cd ~/projects/jobhunter

git pull --ff-only origin agent/p16-v20-source-led-partitioning

python scripts/export_p16_v20_candidate_snapshot.py --job-id tG9K
python scripts/audit_p16_v20_candidate_snapshot.py --job-id tG9K
```

Then inspect/upload:

```text
review-snapshots/jobs/tG9K.json
```

Do **not** run `t4jp` yet.

Dense semantic acceptance checklist for artifact 36:

- required `Master's degree`;
- `Professional experience` + exact `three to six years` depth;
- all six structured skills;
- correct high-level role purpose and concrete duty surfaces;
- no silent dense factual loss versus source/projection and accepted v9 artifact 29;
- `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort` correctly attached;
- MATLAB/C++ preferred with null technical depth unless independently supported;
- `industrial / edge deployment` retains scope without fabricated depth or experience;
- contextual technical stack remains contextual;
- semiconductor-domain concept has no unsupported expertise wording;
- structured Python and prose `Python (expert)` remain provenance-distinct;
- concept-type differences are semantically defensible.

## 8. Promotion boundary

Only after artifact 36 mechanical + semantic PASS:

```bash
python scripts/run_p16_v20_candidate.py --job-id t4jp
```

Sparse v20 must then non-regress against accepted sparse v16 artifact 35.

Promotion requires:

```text
v20 deterministic CI PASS
+ dense tG9K mechanical snapshot audit PASS
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
candidate PR merge              → blocked
```

After eventual P1.6 promotion, rebuild Capability v7 against the promoted P1.6 artifact rather than treating artifact 9 as current-chain.

## 9. Deferred boundaries

Blueprint remains implemented but not accepted for Phase-1 decision use. Do not create Blueprint v7 or resume nearby model shopping during this gate.

Historical fixed list ceilings outside the current requirements path remain a later source-led-capacity audit unless live evidence proves they are current blockers.
