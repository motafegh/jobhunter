# Phase 1 — Jobinja Workflow Automation Plan

**Status:** Active implementation/acceptance plan  
**Date:** 2026-08-08  
**Scope:** Phase 1  
**Primary source:** Jobinja (`https://jobinja.ir/`)  
**Branch policy:** Work directly on `main` unless a concrete isolation need appears.

This document is subordinate to:

1. product/domain/source/architecture constraints;
2. `docs/ROADMAP.md` for strategic sequencing;
3. `docs/IMPLEMENTATION_PLAN.md` for product-level delivery order.

`docs/EXECUTION_TODO.md` is the current working checklist. `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md` is the focused sub-plan for the currently active semantic-quality acceptance tranche.

---

## 1. Objective

Replace the old manual workflow:

```text
manual search
→ open job
→ copy text
→ send to AI
→ manually compare outputs
```

with a repeatable local pipeline:

```text
configured bilingual Jobinja coverage
→ bounded repeat-safe acquisition
→ immutable evidence
→ deterministic source structure/version/check history
→ hardened English projection
→ strict factual semantic extraction
→ bounded per-job reasoning review
→ truthful individual/aggregate outputs
```

Browser is the normal human interface. CLI remains the advanced/automation/debug interface. Both use the same services and durable state.

---

## 2. Final intended Phase-1 run

A complete Phase-1 run should:

1. load configured bilingual search coverage;
2. construct a bounded request plan;
3. acquire search pages and preserve evidence;
4. discover stable Jobinja identities repeat-safely;
5. select missing/refresh-due details;
6. acquire/classify detail responses and preserve valid evidence;
7. parse source-explicit fields deterministically;
8. create/reuse semantic source versions;
9. retain source-check/lifecycle observations;
10. create/reuse current English projection v2;
11. select current analysis-ready jobs;
12. run bounded current P1.6 English analysis;
13. validate evidence/semantics;
14. persist derived artifacts/attempts;
15. update per-job and first Market outputs;
16. expose equivalent browser/CLI behavior;
17. report requested/attempted/completed/reused/skipped/failed/remaining work honestly.

Capability Intelligence, Blueprint, and Review Snapshots are bounded review/acceptance layers around P1.6. They are not yet automatic corpus-wide Phase-1 stages.

---

## 3. Current dependency flow

```text
bilingual TOML search catalog
        ↓
bounded search plan
        ↓
Jobinja acquisition
        ↓
raw immutable evidence
        ↓
logical JobPosting + discovery provenance
        ↓
missing / refresh-due selection
        ↓
detail response classification
        ↓
Jobinja parser v2
        ↓
semantic source version
        ↓
fetch observation + lifecycle evidence
        ↓
current English projection v2
        ↓
P1.6 English v4 factual extraction
        ↓
first Market aggregation

reviewed per-job branch:
P1.6
→ Capability Intelligence v4
→ Role Capability Blueprint v2
→ Review Snapshot v1
```

Google Cloud Translation remains optional external processing, not a normal dependency.

---

## 4. Current active contracts

```text
parser:                       jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2

P1.6 English prompt/runtime:  job-analysis-english-v4
P1.6 Original prompt/runtime: job-analysis-original-v4
P1.6 schema:                  job-analysis-v2

Capability prompt/runtime:    job-capability-intelligence-v4
Capability schema:            job-capability-intelligence-v2

Blueprint prompt/runtime:     role-capability-blueprint-v2
Blueprint schema:             role-capability-blueprint-v1

Review Snapshot:              job-review-snapshot-v1
```

Historical contracts remain preserved and non-current under changed prompt/runtime identity.

---

## 5. Source/search boundary

Search vocabulary is versioned TOML data, not career taxonomy.

Approved current source behavior:

- public Jobinja search/job URLs only;
- bounded requests/pages/details;
- sequential/rate-limited acquisition;
- approved host/path validation;
- immutable source evidence;
- no login automation;
- no CAPTCHA/access-control bypass;
- no proxy/identity rotation to defeat limits;
- no private applicant/recruiter scraping;
- no automated applications/messages.

Critical invariant:

```text
source/provider failure
!=
valid empty result
```

---

## 6. Durable record boundaries

