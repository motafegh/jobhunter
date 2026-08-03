# Evidence-Backed Semantic Analysis

## 1. Purpose

P1.6 converts current parsed Jobinja postings into structured model-derived career concepts
without allowing model interpretation to become source truth.

JobHunter now keeps **two independent semantic-analysis products** for a job:

1. **English analysis** — analyzes only the current hardened English projection.
2. **Original-language analysis** — analyzes only the original employer/source fields.

They are intentionally separate artifacts. Neither mode may use the other mode's text as
analysis input or evidence.

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
prompt: job-analysis-english-v1
schema: job-analysis-v2
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
prompt: job-analysis-original-v1
schema: job-analysis-v2
```

## 3. Why the split exists

The English projection is generally the easier and more consistent representation for semantic
interpretation across a bilingual corpus. The original source remains independently valuable for
reviewing how the model behaves directly on employer-language text.

The two jobs should therefore not be conflated:

```text
English interpretation quality     → English analysis
Original-language interpretation   → Original analysis
```

A successful English artifact does not imply that original-language analysis succeeded, and a
successful original artifact does not satisfy the English Market contract.

## 4. Evidence hierarchy

```text
original Jobinja employer fields     source truth
English projection v2               hardened derived representation
English analysis artifact           interpretation of English projection
Original analysis artifact          interpretation of original source
Market aggregate                    aggregation of accepted English analyses only
```

Within each analysis mode, the selected representation is the only permitted evidence surface:

```text
English analysis  → English projection evidence only
Original analysis → original source evidence only
```

There is no mixed evidence-repair path.

## 5. Artifact identity and persistence

One analysis artifact is identified by:

```text
source semantic version
+ exact LM Studio model
+ prompt version
+ analysis schema version
```

Because English and Original use different prompt identities, both artifacts can coexist for the
same current source version and model without overwriting or reusing each other.

For every accepted artifact JobHunter stores:

- source detail-version identity;
- translation artifact ID for English analysis, or `NULL` for Original analysis;
- exact model ID;
- prompt version;
- schema version;
- validated analysis JSON;
- full structured inference request body for the accepted response;
- raw LM Studio response body for the accepted response;
- creation timestamp.

Operational analysis attempts record:

```text
completed
failed
reused
```

Reuse is mode-specific because prompt identity is mode-specific.

## 6. Shared analysis schema

Both modes currently use `job-analysis-v2`.

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

The model is explicitly instructed that familiarity, proficiency, mastery, expertise, and years
of experience describe depth/experience and do not independently determine required/preferred.

## 8. Structured output and deterministic validation

Provider-side JSON-schema support is not sufficient by itself.

For either analysis mode:

```text
selected analysis fields
→ LM Studio structured response
→ local JSON Schema validation
→ local evidence/domain validation against the SAME selected fields
        ↓ passes
        persist mode-specific artifact

        ↓ evidence/domain validation fails
record failed operational attempt
→ one bounded mode-specific repair request
→ same selected analysis fields only
→ rejected semantic object with evidence strings removed
→ same JSON Schema validation
→ same evidence/domain validation
        ↓ passes
        persist repaired artifact
        ↓ fails
        record failed repair attempt
        persist no artifact
```

The repair pass never receives the other language representation.

For English repair:

```text
analysis_fields = English projection only
```

For Original repair:

```text
analysis_fields = original employer/source fields only
```

`rejected_analysis_without_evidence` may preserve statements, concepts, classifications, and
confidence as non-authoritative guidance, but all prior evidence strings are removed before the
repair request.

## 9. Evidence validation

Every role-purpose, responsibility, and requirement evidence excerpt must occur in one selected
analysis-field string.

Whitespace and Persian zero-width spacing are normalized for matching, but evidence must still
represent one contiguous excerpt. The validator rejects unsupported evidence, parser metadata,
duplicate claims, invalid requirement types, inferred requirements without rationale, and
bounded-claim violations.

The validator proves evidence existence in the selected representation. It does not prove every
semantic interpretation is correct.

## 10. Browser workflow

On a job page, the controls are deliberately separate:

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

It creates/reuses only `job-analysis-english-v1`.

### Analyze Original

Requires:

```text
current parsed source
```

It creates/reuses only `job-analysis-original-v1` and does not require translation.

The job page displays the two resulting artifacts separately so English evidence and original
source evidence are never visually conflated.

Bulk Jobs actions also expose separate English and Original analysis commands.

## 11. Market and automation policy

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
analysis appear complete and must not contribute Persian/mixed-language concepts to the
normalized Market taxonomy before an explicit future design says otherwise.

## 12. Local model selection and context

Both modes currently use the same configured analysis-model resolution order:

```text
analysis_lm_studio_model
→ lm_studio_model
→ translation_lm_studio_model
```

They may later use separate dedicated models if evidence demonstrates a need, but no implicit
model split is assumed today.

For the current Gemma acceptance environment, LM Studio must be loaded with enough context for
prompt + reasoning + structured output. A JobHunter `max_tokens` request cannot override a
smaller LM Studio loaded context window.

## 13. Acceptance strategy

P1.6 is not accepted merely because either mode returns structured JSON.

### English acceptance

For a reviewed real posting:

1. inspect hardened English v2;
2. run `Analyze English`;
3. verify every accepted statement/concept against the English projection;
4. verify every evidence excerpt is English and present in the English projection;
5. verify responsibility versus qualification classification;
6. verify required/preferred/contextual/inferred semantics;
7. check for omitted or invented technologies/concepts;
8. rerun and verify exact English artifact reuse;
9. only then expand to a representative English-analysis batch and Market review.

### Original-language acceptance

Separately:

1. inspect original source fields;
2. run `Analyze Original`;
3. verify no English projection was supplied to the model request;
4. verify statements/evidence remain grounded in original source text;
5. verify semantic classification independently;
6. rerun and verify exact Original artifact reuse.

Failure in one mode does not invalidate a correctly accepted artifact in the other mode.

## 14. Known limits

Current P1.6 still does not provide:

- reviewed canonical aliases/taxonomy;
- manual editing of individual semantic claims;
- calibrated model-quality scoring against a reviewed gold corpus;
- deterministic bilingual sentence/span alignment between English and original artifacts;
- repost/duplicate merging before aggregation;
- personal capability comparison;
- readiness scores or career recommendations.

The English/Original split intentionally removes cross-language coupling from the current
acceptance problem. Future bilingual alignment can be introduced as its own explicit capability
rather than hidden inside semantic-analysis prompting.
