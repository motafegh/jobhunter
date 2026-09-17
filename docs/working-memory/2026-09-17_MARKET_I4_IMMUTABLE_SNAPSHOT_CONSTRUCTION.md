# Market I4 — Immutable Snapshot Construction

**Date:** 2026-09-17  
**Status:** ACCEPTED / CLOSED FOR I4  
**Branch:** `main`  
**Implementation:** `src/jobhunter/market_snapshot_service.py`  
**Tests:** `tests/test_market_snapshot_service.py`  
**Controlling plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Foundation:** `docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

## 1. Scope

I4 turns exact accepted I1-I3 runtime identities into one immutable point-in-time Market corpus snapshot.

It does **not** acquire/refresh vacancies, translate, generate/review P1.6, infer target membership, calculate the final Market aggregate profile, render browser/CLI reports, perform repost collapsing, or publish Market state.

The service entry point is:

```text
MarketSnapshotService.build_snapshot(
    run_id,
    membership_ids,
    refresh_after_hours,
)
```

The caller supplies exact I3 membership IDs from one completed Market run. I4 validates those decisions against current I2/source/dependency state and freezes them through the existing immutable `MarketStore` snapshot tables.

## 2. Exact membership/currentness boundary

A snapshot may be created only from a Market run in:

```text
completed
completed_with_failures
```

A running or failed run cannot become snapshot authority.

For every supplied membership I4 requires:

- membership belongs to the run's exact target-definition version;
- membership uses the current `market-membership-v1` contract;
- current I2 source eligibility still holds;
- membership source detail version is still the current parsed source version;
- membership is the latest effective decision for its exact dependency identity rather than a superseded correction ancestor;
- one source job contributes at most one membership to one snapshot.

For model memberships, exact consumed derived dependencies must also still be current:

```text
current translation artifact
+ current accepted P1.6 when accepted P1.6 now exists
```

Therefore a model membership created before a newly accepted current P1.6 artifact becomes stale for new snapshot assembly and must be re-qualified under the richer exact dependency identity.

Deterministic source-only membership remains source-only as a membership dependency. I4 may still freeze the current semantic-coverage state separately for that source; semantic coverage is snapshot evidence state, not retroactive membership input.

## 3. Semantic coverage authority

I4 derives P1.6 coverage itself instead of trusting a caller-supplied status/artifact pair.

Coverage states are:

```text
accepted
pending
missing
failed
rejected
```

### Accepted / pending

When I2 exposes a current exact-contract P1.6 artifact:

```text
semantic_review_status=accepted → accepted
semantic_review_status=pending  → pending
```

The snapshot stores the exact current translation and live P1.6 artifact IDs.

### Missing

`missing` means there is no current live P1.6 artifact and no newer current-contract failed/rejected processing event that better describes the current processing state.

It does **not** mean zero responsibilities or zero requirements.

### Failed / rejected

The existing P1.6 persistence separates failed attempts and rejected semantic artifacts from live analysis artifacts. I4 reads that history without mutating it.

Rejected evidence must match the exact:

```text
current source detail
+ current translation
+ configured analysis model
+ job-analysis-english-v20
+ job-analysis-v5
```

Failed attempts must match current source/model/prompt/schema and occur no earlier than creation of the current translation artifact. This prevents an old failure from leaking forward across a newer translation dependency.

If both a qualifying rejected artifact and failed attempt exist after the current dependency boundary, the newest processing event determines the frozen coverage state.

## 4. Snapshot denominator semantics

One snapshot preserves all qualified dispositions separately:

```text
core_match
adjacent_match
uncertain
excluded
```

Only `core_match` is marked:

```text
included_in_primary_corpus = true
```

I4 snapshot metadata freezes deterministic evidence-quality counts, including:

```text
member_count
disposition counts
primary_core_postings
all-member semantic coverage counts
core-only semantic coverage counts
accepted_semantic_core_postings
denominator_language = qualified source postings
repost_adjustment = not_implemented
membership contract
P1.6 contract/model identity
```

These are snapshot-state/quality facts required to preserve denominator authority. I4 does **not** calculate the I5 Market profile, requirement prevalence, employer concentration, responsibility counts, or other report aggregates.

The denominator boundary remains:

```text
source-level Market facts
→ qualified core source postings

