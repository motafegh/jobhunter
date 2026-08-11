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
  prompt:   role-capability-blueprint-v3
  schema:   role-capability-blueprint-v2
        ↓
Review Snapshot
  schema:   job-review-snapshot-v1
```

Capability v7/v4 passed the bounded rich `tG9K` B3 gate on artifact **9** and is frozen while B4 proceeds. Blueprint v3/v2 is implemented on `main` but is **not semantically accepted** until a live artifact built from Capability 9 passes mechanical and complete semantic review.

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

## Role Capability Blueprint v3

Blueprint remains the human-facing professional interpretation layer, but v3 makes strong interpretations auditable against accepted upstream truth.

Key v3 properties:

- every Blueprint area links accepted Capability profile indices and collectively covers the accepted Capability substrate;
- source-named tools link accepted P1.6 facts;
- JobHunter derives source-named tool strength and explicit depth deterministically;
- inferred examples carry no employer-source strength/depth;
- preferred/contextual tools cannot silently become mandatory;
- role-level degree/experience constraints are injected from Capability v7 source truth;
- highly-likely hidden requirements require accepted upstream grounding;
- every end-to-end scenario is either `source_stated_workflow` or `professional_example`;
- practitioner-created examples cannot be `highly_likely`;
- unresolved assumptions cannot hide inside highly-likely scenarios;
- a technology list is not treated as an employer architecture specification.

See:

```text
docs/experiments/2026-08-11_BLUEPRINT_V3_GROUNDED_INTERPRETATION.md
```

## Current B4 acceptance workflow

Keep these upstream artifacts fixed:

```text
English projection: 33
English P1.6:        29
Capability v7:       9
```

Run only the downstream Blueprint stage:

```bash
jobhunter jobs blueprint tG9K
jobhunter jobs snapshot tG9K
python scripts/audit_blueprint_v3_snapshot.py
```

Do **not** rerun P1.6 or Capability merely to test Blueprint.

The audit is necessary but not sufficient. B4 still requires full semantic review for useful professional interpretation, technical correctness, optionality preservation, scenario realism, unknown boundaries, and absence of invented employer architecture.

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
git commit -m "review: evaluate tG9K blueprint v3"
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

Keep the Blueprint model fixed for the first v3 same-job acceptance run. If the contract is mechanically correct but E2B remains semantically inadequate, compare a stronger reasoning model with source/P1.6/Capability/contract/rubric held fixed.

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
→ B4: live Blueprint v3/v2 tG9K acceptance
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
