# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-09-17  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active working branch:** `main`  
**Current product gate:** MARKET I1-I4 ACCEPTED / I5 NEXT  
**P2.2B-B1:** CLOSED — NO-PROMOTION / DEFER  
**Parallel portfolio:** MIT complete; GitHub metadata + screenshots + release + owner mastery pending

## 1. Read this first

Current status authority:

`docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`

Current Market design authority:

`docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`

Foundation decision:

`docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`

Accepted implementation records:

```text
docs/working-memory/2026-09-16_MARKET_I1_DOMAIN_AND_PERSISTENCE_IMPLEMENTATION.md
docs/working-memory/2026-09-16_MARKET_I2_TARGET_SCOPED_AFFECTED_WORK_IMPLEMENTATION.md
docs/working-memory/2026-09-17_MARKET_I3_MEMBERSHIP_QUALIFICATION_IMPLEMENTATION.md
docs/working-memory/2026-09-17_MARKET_I4_IMMUTABLE_SNAPSHOT_CONSTRUCTION.md
```

I3 real-model boundary evaluation:

`docs/experiments/2026-09-17_market-i3-real-model-acceptance/README.md`

Execution checklist:

`docs/EXECUTION_TODO.md`

Do not follow older `I1 NEXT` / `I2 NEXT` / `I3 NEXT` / `I4 NEXT`, open-B1, or pre-foundation instructions when they conflict with these current owners.

---

## 2. Frozen accepted substrate

```text
parser:                     jobinja-detail-v2
translation:                english-projection-v2 / lm-studio-translation-v2
English P1.6:               job-analysis-english-v20 / job-analysis-v5
Capability:                 job-capability-intelligence-v9 / job-capability-intelligence-v5
Canonical Registry:         jobhunter-canonical-concept-registry-v1 / P2.1 CLOSED
Work Intelligence:          job-work-intelligence-v2 / v2.0 / P2.2A CLOSED
Public Corpus:              jobhunter-public-corpus-v1
Market membership:          market-membership-v1 / market-membership-v1.0
Market snapshot:            market-corpus-snapshot-v1
Market aggregate storage:   market-aggregate-profile-v1
```

Public corpus remains:

```text
353 known/discovered jobs
43 fetched/parsed details
21 current English projections
5 accepted/current English P1.6
5 accepted/current Capability
```

B1 remains closed as NO-PROMOTION / DEFER.

---

## 3. Permanent first-slice boundaries

```text
source = Jobinja only
search vocabulary != target membership truth
membership = core_match | adjacent_match | uncertain | excluded
primary corpus = core_match only
accepted P1.6 not required for source-level membership
accepted P1.6 required for strong semantic prevalence
Capability/Work optional, not gates
missing/pending/failed/rejected P1.6 != zero demand
repost/new-ID automatic collapse deferred
use 'qualified source postings', not 'unique demand units'
Market state local/private by default
```

Semantic role-subfamily synthesis, trends/forecasting, personal Market→You scoring, P2.2C/P2.2D promotion, and Market publication remain outside the first slice.

I3 also established a material target-definition lesson:

> `TargetMarketDefinitionVersion.membership_intent` must state material core-vs-adjacent boundaries explicitly. Do not patch individual vacancies into the membership prompt when the missing distinction belongs to target meaning.

---

## 4. I1-I3 accepted summary

### I1 — domain + persistence

Accepted:

- stable target identity vs immutable definition versions;
- run lifecycle + ledger history;
- immutable exact-dependency membership history;
- immutable snapshot/member and aggregate-profile persistence;
- target-definition changes do not invalidate source/translation/P1.6.

Evidence:

```text
head f0cded55a9887c061898d0dcab7f5e6b10300d8e
CI 1160: PASS through pytest -W error
```

### I2 — target-scoped affected work

Accepted:

- target-only missing-detail, refresh, translation and P1.6 planning;
- no unused target budget spills into global backlog;
- failed refresh neither freshens evidence nor proves disappearance;
- exact translation/P1.6 reuse/currentness;
- pending P1.6 remains pending review rather than regeneration.

Evidence:

```text
head 2ada4e92207f694bb5b7a4cba8c17108a67a4863
CI 1167: PASS through pytest -W error
```

### I3 — membership qualification

Accepted:

- deterministic constraints first;
- bounded semantic classification into exactly core/adjacent/uncertain/excluded;
- title/skills alone cannot establish core membership;
- accepted P1.6 optional evidence, pending P1.6 not a gate;
- exact dependency reuse and explicit immutable correction history;
- invalid/stale/provider failures remain failures rather than stored uncertainty.

Evidence:

```text
implementation 0eaf04109a57846aa6d0a920d0563f89a4dfb535
CI 1172: 608 passed under normal and -W error runs
```

Real-model boundary evidence:

```text
broad target       7/8 expected outcomes overall; tGM0 sole miss
clarified target   8/8 expected outcomes
```

The clarified result is post-hoc target-boundary calibration, not a population accuracy benchmark. The preserved evidence is under `docs/experiments/2026-09-17_market-i3-real-model-acceptance/`.

---

## 5. I4 — IMMUTABLE SNAPSHOT CONSTRUCTION — ACCEPTED / CLOSED

