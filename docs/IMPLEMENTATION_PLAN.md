# JobHunter Implementation Plan

## 1. Purpose

This is the product-level delivery order. It is not a learning roadmap.

Detailed Phase 1 source/analysis work is controlled by
[Phase 1 — Jobinja Workflow Automation Plan](PHASE_1_JOBINJA_AUTOMATION_PLAN.md).

## 2. Delivery rules

- Build operable vertical slices.
- Keep acquisition usable when LM Studio is unavailable.
- Preserve raw evidence before parsing, translation, or analysis.
- Keep source, translation, model analysis, and personal/user state separate.
- Prefer local-first providers when they satisfy the requirement.
- Keep search coverage data-driven and acquisition bounded.
- Keep failures inspectable/retryable only when their classification permits retry.
- Require deterministic tests before live acceptance.
- Require reviewed live examples before trusting model-derived layers at scale.
- Let the web UI and CLI share application services/database rather than fork logic.
- Add product/UI complexity only where it improves repeated operation.

## 3. Product delivery overview

| Stage | Outcome | Status |
|---|---|---|
| M0 | Runnable local foundation, SQLite, LM Studio boundary, tests | Complete |
| Phase 1 | Full Jobinja workflow through evidence-backed analysis/reporting | Active |
| Phase 2 | Canonical career taxonomy and reliable market matrices | Deferred |
| Phase 3 | Personal capability evidence and gap analysis | Deferred |
| Phase 4 | Explainable actions and application readiness | Deferred |
| Phase 5 | Trends, backup/restore, quality and sustained operation | Deferred |

## 4. Phase 1 increments

| Increment | Outcome | Current state |
|---|---|---|
| P1.0 | Repository alignment and controlling plan | Accepted |
| P1.1 | Search acquisition and persisted Jobinja discovery | Accepted |
| P1.2 | Bounded pagination, multiple searches, repeat-safe discovery | Accepted |
| P1.3 | Detail acquisition, immutable evidence, response classification | Classification/retry implementation pending live acceptance |
| P1.4 | Deterministic parser, multilingual handling, English projection | Parser accepted; hardened translation v2 pending migration/live acceptance |
| P1.5 | Posting identity, versions, lifecycle, triage/prioritization | Semantic versions accepted; lifecycle/triage implementation pending acceptance |
| P1.6 | Evidence-backed local LLM semantic analysis | Implemented; pending deterministic + first reviewed live acceptance |
| P1.7 | Individual/aggregate views and final `jobhunter run` | Partial: job analysis UI + first market view implemented |

## 5. Previously accepted live foundation

Before the current hardening/analysis increment, live evidence established:

- repeat-safe discovery and identical-rerun idempotency;
- a later browser sync with 40/40 search requests, 273 unique postings, 241 new postings,
  32 known postings, and zero search failures;
- bounded detail acquisition with 10/10 selected details succeeding in that browser run;
- 26/26 current parsed jobs structurally clean under parser-v2 audit at that point;
- raw response evidence, semantic versions, and fetch observations remaining distinct;
- data-driven Persian/English search profiles and packs;
- local LM Studio translation, artifact reuse, and bounded output-truncation recovery;
- 15/15 English artifacts under translation v1 before a real field-association defect was
  discovered on later translations;
- local browser application, guided sync controls, Quick Add, concise operation summaries,
  and missing-detail backlog acquisition functioning against the real corpus.

The translation field-association defect is why v1 is now historical rather than trusted
as the current downstream-analysis contract.

## 6. Current hardening and intelligence increment

### 6.1 Hardened English projection v2

`english-projection-v2` and `lm-studio-translation-v2` replace v1 as the current contract.
V1 artifacts are preserved historically; they are not deleted or silently rewritten.

The v2 path:

```text
current parsed source version
→ collect Persian/mixed semantic strings
→ one semantic segment per LM Studio request
→ content-derived response identity
→ structured response validation
→ deterministic source/English integrity audit
→ persist v2 artifact only when clean
```

This intentionally spends more local model calls to remove cross-field permutation risk.
Current English export and P1.6 analysis accept only v2 projections.

### 6.2 Human triage and acquisition priority

User workflow state is separate from employer/source truth:

```text
unreviewed
interested
review_later
reviewed
not_relevant
```

Jobs marked `not_relevant` remain in evidence/history but are excluded from automatic
missing-detail priority selection.

Priority is deterministic acquisition evidence, not career fit. It currently uses:

- number of distinct searches finding the posting;
- number/type of configured search packs finding it;
- conservative title signals relevant to AI/ML/security/Python/platform work.

### 6.3 Classified source checks and cautious lifecycle

Jobinja acquisition now classifies important response conditions including:

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

Only transient network/429/5xx classes receive bounded automatic retry.

Lifecycle transitions are deliberately conservative:

- normal successful detail fetch -> `active`;
- explicit employer/site expiry signal -> `expired`;
- first 404/410 -> `possibly_unavailable`;
- two consecutive 404/410 signals -> `removed`;
- rate limits, access failures, challenges, server failures, and network failures do not
  become destructive lifecycle conclusions.

