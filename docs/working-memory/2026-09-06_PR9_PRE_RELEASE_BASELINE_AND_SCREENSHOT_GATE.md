# PR9 Pre-Release Baseline and Screenshot Gate — 2026-09-06

**Status:** PRE-RELEASE BASELINE VERIFIED / SCREENSHOT + GITHUB-METADATA GATE REMAINS  
**Branch:** `main`  
**Verified main commit:** `828d50972268ef7d1fcc93bf3a95d38be9cc0245`  
**Product-development boundary:** P2.2B-B1 remains unchanged and separately blocked on machine-local `ta9l` English projection/P1.6 acceptance.

## Verified repository/release baseline

At the commit above:

- GitHub Actions CI run `#1110` completed successfully.
- Package version remains `0.1.0`.
- The repository contains a standard MIT `LICENSE` and `pyproject.toml` declares the license file plus the MIT classifier.
- GitHub repository metadata detects `MIT License` / SPDX `MIT`.
- The committed public corpus manifest still reports:
  - 353 jobs/source identities;
  - 20 English projections;
  - 5 accepted English P1.6 artifacts;
  - 0 original-language P1.6 artifacts;
  - 5 Capability artifacts.
- GitHub currently reports no releases.

This establishes a clean pre-release baseline after the explicit MIT licensing decision.

## Screenshot gate

The screenshot requirement remains intentionally open.

The reproducible demo contract states that a fresh clone starts with an empty local SQLite database and that the committed public corpus is not silently imported into runtime state. Therefore a CI/Actions-generated empty-state browser screenshot would be a real runtime image but would not satisfy the intended portfolio evidence requirement.

Do not close this gate with:

- generated/mock screenshots;
- template-only rendering presented as runtime state;
- an empty fresh-clone screen merely to satisfy the checklist;
- private/local state that has not been privacy-reviewed.

Required closure evidence remains 2–4 screenshots from the real local application using meaningful public-safe state, followed by a privacy review for local paths, secrets/tokens, unrelated personal data, and other private runtime details.

Preferred screens remain:

1. dashboard/job catalog with meaningful corpus/workflow state;
2. accepted job detail showing source / English / P1.6 separation;
3. Capability or Work Intelligence view;
4. Canonical Registry or Market view only if it communicates a current accepted boundary clearly.

## GitHub metadata gate

Repository description/topics remain an external settings action because the current GitHub connector exposes read access but no repository-settings mutation for those fields.

Prepared values remain:

**Description**

`Local-first career intelligence from real job evidence, with provenance-preserving LLM analysis, semantic review, and auditable Python workflows.`

**Topics**

`python`, `fastapi`, `sqlite`, `llm`, `lm-studio`, `career-intelligence`, `job-market`, `provenance`, `local-first`, `pydantic`

Homepage should remain blank until a meaningful separate hosted destination exists.

## Release decision

Do not create `v0.1.0` yet.

Current remaining release sequence:

```text
GitHub description/topics
→ real local screenshots + privacy review
→ README/demo screenshot integration
→ repeat final public-count/version/current-state check on the final release commit
→ final CI green on that commit
→ tag v0.1.0
→ GitHub release using prepared notes
→ verify tagged public surfaces
→ complete owner mastery verification
→ PR9 CLOSED
```

Owner mastery can proceed while the external/local screenshot and repository-settings actions remain pending.
