# JobHunter Domain and Analysis Model

## 1. Purpose

This document defines the concepts JobHunter must represent so acquisition,
translation, local LLM extraction, aggregation, and personal career analysis do
not collapse into an unreliable collection of keywords.

The model separates:

- source evidence;
- job identity and semantic version history;
- derived English translation artifacts;
- employer-stated responsibilities and requirements;
- model-inferred supporting capabilities;
- normalized career concepts;
- personal capabilities and evidence;
- derived gaps and recommendations.

## 2. Provenance rule

Every material claim must be attributable to one or more explicit provenance
classes:

1. **Source-explicit:** directly stated in original employer text.
2. **Source-derived:** deterministically derived from source structure/metadata.
3. **Translation-derived:** machine-translated representation of source text.
4. **Model-inferred:** inferred by an LLM from source evidence.
5. **Taxonomy-derived:** produced by an approved concept mapping.
6. **User-provided:** entered or confirmed by the user.
7. **System-derived:** calculated from stored records using a versioned rule.

Translation-derived text is not source-explicit evidence. A translated passage
must retain a link to the exact source semantic version and original source text.

The product must never display an inferred, translated, or derived claim as though
the employer wrote that wording in English.

## 3. Acquisition entities

### 3.1 SourceDefinition

Represents an approved source configuration with identity, adapter type, enabled
state, public/private boundary, acquisition method, bounds, policy notes, and
configuration version.

### 3.2 AcquisitionRun

Represents one execution of all or part of source acquisition with timestamps,
configuration/search scope, counts, terminal status, and error summary.

### 3.3 AcquisitionAttempt / fetch observation

Represents one retrieval/check operation with source identity, requested URL,
time, status/outcome, error, and raw-evidence reference where available.

### 3.4 EvidenceObject

Represents immutable acquired content with content hash, media type, byte length,
local path, creation time, and derivation metadata where applicable.

A cleaned or translated document never replaces the original evidence object.

## 4. Job identity entities

### 4.1 JobPosting

Represents one logical source job across retrievals and edits.

Important fields include source ID, canonical URL, company/title observations,
first/last seen, lifecycle state, duplicate/repost relationships, and latest
semantic version.

### 4.2 JobPostingVersion

Represents one materially distinct deterministic source version.

Important fields:

- posting identifier;
- source evidence reference;
- semantic content fingerprint;
- publication/validity dates when explicit;
- observed time;
- parser and language metadata;
- deterministic source fields.

Translation provider/model changes do not create JobPostingVersion records.

### 4.3 JobContext

Stores source-explicit contextual metadata such as company, location, arrangement,
employment type, seniority, compensation, language, travel, on-call, and legal
constraints. Unknown, unstated, and not applicable remain distinct.

## 5. Translation and language entities

### 5.1 JobTranslationArtifact

Represents one derived target-language projection of one exact source semantic
version.

Important fields:

- source `JobPostingVersion` reference;
- source semantic SHA-256;
- source and target language;
- translation provider;
- provider model;
- translation schema version;
- structured translated/projected fields;
- complete target-language document;
- segment provenance;
- translated/native segment counts;
- artifact SHA-256;
- creation timestamp.

Artifact identity includes source version, target language, provider, model, and
translation schema. An older artifact remains historical but is not current once a
newer source semantic version exists.

### 5.2 JobTranslationAttempt

Represents an operational translation operation:

```text
completed
failed
reused
```

It retains source version, provider/model/schema, timestamp, resulting artifact
when available, and error information when failed.

### 5.3 Segment provenance

Each text-bearing path in an English artifact is classified at minimum as:

```text
native
translated
```

This allows later ML/analytics to separate native-English content from translated
content and control translation-induced bias.

### 5.4 Translation evidence rule

A translation is a convenience representation. Material analytical claims must
remain traceable to original source text.

Example:

```text
Original: آشنایی با Docker
Translation: Familiarity with Docker
```

If another translator renders the same phrase as `Proficiency with Docker`, that
translation difference must not silently strengthen the employer requirement.

## 6. Extracted work entities

### 6.1 Responsibility

A responsibility represents work the employee is expected to perform.

It should retain normalized action/object/context/outcome, ownership indicators,
original wording, evidence passage, explicit/inferred state, confidence, and
review status.

### 6.2 Requirement

A requirement represents an employer expectation classified as required,
preferred, contextual, or inferred supporting capability.

