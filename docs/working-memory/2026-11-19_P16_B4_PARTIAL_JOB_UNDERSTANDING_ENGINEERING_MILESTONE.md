# P1.6 B4 — Source-grounded job-understanding engineering milestone

**Date:** 2026-11-19
**Disposition:** PASS_ENGINEERING_BOUNDARIES_SEMANTIC_GATE_OPEN
**Branch:** `main`
**Evaluation:** Four previously exposed B0 development ads; not an unseen holdout.

## Delivered

B4 now has an isolated, source-qualified, non-authoritative job-understanding candidate. It retains all exact B2 original-language source items and hashes, B3 item-bound English candidates, metadata/prose conflicts, nested eligibility graphs, explicit translation-review authority and per-item coverage. Model-facing short IDs are mapped back to canonical source-item IDs before a claim is retained. Board metadata and graph identifiers are not passed to the model.

The local candidate supports a model brief and separate source-only fallback. For a vacancy with no explicit work-duty source item, it intentionally abstains from model-generated tasks and presents source-bound qualifications instead. Unsupported model fragments are quarantined rather than forcing the entire otherwise useful source-linked response to fail. Such filtering is **not** semantic verification.

The frozen v30/v9 comparison is in an isolated, standalone SQLite backup, with four B4 candidate rows, four B4 attempt rows, integrity PASS, zero foreign-key violations, journal mode DELETE and unchanged original source snapshot. The local Gemma 4 E4B provider ran with reasoning explicitly off. No raw reasoning content or complete HTTP response bodies were retained.

## Four-job result

| Exposed case | B4 result | Frozen baseline | Assistant source check |
| --- | --- | --- | --- |
| `tNhZ` | Partial candidate; four unsupported model fragments quarantined | v30 failed; no v9 | Six explicit duties and three work-implied capabilities are grounded in the original source. Applicant expectations were omitted from the model summary; the preferred-not-mandatory LLM detail remains only in source evidence. |
| `tMps` | Model rejected; readable source-only fallback | v30 failed; no v9 | Three model-output schema length failures. More importantly, rejected text can flatten alternative Middle/Senior qualification paths into cumulative expectations. The B2 candidate graph remains separate; no accepted job-level model assertion. |
| `tNDx` | Partial candidate | v30 failed; mechanically accepted v9 | Five explicit duties, four explicit applicant qualifications and four work-implied capabilities have plausible original-source support. A possible named ticketing-system mistranslation (Fadak vs FDC) needs verification. Preferred teamwork and the entrance-exam condition are not sufficiently prominent in the model summary. |
| `tMjm` | Intentional source-only candidate; model request skipped | v30 candidate rejected; no v9 | Source offers applicant qualifications but no distinct explicit work-duty statement. No work responsibilities were fabricated. |

The exposed-cohort assistant check is **not independent blind human review**. A valid citation or a JSON-schema pass is not evidence of semantic fidelity. The source record remains authoritative; model text is revocable.

## Inspectable results

- 78 source items; 63 Persian item-bound translations and one native-English identity; 14 excluded items; 53 distinct board metadata values; 12 nested eligibility subspans.
- Three local Gemma requests; two structurally/source-reference validated partial candidates; one rejected; one qualifications-only deterministic abstention; four quarantined generated fragments.
- Unchanged baseline comparison: three v30 attempts without valid artifacts, one rejected v30 candidate, one mechanically accepted original-language v9 artifact (not independent correctness certification).
- Full local regression suite: **1,085 passed** with warnings treated as errors; Ruff lint, relevant formatting, dependency checks and Python compilation PASS.
- `scripts/verify_p16_b4_milestone.py` checks private hashes, source identity, canonical source refs, B4 candidate/reference coverage, unchanged B2/B3 inputs, the standalone SQLite file and zero production promotion.
- Private model/source data, final messages, receipts and assistant-review evidence remain ignored under `data/local-acceptance/p16-stage-b4-2026-11-19/primary-v4c/`.
- Safe inspectable aggregates: `docs/working-memory/2026-11-19_p16_b4/SAFE_B4_MILESTONE.json`.

## Decision and next gate

**B4 engineering milestone: PASS. B4 semantic/usefulness acceptance: OPEN.**

The source-only fallback gives meaningful, traceable coverage even on rejected or skipped model results. However, missing preferred/conditional information, alternate-path logic and possible named-entity drift block any broader claim of semantic quality or promotion.

The next increment must improve the readability and completeness of source-qualified expectations and alternative eligibility without hardening B2's provisional semantic categories into rigid employer facts. The `tMps` failure and `tNDx` potential name mismatch become explicit exposed regressions. Make bounded, evidence-based repairs and re-evaluate; do not claim that the model always succeeds or that developer examples prove generalization.

**Not authorized:** new public P1.6 route, accepted employer facts, Capability/Work/Registry/Market mutation, production DB writes, unseen B5 pass, measured owner-time savings, or B6 promotion/rollback.
