# JobHunter Product Specification

**Status:** Current product definition  
**Product type:** Local-first personal career-intelligence application  
**Primary user:** Repository owner  
**Strategic roadmap:** `docs/ROADMAP.md`  
**Controlling delivery plan:** `docs/IMPLEMENTATION_PLAN.md`

## 1. Purpose

JobHunter converts selected job-market data into reliable, actionable personal career intelligence.

The complete product should eventually answer:

- Which real role families match the intended career direction?
- What responsibilities do those roles actually perform?
- Which skills, knowledge areas, tools, practices, deliverables and experience patterns recur?
- What depth appears expected?
- Which requirements are required, preferred, contextual or inferred?
- Which personal differences are knowledge, practice, depth, integration, evidence, recency, experience-context, presentation or constraint gaps?
- What actions should be learned, practised, built, improved, documented, assessed, monitored, investigated or ignored for now?
- Which opportunities are reasonable now, which need preparation, and why?
- How does the observed target market change over time?
- What explicit evidence changed after learning, building, applying or receiving real feedback?

Job acquisition is therefore an input subsystem, not the final product value.

## 2. Product character

JobHunter is a **real repeated-use local utility**, not a learning-roadmap artifact, generic job board, opaque fit-score engine, or autonomous application bot.

Daily usefulness, data integrity, explainability, privacy, configurability, maintainability, conservative evidence handling and repeated-run reliability control product decisions.

The normal human interaction surface is the local browser application. The CLI remains a supported technical interface for automation, debugging, tests and advanced workflows. Both operate on the same application services and durable records.

## 3. Authority and roadmap relationship

Product/domain/source/architecture documents define what JobHunter is allowed to mean and how evidence authority works.

```text
PRODUCT_SPECIFICATION.md
DOMAIN_AND_ANALYSIS_MODEL.md
SOURCE_POLICY.md
ARCHITECTURE.md
        ↓
ROADMAP.md
strategic sequencing / proposal disposition
        ↓
IMPLEMENTATION_PLAN.md
exact delivery order / acceptance gates
        ↓
phase-specific plans
        ↓
implementation / tests / live acceptance
```

`docs/proposals/` remains a non-controlling candidate-idea library. Proposal presence never authorizes implementation.

## 4. Current operating experience

The browser application can currently support the Jobinja-centered repeated workflow through implemented Phase-1 surfaces:

1. inspect current corpus and pipeline coverage;
2. inspect the configured bilingual search catalog and generated bounded plan;
3. start bounded Jobinja discovery/sync operations;
4. browse/filter local jobs using human-readable source/workflow states;
5. use Quick Add for an approved Jobinja job URL, Jobinja search URL or Persian/English keyword phrase;
6. inspect original employer data and derived English representation separately;
7. inspect source evidence identity, semantic versions and source-check history;
8. refresh/fetch missing or due job details;
9. translate/repair one job or a bounded eligible queue using current translation-v2 rules;
10. run the deterministic parser audit;
11. run bounded evidence-backed P1.6 semantic analysis for eligible jobs;
12. inspect per-job responsibilities/requirements and their exact source evidence;
13. inspect the first Market aggregation over current analysis artifacts;
14. inspect search-effectiveness/provenance information;
15. inspect long-running browser-operation state/results;
16. use the same underlying services through CLI paths for advanced operation/debugging.

Several newer Phase-1 capabilities are **implemented but remain acceptance-pending**. The master and Phase-1 plans define the exact live acceptance sequence.

One failed search, posting, parser, translation, semantic-analysis or UI operation must not invalidate successful durable work from the rest of a bounded run.

## 5. Current inputs

### 5.1 Approved current inputs

- packaged or user-supplied bilingual search catalog TOML;
- configured profiles and packs;
- user-defined Persian/English keyword groups;
- approved public Jobinja result URLs;
- public Jobinja job URLs supplied directly through Quick Add;
- one-off Persian/English Quick Add search phrases;
- public Jobinja job pages discovered by the application;
- local TOML configuration;
- local LM Studio configuration;
- optional Google Cloud Translation credentials when deliberately selected.

### 5.2 Later approved-input families

Only after explicit design/policy promotion:

