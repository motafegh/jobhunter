# Evidence-Backed Semantic Analysis

**Status:** Implemented; semantic-quality acceptance active  
**Date:** 2026-08-08

P1.6 is JobHunter's strict factual semantic layer. It extracts job-level facts from one selected language representation while keeping evidence/provenance mechanically enforceable.

The active quality sequence is controlled by `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`.

---

## 1. Purpose

P1.6 converts a current parsed Jobinja posting into structured model-derived facts without allowing model interpretation to become source truth.

JobHunter keeps two independent products:

1. **English analysis** — reads only the current hardened English projection.
2. **Original-language analysis** — reads only original employer/source fields.

They are independent artifacts. Neither analysis uses the other language representation as hidden evidence or repair context.

---

## 2. Current contracts

### English

```text
source
→ english-projection-v2
→ job-analysis-english-v4
→ job-analysis-v2 persisted schema
```

### Original

```text
original source fields
→ job-analysis-original-v4
→ job-analysis-v2 persisted schema
```

Current constants are defined in `src/jobhunter/analysis_service.py`.

Historical prompt/runtime identities remain historical. Prompt/runtime changes intentionally make prior artifacts non-current even when the persisted schema shape remains `job-analysis-v2`.

---

## 3. Current v4 change set

V4 keeps the factual persisted shape while making dense/long postings more robust.

Implemented v4 behavior includes:

- deterministic evidence-reference catalogs supplied to the model;
- heading-aware long-description segmentation;
- clause-level references for semicolon-delimited mixed-strength lines;
- the model selects evidence IDs instead of copying quotations in production;
- JobHunter resolves selected references back to exact source text before persistence;
- rich-source `0 responsibilities / 0 requirements` responses are rejected when the source plainly contains substantial duties/qualifications;
- mixed core/optional clauses must be emitted atomically rather than as one strength claim;
- `preferred` requires actual preference/advantage/plus/helpful-style source wording;
- global wording such as `we don't expect every single item` prevents automatic mandatory treatment but does not automatically make every stack item preferred;
- explicit depth words such as expert/proficient/familiar remain distinct from obligation strength;
- long local Instructor reads do not use an arbitrary read-time deadline after successful connection;
- transport replay remains disabled and Instructor validation retry remains bounded.

---

## 4. Evidence hierarchy

```text
original Jobinja employer/source fields    authoritative source truth
English projection v2                      hardened derived representation
English P1.6 artifact                      interpretation of English projection
Original P1.6 artifact                     interpretation of original source
Capability Intelligence                    derived reasoning above accepted English P1.6
Role Capability Blueprint                  human-facing interpretation above those layers
Market aggregate                           deterministic aggregate of accepted English P1.6
```

Within one P1.6 mode, the selected representation is the only evidence surface:

```text
English analysis  → English projection evidence only
Original analysis → original source evidence only
```

No cross-language repair is allowed.

---

## 5. Artifact identity and persistence

An accepted analysis artifact records:

- source detail-version identity;
- translation artifact ID for English analysis, `NULL` for Original;
- exact model ID;
- prompt/runtime version;
- schema version;
- validated structured analysis;
- accepted inference request metadata;
- raw final local-model response;
- creation timestamp.

Attempts record:

```text
completed
failed
reused
```

Current analysis-store identity is keyed by source version + model + prompt + schema. The English artifact also stores its exact translation dependency. A future persistence migration may include translation artifact ID directly in uniqueness semantics, but that is explicit technical debt and must not be hidden inside semantic-quality tuning.

---

## 6. Shared persisted schema

Both modes use `job-analysis-v2`.

### Role purpose

Zero or one concise supported purpose statement:

```text
statement
evidence
confidence
```

If no concise supported purpose exists, `role_purpose` may be empty.

### Responsibilities

Up to the configured schema bound, each with:

```text
statement
evidence
confidence
```

Responsibilities are employee work duties/actions.

Candidate qualification wording such as skill, ability, mastery, familiarity, knowledge, education, or experience belongs under requirements unless explicitly framed as work.

### Requirements

Each contains:

```text
concept
requirement_type
concept_type
evidence
confidence
rationale
```

Current requirement types:

```text
required
preferred
contextual
inferred
```

Current concept types:

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

The current four-way requirement-strength enum is under quality review because dense postings can contain globally mixed/unspecified stack optionality that may not be truthfully representable as either `required` or `preferred`. Do not change the enum until reviewed examples establish that a contract extension is necessary.

---

## 7. Obligation strength is not technical depth

These are different dimensions.

Examples:

```text
Python (expert)
→ explicit depth: expert
→ obligation determined separately

MATLAB a plus
→ preference/optionality signal
→ not automatically a depth claim

some C/C++ helpful
→ optional/helpful

familiarity with Docker
→ familiarity is depth
→ does not by itself mean preferred

we don't expect every item
→ individual listed stack obligation may be contextual/uncertain
→ does not mean every item preferred
```

A depth adjective attached to one technology must not spread to neighboring technologies.

`tG9K` demonstrated why this matters: `Python (expert)` does not prove expert-level scikit-learn, PyTorch, TensorFlow, XGBoost, or LightGBM.

---

## 8. Evidence references

Production P1.6 receives a deterministic reference catalog.

Examples:

```text
field:title
field:skills:0
field:description:segment:3
field:description:segment:12:clause:1
```

The model emits one known reference ID in each evidence field. JobHunter resolves that ID to exact selected-representation text before the artifact is persisted.

Reference IDs are generation-time bookkeeping. Persisted evidence remains source text.

Historical low-level tests/callers may still use exact text directly.

---

