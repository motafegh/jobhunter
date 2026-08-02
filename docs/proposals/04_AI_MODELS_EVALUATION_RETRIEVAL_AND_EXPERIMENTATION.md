# JobHunter AI Models, Evaluation, Retrieval, and Experimentation Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B011-B012, B116, B121, B123-B129, B159-B160, B167-B169, B185-B187

---

## Relationship to the existing AI proposal

`../AI_INTELLIGENCE_RAG_CONTINUAL_LEARNING_PROPOSAL.md` is the existing deep proposal for multi-provider inference, specialist agents, RAG, continual learning, AI Lab, evaluation, security, and future AI product surfaces. This category does **not** replace it. The purpose here is to preserve the brainstorm items B001-B200 in the common proposal catalog and to identify how these specific ideas relate to that larger AI architecture.

Where this file and the existing AI proposal overlap, the existing deep proposal should be treated as the richer design reference. Neither document is controlling implementation scope.

---

## B011 — Translation golden corpus and quality evaluation

**Intent:** Make translation-provider/model changes measurable rather than subjective.

**Proposal:** Maintain a curated corpus of Persian/mixed-language source segments with human-reviewed English references and important semantic annotations such as requirement strength, negation, technical terms, names, and content that must not be omitted.

**Evaluation dimensions:**

- meaning preservation;
- modality/requirement-strength preservation;
- negation preservation;
- technical terminology;
- completeness;
- field/segment association integrity;
- hallucinated or missing information.

**Design direction:** Keep deterministic v2 integrity checks as production gates. The golden corpus is a deeper benchmark, not a replacement for those invariants.

**Guardrails:** Do not use one model's output as ground truth merely because it is fluent. Gold references require deliberate review.

**Promotion signal:** Before changing the trusted translation contract or introducing additional translation providers.

---

## B012 — JobHunter model laboratory

**Intent:** Compare models, prompts, and inference strategies against JobHunter-specific evidence.

**Proposal:** Create an isolated AI Lab that can run candidate models/contracts on frozen reviewed corpora without silently promoting results into current production artifacts.

**Metrics may include:** unsupported claims, missed requirements, required/preferred errors, evidence-validation failures, translation fidelity, latency, output truncation, tokens, and provider cost where relevant.

**Design direction:** Experiments should have explicit input snapshot, candidate contract, baseline contract, metrics, review sample, and promotion decision.

**Guardrails:** No production artifact becomes current because an experiment “looks better.” Promotion requires defined acceptance thresholds and rollback.

**Promotion signal:** When a second serious analysis/translation contract or provider is being evaluated.

---

## B116 — Model/prompt/analysis contract registry

**Intent:** Prevent durable AI behavior from being identified only by scattered constants or configuration strings.

**Proposal:** Once enough versions exist, introduce a registry describing durable inference contracts such as translation, semantic analysis, verification, retrieval, and synthesis.

**Possible fields:**

```text
contract_id
capability/task
provider requirements
model identity or routing policy
prompt version
schema version
created_at
status: candidate/current/historical/retired
supersedes
notes / benchmark evidence
```

**Design direction:** Artifact identity remains exact and reproducible. The registry should describe contracts, not rewrite historical artifacts.

**Guardrails:** Do not introduce a registry while one or two constants remain simpler and clearer. Avoid a generic workflow DSL.

**Promotion signal:** When contract versioning becomes operationally confusing or multiple candidates are routinely compared.

---

## B121 — Model chaos testing

**Intent:** Verify that AI boundaries reject structurally valid-looking but semantically dangerous model failures.

**Proposal:** Build deterministic fake providers/fixtures that deliberately return outputs such as wrong content IDs, extra fields, hallucinated source excerpts, duplicated claims, malformed JSON, truncated output, incorrect language, wrong-field translations, or valid JSON with unsupported evidence.

**Design direction:** Run these in normal deterministic tests without live model/network access. Each known historical failure should become a durable regression case.

**Guardrails:** Chaos fixtures should exercise product contracts, not attempt to simulate every imaginable model behavior.

**Promotion signal:** Near-term whenever a new model-derived durability boundary is added.

---

## B123 — Task-specific local model routing

**Intent:** Let different local models specialize by task rather than forcing one model to do everything.

**Proposal:** Future routing could select different models for translation, structured semantic extraction, lightweight classification, embeddings, reranking, and synthesis, based on measured JobHunter benchmarks.

**Design direction:**

- route by explicit task contract;
- persist the model/provider that actually executed durable work;
- keep personal-data privacy rules independent from model preference;
- allow a simple single-model configuration to remain valid.

**Guardrails:** Complexity is justified only by measured quality/latency/cost improvements. Do not build model orchestration for novelty.

**Promotion signal:** When benchmarks demonstrate that one-model-for-all materially underperforms.

---

