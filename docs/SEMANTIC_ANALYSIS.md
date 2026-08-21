# Evidence-Backed Semantic Analysis

**Status:** English P1.6 v20/v5 promoted/current; heterogeneous non-regression closed
**Date:** 2026-08-21

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
current parsed source
→ english-projection-v2
→ job-analysis-english-v20
→ job-analysis-v5 persisted schema
```

### Original

```text
original source fields
→ job-analysis-original-v9
→ job-analysis-v4 persisted schema
```

Current public routing is defined through `src/jobhunter/analysis_current.py`. Historical implementations remain versioned for reproducibility.

Prompt/runtime or schema changes intentionally create distinct current/historical artifacts. Deterministic implementation hardening inside the promoted v20 semantic contract does not require a new prompt/schema identity unless the public contract itself materially changes.

---

## 3. Current English v20 / schema-v5 behavior

V20 is a source-led, partition-scoped factual extraction path built from lessons learned through the earlier v9→v19 iterations.

Current behavior includes:

- deterministic evidence-reference catalogs supplied to the model;
- heading-aware long-description segmentation;
- clause-level references for mixed/compound source wording where useful;
- deterministic requirement and responsibility coverage plans;
- bounded requirement/responsibility partitions so correction of one subset cannot silently replace another valid subset;
- model evidence-reference selection followed by deterministic resolution back to exact English-projection text before persistence;
- rich-source non-empty protection;
- deterministic structured source-skill survival;
- mixed core/optional clauses kept atomic rather than merged into one strength claim;
- `preferred` requires actual employer preference/plus/helpful/advantage wording;
- requirement strength remains separate from technical depth;
- exact source depth/experience-extent is scoped to the exact concept;
- concepts remain standalone depth-neutral noun phrases;
- qualification wording cannot silently become employee duties;
- prior-experience classification requires explicit applied-exposure evidence;
- exact deterministic reconciliation of partition outputs and coverage;
- long local Instructor reads use no arbitrary read deadline after successful connection;
- transport replay remains disabled and validation retry remains bounded.

Heterogeneous review has additionally hardened v20 around several real software-posting shapes:

- `Sufficient knowledge` is accepted as explicit employer depth while plain `knowledge` remains non-depth;
- one dense evidence segment may contain several different depth levels, and each requirement preserves its own exact level rather than inheriting the first marker;
- if multi-level evidence lacks item-specific depth, validation fails closed rather than guessing;
- `Ability to effectively use AI ...` is treated as application/manner rather than technical depth when the evidence contains no genuine depth marker;
- a coverage reference positively represented by an extracted requirement cannot simultaneously remain as a redundant exclusion for that same reference.

These are general deterministic protections derived from live evidence, not vacancy-specific prompt patches.

---

## 4. Evidence hierarchy

```text
original Jobinja employer/source fields    authoritative source truth
English projection v2                      hardened derived representation
English P1.6 artifact                      strict factual interpretation of English projection
Original P1.6 artifact                     strict factual interpretation of original source
Capability Intelligence v9                 bounded reasoning above accepted English P1.6
Role Capability Blueprint v6               experimental/non-authoritative historical-chain interpretation
Market aggregate                           deterministic aggregate of accepted/current English P1.6
```

Within one P1.6 mode, the selected representation is the only evidence surface:

```text
English analysis  → English projection evidence only
Original analysis → original source evidence only
```

No cross-language repair is allowed.

The original employer source remains ultimate authority at the product level; therefore a material translation error discovered during review blocks English P1.6 acceptance rather than being silently repaired by giving English P1.6 hidden original-language evidence.

---

## 5. Artifact identity and persistence

An English analysis artifact records:

- source detail-version identity;
- exact English translation/projection artifact dependency;
- exact model ID;
- prompt/runtime version;
- schema version;
- validated structured analysis;
- accepted inference request metadata;
- raw final local-model response in local runtime history;
- creation timestamp.

Original-language analysis records no translation dependency.

Attempts record operational outcomes such as:

```text
completed
failed
reused
```

Current analysis identity is versioned by source/model/prompt/schema and records the exact English translation dependency for English artifacts. Historical identities remain preserved rather than overwritten.

A mechanically completed artifact is still a semantic-review candidate when the active acceptance gate requires manual review. A rejected candidate must not feed Capability.

---

## 6. Persisted English schema v5

English v20 persists `job-analysis-v5`.

### Role purpose

Zero or one concise supported purpose statement:

```text
statement
evidence
confidence
```

If no concise supported purpose exists, `role_purpose` may be empty.

### Responsibilities

Each responsibility contains:

```text
statement
evidence
confidence
```

Responsibilities are employee work duties/actions.

Candidate qualification wording such as skill, ability, mastery, familiarity, knowledge, education, experience or behavioral expectations belongs under requirements unless the source actually frames it as employee work.

### Requirements

Each requirement persists:

```text
concept
depth_signal
requirement_type
concept_type
evidence
confidence
rationale
```

`depth_signal` is nullable and, when present, represents exact source-supported depth/extent scoped to that concept.

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

### Coverage

The accepted artifact retains reviewable deterministic coverage of source requirement/responsibility inputs after generation-time references are resolved.

Coverage is bookkeeping about source treatment; it does not itself certify semantic quality.

---

## 7. Obligation strength is not technical depth

These are independent dimensions.

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
→ vague `some` is not technical depth

familiarity with Docker
→ familiarity is depth
→ does not by itself mean preferred

sufficient knowledge of OOP
→ sufficient knowledge is explicit source depth
→ plain knowledge without a degree qualifier is not

ability to effectively use AI
→ application/manner requirement
→ not automatically technical depth
```

