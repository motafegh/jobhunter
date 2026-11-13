# P1.6 source fidelity V31 — bounded experiment closure and next source-first gate

**Date:** 2026-11-12
**Disposition:** **NO PROMOTION** to current English P1.6; an isolated source-section / candidate experiment is retained
**Branch:** `experiment/p16-source-fidelity-2026-11-12`
**Accepted product baseline:** `main` commit `74ffec25533c5cd4b1afa90b0c3bc76ee023e7aa`, public current English `job-analysis-english-v30 / job-analysis-v5`
**Evidence:** `docs/working-memory/2026-11-12_p16_source_fidelity_v31/CANDIDATE_MECHANICAL_AND_SEMANTIC_RESULTS.json`
**Prior independent source review:** `evaluation/current-real-ads-2026-11-12` at `0a4287676795742f933dbb8142a8f9ae9c55f9a9`

> **Corrective erratum — November 13, 2026:** Reinspection of the original Persian source found the prior `tNDx` translation-error diagnosis was wrong. The source says teamwork is an advantage and the English rendering preserves it. The actual defect was the v31 ledger’s inferred required obligation. Run outcomes and no-promotion remain unchanged.

## 1. Product question and conclusion

Can JobHunter produce useful source-backed technical-job understanding for the five real Jobinja ads that exposed failures in English P1.6, without loosening source-truth validation or fabricating requirements?

**Partial engineering improvement, insufficient product quality.** We proved that explicit source-section ownership helps the P1.6 model recover substantive duties and avoid conflating application instructions with candidate qualifications. On the four previously failed English P1.6 cases rerun, one generated a candidate and three still had no usable candidate (two rejected, one timed out). The generated candidate remains semantically **pending/not advice-ready** due a conflict between required structured Jobinja skill tags and the employer's explicitly optional wording. No candidate from this experiment may feed accepted Work, Capability, Registry, Market or personal readiness.

The experiment is complete; looping on prompt variants to obtain superficial passes is not the next step. The next milestone must improve *upstream source-and-translation authority* so the model receives well-owned, verifiable facts.

## 2. What was built and verified

This was code development on a separate branch, **not a modification of the public analysis route**:

- `source_section_spine.py`: source-exact English `SourceSection` segments and offsets for responsibility, qualification, preferred, tiered eligibility, arrangement, application and context boundaries. A narrow explicitly labeled inference separates flattened EDR-style duties from qualification bullets.
- `evidence_refs_v31.py`: candidate-only P1.6 coverage ownership. The initial version replaced some fine-grained inherited references with broad section spans; a *post-trial correction* now retains every source-exact narrowly owned legacy clause, replaces only a cross-heading reference, and fills uncovered section spans instead of making the model repeat whole paragraphs. The original v30 ledger remains unchanged.
- `instructor_lm_studio_v31.py`, `analysis_service_v31.py`, `analysis_runtime_v31.py`: explicit candidate contract `job-analysis-english-v31 / job-analysis-v5`, strict source-evidence and pending-review semantics preserved. No public CLI alias, `analysis_current.py`, schema/currentness migration, or historical accepted artifact was changed.
- `source_obligation_conflicts.py`: **advisory only** source-exact conflict recognition when a structured skill tag (normally materialized as `required`) appears inside an explicitly *not required* prose preference span. The real `tNhZ` ad flags `LLM`; no automatic promotion, deletion or coercion of either claim. This is not a universal multilingual contradiction detector.
- Synthetic deterministic regressions now check source spans, alternatives, EDR duty ownership, application exclusion, refusal to invent sections, preservation of structured source fields, granular ledger retention, cross-heading repair, and explicit optional structured-skill conflicts.

### Mechanical verification

