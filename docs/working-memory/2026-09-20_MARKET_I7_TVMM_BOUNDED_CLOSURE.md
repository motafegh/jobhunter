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

## Bounded post-repair evaluation decision

The owner's continuation authorizes one post-repair `jobs analyze tvMm` command
against the unchanged source 47 / projection 41 and existing configured model and
v20/v5 contract. The only changed inference inputs are the published general
structured-skill ownership correction. Existing runtime validation bounds remain.

Evaluate two separate questions: whether absent structured-skill citations recur,
and whether the complete result is valid enough for semantic review. A candidate
must still pass source coverage, optionality, depth and qualification/duty review.
A failed attempt ends this evaluation without another generation or vacancy switch.
No acquisition, translation, model change, validator relaxation or automatic
acceptance is included. Back up SQLite first; verify historical state, integrity
and public-corpus privacy afterward.

## Post-repair result and semantic review

Attempt 107 completed and created pending artifact 49 with 10 responsibilities,
15 requirements and no role-purpose claim. The absent structured-skill citation
failure did not recur in this one case. Exact `Ai` and `Engineer` tags were injected
by the application. This is bounded repair evidence, not general model accuracy.

Complete source/projection/artifact review rejected artifact 49:

1. Seven experience requirements incorrectly acquired `familiarity` depth:
   LLM/API experience, Agent/workflow building, production Agents, Multi-Agent work,
   real database/API integration, Docker/cloud experience, and AI product building.
   The raw model response had null depth for all of them. Deterministic validation
   inserted the first neighboring marker because all markers in each broad evidence
   span had the same spelling. Repeated identical markers do not establish one
   shared subject or scope.
2. Requirement 12 turns the intended AI system's task execution/accounting-system
   interaction into a required candidate skill. The source subject is the AI system;
   the candidate's separate requirement is to build a reliable product Agent.

The 10 responsibility statements are supported by the explicit duty passage;
preferred experience remained preferred. These positive findings do not offset the
material requirement/depth defects or establish complete requirement coverage.

Rejection used the supported review command. Artifact 49 is archived as rejection 8
and excluded from current reuse/export. Its raw response and persisted payload were
also retained locally for diagnosis. No accepted semantic artifact, membership,
snapshot or profile was created. Every Market table matches the pre-evaluation
backup; SQLite integrity is `ok` and foreign-key checks are empty. The public corpus
remains unchanged at 5 accepted English P1.6 artifacts.

### Next bounded repair

The repeated-identical-marker case belongs to v20 deterministic depth validation.
Reject ambiguous automatic depth filling when multiple source markers occur, even
when their spelling is identical. Preserve explicit model-supplied item-specific
depth handling and historical validators. Cover the failure with offline regressions
and replay the retained raw artifact without model calls. This does not resolve the
separate semantic subject error. No further live generation belongs to this evaluation.

## Deterministic depth repair and current stop line

V20 no longer auto-fills null depth from an evidence span containing multiple
depth markers, even when every marker uses the same word. The model must supply
a source-exact item-specific phrase for an explicit depth claim. Historical v19
and earlier validators are untouched. A focused regression covers repeated-marker
rejection and preservation of a supplied scoped phrase.

Read-only replay of artifact 49's retained raw model response found that all 12
model-authored requirements cited broad spans with repeated markers while carrying
null depth; all now fail before borrowing depth. This is fail-closed diagnostic
evidence, not proof the model can generate a valid replacement. Read-only checks
over the five accepted public anchors found no new validation failures. One
historical `more than six years` result retains its existing separate lower-bound
preservation behavior.

Artifact 49 remains rejected. Its separate subject-attribution error is not fixed
by this depth change. I7 remains HOLD with no accepted-semantic core posting.
Further model attempts or a different vacancy require a new bounded evidence
decision; this closure work stops at the reviewed rejection and deterministic repair.

Repair gate: **640 passed with warnings-as-errors**, Ruff and dependency checks
passed, and public-corpus verification passed for all 394 known jobs. Post-mutation
SQLite integrity and foreign-key checks passed; every Market table still matches
the pre-evaluation backup, and the corpus privacy scan found no Market or local
host/path leakage. These checks do not change the I7 HOLD decision.
