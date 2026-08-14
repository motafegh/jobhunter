# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-14  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** CI-3 heterogeneous semantic validation of P1.6 + Capability v7  
**Exact current point:** P1.6 v19 depth/optionality canonicalization candidate is implemented and deterministic CI passes; dense `tG9K` live acceptance is the next gate.

This file is not controlling. Product/domain/source/architecture constraints, roadmap/implementation plans, the active semantic-quality acceptance plan, and `docs/EXECUTION_TODO.md` win on conflict. Dated working-memory records preserve the detailed evidence trail.

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

No candidate artifact is public truth until its acceptance gate passes. Capability artifact 9 remains tied to analysis artifact 29.

## 3. Current isolated candidate chain

```text
v17 branch:                   agent/p16-v17-source-led-capacity
v17 draft PR:                 #5
v18 branch:                   agent/p16-v18-deterministic-structured-requirements
v18 stacked draft PR:         #6
active v19 branch:            agent/p16-v19-depth-optionality-canonicalization
active stacked draft PR:      #7
English P1.6 candidate:       job-analysis-english-v19
candidate schema shape:       job-analysis-v5
deterministic CI:             PASS (run 737 before docs reconciliation)
dense tG9K v19 live status:   NOT RUN YET
sparse t4jp v19 regression:   waits for dense semantic acceptance
public promotion:             NOT AUTHORIZED
```

Detailed current record:

```text
docs/working-memory/2026-08-14_P16_V19_DEPTH_OPTIONALITY_CANONICALIZATION.md
```

Supporting history:

```text
docs/working-memory/2026-08-14_P16_V16_DENSE_REGRESSION_FAILURE_AND_STATE_RECONCILIATION.md
docs/working-memory/2026-08-14_P16_V17_SOURCE_LED_CAPACITY_IMPLEMENTATION.md
docs/working-memory/2026-08-14_P16_V17_DENSE_COVERAGE_FEEDBACK_CORRECTION.md
docs/working-memory/2026-08-14_P16_V18_DETERMINISTIC_STRUCTURED_REQUIREMENTS.md
```

## 4. What v17 established

V17 corrected two real dense-path defects while preserving accepted/public v9/v4:

1. removed the inherited fixed 32-requirement ceiling from the isolated candidate;
2. changed response-level coverage feedback from first-error-only to one aggregate repair set while keeping one bounded retry.

The second live `tG9K` v17 run proved aggregate feedback worked:

```text
generation 1
→ all seven duties represented
→ dense requirements represented
→ one error reported BOTH field:minimum_experience + field:education

generation 2
→ added both structured facts
→ failed because concept included years wording:
   "Professional experience of three to six years"
→ strict depth-neutral concept rule correctly rejected it
```

No v17 artifact persisted.

## 5. What v18 established

The v17 rerun showed some failures came from giving the LLM authority over facts whose representation JobHunter already knows exactly.

V18 refined ownership:

```text
JobHunter owns
→ deterministic evidence identity
→ mechanically provable structured facts
→ coverage/provenance/accounting
→ fail-closed guards

LLM owns
→ bounded semantic interpretation where meaning/classification really requires reasoning
```

V18 moved parseable structured minimum experience and structured education out of model ownership while leaving ambiguous/unparseable experience model-owned. Structured skills remained model-visible because concept-type classification can require semantic judgment, but every skill received explicit non-excludable coverage.

The first dense v18 live run then failed on a narrower representation class, not on education/experience coverage.

## 6. First dense v18 live run — confirmed narrower blocker

Command:

```bash
python scripts/run_p16_v18_candidate.py --job-id tG9K
```

No v18 artifact persisted.

The generated output represented:

- all seven duty surfaces;
- all six structured skills;
- broad dense technical-stack coverage;
- required/preferred/contextual distinctions broadly correctly.

Three typed-item validation failures remained in both Instructor generations:

```text
MATLAB a plus
→ requirement_type = preferred
→ depth_signal = "a plus"
→ invalid because optionality is not technical depth

some C / C++ helpful
→ requirement_type = preferred
→ depth_signal = "helpful"
→ invalid because optionality is not technical depth

Semiconductor domain: FDC / APC / SPC, ...
→ generated concept added unsupported word "expertise"
→ strict depth-neutral concept rule rejected it
```

This failure does not justify weakening strictness. It demonstrates a mechanical normalization boundary:

```text
obligation / optionality != technical depth
```

and normalized concepts must not gain unsupported depth vocabulary.

## 7. Why v19 exists

V19 canonicalizes only mechanically provable depth/optionality representation mistakes before inherited strict item validation.

### Preference wording in depth_signal

V19 clears `depth_signal` only when all are true:

