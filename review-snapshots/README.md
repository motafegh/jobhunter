# JobHunter Review Snapshots

`review-snapshots/` contains deliberately exported, reviewable JSON snapshots of selected public Jobinja jobs.

These files are **not** the JobHunter SQLite database and are not runtime inputs.

## Why this exists

The live database stays local and ignored because it is binary, changes frequently, is poor Git-review material, and may later contain private/personal state.

A Review Snapshot captures the selected current logical intelligence chain in stable UTF-8 JSON so another reviewer or AI conversation can inspect quality directly from the repository.

Normal reviewed chain:

```text
public Jobinja source
→ English projection
→ English P1.6 factual analysis
→ Capability Intelligence
→ Role Capability Blueprint
```

## Create or refresh a snapshot

```bash
source .venv/bin/activate
jobhunter jobs snapshot tG9K
```

Standalone compatibility entry point:

```bash
jobhunter-review-snapshot tG9K
```

Default output:

```text
review-snapshots/jobs/tG9K.json
```

Inspect before publishing:

```bash
git diff -- review-snapshots/jobs/tG9K.json
```

Then intentionally commit/push:

```bash
git add review-snapshots/jobs/tG9K.json
git commit -m "review: update tG9K intelligence snapshot"
git push origin main
```

A reviewer can then inspect the full selected chain without manual copy/paste of browser pages.

## Included

A snapshot may contain current:

- public Jobinja source fields and source-version provenance;
- English projection and translation identity/provenance;
- English P1.6 semantic analysis;
- Original-language analysis when it exists;
- Capability Intelligence when it matches the current English-analysis dependency;
- Role Capability Blueprint when it matches the current Capability dependency;
- artifact/model/prompt/schema IDs and timestamps;
- dependency IDs;
- current-chain status flags;
- configured/effective model roles used for chain selection.

Current snapshot schema:

```text
job-review-snapshot-v1
```

## Deliberately excluded

Snapshots do not export:

- SQLite/WAL/SHM;
- raw HTML contents;
- raw LM Studio responses;
- model request bodies/system prompts;
- API tokens/secrets/local configuration;
- operation/debug histories;
- candidate/private personal data or future user notes.

The repository is public. Commit only selected snapshots whose source material is appropriate to publish.

## Dependency status

The `status` object is authoritative for whether a derived stage belongs to the selected current chain.

Important flags include:

```text
translation_matches_english_analysis
capability_is_current_chain
blueprint_is_current_chain
```

A stale downstream artifact is not exported as if it were current.

If a P1.6/Capability/Blueprint contract changes, rebuild the affected downstream layers before expecting all current-chain flags to become true.

## Model-role selection

JobHunter supports independent models for:

```text
analysis
Capability Intelligence
Role Capability Blueprint
```

A snapshot should follow the **effective configured model roles**, not merely whichever valid artifact was written most recently.

### Integrated routing status

The standalone `jobhunter-review-snapshot` entry point and integrated command both pass effective model roles to the exporter.

The normal command:

```bash
jobhunter jobs snapshot <id>
```

selects the configured analysis/Capability/Blueprint chain and records those role models. The selected `tG9K` snapshot identifies `gemma-4-e4b-it-ud` for analysis and `gemma-4-e2b-it` for both downstream roles. It includes Capability artifact 7 because that artifact depends on accepted analysis artifact 29; the artifact is present for negative semantic review, not B3 acceptance. Blueprint remains absent because the existing Blueprint was built from an older chain.

The routing is covered by deterministic CLI tests. See:

```text
docs/EXECUTION_TODO.md
docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md
```

## Current reviewed example

```text
review-snapshots/jobs/tG9K.json
```

This is the first complete repository-native acceptance example and proved that the snapshot workflow is sufficient for remote/repository semantic-quality review.

Do not automatically snapshot/commit the whole corpus. Keep these files selected review/acceptance artifacts.
