# JobHunter Current-State Reconciliation — 2026-10-10

**Status:** CURRENT / CONTROLLING STATUS-ONLY OVERLAY  
**Date:** 2026-10-10
**Last reconciled:** 2026-11-18
**Branch:** `main` — B2/B3 candidate code integrated via clean fast-forward; production routing unchanged
**Scope:** Present-tense project state and execution routing.  
**Supersedes for current-state reading:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`

This file changes present-tense status/routing only. It does not replace durable product, domain, source, architecture, roadmap, implementation-plan, or phase-plan semantics.

## November 18 B2/B3 integration into main — latest status overlay

The repository owner requested direct-main development. All 13 B2/B3 commits were applied in ancestry order via two conflict-free fast-forwards, preserving B2 `97d5fda` and B3 `939f99f`. GitHub Actions for both feature heads passed. Candidate modules, tests and safe scorecards are committed to `main`; private source/model request-response data remains ignored locally.

**Engineering integration does not imply semantic promotion.** Current English v30/v5 and original v9/v4 are still the active production routes; Capability, Work, Registry, Market and persistence authority remain unchanged. B2 full semantic generalization and B5 unseen generalization remain unestablished. B4 source-qualified job-level candidate briefs are next, with B6 promotion/rollback still separately gated.

Integration handoff: `docs/working-memory/2026-11-18_B2_B3_MAIN_INTEGRATION_AND_B4_HANDOFF.md`. The following B3 entry is pre-integration historical context.

## November 18 B3 bounded source-bound translation milestone — historical pre-integration overlay

The local checkout is on feature/p16-b3-source-bound-item-translation-2026-11-18, based on the B2 research branch at 97d5fda. The B2 PR #20 remains draft and unmerged. Main and all accepted P1.6/v30/v9, Capability, Work, Registry and Market records remain unchanged.

B3 selection and execution completed on the four frozen, previously exposed B0 ads: 78 source items; 64 eligible top-level items (63 Persian translation candidates and one native-English identity); 12 context-only and two generic application instructions excluded; 12 nested eligibility leaves retained as source subspans without duplicate model calls or separate target offsets. Local gemma-4-e2b-it translation-v2 completed 63 primary requests plus one evidence-justified corrective request (64/64 total), with zero retries and zero truncation recoveries. All 64 request/response hash pairs were verified; all four B1-compatible bundles pass.

Assistant review covered all 63 Persian translations on this exposed cohort. One material primary mistranslation of a personal trait was retained for audit, corrected with the single allowed corrective candidate, and selected with a documented terminology normalization. No material meaning-changing issue remains in the selected translations for these four ads. This is not independent blind human review or unseen generalization. Twelve nested child target offsets remain not established.

Local quality: 1,063 passed with warnings as errors; Ruff lint, pip dependency check, compileall, and targeted formatting checks passed. No production database write, accepted fact promotion, downstream authority, or public route change occurred. Full-repository format-check baseline still has unrelated pre-existing deviations; no global reformat was applied. B3 final audit: ignored/private data/local-acceptance/p16-stage-b3-2026-11-18/primary-v1/B3_FINAL_AUDIT.json; safe decision: docs/working-memory/2026-11-18_P16_B3_SOURCE_BOUND_TRANSLATION_MILESTONE.md.

Next: B4 useful non-authoritative job-understanding brief and isolated comparison against unchanged v30/v9 on the same frozen sources. B2 full semantic generalization, B5 unseen-cohort generalization and B6 promotion remain NOT ESTABLISHED. B3 GitHub CI and PR #21 are pending; PR #20 remains draft.


## November 16 B2 native model-suggested item references — previous research overlay

A fixed native Gemma `reasoning: off` source-ref prompt on four **already
exposed** original-source cases returned 4/4 structured results: 75 model
claims, 73 mechanically valid suggested item IDs, two unlinked claims,
25 heuristic source-category/obligation disagreement signals. This proves
**citation presence only**, not Persian employer-fact semantic entailment.

Reapplying 12 previously selected assistant/exposed diagnostic checks
produced v4 5 pass/4 partial/3 fail versus v3 6/2/4; formats and prompts
differ and neither is an independent accuracy rate. Important errors
persist: invented pentest assigned duties, Kaspersky/customer-experience
strength overclaims, and wrongly represented eligibility alternatives.
Technical work-implied capabilities were also partially lost. Relative
to v3, model output count dropped 85 to 75 while four-request observed
latency increased 24.290s to 33.606s and output tokens 1,627 to 2,227.

B2 **OPEN_NO_PROMOTION**, PR #20 draft and main/current P1.6 v30/v9,
B1, translation v2, Capability/Work/Registry/Market remain unaffected.
Stop more prompt-only reference tuning; next is a separate B2 strategy
decision, not an authorized production rollout or unseen-cohort use.

Decision: `docs/working-memory/2026-11-16_P16_B2_NATIVE_SOURCE_REFERENCES_MIXED_SEMANTIC_RESULT.md`.

## November 16 B2 advisory claim grounding — previous diagnostic overlay

Draft PR #20 adds a pure, inactive, source-item-linked advisory claim
reconciler. Valid Stage A anchors prove provenance **location** and
source-version integrity only; associated original-source item category and
model interpretation remain separate, unreviewed candidate semantics.

On the same four exposed native-v3 jobs (no additional model/source calls):
85 model-generated claims, 14 retrospective assistant-selected exact-source
item links, 9 source-candidate discrepancy signals, and 71 unlinked claims
that remain UNKNOWN, not false. Five linked claims remain semantically
unreviewed. The 9 signals are not independently confirmed model errors.
The saved model outputs contain no original-item citations and no
automatic bilingual alignment is demonstrated.

B2 full semantic gate **OPEN_NO_PROMOTION**; draft PR #20 unmerged,
production v30/v9 and all accepted downstream facts unchanged.
Local full suite: 1030 passed with warnings as errors; Ruff and pip check
passed. Next decide a strictly bounded source-link output interface only
if its accuracy/usefulness/cost merits an additional experimental trial.

Decision: `docs/working-memory/2026-11-16_P16_B2_ADVISORY_SOURCE_CLAIM_GROUNDING_INCREMENT.md`.

## November 17 B2 bounded source-first candidate milestone — PASS for exposed scope

The deterministic candidate-only source inventory and B1 projection now pass the bounded four-ad exposed-cohort engineering milestone. Recomputed from the exact frozen B0 source DB: **78 original items, 53 board refs, 10 optional work-capability hints, 3 alternative groups, 2 candidate eligibility graphs / 11 B1 item leaves, and 4 correctly typed board/prose conflict pairs** (strength, arrangement, experience, compensation). The five EDR duties, explicit preferred teamwork, unresolved Kaspersky/customer-experience strength, certificate OR equivalent knowledge, Middle OR Senior topology, and the zero-duty pentesting case remain represented without converting candidate output into accepted facts.

Salary discrepancy detection is narrow: explicit same-currency, non-overlapping numeric amounts only; compatible ranges and negotiated salary do not generate false conflict signals. All four conflict pairs preserve both source-owned values. Focused source/eligibility tests: 46 passed locally; a separate local milestone-reconciliation check added 4 passing tests. The three new conflict-projection regressions passed in clean GitHub CI at commit c604600f (run 43985803756). The full local suite was not rerun after the final CI correction.

**Milestone scope:** `PASS_BOUNDED_EXPOSED_COHORT`; candidate labels remain unreviewed, no independent accuracy/generalization claim, no accepted employer facts or downstream authority. B2 generalization remains **NOT ESTABLISHED**; the source-reference model route remains research-only / no promotion. Next stage: B3 source-bound item translation under the existing 64-request budget. See `docs/working-memory/2026-11-17_P16_B2_BOUNDED_SOURCE_CANDIDATE_MILESTONE.md`.

## November 16 B2 native model comparison — previous research overlay

B2 research branch `feature/p16-b2-source-items-metadata-2026-11-15`
has resolved **local inference-output availability**, NOT source
semantic fidelity. The warm OpenAI-compatible endpoint exhausted its
760-token answer allowance on reasoning; native local Gemma with
`reasoning: off` returned complete JSON for all four frozen exposed
cases in ~24s per four cases. A single short corrective prompt
improved some alternative statements but left serious false employer
requirements and invented duties. The exposed assistant diagnostic
12-check tally is 4 pass/3 partial/5 fail (v2) versus 6/2/4 (v3);
do not treat these as independent accuracy measurements.

An offline source/prompt/review-fidelity gate records
`OPEN_NO_PROMOTION`. B2 remains **full gate OPEN** and draft PR #20
remains unmerged. `main` still serves P1.6 v30/v9; no accepted
records, existing source identities, or downstream fact owners were
changed. Next inspect source-grounded reconciliation of advisory model
suggestions versus exact source candidates; do not add another
unbounded prompt iteration.

Decision: `docs/working-memory/2026-11-16_P16_B2_NATIVE_REASONING_OFF_SEMANTIC_COMPARISON_DECISION.md`.

## November 15 B2 second draft diagnostic — latest implementation overlay

Draft PR #20 now carries exact-source, syntax-bounded nested AND/OR graph
candidates for the exposed Middle/Senior and credential-equivalence cases.
B1 validates each source subspan and Boolean topology; employer semantics
and applicant eligibility remain **unreviewed**. The first bounded local
Gemma original-description request timed out after 95.02 seconds with no
model output; the remaining three planned calls were cancelled. Thus the
LLM comparison is **NOT ESTABLISHED**, not evidence of superior rule accuracy.
The B2 full gate is **OPEN**, no source/production/downstream data changed,
and `main` is still the last accepted v30 state.

Detail: `docs/working-memory/2026-11-15_P16_B2_NESTED_ELIGIBILITY_AND_LOCAL_MODEL_PROBE_RESULT.md`.

## November 15 B2 first read-only diagnostic — prior diagnostic overlay

B2 candidate code now exists **only on its dedicated feature branch**, not in
accepted `main`, production analysis routing, P1.6 persisted artifacts,
Capability/Work/Registry/Market or published corpus. It preserves exact
original source anchors, separately referenced board metadata and optional
work-implied capability hints. Four **exposed** cases and general negative
tests pass locally; complete nested eligibility AND/OR semantics and
independent semantic usefulness remain incomplete. **The full B2 gate stays
OPEN**, and there is no authorization for production rollout.

Record: `docs/working-memory/2026-11-15_P16_B2_SOURCE_ITEM_DIAGNOSTIC_FIRST_SLICE_AND_OPEN_GATE.md`. This newer implementation overlay supersedes previous
"NOT STARTED" wording only for B2 *diagnostic engineering*, not for accepted
product state.

## November 15 B2 duty/capability calibration — prior planning decision

The owner approved a **planning-only** clarification to the upcoming B2
implementation. Employer-stated duties and qualifications retain their
separate evidence authority, but the system should preserve their conceptual
overlap and useful work-implied capabilities. The implication does **not**
become mandatory previous professional experience or a requirement for
unstated tools. Avoid prompt bloat, rigid exclusive micro-classes, extra
model-call stages and unnecessary validation rules; test both false mandatory
claims and relevant context lost to over-separation.

Accepted B1 contract, production P1.6 v30/v9 and downstream data are unchanged.
B2 source-item/board-reconciliation implementation is **NOT STARTED**.
Focused decision: `docs/working-memory/2026-11-15_P16_B2_DUTY_CAPABILITY_RELATIONSHIP_AND_COMPLEXITY_CALIBRATION.md`.
Documentation change based on main `a758952aa2a7e90ed63312dc228327c89df5039f`.

## November 14 Stage B1 contract-design gate — previous accepted gate

**Current execution: P1.6 Stage B2 original-source item interpretation and
structured board-field reconciliation.** B1 design gate is now accepted as
*contract design* only, based on B0's frozen baseline, four exposed A1 jobs,
30 source-exact description fragments, 5 typed board-field references,
2 alternative-eligibility graphs, explicit source/reviewer/translation
boundaries and a source-safe JSON Schema plus validation tests.

**No** B1 actual extracted analysis model, source-bound translation model,
new persistent source/analysis schema, public currentness route or new
accepted P1.6 artifacts exist. The five accepted English anchors and
Capability v9, Work v2, Registry, Market snapshot 15/report 2 remain unchanged.
Legacy `english-projection-v2` still establishes field association only.

**B1 ADR:** `docs/working-memory/2026-11-14_P16_B1_SOURCE_ITEM_BILINGUAL_CONTRACT_ARCHITECTURE_DECISION.md`.
**Next B2 gate:** `docs/P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md` `B2`.
B5's genuinely new 6–8 job cohort remains not acquired.

Earlier "B1 next" and "B0 next" messages below remain historical gate
overlays superseded by this status, not a reopening of historical P2.2B-B2
or a direct promotion of v31/research source heuristics.

## November 14 B0 baseline acceptance — historical previous gate

**Current focused execution gate: P1.6 Stage B B1 (contract and ADR).** B0 baseline
was completed on a separate evidence-only branch, with no production code,
source, translation, schema, accepted artifact, or current router changes.

B0 proves all selected nine original raw HTML evidence hashes against
their stored identities; all 59 retained exposed original-source review
anchors; all five accepted P1.6→Capability anchor pairs; three healthy
private SQLite online backups; and 485 previously known job IDs across 45
locally available SQLite datasets as an **initial** fresh-cohort exclusion index.
The configured database remained byte-identical. B0 froze a source-first,
predeclared evaluation/scoring and local provider budget protocol. **No fresh
unseen cohort has been acquired or independently reviewed.** The next separate
gate is B1; B2–B6 remain conditional.

**B0 closure:** `docs/working-memory/2026-11-14_P16_B0_FROZEN_BASELINE_AND_EVALUATION_PROTOCOL.md`.
**Controlling Stage B implementation plan:** `docs/P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md`.

The earlier November 13 "B0 next" status overlay below is **historical**;
the November 11 "P2.3 capability expectations next" status remains sequenced
after qualified Stage B results. Public English P1.6 still v30/v5; original
v9/v4; translation v2; Capability v9, Work v2, Registry and Market unchanged.

## November 13 Stage B plan adoption overlay — CURRENT execution precedence

**Current next execution:** P1.6 Stage B B0, **not** the historical November 11
next-feature candidate. The authoritative focused plan
`docs/P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md`
has reconciled all four delegated original-source/model A1 reviews and Stage A
passive identity integration into explicit B0–B6 implementation/validation gates.

- Stage B PLAN: CREATED / EXECUTION NOT STARTED. B0 baseline, source and
  unseen-cohort protocol is next. B1–B4 research and B5 evaluation require
  gate-specific results. B6 is conditional and separately promoted.
- Current English P1.6: v30/v5; original P1.6: v9/v4; English projection v2;
  Capability v9, Work v2, Registry and Market accepted states unchanged.
- Previous November 11 proposed capability-expectation slice:
  VALID / SEQUENCED AFTER Stage B qualification; **not cancelled** and
  not permitted to become a parallel new persistent profile program.
- Owner has delegated routine source/model review; assistant assessments
  must remain labeled and cannot impersonate independent human certification.
- Any old “review pending,” “next P2.3 capability increment now,” or “B2 active”
  present-tense wording below is historical and superseded by this overlay.

No new Stage B runtime behavior, accepted artifact, schema or migration exists
at plan adoption.

## November 13 Owner Audit A1 completion overlay (supersedes Stage A review-pending wording)

The owner submitted a partial, independent Pass A review covering two of the four A1 cases. That original submission was preserved verbatim and hashed. Under explicit owner delegation the assistant reviewed all four original Persian postings, froze 59 source-anchored assessment items, then compared the saved model outputs. The assistant identified 18 diagnostic model/pipeline flags and 11 original-versus-English translation observations. The remaining two cases were NOT human-owner reviewed. The assistant had prior context about earlier model failures, so this is not an independent blind human validation.

**Current owner-approved workflow:** routine source/model assessment delegated to the assistant; ask the owner only when their own judgment is necessary. Source ambiguities requiring employer clarification stay unresolved, not guessed. Assistant evaluation is not automatic semantic promotion.

Production English P1.6 stays v30/v5; original v9/v4, translation v2, Capability, Work and Market remain unchanged. No P1.6 candidates were accepted as a result of this evaluation; the next build gate is a source-owned bilingual alignment/review contract and separate unseen verification cohort.

Complete record: `docs/working-memory/2026-11-13_OWNER_A1_ASSISTANT_SOURCE_AND_MODEL_RECONCILIATION.md`.

## November 13 source-first Stage A status overlay

Stage A delivered an **inactive, versioned source identity foundation** and a
local-only owner source-first review packet (JH-OWNER-A1-20261113). The
foundation verifies exact original description spans and makes the existing
field-level English translation's lack of item alignment explicit. It introduces
no new accepted source classifications or English P1.6 artifacts. P1.6 v30/v5
remains the current production English analyzer; original v9/v4, Capability,
Work, Registry and Market current behavior are unchanged.

The owner has a source-only offline review package for four exposed jobs; Pass A
verdicts are pending and model-comparison Pass B is withheld. The research-only
heuristic parser, source-bound LM Studio trial and v31 candidates remain outside
main. The next gate is reviewed bilingual item alignment and a separate unseen
cohort, NOT a direct source-semantic promotion.

Record: `docs/working-memory/2026-11-13_P16_PASSIVE_SOURCE_IDENTITY_STAGE_A_CLOSURE.md`.
Public Pass A: `docs/review-packets/2026-11-13_JH_OWNER_A1_SOURCE_ONLY.md`.

## 1. Current operating state

```text
Phase 1 / P2.1 / P2.2A              CLOSED / ACCEPTED
P2.2B-B1                            CLOSED / NO-PROMOTION / DEFER
P2.2B-B2                            CLOSED / ACCEPTED, SIX-CANDIDATE SCOPE
Market I1-I7 + coverage follow-up    ACCEPTED / CLOSED FOR BOUNDED SCOPE
Candidate V6 / report R1-R4          ACCEPTED / CLOSED FOR BOUNDED REPORTING
P2.3A-0 evaluation                  EXECUTED / BOUNDED FINDINGS RECORDED
P2.3A bounded factual comparison     DELIVERED / ENGINEERING CLOSED
Market-context navigation repair    ACCEPTED / PROMOTED TO MAIN
At-a-glance UI experiment           CLOSED / NO-PROMOTION
Owner efficiency measurement        NOT ESTABLISHED / NOT CLAIMED
Next capability expectation slice   PROPOSED / BOUNDED DECISION PENDING
Persistent P2.3 profiles             NOT AUTHORIZED
P2.2C / P2.2D / P2.4                 NOT AUTHORIZED
Blueprint                           EXPERIMENTAL / NON-AUTHORITATIVE
Personal readiness / scoring        NOT AUTHORIZED
```

Current focused decision and closure proof:

`docs/working-memory/2026-11-11_P23A_COMPARISON_STAGE_CLOSURE_AND_NEXT_CAPABILITY_GATE.md`

The October 26 historical authorization remains `docs/working-memory/2026-10-26_B2_CLOSURE_AND_P2_3A_BOUNDED_BROWSER_DECISION.md`.

The owner approved B2 closure reconciliation, existing composition evaluation, and a bounded browser understanding/comparison slice on October 26. This supersedes the old instruction to apply R3–R6: those exact mappings already exist and were reverified without production mutation. It does not authorize the whole P2.3 program.

## 2. Proven B2 state

R1–R6 are accepted, applied, and verified. The six concepts map twelve exact responsibility claims across `tvMm` artifact 50 and `tNVe` artifact 56. R3–R6 occupy mapping rows 11–18, applied October 20. Current selection: **12/35 mapped; 23 pending**. Artifact 50 responsibility[9] and broader boundary claims remain pending.

The local Registry has ten concepts, eighteen claim decisions, and one pre-existing alias. No R3–R6 aliases were created. The original six P2.1 decisions include one explicitly unmapped claim.

The retained pre-application backup and current database differ only by four added concepts, eight added mappings, and sequence bookkeeping. No unrelated Registry row, accepted P1.6 identity, source, Capability, Work, or Market row changed. Integrity/FKs, CLI idempotency on a copy, rendered browser/CLI agreement, and public-corpus verification pass. Detailed proof and its browser limits are in the focused record.

B2 closure creates reviewed normalized correspondence, not promoted responsibility families or prevalence authority. The earlier October 10/17 decisions remain the semantic-definition history; their pending-application wording is superseded for present-tense routing.

## 3. Current accepted evidence and contracts

```text
Public corpus: 420 known jobs / 52 parsed details / 30 English projections
               11 accepted English P1.6 / 5 Capability artifacts
