# P1.6 v20 — Second Live Scope/Depth Correction

**Date:** 2026-08-14  
**Status:** correction implemented; deterministic CI passed; dense live rerun pending  
**Candidate:** `job-analysis-english-v20` / `job-analysis-v5`  
**Branch:** `agent/p16-v20-source-led-partitioning`  
**Draft PR:** #8

## 1. Second live result

The second dense `tG9K` v20 run still did not persist an artifact, but it progressed beyond the first bounded partition. The earlier `some C / C++ helpful` failure did not recur. The failing partition had no responsibility ledger and contained seven model-owned requirement references:

```text
field:description:segment:22:clause:1
field:skills:0
field:skills:1
field:skills:2
field:skills:3
field:skills:4
field:skills:5
```

Both Instructor generations represented all six structured skills:

```text
Artificial Intelligence
Python
Microsoft Office
Machine learning
Linux
Git
```

The remaining blocking reference was exact evidence:

```text
industrial / edge deployment a plus
```

Generation 1 produced:

```text
concept:          Deployment
depth_signal:     industrial / edge deployment
requirement_type: preferred
concept_type:     experience
```

Generation 2 changed only the ontology classification:

```text
concept:          Deployment
depth_signal:     industrial / edge deployment
requirement_type: preferred
concept_type:     skill
```

Both were rejected because `industrial / edge deployment` is not an accepted technical-depth or experience-extent signal.

## 2. Semantic classification

The source contains two independent pieces of meaning:

```text
industrial / edge deployment   a plus
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   ^^^^^^
subject/scope                   preference
```

`industrial / edge` narrows what kind of deployment the employer is talking about. It does not state how deep, advanced, strong, proficient, experienced, or long-tenured the candidate must be.

The conservative normalized representation therefore keeps that exact scope in the concept and keeps depth null:

```text
concept:          industrial / edge deployment
requirement_type: preferred
depth_signal:     null
evidence:         industrial / edge deployment a plus
```

The ontology remains model-owned except for one fail-closed boundary: `concept_type=experience` is not allowed unless the exact evidence actually states prior applied exposure.

## 3. V20 correction

`AnalysisRequirementV20` now canonicalizes a preferred non-depth scope phrase only when all of the following are mechanically proven:

1. the requirement is already `preferred`;
2. `depth_signal` is a non-empty exact contiguous source excerpt;
3. the cited evidence independently contains explicit preference/optionality wording;
4. neither the evidence nor the proposed signal contains a recognized JobHunter depth/experience-extent marker;
5. the proposed signal is the same concept or ends with the existing normalized concept, proving it is a scoped form of that concept rather than an unrelated phrase.

For the live shape:

```text
concept=Deployment
depth_signal=industrial / edge deployment
```

V20 deterministically becomes:

```text
concept=industrial / edge deployment
depth_signal=null
```

Exact evidence remains unchanged.

## 4. Experience ontology guard

The first generation additionally typed the bare preferred scope as `experience` even though the source did not say experience, years, hands-on exposure, worked/background, or another prior-applied-exposure marker.

V20 does **not** silently relabel that to `skill` or another ontology. Instead it fails closed when all are true:

- requirement is preferred;
- model chooses `concept_type=experience`;
- exact evidence contains preference wording;
- exact evidence contains no explicit prior-applied-exposure signal.

This preserves the semantic contract that `experience` means prior applied exposure.

A source such as:

```text
Experience with industrial / edge deployment preferred
```

still permits `concept_type=experience`.

## 5. Regression coverage

`tests/test_analysis_v20_candidate.py` now proves:

- the exact live scope/depth shape moves `industrial / edge deployment` into the concept and clears depth;
- exact source evidence remains unchanged;
- unsupported preferred `experience` classification fails with an explicit prior-exposure error;
- explicit preferred experience evidence remains accepted;
- the previous C/C++ `some` normalization still works;
- real preferred technical depth remains preserved;
- partition/merge/scope-leakage regressions remain active.

## 6. Deterministic verification

Second-live correction implementation CI:

```text
run 759
Ruff: PASS
full pytest: PASS
pytest -W error: PASS
```

A final CI pass is required after rolling handoff/TODO reconciliation.

## 7. Acceptance boundary

Public/accepted truth remains unchanged:

```text
job-analysis-english-v9 / job-analysis-v4
tG9K P1.6 artifact 29
Capability v7 artifact 9 derived from artifact 29
```

No v20 artifact has persisted yet. Do not run sparse `t4jp`, rebuild Capability, advance heterogeneous-role review, promote P1.6, or merge the candidate PR chain.

## 8. Next live action

After pulling the reconciled v20 branch:

```bash
python scripts/run_p16_v20_candidate.py --job-id tG9K
```

If an artifact persists, perform the complete dense semantic acceptance review before authorizing sparse non-regression.
