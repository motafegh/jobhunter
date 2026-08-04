# Evidence-Backed Semantic Analysis

## 1. Purpose

P1.6 converts current parsed Jobinja postings into structured model-derived career concepts
without allowing model interpretation to become source truth.

JobHunter keeps **two independent semantic-analysis products** for a job:

1. **English analysis** — analyzes only the current hardened English projection.
2. **Original-language analysis** — analyzes only the original employer/source fields.

They are separate artifacts. Neither mode may use the other mode's text as analysis input or
evidence.

## 2. Two independent analysis contracts

### English analysis

```text
original source
→ hardened English projection v2
→ English-only semantic analysis
→ English evidence
→ English analysis artifact
```

The model receives only the hardened English projection as `analysis_fields`.

The English artifact:

- uses normalized English statements/concepts;
- cites exact contiguous English excerpts from the English projection;
- stores the supporting translation artifact ID;
- is the canonical normalized analysis used by Market, dashboard analysis counts, automated
  analysis-ready queues, Quick Add complete processing, and the full market workflow.

Current identity:

```text
prompt/runtime: job-analysis-english-v2
schema:         job-analysis-v2
```

### Original-language analysis

```text
original source
→ original-language semantic analysis
→ original-language evidence
→ original-language analysis artifact
```

The model receives only original employer/source fields as `analysis_fields`.

The original artifact:

- does not receive the English projection or any English comprehension aid;
- keeps statements/concepts in the language used by the relevant source text;
- cites exact contiguous excerpts from original employer/source fields;
- has no translation-artifact dependency;
- is a per-job review/diagnostic artifact and is not merged into normalized Market aggregates.

Current identity:

```text
prompt/runtime: job-analysis-original-v2
schema:         job-analysis-v2
```

The v2 prompt/runtime identities intentionally distinguish the Instructor/Pydantic extraction
runtime from historical v1 artifacts. Historical artifacts remain preserved but are not reused
as current v2 analyses.

## 3. Why the split exists

The English projection is generally the easier and more consistent representation for semantic
interpretation across a bilingual corpus. The original source remains independently valuable for
reviewing how the model behaves directly on employer-language text.

```text
English interpretation quality   → English analysis
Original-language interpretation → Original analysis
```

A successful English artifact does not imply that original-language analysis succeeded, and a
successful Original artifact does not satisfy the English Market contract.

## 4. Evidence hierarchy

```text
original Jobinja employer fields   source truth
English projection v2             hardened derived representation
English analysis artifact         interpretation of English projection
Original analysis artifact        interpretation of original source
Market aggregate                  accepted English analyses only
```

Within each analysis mode, the selected representation is the only permitted evidence surface:

```text
English analysis  → English projection evidence only
Original analysis → original source evidence only
```

There is no cross-language repair or evidence path.

## 5. Artifact identity and persistence

One analysis artifact is identified by:

```text
source semantic version
+ exact LM Studio model
+ prompt/runtime version
+ analysis schema version
```

Because English and Original use different prompt/runtime identities, both artifacts can coexist
for the same current source version and model without overwriting or reusing each other.

For every accepted artifact JobHunter stores:

- source detail-version identity;
- translation artifact ID for English analysis, or `NULL` for Original analysis;
- exact model ID;
- prompt/runtime version;
- schema version;
- validated analysis JSON;
- accepted inference request metadata;
- raw final LM Studio response;
- creation timestamp.

Operational analysis attempts record:

```text
completed
failed
reused
```

Reuse is mode-specific because prompt/runtime identity is mode-specific.

## 6. Shared analysis schema

Both modes use `job-analysis-v2`.

### Role purpose

Zero or one concise statement with:

- exact evidence from the selected analysis representation;
- confidence.

If no single contiguous excerpt supports a concise purpose claim, the model must return an empty
`role_purpose` array.

### Responsibilities

Up to 16 explicit responsibility claims, each with:

- statement;
- exact evidence from the selected representation;
- confidence.

Responsibilities are work duties/actions. Candidate qualification wording such as ability,
mastery, familiarity, knowledge, or skill belongs under requirements unless explicitly framed
as a duty.

### Requirements

Up to 32 requirement/concept claims, each with:

- concept;
- requirement type;
- concept type;
- exact evidence from the selected representation;
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

## 7. Required versus preferred discipline

Requirement type is about employer obligation/optionality, not technical depth.

Examples:

```text
"familiarity with Docker"
→ familiarity is a depth signal
→ it does NOT by itself mean preferred

"Docker is preferred"
→ preferred

"the team deploys on Kubernetes"
→ may be contextual
→ must not automatically become a candidate requirement
```

Familiarity, proficiency, mastery, expertise, and years of experience describe depth/experience;
they do not independently determine required versus preferred.

## 8. Instructor + Pydantic structured extraction

Analysis no longer uses a hand-built outer repair request.

The live path is:

```text
selected analysis_fields
        ↓
LM Studio OpenAI-compatible chat API
        ↓
Instructor JSON_SCHEMA mode
        ↓
Pydantic JobAnalysisResponse
        ├─ structural/type validation
        ├─ exact evidence validation using runtime context
        ├─ inferred-rationale validation
        ├─ safe scalar evidence canonicalization
        └─ exact duplicate collapse
        ↓
invalid?
        ├─ yes → Instructor supplies validation feedback and performs one bounded re-ask
        └─ no
        ↓
existing JobHunter JSON-Schema guard
        ↓
existing JobHunter independent evidence/domain guard
        ↓
persist or fail closed
```

Instructor is generic retry/structured-output plumbing. JobHunter retains ownership of all domain
rules and final acceptance decisions.

