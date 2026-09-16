# Market I2 — Target-Scoped Source Eligibility and Affected-Work Planning

**Date:** 2026-09-16  
**Status:** ACCEPTED / CLOSED FOR I2  
**Branch:** `main`  
**Controlling plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Foundation decision:** `docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`  
**I1 dependency:** `docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md`

## 1. Scope

I2 implemented one read-only planning boundary:

> Given one immutable Market target-definition version and one already-discovered target candidate set, determine exact source eligibility and target-scoped missing/stale source, English-projection, and P1.6 affected work without consuming unrelated global backlog.

I2 does **not** execute discovery/detail/translation/P1.6 work, classify semantic market membership, create production Market snapshots, calculate aggregates, or expose browser/CLI Market workflows.

## 2. Implemented files

```text
src/jobhunter/job_detail_observations.py
src/jobhunter/market_affected_work.py
tests/test_market_affected_work.py
```

### Existing owner extension

`JobDetailObservationStore` now exposes:

```text
latest_successful_check_at(source_job_id)
```

This returns the newest successful **parsed** detail check only. Failed retry attempts therefore do not make stale source evidence look fresh.

The existing global `refresh_due_job_ids()` behavior is unchanged. I2 deliberately does not change Phase-1/global maintenance semantics.

## 3. Target-only planning boundary

`MarketAffectedWorkPlanner` accepts:

```text
target_definition_version_id
candidate_source_job_ids
missing detail budget
refresh budget + refresh threshold
translation budget
P1.6 budget
```

The candidate IDs are the exact target scope. The planner never asks global missing/translation/P1.6 queues to fill unused capacity.

An unknown candidate ID fails integrity because target candidates must already exist in persisted Jobinja discovery state.

The first I2 implementation supports only the already-authorized:

```text
source = jobinja
freshness_rule = current-active
```

No second source policy or generalized freshness engine was introduced.

## 4. Deterministic source eligibility

Per candidate, I2 records:

```text
source identity/title/company
lifecycle state
source status
source action
source eligibility
exact current parsed detail-version ID when available
latest detail timestamp
latest observation outcome
warnings
translation currentness/action
P1.6 currentness/action/review state
```

Source statuses:

```text
current
missing_detail
refresh_due
invalid_current_detail
expired
removed
ineligible_lifecycle
```

Source actions:

```text
none
fetch_missing_selected
fetch_missing_remaining
refresh_selected
refresh_remaining
```

A job becomes source-eligible for later membership evaluation only when:

- the current detail exists and parsed successfully;
- lifecycle is `active` or cautiously `possibly_unavailable`;
- valid source evidence is within the run's refresh threshold;
- no source repair/refresh action is still required.

`expired` and `removed` are outside the current-active eligibility set.

`possibly_unavailable` may remain eligible when recent valid evidence exists, with an explicit warning.

## 5. Freshness and failed-refresh semantics

I2 freshness is based on successful valid evidence:

```text
latest successful parsed detail observation
→ otherwise current parsed detail fetched_at
```

A failed observation is separately exposed as a warning and does **not** refresh the evidence clock.

Therefore:

```text
failed refresh != disappearance
failed refresh != fresh evidence
```

A recent failed retry against old valid evidence remains refresh-due, while the prior evidence stays preserved.

An unchanged successful parsed check *does* refresh the freshness clock without creating a new semantic source version.

## 6. Target-scoped source work

I2 separates:

```text
missing detail selected / remaining
refresh selected / remaining
source ready
```

Invalid current details are treated as refresh/repair candidates and are prioritized ahead of ordinary freshness refreshes within the target refresh budget.

Unused target capacity remains unused. It is never filled by an unrelated global job.

## 7. Translation affected work

Only source-ready target candidates enter translation planning.

For each such candidate, I2 uses the existing `TranslationService` effective identity/currentness rules.

Translation states:

```text
blocked_source
current
needed_selected
needed_remaining
unavailable_provider
```

