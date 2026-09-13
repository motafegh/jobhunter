# P2.2B-B1 ta9l local generation checkpoint

**Date:** 2026-09-13\
**Status:** ENGLISH PROJECTION REVIEWED / P1.6 GENERATION FAILED / B1 OPEN / NO PROMOTION\
**Repository baseline:** `d45313b` on `main`\
**Controlling plan:** `docs/P2_2B_SELECTIVE_RESPONSIBILITY_PROMOTION_PLAN.md`

## Outcome

The selected job now has English projection **40**, tied to source detail **25**.
English P1.6 generation attempt **98** failed after its one bounded validation
retry. It created no analysis artifact. There is consequently no whole artifact
to semantically accept or reject, and no eligible second accepted responsibility
for the final correspondence review.

B1 remains open. This checkpoint does not declare B1 PASS or NO-PROMOTION/DEFER,
reject the source job, disprove the proposed correspondence, or activate the
Market foundation investigation.

## Verified takeover baseline

The checkout fast-forwarded from `3fffafd` to `d45313b` (91 commits). Before local
generation, the working tree was clean and HEAD matched origin/main. Dependency
consistency and Ruff passed; the complete deterministic suite passed with warnings
as errors: **540 passed**. SQLite quick_check returned `ok`. Public-corpus
verification matched all 353 known jobs.

The five accepted/current P1.6 anchors remain 36, 37, 39, 44, and 46. The registry
still contains four concepts, one alias, and six claim decisions. The tentative
`responsibility:design-ai-evaluation-monitoring` concept is absent.

## Local runtime and translation

Doctor/model discovery found the configured models, but available-model listing
did not establish loaded-model readiness. Translation attempt **58** failed with
HTTP 400, `Model is unloaded.` No translation artifact was created by that attempt.

The configured translator `gemma-4-e2b-it` was explicitly loaded through the local
LM Studio model-load endpoint, with a 16,384-token context. The subsequent normal
translation command succeeded as attempt **59**, artifact **40**:

```text
provider:                 lm-studio-translation-v2
model:                    gemma-4-e2b-it
projection contract:      english-projection-v2
source detail:            25
source semantic SHA-256:  cd9dbf6be622113836b951e9042c87798954fc01dea520ba08b090eae2b54fc6
projection SHA-256:       840245708da621f072cd2f8e24b0fc60e384e55f6395819b8f4d98c737f078e2
translated/native:        11 / 5
```

Review covered all projected fields against the original source. The English job
description is native and exactly unchanged; a direct equality check passed. Its
five direct duties and six qualification sentences therefore retain exact source
wording. The experience range remains three to six years; education, military
service, employment, location, and skill tags retain their source meaning.
Awkward non-consequential translation wording such as salary `agreement` is not a
reason to regenerate or strengthen the source.

The normal CLI synchronized the local public projection: **353 jobs, 43 fetched
details, 21 current v2 English projections, 5 accepted English P1.6, 5 Capability**.
This is local projection state, not a new Git publication. The previously published
20-projection baseline remains historical publication evidence.

## P1.6 failure and bounded diagnosis

The configured analysis model `gemma-4-e4b-it-ud` was loaded with a 32,768-token
context. The unchanged normal command was:

```bash
.venv/bin/jobhunter jobs analyze ta9l --mode english
```

It used `job-analysis-english-v20 / job-analysis-v5`, translation 40, source 25,
and the existing bounded partition/validation protocol. Attempt **98** is stored
as `failed`, `InferenceResponseError`, with no artifact ID. The failure concerns
the residual qualification partition containing:

> Strong SQL and relational database expertise.

The first response placed `Expertise` in its normalized concept and was rejected
for depth-bearing concept wording. The bounded correction used the entire source
sentence as `depth_signal`; the validator rejected the two recognized depth
markers (`Strong` and `expertise`) in one signal.

Offline validation with the exact source evidence reproduced:

| Concept | Depth signal | Result |
| --- | --- | --- |
| Expertise with SQL and relational database | Strong | Rejected: depth-bearing concept |
| SQL and relational database | Entire source sentence | Rejected: multiple markers in one signal |
| SQL and relational database | Strong | Pass |
| SQL and relational database | expertise | Pass |

These are validator probes, not accepted employer interpretations or substituted
model output. They show that the existing contract can represent the source
qualification. They do not establish a deterministic integrity defect justifying
a frozen-contract change, nor prove complete extraction quality.

No prompt patch, validator weakening, model substitution, hand-assembled analysis,
additional extraction run, or broader job scan was performed. The configured
bounded retry is exhausted for this attempt. Raw failed-generation details remain
in local SQLite; they are not copied into the repository.

## Review and browser boundary

`jobs review-analysis ta9l status` reports:

```text
No current English P1.6 artifact matches the configured review contract
```

The local browser application was started on loopback port 8765. A GET of
`/jobs/ta9l` returned HTTP 200 and correctly rendered original source and derived
English separately, with `English v2 ready`, `English analysis missing`, and
`Not analyzed`. This verifies served page content, not visual layout acceptance.

Computer Use initialization failed before any window action because its runtime
rejected the WSL workspace URI (`sandboxCwd is not a local file URI`). No visual
browser review or registry browser acceptance is claimed.

## Next decision and stop lines

Resolve whether to continue a focused extraction-recovery investigation or to
explicitly close B1 as evidence-based NO-PROMOTION/DEFER. The latter would mean
accepted evidence was not obtained within this run; it would not mean the two
responsibilities are semantically incompatible.

Until that decision:

- retain projection 40 and failed attempt 98;
- do not repeat successful translation or the completed corpus selection;
- do not label generation failure as semantic rejection;
- do not create a concept/mapping or change accepted contracts to force B1 success;
- do not start the formal Market investigation while B1 remains open;
- keep all local model protocol, registry state, and SQLite out of publication.

No source code or tests changed. The existing quality result remains applicable;
this checkpoint does not require the owner to rerun it.

## Continuation decision

The owner authorized continued focused extraction recovery, progressive recording,
and Git publication of repository-safe work. B1 remains open. The next bounded
recovery examines correction feedback: the concept-depth error asks for an exact
source depth phrase without stating the already-enforced single-marker restriction.
A generic clarification may improve the existing retry without changing accepted
inputs, normalization, evidence, prompt/schema IDs, or retry limits. Verify that
the validation acceptance set is unchanged before one further normal local run.
Do not include vacancy names, technologies, or preferred answers in the feedback.
