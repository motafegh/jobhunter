# JobHunter Product Specification

**Status:** Current product definition  
**Product type:** Local-first personal career-intelligence application  
**Primary user:** Repository owner

## 1. Purpose

JobHunter converts selected job-market data into reliable, actionable personal career
intelligence.

The complete product should eventually answer:

- Which real role families match the intended career direction?
- What responsibilities do those roles perform?
- Which skills, knowledge areas, tools, practices, and experience patterns recur?
- What depth appears expected?
- Which requirements are mandatory, preferred, contextual, or inferred?
- Which personal gaps are knowledge, practice, depth, integration, evidence, or
  presentation gaps?
- What actions should be learned, practised, built, improved, documented, assessed,
  monitored, or ignored for now?
- How does the target market change over time?

## 2. Product character

JobHunter is a **real repeated-use local utility**, not a learning-roadmap artifact.

Daily usefulness, data integrity, explainability, privacy, configurability,
maintainability, and conservative evidence handling control product decisions.

The normal human interaction surface is the local browser application. The CLI remains a
supported technical interface for automation, debugging, tests, and advanced workflows.
Both interfaces operate on the same services and durable records.

## 3. Normal operating experience

The current browser experience can already:

1. show current corpus/detail/translation coverage;
2. inspect the configured bilingual search catalog and generated plan;
3. start a guided bounded Jobinja sync from a form with visible safety limits/presets;
4. browse/filter local jobs using human-readable source states;
5. accept a focused Quick Add input as a Jobinja job URL, Jobinja search URL, or one
   Persian/English keyword phrase;
6. inspect original and English representations side by side;
7. inspect source evidence identity and check history;
8. refresh one job;
9. translate one job or a bounded missing queue;
10. run the deterministic parser audit;
11. export the current English JSONL corpus;
12. inspect long-running browser-operation status.

A future complete Phase 1 run will add:

1. lifecycle-aware selection;
2. local evidence-backed semantic analysis;
3. structured validation/review states;
4. individual analysis views;
5. combined role/requirement reporting.

One failed search, posting, parser, translation, UI operation, or model call must not
invalidate successful durable work from the rest of the run.

## 4. Current inputs

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

Later inputs include pasted/local job documents, additional approved sources, personal
capability evidence, and manual review/correction decisions.

## 5. Current outputs

### Acquisition outputs

- inspectable effective search plan;
- bounded request/detail selection;
- immutable search/detail evidence;
- logical JobPosting identities;
- discovery provenance for search-based acquisition;
- semantic posting versions;
- successful/failed fetch observations;
- parser audit findings;
- concise acquisition summaries.

### Derived English corpus

- one English projection tied to one exact current source semantic version;
- structured English fields;
- one complete English document;
- native-versus-translated segment provenance;
- provider/model/schema/prompt-contract identity;
- completed/failed/reused translation attempts;
- current-version-only JSONL export.

The English corpus is derived convenience data and never replaces original employer text.

### Browser outputs

- dashboard metrics;
- guided sync controls and deterministic presets;
- Quick Add intake for approved Jobinja inputs;
- filtered job catalog;
- source/English job detail views;
- source-check timeline;
- search-catalog/profile/pack views;
- live browser-operation state/output;
- local system/configuration visibility.

## 6. Functional requirements

### FR-1: Source registry and acquisition policy

Sources must have explicit type/method/limits/policy. JobHunter must not silently expand
from approved public acquisition into unrestricted crawling.

Quick Add is an alternate operator input, not a policy bypass. Until another source has a
dedicated approved adapter, Quick Add must reject non-Jobinja URLs.

### FR-2: Reproducible evidence

Record acquisition attempts and preserve retrieved bytes/metadata before model processing.
Directly supplied Jobinja job URLs must enter the same logical job/detail evidence model as
search-discovered jobs.

### FR-3: Data-driven bilingual search planning

Search vocabulary must be versioned data rather than Python word constants. Persian and
English terms, normalized identity/deduplication, raw URL escape hatches, plan inspection,
search windows, and global request bounds must remain supported.

One-off browser phrases and Jobinja search URLs may create focused searches without
mutating the saved search catalog. These searches must still use the normal request/page
bounds and evidence persistence.

### FR-4: Identity/version/check separation

Distinguish logical posting identity, raw HTTP observation, semantic employer-content
version, and operational source check. Stable Jobinja codes remain technical identity but
must be labelled as such in human-facing UI rather than presented as meaningful role data.

### FR-5: Evidence-preserving deterministic extraction

Explicit Jobinja facts must be parsed deterministically. Missing source fields remain
missing. Unsupported model output cannot become accepted source fact.

### FR-6: Derived English projection

For accepted source semantic versions, JobHunter must be able to build an English view that:

- preserves source evidence unchanged;
- passes native-English segments through without translation calls;
- translates Persian-containing semantic units through an isolated provider;
- retains native/translated provenance;
- records provider/model/schema identity;
- is idempotent;
- becomes stale when a newer semantic source version exists;
- never silently falls back to an older translation when the newest parse is incomplete;
- exports independently from source evidence.

### FR-7: Local translation-provider isolation

