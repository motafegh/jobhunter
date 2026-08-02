# JobHunter Architecture, Platform, and Developer-Knowledge Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B146, B148-B154, B171-B173

---

## Purpose

This family covers architectural evolution and internal tooling that can make JobHunter easier to understand, extend, debug, and learn from without abandoning the current modular-monolith discipline. Most proposals here are valuable only when a real complexity threshold is crossed.

---

## B146 — Career knowledge graph as a logical model

**Intent:** Represent relationships among jobs, companies, roles, responsibilities, requirements, concepts, personal capabilities, gaps, projects, and decisions.

**Proposal:** Treat these relations as a logical knowledge graph while continuing to implement them with explicit relational tables/foreign keys as long as SQLite serves the queries well.

**Conceptual nodes:**

```text
Job
Company
RoleArchetype
Responsibility
Requirement
CareerConcept
PersonalCapability
CapabilityEvidence
GapAssessment
LearningAction
Project
Application
```

**Design direction:** Define typed relationships and provenance first. Graph visualizations or specialized storage come later if real traversal queries justify them.

**Guardrails:** No Neo4j/graph database merely because the domain can be drawn as nodes and edges.

**Promotion signal:** Use as a modeling lens during Phase 2-4 schema design.

---

## B148 — Developer/learning mode

**Intent:** Make JobHunter itself easier to study as an engineering project without polluting the normal user experience.

**Proposal:** Add optional local developer surfaces exposing architecture maps, data-flow traces, schema information, pipeline stages, model contracts, evidence lineage, and explanation links.

**Design direction:** Developer mode is read-only by default and gated by explicit local configuration. It uses existing runtime/store introspection rather than a second implementation path.

**Guardrails:** Do not expose secrets, raw credentials, unsafe arbitrary SQL, shell access, or unrestricted debug endpoints.

**Promotion signal:** Add individual tools when they materially reduce debugging/learning cost.

---

## B149 — Trace one job end-to-end

**Intent:** Make one posting's complete path through JobHunter inspectable.

**Proposal:** Given a `source_job_id`, render a trace such as:

```text
discovered in run/search
→ search evidence
→ detail fetch observation
→ raw detail evidence
→ parsed semantic version
→ lifecycle state
→ English artifact/attempt
→ analysis artifact/attempt
→ canonical mappings / Market contribution
→ user workflow / later application state
```

**Design direction:** Build the trace from existing durable identifiers. Each step links to its record and contract/version.

**Guardrails:** The trace should not duplicate records or become a new authority store.

**Promotion signal:** High-value developer/support feature once the pipeline has several layers.

---

## B150 — Architecture diagnostics page

**Intent:** Provide a concise runtime view of how the local application is composed.

**Proposal:** A developer-only System page could show active configuration (safe subset), registered source adapters, database/schema version, evidence paths, current translation/analysis contracts, provider/model health, operation queue state, and feature capability flags.

**Design direction:** Redact secrets and personal payloads. Prefer explicit structured diagnostics over dumping environment variables.

**Guardrails:** Read-only; no generic runtime object inspector or arbitrary configuration mutation.

**Promotion signal:** When diagnosing environment/configuration problems becomes frequent.

---

## B151 — Data-flow visualizer

**Intent:** Show how an actual operation moves through application services and durable boundaries.

**Proposal:** For a selected workflow/job, render a simplified logical flow:

```text
HTTP/UI or CLI request
→ application service
→ source/provider adapter
→ evidence/store writes
→ downstream eligible selector
→ derived artifact
```

Optionally display actual record IDs and input/output summaries.

**Design direction:** Source the graph from a maintained architecture definition or trace events; avoid hand-drawn diagrams that silently drift from code.

**Guardrails:** Do not instrument every Python function merely to create animation. Focus on architectural boundaries.

**Promotion signal:** Primarily educational/debugging; add if it helps maintainers understand the growing pipeline.

---

## B152 — “Why does this code exist?” engineering context

