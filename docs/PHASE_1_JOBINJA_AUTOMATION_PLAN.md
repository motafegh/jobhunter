# Phase 1 — Jobinja Workflow Automation Plan

**Status:** Active implementation/acceptance plan  
**Date:** 2026-08-21  
**Scope:** Phase 1  
**Primary source:** Jobinja (`https://jobinja.ir/`)  
**Branch policy:** Work directly on `main` unless the repository owner explicitly changes this rule or a concrete isolation need is agreed first.

This document is subordinate to:

1. product/domain/source/architecture constraints;
2. `docs/ROADMAP.md` for strategic sequencing;
3. `docs/IMPLEMENTATION_PLAN.md` for product-level delivery order.

`docs/EXECUTION_TODO.md` is the current working checklist. `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md` is the focused sub-plan for the active semantic-quality acceptance tranche.

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
→ bounded per-job Capability Intelligence
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
12. run bounded current English P1.6 v20 analysis;
13. validate evidence/semantics and persist current artifacts/attempts;
14. allow bounded current Capability v9 generation only above accepted/current English P1.6;
15. update per-job and first Market outputs;
16. refresh the repository-safe local `corpus/` projection after durable mutating work;
17. expose equivalent browser/CLI behavior;
18. report requested/attempted/completed/reused/skipped/failed/remaining work honestly.

Capability Intelligence is an accepted bounded per-job Phase-1 reasoning layer but is not yet an automatic corpus-wide Market stage. Blueprint remains experimental/deferred. Review Snapshots and the public corpus are repository projections, not runtime authorities.

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
jobinja-detail-v2
        ↓
semantic source version
        ↓
fetch observation + lifecycle evidence
        ↓
english-projection-v2
provider: lm-studio-translation-v2
        ↓
English P1.6 v20/v5 factual extraction
        ↓
Capability Intelligence v9/v5 (bounded per-job accepted layer)
        ↓
first Market aggregation still reads accepted/current English P1.6 only

repository-safe projections:
current public state → jobhunter-public-corpus-v1
selected review evidence → job-review-snapshot-v1

experimental/deferred:
historical Blueprint-compatible accepted chain
→ Role Capability Blueprint v6/v5
```

Google Cloud Translation remains optional external processing, not a normal dependency.

---

## 4. Current active contracts

```text
parser:                       jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:           english-projection-v2

P1.6 English prompt/runtime:  job-analysis-english-v20
P1.6 English schema:          job-analysis-v5
P1.6 Original prompt/runtime: job-analysis-original-v9
P1.6 Original schema:         job-analysis-v4

Capability prompt/runtime:    job-capability-intelligence-v9
Capability schema:            job-capability-intelligence-v5

Blueprint prompt/runtime:     role-capability-blueprint-v6
Blueprint schema:             role-capability-blueprint-v5
Blueprint disposition:        deferred / non-authoritative / historical-v7-pinned

Review Snapshot:              job-review-snapshot-v1
Public Corpus:                jobhunter-public-corpus-v1
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

