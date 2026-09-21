# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-09-20
**Active branch:** `main`  
**Current state:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`  
**Market plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Current product gate:** MARKET I1-I6 ACCEPTED / I7 EXECUTED / HOLD — CLOSURE FOLLOW-UP NEXT

Status vocabulary:

```text
[ ] not started
[~] in progress / acceptance incomplete
[x] accepted/completed for stated scope
[!] blocking defect
[-] deliberately deferred
```

---

## A. Closed accepted substrate

- [x] Phase 1 CLOSED.
- [x] P2.1 Canonical Registry CLOSED.
- [x] P2.2A Job Work Intelligence CLOSED.
- [x] P2.2B-B1 CLOSED / NO-PROMOTION / DEFER.
- [x] Market foundation Q1-Q12 PASS / first vertical slice authorized.

Do not reopen accepted historical work without a repeatable current contradiction.

---

## B. Market first vertical slice

### I1 — domain + persistence — ACCEPTED

- [x] stable target + immutable definition versions.
- [x] run lifecycle/ledger persistence.
- [x] immutable exact-dependency memberships/corrections.
- [x] immutable snapshot/member history.
- [x] immutable deterministic aggregate-profile storage.
- [x] target-definition changes do not invalidate generic source/translation/P1.6.

Acceptance: `docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md`

### I2 — target-scoped affected work — ACCEPTED

- [x] target-only source missing/refresh planning.
- [x] target-only translation/P1.6 planning.
- [x] no global-backlog budget spill.
- [x] failed refresh != disappearance/fresh evidence.
- [x] exact downstream currentness/reuse.

### I3 — membership qualification — ACCEPTED

- [x] deterministic constraints first.
- [x] bounded semantic relevance only when needed.
- [x] `core_match / adjacent_match / uncertain / excluded`.
- [x] title/skills alone cannot prove core.
- [x] accepted P1.6 optional; pending/missing P1.6 not a membership gate.
- [x] exact dependency reuse and immutable reviewed corrections.
- [x] real-model boundary evidence preserved under `docs/experiments/2026-09-17_market-i3-real-model-acceptance/`.

Acceptance: `docs/working-memory/2026-09-17_MARKET_I3_MEMBERSHIP_QUALIFICATION_IMPLEMENTATION.md`

### I4 — immutable snapshot construction — ACCEPTED

- [x] terminal Market run required.
- [x] exact current membership identities only.
- [x] stale/superseded membership rejected.
- [x] semantic coverage preserved as accepted/pending/missing/failed/rejected.
- [x] only core enters primary corpus.
- [x] historical snapshot/member state immutable.

### I5 — deterministic aggregate profile — ACCEPTED

- [x] snapshot-only deterministic aggregation.
- [x] source/core vs accepted-semantic denominators remain separate.
- [x] per-posting concept deduplication.
- [x] immutable source-detail employer authority.
- [x] employer breadth/concentration warnings.
- [x] requirement strength and responsibility evidence drill-down.
- [x] Registry enrichment only as-of snapshot time.
- [x] no model-authored numeric facts.
- [x] repost/new-ID limitation explicit.

### I6 — shared browser + CLI workflow — ACCEPTED

Acceptance: `docs/working-memory/2026-09-17_MARKET_I6_BROWSER_CLI_WORKFLOW_IMPLEMENTATION.md`

- [x] one shared `MarketWorkspaceService` for browser/CLI.
- [x] immutable target acquisition/search envelope.
- [x] target search catalog version drift rejected.
- [x] bounded discovery/detail/translation/P1.6/membership controls.
- [x] explicit membership budget + remaining-work ledger.
- [x] partial-success run ledger preserves durable stage success.
- [x] read-only target preview does not construct model/provider runtime.
- [x] existing I5 aggregate contract restored/frozen after integration regression was caught.
- [x] CLI target/create-version/preview/run/run-show/snapshot-show.
- [x] browser `/market/targets`, run ledger and snapshot/profile drill-down.
- [x] existing one-mutable-web-operation boundary reused.
- [x] Market tables remain local/private; only existing upstream public artifacts may sync.
- [x] CI 1210 green: installed-entrypoint smoke, Ruff, 632 tests, 632 tests with warnings-as-errors.

### I7 — bounded real local acceptance — EXECUTED / HOLD

Protocol:

`docs/working-memory/2026-09-18_MARKET_I7_LOCAL_ACCEPTANCE_PROTOCOL.md`

Execution result:

`docs/working-memory/2026-09-18_MARKET_I7_REAL_LOCAL_ACCEPTANCE_HOLD.md`

- [x] local runtime/SQLite/provider readiness established and pre-run integrity was clean.
- [x] stable Applied AI / ML target + immutable definition created.
- [x] exact five-search / one-page / request-budget-five preview verified.
- [x] two bounded real Jobinja runs completed with explicit partial-success state.
- [x] discovery/acquisition remained target-scoped; rerun discovered 52 known candidates and zero new IDs.
- [x] translation currentness/reuse was visible; final rerun plan reported 9 current translations reused.
- [x] P1.6 pending/missing/failed coverage remained explicit and never became zero demand.
- [x] membership completed without membership failures; rerun dispositions were 6 core / 1 adjacent / 1 excluded.
- [x] run ledgers preserved partial failures rather than rolling back successful durable work.
- [x] first immutable snapshot/profile existed and exposed 6 core / 0 accepted-semantic postings.
- [x] browser usability/evidence presentation defect found during I7 was repaired and regression-tested.
- [x] Market-local tables/paths/provider identity were absent from public corpus publication.
- [x] initial I7 publication head passed CI 1246; closure-repair heads passed CI 1248 and CI 1249.
- [~] live accepted-semantic requirement/responsibility aggregate + evidence drill-down remains unexercised because accepted-semantic core denominator was zero.
- [x] recovered run-2 snapshot/profile 2 and proved snapshot-1/member/profile equality against both retained pre-rerun JSON captures on 2026-09-19.
- [x] post-run operational SQLite integrity is `ok`; foreign-key check is empty (2026-09-19).
- [x] inspected pending `t7ck` artifact 48: material coverage, optionality and qualification/duty defects; rejection recommended.
- [x] applied the reviewed rejection of artifact 48 during the authorized continuation; backup, exact historical-row comparison and SQLite integrity checks passed.
- [x] repaired rejection of a pending candidate referenced by an immutable Market snapshot; real-database-copy replay and 636 strict-warning tests passed.
- [x] fixed headingless qualification residual coverage and false implicit-duty detection; five accepted anchors were unchanged and the full strict-warning suite reached 638 passed.
- [x] recovered immutable definition-1 fingerprint from operational SQLite.
- [x] executed the one selected `tvMm` generation: attempt 106 failed validation; no candidate was persisted or accepted. See `docs/working-memory/2026-09-20_MARKET_I7_TVMM_BOUNDED_CLOSURE.md`.
- [x] repaired the exposed v20 structured-skill prompt/payload ownership contradiction with an offline provider-boundary regression; historical prompts and strict evidence/depth validation remain unchanged.
- [x] one bounded post-repair `tvMm` attempt created artifact 49; complete review rejected borrowed familiarity depth and an AI-system-behavior subject error.
- [x] repaired repeated-identical depth-marker borrowing in v20 with regression and retained raw-response replay; artifact 49 stays rejected.
- [x] inspected the remaining artifact-49 subject error across all 27 current English projections; four broad coverage spans in two jobs cross company-goal/application text. No safe deterministic cutoff or live retry is justified by this evidence.
- [x] source-backed evidence-span repair keeps `; to ...` with its subject and ends requirement scope at explicit `How to Apply:`; five accepted anchor plans unchanged. This does not semantically accept artifact 49 or close I7.
- [x] one bounded live check after that repair: `tvMm` attempt 108 failed depth-field validation after its allowed retry; no candidate was created. All seven Market tables matched the pre-run backup and SQLite integrity/foreign-key checks passed. The check is closed; I7 remains HOLD.
- [x] audited all 27 current English projections offline: 14 of 111 requirement references across 13 jobs have multiple depth markers, including one successfully reviewed accepted anchor. No length-only or punctuation-only split is justified; retain the fail-closed validator.
- [x] closed the explicit repeated-marker v20 guard gap: one `depth_signal` cannot combine two equal marker occurrences from different subjects. The five accepted P1.6 anchors validate read-only; 642 strict-warning tests pass. This does not resolve attempt 108 or I7 HOLD.
- [x] diagnosed attempt 108 at exact item scope: broad v20 coverage references make some correct null depths indistinguishable from omitted applicable familiarity; eight of fourteen multi-marker references also need shared preferred context. The closure record specifies the versioned candidate evidence boundary; do not relax v20 or repeat the same command.
- [x] implemented the isolated v21 scoped-evidence response contract: parent coverage and exact item excerpts remain separate, item depth and inherited preferred strength fail closed, and candidate-only scope is removed before unchanged v5 persistence validation. Six focused offline cases pass; no runtime route or live call yet.
- [ ] obtain at least one semantically valid accepted-current P1.6 core member and verify live semantic drill-down.
- [x] verified second snapshot/profile and first snapshot/profile historical immutability after the rerun.
- [x] verified post-execution SQLite integrity/foreign-key + privacy checks; repeat after future operational mutations.
- [ ] change I7 to PASS only after those remaining checks succeed; otherwise preserve HOLD.

---

## C. First-slice permanent invariants

- [x] target identity separate from immutable meaning versions.
- [x] target meaning does not invalidate generic upstream artifacts.
- [x] target-scoped work does not spill into unrelated backlog.
- [x] `uncertain` is a successful semantic outcome.
- [x] adjacent/uncertain/excluded never silently enter primary core denominator.
- [x] missing/pending/failed/rejected P1.6 never means zero demand.
- [x] only accepted-current P1.6 contributes to strong semantic statistics.
- [x] snapshot members reference exact dependencies.
- [x] snapshots remain immutable after future source/target/contract changes.
- [x] aggregate profiles reference one exact snapshot/contract.
- [x] first slice says `qualified source postings`, not unproven unique demand.
- [x] browser and CLI share state/service owners.
- [~] real local acceptance executed; HOLD closure checks remain before first-slice closure.

---

## D. Explicitly deferred / not authorized

- [-] P2.2C promoted responsibility families.
- [-] P2.2D stable promoted role archetypes.
- [-] P1.6 auto-acceptance.
- [-] Capability/Work as mandatory Market gates.
- [-] automatic repost/new-ID collapse.
- [-] semantic role-subfamily report synthesis in first slice.
- [-] trends / emerging / forecasting.
- [-] Market → You / personal readiness/gap/scoring.
- [-] Market publication to `corpus/`.
- [-] generic vector/RAG/graph/autonomous-agent/source-plugin infrastructure.

---

## E. Parallel portfolio/release

- [x] MIT license complete.
- [ ] GitHub description/topics settings action.
- [ ] real browser screenshots + privacy review.
- [ ] intentional `v0.1.0` tag/release.
- [ ] owner mastery verification.

Portfolio work does not broaden I7 authorization.

---

## Exact next action

```text
I7 HOLD semantic-evidence closure only
→ post-repair tvMm artifact 49 reviewed and rejected; no candidate is current
→ repeated-marker depth borrowing repaired and verified offline
→ candidate subject-attribution and model reliability remain unproven
→ source-span repair checked live once; attempt 108 failed item-specific depth validation and created no candidate
→ I7 HOLD; require independent representative evidence of a generalizable semantic improvement or naturally available valid accepted-semantic core evidence before another closure attempt
→ accepted-semantic snapshot/profile + CLI/browser proof still required for PASS
```