Current runtime dependencies:

```text
Instructor 1.x
OpenAI Python 2.x
Pydantic 2.x
LM Studio OpenAI-compatible local endpoint
```

The selected Instructor mode is `JSON_SCHEMA`, matching LM Studio's native structured-output
surface. Tool calling is not required for this workflow.

## 9. Runtime validation context

Instructor passes the selected `analysis_fields` into Pydantic validation context. Evidence
validators compare every generated evidence value against those exact runtime fields.

This is mode-specific:

```text
English  context → hardened English projection fields
Original context → original employer/source fields
```

A validation error is returned to the same model by Instructor during the bounded re-ask. The
other language representation is never introduced during that retry.

## 10. Safe deterministic normalization

Two failure classes are handled deterministically because no model reasoning is needed.

### Exact duplicate claims

If a model emits the same responsibility or requirement twice with the same normalized identity
and evidence, JobHunter keeps the first and drops the exact duplicate.

This avoids spending a model call to fix a mechanically provable duplicate.

### Invented JSON field prefixes

A model may emit:

```text
minimum_experience: three to six years
```

when the actual English field is:

```text
minimum_experience = "three to six years"
```

JobHunter may canonicalize that evidence to:

```text
three to six years
```

**only** when all of the following are true:

1. the prefix names a real `analysis_fields` key;
2. the suffix exactly matches that field's scalar value, or exactly matches one string item in
   that field's list;
3. no semantic rewriting is required.

Arbitrary prefixes, paraphrases, reconstructed text, translations, or concatenations still fail
validation.

## 11. Independent final guards

Instructor/Pydantic acceptance is necessary but not sufficient.

JobHunter still runs its established local JSON-Schema validation and an independent final
analysis-domain guard before persistence.

The final guard checks:

- evidence occurrence in the selected representation;
- role-purpose/responsibility/requirement bounds;
- requirement type validity;
- inferred rationale presence;
- duplicate claims;
- parser metadata exclusion.

No invalid analysis artifact is persisted.

## 12. Network and local-runtime behavior

LM Studio remains local-first.

The OpenAI client used by Instructor is configured with the existing LM Studio base URL and uses
an HTTPX client with `trust_env=False`, so host proxy environment variables do not intercept
localhost LM Studio requests.

The generic LM Studio provider remains in place for:

- model listing;
- doctor/smoke tests;
- generic structured inference;
- bounded truncation recovery outside the Instructor analysis path.

Injected custom transports remain on the raw provider path so low-level protocol tests stay
deterministic and do not accidentally test Instructor internals.

## 13. Browser workflow

On a job page the controls remain deliberately separate:

```text
Analyze English
Analyze Original
```

### Analyze English

Requires:

```text
current parsed source
+ current hardened English projection v2
```

It creates/reuses only `job-analysis-english-v2`.

### Analyze Original

Requires:

```text
current parsed source
```

It creates/reuses only `job-analysis-original-v2` and does not require translation.

The job page displays the two artifacts separately so English evidence and original-source
evidence are never visually conflated.

Bulk Jobs actions also expose separate English and Original analysis commands.

## 14. Market and automation policy

The normalized corpus pipeline uses **English analysis only**.

That includes:

- `WebRepository` analyzed/missing state;
- dashboard analyzed counts;
- `Analyze English-ready jobs`;
- full workflow analysis stage;
- Quick Add complete processing;
- Market aggregation and warnings;
- source/model/prompt/schema coverage counts.

Original-language analysis remains supplementary review evidence. It must not make an English
analysis appear complete and must not contribute Persian/mixed-language concepts to normalized
Market aggregation without a future explicit design.

## 15. Local model selection and context

Both modes currently use the same configured analysis-model resolution order:

```text
analysis_lm_studio_model
→ lm_studio_model
→ translation_lm_studio_model
```

They may later use separate dedicated models if evidence demonstrates a need.

The LM Studio loaded context window must cover prompt + reasoning + structured output. A
JobHunter `max_tokens` request cannot override a smaller loaded context. The current acceptance
environment uses a 16,384-token loaded context for `gemma-4-e2b-it`.

## 16. Acceptance strategy

P1.6 is not accepted merely because a typed object was returned.

### English acceptance

For a reviewed real posting:

1. inspect hardened English v2;
2. run `Analyze English`;
3. verify every accepted statement/concept against the English projection;
4. verify every evidence excerpt is English and present in the English projection;
5. verify responsibility versus qualification classification;
6. verify required/preferred/contextual/inferred semantics;
7. check for omitted or invented technologies/concepts;
8. rerun and verify exact English v2 analysis reuse;
9. only then expand to a representative English-analysis batch and Market review.

### Original-language acceptance

Separately:

1. inspect original source fields;
2. run `Analyze Original`;
3. verify no English projection was supplied to the model request;
4. verify statements/evidence remain grounded in original source text;
5. verify semantic classification independently;
6. rerun and verify exact Original v2 artifact reuse.

Failure in one mode does not invalidate a correctly accepted artifact in the other mode.

## 17. Known limits

Current P1.6 still does not provide:

- reviewed canonical aliases/taxonomy;
- manual editing of individual semantic claims;
- calibrated model-quality scoring against a reviewed gold corpus;
- deterministic bilingual sentence/span alignment between English and original artifacts;
- repost/duplicate merging before aggregation;
- personal capability comparison;
- readiness scores or career recommendations.

Instructor improves structured-output reliability; it does not make a small model semantically
correct. Semantic quality still requires representative live acceptance and, if needed, a
controlled comparison against a stronger dedicated analysis model.
