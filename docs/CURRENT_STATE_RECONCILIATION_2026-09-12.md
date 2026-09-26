# JobHunter Current-State Reconciliation — 2026-09-12

**Status:** CURRENT / CONTROLLING STATUS-ONLY OVERLAY  
**Last reconciled:** 2026-09-26
**Branch:** `main`  
**Scope:** Present-tense project state and execution routing.  
**Supersedes for current-state reading:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-05.md`

## 1. Current authoritative operating state

```text
Phase 1                              CLOSED / ACCEPTED
P2.1 Canonical Registry             CLOSED / ACCEPTED
P2.2A Job Work Intelligence         CLOSED / ACCEPTED
P2.2B-B1                            CLOSED / NO-PROMOTION / DEFER
P2.2C promoted responsibility       NOT ACTIVE / NOT AUTHORIZED
P2.2D stable role archetypes        LATER / NOT AUTHORIZED
Blueprint v6                        EXPERIMENTAL / HISTORICAL / NON-AUTHORITATIVE

Market foundation investigation     PASS / COMPLETE
Market I1 domain + persistence      ACCEPTED / CLOSED
Market I2 affected-work planning    ACCEPTED / CLOSED
Market I3 membership qualification ACCEPTED / CLOSED
Market I4 snapshot construction     ACCEPTED / CLOSED
Market I5 aggregate profile         ACCEPTED / CLOSED
Market I6 browser + CLI workflow    ACCEPTED / CLOSED
Market I7 real local acceptance     PASS / CLOSED FOR BOUNDED SCOPE
First Market vertical slice         ACCEPTED / CLOSED FOR BOUNDED SCOPE
Semantic subfamily/report synthesis DEFERRED FROM FIRST SLICE
Market → You                        LATER / NOT AUTHORIZED

