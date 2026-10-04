# RoleFamilyIntelligenceReport persistence contract

**Date:** 2026-10-03  
**Status:** R1-R3 ACCEPTED / CLOSED; R4 BOUNDED REAL-LOCAL ACCEPTANCE ACTIVE / AUTHORIZED  
**Owner scope:** Persist the accepted bounded Market candidate interpretation as a local, immutable, reviewable analytical artifact.  
**Predecessor:** `docs/working-memory/2026-09-29_MARKET_CANDIDATE_INTERPRETATION_V1.md`  
**Accepted generator:** `market-role-family-candidate-v6 / market-role-family-candidate-prompt-v6`

## 1. Decision

The snapshot-15 V6 real-model/browser result is accepted for **bounded report generation**.

Observed V6 acceptance evidence:

```text
snapshot:                       15
accepted-semantic core jobs:     6
available P1.6 claims:          175
unique cited claims:             49
work clusters:                    4
multi-posting subfamilies:        1
single-posting specialty:         1
internal C* leakage:              0
integrity rejections:             0
```

The exact review artifact is:

`docs/working-memory/review-artifacts/2026-10-03_snapshot15_candidate_report_v6.html`

V6 restored useful synthesis without reopening the integrity defects found in V3-V5. The candidate-interpretation experiment is therefore closed successfully. There is no V7 repair cycle.

The next authorized increment is persistence and review of the report as a durable **analytical artifact**.

This authorization does **not** authorize:

- canonical role-family taxonomy;
- responsibility-family promotion;
- automatic subfamily promotion;
- broad-market prevalence from six postings;
- personal readiness/gap scoring;
- public-corpus publication of Market reports.

## 2. Authority boundary

Permanent interpretation chain:

```text
immutable MarketCorpusSnapshot
+ exact accepted P1.6 dependencies
        ↓
candidate generator v6
        ↓
application post-validation / normalization
        ↓
immutable RoleFamilyIntelligenceReport
        ↓
append-only human review
```

And explicitly:

```text
reviewed RoleFamilyIntelligenceReport
!= employer fact
!= canonical taxonomy
!= market-wide prevalence
!= automatic promotion
```

The normalized persisted report is the bounded product artifact. Model text has no authority outside the exact cited evidence and application-derived facts attached to it.

## 3. Contract identities

Persistence envelope:

```text
market-role-family-intelligence-report-v1
```

Accepted initial generation dependency:

```text
candidate contract: market-role-family-candidate-v6
prompt:             market-role-family-candidate-prompt-v6
model:              exact configured model ID
```

Review event contract:

```text
market-role-family-report-review-v1
```

The persistence-envelope contract and generation contract are deliberately separate. A later candidate-generation contract may produce a report under a new persistence contract or an explicitly compatible envelope; it must never silently relabel an older artifact.

## 4. Durable domain objects

### 4.1 `MarketRoleFamilyIntelligenceReport`

Immutable completed analytical artifact.

Required identity/provenance:

```text
id
snapshot_id
report_contract_version
candidate_contract_version
prompt_version
model
generation_identity
input_fingerprint
generation_fingerprint
report_sha256
report
request_body
raw_response
created_at
```

Semantics:

- `snapshot_id` references one immutable `MarketCorpusSnapshot`;
- `input_fingerprint` hashes the exact normalized candidate input derived from the snapshot and accepted P1.6 evidence;
- `generation_fingerprint` hashes the input fingerprint plus candidate/prompt/model/generation settings;
- `report_sha256` hashes the normalized post-validation report payload;
- `report` is the only ordinary user-facing semantic payload;
- `request_body` and `raw_response` are local audit/debug evidence and are not ordinary UI content;
- rejected model prose may exist in private raw-response audit data, but must never appear in the normalized report payload;
- numeric counts in the normalized report remain application-derived.

### 4.2 `MarketRoleFamilyReportAttempt`

Append-only execution evidence for completed, failed or reused generation.

Required fields:

```text
id
snapshot_id
attempted_at
report_contract_version
candidate_contract_version
prompt_version
model
generation_identity
input_fingerprint
generation_fingerprint
outcome = completed | failed | reused
artifact_id?
error_type?
error_message?
```

A failed attempt creates no report artifact.

A reused attempt points to the exact reused artifact.

### 4.3 `MarketRoleFamilyReportReview`

