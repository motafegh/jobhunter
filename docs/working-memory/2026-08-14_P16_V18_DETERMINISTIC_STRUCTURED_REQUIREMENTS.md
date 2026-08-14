# P1.6 v18 Deterministic Structured Requirements

**Date:** 2026-08-14  
**Status:** Implemented candidate / deterministic CI PASS / live dense acceptance pending  
**Branch:** `agent/p16-v18-deterministic-structured-requirements`  
**Stacked draft PR:** #6 (base: `agent/p16-v17-source-led-capacity`)  
**Candidate:** `job-analysis-english-v18` / `job-analysis-v5`  
**Public accepted P1.6 remains:** `job-analysis-english-v9` / `job-analysis-v4`

## 1. Why v18 exists

V17 solved two real dense-path defects without weakening P1.6 semantics:

1. the inherited 32-requirement representation ceiling;
2. fail-fast response-level coverage feedback that exposed only one missing reference per retry.

The second live dense `tG9K` v17 run proved the aggregate-feedback correction worked. Generation 1
reported both missing structured fields in the same error:

```text
field:minimum_experience
field:education
```

The single Instructor retry then added both fields. However, it encoded the experience requirement
as:

```text
concept:       Professional experience of three to six years
depth_signal:  three to six years
```

The strict P1.6 depth validator correctly rejected this because the normalized concept must remain
depth-neutral. The desired representation is:

```text
concept:       Professional experience
depth_signal:  three to six years
```

This failure is not a reason to weaken the validator. It demonstrates that the model still owns a
fact whose representation JobHunter can derive mechanically and exactly.

## 2. Architectural decision

Refine P1.6 ownership:

```text
JobHunter code
→ deterministic evidence identity
→ mechanically provable structured facts
→ coverage/provenance/accounting
→ fail-closed guards

LLM
→ bounded semantic interpretation only where classification, normalization,
  optionality, ontology, or meaning genuinely requires reasoning
```

The objective is not fewer checks. The objective is fewer unnecessary model failure modes while
preserving the same strict correctness contract.

## 3. Deterministic minimum-experience ownership

V18 examines the structured `minimum_experience` field using the same shared P1.6 years-pattern
already used by the strict depth validator.

When an exact years extent is mechanically provable, for example:

```text
three to six years
```

JobHunter creates:

```text
concept:           Professional experience
depth_signal:      three to six years
requirement_type:  required
concept_type:      experience
evidence:          three to six years
confidence:        high
```

The exact structured field is removed from the model-facing evidence view for that call, so the
model cannot duplicate, omit, or mis-normalize it.

This is conservative. If the existing parser cannot prove an exact years phrase, for example:

```text
Several years of professional experience
```

V18 does **not** guess. The field remains model-visible/model-owned and the existing fail-closed
validation path remains authoritative.

## 4. Deterministic education ownership

A meaningful structured education field is already a credential-valued source fact. V18 therefore
materializes it directly:

```text
concept:           exact education field value
requirement_type:  required
concept_type:      education
depth_signal:      null
evidence:          exact education field value
confidence:        high
```

For `tG9K`, `Master's degree` therefore no longer depends on the model remembering or formatting
that structured field correctly.

## 5. Structured skills remain semantic but cannot disappear

V18 deliberately does **not** deterministically assign `concept_type` to all top-level `skills[]`.
A structured item such as Linux/Git/Microsoft Office can be a tool, while broader AI/ML labels may
need semantic ontology judgment.

Instead:

- every non-empty `skills[]` item remains visible to the model;
- every `field:skills:N` receives an explicit non-excludable requirement-coverage entry;
- obligation hint remains `required` under the current candidate contract;
- v17 aggregate feedback reports all omitted skills together in the one bounded retry.

Thus JobHunter owns skill coverage/provenance while the model retains only the semantic
classification that actually requires interpretation.

## 6. Validation remains strict

The deterministic additions are not a validator bypass.

After generation, V18:

1. appends deterministic structured requirements;
2. preserves v15 schedule/concept normalization;
3. injects deterministic decomposition bookkeeping;
4. validates the combined output through the existing v10→v16 semantic guards;
5. persists through the existing v14 provenance/coverage path;
6. validates the persisted combined artifact through the v17 source-led final evidence guard.

Therefore exact evidence, depth separation, obligation strength, ontology, structured-skill
coverage, qualification-vs-duty separation, decomposition, duplicate protection, and fail-closed
behavior remain intact.

## 7. Candidate files

```text
src/jobhunter/analysis_service_v18.py
src/jobhunter/analysis_runtime_v18.py
scripts/run_p16_v18_candidate.py
tests/test_analysis_v18_candidate.py
```

## 8. Regression coverage

The v18 tests prove:

- distinct prompt identity `job-analysis-english-v18`;
- schema shape remains source-led `job-analysis-v5` with no legacy requirement cap;
- parseable minimum experience and education leave the model-facing field set;
- exact deterministic `Professional experience` + years-depth representation;
- exact deterministic education representation;
- unrecognized experience wording remains model-owned rather than guessed;
- every structured skill gets non-excludable explicit coverage;
- aggregate retry feedback reports all omitted structured skills together;
- deterministic + model-generated requirements pass the existing strict validation/persistence
  chain;
- deterministic materialization is idempotent.

## 9. Deterministic verification

Final implementation CI before documentation reconciliation:

```text
CI run 731
head b95bcdfa4188adc26d715dfbf5c64a31ebfde00d
Ruff: PASS
pytest: PASS
pytest -W error: PASS
```

Documentation commits must also leave the normal CI gate green before the live run is treated as
the current handoff.

## 10. Live acceptance gate

Run only dense `tG9K` next:

```bash
python scripts/run_p16_v18_candidate.py --job-id tG9K
```

A persisted artifact is necessary but not sufficient. Review against accepted v9 artifact 29 and
the source/projection for:

- `Master's degree` present as required education;
- `Professional experience` present with exact `three to six years` depth;
- all six structured `skills[]` represented;
- all seven duty surfaces represented;
- no dense factual coverage silently lost;
- `Solid`, Python `expert`, `Strong`, `Hands-on`, and `Comfort` correctly attached;
- MATLAB/C++ remain preferred;
- contextual stack remains contextual where source wording requires it;
- structured Python and prose `Python (expert)` remain provenance-distinct;
- concept-type differences are reviewed separately after mechanical validity.

If v18 still fails, classify the new concrete failure. Do not increase retries or loosen semantic
validation by default.

## 11. Sparse non-regression and promotion boundary

Only after dense v18 yields a semantically accepted artifact, run:

```bash
python scripts/run_p16_v18_candidate.py --job-id t4jp
```

Compare against accepted sparse v16 artifact 35. Deterministic ownership must not cause sparse
over-extraction or fabricated duties.

Promotion remains blocked until:

```text
v18 deterministic CI PASS
+ dense tG9K mechanical PASS
+ dense tG9K semantic PASS
+ sparse t4jp non-regression PASS
```

Until then:

- public P1.6 remains v9/v4;
- Capability v7 artifact 9 remains tied to P1.6 artifact 29;
- no Capability rebuild over v18;
- no heterogeneous-role progression;
- PR #5 and stacked PR #6 remain candidate/draft work.
