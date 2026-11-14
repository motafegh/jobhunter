# P1.6 Stage B — Source-grounded bilingual job understanding
## Authoritative focused implementation plan and acceptance gates

**Date:** 2026-11-13
**Disposition:** Stage B focused plan active; B0 baseline/protocol accepted 2026-11-14; **B1 contract design NEXT**, no new semantic/runtime contract promoted
**Current accepted baseline:** main `8eded9e15949fc34a041984a90e40d930f91f6fd` (Stage A passive evidence identity accepted)
**Current English P1.6:** `job-analysis-english-v30 / job-analysis-v5`
**Current original-language P1.6:** `job-analysis-original-v9 / job-analysis-v4`
**Current execution status:** B0 PASS (read-only backups, 4 exposed sources, 5 accepted anchors, 485 known exclusions, no unseen cohort yet); B1 NEXT. B0 record: §docs/working-memory/2026-11-14_P16_B0_FROZEN_BASELINE_AND_EVALUATION_PROTOCOL.md`.
**Priority:** Material source-fidelity recovery before the previously proposed job-specific capability-expectation slice. That earlier P2.3 candidate is **deferred in sequence, not cancelled or disapproved**.
**Scope:** Job-level source-to-translation alignment, factual and obligation quality, useful candidate output, evidence-qualified acceptance and eventual bounded rollout. **Not** P2.2B-B1/B2, which are separate previously closed work programs.

### Decision in one paragraph

Implement an opt-in, **original-source-owned, bilingual evidence candidate pipeline** that ties each consequential job claim to exact original-language text; distinguishes duties, qualifications, optionality, mutually alternative eligibility, arrangements and unresolved meaning; preserves translation-to-source association without mistaking association for linguistic correctness; prevents structured board metadata from silently creating mandatory employer requirements; and offers bounded useful job understanding even when full P1.6 generation fails. Initially persist/run only in isolated diagnostic state and retain v30/v9 as authoritative production behavior. Allow staged promotion only after source-integrity, semantic-evaluation, usability, dependency, privacy and rollback gates. No automatic acceptance of AI-generated employer facts and no requirement for the owner to manually audit every job.

---

## 0. Authority, reasoning policy, and fixed boundaries

This is the **focused Stage B execution owner** after the accepted Stage A foundation. Its scope and sequencing are reconciled into `docs/ROADMAP.md`, `docs/IMPLEMENTATION_PLAN.md`, the current-state overlay, `docs/EXECUTION_TODO.md`, and `docs/WORKING_MEMORY.md`. Those controlling product/domain/source/architecture/reasoning documents remain superior to this focused plan. An individual B-slice result cannot amend those invariants by implication.

Read the governing owners in the order in `AGENTS.md`, especially `PRODUCT_SPECIFICATION.md` FR-4/5/7/10/11/13, `DOMAIN_AND_ANALYSIS_MODEL.md` §5/6/13–15, `ARCHITECTURE.md` §3–11/24–25, `SOURCE_POLICY.md`, `UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md` §3–10, and `TRANSLATION_AND_ENGLISH_CORPUS.md` §19. Then read this plan, the November 13 research/owner audit and the specific module before changing it.

**Protected currentness and downstream invariants:**

1. Source evidence remains immutable and authoritative; `jobinja-detail-v2` parsed source versions, raw acquisitions, and original-source identity do not change through translation or inference. Only permitted, source-exact original spans may support an asserted employer fact.
2. The Stage A `jobhunter-source-span-identity-v1` `OriginalSourceAnchor` contract is the sole accepted exact original-description span identity for new work. Its 64-character anchor ID is **not** the 32-character heuristic research `SourceSection.span_id`; do not silently remap or reuse identifiers. The existing Stage A primitive supports `description` only; richer structured fields require an explicitly versioned extension.
3. `english-projection-v2` proves source **field** association, not Persian-item/English-item association. Current English v30 gets **only** its English representation; original v9 gets **only** original fields. **Never inject Persian source spans as hidden v30 evidence or rewrite an existing English artifact to cover a bad translation.** New cross-language interpretation needs its own versioned sidecar/candidate contract, and eventual separately approved router.
4. Existing English accepted v20/v21/v23/v28 v5 compatibility, accepted anchor IDs `36/37/39/44/46`, Capability v9 `11–15`, Work v2, Registry mappings, Market snapshots/reports, and public corpus stay unchanged through research. No backfill/regeneration, schema-currentness shortcut, user score, or new authoritative Market denominator is authorized.
5. Hard fail: wrong/stale source/translation/model identity; fabricated/incorrectly sourced employer facts; invalid exact offsets; corrupt persistence; unsafe acceptance/rollback; source instruction injection; leakage to public files; silently altered accepted dependencies. Soft uncertainty: unresolved candidate qualification strength; translation interpretation doubt; incomplete work detail; possible role purpose; unverified noncritical example tool. These remain visible/unknown or excluded from qualified output rather than becoming a general workflow failure.
6. Structured board metadata is **source-labeled data**, not a universal normative employer requirement. A job-board `skills` array, experience range, education tag, work mode or salary must never silently override a contradictory original employer narrative. Preserve both claims, exact provenance and contradiction state; use the employer's explicit item wording for what the employer explicitly stated without rewriting metadata history.
7. The model receives **untrusted job text as data only**; all translation/inference uses the existing authorized local LM Studio policy, no unauthorized cloud calls, scraping bypasses, unrestricted tools, speculative “helpful” source facts, or unbounded retries.
8. Protect useful candidate reasoning: strict source facts need proof; a **clearly labeled, revocable, bounded job-level candidate** may show interpretation and uncertainty without requiring human review of every screen. Durable accepted P1.6, canonical/Market/Capability authority needs separately stronger review and compatibility rules.

## 1. Why Stage B has priority now: exact empirical baseline

The latest accepted main revision provides the passive anchor and review packager; it **does not improve the public P1.6 model output**. A five-job source-first development cohort produced 53 mechanically exact original-description spans, but all existing Persian-to-English v2 item alignments are `translated_field_only_unaligned`; two source-bound local LM Studio translation examples preserved optional wording but are **not representative model accuracy**.

Owner Audit A1 preserved the owner's independent source-only comments on two jobs and completed assistant source-first review on four exposed diagnostic jobs. Assistant review covered 59 source-anchored factual/interpretive items and compared archived model results, yielding **18 diagnostic flags and 11 translation observations**. The assistant had prior outcome context and is **not a blinded independent human evaluator**. None of these counts is a reliability rate.

| Diagnostic job | Observed source/product failure | Required regression behavior |
| --- | --- | --- |
| `tNhZ`: trading Python/backend + optional LLM | Original prose explicitly says prior LLM familiarity is nonmandatory; Jobinja LLM tag materialized as **required**; v30 no usable English candidate; v31 found 6 duties but remained pending/wrong strength | Separate job task “develop AI/LLM features” from qualification “prior LLM familiarity optional”; preserve backend duties, remote/negotiated/part- or full-time and source-labeled tag disagreement |
| `tMps`: enterprise applied AI | Neither tested English P1.6 persisted valid output; explicit Middle 2–4 or Senior 4–7 tracks, a **one of** technical-domain list and preferred tools | Preserve alternatives (OR paths, AND within path); recognize  actual duties and required vector-search skills; report failed inference as failure, not absent employer demand |
| `tNDx`: EDR security operations | Original-language v9 mechanically accepted but 1 of 5 duties was under role purpose; v31 overrode explicit teamwork preference; translation absorbed `نیازمندی‌ها` heading and inserted unsupported “Advantages” boundary | Keep all 5 explicit EDR duties as direct work; teamwork **preferred** (original says `مزیت محسوب می‌شود`); retain Network+/Security+ **certificate OR equivalent knowledge**, unresolved Kaspersky credential strength; do not invent employment-remote from remote customer-support channel |
| `tMjm`: penetration-testing applicant requirements | v30 candidate was rejected: `امکان دورکاری` “remote-work possibility” mislabeled mandatory skill; `وظیفه شناس` mistranslated as identifying duties; applicant competencies can be mistaken for assigned duties | Remote-work possibility = arrangement; conscientiousness remains trait; qualification abilities are **not** invented day-to-day duties; original source uncertainty retained |

Source records: `docs/working-memory/2026-11-13_OWNER_A1_ASSISTANT_SOURCE_AND_MODEL_RECONCILIATION.md`, source-safe `.../2026-11-13_owner_a1_assistant_review/SAFE_RECONCILIATION_METRICS.json`, Stage A closure, November 12 v31 closure with **November 13 EDR erratum**. Original HTML, Persian/English descriptions, owner responses and model completions remain ignored in `data/local-acceptance/`, not in the repository.

**Hypotheses, not yet proof:** item-level original-language ownership plus explicit translation alignment will reduce unsupported requirement-strength and boundary errors; source-labeled metadata reconciliation will stop contradictory automatic mandatory tags; bounded fallback can save user reading time after a P1.6 failure. These must be tested separately.

## 2. Explicit scope and component ownership

| Existing owner | Accepted role / planned Stage B use | No-go |
| --- | --- | --- |
| `source_span_identity.py` | Reuse exact original-description binding, stale/content verification, native identity vs legacy field-unaligned states | No semantic section/obligation inferred by anchor utility |
| `translation_store.py`, `translation_service.py`, `translation/` | Read source version, translation identity, existing provider limits and current v2 projection; candidate source-bound translation in isolated sidecar | No direct mutation/implicit v2→v3 promotion or original/English evidence blending into v30 |
| Research `source_lineage_v1.py`, `source_bound_translation_v1.py`, `source_obligation_audit_v1.py` on `research/p16-original-source-evidence-spine-2026-11-13` | Mine reviewed concepts/tests for heading coverage, source-bound calls, modality flags | Do **not** bulk merge; research ID incompatible; heuristic matches and 2 successful translations are not proof |
| `analysis_service_v30.py`, `analysis_runtime_v30.py`, `evidence_refs.py` and versioned `inference/` | Read v30 requirements/coverage contract and failure modes to design **new** candidate; reuse safe validation helpers only with exact contract proof | No prompt-only v32 churn, no edits to current v30 behavior during sidecar research |
| `analysis_store.py`, `analysis_item_review.py`, `analysis_failure_diagnostics.py` | Reuse append-only review/attempt ideas, pending/accepted/rejected distinction, bounded private diagnostic retention | No pretending original v9 mechanically accepted means independent semantic review; no direct writing to accepted P1.6 rows |
| `public_corpus.py`, `review_snapshot.py`, Work v2, Capability v9, Registry and Market | Regression/currentness/read-model consumers and later compatibility tests | No new accepted downstream facts, denominator changes or historical backfill from experimental claims |
| `docs/working-memory/` and `data/local-acceptance/` | Public safe reports; ignored private immutable raw evidence, source/translation/model logs, local SQLite copies | No raw ads, personal answers or model completions in tracked docs or public corpus |

**Do not create a generic source/translation plugin platform or duplicate analysis database simply because the next contract is bilingual.** Reuse the modular monolith, deterministic checks and existing SQLite source ownership. Experimental output can first be JSON/SQLite in a frozen ignored workspace; only then consider a narrow durable migration if the user-facing product requires it.

## 3. Candidate information architecture: explicit contract to design in B1

Name new research contracts distinctly from current P1.6, with draft identities (names are design candidates, not shipped schemas):

- `jobhunter-source-item-candidate-v1`: one job-source-version-bound original item. Mandatory fields: source `source_job_id`, detail version, semantic SHA, immutable `OriginalSourceAnchor.anchor_id`, exact original substring, parser/origin label (`original_description` vs structured board `skills/experience/salary/etc.`), inferred category candidate, evidence basis (explicit text / heading inference / model interpretation), and uncertainty. Semantic category options: `work_duty`, `candidate_requirement`, `employer_preference`, `alternative_eligibility`, `work_arrangement`, `compensation`, `benefit`, `application_instruction`, `context`, `unresolved`. **Anchor object must not itself imply category**.
- `jobhunter-source-item-alignment-v1`: an independently versioned **relation** between original item and an English item; includes original anchor + target exact translation artifact/version or separately recorded source-bound translation attempt/content digest, target exact UTF-8/Unicode offsets **when actually established**, provider/model/prompt/schema, evidence for alignment and review state. States are `native_english_exact`, `source_bound_translation_candidate`, `legacy_field_only_unaligned`, `semantic_mismatch`, `unresolved`. A single source-bound request establishes association to input, **not** automatic semantic fidelity/requirement strength. A model-suggested match inside a historical long-form translation is a *candidate*, never verified offset identity by itself.
- `jobhunter-source-obligation-assessment-v1`: source-item class and employer-strength attribution **separate** from depth/years, normalized concept, metadata source field, optional/rejected claim and alternative-group structure. Employer obligation states: `required`, `preferred`, `contextual`, `inferred`, `unresolved`; carry explicit source cue and confidence/basis, never silently coerce unknown to required. Track `OR` groups (Middle vs Senior, credential vs equivalent knowledge) and `AND` conditions *inside* an alternative path. Preserve source years and experience terms without converting them to proficiency level.
- `jobhunter-job-understanding-brief-v1`: a non-authoritative, bounded, traceable job-level result organized into (a) employer-exact work, (b) explicit qualifications/preference/alternatives, (c) work/contract conditions, (d) board-only metadata and contradictions, (e) unresolved facts and source gaps, (f) clear current status of translation/analysis. This may be shown to the owner as **candidate** after sufficient integrity checks even where full P1.6 fails; it cannot feed stable Market/Registry/Capability/Work authority.

**Identity and review are orthogonal.** Design separate review dimensions rather than one misleading `accepted` boolean: (i) source identity/integrity valid/invalid; (ii) translation association known/unknown/invalid; (iii) linguistic modality fidelity review unreviewed/assistant-checked/independently-checked/contradicted; (iv) semantic category/obligation review candidate/needs-review/qualified-for-bounded-view/rejected/approved-for-durable-use; (v) operational attempt completed/failed/timed-out/reused. An assistant check is useful but never silently relabeled independent human review.

**Important unresolved design choices to resolve before coding:** exact item split/compound clause representation; structured-field anchor extension/version versus separate stable field reference; one-to-many English translation alignment; what is auto-qualified for a candidate brief; which reviewed checks are required for durable P1.6 promotion; whether a new English projection schema is actually necessary. B1 must resolve these with contract samples and explicit ADR-like rationale; do not silently decide them in implementation.

## 4. Implementation slices, dependencies, and acceptance decisions

### B0 — Seal baseline, test matrix and implementation budget (first task)

**Purpose:** Prevent moving-goalpost experiments and false “latest” measurements.

Actions:
1. Record clean `main` SHA, current contracts, accepted anchor/dependency matrix, branch policy, accepted P1.6/Capability/Work/Market exact state, SQLite integrity and foreign keys. Take a **SQLite online backup** of configured runtime before any persistence experiment; never use production database for tests.
2. Freeze the **exposed development cohort** `tNhZ/tMps/tNDx/tMjm` plus the existing five accepted anchor jobs `tG9K/t4jp/tmBK/t4qV/tmyX`. Keep source SHA and parser/translation dependency identities, expected source assertions, model outputs, unresolved items, and prior trial version **separately**. Test facts are not reverse-engineered from prior model outputs.
3. Define source-anchored independent reference rubric for each case: direct duties, required vs preferred, OR/AND pathways, arrangements, board-only fields, supported omissions, uncertain items, and critical misclassification blockers. Keep **diagnostic exposure** explicit. No market reliability claims.
4. Predeclare a **fresh evaluation cohort selection protocol** (target 6–8 independently sourced, recently available postings if obtainable lawfully) *before* candidates inspect them. Stratify across software/Python, applied AI, cyber/security and one low-structure posting, mix Persian and native-English when possible, include a material alternative and a preference/metadata contradiction when available. Freeze full original evidence, source URL/capture time, hashes and original-language pre-model review. Hold it outside iterative model development. If source access is denied, do not bypass source restrictions or reuse exposed jobs as an “unseen” cohort; record blocked status and postpone generalization/promotion.
5. Predeclare model-call wall/inference limits consistent with existing LM Studio runtime policy (bounded transport/retries, reasonable local post-connect computation), failure capture and evaluation budget; distinguish timeouts vs schema errors vs source lack. Plan at most **one primary candidate plus one justified corrective candidate per acceptance slice** before a mandatory root-cause/stop review. Expanding this budget requires written evidence, not endless prompt versioning.

**Gate B0 PASS:** named baselines, reproducible safe reference report, exact identities, clear exposure labels, resource budget and holdout protocol. B0 produces no code mutation, accepted facts or new stable model.

### B1 — Contract/review boundary and compatibility design

**Purpose:** Choose the minimal sound source-owned architecture, without prematurely merging the research parser.

Actions: instantiate the four candidate contract examples above against all four diagnostic jobs, include source-anchored `tNDx` unknown certificates and `tMps` OR eligibility; review source-identifier continuity and field extension; define item authority and provenance; compare existing `analysis_item_review.py` to avoid duplicated review state; design append-only corrections + conflict state; specify API and schema compatibility separately for candidate brief and durable P1.6. Produce a compact ADR with alternatives: (A) sidecar-only first (selected default), (B) direct v30 patch (rejected: violates English-only evidence), (C) immediate new durable v3 projection (deferred unless justified). Capture target modules, schemas, migration/no-migration decision, persistence owner and rollback. Decide what is an evidence-qualified fact versus a provisional interpretation **by category**.

**Gate B1 PASS:** versioned JSON/schema fixtures (nonexecutable design acceptable), explicit original-vs-board authority table, semantics of unknown/inferred/review, alternative-group truth table, item alignment guarantees, privacy, invariants and a machine-checkable decision record. Do not start B2 implementation before B1 is coherent.

### B2 — Original-source item interpretation and structured-metadata reconciliation

**Purpose:** Deliver bounded, exact original evidence coverage, without claiming perfect Persian comprehension.

Actions:
- Build item segmentation as explicit **candidate** structure on Stage A anchors; preserve evidence-exact split boundaries and avoid swallowing adjacent section headings. Use heuristics as suggestions only, with direct source-cue override and `unresolved` for mixed, ambiguous, missing or conflicting cues; inspect the research parser but do not import its weaker identities.
- Distinguish explicit work assignments from role purpose, applicant “ability to ...”, qualifications, generic team traits, work arrangements, benefits and application instructions. Preserve explicit employers' lists and document gaps separately from facts.
- Reconcile structured `skills`, experience, education, employment mode and salary **against prose** as separate source-labeled items. Strip non-skill board/page contamination only with source-path proof; flag conflict instead of inventing an override. An LLM-tagged required-like board token must not force required strength contrary to explicit optional employer prose.
- Treat `tNDx` “teamwork is an advantage” as preferred; Kaspersky certificates and government-customer experience as **unresolved** unless explicit source evidence establishes strength. Keep `tMps` Middle OR Senior paths with within-track AND requirements and one-of domain choice. Recognize `tMjm` remote option as arrangement.

**Gate B2 PASS:** deterministic tests and inspected original-source outputs cover known 4 cases, heterogeneous old anchors and counterexamples; exact original spans and references; zero fabricated literal source strings or unsupported **mandatory** claims in tested fixtures; all explicit alternatives preserved; required-vs-preferred and duty-vs-ability tests; no historical source/translation/P1.6 mutation. Ambiguous item detection may abstain rather than force a label.

### B3 — Source-bound bilingual alignment and translation-quality fence

**Purpose:** Establish correct **item association and meaning preservation**, not just one request per string.

Actions:
- Reuse current `translation v2` source identity and provider isolation; add **candidate-only** one-source-item-to-English responses with original anchor and hash, target output digest and version, native identity where valid; do not pretend old whole-description v2 artifacts gain exact item links. If keeping existing v2 projection, maintain sidecar with separate evidence/identity; create a new projection schema only if required by justified runtime read semantics.
- Guard exact negative/positive modality; OR/AND qualifiers, minimum durations, certificate equivalence, technical terms, heading boundaries, scope changes and work-mode terms. Semantic quality cannot be proven by regex alone; use tests and source-grounded review. If a clause shifts materially, mark mismatch/unusable for derived factual claims. A bad translation is **not repaired by adding Persian evidence inside an old English v30 artifact**.
- Inspect translated claims against original exact items, retain new source-bound model request/response privately with bounded retention and hashes, log provider/model/prompt/schema and failure reasons. Keep native English a genuine identity case and unknown target offsets unknown.

**Gate B3 PASS:** original-to-target association mechanically exact for new candidates, source meaning verified on exposed diagnostic clauses (including EDR heading distortion and `وظیفه شناس`), no invented implicit equivalence for legacy v2; original/translated modality agreement or blocked flag; no mixed-evidence currentness violation; local provider privacy and bounded behavior verified.

### B4 — Useful non-authoritative job understanding and P1.6 candidate comparison

**Purpose:** Return job-relevant insight without corrupting durable accepted facts.

Actions:
- Build a bounded job-understanding **candidate** view using source-qualified items and clearly indicated unknowns; when P1.6 fails, show factual source-exact items that are safe to show, clearly label missing semantic analysis and unverifiable qualifiers. Do not call it a valid P1.6 artifact or feed accepted downstream consumers. Partial results can still be useful but must not imply the full job was analyzed.
- Compare **new experimental candidate** against v30/v9 under the same source snapshots in a separate DB. Keep source fact, translation, candidate inference, coverage account, and review state separate. Existing `analysis_item_review` and failure diagnostic mechanics are reusable patterns; avoid unreviewed automatic `accepted`.
- Exact coverage ledger: obligations for each classified source item (covered as duty/requirement/arrangement/unresolved/excluded with reason); no arbitrary “all source words must become requirements.” Allow an unknown or legitimately context-only item rather than demand a false classification.
- Prototype user-facing readability (read-only brief or diagnostic HTML/CLI), avoiding raw provenance-overload. Show fast understanding, supporting original quote on demand, and no erroneous job skill conclusions. No production router/normal page changes yet.

**Gate B4 PASS:** useful source-grounded brief for all four exposed test cases, or explicit per-case blocked explanation without invented facts; original-language quote + target item provenance; acceptance of uncertainty where justified; no critical mandatory/preferred or duty/arrangement mistakes in tested known cases; typed failure states with preserved partial success. Compare useful information / review time to raw ads honestly; do not assert measured owner-time savings until measured.

### B5 — Fresh, independent verification (do not tune on this cohort)

**Purpose:** Check generalization and avoid self-congratulatory overfitting.

Actions:
- Run the **previously frozen and unexposed** corpus once under the chosen candidate with the fixed model/runtime and separately under unchanged v30 baseline where comparable. Record prompt/model and dependencies; save original source, candidate, validation/failure and source-review judgments with frozen hashes.
- Independently read original postings before reading model outputs; reviewer must be shielded from candidate outputs and, to the extent feasible, from outcome-specific rules. If the same assistant is reviewing with prior knowledge, label it **assistant source assessment, not independent blind human**; optionally use truly context-isolated reviewer/cross-review for consequential promotion. The owner's routine involvement is not mandatory. Any ambiguous employer intent stays unknown, even if the model confidently guesses.
- Score **only evaluated claims**: source-exactness, classified work completeness, requirement strength, within/alternative path logic, context/arrangement leakage, translation semantic drift, accepted/rejected/timeout completion, informative fallback, model-call cost/time, and recoverable provenance. Separate errors from correct abstention. Preserve case-level denominators and uncertainty; a tiny corpus cannot justify market accuracy claims.
- Fatal failures: fabricated/unsupported mandatory employer fact; source identity mismatch; translated modality reversal promoted as fact; inferred credential/experience as required without support; failed privacy/migration. Any such case blocks affected promotion pending root cause and a verified generalized repair. Incomplete noncritical analysis may yield a candidate-only partial brief, not an accepted full analysis.
- Bounded corrective follow-up: if unseen cases fail, analyze root causes on **new exposed regression fixtures** and reserve a different untouched verification set for any subsequent promotion claim. The failed holdout becomes exposed after its first inspection.

**Gate B5 PASS:** no unresolved critical source/truth errors in evidence-qualified claims, maintained old-anchor compatibility, demonstrably usable/less misleading output than the unchanged v30 reference on specific cases, and publicly inspectable counts/hashes without source content. If acquisition or review independence fails, report **NOT ESTABLISHED**, not PASS. Do not demand a universal model-accuracy percentage from 6–8 jobs.

### B6 — Controlled public integration, regression, rollback and closure

**Purpose:** Upgrade P1.6 product capability only on proved, bounded evidence.

Prerequisites: B0–B5 gates satisfied and a separate explicit promotion decision naming candidate contract, intended user flow, version, review/authority, affected stores, provider fallback and rollback. Required product choices: (a) retain sidecar + bounded brief with no new accepted P1.6, or (b) introduce a **new versioned** public semantic route/English projection contract after evidence review. Do **not** rename v30 to a new version without a meaningful changed contract.

Actions:
- Choose one narrow vertical integration; share browser/CLI service and use SQLite as runtime authority if persistence is justified. A fresh schema/migration must be additive, backed up, verified for FKs/currentness and idempotency, with rollback restoring prior public routing. Preserve immutable old artifacts and attempt/review logs, never rewrite 36/37/39/44/46 or the v9 mechanically accepted records.
- Update currentness/compatibility rules explicitly. New pending and rejected candidates must not enter Capability v9, Work v2, Registry, Market aggregates, Review Snapshot accepted chains or public corpus as `accepted` without the approved promotion boundary.
- Test on production-like read-only/isolated copies first, then the bounded explicit switch. Include CLI, browser and HTML escaping/source-injection tests, successful and failed local inference, stale source/translation, re-run/idempotency, partial-result screens, privacy, request-size ceilings and no unexpected external services.
- Verify old accepted chains, exact downstream IDs, Market snapshot/report immutability, corpus stability, backup integrity, and CI. Update governing architecture/domain/translation docs when new accepted semantics **actually ship**. Produce release notes, successful branch/PR CI, rollback command/procedure, and a truthful measured-user-value report.

**Gate B6 PASS:** accepted integration changes only named routing/contracts; old and new histories coexist, all tests and CI pass, live bounded test matches source-grounded evidence, no destructive migration, and rollback demonstrated. Otherwise keep the new feature candidate-only / research and leave public v30.

## 5. Concrete test and inspection matrix

Mandatory synthetic/counterexample classes, not prompt-specific hacks:

| Scenario / exact fixture | Expected outcome | Fail condition |
| --- | --- | --- |
| `tNhZ` employer “LLM familiarity not mandatory” + board LLM tag | Source preferred, board tag source-labeled; unresolved conflict warning | “LLM required” persisted as employer requirement |
| `tNhZ` develops LLM feature as job duty | Duty present; do not transfer prior skill requirement | Duty magically makes prior LLM expertise mandatory |
| `tMps` Middle OR Senior, 2–4 vs 4–7; one of LLM/RAG/GenAI/ML/NLP | Alternative track DAG with correct AND/OR and years | Both tracks/all named domains required simultaneously |
| `tNDx` teamwork “مزیت محسوب می‌شود” | Preferred item even inside broad requirements section | Heading guess strengthens item to required |
| `tNDx` Network+/Security+ certificate or equivalent knowledge | Explicit equivalent qualification path | Certificate forced when knowledge alternative supported |
| `tNDx` Kaspersky certifications and government-customer experience | Unresolved strength pending actual employer evidence | Invented “advantages” or forced required classification |
| `tNDx` 5 work duties, report-writing followed by `نیازمندی‌ها` | All direct duties accounted for; heading not swallowed | Implementation duty only in role purpose; heading joins duty |
| `tMjm` “امکان دورکاری” | Work arrangement/possibility | Required applicant qualification |
| `tMjm` “وظیفه شناس” | Conscientiousness trait or unresolved if translation unstable | “identification of duties” counted as source fact |
| Requirement-only role with no explicit duties | Valid bounded requirements + unknown work | Fabricated task list; “no work required” inferred |
| Board salary/hours/experience versus prose mismatch | Keep both labels/values and discrepancy | Silent overwrite or one merged authoritative claim |
| Native-English original and mixed Persian text | Exact native identity or separately bound translation | Fake English offsets based on string similarity |
| Changed source semantic SHA or translation artifact version | Reject stale link and candidate reuse | Outdated fact displayed as current |
| Missing model / timeout / malformed output | Correct attempt status; limited qualified brief when possible | Empty source claim, silent success, invalid durable artifact |
| Source prompt injection, HTML/URLs and page text in `skills` | Treated as untrusted data, escaped and field-scoped | Execution/instruction adoption, metadata-as-authority |
| Historical accepted 5 anchors and downstream consumers | Exactly preserved accepted IDs and read-model/currentness | Silent regeneration, accept-state drift, changed Market count |

**No per-ad, framework-specific regex patch is an adequate substitute for these general invariants.** After a defect, add a generalized counterexample, negative test and at least one related non-regression check.

## 6. Evidence, evaluation scorecard, and release-quality controls

Every gate must leave a **decision artifact** and machine-readable metrics with exact code commit, source semantic version, affected model/prompt/schema, date, test commands, status and unresolved issues. Keep hashes/status/counts in Git; full original ads, local source files, owner answers, model prompts/responses and possibly identifying information in ignored `data/local-acceptance/`.

At minimum record per job:
- source and field hashes; original-version and translation identity; whether item alignment is exact/native/source-bound candidate/unknown;
- number of explicit source duties, correctly represented duties, omitted direct duties, invented duties, and obligations whose source strength is supported/contradicted/unresolved;
- number of alternative eligibility groups and whether OR/AND is preserved;
- translated item semantic-cue divergence (negation, years, role scope, heading boundary, optionality);
- full vs partial vs no product result, failure class, attempts, elapsed time, LM calls, estimated tokens where available, reviewer exposure/independence;
- candidate/qualified/rejected/superseded disposition and any downstream authority gained (normally **none** until B6).

**No invented performance denominator.** For example, 18 flags among four exposed ads ≠ “JobHunter has 4.5 errors per posting.” Zero accepted candidate for a case ≠ empty employer requirements. Successful two-span translation trial ≠ bilingual accuracy certification. No claimed owner time saved without a controlled observation.

**Engineering gates:** normal `pytest -q -W error`, `ruff check .`, `python -m pip check`, `git diff --check`, SQLite `integrity_check` and `foreign_key_check` for relevant snapshots, privacy/ignore checks, accepted-current identity probes, local-only provider policy, branch PR CI and meaningful real-input smoke tests. Additional new tests must not silently weaken accepted tests.

**Risk register and mitigations:**
- False source segmentation -> preserve exact spans, candidate categories, unknown strength, counterexamples.
- Invalid English/Persian mixing -> sidecar bilingual contract, no old v30 injection, versioned router if promoted.
- Structured metadata stronger than employer -> field-scoped authority and conflict ledger.
- Real-model latency/timeouts -> bounded provider calls with controlled diagnostics, partial user-visible source result.
- Human/assistant review contamination -> freeze original judgments first, label prior exposure, unseen cohort and promotion review.
- Parser/source acquisition failure -> preserve source failure class and source policy, never use restricted bypasses.
- Existing accepted authority drift -> versioned sidecar, old artifact ID and currentness regression, no direct writes to main DB in experiments.
- Raw evidence/privacy leakage -> ignored storage, public sanitization, source HTML escape, strict source URL allowlist, provider network confinement.
- Iteration spiral -> predeclared gates/call budget, stop and redirect after bounded corrective attempt, avoid v32/v33 prompt-only cycles.

## 7. Build order, dependencies, ownership and stop rules

```text
Stage A accepted on main (passive original-source anchors + owner packager)
    |
    v