Keep separate:

```text
JobPosting
SearchPageSnapshot
JobPostingVersion
JobDetailFetchObservation
JobLifecycle state/events
JobTranslationArtifact / Attempt
JobAnalysisArtifact / Attempt
Capability Intelligence Artifact / Attempt
Role Blueprint Artifact / Attempt
JobUserWorkflow
Browser WebOperation
Review Snapshot export
```

Review Snapshots are generated repository-review artifacts. They are **not** runtime inputs and do not replace SQLite/raw evidence.

---

## 7. Source classification/lifecycle

Current response/failure classes include:

```text
active
rate_limited
access_denied
challenge
auth_required
not_found
gone
server_error
network_error
unexpected_page
expired_explicit
```

Retry only explicitly transient classes within bounds.

Required lifecycle truth:

```text
500/502/503/504 != expired/removed
network failure   != expired/removed
rate limit        != expired/removed
challenge/auth    != vacancy gone
```

First missing/gone evidence remains cautious; destructive lifecycle conclusions follow the defined repeated/strong evidence policy.

---

## 8. Parser boundary

`jobinja-detail-v2` deterministically extracts source-explicit fields and complete relevant text.

Missing stays missing.

Source skill tags remain distinct from description-derived semantic claims.

Parser metadata such as `language` and `parser_version` is not employer evidence.

Parser audit checks structure/contamination only; it is not semantic certification.

---

## 9. Translation v2 boundary

Translation v1 remains historical after real field-association corruption was observed.

Current path:

```text
current parsed source version
→ semantic source segments
→ native-English identity OR bounded local translation
→ structured output validation
→ deterministic integrity checks
→ english-projection-v2 artifact
```

Rules:

- source evidence never changes because translation succeeds/fails;
- native English passes through without model translation;
- Persian-containing units translate through isolated provider calls;
- v1 is never silently relabeled;
- corrupt/malformed output fails rather than becoming current.

---

## 10. P1.6 factual semantic boundary

Current P1.6 is v4.

```text
English projection
→ job-analysis-english-v4
→ job-analysis-v2 persisted facts
```

Original-language analysis remains independent:

```text
original source
→ job-analysis-original-v4
→ job-analysis-v2
```

Current v4 protections include:

- evidence-reference IDs in production;
- heading-aware long-description segmentation;
- clause-level evidence references;
- exact source-text resolution before persistence;
- rich-source empty-analysis rejection;
- mixed-strength atomicity rules;
- source preference wording required for `preferred` claims;
- obligation strength separated from technical depth;
- no arbitrary read deadline for long local generation after connection;
- bounded Instructor retry and fail-closed final validation.

P1.6 remains factual. It must not manufacture a technical curriculum merely because a technology is named.

### Current acceptance issue

`tG9K` proved that long-posting mechanics now work, but factual quality still needs focused work on:

- complete explicit requirement coverage;
- global stack optionality;
- explicit depth preservation;
- structured experience/education participation;
- avoiding depth propagation from one technology to neighboring stack items.

This is the immediate semantic-quality target before further downstream calibration.

See `docs/SEMANTIC_ANALYSIS.md` and `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`.

---

## 11. Bounded Capability/Blueprint acceptance branch

These layers exist because strict factual extraction and useful career interpretation have different uncertainty contracts.

```text
accepted English P1.6
→ Capability Intelligence v4
→ Role Capability Blueprint v2
```

They are manually reviewed per job and excluded from current automatic Market aggregation.

Current live examples:

```text
t4jp  sparse/ambiguous source case
tG9K  rich semiconductor/industrial-ML case
```

`tG9K` is committed as a repository review artifact:

```text
review-snapshots/jobs/tG9K.json
```

CI-3 remains open. Review materially different Python/software, network/security, and operations/platform jobs before promotion.

---

## 12. Review Snapshot workflow

Normal command:

```bash
jobhunter jobs snapshot <job-id>
```

Default output:

```text
review-snapshots/jobs/<job-id>.json
```

The live SQLite database remains local/ignored.

Snapshots intentionally include public source + current review-relevant derived artifact chain and exclude raw model protocol, HTML contents, secrets, SQLite internals, and future private user state.

### Known defect before model comparison

