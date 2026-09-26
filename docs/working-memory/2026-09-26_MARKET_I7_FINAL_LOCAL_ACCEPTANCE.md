# Market I7 — final bounded real local acceptance

**Date:** 2026-09-26

**Decision:** PASS for the first target-scoped Market vertical slice (I1-I7).

**Scope:** One repeated-use Applied AI / ML Engineering target workflow, not broad-market representativeness.

## Exact authority and controls

- Target 1, immutable definition 1, fingerprint `4f77e7966b68cae9c4d2545212269f7b85482458ce30e51bee435bdd65400d9f`.
- Five existing Jobinja searches, one page each, request budget 5. Source missing budget 0, refresh budget 8, 168-hour freshness rule. Translation and analysis budgets 0; membership budget 8.
- English P1.6 `job-analysis-english-v23 / job-analysis-v5` artifact 50 for `tvMm` was separately reviewed against source detail 47 and English projection 41, then explicitly accepted. Its 25 requirements and 11 duties exactly matched the complete reviewed non-persistent result. Acceptance was a human review action, not a validator or model promotion.

## Real run and reuse evidence

| Run | Source work | Membership | Immutable result |
| --- | --- | --- | --- |
| 4 | 8 due details refreshed, all unchanged | 8 completed; 6 core, 1 adjacent, 1 excluded | snapshot/profile 4 |
| 5 | 2 further details refreshed; one new source version among target candidates | 8 completed; same dispositions | snapshot/profile 5 |
| 6 | 0 detail refreshes, 0 translations, 0 analyses; 5 bounded search requests, 53 discovered candidates and 8 carried source IDs, 55 distinct target candidates | 8 reused/completed; same dispositions; 2 ready candidates remain outside the membership budget | snapshot/profile 6 |

Each run completed without stage failures. Run 6 reused eight current English projections in affected-work planning and one accepted current P1.6. The remaining two ready membership candidates and seven missing P1.6 analyses are explicit ledger work, not zero demand or hidden completion. The first post-acceptance run 3 had an empty snapshot because all eight prior members were refresh-due with refresh budget zero; the subsequent source-refresh runs resolved that currentness condition. The coordinator now carries forward source IDs from the latest nonempty snapshot of the same definition so search-page turnover cannot silently erase the target cohort.

Snapshot/profile 6 freezes eight members: six qualified core source postings, one adjacent, one excluded. Exactly one of the six core postings has accepted-current semantic evidence. The aggregate exposes 25 requirement and 11 responsibility evidence rows from frozen artifact 50, with job, source, English, P1.6 and membership identities. Profile 4 and 6 corpus, requirement, responsibility and employer sections match exactly. Historic snapshots/profiles 1–4 remained byte-stable across the final rerun.

The browser server rendered the real target, run 6 and snapshot 6 routes with HTTP 200. A headless Edge rendering of snapshot 6 was inspected locally: it displays 8 members, 6 core postings, 1 accepted semantic core posting, disposition/coverage rows and requirement evidence drill-down. The server-rendered HTML exposes the same frozen artifact 50 evidence and denominator warnings as the CLI. This checks rendered browser output and read-only route parity; manual mouse interaction was not performed. The private screenshot remains outside Git.

SQLite `integrity_check` returned `ok` and `foreign_key_check` returned no rows. Public-corpus verification passed for 410 known jobs, 51 detail jobs, 27 current English projections, 6 accepted English P1.6 and 5 accepted Capability artifacts. No SQLite, Market tables, target state, private run captures or screenshots entered `corpus/`; only governed public source observations and accepted P1.6 projection changed.

## Decision and limits

The protocol's repeated-use path, exact currentness/reuse, immutable history, accepted-semantic evidence, CLI/browser read parity, source integrity and privacy boundaries pass. I7 is **PASS** for this bounded first slice. The profile correctly warns that six source postings and one accepted-semantic posting are small samples, that five core postings lack accepted P1.6, and that repost/new-ID adjustment is unimplemented. The displayed 100% semantic-row shares have denominator **one accepted-semantic posting**; they are not market prevalence. No promoted role subfamily, trend, personal gap or recommendation claim follows from this acceptance.

Evidence owners: `docs/working-memory/2026-09-26_MARKET_I7_ACCEPTED_CORE_AND_REUSE_REPAIR.md` for the preceding repair, the immutable local Market runs/snapshots/profiles, and the private captures under `data/local-acceptance/i7/` (not published).
