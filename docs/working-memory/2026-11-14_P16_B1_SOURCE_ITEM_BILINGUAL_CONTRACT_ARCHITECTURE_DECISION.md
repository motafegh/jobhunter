# P1.6 Stage B1 — Source-item, bilingual alignment and review-authority ADR

**Date:** 2026-11-14
**Disposition:** B1 architecture selected and contract examples validated; **B2 implementation NOT STARTED**
**Parent accepted state:** `main` at `73b170ced75d1ee424cf5d8a90f4d47b5ea1c893` (B0 closed)
**Scope:** Contract design and source-safe validation tooling only; no public P1.6, UI, database, model, translation, or downstream routing modifications
**Controlling plan:** `docs/P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md` §B1
**Frozen B0:** `docs/working-memory/2026-11-14_P16_B0_FROZEN_BASELINE_AND_EVALUATION_PROTOCOL.md`

## 1. Decision and tradeoffs

**Selected (A): non-authoritative, versioned, source-owned sidecar candidate contract**, with separate exact original-source references, parsed board-field references, proposed semantics, obligation/eligibility logic, English association, evidence review and a bounded job-understanding brief. B1 publishes only design schemas, machine validators, real exposed case examples and test cases. B2 and later may implement a private candidate producer that emits this shape or a justified revision. The accepted v30 English analyzer and original v9 analyzer remain the only public current pipelines.

**Rejected (B): direct modification of v30 evidence/prompt or injecting original Persian evidence into its English-only artifact.** Current `english-projection-v2` proves field-level association but not item-level translation. Adding Persian spans under an old English-v30 version would hide changed evidence authority, produce false currentness, and risk downstream Capability/Work/Market reuse of unreviewed facts.

**Deferred (C): an immediate `english-projection-v3` schema and new durable bilingual SQLite analysis table.** Such a migration is not justified by four exposed cases. B3 must test per-item translation association and fidelity before deciding whether v2 plus a separate sidecar suffices; B4 must demonstrate actual usefulness; B5 must evaluate genuinely new sources; B6 owns any durable migration, rollout and rollback decision.

**Explicit nondecision:** This ADR does **not** accept a new requirement taxonomy, LLM-generated source classification, language-model preference strength, or individualized job/career judgment. Every meaning field in the exposed B1 design examples is **assistant-proposed from earlier exposed source review**, not independently certified employer truth.

## 2. Contract ownership and examples

| Deliverable | Current B1 design / accepted reference |
| --- | --- |
| Exact original description anchor | Reuse accepted `jobhunter-source-span-identity-v1` and `OriginalSourceAnchor`; SHA-256, source job ID, detail version, field hash, character and UTF-8 offsets; **no semantic authority** |
| Structured board field value | Separate draft `structured_board_value` reference bound to original source semantic SHA, field name, JSON Pointer selection, canonical field/value JSON SHA-256 (see §3). **Not** an invented description anchor |
| Source-item meaning candidate | `item_id`, source reference, `category`, `employer_strength`, `basis`, `qualifier_status`, `scope`, and a separate review label |
| Per-item English association | Source-item-to-target relation with state, immutable source/translation IDs, translated target references where available, and independent linguistic meaning review |
| Eligibility structure | Explicit, source-owned directed acyclic graph of `all_of` and `any_of` with leaf item references, original qualifier-anchor references and conditional requirement scope |
| Metadata conflict | Two distinct source-labeled references plus a typed conflict relation; never overwrite board text or silently convert it into employer prose |
| Item review provenance | Append-only events keyed to item, dimension, source-value digest, reviewer class and previous-event ID; **not** a second “accepted” production database |
| Candidate brief | May later show supported facts and unknowns; always `candidate_only` and `downstream_authority=none`; B1 does **not** generate a user-facing brief |

The reference schema is `docs/contracts/p16-stage-b1/source_evidence_bundle.schema.json`, contract marker `jobhunter-stage-b1-source-evidence-bundle-draft-v1`. A pure inspection utility, `scripts/validate_stage_b1_design.py`, validates schema, references, review provenance, field-vs-original authority, duplicate/cyclic graphs, and optionally verifies source and translation identities against an explicitly supplied source object. It is **not** imported by public JobHunter runtime.