Acceptance owner:

`docs/working-memory/2026-09-17_MARKET_I4_IMMUTABLE_SNAPSHOT_CONSTRUCTION.md`

Implementation:

```text
src/jobhunter/market_snapshot_service.py
tests/test_market_snapshot_service.py
```

I4 is a service-level assembly authority over the I1 immutable snapshot tables. The caller supplies exact I3 membership IDs from one completed Market run; I4 validates currentness and derives semantic coverage itself.

### Snapshot admission

Allowed run states:

```text
completed
completed_with_failures
```

Rejected:

```text
running
failed
```

Every membership must:

- belong to the run target definition;
- use `market-membership-v1`;
- still have current I2 source eligibility;
- name the current source detail version;
- be the latest effective decision for its exact dependency/correction chain;
- be the only membership for that source in the snapshot.

For model memberships, the consumed translation and accepted-P1.6 identities must still match current state. A newly accepted current P1.6 therefore makes an older model membership without that dependency stale for new snapshot construction.

Deterministic source-only membership remains source-only as membership identity; current semantic coverage is frozen separately and does not retroactively become a membership dependency.

### Semantic coverage

I4 derives and freezes:

```text
accepted
pending
missing
failed
rejected
```

Accepted/pending come from the current live exact-contract P1.6 artifact.

Rejected history is matched to exact current source + translation + model/prompt/schema.

Failed attempts are matched to current source/model/prompt/schema and must occur after creation of the current translation artifact, preventing stale failures from leaking across a newer translation dependency.

If both failed and rejected current-processing evidence exists, the newest qualifying event determines the frozen state.

`missing`, `failed`, `pending`, or `rejected` never means zero requirements/responsibilities.

### Denominators frozen by I4

Only `core_match` gets:

```text
included_in_primary_corpus = true
```

Snapshot metadata freezes:

```text
member_count
disposition counts
primary_core_postings
semantic coverage counts
core-only semantic coverage counts
accepted_semantic_core_postings
denominator_language = qualified source postings
repost_adjustment = not_implemented
membership + P1.6 contract identity
```

This metadata preserves evidence-quality and denominator authority. It is not yet the I5 Market aggregate profile.

### Historical authority

Snapshot/member rows remain immutable. A later source semantic version, membership decision, or snapshot does not mutate old snapshot identities or dispositions.

### I4 verification

Focused tests cover:

- all five P1.6 coverage states;
- core-only primary inclusion;
- correction/supersession;
- stale source membership rejection;
- newly accepted P1.6 invalidating older model membership;
- deterministic source-only membership;
- terminal-run requirement;
- duplicate-source prevention;
- failed-vs-rejected processing ordering;
- historical snapshot immutability.

Final technical evidence:

```text
head 4b5e83134202d32ee167f499c3aca9cb43478f56
CI 1182 / 35249049607
Ruff: PASS
pytest: 617 passed
pytest -W error: 617 passed
conclusion: SUCCESS
```

No Jobinja network request or LM Studio generation was required for I4 acceptance.

---

## 6. Exact next action — I5 only

**I5 responsibility:** deterministic Market aggregate profile over one exact immutable I4 snapshot.

The central rule is:

> I5 may read historical source/P1.6 evidence by the exact IDs frozen in the snapshot, but it must never reconstruct the corpus from today's current state.

### I5 must produce

At minimum:

```text
target/definition/snapshot/run identity
snapshot time and source/search scope
core / adjacent / uncertain / excluded counts
qualified core source-posting denominator
accepted / pending / missing / failed / rejected core P1.6 coverage
accepted-semantic core denominator
raw source posting count
repost-adjustment limitation
distinct employer count
largest-employer contribution/share
freshness/lifecycle warnings and processing-state disclosure
```

For accepted-semantic core members, I5 should deterministically aggregate P1.6 requirement/responsibility evidence with exact job/artifact drill-down.

### I5 semantic support invariants

- one source posting contributes at most once to one normalized concept-support count;
- requirement strength support must remain explicit (`required / preferred / contextual / inferred`);
- distinct-employer support must be calculated deterministically;
- Registry mappings may enrich reviewed correspondences where already available, but unmapped source/P1.6 evidence remains valid;
- no model may write counts, percentages, scores, or denominator values.

### I5 explicit non-goals

Do not add:

- browser/CLI workflow yet;
- role-subfamily clustering;
- opaque importance scores;
- core/common/specialized bands;
- repost/new-ID collapsing;
- trends/emerging/forecasting;
- personal readiness/gap scoring;
- new Capability/Work gates;
- Market publication.

---

## 7. First-slice sequence

```text
I1  domain + persistence                         ACCEPTED
I2  target source eligibility / affected work   ACCEPTED
I3  membership qualification                    ACCEPTED
I4  immutable snapshot construction             ACCEPTED
I5  deterministic aggregate                     NEXT
I6  browser + CLI                               BLOCKED BY I5
I7  bounded real local acceptance               BLOCKED BY I6
```

---

## 8. Parallel portfolio/release state

Still pending:

```text
GitHub description/topics
real browser screenshots + privacy review
intentional v0.1.0 release
owner mastery verification
```

This parallel track does not change the I5 product frontier.
