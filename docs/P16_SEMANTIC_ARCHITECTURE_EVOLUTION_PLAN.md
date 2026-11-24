# P1.6 Semantic Architecture Evolution and Reliability — execution checklist

**Adopted:** 2026-11-24, following owner agreement to the strategic review and staged investigation.
**Status:** ACTIVE — investigation and planning authorized; architectural outcome undecided.
**Baseline:** main at `c1770ff688eb3e28309cdcf843f51d8d8c0bdeff`.
**Active next item:** E1.1 (governance and design/history review).
**Authority:** This is the single execution tracker for the P1.6 evolution within Stage B, not a parallel product roadmap or a replacement of Stage B acceptance gates. The existing [Stage B focused plan](P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md), permanent governance and explicit promotion rules control. The previously proposed P2.3 capability-expectation slice remains deferred.

## 1. Purpose and protected boundaries

Optimize for useful, decision-relevant job intelligence per unit of user time, not structural PASS counts alone. Investigate before committing to an architecture. Preserve local-first modular monolith, SQLite, source acquisition/lifecycle, original-source identity and provenance, privacy, currentness, accepted historical artifacts, and downstream authority boundaries. Work on main unless an explicit isolation decision is made; use isolated private DB copies for experiments.

- Let the LLM reason about natural job language, duties/qualification relationships, implied capabilities and uncertainty. Distinguish explicitly stated employer facts from inference; do not invent mandatory paid experience, tools or duties.
- Assign deterministic machinery identity, evidence binding, bookkeeping, counts, safe representation recovery, persistence and integrity checks. Do not substitute rigid rules for semantic judgment without evidence.
- Separate representation errors, semantic errors, evidence/integrity failures and incomplete coverage. Consider useful partial candidates without granting them accepted downstream authority. Never weaken hard integrity guards to obtain a pass.
- Treat B2v7, source-bound translation and v30 as valuable existing work, not immutable design commitments. Compare alternatives rather than presume that original-language reasoning, a simpler schema, more calls, or a different model is superior.
- Preserve frozen results and denominators. All four prior B5 cohorts and the November 23 three source-distinct diagnostic ads are exposed. No reuse as unseen evidence. No automatic fifth acquisition.
- Current production English v30/v5 and original v9/v4 remain unchanged; new v9 artifacts are pending review. No automatic retrospective relabeling or regeneration of accepted facts. No new Capability, Work, Market, Registry or personal readiness authority; no B6 routing or rollout without a separate explicit decision.
- Use configured local LM Studio only, bounded budgets (actual HTTP attempts including retries, tokens, wall time), no cloud inference, and no private inputs or raw model responses in Git.

## 2. Checklist and evidence discipline

One checkbox per independently verifiable deliverable. Check only when the stated completion criteria are satisfied and its result is linked in the milestone record. A failed experiment can be completed as an investigation, but cannot check a success/promotion gate. If blocked, retain unchecked and record the blocker, evidence and next decision. Never check future work based on code existence, a previous promise, passing tests alone or an exposed-case score. Reopen a checked item explicitly if evidence invalidates it; retain earlier receipts. Update this tracker, execution TODO, and working memory at each meaningful milestone; commit coherent work to main, verify CI and local/remote alignment. Do not duplicate full checklists in other documents.

For each milestone use one dated record under `docs/working-memory/` (suggested names below); put any public-safe aggregates in a sibling evidence directory and raw source/model/private DBs in ignored `data/local-acceptance/`. Record task IDs, base/implementation commits, date, scope, hypotheses, inputs and hashes, model/config/contract versions, reproducible commands, budgets and actual calls/latency, tests, results and denominator, reviewer exposure/authority, failures and uncertainty, changed files and state/privacy checks, decision and next eligible item. Record N/A with justification, not fabricated evidence. Keep a small status/receipt ledger in section 5 of this file. Preserve historical records unchanged.

## 3. Execution phases

### E0 — Adopt and anchor the review (planning only)