Four source-safe A1 examples are frozen in `docs/contracts/p16-stage-b1/fixtures/`, with hashes and exact source offsets but without raw Persian job descriptions. The fixture index records precisely four **exposed** scenarios and zero unseen or accepted candidate analyses. Private original content, the fixture-generation script and source review remain in ignored local `data/local-acceptance/`.

## 3. Item identity and source split design

**A. Description source spans.** New items reuse the accepted exact `OriginalSourceAnchor` identity and canonical `description` field only. Source job ID, parsed detail version and semantic SHA are mandatory. An exact span can be (a) a whole employer clause, (b) a nested fragment, or (c) a context/heading cue; source text need not be line- or sentence-delimited. Overlap is legal when one qualifier governs multiple nested technical alternatives. A span's presence does **not** prove it is required, preferred, a duty, or a valid split. Heading absorption, incidental mentions and partially missing scopes must produce `unresolved` rather than a fabricated exact item. For auditability, any later automated segmentation must preserve the pre-split exact original substring and its enclosing qualifier.

**B. Structured source metadata.** Source-derived arrays such as Jobinja `skills` and scalar fields like `minimum_experience`, `education`, `salary`, and `employment_type` are represented by `structured_board_value`, not `OriginalSourceAnchor`. Its `selector` is a JSON Pointer into the frozen parsed original fields (e.g. `/skills/3`, `/employment_type`) with `field_json_sha256` and `selected_value_json_sha256`. For draft v1, SHA input is UTF-8 of canonical `json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))`. Source-version identity plus these hashes prevents reusing the same index with shifted meaning. The B2 implementation must define pointer escaping and reject values absent from parsed source. This is a **new draft source-field reference**, not an extension to the accepted description-only span utility.

**C. Authority by origin.** The original employer narrative explicitly saying a skill is *optional* has stronger evidentiary force for what the employer *actually required* than a board `skills` label. A structured board value remains a real observed source fact, but it alone cannot establish `employer_strength=required`. A mismatch creates a conflict relation; neither value disappears. A board-level Bachelor's degree, “full-time,” experience range or salary must not be silently reattributed as an employer-prose sentence.

**D. Category vs strength vs conditional scope.** `category` identifies work duty, candidate qualification, behavior, work arrangement, compensation, benefit, application instruction, context or unresolved. `employer_strength` separately records `required`, `preferred`, `stated_expectation`, `not_applicable`, `unresolved`. `basis` records exact original wording vs source-section context vs model inference vs board metadata. `qualifier_status` preserves explicit negative wording. `scope` is `standalone`, `alternative_path`, `chosen_option` or `not_applicable`. An OR-choice leaf is *required only if that option is chosen*, not a globally mandatory applicant skill. Model-inferred obligation may be shown as a **hypothesis**, not labeled an employer-explicit required skill.

## 4. AND/OR eligibility truth table (source-first, not applicant matching)

The `tMps` Middle-vs-Senior example is represented as:

```text
eligible = middle OR senior
middle = middle_experience AND (LLM OR RAG OR GenAI OR ML OR NLP)
         AND completed_project
senior = senior_experience AND designed_and_production_deployed_system
```

This representation preserves both the **OR between tracks** and the **OR within Middle experience domains**; conditions inside each track remain **AND**. A leaf labeled `required` and `chosen_option` cannot be flattened into a standalone mandatory skill. Under the exposed contract test values, Middle-years + completed-project alone is **false**; adding one source-listed domain makes that Middle path **true**. Senior experience + deployment makes the Senior path true without needing Middle experience. These are only Boolean truth-table examples, **not** determinations about the user's eligibility.

The `tNDx` credential example retains **certificate OR equivalent knowledge**. Choosing either path is sufficient for that specific equivalence condition; a separate overall Network+/Security+ conceptual requirement remains part of the employer's statement. The Kaspersky specialist certificate and government-customer experience have **unresolved strength** because the original source does not make their modality unambiguous. Their existence as source phrases is **not** evidence that they are required or preferred. The code-level test harness evaluates the graph over synthetic truth assignments only; it is not a product applicant matcher.

