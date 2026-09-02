# JobHunter Review Snapshots

`review-snapshots/` contains deliberately selected, repository-safe JSON snapshots used for semantic review, acceptance evidence, and regression anchors.

These files are **not** the live SQLite database, are **not** runtime inputs, and are **not** the complete public job dataset. The complete version-controlled public projection lives in [`../corpus/`](../corpus/README.md).

```text
corpus/
→ complete current repository-safe public dataset
→ routine deterministic projection

review-snapshots/
→ selected jobs only
→ explicit semantic review / acceptance evidence
→ curated regression and decision anchors
```

## Create or inspect a snapshot

```bash
jobhunter jobs snapshot <job-id>
git diff -- review-snapshots/jobs/<job-id>.json
```

Compatibility entry point:

```bash
jobhunter-review-snapshot <job-id>
```

Current schema:

```text
job-review-snapshot-v1
```

## What a snapshot may include

A selected snapshot may preserve:

- current public source provenance and parsed fields;
- English projection;
- current English/original P1.6 artifacts;
- dependency-current Capability artifact;
- optional experimental Blueprint evidence only when it belongs to its historical-compatible dependency chain;
- artifact/model/prompt/schema identities;
- dependency IDs;
- configured model roles;
- current-chain flags;
- explicit P1.6 semantic-review status and selected review note/time where intentionally published.

## Deliberately excluded

Snapshots do not export:

- SQLite/WAL/SHM;
- raw HTML contents;
- raw LM Studio responses;
- model request bodies/system prompts;
- API tokens, secrets, or local config;
- operation/debug histories;
- future private/personal user state.

The repository is public. Commit selected review examples intentionally.

## Dependency currentness is not semantic acceptance

Flags such as:

```text
translation_matches_english_analysis
capability_is_current_chain
blueprint_is_current_chain
```

prove dependency/currentness relationships only. They do **not** by themselves prove semantic acceptance.

A current-chain artifact can still fail semantic review. A historical artifact can remain useful experimental evidence without being current. P1.6 semantic acceptance is recorded separately through the review state.

## Current accepted semantic anchors

Current public contracts:

```text
English P1.6: job-analysis-english-v20 / job-analysis-v5
Capability:   job-capability-intelligence-v9 / job-capability-intelligence-v5
```

Accepted/current representative chains:

```text
tG9K  → P1.6 36 → Capability 11
t4jp  → P1.6 37 → Capability 12
tmBK  → P1.6 39 → Capability 13
t4qV  → P1.6 44 → Capability 14
tmyX  → P1.6 46 → Capability 15
```

The heterogeneous accepted set covers dense AI/ML, sparse, Python/software, network/security, and operations/platform role shapes. Rejected P1.6 candidates never became eligible for downstream accepted Capability artifacts.

Blueprint v6 remains deferred/non-authoritative and pinned to historical Capability-v7 dependency semantics. It must not be presented as current merely because a historical snapshot can contain it.

## Public corpus baseline

The public corpus gate is closed: the local database was projected, deterministically verified, intentionally published, and remotely inspected.

Current published/verified baseline:

```text
Known/discovered jobs:       353
Fetched/parsed job details:   43
Current English projections:  20
English P1.6:                  5
Original P1.6:                 0
Capabilities:                  5
```

`353` means known/discovered job identities, **not** 353 complete advertisements. Only jobs with a current fetched/parsed detail are eligible for downstream semantic-review selection.

The authoritative current corpus structure and commands are documented in [`../corpus/README.md`](../corpus/README.md).

## Historical Phase-1 semantic-review route

The representative heterogeneous review sequence is complete:

```text
Python/software       tmBK 39 → 13 accepted
network/security      t4qV 44 → 14 accepted
operations/platform   tmyX 46 → 15 accepted
```

That route established the current P1.6/Capability acceptance substrate. It is retained as engineering evidence; it is **not** the current product-development gate.

For a selected semantic review, the permanent pattern remains:

1. inspect original source and English projection quality;
2. run/reuse the current English P1.6 contract;
3. inspect the complete pending candidate and explicitly accept or reject it;
4. run/reuse current Capability only after accepted P1.6;
5. verify exact factual coverage, obligation/depth calibration, evidence, and provenance;
6. distinguish deterministic defects from model limitations or harmless non-authoritative wording variation;
7. turn repeatable deterministic defects into fixtures rather than endlessly changing accepted contracts.

## Blueprint research audit

If intentionally inspecting the historical experimental Blueprint:

```bash
jobhunter jobs blueprint <job-id>
jobhunter jobs snapshot <job-id>
python scripts/audit_blueprint_v6_snapshot.py review-snapshots/jobs/<job-id>.json --job-id <job-id>
```

The audit checks mechanical provenance/shape only. A PASS is never semantic acceptance.

## Publishing selected snapshots

Before committing a selected snapshot:

```bash
git diff --check
git status --short
git diff -- review-snapshots/jobs/<job-id>.json
```

Commit only deliberately selected public review evidence. Routine complete public data belongs in `corpus/`, not here.
