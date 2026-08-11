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
Capability Intelligence — B3 accepted baseline
  prompt:   job-capability-intelligence-v7
  schema:   job-capability-intelligence-v4
        ↓
Role Capability Blueprint — active B4 candidate
  prompt:   role-capability-blueprint-v4
  schema:   role-capability-blueprint-v3
        ↓
Review Snapshot
  schema:   job-review-snapshot-v1
```

Capability v7/v4 passed the bounded rich `tG9K` B3 gate on artifact **9** and is frozen while B4 proceeds. Blueprint v3/v2 failed controlled E2B/E4B B4 comparison; Blueprint v4/v3 is now implemented on `main` but is **not semantically accepted** until a live artifact built from Capability 9 passes mechanical and complete semantic review.

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

The accepted `tG9K` artifact proves 25/25 capability-relevant requirements and 7/7 responsibilities are linked. Role-level requirements 25 and 26 remain deterministic source truth rather than being forced into capability profiles.

The CLI reports five of six explicit depth facts inside profiles because the sixth is intentionally role-level professional experience (`three to six years`, requirement 26). No accepted depth fact is lost.

See:

```text
docs/experiments/2026-08-11_CAPABILITY_V7_B3_ACCEPTANCE.md
```

## Role Capability Blueprint v4

Blueprint remains the human-facing professional interpretation layer. V4 applies the same source-survival principle that made Capability v7 robust:

> **The model reasons; JobHunter owns provenance bookkeeping.**

Key v4 properties:

- the model-facing schema contains no Capability/P1.6 numeric provenance;
- the model returns exactly one semantic interpretation per accepted Capability profile in source order;
- JobHunter deterministically attaches Capability identity and complete coverage;
- JobHunter deterministically attaches each area's accepted P1.6 source requirements/responsibilities, including exact strength/depth/evidence;
- source-named technologies remain deterministic source anchors rather than model-created provenance records;
- model-created tool suggestions are only `likely_example` / `possible_example` and carry no employer-source provenance;
- role-level degree/experience constraints are injected from Capability v7 source truth;
- model-created hidden requirements are only plausible/speculative;
- model-created workflows are explicitly `professional_example_scenarios`, only plausible/speculative, with deterministic `professional_example` basis;
- unstated topology/latency/vendor/batch-stream/cloud-edge/scale/ownership/orchestration choices must remain assumptions;
- a technology list is not treated as an employer architecture specification.

V3/v2 is preserved as historical negative evidence because both E2B and E4B confused provenance namespaces and retained material architecture/optionality overreach.

See:

```text
docs/experiments/2026-08-11_BLUEPRINT_V3_GROUNDED_INTERPRETATION.md
docs/experiments/2026-08-11_BLUEPRINT_V4_DETERMINISTIC_PROVENANCE_BOUNDARY.md
```

## Current B4 acceptance workflow

Keep these upstream artifacts fixed:

```text
English projection: 33
English P1.6:        29
Capability v7:       9
```

Confirm the active Blueprint contract:

```bash
python -c "from jobhunter.role_blueprint_service import BLUEPRINT_PROMPT_VERSION, BLUEPRINT_SCHEMA_VERSION; print(BLUEPRINT_PROMPT_VERSION); print(BLUEPRINT_SCHEMA_VERSION)"
```

Expected:

```text
role-capability-blueprint-v4
role-capability-blueprint-v3
```

Run only the downstream Blueprint stage:

```bash
jobhunter jobs blueprint tG9K
```

Do **not** rerun translation, P1.6 or Capability merely to test Blueprint.

If a valid Blueprint artifact is produced:

```bash
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v4_snapshot.py
```

The audit is necessary but not sufficient. B4 still requires full semantic review for useful professional interpretation, technical correctness, optionality/depth preservation, scenario realism, unknown boundaries, and absence of invented employer architecture.

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

Inspect and intentionally publish selected examples only after live acceptance review:

```bash
git diff -- review-snapshots/jobs/tG9K.json
git add review-snapshots/jobs/tG9K.json
git commit -m "review: evaluate tG9K blueprint v4"
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
blueprint:  gemma-4-e4b-it-ud
```

Blueprint inference automatically prepares the selected LM Studio instance with a 16,384-token context window, reusing or reloading the same model as needed. Manual LM Studio context-window setup is not part of the normal workflow.

Keep the Blueprint model fixed for the first v4 same-job acceptance run. Do not change evidence, upstream artifacts, contract and model simultaneously. No multi-model voting.

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
B3: Capability v7/v4 accepted on bounded tG9K gate
→ B4: live Blueprint v4/v3 tG9K acceptance
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
