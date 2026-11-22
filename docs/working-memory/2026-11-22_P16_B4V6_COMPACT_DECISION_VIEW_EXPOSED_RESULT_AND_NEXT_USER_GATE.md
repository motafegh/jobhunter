# P1.6 B4v6 — compact decision-question-first exposed result and next user gate

**Date:** 2026-11-22
**Branch:** `main`
**Decision:** **PASS a bounded, source-replayable presentation-engineering experiment. No independent user usefulness, B5 unseen generalization, or B6 production promotion established.**

## 1. Problem and preregistration

B4v5 retained source-qualified information when the historical v30 model failed or was rejected, but an initial 64-item inventory across four ads still demanded much manual inspection. We need a more immediately useful job-reading experience without fabricating employer statements, hard qualifications, translations, or eligibility rules.

The evaluation design was frozen **before B4v6 implementation/outcomes**, in `docs/working-memory/2026-11-22_P16_B4V6_COMPACT_DECISION_VIEW_FROZEN_PROTOCOL.md` at `e830c3c`. It fixes the same four **exposed** cases and nine original-source questions first registered for B4v5 at `1abd1e0`. No new jobs, model inference, original-source review labels, or generated v30 artifacts were acquired.

**The evaluation compares two source presentation surfaces, not the semantic accuracy of B4v6 versus a valid v30 model:** none of the four archived same-source English v30 attempts yielded an accepted artifact (three failed, one rejected).

## 2. What was built

`src/jobhunter/source_qualified_b4v6.py` provides a generic, non-production candidate projection and Markdown renderer. It organizes existing B4v5 source-qualified items around four applicant questions, in this order:

1. **What would I do?** Up to three distinct duty evidence items, prioritizing a pre-existing source-reviewed terminology correction. Additional work statements remain in source drilldown. Zero candidates is explicitly *not* "this job has no duties."
2. **What capabilities are expected?** Applicant capability and overlapping behavioral evidence shown in required/preferred/other-or-uncertain **candidate** tiers (up to two each), without manufacturing required professional experience from a work duty or trait.
3. **Are there alternatives?** All two existing **unreviewed, source-anchored** OR/AND eligibility candidate graphs on the fixed cohort remain visible, including original nested alternative leaves whose independent English child translation is **not established**. Example lists are not converted into formal eligibility.
4. **What conditions and uncertainties matter?** Explicit conditional application instructions precede work arrangements, with the existing corrected reading aid retained. Rejected/failed/partial model state, excluded source items, suppressed prior model claims, and unresolved categories remain disclosed.

Every displayed item preserves exact original text, original SHA-256, B4v5 English reading aid, candidate category/strength and its source ID. **All 64** B4v5 source-qualified items stay accessible via a complete drilldown *record*, not as the default first-view text. No employer text is published in the source-safe scorecard. The output is a research artifact, not an integrated new browser route. The accepted v30/v9 pipeline, source parser, local database, public corpus and operational user UI are untouched.

## 3. Real bounded same-source result

| Observable for the same four exposed source ads | B4v5 verbose | B4v6 compact |
| --- | ---: | ---: |
| Immediately visible source-qualified evidence items | 64 | 34 |
| Retained source-qualified evidence items in drilldown | 64 | 64 |
| Original + English evidence characters initially displayed | 8,795 | 5,244 |
| Rendered Markdown characters (all four ads) | 25,259 | 19,345 |
| Existing unreviewed eligibility candidate graphs retained | 2 | 2 |
| Reviewed terminology correction retained | 1 | 1 |
| Translation-affected old model claims withheld | 2 | 2 |

**Item inventory reduction: 30 of 64 items (46.9%)**; raw reading-surface length reduction: **5,914 of 25,259 Markdown characters (23.4%)**. The large source identifiers and source text still consume substantial display area. These figures are reproducible proxy counts, *not measured time saved or evidence of better human comprehension*.