Requirement types include knowledge, applied skill, tool, practice, domain/general
experience, education, certification, language, legal/location constraints, and
interpersonal capabilities.

Important fields include original wording, normalized meaning, classification,
concept mapping, depth signals, duration, source evidence, inference reason,
confidence, and review state.

Original wording means the source-language employer wording. An English
translation may be attached separately for convenience.

### 6.3 Deliverable

Represents an expected artifact/outcome such as a detection rule, security
platform, ML model, service, incident report, data pipeline, or architecture.

## 7. Career concept taxonomy

### 7.1 CareerConcept

Represents canonical knowledge, skill, tool, platform, language, framework,
protocol, practice, domain, deliverable, credential, or role-archetype concepts.

### 7.2 ConceptMention

Preserves exact source wording and its mapping to a canonical concept. A translated
alias may assist retrieval but does not replace the original mention.

### 7.3 Skill versus tool rule

A tool name is not the capability itself. Tool mentions must connect to applied
responsibilities/capabilities when evidence supports that connection.

## 8. Role archetypes

A RoleArchetype represents a recurring pattern of responsibilities and capability
expectations independent of inconsistent titles. Archetypes emerge from evidence;
they are not predefined buckets that every job must fit.

## 9. Personal capability entities

### 9.1 PersonalCapability

Represents current capability for a concept or integrated activity with depth,
confidence, recency, context, independence, evidence, limitations, and review time.

### 9.2 Capability depth scale

0. **Unassessed**  
1. **Awareness**  
2. **Introductory understanding**  
3. **Guided practice**  
4. **Independent bounded execution**  
5. **Integrated application**  
6. **Repeated independent evidence**  
7. **Production or production-like operation**

The scale is ordinal and context-dependent.

### 9.3 CapabilityEvidence

Evidence may include source code, tests, working deployment, documentation,
architecture explanation, assessment, troubleshooting, repeated exercise,
professional experience, and self-report.

AI-assisted implementation is valid evidence of project work but is not automatic
evidence of independent execution or full conceptual mastery.

## 10. Gap model

Gap classes include:

- knowledge;
- practice;
- depth;
- integration;
- evidence;
- recency;
- presentation;
- experience-context;
- constraint mismatch.

Every GapAssessment retains supporting market postings and personal evidence.

## 11. Recommendation model

Actions include learn, practise, build, improve, document, assess, monitor, ignore
for now, investigate, and prepare application evidence.

Recommendations remain advisory and explainable.

## 12. Skill and responsibility matrix

Aggregate matrices should support concept, original aliases, posting counts,
required/preferred distributions, responsibility-linked counts, role/seniority/
location/industry dimensions, co-occurrence, depth signals, time windows,
personal evidence, gaps, and recommendation state.

Language/translation dimensions must also be available:

- original source language;
- native-English versus translated-English origin;
- translation provider/model/schema;
- inclusion/exclusion of translated segments.

Duplicate and unchanged postings must not inflate counts.

## 13. Confidence and review

Confidence is field-specific. Suggested states are high, medium, low, unresolved,
and rejected.

Manual corrections retain previous value, corrected value, reason, timestamp, and
whether the correction should become a future deterministic mapping.

Translation quality review is separate from source parser review and semantic LLM
analysis review.

## 14. Analytical safeguards

- Do not treat every mention as equal demand.
- Do not equate requested years with actual depth automatically.
- Do not count duplicate postings as independent evidence.
- Do not infer trends from small/changing corpora without warnings.
- Do not rank personal priorities solely by keyword frequency.
- Do not treat absence from a posting as proof that a capability is unnecessary.
- Do not convert a model inference into an employer-explicit requirement.
- Do not convert stronger/weaker translation wording into employer intent.
- Do not merge translated and native-English corpus observations without retaining
  provenance.
- Do not present a readiness percentage without transparent meaning/components.

## 15. Versioning

Version because changes can alter historical results:

- source parser schema/version;
- normalization logic;
- semantic fingerprint logic;
- translation provider/model/schema;
- translation prompt or glossary if introduced later;
- analysis schema/prompt/model/parameters;
- deduplication rules;
- taxonomy mappings;
- role-archetype definitions/clustering method;
- gap rules;
- priority formula;
- report calculations.

Old source evidence, source versions, translation artifacts, and analysis results
remain available when a new derived version is introduced.
