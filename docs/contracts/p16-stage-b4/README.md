# P1.6 B4 job-understanding candidate contract

Contract: jobhunter-p16-b4-job-understanding-candidate-v1
Status: experimental, candidate-only; not a P1.6 artifact, route, migration, or downstream input.

The model response schema describes a concise job-level interpretation:
- a source-linked role summary;
- explicit work activities (empty when no distinct duties are stated);
- grouped employer expectations;
- work-implied capability hypotheses linked to duties;
- material unknowns/questions.

The model receives compact ephemeral IDs (I01, I02, ...) to keep the request within the configured local model context; the deterministic validator maps them back to exact B2 source-item IDs before persisting the brief. Every model-generated assertion therefore persists with one or more exact B2 source-item IDs. B2 categories and strengths remain provisional candidates. B3 English item text is a source-bound translation convenience; the original Persian span remains authoritative. B3's separate exposed-cohort semantic-review record is the review evidence. The meaning_review field in the original B3 raw candidate record remains unreviewed and must not be overwritten or mistaken for the separate review.

The LLM does not receive the nested eligibility graph identifiers (only the source-owned evidence retains them). The deterministic candidate evidence view retains all B2 source items, selected B3 target text, excluded-item reasons, board metadata as a separate source, B2 conflicts, and eligibility graph candidates. The model does not receive structured board values, so they cannot silently become employer requirements.

A work-implied capability must cite an explicit work-duty item. It is an analytical interpretation, not an employer-stated requirement for prior professional employment. The output schema intentionally has no field allowing the model to set employer obligation strength; the B2 candidate evidence index retains that separately.

The runner writes only under ignored data/local-acceptance/, using a copy of the frozen B0 database for comparison and new B4-only tables. The configured local LM Studio analysis model is called through the native local API with reasoning explicitly off, a loaded-model preflight, up to four one-shot requests (three in the frozen B4 v4c experiment because the qualifications-only case intentionally abstained), no retry or corrective call, and a bounded output budget. Only final message content is parsed; raw reasoning channels and full raw response bodies are not retained. To fit the configured model context, model input contains the B3-reviewed English item translations and exact source-item IDs, not the original Persian text or structured board values. Original Persian spans, selected translations, hashes and review evidence remain in the private evidence bundle for subsequent assistant source review. A failed request leaves a source-evidence-only fallback and a typed failure state.

The B4 comparison reports the actual frozen v30/v9 attempt/artifact state. It does not re-run v30, treat rejected candidates as valid, include v31 as a baseline, or claim owner-time savings. Four previously exposed ads are a development cohort, not unseen validation.

## Bounded 2026-11-19 result

The candidate-only research produced two source-reference validated **partial** model briefs, one rejected model output and one qualifications-only source-only brief. Model-generated fragments with unsupported categories are quarantined without discarding unrelated, source-grounded work descriptions; the raw final model response remains private for inspection. Mechanical validity is not semantic correctness. The original-language source comparison found open optional/alternative completeness and possible named-platform translation issues. See `docs/working-memory/2026-11-19_P16_B4_PARTIAL_JOB_UNDERSTANDING_ENGINEERING_MILESTONE.md`. No production route is changed.