All eligibility graph roots and `all_of`/`any_of` nodes must be acyclic, referenced, and linked to original qualification items and explicit qualifier anchors. Unreferenced, dangling or self-looping paths are validation failures. Work arrangements and job duties cannot become eligibility leaves.

## 5. Translation alignment and fidelity authority

| Relation state | What it establishes | What it does NOT establish |
| --- | --- | --- |
| `native_english_exact` | Verified byte-exact original/native-English description and exact target offsets for the same source version | Automatic semantic review of a separately inferred classification |
| `source_bound_translation_candidate` | A source-item-bound local request/output identity and target span digest, with recorded provider/model/prompt where created | Correct negation, requirement strength, years, section roles or target semantic equivalence |
| `legacy_field_only_unaligned` | Historical `english-projection-v2` has a related translated description field and known artifact hash | Any one-to-one Persian/English item offsets, item meaning or old v30 evidence expansion |
| `semantic_mismatch` | Explicitly recorded contradiction in meaning, with a traceable target reference | A usable item for factual authority |
| `unresolved` | Alignment is not established | A failure to recover employer original facts |

The draft `legacy_field_only_unaligned` is intentionally mapped to the existing Stage A name `translated_field_only_unaligned`; they refer to the same lack of item alignment and do **not** replace or rewrite the accepted Stage A contract. Source-bound translation is intentionally many-to-many **at the relation level**: more than one target item may relate to one original span, and overlapping source fragments may share a target; each target must carry its own identity and review. Mere string similarity is not sufficient to call an old v2 field per-item aligned.

Translation semantic checks must guard negation, preference/modality, alternative conjunctions, years, credential/equivalence, factual scope, section headings and role/task/qualification transitions. The four exposed A1 source records already demonstrate unsafe heading insertion, heading absorption and mistranslation of a professional trait. These are B3 **verification targets**, not failures that a schema alone solves.

## 6. Five orthogonal review / execution dimensions

| Dimension | Candidate status and what proves it | Durable authority? |
| --- | --- | --- |
| Original source integrity | Deterministic exact source version, SHA, offsets, value hash and parser version | Necessary but not sufficient |
| Translation association | Native exact; source-bound candidate; translated legacy field-only; mismatch/unknown | Item relation only |
| Linguistic meaning fidelity | Unreviewed / assistant checked / independently checked / contradicted | Separate semantic evidence needed |
| Employer category/strength | Candidate / assistant checked / independently checked / rejected; explicit original cue vs heading/context inference | No automatic employer-required upgrade |
| Operational execution and reusable authority | Attempt not run / complete / partial / failed / timeout; candidate view vs explicit downstream approved contract | **B6 only** |

B1 JSON `review_events` retain event, item, dimension, exact source digest, reviewer provenance and predecessor. **Review dimensions are not interchangeable**: an independent/assistant finding on translation association or source integrity cannot satisfy an item-level `semantic_classification` review status. This is enforced with negative contract tests. Board JSON Pointer traversal additionally rejects malformed RFC 6901 escapes and noncanonical array indices. They do not modify the pre-existing database review history. Assistant source review is recorded as `assistant_prior_context_exposed`, never as independent human assessment. Existing `AnalysisItemReviewStore` applies to **pending v5 English P1.6 artifacts** and its append-only event/fence protects the existing accepted English route; the new sidecar will **reuse its principles, not mutate its tables**. Existing original-language v9 mechanically accepted status remains historical; B1 does not retrospectively certify it.

**Promotion boundary:** In B4, a bounded job brief may show directly source-linked facts with accurate category/strength and explicit unknowns after the source integrity and relevant interpretation check; a board-only tag cannot claim employer strength. In B6, any durable new accepted P1.6/Capability/Market reuse requires **additional explicit review and compatibility authority**, a reviewed promotion policy and evaluation results; it is never inferred from successful JSON validation or assistant-only review. Human manual review is not required for every candidate user-facing brief, consistent with the product reasoning policy.

## 7. Implementation ownership, persistence/API compatibility and rollback

