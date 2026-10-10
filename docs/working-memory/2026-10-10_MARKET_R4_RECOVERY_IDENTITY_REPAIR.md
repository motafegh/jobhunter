# Market R4 generation-identity repair

**Date:** 2026-10-10  
**Status:** REPAIR IMPLEMENTED / REAL R4 RE-RUN REQUIRED  
**Scope:** RoleFamilyIntelligenceReport R4 bounded real-local acceptance.

## Observation

The first real durable snapshot-15 report was persisted successfully as report artifact `#1` with:

```text
snapshot                         15
model                            gemma-4-e4b-it-ud
report contract                  market-role-family-intelligence-report-v1
candidate contract               market-role-family-candidate-v6
review state                     pending
available P1.6 claims            175
cited claims                     27
integrity rejections             0
reports / attempts / reviews     1 / 1 / 0
SQLite integrity                 ok
foreign-key violations           none
```

However, real audit evidence exposed an identity defect:

```text
persisted generation identity max_tokens = 2048
successful persisted LM request max_tokens = 8192
```

This is explained by the accepted LM Studio provider behavior: candidate generation starts at the prepared `max_tokens` value and, after an `InferenceTruncatedError`, retries with a four-times larger token budget up to the provider recovery ceiling. The successful request for artifact #1 was therefore the 8192-token recovery attempt.

The durable generation fingerprint recorded the initial token budget but did not record the truncation-recovery policy. That made the persisted generation identity incomplete for exact-reuse semantics.

Artifact #1 is immutable and remains `pending`; it is not eligible for R4 owner acceptance.

A second presentation defect was observed at the same time: the persisted candidate payload still used the pre-persistence wording `Ephemeral analytical candidate`, which is false once wrapped in an immutable durable report artifact.

## Repair

The durable report service now augments the candidate generation identity with the accepted provider recovery policy:

```text
max_tokens                        prepared initial budget
truncation_recovery_multiplier    4
max_recovery_tokens               32768
```

The model candidate input, prompt, schema, post-validation and V6 semantic generation path are unchanged. The extra fields describe the inference policy used by the durable wrapper so exact persisted reuse can distinguish pre-repair artifacts.

Because artifact #1 lacks those recovery-policy fields, its generation fingerprint cannot match the repaired durable identity. A normal post-repair generation request must therefore generate a new immutable artifact rather than reuse #1.

The durable wrapper also replaces only the application-authored authority note with:

> Bounded analytical candidate based on accepted P1.6 in this frozen snapshot. Not employer wording, a promoted taxonomy, or broad-market prevalence.

No model-authored interpretation text is changed by this normalization.

## Verification

Regression coverage now verifies:

- durable generation identity includes the recovery multiplier and ceiling;
- exact subsequent calls still reuse the repaired generation identity;
- durable authority wording no longer claims the persisted artifact is ephemeral;
- explicit regeneration semantics and append-only attempt/review behavior remain unchanged.

Git commits:

```text
5289d4cb  Record role-family recovery policy in generation identity
32f952a3  Cover durable role-family recovery identity
```

## R4 continuation

R4 remains open.

Required next real-local sequence:

1. pull the repair;
2. restart the JobHunter app on the repaired code;
3. use ordinary snapshot-15 generate/reuse (not explicit regenerate);
4. verify a new durable artifact is created because artifact #1 is not an exact repaired identity match;
5. confirm the new artifact records the recovery-policy fields in `generation_identity_json` and that its persisted successful request remains auditable;
6. perform restart/browser/CLI agreement checks on that new artifact;
7. only then perform owner review and final SQLite/public-corpus invariants.

Do not delete or mutate artifact #1. Its pending immutable history is evidence of the R4 repair discovery.