## B124 — Cheap-first / deterministic-first analysis

**Intent:** Reserve expensive inference for ambiguity that actually needs it.

**Proposal:** Use a staged pipeline where deterministic extraction/classification or a smaller model handles simple cases, escalating to a stronger model only when confidence/validation signals require it.

**Conceptual flow:**

```text
deterministic rules
→ lightweight model if needed
→ strong model for unresolved/ambiguous cases
→ deterministic validation
```

**Design direction:** Record which path was used. Evaluate end-to-end quality, not just per-model accuracy.

**Guardrails:** Do not let early-stage heuristics silently reduce recall. Escalation criteria must be measurable and testable.

**Promotion signal:** When inference volume/cost/latency becomes material and a benchmark corpus exists.

---

## B125 — Model disagreement review

**Intent:** Use disagreement as a targeted uncertainty signal rather than blindly trusting or majority-voting models.

**Proposal:** For selected ambiguous/high-value items, run a second independent contract/model and compare material claims such as requirement strength or concept classification. Disagreement becomes a review signal.

**Design direction:**

- store both outputs independently;
- compare normalized claim identities;
- surface exact disagreement and evidence;
- allow human resolution or leave unresolved;
- measure whether disagreement predicts real errors.

**Guardrails:** Do not double inference cost for every job by default. Two models agreeing is not proof of truth.

**Promotion signal:** After a reviewed corpus shows specific error classes where independent disagreement is useful.

---

## B126 — Semantic search over JobHunter evidence

**Intent:** Find jobs or personal evidence by meaning when keyword/title matching is insufficient.

**Proposal:** Add embeddings/retrieval only for concrete queries such as “find jobs with similar work despite different titles” or “find project evidence relevant to this requirement.”

**Design direction:**

- index derived/normalized chunks with source references;
- version embedding model, chunking, and index strategy;
- retain keyword/structured filtering alongside vectors;
- evaluate retrieval against reviewed query sets;
- never make the vector index an authority store.

**Guardrails:** Do not introduce a vector database merely because embeddings are fashionable. SQLite plus an appropriate local index may be sufficient.

**Promotion signal:** When real user queries cannot be served well by structured/keyword search alone.

---

## B127 — Similar-job explorer with explicit similarity dimensions

**Intent:** Let the user find related opportunities without conflating different notions of similarity.

**Proposal:** Support separate similarity modes such as:

```text
similar responsibilities
similar required capabilities
similar company stack
similar role archetype
similar personal-evidence fit
```

**Design direction:** Use structured semantic analysis first where possible, embeddings as a complementary retrieval layer, and explain why each result is considered similar.

**Guardrails:** Avoid one opaque cosine-similarity ranking presented as universal similarity.

**Promotion signal:** After canonical role/responsibility concepts and/or evaluated semantic retrieval exist.

---

## B128 — “Show me jobs like this but easier”

**Intent:** Discover nearby opportunities with similar work but fewer major personal-evidence gaps.

**Proposal:** Combine responsibility/role similarity with personal gap analysis to retrieve jobs that resemble a selected role while having fewer critical missing requirements or lower required depth.

**Design direction:**

1. retrieve a similar-work candidate set;
2. calculate explicit requirement-by-requirement evidence states;
3. filter/order by major-gap count or categorical readiness policy;
4. explain both similarity and why the result is considered more approachable.

**Guardrails:** “Easier” means fewer evidenced gaps under the chosen policy, not objectively easy to obtain.

**Promotion signal:** After semantic similarity and personal gap comparison are both accepted.

---

## B129 — Bridge-role discovery

**Intent:** Find roles that connect current evidence to a longer-term target.

**Proposal:** Identify job/role archetypes whose responsibility profile overlaps current demonstrated capabilities while building capabilities that recur in the target role.

**Design direction:** Use explicit capability/role graphs and market evidence. A bridge role should show:

- capabilities already supported;
- target capabilities it would exercise;
- major remaining gaps;
- market availability/sample size.

**Guardrails:** This is not a guaranteed career ladder. Avoid inferring that one employer role automatically leads to another.

**Promotion signal:** After role archetypes, personal capability mapping, and target role specifications exist.

---

## B159 — Analysis drift detection

**Intent:** Detect quality or behavior changes after model, prompt, schema, provider, or runtime changes.

**Proposal:** Monitor stable metrics across analysis contracts, for example average claims/job, required/preferred distribution, evidence-validation failure rate, unsupported-claim review rate, and concept distribution on a fixed benchmark corpus.

**Design direction:** Compare candidate to baseline on the same snapshot. Production time-series monitoring may complement benchmark tests but should not replace them.

**Guardrails:** Real market change can alter production distributions; do not automatically call every distribution shift model drift.

**Promotion signal:** Before frequent model/provider upgrades become normal.

---

## B160 — Taxonomy drift and new-concept discovery