LM Studio is the normal translator and must support explicit/dedicated model selection,
fail-closed ambiguous selection, structured JSON output, exact ID/count validation,
bounded requests, bounded retries, and bounded output-truncation recovery.

Google Cloud Translation remains an optional external provider and must never be required
for normal operation.

### FR-8: Browser application

The browser application must:

- operate on the same services/database as the CLI;
- provide normal daily controls without requiring CLI knowledge;
- explain non-obvious run limits in the UI rather than exposing configuration names alone;
- provide bounded presets without hiding the concrete values they set;
- support focused Quick Add intake for a Jobinja job URL, Jobinja search URL, or one search
  phrase;
- distinguish friendly role/company information from technical Jobinja references;
- show discovered-but-unfetched jobs as actionable normal states rather than CLI errors;
- keep source and translated representations visually distinct;
- expose inspectable errors/summaries for long operations;
- run at most one mutable browser operation at a time;
- remain local/loopback-first;
- protect mutating forms from cross-site request forgery;
- ship its own static assets rather than depending on remote CDNs;
- never bypass acquisition/translation bounds.

### FR-9: Structured local semantic inference

Future P1.6 model responses must use versioned prompts/schemas, retain raw request/response
evidence, validate structured output, and move invalid/uncertain results to explicit review.

### FR-10: Requirement classification

Future analysis must distinguish required, preferred, contextual, and inferred concepts.
Inferred concepts require reason and confidence.

### FR-11: Canonicalization

Career-concept aliases may map to canonical concepts without losing original wording.
Search normalization, translation, and career taxonomy canonicalization remain different
operations.

### FR-12: Human review

Future uncertain extraction/taxonomy decisions must be reviewable/editable rather than
silently accepted.

### FR-13: Personal capability evidence

Future personal capabilities must include depth, recency, evidence type/reference, and
confidence. Binary known/unknown is insufficient.

### FR-14: Explainable recommendations

Future recommendations must expose market evidence, personal evidence, assumptions,
uncertainty, and conditions that would change the recommendation.

### FR-15: Export/backup/recovery

Normalized data and English corpus must be exportable. Database/raw evidence must remain
back-up/restorable in later operational hardening.

## 7. Non-functional requirements

- **Local-first:** normal acquisition/translation require no cloud service.
- **Browser-local by default:** UI binds loopback unless exposure is explicit.
- **Inspectable:** original evidence, semantic records, translated records, and operation
  outcomes remain traceable.
- **Idempotent:** reruns do not multiply unchanged logical/semantic/derived artifacts.
- **Recoverable:** one failure does not require restarting the entire corpus workflow.
- **Configurable:** vocabulary, models, limits, paths, and thresholds are explicit config.
- **Provider-isolated:** source, translation, and future analysis boundaries remain separate.
- **Conservative:** missing/review-required beats unsupported certainty.
- **Testable:** deterministic logic is separated from source/model/provider calls.
- **Resource-aware:** local GPU/RAM/model latency and source-request impact matter.
- **Private by default:** personal data and local analysis remain local unless explicitly
  configured otherwise.
- **Bounded:** broad vocabulary, Quick Add, and model translation cannot trigger
  unrestricted work.
- **No duplicate UI state:** browser convenience state must not become a second durable
  database.

## 8. Current accepted capability boundary

Before the current guided-UI/Quick-Add increment, live acceptance established that
JobHunter can:

1. load and inspect bilingual search configuration;
2. discover jobs repeat-safely;
3. preserve raw search/detail evidence;
4. fetch missing/refresh-due details;
5. distinguish raw responses, semantic versions, and fetch observations;
6. parse explicit Jobinja fields deterministically;
7. audit parser structure;
8. create local LM Studio English projections;
9. recover boundedly from a real long-output translation truncation;
10. retain 15/15 current English artifacts;
11. export a 15-record current English corpus;
12. launch and browse the local web application successfully against the real local corpus.

The guided sync explanations/presets, human-readable source-reference presentation, and
Quick Add intake are implemented on top of that accepted foundation and require their own
local acceptance after the deterministic test suite passes.

## 9. Current non-capabilities

JobHunter must not yet claim completion of:

- challenge/login/CAPTCHA/error/expired-page classification;
- complete posting lifecycle/repost/duplicate resolution;
- responsibility extraction;
- required/preferred semantic classification;
- canonical description-derived skills;
- aggregate market intelligence;
- personal relevance/readiness/gap analysis;
- career recommendations;
- final Phase 1 combined analysis/report run.

Quick Add is also not an arbitrary-web ingestion engine. Additional websites require
explicit source adapters/policy before they become accepted inputs.

## 10. Explicit exclusions

The product does not include authenticated-platform scraping, CAPTCHA bypass, stealth proxy
rotation, automatic applications/messages, autonomous resume claims, distributed
microservices, cloud LLM analysis by default, model fine-tuning, salary/hiring-probability
prediction, unrestricted internet crawling, or a vector database without demonstrated
need.

## 11. Success standard

JobHunter succeeds when repeated use changes or strengthens a real decision while remaining
traceable to trustworthy evidence.

Scraped volume, vocabulary size, translation volume, UI polish, technology count, and
apparent AI sophistication are not success metrics by themselves.
