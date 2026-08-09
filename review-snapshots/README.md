# JobHunter Review Snapshots

`review-snapshots/` contains deliberately exported, repository-safe JSON snapshots of selected public Jobinja jobs. These files are **not** the live SQLite database and are not runtime inputs.

A snapshot makes the selected dependency chain reviewable:

```text
public Jobinja source
→ English projection
→ English P1.6 factual analysis
→ Capability Intelligence
→ Role Capability Blueprint
```

## Create / inspect / publish

```bash
jobhunter jobs snapshot <job-id>
git diff -- review-snapshots/jobs/<job-id>.json
```

For the current B3 `tG9K` Capability v7 acceptance:

```bash
jobhunter jobs capability tG9K
jobhunter jobs snapshot tG9K
python scripts/audit_capability_v7_snapshot.py
```

Then, after inspecting the diff:

```bash
git add review-snapshots/jobs/tG9K.json
git commit -m "review: evaluate tG9K capability v7"
git push origin main
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

## Dependency status

The `status` object is authoritative for whether a downstream artifact belongs to the selected current chain:

```text
translation_matches_english_analysis
capability_is_current_chain
blueprint_is_current_chain
```

A stale downstream artifact is not exported as current.

## Current `tG9K` state

Configured role models:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-e2b-it
```

Accepted upstream anchor:

```text
English projection artifact 33
English P1.6 artifact 29
```

The currently committed snapshot contains **Capability artifact 8, v6/v3**, as negative B3 evidence. That artifact is dependency-current but semantically rejected. Blueprint is absent from the current chain because it was built against an older Capability dependency.

The runtime on `main` is now the unaccepted **Capability v7/v4** candidate. After a successful local v7 run, regenerate this snapshot and run `scripts/audit_capability_v7_snapshot.py` before committing it.

Do not automatically snapshot/commit the whole corpus.