- pasted/local job documents;
- additional approved public source adapters;
- public ATS/API feeds;
- personal capability evidence;
- manual review/correction decisions;
- application/outcome state;
- optional additional inference providers subject to privacy policy.

## 6. Current outputs

### 6.1 Acquisition/source outputs

- inspectable effective search plan;
- bounded request/detail selection;
- immutable search/detail evidence;
- logical JobPosting identities;
- discovery provenance;
- semantic posting versions;
- successful/failed detail-fetch observations;
- classified source-response/failure states;
- cautious lifecycle evidence/state;
- parser audit findings;
- user workflow triage kept separate from source truth;
- concise acquisition/operation summaries.

### 6.2 Derived English corpus

- one English projection tied to one exact current source semantic version;
- structured English fields;
- one complete English document;
- native-versus-translated segment provenance;
- provider/model/schema contract identity;
- completed/failed/reused translation attempts;
- current-version-only export.

The English corpus is derived convenience data and never replaces original employer text.

### 6.3 Semantic-analysis outputs — implemented, acceptance pending

P1.6 can produce versioned model-derived artifacts containing:

- role purpose;
- responsibilities;
- requirements;
- requirement strength: required / preferred / contextual / inferred;
- concept type;
- confidence;
- exact original-source evidence excerpt;
- rationale for inferred concepts;
- exact model/prompt/schema identity;
- retained structured request and raw provider response;
- completed/failed/reused operational attempt state.

A material claim whose evidence cannot be validated against authoritative employer fields must not become an accepted analysis artifact.

### 6.4 Market outputs — first implementation, not yet Phase-2 canonical market intelligence

The current Market surface can aggregate accepted/current P1.6 artifacts for bounded sample inspection. It may show:

- analyzed sample size;
- responsibility-claim counts;
- concept/requirement prevalence by posting;
- required/preferred/contextual/inferred posting counts;
- search-effectiveness/provenance-related views.

This layer is **not yet** a reviewed canonical taxonomy, duplicate-adjusted market model or complete-labor-market claim.

### 6.5 Browser outputs

- dashboard/coverage metrics;
- guided bounded operations;
- Quick Add intake for approved Jobinja inputs;
- filtered job catalog;
- source/English/analysis job detail views;
- source-check/lifecycle state;
- search-catalog/profile/pack views;
- first Market view;
- live/recent browser-operation state/results;
- local system/configuration/provider visibility.

## 7. Core authority model

Never conflate:

```text
original employer/source text      authoritative market evidence
deterministic parsed source fields source-derived
English projection                 translation-derived convenience
semantic analysis                  model-derived interpretation
canonical taxonomy                 reviewed/derived mapping
market aggregate                   deterministic aggregate of accepted derived claims
user triage                         local workflow state
personal evidence                  future user-provided/reviewed evidence layer
recommendation                     future explainable system-derived decision
```

No derived layer becomes more authoritative than the evidence from which it was produced.

## 8. Functional requirements

### FR-1: Source registry and acquisition policy

Every recurring source must have explicit method, bounds, policy and accepted hosts/paths. JobHunter must not silently expand from approved public acquisition into unrestricted crawling.

Quick Add is an operator input, not a policy bypass. Non-Jobinja URLs remain rejected until another source has an approved adapter.

### FR-2: Reproducible source evidence

Record acquisition/check outcomes and preserve retrieved evidence before model processing. Directly supplied approved job URLs must enter the same logical source/evidence model as search-discovered jobs.

### FR-3: Data-driven bilingual search planning

Search vocabulary is versioned data rather than Python constants. Persian and English terms, normalized identity/deduplication, raw approved URL escape hatches, plan inspection, search windows and global request bounds must remain supported.

Search vocabulary is acquisition recall. It is not career taxonomy, fit truth or a personal target-role specification.

### FR-4: Identity/version/check separation

Distinguish logical posting identity, raw source observation, meaningful semantic employer-content version and operational source check.

Transient HTTP/HTML changes must not manufacture semantic job versions.

### FR-5: Evidence-preserving deterministic extraction

Explicit source facts are parsed deterministically. Missing source fields remain missing. Model output cannot become source truth.

