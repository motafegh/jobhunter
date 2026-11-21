# P1.6 B5 — eight fresh-source cases acquired; upstream source-semantic gate BLOCKED

**Date:** 2026-11-21
**Branch:** `main`
**Decision:** `STOP_B5_PAIRED_EVALUATION_BLOCKED_UPSTREAM_SOURCE_SEMANTICS`

## What happened

We followed the B0 preregistered fresh-source procedure, not the earlier exposed four-ad development comparison. Through the existing authorized Jobinja source adapter, nine initial search pages and eleven additional deeper pages were obtained with normal HTTP 200 access and no bypass or cloud model. The isolated discovery database recorded 258 distinct listing IDs. Screening against the 485-ID B0 exposure index, the original committed public corpus, and identical company/title reposts left 191 metadata-eligible listings. The ordered pool and exclusion ledger were preserved privately. The provisional exclusion is not claimed to be exhaustive against all historical private chats.

Before reading source detail or model output, eight distinct primary ads and six reserves were selected and frozen: **two Python/backend, three applied AI/LLM, three security/network/cyber**. All eight primary original detail pages fetched and parsed successfully; every raw HTML SHA and parsed semantic SHA was independently verified, and the source snapshot SQLite passed integrity/FK checks. The live application database remained byte-identical.

**Acquisition-side-effect handling:** The normal CLI entrypoint automatically synchronizes the tracked public corpus from whichever database is configured. Initial B5 discovery through that CLI temporarily caused a tracked corpus rewrite from the isolated database. It was detected and completely restored to the committed 420-job state; the worktree returned clean and no production DB was changed. Subsequent detail fetches used the existing approved underlying Jobinja service directly, avoiding that public-corpus hook. This is also a candidate for a narrow future isolation regression; do not pretend the first CLI step was side-effect-free.

## Preregistered source-only review before B2

The assistant read **only the eight frozen original descriptions** and sealed **93 exact original source quote anchors** with character offsets, source semantic SHAs, modality, concise source-first reading and unknowns. It was done **before** the new B2 candidate was run or seen; no B3 translation, B4 job-level inference, or v30 baseline was run.

This is a **selected high-risk original-source review**, not a complete statement inventory, market accuracy denominator, owner-approved facts, or independent blind human reference. Original quotations and employer data remain ignored under `data/local-acceptance/p16-stage-b5-2026-11-21/`, not in the tracked Git decision.

## Source gate result: mechanical evidence PASS, semantic interpretation FAIL

The *unchanged* B2 source parser mechanically validated all eight source-item candidates and their original span hashes. However, the source-first comparison identified critical upstream errors:

| Frozen source-first check | Observed |
| --- | ---: |
| Original source-review anchor assertions | 93 |
| Assertions with direct duty/qualification/behavior/arrangement reference roles | 86 |
| Matching B2 role-category anchors | 25 |
| Role-category mismatches among selected anchors | 58 |
| Explicit work-duty anchors not correctly classified as duties | 19 |
| Optional/preferred original assertions incorrectly classified as required | 2 |
| Jobs missing the structured “one or more security specialties” alternative | 1 |
| Jobs with structural or category gaps among eight | 7 |

The counts refer to **preselected assistant source assertions**; they are **not** the full source-claim denominator or accuracy percentages. Distinct failure examples include a Python/backend ad collapsed into three unresolved spans; an AI role with explicit duties but zero recognized duties; an AI agent role collapsed into one unresolved description item; native-English requirements given mostly unresolved classification; and a multi-specialty security role whose alternative pathways were not represented. In a sparse threat-detection role, two skills explicitly labeled advantageous were incorrectly marked required. One application/platform-security ad passed the selected role assertion checks, but that does not certify its total accuracy.

**Critical stop triggers:** falsely required employer qualifications, missing alternative eligibility logic and failure to recover explicit work assignments are sufficient blockers under B0. No reasonable B4 summary or additional translation can transform these unsupported classifications into accepted employer facts.

**Outcome:** `BLOCKED_UPSTREAM_SOURCE_SEMANTICS`. The source-only reviewer, candidate selection, all source originals and evaluation decisions were frozen in that order. `scripts/verify_p16_b5_source_gate.py` independently replays the frozen result against the original unmodified B2 parser and checks original immutable SHAs, production DB identity and zero accepted promotions.

## What this gate does NOT prove

- **Not a B5 PASS:** No same-source B4-versus-v30 paired analysis was performed. No model output quality or owner usefulness can be inferred from a stopped run.
- **Not an independent human blind review:** An assistant reviewed source evidence first; selected anchors are not an exhaustive ground-truth corpus.
- **Not proof the existing accepted v30/v9 runtime fails in those same ways:** The evaluated component was the candidate B2 source-item classifier only.
- **Not reusable unseen evidence:** These eight source cases have now been compared with B2 and become an **exposed development/regression cohort**. Any repairs may use them as regressions, but a later B5 acceptance check must acquire another genuinely fresh, reserved six-to-eight-job cohort.
- **No production promotion:** Source B0, existing accepted English v30, original-language v9, Capability/Work/Registry/Market, five accepted anchors and main persistence remain untouched. B6 stays unauthorized.

## Next engineering decision

Repair B2 **generally**, not with eight employer- or posting-specific exceptions: broaden robust structural support for flattened mixed-language headings and native-English section labels; preserve explicit duties versus qualifications while allowing overlap and uncertainty; prevent preferred-section labels leaking into required strength; preserve separately recruited multi-specialty alternatives instead of merging all skills into mandatory requirements. Test both positive and negative counterexamples and explicitly measure prompt/complexity tradeoffs. Retain the exact frozen eight cases only as **new exposed regression evidence**. Acquire a completely new, never-compared B5 cohort for a fresh source-first assessment and paired v30/candidate comparison before considering B6.

## Inspectable record

Tracked implementation: `scripts/evaluate_p16_b5_source_gate.py`, `scripts/verify_p16_b5_source_gate.py` and `tests/test_p16_b5_source_gate.py`.
Safe, non-identifying aggregate: `docs/working-memory/2026-11-21_p16_b5/SAFE_B5_SOURCE_GATE_HALT.json`.
Private raw HTML, original quotes, selected source IDs/URLs, pool/exclusions, source-only review, snapshots and failed gate: ignored `data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1/`.

**Verification:** 1,109 full local warnings-as-errors regression tests passed; Ruff lint/format, package dependency consistency, compilation, staged diff checks and both B4v5/B5 private evidence replayers passed. Private data staged for Git: zero. GitHub Actions is checked separately.

This is a useful B5 **failure discovery and stop-line milestone**, not the completion of B5 semantic verification.
