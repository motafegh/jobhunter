# JobHunter

JobHunter is a **local-first personal career-intelligence application**.

It acquires approved public job-market evidence, preserves authoritative source data, creates a hardened English projection, performs strict evidence-backed factual extraction, and builds bounded reasoning layers for capability and professional-role interpretation.

The browser application is the primary human interface. The CLI remains supported for automation, debugging, tests, and advanced workflows.

## Product direction

```text
MARKET
→ ROLE / CAPABILITY INTELLIGENCE
→ REVIEWED PERSONAL EVIDENCE
→ GAPS / CONSTRAINTS
→ LEARN / PRACTISE / BUILD / VERIFY
→ APPLICATION DECISION
→ OUTCOME
→ UPDATED EVIDENCE AND DECISIONS
↺
```

Every consequential conclusion should remain traceable to source and/or reviewed personal evidence.

Current entry points:

- `AGENTS.md`
- `docs/EXECUTION_TODO.md`
- `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`
- `docs/WORKING_MEMORY.md`
- `review-snapshots/README.md`

## Current implementation state

Accepted/strong Phase-1 foundation includes bounded Jobinja discovery/acquisition, immutable evidence, stable source identity/versioning, deterministic `jobinja-detail-v2` parsing, `english-projection-v2`, browser + CLI surfaces, independent LM Studio model roles, and Review Snapshot export.

Current semantic stack:

```text
Jobinja source
        ↓
english-projection-v2
        ↓
P1.6 strict factual extraction
  English:  job-analysis-english-v9
  Original: job-analysis-original-v9
  schema:   job-analysis-v4
        ↓
Capability Intelligence — active B3 candidate
  prompt:   job-capability-intelligence-v7
  schema:   job-capability-intelligence-v4
        ↓
Role Capability Blueprint
  prompt:   role-capability-blueprint-v2
  schema:   role-capability-blueprint-v1
        ↓
Review Snapshot
  schema:   job-review-snapshot-v1
```

**B3 is not accepted yet.** v7/v4 is the current runtime candidate on `main`; live `tG9K` evidence must pass mechanical and semantic review before Blueprint B4 continues.

## P1.6 — factual substrate

P1.6 records conservative employer-supported facts:

- role purpose;
- responsibilities;
- requirements;
- requirement strength;
- concept type;
- explicit depth;
- confidence;
- exact evidence.

The accepted dense `tG9K` anchor is English analysis artifact **29**. It contains 27 requirements and 7 responsibilities with reviewed obligation/depth preservation.

## Capability Intelligence v7

v7 moves source survival outside model control:

```text
accepted P1.6
→ deterministic source partition
→ model semantic grouping + derived reasoning
→ complete-coverage validation
→ deterministic source_truth / strength / source depth / source work
→ persisted Capability
```

Key properties:

- all accepted P1.6 facts remain in deterministic `source_truth`;
- every capability-relevant requirement must be linked;
- every responsibility must be linked;
- education and standalone experience-duration constraints remain role-level source truth;
- dense jobs require more than one coherent capability profile;
- source-explicit depth and work activities are generated deterministically;
- positive autonomy/ownership inference is deferred;
- cross-capability synthesis is deferred;
- model reasoning remains responsible for coherent grouping, derived prerequisites/context, and unknown boundaries.

Capability v6/v3 artifact 8 is retained as negative B3 evidence. It proved deterministic reconciliation worked for linked facts but also proved that model-selected source links were too weak.

See:

```text
docs/experiments/2026-08-09_CAPABILITY_V6_DETERMINISTIC_RECONCILIATION.md
docs/experiments/2026-08-09_CAPABILITY_V7_SOURCE_TRUTH_BOUNDARY.md
```

## Current acceptance workflow

Keep `tG9K` P1.6 artifact 29 fixed.

```bash
jobhunter jobs capability tG9K
jobhunter jobs snapshot tG9K
python scripts/audit_capability_v7_snapshot.py
```

Do **not** rerun English analysis or rebuild Blueprint merely to test v7.

The audit is necessary but not sufficient. B3 also requires semantic review for coherent grouping, evidence relevance, optionality preservation, technically sound prerequisites, useful unknowns, and absence of unsupported architecture/ownership claims.

## Review Snapshots

The live SQLite database remains local and ignored.

Generate a selected repository-safe review snapshot:

```bash
jobhunter jobs snapshot tG9K
```

Default output:

```text
review-snapshots/jobs/tG9K.json
```

Inspect and intentionally publish selected examples only:

```bash
git diff -- review-snapshots/jobs/tG9K.json
git add review-snapshots/jobs/tG9K.json
git commit -m "review: evaluate tG9K capability v7"
git push origin main
```

Snapshots exclude raw model responses/prompts, SQLite/WAL/SHM, raw HTML contents, secrets, logs, and future private user state.

## Independent local model roles

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

Current controlled `tG9K` roles:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-e2b-it
```

Do not change the capability model during the first v7 same-job acceptance run. If v7 is mechanically correct but E2B remains semantically inadequate, compare a stronger reasoning model with source/P1.6/contract/rubric held fixed.

## Start the application

Requires Python 3.12+.

```bash
python -m pip install -e ".[dev]"
jobhunter-app
```

Default local URL:

```text
http://127.0.0.1:8765/
```

No Node/npm runtime or CDN is required.

## Important CLI commands

```bash
jobhunter run
jobhunter jobinja plan
jobhunter jobinja sync
jobhunter jobs list
jobhunter jobs show <job-id>
jobhunter jobs health <job-id>
jobhunter jobs checks <job-id>
jobhunter jobs audit
jobhunter jobs capability <job-id>
jobhunter jobs blueprint <job-id>
jobhunter jobs snapshot <job-id>
jobhunter translations status
jobhunter translations models
jobhunter translations run --missing --limit 20
jobhunter translations export
```

Browser and CLI share the same services/state.

## Current near-term sequence

```text
B3: live Capability v7/v4 tG9K acceptance
→ B4: Blueprint calibration/model comparison if needed
→ B5/CI-3: heterogeneous live-role review
→ Phase-1 Market/source/lifecycle/partial-success/P1.7 closure
→ only then corpus-wide Phase 2
```

JobHunter does not yet claim Phase 1 is closed, production-quality reasoning across all role types, canonical Phase-2 taxonomy, reviewed personal readiness/gap state, arbitrary-web ingestion, autonomous applications, or an evaluated RAG/agent platform.

## Development validation

```bash
ruff check .
python -m pytest
python -m pytest -W error
```

Normal deterministic tests do not contact Jobinja, Google Cloud, or LM Studio. Live source/model validation is separate and bounded.