### FR-6: Conservative source failure/lifecycle semantics

Source outcomes must preserve classes such as normal/active, rate limited, access denied, challenge/auth, not found/gone, server/network error, unexpected content and explicit expiry where supported.

Critical invariant:

```text
provider/source failure != legitimate empty result
transient network/5xx != expired or removed vacancy
```

Destructive lifecycle conclusions require the defined evidence sequence; they must never be inferred from one transient failure.

### FR-7: Derived English projection

For accepted source semantic versions, JobHunter must be able to build an English view that:

- preserves source evidence unchanged;
- passes native-English segments through without translation calls;
- translates Persian-containing semantic units through an isolated provider;
- retains native/translated provenance;
- records provider/model/schema identity;
- is idempotent;
- becomes stale when a newer semantic source version exists;
- rejects malformed/corrupt output rather than creating a false current artifact;
- exports independently from source evidence.

### FR-8: Translation-provider isolation

LM Studio is the normal local translator. Optional external translation remains deliberate and policy-controlled. Provider/model failures must not modify source history.

### FR-9: Browser application

The browser application must:

- operate on the same services/database as the CLI;
- provide normal daily controls without requiring CLI knowledge;
- explain important limits and state transitions in user-facing language;
- never bypass acquisition/model bounds;
- distinguish source truth from English/model/user-workflow state;
- expose partial failures rather than collapsing them into generic success;
- remain local/loopback-first;
- protect mutating forms from CSRF;
- ship local static assets rather than runtime CDN dependencies;
- avoid a second durable browser-only truth store.

### FR-10: Evidence-backed structured semantic inference

Durable semantic analysis must:

- use versioned prompt/schema/provider/model identity;
- retain raw structured request/response evidence where required by the contract;
- separate analysis from translation/source truth;
- require exact original-source evidence for material claims;
- validate evidence locally;
- reject unsupported/hallucinated evidence;
- keep uncertain claims omitted/reviewable rather than guessed;
- remain bounded by configured batch/token limits.

### FR-11: Requirement classification

Semantic analysis must preserve required, preferred, contextual and inferred distinctions. Inferred concepts require an explicit rationale plus source evidence.

Future refinements such as requirement depth/criticality must not weaken the current strength distinction.

### FR-12: Canonicalization

Future career-concept aliases may map to reviewed canonical concepts without losing source wording. Search normalization, translation and career-taxonomy canonicalization remain distinct operations.

### FR-13: Human review and reversibility

Future semantic/taxonomy/personal-evidence corrections must remain reviewable and reversible where they affect durable intelligence. Original source/model history must not be silently overwritten.

### FR-14: Market truthfulness

Every market view must expose or retain enough context to recover:

- source scope;
- analyzed sample size;
- filter scope;
- analysis/taxonomy contract;
- required/preferred/etc. semantics;
- duplicate/repost-adjustment state where applicable.

Small/concentrated samples require explicit warnings before broad market conclusions are presented.

### FR-15: Personal capability evidence

Future personal capability claims require explicit reviewed evidence with depth, confidence, recency, evidence type/reference, limitations and AI-assistance/independence context where relevant.

Binary `known/unknown` is insufficient.

Chat memory, repository keywords, dependency files and project completion do not automatically prove mastery.

### FR-16: Explainable gap/readiness/action intelligence

Future gap/readiness recommendations must expose:

- employer/market evidence;
- personal evidence;
- gap class;
- requirement strength/depth context;
- uncertainty/unknowns;
- constraints/preferences;
- decision policy;
- what would change the conclusion.

Prefer categorical/requirement-by-requirement decisions over opaque fit percentages.

### FR-17: Application preparation

Future resume/interview/application assistance must derive material user claims only from reviewed personal evidence. The user remains final approver.

JobHunter must not autonomously submit applications or recruiter messages.

### FR-18: Outcome learning with causal restraint

Future application outcomes and explicit employer feedback are separate records. `Rejected` plus a known gap does not prove `rejected because of that gap`.

### FR-19: Export/backup/recovery

Public market data, derived corpora and future personal evidence must have explicit export/backup boundaries. Before irreplaceable personal evidence is stored long-term, supported backup/restore must exist.

