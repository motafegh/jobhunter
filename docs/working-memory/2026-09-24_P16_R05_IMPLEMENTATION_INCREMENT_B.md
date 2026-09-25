# R05 Increment B — pending-candidate item review

**Date:** 2026-09-24  
**Status:** MERGED TO `main` / CI GREEN / REAL-LOCAL ACCEPTANCE OUTSTANDING  
**Branch:** `agent/r05-item-review-2026-09-24`  
**Merged PR:** https://github.com/motafegh/jobhunter/pull/10 — merged after A1–A2 PR #9 on 2026-09-25 (`99072e97ed47ee169d99fefaaea385ec3a45a6d6`).  
**Parents:** `2026-09-24_P16_R05_ITEM_LEVEL_REVIEW_DIRECTION.md`, `2026-09-24_P16_R05_CORRECTION_LIFECYCLE_AND_PROPORTIONAL_GUARDS.md`, `2026-09-24_P16_R05_MINIMAL_RECORD_AND_DIAGNOSTIC_CAPTURE_DESIGN.md`, `2026-09-24_P16_R05_REVISION_DEPENDENCIES_AND_FAILURE_CAPTURE_FINDINGS.md`, `2026-09-24_P16_R05_IMPLEMENTATION_INCREMENT_A2.md`.

## Delivered

`analysis_item_review.py` holds independent append-only review events, original item digest/index/collection and source excerpt, optional correction proposals, materiality, independently anchored source-coverage gaps, and a review session that must assess every original claim before completion. Beginning an item review establishes a SQLite acceptance trigger on the existing analysis table; a still-open session prevents the old CLI/browser whole-artifact accept operation. A newly recorded finding reopens a completed item-review session. Historical accepted or untouched pending analyses are not mass-reopened; only current pending v21/v5 English candidates can start this review. Original accepted and rejected artifact history, Registry claim indexes, Market snapshots and public corpus are not rewritten. Material unsupported employer claims and material open coverage gaps block completion; an explicit reviewer may record that an earlier finding was mistaken, retaining the full audit history. A submitted corrected/additional wording remains a non-authoritative proposal even after item-review completion.

The existing CLI dispatches private `jobhunter --config config/local.toml item-review ...` commands without public-corpus export. The existing local browser runtime registers `/jobs/<job-id>/item-review`; pending job details link to the page. It displays source evidence and original statements, accepts per-item and exact-projection-anchored coverage findings using existing CSRF, and preserves separate whole-artifact accept/reject. `tests/test_analysis_item_review.py` and `tests/test_web_item_review.py` cover acceptance fence, material issue/gap resolution, candidate immutability, exact source proof, rejected-candidate history, legacy behavior, CSRF, stale ID and finish-without-auto-accept.

## Verification

GitHub Actions CI #1345, commit `b3091c891a5845d51fe4e32d1236a5c8cfa3685a`, passed entrypoint smoke, Ruff, full tests and full warnings-as-errors. No real-local user DB acceptance, reviewer usability session with representative `tvMm`, actual provider failure capture, or Market I7 acceptance was performed.

## Bounded continuation and stop line

This is a review workflow, not automatic semantic fact repair. No reviewed new claim set or accepted revision is created. C requires an explicit immutable revision identity/current-selector and downstream-dependency migration across Capability, Registry mappings, Work, immutable Market snapshots and public corpus; preserve old accepted IDs and source/projection identities. PRs #9 and #10 are merged into `main` by explicit user authorization on 2026-09-25. Real-local verification and reviewer usability acceptance remain outstanding. The active public v21/v5 route and Market I7 HOLD are unchanged.