- **898 warnings-as-errors tests passed**, including 14 new candidate tests; Ruff passed; Python dependency consistency passed; no diff whitespace errors.
- The static v30-v31 comparison retained every fine-grained source ref on the five historical anchors `tG9K`, `t4jp`, `tmBK`, `t4qV`, `tmyX`. `tmBK` retained both v30 refs rather than collapsing two into one; an uncovered source span remains separately visible.
- For the fresh EDR posting `tNDx`, the source-section planner identifies **five** distinct direct-duty spans versus **zero** from the unchanged v30 work planner. This is **planning coverage evidence**, not model-output correctness.
- On `tMjm`, the candidate now retains ten original source references and deliberately replaces the one merged cross-heading reference with separately exact section coverage; this revised candidate was **not** run live against that job.
- All source text and trial details live under ignored local evaluation folders. No raw employer source, translated input, model completion, secrets or SQLite files were committed.

## 3. Explicit pre-revision live-model results

The controlled live trials used **commit `37e13830ece5d4ef587ddb08ecf88d29f3b5fda4`**, `gemma-4-e4b-it-ud` over LM Studio `127.0.0.1:18080`, the **same five-posting acquisition/translation evidence** as the independent audit, and a fresh isolated SQLite online backup. We did not substitute a new prompt for the old native baseline without recording the new v31 identity. Every trial used a bound and its exact log, status and result integrity were retained.

| Posting | v30 baseline | v31 live trial | Independent conclusion |
| --- | --- | --- | --- |
| `tNhZ` Python-fintech backend / optional LLM | Failed | Generated pending in 119 s, six explicit duties | Partial recovery, **not approved**: `LLM` site tag materialized as required while employer text says familiarity is not mandatory. Also one residual label remains overly literal. |
| `tMps` applied AI with Middle/Senior tracks | Failed | Failed in 105 s | Source sections separated alternatives, but model omitted required duty coverage refs; no artifact. |
| `tMqd` Python/AI backend, optional LLM frameworks | Failed | **Timed out** (bounded command exited 124 after 306 s) | Runtime/model completion unresolved; no candidate. Timeout does not establish semantic failure or success. |
| `tNDx` EDR technical support | Failed | Failed in 56 s | The Persian item says “مزیت محسوب می‌شود” (“considered an advantage”); the English translation preserves this. The v31 planner incorrectly labeled this item required; strict validation rejected the mismatch. |
| `tMjm` pentesting qualifications | Generated but human-rejected on v30 | **Not run on v31** | Do not infer a repair from static ledger checks. |

The isolated `tNhZ` v31 candidate is **pending** (artifact ID 3, exact analysis SHA-256 in the machine-readable report). Neither this candidate nor the separate native original-language EDR `accepted` artifact from the prior audit establishes independent semantic correctness. There is no new approved Work/Capability result.

### Two distinct revisions — do not combine their evidence

1. **`37e1383`:** first source-exact v31 model-probed candidate; 892 tests passed. Only this commit was used for the four live generation trials above.
2. **`e35b28a`:** safety refinements *after* those trials: preserved inherited granular source coverage and added the structured-skill/prose conflict warning; 898 tests passed. **Not re-run against LM Studio**. Its deterministic tests must not be counted as additional successful live P1.6 cases.

No evidence authorizes promoting either revision. All accepted v30 historical behavior is intentionally preserved unchanged on `main`.

## 4. Root causes distinguished by this experiment

**A. Lost source-section ownership.** A flattened translated description obscures the difference between employer duties, qualifications, preference headings, application requests and work arrangements. Source-exact section reading helps, but only if it retains fine-grained provenance and does not manufacture missing facts.

**B. Original item-level preference misclassified by v31.** In `tNDx`, the original Persian marks teamwork as an **advantage** (`مزیت محسوب می‌شود`), and the English translation agrees. The prior mistranslation diagnosis was incorrect. The v31 planner overrode item-level wording with a required section hint. Heading guesses must never supersede source-explicit modality.

