# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-10-10  
**Active branch:** `main`  
**Current state:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md` plus the newer dated closure/status records under `docs/working-memory/`  
**Market plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Current product gate:** MARKET I1-I7 ACCEPTED / BOUNDED FIRST SLICE CLOSED; ROLE-FAMILY REPORT R1-R4 ACCEPTED / CLOSED  
**Active increment:** Phase-2 semantic direction reconciliation. No P2.2C responsibility-family promotion, P2.2D stable role-archetype promotion, P2.3 capability-profile implementation, or Market v2 expansion is authorized until the next bounded semantic increment is explicitly selected and planned.

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
- [x] Candidate interpretation V6 CLOSED / accepted for bounded reporting.
- [x] Durable `RoleFamilyIntelligenceReport` R1-R4 ACCEPTED / CLOSED.

Do not reopen accepted historical work without a repeatable current contradiction.

Key closure records:

- `docs/working-memory/2026-09-26_MARKET_I7_FINAL_LOCAL_ACCEPTANCE.md`
- `docs/working-memory/2026-09-26_MARKET_I7_TARGET_COVERAGE_FOLLOWUP.md`
- `docs/working-memory/2026-10-10_MARKET_R4_FINAL_LOCAL_ACCEPTANCE.md`

Historical HOLD-era execution remains evidence only and does not control current routing.

---

## B. RoleFamilyIntelligenceReport persistence — ACCEPTED / CLOSED

Controlling design/history:

`docs/working-memory/2026-10-03_ROLE_FAMILY_INTELLIGENCE_REPORT_PERSISTENCE_PLAN.md`

Final acceptance:

`docs/working-memory/2026-10-10_MARKET_R4_FINAL_LOCAL_ACCEPTANCE.md`

Accepted precursor:

- [x] Candidate V6 real snapshot-15 report reviewed and accepted for bounded reporting.
- [x] Review artifact: `docs/working-memory/review-artifacts/2026-10-03_snapshot15_candidate_report_v6.html`.
- [x] Candidate experiment CLOSED; no V7 authorized.
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
- [x] Tier-1 deterministic tests accepted.
- [x] CI `37217405526`: Ruff PASS; 825 tests PASS; 825 warnings-as-errors tests PASS.

Acceptance boundary:

```text
persisted/reviewed analytical artifact
!= promoted role-family taxonomy
```

R2 — shared service + V6 integration: ACCEPTED / CLOSED

- [x] One shared `market_role_family_report_service.py` owner.
- [x] Exact normalized candidate input and semantic generation identity derived before LM Studio call.
- [x] Ordinary exact reuse records `reused` and skips generation.
- [x] Explicit regeneration may persist another immutable artifact.
- [x] Generation failure records `failed` and creates no report artifact.
- [x] Generated identity mismatch fails closed before persistence.
- [x] Request/raw-response audit payloads are persisted privately without a second semantic path.
- [x] Review/effective-state/latest-accepted operations use the same service.
- [x] CI `37220490754`: Ruff PASS; 830 tests PASS; 830 warnings-as-errors tests PASS.

R3 — shared browser + CLI workflow + bounded Market UX redesign: ACCEPTED / CLOSED

- [x] Browser in-process candidate-report ownership removed.
- [x] Browser uses durable report IDs/history/review state via the shared service.
- [x] Ordinary generate/reuse and explicit fresh regeneration are visibly distinct.
- [x] Durable report survives fresh app instance/restart.
- [x] Browser review actions append `accepted_for_bounded_use | rejected` events.
- [x] CLI `role-report list|generate|show|review` uses the same service/report IDs.
- [x] Browser and CLI agree on persisted report ID/payload/effective review state.
- [x] Private request/raw model response remain outside ordinary browser/CLI presentation.
- [x] Market workspace uses guided target → scope → refresh → intelligence flow and progressive disclosure.
- [x] Snapshot/report presentation prioritizes decision-relevant findings while preserving exact evidence/provenance drill-down.
- [x] Closure record: `docs/working-memory/2026-10-04_MARKET_R3_DURABLE_WORKFLOW_AND_UX_CLOSURE.md`.
- [x] CI `37223301900`: Ruff PASS; 830 tests PASS; 830 warnings-as-errors tests PASS.

R4 — bounded real-local acceptance: PASS / CLOSED

- [x] Maintainer SQLite backed up before R4; pre-existing local corpus modifications were fingerprinted rather than reset.
- [x] LM Studio endpoint `http://127.0.0.1:18080/v1` and `gemma-4-e4b-it-ud` verified.
- [x] Snapshot 15 remained ten members / six accepted-semantic core postings with expected P1.6 identities.
- [x] First real artifact #1 exposed incomplete recovery-policy generation identity and remained immutable/pending.
- [x] Recovery-policy identity defect repaired and regression-tested; CI `38068073900`: Ruff PASS; 830 tests PASS; 830 warnings-as-errors PASS.
- [x] Repaired ordinary generation persisted artifact #2 with recovery identity: initial 2048, multiplier 4, ceiling 32768; successful request 8192.
- [x] Artifact #2 result: six source postings, 175 available claims, 27 cited claims, four work clusters, one multi-posting subfamily hypothesis, two singleton specialty/outlier candidates, zero integrity rejections.
- [x] Full app restart preserved report #2 and browser/CLI agreed on the durable artifact.
- [x] Owner accepted report #2 for bounded analytical use; artifact #1 remains pending historical evidence.
- [x] Exact ordinary reuse produced attempt `(3, reused, artifact 2)` and report count remained two; no artifact #3 was generated.
- [x] Final SQLite `integrity_check = ok` and `foreign_key_check = []`.
- [x] Snapshot 15 remained ten members / six accepted-semantic members after R4.
- [x] Pre-existing corpus files remained byte-identical to their pre-R4 SHA-256 baseline.
- [x] Final acceptance/disposition recorded in `docs/working-memory/2026-10-10_MARKET_R4_FINAL_LOCAL_ACCEPTANCE.md`.

