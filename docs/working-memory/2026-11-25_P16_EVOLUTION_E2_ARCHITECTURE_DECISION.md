# P1.6 evolution E2 — architectural alternatives, experiment design and decision

**Date:** 2026-11-25. **Base:** `a092f68ed0144fe9633c967cd8e33ac6c0a14a07`. **Scope of this entry:** E2.1 alternatives, not E2.2–E2.6 completion or selected architecture. **State:** design published; local reconciliation pending (Desktop Commander offline). Prior E1 closure CI [45658879033](https://github.com/motafegh/jobhunter/actions/runs/45658879033) verified successful at exact base. No new code, source acquisition, inference, training, model load, database write, review or rollout authorized.

**Authority:** [P1.6 execution tracker](../P16_SEMANTIC_ARCHITECTURE_EVOLUTION_PLAN.md), [Stage B](../P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md), [architecture](../ARCHITECTURE.md), [domain](../DOMAIN_AND_ANALYSIS_MODEL.md), [reasoning policy](../UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md) and [AI research companion](../AI_ARCHITECTURE_RESEARCH_AND_EVOLUTION_PLAN.md). Inputs: [E1 causal matrix](2026-11-24_P16_EVOLUTION_E1_ROOT_CAUSE_INVESTIGATION.md#2026-11-25-continuation--e111-consolidated-causal-findings-and-e2-decision-inputs) and [DOC.2 as-built map](2026-11-25_ARCHITECTURE_UNDERSTANDABILITY_DOC2_P16_RUNTIME_BASELINE.md). All prior diagnostic cases exposed. Existing v30/v5 English and v9/v4 original routes and accepted-compatible artifacts remain unchanged. This document is the evolving E2 decision record, not a separate checklist.

## 1. Product question and invariant requirements

Which design lets JobHunter understand a real vacancy more accurately, completely and efficiently than the user reading the original, with actionable uncertainty rather than a false sense of certainty? We do not optimize JSON completion, number of categories, model sophistication or benchmark scores in isolation. Accurate employer facts, useful model interpretations, and accepted durable facts are not the same product.

Retain original immutable source, exact version/anchors, source observation vs semantic identity, local-first modular monolith, SQLite, original/derived language distinction, privacy, currentness, existing accepted history and consumer gates. Avoid either under-grounded intelligence or over-gated delivery. Preserve rich natural context: duties and qualifications can overlap or inform each other. A duty may imply ability at some depth without establishing prior paid experience or mandatory employer eligibility. Behavior can be a qualification; classification disagreement without semantic harm is not automatically critical. Keep employer wording and interpretation separately accessible. Review effort proportionate to consequence. No automatic fact promotion from schema success, citations, critic agreement, deterministic label or model confidence.

All arms operate only in isolated research state until applicable E4/B5 and explicit E5/B6 gates. Current selectors for Capability, Work, Registry and Market must remain unchanged. B5 has four exposed failures; no new cohort or autonomous rollout. P2.3 remains deferred.

## 2. Separate the experimental dimensions

A0, A1 and A2 designate semantic architecture families; A3 designates the language-axis alternatives to be compared with a compatible architecture. Not four mandatory end-to-end products, and not a full factorial matrix. Use E2.A0 etc as local labels to avoid confusion with older Stage A or A1 review records.

| Dimension | Candidate choices | Hold fixed when studying |
| --- | --- | --- |
| Semantic architecture | A0 unchanged v30; A1 targeted repair; A2 contextual candidate plus deterministic reconciliation | Same source versions, language representation, model/runtime, common measurement envelope |
| Language (A3) | L0 current English v2; L1 improved contextual/source-aligned English; L2 original-first; L3 hybrid original plus aligned English aids | Same semantic task and compatible architecture, model and task rubric, matched source scope |
| Model | Incumbent E4B; MiMo 9B challenger if feasible; other local models conditional | Same task/contract/input, comparable runtime/decode and budget; disclose unavoidable tokenizer/template differences |
| Recovery/delivery | Existing whole-artifact behavior; targeted local recovery; qualified partial candidate plus source fallback | Same inputs/model outputs for deterministic replay; separately compare new calls and user-facing output |
| Context allocation | Whole coherent ad if it fits; section/group with surrounding context; bounded escalation for unresolved relationships | Same original units and coverage rubric; no silent omission/truncation |

Hard budget envelope belongs to experiment runner for *all* arms, including A0. Do not change A0 semantics or validators to achieve fairness. If a deadline/call ceiling interrupts A0, record budget-stopped rather than pretend the unbounded historical run completed. Measure actual physical requests, preflights, tokens, latency including cold/warm and model switching, failures and review burden. E2.3/4 will freeze exact arms, thresholds and feasible schedules before E3. No new calls now.

## 3. A0 — unchanged English v30 baseline

Purpose: reproduce the current semantic path as a comparator, not repair it or declare it acceptable.

```mermaid
flowchart TD
  S[Original parsed source] --> T[Current v2 English projection]
  T --> P[Inherited requirement and duty planner]
  P --> M[Scoped Instructor calls and v30 schema]
  M --> V[Inherited validators and scoped filters]
  V --> G[Whole merge and global validation]
  G --> A[Pending whole artifact]
  G -->|failure| F[Failed attempt]
  M -->|unrecovered failure| F
```

As-built: analysis_current -> V30 service (V21/V20 entry) -> V16/V15 nested recovery -> V27/V25/V23/V21/V20 _run_once, requirement partitions and first-part duties, v30/v24/v20 Instructor, inherited model validators, filtering/merge, V28 persistence, pending review. Exact dependency reuse of accepted compatible v20/v21/v23/v28 v5 is current behavior; in paired fresh generation comparisons isolate caches without deleting accepted history, record reuse separately. A0 reads unchanged frozen v2 fields and current contract, not an edited projection. A0 may fail before returning claims; report delivery failure and score available outputs without inventing absent results. Use source-brief and existing B4v6 as separate user-delivery comparators, not replacement semantic baseline.

Strengths: extensive historical compatibility and tested evidence guards, known interface and persistent shape, exact source/translation identities, established review. Limitations: RC01–05/08/10/12, scope conflicts, deterministic board tag inflation, nested recovery, no persisted partial artifact, English fidelity dependence. Keeping A0 is a valid outcome if alternatives cannot demonstrate net improvement; that does not resolve existing defects or reopen promotion.

## 4. A1 — targeted repair in existing architecture

Purpose: determine whether correcting demonstrated deterministic and representational defects restores reliability without a broader semantic redesign. Keep v30-shaped task, current English input, partition strategy and unchanged output authority for the controlled architecture comparison. Implement future candidate under distinct experimental version and isolated dependency injection; never modify A0 or silently reuse accepted artifacts as candidate outputs.

| Repair candidate | Owner/mechanism | Required proof and non-goal |
| --- | --- | --- |
| Compound requirement scope | v23 preserve_source_alternatives, _source_alternative_concept and v21/v20 depth validators (RC01) | Avoid whole-parent concept overwrite of separate child. Keep exact parent relation and local modifier scope; replay neutral retry and negative controls. No blind deletion of depth or OR. |
| Motivation vs technical depth | v21 lexical explicit-degree requirement and v20 scoped-depth guard (RC02) | Null depth acceptable for non-depth concept when evidence supports it; explicit depth remains preserved or qualified unresolved. Reject borrowed/unsupported values. No regex exception for one advertisement or words in isolation. |
| False duty ownership | evidence_refs_v21 duty section boundaries and V21._responsibility_coverage_plan (RC03) | Identify non-duty section boundaries without losing genuine duties; unchanged retained retry with only false ref corrected is a causal control. Ambiguous units stay unresolved, not magically duties or exclusions. Negative control still rejects missing genuine duty. |
| Board/source separation | analysis_runtime_v20._v20_deterministic_structured_skills (RC08) | Board tags remain source observations; no automatic required/high employer strength solely from tag. Preserve useful metadata. Candidate projection compatibility must be assessed; if schema cannot express without meaning change, make limitation explicit rather than retrofit accepted rows. |
| Coherent instructions | assembled versioned prompts and scoped coverage payload (RC04) | Remove demonstrably obsolete/conflicting instructions only when actual contract behavior agrees. Distinguish a prompt cleanup arm from representation repairs if feasible. No claim fewer characters alone improves meaning. |

A1 is an experimental repair family, not a mandate to implement every row simultaneously. E2.5 select minimal coherent patch set; offline retained response replays isolate first three mechanisms before inference. For combined changes, record ablation or inability to attribute individual effects. Board authority fix may require a distinct candidate projection, not silent v5 semantics amendment. Preserve exact source/translation dependency and hard guards. Budget enforcement is common harness, not A1's claimed improvement; targeted retry policy can be separately compared. Do not use A1 as pretext for broad historical inheritance flattening. Expected advantage: low-to-moderate change scope, compatibility and causal attribution; remaining burden from partitioned task, long inherited instructions, English translation, whole merge and possible misleading coverage classifications. A1 may be sufficient, or may expose a representation ceiling.

## 5. A2 — contextual source-local semantic architecture

### 5.1 Processing and responsibility split

Hypothesis: an LLM given coherent employer language with relevant source context and a compact meaning-oriented contract can interpret more reliably than a model forced to satisfy prespecified semantic categories, depth and coverage obligations; deterministic orchestration should protect evidence and expose missing/invalid claims without forcing every interpretation into a rigid output. This is not proven by prior native JSON tests. Source-local does NOT mean per-sentence isolated prompting; begin with an intact ad where feasible.

```mermaid
flowchart TD
  S[Original source and exact version] --> C[Lossless context packet]
  T[Optional aligned language aid] -.-> C
  C --> M[Contextual semantic interpretation]
  M --> E[Resolve source associations]
  E --> L[Assess meaning coverage and relations separately]
  L -->|safe candidate| P[Qualified candidate view]
  L -->|uncertain or failed| U[Unresolved material and original fallback]
  L -->|specific recoverable gap| R[Bounded targeted recovery]
  R --> E
  P -.-> G[Separate applicable review and promotion gate]
  U -.-> P
```

| Stage | Deterministic responsibility | LLM semantic responsibility | Failure behavior |
| --- | --- | --- | --- |
| Context packet | Original source/version identity, exact spans and metadata pointers, order, headings, group boundaries, dedup of exact representations, token budget and omitted inventory | None required at preprocessing | Hard identity failure abort affected output; preserve unknown/unclassified original material rather than erase it |
| Primary interpretation | Supply relevant context, validate compact transport envelope, preserve response and provenance | Understand role purpose, work, explicit expectations, preference/conditions, alternatives, motivation and implied ability; retain relevant ambiguity and relationships | Invalid envelope bounded repair if justified; failed generation still source fallback |
| Association and representation | Resolve cited source anchors/child spans/board pointers; ensure exact version/scope; reject fabricated IDs; safe shape normalization only | Propose which evidence supports interpretation and scope; uncertainty if unclear | Invalid association quarantined; exact association not entailment |
| Reconcile | Track coverage inventory, duplicates, shared dependencies, conflicts and provenance; no deterministic semantic coercion | Interpret relations, alternative topology and shared modifiers, distinguish evidence from inference; investigate only selected gaps | If group relationship unresolved, withhold dependent eligibility conclusions; retain safe independent material and source quotes |
| Delivery | Status labels, preview/full drilldown, currentness and authority, source-first fallback and unattempted ledger | Candidate summary of meaning, explicitly inferred capabilities, notable ambiguities | Partial not whole success, no missing-is-absent claims |
| Promotion | Separate explicit review and exact compatible dependency gate | Advisory support only | No auto-acceptance, no downstream candidate adapter |

### 5.2 Context and output design choices for E2.2

Use Stage A exact original anchors, B1 evidence/board/overlap concepts and original HTML groups as substrate. Do not trust B2v7 candidate labels as input truth; its heading heuristics can lose non-list passages and inherit incorrect obligation. Include original unclassified blocks and coverage inventory independent of B2 labels. Preserve title, heading and neighboring context with scoped evidence; never transfer heading scope merely because a finite regex misses a boundary. Whole source if it fits token budget; otherwise coherent group/section with adjacent or shared context, stable group IDs, links to earlier/later clauses and explicit unprocessed inventory. No blind truncation or rigid partition by qualification categories. Evaluate any section planner itself.

Minimal conceptual response (not final schema): a compact list of candidate statements with source references and semantic basis (explicit claim, implied interpretation, unresolved/context), natural-language meaning and only the role/strength/scope/depth/experience/alternative attributes justified by content. A claim can serve multiple semantic functions; shared evidence is allowed, distinct claims use stable identities and linked relations to avoid double counts. Preserve exact source text separately, no requirement for model to retype hashes or all evidence. Use optional relation or group representations when material, not mandatory graph generation. Explicit absence requires evidence and proper scope, not empty arrays or missing output. Do not require the LLM to output every possible field per statement or emit an exhaustive ontology. Confidence may signal uncertainty, never substitute for evidence or review. E2.2 defines actual envelope, identity, optional fields, verification and authority; this entry proposes meaning and responsibility only.

Keep original and candidate claim coverage distinct: every source group accounted for as inspected/summarized/not attempted/excluded with reason/unresolved (implementation vocabulary E2.2); inspected does not mean understood, a reference does not establish meaning completeness. Deterministic ledger based on known inputs and actual outcomes; semantic coverage evaluated source-first. Cross-group dependencies are reconciled before eligibility summary. Candidate views retain unresolved clauses and original drilldown even if translation missing. B4 fragment filtering and compact view are useful engineering seeds, not semantic truth. Use original source-brief fallback independently of B4's translated input dependency.

### 5.3 Illustrative synthetic passage (authored, not an archived ad)

> Build and maintain internal APIs using Python or Go. Solid knowledge of engineering principles is expected. Experience deploying services is preferred. A degree or equivalent project experience is acceptable. Strong interest in learning is important. Hybrid work by agreement.

Desired interpretation, not model output or accepted evaluation labels:

| Material meaning | Candidate interpretation | What must not be inferred |
| --- | --- | --- |
| Assigned work and tools | Build/maintain APIs; Python or Go associated with duty; implies ability to do API work | Both languages mandatory; prior paid API experience required |
| Engineering principles | Explicit expected solid knowledge, separate concept and depth | Copy solid to programming or motivation |
| Deployment | Explicit preferred experience | Mandatory deployment or exact years |
| Degree/experience | Preserve OR and equivalent scope, or show intact clause unresolved | Require both; substitute paid work for project experience |
| Motivation | Behavioral expectation/qualification as appropriate, no technical degree | Strong proficiency or mandatory work history |
| Arrangement | Hybrid by agreement, separately visible | Technical qualification or guaranteed remote |

This example illustrates overlap without forced separation. One source group can contribute work and capability meaning. The UI can answer "what would I do, what do they expect me to know, what prior evidence do they ask for, what is optional, what conditions/alternatives matter?" without forcing unrelated claims into an artificial single score. Actual interpretation and user benefit must be evaluated.

### 5.4 Recovery and reuse of existing modules

Propose bounded targeted recovery for invalid representation or unresolved material, not endless full-job rewrites. An independent fragment survives only if its own source/contract/model/run dependencies are valid and unresolved global relation cannot change its meaning. Example: if degree/experience OR topology unresolved, retain exact clause and qualified uncertainty; do not mark degree mandatory. An unrelated valid location statement can remain visible. Distinguish malformed JSON (recoverable only without inventing meaning), unsupported association, contradictory semantics and incomplete coverage. No auto-promotion from partial. Receipts preserve raw/normalized versions privately, actual stage attempts and dependency identities. No new agent framework or separate database by default; use isolated research artifact and existing local runtime/budget seam if compatible. E2.2 determines whether local checkpointing is necessary versus safe end-of-run receipts. E2.3 freezes recovery caps.

Benefits hypothesized: broader contextual meaning, fewer mandatory fields, lower validation failure blast radius, original source visibility, potentially lower repeated prompt cost. Risks: larger whole-context prompts, missed units/relations, freeform hallucinations, weaker comparability with v5, new candidate schema/review/presentation burden, no guarantee small models perform better. Compare against A0 and A1 with same language/model before claiming A2 advantage. Do not simply rebuild old native v2/v3 prompt or B4 as new production path: prior native source-ref trials passed structure while missing material semantics, B4 reference filtering passed incorrect obligation.

## 6. A3 — language strategy, orthogonal to A1/A2

Current English v30 is translation-dependent, but translation is derived convenience, not source authority. English-native descriptions still failed due to nontranslation causes. Original v9 is a historical comparator (known semantic errors, new outputs pending), not evidence original-first is superior. Use the same compatible semantic architecture and task across language arms to isolate language contribution.

| Arm | Flow | Context/fidelity tradeoff | Resource hypothesis |
| --- | --- | --- | --- |
| L0 existing v2 | Current whole-field derived English -> semantic reasoning -> resolve to original where possible | Familiar analysis language; translation may alter names/strength/duties; field association not exact original span equivalence | Reuse possible; translation and model switches when cold |
| L1 improved contextual translation | Original groups with headings/shared clauses -> source-aligned translation or reviewed aid -> same semantic reasoning | Better possible alignment; still depends on linguistic fidelity and original scope | Extra translation calls or bounded batches; compare existing B3/B5 without assuming superiority |
| L2 original-first | Original-language text with stable anchors -> semantic reasoning -> translate selected display content if needed | Original context direct; model Persian/mixed-language competence unknown; English presentation separate | May avoid prerequisite translation; display translation and recovery still cost |
| L3 hybrid | Original plus aligned English aids when useful -> semantic reasoning over paired views -> preserve discrepancies | Potential support for names/technical terms, but conflicting aids may bias interpretation; original controls | Larger input and possibly extra translation; selective rather than automatic double context |

Native English uses identity for native description, but metadata may still require translation. No lossless-language assumption for metadata. For L0/A2 mapping of exact English refs to original: if v2 only provides field-level alignment, label original field association and unresolved exact original child evidence, not fabricated exact anchor. Do not disadvantage a language arm by granting another unsupported source precision. Compare both what each arm can establish and what it cannot. Preserve original group/compound relation context and terminology, negation, numbers, names, scope, conditions and attribution. Translation aid invalidation affects only dependent candidates, not source truth. L2/L3 source-local refs can bind original exact anchors; alignment does not prove meaning. Translation of display must not rewrite accepted original claim. LLM output language fixed where practical; record unavoidable tokenization and context differences. Separate translation accuracy/cost from semantic interpretation and end-to-end user task. Reuse B3/B5 alignment and budget facilities only if verified adequate; no forced one-call-per-item translation.

## 7. Comparative tradeoff matrix (design estimates, not measured ranks)

| Dimension | A0 | A1 | A2 | A3 language variants |
| --- | --- | --- | --- | --- |
| Context preservation | Scoped parent/child partitions, known false plan | Same context with corrected ownership | Coherent source groups/whole ad, cross-group relation need | Original, translated or both; potential conflict/overhead |
| Evidence safety | Tested derived-field association and strict guards; known semantic false passes | Preserve hard association; repair proven scope/authority defects | Exact source identities where available, explicit unresolved, quarantine; new contract needs tests | Original binding and translation association distinct |
| Useful delivery | Whole pending or failure; separate source fallback | Similar whole delivery, fewer demonstrated blockers hypothesized | Candidate partial + source fallback; full only when justified | Same delivery contract; language fidelity affects result |
| Model demand | Large inherited prompt and fixed fields | Similar, possibly coherent narrower instructions | Fewer mandatory fields; richer context reasoning may be demanding | Language skill/tokenizer/dual context differences |
| Latency/cost | Historical long failure and nested retry potential | Potentially fewer failed reruns; unmeasured | Potential fewer redundant calls; larger context or recovery may offset | Translation/model-switch savings vs input and display costs |
| Implementation | Existing, no semantic change | Narrow versioned experimental patches; compatibility limits | New candidate envelope and reconciliation/view; higher initial burden | Depends on chosen common architecture and mapping |
| Maintenance | Deep inheritance and patch interactions | Modest local changes, risk new patch accumulation | More explicit ownership hypothesized; risk new generic framework complexity | Additional bilingual lineage and evaluation |
| Authority/compatibility | Existing pending/accepted selectors | Candidate isolation; no silent v5 semantics change | Sidecar initially, no automatic durable adapter | Same protection; no original-as-English shortcut |

These alternatives address RC01–03 (A1); RC04/06–09/12–13 (A2 with A1 comparator); RC10–11 (A3); RC05/16 (model/budget/recovery comparison); RC14–15 (protected authority and qualified presentation, separate V9 audit); RC17 (source-first and user-task evaluation); RC18 (DOC track and measured maintainability). Do not use any improvement direction to remove hard integrity/currentness guards.

## 8. Proposed discriminating sequence, not frozen protocol

1. Offline retained-response controls for A1; candidate design must preserve genuine meaning and reject genuine missing duty/unsupported scope. A1 may be rejected if repair harms meaning or requires unbounded special-case logic.
2. Model-only screen A0 with E4B and viable MiMo 9B challenger; exact current input/contract and shared bound. Preserve failure, not only complete outputs. If A0 causes all failures, record floor effect and compare selected same-task model pair on A2 separately rather than declare models equal.
3. Architecture-only A0/A1/A2 using incumbent, frozen common English v2 input and original evidence availability tracked; if A2 uses original for association only, explicitly keep that operation separate from model input. Score original-source meaning and delivery for all; exact English vs original evidence precision differences are outcomes, not erased.
4. Language-axis L0/L2/L3 and L1 if justified, on selected compatible architecture and same model, matched source context. Include native-English control and Persian/mixed language. Do not compare unpaired original v9 vs v30 as causal language study.
5. Selected interaction/challenger tests and recovery/partial delivery replay only if needed. Consider conditional 12B QAT or specialized translation if E2 hardware and budgets support them. No full model × architecture × language × recovery grid; no mandatory RAG/agents/embedding/training in E3. Source-brief/B4v6/original reading are practical output/utility controls.
6. E2.3–4 freeze cases, stratification, reviewers/exposure, thresholds, scoring denominators, caps and stop rules before new inference. E2.5 selects actual minimal experimental arms and explicit owner decisions where required; E2.6 reconciles docs and freezes E3. No new independent cohort until E4 applicable gates.

The sequence is a recommendation, not selected implementation. A1 and A2 are both legitimate candidates; A2 is the leading architectural hypothesis because it can address shared responsibility/delivery defects rather than patch isolated symptoms. A3 could complement either. If targeted repair delivers comparable fidelity/utility at lower cost, prefer it; if none improves over protected baseline, retain/defer. No proof yet.

## 9. Existing components to retain, adapt experimentally or leave alone

| Component | E2.1 disposition |
| --- | --- |
| Source acquisition, SQLite source versions, exact hashes/anchors, source policy | Retain unchanged; no fetch or parser rewrite needed to design alternatives |
| v30/v5 and compatible accepted paths, original v9/v4 | Preserve as current/baseline; candidate changes have distinct identity and isolated state |
| Stage A / B1 evidence and relation contracts | Reuse original span, pointer, lineage primitives and relationship semantics where suitable; E2.2 evaluate contract fit |
| B2v7 DOM and source brief | Reuse structural groups and read-only fallback; classification only candidate, not truth or exhaustive segmentation |
| B3/B5 alignment/budget | Reuse exact alignment and bounded transport concepts as compatible; validate context fidelity and actual enforcement |
| B4/B4v5/v6 | Reuse candidate evidence/visibility patterns; do not inherit misleading complete state, summary blast radius or translation dependency blindly |
| Analysis diagnostics/item review | Retain old contracts, examine actual failure/review states for new candidate receipt design; do not create competing authority ledger |
| Capability, Work, Registry, Market, public corpus | No new semantic consumer route or accepted facts. Historical V9 blast-radius audit independent. |
| AR.2 AI Lab and DOC.3/4/7 | Minimal reusable experiment manifests and component profiles; future generator only if useful, no general platform build |

## 10. Handoff, verification and limitations

E2.1 design deliverable contains required four directions, comparable dimensions, concrete processing responsibilities, causal evidence links, existing component reuse and no-change alternative. E2.2 should specify candidate authority, evidence group/child alignment, optional depth/experience, source vs inference relations, uncertainty and partial state, alternative scope, reconciliation and promotion compatibility. This is the next design task after E2.1 reconciliation; no final schema, implementation, model selection or scoring thresholds here.

Remote-only documentation increment: Desktop Commander reported both registered local devices offline. Remote main verified at exact base and E1 CI successful; reviewed repository tracker, E1 matrix, DOC.2 owners, architecture/domain/reasoning policy, Stage B and AI research references via GitHub. No new private source/DB access, no local verification/tests, no inference or production work. Reproducibility of E1 remains existing receipts, not new replay. Remote document-only diff, linked paths and tracker count to be verified at publication. E2.1 checkbox intentionally remains open pending local main synchronization and protected-state reconciliation under existing milestone discipline. Recheck with `git status --short --branch`, `git pull --ff-only` only if safe, exact HEAD/origin/main, `.venv/bin/python data/local-acceptance/2026-11-23-fresh-e2e-manual-audit/verify_reconciliation_2026_11_24.py`, and CI at new revision; then close E2.1 and proceed. If local changed or pull conflicts, preserve state and reconcile, not force. No data exports or automatic promotion. User has approved continuing design, not a selected architecture or governing contract change.
