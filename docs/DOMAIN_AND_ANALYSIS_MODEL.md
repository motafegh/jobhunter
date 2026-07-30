# JobHunter Domain and Analysis Model

## 1. Purpose

This document defines the concepts JobHunter must represent so that scraping, local LLM extraction, aggregation, and personal career analysis do not collapse into an unreliable collection of keywords.

The model separates:

- source evidence;
- job identity and version history;
- employer-stated responsibilities and requirements;
- inferred supporting capabilities;
- normalized career concepts;
- the user's current capabilities and evidence;
- derived gaps and recommendations.

## 2. Provenance rule

Every material claim must be attributable to one of these provenance classes:

1. **Source-explicit:** directly stated in the job posting.
2. **Source-derived:** deterministically derived from source metadata or structure.
3. **Model-inferred:** inferred by the LLM from one or more explicit passages.
4. **Taxonomy-derived:** produced through an approved concept mapping or relationship.
5. **User-provided:** entered or confirmed by the user.
6. **System-derived:** calculated from stored records using a versioned rule.

The product must not display an inferred or derived claim as though the employer explicitly stated it.

## 3. Acquisition entities

### 3.1 SourceDefinition

Represents an approved source configuration.

Important fields:

- identifier;
- name;
- source type;
- base URL or local input type;
- adapter type;
- enabled state;
- allowed acquisition method;
- rate limit;
- request headers allowed;
- policy review notes and date;
- last successful run;
- last failure;
- configuration version.

### 3.2 AcquisitionRun

Represents one execution of all or part of the acquisition pipeline.

Important fields:

- run identifier;
- start and finish time;
- trigger type: manual or scheduled;
- configuration snapshot;
- source scope;
- counts by outcome;
- terminal status;
- error summary.

### 3.3 AcquisitionAttempt

Represents one attempt to retrieve or import one candidate.

Important fields:

- run identifier;
- source identifier;
- candidate identity;
- requested URL or local input reference;
- retrieval time;
- HTTP status when applicable;
- media type;
- outcome;
- error class;
- retry number;
- raw evidence reference.

### 3.4 EvidenceObject

Represents immutable acquired content.

Important fields:

- SHA-256 content hash;
- media type;
- byte length;
- local relative path;
- encoding when applicable;
- creation time;
- sanitization status;
- parent evidence object when derived;
- derivation method and version.

A cleaned text document is a derived evidence object. It does not replace the original.

## 4. Job identity entities

### 4.1 JobPosting

Represents the logical job opportunity across retrievals and edits.

Important fields:

- internal identifier;
- source-specific posting identifier;
- canonical URL;
- company;
- title;
- role family when accepted;
- first observed time;
- most recent observed time;
- active, expired, removed, or unknown state;
- duplicate/repost relationships;
- latest accepted version.

### 4.2 JobPostingVersion

Represents one materially distinct version of a posting.

Important fields:

- posting identifier;
- version number;
- evidence object;
- content fingerprint;
- publication and closing dates when explicit;
- observed time;
- change classification;
- extraction status;
- accepted extraction identifier.

### 4.3 JobContext

Stores contextual metadata such as:

- company;
- team or department;
- location;
- remote eligibility and permitted region;
- work arrangement;
- employment type;
- seniority;
- compensation;
- language;
- travel;
- on-call duty;
- visa, citizenship, clearance, or legal constraints.

Unknown, unstated, and not applicable must remain distinguishable.

## 5. Extracted work entities

### 5.1 Responsibility

A responsibility represents work the employee is expected to perform.

It should preserve more structure than a sentence or keyword:

- normalized action;
- object of the action;
- operational context;
- intended outcome;
- frequency or scope when stated;
- collaboration target when stated;
- expected ownership level;
- original wording;
- evidence passage;
- explicit or inferred state;
- confidence;
- review status.

Example:

```text
Action: Design
Object: security automation services
Context: production incident-response workflows
Outcome: reduce repetitive analyst work
Ownership: primary contributor
```

