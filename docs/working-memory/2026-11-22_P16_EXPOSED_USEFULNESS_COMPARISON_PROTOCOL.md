# P1.6 Stage B — frozen exposed-cohort job-understanding usefulness protocol

**Date:** 2026-11-22. **Decision:** development usefulness evaluation only; never B5 unseen acceptance or B6 promotion.

## Goal and fixed sources

Determine what an applicant can *actually understand and act on* from the existing, source-qualified B4v5 first view, compared with **existing** English v30/v5 and original-language v9/v4 artifacts where they have valid, same-source comparable material. No regenerations, new LM Studio calls, Jobinja acquisitions, trusted-label promotions, browser routing or writes to production SQLite. The only outputs are an ignored-local private audit and a public-safe result with counts and hashes.

Exactly four **previously exposed** B0/B4 jobs, in fixed order `tNhZ`, `tMps`, `tNDx`, `tMjm`. Do not substitute easier ads or count source-only cases as model generation successes. Candidate under review is the already-frozen `B4v5` source-qualified projection, *not* new B2v5, whose four-cohort retrofitting does not qualify it for a user-facing comparison. The archived B4v4c run includes two partial B4 model candidates, one failed, and one intentional source-only abstention; missing interpretations must remain missing.

## Input freeze (SHA-256, relative to repository root)

| Input | SHA-256 |
| --- | --- |
| `data/local-acceptance/p16-stage-b4-2026-11-19/primary-v4c/B4_BASELINE_COMPARISON.json` | `e7d6b37235136bd98df568240ae36e1a05deb79c2ccf5ed58ac9e9eda22a279d` |
| `data/local-acceptance/p16-stage-b4-2026-11-19/primary-v4c/PRIVATE_B4_CANDIDATES.json` | `8d7155448f0311ad0fff4e3d739c4fd3fb57dca33d08e46815e2618686837bc3` |
| `data/local-acceptance/p16-stage-b4-2026-11-19/primary-v4c/B4_EXPOSED_ASSISTANT_SEMANTIC_REVIEW.json` | `a3a61f5cc35fa460102d0c0960c7ff3a9c58536d3ed74dcb1448315e92087d26` |
| `data/local-acceptance/p16-stage-b4-2026-11-19/source-projection-v5c/PRIVATE_SOURCE_PROJECTIONS.json` | `a9ea424cfa497620799600947d31ee3906f8b351a959d8325c983dc5abc63a27` |
| `data/local-acceptance/p16-stage-b4-2026-11-19/source-projection-v5c/FINAL_AUDIT.json` | `16078e2c8e894289cb3a5174f76d4d1fb985bba3fd76fffcf8877982d86ee6ee` |
| `data/local-acceptance/p16-stage-b4-2026-11-19/reviewed-terminology-correction-v5.json` | `054c1065c54e0a1abdf27e93803dbf3feedac25859f01e2778a3e464594450f4` |
| Production `data/jobhunter.sqlite3` | `d9068fcb503860638cb2187b537e57151bea0192ff69ab7dbe381c84fb2353d8` |
| Public `corpus/manifest.json` | `7a65485c813a855d144160f1009559decaf0383dba06a089760d2101726fda4` |

A verifier must reject changed inputs and protect the prior read-only `verify_p16_b4v5_source_projection.py` result. Do not expose original employer prose, private paths, job-board URLs or any LLM responses in the public scorecard.

## Fixed questions and task-level assessment (selected high-risk checks)

The following questions are **preselected from known development failure classes**; this is a deliberately diagnostic, nonrandom sample, not a whole-ad denominator:

| Case | Question A | Question B | Optional question C |
| --- | --- | --- | --- |
| `tNhZ` | What are the explicitly assigned work duties? | Is previous financial/LLM familiarity mandatory or an advantage? | — |
| `tMps` | What are the explicit work duties? | Are Middle and Senior paths alternatives, including nested option conditions, or cumulative? | — |
| `tNDx` | What are the explicit security work duties? | Are certificate and equivalent knowledge alternative routes, and is teamwork preferred? | Does the user-facing English rendering preserve the original ticketing product name and the exam condition? |
| `tMjm` | Does the source actually assign any explicit work duties? | Is remote work presented as a possibility, not a mandatory qualification? | — |

For each task, inspect original-source anchors in the frozen B4v5 projection (and earlier source-first review where available). Record **source-qualified candidate answer** separately from model-generated claims. Explicitly check false requiredness, genuine duty omission, OR/AND, negative/optional wording, translated technical/name drift, provenance, and declared unknown. The B4v5 original quote is primary inspection evidence; the English candidate is merely a reading aid and can be partial or wrong.

## Frozen comparison and verdict language

- Determine **same-source identity** and actual baseline state before comparisons. `v30` with failed, rejected, pending, absent or stale attempts is not a comparable accepted output; report **no qualifying same-source v30 answer** rather than claiming B4v5's source text “beats” a model or treating a failure as no employer requirements. `v9` mechanical acceptance alone does not independently certify its semantics or its English usability.
- Where a genuine usable same-source baseline exists, cite exact artifact IDs/source identity and compare **what is visible**, including contradictions or omissions. If only status summaries are archived, say qualitative semantic comparison **not established**; do not invent baseline text.
- Per-task verdict vocabulary: `source_supported_visible`, `partially_visible_or_uncertain`, `potentially_misleading`, `not_visible`, `not_evaluable`. A readable original quote without a validated interpreted answer should remain qualified, not necessarily `source_supported_visible`.
- Count observables: source item coverage, alternative graph presence, conditional/preferred visibility, corrected-name overlay, suppressed old model claims, failed model/valid source-only fallbacks, accepted/attempted baseline status, and exact provenance. Missing job purpose, untyped section relations, translation defects or partial presentation count as limitations. No automated model correctness percentage, no universal user-readiness score.
- **Usefulness judgment is qualitative:** Is the view likely to reduce manual reading while avoiding dangerous conclusions? The same assistant and known exposed examples may bias answers; this is **not** blind independent human review. No measured human time saved, A/B effect, market generalization, or owner approval can be claimed.
- Avoid treating coverage and large JSON counts as a win. On an incomplete/failed model job, a source-only view can be useful as a **candidate fallback**, not a validated replacement for v30. The benchmark's outcome may be positive, mixed, negative, or unassessable.

## Stop and next-step rules

Stop/mark blocked for original source/version drift, unreviewed mandatory claim promotion, missing alternative treated as a confirmed requirement, fabricated duties, or private-data exposure. Pass only an **offline evaluation engineering gate** when all input hashes, exact source identities, baseline states, candidate nonpromotion, and audit reproduction checks pass. B5 and B6 remain closed regardless of development usefulness; the next design decision may select targeted model-assisted *interpretation*, not source-truth promotion. If qualitative evaluation is too weak, report what remains unestablished and propose an actual blinded/user decision experiment.

**Freeze intent:** Commit this scope and method to `main` before running the usefulness comparison or interpreting its result. Prior exposure to known case failures is recorded; no assertion of blinding.