English P1.6:  job-analysis-english-v30 / job-analysis-v5
Capability:    job-capability-intelligence-v9 / job-capability-intelligence-v5
Registry:      jobhunter-canonical-concept-registry-v1
Work:          job-work-intelligence-v2 / job-work-intelligence-v2.0
```

Accepted-only historical P1.6 v20/v21/v23/v28 compatibility remains intentional under exact dependencies. Do not regenerate accepted anchors merely because generation uses v30.

Snapshot 15 still has six accepted-semantic core postings, 140 requirements, and 35 responsibilities. Exact analysis IDs remain `tvMm=50`, `tNVe=56`, `tmvA=61`, `tjgi=60`, `t7ck=52`, `t7Ay=62`. The last two contain no direct responsibilities. Snapshot/report history remains immutable; report #2 is accepted for bounded analytical use, while #1 remains pending historical evidence.

## 4. Evaluation disposition and next build

Strategy A preserves all 175 target claims in 175 buckets. Strategy B is unavailable for those six jobs. On five older accepted anchors it organizes 98 distinct claims into 22 groups, retains ten ungrouped claims, and exposes 35 repeated group memberships. Exact-partition metrics fail; work-activity boundaries pass. Those results remain unchanged evidence, not an architecture acceptance score.

Use complete factual projection as the browser baseline and optional current Capability organization as job-local navigation. Count each source claim once, expose shared group support, retain missing/unmapped evidence, and validate exact current source/translation/P1.6 dependencies. Runtime reads remain SQLite-based; the public corpus does not become a runtime input.

The implemented bounded view compares up to three jobs, finds exact capability wording, separates requirements/depth from direct work, and links back to evidence. It makes no personal-fit or canonical-equivalence claim from lexical matches. No new model calls or profile persistence are authorized.

## 5. Unchanged stop lines

Do not reopen B1, accepted anchors, Capability v9, or Blueprint merely to fill this view. Do not bulk-map the pending claims, promote families/archetypes, start Market v2/personal scoring, add Strategy-C inference, or publish private state. Any additional inference or durable profile architecture requires a separate bounded decision.

Portfolio/release work remains parallel: MIT complete; metadata, screenshots/release, and owner mastery retain their own scope.


## 6. November 11 completion and next product routing

The factual `/compare` implementation is retained. A reproducible frozen-Market-context bug was repaired so every compared job that actually belongs to the originating frozen snapshot preserves validated report/finding navigation; nonmembers cannot impersonate snapshot evidence. The repaired code and regression tests were validated against real snapshot #15/report #2.

The optional `at a glance` prototype was **not promoted**: its raw-count summary was not shown to improve owner comprehension or time-to-decision, and introduced reading/editing tradeoffs. No measured owner benefit or time savings are asserted. That experimental UI work is closed rather than a standing condition for the next feature stage.

The next product **candidate** is `docs/working-memory/2026-11-11_NEXT_SUBSTANTIVE_CAPABILITY_EXPECTATION_SLICE.md`: job-specific, evidence-grounded technical work and capability expectations with explicit/implied/inferred/unknown distinctions. Its design and real-case gate precede persistent profiles or corpus-scale promotion. No new inference, Market v2, personal scoring or taxonomy authority is granted by this record.
