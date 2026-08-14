# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-14  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Current gate:** CI-3 heterogeneous semantic validation of P1.6 + Capability v7  
**Exact current point:** P1.6 v18 deterministic-structured-requirement candidate is implemented and deterministic CI passes; dense `tG9K` live acceptance is the next gate.

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

## 3. Current isolated candidate

```text
base candidate branch:        agent/p16-v17-source-led-capacity
base draft PR:                #5
active branch:                agent/p16-v18-deterministic-structured-requirements
stacked draft PR:             #6
English P1.6 candidate:       job-analysis-english-v18
candidate schema shape:       job-analysis-v5
deterministic CI:             PASS (run 731 before docs reconciliation)
dense tG9K v18 live status:   NOT RUN YET
sparse t4jp v18 regression:   waits for dense semantic acceptance
public promotion:             NOT AUTHORIZED
```

Detailed current record:

```text
docs/working-memory/2026-08-14_P16_V18_DETERMINISTIC_STRUCTURED_REQUIREMENTS.md
```

Supporting history:

```text
docs/working-memory/2026-08-14_P16_V16_DENSE_REGRESSION_FAILURE_AND_STATE_RECONCILIATION.md
docs/working-memory/2026-08-14_P16_V17_SOURCE_LED_CAPACITY_IMPLEMENTATION.md
docs/working-memory/2026-08-14_P16_V17_DENSE_COVERAGE_FEEDBACK_CORRECTION.md
```

## 4. What v17 established

V17 corrected two real dense-path defects while preserving accepted/public v9/v4:

1. removed the inherited fixed 32-requirement ceiling from the isolated candidate;
2. changed response-level coverage feedback from first-error-only to one aggregate repair set while keeping one bounded retry.

The second live `tG9K` v17 run proved the aggregate feedback worked:

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

Positive but non-authoritative v17 signals included `Solid`, `Strong`, `Hands-on`, `Comfort`, Python `expert`, MATLAB/C++ preference, and broad dense stack coverage. No v17 artifact persisted.

## 5. Why v18 exists

The v17 rerun showed that some failures are caused by giving the LLM authority over facts whose representation JobHunter already knows exactly.

V18 therefore refines ownership rather than weakening validation:

```text
JobHunter owns
→ deterministic evidence identity
→ mechanically provable structured facts
→ coverage/provenance/accounting
→ fail-closed guards

LLM owns
→ bounded semantic interpretation where meaning/classification really requires reasoning
```

This is the preferred direction for reducing repeated model-format failures without accepting weaker data.

## 6. V18 deterministic structured facts

### Minimum experience

When the shared P1.6 years parser can prove an exact years phrase, JobHunter materializes:

```text
concept:           Professional experience
depth_signal:      exact years phrase
requirement_type:  required
concept_type:      experience
evidence:          exact structured field value
```

For `tG9K`:

```text
Professional experience
three to six years
```

If an experience field cannot be mechanically parsed, V18 does not guess; it remains model-owned/fail-closed.

### Education

A meaningful structured education credential is materialized directly as:

```text
concept:           exact credential value
requirement_type:  required
concept_type:      education
depth_signal:      null
evidence:          exact credential value
```

For `tG9K`, `Master's degree` no longer depends on LLM recall or formatting.

### Structured skills

Top-level `skills[]` remain model-visible because ontology classification can genuinely require semantic judgment. However every skill now receives an explicit non-excludable coverage reference so the aggregate retry reports all missing skills together and no structured skill may silently disappear.

## 7. Strictness remains intact

V18 does not bypass validation. The combined model + deterministic output still passes through:

- exact evidence/provenance checks;
- required/preferred/contextual strength rules;
- depth-neutral concept/depth separation;
- skill/tool/knowledge/practice/domain/experience/education/other ontology;
- qualification-vs-duty protection;
- structured-skill coverage;
- qualification/residual decomposition accounting;
- duplicate protection;
- source-led requirement capacity;
- one bounded correction and fail-closed behavior.

Deterministic structured requirements are inserted before the existing semantic/persistence/final-validation chain.

## 8. Deterministic verification

V18 implementation CI:

```text
run 731
head b95bcdfa4188adc26d715dfbf5c64a31ebfde00d
Ruff: PASS
pytest: PASS
pytest -W error: PASS
```

Regression tests prove deterministic partitioning, conservative fallback for unparseable experience, structured-skill coverage, aggregate missing-skill feedback, strict final validation, and idempotent materialization.

Documentation reconciliation commits follow this head and must keep normal CI green.

## 9. Next action — dense v18 `tG9K`

On the local machine:

```bash
git fetch origin
git switch agent/p16-v18-deterministic-structured-requirements
git pull --ff-only origin agent/p16-v18-deterministic-structured-requirements
python scripts/run_p16_v18_candidate.py --job-id tG9K
```

Do not run `t4jp` yet.

If a v18 artifact persists, review it against accepted v9 artifact 29 and the source/projection for:

- `Master's degree` present as required education;
- `Professional experience` + exact `three to six years` depth;
- all six structured skills represented;
- all seven duty surfaces represented;
- no dense factual assertion silently lost;
- `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort` correctly attached;
- MATLAB/C++ remain preferred;
- contextual technical-stack semantics remain contextual where source wording requires it;
- structured Python and prose `Python (expert)` remain provenance-distinct;
- concept-type differences reviewed only after mechanical validity.

If v18 fails, classify the concrete new failure rather than increasing retries or loosening semantic validation by default.

## 10. Sparse non-regression and promotion boundary

Only after dense v18 semantic acceptance:

```bash
python scripts/run_p16_v18_candidate.py --job-id t4jp
```

Compare against sparse v16 artifact 35. Deterministic ownership must not cause unsupported sparse extraction or fabricated duties/purpose.

Promotion remains blocked until:

```text
v18 deterministic CI PASS
+ dense tG9K mechanical PASS
+ dense tG9K semantic PASS
+ sparse t4jp non-regression PASS
```

Until then:

```text
public P1.6 promotion           → blocked
Capability v7 rebuild over v18 → blocked
Python/software CI-3 role      → blocked
network/security CI-3 role     → blocked
operations/platform CI-3 role  → blocked
```

After eventual P1.6 promotion, rebuild Capability v7 against the promoted P1.6 artifact rather than reusing artifact 9 as though it were current-chain.

## 11. Blueprint remains deferred

Blueprint remains implemented but not accepted for Phase-1 decision use. Do not create Blueprint v7, weaken its validators, or reopen nearby model shopping during this gate.

## 12. Later engineering audit

Historical fixed list ceilings remain elsewhere (notably responsibility/coverage bounds). They are not the current blocker unless live evidence demonstrates one, but they should receive a separate source-led-capacity audit after the current P1.6 acceptance path is stable.