The integrated `jobhunter jobs snapshot` CLI currently does not pass effective model-role arguments into the exporter. The standalone exporter does.

Fix the integrated routing before comparing multiple Capability/Blueprint models, then regenerate `tG9K` so `configured_models` is explicit.

---

## 13. User triage and acquisition priority

User workflow remains separate from source truth:

```text
unreviewed
interested
review_later
reviewed
not_relevant
```

`not_relevant` may affect automatic fetch priority but never deletes source history.

Acquisition priority is not fit/readiness/recommendation.

---

## 14. First Market layer

Current Market aggregates accepted/current **English P1.6** artifacts under the selected contract.

It does not aggregate Capability or Blueprint yet.

Before Phase-1 Market acceptance:

- expose exact analyzed-current sample size;
- preserve source/filter scope;
- keep requirement-strength semantics honest;
- warn on small/concentrated samples;
- avoid duplicate claim inflation when metric semantics are per-job;
- keep coverage and quality distinct.

---

## 15. Partial-success semantics

For multi-stage workflows expose where applicable:

```text
requested
attempted
completed
reused
skipped intentionally
failed
remaining eligible
```

Valid earlier durable work remains even if a later stage fails.

`no eligible work` is not `attempt failed`.

Browser and CLI must agree on the underlying semantics.

---

## 16. Current delivery state

| Increment | State |
|---|---|
| P1.0 repository alignment | Accepted foundation; current docs being reconciled again after semantic v4 work |
| P1.1 discovery | Accepted foundation |
| P1.2 bounded repeat-safe discovery | Accepted foundation |
| P1.3 detail acquisition | Core implemented; remaining failure/lifecycle acceptance pending |
| P1.4 parser | Accepted foundation |
| P1.4 translation v2 | Implemented and actively used; broader corpus/model quality still bounded by acceptance scope |
| P1.5 semantic versions/observations | Accepted foundation |
| P1.5 lifecycle/triage/priority | Implemented; remaining acceptance pending |
| P1.6 factual analysis v4 | Implemented; semantic-quality acceptance active |
| Capability Intelligence v4 | Implemented bounded per-job slice; CI-3 open |
| Role Blueprint v2 | Implemented bounded per-job slice; semantic-quality acceptance open |
| Review Snapshot v1 | Implemented; first live pushed example works; integrated model-routing defect open |
| P1.7 Market/run/reporting | Partial implementation / closure acceptance pending |

---

## 17. Current exact execution order

Do not restart the old August-3 checklist from the beginning. Continue from the current repository state:

```text
1. fix integrated Review Snapshot effective-model routing
2. run deterministic gate
3. harden P1.6 coverage / obligation / depth on tG9K
4. rebuild/review tG9K P1.6
5. calibrate/rebuild Capability
6. calibrate/rebuild Blueprint
7. compare a stronger dedicated reasoning model if Gemma remains inadequate
8. complete CI-3 representative review using snapshots
9. stop expanding the semantic slice once accepted
10. return to Market/source/lifecycle/partial-success/P1.7 closure
11. close Phase 1
12. only then begin corpus-wide Phase 2
```

The operational details live in `docs/EXECUTION_TODO.md`.

---

## 18. Phase-1 closure after semantic acceptance

Remaining closure areas include:

- Market sampling/concentration truthfulness;
- source failure/lifecycle regression/live acceptance;
- last-successful/consecutive-failure visibility;
- explicit partial-success result semantics;
- final per-job/report links;
- current-corpus report;
- final bounded `jobhunter run` acceptance;
- browser equivalent acceptance;
- rerun/idempotency evidence;
- accepted-state documentation.

---

## 19. Explicit non-claims

Phase 1 is not complete.

JobHunter does not yet claim:

- complete lifecycle/repost resolution;
- production-quality semantic extraction across all roles;
- production-quality Capability/Blueprint reasoning across all roles;
- canonical Phase-2 taxonomy;
- corpus-wide inferred capability aggregation;
- full-market truth from a bounded Jobinja sample;
- reviewed personal evidence/gaps/readiness;
- career/application recommendations;
- arbitrary-web ingestion;
- generic source-plugin platform;
- autonomous applications;
- evaluated RAG/agent authority.
