# Market R4 generation-identity repair

**Date:** 2026-10-10  
**Status:** REPAIR ACCEPTED / R4 RE-RUN PASSED / CLOSED  
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

Artifact #1 is immutable and remains `pending`; it is not the accepted R4 artifact.

A second presentation defect was observed at the same time: the persisted candidate payload still used the pre-persistence wording `Ephemeral analytical candidate`, which is false once wrapped in an immutable durable report artifact.

## Repair

The durable report service augments the candidate generation identity with the accepted provider recovery policy:

```text
max_tokens                        prepared initial budget
truncation_recovery_multiplier    4
max_recovery_tokens               32768
```

The model candidate input, prompt, schema, post-validation and V6 semantic generation path are unchanged. The extra fields describe the inference policy used by the durable wrapper so exact persisted reuse can distinguish pre-repair artifacts.

Because artifact #1 lacks those recovery-policy fields, its generation fingerprint cannot match the repaired durable identity. A normal post-repair generation request therefore generated a new immutable artifact rather than reusing #1.

The durable wrapper also replaces only the application-authored authority note with:

> Bounded analytical candidate based on accepted P1.6 in this frozen snapshot. Not employer wording, a promoted taxonomy, or broad-market prevalence.

No model-authored interpretation text is changed by this normalization.

## Verification

Regression coverage verifies:

- durable generation identity includes the recovery multiplier and ceiling;
- exact subsequent calls reuse the repaired generation identity;
- durable authority wording no longer claims the persisted artifact is ephemeral;
- explicit regeneration semantics and append-only attempt/review behavior remain unchanged.

Git commits:

```text
5289d4cb  Record role-family recovery policy in generation identity
32f952a3  Cover durable role-family recovery identity
09d1249c  Record R4 generation identity repair
```

CI `38068073900` passed:

```text
Ruff                     PASS
pytest                   830 passed
pytest -W error          830 passed
```

## Real-local repaired result

The repaired ordinary generate/reuse path persisted artifact `#2` because artifact #1 was no longer an exact identity match.

Artifact #2 recorded:

```text
snapshot                           15
model                              gemma-4-e4b-it-ud
initial max_tokens                 2048
truncation recovery multiplier        4
max recovery tokens               32768
successful request max_tokens      8192
available P1.6 claims              175
cited claims                        27
work clusters                        4
multi-posting subfamilies            1
singleton specialties/outliers       2
integrity rejections                  0
review state                       accepted_for_bounded_use
```

Exact post-repair reuse then produced:

```text
(1, completed, artifact 1)
(2, completed, artifact 2)
(3, reused,    artifact 2)
reports = 2
```

No artifact #3 was created.

Final SQLite integrity was `ok`, foreign-key violations were empty, snapshot 15 remained ten members / six accepted-semantic members, and the pre-existing local corpus file hashes remained byte-identical to the pre-R4 baseline.

## Closure

The repair is accepted and R4 passed.

Artifact #1 remains immutable/pending historical evidence. Artifact #2 is the reviewed accepted R4 artifact.

Final R4 decision:

`docs/working-memory/2026-10-10_MARKET_R4_FINAL_LOCAL_ACCEPTANCE.md`

Do not repeat generation merely to replace artifact #1 or obtain preferred wording. The persistence program is closed; the project returns to Phase-2 semantic direction reconciliation.