## 9. Long-description segmentation

Dense descriptions often contain inline headings and bullet lists.

Current evidence-reference construction recognizes heading boundaries and creates narrower bullet/segment references. Semicolon-delimited mixed clauses may also receive clause references.

Goal:

```text
large description
→ specific supported span
→ atomic factual claim
```

not:

```text
large description
→ whole paragraph as evidence
→ accidental heading leakage / mixed optionality
```

Segmentation is deterministic evidence addressing. It does not itself decide semantic meaning.

---

## 10. Rich-source empty-analysis guard

A structurally valid response such as:

```json
{
  "role_purpose": [],
  "responsibilities": [],
  "requirements": []
}
```

is not automatically acceptable.

If deterministic source signals show that the posting contains substantial job-description/skills content, a completely empty extraction is invalid and Instructor receives its one bounded correction attempt.

A genuinely sparse posting may still legitimately return little or nothing.

This protects against the historical `tG9K` failure where a very rich semiconductor posting was persisted as `0/0`.

---

## 11. Atomic optionality guard

A mixed-strength source line such as:

```text
Programming: Python (expert) and SQL; MATLAB a plus; some C/C++ helpful
```

must not become one monolithic required claim.

V4 supplies clause references and validation/prompt rules that require separate coherent strength claims.

Likewise, an English `preferred` claim must cite evidence that itself contains preference/advantage/plus/helpful-style wording or equivalent employer language.

These are general semantic contracts, not technology-specific rules.

---

## 12. Instructor + Pydantic flow

Current live path:

```text
selected analysis_fields
+ deterministic evidence references
        ↓
LM Studio OpenAI-compatible API
        ↓
Instructor JSON_SCHEMA mode
        ↓
Pydantic JobAnalysisResponse
        ├─ shape/type validation
        ├─ evidence-reference resolution
        ├─ exact source-span validation
        ├─ inferred-rationale validation
        ├─ optionality/atomicity rules
        ├─ rich-source non-empty guard
        └─ exact duplicate normalization
        ↓
invalid?
  ├─ yes → one bounded Instructor correction attempt
  └─ no
        ↓
independent JobHunter JSON/domain guards
        ↓
persist or fail closed
```

Instructor is structured-output/retry plumbing. JobHunter owns domain truth/validation rules.

---

## 13. Safe deterministic normalization

Permitted mechanical repair includes:

- exact duplicate collapse;
- exact field-value/source-span recovery;
- mechanically equivalent whitespace/ZWNJ/case normalization where the exact source span is provable;
- known evidence-reference resolution.

Do not repair through:

- paraphrase;
- translation;
- semantic reconstruction;
- invented field prefixes;
- invented list indexes;
- concatenation that cannot be independently proved.

---

## 14. Network/runtime policy

The analysis client remains local-first and uses `trust_env=False` so host proxy variables do not intercept localhost LM Studio traffic.

Current long-generation policy:

```text
connect timeout: bounded
read timeout: none after connection
write/pool timeout: bounded
transport retries: 0
Instructor validation retry: bounded separately
max output tokens: bounded
```

This prevents legitimate local reasoning from being terminated by an arbitrary read deadline while preserving other operational bounds.

---

## 15. Model selection

Effective analysis model:

```text
analysis_lm_studio_model
→ lm_studio_model
→ translation_lm_studio_model
```

Capability and Blueprint have independent model roles and may use stronger models without changing P1.6.

Do not assume the best expert-reasoning model must also be the best factual extractor.

---

## 16. Browser and CLI behavior

Browser actions remain separate:

```text
Analyze English
Analyze Original
```

English requires current parsed source + current English projection.

Original requires only current parsed source.

English and Original artifacts do not satisfy or reuse each other.

The normalized Market path continues to use English P1.6 only.

---

## 17. Live acceptance state

P1.6 mechanics/grounding are substantially stronger than the earlier v2/v3 path, but semantic acceptance is still open.

### `t4jp`

Sparse AI/content posting. Useful for testing conservative extraction/inference when the employer provides little technical detail.

### `tG9K`

Rich semiconductor/industrial-ML posting. V4 fixed the historical empty extraction and now captures responsibilities well, but the first reviewed snapshot still exposed requirement-coverage and obligation/depth issues.

Observed remaining issues include:

- some explicit requirement families omitted on a dense posting;
- broad stack items overclassified as required despite global optionality wording;
- explicit `Python (expert)` depth overgeneralized downstream to broader ML-framework expertise;
- some structured experience/education signals not represented in the reviewed factual output.

These are the next P1.6 quality targets.

---

## 18. Acceptance strategy

Do not scale P1.6 merely because an artifact validates structurally.

For each reviewed job:

1. inspect source and English projection;
2. inspect role purpose;
3. inspect every responsibility;
4. inspect every requirement;
5. verify evidence is exact selected-representation text;
6. verify responsibility versus qualification classification;
7. verify obligation strength;
8. verify explicit depth is preserved without spreading;
9. look for omitted explicit source requirements;
10. rerun unchanged identity and verify reuse;
11. record repeatable failure classes as regression fixtures.

Representative acceptance must vary role family, company, language mix, description length, requirement density, and optionality wording.

---

## 19. Known limits

P1.6 still does not provide:

- reviewed canonical aliases/taxonomy;
- personal capability comparison;
- readiness/career recommendations;
- calibrated model-quality scoring against a broad gold corpus;
- complete bilingual span alignment;
- repost/duplicate normalization before aggregation;
- guaranteed complete requirement recall across every dense posting.

The current acceptance work specifically targets factual coverage and obligation/depth preservation before broader Phase-2 promotion.