Append-only human decision over one immutable report.

Required fields:

```text
id
report_artifact_id
review_contract_version
disposition
note?
reviewed_at
```

V1 dispositions:

```text
accepted_for_bounded_use
rejected
```

No review row means:

```text
pending
```

The latest review event is the effective review state. Older review events remain immutable audit history.

Changing a review decision appends a new event; it never edits the report or prior review.

## 5. Generation identity and reuse

`generation_identity` must contain semantic generation settings, not machine-location details:

```text
provider = lm-studio
model
context_length
max_tokens
seed
structured-schema identity
```

The local endpoint URL is operational configuration and does not define report semantics.

Default product behavior:

1. derive the exact candidate input and `input_fingerprint`;
2. derive `generation_fingerprint`;
3. if an exact report for that generation fingerprint already exists and regeneration was not explicitly requested, reuse it and record a `reused` attempt;
4. explicit regeneration may create another immutable report artifact under the same generation fingerprint;
5. never overwrite an existing report.

Multiple artifacts from the same generation fingerprint are allowed because local model inference is not assumed bit-deterministic. Review chooses which artifact is accepted for bounded use.

## 6. Persistence schema direction

Use local SQLite only.

Recommended dedicated owner:

`src/jobhunter/market_role_family_report_store.py`

This keeps `market_store.py` focused on target/run/membership/snapshot/aggregate authority while the report store owns model-derived report history.

Tables:

```text
market_role_family_reports
market_role_family_report_attempts
market_role_family_report_reviews
```

All completed report rows and review rows are immutable via SQLite update/delete triggers.

Attempts are append-only terminal records; no mutable running row is required for the synchronous local model call.

Foreign keys:

- report → `market_corpus_snapshots(id)`;
- attempt artifact → report;
- review → report.

Indexes should support:

- reports by snapshot newest-first;
- exact generation-fingerprint reuse lookup;
- reviews by report newest-first;
- attempts by snapshot/time.

Do not add Market report tables to public-corpus export.

## 7. Service boundary

Add one shared application service, tentatively:

`market_role_family_report_service.py`

Responsibilities:

```text
snapshot/evidence validation
→ call existing V6 candidate generator
→ persist completed normalized artifact
→ record attempt
→ resolve exact reuse
→ append review event
→ derive effective review state
```

Browser and CLI must use this same service.

Do not create a second semantic generation path.

The existing V6 generator remains the generation/validation owner. Persistence wraps its accepted output.

## 8. Browser workflow

Primary flow:

```text
Market snapshot
→ report history
→ generate/reuse report
→ report detail
→ exact evidence drill-down
→ integrity diagnostics
→ review history
→ Accept for bounded use / Reject
```

Report detail must show:

- exact snapshot;
- persistence and candidate contract identities;
- model/prompt;
- generated time;
- effective review state;
- available vs cited evidence counts;
- work clusters / subfamilies / specialties;
- limitations;
- exact evidence;
- integrity diagnostics;
- review history.

Raw model response/request are not shown by default.

After app restart, report history remains available because it is durable local state.

## 9. CLI workflow

Secondary CLI must expose the same service/state.

Minimum responsibilities:

```text
list reports for snapshot
generate/reuse report
show one report
review one report
```

Exact command spelling is an implementation detail.

No CLI-only semantics.

## 10. Currentness and selection

A report is not globally "current".

Its meaning is exact to:

```text
snapshot
+ input fingerprint
+ report contract
+ candidate contract
+ prompt/model/generation identity
```

UI may identify:

- newest report for a snapshot;
- newest `accepted_for_bounded_use` report for a snapshot.

It must not silently treat a report from an older snapshot as current for a newer snapshot.

A rejected report remains inspectable but must not be selected as the accepted report.

## 11. Failure and integrity rules

Hard failures:

- snapshot missing;
- exact P1.6 dependency mismatch;
- unknown evidence refs;
- persistence fingerprint corruption;
- foreign-key/integrity failure;
- no integrity-safe interpretation survives.

Soft/partial outcomes remain inside the normalized report:

- omitted unsafe generated elements with diagnostics;
- missing responsibility coverage;
- one-posting specialty;
- bounded uncertainty/alternatives.

A generation failure records an attempt but creates no report artifact.

## 12. Review semantics

Human review answers only:

