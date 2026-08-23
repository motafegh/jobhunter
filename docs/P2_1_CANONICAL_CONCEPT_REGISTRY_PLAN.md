# P2.1 Canonical Concept Registry Plan

**Status:** CLOSED / ACCEPTED
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

### P2.1D — Seed and acceptance — ACCEPTED

- [x] seed a deliberately small cross-role set from the five accepted chains;
- [x] include at least one alias, one ambiguous/unmapped case, one responsibility, and one
  education/credential or experience signal;
- [x] inspect every seed decision against exact accepted P1.6 evidence;
- [x] verify rerun/idempotency and stale-dependency behavior;
- [x] complete real-local CLI/browser inspection and standard Ruff/full-pytest/warnings-as-errors
  acceptance;
- [x] keep registry publication separate; no repository projection was authorized for P2.1D.

Accepted seed shape:

```text
canonical concepts: 4
reviewed aliases:   1
claim decisions:    6
  mapped:           5
  unmapped:         1
accepted chains:    5
```

Final acceptance record:

```text
docs/working-memory/2026-08-23_P2_1D_AND_P2_1_FINAL_ACCEPTANCE.md
```

## 5. Non-goals

- no automatic model-generated taxonomy growth;
- no bulk mapping of all 85 current requirement claims in the first increment;
- no forced title-to-role taxonomy;
- no similarity embeddings, vector database, graph database, or RAG;
- no Capability/Blueprint prose promotion;
- no Market v2 aggregation until a later focused increment explicitly starts it;
- no second source, personal evidence, scoring, recommendations, or applications.

## 6. Acceptance

P2.1 closure criteria are satisfied:

- [x] stable IDs, categories, aliases, mappings, supersession, and unmapped state are durable;
- [x] every accepted mapping retains exact P1.6 artifact/claim provenance;
- [x] stale P1.6 dependencies cannot count as current mappings;
- [x] no automated path can silently accept a concept or alias;
- [x] CLI/browser review paths share the same service contract;
- [x] deterministic tests and warning gates pass;
- [x] the small seed is completely human/semantic reviewed;
- [x] docs distinguish canonical correspondence from employer wording and market prevalence.

Observed final quality evidence includes:

```text
ruff check .          PASS
pytest                PASS — 510 passed in 14.89s
pytest -W error       PASS — explicitly confirmed by repository owner
focused P2.1D test    PASS — 2 passed in 2.47s
```

The repository connection did not mutate the owner's machine-local SQLite. Actual local seed
application, rerun/idempotency, CLI state, and browser state were executed and reported by the owner
against `data/jobhunter.sqlite3`; deterministic disposable regression evidence remains separate.

## 7. Closure and next-work boundary

P2.1A, P2.1B, P2.1C, and P2.1D are accepted. **P2.1 is closed.**

The accepted registry remains deliberately bounded. Closure does not authorize additional mappings,
ontology expansion, registry publication, Market v2, or personal intelligence.

Next action:

1. inspect the controlling roadmap and implementation-plan sequence after P2.1;
2. define the next bounded focused Phase-2 increment before implementation;
3. preserve the accepted P1.6 v20/v5, Capability v9/v5, and canonical-registry v1 boundaries;
4. make any registry publication path a separate privacy/source decision.

Until that next focused plan is explicitly selected:

- do not bulk-map the remaining accepted claim corpus;
- do not broaden the ontology merely to eliminate unmapped cases;
- do not publish registry state;
- do not start Market v2;
- do not add personal readiness/scoring/recommendations.
