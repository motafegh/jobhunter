# Review Snapshots and Independent Reasoning Model Roles

Date: 2026-08-06  
Updated: 2026-08-08  
Status: active implementation decision

## Decision 1 — Keep the live SQLite database local

JobHunter will not commit the live runtime database merely to make AI/reviewer inspection easier.

Reasons:

- the repository is public;
- SQLite is binary and noisy in Git;
- SQLite/WAL/SHM are poor review/diff artifacts;
- future runtime state may contain private/personal information;
- Git history is a poor place for mutable local state.

Instead JobHunter provides a deliberate review export.

Normal command:

```bash
jobhunter jobs snapshot <job-id>
```

Standalone compatibility entry point:

```bash
jobhunter-review-snapshot <job-id>
```

Default output:

```text
review-snapshots/jobs/<job-id>.json
```

The snapshot contains the current public Jobinja source plus review-relevant current derived artifacts and their dependency identities.

Deliberately excluded:

- SQLite/WAL/SHM;
- raw HTML contents;
- raw LM Studio responses;
- model request bodies/system prompts;
- secrets/API tokens/local configuration;
- operation/debug logs;
- private candidate/user state.

A stale downstream artifact is not exported as if it belonged to the current dependency chain. Status flags expose missing/stale relationships.

The first real pushed acceptance example is:

```text
review-snapshots/jobs/tG9K.json
```

This proved that repository-native quality review can replace manual copy/paste of large browser pages.

### Known integrated-CLI defect discovered by the first snapshot

The standalone `jobhunter-review-snapshot` path passes the effective analysis/capability/blueprint model roles to `write_review_snapshot()`.

The integrated `jobhunter jobs snapshot` path currently loads settings but does not pass those effective model arguments. The first `tG9K` snapshot therefore recorded:

```json
"configured_models": {
  "analysis": null,
  "capability": null,
  "blueprint": null
}
```

while the persisted artifacts themselves correctly recorded the actual `gemma-4-e2b-it` model.

This is harmless only while one relevant artifact/model exists. It becomes unsafe for controlled model comparison because `latest_current(..., model=None)` may select a different current model artifact than the configured role.

**Required correction before model comparison:** make the integrated CLI pass:

```text
effective_analysis_lm_studio_model()
effective_capability_lm_studio_model()
effective_blueprint_lm_studio_model()
```

and cover the routing with deterministic tests.

## Decision 2 — Reasoning model roles are independently configurable

Strict factual extraction, Capability Intelligence, and the human-facing Role Capability Blueprint have different quality objectives. The best extraction model is not assumed to be the best expert-reasoning model.

Configuration supports:

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

Effective fallback implemented in `Settings`:

```text
analysis
→ dedicated analysis model
→ general LM Studio model
→ explicit translation model

Capability
→ dedicated capability model
→ effective analysis model

Blueprint
→ dedicated Blueprint model
→ effective Capability model
```

This enables controlled same-job model comparisons without perturbing acquisition, translation, or strict P1.6 evidence.

The browser Capability/Blueprint readers were also corrected to use the dedicated model roles rather than assuming that every reasoning layer uses the analysis model.

## Decision 3 — General calibration rules, not domain-specific prompt patches

The `t4jp` and `tG9K` reviews exposed two different classes of semantic behavior:

```text
sparse source
→ legitimately limited conclusions / more unknowns

rich source
→ deep analysis expected / omissions and overconfidence become real quality defects
```

JobHunter will harden general principles rather than accumulating one-off domain instructions:

- explicit work stays distinct from inferred prerequisites;
- employer optionality and technical depth remain separate;
- listed stack items do not automatically become mandatory/preferred;
- a technology list is not an architecture specification;
- company-domain descriptions do not automatically prove regulation/compliance/scale;
- suggested tools remain examples rather than hidden employer facts;
- tool/protocol/metric/domain concepts retain their normal technical meaning;
- highly-likely conclusions must not contradict explicit unresolved unknowns;
- interpretation depth should scale with source evidence density;
- deterministic bookkeeping problems are repaired deterministically;
- model/domain judgment is evaluated through heterogeneous examples and model comparison rather than endless prompt patches.

The exact active quality sequence is now documented in:

```text
docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md
```

## Decision 4 — Review Snapshots are acceptance evidence, not runtime truth

Snapshots are generated review artifacts.

They do not become application inputs and do not replace SQLite/raw evidence as runtime truth.

Use them to:

- review complete source→analysis→Capability→Blueprint chains;
- compare artifact/model identities;
- inspect semantic quality in Git;
- preserve selected acceptance examples;
- allow another conversation/reviewer to continue without manual pasted output.

Do not automatically commit every analyzed job. Commit selected review/acceptance examples intentionally.