> Is this immutable report useful and sufficiently evidence-grounded for bounded JobHunter Market interpretation?

`accepted_for_bounded_use` means yes for that exact artifact.

It does not mean:

- the labels are canonical;
- role families are promoted;
- every observed market role belongs to one group;
- prevalence is established beyond the snapshot;
- downstream personal scoring may consume it as ground truth.

Any future taxonomy-promotion workflow requires a separate contract and explicit authorization.

## 13. Testing / acceptance

### Tier 1 — deterministic store/service

Must prove:

- report persistence is immutable;
- multiple reports may reference one snapshot;
- exact generation lookup/reuse works;
- explicit regeneration can persist a second artifact;
- report SHA/fingerprints are deterministic;
- failed attempts do not create reports;
- reuse attempts reference the reused report;
- review events are append-only;
- effective review state is latest event;
- rejection never deletes report evidence;
- accepted report selection excludes rejected/pending artifacts as specified;
- snapshot/P1.6 state is not mutated.

### Tier 2 — browser/CLI shared workflow

Must prove:

- browser and CLI see the same persisted report;
- app restart does not lose report history;
- exact evidence links remain resolvable;
- review status/history render correctly;
- raw response is not ordinary report UI;
- no Market report data enters public corpus.

### Tier 3 — bounded real local acceptance

Using snapshot 15:

1. generate/persist one V6 report;
2. verify it survives app restart;
3. verify exact evidence/counts/integrity diagnostics;
4. append owner review;
5. verify browser/CLI effective review state agrees;
6. verify SQLite integrity/foreign keys;
7. verify public corpus unchanged.

## 14. Implementation increments

### R1 — domain + persistence

Implement typed models, tables, immutable triggers, fingerprint helpers, report/attempt/review store APIs, and deterministic tests.

No browser/model call required for R1 tests.

### R2 — service + V6 integration

Wrap the existing candidate generator with persistence/reuse/attempt behavior and review-state resolution.

Keep direct generator logic intact except for the minimum interface needed by the service.

### R3 — shared browser/CLI workflow

Persisted report history/detail/review in browser and equivalent CLI access over the same service.

### R4 — bounded real local acceptance

Run snapshot 15, persist V6, restart, review, verify DB/public-corpus invariants, then close the persistence increment.

## 15. Stop lines

Do not combine this increment with:

- P2.2C responsibility-family promotion;
- P2.2D stable role-archetype promotion;
- `JobCapabilityRequirementProfile`;
- Personal Evidence / Market → You;
- second-source abstraction;
- public Market export;
- vector/RAG/graph/agent infrastructure.

After R4 acceptance, return to the broader Phase-2 semantic plan. The persisted report becomes a durable evidence-linked analytical input, not a shortcut around the remaining semantic work.

## 16. R1 implementation closure — 2026-10-04

R1 is implemented and accepted on commit `bb6ef4af`.

Implementation:

- `src/jobhunter/market_models.py`
  - `MarketRoleFamilyIntelligenceReport`
  - `MarketRoleFamilyReportAttempt`
  - `MarketRoleFamilyReportReview`
  - attempt/review enums and v1 contract constants.
- `src/jobhunter/market_role_family_report_store.py`
  - dedicated local SQLite persistence owner;
  - canonical JSON hashing;
  - input, generation and normalized-report fingerprints;
  - immutable report storage;
  - exact generation-fingerprint reuse lookup;
  - explicit multiple immutable artifacts for regeneration;
  - append-only terminal attempt records;
  - append-only review events;
  - effective review-state resolution;
  - newest effectively accepted report selection;
  - read-time generation/report fingerprint corruption checks.
- `tests/test_market_role_family_report_store.py`
  - deterministic Tier-1 coverage only; no LM Studio/network dependency.

Persistence tables:

```text
market_role_family_reports
market_role_family_report_attempts
market_role_family_report_reviews
```

All three histories reject UPDATE/DELETE through SQLite triggers. Failed attempts cannot reference an artifact. Completed/reused attempts must reference an artifact from the exact same snapshot/generation fingerprint. Explicit regeneration is intentionally permitted under the same generation fingerprint because local model inference is not assumed bit-deterministic.

Generation identity V1 requires:

```text
provider
model
context_length
max_tokens
seed
structured_schema
```

