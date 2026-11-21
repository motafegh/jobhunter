# P1.6 B2v2 — source-structure repair on exposed B5 regression cases

**Date:** 2026-11-21
**Status:** Exposed original-source regression improvement, **candidate only**; fresh B5/B6 gates remain blocked
**Execution:** Directly on `main`
**Predecessor:** `docs/working-memory/2026-11-21_P16_B5_UNSEEN_SOURCE_GATE_FAILURE_AND_HALTED_EVALUATION.md`

## Problem and separation of historical evidence

The original B2 candidate splitter was correct about exact source identity, but had a narrow set of Persian/English headings. When Jobinja flattened list formatting, it produced unresolved paragraphs, work/qualification confusion, false requirements from preferred clauses, and missed multi-specialty alternatives on an eight-case newly seen B5 candidate cohort. The *original* B2 source review was sealed before candidate output. Those eight cases became **exposed development evidence** at the first comparison: no future B5 accuracy claim may reuse them.

**Do not replace the previous engine in place.** Frozen B2/B3/B4 evidence and previous accepted P1.6/Capability must remain mechanically replayable. This increment creates a separately named, opt-in, non-authoritative `jobhunter-p16-b2-source-structure-exposed-candidate-v2` parser. No existing accepted routes, ORM schema, B2v1 function, prior B3 translation, local model prompts, reviewed source truth, or production artifact changes.

## Engineering change

New `src/jobhunter/source_item_candidate_b2_v2.py`:

- Recognizes generic original-language section markers across flattened Persian, English and mixed-language descriptions: duties, qualifications, preferred/bonus expectations, work arrangements and candidate interview/assessment.
- Uses original character and UTF-8 offsets and exact SHA-bound source item anchors; splits at visible bullets and complete sentence boundaries, and only cautiously at separate item openings. Governing phrases such as “experience designing and implementing” remain **one qualification**, not invented duties. Old conditional Middle/Senior track compounds remain intact.
- Separates explicit preferred skill sections and negative “no … required” text from employer-required expectations. Job duties can still imply a relevant capability without inventing prior professional employment or a required individual framework.
- Preserves a source-explicit “one or more separately hired security specialties” alternative as an **unreviewed candidate** with **unresolved option boundaries**; it does NOT invent a full eligibility graph.
- Applies source-benefit versus source-location distinction when flattened HTML puts a location after benefits; preserves native-English original spans without unnecessary translation.
- Reuses existing typed B2 candidate/board-provenance and source-integrity validator contracts. The historical `interpret_original_source_candidate` is **unchanged**.

## Repeatable exposed evidence

The comparator checked **the same 93 previously sealed, assistant-reviewed original-source anchors on the eight exposed jobs**. 86 of those anchors have a directly comparable role category; totals are not complete-source or market accuracy estimates.

| Selected source-first measure | B2v1 historical | B2v2 candidate |
| --- | ---: | ---: |
| Comparable role-category anchors correctly classified | 25 | 82 |
| Comparable role-category mismatches | 58 | 1 |
| Explicit duty anchors not classified as duties | 19 | 0 |
| Preferred or negative items marked required | 2 | 0 |
| Missing source-explicit specialty-choice signal | 1 job | 0 jobs |
| Jobs flagged for source role/structural issues | 7 | 1 |

**Residuals are not hidden:** one selected source-review category disagrees with a framework presented as an *example within a job duty*. It remains a **duty**, not a newly employer-required prior qualification. The general comparison also includes anchors spanning source headings/item boundaries that cannot be represented as a single B2 item; these are retained as *not contained*, not scored as correct. More subtle required/preferred semantics and the individual specialty-track option set remain unresolved beyond the selected review assertions.

**Regression protection:** all four prior exposed B0 jobs retained their original explicit-duty counts (6/11/5/0) and existing conditional graphs (one Middle OR Senior graph and one certificate OR equivalent-knowledge graph). The B4v5 historical presentation and the original B5 source-failure verifiers both still pass byte-exact replay. These are separate exposed compatibility checks; they do not establish B2v2 generalization.

## Verification and authority

- Pure local source parser, no new HTTP fetch, translation model or inference model calls.
- `scripts/replay_p16_b2v2_exposed_regressions.py` freezes the comparator's per-case full diagnostics in ignored private evidence.
- `scripts/verify_p16_b2v2_exposed_regressions.py` replays it against exact source snapshot, unchanged original B2 code, prior source-first review, four prior B0 conditional cases and live production database hash.
- `tests/test_source_item_candidate_b2_v2.py` supplies positive/negative synthetic counterexamples, including no required-strength promotion from bonus sections, native-English negation, governed phrase segmentation, conditional specialty alternatives and false OR negatives. Private real-fixture tests skip only in clean public environments that lack the ignored originals.
- Public-safe hashes/counts: `docs/working-memory/2026-11-21_p16_b2v2/SAFE_B2V2_EXPOSED_REGRESSIONS.json`. Full employer text, URLs, reviewer wording and original source statements are **not committed**.

**Downstream B1/B3-readiness preflight (no model calls):** All eight candidate source-item bundles passed the existing B1 schema and source-anchor validator. On these *exposed* ads, the revised parser selected 258 source items: 142 Persian translation-eligible, 96 native original-language items, and 20 excluded context-only items. These are potential work units, **not** translated artifacts or new model requests. At one model request per Persian item, that would be substantial local inference work. Before a new B5 cohort is evaluated, budget and test bounded source-item batching while preserving per-item identity, original quotation, context, modality and failure granularity. The 80-call B5 paired-analysis budget is a separate ceiling, not an automatic allowance to translate 142 items or a reason to abandon source coverage.

**Local validation:** 1,126 warnings-as-errors regression tests passed; Ruff, formatting, dependency consistency, compileall, original B2/B5 failure replay, B2v2 read-only replay and historical B4v5 replay passed. No accepted analyzer route or live production database modified; zero private original documents staged. GitHub CI is a separate verification boundary.

**Disposition:** `BOUNDED_EXPOSED_REGRESSION_IMPROVEMENT_NO_GENERALIZATION`. Source-item classifications are still unreviewed candidates, not accepted employer facts, and no automatic downstream use is approved.

## Next gate

Freeze the selected **B2v2 candidate code** and then acquire a completely new, distinct, unexposed six-to-eight-job B5 cohort with source-first assessment sealed before the next output. Perform source identity, claim category/strength and alternatives checks; run source-bound bilingual translation and candidate-vs-unchanged-v30 paired tests only when the source-semantic gate is actually sound. Explicitly track local model failure, cost and usability, and retain unresolved cases. Re-evaluate whether any added structural complexity demonstrably improves source meaning rather than adding ad-specific rules.

No B6 promotion or current P1.6 route replacement before that evidence.
