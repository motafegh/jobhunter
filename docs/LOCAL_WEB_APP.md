# JobHunter Local Web Application

**Status:** Current browser architecture/surface guide  
**Date:** 2026-08-08

## 1. Purpose

The local web application is the normal human-facing interface for repeated JobHunter use.

CLI remains available for automation, debugging, tests, acceptance work, and advanced operation.

The browser is a **second interface over the same application services and SQLite/evidence state**. It does not maintain separate parsers, translations, analyses, Capability/Blueprint truth, or user data.

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

The app binds loopback by default.

Non-loopback binding requires explicit intent.

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
Role Capability Blueprint
Search plan / search effectiveness
Market
Operations
System
```

Browser and CLI must render/use the same underlying current artifacts and model-role identities.

---

## 5. Overview

Overview provides current corpus/pipeline visibility and bounded operational actions.

Typical information includes:

- discovered jobs;
- detail/parsed coverage;
- current English coverage;
- current analysis coverage;
- recent acquisition/workflow operations;
- missing/eligible work;
- important runtime/model/config state where useful.

Typical guided actions include bounded sync/detail/translation/analysis work.

### Sync controls

The browser exposes visible bounds instead of hiding them in implementation defaults:

- search terms/searches selected;
- search request budget;
- missing-detail fetch limit;
- refresh-due detail limit;
- refresh age threshold.

Presets fill the form; they do not create hidden behavior.

Combined detail work remains bounded.

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

It exposes explicit search/detail bounds.

Quick Add is not arbitrary-web ingestion.

---

## 7. Job detail

Job detail keeps authority layers visually separate.

Current sections can include:

```text
original authoritative source data
English projection v2
English P1.6 factual analysis
Original-language P1.6 analysis
source/discovery/lifecycle provenance
semantic/raw evidence identity
user triage state
actions for refresh/translation/analysis/reasoning
```

A discovered-but-unfetched job is a normal actionable state, not an application error.

Source and English/model-derived content must not be visually conflated.

### Current semantic actions

```text
Analyze English
Analyze Original
Capability Intelligence
Role Capability Blueprint
```

Current contracts:

```text
English P1.6:   job-analysis-english-v9
Original P1.6:  job-analysis-original-v9
Capability:     job-capability-intelligence-v4
Blueprint:      role-capability-blueprint-v2
```

English and Original P1.6 remain independent.

Capability depends on current accepted English P1.6.

Blueprint depends on current Capability Intelligence.

A stale dependency must not render a downstream artifact as current.

---

## 8. Capability Intelligence page

This page is the auditable reasoning layer above P1.6.

It should expose:

- role interpretation;
- capability areas;
- work activities;
- depth signals;
- sub-capabilities;
- underlying knowledge;
- operational practices/context;
- independence/ownership;
- unknown scope;
- evidence status/confidence;
- exact resolved supporting evidence;
- model/prompt/schema/dependency provenance.

It is still a manually reviewed per-job surface and is not automatically aggregated into Market.

---

## 9. Role Capability Blueprint page

Blueprint is the human-facing professional interpretation layer.

It prioritizes readable explanation over evidence cards while retaining artifact/model/dependency provenance.

Typical sections include:

- senior-practitioner role read;
- likely role shape;
- capability areas/depth;
- likely subskills;
- named/likely/possible tools/examples;
- likely work products;
- operational concerns/failure modes;
- hidden likely requirements;
- end-to-end scenarios;
- probable non-requirements;
- important unknowns;
- bottom line.

The UI should make it clear that this layer is freer professional interpretation, not employer fact.

---

## 10. Search plan / effectiveness

Search views expose configured bilingual acquisition coverage and observed search contribution/overlap.

Search vocabulary is acquisition recall, not canonical career taxonomy or personal relevance.

Do not auto-prune vocabulary solely because two searches overlap.

---

## 11. Market

Current Market aggregates accepted/current **English P1.6** only.

It does not yet aggregate Capability/Blueprint.

Market must retain/expose enough context to understand:

- analyzed-current sample size;
- source/filter scope;
- current analysis contract;
- requirement-strength semantics;
- concentration/small-sample warnings.

Coverage is not semantic-quality certification.

---

## 12. Operations

Long browser work uses bounded in-process execution rather than a distributed queue system.

Current design avoids overlapping mutable browser workflows until concurrency is proven safe.

Durable domain results live in SQLite/evidence/artifact stores. Operation cards are runtime convenience only.

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

Browser artifact readers must use the appropriate effective model role and must not assume all reasoning uses the analysis model.

This was corrected for Capability/Blueprint review pages during the v4/v2 reasoning tranche.

---

## 15. Review Snapshot workflow

Review Snapshots are produced through CLI rather than a browser-only hidden export path:

```bash
jobhunter jobs snapshot <job-id>
```

The resulting selected JSON is intended for Git/reviewer/AI quality inspection, not as runtime state.

Current selected live example:

```text
review-snapshots/jobs/tG9K.json
```

The integrated snapshot CLI passes all effective model roles into the exporter, and the selected `tG9K` snapshot records the configured dependency-correct chain.

See `review-snapshots/README.md`.

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

A browser operation failure does not roll back previously preserved source evidence, semantic versions, successful translations, accepted P1.6 artifacts, Capability artifacts, or Blueprint artifacts.

Each derived stage has its own attempt/history semantics.

Keep distinct:

```text
source failure
translation failure
P1.6 failure
Capability failure
Blueprint failure
```

A later failure does not retroactively invalidate a correct upstream artifact.

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
- Capability/Blueprint artifact/model selection;
- operation partial-success semantics;
- stale/current derived-state display.

Live acceptance separately verifies real Jobinja/model behavior.

---

## 19. Current acceptance status

Browser architecture is established and actively used.

Remaining acceptance belongs mainly to the underlying Phase-1 semantic/source/lifecycle/Market/final-run gates rather than a separate browser rewrite.

The current focused sequence is documented in:

```text
docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md
docs/EXECUTION_TODO.md
```