**C. Structured metadata conflicts with narrative authority.** In `tNhZ`, the site's required-like structured `LLM` skill tag conflicts with an explicitly non-required prose familiarity statement. Blindly treating every structured skill tag as mandatory yields contradictory outputs even when duties are correct. Keep both evidence sources distinguishable and show **requires human/source reconciliation** before promotion.

**D. Model and coverage contract limitations.** `tMps` still fails required duty references; `tMqd` times out under a bounded command. Neither is addressed by merely changing heading regexes, and larger local models cannot substitute for sound source ownership.

**E. Review-state authority discrepancy.** The older original-language v9/v4 route previously stored a semantically mistaken EDR artifact as `accepted` without independent review. That status is not a license for downstream use under a stricter current pipeline. A future authority migration must distinguish mechanical validation, candidate persistence and reviewed source fidelity without silently rewriting historical artifacts.

## 5. Selected next engineering milestone: source-first bilingual P1.6 input and authority

**Decision: build an original-source-owned factual evidence spine before another model prompt revision or P2.3B expansion.** This is a specific product reliability prerequisite, not a new market taxonomy or cosmetic screen.

Proposed implementation scope, in order:

1. **Original-language source spans.** Derive versioned, exact-field-offset source sections from Jobinja's original parsed employer description, including Persian headings and list boundaries, while retaining the exact original bytes, source version and section IDs. Section labels distinguish explicit work, qualifications, preferences, tiered eligibility, nonqualification context and genuinely unresolved spans. No inferred fact is promoted solely from a heading guess.
2. **Translation aligned to original sections.** Build a faithful per-section English view or verified section-to-segment alignment rather than trusting one flattened translated blob. Where translation modifies required/preferred meaning, mark `translation_semantic_conflict` and require review or preserve the original-language exact span without falsely classifying it.
3. **Structured-versus-narrative obligation reconciliation.** A Jobinja skill tag remains source metadata. It is not unconditionally a mandatory employer qualification when the detailed employer description says otherwise. Preserve the contradiction and its exact evidence, with an explicit unresolved status until reviewed. No silent rewriting of historical records.
4. **Candidate P1.6 lifecycle and acceptance.** Keep a cheap inspectable factual brief when possible, but only source-supported, correctly classified facts cross durable accepted authority. Investigate original-language v9 auto-accepted semantics separately and preserve historical identity/compatibility during any future migration.
5. **Performance and usefulness acceptance.** Establish a bounded per-job inference budget and report useful claim coverage, obligation errors, source/exact-evidence integrity, rejection reasons and elapsed time separately. A failed/unknown result is not zero employer demand.

**Acceptance before replacing v30:** independently reviewed source-grounded duties and requirements on a meaningful varied real cohort; no fabricated work or mandatory skills, correct Middle/Senior alternatives and preferred options, exact original/translation linkage; regressions on accepted historical anchors; at least one fresh separate verification cohort that was not used to design rules; no input state or reference migration by stealth. Do not set an arbitrary model-success percentage or autoaccept a mechanically valid artifact.

## 6. Status and reproducibility

- All accepted product code on `main` remains unchanged at `74ffec2`.
- Candidate commits `37e1383` (live-trial source) and `e35b28a` (subsequent static safety correction) are retained in `experiment/p16-source-fidelity-2026-11-12`.
- Repository-safe evaluation metrics and hashes: `docs/working-memory/2026-11-12_p16_source_fidelity_v31/CANDIDATE_MECHANICAL_AND_SEMANTIC_RESULTS.json`.
- Local-only source/translation/model logs, exact rejected and pending records and isolated databases: `data/local-acceptance/current-real-ads-2026-11-12/` and `data/local-acceptance/p16-source-fidelity-v31-2026-11-12/`. Do not `git add -A` those directories.
- No broad market-reliability claim or production P1.6 source promotion has been made.

**Stop line for this experiment:** This v31 candidate is research evidence and reusable code, not current JobHunter semantics. Resume implementation only under the source-first bilingual authority gate above; do not continue indefinite v32/v33 prompt-only trials against these exposed five cases.
