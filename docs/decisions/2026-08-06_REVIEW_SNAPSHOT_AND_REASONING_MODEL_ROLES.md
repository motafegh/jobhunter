# Review Snapshots and Independent Reasoning Model Roles

Date: 2026-08-06
Status: active implementation decision

## Decision 1 — Keep the live SQLite database local

JobHunter will not commit the live runtime database merely to make AI/reviewer inspection easier.
The repository is public, SQLite is binary and noisy in Git, and future runtime state may contain
private or user-specific information.

Instead JobHunter provides a deliberate review export:

```bash
jobhunter-review-snapshot <job-id>
```

The default output is:

```text
review-snapshots/jobs/<job-id>.json
```

The snapshot contains the current public Jobinja source plus the review-relevant derived artifact
chain and their identities. Raw LM Studio responses, request bodies/prompts, raw HTML contents,
SQLite internals, secrets, logs, and private candidate/user state are excluded.

A stale downstream artifact is never exported as if it belonged to the current dependency chain.
Status flags make missing/stale stages explicit.

## Decision 2 — Reasoning model roles are independently configurable

Strict factual extraction, Capability Intelligence, and the human-facing Role Capability Blueprint
have different quality objectives. The best extraction model is not assumed to be the best expert
reasoning model.

Configuration now supports:

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

Fallback remains simple:

```text
Capability -> analysis model -> general model -> translation fallback
Blueprint  -> capability model -> analysis/general fallback
```

This enables controlled same-job model comparisons without perturbing source acquisition,
translation, or P1.6 extraction.

## Decision 3 — General calibration rules, not domain-specific prompt patches

The `tG9K` semiconductor review exposed technically plausible but overconfident reasoning. JobHunter
will harden general principles rather than accumulating one-off semiconductor instructions:

- explicit work should be distinguished from inferred prerequisites;
- listed stack items do not automatically become mandatory or preferred;
- company-domain descriptions do not automatically prove regulation/compliance requirements;
- suggested tools remain examples rather than hidden employer facts;
- tool/protocol/domain concepts must retain their normal technical meaning;
- interpretation depth should scale with source evidence density.

These rules belong in the reasoning contracts and generic validators. Domain-specific correctness is
then evaluated through heterogeneous live examples and, where useful, controlled model comparison.
