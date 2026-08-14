# P1.6 v16 Sparse Acceptance — t4jp

**Date:** 2026-08-14  
**Gate:** CI-3 sparse/ambiguous P1.6 calibration  
**Job:** `t4jp`  
**Status:** **ACCEPTED for the bounded sparse case; dense regression is next**

## Accepted artifact

```text
English P1.6 artifact: 35
Prompt:                 job-analysis-english-v16
Schema:                 job-analysis-v4
Model:                  gemma-4-e4b-it-ud
Translation artifact:   34
Job detail version:     41
Requirements:           8
Responsibilities:       0
Role purpose:           0
```

The committed review snapshot passed the v16 mechanical audit before semantic review.

## Semantic review

The eight persisted requirements are source-grounded and semantically acceptable for this sparse case:

1. `Artificial Intelligence` — `skill` — required — structured required skill.
2. `Video content production` — `skill` — required — structured required skill.
3. `Social networks` — `skill` — required — structured required skill.
4. `Content creation with AI` — `skill` — required — explicit qualification.
5. `Creativity in creating visual and video content` — `other` — required — explicit candidate-quality expectation.
6. `Website design` — `skill` — required — explicit qualification.
7. `Production of visual content` — `skill` — required — exact evidence remains `ability to produce visual content full-time and part-time`; schedule wording is not retained in the normalized concept or depth, and the evidence is not mis-typed as prior experience.
8. `Ethics and work commitment` — `other` — required — explicit employer expectation.

No requirement contains a fabricated depth signal.

The residual source material is completely and truthfully accounted for:

```text
the work is teachable.
→ excluded_non_requirement

Ethics and your work commitment are important to us.
→ extracted_requirement

Please do not send your resume for remote work.
→ excluded_non_requirement

Location / benefits / travel details
→ excluded_non_requirement
```

No responsibility is fabricated from qualification wording, and no unsupported role purpose is created.

## v16 disposition

`job-analysis-english-v16 / job-analysis-v4` is now the first candidate in this sparse-calibration sequence to pass both:

```text
mechanical provenance / coverage audit
+
complete semantic review
```

This is a **bounded sparse acceptance**, not public promotion yet.

Public production P1.6 remains v9 until dense regression is completed.

## Next gate

Run isolated v16 on dense `tG9K` and compare it against accepted v9 artifact `29`.

Dense regression must preserve, at minimum:

- 27 accepted requirements and 7 responsibilities or a semantically equivalent complete accounting;
- required/preferred/contextual optionality;
- Python-specific `expert` depth;
- MATLAB and C/C++ as preferred;
- contextual framework/cloud/tool requirements as contextual rather than promoted;
- industrial AI/ML experience `Strong`;
- process-control/manufacturing analytics `Hands-on`;
- high-dimensional sensor/time-series data `Comfort`;
- Master's degree and 3–6 years professional experience;
- complete deterministic source accounting;
- no new normalization/type regressions.

Do **not** generate Capability v7 above v16 yet. Capability is allowed only after the dense v16 regression passes and the P1.6 promotion decision is made.
