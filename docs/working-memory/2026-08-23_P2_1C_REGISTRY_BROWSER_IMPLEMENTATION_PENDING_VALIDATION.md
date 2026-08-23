# P2.1C registry browser review — implementation checkpoint

Date: 2026-08-23
Status: **IMPLEMENTED / ACCEPTANCE PENDING**

## 1. Accepted parent state

P2.1A deterministic persistence and P2.1B manual CLI are accepted. The governing active increment is P2.1C from `docs/P2_1_CANONICAL_CONCEPT_REGISTRY_PLAN.md`.

P2.1C remains bounded to browser review over the existing accepted canonical-registry contract. It does not authorize taxonomy seeding, corpus-wide mapping, registry publication, Market v2, or personal intelligence.

## 2. Shared review boundary

A neutral UI-agnostic reader now lives in:

```text
src/jobhunter/canonical_registry_review.py
```

It owns the shared read model for:

- accepted/current English P1.6 requirement/responsibility claims;
- exact current translation dependency checks;
- immutable reviewed mapping lookup;
- reviewed concept aliases;
- concept-to-source-claim mapping inspection;
- current-vs-historical mapping derivation.

The P2.1B CLI was refactored to consume this neutral reader rather than owning a CLI-specific copy. Authoritative mapping writes still go through `CanonicalRegistryService.record_current_claim_mapping(...)`.

## 3. Browser review surface implemented

Normal runtime registration now includes `register_registry_routes(...)`.

Read surfaces:

```text
GET /registry
GET /registry/concepts/{concept_id}
GET /registry/claims
```

They provide:

- registry overview with category/status/text filters;
- explicit pending/mapped/unmapped/rejected current-claim counts;
- concept detail with preferred label, review state, aliases, successor history, and source-backed job mappings;
- current-vs-historical mapping visibility;
- accepted-current P1.6 claim queue filtered by job, claim kind, and mapping state;
- direct navigation from mappings/claims to exact JobHunter job records.

Manual review writes:

```text
POST /registry/concepts
POST /registry/concepts/{concept_id}/aliases
POST /registry/concepts/{concept_id}/deprecate
POST /registry/claims/decide
```

All browser writes require the existing local CSRF token. Concept/alias/deprecation writes use `CanonicalRegistryStore`; claim decisions use the same `CanonicalRegistryService` used by the CLI.

## 4. Important mutation/publication boundary

Registry review writes are intentionally synchronous and are **not** submitted to `WebOperationManager`.

Reason:

```text
WebOperationManager successful operation
→ current launcher after_success hook
→ public-corpus refresh
```

P2.1C does not authorize canonical-registry publication into `corpus/`. Running registry review writes outside that operation hook therefore prevents accidental coupling between private/local reviewed registry state and the existing public Phase-1 projection.

A regression test asserts that a registry review write does not trigger `_synchronize_public_corpus(...)`.

## 5. Navigation decision

The normal runtime now exposes Registry in primary navigation. Registry claims and concept mappings link to their exact JobHunter job records; concept pages link back to the registry and pending review queue.

No background-operation result was changed merely to force a Registry link. Registry decisions are synchronous review actions rather than long-running operations, and P2.1C intentionally avoids creating an operation/public-corpus coupling for navigation convenience.

## 6. Tests added

`tests/test_canonical_registry_web.py` covers:

1. runtime route registration;
2. explicit empty-registry state before P2.1D seeding;
3. CSRF rejection;
4. reviewed concept creation and alias provenance through the browser;
5. accepted/current P1.6 pending-claim rendering;
6. browser mapping through the shared canonical-registry service;
7. source-backed concept detail and current mapping state;
8. immutable mapping rewrite rejection;
9. registry review writes do not trigger public-corpus export.

Existing P2.1B CLI tests remain the non-regression gate for the shared reader refactor.

## 7. Acceptance status

P2.1C is **not accepted yet**. The full repository-equivalent local gate must pass after this implementation:

```text
ruff check .
pytest
pytest -W error
```

Do not mark D3/P2.1C accepted until all three are green.

## 8. After validation

If the full gate passes:

1. mark P2.1C accepted and reconcile `docs/EXECUTION_TODO.md`, the focused P2.1 plan, and rolling working memory;
2. advance to P2.1D only;
3. design a deliberately small cross-role seed from the five accepted chains;
4. human-review every seed concept/alias/mapping against exact accepted P1.6 evidence;
5. include the required alias, ambiguous/unmapped case, responsibility, and education/credential or experience signal;
6. keep registry publication a separate privacy/source decision.
