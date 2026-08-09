# JobHunter Repository Instructions

These instructions apply to AI assistants and human contributors.

## 1. Product priority

JobHunter is a real repeated-use local utility.

Prefer dependable, inspectable, evidence-grounded behavior over impressive complexity. Speed means coherent useful increments, not bypassing tests, bounds, provenance, source policy, acceptance, or state.

The mature product is an evidence-backed personal career-intelligence system, not merely a scraper, generic job matcher, resume generator, or autonomous application bot.

---

## 2. Required reading order

Before material changes, read in this order:

1. `README.md`
2. `docs/PRODUCT_SPECIFICATION.md`
3. `docs/ARCHITECTURE.md`
4. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
5. `docs/SOURCE_POLICY.md`
6. `docs/ROADMAP.md`
7. `docs/IMPLEMENTATION_PLAN.md`
8. `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`
9. `docs/EXECUTION_TODO.md`
10. `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md` while the current semantic gate is active
11. `docs/WORKING_MEMORY.md` when present/current
12. feature-specific docs relevant to the task, including as needed:
    - `docs/SEMANTIC_ANALYSIS.md`
    - `docs/PHASE_2_CAPABILITY_INTELLIGENCE_PLAN.md`
    - `docs/ROLE_CAPABILITY_BLUEPRINT_PLAN.md`
    - `docs/LOCAL_WEB_APP.md`
    - `docs/SEARCH_CONFIGURATION.md`
    - `docs/TRANSLATION_AND_ENGLISH_CORPUS.md`
    - `docs/ACQUISITION_OPERATIONS.md`
    - `review-snapshots/README.md`

Proposal files under `docs/proposals/` are candidate inputs only. They do not authorize implementation.

`docs/WORKING_MEMORY.md` is a handoff/current-state aid, not a higher authority than the plans/specifications.

---

## 3. Authority chain

```text
product/domain/source/architecture constraints
        ↓
ROADMAP.md
strategic sequencing
        ↓
IMPLEMENTATION_PLAN.md
product-level exact order / gates
        ↓
PHASE_1_JOBINJA_AUTOMATION_PLAN.md
active Phase-1 detail
        ↓
focused active sub-plans
for example SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md
        ↓
EXECUTION_TODO.md
current operational checklist
        ↓
implementation / tests / live acceptance
```

If a lower artifact conflicts with a higher one, reconcile the conflict instead of choosing the convenient instruction.

---

## 4. Current exact implementation state

Active source/derived contracts:

```text
parser:                       jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2

English P1.6:                 job-analysis-english-v9
Original P1.6:                job-analysis-original-v9
P1.6 schema:                  job-analysis-v4

Capability:                   job-capability-intelligence-v4
Capability schema:            job-capability-intelligence-v2

Role Blueprint:               role-capability-blueprint-v2
Blueprint schema:             role-capability-blueprint-v1

Review Snapshot:              job-review-snapshot-v1
```

Do not write current-state documentation that calls v2/v3 P1.6 or earlier Capability/Blueprint prompt versions current. Historical incident records may retain old identities when explicitly historical.

---

## 5. Current accepted/strong foundations

Current strong foundations include:

- local Python modular monolith;
- SQLite structured state + immutable raw evidence;
- browser + CLI on shared services/data;
- bounded repeat-safe bilingual Jobinja discovery;
- stable job identity/discovery provenance;
- deterministic `jobinja-detail-v2` parsing;
- semantic source versions distinct from checks;
- classified source outcomes/cautious lifecycle logic;
- hardened `english-projection-v2` architecture;
- P1.6 Instructor/Pydantic structured factual extraction;
- per-job Capability Intelligence persistence/review surface;
- per-job Role Capability Blueprint persistence/review surface;
- independent analysis/capability/blueprint model configuration;
- Review Snapshot export for selected quality review jobs.

Historical translation-v1 remains preserved but non-current.

Phase 1 is **not closed** merely because these implementations exist.

---

## 6. Current exact next-work rule

Do not restart the old August-3 checklist from the beginning.

Follow the current TODO and semantic-quality plan:

```text
1. calibrate Capability Intelligence against accepted tG9K P1.6 artifact 29
2. calibrate Role Capability Blueprint
3. compare a stronger dedicated reasoning model only if evidence warrants it
4. complete CI-3 with heterogeneous real jobs using Review Snapshots
5. stop expanding semantic reasoning once accepted
6. finish Market/source/lifecycle/partial-success/P1.7 acceptance
7. close Phase 1
8. only then begin corpus-wide Phase 2
```

