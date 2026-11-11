# P2.3A comparison: independent first-view review and next-slice predecision — 2026-11-11

**Status:** INDEPENDENT TECHNICAL/MAINTAINER REVIEW COMPLETE; OWNER REPEATED-USE ACCEPTANCE PENDING.
**Source base:** main commit `21f9d03` (2026-10-26), evaluated using the isolated review branch at `f099aa3`.
**Scope:** Existing bounded `/compare` view, four public accepted-job scenarios, real Chromium rendering at desktop/mobile widths. No production-state mutation or new inference.

## Findings and evidence

The repository-safe aggregate record is `2026-11-06_p23a_compare_owner_usefulness/AUTO_METRICS.json`.
All four scenarios were evaluated from an online SQLite copy, with integrity `ok`, zero foreign-key violations, no source calls, and no model calls.
The 878 strict-warning tests, Ruff, pip consistency checks, and TestClient rendered-route probes passed in the earlier local review.

An independent Chromium run used the current application against a separate temporary SQLite copy on loopback.
Browser tool binaries were already cached locally; no new dependency was added to the repository.
Four scenarios were exercised at **1440×900** and **390×844** viewport sizes:

| Scenario | Matching distinct claims | Direct matching duties | Browser result |
| --- | --- | --- | --- |
| RAG across `tvMm`, `tNVe`, `t7Ay` | 3 / 4 / 3 | 1 / 1 / 0 | HTTP 200; ten expandable evidence items; no false direct duty for `t7Ay` |
| Python across `tG9K`, `tmBK` | 2 / 2 | 0 / 0 | HTTP 200; optional job-local grouping and expansion displayed |
| Requirement-only across `t7ck`, `t7Ay` | 18 / 26 | 0 / 0 | HTTP 200; direct-duty absence disclosed rather than inferred |
| Deliberate no-match across `tvMm`, `tNVe` | 0 / 0 | 0 / 0 | HTTP 200; explicitly states no wording match, not no demand |

At both viewport sizes: expandable evidence, source drill-down links, and optional grouping toggles worked. The tested pages had no document-level horizontal overflow. The RAG first evidence drill-down navigated to `/jobs/tvMm#english-analysis`; browser Back restored the original compare selection and filter. No browser page errors or off-origin network requests occurred in that navigation check.

### Measured structural friction (not user timing)

For the RAG comparison, at the inspected viewport:
- 1440×900: job grid begins approximately **485 px** from page top; first claim begins approximately **822 px**; document height approximately **1,851 px**.
- 390×844: job grid begins approximately **1,074 px** from page top; first claim begins approximately **1,411 px**; document height approximately **4,740 px**.
- At 390 px, the navigation uses intentionally horizontally scrollable groups and the three job cards stack vertically. This avoids page overflow but pushes the substance well below the initial viewport.

These positions are a single run's geometry, not a time-savings estimate or an accessibility conformance result. Local screenshots and browser script/results stay under ignored `data/local-acceptance/` and are **not** committed.

### Practical design issue

The current UI is a faithful *multi-job factual reader*: it presents separate per-job lists. It does not form a semantic alignment of different wording across jobs. It can answer the RAG direct-duty question by comparing two job cards against a requirement-only third, but the reader still scans separate sections manually. This is not a regression or an authority defect; it is the next usability/decision-quality hypothesis.

## Options considered

**A — Read-only cross-job overview (preferred, bounded experimental increment).**
Display a compact *at-a-glance* summary for the currently selected jobs near the start of the results, with distinct matching requirement and direct-duty counts, exact-claim coverage, known explicit-depth counts, and links into each job's original claim cards. Explain that counts are document observations, not rankings, fit, or market demand. Make mobile navigation to results discoverable. This reuses the existing read model; no new inference or persistence. It does not equate unrelated claims.

**B — Cross-job semantic alignment.**
When multiple jobs have an *exact same reviewed Registry concept ID*, a separate alignment view may show them together while preserving each original claim and mapping decision. Unmapped lexical or inferential similarity must not become canonical equivalence. This requires a separate scoped experiment and may have limited coverage today.

**C — New model-proposed capability profiles or broader taxonomy.**
Do not implement now. Existing six-target Strategy-B coverage is unavailable and owner repeated-use outcomes are not established; there is no authority for persistent P2.3 profiles, Strategy C, or P2.2C/P2.2D promotion.

## Recommended next slice / gates

1. Build **Option A as a read-only candidate on a separate experimental branch**, without replacing the accepted `/compare` evidence cards.
2. Test against the same four cases and real 1440px/390px Chromium: preserve unique claim counts; distinguish requirements from direct duties; show unknowns; no silent inference; links navigate to exact claim evidence; no browser errors, external traffic, profile mutation, or horizontal overflow.
3. Record before/after structural geometry and ensure the overview can be reached with minimal scrolling. Treat it as an engineering observation, not owner benefit.
4. Request genuine owner repeated-use assessment of the prototype and the baseline. Use the comparison to authorize/reject any next main-branch change.
5. Reconsider exact reviewed-concept alignment (B) only if it materially helps answer an observed question.

**No acceptance claim:** Owner notes in `2026-11-06_p23a_compare_owner_usefulness/OWNER_REVIEW.md` remain pending. No measured comprehension, time savings, or product adoption was demonstrated. This record authorizes no main-branch merge or higher-semantic promotion.
