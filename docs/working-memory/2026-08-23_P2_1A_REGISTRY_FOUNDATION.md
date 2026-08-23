# P2.1A Canonical Registry Foundation

**Date:** 2026-08-23
**Disposition:** ACCEPTED
**Contract:** `jobhunter-canonical-concept-registry-v1`

## Implemented

`src/jobhunter/canonical_registry.py` establishes the non-model Phase-2 registry boundary:

- thirteen explicit concept categories;
- stable `category:lowercase-kebab-slug` IDs;
- preferred labels and conservative NFKC/casefold/whitespace lookup normalization;
- reviewed active/deprecated concepts and same-category successor constraints;
- reviewed aliases with category-scoped collision protection and provenance;
- immutable job-claim decisions with `mapped`, `unmapped`, and `rejected` dispositions;
- exact analysis artifact, source job, detail version, translation artifact, claim kind/index, and
  original source text on every decision;
- service-level admission only from the configured current English projection and semantically
  accepted P1.6 v20/v5 artifact.

No concepts or aliases were seeded. No model, network, CLI mutation, browser mutation, Market v2,
Capability prose, Blueprint, or personal evidence entered this increment.

## Key invariants

```text
model output                          != accepted canonical concept
normalized lookup text               != replacement source wording
same alias in different categories   allowed
same alias → two concepts/category   blocked
responsibility claim → other category blocked
pending/stale P1.6                    blocked
changed mapping decision              blocked; history immutable
unknown                               explicit unmapped decision
```

## Validation

```text
focused canonical registry tests: 6 passed
ruff check .:                     PASS
pytest -q -W error:               498 passed
git diff --check:                 PASS
jobhunter-corpus verify:          PASS (353 known jobs)
```

The schema also initialized successfully against the real existing SQLite database. All three
registry tables remained at zero rows and `PRAGMA foreign_key_check` returned no findings.

## Exact next step

Implement P2.1B manual CLI workflows through the accepted store/service. Do not seed the registry
or add browser mutation until the CLI review contract and claim queue are inspectable and accepted.
