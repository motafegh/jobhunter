# P1.6 B2 — native source-reference trial improves citation coverage, not semantic fidelity

**Date:** 2026-11-16
**Branch / PR:** `feature/p16-b2-source-items-metadata-2026-11-15` / draft #20
**Accepted main before experiment:** `5d4a5e0a64e1dc1da64bc9f28848b4357895aa7e`
**Parent experimental head:** `d4b656869a9812d40a50143dee73fea443861665`
**Disposition:** One bounded original-source-reference inference trial **EXECUTED**; **B2 semantic gate remains OPEN_NO_PROMOTION**. No employer fact, applicant-eligibility policy, source, translation, accepted P1.6, Capability, Work, Registry, Market or public runtime has been promoted.

## Decision

A compact, single native LM Studio inference request can produce **model-suggested references to numbered exact original Persian source items** for most generated English claims, without an additional model stage. The returned integer references map mechanically to verified Stage A anchors under the isolated, candidate-only B2 source object.

**This does not solve source-semantic fidelity.** Several linked claims still misrepresent original employer modality or turn applicant capabilities into assigned duties. The source-candidate reconciler correctly emits many **diagnostic warnings**, but it is heuristic and cannot be treated as an independent Persian entailment verifier. Valid IDs do not authorize acceptance. The revised prompt also consumes more output tokens, has higher observed latency, and drops several useful interpretations. No second corrective prompt or source/ad-specific optimization is justified by this result. Retain this trial as **research only**, not B2 PASS or a candidate production route.

## Controlled design and exact boundaries

- **Input:** The exact same four already exposed, frozen original-job versions (`tNhZ`, `tMps`, `tNDx`, `tMjm`). A read-only SQLite copy feeds the previously introduced candidate segmentation. Input has numbered original fragments **with original headings and no supplied heuristic category labels**. Exact Stage A source-item anchor identities remain unchanged. Semantic meaning of headings or items is not automatically validated by those spans.
- **Model/runtime:** Existing `gemma-4-e4b-it-ud`; native `http://127.0.0.1:18080/api/v1/chat`; `reasoning: off`; temperature 0; `store: false`; 2,700 max output tokens and 55-second timeout per call; no proxy, remote cloud model, source acquisition or retries. A separate short, source-free readiness request loaded the previously unloaded model (25.755 seconds; 'OK'; 0 reasoning tokens) **before** trial timing.
- **Prompt:** One globally fixed concise source-ref prompt, not tuned by job. Existing seven category arrays retained, changing their items to compact `{"t":"short English claim","s":[original item numbers]}`. Unknown citations are `[]`. Model prompt SHA-256: `5c2130651e416bd2a0def98713f924355b1bd89480eec5d0a690dfcf2f259fc9`.
- **Verification:** Structural shape, numeric IDs, duplicate/out-of-range citation detection, source-version and Stage A anchor checks; `model_suggested` provenance; candidate-category discrepancy signals. The reconciliation layer does **not** accept or reject employer meaning; it cannot auto-assert that a linked clause truly supports an English paraphrase.
- **Records:** Full original text, numbered inputs, model responses, prompts, source map, provider stats and candidate claim traces stay in ignored `data/local-acceptance/`. Tracked files contain hashes, source-safe counts and non-independent check rationales only.

## Exact exposed-case results

Frozen B0 SQLite SHA-256: `bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe`

| Job | Source-ref v4 claims | Valid model-suggested source IDs | Unlinked | Source-candidate disagreement signals |
| --- | ---: | ---: | ---: | ---: |
| `tNhZ` | 18 | 17 | 1 | 8 |
| `tMps` | 20 | 20 | 0 | 2 |
| `tNDx` | 18 | 17 | 1 | 4 |
| `tMjm` | 19 | 19 | 0 | 11 |
| **Total** | **75** | **73** | **2** | **25** |

All four model requests completed with structured JSON; no out-of-range source references were generated. Of the 73 linked claims, **48** had no candidate-category discrepancy but remain *semantically unreviewed*; **25** raised candidate-to-candidate signals. This is **not 48 confirmed correct and 25 confirmed wrong**. Absence of a signal cannot prove employer meaning, and signals can also reflect source heuristic uncertainty. No linked claim became an accepted fact.

### Same 12 exposed, non-independent diagnostic checks

| Outcome | Previous native corrective v3 | Source-ref v4 |
| --- | ---: | ---: |
| Pass | 6 | 5 |
| Partial | 2 | 4 |
| Fail | 4 | 3 |

The v4 judgments are a **post-output, assistant-prior-context-exposed** comparison against the same selected reference checks used earlier. They were not blind, not a fresh holdout, not statistically representative, and not a controlled test of model accuracy. Moreover, v3 and v4 have different output formats and input presentation. The check tally must not be used as an accuracy percentage or a numerical production-promotion threshold.

