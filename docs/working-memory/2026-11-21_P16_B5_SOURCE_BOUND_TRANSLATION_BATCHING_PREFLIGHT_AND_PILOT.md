# P1.6 B5 — bounded source-bound translation batching: preflight and local pilot

**Date:** 2026-11-21
**Branch:** main
**Disposition:** Experimental batching and two-item exposed local pilot PASS; **unseen B5 semantic acceptance and B6 promotion remain OPEN/BLOCKED**.

## Motivation and scope

The B2v2 source-structure candidate selected 142 Persian item-level translation candidates from eight **previously exposed** development ads, alongside 96 native original-language items and 20 excluded context items. Calling the local model once per item has a high request count, but batching unrelated clauses could swap identity, hide preferences, strengthen requirements or introduce semantic drift.

This increment adds an **opt-in, non-authoritative sidecar**, leaving the established LM Studio translation-v2 provider, original B2/B3 evidence, accepted P1.6 v30/v9, source snapshots, downstream consumers, production database and public routes unchanged.

## Engineering implementation

- `src/jobhunter/source_bound_translation_batch_b5.py` defines source-exact, deterministic batches, preserving original source anchor IDs, source field/semantic/span hashes, candidate category, strength and source heading digest. A batch never mixes jobs, different semantic versions, headings, obligation strength or categories.
- Request bounds: at most four source items and 1,200 total source characters. Oversized items are explicitly deferred; duplicate content-derived IDs cannot occur in one request. The proposed offline selection uses **three items maximum**.
- The local Gemma E2B provider inherits the existing strict structured JSON contract. Wrong, extra, duplicate or missing IDs fail the batch rather than silently permuting translations. Valid responses associate each English result with its source; they do **not** certify linguistic fidelity.
- A member that still contains Persian script or blank output is marked unresolved; failed requests also produce unresolved individual entries. Existing truncation recovery can produce multiple physical HTTP attempts per invocation, so a future larger trial must measure and cap *actual* attempts separately from planned batches.
- Synthetic tests cover deterministic planning, source integrity, ID/order permutation, malformed JSON/schema, wrong IDs, blank/Persian outputs, timeout/truncation recovery, duplicate text, oversize deferral and unchanged legacy one-item translation behavior.

## Offline preflight — eight exposed cases

| Max compatible items per request | Planned requests | Deferred items |
| --- | ---: | ---: |
| 1 | 142 | 0 |
| 2 | 87 | 0 |
| 3 | 74 | 0 |
| 4 | 67 | 0 |

These are **planned request counts, not actual calls, latency or model accuracy**. Batch segmentation is deliberately conservative, grouped by source and meaning context. The B5 80-call paired-analysis ceiling is **separate** from translation; no new translation budget is yet approved.

Private source-inventory and plan receipts were frozen before the pilot. Replayer: `scripts/verify_p16_b5_translation_batch_preflight.py`. Safe plan: `docs/working-memory/2026-11-21_p16_b5_translation_batch/SAFE_EXPOSED_TRANSLATION_BATCH_PREFLIGHT.json`.

## Local pilot: two preferred-source items

Before inference, the scope was fixed to two source-owned qualification items from the **exposed** eight-job set, with a common heading and provisional `preferred` strength. Model: local `gemma-4-e2b-it` via `127.0.0.1:18080`, with strict JSON schema, one batched request plus two independent single-item controls, and a predeclared four-physical-HTTP-attempt maximum. The three observed calls stayed within that bound; transport-level per-request enforcement under multi-attempt truncation recovery is still required before a broader pilot.

Observed: **3 logical invocations, 3 HTTP 200 completions, 2/2 exact batch-versus-single English target matches**. Source-to-target hashes and original item association were verified. The exposed assistant review found both item-level translations faithfully preserved their original limited wording (basic-level malware analysis; familiarity with PowerShell and Sysinternals), without upgrading skill strength. This is **not independent blind linguistic review**.

**Key limitation:** the original `preferred`/advantage status comes from the source *section heading*, not from the isolated translated English phrases. It is retained only in the separate source metadata. Downstream model consumers must preserve that context and must not treat an unqualified English phrase as evidence that an employer explicitly *requires* prior experience.

Two original-source B1 item identities were also rebuilt and aligned to their exact candidate translations through an opt-in `src/jobhunter/source_bound_translation_b1_alignment_b5.py` bridge. The earlier B1 draft validator passed; both alignments remain unreviewed candidates with no downstream authority.

The batched call took roughly 16 seconds; subsequent singles roughly 2.7 and 2.9 seconds each. The sequence is not randomized or warmup-controlled, so fewer requests did **not** establish a latency saving. All raw source excerpts, provider requests/responses and item-level assistant review were retained only in ignored private local acceptance evidence.

Replay and boundary verifier: `scripts/verify_p16_b5_translation_batch_pilot.py`. Safe outcome: `docs/working-memory/2026-11-21_p16_b5_translation_batch/SAFE_EXPOSED_TRANSLATION_BATCH_PILOT.json`.

## Decision and next milestone

**PASS — experimental source-association/transport proof on exposed cases only.** There are no new accepted employer facts, public routing changes, production database writes, or approved B5 model-quality claims.

Before a larger live run, define and enforce a separate physical-request/time budget for translation, verify all-member failure behavior under truncated/error responses, and evaluate representative varied exposed examples for modality, alternatives and named-entity drift without making the prompt too rule-heavy. When the candidate and budgets are frozen, select **new, different, unexposed** six-to-eight original ads, seal source-first review before inference, and perform fair paired comparison with unchanged v30. Do not reuse these eight as a B5 unseen success set.

**Verification:** 1,150 warnings-as-errors local tests passed, including 24 batching/B1 bridge tests; Ruff, formatter, dependency consistency and compilation passed. Frozen private batch planning, actual three-call pilot/B1 alignment and B2v2 historical replayers passed. No raw source descriptions or complete provider responses are staged for Git. GitHub CI must be verified independently.

**B5 generalization NOT ESTABLISHED. B6 production promotion remains UNAUTHORIZED.**