## 6. Durable record and projection boundaries

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
Market aggregate
Public Corpus projection
Review Snapshot export
Raw evidence
```

Runtime/history authority:

```text
data/jobhunter.sqlite3
+ local raw evidence
```

Repository projections:

```text
corpus/            complete current repository-safe public dataset
review-snapshots/  selected semantic-review evidence
```

Neither repository projection replaces SQLite or becomes a runtime write authority.

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
- corrupt/malformed output fails rather than becoming current;
- translation is derived convenience data and may block downstream analysis when materially mistranslated during review.

The first heterogeneous candidate `tI1n` is a concrete example of a source whose English projection was manually blocked from P1.6 because a material source phrase was mistranslated. That evidence is a translation-quality issue, not permission for P1.6 to compensate for bad upstream meaning.

---

## 10. P1.6 factual semantic boundary

Current public English P1.6 is:

```text
English projection
→ job-analysis-english-v20
→ job-analysis-v5 persisted facts
```

Original-language analysis remains independent:

```text
original source
→ job-analysis-original-v9
→ job-analysis-v4
```

Current v20/v5 protections include:

- evidence-reference IDs and exact source-text resolution before persistence;
- source-led bounded partitions so one repair cannot silently replace another valid partition;
- rich-source complete requirement/responsibility accounting;
- structured source-skill survival;
- mixed-strength atomicity rules;
- source preference wording required for `preferred` claims;
- obligation strength separated from technical depth;
- concept-specific explicit depth and experience-extent handling;
- qualification-vs-duty separation;
- fail-closed evidence/ontology/decomposition rules;
- no arbitrary read deadline for valid long local generation after connection;
- bounded validation retries;
- deterministic final reconciliation.

Accepted opposite-end anchors:

```text
tG9K artifact 36 — 33 requirements / 8 responsibilities / 0 role purpose
t4jp artifact 37 —  8 requirements / 0 responsibilities / 0 role purpose
```

Both are accepted/current under v20/v5.

### Heterogeneous hardening already learned from `tmBK`

The first Python/software anchor `tmBK` (detail 44, English projection 38) has exposed real repeatable v20 edge cases:

- `Sufficient knowledge` is a valid explicit employer depth phrase; plain `knowledge` remains non-depth.
- Multi-level evidence cannot canonicalize every concept to the first marker; supplied item-specific depth is preserved.
- If multi-level evidence has no item-specific depth signal, validation fails closed rather than borrowing another concept's marker.
- `Ability to effectively use AI ...` expresses application/manner, not technical depth; the exact signal is cleared only when its evidence contains no genuine depth marker.
- A coverage reference already positively extracted cannot also remain as a redundant exclusion for the exact same reference.

The first persisted `tmBK` P1.6 artifact 38 was semantically rejected because Linux, SQL/NoSQL, OOP/modular design, and locking/concurrency/transactions inherited `Mastery` incorrectly. It must not feed Capability. No downstream Capability artifact was created from it.

The heterogeneous gate is closed: Python/software `tmBK` uses P1.6 39 → Capability 13; network/security `t4qV` uses 44 → 14; operations/platform `tmyX` uses 46 → 15. Rejected artifacts remain archived evidence. Fresh v20 output persists as `pending`; explicit accept/reject records the decision, and only accepted output can feed Capability, Market, accepted browser counts, or the public corpus.

P1.6 remains factual. It must not manufacture a technical curriculum merely because a technology is named.

See `docs/SEMANTIC_ANALYSIS.md` and `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`.

---

## 11. Capability Intelligence v9 boundary

Capability v9 is the accepted/current bounded per-job reasoning layer above accepted English P1.6.

Architecture:

```text
accepted P1.6 source truth
→ compact semantic capability-group plan
→ bounded exact source-fact assignment
→ bounded optional per-group reasoning
→ deterministic source-link injection
→ deterministic reconciliation
→ persisted Capability v9/v5
```

Authority split:

```text
AUTHORITATIVE SOURCE TRUTH → STRICT
PLANNER PROSE              → NON-AUTHORITATIVE / NORMALIZE
MODEL SOURCE-TRUTH ECHO    → REDUNDANT / FILTER
OPTIONAL MODEL ENRICHMENT  → OPTIONAL + FAIL-CLOSED
```

Accepted/current artifacts:

```text
tG9K → P1.6 36 → Capability 11
t4jp → P1.6 37 → Capability 12
```

Permanent rules include complete capability-relevant requirement/responsibility coverage, deterministic source strength/depth/work, role-level education/duration-only experience separation, anti-collapse protection on dense sources, optionality protection, and blocking/filtering of unsupported ownership/lifecycle/autonomy/architecture claims.

Capability v9 promotion is operationally closed, but heterogeneous review must still prove that the promoted behavior generalizes across materially different role families before the stack is frozen as Phase-2 input.

Do not run Capability for a heterogeneous anchor until that anchor's current P1.6 artifact has been manually accepted.

---

## 12. Blueprint and Review Snapshot boundaries

### Blueprint

Blueprint v6/v5 is implemented for research/inspection but is **deferred and non-authoritative** during Phase 1.

It remains pinned to historical Capability v7 semantics and must not feed Market, personal readiness, recommendations, or other authoritative decisions.

Do not create Blueprint v7 or resume nearby tuning during the current heterogeneous gate.

### Review Snapshot

Normal command:

```bash
jobhunter jobs snapshot <job-id>
```

Default output:

```text
review-snapshots/jobs/<job-id>.json
```

Snapshots intentionally include public source + current review-relevant derived chain and exclude raw model protocol, HTML contents, secrets, SQLite internals, and future private user state.

Current-chain status proves dependency currentness, not semantic acceptance.

---

## 13. Complete public corpus

The public-corpus gate is **operationally closed**.

Contract:

```text
jobhunter-public-corpus-v1
```

Accepted real publication baseline:

```text
Known/discovered jobs:       344
Fetched/parsed job details:   43
English projections:          33
English P1.6:                  5
Original P1.6:                 0
Capabilities:                  5
```

Important interpretation:

```text
344 known/discovered jobs != 344 fully fetched advertisements
```

Discovery-only identities remain useful with `current_detail: null`; only fetched/parsed jobs are eligible heterogeneous anchors.

Normal mutating CLI and completed browser operations refresh local `corpus/` after durable SQLite work. Projection failure surfaces but never rolls back SQLite. Git commit/push remains explicit.

---

## 14. User triage and acquisition priority

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

## 15. First Market layer

Current Market aggregates accepted/current **English P1.6** artifacts under the selected current contract.

It does not aggregate Capability or Blueprint yet.

Before Phase-1 Market acceptance:

- expose exact analyzed-current sample size;
- preserve source/filter/contract scope;
- keep requirement-strength semantics honest;
- warn on small/concentrated samples;
- avoid duplicate claim inflation when metric semantics are per-job;
- keep coverage and quality distinct.

---

## 16. Partial-success semantics

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

## 17. Current delivery state

| Increment | State |
|---|---|
| P1.0 repository alignment | Accepted foundation; current docs reconciled with promoted semantic stack |
| P1.1/P1.2 discovery | Accepted foundation |
| P1.3 detail acquisition | Core implemented; source/lifecycle acceptance closed |
| P1.4 parser | Accepted foundation |
| P1.4 translation v2 | Implemented/current; heterogeneous translation quality remains reviewable per anchor |
| P1.5 semantic versions/observations | Accepted foundation |
| P1.5 lifecycle/triage/priority | Implemented; source/lifecycle acceptance closed |
| P1.6 English v20/v5 | Promoted/current; dense+sparse plus three heterogeneous families accepted |
| Capability Intelligence v9/v5 | Promoted/current; dense+sparse plus three heterogeneous families accepted |
| Role Blueprint v6/v5 | Implemented experimental; Phase-1 deferred/non-authoritative |
| Review Snapshot v1 | Accepted current-chain routing |
| Public Corpus v1 | Implemented, populated, verified, published, remotely available |
| P1.7 Market/run/reporting | Partial implementation / closure acceptance pending |

---

## 18. Current exact execution order

Do not restart historical semantic-calibration checklists. Continue from the actual repository state:

```text
1. preserve accepted heterogeneous chains: tmBK 39→13, t4qV 44→14, tmyX 46→15
2. preserve accepted Market truthfulness/sampling behavior
3. preserve accepted source/lifecycle behavior
4. complete partial-success semantics
5. complete P1.7 report/run/browser acceptance
6. close Phase 1
7. only then begin corpus-wide Phase 2
```

The operational details live in `docs/EXECUTION_TODO.md`.

---

## 19. Phase-1 closure after semantic acceptance

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

## 20. Explicit non-claims

Phase 1 is not complete.

JobHunter does not yet claim:

- complete lifecycle/repost resolution;
- semantic acceptance across all target role families;
- canonical Phase-2 taxonomy;
- corpus-wide job capability requirement profiles;
- full-market truth from a bounded Jobinja sample;
- reviewed personal evidence/gaps/readiness;
- career/application recommendations;
- arbitrary-web ingestion;
- generic source-plugin platform;
- autonomous applications;
- evaluated RAG/agent authority;
- authoritative Blueprint reasoning.
