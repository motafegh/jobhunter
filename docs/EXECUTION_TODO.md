# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-09-26
**Active branch:** `main`  
**Current state:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`  
**Market plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Current product gate:** MARKET I1-I6 ACCEPTED / I7 EXECUTED / HOLD — V23 CASE REVIEW PASS / PERSISTED ACCEPTANCE NEXT

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
- [x] implemented the isolated v21 provider boundary over the shared v20 transport/partition coordinator; typed response selection and candidate-scope stripping are covered by offline tests. Current v20 service/routing/persistence remain unchanged.
- [x] validated all 85 requirements in the five accepted P1.6 anchors read-only under v21, including exact item excerpts for the seven shared-list `tmBK` claims and canonical source casing. No accepted artifact was regenerated.
- [x] ran one non-persistent v21 `tvMm` evaluation after offline/CI gates: it failed with seven omitted familiarity depths and no artifact/state mutation. Added candidate-only source-proven leading-depth canonicalization plus a coordinated-list scope stop line; unchanged v20 remains current.
- [x] rejected a mechanically complete second v21 result: one broad responsibility span hid two duties and one broad preferred span hid required architecture/system-building wording. Added a candidate-only exact sentence/item ledger; accepted v20 and all five accepted-anchor requirement plans remain unchanged.
- [x] repaired candidate reference registration after a no-model preflight failure; the optional transport catalog extension is supplied only by v21 and SQLite remained byte-identical.
- [x] ran one bounded non-persistent scoped-ledger evaluation: exact depth and all 11 duties passed review, but the model excluded an explicit required reliable-product candidate capability. The result remains rejected; direct candidate-mandate sentences are now non-excludable and retained-response replay fails closed. No artifact or operational state was created.
- [x] audited headingless candidate-experience wording across all 27 projections and added candidate-only exact coverage for four representative forms spanning `t7ck`, `tGM0`, `taku`, and `tvMm`; generic recruiting prose and application directives remain excluded, and accepted-anchor requirement plans remain unchanged.
- [x] validated the v21 transport ledger across all 27 projections (165 requirement refs, 60 responsibility refs, 39 partitions, zero collisions/non-source spans) and repaired duty-list handling for dependent `including` modifiers, independent Oxford-comma final duties, and coordinated bare-gerund chains.
- [x] removed candidate requirement leakage from Benefits/Location/KPI/Tasks/application sections, preserved shared preferred list/group scope, and recovered/refined explicit Job Description/Tasks/headingless duties. The current 27-projection audit covers 170 requirement refs, 100 responsibility refs and 38 partitions with no collisions, duplicates, unbalanced parentheses or non-source spans; accepted v20/v5 artifacts remain untouched.
- [x] promoted the complete 27-projection v21 exact-source/catalog/transport audit into a permanent offline regression.
- [x] one post-ledger non-persistent v21 `tvMm` evaluation failed after its bounded retry: exact duties and repaired subject coverage held, but familiarity depth was omitted and retained-response replay after safe single-marker canonicalization still omits one non-excludable headingless candidate-experience statement. No candidate/state mutation; evaluation closed.
- [x] isolated explicit headingless candidate-experience references from dense section/duty partitions in v21; the 27-projection regression preserves all 170 requirement refs without duplicates across 43 bounded partitions, and 677 strict-warning tests pass. Public v20 remains unchanged; real-model compliance is not yet proven.
- [x] one non-persistent isolated-partition `tvMm` evaluation completed with both headingless references, exact depths and all duties, proving the partition repair; semantic review rejected loss of explicit experience type and partial omission inside the second compound candidate statement. SQLite remained byte-identical and no state was created.
- [x] added exact compound-fact coverage within v21 candidate-experience parents and preserved source-explicit experience type; six representative parents across five jobs yield ten exact fact items, retained-response replay fails closed, 680 strict-warning tests and the 394-job corpus gate pass.
- [x] one non-persistent compound-fact `tvMm` evaluation captured all five exact candidate facts but failed because the model placed checklist items in both `evidence` and `item_excerpt` instead of retaining parent evidence. SQLite remained byte-identical; the evaluation is closed pending unique exact item-to-parent canonicalization.
- [x] added candidate-only unique exact item-to-parent restoration; retained real response replay now validates all five facts with durable parent evidence, ambiguous ownership still fails closed, and 682 strict-warning tests plus the 394-job corpus gate pass.
- [x] one non-persistent fact-parent `tvMm` evaluation preserved all headingless facts, depths, strengths and duties but was semantically rejected because `understanding the architecture` and `real system building experience` collapsed into one knowledge claim. SQLite remained byte-identical; the evaluation is closed.
- [x] extended v21 exact-item coverage to clear sentence-leading understanding/experience conjunctions; `tvMm` now requires separate knowledge and experience items, retained-response replay fails closed, and 684 strict-warning tests plus the 394-job corpus gate pass.
- [x] one non-persistent mixed-fact `tvMm` evaluation preserved the mixed knowledge/experience facts and all prior boundaries but was rejected for labeling a source-stated reliable-product capability as experience without prior-exposure evidence. SQLite remained byte-identical; the evaluation is closed.
- [x] executed the first normal persisted v21 `tvMm` path after promotion: generation failed closed after the bounded validation retry because the model twice labeled a capability-only exact item as prior experience; no current artifact exists and no semantic acceptance occurred. The retry did correct the two initial depth-signal errors, isolating the remaining failure to concept-type adherence. See `docs/working-memory/2026-09-22_MARKET_I7_V21_PERSISTED_RUNTIME_FAILURE.md`.
- [x] implemented isolated v22 ontology-abstention candidate under distinct `job-analysis-english-v22` identity; unsupported `experience` typing is deterministically reduced to neutral `other` without changing concept/evidence/strength/depth/confidence. Current routing remains v21.
- [x] v22 offline proof preserves all six accepted historical `experience` claims, keeps the exact v21 requirement/responsibility ledgers across all 27 English projections, retains v5 persistence shape, and marks v22 runtime provenance explicitly.
- [x] CI run 1304 / `35761148349`: Ruff PASS, 701 tests PASS, 701 warnings-as-errors PASS.
- [x] first direct non-persistent v22 `tvMm` evaluation failed closed because v22 applied ontology abstention before resolving raw evidence IDs; SQLite remained unchanged and no artifact/state was created.
- [x] repaired v22 to resolve evidence aliases through the existing exact evidence catalog before ontology abstention; added requirement-level and full-response regressions for the live `built an Agent yourself to date` failure shape.
- [x] exact-head CI 35764994184 passed; the one authorized post-alias v22 evaluation completed with 27 requirements and 11 duties, then was semantically rejected because type-only abstention retained unsupported experience wording. SQLite/corpus unchanged.
- [x] v22 now rejects that unsafe abstention; retained-response replay isolates the error, the experience partition still passes, and 708 strict-warning tests pass.
- [x] completed offline representative evidence/design for generated claim wording and omitted preferred proof-of-work coverage after the v22 repair. The 2026-09-24 no-generation stop line was superseded by the owner's corrected v23 evaluation request. See `docs/working-memory/2026-09-24_P16_V22_POST_ALIAS_EVALUATION_CLOSURE.md` and the v23 review below.
- [x] isolated v23 preferred proof coverage, retained full source follow-up questions, and ran one non-persistent `tvMm` evaluation. Both allowed responses failed the inherited value-preference validator; no candidate or state mutation occurred. V23-only offline repair validates retained proof partitions, and the `tjgi` at-least-one sample was corrected from preferred to an uncovered required-strength case. The call is closed; see `docs/working-memory/2026-09-26_MARKET_I7_V23_OFFLINE_CANDIDATE_DECISION.md`.
- [~] required proof-sample coverage in `tjgi` remains a separate offline design question; it does not block the source-reviewed `tvMm` core candidate path.
- [x] owner-directed corrected v23 non-persistent `tvMm` evaluation passed complete manual source review: 25 requirements, 11 duties, three explicit proof preferences, no material semantic defects, and unchanged operational/public state. See `docs/working-memory/2026-09-26_MARKET_I7_V23_FULL_EVALUATION_REVIEW.md`.
- [x] promote v23/v5 public routing with accepted-only v20/v21 compatibility and exact historical artifact identities; normal persisted candidate and Market drill-down remain next.
- [x] first normal v23 `tvMm` attempt 110 exposed inherited old-plan persistence mismatch after generation; no artifact was created. Versioned v23 persistence now uses its exact model-facing plan, retained full-result replay and 740 strict-warning tests pass, and the public corpus verifies. See the v23 promotion reconciliation.
- [x] normal v23 `tvMm` artifact 50 persisted with 25 requirements and 11 duties; its complete payload exactly matched the independently source-reviewed result. Explicit semantic review accepted artifact 50, and the public corpus now has 410 known jobs and 6 accepted English P1.6 artifacts.
- [x] a bounded Market run 3 recorded 53 current search-page candidates, 16 new IDs, zero new acquisition/translation/analysis, and immutable snapshot/profile 3 with zero members; all prior members were refresh-due under the 168-hour rule while refresh budget was zero. No semantic demand was inferred as zero.
- [x] target-run candidate scope now carries forward the latest nonempty snapshot's qualified source IDs in addition to current discovery, records both counts separately, and still applies source freshness/currentness and bounded membership checks; 741 strict-warning tests and 410-job corpus verification pass.
- [~] run one bounded source refresh with the unchanged 168-hour rule, then freeze accepted-semantic snapshot/profile and verify CLI/browser drill-down plus integrity/privacy.
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
public/current stays v21/v5 with accepted-only v20 compatibility
→ post-alias v22 evaluation CLOSED / semantically rejected
→ observed unsafe ontology abstention repaired offline; preferred proof-of-work gap remains
→ representative offline claim/section evidence and versioned design decision NEXT
→ no automatic retry, persisted generation, promotion, or vacancy/model switch
→ accepted-current semantic evidence + immutable snapshot/profile + live drill-down still required
→ preserve Market I7 HOLD
```