B0 baseline/fixture/holdout protocol  -> B1 contract + authority decision
    |                                    |
    +------------------------------------+
                 |
                 v
B2 original item/source metadata assessment
                 |
                 v
B3 source-bound bilingual candidate alignment
                 |
                 v
B4 useful job understanding / shadow P1.6 comparison
                 |
                 v
B5 reserved fresh cohort / independent source assessment
                 |
           explicit promotion decision
                 |
                 v
B6 selected public integration or NO-PROMOTION
                 |
                 v
resume bounded P2.3 capability-expectation experiment as separately authorized
```

**Ownership/decision policy:**
- Assistant: inspect sources, formulate precise generic contracts, implement/test on separate branches, review routine semantics, flag ambiguities, preserve evidence, report failures and make evidence-based recommendations. Owner explicitly delegated routine review; do not demand another four-job questionnaire.
- Owner: reserve decisions that affect product tradeoffs, personal workflows, irreversible data/publication boundaries, or meaningful human sign-off where the governing contract requires it. Ask only if necessary; do not ask owner to infer undocumented employer intent.
- Semantic uncertainty requiring employer clarification stays `unresolved`. Neither owner nor model should invent it.
- Git: branch from clean main; one approved acceptance gate per reviewable increment; safety/compatibility checks; PR CI; separate migration and routing gate. Do not merge all research files because they share a branch.
- Time/budget: no promise of fixed calendar delivery or background execution; measure real call costs and elapsed time, maintain capped trial budgets.
- **Stop / redirect** if critical source errors persist after justified corrective revision, if input source provenance cannot be established, if a fresh verification set is unavailable, if an unauthorized data mutation is required, or if additional complexity has no demonstrated job-understanding benefit. Keep the safe brief if it is useful, defer unreliable durable inference.

**Next executable task after B0 acceptance (2026-11-14):** implement the B1 typed contract/ADR design on a separate branch, using the frozen B0 private snapshots, safe evaluation protocol, and A1 source-exact reference. No B2 classifier, model prompt, public routing, translation schema or database migration before B1 acceptance. B0 captured **zero** unseen jobs; B5 must obtain and source-review the predeclared 6–8 new cases.

---

## 8. Relationship to remaining roadmap (explicit sequencing reconciliation)

The previously selected **job-specific capability-expectation** scope in `docs/working-memory/2026-11-11_NEXT_SUBSTANTIVE_CAPABILITY_EXPECTATION_SLICE.md` is still a valid, separately scoped product candidate. Its inputs rely on trustworthy P1.6 duty/qualification/obligation facts. The **November 13 four-case audit establishes a concrete upstream correctness risk**, so this plan changes the *next execution order*: Stage B becomes the active product reliability prerequisite before moving on to that P2.3 experimentation. The earlier November 11 proposal remains evidence and future scope, **not an instruction to run it concurrently or invalidate accepted P2.3A comparison closure**.

Other tracks not authorized by Stage B: broad new Jobinja/ATS adapter, generalized source browsing, Market v2, promoted role families/archetypes, persistent capability profiles, bulk canonical mappings, personalized scoring, resume automation, job application automation, generalized evaluator-agent framework, wholesale replacement of SQLite, and indiscriminate regeneration of accepted artifacts. Source fixes and approved maintenance may proceed separately when justified.

**Definition of completed Stage B:** a useful source-faithful job understanding capability shipped or deliberately held back after explicit source/translation identity and semantic gates; a comparison against current v30 with fresh independently evaluated evidence; no critical source-fact/obligation regression in promoted claims; unchanged old accepted IDs/currentness and downstream behavior; reproducible PR/CI/privacy and rollback record; and accurate status in governing documents. A partially completed stage is **not** called done because tests pass or two model clauses translate correctly.
