# P1.6 evolution E1 — root-cause investigation, initial evidence and architecture trace

**Date:** 2026-11-24
**Scope:** E1.1–E1.3 only; intermediate investigation record, not E1 closure.
**Base:** `962611a405d22374159237e29bfe753d8e61e0fb` (main); unchanged production contracts.
**Disposition:** Governance map, active execution ownership and primary exposed diagnostic inventory established. Next E1.4 (depth/concept failure replay). E1.5–E1.11 and V9 remain open.
**Authority:** [Evolution tracker](../P16_SEMANTIC_ARCHITECTURE_EVOLUTION_PLAN.md); [Stage B plan](../P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md); [Nov 23 repair/Nov 24 reconciliation](2026-11-23_P16_REAL_AD_SOURCE_FIRST_REPAIR_AND_OPEN_SEMANTIC_GATES.md). Owner authorized the investigation-first sequence, not a new production contract.

## E1.1 — Requirements, constraints and governing owners

Review relevant sections of README, AGENTS, product specification, architecture, domain model, source policy, utility/epistemic policy, roadmap/master plan/current-state overlay, Stage B plan, B1 ADR (Nov 14), duty/capability calibration (Nov 15), November 11 comparison closure and deferred capability proposal, Stage A/B0 records, recent B2–B5 and live-audit decisions. The governing policy already supports the intended direction; no permanent rule amendment is needed to conduct E1.

| Requirement / decision | Governing source | Concrete owner / consequence |
| --- | --- | --- |
| Original source is authority; acquire before inference, separate semantic version and observation | Product FR-2/4/5/6; architecture §§7–10; source policy | Jobinja detail service, storage and translation store, Stage A span identity; never alter source to fit model |
| English is a derived view, not new source authority | Product FR-7/8; domain §5; architecture §10; source policy §§12–13 | TranslationService, projection v2; original-to-target fidelity separate from identity; alternative semantic routes remain experiments |
| Durable evidence-backed requirements and strength/depth separation | Product FR-10/11/13; architecture §11; domain §6 | P1.6 v30/v5 pending English and original v9/v4 pending for new generation; exact dependencies and review fence |
| Useful inferred ability from assigned work without invented employer eligibility | Product FR-11A; domain §6; Nov 15 calibration | Capability interpretation may relate to duties; do not equate prior paid experience with ability or expand frameworks without evidence |
| Strictness proportional to authority and blast radius | Utility policy §§3,5,6,12; architecture §§11–13,24–25 | Fail hard on identity/fabricated source/persistence/privacy; allow qualified uncertainty/partial candidate; accepted-only consumers retain strong fence |
| Original item identities, board values, conditional alternatives and orthogonal review dimensions | B1 ADR §§3–7; Stage B §0 | OriginalSourceAnchor vs board JSON Pointer; category/strength/scope separate; source integrity, association, linguistic fidelity, classification, reuse authority distinct |
| Source-first candidate sidecar, B5/B6 gates and local privacy/budget | Stage B §§0,2,4; source policy §§12–18; latest repair | Local LM Studio only in this experiment; candidate-only B2/B3/B4; no accepted reuse or automatic rollout |
| Subsequent roadmap priority | Roadmap, master plan §2.1, Nov 11 closure/proposal and Nov 24 tracker | P2.3 capability-expectation work deferred; B5 independent gate not accepted; B6 closed |

### Settled vs open and real tensions

1. **Settled:** do not discard evidence spine, immutable source and artifact history, SQLite, acquisition, privacy and currentness. LLM interpretation is expected, not an exception. Explicit employer requirements and work-implied abilities can coexist. Category assignment need not prohibit semantic relationships. Review granularity and authority are separate. No blanket weakening of evidence guards.
2. **Concrete current-vs-candidate semantic tension:** `analysis_runtime_v20._v20_deterministic_structured_skills` (line 45, used in active inherited v20 runtime line 355 and persistence replay) materializes skill tags as required with high confidence. B1 ADR §3C explicitly forbids a board value alone establishing employer-required strength. These are different contracts, not permission to silently reinterpret existing artifacts. Prior optional-vs-board conflict is a documented real defect (Stage B A1). E1.7/E2 must examine safe provenance separation and accepted compatibility.
3. **Translation dependency vs meaning:** domain §5.4 requires traceability to original; v30's current evidence contract uses the derived English fields, and v2 can be field-only unaligned. B1 introduces original item binding but does not fix linguistic fidelity. The gap is real; it is not proof that native-language inference is superior. E1.8 tests the mechanism.
4. **Representational failure vs policy:** architecture §11 already allows malformed/unscoped optional depth to normalize to unknown where the concept/evidence remain valid and explicit degree is not erased. Yet Nov 23 v30 rejected two artifacts for depth words embedded in concepts. These are not necessarily the same situation. E1.4 must establish whether a safe normalization exists at the actual failing validator, not assume that it does.
5. **Status/routing documentation drift:** architecture §10 describes earlier source-section and per-item translation as separate research; current main includes integrated candidate modules but not production activation. The original-language v9 route docstrings/older ADR wording mention historical acceptance; Nov 23 guard and latest status control new pending generation. Master plan older B5 table summarizes an earlier failure and contains old separate-branch wording; the Nov 24 tracker and AGENTS main-branch instruction control present execution. Preserve historic text, avoid treating these as fresh authorization; reconcile durable wording in E2.6 or sooner if misleading current behavior. No production mutation here.
6. **Unknown:** whether observed failures are principally model capacity, model-facing representation, lost context, partition ownership, translation, filters, retries, or a combination. No causal claim yet.