strong P1.6 semantic facts
→ qualified core postings with accepted-current P1.6
```

Pending/missing/failed/rejected semantic coverage never enters the accepted-semantic denominator and never becomes zero semantic demand.

## 5. Immutable evidence frozen per member

Each snapshot member preserves exact foreign identities plus bounded state needed to interpret the point-in-time corpus:

- membership ID and dependency fingerprint;
- exact source-detail version;
- exact current translation/P1.6 IDs where applicable;
- membership disposition;
- semantic coverage status;
- primary-corpus inclusion flag;
- source/lifecycle/currentness state;
- latest source observation outcome and warnings;
- translation/P1.6 planning/currentness state;
- explicit coverage basis.

The snapshot header also freezes target/search scope, target-definition fingerprint, exact supplied membership IDs, freshness rule, and first-slice denominator/repost limitations.

No full source, translation, or P1.6 payload is copied into Market persistence.

## 6. Historical behavior

The underlying I1 snapshot/member tables remain immutable through SQLite triggers.

I4 proves that after a source receives a new semantic version and a new membership decision/snapshot is created, the earlier snapshot still points to its original:

```text
source detail version
membership ID
disposition
semantic state
```

Historical snapshots are never reconstructed from today's database state.

## 7. Focused regression coverage

`tests/test_market_snapshot_service.py` adds nine I4 tests covering:

1. all five semantic coverage states plus core-only primary-corpus inclusion;
2. superseded membership rejection and corrected-membership acceptance;
3. stale source-version membership rejection;
4. newly accepted current P1.6 invalidating an older model-membership dependency;
5. source-only deterministic membership remaining independent from derived membership inputs while snapshot coverage can still be accepted;
6. terminal non-failed run requirement;
7. duplicate memberships for one source cannot enter one snapshot;
8. latest failed-vs-rejected processing event determines frozen coverage;
9. historical snapshot/member identity remains immutable after later source/membership changes.

The existing I1 store tests continue to protect table-level immutability, duplicate source-detail prevention, and exact P1.6 dependency validation.

## 8. Quality evidence

Final I4 implementation/test head before state-document reconciliation:

```text
4b5e83134202d32ee167f499c3aca9cb43478f56
```

GitHub Actions:

```text
run 1182 / 35249049607
package install                     PASS
pip dependency consistency          PASS
installed public entrypoint smoke   PASS
Ruff                                PASS
pytest                              PASS — 617 passed
pytest -W error                     PASS — 617 passed
CI conclusion                       SUCCESS
```

No Jobinja network request, LM Studio generation, operational Market mutation, Registry mutation, P1.6 acceptance, or corpus publication was required for I4 CI.

## 9. Non-claims

I4 does not yet prove:

- the final deterministic Market aggregate/profile is correct or useful;
- one real target run can yet be executed end-to-end through browser/CLI;
- a real acquisition/membership batch has produced an accepted operational snapshot;
- repost/new-ID adjustment exists;
- trend/emerging/subfamily/personal inference is justified.

Those remain later increments, especially I5-I7.

## 10. Decision

```text
MARKET I4: ACCEPTED / CLOSED
NEXT: I5 — DETERMINISTIC AGGREGATE PROFILE
```

I5 must calculate deterministic Market statistics strictly from one immutable I4 snapshot. It must keep source-level and accepted-semantic denominators explicit, preserve evidence drill-down, enforce one-posting-at-most-once support semantics, expose employer breadth/concentration and first-slice limitations, and never let a model author numeric counts or percentages.

Do not start I6 browser/CLI or I7 real workflow acceptance until I5 is coherent and accepted.
