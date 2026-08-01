# JobHunter Product Specification

**Status:** Current product definition  
**Product type:** Local-first personal career-intelligence application  
**Primary user:** Repository owner

## 1. Purpose

JobHunter converts selected job-market data into reliable, actionable personal
career intelligence.

It must help answer:

- Which real role families match the intended career direction?
- What responsibilities do those roles perform?
- Which skills, knowledge areas, tools, practices, and experience patterns recur?
- What depth of capability appears expected?
- Which requirements are mandatory, preferred, contextual, or inferred?
- Which personal gaps are knowledge, practice, integration, evidence, or
  presentation gaps?
- What should be learned, practised, built, improved, documented, assessed,
  monitored, or ignored for now?
- How does the target market change over time?

## 2. Product character

JobHunter is a real personal utility for repeated local use. It is not governed
as a learning roadmap, and its architecture must not expand merely to create
learning opportunities.

Daily usefulness, data integrity, explainability, privacy, configurability, and
maintainability control product decisions.

## 3. Daily operating scenario

A complete normal run should eventually:

1. load the effective bilingual search catalog, profiles, custom groups, and raw URLs;
2. build an inspectable bounded search plan;
3. acquire new and changed postings conservatively;
4. preserve source material and acquisition metadata;
5. identify logical jobs, semantic versions, duplicates, reposts, and failures;
6. parse Jobinja's explicit source fields deterministically;
7. optionally create a separate English projection for accepted source versions;
8. send accepted new or changed content to the configured local analysis model;
9. validate model output against explicit versioned schemas;
10. store responsibilities, requirements, concepts, confidence, and evidence;
11. update aggregate role and skill analyses;
12. compare market evidence with personal capability evidence;
13. generate an inspectable report;
14. surface uncertain items for manual review.

One failed search, posting, parser, translation, or model call must not invalidate
successful work from the rest of the run.

## 4. Inputs

### 4.1 Current inputs

- packaged or user-supplied bilingual search catalog TOML;
- built-in/configured search profiles and packs;
- user-defined Persian and English keyword groups;
- permitted public Jobinja result URLs;
- one-off command-line terms or URLs;
- public Jobinja job pages discovered by the application;
- local TOML configuration;
- optional Google Cloud Translation credentials;
- local LM Studio configuration.

### 4.2 Later inputs

- pasted job-description text;
- saved HTML, JSON, text, or PDF documents;
- approved company career pages;
- public Applicant Tracking System endpoints or feeds;
- source lists grouped by role, region, company, or priority;
- personal capability profiles and evidence;
- manual corrections and review decisions.

## 5. Core outputs

### 5.1 Acquisition outputs

- effective search plan;
- request and detail-selection bounds;
- search-page and detail-page evidence;
- logical JobPosting identities;
- discovery provenance;
- semantic posting versions;
- successful and failed fetch observations;
- parser audit results;
- concise acquisition summaries.

### 5.2 Derived English corpus outputs

When enabled, JobHunter must provide:

- one English projection tied to one exact source semantic version;
- structured English fields;
- one complete English document;
- native-versus-translated segment provenance;
- translation provider, model, schema version, and timestamps;
- completed, failed, and reused translation attempts;
- JSONL export containing only current-source-version artifacts.

The English corpus is a derived convenience layer. It must never replace original
Persian, English, or mixed employer text.

### 5.3 Per-posting analysis

Each analyzed posting should provide:

- source identity and retrieval metadata;
- title, company, location, arrangement, employment type, and seniority;
- concise role purpose;
- structured responsibilities;
- required and preferred qualifications;
- tools and technologies;
- knowledge areas and practices;
- domain experience;
- education, certification, language, clearance, travel, and on-call constraints;
- explicit compensation when stated;
- explicit versus inferred classification;
- confidence;
- exact supporting evidence;
- review status.

### 5.4 Aggregate analysis

The system should eventually provide:

- canonical skill and knowledge matrices;
- responsibility clusters;
- role archetypes independent of inconsistent titles;
- co-occurrence patterns;
- demand by role, seniority, location, industry, source, search, and time;
- required-versus-preferred distributions;
- expected-depth signals;
- duplicate and repost patterns;
- date-bounded market trends.

### 5.5 Personal analysis

The system should eventually provide:

- capability-to-market comparison;
- knowledge, practice, depth, integration, evidence, and presentation gaps;
- project and repository evidence mapping;
- priority recommendations with visible reasoning;
- job-level readiness analysis;
- safe and unsupported claim distinctions;
- actions classified as learn, practise, build, improve, document, assess,
  monitor, or ignore for now.

## 6. Functional requirements

### FR-1: Source registry

Maintain explicit source definitions with source type, enabled state,
acquisition method, limits, and policy notes.

### FR-2: Reproducible acquisition

Record every acquisition attempt with timestamp, outcome, errors, and source
configuration. Hash and store retrieved material before model processing.

### FR-3: Search planning and coverage

The application must:

- load search vocabulary from versioned data rather than Python word constants;
- support a complete user-supplied replacement search catalog;
- support Persian and English terms;
- retain original display terms;
- normalize terms only for identity, deduplication, and exclusions;
- generate inspectable canonical Jobinja keyword URLs;
- retain raw URL support for source-owned filters;
- expose the effective plan before network use;
- enforce search, page, request, and detail bounds;
- support deterministic windows across a large catalog;
- report controlled budget exhaustion without treating it as failure.

