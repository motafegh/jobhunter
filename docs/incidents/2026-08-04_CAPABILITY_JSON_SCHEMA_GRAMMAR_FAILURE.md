# Capability Intelligence JSON-Schema Grammar Failure

**Date:** 2026-08-04  
**Status:** Root cause identified; deterministic fix implemented, live re-acceptance pending  
**Affected path:** Per-job Capability Intelligence through LM Studio + Instructor `Mode.JSON_SCHEMA`

## Symptom

A real Capability Intelligence request failed before model generation with:

```text
InferenceResponseError: Instructor could not produce a JobHunter-valid capability intelligence
artifact after 1 bounded validation retries: Error code: 400 ...
Failed to initialize samplers: failed to parse grammar
```

LM Studio's engine log contained:

```text
parse: error parsing grammar: number of repetitions exceeds sane defaults,
please reduce the number of repetitions
```

The generated grammar showed rules including:

```text
char{3,600}
char{3,1200}
char{8,1000}
char{12,1600}
char{20,2400}
```

The model did not begin semantic reasoning. This was a provider/grammar initialization failure, not a capability-quality failure.

## Root cause

`JobCapabilityIntelligence` used Pydantic `Field(min_length=..., max_length=...)` metadata on long prose strings. Instructor `Mode.JSON_SCHEMA` converted the Pydantic schema into the OpenAI-compatible structured-output request. LM Studio's GGUF structured-output engine then converted that JSON Schema into llama.cpp grammar repetitions.

The large prose bounds became large explicit grammar repetition ranges. llama.cpp rejected those ranges as exceeding its sane repetition limits before a generation slot could start.

This is a boundary-design error:

```text
application validation bound
!=
provider sampling grammar requirement
```

A 2400-character application ceiling is useful as a fail-closed persisted-artifact rule, but the inference engine does not need to encode that ceiling into token sampling grammar.

## Fix

Keep Instructor `Mode.JSON_SCHEMA` and the structured response shape, but move long text-length limits out of Pydantic `Field` JSON-Schema metadata and into runtime `field_validator` checks.

Provider-visible schema still contains:

- object structure;
- required fields;
- enums;
- bounded collection sizes;
- nested capability/expectation structure.

Runtime validation still enforces the original text bounds:

- capability expectation statement: 3–600;
- rationale: 3–1200;
- capability label: 2–160;
- capability summary: 12–1600;
- cross-capability statement: 8–1000;
- cross-capability rationale: 3–1200;
- role interpretation: 20–2400.

Instructor still receives Pydantic validation failures and may perform the existing single bounded re-ask. JobHunter still independently validates the returned object before persistence.

## Regression protection

`tests/test_capability_models.py` now asserts that `JobCapabilityIntelligence.model_json_schema()` contains no `minLength` or `maxLength` keys, while a separate test proves the prose bounds remain enforced by runtime validation.

This prevents a future refactor from accidentally reintroducing huge llama.cpp grammar repetitions while appearing to make the Pydantic model 'more declarative'.

## Rejected immediate alternatives

### Switch Capability Intelligence to unconstrained/free-form text

Rejected. It would unnecessarily give up useful schema-guided generation and make a small local model carry more formatting burden.

### Disable validation limits entirely

Rejected. Persisted capability artifacts still need bounded prose and predictable payload sizes.

### Increase LM Studio context length

Rejected. The failure occurs during grammar parser/sampler initialization, before normal generation. Context capacity does not address it.

### Retry the same request repeatedly

Rejected. The schema itself is invalid for the engine's grammar limits; retries cannot change that deterministic provider failure.

## Permanent lesson

When using local grammar-constrained structured output, distinguish:

```text
constraints needed to guide generation
from
constraints needed to validate application data
```

Do not automatically expose large application-level string bounds to provider JSON Schema. Keep provider grammar structurally useful and enforce high prose limits in deterministic application validation.