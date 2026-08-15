# Capability v9 Derived-Expectation Filtering Checkpoint

**Date:** 2026-08-15  
**Branch:** `main`  
**Status:** deterministic correction PASS; follow-up live run exposed inherited schema contradiction; superseded for current-state guidance by `2026-08-15_CAPABILITY_V9_LIVE_FAILURES_AND_DESIGN_PAUSE.md`

## Trigger

The first live Capability v9 candidate run on dense `tG9K` did not persist an artifact.

The staged architecture reached bounded profile reasoning. Generation 1 produced a model-owned
profile summary containing unsupported technical-depth language (`expertise`), which correctly
triggered the v9 hard semantic guardrail. The single bounded repair corrected the summary.

Generation 2 then had a neutral valid summary, but optional model-derived `depth_signals` still
contained obligation/necessity language such as `necessary`, `prerequisite`, `must`, and
`necessitates`. The v9 validator rejected the whole profile because any unsafe derived expectation
raised a profile-level validation error.

No `job-capability-intelligence-v9` artifact persisted.

## Diagnosis

The semantic authority boundary was correct but enforcement granularity was too coarse.

Two different outputs need different treatment:

1. **Profile/group summaries** define the capability grouping itself. Unsupported depth,
   obligation, ownership/lifecycle, autonomy, or architecture language there remains a hard
   validation failure and may use the one bounded model repair.
2. **Fine-grained derived expectations** are optional analytical additions above deterministic
   P1.6 truth. One overreaching optional inference should not invalidate an otherwise grounded
   capability profile.

Retrying an entire bounded profile because one optional inference says `necessary` creates the same
kind of avoidable whole-answer repair pressure that JobHunter has already removed from other
source-led stages.

## Correction

Capability v9 now validates every optional derived expectation independently after normal evidence
canonicalization.

For model-owned sections:

```text
depth_signals
work_activities
sub_capabilities
underlying_knowledge
operational_practices
operational_context
```

an item is retained only if it passes all applicable v9 semantic guardrails:

- no source-obligation/necessity restatement;
- no unsupported ownership/lifecycle/autonomy/architecture claim;
- no unsupported depth language outside `depth_signals`;
- no `model_inferred_prerequisite` grounded only in preferred/contextual source truth without an
  independent required basis.

Unsafe optional items are discarded individually rather than causing full-profile regeneration.
The profile receives a deterministic uncertainty note recording how many model-derived expectations
were discarded. Raw model responses remain available in artifact audit material if a later complete
run persists.

Profile/group summary inflation remains a hard failure.

This correction does **not** weaken deterministic P1.6 source truth, source-link coverage,
requirement strength, explicit depth, source work activities, role-level constraints, or final
whole-artifact reconciliation.

At the time of this correction, the intended v9 policy was that a profile could contribute no safe
model-derived expectations after filtering, relying on its neutral grouping plus JobHunter-owned
deterministic source facts rather than forcing unsupported extra reasoning.

## Regression coverage

Added/updated tests prove:

- profile summary ownership/scope inflation still fails hard;
- one unsafe derived expectation is discarded without failing the profile;
- preferred-only prerequisite inference is discarded without retrying the profile;
- an obligation-inflated derived depth item is discarded while a safe sibling depth item remains;
- existing v9 source-truth accounting and distinct persistence identity remain intact.

## Deterministic gate

```text
CI run 838
Ruff:               PASS
full pytest:        PASS
warnings-as-errors: PASS
```

## Follow-up live result — important correction to this checkpoint

A second dense v9 live run failed before persistence with:

```text
Capability profile reasoning must add derived reasoning or an explicit unknown boundary
```

Both generations returned a bounded profile with a summary and no derived expectations. The failure
comes from the inherited `CapabilityProfileReasoningV8` validator, which still requires at least one
derived item or explicit unknown-scope item.

Therefore the intended statement above — that a v9 profile may contribute no safe model-derived
expectations — was **not actually effective in the live runtime**. The filtering correction and its
unit tests did not remove the inherited non-empty-derived invariant.

This creates an unresolved design contradiction between v9's fail-closed semantic restraint and
v8's inherited requirement to always add derived reasoning or unknown scope.

No second-run v9 artifact persisted.

Implementation is now explicitly paused. Do not infer a new implementation from this file. The
current authoritative checkpoint for this issue is:

```text
docs/working-memory/2026-08-15_CAPABILITY_V9_LIVE_FAILURES_AND_DESIGN_PAUSE.md
```

The next action is design discussion, not another patch or live rerun.