Integrated snapshot model routing and B2 P1.6 factual coverage/optionality/depth are accepted. The first current code task is Capability Intelligence calibration in B3/SQ-2.

---

## 7. Current semantic-quality philosophy

### P1.6

Strict factual substrate.

- preserve explicit source facts;
- exact selected-representation evidence;
- do not invent missing requirements;
- do not omit meaningful explicit requirements on dense postings if the contract can represent them;
- keep obligation strength and technical depth separate;
- do not spread one depth adjective across neighboring tools;
- uncertain/source-ambiguous claims should remain contextual/unknown rather than forced.

### Capability Intelligence

Auditable machine reasoning.

- connect work and requirements;
- decompose only as evidence supports;
- distinguish `source_explicit`, `strongly_implied_by_work`, `model_inferred_prerequisite`, `unknown_or_unsupported`;
- keep unknown scope explicit;
- do not upgrade optional source wording into mandatory capability depth;
- deterministic bookkeeping issues are repaired in code, not by repeated full LLM calls.

### Role Capability Blueprint

Human-facing professional interpretation.

- use the professional frame that fits the vacancy;
- add useful interpretation beyond rereading the ad;
- preserve upstream optionality/unknowns;
- a technology list is not an architecture specification;
- possible/likely examples remain examples;
- `highly_likely` must not contradict an unresolved unknown;
- technical correctness matters more than sophisticated prose;
- avoid domain-specific prompt-patch collections.

---

## 8. Current live acceptance anchors

```text
t4jp  sparse/ambiguous AI-content source
tG9K  rich semiconductor/industrial-ML source
```

`t4jp` tests conservative behavior when the source is weak.

`tG9K` tests long/dense factual coverage and deeper reasoning. Current selected review artifact:

```text
review-snapshots/jobs/tG9K.json
```

Use Review Snapshots as the normal handoff/review evidence instead of manually pasting long browser pages.

---

## 9. Review Snapshot rules

Normal command:

```bash
jobhunter jobs snapshot <job-id>
```

Default output:

```text
review-snapshots/jobs/<job-id>.json
```

The live SQLite database remains local and ignored.

Snapshots are generated review artifacts, not runtime inputs.

Do not automatically commit every job. Commit selected acceptance/review examples intentionally after inspecting the diff.

Snapshots deliberately exclude raw model responses, prompts/request bodies, SQLite/WAL/SHM, raw HTML contents, secrets, logs, and private user state.

The integrated `jobhunter jobs snapshot` command passes effective analysis/capability/blueprint model-role arguments to the exporter. The selected `tG9K` snapshot records those configured roles explicitly.

---

## 10. Record and authority boundaries

Never conflate:

```text
JobPosting                    logical source identity
SearchPageSnapshot            exact search evidence
JobPostingVersion             meaningful employer-content version
JobDetailFetchObservation     operational source check
JobLifecycle state/event      cautious source-availability interpretation
JobTranslationArtifact        derived English view
JobAnalysisArtifact           P1.6 strict factual interpretation
Capability artifact           auditable reasoning above P1.6
Role Blueprint artifact       human-facing interpretation
JobUserWorkflow               local triage state
Market aggregate              deterministic accepted-P1.6 aggregate
Review Snapshot               generated review export
Raw evidence                  authoritative acquired bytes/metadata
```

Authority:

```text
source/original employer text
→ parsed fields
→ English projection
→ P1.6 factual extraction
→ Capability reasoning
→ Blueprint interpretation
```

No downstream layer replaces upstream authority.

---

## 11. Interaction-surface rules

```text
local browser UI   normal repeated human use
CLI                automation/debug/advanced operation
```

Both use the same application services and SQLite/evidence stores.

Do not create browser-only parsing, translation, analysis, or reasoning truth stores.

---

## 12. Browser/security rules

- loopback-first;
- explicit intent required for non-loopback binding;
- CSRF on mutating forms;
- restrictive CSP/security headers;
- local static assets; no runtime CDN requirement;
- acquired content is untrusted data;
- one mutable browser operation at a time unless concurrency is proven safe;
- source/English/P1.6/Capability/Blueprint/user state must remain visually/semantically distinct;
- persistent advanced configuration stays in TOML until safe write UX is justified.

---

