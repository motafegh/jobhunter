# P2.2B-B1 focused extraction recovery

**Date:** 2026-09-14
**Status:** FEEDBACK CLARIFICATION VERIFIED / LOCAL RUN IN PROGRESS / B1 OPEN

The owner authorized focused recovery, progressive recording, and publication of
repository-safe changes. The preceding checkpoint and English projection 40 were
published in `1ef559c`. SQLite, raw model protocol, and registry state remain local.

## Bounded change

Attempt 98's first correction instruction said to copy an exact source depth phrase
without explaining the existing restriction to one explicit marker. Clarified the
two relevant v20 validation messages to request an exact excerpt with one marker
applying to the concept, retain full source evidence, and avoid borrowing another
subject's depth. The feedback contains no vacancy-specific terminology or answer.

This changes retry feedback only. Validation predicates, normalization, source
evidence, model, system prompt, schema/prompt IDs, and retry limits are unchanged.
It does not justify re-running accepted anchors or broadening accepted semantics.
The changed source revision must be retained alongside any new runtime evidence:
contract IDs alone do not identify the revised feedback.

## Verification before the live run

- Ruff: PASS.
- Focused v20 candidate/depth regression tests: 33 passed.
- Complete suite with warnings as errors: 544 passed.
- Reproduced both observed rejected representations and the two valid exact-marker
  representations, retaining concept and exact evidence on successful validation.
- No ta9l P1.6 artifact existed before the recovery run.

## Runtime evidence boundary

The recovery command reuses source detail 25 and English projection 40 with
`gemma-4-e4b-it-ud`, `job-analysis-english-v20 / job-analysis-v5`.
No translation or acquisition is repeated.

Before this run, LM Studio reported the configured E4B instance loaded with a
16,384-token context. The earlier loading request had specified 32,768. This
runtime difference prevents a strict single-variable causal comparison between
attempt 98 and this run. It does not change the source/artifact contract, and a
successful run would still need whole-artifact semantic review.

Full CLI/provider diagnostics are redirected to an ignored local file. This
record will be updated with the result; no success or B1 closure is claimed yet.
