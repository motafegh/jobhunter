# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-14  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** CI-3 heterogeneous semantic validation of P1.6 + Capability v7  
**Exact current point:** the second dense `tG9K` v20 live run progressed beyond the previously failing first partition, then failed on `industrial / edge deployment` being misfiled as technical depth. The narrow v20 scope/depth + experience-evidence correction is implemented and CI run 759 passes; dense `tG9K` v20 rerun is next.

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
public promotion:  NOT AUTHORIZED
```

Current detailed v20 records:

```text
docs/working-memory/2026-08-14_P16_V20_SOURCE_LED_PARTITIONING.md
docs/working-memory/2026-08-14_P16_V20_FIRST_LIVE_PARTITION_CORRECTION.md
docs/working-memory/2026-08-14_P16_V20_SECOND_LIVE_SCOPE_DEPTH_CORRECTION.md
```

Earlier dense correction trail:

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
- exposed unnecessary model ownership of mechanically known education/minimum-experience facts.

### v18

- moved mechanically provable structured education and minimum experience to JobHunter ownership;
- kept ambiguous semantics model-owned and fail-closed;
- made every structured skill non-excludable coverage.

### v19

- kept optionality (`a plus`, `helpful`) separate from technical depth;
- removed unsupported generated depth vocabulary only when exact source evidence proves it was model-added;
- preserved real source depth such as `Python (expert)`;
- dense live run exposed whole-answer retry oscillation: one generation repaired a subset while losing another already-valid subset.

### v20

V20 changes extraction granularity rather than weakening validation or increasing retries:

```text
complete source-led coverage ledger
→ bounded independent semantic partitions
→ exact partition-scope enforcement
→ merge validated partitions
→ deterministic education/experience materialization
→ inherited normalization/semantic guards
→ full original-source validation
→ persistence only if everything passes
```

Each model-owned requirement partition is bounded to at most 8 references. Responsibility coverage belongs only to partition 1. Cross-partition requirement/duty/exclusion leakage fails closed.

## 5. First live v20 result and correction

The first live `tG9K` v20 run stopped in partition 1 on:

```text
some C / C++ helpful
→ preferred
→ model depth_signal=some
```

`some` is preserved in exact evidence but is not accepted JobHunter technical depth. V20 now clears it only in the mechanically proven preferred case while preserving real depth such as `Strong`.

The same run showed a role-purpose/responsibility semantic drift. No tG9K-specific rewrite was added; the prompt now reinforces high-level purpose vs concrete-duty semantics, which remains an acceptance-review item after persistence.

Implementation CI for that correction: run 753 PASS. Documentation-reconciled CI: run 756 PASS.

## 6. Second live v20 result — current evidence

The second live `tG9K` run **progressed past the prior partition-1 blocker**. That is evidence that the first correction worked and that bounded partitioning is advancing rather than oscillating over the whole artifact.

The failing later partition had no responsibility ledger and contained:

```text
field:description:segment:22:clause:1
field:skills:0
field:skills:1
field:skills:2
field:skills:3
field:skills:4
field:skills:5
```

Both generations represented all six structured skills:

```text
Artificial Intelligence
Python
Microsoft Office
Machine learning
Linux
Git
```

The blocker was:

```text
source:            industrial / edge deployment a plus
model concept:     Deployment
model depth:       industrial / edge deployment
requirement_type:  preferred
```

Generation 1 typed it as `experience`; generation 2 changed the type to `skill`, but both retained the invalid depth representation. No artifact persisted.

## 7. Current v20 correction

The source means:

```text
industrial / edge deployment   a plus
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   ^^^^^^
subject/scope                   preference
```

V20 now handles this conservatively:

```text
concept:          industrial / edge deployment
requirement_type: preferred
depth_signal:     null
exact evidence:   unchanged
```

The scope move happens only when the proposed signal is an exact source excerpt, the evidence independently proves preference, no accepted depth marker exists, and the signal is mechanically the same concept with additional leading scope.

Separately, preferred `concept_type=experience` now fails unless the exact evidence explicitly states prior applied exposure. V20 does **not** silently relabel unsupported experience to skill/domain/practice; ontology remains model-owned within the strict evidence boundary.

Regression coverage proves:

- exact live scope phrase moves from depth into concept without losing evidence;
- unsupported preferred `experience` fails closed;
- explicit preferred experience remains accepted;
- previous C/C++ `some` normalization still passes;
- genuine preferred depth remains preserved;
- all partition/merge/leakage tests remain active.

Implementation CI:

```text
run 759
Ruff: PASS
full pytest: PASS
pytest -W error: PASS
```

## 8. Strictness remains intact

V20 retains:

- exact evidence/provenance;
- no unsupported career claims;
- required/preferred/contextual separation;
- technical depth separate from obligation and concept scope;
- prior-applied-exposure evidence for `experience`;
- deterministic structured education/minimum experience;
- structured-skill non-excludable coverage;
- source-led requirement capacity;
- qualification/residual decomposition accounting;
- responsibility coverage;
- skill/tool/knowledge/practice/domain/experience/education/other ontology;
- schedule/depth normalization;
- v19 depth/optionality canonicalization;
- duplicate protection;
- fail-closed persistence.

These corrections move mechanically provable representation decisions out of the LLM path; they do not weaken the truth contract.

## 9. Next action — dense v20 `tG9K` rerun

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
- correct high-level role purpose and concrete duty surfaces;
- no silent dense factual loss;
- `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort` correctly attached;
- MATLAB/C++ preferred with null technical depth unless independently supported;
- `industrial / edge deployment` retains scope without fabricated technical depth or experience;
- contextual technical stack remains contextual;
- semiconductor-domain concept has no unsupported expertise wording;
- structured Python and prose `Python (expert)` remain provenance-distinct;
- concept-type differences reviewed after mechanical validity.

## 10. Promotion boundary

Only after dense v20 mechanical + semantic PASS:

```bash
python scripts/run_p16_v20_candidate.py --job-id t4jp
```

Compare with sparse v16 artifact 35.

Promotion requires:

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
candidate PR merge              → blocked
```

After eventual P1.6 promotion, rebuild Capability v7 against the promoted P1.6 artifact rather than treating artifact 9 as current-chain.

## 11. Deferred boundaries

Blueprint remains implemented but not accepted for Phase-1 decision use. Do not create Blueprint v7 or resume nearby model shopping during this gate.

Historical fixed list ceilings outside the current requirements path remain a later source-led-capacity audit unless live evidence proves they are current blockers.