### FR-4: Version and duplicate handling

Distinguish:

- the same posting retrieved unchanged;
- an updated version of a known posting;
- a repost of substantially equivalent content;
- a genuinely new posting;
- one raw response from one semantic version;
- one operational check from both semantic content and raw evidence.

### FR-5: Evidence-preserving extraction

Every extracted fact must retain supporting source text or a precise location.
Unsupported model output must not silently become accepted data.

### FR-6: Derived English projection

For every accepted source semantic version, JobHunter must be able to create a
separate English projection that:

- leaves source evidence unchanged;
- passes native-English segments through without an external translation request;
- translates Persian-containing segments through an isolated provider;
- records segment-level `native` versus `translated` provenance;
- records provider/model/schema identity;
- is idempotent for the same source/provider/model/schema combination;
- becomes stale when a newer source semantic version exists;
- can be exported independently from the source corpus.

### FR-7: Translation-provider isolation

The translation provider must be replaceable without changing parsing or source
version logic.

The current external provider is Google Cloud Translation Basic v2. Google
translation must remain disabled by default because it transmits parsed source
text outside the local machine.

### FR-8: Structured local inference

Validate model responses against versioned schemas. Invalid output must be
retried within a bounded policy or moved to review without corrupting data.

### FR-9: Requirement classification

Distinguish required, preferred, contextual, and inferred concepts. Inferred
concepts require a reason and confidence.

### FR-10: Canonicalization

Aliases such as `AWS` and `Amazon Web Services` must connect to a canonical
concept without losing original wording.

Search-term normalization, translation, and career-concept canonicalization are
three different operations and must remain separate.

### FR-11: Human review

The user must be able to approve, reject, edit, merge, or remap uncertain
extraction and taxonomy decisions.

### FR-12: Personal capability evidence

A capability must include depth, recency, evidence type, evidence references,
and confidence. Binary known/unknown is insufficient.

### FR-13: Explainable recommendations

A recommendation must show market evidence, personal evidence, assumptions,
weighting, uncertainty, and conditions that would change it.

### FR-14: Run reporting

Every run must summarize new, updated, unchanged, failed, analyzed, and
review-required items. Acquisition and translation summaries must remain useful
before semantic analysis exists.

### FR-15: Export, backup, and restore

Important normalized data must be exportable, and the local database and raw
evidence store must be back up and restorable. The derived English corpus must be
exportable as a versioned machine-readable dataset.

## 7. Non-functional requirements

- **Local-first by default:** normal acquisition and analysis require no cloud
  dependency.
- **Explicit external boundary:** enabling Google translation is a deliberate
  exception and must be visible in configuration and operation.
- **Inspectable:** source, intermediate data, translation metadata, model request,
  response, and final records remain traceable.
- **Idempotent:** reruns do not multiply unchanged logical, semantic, or derived
  artifacts.
- **Recoverable:** interruption does not require restarting the whole pipeline.
- **Configurable:** models, source vocabulary, limits, paths, and thresholds are
  configuration rather than scattered constants.
- **Provider-isolated:** LM Studio and translation providers remain behind separate
  interfaces.
- **Conservative:** missing or review-required data is preferred to certainty
  without evidence.
- **Testable:** deterministic logic is separated from network and model calls.
- **Resource-aware:** the application accounts for local model latency,
  context limits, GPU/RAM, external translation use, and source request impact.
- **Private by default:** personal evidence and analysis remain local unless the
  user explicitly configures otherwise.
- **Bounded:** broad vocabulary cannot trigger unrestricted acquisition, and
  translation batches remain bounded.

## 8. Current usable boundary

The current application can:

1. load a packaged or user-replaced bilingual search catalog;
2. inspect and window the effective plan;
3. discover jobs repeat-safely;
4. preserve immutable search and detail evidence;
5. fetch missing and refresh-due details;
6. distinguish raw responses, semantic versions, and fetch observations;
7. parse explicit Jobinja fields deterministically;
8. audit structural parser quality;
9. rerun without false logical or semantic duplicates;
10. expose failures and check history;
11. optionally create versioned English projections through Google Cloud;
12. distinguish native-English from translated segments;
13. export a current English JSONL corpus for downstream analysis/ML.

## 9. Phase 1 completion boundary

Phase 1 is not complete until the user can also:

1. analyze new or changed posting versions locally;
2. inspect evidence for every important claim;
3. retry or review invalid analysis safely;
4. inspect individual job reports;
5. inspect a combined report without duplicate inflation;
6. run the complete workflow through one normal command.

## 10. Explicit exclusions

The product does not include:

- LinkedIn or authenticated-platform scraping;
- CAPTCHA or access-control bypass;
- proxy rotation or stealth crawling;
- automatic job applications or recruiter messages;
- autonomous resume claims;
- distributed microservices;
- cloud LLM analysis by default;
- model fine-tuning;
- hiring-probability or salary prediction;
- internet-wide real-time crawling;
- a vector database without demonstrated need;
- automatic project generation for every gap.

## 11. Success standard

JobHunter succeeds when repeated use produces information that changes or
strengthens a real decision while remaining traceable to trustworthy source
evidence.

Scraped volume, vocabulary size, translation volume, technology count,
dashboards, and apparent AI sophistication are not success metrics by themselves.
