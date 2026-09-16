# Market I1 — Domain and SQLite Persistence Implementation

**Date:** 2026-09-16  
**Status:** ACCEPTED / CLOSED FOR I1  
**Branch:** `main`  
**Controlling plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Foundation decision:** `docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

## 1. Scope

I1 implemented only the first Market vertical slice's domain/history substrate:

```text
TargetMarket
TargetMarketDefinitionVersion
MarketResearchRun
MarketJobMembership
MarketCorpusSnapshot + members
MarketAggregateProfile
```

It did **not** implement target acquisition orchestration, source-eligibility planning, semantic membership inference, aggregate calculation, browser/CLI workflows, repost detection, trends, role-subfamily synthesis, or personal intelligence.

## 2. Implemented files

```text
src/jobhunter/market_models.py
src/jobhunter/market_store.py
tests/test_market_store.py
```

### Domain records

`market_models.py` adds bounded typed records and first-slice vocabulary for:

- stable target identity;
- immutable target-definition versions;
- research runs;
- membership dispositions;
- P1.6 coverage state;
- immutable snapshot/member records;
- deterministic aggregate-profile records.

Current first-slice values include:

```text
membership:
core_match | adjacent_match | uncertain | excluded

P1.6 coverage:
accepted | pending | missing | failed | rejected

run state:
running | completed | completed_with_failures | failed
```

Contract identifiers introduced:

```text
market-corpus-snapshot-v1
market-aggregate-profile-v1
```

## 3. SQLite persistence boundary

`MarketStore` initializes on top of the existing source → translation → analysis SQLite dependency chain and adds:

```text
market_targets
market_target_definition_versions
market_research_runs
market_job_memberships
market_corpus_snapshots
market_corpus_snapshot_members
market_aggregate_profiles
```

No second database, cache, document store, vector store, or workflow system was introduced.

### Stable target vs immutable definition

`market_targets` owns a stable user-recognizable slug/identity. Display metadata may change.

`market_target_definition_versions` stores canonicalized immutable definition JSON plus a SHA-256 semantic fingerprint. Re-recording the same normalized definition reuses the same version; a material definition change creates the next version.

The first slice accepts only the already-approved `jobinja` source. Search profiles/packs/terms/raw searches and membership-intent constraints are stored as definition semantics. Operational run budgets remain separate run controls.

### Research runs

`market_research_runs` preserves:

- exact target-definition version;
- run controls;
- stage ledger JSON;
- running/terminal status;
- start/completion timestamps;
- optional error summary.

The store API permits ledger mutation only while the run is `running`, then one terminal transition.

### Membership identity and correction

`market_job_memberships` references exact existing upstream identities instead of copying authoritative payloads:

```text
target definition version
job detail/source version
optional translation artifact
optional accepted P1.6 artifact
classifier contract
classifier method
classifier identity
```

These form a deterministic dependency fingerprint.

A membership decision is immutable. Exact reruns reuse the same decision. A changed decision over the same dependency identity requires an explicit `supersedes_membership_id` correction record rather than rewriting history.

If membership consumes P1.6, the store verifies that the P1.6 artifact belongs to the exact source/translation chain and is `accepted`. Pending P1.6 may not become membership authority merely because an artifact exists.

### Snapshot history

`market_corpus_snapshots` and `market_corpus_snapshot_members` are immutable via SQLite triggers.

A snapshot freezes:

- exact target-definition version;
- exact run;
- snapshot contract;
- freshness/source scope and metadata;
- exact membership record;
- exact source detail version;
- translation/P1.6 artifacts used for semantic coverage where applicable;
- membership disposition;
- explicit P1.6 coverage state;
- whether the member belongs to the primary core corpus.

Primary-corpus inclusion is deterministic in I1:

```text
core_match       → included
adjacent_match   → not included
uncertain        → not included
excluded         → not included
```

This is only denominator-state persistence. I2/I3 still own actual source eligibility and membership decisions.

Accepted/pending/missing semantic coverage remains distinct. Missing P1.6 is never persisted as zero semantic demand.

### Aggregate profile history

`market_aggregate_profiles` persists an immutable deterministic profile over one exact snapshot + aggregate contract.

Canonical JSON is SHA-256 hashed. Repeating the same snapshot/contract/profile is idempotent. Producing different numeric/profile content for the same immutable snapshot + contract raises an integrity error rather than silently overwriting history.

I1 does not yet calculate that profile; I5 will own aggregate calculation.

## 4. Deterministic tests

`tests/test_market_store.py` covers the first I1 invariants:

1. stable target identity vs normalized immutable definition versions;
2. definition fingerprint idempotency;
3. SQLite immutability protection;
4. research-run ledger and terminal lifecycle;
5. exact membership dependency reuse;
6. explicit correction rather than hidden membership overwrite;
7. pending P1.6 cannot be consumed as membership authority;
8. a new source semantic version does not reuse the old source-version membership;
9. one snapshot preserves core/uncertain/adjacent disposition separately;
10. accepted/pending/missing P1.6 coverage remains distinct;
11. snapshot history is immutable;
12. one snapshot + aggregate contract cannot silently persist conflicting deterministic profiles.

## 5. Quality evidence

Final I1 head before documentation reconciliation:

```text
e871e23d88e301a885d4b153e672d5d593c9961d
```

GitHub Actions CI run:

```text
1158 / 35107895662
```

Result:

```text
package install                     PASS
pip dependency consistency          PASS
installed public entrypoint smoke   PASS
Ruff                                PASS
pytest                              PASS
pytest -W error                     PASS
CI conclusion                       SUCCESS
```

Earlier I1 pushes exposed only formatting/lint issues and were repaired from CI evidence before acceptance. No test or runtime-integrity failure was hidden or waived.

## 6. What I1 intentionally does not claim

I1 does **not** prove yet that:

- target-scoped acquisition selects the right affected work;
- lifecycle/freshness eligibility is correct in a real Market run;
- semantic membership classification is accepted;
- snapshots are assembled from a real target run;
- aggregate values are product-useful;
- browser/CLI Market workflows exist;
- a real local target run is accepted.

Those remain I2–I7 responsibilities.

Repost/new-ID automatic collapse is still deferred. The eventual first report must use `qualified source postings`, not `unique demand units`.

## 7. Decision

```text
MARKET I1: ACCEPTED / CLOSED
NEXT: I2 — TARGET-SCOPED SOURCE ELIGIBILITY + AFFECTED-WORK PLANNING
```

I2 should compose existing Jobinja/source/lifecycle/translation/P1.6 owners and prove that one target run selects only target-scoped missing/stale affected work while preserving partial success and `failed refresh != disappearance`.

Do not start I3 membership inference, I4 snapshot assembly, I5 aggregate calculation, I6 UI/CLI, or I7 live acceptance before I2 is coherent.
