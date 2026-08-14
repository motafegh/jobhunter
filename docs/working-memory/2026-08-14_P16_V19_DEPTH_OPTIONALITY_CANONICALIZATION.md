# P1.6 v19 — Depth / Optionality Canonicalization

**Date:** 2026-08-14  
**Status:** Candidate implementation complete; deterministic CI PASS; dense live acceptance pending  
**Branch:** `agent/p16-v19-depth-optionality-canonicalization`  
**Stacked draft PR:** #7  
**Base candidate:** P1.6 v18 / PR #6  
**Prompt:** `job-analysis-english-v19`  
**Schema shape:** `job-analysis-v5`

## 1. Why this candidate exists

The first dense `tG9K` live run on P1.6 v18 failed before persistence after the initial generation plus one Instructor retry.

V18 had already removed structured education and parseable minimum experience from model ownership. The live failure therefore moved to a narrower requirement-normalization boundary.

The generated dense output represented all seven responsibility surfaces and all six structured skills, but three requirement items were mechanically invalid:

```text
MATLAB a plus
→ requirement_type = preferred
→ depth_signal = "a plus"

some C / C++ helpful
→ requirement_type = preferred
→ depth_signal = "helpful"

Semiconductor domain: FDC / APC / SPC, ...
→ generated concept = "Semiconductor domain expertise (...)"
→ source itself does not contain expert/expertise depth wording
```

The same three validation errors remained after the one bounded Instructor retry.

No v18 artifact persisted.

## 2. Failure classification

This is not evidence that the semantic validators are too strict.

The validators correctly distinguish:

```text
obligation / optionality
!=
technical depth
```

Therefore:

```text
"a plus" / "helpful"
→ preferred obligation
→ not depth_signal
```

Likewise, a normalized concept must not introduce unsupported depth vocabulary such as `expertise` when the cited source says only `Semiconductor domain: ...`.

The failure class is therefore:

```text
model produces factually recognizable requirement
→ model leaks optionality wording into depth_signal
  OR adds unsupported depth vocabulary to normalized concept
→ strict typed validation rejects before persistence
```

## 3. V19 ownership decision

Do not weaken the strict validator and do not increase retries.

Instead, canonicalize only mechanically provable representation mistakes before strict item validation.

### Optionality-only depth

V19 clears `depth_signal` only when all of the following are true:

1. `requirement_type == preferred`;
2. the proposed `depth_signal` contains no accepted P1.6 depth/experience-extent signal;
3. the proposed signal itself contains explicit optionality wording;
4. the exact cited source evidence also contains explicit optionality wording.

The preferred obligation remains unchanged.

For the live case:

```text
MATLAB
preferred
MATLAB a plus
→ depth_signal = null

C / C++
preferred
some C / C++ helpful
→ depth_signal = null
```

### Unsupported depth wording in concept

V19 inspects the same depth vocabulary already used by the strict P1.6 depth validator.

A generated depth token may be removed from the normalized concept only when:

1. that depth token occurs in the generated concept;
2. the same token does not occur in the cited exact source evidence;
3. cleanup leaves a non-empty, non-generic concept.

If cleanup would destroy the concept, V19 leaves it unchanged and inherited strict validation still fails closed.

For the live case:

```text
source:
Semiconductor domain: FDC / APC / SPC, virtual metrology, run-to-run control, yield analysis

generated:
Semiconductor domain expertise (...)

v19 canonicalized concept:
Semiconductor domain (...)
```

Exact evidence is unchanged.

## 4. What v19 does not change

V19 preserves all prior candidate boundaries:

- v18 deterministic structured education ownership;
- v18 deterministic parseable minimum-experience ownership;
- v18 explicit non-excludable structured-skill coverage;
- v17 source-led requirement capacity;
- v17 aggregate dense coverage feedback;
- exact evidence/provenance;
- required/preferred/contextual strength semantics;
- genuine source depth extraction;
- concept ontology;
- qualification-vs-duty separation;
- qualification/residual decomposition;
- responsibility coverage;
- duplicate protection;
- one bounded correction;
- fail-closed behavior.

Genuine source depth is not cleared. Example regression coverage proves `Python (expert)` still yields:

```text
concept = Python
depth_signal = expert
```

## 5. Regression coverage

`tests/test_analysis_v19_candidate.py` proves:

- v19 has a distinct prompt identity and keeps the v5 source-led schema shape;
- `MATLAB a plus` preserves preferred obligation and canonicalizes depth to null;
- `some C / C++ helpful` preserves preferred obligation and canonicalizes depth to null;
- unsupported `expertise` is removed from the semiconductor-domain normalized concept;
- genuine source `expert` depth remains preserved;
- cleanup that would destroy the concept still fails closed;
- the exact three live v18 failure shapes validate together under the v19 typed response.

## 6. Deterministic verification

After Ruff import cleanup:

```text
CI run 737
head e19feb1fa70ed4e4bb8e8458cf289785a1c917bb
Ruff: PASS
pytest: PASS
pytest -W error: PASS
```

This proves the exact known v18 failure trio is mechanically removed without weakening the inherited semantic/final-validation stack.

## 7. Current acceptance boundary

V19 is still a candidate. Public P1.6 remains v9/schema-v4.

Next run only dense `tG9K`:

```bash
git fetch origin
git switch agent/p16-v19-depth-optionality-canonicalization
git pull --ff-only origin agent/p16-v19-depth-optionality-canonicalization
python scripts/run_p16_v19_candidate.py --job-id tG9K
```

Do not run sparse `t4jp` yet.

If a v19 artifact persists, review against accepted v9 artifact 29/source projection for:

- required `Master's degree`;
- `Professional experience` + exact `three to six years` depth;
- all six structured skills;
- all seven duty surfaces;
- no silent dense fact loss;
- `Solid`, Python `expert`, `Strong`, `Hands-on`, `Comfort` correctly attached;
- MATLAB and C/C++ preferred with null technical depth unless the source independently supplies depth;
- contextual technical-stack semantics preserved;
- semiconductor-domain concept no longer gains unsupported expertise wording;
- structured Python and prose `Python (expert)` remain provenance-distinct.

Only after dense semantic PASS should sparse `t4jp` v19 non-regression run.

## 8. Promotion boundary

Until dense + sparse v19 acceptance:

```text
public P1.6 promotion          → blocked
Capability rebuild over v19   → blocked
heterogeneous CI-3 progression → blocked
PR #5 / #6 / #7               → candidate/draft chain
```
