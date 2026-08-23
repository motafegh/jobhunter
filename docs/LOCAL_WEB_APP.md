# JobHunter Local Web Application

**Status:** Current browser architecture/surface guide  
**Date:** 2026-08-23

## 1. Purpose

The local web application is the normal human-facing interface for repeated JobHunter use.

CLI remains available for automation, debugging, tests, acceptance work, and advanced operation.

The browser is a **second interface over the same application services and SQLite/evidence state**. It does not maintain separate parsers, translations, analyses, Capability/Blueprint truth, public-corpus truth, or user data.

---

## 2. Launch

Install/update the editable package:

```bash
python3 -m pip install -e ".[dev]"
```

Launch:

```bash
jobhunter-app
```

Default:

```text
http://127.0.0.1:8765/
```

Repeated launch while the same local instance is already bound should reopen/use that instance rather than creating a second server.

Linux desktop launcher:

```bash
jobhunter-app --install-desktop
```

The desktop entry stores the resolved config path and working directory used at installation.

---

## 3. Network/security boundary

The app binds loopback by default. Non-loopback binding requires explicit intent.

Browser safeguards include:

- CSRF validation for mutating forms;
- restrictive Content Security Policy;
- `X-Frame-Options: DENY`;
- `X-Content-Type-Options: nosniff`;
- `Referrer-Policy: no-referrer`;
- `Cache-Control: no-store`;
- packaged local static assets;
- no runtime CDN requirement;
- acquired job content treated as untrusted data;
- source/model operations still governed by service/config bounds.

The browser must never become a source-policy bypass.

---

## 4. Current main screens

```text
Overview
Jobs
Job detail
Capability Intelligence
Role Capability Blueprint   # experimental/non-authoritative
Search plan / search effectiveness
Market
Operations
System
```

Browser and CLI must render/use the same underlying current artifacts and effective model-role identities.

---

## 5. Overview

Overview provides current corpus/pipeline visibility and bounded operational actions.

Typical information includes:

- discovered jobs;
- fetched/parsed detail coverage;
- current English coverage;
- current P1.6 coverage;
- recent acquisition/workflow operations;
- missing/eligible work;
- important runtime/model/config state where useful.

Important coverage terminology must remain honest:

```text
known/discovered jobs != fetched/parsed detail jobs
```

The repository public corpus currently has an accepted projection baseline of 353 known/discovered jobs, 43 fetched/parsed detail jobs, and 20 current English v2 projections. Those numbers are not interchangeable; preserved historical English v1 artifacts are not current.

### Sync controls

The browser exposes visible acquisition bounds instead of hiding them in implementation defaults. Presets fill forms; they do not create hidden behavior.

---

## 6. Jobs

The jobs catalog is a local read over persisted state.

Filters/search may use human-readable title/company/location/reference plus source/English/analysis/lifecycle/user-workflow state.

Browsing/filtering local jobs does not itself contact Jobinja.

Opaque Jobinja IDs remain stable provenance but visually secondary to role/company information.

### Quick Add

Quick Add accepts only:

1. public Jobinja job URL;
2. public Jobinja `/jobs` search URL;
3. Persian/English keyword/role phrase interpreted as a bounded Jobinja search.

It exposes explicit search/detail bounds and is not arbitrary-web ingestion.

---

## 7. Job detail and semantic actions

Job detail keeps authority layers visually separate.

Current sections can include:

```text
original authoritative source data
English projection v2
English P1.6 factual analysis
Original-language P1.6 analysis
Capability Intelligence v9
experimental Blueprint review
source/discovery/lifecycle provenance
semantic/raw evidence identity
user triage state
actions for refresh/translation/analysis/reasoning
```

A discovered-but-unfetched job is a normal actionable state, not an application error.

Source and English/model-derived content must not be visually conflated.

Current semantic actions:

```text
Analyze English
Analyze Original
Capability Intelligence
Role Capability Blueprint   # experimental only
```

Current contracts:

```text
English P1.6:   job-analysis-english-v20 / job-analysis-v5
Original P1.6:  job-analysis-original-v9 / job-analysis-v4
Capability:     job-capability-intelligence-v9 / job-capability-intelligence-v5
Blueprint:      role-capability-blueprint-v6 / role-capability-blueprint-v5
```

English and Original P1.6 remain independent.

Capability v9 depends on current accepted/current English P1.6 selected through the neutral public service facade.

Blueprint is **not** rebased onto current Capability v9. During Phase 1, Blueprint v6 remains pinned to historical Capability v7 dependency semantics and is non-current on the accepted v9 anchor chains. The UI must not imply that a Blueprint is the authoritative next stage after current Capability.

A stale or dependency-incompatible downstream artifact must not render as current.

---

## 8. Capability Intelligence page

Capability Intelligence v9 is the accepted/current bounded reasoning layer above accepted English P1.6.

The page should make the authority split visible:

```text
P1.6/source truth                         strict
Capability grouping/source bookkeeping   deterministic/strict
planner prose                             non-authoritative
optional model enrichment                 subordinate/fail-closed
```

Useful review information includes:

- capability groups and neutral summaries;
- complete linked source requirements/responsibilities;
- deterministic source requirement strength;
- deterministic source-explicit depth;
- role-level constraints separated from capability requirements;
- bounded optional inferred/prerequisite/context/depth/unknown reasoning where present;
- exact source provenance;
- model/prompt/schema/dependency identity.

