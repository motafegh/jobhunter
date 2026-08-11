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

## Current `tG9K` acceptance chain

Configured role models:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-e4b-it-ud
```

Accepted fixed upstream chain:

```text
English projection artifact 33
→ English P1.6 artifact 29
→ Capability v7/v4 artifact 9
```

Capability artifact 9 passed the bounded B3 acceptance gate.

Blueprint status:

- v3/v2 failed B4 structurally/semantically;
- v4/v3 completed and passed its mechanical audit but failed complete semantic review;
- v5/v4 is the active B4 candidate.

A locally generated v4 `tG9K` snapshot is rejected B4 evidence. Do not commit it as an accepted review example. The next intended selected snapshot is a v5 candidate after successful generation, audit and semantic review.

## Current B4 Blueprint review workflow

Do **not** rerun translation, accepted P1.6 or Capability merely to test Blueprint.

Confirm the active contract:

```bash
python -c "from jobhunter.role_blueprint_service import BLUEPRINT_PROMPT_VERSION, BLUEPRINT_SCHEMA_VERSION; print(BLUEPRINT_PROMPT_VERSION); print(BLUEPRINT_SCHEMA_VERSION)"
```

Expected:

```text
role-capability-blueprint-v5
role-capability-blueprint-v4
```

Run only:

```bash
jobhunter jobs blueprint tG9K
```

If a valid Blueprint artifact is produced, then:

```bash
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v5_snapshot.py
```

The v5 mechanical audit checks:

- exact P1.6 artifact 29 / Capability artifact 9 dependency identity;
- one-to-one Blueprint-area mapping to accepted Capability profiles in source order;
- complete deterministic Capability coverage;
- exact source role purpose;
- exact P1.6 source requirement/responsibility anchors per Capability;
- exact source strength/depth/evidence propagation;
- exact role-level constraints;
- each model-created Capability interpretation is mechanically `plausible` and carries non-empty `interpretation_uncertainty`;
- professional considerations are only plausible/speculative and carry uncertainty;
- generic obligation/full-ownership language is absent from model prose;
- legacy v4 expansion fields such as role shape, likely depth, hidden requirements, tool suggestions, scenarios and bottom line are absent.

A mechanical pass does **not** itself accept B4. Complete semantic review must still reject employer-specific topology, latency, real-time/control-loop behavior, process-physics obligation, ownership, optionality/depth promotion or other unsupported certainty.

After successful generation, audit and semantic review, inspect the snapshot diff:

```bash
git diff --check
git status --short
git diff -- review-snapshots/jobs/tG9K.json
```

If only the intended review snapshot changed and B4 is actually accepted, publish it deliberately:

```bash
git add review-snapshots/jobs/tG9K.json
git commit -m "review: evaluate tG9K blueprint v5"
git push origin main
```

Do not automatically snapshot/commit the whole corpus.
