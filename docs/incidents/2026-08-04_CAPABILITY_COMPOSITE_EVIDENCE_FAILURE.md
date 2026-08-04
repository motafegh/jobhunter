# Capability Intelligence Composite Evidence Failure

**Date:** 2026-08-04  
**Status:** Fixed deterministically; local/live acceptance pending

## Symptom

After the JSON-Schema/grammar failure was fixed, Capability Intelligence reached the model and produced a substantive structured response, but Instructor/Pydantic rejected it.

The main repeated error was an `operational_context` evidence value such as:

```text
familiarity with the fundamentals of photography, videography, and editing,
familiarity with content production trends on Instagram, YouTube, and TikTok
```

Both clauses were genuine source facts, but they were **not contiguous in the source**. Other requirement text appeared between them. The model had concatenated two real source excerpts into one evidence string.

The first generation also had a similar Adobe evidence-bookkeeping issue. Instructor corrected that one on retry but repeated the operational-context composite quote.

## What this proved

The infrastructure/grammar failure was resolved: the model ran normally, generated reasoning, and Instructor validation executed.

The remaining failure was quotation bookkeeping, not absence of semantic reasoning.

This distinction matters:

```text
semantic statement
    may synthesize/infer

evidence[]
    must remain exact source anchors
```

The model should not be required to perform perfect source-span bookkeeping when JobHunter can prove a safe normalization itself.

## Rejected fixes

### Loosen evidence validation

Rejected. Allowing arbitrary paraphrased or reconstructed evidence would weaken auditability.

### Increase validation retries

Rejected. The retry already repeated the same composite-quote pattern. More retries would spend inference budget on deterministic formatting.

### Accept concatenated evidence as-is

Rejected. A concatenated quote is not an exact contiguous source excerpt and could later make evidence drill-down misleading.

## Implemented fix

Capability evidence canonicalization now has a bounded deterministic composite-recovery path.

When a model-provided evidence string is not itself an exact source excerpt, JobHunter may split it only when all of the following hold:

1. splitting occurs only at simple punctuation/newline separators;
2. every resulting fragment independently resolves to exact source text;
3. the smallest successful fragment count is used;
4. at most three fragments may be recovered from one model evidence item;
5. normal evidence-list bounds remain enforced;
6. any unsupported/paraphrased fragment causes validation failure.

Example:

```text
model evidence:
"Mastery of VPN and network infrastructure, Troubleshoot connectivity and security incidents"
```

when the source contains those as separate non-contiguous excerpts becomes:

```json
[
  "Mastery of VPN and network infrastructure",
  "Troubleshoot connectivity and security incidents"
]
```

JobHunter persists the actual exact source spans, not the model's reconstructed composite string.

## Important semantic issue observed in the same run

The model also placed an item under `unknown_scope` while labeling it:

```text
model_inferred_prerequisite
```

That contradicts the capability contract. This was not silently normalized in software. Once deterministic evidence normalization allows validation to proceed, Instructor should receive that focused semantic/section error and use its single bounded validation retry.

This preserves an important boundary:

- quote formatting and mechanically provable source-span recovery -> deterministic software;
- evidence-status/section meaning -> model correction and human quality review.

## Permanent lesson

Use the model where interpretation is valuable. Use deterministic code for exact bookkeeping whenever correctness can be mechanically proven.

Do not weaken evidence guarantees merely because a model combines genuine quotes inconveniently, and do not spend repeated model calls on transformations that deterministic software can perform safely.
