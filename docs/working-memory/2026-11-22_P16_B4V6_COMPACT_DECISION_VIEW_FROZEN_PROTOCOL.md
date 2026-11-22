# P1.6 B4v6 — compact decision-question-first view: preregistered exposed-only protocol

**Date:** 2026-11-22. **Stage:** source-backed local research, NOT B5 prospective evaluation or B6 production. **Protocol must be committed before B4v6 implementation/outcome evaluation.**

## Purpose

Determine whether a bounded source-only first view helps an applicant answer actionable job questions with fewer immediately visible evidence excerpts than B4v5's verbose inventory. Do not confuse **shorter output** with demonstrated user comprehension, decision improvement, correctness, or reading-time savings. The source and authority model remain unchanged.

## Frozen cohort and artifacts

Exactly four previously exposed B4 original-source cases **in this order**: `tNhZ`, `tMps`, `tNDx`, `tMjm`. Reuse the frozen B4v5 projection, baseline identity and nine-task matrix from `docs/working-memory/2026-11-22_P16_EXPOSED_USEFULNESS_COMPARISON_PROTOCOL.md` (committed `1abd1e0`) and `scripts/evaluate_p16_exposed_usefulness.py`. The prior public scorecard is immutable. Its selected anchors may be used **only by the evaluator**, not to hardwire the new first-view ranking.

Frozen SHA-256:
- `data/local-acceptance/p16-stage-b4-2026-11-19/source-projection-v5c/PRIVATE_SOURCE_PROJECTIONS.json`: `a9ea424cfa497620799600947d31ee3906f8b351a959d8325c983dc5abc63a27`.
- `data/local-acceptance/p16-stage-b4-2026-11-19/primary-v4c/B4_BASELINE_COMPARISON.json`: `e7d6b37235136bd98df568240ae36e1a05deb79c2ccf5ed58ac9e9eda22a279d`.
- `data/local-acceptance/p16-stage-b4-2026-11-19/source-projection-v5c/FINAL_AUDIT.json`: `16078e2c8e894289cb3a5174f76d4d1fb985bba3fd76fffcf8877982d86ee6ee`.
- `data/local-acceptance/p16-stage-b4-2026-11-19/reviewed-terminology-correction-v5.json`: `054c1065c54e0a1abdf27e93803dbf3feedac25859f01e2778a3e464594450f4`.
- Production SQLite: `d9068fcb503860638cb2187b537e57151bea0192ff69ab7dbe381c84fb2353d8`. Public corpus: `7a65485c813a855d144160f1009559decaf0383dba06a089760d2101726fda4a`.

## Candidate first-view design (frozen before implementation)

Construct a **generic, deterministic, source-backed view** from a B4v5 projection without any case-ID, employer-name or task-specific anchor filtering. No LLM or new translation requests. The view must lead with four applicant questions in this order:

1. **What would I do?** Show at most three distinct candidate duty excerpts by original source order; prioritize separately reviewed terminology-corrected duties, and disclose remaining duty count. If zero, report *no separately extracted explicit duty candidates*, not "the job has no duties".
2. **What capabilities are expected?** Split applicant-capability candidates by `required`, `preferred`, and `unresolved`; display at most two in each tier in original order, and explicitly disclose undisplayed counts. A behavior/trait can also be a broad qualification, but does not establish required paid professional experience. Strength remains candidate-only, never authoritative.
3. **Are there options or alternatives?** Show every source-linked B4v5 candidate eligibility graph (max four per job; if more, refuse rather than silently omit). Label each **unreviewed candidate OR/AND**, not a verified eligibility rule. Nested original-language children remain source-first with English child alignment **not established**. No illustrative example list may become a formal mandatory eligibility OR.
4. **What conditions or uncertainties matter?** Prioritize explicit conditional application instructions and working arrangements over ordinary context. Show at most three condition excerpts; disclose remaining counts. Show suppressed model-claim count, missing B4 model status, untranslated/excluded source-item count, and any `unresolved` candidate category; never imply missing means zero real responsibilities.

All first-view excerpts must have `source_item_id`, SHA-256 of exact original text, original-language evidence and an English reading aid **only if already present in B4v5**. Preserve every B4v5 source item as a full-drilldown record in the candidate object; hide it from the default rendered body, not from evidence. Preserve existing reviewed correction and model suppression. Use Markdown escaping for untrusted employer prose, prohibit HTML injection, omit raw job URLs in public-safe report. No new employer fact/accepted state.

## Frozen comparison / measurement rules

Evaluate B4v5 and B4v6 on identical original/source versions; **not against accepted v30 semantics** because none of these four has a valid same-source English v30 artifact. For each of the **nine fixed tasks**, use existing original-first task anchors and graph IDs to determine whether the key evidence is immediately visible, available only through full source drilldown, absent, or non-evaluable. **Do not auto-grade textual meaning**, e.g. a visible preferred item is still an *assistant-reviewed candidate*, not independently proven human understanding. Reject a source hash drift, wrong case identity, missing drilldown original, false required-strength promotion, invented eligibility graph, lost translation correction/entrance exam, false absence of duties, or new visibility of source-suppressed model claims.

Compare measurable display cost using **visible evidence-item count, visible original/English characters, rendered markdown characters, and number of source links a reader must open for each of the nine tasks**. These are proxies, NOT measured user time or real comprehension. Record default-visible, drilldown-required, lost, or not-evaluable per task, plus case-level model and translation limitations. Success of this *engineering* slice means verified exact source identity, nonpromotion, zero lost evidence and explicit honest tradeoffs. It does **not require all nine questions immediately answered**, since compactness can introduce real retrieval costs. Do not hide failures.

## Privacy, authority, and stop rules

The outputs are (1) a private ignored local candidate/inspection record and markdown demo containing original text; (2) a tracked **aggregate-only**, source-safe counts/SHA report and decision document. Never publish raw employer statements, source IDs, job-board URLs, private source paths, entire model outputs, or any stable personal data. Any private artifact should be made only once and verified on subsequent runs. No production SQLite or public corpus modification; no calls to Jobinja, LM Studio or cloud. Only the existing source-based B4v5 candidate layer is in scope; B2v6 belongs to a separate exposed-only semantic gate.

**Interpretation:** Assistant inspection of four exposed ads is development feedback, not blinded human trial or proof of reduced time. The next honest action, if engineering succeeds, is a real owner/context-isolated reading/usefulness test and targeted semantic reasoning research before a newly frozen prospective B5 gate.