- [x] E0.1 Owner agrees to the strategic review, root-cause-first approach, staged redesign and implementation; record objectives, principles and stop lines here.
- [x] E0.2 Anchor current baseline: local and remote main at c1770ff; prior CI green, recorded 1,274-test repair suite, fresh local lint/dependency/integrity/reconciliation checks, baseline DB and corpus manifest unchanged. Sources: [Nov 23 repair/Nov 24 reconciliation](working-memory/2026-11-23_P16_REAL_AD_SOURCE_FIRST_REPAIR_AND_OPEN_SEMANTIC_GATES.md), [CI at baseline](https://github.com/motafegh/jobhunter/actions/runs/45430793640). These establish engineering state, not semantic reliability.
- [x] E0.3 Publish this checklist and route current instructions, Stage B focused plan and execution/status records here; keep existing contract authority and frozen evidence intact.

### E1 — Strategic and technical investigation (read-only first)

**Goal:** isolate causal mechanisms, not simply catalogue symptoms. Result record: `YYYY-MM-DD_P16_EVOLUTION_E1_ROOT_CAUSE_INVESTIGATION.md`.

- [ ] E1.1 Read controlling product, architecture, domain, source and reasoning policy, roadmap/master plan, focused Stage B plan, ADRs and relevant historical decisions; map existing requirements and constraints to concrete owners. Identify what is settled versus open and any genuine contradictions.
- [ ] E1.2 Inventory semantic architecture evolution (v30 inheritance, relevant historical variants and failed prompt probes, B1-B4 candidates, parser/translation routes, downstream gates). Trace real execution from source capture to review/persistence and consumption; record file/function boundaries, not only a conceptual diagram.
- [ ] E1.3 Freeze an exposed diagnostic evidence inventory from the November 23 real-ad audit, four prior B5 cohorts and relevant accepted anchor/sparse/dense cases. Verify source/translation/attempt IDs, hashes and isolation; enumerate unavailable evidence. No unseen sources or model calls needed for this step.
- [ ] E1.4 Replay the two v30 depth/concept failures from retained outputs; trace schema/validators and inheritance, distinguish recoverable representation from actual wrong meaning and unsupported evidence. Demonstrate safe and unsafe normalization examples with source-local degree/obligation/experience.
- [ ] E1.5 Replay the v30 dense-duty coverage failure: trace source plan, partition/context, model response, filters, reconciliation and coverage validation. Locate the loss or mark it unresolved with evidence.
- [ ] E1.6 Audit actual model-facing schemas, assembled prompts, constraints, retries and token/context budgets for burden, redundancy and contradiction; compare with earlier failed/successful variants. Separate measured findings from conjecture.
- [ ] E1.7 Audit B2v7 semantic classification/heading dependence, unresolved items, formal alternatives, metadata conflicts, duty-capability relationships and known remaining exposed failures. Identify where structure helps and where semantic rules risk lost context.
- [ ] E1.8 Audit bilingual path: compare original and v2 translation and B3 evidence-bound candidates for proper names, technical terminology, distinct duties, depth, modality, alternatives and source attribution. Test whether translation is a necessary intermediate step versus a presentation/alignment function; establish hypotheses, not premature changes.
- [ ] E1.9 Inspect authority and delivery boundaries for partial output, including B4v6 and source-brief, pending/rejected results and accepted-only consumers. Specify what can be shown safely vs what requires whole-artifact acceptance.
- [ ] E1.10 Baseline comparative model/resource characteristics and practical user workflow; distinguish model capability, schema/prompt burden, translation error, validation, coverage and architecture hypotheses. Record available model versions and measured latency/calls; any new inference needs a frozen bounded protocol in E2/E3.
- [ ] E1.11 Publish root-cause matrix with evidence, impact, confidence, unknowns, reproducible replays, ranked improvement opportunities and alternatives to test. Verify no production mutations. Close E1 as investigation only; unresolved causes stay explicit.

### E2 — Architecture alternatives and design/plan decision

**Dependency:** E1 record. Result record: `YYYY-MM-DD_P16_EVOLUTION_E2_ARCHITECTURE_DECISION.md` (ADR if a durable contract changes).

- [ ] E2.1 Define at least the unchanged v30 baseline, targeted safe representation/coverage repair, simpler source-local semantic contract with deterministic reconciliation, and original-source/bilingual interpretation alternatives. Compare context preservation, evidence safety, output utility, implementation/maintenance burden, model demands and latency. Reuse existing B1/B2/B3/B4 components where justified; consider no-change if alternatives lack benefit.
- [ ] E2.2 Design candidate authority boundaries, item/child alignment, optional depth and semantic normalization, source-vs-inference relationships, unknown/partial states, alternatives and candidate-to-accepted promotion. Explicitly protect downstream currentness and historical compatibility.
- [ ] E2.3 Design a bounded exposed-case experiment protocol: identical source versions, baseline and alternatives, fixed model/config where isolating architecture, frozen selection and metrics, representative sparse/dense and Persian/English cases, source-first review and fair comparators. Predeclare budgets and stop rules. If model comparisons are justified, control architecture/model variables and measure resource constraints; do not conflate them.
- [ ] E2.4 Specify scoring and acceptance thresholds before experiments, including critical false-required/unsupported evidence, missing material duties/requirements, translation fidelity, alternatives, depth/experience, delivery rate and partial utility, latency/calls/tokens, maintainability and user task accuracy/time. Separate structural success, correct rejection and semantic approval; define denominators and uncertain cases.
- [ ] E2.5 Select evidence-supported experimental design and document rejected alternatives/tradeoffs, remaining uncertainty, versioning and migration/rollback considerations. Obtain explicit owner decision for material governing contract changes, production routing, or scope expansion. No architecture declared superior before comparative evidence.
- [ ] E2.6 Reconcile relevant product/domain/architecture/reasoning policy, Stage B plan, roadmap, master plan, current-state overlay, AGENTS, TODO, working memory and research index to the actual selected design and next work; preserve historical records. If amendments are premature, record why and retain existing authority. Freeze E3 implementation sequence and acceptance gates.

### E3 — Versioned experimental implementation and comparative evaluation

**Dependency:** E2 selected design and frozen protocol. Result record: `YYYY-MM-DD_P16_EVOLUTION_E3_EXPOSED_COMPARATIVE_RESULT.md`.

- [ ] E3.1 Implement selected experimental semantic candidate(s) on isolated state; keep original evidence binding and explicit authority. Add deterministic unit/contract tests for safe recovery and hard failures, coverage/currentness and negative cases; no production routing.
- [ ] E3.2 Improve/test bilingual semantic fidelity according to E2 design, including source-bound associations, exact source structure, technical/name identity, duty boundaries and modality/alternatives; no claim of linguistic correctness from alignment alone.
- [ ] E3.3 Implement/test qualified partial job intelligence and natural duty-to-capability reasoning if selected; preserve unresolved states, drilldown and employer-vs-inferred labeling. No implicit promotion. Reuse B4v6/source-brief where useful.
- [ ] E3.4 Run the frozen paired protocol against exposed cases with configured local models and actual call/time/token accounting. Include unchanged v30, not invalid outputs treated as a fair semantic comparison. Report failed/rejected/partial/valid/semantically approved separately.
- [ ] E3.5 Source-first review each consequential assertion and coverage, compare bilingual meaning and source/metadata conflicts, score with denominators, reviewer exposure and uncertainty. Run accepted-anchor and older exposed regressions and privacy/isolation checks; no per-job rule patching to inflate scores.
- [ ] E3.6 Decide retain/revise/reject based on measured accuracy, delivery, efficiency and maintainability; seal results and record any changed design/protocol before repeating. No fresh B5 until frozen candidate and separate prospective protocol are ready.

### E4 — Product usefulness and independent verification

**Dependency:** E3 comparative decision. Result records: `YYYY-MM-DD_P16_EVOLUTION_E4_USEFULNESS_RESULT.md` and prospective B5 protocol/result records.

- [ ] E4.1 Freeze genuine owner or context-isolated reviewer task protocol against original advertisements and relevant current B4v5/v6/current output; measure comprehension, task accuracy, reading/decision time, unresolved/incorrect conclusions, drilldown burden. No proxy-only user value claims.
- [ ] E4.2 Execute usefulness evaluation, preserve adverse results and limitations, select the useful candidate or return to E2/E3. Do not claim independent human review from same-assistant inspection.
- [ ] E4.3 Explicitly prefreeze corrected prospective B5 method, versioned candidate and budget, source-only assertions, granularity, alternatives, uncertainty and critical guard thresholds, paired translation/semantic checks. Check archive-relative novelty by original-description SHA across job IDs before independent testing. No selection after viewing candidate results.
- [ ] E4.4 Run independent fresh B5 evaluation with original-source-first assessment and strict stop conditions. Preserve failure if any material gate fails; report all attempted and excluded sources, denominator, translation/semantic and utility outcomes, reviewer independence and limitations. Do not change frozen evaluator or candidate in flight.
- [ ] E4.5 B5 acceptance decision: only check PASS after applicable source, semantic, bilingual and usefulness gates are met on independent evidence. Otherwise record HOLD/FAIL, expose cohort and return to E2/E3 without automatically consuming another cohort. No B6 authorization by implication.

### E5 — Controlled production integration and roadmap resumption

**Dependency:** explicit accepted B5 and explicit owner authorization for B6. Result record: `YYYY-MM-DD_P16_EVOLUTION_E5_B6_ROLLOUT_DECISION.md`.

- [ ] E5.1 Select opt-in sidecar vs new route or no promotion; design migration, rollback, accepted-only compatibility, currentness and review semantics; preserve historical artifact identities and privacy. Explicitly approve production scope.
- [ ] E5.2 Implement gated integration, tests for downstream Capability/Work/Market/Registry, CLI/browser, public corpus and historical dependencies. Verify migration and rollback in isolation.
- [ ] E5.3 Perform bounded real local end-to-end acceptance with source-first review, dependency checks, tests with warnings as errors, CI, SQLite integrity/FKs, privacy/corpus and rollback verification; record qualified user benefit and residual limits.
- [ ] E5.4 Record B6 acceptance/no-promotion decision; align all governing and status documents, local/remote main, installed CLI/browser and reproducible records. Resume the deferred P2.3 capability-expectation slice only by explicit next-feature decision.

## 4. Parallel historical v9 review track (independent, not a shortcut to B5)

Result record: `YYYY-MM-DD_P16_EVOLUTION_V9_HISTORICAL_ACCEPTANCE_AUDIT.md`. Start read-only; may proceed during E1-E3 without delaying investigation unless a material authority leak is found.

- [ ] V9.1 Inventory historical accepted original-language v9 artifacts, exact source versions, acceptance mechanism, current selectors/consumers and potential downstream blast radius; distinguish trial from production.
- [ ] V9.2 Source-first review affected artifacts for unsupported requirements, benefit/qualification confusion, omissions, duty/qualification distinctions, depth/modality and evidence locality. Preserve historical statuses; no automatic reapproval/rejection.
- [ ] V9.3 Publish impact/triage results, proposed explicit review or rejection decisions and dependencies; if material unsafe reuse is established, stop affected promotion and seek a separately bounded remediation decision. Execute authorized review workflow only with historical integrity and regression checks.

## 5. Current ledger and continuation

| Task/gate | State | Evidence / result | Next |
| --- | --- | --- | --- |
| E0.1-E0.3 | DONE (planning) | This file; owner agreement; baseline decision and CI above; routing links | E1.1 |
| E1 | NOT STARTED | Existing exposed evidence retained; investigation not yet executed | E1.1-E1.11 |
| V9 | NOT STARTED | New-v9 pending guard exists; historical review still open | V9.1 |
| E2-E3 | GATED | No architecture selected or new candidate implemented | After E1 |
| E4 / B5 | GATED / NOT ACCEPTED | Four prior prospective source gates failed; all cohorts exposed | After E3 |
| E5 / B6 | CLOSED | No production authorization | After B5 and explicit decision |

**Next action:** E1.1, then E1.2 and E1.3; start with read-only governance/design and evidence inventory. Update checkboxes with actual records as each deliverable is verified. If evidence supports a different sequence, record the rationale and dependency changes here before execution. Do not skip the causal investigation for another version bump.