### Final verification checkpoint — 2026-09-22

- Prior-exposure guard: 687 strict-warning tests, Ruff, public corpus verification, and pushed implementation CI passed (`9c277f1`).
- One non-persistent v21 tvMm result passed bounded manual source review (22 requirements, 11 duties); SQLite unchanged and integrity/FK checks clean.
- Pre-promotion final testing completed with v21 still experimental and public v20/v5 unchanged at that checkpoint. That checkpoint is now superseded by the v21 promotion reconciliation below; the retained evaluation evidence remains historical input.


### P1.6 v21 promotion reconciliation — 2026-09-22

- [x] public/current English routing now uses `job-analysis-english-v21 / job-analysis-v5`.
- [x] accepted v20/v5 artifacts remain reusable only when already semantically accepted.
- [x] pending/rejected v20 candidates do not satisfy v21 currentness.
- [x] exact reused artifact prompt/schema identity is carried through the result and surfaced by CLI compatibility output.
- [x] promotion regression coverage added for accepted-v20 reuse and pending-v20 rejection.
- [x] CI run 1294 / `35753325406`: entrypoint smoke PASS, Ruff PASS, 690 pytest PASS, 690 warnings-as-errors PASS.
- [~] I7 accepted-semantic live closure remains the only active first-slice gate.