## E1.2 — Active architecture and historical component ownership

### Current runtime trace at base

The following was checked by source inspection and Python method-resolution-order inspection in the installed WSL environment, not inferred from version names.

| Layer | Active module/function boundary | Output/authority |
| --- | --- | --- |
| Source | `jobinja_detail_service.JobinjaDetailService.fetch`, `_semantic_sha256`; storage persists parsed job_detail_versions with raw evidence/content SHA and semantic SHA | Source-derived records; parser `jobinja-detail-v2` |
| Translation | `translation_store.TranslationStore.latest_source_version`; `translation_service.TranslationService._translate_source/current_artifact`; collect translatable texts, local provider, `translation.projection.build_english_projection`, require_translation_integrity, record artifact and attempt | v2 projection identity tied to exact source; translation does not assert semantic equivalence |
| Public routing | `analysis_current.build_job_analysis_service` -> `analysis_runtime_v30.build_v30_analysis_service` or original `analysis_runtime.build_job_analysis_service` | English v30/v5, original v9/v4; CLI/browser share public route |
| English orchestration | `JobAnalysisServiceV21.analyze_english_job` (wrapper) -> `JobAnalysisServiceV20.analyze_english_job` | Require latest parsed source and current English projection; exact artifact lookup by dependency/model/prompt/schema; call provider, validate v17 structured/evidence, persist pending or record failure |
| Provider plan | `V27CandidateAnalysisProvider._run_once` inherits additional-plan ownership then delegates; v20 engine handles source-led partitioning; `V26CandidateAnalysisProvider._requirement_coverage_plan`, `V21CandidateAnalysisProvider._responsibility_coverage_plan`, `V25CandidateAnalysisProvider._requirement_partitions` | Inherited coverage/ownership rules, not a simple whole-document extraction |
| Model call | `V30CandidateAnalysisProvider._complete_partition` -> `inference.instructor_lm_studio_v24.complete_analysis_partition_with_instructor_v24` with v30 response model and partition refs -> `analysis_runtime_v23._filter_unassigned_partition_claims` | Model output locally schema-validated and scoped; distinct potential loss points |
| Persistence | `JobAnalysisServiceV28._persist_analysis` -> `analysis_persistence_v23.persisted_analysis_v23` using `persisted_qualification_plan_v28`; `V23CandidateAnalysisProvider._persistable_structured`; `analysis_store.AnalysisStore.record_artifact/record_attempt/review_current` | Pending generated artifacts; failures recorded, rejected history archived; original route now pending for new v9 |
| Diagnostics | `analysis_failure_diagnostics`, attempt rows and bounded completion evidence | Failed response data not accepted artifact; E1.4–6 replay inputs |
| Consumers | `capability_service_v9` inherits v8 dependency gate; `capability_service_v8._current_dependencies`; `work_intelligence_service._current_p16`; `market_insights` accepted-only selector | Accepted current English required for semantic capability/work/market facts; source-level market membership is separate |
| Source-first alternative | `source_span_identity.bind_original_source_span/verify_original_source_anchor`, `source_item_candidate_b2_v7_dom.interpret_original_source_candidate_v7`, B1 contracts, B3 `make_b1_source_bound_alignment`, B4 `build_b4_evidence_bundle/build_b4_model_payload/validate_b4_model_response/build_source_only_brief`, B4v6 `build_compact_decision_view`, `source_brief_cli.source_brief` | Opt-in read-only/candidate only; original evidence and partial view can exist with no valid v30; no accepted-only substitution |

### Observed inheritance and evolution