## 13. Source/acquisition discipline

- search vocabulary is TOML data, not Python career taxonomy;
- preserve display terms; normalize only where identity requires it;
- bounded pages/requests/details;
- sequential/rate-limited Jobinja acquisition;
- raw valid evidence before downstream processing;
- acquisition remains useful without LM Studio;
- source/provider failure != legitimate empty result.

Retry only explicitly transient classes.

Critical lifecycle invariant:

```text
500/502/503/504/network/429/challenge/auth/access failure
!=
expired/removed vacancy
```

---

## 14. Quick Add/source policy

Quick Add may accept only current approved Jobinja inputs:

- one public Jobinja job URL;
- one public Jobinja `/jobs` URL;
- one Persian/English keyword phrase interpreted as bounded Jobinja search.

It is not an arbitrary-web policy bypass.

Do not automate login/applications, private profiles, CAPTCHA bypass, paywall/access bypass, proxy rotation, or autonomous messages.

---

## 15. Translation rules

Current trusted contracts:

```text
lm-studio-translation-v2
english-projection-v2
```

- preserve v1 historically;
- one semantic segment per current hardened translation request;
- content-derived response identity;
- strict structured output;
- deterministic source/English integrity validation;
- source text is never shortened to fit translation batching;
- native English is identity-projected;
- translation failure never mutates source evidence/history.

---

## 16. P1.6 rules

Production v4 uses evidence-reference IDs internally and persists exact resolved source text.

Current generic protections include:

- heading-aware long-field segmentation;
- clause evidence references;
- rich-source empty-analysis guard;
- mixed-strength atomicity;
- preference wording validation;
- exact duplicate normalization;
- final independent evidence/domain validation;
- no arbitrary read timeout after successful local connection.

Do not scale model work before reviewed real-job acceptance.

---

## 17. Capability evidence resilience

- supported claim + valid evidence + bad extra reference → keep valid evidence;
- supported claim + invalid-only evidence → fail closed;
- `unknown_or_unsupported` + invalid-only evidence → normalize to `[]`;
- do not spend full model retries on purely mechanical unknown-scope reference cleanup.

---

## 18. Independent model roles

Configuration supports:

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

Use controlled same-job comparison when model adequacy is the variable. Do not change evidence/prompt/schema/model simultaneously.

No multi-model voting unless a future measured requirement explicitly justifies it.

---

## 19. Market rules

Current Market aggregates accepted/current English P1.6 only.

Always retain/recover:

- analyzed sample size;
- source/filter scope;
- requirement-strength semantics;
- contract identity;
- sampling/concentration warning state.

Capability/Blueprint are not yet Market inputs.

---

## 20. Partial-success rules

For multi-stage work expose where applicable:

```text
requested
attempted
completed
reused
skipped intentionally
failed
remaining eligible
```

Successful durable earlier work remains even when a later stage fails.

Do not call mixed success a simple success.

---

## 21. Personal-evidence boundary

Do not implement personal readiness/gaps/recommendations until a reviewed personal-evidence schema exists with depth, confidence, recency, evidence references, limitations, and AI-assistance/independence context.

Do not turn chat memory, repository dependencies, or project completion into durable mastery claims.

---

## 22. Architecture-evolution discipline

- preserve local modular monolith;
- keep SQLite until measured limits justify replacement;
- implement a real second source before generic adapter/plugin abstraction;
- structured/keyword queries before embeddings/RAG;
- no graph/vector DB without demonstrated query need;
- no autonomous agent orchestration without measured benefit and explicit privacy/provenance/budget controls.

---

## 23. Development rules

- build coherent vertical increments;
- separate deterministic logic from network/model/provider calls;
- keep handlers thin;
- keep SQL in focused repositories/read models;
- use typed config and versioned contracts;
- preserve historical artifacts;
- reconcile docs whenever implementation state materially changes;
- normal tests never contact Jobinja/Google/LM Studio;
- important real incidents become deterministic fixtures where possible.

---

## 24. Definition of done

An increment is done only when:

- intended local workflow works;
- Ruff/tests/warnings acceptance gates pass where applicable;
- live source/model behavior is reviewed when required;
- failures are bounded/inspectable;
- partial-success semantics are honest;
- provenance/dependencies are retained;
- docs match behavior;
- privacy/network boundaries are explicit;
- no unrelated future scope is claimed.

Work directly on `main` unless a concrete isolation need appears.
