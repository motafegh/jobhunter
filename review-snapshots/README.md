# JobHunter Review Snapshots

`review-snapshots/` contains deliberately selected, repository-safe JSON snapshots used for semantic review and acceptance evidence.

These files are **not** the live SQLite database, are **not** runtime inputs, and are **not** the complete public job dataset.

The complete version-controlled public dataset now lives in:

```text
corpus/
```

Difference:

```text
corpus/
→ every known public Jobinja job
→ current repository-safe source/translation/P1.6/Capability projection
→ routine remote dataset

review-snapshots/
→ selected jobs only
→ explicit semantic review/acceptance evidence
→ deliberately curated regression/decision anchors
```

## Create / inspect a review snapshot

```bash
jobhunter jobs snapshot <job-id>
git diff -- review-snapshots/jobs/<job-id>.json
```

The compatibility entry point remains:

```bash
jobhunter-review-snapshot <job-id>
```

Current snapshot schema:

```text
job-review-snapshot-v1
```

## Included

A snapshot may include:

- current public source provenance and parsed fields;
- English projection;
- current English/original P1.6 artifacts;
- dependency-current Capability artifact;
- optional experimental Blueprint artifact when it belongs to the selected dependency chain;
- artifact/model/prompt/schema identities;
- dependency IDs;
- configured effective model roles;
- current-chain flags.

## Deliberately excluded

Snapshots do not export:

- SQLite/WAL/SHM;
- raw HTML contents;
- raw LM Studio responses;
- model request bodies/system prompts;
- API tokens/secrets/local config;
- operation/debug histories;
- future private/personal user state.

The repository is public. Commit selected review examples intentionally.

## Dependency status vs semantic acceptance

The `status` object records whether a downstream artifact belongs to the selected dependency chain:

```text
translation_matches_english_analysis
capability_is_current_chain
blueprint_is_current_chain
```

These are **dependency/currentness flags, not semantic-acceptance flags**.

A current-chain artifact can still fail semantic review. Conversely, a historical artifact can remain useful experimental evidence without being current.

## Current accepted Capability anchors

Current public semantic contracts:

```text
English P1.6: job-analysis-english-v20 / job-analysis-v5
Capability:   job-capability-intelligence-v9 / job-capability-intelligence-v5
```

Accepted/current opposite-end anchors:

```text
tG9K
English P1.6 artifact 36
→ Capability artifact 11

t4jp
English P1.6 artifact 37
→ Capability artifact 12
```

Operational verification proved:

```text
tG9K capability_is_current_chain=True
Capability artifact=11
analysis artifact=36
blueprint_is_current_chain=False

t4jp capability_is_current_chain=True
Capability artifact=12
analysis artifact=37
blueprint_is_current_chain=False
```

Blueprint v6 remains deferred/non-authoritative and pinned to historical Capability v7 dependency semantics. It is not an accepted Phase-1 decision layer.

## Current semantic review workflow

Before heterogeneous live review, the full public corpus is being backfilled/published through `corpus/` so representative jobs can be selected remotely rather than depending on local SQLite access.

After corpus publication, review materially different current roles:

```text
Python/software
network/security
operations/platform/DevOps
```

For each selected role inspect:

- original source and English provenance;
- P1.6 factual coverage, strength, optionality, explicit depth and evidence;
- Capability requirement/responsibility coverage;
- Capability grouping coherence;
- role-level source partition;
- deterministic source truth;
- absence of unsupported ownership/autonomy/lifecycle/architecture or contextual-tool promotion.

Repeatable deterministic defects become fixtures. Harmless non-authoritative wording variation does not justify reopening accepted contracts.

## Blueprint audit remains available for research

If intentionally inspecting the experimental v6 Blueprint:

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

Commit only deliberately selected public review evidence. The complete routine public dataset belongs in `corpus/`, not here.
