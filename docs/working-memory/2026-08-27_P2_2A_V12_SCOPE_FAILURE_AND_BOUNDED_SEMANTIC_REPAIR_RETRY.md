# P2.2A v1.2 Scope Failure and Bounded Semantic Repair Retry

**Date:** 2026-08-27  
**Status:** REPAIR IMPLEMENTED / CI GREEN / REAL-LOCAL RERUN NEXT  
**Branch:** `main`

## Context

P2.2A Job Work Intelligence is implemented and is in real-local semantic/product acceptance.

Current identities:

```text
contract/schema: job-work-intelligence-v1
prompt:          job-work-intelligence-v1.2
```

The v1.2 prompt was introduced after two independent candidate outputs strengthened accepted action authority:

```text
tmyX: develop/provide hardening solutions
      → candidate said implementing hardening solutions

tG9K: partner to move models toward production
      → candidate said deploying models
```

The v1.2 prompt explicitly requires preservation of action strength and responsibility relationship without introducing a brittle deterministic verb-equivalence system.

## Real-local v1.2 tG9K result

The first real-local `tG9K` generation under v1.2 did not persist an artifact. It failed the existing post-generation scope guard with:

```text
Work Intelligence introduced unsupported lifecycle/scope intensifier(s): entire lifecycle
```

This is an integrity-safe failure: the guard rejected unsupported lifecycle amplification before persistence.

However, it exposed a product/runtime weakness. Instructor retries schema/Pydantic generation failures, but JobHunter's source-reference and semantic authority checks run after typed generation. A repairable wording violation therefore bubbled all the way to the user and required another manual command.

## Decision

Keep the authority validator strict, but add exactly one bounded service-level semantic repair attempt for model-generated Work Intelligence.

New flow:

```text
structured model generation
→ service reference + semantic validation
→ if valid: persist candidate
→ if service validation fails: one corrective regeneration with the exact validation error
→ validate fresh candidate again
→ if valid: persist
→ if still invalid: hard fail; persist nothing
```

This is not a relaxed acceptance path. The second candidate must pass the same validators as an initially valid candidate.

## Repair behavior

`WorkIntelligenceService._generate_with_semantic_repair(...)` now:

1. performs the normal typed generation;
2. runs complete accepted-work reference coverage and scope validation;
3. on one `WorkIntelligenceError`, appends a bounded semantic-repair instruction containing the exact rejection reason;
4. performs one fresh model generation;
5. runs the same service validators again;
6. persists only a valid final candidate;
7. preserves the first request/response plus the repair trigger in artifact audit metadata when the repair succeeds;
8. raises after the second invalid candidate rather than looping or weakening a validator.

The repair prompt explicitly says not to:

- weaken, guess, clamp, or omit source references;
- invent duties;
- strengthen action ownership;
- invent lifecycle scope;
- transfer unsupported source details.

## Regression coverage

Added:

```text
tests/test_work_intelligence_semantic_repair.py
```

The tests prove:

1. unsupported `entire lifecycle` in the first candidate triggers exactly one repair call;
2. the second prompt contains the exact validator failure;
3. a valid repaired candidate is returned;
4. both initial and final raw responses remain represented in audit metadata;
5. if the second candidate is also invalid, JobHunter fails after exactly two calls.

## Quality evidence

Final implementation/test head before this documentation commit:

```text
c73d6e3e43b494b93d8b85504d5e39aeb24162a8
```

GitHub CI on that exact head:

```text
Ruff                 PASS
full pytest           PASS
pytest -W error       PASS
```

Do not ask the repository owner to repeat these repository-level quality gates locally.

## Current artifact state

Historical candidates remain immutable:

```text
artifact 2  t4qV  v1.1
artifact 3  tmyX  v1.1
artifact 4  tG9K  v1.1
```

The failed v1.2 `tG9K` attempt created no artifact.

The prompt remains `job-work-intelligence-v1.2`; the bounded retry is runtime resilience, not a semantic contract change, so no prompt-version bump is required.

## Exact next action

On the owner's real local environment:

```bash
git pull --ff-only origin main
python -m jobhunter.work_intelligence_cli generate tG9K
```

Expected behavior:

- if the first generated candidate is valid, persist it directly;
- if it repeats a repairable service-level validation failure such as unsupported lifecycle wording, JobHunter should automatically issue one corrective regeneration internally;
- the user should see only the final successful Work Intelligence result, unless the corrective candidate also fails.

Review the final candidate for:

1. useful industrial-ML work grouping;
2. production wording that preserves `partner ... move toward production` rather than claiming deployment ownership;
3. no unsupported lifecycle/scope intensifier;
4. sensible primary/supporting emphasis;
5. material reduction of manual reading/synthesis effort.

## Stop line

Do not start P2.2B. P2.2A real-local semantic/product acceptance remains open.
