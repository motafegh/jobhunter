# Capability Intelligence read-timeout incident

**Date:** 2026-08-04  
**Status:** Fixed on `main`

## Symptom

A live per-job Capability Intelligence run failed with:

```text
InferenceResponseError: Instructor could not produce a JobHunter-valid capability intelligence
artifact after 1 bounded validation retries: Request timed out.
```

LM Studio showed that generation had started successfully and continued for roughly 30 seconds at
about 90-100 tokens/second. The client then disconnected while the model was still generating.
There was no preceding grammar, schema, or evidence-validation failure.

## Root cause

`CapabilityInferenceProvider` still inherited the shared short-form inference policy:

```text
timeout_seconds = 30
OpenAI max_retries = configured network retries
```

Capability Intelligence can legitimately produce several thousand output tokens. A 30-second read
window is therefore too short for some real jobs even when the local model is healthy.

The OpenAI transport retry policy was also inappropriate for this workload. Replaying a complete
long-running generation after a read timeout wastes compute and latency and does not repair a slow
but otherwise valid generation.

## Fix

Capability Intelligence now uses the same long-form transport policy as Role Capability Blueprint:

```text
effective read timeout >= 120 seconds
connect timeout <= 10 seconds
transport-level automatic retries = 0
Instructor validation retries remain bounded separately
```

The configured shared timeout can still raise the effective read window above 120 seconds.

Instructor's retry remains useful only after a response completes but violates the typed JobHunter
capability contract. Network/read timeouts fail once and remain inspectable.

## Regression protection

Provider-level tests require that:

1. passing the shared 30-second timeout still produces a 120-second Capability Intelligence read
   timeout;
2. the OpenAI client receives `max_retries=0` even when general network retries are configured;
3. persisted request audit metadata records the effective timeout and transport retry policy.

## Permanent lesson

Do not assume every LM Studio request should share one timeout/retry policy merely because the same
endpoint/model is used.

Current inference classes differ materially:

```text
short structured extraction / translation
    -> comparatively short response budget

Capability Intelligence
    -> multi-thousand-token typed reasoning

Role Capability Blueprint
    -> multi-thousand-token human-facing expert synthesis
```

Timeouts and retries should match the expected generation shape. A slow but active local generation
is not equivalent to a failed network request.
