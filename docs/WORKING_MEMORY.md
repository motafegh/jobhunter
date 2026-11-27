# JobHunter Working Memory / Handoff

**2026-11-27 E3.1a increment 1:** [Offline AI Lab implementation and limits](working-memory/2026-11-27_P16_EVOLUTION_E3_1A_OFFLINE_LAB_INCREMENT1.md) verified (51 new tests, 126 focused passed, three frozen copies, synthetic guarded worker). Real dispatch disabled; E3.1 remains open. Continue E3.1a preflight/worker/provider guard coverage before E3.1b. No production runtime or accepted authority change.

**2026-11-27 E2.6:** [Final requirements freeze](working-memory/2026-11-25_P16_EVOLUTION_E2_ARCHITECTURE_DECISION.md#2026-11-27-continuation--e26-final-implementation-requirements-freeze) and [machine-readable seal](working-memory/2026-11-27_p16_e2_freeze/E3_REQUIREMENTS_FREEZE.json) complete. E2 closed as design; E3.1a offline guard/runner next, then E3.1b adapters and reconciliation. 47 cells, 382 generation POST ceiling, existing rubric and selected model roles unchanged; all 1,286 tests with warnings as errors, Ruff, pip check, protected checks and prior CI 45877475918 passed. No model qualification, inference, production routing or B5/B6. DOC.6 incremental; V9 separate.

**2026-11-26 DOC.5:** [Selected proposed architecture](working-memory/2026-11-26_ARCHITECTURE_UNDERSTANDABILITY_DOC5_SELECTED_DESIGN.md) complete as implementation-facing design: A0 unchanged, A1 repair seams, A2 six components/compact response, language views, independent state axes, guard/receipts/authority and rollback. 139 focused tests; prior CI 45873047605 passed. Protocol/rubric/selection unchanged; no runtime implementation or measured winner. Required DOC companions complete; next E2.6 freeze, DOC.6 remains incremental.

**2026-11-26 DOC.7:** [Orientation and documentation-currentness practice](working-memory/2026-11-26_ARCHITECTURE_UNDERSTANDABILITY_DOC7_ORIENTATION_CURRENTNESS.md) complete and demonstrated against actual November 23 repair 76c497b. AGENTS §13.1 and definition of done updated; original v9 pending/ready-label, source-brief coverage and export scope clarified in living references. 62 focused tests, prior CI 45867590818 and protected checks passed; no production changes or new CI gate. Next DOC.5 then E2.6; DOC.6 remains incremental.

**2026-11-26 DOC.4:** [Bounded inspection feasibility/prototype](working-memory/2026-11-26_ARCHITECTURE_UNDERSTANDABILITY_DOC4_INSPECTION_FEASIBILITY.md) complete. Optional `scripts/inspect_p16_architecture.py` extracts curated AST/imports, effective owners/MRO, schema and frozen SQLite metadata; 44 files, 456 definitions, 281 file/import pairs, 10 owners, 40 focused tests (12 new). Prior CI 45860931648 passed. Manual verified maps remain primary; no inference, production mutation or whole-system call graph. Next DOC.7, DOC.5 then E2.6.

**2026-11-26 DOC.3:** [Component profile standard](COMPONENT_PROFILE_STANDARD.md) and [worked P1.6 profiles](working-memory/2026-11-26_ARCHITECTURE_UNDERSTANDABILITY_DOC3_COMPONENT_PROFILES.md) complete: current English analysis, opt-in source brief, review and consumers. Reader paths, responsibility/contract/dependency/failure/authority fields and evidence notation established. 31 DOC.2 file fingerprints, 65 symbols, 10 method owners and four MROs reverified; 112 focused tests passed. Prior CI 45859825925 passed. No production change or whole-system coverage claim. Next DOC.4, DOC.7, DOC.5 then E2.6.

**2026-11-26 E2.5:** [Experimental design selection](working-memory/2026-11-25_P16_EVOLUTION_E2_ARCHITECTURE_DECISION.md#2026-11-26-continuation--e25-bounded-experimental-design-selection) and [machine-readable decision](working-memory/2026-11-26_p16_e2/EXPERIMENT_SELECTION.json) complete. A0 unchanged; A1 four-repair family; A2 contextual candidate; L0/L2/L3, M0/M1 with predeclared technical M2 fallback. Existing 47 cells and scoring thresholds preserved, new models deferred to separate bounded research. 134 focused tests passed; 20 static symbols verified; prior CI 45837660472 passed. No implementation, new calls, production contract or winning architecture. Next DOC.3, DOC.4, DOC.7 and DOC.5 before E2.6 freeze.

**2026-11-26 E2.4:** [Source-first scoring/acceptance](working-memory/2026-11-25_P16_EVOLUTION_E2_ARCHITECTURE_DECISION.md#2026-11-26-continuation--e24-scoring-acceptance-thresholds-and-model-discovery), [rubric](working-memory/2026-11-26_p16_e2/EVALUATION_RUBRIC_DRAFT.json) and [model discovery register](working-memory/2026-11-26_AI_MODEL_DISCOVERY_AND_QUALIFICATION_REGISTER.md) complete as design. Proposed hard safety gates, strict precision/recall, useful delivery, relationship/bilingual/task and resource/maintenance criteria; 21 synthetic arithmetic controls and 132 existing focused tests passed. Owner plans downloads; 47-cell protocol unchanged, no model qualification/inference. Prior CI 45819165603 passed. Next E2.5 selection, DOC companions and E2.6 freeze.

**2026-11-26 E2.3:** [Bounded comparative protocol](working-memory/2026-11-25_P16_EVOLUTION_E2_ARCHITECTURE_DECISION.md#2026-11-26-continuation--e23-bounded-exposed-comparative-protocol) and [draft cell manifest](working-memory/2026-11-26_p16_e2/EXPERIMENT_PROTOCOL_DRAFT.json) complete as design: 9 comparative + 3 offline compatibility cases, exact source and v2 dependencies, 3 hashed local model files, 47 planned cells including conditional interaction, 382 max generation attempts including preflight, 4h active ceiling. 113 focused tests passed; prior CI 45817475794 passed. No inference or model qualification, exact local rights/runtime feasibility still gated. Next E2.4 scoring/thresholds; E2.5 selection and E2.6 freeze, DOC companions.

**2026-11-26 E2.1/E2.2:** Local synchronization and protected-state verification complete; E2.1 base CI 45694817594 passed. [Architecture/semantic authority design](working-memory/2026-11-25_P16_EVOLUTION_E2_ARCHITECTURE_DECISION.md) and [synthetic examples](working-memory/2026-11-26_p16_e2/SEMANTIC_CONTRACT_EXAMPLES.json) complete as design only; 130 focused existing tests passed, 12 exact anchors checked, 2 tamper/stale rejections. Four required statement fields, optional meaning dimensions; system-owned identity, coverage, execution and authority. No new inference, selected architecture or production contract. Next E2.3 bounded comparative protocol. DOC.3/4/7 before E2.6.

**2026-11-25 E2.1 design:** [Architecture alternatives and E2 decision record](working-memory/2026-11-25_P16_EVOLUTION_E2_ARCHITECTURE_DECISION.md) published: unchanged A0, targeted A1, contextual A2 and orthogonal A3 language arms, model/recovery comparisons and no-change outcome. No selected implementation or new inference. Local device offline; E2.1 checkbox remains open pending synchronization, protected-state and CI verification. Next E2.2 after reconciliation.

**2026-11-25 E1 closure:** E1.11 and DOC.2 complete. [Root-cause synthesis](working-memory/2026-11-24_P16_EVOLUTION_E1_ROOT_CAUSE_INVESTIGATION.md#2026-11-25-continuation--e111-consolidated-causal-findings-and-e2-decision-inputs) (18 mechanisms); [verified current P1.6 map](working-memory/2026-11-25_ARCHITECTURE_UNDERSTANDABILITY_DOC2_P16_RUNTIME_BASELINE.md) (including corrected nested V15/V16 recovery, 90 focused tests and offline controls). Next E2.1 design alternatives; DOC.3/4/7 before E2.6, V9 independently open. No semantic or production promotion.

**2026-11-25 E1.10:** Read-only model/resource investigation complete: 14 catalog entries and GGUF headers, 137 historical logical attempts/47 retained artifacts, 27 retained usage rows; E4B/MiMo 9B initial comparative candidates, 12B QAT conditional, no quality ranking or load verification. No new inference, downloads or promotion. Next E1.11; DOC.2 before closure. See [E1 record](working-memory/2026-11-24_P16_EVOLUTION_E1_ROOT_CAUSE_INVESTIGATION.md) and [safe audit receipt](working-memory/2026-11-24_p16_evolution_e1/SAFE_E1_10_MODEL_RESOURCE_AUDIT.json).

**2026-11-25 AI research strategy:** [JobHunter AI Architecture, Research and Evolution Plan](AI_ARCHITECTURE_RESEARCH_AND_EVOLUTION_PLAN.md) records the owner-approved research directions and controlled evaluation gates. It is a strategic companion, not a production route or parallel execution plan. E1 closed as investigation only; E2.1-E2.6 design frozen; E3.1a offline guard/runner next; E2/E3 explicitly compare viable local models and architecture alternatives. Broader RAG/agents/training/learning/graph work remains gated. The August 2 proposal is preserved as history; local-only inference and B5/B6 boundaries remain unchanged.

**2026-11-25 E1.9:** Partial intelligence/authority investigation complete: three historical B4 replays, three source-only briefs, five synthetic controls, 157 focused tests passed. Candidate display remains distinct from semantic acceptance; discovered B4 completeness/translation gaps and original-v9 browser status-label gap. No promotion, new inference or runtime changes. Next E1.10; DOC.2 open. See [E1 record](working-memory/2026-11-24_P16_EVOLUTION_E1_ROOT_CAUSE_INVESTIGATION.md) and [safe audit receipt](working-memory/2026-11-24_p16_evolution_e1/SAFE_E1_9_PARTIAL_AUTHORITY_AUDIT.json).

**2026-11-25 E1.8:** Bilingual fidelity investigation complete: seven frozen v2 pairs, 64 B3 item records, two original v9 artifacts and existing budget/batch verifiers. Translation-first is a current dependency, not proven necessary for semantic reasoning. Original-first and hybrid remain E2 hypotheses; no promotion or new inference. Next E1.9; DOC.2 open. See [E1 record](working-memory/2026-11-24_P16_EVOLUTION_E1_ROOT_CAUSE_INVESTIGATION.md) and [safe audit receipt](working-memory/2026-11-24_p16_evolution_e1/SAFE_E1_8_BILINGUAL_AUDIT.json).

**2026-11-24 E1.7:** Original-source classification investigation completed. 32 archived and 3 recent sources checked; 7 synthetic probes. Identified heading-driven omission/false mandatory labels, unresolved alternatives and limited lexical metadata/work-capability links. No production change or semantic promotion. Next E1.8; DOC.2 remains open. See [E1 record](working-memory/2026-11-24_P16_EVOLUTION_E1_ROOT_CAUSE_INVESTIGATION.md) and [safe audit receipt](working-memory/2026-11-24_p16_evolution_e1/SAFE_E1_7_CLASSIFICATION_AUDIT.json).

**2026-11-24 E1.6 / DOC.1:** Actual prompt/schema/retry audit complete: 28,068 base prompt characters, 128 bullet lines, active inherited validator counts, superseded/conflicting instructions and offline reask growth measured. Historical comparisons not controlled; no new inference or production change. [DOC.1 gap audit](working-memory/2026-11-24_ARCHITECTURE_UNDERSTANDABILITY_DOC1_GAP_AUDIT.md) complete; DOC.2 remains open. Next E1.7; see [E1 record](working-memory/2026-11-24_P16_EVOLUTION_E1_ROOT_CAUSE_INVESTIGATION.md) and tracker.

**2026-11-24 E1.4/E1.5 offline causal replay:** Six retained failed completions reject in reconstructed v30 contexts; v23 compound-OR concept overwrite, lexical depth/context misinterpretation and v21 false skills-as-duty coverage directly reproduced. Corrected coverage context alone allows unchanged security retry through partition validation; missing genuine duty still rejects. No production change or semantic acceptance. Next E1.6; DOC.1/2 open. See `docs/working-memory/2026-11-24_P16_EVOLUTION_E1_ROOT_CAUSE_INVESTIGATION.md`.

**2026-11-24 architecture understandability track:** Owner approved DOC.1–DOC.7 in [the evolution plan](P16_SEMANTIC_ARCHITECTURE_EVOLUTION_PLAN.md#5-parallel-architecture-understandability-and-living-documentation-track). Verified runtime diagrams, execution/dependency maps, component profiles, code-derived inspection feasibility, orientation and documentation-currentness are planned companion work. DOC.1–DOC.2 during E1; later items at their specified gates. E3.1a offline guard/runner is next; DOC.1–DOC.5 and DOC.7 complete, DOC.6 pending and no production change is authorized by this amendment.

**2026-11-24 evolution E1 update:** E1.1-E1.3 complete for governance, active runtime trace and retained evidence inventory; 32 B5 source versions, 5 accepted anchors, 4 A1 exposed originals and 3 Nov 23 cases verified. No semantic accuracy claim, new inference or production mutation. Historical E1.1-E1.3 handoff; superseded by E1.4/E1.5 results above. Record: `docs/working-memory/2026-11-24_P16_EVOLUTION_E1_ROOT_CAUSE_INVESTIGATION.md`.

**2026-11-24 active evolution sequence:** Owner-approved investigation-first execution tracker: `docs/P16_SEMANTIC_ARCHITECTURE_EVOLUTION_PLAN.md`. E1.1-E1.11 completed (investigation only); DOC.1-DOC.5 and DOC.7 complete; E2.1-E2.6 design frozen; next E3.1a offline guard/runner (see tracker); use its milestone checkboxes and linked evidence records. This sequences the existing Stage B work; no new production contract, B5 acceptance, B6 authorization or downstream promotion. Earlier dated next-action wording remains historical where superseded.

**Last research-status reconciliation:** 2026-11-24 (Nov 23 bounded repair verified on published CI; governing-document alignment, local database integrity and frozen audit receipt checked; English v30 and translation semantic gates remain open).
**Latest P1.6 research/manual review index:** `docs/working-memory/2026-11-13_JOBHUNTER_RESEARCH_PROMOTION_AND_MANUAL_REVIEW_INDEX.md`.
**Stage A status:** The passive exact-source-span identity and offline source-only review utility are on main. Owner Audit A1 is assistant-reviewed on all four exposed cases; this remains distinct from independent human certification. B3 source-bound translation is integrated into `main` as candidate-only modules, not activated in production; no new English P1.6 authority is approved. Fresh unseen verification is still pending. Stage A closure: docs/working-memory/2026-11-13_P16_PASSIVE_SOURCE_IDENTITY_STAGE_A_CLOSURE.md.
**Pre-evolution engineering baseline:** 2026-11-23 BOUNDED SOURCE-FIRST REPAIR: new opt-in B2v7 candidate recovers 15/15 backend work passages and 5/5 AI mandatory capabilities from three EXPOSED original jobs, preserves all four older exposed 8-job cohort B1 and selected role results without new duty/required regressions. Original-language v9 NEW artifacts now PENDING review, verified by live local-model regeneration on a separate cloned source database (0 newly accepted facts). Read-only original-language `jobs source-brief` CLI exposes SHA-linked extracted original evidence and unreviewed candidate role/obligation labels when model v30 fails; not proven exhaustive semantic coverage. Isolated CLI/browser auto corpus exports can no longer mutate the repository root, and a read-only SHA original-description matcher detects duplicates across different job IDs. CURRENT ENGLISH v30 0/3 and translation semantic flaws remain OPEN; even the bounded guidance-only v31 model trial failed and was not promoted. Historical bad original v9 artifacts require review; no automatic retrospective approval/rejection. B5 unseen verification and B6 production rollout CLOSED. Decision: docs/working-memory/2026-11-23_P16_REAL_AD_SOURCE_FIRST_REPAIR_AND_OPEN_SEMANTIC_GATES.md.
**November 15 approved B2 calibration (planning only):** Duty/qualification categories preserve evidence authority without prohibiting work-implied capability relationships. Do not fabricate employer-required prior professional experience or specific tools. Avoid mandatory per-ad micro-labels and extra model rules; evaluate useful context lost versus unsupported requirements. B1 schema and public v30/v9 remain unchanged. Decision: `docs/working-memory/2026-11-15_P16_B2_DUTY_CAPABILITY_RELATIONSHIP_AND_COMPLEXITY_CALIBRATION.md`. B0 private baseline snapshots, 9 original HTML SHA verifications, 59 source assertions and 5 accepted anchors verified; 485 known source-job IDs excluded as first screen; source-only fresh evaluation protocol frozen. No unseen ads or model calls in B0. See `docs/working-memory/2026-11-14_P16_B0_FROZEN_BASELINE_AND_EVALUATION_PROTOCOL.md`. Read `docs/P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md`. B2–B6 remain gated; no new model/semantic/currentness/schema changes authorized. The November 11 capability-expectation next-feature proposal is preserved as a **subsequent** experiment, not an active parallel build. Stage A passive source identity accepted; four-job A1 assistant source/model review complete (59 source assertions, 18 diagnostic flags, 11 translation checks), not independent blind human verification. The user delegated routine review to the assistant; ambiguous employer intent must stay unresolved.

## 2026-11-23 Bounded source-first corrective engineering milestone

2026-11-23 BOUNDED SOURCE-FIRST REPAIR: new opt-in B2v7 candidate recovers 15/15 backend work passages and 5/5 AI mandatory capabilities from three EXPOSED original jobs, preserves all four older exposed 8-job cohort B1 and selected role results without new duty/required regressions. Original-language v9 NEW artifacts now PENDING review, verified by live local-model regeneration on a separate cloned source database (0 newly accepted facts). Read-only original-language `jobs source-brief` CLI exposes SHA-linked extracted original evidence and unreviewed candidate role/obligation labels when model v30 fails; not proven exhaustive semantic coverage. Isolated CLI/browser auto corpus exports can no longer mutate the repository root, and a read-only SHA original-description matcher detects duplicates across different job IDs. CURRENT ENGLISH v30 0/3 and translation semantic flaws remain OPEN; even the bounded guidance-only v31 model trial failed and was not promoted. Historical bad original v9 artifacts require review; no automatic retrospective approval/rejection. B5 unseen verification and B6 production rollout CLOSED. Decision: docs/working-memory/2026-11-23_P16_REAL_AD_SOURCE_FIRST_REPAIR_AND_OPEN_SEMANTIC_GATES.md.

## 2026-11-23 Live real-ad E2E failure — historical baseline

2026-11-23 LIVE SOURCE-FIRST E2E TEST: six public pages fetched, three source-distinct descriptions retained after cross-ID/source-hash dedup; B2v6/B1 mechanics and English v2 translation succeeded on all three, but current v30 failed 3/3 (depth/concept schema twice, dense responsibility coverage once), preventing Capability. One isolated original-language v9 analysis auto-accepted an unsupported required experience concept drawn from a benefit and omitted a skill, so failed source-first semantic review. The research CLI temporarily regenerated tracked corpus files from the isolated DB; original hashes and Git state were restored. NO product code or accepted production state changed. B5 and B6 remain CLOSED. Next work is a review/decision on these findings, not an automatically approved fix or another unseen B5 gate. Decision owner: docs/working-memory/2026-11-23_P16_LIVE_REAL_AD_END_TO_END_SOURCE_FIRST_AUDIT.md.

## 2026-11-22 Latest: B4v6 compact decision-first exposed evaluation

NEW B4v6 compact source-qualified first-view engineering PASS on four previously EXPOSED B4v5 jobs and nine pre-frozen applicant questions: immediately visible evidence 34/64 vs prior 64/64; 19,345 vs 25,259 Markdown characters; all 64 original candidates retained in private drilldown; six questions immediately source-navigable (including one honest no-distinct-duty abstention), three full-duty questions require drilldown. Both unreviewed eligibility candidate graphs, one reviewed terminology overlay and two suppressed old model claims preserved. No provider/source requests, production writes, accepted facts or valid same-source v30 semantic comparison. These are presentation/inspection proxies, NOT measured owner time, independent usefulness, unseen B5 generalization or B6 production promotion. Next: real owner/context-isolated comprehension and reading-burden test against original source and B4v5; freeze calibrated semantics protocol before any further unseen B5. Decision: docs/working-memory/2026-11-22_P16_B4V6_COMPACT_DECISION_VIEW_EXPOSED_RESULT_AND_NEXT_USER_GATE.md.

## 2026-11-22 Latest: calibrated B5 method and B2v6 exposed repair

NEW calibrated (versioned) B5 source-evaluator repair on the FOURTH EXPOSED cohort: original B2v4 failed gate/frozen evaluator remains unchanged; corrected multi-item duty coverage and illustrative-versus-eligibility alternatives eliminate two mis-scored hard stops without hiding B2v4's 12 material category mismatches. New opt-in B2v6 source-evidence candidate matches 73/73 selected fourth role anchors retrospectively, zero critical mismatch or missed duty in that selected review; all 32 B1 bundle validations across four exposed cohorts passed. First exposed cohort still has a material category mismatch and earlier alternative meanings remain unresolved. This is EXPOSED-only engineering, NOT independent generalization, NOT B5 accepted or B6 promoted; accepted English v30/original v9 unchanged. Next: prefreeze corrected future evaluation method and evaluate compact B4v6 decision usefulness, with no automatic fifth cohort. Decision: docs/working-memory/2026-11-22_P16_B5_CALIBRATED_EVALUATOR_AND_B2V6_EXPOSED_REPAIR.md.

## 2026-11-22 Latest: B4v5 exposed usefulness evaluation

Frozen exposed B4v5 usefulness audit REPLAY PASSED (4 previously exposed jobs, 9 diagnostic questions: 5 source-supported visible, 4 partial/uncertain). Archived same-source English v30 produced 0 valid artifacts (3 failed, 1 rejected); one original-language v9 artifact existed. No fair v30 semantic-output accuracy comparison, independently measured user value or time savings is established. Next: predeclared compact, decision-question-first B4v6 source-linked candidate/usefulness trial on already exposed cases; investigate selective bounded local semantics, not another automatic fresh B5 cohort. B5 independent acceptance NOT ESTABLISHED, B6 CLOSED, accepted v30/v9 and downstream facts unchanged. Decision: docs/working-memory/2026-11-22_P16_EXPOSED_USEFULNESS_COMPARISON_RESULT_AND_NEXT_DECISION.md.

## 2026-11-22 Latest: Fourth B5 failure and B2v5 exposed-only result

FOURTH genuine B5 frozen-source gate FAILED on B2v4 (8 jobs, 80 source-first assistant assertions, 56/73 role-comparable matches, 13 role mismatches, 1 missed explicit duty, 1 job with missing alternative scope). No B3/B4/v30 inference; the cohort is exposed. After exposure, B2v5 source-DOM overlay improved retrospective fourth-cohort role matches to 71/73 but retains the missed duty/alternative; all four cohorts are now exposed. B5 semantic acceptance NOT ESTABLISHED, B6 closed, accepted v30/v9 unchanged. Next: bounded exposed-source usefulness/architecture decision, not an automatic fifth fresh cohort. Decision: docs/working-memory/2026-11-22_P16_B5_FOURTH_FAILURE_B2V5_EXPOSED_AND_NEXT_UTILITY_GATE.md.

## 2026-11-22 Second B5 fresh-source failure, versioned B2v3 exposed candidate

SECOND B5 truly fresh eight-source evaluation on 2026-11-22 FAILED on unchanged B2v2 after 91 source-first sealed assistant assertions: 24 role matches, 59 role mismatches, 26 missed explicit-duty assertions and 3 jobs with missing alternative scopes. STOP before any B3/B4/v30 model calls; these eight are NOW EXPOSED. A separately versioned B2v3 generic flattened-heading source candidate retrospectively recovers 79 of 85 comparable role assertions, no missed duty or false mandatory assertions in the selected review, and retains 82 matches on the earlier exposed 8 and B0 2 conditional graphs. Two new jobs still contain uncontained reviewed qualifications; not unseen B5 or production acceptance. Next examine bounded source-grounded semantic interpretation versus escalating regex rules, then only after freezing the candidate obtain a completely distinct third unseen B5 sample; B6 remains unauthorized. Decision: docs/working-memory/2026-11-22_P16_B5_SECOND_FRESH_SOURCE_FAILURE_AND_B2V3_EXPOSED_REPAIR.md.

## 2026-11-22 B5 bounded physical model budget and exposed source-meaning pilot

B5 bounded local inference now enforces real physical HTTP attempt and POSIX wall-clock limits (retries/truncation included); a sealed 5-batch, 10-source-item EXPOSED pilot used 5/7 HTTP attempts, completed in 60.8s within 240s, and retained all source associations. Assistant source-grounded review: 9 individual meanings supported, 1 materially partial technical-term omission (Secure SDLC). HTTP/JSON success is NOT semantic acceptance; none of these are unseen B5, accepted employer facts or B6 promotion. Next freeze a separate full-cohort translation budget and a DIFFERENT unseen 6-8-source B5 cohort. Decision: docs/working-memory/2026-11-22_P16_B5_HARD_LOCAL_TRANSLATION_BUDGET_AND_EXPOSED_MEANING_REVIEW.md.

## 2026-11-21 B5 source-bound translation batching — exposed pilot

B2v2 exposed original-source improvement remains candidate-only. B5 translation batching now has a bounded source-ID/SHA-preserving offline plan (142 Persian items across the eight EXPOSED ads -> 74 PLANNED physical requests at <=3 items/request) and a local two-item pilot (1 batch + 2 single-item controls, 3 actual HTTP completions, both batch/single English results identical). The two preferred source items retain preferred modality in source-owned B1/B2 metadata, not standalone English translations; two B1 alignment source IDs replay. Neither speedup nor unseen linguistic accuracy is established. Model-budget and physical-attempt stop rules must be frozen before any new unseen B5. Current accepted v30/v9, public corpus, database and downstream routes unchanged. B6 promotion unauthorized. Decision: docs/working-memory/2026-11-21_P16_B5_SOURCE_BOUND_TRANSLATION_BATCHING_PREFLIGHT_AND_PILOT.md.

## 2026-11-21 B2v2 versioned source-structure candidate

B2v2 general source-structure candidate is now an exposed-regression engineering milestone: on the frozen eight-job B5 source-first review (93 selected anchors; 86 role-comparable) source-role matches improved 25→82, role mismatches 58→1, missing explicit-duty anchors 19→0, false required 2→0; one-or-more specialties is now recorded as unresolved OR scope, NOT a graph. Four prior B0 jobs retain duty counts and two eligibility graphs. Original B2/B3/B4 history and accepted v30/v9 unchanged. These eight are exposed and CANNOT establish B5 unseen generalization; next obtain a new sealed cohort and paired inference. B6 remains unauthorized. docs/working-memory/2026-11-21_P16_B2V2_EXPOSED_SOURCE_STRUCTURE_REPAIR_MILESTONE.md.

## 2026-11-21 B5 frozen fresh-source gate — BLOCKED upstream B2 source semantics

B5 first frozen fresh-source evaluation was deliberately HALTED (2026-11-21): 8 source-exact Jobinja descriptions were acquired from a metadata-preselected, isolated 2 backend / 3 applied-AI / 3 security cohort; 93 selected original-source assertions were sealed BEFORE candidate inspection. Unchanged B2 mechanically verified all eight but misclassified 58 reviewed role/category anchors, missed 19 explicit-duty anchors, incorrectly marked two preferred skills required and omitted a multi-specialty OR pathway. Seven of eight cases had source-gate issues. This is a STOP, not a B5 accuracy PASS: the eight are now exposed development regressions and a NEW reserved unseen cohort is required after general source-parser repairs. No B3/B4/v30 model calls or accepted data writes; B6 production promotion closed. Decision: docs/working-memory/2026-11-21_P16_B5_UNSEEN_SOURCE_GATE_FAILURE_AND_HALTED_EVALUATION.md.

## 2026-11-19 B4v5 source-qualified exposed presentation milestone

B4v5 read-only source-first presentation PASS on the four previously exposed B0 cases: all 64 selected source items and exact original quotes are available; optional and explicit entry-exam conditions, Middle OR Senior and certificate OR equivalent paths are visible. A source-SHA reviewed Fadak/FDC terminology correction applies only to the new candidate view while the B3 artifact remains immutable; two dependent old model claims are withheld. Both sealed B4v4c and B4v5 replay verifiers PASS, zero new model calls or production writes. The previously reported B3 semantic review missed the named-entity drift and must not be characterized as flawless. **B2/model semantic generalization and B5 unseen verification are OPEN; B6 promotion remains unauthorized.** See docs/working-memory/2026-11-19_P16_B4V5_SOURCE_QUALIFIED_PRESENTATION_MILESTONE.md.

## November 19 B4 bounded job understanding — engineering PASS, semantic gate OPEN

On four previously exposed B0 ads, the candidate-only B4 prototype linked B2 original source items and B3 translations to concise job-level model briefs and a separate source-only fallback. Three local Gemma E4B inference requests yielded two validated **partial candidates** (`tNhZ`, `tNDx`), one rejected model output (`tMps`), and one no-duty **source-only abstention** (`tMjm`, no model request). Four unsupported model fragments were quarantined. All 78 source items, 53 distinct board metadata values and 12 nested eligibility subspans remain traceable. The copied standalone SQLite comparison has four candidate/attempt rows, integrity PASS, no foreign-key violations; 1,085 warnings-as-errors tests passed.

The semantic/usefulness B4 gate remains **OPEN**. The exposed assistant source check found incomplete presentation of optional/conditional expectations, a rejected Middle/Senior alternative-path interpretation, and possible Fadak/FDC ticketing-name translation drift. This review is not independent or blind. No accepted employer fact, production database, downstream authority or public P1.6 route was changed. Direct work continues on `main`. Decision: `docs/working-memory/2026-11-19_P16_B4_PARTIAL_JOB_UNDERSTANDING_ENGINEERING_MILESTONE.md`; safe scorecard: `docs/working-memory/2026-11-19_p16_b4/SAFE_B4_MILESTONE.json`. Repair only supported issues and freeze a candidate before any fresh B5 cohort.

## 2026-11-18 B2/B3 main integration — code integrated, semantic authority unchanged

B2 (`97d5fda`) and B3 (`939f99f`) were fast-forwarded into local `main` from the formerly stacked branches, preserving all 13 commits; both feature-head GitHub Actions were green. These are candidate-only source-engine and bilingual translation modules, not accepted employer-fact or production route promotions. The owner prefers direct development on `main`; B4 useful source-grounded candidate briefs are next. See the dated integration handoff and original B3 bounded evidence.

## 2026-11-18 B3 bounded source-bound translation milestone — PASS for exposed scope

The B3 source-bound translation experiment passed on the four frozen, previously exposed B0 ads. Selection: 78 source items; 64 eligible top-level items comprising 63 Persian translations and one native-English identity. Twelve context-only items and two generic application instructions were excluded. Twelve nested eligibility leaves remain source-bound under their parent clauses without duplicate requests or invented target offsets.

Execution: 63 primary requests plus one evidence-justified corrective request (64/64 total), zero transport retries, zero truncation recoveries, 18,462 prompt and 24,496 completion tokens. All 63 primary requests carried exactly one original source item without heading context; the corrective carried that exact item plus a scoped correction note. All 64 request/response hash pairs were verified. Four B1-compatible bundles pass.

Assistant review covered all 63 Persian translations on this exposed cohort. One primary mistranslation of a personal trait was retained for audit, corrected with the single allowed corrective candidate, and selected with a documented terminology normalization. No material meaning-changing issue remains in the selected translations for these four ads. This is not independent blind human review or unseen generalization.


**Prior accepted P2.3A execution overlay (below):** 2026-11-11.

**Last reconciled:** 2026-11-11
**Current gate:** B2 CLOSED; bounded P2.3A factual comparison ENGINEERING-CLOSED, with a verified frozen-Market navigation repair. Optional overview NO-PROMOTION; owner time savings NOT ESTABLISHED.
**Current focused owner:** `docs/working-memory/2026-11-11_P23A_COMPARISON_STAGE_CLOSURE_AND_NEXT_CAPABILITY_GATE.md`
**Next substantive candidate:** `docs/working-memory/2026-11-11_NEXT_SUBSTANTIVE_CAPABILITY_EXPECTATION_SLICE.md`
**Current status owner:** `docs/CURRENT_STATE_RECONCILIATION_2026-10-10.md`

The October 26 B2 closure and Registry state remain unchanged (12 mapped/23 pending selected responsibility claims; ten concepts, eighteen decisions, one alias). Historical checklists below are superseded for present execution.

## 2026-11-16 B2 native original-item citations — feasible references, SEMANTIC NO PROMOTION

The previously approved **single bounded source-ref native Gemma trial** is now complete. On the same four already-exposed B0 ads, one fixed no-retry `reasoning: off` prompt produced 4/4 structured responses, 75 English claims and 73 valid model-suggested original-item links. The pure source-candidate reconciliation raised 25 warning signals and left 2 claims unlinked; **valid links prove reference location, not employer meaning**. The former baseline v3 produced 85 claims without citations. New inference total 33.606s/2,227 output tokens versus 24.290s/1,627 for v3 (single serial runs; not controlled comparative latency statistics).

Assistant-with-prior-exposure review using the earlier same 12 diagnostic cases: v3 6 pass/2 partial/4 fail, source-ref v4 5 pass/4 partial/3 fail. This is **not independent accuracy**. EDR teamwork moved to preferred, but credentials with unclear strength remain improperly preferred; applicant pentest abilities remain invented duties; work-mode/eligibility alternatives are still confused; Middle/Senior OR and certificate-or-equivalent structure are lost from the alternatives array, and useful LLM/Python work-implied ability is suppressed. No semantic acceptance, automatic reviewer certification or claims of improved user decisions.

**B2 gate remains OPEN_NO_PROMOTION.** Local full suite 1,043 warnings-as-errors tests, Ruff and pip check passed; GitHub CI must be checked at new PR head. Research trial/scorecards are isolated on PR #20; accepted P1.6/translation, downstream authority and main are unchanged. Do not continue prompt-only patches to raise citation counts. The next work is an explicit bounded B2 strategy decision (source-first partial usability vs justified different-model comparison) before any model matrix, B3/B4 promotion, or unseen holdout use.

Decision: `docs/working-memory/2026-11-16_P16_B2_NATIVE_SOURCE_REFERENCES_MIXED_SEMANTIC_RESULT.md`.

## 2026-11-17 B2 bounded source-first candidate milestone — PASS for exposed scope

The deterministic B2 source-item candidate path now passes its **bounded exposed-cohort engineering milestone**. Fresh reproducibility against the exact frozen B0 database confirms 78 exact source items, 53 structured board values, 10 optional work-capability hints, three candidate alternative groups, two candidate eligibility graphs with 11 B1 item leaves, and four typed board/prose conflicts. Duty candidates remain 6/11/5/0 across `tNhZ/tMps/tNDx/tMjm`; the pentesting ad still has **zero fabricated work duties**.

The final missing B1 projection mappings are now present for employer strength, arrangement, experience and compensation. Numeric salary comparison flags only explicit same-currency non-overlapping amounts: the EDR board/prose discrepancy is retained as an unresolved pair; the compatible 30m minimum vs 30–50m range and negotiated salary are not falsely flagged. All conflicts preserve both source-owned values; no source wins automatically.

The source-first candidate milestone is **PASS_BOUNDED_EXPOSED_COHORT**, not accepted employer truth. Categories, strength and eligibility remain `candidate_unreviewed`; no independent accuracy claim, no accepted fact, no downstream authority and no production route change. The model-generated source-reference trial remains research-only because material semantic errors persisted. B2 full semantic generalization remains **NOT ESTABLISHED**; the four cases are exposed, not a holdout.

Safe scorecard: `docs/working-memory/2026-11-17_p16_b2/SAFE_B2_CANDIDATE_MILESTONE.json` (now includes source/schema/code fingerprints). The ignored-local reproducibility runner is `scripts/reconcile_b2_candidate_milestone.py`; its focused tests are `tests/test_reconcile_b2_candidate_milestone.py`. Full decision: `docs/working-memory/2026-11-17_P16_B2_BOUNDED_SOURCE_CANDIDATE_MILESTONE.md`. Next: B3 source-bound item translation under the predeclared 64-item ceiling: 63 Persian requests plus one native identity.

## 2026-11-16 B2 advisory source-link reconciliation — previous diagnostic overlay

Draft PR #20 now has a **candidate-only, offline original-source claim-link reconciliation**. Exact Stage A anchors and model-claim fingerprints verify *where* assistant-supplied links point; no valid citation, model JSON or heuristic source classification proves the actual Persian-to-English meaning. Source-category and obligation mismatches become review signals, not automatic employer-fact verdicts. Unlinked model claims stay unknown instead of meaning "no employer requirements."

Against the **same four exposed** native-v3 job outputs: 85 generated claims, 14 retrospective assistant-selected source links, nine source-candidate disagreement signals, and 71 unlinked claims. Five selected links remain linked/semantically unreviewed. These are **not** independent error rates or scalable automatic grounding: the saved seven-array model answers contain no item references. No new model calls, accepted records, source evidence, current routes or downstream authority. Local full suite now **1030 warnings-as-errors tests passed** with Ruff and dependency checks green; branch PR CI is a separate gate.

**Full B2 still OPEN_NO_PROMOTION.** Next decide a bounded, versioned advisory-model source-link interface only if it offers measurable net source grounding and useful work context without complexity cost. Do not bulk expand heuristics or silently accept linked claims. B3–B6 remain independently gated.

Decision: `docs/working-memory/2026-11-16_P16_B2_ADVISORY_SOURCE_CLAIM_GROUNDING_INCREMENT.md`.

## 2026-11-16 B2 local inference resolved; semantic promotion BLOCKED

Original v1 timed out on first cold/blocked local inference. A warm
unmodified-prompt run finished all four requests but spent ~757/760
tokens on model reasoning with no visible answers. A supported local
native `/api/v1/chat` call with `reasoning: off` produced complete
seven-array JSON for **4/4** frozen exposed Persian sources in ~24 seconds.
One bounded corrective prompt was tried, no per-job retuning.

**Crucial:** source-aware assistant diagnostic review found v2
4 passes/3 partial/5 failures and v3 6 passes/2 partial/4 failures
across 12 selected exposed checks. Both incorrectly upgraded EDR teamwork
to mandatory, inferred preference for uncertain credentials, and
manufactured pentest duties from applicant capabilities. V3 also confused
work arrangements with eligibility alternatives. These are diagnostic
checks, **not independent accuracy estimates**.

The new offline reconciliation verifies model/source/prompt hashes and
assistant-review authority, and records `OPEN_NO_PROMOTION`. No model
claim enters accepted P1.6/Capability/Work/Registry/Market. All **1013**
local warnings-as-errors tests, Ruff and pip check pass. Branch PR #20
remains draft and unmerged. **Next:** minimal candidate-only source
grounding/reconciliation, not more prompt-only iterations or broad new
rules. B3–B6 remain separately gated.

Decision and detailed evidence: `docs/working-memory/2026-11-16_P16_B2_NATIVE_REASONING_OFF_SEMANTIC_COMPARISON_DECISION.md`.

## 2026-11-15 B2 second diagnostic increment — nested graphs, local model blocked

On the existing draft B2 branch, candidate eligibility graphs now represent
exact-source Middle-OR-Senior and certificate-OR-equivalent choices including
within-track AND/OR structure. Two supported graph forms, 11 conditional
source subspan leaves; draft B1 structural/source validation and synthetic
Boolean truth tables pass. **Not independent semantic evidence or accepted
employer eligibility.**

LM Studio local endpoint is accessible after disabling environment proxy;
a fixed four-case Gemma original-context trial began but the **first**
`tNhZ` request timed out after 95.02 seconds without output. Remaining three
calls stopped to respect latency budget. **No semantic model comparison is
established.** Do not add excessive grammar/prompt complexity to compensate.
Production and frozen B0 evidence unchanged; PR remains draft and B2 gate OPEN.

Record: `docs/working-memory/2026-11-15_P16_B2_NESTED_ELIGIBILITY_AND_LOCAL_MODEL_PROBE_RESULT.md`.

## 2026-11-15 P1.6 B2 first diagnostic increment — full gate still OPEN

A dedicated branch implements source-version-bound, read-only source item
candidates and source-labeled Jobinja board value reconciliation. First four
exposed ads produced 78 original candidate items, 53 board value references,
10 optional source-linked operational capability hints and 3 original
alternative-group candidates. All anchor and board hashes and a conservative
B1 draft structural projection validate on an isolated frozen B0 SQLite copy.
The four earlier exposed B1 references intersect compatible candidate
categories/strengths (30/30), but this is **not** independent accuracy evidence.

20 focused tests; 966 full warnings-as-errors tests, Ruff and pip check
passed locally. Zero model calls, no new acquisition, no accepted P1.6,
Capability, Work, Registry or Market mutation. **Nested alternative-group
semantics, full coverage, unseen generalization and useful model-based
disambiguation remain unproven; B2 is not approved for production.**

Detailed record: `docs/working-memory/2026-11-15_P16_B2_SOURCE_ITEM_DIAGNOSTIC_FIRST_SLICE_AND_OPEN_GATE.md`.
Implementation branch: `feature/p16-b2-source-items-metadata-2026-11-15`.
Keep B3–B6 separately gated. Prefer justified semantic improvements over
extra mandatory regex/prompts; retain the November 15 duty/capability
calibration.

## 2026-11-14 Stage B1 completion handoff (historical; B2 diagnostic in progress)

**B1 design selected:** source-exact Stage A anchor reuse, separate
versioned JSON Pointer/hash reference for board metadata, explicit
provisional classification/obligation/conditional scope, rooted AND/OR
eligibility graph, per-item translation association distinct from semantic
meaning, append-only review provenance and no durable authority from
schema-valid candidate facts.

The draft JSON Schema, four previously exposed source-safe A1 examples
(30 original fragments, 5 structured fields, 2 AND/OR eligibility graphs),
a pure non-production validator and unit tests are recorded. Source
identities were checked against local private B0 evidence; all public
fixtures omit full original employer descriptions. B1 introduced no model
calls, no new ads, no source-version changes, no database migrations and
no public P1.6 analysis route.

**Decision/ADR:** `docs/working-memory/2026-11-14_P16_B1_SOURCE_ITEM_BILINGUAL_CONTRACT_ARCHITECTURE_DECISION.md`.
**Next task:** B2 read-only deterministic original item/metadata candidate
in a new branch from accepted main, tested against exposed sources and
general counterexamples. No accepted source or downstream mutation.
B3–B6 remain separately gated; no unseen generalization evidence exists.

## 2026-11-14 current Stage B handoff (B0 accepted; B1 next)

**Plan-authority decision:** `docs/P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md`.
B0 baseline/snapshot/evaluation protocol PASSED on November 14. B1 contract/ADR is the next action;
B2 original-source classification, B3 bilingual meaning, B4 candidate
job-understanding, B5 independent fresh case verification and B6 controlled
production integration follow only after their respective acceptance gates.
The previous November 11 next capability-expectation proposal remains valid
but is downstream in sequence. Existing B2/Market and P2.3A /compare remain
closed/accepted as documented.

Current production English P1.6 remains v30/v5, original v9/v4 and translation
v2. The accepted Stage A source anchor is passive; experimental v31 and the
heuristic original-language source-section and item-model translation code
remain unmerged. No new Stage B artifact or source fact has been accepted.

**Immediate operator instruction:** start B1 on a separate branch from current main; reuse frozen B0 original-source/evaluation evidence, design item/obligation/translation alignment and review-state contracts with an explicit ADR, test sample schemas and compatibility before any B2 runtime code. B0 contains no captured fresh unseen cohort; that is reserved for B5. User involvement
only for consequential owner decisions; employer ambiguity stays unknown.

## Current execution

- [x] B2 reviewed normalization and bounded Market/report acceptance remain closed.
- [x] Deliver/verify `/compare` factual accepted evidence, depth/obligation versus duties, and source links.
- [x] Repair loss of frozen-Market context for a second compared snapshot member, without assigning provenance to unrelated jobs.
- [x] Independently check live snapshot-15/report-2 navigation with structural probes and desktop/mobile Chromium.
- [x] Archive the optional summary prototype as **NO PROMOTION** with owner time savings explicitly unmeasured.
- [x] Close the bounded comparison engineering/optional-UX investigation; no repeated cosmetic test backlog.
- [ ] Historical next candidate DEFERRED IN SEQUENCE until Stage B qualifies: capability-expectation reuse/gap audit for `tvMm`, `tNVe`, `t7Ay`.

No Strategy-C inference, P2.3 persistent profiles, P2.2C/D, P2.4, personal scoring, bulk mappings, or historical accepted-artifact regeneration is authorized by this closure.

## Historical October 17 handoff/checklist

The remaining sections retain the former checklist as history. Their present-tense B2-active/application-pending and P2.3-not-authorized wording is superseded by the October 26 focused decision above. They do not instruct a new live application or reverse the bounded browser authorization.

## 1. Read this first

Stable authority:

1. `AGENTS.md`
2. `README.md`
3. `docs/PRODUCT_SPECIFICATION.md`
4. `docs/ARCHITECTURE.md`
5. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
6. `docs/SOURCE_POLICY.md`
7. `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`
8. `docs/ROADMAP.md`
9. `docs/IMPLEMENTATION_PLAN.md`
10. `docs/CURRENT_STATE_RECONCILIATION_2026-10-10.md`
11. `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`
12. `docs/EXECUTION_TODO.md`

Current focused records:

- `docs/working-memory/2026-10-10_PHASE2_SEMANTIC_DIRECTION_RECONCILIATION_DECISION.md`
- `docs/working-memory/2026-10-17_P2_2B_B2_R3_SEMANTIC_DECISION.md`
- `docs/working-memory/2026-10-17_P2_2B_B2_R4_R6_SEMANTIC_DECISIONS.md`
- `docs/working-memory/2026-10-17_POST_B2_P2_2C_VS_P2_3_READINESS_PREDECISION.md` — contingent analysis only; no authorization while B2 remains open.
- `docs/working-memory/2026-10-17_P2_3A_TECHNICAL_FEASIBILITY_AND_REUSE_AUDIT.md` — contingent technical supplement; no P2.3 implementation authorization while B2 remains open.
- `docs/working-memory/2026-10-10_MARKET_R4_FINAL_LOCAL_ACCEPTANCE.md`

Historical entry/evidence records remain available but do not override the current-state overlay.

Permanent boundary:

```text
SOURCE FACT
!= NORMALIZED CORRESPONDENCE
!= ANALYTICAL INTERPRETATION
!= RECOMMENDATION / DECISION SYNTHESIS

GENERATED / CANDIDATE
!= REVIEWED / PROMOTED
```

---

## 2. Current accepted product state

```text
Phase 1                              CLOSED / ACCEPTED
P2.1 Canonical Registry             CLOSED / ACCEPTED
P2.2A Job Work Intelligence v2      CLOSED / ACCEPTED
P2.2B-B1                            CLOSED / NO-PROMOTION / DEFER
P2.2B-B2                            ACTIVE / AUTHORIZED
P2.2C promoted families             NOT AUTHORIZED
P2.2D stable archetypes             NOT AUTHORIZED
P2.3 capability profiles            DEFERRED / NOT AUTHORIZED
P2.4 Market v2                      DOWNSTREAM / NOT AUTHORIZED
Blueprint v6                        EXPERIMENTAL / NON-AUTHORITATIVE

Market foundation                   PASS / COMPLETE
Market I1-I7                        ACCEPTED / CLOSED FOR BOUNDED SCOPE
Same-target coverage follow-up      COMPLETE
Candidate interpretation v6         ACCEPTED / CLOSED FOR BOUNDED REPORTING
RoleFamily report R1-R4             ACCEPTED / CLOSED
Market → You                        LATER / NOT AUTHORIZED
```

Current primary contracts:

```text
parser                         jobinja-detail-v2
translation                    lm-studio-translation-v2
English projection             english-projection-v2
English P1.6 generation         job-analysis-english-v30 / job-analysis-v5
Original P1.6                   job-analysis-original-v9 / job-analysis-v4
Capability                     job-capability-intelligence-v9 / job-capability-intelligence-v5
Canonical Registry             jobhunter-canonical-concept-registry-v1
Job Work Intelligence          job-work-intelligence-v2 / job-work-intelligence-v2.0
Market membership              market-membership-v1 / market-membership-v1.0
Market snapshot                market-corpus-snapshot-v1
Market aggregate               market-aggregate-profile-v1
Public Corpus                  jobhunter-public-corpus-v1
Candidate generator            market-role-family-candidate-v6
Role-family report             market-role-family-intelligence-report-v1
Role-family report review      market-role-family-report-review-v1
```

---

## 3. Closed Market/report substrate

Snapshot-15 accepted P1.6 factual set:

```text
tvMm  artifact 50  responsibilities 11  requirements 25
t7ck  artifact 52  responsibilities  0  requirements 18
tmvA  artifact 61  responsibilities  7  requirements 22
tjgi  artifact 60  responsibilities  9  requirements 25
t7Ay  artifact 62  responsibilities  0  requirements 26
tNVe  artifact 56  responsibilities  8  requirements 24

responsibilities 35
requirements    140
total claims    175
```

`t7ck` and `t7Ay` contribute no direct responsibilities and cannot create duties from requirement-only evidence.

Final accepted `RoleFamilyIntelligenceReport`:

```text
report id                         2
snapshot                          15
model                             gemma-4-e4b-it-ud
available claims                 175
cited claims                      27
work clusters                      4
multi-posting subfamilies          1
singleton specialties/outliers     2
integrity rejections               0
review state                      accepted_for_bounded_use
```

Candidate/report interpretation remains analytical, not taxonomy authority.

---

## 4. Phase-2 direction

Direction comparison:

```text
A  P2.2 responsibility/deliverable normalization and later family semantics
B  P2.3 corpus-scale capability requirement profiles
C  P2.4 Market v2
```

Current controlling decision:

```text
A selected at P2.2B level
B deferred, not rejected
C downstream
```

Reasoning remains in `docs/working-memory/2026-10-10_PHASE2_SEMANTIC_DIRECTION_RECONCILIATION_DECISION.md`.

A separate contingent readiness analysis now exists for the mandatory **post-B2** decision. It recommends, if B2 closes cleanly:

```text
P2.3A bounded Job Capability Requirement Profile foundation  SELECT NEXT
P2.2C promoted ResponsibilityFamily implementation           DEFER, NOT REJECT
P2.4 Market v2                                                REMAINS DOWNSTREAM
```

The technical reuse audit refines the likely first step further: if P2.3A is later authorized, begin with a bounded **P2.3A-0 composition/reuse experiment** comparing deterministic P1.6+Registry projection, optional reuse of already-accepted Capability-v9 organization, and only-if-needed bounded reuse of Capability-v9 grouping machinery. Do not start by creating another persistent inference subsystem.

This is **not current authorization**. B2 local application/verification and closure must happen first. See `docs/working-memory/2026-10-17_POST_B2_P2_2C_VS_P2_3_READINESS_PREDECISION.md` and `docs/working-memory/2026-10-17_P2_3A_TECHNICAL_FEASIBILITY_AND_REUSE_AUDIT.md`.

---

## 5. P2.2B-B2 semantic review — COMPLETE

Objective:

```text
accepted/current P1.6 responsibility claims
→ bounded candidate cross-job correspondence
→ explicit semantic review
→ existing P2.1 Registry reviewed responsibility concept + exact immutable claim mappings
```

Decisions:

```text
R1  responsibility:design-implement-ai-agents
    tvMm 50[0] ↔ tNVe 56[0]
    ACCEPTED / APPLIED / VERIFIED

R2  responsibility:integrate-ai-systems-with-services
    tvMm 50[2] ↔ tNVe 56[2]
    ACCEPTED / APPLIED / VERIFIED

R3  responsibility:implement-llm-tool-calling
    tvMm 50[3] ↔ tNVe 56[3]
    ACCEPTED / LOCAL APPLICATION PENDING

R4  responsibility:develop-rag-systems
    tvMm 50[6] ↔ tNVe 56[4]
    ACCEPTED / LOCAL APPLICATION PENDING

R5  responsibility:design-develop-multi-step-ai-workflows
    tvMm 50[7] ↔ tNVe 56[5]
    ACCEPTED / LOCAL APPLICATION PENDING

R6  responsibility:evaluate-improve-ai-system-performance
    tvMm 50[8] ↔ tNVe 56[7]
    ACCEPTED / LOCAL APPLICATION PENDING
```

Important semantic limits:

- R3: `Structured Output` remains specific to `tNVe`.
- R4: the original tentative `develop-rag-knowledge-retrieval` identity was narrowed to `develop-rag-systems` because `Knowledge-based systems` and `Knowledge Retrieval` are not equivalent; only the common RAG-development core is normalized.
- R5: `reliable` remains specific to `tvMm`; Multi-Agent/Email/Ticketing/module integration remains specific to `tNVe`.
- R6: `debugging` remains specific to `tvMm`; quality/reliability/latency/cost remain explicit `tNVe` dimensions.
- `tvMm` 50[9] remains pending because “paying attention to” operational qualities does not assert the same evaluate/improve action.
- broader R1/R2 boundary claims remain pending.
- no R3-R6 aliases are authorized.

Current proven local Registry state remains **4/35 mapped, 31 pending** from R1/R2 only. If all eight R3-R6 claims remain accepted/current and pending, successful application is expected to produce **12/35 mapped, 23 pending**. Do not represent that expected state as current until local verification proves it.

---

## 6. Exact continuation sequence

```text
B2.1 baseline COMPLETE

B2.2 semantic review COMPLETE
   - R1-R6 reviewed individually
   - R1/R2 applied + verified
   - R3-R6 accepted semantically

B2.3 local Registry application NEXT
   - pull current main
   - fresh SQLite backup
   - integrity + foreign keys
   - reconfirm exact pending/current R3-R6 claims
   - create/reuse exactly four accepted concepts
   - map exactly eight approved claims
   - no aliases
   - leave tvMm 50[9] and broader R1/R2 boundaries pending

B2.4 verify
   - exact-command idempotency
   - CLI/browser same reviewed state
   - SQLite integrity/foreign keys
   - R1/R2 + unrelated Registry rows preserved
   - accepted P1.6 / Market unchanged
   - public corpus unchanged by Registry mutation

B2.5 close bounded tranche
   - record exact local row identities + proof
   - record pending boundary claims
   - state normalized correspondence != ResponsibilityFamily != prevalence
   - close B2
   - STOP
   - separate P2.2C vs P2.3 readiness decision
```

Exact commands and verification requirements:

`docs/working-memory/2026-10-17_P2_2B_B2_R4_R6_SEMANTIC_DECISIONS.md`

Do not start P2.2C, P2.2D, P2.3, P2.4, Blueprint authority, personal scoring, bulk mapping, or a new model-review loop during B2.

---

## 7. R1/R2 applied evidence

R1 applied `responsibility:design-implement-ai-agents` with mappings #7/#8 to exact artifact 50/56 responsibility[0] claims. R2 applied `responsibility:integrate-ai-systems-with-services` with mappings #9/#10 to exact artifact 50/56 responsibility[2] claims.

R1 exposed a narrow Registry write-validator defect for accepted-compatible historical P1.6 artifacts; commit `dafdb05` aligned Registry persistence with the accepted v20/v21/v23/v28/v30 v5 compatibility boundary. Ruff, 843 warnings-as-errors tests and normal CI passed before live application. R1/R2 idempotency, CLI/browser agreement, SQLite integrity/foreign keys, other-table preservation and corpus-hash preservation passed. Local backups/results remain ignored under `data/local-acceptance/b2-review-2026-10-16/`.

No later semantic decision changes those exact R1/R2 rows.

---

## 8. Public corpus / reconciliation state

The owner published the previously local `tNpG` source/detail and English projection on 2026-10-17. Current committed repository-safe counts:

```text
jobs                 420
parsed details        52
English projections   30
accepted English P1.6 11
Capability artifacts   5
```

`tNpG` adds no accepted P1.6, Capability, Registry mapping, or Market authority.

The October 15 statements that `tNpG` was unpublished or that all 35 B2 responsibilities were pending are historical checkpoint facts only.

---

## 9. Usability direction

Owner-selected friction: understanding/comparing jobs or Market findings.

Delivered first bounded UI slice:

- research-first Overview;
- navigation grouped into daily research versus management/processing;
- accepted-fact job preview before full source/translation documents;
- frozen role/company evidence labels;
- validated snapshot/report/finding return context through job/Work/Capability reading;
- explicit current-versus-historical source distinction.

Verification included Ruff, 834 warnings-as-errors tests, and a real Edge/Playwright journey on a SQLite copy across desktop and 390px viewport. Subjective repeated-use usefulness remains owner feedback, not mechanically proven acceptance.

No job-comparison feature or new semantic authority layer was added.

---

## 10. Current stop lines

Do not:

- create `ResponsibilityFamily` or stable `RoleArchetype` entities during B2;
- bulk-map the remaining snapshot responsibilities;
- canonicalize requirements in this tranche;
- start P2.3 capability profiles or P2.4 Market v2;
- use Blueprint as authority;
- add personal readiness/gap/scoring;
- publish local Registry/Market/Work state into `corpus/`;
- add new model-review loops merely to obtain promotion;
- treat accepted R1-R6 correspondences as market prevalence.

---

## 11. Exact next action

```text
R1/R2 applied + verified
R3-R6 semantic review complete / accepted
→ execute combined R3-R6 local Registry application protocol
→ verify idempotency + CLI/browser + integrity/FK + preservation
→ update current state to proven post-application counts
→ record B2 closure
→ STOP
→ formal post-B2 direction decision
   - re-read the contingent pre-decision and technical reuse audit against proven local state
   - if no material contradiction: select P2.3A and defer promoted P2.2C
   - if P2.3A is selected: run P2.3A-0 composition/reuse experiment before defining persistent profile state
```

GitHub cannot claim the R3-R6 SQLite rows exist because the maintainer runtime database is intentionally local and excluded from the repository.
