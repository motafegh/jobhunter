# P2.1B manual registry CLI — acceptance

Date: 2026-08-23
Status: **ACCEPTED / CLOSED FOR THE P2.1B SCOPE**

## 1. Accepted baseline

P2.1A deterministic registry persistence remains accepted. P2.1B was implemented on:

```text
c9f6a237073f816cbc7c2e6673831d9771d1e6de
feat: add P2.1B manual registry review CLI
```

The pre-acceptance checkpoint remains preserved at:

```text
docs/working-memory/2026-08-23_P2_1B_MANUAL_CLI_IMPLEMENTATION_PENDING_VALIDATION.md
```

## 2. Accepted P2.1B capability

The bounded auxiliary CLI is:

```text
jobhunter-registry
```

Accepted manual review operations:

- list/show/add/deprecate reviewed canonical concepts;
- add reviewed aliases with explicit provenance/reference/review note;
- list accepted-current English P1.6 requirement/responsibility claims and their mapping state;
- record explicit `mapped`, `unmapped`, or `rejected` decisions;
- preserve exact P1.6 artifact/claim provenance;
- preserve idempotent repeated identical decisions;
- reject attempts to rewrite an existing immutable mapping decision.

The claim queue remains fail-closed to the frozen current English P1.6 contract and exact current English translation dependency.

## 3. Validation evidence

On 2026-08-23 the complete repository-equivalent local acceptance gate was run against the P2.1B implementation and reported green:

```text
ruff check .
pytest
pytest -W error
```

All three commands passed. No CI run number or test count is asserted here because the acceptance evidence supplied was the complete local gate rather than a recorded GitHub Actions result.

Therefore the P2.1B deterministic and warning-as-error acceptance requirement is satisfied.

## 4. Boundary confirmation

P2.1B acceptance does **not** authorize or imply:

- automatic taxonomy growth;
- concept or alias seeding by a model;
- corpus-wide claim mapping;
- browser mutation beyond the next explicitly planned increment;
- Market v2 aggregation;
- public registry projection;
- personal evidence, readiness/gap scoring, ranking, recommendations, or applications.

P1.6 v20/v5 and Capability v9/v5 remain frozen Phase-2 source-truth inputs.

## 5. Next authorized increment

The governing P2.1 delivery order now advances to **P2.1C — read-only and review browser surfaces**:

- registry overview and filters;
- concept detail with reviewed aliases and source-backed job mappings;
- unmapped review queue;
- CSRF-protected bounded manual decisions;
- structured links from existing operations where relevant;
- CLI and browser mutation paths must share the same canonical-registry service contract.

Do not start the P2.1D seed while P2.1C is incomplete. P2.1 itself remains open until the browser/service boundary and the deliberately small fully human-reviewed seed satisfy the focused plan acceptance criteria.