Final boundary:

```text
RoleFamilyIntelligenceReport persistence program = ACCEPTED / CLOSED
reviewed report = useful bounded analytical artifact
reviewed report != canonical taxonomy
```

---

## C. Active Phase-2 semantic direction reconciliation

The report-infrastructure program is closed. Do not create R5 or continue report/prompt polishing merely because model wording can vary.

Current strategic candidates from the controlling implementation plan:

```text
P2.2  source responsibility → canonical responsibility → responsibility family → evidence-derived role archetype
P2.3  corpus-scale capability requirement profiles
P2.4  Market v2 over reviewed/current canonical mappings/profiles
```

Before implementation, reconcile:

- [ ] what accepted P2.1 Canonical Registry and P2.2A Job Work Intelligence already provide;
- [ ] why P2.2B-B1 ended NO-PROMOTION / DEFER and which prerequisite was missing;
- [ ] what the accepted Market snapshot/report evidence now changes, if anything, for that promotion boundary;
- [ ] whether the next useful bounded increment should target responsibilities/deliverables, capability profiles, or another prerequisite;
- [ ] exact authority boundary: candidate analytical interpretation vs reviewed canonical correspondence vs promoted reusable taxonomy;
- [ ] representative evidence/sample required before any P2.2C/P2.2D promotion;
- [ ] how the accepted durable Market report may inform investigation without becoming taxonomy authority;
- [ ] one explicit next plan/acceptance gate before code implementation.

No semantic implementation is authorized until this reconciliation selects it.

---

## D. Permanent Market / authority invariants

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
- [x] reviewed durable Market interpretation remains separate from canonical taxonomy authority.

---

## E. Explicitly deferred / not authorized

- [-] P2.2C promoted responsibility families without representative reviewed evidence and explicit reauthorization.
- [-] P2.2D stable promoted role archetypes without representative reviewed evidence and explicit reauthorization.
- [-] P1.6 auto-acceptance.
- [-] Capability/Work as mandatory Market gates.
- [-] automatic repost/new-ID collapse without real evidence.
- [-] broad-market trend / emerging / forecasting claims before comparable snapshots.
- [-] Market → You / personal readiness, gaps or scoring before reviewed personal evidence.
- [-] Market publication to `corpus/`.
- [-] generic vector/RAG/graph/autonomous-agent/source-plugin infrastructure without demonstrated need.

---

## F. Parallel portfolio/release

- [x] MIT license complete.
- [ ] GitHub description/topics.
- [ ] real browser screenshots + privacy review.
- [ ] intentional `v0.1.0` tag/release.
- [ ] owner mastery verification.

Portfolio work does not broaden the active semantic authorization.

---

## Exact next action

```text
Phase-2 semantic direction reconciliation
→ re-read P2.1 / P2.2A accepted boundaries and P2.2B-B1 no-promotion evidence
→ compare those prerequisites with the newly accepted Market I1-I7 + durable reviewed report evidence
→ choose the next bounded semantic responsibility
→ define promotion/acceptance gate and representative evidence
→ write/update the focused plan
→ only then authorize implementation
```
