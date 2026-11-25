# JobHunter

**2026-11-24 active evolution sequence:** Owner-approved investigation-first execution tracker: `docs/P16_SEMANTIC_ARCHITECTURE_EVOLUTION_PLAN.md`. E1.1-E1.9 and DOC.1 completed; next E1.10 (see tracker); use its milestone checkboxes and linked evidence records. This sequences the existing Stage B work; no new production contract, B5 acceptance, B6 authorization or downstream promotion. Earlier dated next-action wording remains historical where superseded.

[![CI](https://github.com/motafegh/jobhunter/actions/workflows/ci.yml/badge.svg)](https://github.com/motafegh/jobhunter/actions/workflows/ci.yml)

**JobHunter is a local-first career-intelligence system that turns real job postings into traceable, reviewable evidence for career decisions.**

It is designed as more than a scraper or generic LLM wrapper. JobHunter combines bounded public-source acquisition, immutable evidence, deterministic parsing, local model inference, strict factual extraction, explicit semantic review, capability/work intelligence, reviewed canonical mappings, and durable provenance.

The browser application is the primary repeated-use interface. The CLI exposes the same services and durable state for automation, debugging, review, and advanced workflows.

## Development and contribution model

JobHunter is also an AI-assisted engineering project. Ali directs the product, evidence/authority boundaries, semantic-review rules, and acceptance/rejection decisions, and evaluates the resulting behavior and research. Substantial architecture, source, tests, debugging, and continuation have been produced with AI assistance. The repository's product capability is therefore kept separate from claims about Ali's independent FastAPI, SQLite/SQL, LLM-orchestration, or full-source implementation ownership.

## What JobHunter does today

JobHunter currently supports an end-to-end Jobinja-centered workflow:

- discover and refresh public jobs through bounded, configurable search plans;
- preserve immutable source evidence and semantic job versions before interpretation;
- build a provenance-preserving English projection without replacing the employer's original text;
- extract conservative responsibilities, requirements, strength, explicit depth, and exact evidence through accepted P1.6 contracts;
- keep fresh semantic artifacts in a review gate before they can feed higher-authority layers;
- build Capability Intelligence above accepted factual claims while preserving complete source coverage;
- organize accepted work through Job Work Intelligence v2 without letting model prose replace source truth;
- maintain reviewed canonical concepts and exact claim mappings in the Canonical Registry;
- define target markets, retain immutable snapshots, and inspect deterministic profiles plus durable evidence-linked analytical reports;
- inspect the same durable state through a local browser UI and CLI;
- export a deterministic repository-safe public corpus for remote inspection and reproducibility;
- preserve selected semantic-review evidence as curated review snapshots.

The first **target-scoped Market / Role-Family Intelligence vertical slice** (I1-I7) has passed bounded real-local acceptance. Repeated target runs verified acquisition, membership, source-vs-semantic denominators, reuse, immutable snapshots, privacy, and shared browser/CLI read paths. Snapshot 6 contains six qualified core source postings, including one with explicitly accepted English P1.6 artifact 50 and frozen requirement/responsibility drill-down. These small samples do not establish broad-market prevalence. See the [I7 acceptance record](docs/working-memory/2026-09-26_MARKET_I7_FINAL_LOCAL_ACCEPTANCE.md).

The owner-requested same-target coverage follow-up is complete for this bounded target. Snapshot 15 has ten qualified members: six core, two adjacent, and two excluded. All six core postings have accepted-current English P1.6, with exact artifact evidence in the deterministic profile and browser/CLI drill-down. The unchanged rerun reused the same members and analyses. This remains a small target sample, not broad-market prevalence.

## Why the engineering is non-trivial

The central design problem is not "call an LLM on a job description." It is deciding **what may become authoritative, what remains interpretation, and how every important claim stays recoverable to evidence**.

JobHunter uses an explicit authority ladder:

```text
SOURCE FACT
    ↓
NORMALIZED CORRESPONDENCE
    ↓
ANALYTICAL INTERPRETATION
    ↓
RECOMMENDATION / DECISION SYNTHESIS
```

Important boundaries include:

- **source truth before reasoning** — acquired employer evidence is preserved before parsing, translation, or model interpretation;
- **deterministic vs model responsibilities** — identity, provenance, coverage, currentness, lifecycle, counts, and source bookkeeping stay deterministic;
- **reviewed promotion** — generated semantic candidates are not automatically treated as accepted truth;
- **exact lineage** — durable derived artifacts retain model, prompt, schema, source, and dependency identity;
- **local-first inference** — LM Studio is the primary local model boundary for translation and semantic reasoning;
- **partial-success semantics** — one failed fetch, translation, analysis, or downstream operation does not invalidate already successful durable work;
- **public/private separation** — runtime SQLite/history authority is local while only deliberately repository-safe projections are committed;
- **bounded acquisition** — source access, pages, retries, batches, and model calls are intentionally constrained.

## Architecture at a glance

JobHunter is intentionally a **Python modular monolith** with SQLite as the local runtime/history authority.

```text
Public Jobinja source
        ↓
immutable evidence + source observations
        ↓
jobinja-detail-v2 deterministic parsing
        ↓
semantic JobPosting version
        ↓
English projection v2
        ↓
reviewed P1.6 factual substrate
        ├──→ Capability Intelligence v9
        ├──→ Job Work Intelligence v2
        ├──→ reviewed Canonical Registry mappings
        └──→ bounded Market / report read models

Browser UI ─┐
            ├──→ shared application services ──→ SQLite
CLI ────────┘                                  runtime/history authority
                                                     ↓
                                      deterministic repository projections
                                         ├── corpus/
                                         └── review-snapshots/
```

The browser is server-rendered and intentionally shares the same service/data model as the CLI. There is no separate SPA data model, Node runtime, or distributed-service layer.

### Current semantic boundaries

Current accepted/public contracts include:

- English P1.6: `job-analysis-english-v30 / job-analysis-v5` (accepted-only v20/v21/v23/v28 compatibility);
- original-language P1.6: `job-analysis-original-v9 / job-analysis-v4`;
- Capability Intelligence: `job-capability-intelligence-v9 / job-capability-intelligence-v5`;
- Job Work Intelligence: `job-work-intelligence-v2 / v2.0`;
- Canonical Registry: `jobhunter-canonical-concept-registry-v1`;
- Public Corpus: `jobhunter-public-corpus-v1`.

Accepted v20/v21/v23/v28 English v5 artifacts retain their exact historical model and prompt identities and remain current-compatible only when explicitly accepted with current source and translation dependencies. New English generation uses v30/v5; pending or rejected prior-contract candidates do not satisfy v30 currentness. No accepted anchor is mass-regenerated merely because the public runtime advanced.

Role Capability Blueprint v6 remains implemented as **experimental/historical research**, not an accepted current decision layer.

## Public corpus: inspect real output without LM Studio

The operational database remains local at runtime, but the repository includes a deterministic public projection under [`corpus/`](corpus/README.md).

Committed public-corpus baseline (local unpublished projections may differ):

| Public corpus state | Count |
| --- | ---: |
| Known/discovered jobs | 420 |
| Fetched/parsed job details | 52 |
| Current English projections | 30 |
| Accepted English P1.6 artifacts | 11 |
| Accepted Capability artifacts | 5 |

The October 17 publication adds the current `tNpG` source/detail and English projection. It does not add accepted P1.6 or Capability for that job.

`420` means known/discovered job identities, not 420 complete advertisements.

A fresh clone can inspect the committed corpus without SQLite, Jobinja access, or LM Studio:

```bash
python -m pip install -e ".[dev]"
jobhunter-corpus status
```

For a concrete accepted example, inspect the committed `t4qV` chain:

```bash
python -m json.tool corpus/jobs/t4qV/source.json
python -m json.tool corpus/jobs/t4qV/english-projection.json
python -m json.tool corpus/jobs/t4qV/p16-english.json
python -m json.tool corpus/jobs/t4qV/capability.json
```

For a guided two-case walkthrough—including lineage checks and a sparse listing where JobHunter deliberately keeps accepted responsibilities empty—see [`docs/demo/README.md`](docs/demo/README.md).

The corpus intentionally excludes SQLite files, raw HTML evidence, machine-local paths, raw model protocol history, prompts, secrets, logs, local configuration, Market runtime state, and future personal/private evidence.

## Quick start

### Requirements

- Git
- Python 3.12+
- LM Studio only for local translation/semantic-generation workflows
- network access to Jobinja only for live acquisition workflows

### Install an isolated developer environment

```bash
git clone https://github.com/motafegh/jobhunter.git
cd jobhunter
python -m venv .venv
source .venv/bin/activate       # Linux/macOS/WSL
python -m pip install -e ".[dev]"
jobhunter init --path config/local.toml
```

On Windows PowerShell, activate with:

```powershell
.\.venv\Scripts\Activate.ps1
```

`config/local.toml` is ignored by Git and is the recommended fresh-clone configuration path. It avoids coupling a developer setup to maintainer-specific local model identifiers.

Verify the deterministic baseline:

```bash
jobhunter --config config/local.toml jobinja plan
jobhunter-corpus status
python -m pip check
ruff check .
pytest
pytest -W error
```

Normal deterministic tests and offline search planning do not contact Jobinja or LM Studio.

### Launch the local application

```bash
jobhunter-app --config config/local.toml
```

Default URL:

```text
http://127.0.0.1:8765/
```

A fresh local database may be empty; that is valid. The committed `corpus/` is a repository-safe projection for inspection and reproducibility and is not silently imported into local SQLite.

For the complete setup path—including local-state boundaries, optional LM Studio, optional live acquisition, WSL/Windows notes, and troubleshooting—see [`docs/DEVELOPMENT_AND_LOCAL_SETUP.md`](docs/DEVELOPMENT_AND_LOCAL_SETUP.md).

### Selected CLI entry points

```bash
jobhunter jobs list
jobhunter jobs show <job-id>
jobhunter jobs analyze <job-id>
jobhunter jobs review-analysis <job-id> status
jobhunter jobs capability <job-id>

jobhunter-work <...>
jobhunter-registry <...>

jobhunter translations status
jobhunter-corpus status
```

Use `--config config/local.toml` (or set `JOBHUNTER_CONFIG`) for local commands that load runtime settings. Run each command with `--help` for the exact subcommands/options supported by the installed version.

## Technology stack

| Concern | Current choice |
| --- | --- |
| Language/runtime | Python 3.12+ |
| Web application | FastAPI, Uvicorn, Jinja2 |
| Persistence | SQLite |
| Typed validation/contracts | Pydantic, JSON Schema |
| HTTP/source access | HTTPX |
| Local structured inference | LM Studio through OpenAI-compatible APIs + Instructor |
| Testing | pytest |
| Lint/static quality | Ruff |
| CI | GitHub Actions |
| UI model | server-rendered browser UI + shared CLI services |

The architecture deliberately avoids microservices, Kubernetes, a separate SPA, vector infrastructure, queues, or cloud dependencies until a measured product need justifies them.

## Latest Stage B research boundary (November 22, 2026)

The fourth independently selected original-source B5 cohort failed its frozen B2v4 source gate. A later B2v5 candidate improves retrospective diagnostics only; one explicit duty and one alternative still require resolution. No new P1.6, Capability/Work/Registry/Market accepted fact was promoted. The public English v30/v5 and original v9/v4 paths remain unchanged. The next bounded research decision tests source-qualified **user usefulness on already exposed cases** before another frozen fresh-cohort attempt. See [fourth B5 decision](docs/working-memory/2026-11-22_P16_B5_FOURTH_FAILURE_B2V5_EXPOSED_AND_NEXT_UTILITY_GATE.md).

## Original-source job brief and real-ad remediation (November 23, 2026)

Run `jobhunter --config jobhunter.toml jobs source-brief JOB_ID` to inspect the current exact original Jobinja duties, requirement/advantage candidates, conditions and original board metadata without running a local model or promoting unverified facts; use `--all` for complete source evidence or `--json` for inspectable output. A conservative opt-in B2v7 repairs standalone section-heading errors observed in live ads without regressing the four older exposed source cohorts. Newly generated original-language v9 analyses now require explicit semantic review, while automatic corpus exports from isolated/test SQLite databases go to their own local directory rather than tracked `corpus/`. This is a bounded corrective milestone; **current accepted English v30 reliability and translation semantic quality are not solved**, independent B5 and production B6 remain gated. See [technical decision](docs/working-memory/2026-11-23_P16_REAL_AD_SOURCE_FIRST_REPAIR_AND_OPEN_SEMANTIC_GATES.md).

## Latest bounded B4v6 compact job-understanding research (November 22, 2026)

A candidate-only, original-source-backed decision-first view now reveals 34 of 64 B4v5 qualified items initially across four exposed ads while preserving every source excerpt in full drilldown. Six of nine predeclared applicant evidence questions are immediately navigable; three complete-duty questions need drilldown. This is a reproducible presentation experiment, **not measured user benefit, semantic accuracy superiority, or a production feature**. Existing v30/v9 operations remain unchanged, B5 independent verification and B6 promotion remain gated. See [B4v6 result](docs/working-memory/2026-11-22_P16_B4V6_COMPACT_DECISION_VIEW_EXPOSED_RESULT_AND_NEXT_USER_GATE.md).

## Latest source-gate calibration (November 22, 2026)

A versioned, read-only evaluation repair now distinguishes legitimate multi-bullet source-duty evidence from genuinely missing duties, and illustrative technology/method examples from formal applicant-eligibility alternatives. The original fourth B5 prospective failure remains untouched; a separate exposed-only B2v6 candidate recovers source-grounded classifications without production promotion. The selected fourth review is fully covered under the revised diagnostic method, but B5 generalization and B6 rollout remain unapproved. See [calibration decision](docs/working-memory/2026-11-22_P16_B5_CALIBRATED_EVALUATOR_AND_B2V6_EXPOSED_REPAIR.md).

## Most recent bounded research result (November 22, 2026)

The existing source-qualified B4v5 presentation has a reproducible, four-job, nine-question *exposed* usefulness inspection. Five high-risk questions show source-supported information and four remain partial/uncertain; zero archived same-source English v30 results qualify for a semantic-output head-to-head. This is engineering evidence for fallback availability, **not** independently measured user benefit or authorization to promote experimental semantic facts. Next: a compact B4v6 decision-question-first candidate trial; B5/B6 remain gated. See [exposed usefulness decision](docs/working-memory/2026-11-22_P16_EXPOSED_USEFULNESS_COMPARISON_RESULT_AND_NEXT_DECISION.md).

## Current maturity

Accepted/current foundation and active frontier:

```text
Phase 1                                  CLOSED
P2.1 Canonical Registry                 CLOSED
P2.2A Job Work Intelligence             ACCEPTED / CLOSED
P2.2B first responsibility pilot        CLOSED / NO-PROMOTION / DEFER
Market foundation investigation         PASS / COMPLETE
Market first vertical slice             I1-I7 ACCEPTED / CLOSED FOR BOUNDED SCOPE
RoleFamilyIntelligenceReport R1-R4       ACCEPTED / CLOSED
P2.2B-B2 semantic review R1-R6          COMPLETE
P2.2B-B2 R1/R2                          ACCEPTED / APPLIED / VERIFIED
P2.2B-B2 R3-R6                          ACCEPTED / APPLIED / VERIFIED
P2.2B-B2                               CLOSED / ACCEPTED, SIX-CANDIDATE SCOPE
P2.3A factual comparison                DELIVERED / ENGINEERING CLOSED
```

B2 is now closed and the October 26 owner-authorized bounded P2.3A slice is implemented. **Compare jobs** (`/compare`) places up to three jobs' accepted qualifications, explicit depth, and direct responsibilities together, with literal wording search and evidence drill-down. Existing current Capability-v9 grouping is optional job-local interpretation; each factual claim is counted once. Viewing the page does not call models or persist a profile. Owner time savings remain unmeasured; the summary prototype was not promoted. The frozen-Market-context bug is repaired. The next candidate is evidence-backed technical capability expectations, not additional comparison styling. Persistent P2.3 profiles remain separately gated.

Five heterogeneous accepted P1.6 → Capability chains currently serve as semantic anchors across AI/ML, sparse listings, Python/software, network/security, and operations/platform role shapes.

JobHunter does **not** currently claim:

- semantic acceptance across every discovered job;
- broad-market representativeness from the bounded first-slice sample;
- repost/new-ID-adjusted `unique demand` statistics;
- a complete canonical labor-market taxonomy;
- arbitrary-web ingestion;
- reviewed personal capability/gap scoring;
- autonomous job applications;
- production-scale multi-user deployment;
- an evaluated RAG/agent platform.

Those boundaries are intentional: current claims stay narrower than the evidence.

## Project structure

```text
src/jobhunter/        application, domain, persistence, inference, CLI and web modules
tests/                deterministic unit/integration/regression coverage
corpus/               complete current repository-safe public projection
review-snapshots/     selected semantic-review and acceptance evidence
docs/                 product, architecture, policies, plans and engineering history
scripts/              bounded audits and historical/verification utilities
.github/workflows/    CI quality gates
```

Historical/versioned semantic implementations are retained for reproducibility and compatibility. They are not all current runtime paths; disposition is handled conservatively rather than by mass deletion.

## Documentation

Useful entry points:

- [`docs/PRODUCT_SPECIFICATION.md`](docs/PRODUCT_SPECIFICATION.md) — product purpose, current capabilities, outputs, and boundaries;
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — core architecture, authority, persistence, and runtime design;
- [`docs/DOMAIN_AND_ANALYSIS_MODEL.md`](docs/DOMAIN_AND_ANALYSIS_MODEL.md) — domain/analysis semantics;
- [`docs/SOURCE_POLICY.md`](docs/SOURCE_POLICY.md) — acquisition and source-authority rules;
- [`docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`](docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md) — epistemic/decision authority;
- [`docs/CURRENT_STATE_RECONCILIATION_2026-10-10.md`](docs/CURRENT_STATE_RECONCILIATION_2026-10-10.md) — current status/routing overlay;
- [`docs/P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md`](docs/P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md) — current focused Stage B original-source/bilingual quality gates (B0/B1 accepted; B2 bounded source-first candidate-engine milestone passed on four exposed cases; full semantic generalization not established; B3 bounded source-bound translation complete and its code integrated in `main`; B5 second independent fresh eight-job source gate FAILED 2026-11-22 on B2v2, now-exposed generic B2v3 retrospective repair only; no B5/production acceptance. B5 local translation now has a physically enforced HTTP-attempt/wall-clock pilot cap (five calls, ten exposed original items, one materially partial technical-token omission; no unseen accuracy acceptance). B5 has a source-bound bounded translation batching preflight and two-item exposed local LM Studio pilot, but not unseen model-quality acceptance. B2v2 source-structure candidate improves the now-exposed B5 original-source regression comparison but does not validate generalization. B5 first eight-source unseen candidate gate STOPPED November 21 on upstream B2 source-semantic failures; no translation/LLM paired run or promotion. B4v4c engineering plus B4v5 source-qualified presentation passed exposed gates on main; reviewed Fadak/FDC terminology repaired in B4v5 only; B5 unseen/production promotion still open; no new public analysis route);
- [`docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`](docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md) — controlling Market plan and authorized first slice;
- [`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`](docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md) — formal foundation PASS/authorization;
- [`docs/DEVELOPMENT_AND_LOCAL_SETUP.md`](docs/DEVELOPMENT_AND_LOCAL_SETUP.md) — fresh-clone development setup and optional local services;
- [`docs/demo/README.md`](docs/demo/README.md) — guided reproducible public-corpus demo using real accepted artifacts;
- [`corpus/README.md`](corpus/README.md) — public corpus contract and usage;
- [`review-snapshots/README.md`](review-snapshots/README.md) — curated semantic-review evidence;
- [`SECURITY.md`](SECURITY.md) — security scope, secret/private-state rules, and vulnerability reporting.

The repository also retains detailed plans, experiments, working memory, and historical acceptance records for engineering traceability. They are deeper implementation history, not the intended first-pass product narrative.

## Quality and trustworthiness

CI runs the repository's normal deterministic gates on every push to `main` and on pull requests:

```bash
python -m pip check
ruff check .
pytest
pytest -W error
```

CI also smoke-checks installed public entrypoints and offline public/demo paths so packaging/onboarding breakage is visible.

Beyond ordinary tests, the project has regression coverage around source parsing, translation integrity, P1.6 factual contracts, semantic review, Capability reconciliation, lifecycle/source truth, public-corpus projection, Canonical Registry behavior, Work Intelligence, CLI behavior, and browser workflows.

The design prefers **unknown / unresolved / review-required** over fabricated certainty and treats provenance or authority violations as correctness failures rather than presentation details.

## Product direction

The long-term loop remains:

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

The target-scoped Market substrate, durable bounded analytical reports, B2 normalization, and bounded factual comparison are accepted in their respective scopes. The comparison stage is engineering-closed; the next candidate concerns concrete job-specific capability expectations. Promoted families/archetypes, persistent capability profiles, Market v2, trends, and personal comparison retain their separate gates.

The October 26 evaluation and bounded browser slice follow the post-B2 capability-profile direction before promoted P2.2C. Strategy A preserves all 175 target claims without compaction. Optional Capability grouping is available only on the five older anchors and has overlapping claim support. The implemented browser retains factual fallback and distinct counts; no new inference or persistent profile state was introduced. See `docs/working-memory/2026-10-26_B2_CLOSURE_AND_P2_3A_BOUNDED_BROWSER_DECISION.md` for evidence and limits.

## License

JobHunter is licensed under the [MIT License](LICENSE).