### 5.2 Requirement

A requirement represents an employer expectation attached to the role.

Classification:

- required;
- preferred;
- contextual;
- inferred supporting capability.

Requirement types:

- knowledge;
- applied skill;
- tool or technology;
- professional practice;
- domain experience;
- general work experience;
- education;
- certification;
- language;
- legal or location constraint;
- interpersonal or communication capability.

Important fields:

- original wording;
- normalized meaning;
- requirement class;
- concept mappings;
- expected depth signal;
- years or duration when explicit;
- evidence passage;
- inference reason when not explicit;
- confidence;
- review status.

### 5.3 Deliverable

Represents an artifact or outcome the role is expected to produce, such as:

- a detection rule;
- an internal security platform;
- a machine-learning model;
- a production service;
- an incident report;
- a data pipeline;
- an architecture or control design.

Deliverables help distinguish theoretical familiarity from applied expectations.

## 6. Career concept taxonomy

### 6.1 CareerConcept

A canonical concept may represent:

- knowledge area;
- skill;
- tool;
- platform;
- programming language;
- framework;
- protocol;
- practice;
- domain;
- deliverable type;
- credential;
- role archetype.

Important fields:

- canonical name;
- definition;
- concept type;
- aliases;
- parent and child concepts;
- related concepts;
- prerequisite relationships;
- external taxonomy references where useful;
- active or deprecated state;
- creation provenance;
- review status.

### 6.2 ConceptMention

Preserves the exact source wording and its mapping to a canonical concept.

Important fields:

- original text;
- source evidence location;
- mapped concept;
- mapping method;
- mapping confidence;
- user-confirmed state.

### 6.3 Skill versus tool rule

A tool is not treated as the capability itself.

For example:

```text
Tool: Splunk
Possible capabilities:
- query security telemetry;
- create detections;
- investigate events;
- build dashboards;
- operate a SIEM environment.
```

The system should connect tools to responsibilities and applied capabilities rather than count tool names alone.

## 7. Role archetypes

A RoleArchetype represents a recurring pattern of responsibilities and capability expectations independent of inconsistent titles.

Important fields:

- archetype name;
- defining responsibilities;
- core concepts;
- supporting concepts;
- common tools;
- common seniority range;
- distinguishing features from adjacent archetypes;
- supporting postings and date range;
- clustering or manual-definition version;
- confidence;
- review status.

Initial archetypes must emerge from evidence and may include areas such as security automation, detection engineering, security platforms, security data engineering, machine-learning engineering, and AI security. These are hypotheses, not predetermined buckets into which every job must be forced.

## 8. Personal capability entities

### 8.1 PersonalCapability

Represents the user's current capability for a canonical concept or integrated activity.

Important fields:

- career concept;
- current depth;
- assessment confidence;
- recency;
- contexts used;
- independence level;
- repetition count or breadth;
- evidence references;
- limitations and untested areas;
- last reviewed time.

### 8.2 Capability depth scale

The initial depth scale is ordinal and descriptive:

0. **Unassessed:** no reliable conclusion.
1. **Awareness:** recognizes the concept and basic purpose.
2. **Introductory understanding:** can explain a basic mental model.
3. **Guided practice:** has performed relevant work with substantial guidance.
4. **Independent bounded execution:** can complete a defined task with limited help.
5. **Integrated application:** has used the capability as part of a larger system.
6. **Repeated independent evidence:** has demonstrated it across more than one meaningful context.
7. **Production or production-like operation:** has handled realistic reliability, maintenance, security, or operational constraints.

This scale does not imply equal distance between levels. A capability may also have different depth in different contexts.

### 8.3 CapabilityEvidence

Evidence types may include:

- repository source code;
- automated tests;
- working deployment;
- project documentation;
- architecture explanation;
- assessment result;
- troubleshooting record;
- repeated exercise;
- professional experience;
- self-report.

