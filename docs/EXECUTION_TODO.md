# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-10-04  
**Active branch:** `main`  
**Current state:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`  
**Market plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Current product gate:** MARKET I1-I7 ACCEPTED / BOUNDED FIRST SLICE CLOSED  
**Active increment:** `RoleFamilyIntelligenceReport` R2 — shared service + accepted V6 generator integration. R1 domain/persistence is accepted/closed; browser/CLI remain blocked until R2 passes.

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
- [x] Market foundation investigation PASS.
- [x] Market I1-I7 ACCEPTED / bounded first vertical slice CLOSED.
- [x] Same-target coverage follow-up complete in snapshots 14-15: ten qualified members, six core, six accepted-current P1.6.
- [x] Current English P1.6 generation contract: `job-analysis-english-v30 / job-analysis-v5`.
- [x] Public corpus current baseline: 420 jobs, 51 parsed details, 29 English projections, 11 accepted English P1.6, 5 Capability artifacts.

Do not reopen accepted historical work without a repeatable current contradiction.

Key closure records:

- `docs/working-memory/2026-09-26_MARKET_I7_FINAL_LOCAL_ACCEPTANCE.md`
- `docs/working-memory/2026-09-26_MARKET_I7_TARGET_COVERAGE_FOLLOWUP.md`

Historical HOLD-era execution remains evidence only and does not control current routing.

---

## B. RoleFamilyIntelligenceReport persistence — ACTIVE

Controlling design:

`docs/working-memory/2026-10-03_ROLE_FAMILY_INTELLIGENCE_REPORT_PERSISTENCE_PLAN.md`

Accepted precursor:

- [x] Candidate V6 real snapshot-15 report reviewed and accepted for bounded reporting.
- [x] Review artifact: `docs/working-memory/review-artifacts/2026-10-03_snapshot15_candidate_report_v6.html`.
- [x] V6 acceptance: 175 available claims, 49 unique cited claims, four work clusters, one multi-posting subfamily hypothesis, one singleton specialty/outlier, zero `C*` leakage, zero integrity rejections.
- [x] Candidate experiment CLOSED; no V7 authorized.
- [x] Durable report persistence AUTHORIZED.
- [x] Persistence envelope: `market-role-family-intelligence-report-v1`.
- [x] Initial generation dependency: `market-role-family-candidate-v6 / market-role-family-candidate-prompt-v6`.
- [x] Review contract: `market-role-family-report-review-v1`.
- [x] Report remains interpretive: reviewed report != employer fact != canonical taxonomy != broad-market prevalence.
- [x] Market report state remains local/private and is not public-corpus material by default.

R1 — domain + persistence: ACCEPTED / CLOSED

- [x] Typed report / attempt / review records added in `market_models.py`.
- [x] Dedicated local SQLite owner: `market_role_family_report_store.py`.
- [x] Completed normalized reports persist immutably.
- [x] Canonical input/generation/report SHA-256 fingerprints are application-owned.
- [x] Terminal attempts are append-only: `completed | failed | reused`.
- [x] Reviews are append-only: `accepted_for_bounded_use | rejected`; no event = pending.
- [x] Report, attempt, and review update/delete triggers enforce history immutability.
- [x] Exact generation-fingerprint lookup returns newest reusable artifact; explicit regeneration may persist another immutable artifact under the same generation fingerprint.
- [x] Persisted generation/report fingerprints are verified on read and corruption fails closed.
- [x] Effective review state and newest effectively accepted report selection are implemented.
- [x] Tier-1 tests cover canonical hashing, identity validation, immutability, explicit regeneration, exact reuse, terminal attempts, failed-attempt no-report behavior, append-only review reversal/history, accepted selection, generation mismatch, corruption detection, and no upstream Market/P1.6 mutation.
- [x] CI `37217405526`: Ruff PASS; 825 tests PASS; 825 warnings-as-errors tests PASS.

Acceptance boundary:

```text
persisted/reviewed analytical artifact
!= promoted role-family taxonomy
```

R2 — shared service + V6 integration:

- [ ] Add one shared `market_role_family_report_service.py` owner.
- [ ] Derive the exact normalized candidate input used for the V6 generation fingerprint.
- [ ] On ordinary generation, reuse an exact existing report and record a `reused` attempt.
- [ ] On explicit regeneration, call the accepted V6 generator and persist a new immutable report even for the same generation fingerprint.
- [ ] On successful new generation, record report then `completed` attempt.
- [ ] On generation failure, record `failed` attempt and create no report artifact.
- [ ] Persist exact normalized report plus request/raw-response audit data without introducing a second semantic path.
- [ ] Expose review append/effective-state operations through the same service.
- [ ] Add deterministic service tests with the candidate generator stubbed; normal CI must not require LM Studio.
- [ ] Keep R3 browser/CLI and R4 real-local acceptance blocked until R2 passes.

---

## C. Permanent Market / authority invariants

- [x] target identity is separate from immutable target-definition meaning.
- [x] search/acquisition envelope != target membership truth.
- [x] source-level membership is `core_match / adjacent_match / uncertain / excluded`.
- [x] target-scoped work does not spill into unrelated backlog.
- [x] `uncertain` is a successful semantic outcome.
- [x] adjacent/uncertain/excluded never silently enter the primary core denominator.
- [x] missing/pending/failed/rejected P1.6 never means zero demand.
- [x] only accepted-current P1.6 contributes to strong semantic statistics.
- [x] snapshot members reference exact dependencies.
- [x] snapshots and aggregate profiles remain immutable historical authority.
- [x] first-slice denominator remains `qualified source postings`, not unproven unique demand.
- [x] numeric counts are deterministic application responsibilities.
- [x] browser and CLI share state/service owners.
- [x] Market state remains local/private by default.

---

## D. Explicitly deferred / not authorized

- [-] P2.2C promoted responsibility families without representative reviewed evidence.
- [-] P2.2D stable promoted role archetypes without representative reviewed evidence.
- [-] P1.6 auto-acceptance.
- [-] Capability/Work as mandatory Market gates.
- [-] automatic repost/new-ID collapse without real evidence.
- [-] broad-market trend / emerging / forecasting claims before comparable snapshots.
- [-] Market → You / personal readiness, gaps or scoring before reviewed personal evidence.
- [-] Market publication to `corpus/`.
- [-] generic vector/RAG/graph/autonomous-agent/source-plugin infrastructure without demonstrated need.

---

## E. Parallel portfolio/release

- [x] MIT license complete.
- [ ] GitHub description/topics.
- [ ] real browser screenshots + privacy review.
- [ ] intentional `v0.1.0` tag/release.
- [ ] owner mastery verification.

Portfolio work does not broaden the active semantic authorization.

---

## Exact next action

```text
R2 shared service + V6 integration
→ exact candidate-input/generation identity derivation
→ ordinary exact reuse + reused attempt
→ explicit regeneration + persisted report + completed attempt
→ failure attempt without report
→ review/effective-state facade
→ deterministic service tests
→ only after R2 acceptance authorize R3 browser/CLI
```