A depth adjective attached to one technology must never spread to neighboring technologies.

`tG9K` established that `Python (expert)` does not prove expert-level scikit-learn/PyTorch/TensorFlow/etc. `tmBK` then established the adjacent multi-level case: `Mastery`, `Familiarity`, and `Sufficient knowledge` can coexist in one source segment and must remain subject-specific.

---

## 8. Evidence references and source-led partitions

Production English P1.6 receives deterministic evidence references and bounded coverage plans.

Examples:

```text
field:title
field:skills:0
field:description:segment:3
field:description:segment:12:clause:1
```

V20 partitions source-led requirement/responsibility work into bounded subsets while keeping the full evidence catalog available for grounding. This prevents a correction for one dense subset from replacing another already-correct subset.

The model selects known evidence references. JobHunter resolves them to exact selected-representation text before final persistence.

Generation-time reference IDs are bookkeeping. Persisted evidence remains reviewable source-representation text.

---

## 9. Long-description segmentation

Dense descriptions often contain inline headings, bullet lists and mixed-strength compound clauses.

Current evidence-reference construction recognizes heading boundaries and creates narrower bullet/segment references. Compound clauses may receive narrower references where deterministic splitting is useful.

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
→ accidental heading leakage / mixed optionality / depth leakage
```

Segmentation is deterministic evidence addressing. It does not decide semantic meaning by itself.

---

## 10. Rich-source and coverage guards

A structurally valid empty response is not automatically acceptable on a rich posting.

Likewise, a model may not satisfy a source-coverage requirement merely by producing plausible JSON. JobHunter independently reconciles the source-led plan and validates the resulting requirement/responsibility coverage.

A genuinely sparse posting may still legitimately produce little output.

This is why the accepted opposite-end anchors matter:

```text
tG9K — dense
33 requirements / 8 responsibilities / 0 role purpose

t4jp — sparse
8 requirements / 0 responsibilities / 0 role purpose
```

---

## 11. Optionality, depth and concept-scope guards

Mixed-strength source clauses must not become one monolithic required claim.

Preferred claims require explicit source preference semantics.

Depth rules remain concept-specific. The validator may perform deterministic normalization only when scope and meaning are mechanically provable. If a dense evidence segment contains several distinct depth levels and no item-specific signal is available, fail closed instead of borrowing another subject's depth.

Similarly, non-depth wording such as a deployment scope, vague preference extent, schedule wording, or effective-application phrase must not become technical depth merely because a model places it in `depth_signal`.

---

## 12. Instructor + Pydantic flow

Current English live path:

```text
selected English analysis_fields
+ deterministic evidence catalog
+ bounded source-led coverage partition
        ↓
LM Studio OpenAI-compatible API
        ↓
Instructor JSON_SCHEMA mode
        ↓
Pydantic v20 response models
        ├─ shape/type validation
        ├─ evidence-reference resolution context
        ├─ optionality/depth/concept rules
        ├─ qualification-vs-duty rules
        ├─ coverage rules
        └─ bounded validation feedback
        ↓
partition result
        ↓
deterministic JobHunter reconciliation
        ↓
final domain/evidence guards
        ↓