Evidence fields:

- type;
- reference or local path;
- date;
- capability demonstrated;
- context;
- degree of AI assistance when relevant;
- independence level;
- evaluator;
- strength;
- limitations;
- verification status.

AI-assisted implementation remains valid evidence, but the system must not automatically treat generated code as evidence of independent execution or full conceptual mastery.

## 9. Gap model

A GapAssessment connects a market expectation with personal capability evidence.

Gap classes:

- **knowledge gap:** the concept is not sufficiently understood;
- **practice gap:** understanding exists but applied repetition is weak;
- **depth gap:** evidence exists below the level indicated by relevant jobs;
- **integration gap:** component skills exist but have not been combined;
- **evidence gap:** capability may exist but lacks credible demonstration;
- **recency gap:** evidence is stale for a fast-changing area;
- **presentation gap:** evidence exists but is not communicated clearly;
- **experience-context gap:** capability exists in a materially different environment;
- **constraint mismatch:** location, language, clearance, degree, or another non-skill constraint blocks fit.

Important fields:

- market concept or responsibility;
- target role scope;
- supporting posting set;
- expected depth;
- personal depth;
- gap class;
- severity;
- confidence;
- prerequisite dependencies;
- estimated effort range;
- review state.

## 10. Recommendation model

A Recommendation is an explainable proposed action.

Action classes:

- learn;
- practise;
- build;
- improve an existing project;
- document;
- assess;
- monitor;
- ignore for now;
- investigate further;
- prepare application evidence.

Important fields:

- action class;
- target capability or responsibility;
- reason;
- market evidence;
- personal evidence;
- assumptions;
- expected benefit;
- estimated effort;
- prerequisite leverage;
- target-role relevance;
- urgency;
- confidence;
- conditions that would change the recommendation;
- accepted, rejected, deferred, or completed state.

Recommendations are advisory. They must not silently rewrite the user's roadmap or claim certainty about employability.

## 11. Skill and responsibility matrix

A useful aggregate matrix should support at least these dimensions:

- canonical concept;
- concept type;
- original aliases;
- posting count;
- percentage of filtered postings;
- required count and percentage;
- preferred count and percentage;
- responsibility-linked count;
- role archetype distribution;
- seniority distribution;
- location and region distribution;
- industry distribution;
- co-occurring concepts;
- expected-depth signals;
- first and most recent observation;
- trend over an explicit time window;
- personal depth;
- evidence strength;
- gap class and severity;
- learning or project prerequisites;
- recommendation state.

All matrix calculations must retain their corpus filter, date window, and calculation version.

## 12. Confidence and review

Confidence should be field-specific rather than one score for an entire posting.

Suggested states:

- high confidence;
- medium confidence;
- low confidence;
- unresolved;
- rejected.

Automatic acceptance rules must be conservative. High confidence does not override missing evidence.

Manual corrections should record:

- previous value;
- corrected value;
- correction reason;
- user and timestamp;
- whether the correction should become a future mapping rule.

## 13. Analytical safeguards

- Do not treat every mention as equal demand.
- Do not equate years requested with actual depth automatically.
- Do not count duplicate postings as independent market evidence.
- Do not infer a trend from a small or changing source corpus without warning.
- Do not compare jobs across regions without showing the region filter.
- Do not rank personal priorities solely by keyword frequency.
- Do not treat absence from a posting as evidence that a skill is unnecessary.
- Do not convert a model inference into an employer-stated requirement.
- Do not present a numerical readiness percentage without transparent meaning and components.

## 14. Versioning

The following must be versioned because changes can alter historical results:

- extraction schema;
- extraction prompt;
- model identifier and relevant parameters;
- cleaning logic;
- deduplication rules;
- taxonomy mappings;
- role-archetype definitions or clustering method;
- gap rules;
- priority formula;
- report calculation logic.

Old source evidence and extraction results remain available when a new version is introduced.