**Intent:** Preserve the reasoning behind non-obvious implementation constraints that otherwise look unnecessarily complicated later.

**Proposal:** Link important code/design rules to incidents or architectural rationale. Example: one-semantic-segment translation exists because translation-v1 exposed cross-field association corruption.

**Design direction:** Use focused comments/docstrings plus links to ADR/incident docs/tests. A developer UI could surface these links contextually.

**Guardrails:** Do not narrate obvious code or overload source files with historical essays.

**Promotion signal:** Apply opportunistically around high-risk invariants.

---

## B153 — Lightweight Architecture Decision Records (ADRs)

**Intent:** Preserve major technical decisions and their tradeoffs without excessive governance ceremony.

**Proposal:** Use short ADRs only for decisions whose rationale matters across time, such as SQLite/local-first, immutable evidence, segment-level translation, analysis evidence validation, or a future provider/adapter abstraction.

**Suggested format:** context, decision, alternatives considered, consequences, status/date.

**Guardrails:** Do not create ADRs for routine implementation choices. The controlling product/master plans remain higher authority.

**Promotion signal:** Start when the next genuinely cross-cutting architectural decision is made.

---

## B154 — Engineering incident history

**Intent:** Turn real failures into durable engineering knowledge.

**Proposal:** Record significant incidents such as translation field permutation with concise fields: symptom, impact, root cause, resolution, regression protection, remaining limitations, and links to commits/tests.

**Design direction:** Incident docs are factual retrospectives, not blame records. They may later feed regression-corpus and developer-learning surfaces.

**Guardrails:** Do not document every minor bug as an incident.

**Promotion signal:** Appropriate for failures that change architecture/contracts or teach a reusable lesson.

---

## B171 — Generic external-processing provider boundary

**Intent:** Reuse protocol semantics across model/translation/embedding providers without creating brand-specific code everywhere.

**Proposal:** Define capability-oriented provider protocols such as `TranslationProvider`, `StructuredInferenceProvider`, `EmbeddingProvider`, or an OpenAI-compatible transport where actual semantics match.

**Design direction:** Keep task contracts above transport protocols. Provider-specific behavior remains explicit where schemas, tool calling, errors, authentication, or privacy semantics differ.

**Guardrails:** Do not force incompatible APIs behind a leaky universal interface. Do not create abstractions before a second implementation proves the seam.

**Promotion signal:** Existing AI proposal defines the deeper path; implement only when new providers are actually introduced.

---

## B172 — Preserve modular-monolith discipline

**Intent:** Explicitly resist unnecessary distributed-system complexity as feature count grows.

**Proposal:** Continue organizing JobHunter into clear domain/application/adapter/store modules within one local process/application deployment unless measured requirements demand otherwise.

**Design direction:** New domains may have their own repositories/services/schema modules while sharing one SQLite/evidence environment and application composition.

**Guardrails:** Do not introduce microservices, message brokers, Redis, API gateways, Kubernetes, or distributed tracing as portfolio decoration.

**Promotion signal:** This is a standing architectural constraint; any proposal to break the monolith must present a concrete bottleneck/failure it solves.

---

## B173 — Keep SQLite until evidence requires replacement

**Intent:** Avoid replacing a capable local database for prestige or hypothetical scale.

**Proposal:** Continue measuring database size, query latency, locking/contention, migration/backup pain, and analytical workload. Improve schema/indexes/read models before considering a server database.

**Design direction:** Define explicit migration triggers if they ever appear, such as sustained write contention, unsupported analytical queries, or portability limits that cannot be solved cleanly.

**Guardrails:** Corpus size alone is not a reason to migrate. The product is single-user/local-first.

**Promotion signal:** Evaluate only when observed metrics show a real SQLite limitation.

---

## Category-level recommendation

The architecture should evolve by pressure from real product capabilities. The most valuable internal additions are traceability and concise decision/incident knowledge. The strongest anti-feature proposals are equally important: preserve the modular monolith, keep SQLite, and avoid generic plugin/provider frameworks until multiple concrete implementations prove the abstraction.