The local endpoint URL remains operational configuration and is excluded from semantic generation identity.

CI run `37217405526` passed:

```text
Ruff                     PASS
pytest                   825 passed
pytest -W error          825 passed
```

R1 acceptance boundary is satisfied. It did not add model calls, browser/CLI routes, public-corpus export or taxonomy promotion.

## 17. Historical R2 authorization gate

At the R1 closure checkpoint, R2 was authorized under the requirements below. Section 18 records its completed acceptance.

R2 must add one shared application service over the existing accepted V6 generator and the R1 store. It must not create a second prompt/schema/generation path.

Required R2 behavior:

1. derive/reuse the exact normalized V6 candidate input used by the generator;
2. derive the semantic generation identity and exact generation fingerprint;
3. ordinary generation:
   - if an exact artifact exists, return the newest artifact;
   - append a `reused` attempt;
   - do not call LM Studio;
4. explicit regeneration:
   - bypass reuse;
   - call the accepted V6 generator;
   - persist a new immutable report even when the generation fingerprint matches an older artifact;
   - append a `completed` attempt;
5. generation failure:
   - append a `failed` attempt with error diagnostics;
   - create no report artifact;
   - re-raise/preserve the failure for the caller;
6. expose review append, effective review state and accepted-report selection through the same service;
7. deterministic tests stub only the candidate generator / inference boundary and require no live LM Studio.

At that checkpoint, R3 browser/CLI and R4 bounded real-local acceptance remained blocked until R2 acceptance.

## 18. R2 implementation closure — 2026-10-04

R2 is implemented and accepted across commits `3423e84e`, `37a98903`, and `0c50bc87`.

Generator integration:

- `PreparedMarketCandidateReport` derives the exact snapshot/P1.6-backed V6 model input before inference;
- semantic generation identity is explicit: provider, model, 16K context, bounded max tokens, seed and structured-schema identity;
- `GeneratedMarketCandidateReport` returns the validated normalized report plus private request/raw-response audit payloads;
- `build_market_candidate_report(...)` remains the compatibility wrapper used by existing callers;
- the accepted V6 prompt/schema/post-validation logic remains one path only.

Shared service:

`src/jobhunter/market_role_family_report_service.py`

Behavior:

```text
ordinary request
→ prepare exact input
→ exact persisted lookup
→ reuse newest match
→ append reused attempt
→ no LM call

explicit regenerate / no reusable artifact
→ accepted V6 generation
→ validate contract + prompt + snapshot + model identity
→ persist immutable normalized report + audit payload
→ append completed attempt

generation/identity failure
→ append failed attempt
→ create no report artifact
→ preserve exception to caller
```

The service also exposes append-only review, effective review state, latest accepted report, report/attempt/review listing, and exact report retrieval over the R1 store.

Deterministic service tests prove:

- one generation followed by ordinary exact reuse calls the generator only once;
- input fingerprint matches the exact prepared candidate payload;
- explicit regeneration creates a second immutable artifact under the same generation fingerprint;
- failed generation records one failed attempt and no report;
- generated snapshot/contract identity mismatch fails before persistence;
- review acceptance/rejection history controls effective state and accepted selection.

CI run `37220490754` passed:

```text
Ruff                     PASS
pytest                   830 passed
pytest -W error          830 passed
```

R2 did not add browser/CLI routes, public-corpus export, live-model CI requirements, or taxonomy promotion.

## 19. Historical R3 authorization gate

At the R2 closure checkpoint, R3 was authorized under the requirements below. Section 20 records its completed acceptance.

R3 must replace the current ephemeral browser/CLI candidate-report ownership with the durable report service/state without creating UI-specific semantics.

Required browser behavior:

1. snapshot page exposes persisted role-family report history and effective accepted report where available;
2. ordinary generate uses exact reuse semantics by default;
3. explicit regenerate is visibly separate from ordinary generate/reuse;
4. report detail is addressed by durable report artifact ID and survives app restart;
5. detail shows persistence/candidate contract identities, model/prompt, generated time, review state/history, available-vs-cited evidence, work clusters/subfamilies/specialties, limitations, exact evidence and integrity diagnostics;
6. append-only Accept for bounded use / Reject review actions use the service;
7. request body/raw model response stay private audit data and are not ordinary report UI.

Required CLI behavior:

