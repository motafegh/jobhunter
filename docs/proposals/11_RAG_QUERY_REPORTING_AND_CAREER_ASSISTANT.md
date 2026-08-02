# JobHunter RAG, Query, Reporting, and Career-Assistant Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B093-B098

---

## Relationship to the existing AI proposal

The deep architectural treatment of Retrieval-Augmented Generation (RAG), specialist agents, retrieval memory, and AI product surfaces already exists in `../AI_INTELLIGENCE_RAG_CONTINUAL_LEARNING_PROPOSAL.md`. This file preserves the user-facing query/report ideas from the B001-B200 brainstorm and defines the product contracts they should satisfy.

---

## B093 — Natural-language market queries

**Intent:** Let the user ask analytical questions in normal language without giving an LLM unrestricted database access.

**Proposal:** Support questions such as:

- Which technologies most often accompany Python in security-automation roles?
- Show jobs where Docker is preferred rather than required.
- Which jobs mention networking but not Kubernetes?
- How has RAG demand changed in the current sample?

**Design direction:**

```text
user question
→ bounded query planner
→ approved read-only structured queries / retrieval
→ deterministic result tables
→ optional grounded synthesis
```

The plan, filters, data snapshot, and supporting records should remain inspectable.

**Guardrails:** No arbitrary SQL generated and executed without a safe query layer. The model must not invent counts that deterministic queries can calculate.

**Promotion signal:** After stable canonical market tables exist and real questions exceed the usability of predefined filters.

---

## B094 — Evidence-backed career chat

**Intent:** Provide conversational access to JobHunter's own evidence rather than generic model memory.

**Proposal:** A local assistant could answer questions such as “Why are you recommending networking?” or “What evidence supports this gap?” by retrieving relevant market aggregates, employer excerpts, personal evidence, and prior decision records.

**Design direction:** Every answer should distinguish retrieved JobHunter facts from general model explanation. Citations/links point to the exact local records used. Sensitive personal retrieval obeys local/privacy routing rules.

**Guardrails:** The assistant's conversational memory is not durable personal truth. If the evidence is insufficient, answer `insufficient evidence` rather than filling gaps from generic knowledge.

**Promotion signal:** After RAG/retrieval evaluation and personal evidence boundaries are accepted.

---

## B095 — Query reproducibility

**Intent:** Make AI-assisted analytical answers repeatable and debuggable.

**Proposal:** Persist or export a query record containing user question, normalized intent, filters, selected data snapshot, retrieval/query plan, analysis/taxonomy contract, returned deterministic data, model/provider identity where synthesis occurred, and final answer.

**Design direction:** Re-running the exact historical query can either use its frozen snapshot or explicitly re-run against current data as a different operation.

**Guardrails:** Avoid storing conversational noise forever. Persist queries that produce durable reports/decisions or when the user explicitly saves them.

**Promotion signal:** Required before conversational market answers become inputs to durable decisions.

---

## B096 — On-demand generated charts

**Intent:** Let analytical questions produce visual evidence when a chart communicates the answer better than prose.

**Proposal:** Convert structured query results into a constrained set of chart types such as bar, line, heatmap, or distribution plots. Example: compare required capability prevalence between AI Security and ML Engineer archetypes.

**Design direction:** Chart data comes from deterministic query results; generated chart configuration records filters, denominators, and snapshot. Provide an accessible table alongside the visual.

**Guardrails:** The model may select or describe a chart but should not fabricate its data. Avoid decorative charts with tiny samples.

**Promotion signal:** After natural-language query planning or report generation is accepted.

---

## B097 — Versioned report builder

**Intent:** Produce durable analytical outputs for recurring decisions and review.

**Proposal:** Support report types such as:

```text
Weekly Market Report
Target Role Report
Capability Gap Report
Learning Priority Report
Application Preparation Report
Company Report
```

**Design direction:** Reports contain structured facts/tables first and optional grounded narrative second. Each report records source snapshot, filters, analytical contracts, generation time, and references.

**Guardrails:** A report is a derived artifact, not an authority layer above its underlying evidence. Re-generation should create a new version when inputs change.

**Promotion signal:** Begin with the first repeated report users actually need; do not build a generic report designer prematurely.

---

## B098 — Weekly career-intelligence briefing

**Intent:** Summarize what requires attention across the product on a useful cadence.

**Proposal:** A weekly or user-triggered briefing could include new relevant jobs, important lifecycle changes, market movements, search drift, review backlog, personal evidence changes, and gaps whose priority changed.

**Design direction:** Generate from durable change sets and deterministic metrics, with optional synthesis. Allow the user to configure sections/cadence and suppress empty categories.

**Guardrails:** Avoid generic job-news summaries and high-frequency noise. If nothing meaningful changed, say so.

**Promotion signal:** After repeated acquisition and longitudinal snapshots are reliable.

---

## Category-level recommendation

The query/assistant layer should be built only after JobHunter has enough trustworthy structured data to retrieve. Its defining behavior should be: retrieve/calculates first, synthesize second, cite always, and preserve the difference between corpus evidence and generic model knowledge.