1. requirement is already `preferred`;
2. proposed depth contains no accepted P1.6 depth/experience-extent signal;
3. proposed depth itself contains explicit optionality wording;
4. exact cited evidence also contains explicit optionality wording.

Therefore:

```text
MATLAB a plus
→ preferred
→ depth_signal = null

some C / C++ helpful
→ preferred
→ depth_signal = null
```

Obligation and exact evidence remain unchanged.

### Unsupported depth vocabulary in concept

V19 may remove a depth token from a generated concept only when:

1. the generated concept contains a token already classified by P1.6 as depth vocabulary;
2. that token is absent from the cited exact source evidence;
3. cleanup leaves a meaningful non-generic concept.

If cleanup would destroy the concept, no repair is applied and strict validation still fails closed.

For `tG9K`:

```text
source:     Semiconductor domain: FDC / APC / SPC, ...
generated:  Semiconductor domain expertise (...)
v19:        Semiconductor domain (...)
```

Exact evidence remains unchanged.

## 8. Strictness remains intact

V19 does not bypass validation. It preserves:

- v18 deterministic structured education/minimum-experience ownership;
- v18 structured-skill coverage;
- v17 source-led requirement capacity;
- v17 aggregate dense coverage feedback;
- exact evidence/provenance checks;
- required/preferred/contextual strength rules;
- genuine source depth extraction;
- depth-neutral normalized concepts;
- skill/tool/knowledge/practice/domain/experience/education/other ontology;
- qualification-vs-duty protection;
- qualification/residual decomposition accounting;
- responsibility coverage;
- duplicate protection;
- one bounded correction and fail-closed behavior.

Regression coverage explicitly proves genuine `Python (expert)` still becomes:

```text
concept = Python
depth_signal = expert
```

and a cleanup that would leave only an empty/generic concept remains rejected.

## 9. Deterministic verification

V19 implementation CI:

```text
run 737
head e19feb1fa70ed4e4bb8e8458cf289785a1c917bb
Ruff: PASS
pytest: PASS
pytest -W error: PASS
```

The regression suite includes the exact three live v18 failure shapes in one typed response and proves they validate together under v19.

Documentation reconciliation commits follow this head and must keep the normal CI gate green.

## 10. Next action — dense v19 `tG9K`

On the local machine:

```bash
git fetch origin
git switch agent/p16-v19-depth-optionality-canonicalization
git pull --ff-only origin agent/p16-v19-depth-optionality-canonicalization
python scripts/run_p16_v19_candidate.py --job-id tG9K
```

Do not run `t4jp` yet.

If a v19 artifact persists, review it against accepted v9 artifact 29 and source/projection for:

- `Master's degree` present as required education;
- `Professional experience` + exact `three to six years` depth;
- all six structured skills represented;
- all seven duty surfaces represented;
- no dense factual assertion silently lost;
- `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort` correctly attached;
- MATLAB/C++ remain preferred with null technical depth unless an independent depth phrase exists;
- contextual technical-stack semantics remain contextual where source wording requires it;
- semiconductor-domain concept does not gain unsupported expertise wording;
- structured Python and prose `Python (expert)` remain provenance-distinct;
- concept-type differences reviewed only after mechanical validity.

If v19 fails, classify the concrete new failure rather than increasing retries or loosening semantic validation by default.

## 11. Sparse non-regression and promotion boundary

Only after dense v19 semantic acceptance:

```bash
python scripts/run_p16_v19_candidate.py --job-id t4jp
```

Compare against sparse v16 artifact 35. Deterministic ownership/canonicalization must not cause unsupported sparse extraction or fabricated duties/purpose.

Promotion remains blocked until:

```text
v19 deterministic CI PASS
+ dense tG9K mechanical PASS
+ dense tG9K semantic PASS
+ sparse t4jp non-regression PASS
```

Until then:

```text
public P1.6 promotion            → blocked
Capability v7 rebuild over v19  → blocked
Python/software CI-3 role       → blocked
network/security CI-3 role      → blocked
operations/platform CI-3 role   → blocked
```

After eventual P1.6 promotion, rebuild Capability v7 against the promoted P1.6 artifact rather than reusing artifact 9 as though it were current-chain.

## 12. Blueprint remains deferred

Blueprint remains implemented but not accepted for Phase-1 decision use. Do not create Blueprint v7, weaken its validators, or reopen nearby model shopping during this gate.

## 13. Later engineering audit

Historical fixed list ceilings remain elsewhere (notably responsibility/coverage bounds). They are not the current blocker unless live evidence demonstrates one, but they should receive a separate source-led-capacity audit after the current P1.6 acceptance path is stable.