- Service MRO (project classes): V30 → V29 → V28 → V27 → V26 → V25 → V24 → V23 → V22 → V21 → V20 (11).
- Provider MRO: V30 → V29 → V28 → V27 → V26 → V25 → V24 → V23 → V21 → V20 → V19 → V18 → V17 → V16 → V15 → V14 (16).
- Response MRO: V30 → V29 → V27 → V25 → V23 → V22 → V21 → V20 → V19 → V17 → V14 → JobAnalysisResponse → _StrictModel. Requirement MRO separately inherits multiple validators (V30 through V29/27/25/23/22/21/20/19/14/base). v30 itself is a small explicit prior-experience amendment, not the entire system. v20 introduced source-led bounded partitions and deterministic board-tag ownership; v21 scoped evidence and diagnostic capture; v23 scoped item references and filtering/persistence; v24 scoped inference; v25 partition changes; v26 mixed preference/context ownership; v27 inherited additional-plan ownership; v28 persistence plan; v29/v30 schema/ontology amendments. These are trace-level labels, not exhaustive historical performance judgments. E1.6 must examine assembled schema/prompt/validation burden and historical successes/failures. Accepted v20/v21/v23/v28 compatibility remains intentional.
- Stage A passive exact spans -> B1 typed contracts -> B2v1–v7 increasingly source-structure/DOM-aware candidates -> B3 bound item translation and budgeted batching -> B4 partial source-linked presentation -> B4v5 source-qualified projection -> B4v6 decision-question compaction -> latest original-language source-brief. All preserve distinct authority; repeated exposed repairs are not independent B5 acceptance. B0 four A1 and five accepted anchor records, four failed prospective B5 cohorts, Nov 23 audit and failed guidance-only v31 diagnostic are the primary evidence history. The v31 prompt-only experiment failed and was not shipped (Nov 23 decision).
- **Finding:** deep inheritance makes active ownership nonobvious and is a maintainability/diagnostic risk. It is not evidence by itself of excessive model-facing complexity or a causal explanation of failed inference. No recommendation to flatten the code until E1.6/E2.

## E1.3 — Retained diagnostic evidence inventory

Actual local read-only verification on WSL with installed Python and SQLite query_only. See [public-safe receipt](2026-11-24_p16_evolution_e1/SAFE_E1_EVIDENCE_INVENTORY.json). Full private per-case IDs, hashes and diagnostic metadata in ignored `data/local-acceptance/p16-evolution-e1-2026-11-24/PRIVATE_E1_EVIDENCE_INVENTORY.json`. Reproduce from repo root:

```bash
.venv/bin/python data/local-acceptance/p16-evolution-e1-2026-11-24/verify_evidence_inventory.py
```

The helper reads existing snapshots by original manifest hashes, recomputes original parsed semantic hash and exact original HTML SHA, joins job/source/translation/attempt/artifact dependencies, recomputes canonical translation projection hashes and accepted-anchor analysis/capability payload hashes, checks SQLite integrity/FKs, hashes sealed reviews/gates into the inventory and checks the production database/corpus baseline. It emits only counts/hashes publicly. Local source-only review hashes are inventory fingerprints; not a claim of new independent review. The private verifier and receipt remain ignored; no raw source, job identifier, prompts, model text, DB or personal evidence committed.

| Evidence set | Verified result |
| --- | --- |
| Four prior B5 frozen original-source snapshots | 8 source versions per cohort, 32 total; all snapshot hashes match; raw HTML and parsed semantic hashes match, zero translation and analysis attempts on those 32 selected rows in the original source-only snapshots. Review and frozen gate receipt fingerprints recorded. All four remain exposed. |
| B0 frozen baselines | 3 SQLite snapshot hashes and integrity/FKs match; 5 accepted anchors including original/translation/analysis/capability hashes and dependency IDs; 4 exposed A1 originals and recorded translation identities. Accepted anchors include dense/sparse development cases. |
| Nov 23 real-ad cohort | 3 selected source versions and translations; 4 analysis attempts (3 failed v30, 1 original v9), 6 bounded diagnostic rows retained; exact original receipt and both manual review document hashes match; isolated DB matches frozen receipt. |
| Isolation | Production DB and public corpus manifest hashes match previously frozen baseline; no new source or LLM requests; no accepted artifact modifications. |

**Limits and next evidence gaps:** These are 44 source-version checks across retained sets (not asserted to be 44 unique independent jobs), not a new accuracy denominator. Original B5 source-only snapshots intentionally contain no generation attempts for selected sources; later exposed translation/model probes are separate. B0 v31 trial snapshot hash and integrity verified, but individual historical failed-trial outputs remain for E1.6. Bounded failure diagnostics can lack full raw request/response and partition context; E1.4/5 must identify availability per attempt before attributing causation. No new source or model calls; token/latency measurements N/A. No new semantic judgments from hash checks. Existing frozen evidence not rewritten.

## Continuation

E1.1–E1.3 completed for the initial trace/inventory scope; E1 overall remains open. Next E1.4: replay both depth/concept failures with retained completions, actual inherited validators and exact source-local degree/obligation/experience checks. Establish whether each error is representational, semantic, evidence-related or mixed, and whether normalization can preserve meaning. E1.5 then traces dense duty coverage. Do not start E2 architecture selection, new inference, B5 or B6 yet. V9 historical acceptance review remains an independent pending track. No product code or contracts changed; this is an investigation/documentation increment only.