**Intent:** Detect when new terminology appears faster than the canonical taxonomy is evolving.

**Proposal:** Track unmapped/low-confidence concept mentions and their frequency over time. Surface candidate new aliases, technologies, practices, or role terms for review.

**Design direction:**

- preserve source spelling and context;
- aggregate candidate mentions deterministically;
- allow semantic normalizers/models to propose mappings;
- require review before canonical taxonomy mutation;
- maintain taxonomy-version history.

**Guardrails:** A new phrase is not automatically a new concept; it may be an alias or transient wording.

**Promotion signal:** Once canonical concept mapping is active at meaningful corpus scale.

---

## B167 — Local experimentation sandbox

**Intent:** Test alternative search, taxonomy, model, retrieval, or analytical logic without modifying current accepted artifacts.

**Proposal:** Provide an experiment namespace/workspace that can reference a frozen database/evidence snapshot and produce candidate outputs separately from production current-state resolution.

**Design direction:** Experiments have identifiers, input snapshot, parameters/contracts, results, metrics, and promotion status. Re-running an experiment should be reproducible where dependencies permit.

**Guardrails:** No experiment writes current production pointers by default.

**Promotion signal:** When experimental AI/taxonomy work becomes frequent enough that ad hoc scripts are risky.

---

## B168 — Branching analytical contracts

**Intent:** Compare a candidate analysis contract with the current contract over the same source corpus.

**Proposal:** Support parallel durable identities such as `job-analysis-v1` and candidate `job-analysis-v2`. Both may coexist for evaluation; only explicitly accepted contract identities feed current market views.

**Design direction:** Reuse the existing artifact identity philosophy: source semantic version + supporting translation identity + model + prompt + schema. Add explicit candidate/current status outside the immutable artifact.

**Guardrails:** Never relabel v1 artifacts as v2. Market aggregation must select an exact accepted contract.

**Promotion signal:** Before the first material P1.6 schema/prompt revision.

---

## B169 — Historical reproducibility across AI upgrades

**Intent:** Keep old analytical conclusions explainable after newer models/contracts are adopted.

**Proposal:** Preserve historical translation/analysis/retrieval identities and enough configuration metadata to reconstruct which contract produced a report or decision snapshot.

**Design direction:** Reports/snapshots should reference exact analytical contract IDs rather than “current” only. Reprocessing creates new artifacts, never destructive replacement.

**Guardrails:** Reproducibility does not require keeping every executable model binary forever if licensing/storage makes that impractical; at minimum preserve inputs, provider/model identity, contract, output, and validation metadata.

**Promotion signal:** This should remain a permanent design rule as AI contracts evolve.

---

## B185 — Human annotation workspace

**Intent:** Create small, high-quality reviewed datasets that improve evaluation and taxonomy decisions.

**Proposal:** Add a bounded annotation interface for selected source text, translations, requirements, responsibilities, concept mappings, and role labels.

**Design direction:** Annotation schemas are versioned; source evidence is always visible; disagreements can remain unresolved; exports support evaluation tooling.

**Guardrails:** Annotation is expensive and should target high-leverage cases rather than trying to manually label the full corpus.

**Promotion signal:** When model/taxonomy evaluation needs more consistent human reference data.

---

## B186 — Gold-job benchmark collection

**Intent:** Maintain a representative set of deeply reviewed complete job postings for end-to-end regression.

**Proposal:** Curate perhaps tens, later up to roughly a hundred postings spanning important languages, role families, description lengths, ambiguity levels, and source edge cases. For each, maintain reviewed expected analysis/taxonomy outcomes where appropriate.

**Design direction:** Gold jobs are stable benchmark fixtures, distinct from production current data. New failure classes should add targeted examples.

**Guardrails:** Do not assume the gold set represents market frequency. It is a quality benchmark, not a market sample.

**Promotion signal:** Begin small around P1.6/translation acceptance and expand only as real failure classes emerge.

---

## B187 — Representative review sampling

**Intent:** Avoid validating model quality on five conveniently similar jobs.

**Proposal:** Build deterministic sample selection that intentionally covers variation across role family, company, language mix, description length, requirement density, source age, and known edge cases.

**Design direction:** Store the sampling rule and selected IDs with evaluation results. Include some random sampling to avoid only reviewing cases already known to be difficult.

**Guardrails:** Representative sampling is relative to the available corpus; it cannot correct source-market coverage bias by itself.

**Promotion signal:** Immediately useful for the first meaningful P1.6 reviewed batch and later model evaluations.

---

## Category-level recommendation

The existing AI proposal already defines the broad architecture. The strongest near-term ideas from this category are golden/representative evaluation data, chaos/regression tests, exact contract versioning, and a safe experiment boundary. Semantic retrieval, multi-model routing, and bridge-role intelligence should wait until structured Phase-2/3 data proves the need.