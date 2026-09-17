# Market I3 real-model membership evaluation

**Date:** 2026-09-17  
**Implementation under evaluation:** `0eaf04109a57846aa6d0a920d0563f89a4dfb535`  
**Purpose:** bounded semantic acceptance evidence for Market I3 membership qualification.  
**Authority:** evaluation evidence only; this is not a corpus-wide accuracy benchmark or a canonical taxonomy decision.

## Setup

The evaluation used:

- the configured local membership provider `lm-studio-membership-v1`;
- model `gemma-4-e4b-it-ud`;
- `temperature=0`, `seed=0`;
- membership contract/schema `market-membership-v1`;
- prompt `market-membership-v1.0`;
- an isolated copy of the operational SQLite database;
- seven real historical Jobinja postings plus one synthetic sparse case;
- `refresh_after_hours=2160` (90 days) only to permit retrospective evaluation without refreshing or relabeling historical source evidence.

The run did not establish that the historical vacancies remained open on 2026-09-17.
The operational SQLite database was not mutated by this evaluation.

## Baseline target

Baseline membership intent:

```text
Applied AI / ML engineering work
```

Expected dispositions were selected from the already-established Market foundation boundary cases:

| Case | Expected | Baseline result | Match |
| --- | --- | --- | --- |
| `ta9l` | `core_match` | `core_match` | yes |
| `tG9K` | `core_match` | `core_match` | yes |
| `tGM0` | `adjacent_match` | `core_match` | **no** |
| `t4jp` | `excluded` | `excluded` | yes |
| `tmBK` | `excluded` | `excluded` | yes |
| `t4qV` | `excluded` | `excluded` | yes |
| `tmyX` | `excluded` | `excluded` | yes |
| synthetic sparse | `uncertain` | `uncertain` | yes |

Result: **7/8 expected outcomes overall; 6/7 on real vacancies.**

The only disagreement was `tGM0`, a backend/software-infrastructure role inside an AI team. The model treated AI-team context and integration with LLM/agent/RAG systems as enough for `core_match`, despite the posting stating that the role's main focus was scalable backend services used as infrastructure for intelligent systems.

Every immediate second qualification reused the persisted membership and did not call the model again. This demonstrates dependency-keyed persistence reuse, not fresh-call model reproducibility.

## Controlled target-definition comparison

After observing the `tGM0` disagreement, one controlled comparison changed only the target definition. The model, prompt/schema, provider settings, and vacancy evidence were kept fixed.

Clarified membership intent:

```text
Applied AI / ML engineering where the primary work is developing, evaluating, or improving AI/ML models, agents, retrieval, or AI system behavior. Backend/API/database/infrastructure roles primarily enabling or integrating AI services are adjacent rather than core. Using AI tools for general software or content production does not qualify for this target.
```

Comparison result:

| Case | Expected | Clarified-target result | Match |
| --- | --- | --- | --- |
| `ta9l` | `core_match` | `core_match` | yes |
| `tG9K` | `core_match` | `core_match` | yes |
| `tGM0` | `adjacent_match` | `adjacent_match` | yes |
| `t4jp` | `excluded` | `excluded` | yes |
| `tmBK` | `excluded` | `excluded` | yes |
| `t4qV` | `excluded` | `excluded` | yes |
| `tmyX` | `excluded` | `excluded` | yes |
| synthetic sparse | `uncertain` | `uncertain` | yes |

Result: **8/8 expected outcomes in the post-hoc comparison.**

This is not an independent accuracy score. The clarified definition was written after the baseline miss and therefore acts as a boundary-calibration experiment. It demonstrates that membership quality depends materially on an explicit target-market meaning, not only on the model and classifier prompt.

## Product conclusion

The experiment does **not** justify changing the I3 classifier prompt merely to force the `tGM0` outcome.

The stronger conclusion is:

```text
membership quality
= target definition quality
+ source/derived evidence quality
+ classifier contract/model behavior
```

For a target intended to distinguish core Applied AI/ML engineering from AI-adjacent backend/platform work, the immutable `TargetMarketDefinitionVersion.membership_intent` should explicitly encode that distinction.

I3 remains an interpretation layer, not a canonical role taxonomy. `core_match`, `adjacent_match`, `uncertain`, and `excluded` are target-relative analytical dispositions.

## Limits

This evidence is intentionally small:

- seven real historical vacancies are not representative enough for a population accuracy estimate;
- one synthetic case checks sparse-evidence abstention only;
- expected labels are foundation-review expectations, not an independently blinded gold dataset;
- the clarified target was created after one observed miss;
- each target/case received one fresh model call;
- the second call tested persistence reuse and therefore did not test fresh-call repeatability;
- no model comparison, repeated-seed stability study, or corpus-wide evaluation was performed;
- no claim is made about current vacancy availability.

A larger or blinded semantic evaluation may be performed later if Market product behavior demonstrates a need. It is not required to reopen I3 before I4.

## Files

- `report.json` — baseline run result.
- `comparison.json` — clarified-target comparison result.
- `*-input.json` / `*-decision.json` — exact baseline model inputs and structured outputs.
- `*-clarified-input.json` / `*-clarified-decision.json` — exact comparison inputs and outputs.
- `run_baseline.py` — preserved/reformatted baseline runner.
- `run_target_comparison.py` — preserved/reformatted comparison runner.

The sandbox SQLite database and machine-local runtime files are intentionally not committed.
