# JobHunter Product Specification

**Status:** Current product definition  
**Product type:** Local-first personal career-intelligence application  
**Primary user:** Repository owner

## 1. Purpose

JobHunter exists to convert selected job-market data into reliable, actionable personal career intelligence.

The product must help answer questions such as:

- Which real role families best match the career direction I am pursuing?
- What responsibilities do those roles actually perform?
- Which skills, knowledge areas, tools, practices, and experience patterns recur across relevant jobs?
- What depth of capability appears to be expected?
- Which requirements are mandatory, preferred, or merely inferred from the work?
- Which gaps in my profile are knowledge gaps, practice gaps, integration gaps, evidence gaps, or presentation gaps?
- What should I learn, practise, build, improve, document, assess, monitor, or deliberately ignore?
- How is the target market changing over time?

## 2. Product character

JobHunter is a real personal utility intended for repeated local use. It is not governed as a learning roadmap, and its architecture must not be expanded merely to create learning opportunities.

Learning is an acceptable by-product of development. Daily usefulness, data integrity, explainability, and maintainability control product decisions.

## 3. Daily operating scenario

A normal run should eventually perform this sequence:

1. Load enabled source definitions.
2. acquire new and changed job postings conservatively;
3. preserve the retrieved source material and acquisition metadata;
4. identify duplicates, reposts, and changed versions;
5. clean the source without destroying relevant evidence;
6. send the content to the configured local model through LM Studio;
7. validate the model output against an explicit schema;
8. store extracted responsibilities, requirements, concepts, confidence, and evidence;
9. update aggregate role and skill analyses;
10. compare the current market model with the user's capability evidence;
11. generate an inspectable daily report;
12. surface uncertain items for manual correction.

A failed source or failed model extraction must not invalidate the rest of the run.

## 4. Inputs

### 4.1 Initial inputs

- pasted job-description text;
- a user-provided permitted public job URL;
- a saved HTML, JSON, text, or PDF document;
- local configuration for LM Studio and storage.

### 4.2 Later inputs

- approved company career pages;
- public Applicant Tracking System endpoints or feeds;
- source lists grouped by role, region, company, or priority;
- the user's capability profile and evidence references;
- manual corrections and review decisions.

## 5. Core outputs

### 5.1 Per-posting analysis

Each analyzed posting should provide:

- source identity and retrieval metadata;
- title, company, location, arrangement, employment type, and seniority when available;
- concise role purpose;
- structured responsibilities;
- required qualifications;
- preferred qualifications;
- tools and technologies;
- knowledge areas;
- professional practices;
- domain experience;
- education, certifications, language, clearance, travel, and on-call constraints;
- compensation when explicitly stated;
- explicit versus inferred classification;
- extraction confidence;
- exact supporting evidence from the source;
- review status.

### 5.2 Aggregate analysis

The system should eventually provide:

- canonical skill and knowledge matrix;
- responsibility clusters;
- role archetypes independent of inconsistent job titles;
- skill co-occurrence patterns;
- demand by role, seniority, location, industry, source, and time period;
- required-versus-preferred distributions;
- expected-depth signals;
- duplicate and repost patterns;
- market trends with date-bounded evidence.

### 5.3 Personal analysis

The system should eventually provide:

- capability-to-market comparison;
- knowledge, practice, depth, integration, evidence, and presentation gaps;
- project and repository evidence mapping;
- priority recommendations with visible reasoning;
- individual-job readiness analysis;
- claims that are safe to make and claims that are not currently supported;
- actions classified as learn, practise, build, improve, document, assess, monitor, or ignore for now.

## 6. Functional requirements

### FR-1: Source registry

The application must maintain explicit source definitions including source type, enabled state, acquisition method, request limits, and policy notes.

### FR-2: Reproducible acquisition

Every acquisition attempt must record its timestamp, result, errors, and source configuration. Retrieved material must be hashed and stored before LLM processing.

### FR-3: Version and duplicate handling

The application must distinguish:

- the same posting retrieved again unchanged;
- an updated version of a known posting;
- a repost of substantially equivalent content;
- a genuinely new posting.

### FR-4: Evidence-preserving extraction

Every extracted fact must retain supporting source text or a precise source location. Unsupported model output must not silently become accepted data.

### FR-5: Structured local inference

LLM responses must be validated against versioned schemas. Invalid output must be retried within a bounded policy or moved to review without corrupting stored data.

### FR-6: Requirement classification

The system must distinguish required, preferred, contextual, and inferred concepts. Inferred concepts must include a reason and confidence.

### FR-7: Canonicalization

Aliases such as `AWS`, `Amazon Web Services`, and related wording must be connectable to a canonical concept without losing the original wording.

### FR-8: Human review

The user must be able to approve, reject, edit, merge, or remap uncertain extraction and taxonomy decisions.

### FR-9: Personal capability evidence

A personal capability must include depth, recency, evidence type, evidence references, and confidence. A simple binary known/unknown field is insufficient.

### FR-10: Explainable recommendations

A recommendation must show the market evidence, personal evidence, assumptions, weighting, uncertainty, and the conditions under which it would change.

### FR-11: Run reporting

Every run must summarize new, updated, unchanged, failed, analyzed, and review-required items.

### FR-12: Export and backup

The user must be able to export important normalized data and back up or restore the local database and raw evidence store.

## 7. Non-functional requirements

- **Local-first:** no cloud dependency is required for normal operation.
- **Inspectable:** source, intermediate data, model request, model response, and final record remain traceable.
- **Idempotent:** repeated runs do not multiply unchanged data.
- **Recoverable:** interruption does not require restarting the entire pipeline.
- **Configurable:** model, source, limits, storage paths, and analysis thresholds are configuration rather than scattered constants.
- **Provider-isolated:** LM Studio integration is behind an inference interface.
- **Conservative:** the product prefers missing or review-required data over fabricated certainty.
- **Testable:** deterministic logic is separated from network and model calls.
- **Resource-aware:** the application accounts for local model latency, context limits, and finite GPU/RAM availability.
- **Private by default:** personal evidence and local analysis are not transmitted externally unless the user explicitly configures such behavior.

## 8. Initial release boundary

The first usable release is complete when the user can:

1. configure and verify an LM Studio connection;
2. submit pasted job text or one permitted URL;
3. preserve the raw source and metadata;
4. extract a schema-valid analysis locally;
5. inspect evidence for every important field;
6. persist the posting and analysis;
7. rerun the same input without creating a duplicate;
8. see clear failures and retry them;
9. approve or correct the extraction.

## 9. Explicit initial exclusions

The initial product will not include:

- LinkedIn or authenticated-platform scraping;
- CAPTCHA or access-control bypass;
- automatic job applications;
- automatic messages to recruiters;
- autonomous resume claims;
- a mobile application;
- distributed microservices;
- cloud-hosted inference;
- model fine-tuning;
- hiring-probability prediction;
- salary prediction;
- real-time internet-wide crawling;
- a vector database unless later evidence shows it is necessary;
- project generation for every detected gap.

## 10. Success standard

JobHunter succeeds when repeated use produces information that changes or strengthens a real decision while remaining traceable to trustworthy source evidence.

Volume of scraped pages, number of technologies used, number of dashboards, and apparent AI sophistication are not success metrics by themselves.
