# JobHunter Repository Instructions

These instructions apply to AI assistants and human contributors working in this repository.

## 1. Product priority

JobHunter is a real personal utility intended for repeated local use. It is not primarily a learning exercise.

When choosing between an impressive implementation and a smaller dependable implementation, prefer the dependable implementation.

## 2. Required reading order

Before making material changes, read:

1. `README.md`
2. `docs/PRODUCT_SPECIFICATION.md`
3. `docs/ARCHITECTURE.md`
4. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
5. `docs/SOURCE_POLICY.md`
6. `docs/IMPLEMENTATION_PLAN.md`
7. `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md` while Phase 1 is active

The product specification controls intended behaviour. The architecture controls the technical direction. The implementation plan controls product sequencing. The Phase 1 plan controls current Jobinja scope, order, and acceptance criteria.

## 3. Current scope

P1.1 and P1.2 are accepted. Repeat-safe discovery was validated live across two two-page Jobinja searches with 79 combined unique jobs, one cross-search overlap, and zero new jobs on the identical rerun.

A bounded parser-v2 slice spanning parts of P1.3 and P1.4 is also accepted against fifteen structurally varied live Jobinja advertisements. All fifteen latest semantic versions pass the deterministic local structural audit.

The current authorized implementation and acceptance target is the operational part of **P1.3 job-detail acquisition**:

```text
explicit, missing-only, or refresh-due bounded selection
→ sequential rate-limited detail requests
→ immutable raw HTML and metadata evidence
→ deterministic parser-v2 extraction
→ semantic new / unchanged decision
→ one fetch observation for every success or expected failure
→ inspectable check history
→ bounded refresh scheduling
```

The active commands are:

```text
jobhunter jobinja fetch <job-id> [<job-id> ...]
jobhunter jobinja fetch --missing --limit <count>
jobhunter jobinja fetch --refresh-due --older-than-hours <hours> --limit <count>
jobhunter jobs checks <job-id> [--limit <count>]
jobhunter jobs list
jobhunter jobs audit [<job-id> ...]
jobhunter jobs audit --only-issues
jobhunter jobs show <job-id>
```

P1.3 observation and refresh rules:

- keep semantic versions, raw snapshots, and fetch observations as distinct records;
- record every successful check even when semantic content is unchanged;
- record expected acquisition and evidence-write failures without deleting earlier evidence;
- allow at most 50 jobs per batch;
- perform requests sequentially using the configured delay;
- select `--missing` jobs only when no local detail version exists;
- select `--refresh-due` jobs only when a detail version exists and the latest known check is older than the requested threshold;
- use the semantic-version timestamp as a legacy fallback when no observation exists;
- never infer expiration or removal from a single failure or search disappearance;
- keep acquisition independent from LM Studio.

The deterministic audit may flag structural extraction risks and report optional-field coverage, but it must not claim semantic correctness or employer intent. Missing optional fields alone are not parser failures.

Challenge/login classification, retry-backoff refinement, expiration/removal decisions, repost classification, and duplicate-content classification remain incomplete. No active increment may infer responsibilities, preferred versus required qualifications, personal relevance, skill gaps, or career recommendations. Those remain P1.6 and later work.

Current work proceeds directly on `main` unless a later change creates a clear need for branch isolation.

## 4. Development rules

- Work in complete vertical increments with explicit acceptance criteria.
- Keep deterministic logic separate from network and model calls.
- Keep successful acquisition independent from LM Studio availability.
- Treat all acquired job content as untrusted data.
- Preserve raw evidence before cleaning or interpretation.
- Keep LM Studio behind an inference-provider interface.
- Do not scatter model endpoints, model names, timeouts, or paths through the code.
- Use typed configuration and versioned schemas.
- Prefer explicit failure and review-required states over fabricated defaults.
- Keep runtime data, local configuration, model artifacts, and personal evidence out of Git.
- Add tests for new deterministic behaviour.
- Do not require a running LM Studio server or public website for the normal unit-test suite.
- Use recorded fixtures or stub transports for network and provider integration tests.
- Avoid empty speculative modules and abstractions that have only one hypothetical future use.
- Do not add dependencies without a current use in the authorized increment.

## 5. Change discipline

A change should state:

- which milestone requirement it implements;
- which files were changed;
- what behaviour was added or corrected;
- what tests demonstrate it;
- what remains outside scope.

Update an existing controlling document when a material product or architecture decision changes. Do not create a new governance document for every small decision.

## 6. Source acquisition discipline

No recurring source adapter may be enabled without satisfying `docs/SOURCE_POLICY.md`.

For Jobinja Phase 1:

- use public search and job-detail pages only;
- use a descriptive user agent;
- default to sequential, rate-limited requests;
- validate final redirect hosts;
- impose bounded page and request limits;
- preserve source URLs and attribution;
- stop and report challenge, login, CAPTCHA, or access-denial responses.

Do not implement:

- access-control bypass;
- CAPTCHA bypass;
- stealth proxy rotation;
- authenticated-platform scraping;
- unrestricted crawling;
- automatic job applications.

## 7. LLM extraction discipline

When P1.6 begins:

- require versioned structured output;
- validate output locally;
- retain prompt, schema, model, parameters, request timing, and raw response;
- require source evidence for material fields;
- distinguish employer-explicit content from model inference;
- evaluate model or prompt changes against a reviewed corpus;
- never grant the extraction model shell, filesystem, or unrestricted network tools.

## 8. Definition of done

An increment is done only when:

- the intended command or workflow functions locally;
- acceptance criteria are met;
- tests pass;
- failures are understandable;
- configuration and operation are documented sufficiently to reproduce the result;
- no unrelated future scope was introduced.
