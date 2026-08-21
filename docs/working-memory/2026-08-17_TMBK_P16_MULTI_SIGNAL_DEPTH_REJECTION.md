# tmBK P1.6 Heterogeneous Validation Incident Record

Date: 2026-08-21  
Status: ACTIVE VALIDATION CASE / FIRST ARTIFACT REJECTED / DETERMINISTIC DEFECTS FIXED / CLEAN LOCAL REBUILD REQUIRED

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

The posting also contains soft/behavioral requirements and no genuine explicit responsibility section. That makes it a useful test of both concept-specific depth and qualification-vs-duty restraint.

A separate Python candidate, `tI1n`, was blocked before P1.6 because manual source-vs-English review found a material translation error. That case remains translation-quality evidence; downstream P1.6 must not compensate for bad upstream meaning.

## Incident 1 — `Sufficient knowledge` vocabulary gap

The first P1.6 run failed because `Sufficient knowledge` was not recognized as an accepted explicit employer depth signal even though the phrase was exact source evidence.

The narrow correction added `sufficient knowledge` to the v20 accepted depth vocabulary while keeping plain `knowledge` non-depth.

Regression coverage was added and CI passed.

## Incident 2 — first persisted artifact / multi-signal depth propagation

After the first correction, P1.6 completed and persisted local analysis artifact `38` with:

- responsibilities: `0`
- requirements: `17`
- translation dependency: `38`

Mechanical completion did not imply semantic acceptance.

Manual semantic review found a deterministic depth-inflation defect:

- DRF/FastAPI correctly persisted as `Mastery`;
- Linux incorrectly persisted as `Mastery` instead of `Familiarity`;
- SQL/NoSQL incorrectly persisted as `Mastery` instead of `Familiarity`;
- OOP/modular design incorrectly persisted as `Mastery` instead of `Sufficient knowledge`;
- Database locking/concurrency/transaction management incorrectly persisted as `Mastery` instead of `Familiarity`.

Artifact `38` was therefore **REJECTED** and must not feed Capability Intelligence.

### Root cause

The inherited depth validator did two separate operations:

1. correctly verified that the model-supplied `depth_signal` was an exact source-supported depth phrase;
2. then incorrectly returned the **first accepted depth marker found anywhere in the entire cited evidence segment**.

Because the dense segment begins with `Mastery`, later item-specific signals were overwritten to `Mastery` even when the model supplied exact `Familiarity` or `Sufficient knowledge` phrases.

This was deterministic validator canonicalization, not acceptable model variation.

### V20 correction

V20 now uses a multi-signal-safe depth rule:

- when the model supplies an exact source-grounded depth phrase, canonicalize the depth marker from that supplied phrase itself;
- never borrow another subject's depth marker from the same dense evidence block;
- if `depth_signal` is absent and the cited evidence contains multiple distinct explicit depth levels, fail closed and require an item-specific signal instead of guessing;
- retain the existing exact-evidence, obligation, optionality, ontology, and preferred-experience guards.

Regression coverage uses the exact tmBK-style multi-signal segment. CI run `911` passed Ruff, full pytest, and warnings-as-errors.

## Artifact 38 disposition / cleanup state

Rejected `tmBK` P1.6 artifact 38:

- mechanically generated: YES
- semantically accepted: NO
- published as accepted repository corpus state: NO
- Capability downstream created: NO
- may feed Capability: NO

Before the next rebuild attempt, the rejected artifact was already absent from the local analysis-artifact table. A narrow cleanup script therefore stopped on its `artifact 38 was not found` assertion rather than deleting anything else. This was not database corruption: a subsequent public-corpus export/verify/status returned the current English P1.6 count to the two accepted baseline artifacts.

The important current fact is that no rejected `tmBK` P1.6 artifact is eligible for reuse, and no Capability artifact depends on it.

## Incident 3 — `effectively use AI` is not technical depth

A later rebuild attempt produced a model requirement for AI-assisted software development with:

```text
depth_signal = "Ability to effectively use (AI) ..."
```

The phrase is source-grounded but is **not a technical proficiency level**. It describes application/manner: the candidate should effectively use AI to improve software-development quality and speed.

V20 now deterministically clears this exact non-depth signal only when:

- it is an exact source phrase;
- it matches the effective-application pattern;
- neither the signal nor the cited evidence contains a genuine accepted depth marker.

If genuine depth appears anywhere in the same evidence span, validation still fails closed rather than guessing which subject the depth belongs to.

Regression coverage was added. CI run `914` passed Ruff, full pytest, and warnings-as-errors.

The failed rebuild persisted no replacement P1.6 artifact.

## Incident 4 — redundant coverage exclusion bookkeeping

The same live generations also showed that the model could positively extract requirements from a coverage reference while simultaneously adding the exact same reference to `coverage_exclusions`.

That is contradictory bookkeeping, not semantic uncertainty.

V20 now removes only a coverage exclusion whose exact reference is already positively represented by a requirement in the same bounded partition. Genuine exclusions remain untouched.

Regression coverage was added. CI run `916` passed Ruff, full pytest, and warnings-as-errors.

## Current expected source semantics

The next accepted `tmBK` P1.6 artifact must preserve at minimum:

```text
Python/Django                         Mastery
DRF/FastAPI                           Mastery
Git                                   Familiarity
Linux                                 Familiarity
SQL/NoSQL                             Familiarity
OOP + modular design                  Sufficient knowledge
Database locking/concurrency/tx       Familiarity
AI usage for software development     no technical depth signal
```

It must also preserve source-grounded teamwork, learning aptitude, problem-solving, ownership/responsibility/follow-through, continuous-learning, and product-participation requirements without fabricating a duty section.

## Current exact next action

After synchronizing the local checkout to current `main`:

```bash
jobhunter jobs analyze tmBK
```

Then inspect the **complete persisted artifact** before any Capability call:

1. verify all requirements and source evidence;
2. verify all concept-specific depth values;
3. verify AI usage has `depth_signal=null`;
4. verify responsibilities remain empty unless genuine duty evidence appears;
5. verify soft/behavioral expectations remain requirements rather than duties;
6. verify coverage is complete and non-contradictory;
7. accept or reject P1.6 semantically.

Only after P1.6 acceptance:

```bash
jobhunter jobs capability tmBK
```

Then audit Capability v9 complete source coverage/provenance, grouping, deterministic source strength/depth/work, role-level separation, and absence of fabricated prerequisites, ownership, lifecycle, architecture, autonomy, or mandatory strength.

## Acceptance gate remains

`tmBK` is **not yet an accepted heterogeneous anchor**.

Do not run Capability until its rebuilt P1.6 artifact is manually reviewed and accepted.
