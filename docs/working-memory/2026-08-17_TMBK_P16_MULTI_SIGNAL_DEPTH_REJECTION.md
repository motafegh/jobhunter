# tmBK P1.6 Multi-Signal Depth Rejection

Date: 2026-08-17
Status: REJECTED CANDIDATE / DETERMINISTIC DEFECT FIXED / LOCAL REBUILD REQUIRED

## Context

The heterogeneous live semantic gate selected `tmBK` (Python Developer, Hummers Group) as the first Python/software anchor.

Current upstream chain before P1.6:

- source job: `tmBK`
- parsed Jobinja detail version: `44`
- English projection artifact: `38`
- translation provider/schema: `lm-studio-translation-v2 / english-projection-v2`
- P1.6 contract: `job-analysis-english-v20 / job-analysis-v5`
- local analysis model: `gemma-4-e4b-it-ud`

The source contains one dense requirement segment with several different explicit depth levels:

- Mastery of Python/Django
- Mastery of DRF, FastAPI
- Familiarity with Git
- Familiarity with Linux operating system
- Familiarity with SQL and NoSQL databases
- Sufficient knowledge of Object-Oriented concepts, modular design
- Familiarity with Database Locking, Concurrency, and Transaction Management

## First live failure

The first P1.6 run failed because `Sufficient knowledge` was not recognized as an accepted explicit employer depth signal even though the phrase was exact source evidence.

The narrow correction added `sufficient knowledge` to the v20 accepted depth vocabulary while keeping plain `knowledge` non-depth.

Regression coverage was added and CI passed.

## Second live run

After the first correction, P1.6 completed and persisted local analysis artifact `38` with:

- responsibilities: `0`
- requirements: `17`
- translation dependency: `38`

Mechanical completion did not imply semantic acceptance.

Manual semantic review found a deterministic depth-inflation defect:

- DRF/FastAPI correctly persisted as `Mastery`
- Linux incorrectly persisted as `Mastery` instead of `Familiarity`
- SQL/NoSQL incorrectly persisted as `Mastery` instead of `Familiarity`
- OOP/modular design incorrectly persisted as `Mastery` instead of `Sufficient knowledge`
- Database locking/concurrency/transaction management incorrectly persisted as `Mastery` instead of `Familiarity`

Artifact `38` is therefore **REJECTED** and must not feed Capability Intelligence.

## Root cause

The inherited depth validator did two separate operations:

1. correctly verified that the model-supplied `depth_signal` was an exact source-supported depth phrase;
2. then incorrectly returned the **first accepted depth marker found anywhere in the entire cited evidence segment**.

Because the dense segment begins with `Mastery`, later item-specific signals were overwritten to `Mastery` even when the model had supplied exact `Familiarity` or `Sufficient knowledge` phrases.

This was deterministic validator canonicalization, not acceptable model variation.

## V20 correction

V20 now uses a multi-signal-safe depth rule:

- when the model supplies an exact source-grounded depth phrase, canonicalize the depth marker from that supplied phrase itself;
- never borrow another subject's depth marker from the same dense evidence block;
- if `depth_signal` is absent and the cited evidence contains multiple distinct explicit depth levels, fail closed and require an item-specific signal instead of guessing;
- retain the existing exact-evidence, obligation, optionality, ontology, and preferred-experience guards.

Implementation commits:

- `2a25b6fc1291c292a7e698e84d7b77c3775dc556` — v20 multi-signal depth canonicalization
- `815e199499d88ad161aff4eb3b66edd2af70f415` — exact tmBK-style regression coverage

CI run `911` passed Ruff, full pytest, and warnings-as-errors.

## Artifact disposition

`tmBK` analysis artifact `38`:

- mechanically generated: YES
- semantically accepted: NO
- published to repository corpus: NO
- Capability downstream created: NO
- may be reused: NO

The local artifact must be retired before rerunning because the analysis store intentionally reuses the same source/model/prompt/schema identity.

Retirement should be narrowly scoped to artifact `38`, assert that it belongs to `tmBK` detail `44` under v20/v5, assert that no Capability artifact depends on it, preserve a rejection reason in the analysis-attempt ledger, remove the rejected artifact, resynchronize the public corpus projection, and then rerun P1.6 under the corrected validator.

## Acceptance gate remains

Do not run Capability for `tmBK` until the rebuilt P1.6 artifact is manually reviewed and accepted.