Portfolio / release                 PARALLEL
MIT license                         COMPLETE
GitHub metadata/screenshots/release/owner mastery  PENDING
```

Current first-slice contracts:

```text
parser:                       jobinja-detail-v2
translation:                  english-projection-v2 / lm-studio-translation-v2
English P1.6:                 job-analysis-english-v23 / job-analysis-v5
Capability:                   job-capability-intelligence-v9 / job-capability-intelligence-v5
Canonical Registry:           jobhunter-canonical-concept-registry-v1
Work Intelligence:            job-work-intelligence-v2 / job-work-intelligence-v2.0
Market membership:            market-membership-v1 / market-membership-v1.0
Market snapshot:              market-corpus-snapshot-v1
Market aggregate persistence: market-aggregate-profile-v1
Public Corpus:                jobhunter-public-corpus-v1
```

Repository-safe public corpus baseline remains:

```text
known/discovered Jobinja jobs: 410
fetched/parsed detail jobs:      51
current English projections:     27
accepted/current English P1.6:    6
accepted/current Capability:      5
```

### P1.6 v21 promotion reconciliation — 2026-09-22 (historical)

English P1.6 v21/v5 became the public/current generation and review contract at this checkpoint. The five accepted
public anchors remain their exact v20/v5 artifacts and are accepted-only compatibility-current;
they are not regenerated merely to change prompt identity. Pending/rejected v20 candidates do not
satisfy v21 currentness.

The promotion boundary preserves exact lineage in CLI results, and regression coverage proves
accepted v20 reuse while rejecting pending-v20 fallback. Repository CI run 1294
(`35753325406`) passed entrypoint smoke, Ruff, 690 tests, and 690 warnings-as-errors tests.

This promotion did not close Market I7. I7 remains HOLD until a genuinely valid current candidate
for a core member is persisted, explicitly accepted, frozen into a new snapshot/profile, and
verified through the real semantic CLI/browser drill-down plus post-mutation integrity/privacy
checks.

### P1.6 v23 promotion and accepted core analysis — 2026-09-26

V23/v5 is the current English generation/review contract after complete source review
of one non-persistent `tvMm` result. It adds explicit proof-of-work preference coverage
and preserves the v22 fail-closed claim-wording boundary. The five accepted v20/v5
anchors remain accepted-only compatibility-current with exact identities; any accepted
v21/v5 artifacts are also compatibility-current. Pending/rejected prior-contract
candidates do not become v23 current. Normal persisted `tvMm` artifact 50 exactly
matched the complete source-reviewed result and was explicitly accepted. I7 remains
HOLD at that checkpoint. Runs 4-6 subsequently froze the artifact in new Market
snapshots/profiles, verified CLI/rendered-browser drill-down and reuse, and closed I7
with bounded PASS. See `docs/working-memory/2026-09-26_MARKET_I7_FINAL_LOCAL_ACCEPTANCE.md`.

---

## 2. Closed historical frontier

P2.2B-B1 remains **CLOSED / NO-PROMOTION / DEFER**.

Final evidence:

`docs/working-memory/2026-09-14_P2_2B_B1_EXTRACTION_RECOVERY.md`

No responsibility concept or mappings were created. Do not reopen B1 merely to manufacture a promotion.

---

## 3. Market foundation and accepted increments

Foundation decision:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

Decision:

```text
FOUNDATION INVESTIGATION: PASS
FIRST VERTICAL SLICE: AUTHORIZED
```

Accepted implementation sequence:

```text
I1  domain + SQLite persistence                 ACCEPTED
I2  target-scoped source/affected work          ACCEPTED
I3  membership qualification                    ACCEPTED
I4  immutable snapshot construction             ACCEPTED
I5  deterministic aggregate profile             ACCEPTED
I6  browser + CLI thin workflow                 ACCEPTED
I7  bounded real local acceptance               PASS / CLOSED
```

Latest I6 acceptance owner:

`docs/working-memory/2026-09-17_MARKET_I6_BROWSER_CLI_WORKFLOW_IMPLEMENTATION.md`

Prepared I7 execution protocol:

`docs/working-memory/2026-09-18_MARKET_I7_LOCAL_ACCEPTANCE_PROTOCOL.md`

Earlier accepted Market evidence remains applicable:

```text
docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md
docs/working-memory/2026-09-17_MARKET_I3_MEMBERSHIP_QUALIFICATION_IMPLEMENTATION.md
```

I3 real-model evaluation is preserved at:

`docs/experiments/2026-09-17_market-i3-real-model-acceptance/`

Its clarified-target 8/8 result is post-hoc boundary calibration, not a general model-accuracy benchmark.

---

## 4. Accepted I6 product path

The shared first-slice workflow now exists in repository code:

```text
TargetMarket
→ immutable TargetMarketDefinitionVersion
→ exact target acquisition envelope
→ bounded target-only Jobinja discovery
→ bounded I2 source/translation/P1.6 affected work
→ bounded I3 membership qualification
→ terminal MarketResearchRun + partial-success ledger
→ I4 immutable snapshot
→ I5 deterministic aggregate profile
→ shared browser/CLI inspection
```

Browser primary surface:

```text
/market/targets
```

The older `/market` current-corpus aggregate page remains available as a legacy view. It is not the target-scoped historical authority.

CLI surface:

```text
jobhunter market target list
jobhunter market target create
jobhunter market definition create TARGET_ID
jobhunter market show
jobhunter market preview DEFINITION_ID
jobhunter market run DEFINITION_ID
jobhunter market run-show RUN_ID
jobhunter market snapshot-show SNAPSHOT_ID
```

I6 uses the existing `WebOperationManager` one-mutable-operation boundary. Browser and CLI use the same Market workspace/services/state.

Market target/definition/membership/run/snapshot/profile tables remain local/private and are not exported to the repository public corpus by default.

---

## 5. Permanent first-slice semantic/denominator boundaries

- acquisition/search vocabulary is not target-membership truth;
- target meaning is versioned and immutable;
- target search catalog version is locked to the definition meaning;
- `core_match / adjacent_match / uncertain / excluded` remain distinct;
- only core enters the primary corpus;
- accepted P1.6 is not required for source-level membership;
- accepted-current P1.6 is required for strong P1.6-backed prevalence statistics;
- pending/missing/failed/rejected P1.6 never means zero demand;
- Capability and Work are optional enrichments, not Market gates;
- automatic repost/new-ID collapse remains deferred;
- denominator language remains `qualified source postings`;
- no model-authored counts or opaque composite scores;
- semantic subfamily synthesis, trends, forecasts and personal scoring remain outside this slice.

---

## 6. I6 acceptance evidence

Accepted technical head before status reconciliation:

```text
4076bb731b3485aa99fbdf63bf73a96dc7a5773b
```

CI:

```text
run 1210 / 35263630011
installed entrypoint smoke     PASS
Ruff                           PASS
pytest                         632 passed
pytest -W error                632 passed
conclusion                     SUCCESS
```

During integration, repository tests caught an accidental attempted drift in accepted I5 aggregate semantics. The exact accepted I5 implementation was restored before I6 acceptance. Current I6 composes I5 directly and does not redefine the aggregate contract.

---

## 7. I7 final acceptance and historical HOLD evidence

**Current decision:** I7 PASS for the bounded first vertical slice on 2026-09-26.
Runs 4-6 preserved six qualified core source postings, one accepted-semantic core
posting with frozen artifact-50 requirement/responsibility evidence, and exact
source-versus-semantic denominators. Run 6 required no source refresh, translation,
or analysis; remaining budget-limited work stayed explicit. CLI and rendered browser
read paths, immutable history, SQLite integrity and corpus privacy passed. The sample
does not support broad-market prevalence. Final authority:
`docs/working-memory/2026-09-26_MARKET_I7_FINAL_LOCAL_ACCEPTANCE.md`.

The rest of this section is the historical HOLD trail, retained to explain repairs.
Its former present-tense next-work statements are superseded by the final decision.

I7 real-local execution has occurred. Sanitized evidence and the continuing decision record are at:

`docs/working-memory/2026-09-18_MARKET_I7_REAL_LOCAL_ACCEPTANCE_HOLD.md`

Current closed evidence:

```text
target definition fingerprint      RECOVERED
run-2 snapshot/profile             RECOVERED
snapshot-1 historical immutability VERIFIED
post-run SQLite integrity/FKs      VERIFIED
public-corpus privacy boundary     VERIFIED
artifact 48 semantic review        REJECTED
historical pending-rejection FK    REPAIRED
accepted public anchors            NON-REGRESSED
latest strict suite                639 passed
latest code CI                     35468478422 SUCCESS (94a14a1)
```

The historical-pending rejection defect is fixed by retaining the rejected artifact payload/ID when
an immutable Market snapshot references it while excluding that row from current/reuse selection.
Operational rejection of `t7ck` artifact 48 succeeded with snapshot/member/profile history unchanged.

The follow-up also fixed two general P1.6 evidence-preparation defects: headingless qualification text
between detected lists is retained, and implicit-duty detection is restricted to same-sentence infinitive
language without turning ability/capacity/experience qualifications into duties. All five accepted public
anchors retained identical helper plans.

I7 remains **HOLD** for one reason: no current target-core posting has yet produced a genuinely valid
accepted-current P1.6 artifact in this live target, so the real accepted-semantic aggregate and frozen
requirement/responsibility drill-down still have not been exercised end to end.

The selected `tvMm` follow-up began on 2026-09-20 local time. Attempt 106 exposed
a v20 structured-skill prompt/payload contradiction, which was repaired. The one
post-repair attempt 107 produced artifact 49; complete review rejected it for
borrowed familiarity depth and a candidate-versus-AI-system subject error. V20
now fails closed for repeated identical depth markers, with offline regression and
retained raw-response replay. No accepted-semantic core member resulted. Market
history and public-corpus privacy remained intact.

Further read-only inspection found the remaining subject error in a broad
requirement coverage span that crosses company goals and application text. Four
such spans appear across two of 27 current English projections; the current
`allow_exclusion` path already permits correct semantic rejection. There is not
enough representative evidence to promote a deterministic cutoff. I7 stays HOLD
without another model attempt or a substitute vacancy.

A subsequent bounded repair addressed only two source-backed span defects: a
dependent `; to ...` clause retains its explicit subject, and `How to Apply:` ends
requirement-section coverage. The five accepted anchor plans were unchanged in
read-only comparison. This improves future evidence preparation but supplies no
new accepted P1.6 core member, so I7 remains HOLD.

The one bounded post-span-repair live check, `tvMm` attempt 108, failed after its
allowed retry on mixed-depth broad citations. No candidate was created. The depth guard was
not relaxed; all seven Market tables matched the pre-run backup, and SQLite
integrity and foreign-key checks passed. This check is closed with I7 still HOLD.

Exact-source replay then distinguished omitted applicable familiarity from correct
null depth on neighboring experience claims; v20's shared evidence reference
cannot prove the item scope. Eight of fourteen mixed-marker corpus references also
carry shared preferred context. A separate repeated-marker validation gap was
repaired without changing accepted anchors. The next implementation needs a
versioned candidate that keeps exact item evidence and parent coverage/strength
context separately, with offline review before another bounded live evaluation.

Current record: `docs/working-memory/2026-09-20_MARKET_I7_TVMM_BOUNDED_CLOSURE.md`.

Historical next responsibility (reconciled 2026-09-24; superseded by v23 above):

```text
v21/v5 was public/current at this checkpoint; accepted v20 anchors retained compatibility
→ persisted v21 tvMm attempt CLOSED / failed ontology validation
→ isolated v22 candidate and evidence-alias repair implemented
→ exact-head CI 35764994184 on effa861 passed all quality gates
→ authorized post-repair evaluation EXECUTED / SEMANTICALLY REJECTED
→ unsafe type-only abstention repaired offline; preferred proof-of-work gap remains
→ representative offline evidence and versioned design decision next; no new model call
→ live accepted-current persistence + snapshot/profile + CLI/browser proof still required
```

Current evaluation closure and next-work owner:
`docs/working-memory/2026-09-24_P16_V22_POST_ALIAS_EVALUATION_CLOSURE.md`.
Earlier v20/v21 implementation steps above are historical evidence, not new execution instructions.

No full acquisition rerun is required merely to obtain this semantic evidence.

---

## 8. I7 stop lines

During I7 do not:

- broaden into semantic role-subfamily synthesis;
- add trends/emerging/forecasting;
- add Market → You/personal readiness scoring;
- auto-accept P1.6;
- make Capability or Work mandatory;
- invent repost similarity thresholds;
- publish Market local tables to `corpus/`;
- reopen B1/P2.2C/P2.2D;
- introduce a second workflow/persistence/currentness stack;
- weaken deterministic tests merely to accommodate a live provider result.

If real evidence exposes a concrete correctness defect, repair only the owning boundary and rerun the relevant acceptance checks.

---

## 9. Current routing

```text
B1 CLOSED / DEFER
→ Market foundation PASS
→ I1-I6 ACCEPTED
→ v23/v5 artifact 50 explicitly accepted and frozen in Market snapshots 4-6
→ I7 PASS / bounded first Market vertical slice CLOSED
→ choose the next scoped increment under the Market plan
```

For present-tense status use this file together with `docs/EXECUTION_TODO.md` and `docs/WORKING_MEMORY.md`. Older dated `NEXT` wording is historical when it conflicts with this overlay.
