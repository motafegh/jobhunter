# JobHunter Review Snapshots

`review-snapshots/` contains deliberately exported, repository-safe JSON snapshots of selected public Jobinja jobs. These files are **not** the live SQLite database and are not runtime inputs.

A snapshot can make this dependency chain reviewable:

```text
public Jobinja source
→ English projection
→ English P1.6 factual analysis
→ Capability Intelligence
→ optional experimental Role Capability Blueprint
```

## Create / inspect / publish

```bash
jobhunter jobs snapshot <job-id>
git diff -- review-snapshots/jobs/<job-id>.json
```

The standalone compatibility entry point remains:

```bash
jobhunter-review-snapshot <job-id>
```

## Included

A snapshot may include current public source provenance, English projection, P1.6 analysis, dependency-current Capability/Blueprint artifacts, artifact/model/prompt/schema identities, dependency IDs, current-chain flags, and configured effective model roles.

Current snapshot schema:

```text
job-review-snapshot-v1
```

## Deliberately excluded

Snapshots do not export SQLite/WAL/SHM, raw HTML contents, raw LM Studio responses, model request bodies/system prompts, API tokens/secrets/local config, operation/debug histories, or future private/personal user data.

The repository is public. Commit selected review examples intentionally.

## Dependency status vs semantic acceptance

The `status` object records whether a downstream artifact belongs to the selected dependency chain:

```text
translation_matches_english_analysis
capability_is_current_chain
blueprint_is_current_chain
```

These are **dependency/currentness flags, not semantic-acceptance flags**.

A current-chain Blueprint can still be rejected after semantic review. This distinction is now demonstrated by the selected `tG9K` snapshot.

## Current `tG9K` review state

Configured model roles:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-12b-it-qat   # experimental only
```

Accepted bounded chain:

```text
English projection artifact 33
→ English P1.6 artifact 29
→ Capability v7/v4 artifact 9
```

P1.6 artifact 29 and Capability artifact 9 are accepted bounded anchors pending heterogeneous confirmation.

The currently committed snapshot also contains:

```text
Blueprint artifact 7
role-capability-blueprint-v6
schema role-capability-blueprint-v5
model gemma-4-12b-it-qat
```

Artifact 7 passed the v6 mechanical audit and CI, but **failed complete B4 semantic acceptance**. It remains intentionally committed as the best bounded experimental Blueprint evidence, not an accepted decision layer.

Failure examples included assumption-bearing unknowns/considerations around automated APC/SPC feedback loops, cloud/on-prem model hosting, `raw sensor physics`, and strict versioning/quality-standard implementation expectations not established by the vacancy.

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

## Current semantic review workflow

The active Phase-1 semantic gate is now heterogeneous review of:

```text
source
→ English projection
→ P1.6
→ Capability v7
```

Blueprint may be present in a snapshot as non-gating research evidence, but it is not part of Phase-1 semantic acceptance.

For each selected role, inspect:

- source/English provenance;
- P1.6 factual coverage, strength, optionality, explicit depth and evidence;
- Capability requirement/responsibility coverage;
- Capability grouping coherence;
- role-level source partition;
- deterministic source truth;
- absence of unsupported ownership/autonomy or contextual-tool promotion.

Target materially different roles, including `t4jp`, `tG9K`, Python/software, network/security, and operations/platform roles where available.

## Blueprint audit remains available for research

If intentionally generating an experimental v6 Blueprint:

```bash
jobhunter jobs blueprint <job-id>
jobhunter jobs snapshot <job-id>
python scripts/audit_blueprint_v6_snapshot.py review-snapshots/jobs/<job-id>.json --job-id <job-id>
```

The audit checks mechanical provenance/shape only. A PASS never means semantic acceptance.

Do not create Blueprint v7, weaken validators, add vacancy-specific prompt patches, or continue nearby model shopping during Phase 1 merely to obtain a passing artifact.

## Publishing selected snapshots

Before committing a selected review snapshot:

```bash
git diff --check
git status --short
git diff -- review-snapshots/jobs/<job-id>.json
```

Commit only deliberately selected public review evidence. Do not automatically snapshot/commit the whole corpus.