persist or fail closed
```

Instructor is structured-output/retry plumbing. JobHunter owns domain truth, source bookkeeping and deterministic reconciliation.

---

## 13. Safe deterministic normalization

Permitted deterministic repair/normalization includes only transformations whose semantic equivalence can be proved from the selected source representation and contract, for example:

- exact duplicate collapse;
- exact evidence-reference resolution;
- harmless mechanically provable whitespace/ZWNJ/case handling;
- source-led structured-skill preservation;
- narrowly proven non-depth signal normalization;
- removal of a redundant coverage exclusion when the same reference is already positively represented.

Do not repair through:

- paraphrase presented as source text;
- cross-language repair;
- invented field prefixes or list indexes;
- semantic reconstruction that cannot be independently proved;
- borrowing another concept's depth marker;
- converting a qualification into a duty.

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

Effective analysis model is selected through the typed configuration/runtime builder. Capability and Blueprint have independent model roles.

Do not assume the strongest reasoning model must also be the best factual extractor.

Controlled model comparison changes only the model when model adequacy is the variable; it does not simultaneously change source, evidence, prompt/schema and model.

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

The current Market path continues to aggregate accepted/current English P1.6 only.

Capability v9 requires the accepted/current English P1.6 dependency selected by the public service path.

---

## 17. Current live acceptance state

Public English P1.6 v20/v5 is promoted/current and has accepted dense+sparse opposite-end anchors:

```text
tG9K → artifact 36 → accepted/current
t4jp → artifact 37 → accepted/current
```

Current heterogeneous non-regression order:

```text
1. Python/software          ← tmBK accepted: P1.6 39 → Capability 13
2. network/security         ← t4qV accepted: P1.6 44 → Capability 14
3. operations/platform      ← tmyX accepted: P1.6 46 → Capability 15
```

### `tmBK`

Current upstream:

```text
source detail:        44
English projection:   38
P1.6 contract:        v20/v5
```

The first persisted candidate P1.6 artifact 38 was rejected because deterministic depth canonicalization propagated `Mastery` to unrelated concepts. Current v20 fixes that defect and the adjacent `Sufficient knowledge`, effective-AI-application and redundant-coverage-exclusion cases with regressions.

The rejected artifact did not feed Capability. Rebuilt P1.6 artifact 39 was explicitly accepted after complete manual review; Capability artifact 13 then passed 16/16 requirement coverage and 7/7 explicit-depth review. Python/software is closed.

Network/security `t4qV` (detail 30, English projection 20) is accepted on P1.6 44 → Capability 14; its five named certifications remain role-level. Operations/platform `tmyX` (detail 35, English projection 24) is accepted on P1.6 46 → Capability 15. General fixes cover credential ontology, safe generic-heading boundaries, explicit pre-heading candidate duties, and non-depth ability/skill wording. Heterogeneous validation is closed.

Expected source-calibrated depth semantics include:

```text
Python/Django                         Mastery
DRF/FastAPI                           Mastery
Git                                   Familiarity
Linux                                 Familiarity
SQL/NoSQL                             Familiarity
OOP + modular design                  Sufficient knowledge
Database locking/concurrency/tx       Familiarity
AI usage                              no technical depth
```

---

## 18. Acceptance strategy

Do not scale P1.6 merely because an artifact validates structurally.

For each heterogeneous reviewed job:

1. inspect source and English projection quality first;
2. run/reuse English P1.6 through the normal public path;
3. inspect role purpose;
4. inspect every responsibility;
5. inspect every requirement;
6. verify evidence is exact selected-representation text;
7. verify responsibility versus qualification classification;
8. verify requirement strength;
9. verify explicit depth is exact and concept-specific;
10. look for omitted explicit source requirements;
11. verify coverage is complete/non-contradictory;
12. reject the artifact if materially wrong even if mechanical validation completed;
13. run Capability only after P1.6 acceptance;
14. convert repeatable deterministic failures into regression fixtures.

Representative acceptance intentionally varies role family and evidence shape rather than repeatedly tuning one vacancy.

---

## 19. Known limits

P1.6 still does not provide:

- reviewed canonical aliases/taxonomy;
- corpus-scale fine-grained job capability requirement profiles;
- personal capability comparison;
- readiness/career recommendations;
- calibrated model-quality scoring against a broad gold corpus;
- complete bilingual span alignment;
- mature repost/duplicate normalization before later market intelligence;
- proof of semantic stability across every target role family.

Those are later layers or remaining acceptance work. Current Phase-1 work is to prove the promoted factual contract generalizes across a bounded heterogeneous sample without unresolved repeatable material defects.
