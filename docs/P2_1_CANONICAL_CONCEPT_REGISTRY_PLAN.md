# P2.1 Canonical Concept Registry Plan

**Status:** Active focused Phase-2 plan
**Date:** 2026-08-23
**Scope:** P2.1 registry and reviewed mappings only
**Authority:** Subordinate to product/domain/source/architecture, `docs/ROADMAP.md`, and `docs/IMPLEMENTATION_PLAN.md`

## 1. Objective

Build the smallest durable reviewed semantic registry that can map accepted job-level facts to
stable market concepts without replacing source wording or silently growing from model output.

```text
accepted/current P1.6 source claim
→ explicit mapping candidate or explicit unmapped state
→ human review
→ stable canonical concept + reviewed alias
→ later P2.2/P2.3 aggregation
```

Contract:

```text
jobhunter-canonical-concept-registry-v1
```

## 2. Authority and boundaries

- accepted/current English P1.6 is the only initial job-claim input;
- Capability v9 deterministic grouping/source links may inform later design, but model prose is not
  canonical authority;
- original source wording and exact P1.6 artifact/claim identity remain preserved;
- canonicalization is correspondence and review, not evidence that an employer used the preferred
  label;
- no model or import path may create an accepted concept or alias automatically;
- unknown and unmapped are first-class outcomes;
- Blueprint remains excluded;
- no personal evidence, readiness, recommendations, or corpus-wide inference.

## 3. Versioned domain contract

### 3.1 Concept

Each concept has:

- stable explicit ID;
- category;
- preferred label;
- optional bounded description;
- active/deprecated state;
- optional successor concept;
- created/updated review timestamps.

Initial categories:

```text
language
framework
library
tool
platform
skill
knowledge_area
practice
domain
experience_signal
education_credential
responsibility
deliverable
```

### 3.2 Alias

Each alias preserves exact display wording, deterministic normalized lookup text, category,
canonical concept ID, provenance kind/reference, review state/time/note, and historical state.
Ambiguous text across categories is allowed; one normalized alias cannot map to two active concepts
inside the same category.

### 3.3 Job-claim mapping

Each mapping preserves:

- exact accepted P1.6 artifact ID;
- claim kind and zero-based claim index;
- exact source concept/statement and normalized lookup text;
- canonical concept ID when mapped;
- `mapped`, `unmapped`, or `rejected` disposition;
- reviewer time/note;
- current dependency status derived from the owning P1.6 chain.

Rebuilding or changing P1.6 never rewrites historical mappings. Stale mappings become non-current.

## 4. Delivery increments

### P2.1A — Deterministic contract and persistence — ACCEPTED

- [x] typed concept/category/status/mapping records;
- [x] SQLite schema and migrations;
- [x] stable-ID and text-normalization validators;
- [x] explicit supersession constraints;
- [x] reviewed aliases with collision protection;
- [x] mapped/unmapped/rejected claim records with immutable P1.6 provenance;
- [x] deterministic offline tests.

### P2.1B — Manual CLI workflow — ACCEPTED

- [x] list/show/add/deprecate concepts;
- [x] add reviewed aliases with explicit provenance;
- [x] list accepted-current P1.6 claims and mapping state;
- [x] record mapped/unmapped/rejected decisions with meaningful notes;
- [x] preserve idempotency and immutable prior decisions;
- [x] complete local Ruff + pytest + warnings-as-errors gate passed on 2026-08-23.

### P2.1C — Read-only and review browser surfaces — ACTIVE NEXT INCREMENT

- [ ] registry overview and filters;
- [ ] concept detail with aliases and source-backed job mappings;
- [ ] unmapped review queue;
- [ ] CSRF-protected bounded manual decisions;
- [ ] structured links from operations where relevant;
- [ ] browser and CLI review mutations share the same canonical-registry service contract.

### P2.1D — Seed and acceptance — BLOCKED ON P2.1C

- [ ] seed a deliberately small cross-role set from the five accepted chains;
- [ ] include at least one alias, one ambiguous/unmapped case, one responsibility, and one
  education/credential or experience signal;
- [ ] inspect every seed decision against exact accepted P1.6 evidence;
- [ ] verify rerun/idempotency and stale-dependency behavior;
- [ ] publish only repository-safe registry projection if a separate privacy/source review accepts it.

## 5. Non-goals

- no automatic model-generated taxonomy growth;
- no bulk mapping of all 85 current requirement claims in the first increment;
- no forced title-to-role taxonomy;
- no similarity embeddings, vector database, graph database, or RAG;
- no Capability/Blueprint prose promotion;
- no Market v2 aggregation until reviewed registry mappings exist;
- no second source, personal evidence, scoring, recommendations, or applications.

## 6. Acceptance

P2.1 closes only when:

- stable IDs, categories, aliases, mappings, supersession, and unmapped state are durable;
- every accepted mapping retains exact P1.6 artifact/claim provenance;
- stale P1.6 dependencies cannot count as current mappings;
- no automated path can silently accept a concept or alias;
- CLI/browser review paths share the same service contract;
- deterministic tests and warning gates pass;
- the small seed is completely human/semantic reviewed;
- docs distinguish canonical correspondence from employer wording and market prevalence.

## 7. Exact next implementation step

P2.1A and P2.1B are accepted. Implement **P2.1C only**: the bounded browser review surface over the existing canonical-registry store/service and current accepted-P1.6 review reader.

Required scope:

1. registry overview with useful filters and no taxonomy inference;
2. concept detail with reviewed aliases and source-backed claim mappings;
3. accepted-current unmapped/pending review queue;
4. CSRF-protected bounded concept/alias/mapping decisions through the same service contract used by the CLI;
5. structured links from existing operations pages only where they improve review navigation;
6. deterministic browser/service tests plus the standard Ruff/full-pytest/warnings-as-errors gate.

Do not seed concepts, perform corpus-wide mapping, publish registry data, start Market v2, or add personal intelligence during P2.1C. P2.1D remains blocked until P2.1C is accepted.
