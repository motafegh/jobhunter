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

These remain **dependency/currentness flags, not semantic-acceptance flags**. Snapshot v1 now additionally includes `english_analysis_semantic_review` and the analysis review status/time/note as a separate explicit decision record.

A current-chain artifact can still fail semantic review. Conversely, a historical artifact can remain useful experimental evidence without being current.

This distinction is active in heterogeneous validation: rejected candidates for `tmBK`, `t4qV`, and `tmyX` never became eligible for Capability; only explicitly accepted artifacts 39, 44, and 46 fed artifacts 13, 14, and 15.

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

tmBK heterogeneous Python/software
English P1.6 artifact 39
→ Capability artifact 13

t4qV heterogeneous network/security
English P1.6 artifact 44
→ Capability artifact 14

tmyX heterogeneous operations/platform
English P1.6 artifact 46
→ Capability artifact 15
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

tmBK capability_is_current_chain=True
Capability artifact=13
analysis artifact=39
english_analysis_semantic_review=accepted
blueprint_is_current_chain=False

t4qV capability_is_current_chain=True
Capability artifact=14
analysis artifact=44
english_analysis_semantic_review=accepted
blueprint_is_current_chain=False

tmyX capability_is_current_chain=True
Capability artifact=15
analysis artifact=46
english_analysis_semantic_review=accepted
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
English P1.6:                  5
Original P1.6:                 0
Capabilities:                  5
```

Important interpretation:

```text
344 known/discovered jobs != 344 complete advertisements
```

The remote corpus can now be used to select heterogeneous roles without direct local SQLite access.

## Current semantic review workflow

Active order:

```text
1. Python/software          ← tmBK 39 → 13 accepted / closed
2. network/security         ← t4qV 44 → 14 accepted / closed
3. operations/platform      ← tmyX 46 → 15 accepted / closed
```

For each selected role:

1. inspect original source and English projection quality;
2. run/reuse current English P1.6;
3. inspect the complete `pending` candidate and record `accept` or `reject` through `jobhunter jobs review-analysis` (or the browser);
4. run/reuse current Capability v9 only after accepted P1.6;
5. inspect P1.6 factual coverage, strength, optionality, explicit depth and evidence;
6. inspect Capability complete requirement/responsibility coverage and provenance;
7. inspect grouping coherence and role-level source partition;
8. verify deterministic source truth and absence of unsupported ownership/autonomy/lifecycle/architecture or contextual-tool promotion;
9. distinguish deterministic defects from model limitations or harmless non-authoritative variation;
10. convert repeatable deterministic defects into fixtures.

Current accepted Python/software case:

```text
tmBK
source detail 44
English projection 38
P1.6 artifact 39 accepted
Capability artifact 13 accepted
```

Accepted network/security case: `t4qV` (detail 30, projection 20, P1.6 44, Capability 14). Accepted operations/platform case: `tmyX` (detail 35, projection 24, P1.6 46, Capability 15). Their snapshots preserve exact accepted chains and review decisions; rejected candidates remain local archived evidence.

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