1. list persisted reports for one snapshot;
2. generate/reuse by default, with an explicit regeneration option;
3. show one persisted report;
4. append accept/reject review;
5. use the same service and report IDs as the browser.

R3 deterministic acceptance must use one temporary SQLite database and no live LM Studio/network, proving browser/CLI report IDs, persisted payload and effective review state agree, and a fresh app/service instance can still read the same report history.

At that checkpoint, R4 bounded real-local acceptance remained blocked until R3 acceptance.

## 20. R3 implementation closure — 2026-10-04

R3 is accepted/closed.

Primary implementation commit:

`107b0eedf88860b13f29cb06bd3cf14e508392ad`

Compatibility/test follow-ups:

```text
8930032d  preserve frozen snapshot evidence wording
d7f517c0  correct durable browser fixture scope
f3e5b8f1  update Market web tests for guided R3 workflow
```

Dedicated closure record:

`docs/working-memory/2026-10-04_MARKET_R3_DURABLE_WORKFLOW_AND_UX_CLOSURE.md`

Accepted durable workflow:

```text
snapshot
→ persisted report history
→ exact reuse OR explicit regenerate
→ durable report ID/detail
→ append-only owner review
```

Browser and CLI consume the same `MarketRoleFamilyReportService` state. The historical snapshot candidate-report URL is compatibility-only and redirects to the newest durable artifact.

Normal CLI workflow:

```text
jobhunter market role-report list <snapshot_id>
jobhunter market role-report generate <snapshot_id> [--regenerate]
jobhunter market role-report show <report_id>
jobhunter market role-report review <report_id> --disposition ...
```

Private request/raw-response audit payloads remain persisted locally but are absent from ordinary browser/CLI presentation.

R3 also accepts the bounded Market UX direction requested by the owner:

- guide the normal workflow instead of exposing every control equally;
- make the next useful action explicit;
- use progressive disclosure for advanced budgets/history/provenance;
- make snapshot the intelligence hub;
- present the role-family report around review status, findings, evidence and limitations before lower-level identity metadata.

This remains server-rendered FastAPI/Jinja. No SPA/framework expansion was needed.

Final CI run `37223301900`:

```text
Ruff                     PASS
pytest                   830 passed
pytest -W error          830 passed
```

Deterministic R3 acceptance proves persisted report/review durability across a fresh app instance and browser/CLI agreement over the same report ID/state.

## 21. R4 authorization and real-local protocol

R4 is now authorized and is the only active increment in this persistence program.

Use the real maintainer environment and snapshot 15.

Acceptance sequence:

1. sync current `main` and establish a clean working-tree baseline;
2. create a SQLite backup before any R4 generation/review action;
3. record baseline:
   - `PRAGMA integrity_check`;
   - `PRAGMA foreign_key_check`;
   - current snapshot-15 member/analysis identities;
   - current repository-safe public-corpus counts/state;
4. verify the configured LM Studio endpoint `http://127.0.0.1:18080/v1` and accepted analysis model are reachable;
5. start the current app and open snapshot 15 through the redesigned Market workflow;
6. generate/reuse the durable V6 role-family report:
   - ordinary action must reuse an exact persisted generation when available;
   - if no exact artifact exists, it may generate/persist once;
   - explicit regeneration is used only intentionally;
7. inspect the durable report:
   - exact report ID;
   - snapshot/model/contracts;
   - available vs cited evidence;
   - work clusters/subfamilies/specialties;
   - exact cited P1.6 evidence;
   - integrity diagnostics;
   - limitations;
8. stop and restart the app, then prove the same report ID/detail still resolves;
9. prove CLI `role-report list/show` sees the same artifact/payload;
10. append the owner bounded-use review through one surface and prove the same effective review state/history through the other;
11. verify post-run SQLite integrity/foreign keys;
12. verify snapshot/P1.6 upstream identities and repository-safe public corpus are unchanged;
13. record exact evidence and PASS/HOLD/FAIL disposition.

R4 must not:

- introduce another candidate/prompt contract merely to improve output;
- regenerate repeatedly to obtain preferred prose;
- promote generated role labels into canonical taxonomy;
- broaden into responsibility-family/capability-profile implementation;
- publish Market report state into `corpus/`.

A PASS closes the `RoleFamilyIntelligenceReport` persistence increment and returns planning to the broader Phase-2 semantic roadmap.
