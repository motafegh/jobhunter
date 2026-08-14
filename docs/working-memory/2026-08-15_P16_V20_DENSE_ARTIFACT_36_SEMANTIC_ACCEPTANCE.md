# P1.6 v20 — Dense Artifact 36 Semantic Acceptance

**Date:** 2026-08-15  
**Status:** dense semantic PASS with one acceptable classification difference; sparse non-regression next  
**Candidate:** `job-analysis-english-v20` / `job-analysis-v5`  
**Job:** `tG9K`  
**Artifact:** 36  
**Branch:** `agent/p16-v20-source-led-partitioning`  
**Draft PR:** #8

## 1. Gate result

Artifact 36 already passed persistence and the v20-specific mechanical snapshot audit. The pushed review snapshot was then compared against:

- English projection artifact 33;
- accepted dense P1.6 v9 artifact 29;
- the v20 semantic rules and acceptance checklist.

Verdict:

```text
dense persistence:        PASS
dense mechanical audit:   PASS
dense semantic review:    PASS WITH ACCEPTABLE DIFFERENCE
```

This is a bounded acceptance of dense `tG9K` v20 semantics. It is **not** public P1.6 promotion. Sparse `t4jp` v20 non-regression remains required before any promotion decision.

## 2. Requirement completeness

Artifact 36 contains 33 requirements.

The accepted v9 artifact contained 27 source-derived requirements. Artifact 36 preserves those same 27 source-backed requirement surfaces and additionally represents all six structured `skills[]` values:

```text
Artificial Intelligence
Python
Microsoft Office
Machine learning
Linux
Git
```

Therefore the 33-count increase is explained by source coverage rather than duplication or invention:

```text
27 accepted dense source-derived requirements
+ 6 structured required skills
= 33 v20 requirements
```

No accepted dense factual requirement was silently lost.

## 3. Required role-level facts

Correctly retained:

```text
Master's degree
Professional experience — depth_signal="three to six years"
```

Both are deterministically materialized from structured fields and remain required.

## 4. Explicit depth and obligation

The important employer depth surfaces are correctly preserved:

```text
Strong    → AI/ML industrial/manufacturing experience
Hands-on  → process control / manufacturing analytics / yield / anomaly work
Comfort   → high-dimensional time-series / sensor / metrology data
Solid     → statistics and signal-processing fundamentals
expert    → prose Python stack item
three to six years → professional experience
```

Requirement strength remains separate from depth.

The previous live correction surfaces are also correct:

```text
MATLAB a plus
→ preferred
→ depth_signal=null

some C / C++ helpful
→ preferred
→ depth_signal=null

industrial / edge deployment a plus
→ concept="Industrial / edge deployment"
→ preferred
→ depth_signal=null
→ no fabricated prior experience
```

## 5. Contextual technical stack

The technical-stack modifier says the employer does not expect every single item and that depth in the core stack matters most. V20 therefore keeps unnamed individual stack items contextual while retaining explicit preferred wording where present.

The long stack is accounted for, including:

- Python expert and SQL;
- ML/deep-learning frameworks;
- data/statistics libraries;
- multivariate analysis;
- time-series/signal processing and related tools;
- industrial statistics;
- semiconductor domain;
- fab data systems;
- Spark/Kafka and time-series stores/PostgreSQL;
- MLOps, pipelines, model deployment;
- cloud/edge technologies;
- industrial/edge deployment preference.

This is semantically consistent with the source modifier and does not turn the entire stack into mandatory requirements.

## 6. Ontology review

V20 concept types differ from v9 in several places, but the differences are defensible and generally more specific:

- languages/libraries/platforms are commonly represented as `tool`;
- multivariate analysis / time-series processing / industrial statistics are represented as applied `skill` where appropriate;
- semiconductor subject matter is represented as `domain`;
- model deployment is represented as `skill` rather than unsupported experience;
- industrial/edge deployment is not typed as prior `experience` without exposure evidence;
- Master's degree remains `education` and explicit prior work remains `experience`.

Structured Python (`required`, structured source) and prose `Python (expert)` (`contextual`, prose source) remain provenance-distinct rather than being incorrectly collapsed.

No unsupported `expertise` wording remains in the semiconductor-domain concept.

## 7. Responsibilities and role purpose

Artifact 36 contains:

```text
responsibilities: 8
role_purpose:     0
```

Accepted v9 contained seven responsibilities plus one role-purpose statement.

The difference is fully explained by the opening source bullet:

```text
Build and validate ML/AI models on semiconductor process, equipment, and manufacturing data.
```

V9 classified that sentence as `role_purpose`. V20 classifies the same exact source sentence as a responsibility. The remaining seven concrete duty surfaces are preserved in both versions, including the source semicolon line being represented as two atomic duties:

```text
Handle high-volume, high-dimensional sensor / trace and metrology data
build robust pipelines.
```

This v20 difference is accepted because the opening sentence is itself a concrete imperative action under `What you'll do`; treating it as a responsibility is semantically defensible. No duty or mission content is lost or invented.

The acceptance is therefore **not** based on matching v9 counts. It is based on source-faithful meaning.

## 8. Dense acceptance conclusion

Artifact 36 satisfies the dense semantic checklist:

- required education retained;
- exact professional-experience extent retained;
- all six structured skills retained;
- all accepted dense requirement surfaces retained;
- all concrete duty surfaces retained;
- explicit depth signals attached correctly;
- optionality preserved;
- contextual stack remains contextual;
- industrial/edge scope is not misfiled as depth or fabricated experience;
- semiconductor-domain normalization is source-supported;
- structured/prose Python provenance remains distinct;
- ontology choices are defensible;
- no material unsupported claim or silent factual loss was found.

Dense `tG9K` v20 is therefore accepted for this bounded calibration case.

## 9. Next authorized gate

Run sparse v20 only:

```bash
python scripts/run_p16_v20_candidate.py --job-id t4jp
```

Then export/audit/review the sparse result against accepted sparse v16 artifact 35. The sparse acceptance target remains:

- 3/3 structured skills;
- 4/4 qualification items;
- complete residual accounting;
- zero fabricated responsibilities;
- zero fabricated role purpose;
- no deterministic over-extraction.

## 10. Promotion boundary

Public/accepted P1.6 remains:

```text
job-analysis-english-v9 / job-analysis-v4
```

Do not promote v20, rebuild Capability over v20, advance heterogeneous-role review, or merge the candidate chain until sparse `t4jp` v20 non-regression also passes.
