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

Capability artifact 9 passed bounded B3 acceptance.

Blueprint history:

- v3/v2 failed B4 structurally and semantically;
- v4/v3 passed deterministic mechanical provenance but failed semantic review;
- v5/v4 artifact 6 was a valid current-chain review candidate and was committed in snapshot commit `ffa690361e5cbbb755fff7bcd587d6903d5dce89`, but complete semantic review rejected its remaining free-form role-summary inference;
- v6/v5 is the active B4 candidate.

The currently committed `tG9K` snapshot therefore contains **rejected v5 review evidence**, not an accepted Blueprint baseline. Replace it only with a newly generated v6 candidate.

## Current B4 Blueprint review workflow

Do **not** rerun translation, accepted P1.6 or Capability merely to test Blueprint.

Confirm the active contract:

```bash
python -c "from jobhunter.role_blueprint_service import BLUEPRINT_PROMPT_VERSION, BLUEPRINT_SCHEMA_VERSION; print(BLUEPRINT_PROMPT_VERSION); print(BLUEPRINT_SCHEMA_VERSION)"
```

Expected:

```text
role-capability-blueprint-v6
role-capability-blueprint-v5
```

Run only:

```bash
jobhunter jobs blueprint tG9K
```

If a valid Blueprint artifact is produced:

```bash
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v6_snapshot.py
```

The v6 mechanical audit checks:

- exact P1.6 artifact 29 / Capability artifact 9 dependency identity;
- one-to-one Blueprint-area mapping to accepted Capability profiles in source order;
- complete deterministic Capability coverage;
- exact source role purpose;
- exact P1.6 source requirement/responsibility anchors per Capability;
- exact source strength/depth/evidence propagation;
- exact role-level constraints;
- absence of v5 free-form `practical_interpretation`, `interpretation_uncertainty`, area-level strength and `probably_not_required` fields;
- at least one important unknown per Capability;
- professional considerations only plausible/speculative with non-empty uncertainty;
- generic employer-obligation/full-scope wording absent from positive model-generated considerations;
- older expansion fields such as role shape, likely depth, hidden requirements, tool suggestions, scenarios and bottom line absent.

A mechanical pass does **not** accept B4. Complete semantic review must still reject source-unsupported streaming, real-time/low-latency behavior, automated feedback, cloud/edge placement, lifecycle ownership, architecture synthesis, optionality/depth promotion, or unknowns that themselves presume unstated systems.

After successful generation and audit, inspect the snapshot diff:

```bash
git diff --check
git status --short
git diff -- review-snapshots/jobs/tG9K.json
```

To publish the candidate for review:

```bash
git add review-snapshots/jobs/tG9K.json
git commit -m "review: capture tG9K Blueprint v6 candidate"
git push origin main
```

Publishing a candidate makes it reviewable; it does not itself mean B4 is accepted.

Do not automatically snapshot/commit the whole corpus.