The nine **preselected diagnostic questions**, scored only for *source-evidence navigation*, produced:
- **6 immediately navigable source-evidence questions** (including a correctly qualified absence of distinct duty candidates in the last ad); **3 require opening full drilldown** to see all explicitly assigned duties.
- The three drilldown cases involve work statements in the Python/backend, applied-AI, and EDR/security ads. The default first view shows 3 of 6, 3 of 11, and 3 of 5 duty candidates, respectively. Thirteen source references needed to inspect those three full task lists are behind drilldown.
- The explicit nonrequired financial/LLM advantage, Middle-or-Senior *candidate* eligibility structure, certificate-or-equivalent *candidate* path, reviewed product terminology, conditional entrance exam, and remote-arrangement candidate are immediately accessible by evidence reference. Their full semantic correctness remains **not independently certified**.
- **Zero of nine original-source task references lost**, zero source item SHA/role/strength drift, zero unreviewed mandatory upgrades, no fabricated duties or eligibility graph acceptance.

**Important trade-off:** This first view does not answer "what are all the duties?" without drilldown for three jobs. It buys brevity by deferring detail. That is an explicitly measured limitation, not a silently excluded failure.

## 4. Evidence, verification and reproduction

- Precommitted protocol: `docs/working-memory/2026-11-22_P16_B4V6_COMPACT_DECISION_VIEW_FROZEN_PROTOCOL.md` (`e830c3c`).
- Existing prior frozen audit: `scripts/evaluate_p16_exposed_usefulness.py` and its nine source-only task anchors. The old input, its report and SHA checks remain unchanged.
- New candidate: `src/jobhunter/source_qualified_b4v6.py`.
- New audit/CLI replay: `scripts/evaluate_p16_b4v6_compact_usefulness.py`; default invocation checks source fingerprints, prior auditor, all compact evidence and private/report bytes, and rejects mismatches. `--write-once` sealed the first private candidate/task output and source-only Markdown.
- Frozen private (ignored) outputs: `data/local-acceptance/p16-b4v6-compact-2026-11-22/v1/PRIVATE_B4V6_CANDIDATE_AND_TASK_REVIEW.json` and `B4V6_COMPACT_FIRST_VIEW.md`.
- Tracked aggregate-only report: `docs/working-memory/2026-11-22_p16_b4v6_compact/SAFE_EXPOSED_COMPACT_DECISION_NAVIGATION.json`.
- `tests/test_source_qualified_b4v6.py` protects source hashes, candidate-only role/strength, qualification/condition tiering, OR/AND graph authority and nested English alignment, no-duties abstention, HTML/Markdown escaping, accepted-fact refusal, public privacy and optional private replay. Old B4v5 and prior usefulness tests continue to run.

The study uses **zero Jobinja/source requests, zero LLM HTTP calls, zero translation calls, zero accepted facts, and zero production writes**. Local replay is source-SHA guarded; clean CI clones test the bundled safe report and synthetic contracts without requiring ignored private employer material.

## 5. Engineering interpretation and next decision

This experiment validates that we can **frontload actionable evidence while retaining complete drilldown and source integrity**. It does not show that people understand the ads faster, that the first three duties are the most salient, or that the model/translation interpretation is correct. The existing assistant saw the cases before this exercise, so neither blind semantic generalization nor independent utility was established.

**Next recommended gate:** a short owner-led or context-isolated user study using the actual local browser prototype or separately rendered original/compact views. Use representative tasks and measure correct actionable answers, omissions/false hard requirements, optional-vs-required distinctions, eligibility ambiguity, direct source-navigation steps and wall time. Compare against unassisted original ads and the same-source verbose B4v5, not a failed v30 model. If real comprehension benefit emerges, then consider a separate opt-in local browser implementation and selectively budgeted semantic interpretation for unresolved situations. Prevent old accepted routes from treating research candidates as reviewed facts.

**B5 remains unpassed** pending frozen, untouched sources and independent/calibrated source-first semantics. **B6 stays closed** behind an explicit promotion and rollback gate. Do not automatically consume an additional prospective cohort or broaden this experiment into an unbounded LLM prompting/regex endeavor.
