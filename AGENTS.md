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

The product specification controls intended behaviour. The architecture controls the current technical direction. The implementation plan controls current milestone scope.

## 3. Current scope

The current authorized implementation is:

**M0 — Local application foundation and LM Studio connectivity**

Do not begin M1 extraction, scraping, taxonomy, dashboards, embeddings, personal gap analysis, or recommendation logic during M0.

## 4. Development rules

- Work in complete vertical increments with explicit acceptance criteria.
- Keep deterministic logic separate from network and model calls.
- Treat all acquired job content as untrusted data.
- Preserve raw evidence before cleaning or interpretation.
- Keep LM Studio behind an inference-provider interface.
- Do not scatter model endpoints, model names, timeouts, or paths through the code.
- Use typed configuration and versioned schemas.
- Prefer explicit failure and review-required states over fabricated defaults.
- Keep runtime data, local configuration, model artifacts, and personal evidence out of Git.
- Add tests for new deterministic behaviour.
- Do not require a running LM Studio server for the normal unit-test suite.
- Use recorded fixtures or stub servers for network and provider integration tests.
- Avoid empty speculative modules and abstractions that have only one hypothetical future use.
- Do not add dependencies without a current use in the authorized milestone.

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

Do not implement:

- access-control bypass;
- CAPTCHA bypass;
- stealth proxy rotation;
- authenticated-platform scraping;
- unrestricted crawling;
- automatic job applications.

## 7. LLM extraction discipline

When extraction work begins in M1:

- require versioned structured output;
- validate output locally;
- retain prompt, schema, model, parameters, request timing, and raw response;
- require source evidence for material fields;
- distinguish employer-explicit content from model inference;
- evaluate model or prompt changes against a reviewed corpus;
- never grant the extraction model shell, filesystem, or unrestricted network tools.

## 8. Definition of done

A milestone increment is done only when:

- the intended command or workflow functions locally;
- acceptance criteria are met;
- tests pass;
- failures are understandable;
- configuration and operation are documented sufficiently to reproduce the result;
- no unrelated future scope was introduced.