The page remains a manually reviewable per-job surface. Capability is not yet automatically aggregated into current Market.

---

## 9. Role Capability Blueprint page

Blueprint v6/v5 is retained for **experimental/non-authoritative research inspection**.

The UI must clearly communicate:

- it is not an accepted Phase-1 decision layer;
- mechanical/current-chain status is not semantic acceptance;
- current public Capability v9 does not automatically make Blueprint current;
- Blueprint v6 remains pinned to historical Capability v7 dependency semantics;
- it must not feed Market, personal readiness, recommendations or application truth.

The Phase-1 experiment showed that even mechanically valid uncertainty/consideration prose could smuggle unsupported architecture/topology/lifecycle assumptions. Do not present Blueprint output with stronger visual authority than accepted source/P1.6/Capability source truth.

---

## 10. Search plan / effectiveness

Search views expose configured bilingual acquisition coverage and observed search contribution/overlap.

Search vocabulary is acquisition recall, not canonical career taxonomy or personal relevance.

Do not auto-prune vocabulary solely because two searches overlap.

---

## 11. Market

Current Market aggregates accepted/current **English P1.6** only.

It does not yet aggregate Capability or Blueprint.

Market must retain/expose enough context to understand:

- analyzed-current sample size;
- source/filter scope;
- current analysis contract;
- requirement-strength semantics;
- concentration/small-sample warning state.

Coverage is not semantic-quality certification. Market truthfulness is accepted; current P1.7 work preserves that scope and warning contract.

---

## 12. Operations and public-corpus synchronization

Long browser work uses bounded in-process execution rather than a distributed queue system.

Current design avoids overlapping mutable browser workflows until concurrency is proven safe.

Durable domain results live in SQLite/evidence/artifact stores. Operation cards are runtime convenience only.

Completed mutating browser operations use the shared post-success public-corpus projection hook:

```text
durable SQLite/domain work
→ public corpus synchronization
```

If corpus synchronization fails, durable SQLite work remains preserved and the browser operation surfaces the projection failure. The projection never rolls back durable work.

### Result semantics

Multi-stage operation summaries should preserve where applicable:

```text
requested
attempted
completed
reused
skipped intentionally
failed
remaining eligible
```

Do not display generic success when meaningful requested sub-work failed.

Earlier valid durable work remains preserved when later stages fail.

---

## 13. System

System exposes important current runtime/config boundaries, for example:

- SQLite/evidence/export paths;
- LM Studio URL;
- translation model/provider;
- effective analysis model;
- effective Capability model;
- effective Blueprint model;
- acquisition limits;
- translation/analysis limits;
- corpus coverage/state.

Advanced persistent configuration remains in `jobhunter.toml` until a safe configuration-write design is justified.

---

## 14. Independent model roles

Current configuration can independently select:

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

Browser artifact readers must use the appropriate effective model role and must not assume all semantic/reasoning work uses the analysis model.

---

## 15. Review Snapshot workflow

Review Snapshots are produced through the shared CLI/service path rather than a browser-only hidden export:

```bash
jobhunter jobs snapshot <job-id>
```

They are selected repository-safe semantic-review evidence, not runtime state and not the complete public dataset.

Current accepted anchor snapshots are `tG9K` and `t4jp`; their current-chain flags resolve Capability v9 artifacts 11/12 to P1.6 artifacts 36/37 and show Blueprint non-current.

The complete public dataset belongs in `corpus/`.

---

## 16. Dependency strategy

Current browser dependencies remain deliberately small:

- FastAPI;
- Uvicorn;
- Jinja2;
- python-multipart;
- packaged CSS;
- small vanilla JavaScript.

Do not add Node/npm/React merely for fashion. Introduce a frontend build system only when server-rendered Python demonstrably stops meeting product needs.

---

## 17. Failure model

A browser operation failure does not roll back previously preserved source evidence, semantic versions, successful translations, accepted P1.6 artifacts, Capability artifacts, or other earlier durable work.

Keep distinct:

```text
source failure
translation failure
P1.6 failure
Capability failure
Blueprint failure
public-corpus projection failure
```

A later failure does not retroactively invalidate a correct upstream artifact.

A mechanically completed model artifact can still fail manual semantic acceptance. In the active heterogeneous gate, a rejected P1.6 candidate must not feed Capability even though the underlying operation once completed mechanically.

---

## 18. Testing

Normal deterministic web tests do not contact Jobinja or LM Studio.

Coverage should protect:

- primary page rendering;
- local static assets/security headers;
- CSRF rejection;
- local operation execution/polling;
- empty/discovered/unfetched states;
- Quick Add classification/source rejection;
- loopback launcher behavior;
- semantic action routing;
- current Capability/Blueprint artifact/model selection;
- public-corpus post-success hook behavior;
- operation partial-success semantics;
- stale/current derived-state display.

Live acceptance separately verifies real Jobinja/model behavior.

---

## 19. Current acceptance status

Browser architecture is established and actively used. A separate browser rewrite is not the active project gate.

Current project sequence:

```text
heterogeneous P1.6/Capability review accepted
→ Market/source/lifecycle accepted
→ partial-success semantics accepted
→ P1.7 report/run/browser accepted
→ Phase-1 closure accepted
→ P2.1 canonical concept registry
```

The focused state lives in:

```text
docs/P1_7_REPORT_RUN_BROWSER_ACCEPTANCE_PLAN.md
docs/EXECUTION_TODO.md
docs/WORKING_MEMORY.md
```