**Observed strengths:** six correctly listed Python/backend duties; explicit LLM familiarity remains a preference; five EDR duties retained; teamwork properly moved from mandatory to preferred; remote possibility correctly treated as an arrangement; Middle/Senior paths both mentioned in job qualifications.

**Material blockers:**
1. `tMjm`: three apparently well-cited employee duties were **invented from applicant ability clauses**; exact source ID citation does not make them assigned duties.
2. `tNDx`: unresolved Kaspersky credential and government/enterprise-client experience strength again appears under **preferred**; an explicitly stated certificate OR equivalent-knowledge choice is present inside a requirement but the alternatives array incorrectly says *no explicit alternatives*.
3. `tNhZ`: part-time/full-time work-mode choice remains incorrectly filed under applicant eligibility alternatives; work-implied capabilities focus on generic traits and omit obvious source-supported Python/LLM operational capability.
4. `tMps`: the Middle/Senior requirements contain the stated within-track clauses but the alternatives array is empty; no complete independent machine-readable OR/AND eligibility graph emerges. Two generic team-oriented notions are put under work-implied capabilities rather than genuine work-linked technical abilities.

Thus high **citation presence** coexists with wrong **semantic role, obligation and alternative structure**.

### Cost and coverage trade-off

| Diagnostic | Previous v3 | Source-ref v4 |
| --- | ---: | ---: |
| Model-generated claim strings | 85 | 75 |
| Total four-request inference time | 24.290 s | 33.606 s |
| Total output tokens reported | 1,627 | 2,227 |
| Original item citation required by output | No | Yes |

The ~9.3-second observed increase and 600 extra output tokens are descriptive of two sequential local runs, **not performance estimates for all hardware or jobs**. The added source-item input also increases input tokens. Fewer generated claims are not automatically a quality loss, but missing crucial alternatives and work-implied capabilities are material quality regressions on the exposed cases.

## Evidence and verification

- **Source-reference trial code:** `scripts/probe_b2_model_source_refs.py`.
- **Offline v3/v4 source-safe reconciliation:** `scripts/reconcile_b2_source_ref_trial.py`.
- **Synthetic and optional local real-source regression tests:** `tests/test_probe_b2_model_source_refs.py`, `tests/test_reconcile_b2_source_ref_trial.py`.
- **Safe raw-trial metadata:** `docs/working-memory/2026-11-16_p16_b2/SAFE_NATIVE_SOURCE_REF_METRICS.json`; SHA-256 `1c6e6740075e3e0874e334b41984f397ccf89aea9f420848a671b3a3809b1faa`.
- **Safe assistant semantic checks:** `docs/working-memory/2026-11-16_p16_b2/SAFE_NATIVE_SOURCE_REF_ASSISTANT_CHECKS.json`; SHA-256 `34fe1529dcc1c14faa9e945af0b1c24916a4d0c381062fdc29c2b7350d296dec`.
- **Safe derived comparative scorecard:** `docs/working-memory/2026-11-16_p16_b2/SAFE_NATIVE_SOURCE_REF_RECONCILIATION.json`.
- **Private source/model record:** `data/local-acceptance/p16-stage-b2-2026-11-16/native-source-refs-v1/PRIVATE_SOURCE_REFERENCED_TRIAL.json`; SHA-256 `8b058afe51b9452c6b5cf2829d7b684255b842bfa7a0cd5f31f3b2c78a5419b7`; ignored by Git.
- **Private readiness:** exact Gemma model loaded using a source-free local native call; neither a separate generation/trial iteration nor evidence of job-semantic success.

- **Safe comparative scorecard SHA-256:** `ca5b62bb7ce5820e467292e22e33943e06f344e8e765b016feaff4dbd710d058`.
- **Final local quality:** `pytest -q -W error` = **1,043 passed**; `ruff check .`, `python -m pip check`, and `git diff --check` passed. All raw original/model records remain under Git-ignored `data/local-acceptance/`. Remote GitHub CI remains a separate required check after the commit.

Existing English P1.6 v30, original-language v9, English projection v2, B1 contract, Stage A spans and accepted downstream contracts remain untouched.

## What next — exact engineering stop line

**Stop this B2 prompt-and-source-reference exploration; do not promote or merge PR #20 yet.** A further prompt tweak simply to raise citation counts would mistake structural compliance for meaning. The next substantive work is a separately evaluated **B2 strategy decision**: measure which core source-fidelity errors can be addressed without a growing heuristic rulebook. Compare (a) source-first partial candidate reporting with honest unknowns, and (b) a separately budgeted *different model* only if it plausibly improves the specific failed semantic judgments, not merely valid JSON. Neither route automatically satisfies B2, B3, or B4. Do not start a new model matrix, switch production analyzers, regenerate accepted facts, or capture the B5 unseen cohort for iterative prompt tuning.

B2 full semantic generalization remains NOT ESTABLISHED; B3 bilingual meaning, B4 user-facing brief, B5 independent evaluation and B6 controlled promotion remain separately gated.
