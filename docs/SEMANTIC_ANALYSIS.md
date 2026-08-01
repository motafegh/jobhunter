# Evidence-Backed Semantic Analysis

## 1. Purpose

P1.6 converts current parsed Jobinja postings into structured model-derived career concepts
without allowing model interpretation to become source truth.

The analysis layer answers questions such as:

- What is the role trying to accomplish?
- Which responsibilities are explicit?
- Which qualifications/tools/knowledge areas are required versus preferred?
- Which concepts are contextual rather than candidate requirements?
- Which concepts are inferred, and why?

It must not invent unsupported employer intent.

## 2. Evidence hierarchy

```text
original Jobinja employer fields     authoritative evidence
English projection v2               comprehension aid
semantic analysis artifact          model interpretation
market aggregate                    deterministic aggregation of accepted analysis
```

A translated sentence is never the sole authority for a material analysis claim.

## 3. Artifact identity

One analysis artifact is identified by:

```text
source semantic version
+ exact LM Studio model
+ prompt version
+ analysis schema version
```

Current versions:

```text
prompt: job-analysis-prompt-v1
schema: job-analysis-v1
```

A source semantic change invalidates the old analysis as current. A future material prompt
or schema change creates a new analytical artifact rather than rewriting history.

## 4. Stored provider evidence

For every accepted analysis JobHunter stores:

- source detail-version identity;
- supporting English translation artifact ID;
- exact model ID;
- prompt version;
- schema version;
- validated analysis JSON;
- full structured inference request body;
- raw LM Studio response body;
- creation timestamp.

Operational analysis attempts record:

```text
completed
failed
reused
```

## 5. Current analysis schema

### Role purpose

Zero or one concise normalized English statement with:

- original source evidence excerpt;
- confidence.

### Responsibilities

Up to 16 explicit responsibility claims, each with:

- normalized English statement;
- original source evidence excerpt;
- confidence.

### Requirements

Up to 32 requirement/concept claims, each with:

- normalized concept;
- requirement type;
- concept type;
- original source evidence excerpt;
- confidence;
- rationale when inferred.

Requirement types:

```text
required
preferred
contextual
inferred
```

Concept types:

```text
tool
skill
knowledge
practice
domain
experience
education
other
```

## 6. Required versus preferred discipline

The model is explicitly instructed not to strengthen employer language.

Examples:

```text
"familiarity with Docker"
→ must not become "Docker proficiency required"

"Docker is preferred"
→ preferred
→ not required

"the team deploys on Kubernetes"
→ may be contextual
→ must not automatically become a candidate requirement
```

If JobHunter cannot support the strength classification from evidence, the claim should be
omitted rather than guessed.

## 7. Evidence validator

JSON-schema validity alone is insufficient.

After the model returns structured output, JobHunter validates every role-purpose,
responsibility, and requirement evidence excerpt against the original parsed source fields.

Whitespace and Persian zero-width spacing are normalized for matching, but the model must
still copy an actual employer/source excerpt rather than paraphrasing evidence.

If a material claim cites text that does not exist in authoritative source fields:

```text
model output
→ analysis validation failure
→ failed attempt retained
→ no analysis artifact
```

This catches a major hallucination class before aggregation.

## 8. English projection requirement

P1.6 currently requires a current hardened `english-projection-v2` artifact before analysis.

This ensures the local model receives an English comprehension aid that has passed current
translation-integrity rules.

The English artifact does not replace the original evidence requirement.

## 9. Local model selection

Configuration may specify:

```toml
analysis_lm_studio_model = "exact-model-id"
analysis_max_tokens = 8192
analysis_batch_limit = 5
```

Model fallback order is:

```text
analysis_lm_studio_model
→ lm_studio_model
→ translation_lm_studio_model
```

This allows starting with the already configured local model while preserving the option to
use a stronger dedicated analysis model later.

## 10. Browser workflow

On a job page:

```text
Source complete
→ English v2 ready
→ Analyze job
→ inspect every claim + evidence
```

Overview also provides a bounded `Analyze ready jobs` action. The default batch remains
small because model-derived quality must be reviewed before scaling.

The Jobs table exposes analysis-ready/missing state and permits bounded bulk analysis.

## 11. Market aggregation

The Market screen uses only current persisted analysis artifacts.

It currently reports:

- analyzed sample size;
- responsibility-claim count;
- requirement-claim count;
- concept demand by number of postings;
- required/preferred/contextual/inferred posting counts.

This is intentionally not a canonical taxonomy yet. Case/whitespace normalization is
minimal. Alias consolidation and reviewed taxonomy belong to Phase 2.

## 12. Acceptance strategy

P1.6 is not live-accepted merely because structured JSON succeeds.

First live acceptance should use one reviewed real posting:

1. inspect source and English v2;
2. run one analysis;
3. read every responsibility;
4. read every requirement type;
5. verify every evidence excerpt against source;
6. check that requirement strength is not inflated;
7. check that unsupported technologies/concepts are absent;
8. only then analyze a small batch of about five jobs;
9. inspect the resulting Market view.

## 13. Known limits

Current P1.6 does not yet provide:

- reviewed canonical aliases/taxonomy;
- manual editing of individual semantic claims;
- model quality scoring across a reviewed gold analysis corpus;
- repost/duplicate merging before aggregation;
- personal capability comparison;
- readiness scores or career recommendations.

These are deliberate later layers rather than hidden assumptions inside P1.6.
