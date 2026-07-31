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

P1.1 discovery and the bounded complete-job parser-v2 slice are accepted. Five structurally varied live Jobinja advertisements have complete local details and pass the deterministic structural audit.

The current authorized implementation and acceptance target is **P1.2 repeat-safe daily discovery**:

```text
enabled Jobinja searches
→ sequential rate-limited page acquisition
→ immutable search-page evidence
→ canonical job-ID extraction
→ empty-page and repeated-result-set stopping
→ cross-search identity deduplication
→ discovery provenance
→ per-search stop summaries
→ combined new, known, unique, overlap, and failure totals
```

The active discovery command is:

```text
jobhunter jobinja discover [--url <search-url> ...] [--pages <count>] [--show-jobs]
```

P1.2 rules:

- compare repeated pages by sorted stable Jobinja job IDs, never raw HTML;
- preserve each successfully acquired page before parsing or deciding to stop;
- delay only between actual requests;
- retain successful searches when another search fails;
- keep cross-search overlap separate from combined unique-job totals;
- report one explicit stop reason per search: `page_limit_reached`, `empty_page`, `repeated_result_set`, `page_failed`, or `invalid_search`;
- do not use advertisement age as a pagination stop condition;
- do not fetch job-detail pages or invoke LM Studio as part of discovery.

The already accepted detail inspection commands remain available:

```text
jobhunter jobs list
jobhunter jobinja fetch <job-id> [<job-id> ...]
jobhunter jobinja fetch --missing --limit <count>
jobhunter jobs audit [<job-id> ...]
jobhunter jobs audit --only-issues
jobhunter jobs show <job-id>
```

Detail batches must remain sequential, use the configured request delay, and contain at most 50 jobs. `--missing` may select only jobs with no existing local detail version. Do not introduce unrestricted crawling or automatic refresh of every known job.

The deterministic audit may flag structural extraction risks and report optional-field coverage, but it must not claim semantic correctness or employer intent. Missing optional fields alone are not parser failures.

No active increment may infer responsibilities, preferred versus required qualifications, personal relevance, skill gaps, or career recommendations. Those remain P1.6 and later work.

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