Current exact English-projection artifacts are reused by immutable artifact ID.

Persian/mixed evidence with no configured translation provider is explicit `unavailable_provider`, not silently treated as translated or excluded.

Jobs needing source work do not consume translation budget before their source state is current.

## 8. P1.6 affected work

Only target candidates with a current effective English projection enter P1.6 planning.

Currentness uses the accepted public contract identity:

```text
current source detail version
+ exact current translation artifact
+ configured analysis model
+ job-analysis-english-v20
+ job-analysis-v5
```

P1.6 planning states:

```text
blocked_source
blocked_translation
current_accepted
current_pending_review
needed_selected
needed_remaining
unavailable_model
```

A pending current P1.6 artifact is **not regenerated** merely because it is not accepted. It remains explicit `current_pending_review` for the later coverage/review workflow.

A new semantic source version invalidates current translation/P1.6 reuse through the existing exact dependency identities; old artifacts remain historical evidence.

## 9. Planning ledger

`MarketAffectedWorkPlan.ledger()` exposes deterministic target-scoped counts for later `MarketResearchRun` integration:

```text
source:
  candidate / ready / blocked
  missing selected / remaining
  refresh selected / remaining
  latest failed refresh

translation:
  reused / selected / remaining / unavailable / blocked source

analysis:
  current accepted / current pending review
  selected / remaining / unavailable / blocked
```

This is a planning ledger only. Actual run attempts/completions/failures remain the future target coordinator's responsibility.

## 10. Regression tests

`tests/test_market_affected_work.py` covers:

1. target missing-detail selection never spills into unrelated global missing backlog;
2. a recent failed refresh does not freshen source evidence or mark the posting removed;
3. an unchanged successful parsed check refreshes freshness without a new semantic version;
4. recent `possibly_unavailable` evidence may remain usable with warning;
5. `removed` and `expired` are excluded from current-active source eligibility;
6. exact current translation and accepted P1.6 artifacts are reused;
7. current pending P1.6 remains pending-review rather than being regenerated;
8. translation-needed target work blocks P1.6 until the English projection exists;
9. unrelated globally eligible translation/P1.6 work never enters the target plan;
10. a new source semantic version invalidates old translation/P1.6 currentness;
11. target budgets leave remaining target work explicit instead of filling capacity globally.

No test requires Jobinja network access or LM Studio.

## 11. Quality evidence

Final I2 technical head before documentation reconciliation:

```text
2ada4e92207f694bb5b7a4cba8c17108a67a4863
```

GitHub Actions:

```text
run 1167 / 35123454023
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

The preceding planner-only run also reached successful Ruff/pytest/warnings-as-errors steps before being superseded/cancelled by the test commit; the accepted authority is run 1167 on the complete I2 code + tests.

## 12. What I2 intentionally does not claim

I2 does **not** prove yet that:

- source/title/work evidence is semantically a core/adjacent/uncertain/excluded target match;
- model-backed membership classification is trustworthy;
- Market memberships are recorded automatically;
- target discovery/search expansion is wired into a production Market coordinator;
- source/translation/P1.6 selected work is executed by one Market run;
- run ledger failures are persisted from real stage execution;
- snapshots or aggregates are constructed from the plan;
- browser/CLI or real local target acceptance exists.

Those remain later first-slice increments.

## 13. Decision

```text
MARKET I2: ACCEPTED / CLOSED
NEXT: I3 — MEMBERSHIP QUALIFICATION CONTRACT + SERVICE
```

I3 should consume only I2 source-eligible candidates and decide `core_match / adjacent_match / uncertain / excluded` using staged evidence: deterministic target constraints first, then bounded semantic role/work relevance where necessary.

Accepted-current P1.6 may strengthen a membership decision but must not become a prerequisite. Capability and Work Intelligence remain optional and must not become I3 gates.

Do not start I4 snapshot construction, I5 aggregate calculation, I6 browser/CLI, or I7 live acceptance before I3 is coherent.
