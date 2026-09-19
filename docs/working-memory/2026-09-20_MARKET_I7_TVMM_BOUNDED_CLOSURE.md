# Market I7 — tvMm bounded closure follow-up

**Date:** 2026-09-20 (Asia/Tehran; execution timestamps are UTC)  
**Status:** EXECUTED / HOLD  
**Baseline:** `6fc2a85110` on `main`

## Executed boundary

Fetched all remote branches with pruning and fast-forwarded the clean checkout from
`8c7fdb0` to `6fc2a85`. The latest handoff selected `tvMm`; operational inspection
confirmed no current English P1.6 candidate. Source detail 47 and English projection
41 were inspected against the public source/projection evidence.

After SQLite backup and clean integrity/foreign-key checks, executed exactly one
supported `jobs analyze tvMm` command with the existing configured model and v20/v5
contract. No acquisition, translation, model switch, or additional generation was run.
The normal runtime's bounded validation retry is part of this one command.

## Result

Attempt 106 failed with `InferenceResponseError`; no analysis artifact was persisted
or accepted. Final validation reported:

- a requirement retained familiarity depth wording in its concept instead of the
  required separate depth field;
- two model-authored requirements cited `field:skills:0` and `field:skills:1`, which
  were absent from the model-facing evidence catalog.

The latter exposed a concrete instruction/payload contradiction: v20 materializes
structured skill tags deterministically and removes them from model fields, but its
inherited v18 prompt still says those tags remain model-visible and require model
classification. The payload also lists their deterministic references. This does not
justify accepting invented references or relaxing evidence validation.

The former remains a model semantic-normalization failure. Fixing the instruction
contradiction alone cannot establish semantic acceptance or I7 PASS.

## Verification

- Full deterministic suite: **638 passed with warnings-as-errors**.
- Ruff and dependency consistency: passed.
- Pulled-head GitHub CI: run `35462865219`, success.
- Post-generation SQLite integrity: `ok`; foreign-key violations: none.
- Every Market table exactly matches the pre-generation backup, including historical
  snapshots, members, and profiles.
- Public corpus unchanged: 394 jobs, 27 English projections, 5 accepted English P1.6,
  and 5 Capability artifacts. Market-table/local-path privacy scan found no matches.
- Raw provider error/completion evidence and SQLite backup remain ignored local data.

## Bounded next work

Repair the general v20 structured-skill instruction/payload ownership contradiction
and protect it with an offline provider-boundary regression. Preserve historical
prompts, deterministic skill facts, and strict evidence/depth validation. Do not
rerun the selected case repeatedly or select another vacancy to manufacture PASS.

I7 remains HOLD: no accepted-semantic core artifact or new semantic snapshot/profile
was created, and live accepted-semantic CLI/browser drill-down remains unexercised.

## Completed bounded repair

The v20 prompt now replaces the inherited model-owned structured-skill instruction
with its actual deterministic ownership rule. Historical v18/v19 prompt values remain
unchanged. Deterministic requirement references remain in local request runtime
metadata but are omitted from model-facing input; they are not valid model evidence.

An offline provider-boundary regression exercises real v20 partition preparation and
merge validation with a stubbed inference call. It verifies that description
requirements remain extractable, exact structured skill facts are injected once,
deterministic IDs remain in runtime metadata, and invented skill references still
fail evidence validation. This is a general ownership correction, not a vacancy
rule, semantic validator change, or acceptance claim.

No second live generation was performed. The remaining depth-normalization failure
was not relaxed or treated as fixed. Before another live attempt, define a bounded
post-repair evaluation decision; do not blindly repeat the previous next command.

Repair validation: **639 tests passed normally and 639 with warnings-as-errors**;
Ruff passed. This establishes deterministic repair coverage, not post-repair
real-model accuracy or accepted-semantic product completion.

Published execution record: `4fe74d4`. Published repair: `94a14a1`.
GitHub CI run `35468478422` passed all gates on the repair, including installed
entrypoints, Ruff, normal tests and strict-warning tests. Public-corpus verification
also passed against all 394 known jobs. Current routing documents preserve HOLD and
the unexecuted post-repair real-model boundary.
