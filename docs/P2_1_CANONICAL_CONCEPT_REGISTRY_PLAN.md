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

### P2.1C — Read-only and review browser surfaces — ACCEPTED

- [x] registry overview and filters;
- [x] concept detail with aliases and source-backed job mappings;
- [x] accepted-current pending/unmapped review queue;
- [x] CSRF-protected bounded manual decisions;
- [x] structured links for registry review navigation where useful;
- [x] browser and CLI review mutations share the same canonical-registry service contract;
- [x] registry review writes remain outside public-corpus refresh side effects;
- [x] complete local Ruff + pytest + warnings-as-errors gate passed on 2026-08-23.

### P2.1D — Seed and acceptance — ACTIVE NEXT INCREMENT

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

P2.1A, P2.1B, and P2.1C are accepted. Execute **P2.1D only**: create and semantically review the deliberately small cross-role seed needed to prove the registry on real accepted evidence and close P2.1.

Required scope:

1. inspect exact accepted/current P1.6 claims from all five accepted chains before choosing seed identities;
2. keep the seed deliberately small rather than mapping the available claim corpus;
3. include at least one reviewed alias, one explicit ambiguous/unmapped decision, one responsibility mapping, and one education/credential or experience-signal mapping;
4. preserve exact artifact/claim provenance and meaningful review notes for every decision;
5. prove rerun/idempotency and stale-dependency behavior on the accepted seed;
6. run the standard Ruff/full-pytest/warnings-as-errors gate;
7. make any repository-safe registry projection a separate privacy/source decision rather than an implicit consequence of P2.1D.

Do not bulk-map the accepted claim corpus, start Market v2, add personal intelligence, or publish registry state during P2.1D unless the separate publication decision is explicitly made. P2.1 remains open until the seed and every focused-plan acceptance criterion pass.
