# JobHunter Review Snapshots

`review-snapshots/` contains deliberately selected, repository-safe JSON snapshots used for semantic review and acceptance evidence.

These files are **not** the live SQLite database, are **not** runtime inputs, and are **not** the complete public job dataset.

The complete version-controlled public dataset lives in:

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

Compatibility entry point:

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
- optional experimental Blueprint artifact when it belongs to the selected historical-compatible dependency chain;
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

The `status` object records whether a downstream artifact belongs to the selected dependency chain, for example:

```text
translation_matches_english_analysis
capability_is_current_chain
blueprint_is_current_chain
```

These are **dependency/currentness flags, not semantic-acceptance flags**.

A current-chain artifact can still fail semantic review. Conversely, a historical artifact can remain useful experimental evidence without being current.

This distinction is active in heterogeneous validation: `tmBK`'s first P1.6 candidate mechanically completed but was semantically rejected, so it is not eligible to feed Capability.

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

Blueprint v6 remains deferred/non-authoritative and pinned to historical Capability v7 dependency semantics. It is not an accepted Phase-1 decision layer and must not be silently rebased onto current Capability v9.

## Public corpus gate — closed

The complete public corpus has already been backfilled from the real local database, deterministically verified, intentionally committed/pushed, and remotely inspected.

Accepted publication baseline:

```text
Known/discovered jobs:       344
Fetched/parsed job details:   43
English projections:          33
English P1.6:                  2
Original P1.6:                 0
Capabilities:                  2
```

Important interpretation:

```text
344 known/discovered jobs != 344 complete advertisements
```

The remote corpus can now be used to select heterogeneous roles without direct local SQLite access.

## Current semantic review workflow

Active order:

```text
1. Python/software          ← tmBK active
2. network/security
3. operations/platform/DevOps
```

For each selected role:

1. inspect original source and English projection quality;
2. run/reuse current English P1.6;
3. manually accept P1.6 before Capability;
4. run/reuse current Capability v9 only after accepted P1.6;
5. inspect P1.6 factual coverage, strength, optionality, explicit depth and evidence;
6. inspect Capability complete requirement/responsibility coverage and provenance;
7. inspect grouping coherence and role-level source partition;
8. verify deterministic source truth and absence of unsupported ownership/autonomy/lifecycle/architecture or contextual-tool promotion;
9. distinguish deterministic defects from model limitations or harmless non-authoritative variation;
10. convert repeatable deterministic defects into fixtures.

Current Python/software case:

```text
tmBK
source detail 44
English projection 38
P1.6 rebuild/review required
Capability must not run until P1.6 acceptance
```

Repeatable deterministic defects become fixtures. Harmless non-authoritative wording variation does not justify reopening accepted contracts.

## Blueprint audit remains available for research

If intentionally inspecting the experimental v6 Blueprint:

```bash
jobhunter jobs blueprint <job-id>
jobhunter jobs snapshot <job-id>
python scripts/audit_blueprint_v6_snapshot.py review-snapshots/jobs/<job-id>.json --job-id <job-id>
```

The audit checks mechanical provenance/shape only. A PASS never means semantic acceptance.

Do not create Blueprint v7, weaken validators, add vacancy-specific prompt patches, rebase v6 onto Capability v9, or continue nearby model shopping during Phase 1 merely to obtain a passing artifact.

## Publishing selected snapshots

Before committing a selected review snapshot:

```bash
git diff --check
git status --short
git diff -- review-snapshots/jobs/<job-id>.json
```

Commit only deliberately selected public review evidence. The complete routine public dataset belongs in `corpus/`, not here.