### 6.4 Search-effectiveness evidence

The Search Plan screen now measures observed acquisition contribution:

- distinct jobs per search;
- distinct search/job/run matches;
- runs in which the search participated;
- unique contributions where a posting was found by only that search in the run.

High overlap is not treated as failure automatically. Cross-domain roles may legitimately
match several terms/packs. JobHunter reports the evidence but does not auto-prune the
catalog.

### 6.5 P1.6 evidence-backed semantic analysis

P1.6 is now implemented as a separate derived artifact layer.

Each analysis is tied to:

```text
source semantic version
+ current hardened English artifact
+ exact LM Studio model
+ prompt version
+ analysis schema version
```

The analysis schema currently supports:

- role purpose;
- responsibilities;
- requirements;
- requirement strength: required / preferred / contextual / inferred;
- concept type: tool / skill / knowledge / practice / domain / experience / education / other;
- confidence;
- original source evidence excerpt;
- rationale for inferred concepts.

The original employer/source fields remain authoritative. The English v2 projection is a
comprehension aid only.

Every material claim must carry an evidence excerpt that JobHunter can locate in the
original source fields. Invalid/hallucinated evidence prevents artifact acceptance.
Raw structured-inference request and response payloads are retained with the analysis
artifact for auditability.

### 6.6 First market aggregation

The Market screen aggregates only accepted current semantic-analysis artifacts and exposes:

- analyzed sample size;
- responsibility-claim count;
- requirement-claim count;
- posting-level concept demand;
- required/preferred/contextual/inferred counts separately.

This is not yet Phase 2 canonical taxonomy. Alias consolidation such as `Postgres` versus
`PostgreSQL` remains future reviewed canonicalization.

## 7. Browser workflow after this increment

```text
Overview
→ run bounded market sync
→ fetch priority missing details without re-running searches
→ repair/build current English v2
→ analyze a small ready batch
→ inspect aggregate Market view

Jobs
→ filter source / English / analysis / lifecycle / triage state
→ bulk triage up to 50 jobs
→ bulk fetch / translate / analyze with existing service bounds
→ inspect one job's source, English v2, semantic analysis, discovery provenance,
  lifecycle events, source checks, and evidence identity

Search plan
→ inspect configured catalog + observed search effectiveness

Market
→ inspect aggregate requirements only from accepted current analyses
```

## 8. Acceptance order for the current increment

Do not scale model work until each gate passes in order.

### Deterministic gate

1. Ruff.
2. Full pytest suite.
3. `pytest -W error`.
4. Translation v1 -> v2 migration behavior.
5. Translation field-permutation/integrity rejection tests.
6. One-segment LM translation association tests.
7. Source response classification/retry tests.
8. Cautious lifecycle transition tests.
9. Triage/priority tests.
10. Evidence-validation analysis tests.
11. Search-effectiveness/market aggregate tests.
12. Browser rendering/action tests.

### Live translation gate

1. Repair one posting that previously showed field-association corruption.
2. Confirm source and English scalar fields align correctly.
3. Confirm the artifact identifies `lm-studio-translation-v2` and
   `english-projection-v2`.
4. Repair a second previously affected posting.
5. Only then repair the wider parsed corpus in bounded batches.

### Live P1.6 gate

1. Select one reviewed, current v2 job.
2. Run per-job analysis.
3. Inspect every extracted responsibility/requirement and its original-language evidence.
4. Confirm required/preferred strength was not inflated.
5. Confirm unsupported concepts were omitted/rejected.
6. Then analyze a small batch (default 5), not the entire discovery corpus.
7. Inspect the Market screen only after that reviewed sample is acceptable.

## 9. Remaining Phase 1 work after acceptance

- broaden real fixtures for expired/challenge/access/rate-limit states;
- preserve error-response evidence where useful and permitted;
- expose last-successful source check and consecutive failure summaries more prominently;
- add repost/near-duplicate classification when corpus evidence justifies it;
- add reviewed translation golden-corpus benchmarks for model comparison;
- add review/correction workflow for uncertain semantic claims if live P1.6 evidence shows
  the need;
- finish P1.7 combined reporting and final `jobhunter run` orchestration.

## 10. Later phases

### Phase 2

Reviewed canonical career concepts, aliases, role archetypes, responsibility families,
demand matrices, and co-occurrence.

### Phase 3

Depth-aware personal capability evidence and gap classes. This remains deliberately
unimplemented until a reviewed personal-evidence schema/record exists; JobHunter must not
invent a personal capability profile from conversational assumptions.

### Phase 4

Evidence-backed career actions and application readiness.

### Phase 5

Historical trends, backup/restore, regression quality, retention, performance, and
sustained operation.

## 11. Remaining non-claims

Until the current increment is live-accepted, JobHunter must not claim:

- translation v2 quality across the full corpus;
- complete source lifecycle/repost resolution;
- production-quality semantic extraction across all role types;
- canonical market taxonomy;
- full-market conclusions from a small analyzed sample;
- personal capability gaps, readiness scores, or career recommendations;
- arbitrary-web Quick Add ingestion;
- final P1.7 end-to-end analysis/report automation.
