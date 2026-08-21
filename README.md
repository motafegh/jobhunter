# JobHunter

JobHunter is a **local-first personal career-intelligence application**.

It acquires approved public job-market evidence, preserves source provenance, creates a hardened English projection, performs strict evidence-backed factual extraction, and builds auditable Capability Intelligence above that source truth.

The browser application is the primary repeated-use interface. The CLI remains supported for automation, debugging, acceptance work, and advanced workflows.

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

Start with:

- `AGENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/EXECUTION_TODO.md`
- `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`
- `docs/WORKING_MEMORY.md`
- `corpus/README.md`
- `review-snapshots/README.md`

## Current accepted semantic stack

```text
Jobinja public source
        ↓
jobinja-detail-v2
        ↓
english-projection-v2
  provider: lm-studio-translation-v2
        ↓
P1.6 strict factual extraction
  English:  job-analysis-english-v20 / job-analysis-v5
  Original: job-analysis-original-v9 / job-analysis-v4
        ↓
Capability Intelligence
  job-capability-intelligence-v9 / job-capability-intelligence-v5
```

Current accepted/current anchors:

```text
tG9K
P1.6 artifact 36
→ Capability artifact 11

t4jp
P1.6 artifact 37
→ Capability artifact 12
```

Capability v9 public promotion is fully closed and operationally verified. Normal public commands reuse those accepted artifacts on their exact P1.6 dependencies.

Role Capability Blueprint remains implemented experimentally at:

```text
role-capability-blueprint-v6 / role-capability-blueprint-v5
```

Blueprint is **not an accepted Phase-1 decision layer**, is pinned to historical Capability v7 dependency semantics, and is not current on the accepted v9 chains.

## P1.6 — factual substrate

P1.6 records conservative employer-supported facts including:

- role purpose when actually stated;
- responsibilities;
- requirements;
- required/preferred/contextual strength;
- concept type;
- explicit depth attached to the exact concept;
- confidence;
- exact evidence/provenance.

Dense `tG9K` v20/v5 acceptance:

```text
requirements:      33
responsibilities:  8
role purpose:      0
```

Sparse `t4jp` v20/v5 acceptance:

```text
requirements:      8
responsibilities:  0
role purpose:      0
```

The accepted contract preserves structured source skills, optionality, experience/education constraints, qualification-vs-duty separation, and exact source depth without spreading one adjective across neighboring technologies.

Heterogeneous validation is now exercising the same promoted contract against materially different role shapes. The active Python/software anchor is `tmBK` (Python Developer; source detail 44; English projection artifact 38). Its first persisted P1.6 artifact was rejected during manual review because a deterministic validator bug spread the first depth marker in a dense evidence segment to unrelated concepts. The rejected artifact does not feed Capability. Current v20 hardening on `main` also covers `Sufficient knowledge`, multi-level evidence fail-closed behavior, non-depth `effectively use ...` wording, and redundant coverage-exclusion filtering. The next live step is to rebuild and review `tmBK` P1.6 before any Capability run.

## Capability Intelligence v9

Capability v9 separates semantic grouping from authoritative source bookkeeping:

```text
accepted P1.6 source truth
→ compact capability-group plan
→ bounded exact source-fact assignment
→ bounded optional per-group reasoning
→ deterministic source-link injection
→ deterministic reconciliation
→ persisted Capability
```

Authority split:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

Complete source coverage/provenance is mandatory. Source requirement strength, source-explicit depth, and source work activities are deterministic. Unsupported ownership/lifecycle/autonomy/architecture or optionality inflation is blocked/filtered. Zero optional model enrichment is valid.

Historical v7/v8 modules and artifacts remain available for reproducibility but are not the public/current Capability contract.

## Complete versioned public corpus

The operational database remains local:

```text
data/jobhunter.sqlite3
```

The complete repository-safe public projection is:

```text
corpus/
```

Contract:

```text
jobhunter-public-corpus-v1
```

Layout:

```text
corpus/
├── manifest.json
└── jobs/
    └── <job-id>/
        ├── source.json
        ├── english-projection.json
        ├── p16-english.json
        ├── p16-original.json
        └── capability.json
```

The corpus preserves current public Jobinja source fields—including original Persian/English text—and current successful translation/P1.6/Capability outputs with exact artifact/dependency/model/contract identities.

It deliberately excludes SQLite files, raw HTML evidence, machine-local evidence paths, model request/raw protocol responses, prompts, secrets, logs/configuration, and future private/personal state.

The real published/verified baseline is:

```text
Known/discovered jobs:       344
Fetched/parsed job details:   43
English projections:          33
English P1.6:                  2
Original P1.6:                 0
Capabilities:                  2
```

`344` therefore means known/discovered identities, not 344 complete advertisements. Only jobs with a current fetched/parsed detail are eligible for downstream semantic-review selection.

Commands:

```bash
jobhunter-corpus export
jobhunter-corpus verify
jobhunter-corpus status
```

Normal mutating CLI workflows and completed browser background operations refresh the local `corpus/` projection after durable SQLite work. JobHunter does **not** automatically Git commit or push; repository publication remains intentional.

See `corpus/README.md`.

## Review Snapshots

`review-snapshots/` remains a separate small set of deliberately selected semantic-review/acceptance artifacts.

```text
corpus/           complete current public dataset
review-snapshots/ selected acceptance evidence
```

Generate a snapshot with:

```bash
jobhunter jobs snapshot <job-id>
```

Current-chain flags prove dependency currentness, not semantic acceptance.

## Independent local model roles

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

Current tracked project configuration uses independent local model roles. Blueprint's configured model does not make Blueprint an accepted decision layer.

The tracked `jobhunter.toml` is public project configuration. Never put actual API tokens/passwords/keys into it; use an ignored local secret mechanism.

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
jobhunter jobinja discover
jobhunter jobinja sync
jobhunter jobinja fetch <job-id>

jobhunter jobs list
jobhunter jobs show <job-id>
jobhunter jobs health <job-id>
jobhunter jobs checks <job-id>
jobhunter jobs audit
jobhunter jobs analyze <job-id>
jobhunter jobs capability <job-id>
jobhunter jobs blueprint <job-id>   # experimental
jobhunter jobs snapshot <job-id>

jobhunter translations status
jobhunter translations models
jobhunter translations run --missing --limit 20
jobhunter translations export

jobhunter-corpus export
jobhunter-corpus verify
jobhunter-corpus status
```

Browser and CLI share the same durable application state and service boundaries.

## Current near-term sequence

```text
P1.6 v20/v5 promoted/closed
→ Capability v9/v5 promoted/closed
→ public corpus operationally closed / remotely available
→ Python/software heterogeneous validation (tmBK active)
→ network/security review
→ operations/platform/DevOps review
→ freeze P1.6 + Capability as Phase-2 input if heterogeneous acceptance passes
→ Market/source/lifecycle/partial-success/P1.7 closure
→ Phase-1 closure
→ only then corpus-wide Phase 2
```

JobHunter does not yet claim Phase 1 is closed, semantic acceptance across all role families, canonical Phase-2 taxonomy, reviewed personal readiness/gap state, arbitrary-web ingestion, autonomous applications, or an evaluated RAG/agent platform.

## Development validation

```bash
ruff check .
python -m pytest
python -m pytest -W error
```

Normal deterministic tests do not contact Jobinja, Google Cloud, or LM Studio. Live source/model validation is separate and bounded.
