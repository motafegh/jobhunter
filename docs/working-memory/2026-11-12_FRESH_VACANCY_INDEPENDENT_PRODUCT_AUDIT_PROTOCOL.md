# JobHunter real-vacancy adversarial audit — protocol and limits

**Date:** 2026-11-12
**Status:** In execution; neither product-level general reliability nor fresh-market coverage is implied
**Branch:** `evaluation/fresh-job-ads-blind-2026-11-12`
**Accepted code baseline:** `main` commit `2de22a877772cf4a40154d8118a35ad19d1af8b7`
**Purpose:** Measure JobHunter's real behavior against independent human-style reading of real vacancy source evidence, before further development.

## Stage A — Attempt current acquisition without bypass

The supported Jobinja adapter was run in a *new isolated empty SQLite database* with a strict budget of three requests, one page each, using Persian AI, RAG, and Python searches. Every request returned HTTP 403. The adapter correctly stopped and discovered no jobs. This is an actual reproducible upstream availability blocker and source-coverage limitation. No browser impersonation, cookies, proxy rotation, challenge bypass or repeat-request escalation is allowed.

**No currently live November Jobinja postings have been ingested.** Do not mislabel this outcome as successful fresh acquisition.

## Stage B — Evaluate unprocessed, previously captured vacancies instead

A separate, isolated online SQLite copy of the existing local JobHunter database is used to run the accepted native translation/analysis commands on four parsed Jobinja vacancies that had **zero prior P1.6 analysis artifacts**. Their immutable original HTML was acquired on 2026-08-01 or 2026-09-29, before this test:

| Job ID | Source category indicated by publicly visible title/URL | Original evidence date |
| --- | --- | --- |
| `tNpG` | LLM/RAG software in health context | 2026-09-29 |
| `t4Ay` | Senior AI / LLM / RAG / agents | 2026-08-01 |
| `ta9l` | Senior applied AI engineer | 2026-08-01 |
| `t4wP` | Security engineer | 2026-08-01 |

The original immutable HTML hashes were verified against the stored acquisition ledger before running any derived processing. Full original pages, model inputs/outputs and job-specific files remain local under ignored `data/local-acceptance/`. Never commit real candidate records, ad text or other private files by a blanket `git add`.

**Scope note:** This is a *new analysis of older preserved real vacancies*, not a November live-ad cohort. Original ad URLs may now be unavailable. We will attempt to open their URL directly before independent review, but a denied URL cannot be worked around; the preserved original HTML is the auditable fallback and is not proof that the job is still open.

## Stage C — Freeze JobHunter's native result before independent reading

Run the project's configured, supported CLI against only the isolated SQLite copy:
1. Translation to English via the configured local LM Studio model, preserving provider identity and failure states.
2. Accepted P1.6 English analysis candidate generation for each successfully translated job, **without auto-accepting**.
3. Save per-job CLI status, immutable analysis artifact IDs, source linkage, model/prompt/schema identities, acceptance state, full local candidate snapshots and local hashes.
4. Run optional Capability/Work only if their existing accepted prerequisites are independently reviewed and fulfilled, recording any stop as a legitimate boundary.

The evaluator must *not* inspect or use substantive model-generated findings during this stage (only process state, counts, errors and checksums). Lock the input/job cohort before evaluating.

## Stage D — Independent source assessment

The evaluator reads each original public ad at the URL when accessible, otherwise the previously preserved original HTML directly (not the derived P1.6/English projections). Record a new independent checklist for each job, **before** examining any JobHunter semantic output:
- explicitly stated technical qualifications and requirement strength/alternatives;
- directly described work/responsibilities versus implied work;
- seniority/experience and explicit depth, technology stack and operational context;
- important source ambiguity or information not provided;
- original-source identifier, hash, original capture date and evidence-access path.
- Refrain from adding unstated generic skill requirements.

Freeze/hash the independent checklist before opening model-derived results. Independent source extraction from the same HTML is not a fully blinded third-party judgment, but this procedure prevents model-output anchoring.

## Stage E — Compare, classify, decide

Compare preserved JobHunter outputs to the independently locked source checklist. For every mismatch record source paragraph or field, P1.6 claim/reference when available, and one of:
- **unsupported/invented fact**
- **missed explicit source fact**
- **requirement strength/alternatives error**
- **qualification promoted into direct duty**
- **technical depth or lifecycle/ownership overstatement**
- **translation/parse distortion**
- **missing currentness/source linkage**
- **correctly unknown / safely withheld**
- **inconclusive because source inaccessible**

Separate acquisition/translation/analysis stage reliability from semantic fidelity. Judge no claim as accepted without an explicit review decision. Record actionable fixes and decide which one is highest impact for the next capability intelligence increment.

**Success criteria:** safe source boundaries, inspectable provenance, at least three independently checkable candidate records if available, and decision-driving concrete mismatch evidence. Failure and stop are reportable, not reasons to fabricate a complete pipeline.

**Stop lines:** no external-source bypass, no ad text published, no inferred job availability, no silent backfilling of new data, no production database changes, and no Model output treated as accepted before review.