| Future slice | Ownership / implementation decision |
| --- | --- |
| B2 original interpretation | Use existing `TranslationSourceVersion` / parsed `job_detail_versions` read path, accepted Stage A anchors, typed board field references and source semantics; avoid adding code to `source_span_identity.py` that claims classification authority |
| B3 bilingual semantic fence | Implement a separate, versioned item relation and local LM Studio bounded provider path; do not modify `english-projection-v2` artifacts or v30 evidence format |
| B4 useful bounded view | Candidate-only sidecar JSON in isolated ignored workspace initially; optional read-only CLI/HTML diagnostic view, no stable downstream consumers or unreviewed accepted database rows |
| B5 evaluation | Use frozen B0 unseen selection and original-source scoring protocol, not previously exposed four A1 ads as holdouts |
| B6 migration and public API | **Separate accept/no-promote decision**; if approved, additive versioned tables or fields only, backup, idempotent migration, source-dependency currentness and rollback, safe browser/CLI route and downstream fences |

**No migration is approved in B1.** B0 local source/accepted state, historical artifact IDs `36/37/39/44/46`, accepted Capability IDs `11–15`, Work, Registry, Market snapshot 15/report 2 and corpus content remain invariant. On B2–B4 failure, delete or abandon isolated sidecar candidates; public v30 remains active. On any hypothetical B6 failure, restore explicit prior route and backed-up state. The new draft contract never substitutes for `job-analysis-v5` and has no ability to write to accepted P1.6 tables.

## 8. B1 acceptance evidence and limits

**Files:**

- `docs/contracts/p16-stage-b1/source_evidence_bundle.schema.json` — versioned JSON Schema 2020-12 draft, source-safe metadata-only example format.
- `docs/contracts/p16-stage-b1/fixtures/{tNhZ,tMps,tNDx,tMjm}_source_safe_design.json` and `INDEX.json` — four **exposed** source-anchored design examples with exact identities/hashes but no employer original text.
- `scripts/validate_stage_b1_design.py` — pure design validator, cross-reference/graph/review/source-hash checking and synthetic AND/OR truth-table evaluator; **not a production component**.
- `tests/test_p16_stage_b1_contract_design.py` — schema, real A1 case classification boundary, 12 Boolean logic assignments, negative-contract mutations (including review-dimension isolation and noncanonical JSON Pointers), exact private source verification when available, and stable v30 routing.
- `docs/working-memory/2026-11-14_p16_b1/DECISION_REGISTER.json` — machine-readable selected/rejected/deferred decisions and no-promote disposition.

**Engineering verification:** Local full warnings-as-errors suite: **946 passed**; B1 focused suite: **39 passed**; repository Ruff, installed dependency consistency and Git diff checks passed. Four source-safe fixtures and their index/schema digests were independently rechecked; frozen B0 exposed-source snapshot SHA-256 remained `bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe`. No accepted data/database/current P1.6 route changed. Separate PR CI is required before merge.

**Verification claim boundaries:** JSON Schema validation establishes **structure**, and the design validator establishes referential safety and (when original private data are available) exact original-source and legacy translation identity. It cannot independently certify the model's interpretation, the employer's intent, fluent Persian-to-English meaning preservation, complete job coverage, or generalization. The original assistant A1 review had prior model context; the fixtures inherit that limitation. CI without private A1 source verifies schema and reference *shape*, while source-exact verification is retained in the ignored local B0/B1 evidence.

**B1 gate status:** Contract shape/ADR and source identity reference examples prepared. Full test/CI and merge outcomes are recorded in the separate B1 closure; **do not mark B2 started until B1 actually passes CI and is reconciled into main**.

## 9. First executable B2 slice after B1 acceptance

Start a new branch from the accepted B1 main commit. First implement a **read-only deterministic source-item candidate renderer**, using current exact original spans and board-value references, with general tests around headings, scope, strength, alternative group boundaries and metadata conflict detection. Keep original parsed source as the reference, abstain on uncertain certificate strength, and do not persist new accepted facts. Demonstrate meaningful improvement on the already exposed four A1 cases before introducing source-bound language-model translation in B3.

B2 success is not a new P1.6 release. Fresh unseen validation and controlled promotion remain B5/B6.
