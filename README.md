# JobHunter

JobHunter is a **local-first personal career-intelligence application**.

It acquires approved public job-market evidence, preserves authoritative source data, creates a hardened English projection, performs strict evidence-backed factual extraction, and builds auditable capability intelligence above that source truth.

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

Current accepted semantic stack:

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
Capability Intelligence — bounded B3 accepted baseline
  prompt:   job-capability-intelligence-v7
  schema:   job-capability-intelligence-v4
        ↓
Review Snapshot
  schema:   job-review-snapshot-v1
```

Role Capability Blueprint remains implemented experimentally at:

```text
prompt: role-capability-blueprint-v6
schema: role-capability-blueprint-v5
best bounded model tested: gemma-4-12b-it-qat
```

Blueprint is **not an accepted Phase-1 decision layer** and is not on the Phase-1 critical path after the completed calibration experiment.

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

Current analysis model:

```text
gemma-4-e4b-it-ud
```

## Capability Intelligence v7

Capability v7 moves source survival outside model control:

```text
accepted P1.6
→ deterministic source partition
→ model semantic grouping + derived reasoning
→ complete-coverage validation
→ deterministic source_truth / strength / source depth / source work
→ persisted Capability
```

The accepted `tG9K` artifact **9** links 25/25 capability-relevant requirements and 7/7 responsibilities. Role-level requirements 25 and 26 remain deterministic source truth rather than being forced into capability profiles.

Five of six explicit depth facts appear inside profiles because the sixth is intentionally role-level professional experience (`three to six years`, requirement 26). No accepted depth fact is lost.

A key downstream lesson is explicit: **accepted Capability grouping may flow downstream, but Capability model-derived explanatory prose is not automatically authoritative downstream context.**

Decision record:

```text
docs/experiments/2026-08-11_CAPABILITY_V7_B3_ACCEPTANCE.md
```

## Blueprint experiment disposition

Blueprint was investigated as a bounded human-facing professional interpretation layer.

The experiment intentionally tested progressively stronger deterministic boundaries:

```text
v3/v2 + E2B/E4B
→ provenance/index confusion + semantic architecture overreach

v4/v3 + E4B
→ deterministic provenance fixed; broad generated prose still overreached

v5/v4 + E4B
→ Capability-derived prose removed; free-form interpretation still inflated scope

v6/v5 + E4B
→ narrow contract; structured repair failed and assumptions remained

v6/v5 + gemma-4-12b-it-qat
→ mechanically valid and materially better; still violated explicit semantic boundary
```

Best bounded experimental evidence:

```text
job: tG9K
Blueprint artifact: 7
P1.6 artifact: 29
Capability artifact: 9
model: gemma-4-12b-it-qat
snapshot commit: 671bd6e3c43555c631958531671a0f1be9726554
```

The v6 mechanical audit and CI passed, but complete semantic review still found assumption-bearing unknowns/considerations: automated APC/SPC feedback-loop framing, assumed cloud/on-prem model-hosting choices, `raw sensor physics`, and strict versioning/quality-standard implications not established by source.

Therefore:

- Blueprint code remains available and inspectable;
- artifact 7 remains review evidence;
- Blueprint is not accepted for Market, personal readiness, recommendations, or other authoritative Phase-1 decisions;
- no Blueprint v7, validator weakening, vacancy-specific prompt patching, or adjacent model shopping is planned during Phase 1;
- Blueprint may be revisited later only with a materially different grounding/inference approach or a demonstrated product-value gap.

Decision record:

```text
docs/experiments/2026-08-12_BLUEPRINT_V6_12B_REVIEW_AND_PHASE1_DEFER_DECISION.md
```

## Current semantic acceptance workflow

The active gate is heterogeneous validation of the layers that have actually passed bounded acceptance:

```text
source
→ English projection
→ P1.6
→ Capability v7
```

Target materially different roles:

```text
t4jp  sparse/ambiguous anchor
tG9K  rich industrial AI/ML baseline
+ Python/software
+ network/security
+ operations/platform/DevOps
```

For each selected role review:

- factual coverage and exact evidence;
- responsibility vs candidate-qualification classification;
- requirement strength and optionality;
- explicit depth attachment;
- education/experience preservation;
- Capability requirement/responsibility coverage;
- Capability grouping coherence;
- deterministic source truth;
- no unsupported ownership/autonomy or contextual-tool promotion.

Repeatable deterministic defects become tests. Model limitations are documented separately.

## Review Snapshots

The live SQLite database remains local and ignored.

Generate a repository-safe review snapshot:

```bash
jobhunter jobs snapshot <job-id>
```

Selected example:

```text
review-snapshots/jobs/tG9K.json
```

The current `tG9K` snapshot contains accepted P1.6 artifact 29 and Capability artifact 9 plus **experimental rejected Blueprint artifact 7**. Current-chain status does not mean semantic acceptance.

Snapshots exclude raw model responses/prompts, SQLite/WAL/SHM, raw HTML contents, secrets, logs, and future private user state.

## Independent local model roles

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

Current configured roles:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-12b-it-qat   # experimental Blueprint only
```

Blueprint runtime automatically prepares the selected LM Studio model with an 8,192-token context and unloads other loaded LLM instances first; embedding models are left alone. Manual context/model switching is not part of normal Blueprint execution.

The tracked `jobhunter.toml` is public configuration and contains no secret. Do not put actual API tokens/passwords/keys into it; use an ignored local secret mechanism.

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
jobhunter jobs blueprint <job-id>   # experimental
jobhunter jobs snapshot <job-id>
jobhunter translations status
jobhunter translations models
jobhunter translations run --missing --limit 20
jobhunter translations export
```

Browser and CLI share the same services/state.

## Current near-term sequence

```text
P1.6 dense baseline accepted on tG9K
→ Capability v7 bounded baseline accepted on tG9K
→ Blueprint calibration experiment concluded/deferred
→ heterogeneous P1.6 + Capability review
→ Market/source/lifecycle/partial-success/P1.7 closure
→ Phase-1 closure
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
