# Role Capability Blueprint read-timeout incident

**Date:** 2026-08-04  
**Status:** Fixed in provider runtime policy; local acceptance pending

## Symptom

A live Role Capability Blueprint operation failed with:

```text
InferenceResponseError: Instructor could not produce a structurally valid
Role Capability Blueprint after 1 bounded retries: Request timed out.
```

LM Studio logs showed the model was still actively generating at roughly 90–110 tokens/second when the client disconnected at about 30 seconds. The OpenAI client then automatically replayed the full request and that second long generation was also disconnected at about 30 seconds.

## Root cause

The first Blueprint implementation inherited the shared:

```text
inference_timeout_seconds = 30
inference_max_retries = 1
```

settings used by shorter inference operations.

That policy is inappropriate for a deliberately richer human-facing Blueprint that may legitimately generate several thousand tokens.

This was not:

- an LM Studio context-window problem;
- a JSON-Schema grammar problem;
- a Pydantic validation failure;
- evidence-grounding failure;
- proof that the model could not perform the expert-role reasoning.

The client stopped otherwise-progressing generation before it could finish.

## Evidence from the live run

The interrupted generation was already producing non-trivial expert interpretation, including examples such as:

- end-to-end RAG engineering;
- chunking and embedding decisions;
- HNSW/vector-index trade-offs;
- hybrid/re-ranked retrieval;
- latency and streaming behavior;
- async Python and caching as likely system concerns;
- data-governance/provenance implications;
- concrete likely work products;
- explicit boundaries around topics probably not required.

This indicates that the Role Blueprint contract itself is directionally closer to the intended human-facing analysis than the earlier evidence-oriented capability screen.

## Fix

`RoleBlueprintInferenceProvider` now applies a dedicated long-form runtime policy:

```text
minimum read timeout: 120 seconds
OpenAI transport retries: 0
Instructor structural retries: at most 1
```

A caller may still provide a timeout greater than 120 seconds. A shorter shared timeout cannot reduce the Blueprint read window below 120 seconds.

The connection phase remains separately bounded at up to 10 seconds.

## Why transport retry is disabled

A read timeout during a long local generation is different from a quick connection failure. Automatically replaying the complete request can:

- discard substantial already-generated work;
- immediately consume another long LM Studio generation slot;
- double latency/compute;
- still fail at the same timeout boundary.

Instructor retry remains useful for a **completed response** that violates the lightweight Blueprint structure. It should not be confused with transport replay.

## Regression coverage

Tests now assert that:

1. a supplied 30-second shared timeout becomes a 120-second Blueprint timeout;
2. the underlying OpenAI client receives `max_retries=0` for Blueprint generation;
3. the persisted request metadata records the effective timeout and transport-retry policy.

## Permanent lesson

Do not assume all LLM calls should share one timeout/retry policy.

Choose runtime behavior from the operation shape:

```text
short structured extraction
→ relatively short read budget; retries can sometimes be useful

long-form expert synthesis
→ longer read budget; avoid replaying an in-progress generation on read timeout
```

Do not solve long-form timeout failures by shrinking the Role Capability Blueprint into a short evidence report. The richer output is the intended product behavior; the runtime policy must accommodate it within bounded limits.