### FR-20: Advanced retrieval/AI only after demonstrated need

Structured/keyword queries remain preferred while sufficient. Embeddings/RAG, multi-provider routing and bounded specialist agents require explicit evaluated use cases and must preserve provenance/privacy/bounds.

## 9. Non-functional requirements

- **Local-first:** normal use does not require a cloud AI service.
- **Browser-local by default:** UI binds loopback unless exposure is explicit.
- **Inspectable:** source evidence, source versions, translations, analyses, aggregates and operation outcomes remain traceable.
- **Idempotent:** reruns do not multiply unchanged logical/semantic/derived artifacts.
- **Recoverable:** one failure does not require restarting the entire corpus workflow.
- **Configurable:** vocabulary, models, limits, paths and policies are explicit configuration.
- **Provider-isolated:** source, translation and analysis boundaries remain separate.
- **Conservative:** missing/review-required/uncertain beats unsupported certainty.
- **Testable:** deterministic logic is separated from source/model/provider calls.
- **Regression-driven:** important real failure classes become offline regression fixtures.
- **Resource-aware:** local GPU/RAM/model latency and source-request impact matter.
- **Private by default:** personal data remains local unless explicitly configured otherwise.
- **Bounded:** search breadth, detail fetches, translation, analysis, retries and future automation have explicit ceilings.
- **No duplicate UI truth:** browser convenience state does not become a second analytical database.
- **Modular monolith:** distributed-system complexity requires measured justification.
- **SQLite-first:** replace only after measured limitations.

## 10. Current capability state

### 10.1 Accepted foundation

Live-accepted foundations include the local app, repeat-safe bounded Jobinja discovery, raw evidence preservation, parser-v2/semantic source version foundations, fetch observations/refresh selection, browser operation foundations and historically proven local translation architecture.

Exact current acceptance details are maintained in `IMPLEMENTATION_PLAN.md` and the Phase-1 plan.

### 10.2 Implemented / acceptance pending

Current implementation includes but must not over-claim until the controlling gates pass:

- source-response classification and cautious lifecycle logic;
- translation-v2 and migration/repair path;
- user triage/acquisition priority;
- P1.6 evidence-backed analysis;
- first per-job semantic analysis views;
- first Market aggregation;
- expanded bounded browser workflow actions.

### 10.3 Planned next product layers

After Phase 1 acceptance:

1. canonical market taxonomy/responsibilities/role archetypes;
2. one carefully selected second source and later minimal adapter abstraction;
3. reviewed personal evidence model;
4. gap/readiness/learning/action intelligence;
5. application/interview/outcome workspace;
6. sustained longitudinal operation/trends/backup;
7. advanced evaluated retrieval/assistant/model-lab capabilities only where demonstrated useful.

See `docs/ROADMAP.md`.

## 11. Current non-capabilities / non-claims

Until their respective acceptance gates pass, JobHunter must not claim:

- complete lifecycle/repost/duplicate resolution;
- production-quality translation-v2 across all future source/language cases;
- production-quality semantic extraction across all role types;
- reviewed canonical market taxonomy;
- full-market conclusions from a bounded/source-biased corpus;
- duplicate-adjusted mature market statistics;
- reviewed personal capability state;
- personal gaps/readiness/career recommendations;
- automated learning/project prioritization;
- evidence-backed resume/interview assistance;
- autonomous job applications;
- mature longitudinal trend conclusions;
- arbitrary-web ingestion;
- generic third-party source plugin support;
- evaluated RAG/career assistant as an authority layer.

## 12. Explicit exclusions

The product does not include authenticated-platform scraping, CAPTCHA bypass, stealth proxy rotation, automatic applications/messages, autonomous resume claims, distributed microservices for decoration, cloud LLM analysis by default, self-training on unverified generations, salary/hiring-probability prediction, unrestricted internet crawling, opaque readiness scoring, or a vector/graph database without demonstrated need.

## 13. Success standard

JobHunter succeeds when repeated use changes or strengthens a real career decision while remaining traceable to trustworthy market and personal evidence.

Scraped volume, source count, vocabulary size, translation volume, model count, agent count, chart count, UI polish and apparent AI sophistication are not success metrics by themselves.
