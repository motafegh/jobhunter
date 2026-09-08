# Market First-Slice Acceptance and Testing Strategy

**Date:** 2026-09-08  
**Status:** REMOTE DESIGN RESEARCH / IMPLEMENTATION NOT AUTHORIZED  
**Branch:** `main`  
**Controlling future plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Current product gate:** P2.2B-B1 remains open; local `ta9l` execution is intentionally postponed until owner PC access returns

## 1. Purpose

This is the sixth bounded research pass for the future Market / Role-Family Intelligence responsibility.

It answers:

> What evidence and tests should be required before the first Market vertical slice is considered trustworthy enough to use, without turning semantic uncertainty into brittle test ceremony or requiring live-model execution for every CI run?

This document is design input only. It does **not** start Market-v2 implementation, does not close B1, and does not authorize new runtime code.

---

## 2. Existing JobHunter testing behavior worth preserving

The current repository already demonstrates the right separation of concerns:

- `tests/test_market_insights.py` checks deterministic counts, requirement-strength separation, sample warnings, employer concentration, and explicit disclosure of missing duplicate adjustment.
- `tests/test_phase1_run.py` checks bounded work selection, remaining-work counts, partial-success semantics, disabled-stage behavior, and the distinction between `no eligible work` and `failure`.
- P1.6, Capability, Canonical Registry, Work Intelligence, Review Snapshot, lifecycle, acquisition, browser, and CLI each have focused boundary tests rather than one giant end-to-end test owning every rule.
- Work/Capability semantic tests protect dangerous authority boundaries and structured references while avoiding exact free-form wording as the acceptance oracle.

**Market implication:**

The first Market slice should extend these patterns rather than introduce a separate testing philosophy.

Use:

```text
exact tests for exact state/provenance/count rules
+
representative semantic evaluation for interpretive behavior
+
small real/local acceptance for runtime truth
```

---

## 3. Acceptance layers

The first Market slice should be accepted through six layers, with strictness proportional to authority and blast radius.

### Layer A — domain and persistence invariants

These tests should be deterministic, fast, and CI-safe.

They should prove at minimum:

```text
stable target identity is separate from immutable definition versions
old definition versions cannot be silently rewritten
market run points to one exact definition version
membership is target-specific, not a global flag on a job
membership decisions reference the exact source semantic version used
snapshot membership is immutable after finalization
snapshot members reference exact upstream artifacts rather than copying authority
aggregate profile references one exact snapshot/contract
history remains readable after newer source/target versions appear
```

Integrity defects here are hard failures.

### Layer B — currentness, reuse, and affected-work planning

Tests should prove that Market orchestrates existing artifact reuse rather than rebuilding everything.

Representative cases:

```text
unchanged source + unchanged contracts
→ translation/P1.6/membership reused

new semantic source version
→ old historical snapshot remains valid
→ new run sees the job as affected
→ stale downstream membership/P1.6 is not silently reused

changed target-definition version
→ source/translation/P1.6 may remain reusable
→ target membership must be reconsidered where definition semantics require it

changed membership contract/model identity
→ old membership remains historical
→ new effective decision is required

changed aggregate contract only
→ snapshot remains valid
→ aggregate profile must be rebuilt under the new contract
```

Do not test timestamps alone as semantic currentness.

### Layer C — snapshot and deterministic aggregate correctness

This is the strongest first-slice product authority.

Every statistic must be derivable from frozen snapshot members and exact eligible upstream artifacts.

Tests should cover:

- denominator identity is explicit;
- each unique demand unit counts at most once per applicable concept/classification;
- raw advertisements and duplicate-adjusted demand units remain distinguishable;
- required/preferred/contextual/inferred counts remain separate;
- distinct-employer support is correct;
- employer concentration warnings are deterministic;
- missing fields do not become negative evidence;
- pending/rejected/stale P1.6 cannot enter an accepted-only semantic denominator;
- broader qualified-source count is not confused with accepted-P1.6 coverage;
- mapped canonical claims use reviewed correspondence where available;
- unmapped valid claims remain visible rather than disappearing;
- snapshot reconstruction produces the same aggregate result under the same contract.

Numeric values are application-owned. A model must never author or repair them.

### Layer D — orchestration and partial-success behavior

Use fake/stub acquisition/model providers in CI. Do not require Jobinja or LM Studio network/runtime access for ordinary automated tests.

Representative cases:

```text
discovery partially fails
→ successful source work remains durable
→ run status exposes failure

one detail refresh fails
→ previously known source state is not treated as disappearance
→ other jobs continue

translation fails for one job
→ unaffected jobs continue
→ missing semantic coverage is explicit

P1.6 generation succeeds but remains pending review
→ it is recorded as pending
→ it does not silently enter accepted-only market statistics

membership qualifier is uncertain
→ disposition remains uncertain / excluded from primary denominator per policy
→ entire run does not fail

no jobs need processing
→ explicit no-op/reuse outcome, not false failure
```

The run ledger should expose requested, eligible, attempted, completed, reused, failed, pending/review-needed, and remaining work where those concepts apply.

### Layer E — semantic relevance and candidate-interpretation evaluation

Semantic tests should evaluate dangerous behavior, not exact prose.

The curated relevance set should include at least:

```text
1. obvious core role despite non-obvious title
2. obvious core role with expected title
3. adjacent role sharing many technologies
4. misleading keyword/title hit with unrelated actual work
5. sparse posting with insufficient evidence
6. dense hybrid posting
7. posting plausibly belonging to two subfamilies
8. genuinely ambiguous role where uncertain is correct
9. source with preferred/contextual AI/security wording but non-core work
10. source where responsibilities strongly support the target despite weak title vocabulary
```

For semantic membership qualification, acceptance should prioritize:

- no fabricated source facts;
- no title-only authority;
- evidence/reasons refer to supplied source/P1.6 material;
- deterministic hard exclusions are respected;
- ambiguous cases may remain uncertain;
- adjacent evidence does not contaminate the primary core denominator;
- output does not silently promote a candidate role/subfamily taxonomy.

Do **not** require identical labels, rationales, or prose between model runs.

### Layer F — browser/CLI and real local acceptance

After repository implementation/tests are green, perform a bounded real local acceptance using the configured runtime.

This should prove the actual repeated-use path:

```text
create/select target
→ preview bounded scope
→ run refresh
→ inspect stage/partial-success ledger
→ review qualified corpus and coverage
→ inspect deterministic aggregate profile
→ drill down from an aggregate row to supporting source evidence
→ rerun unchanged target and observe reuse/idempotency
```

The browser is the primary repeated-use acceptance surface. CLI should expose the same underlying state for inspection/debugging.

Real local acceptance should not require processing the entire known corpus merely to prove the vertical slice.

---

## 4. Representative deterministic fixture matrix

The first implementation should build a compact synthetic/in-memory SQLite fixture corpus rather than hundreds of artificial jobs.

A strong initial matrix is approximately 10-14 postings with deliberately overlapping properties:

| Case | Purpose |
| --- | --- |
| core-native | core role, native English, accepted P1.6 |
| core-translated | core role requiring English projection |
| adjacent | relevant adjacent work, not primary denominator |
| keyword-false-positive | title/keyword match but unrelated work |
| sparse | limited evidence |
| dense-hybrid | multiple responsibilities/requirements |
| same-employer-1 | employer concentration case |
| same-employer-2 | employer concentration case |
| repost-a | first source identity in duplicate candidate pair |
| repost-b | second source identity in duplicate candidate pair |
| stale-version | newer source semantic version invalidates old current chain |
| pending-p16 | qualified source but P1.6 not accepted |
| translation-failure | partial processing failure |
| uncertain-membership | legitimate unresolved semantic case |

One fixture may serve multiple assertions; do not build one isolated fixture per micro-rule when a coherent mini-market is clearer.

---

## 5. Duplicate/repost test contract

Duplicate handling is not yet implemented, so the first implementation investigation must finalize the policy before strong prevalence claims.

When it is implemented, tests must distinguish:

```text
same source_job_id observed repeatedly
→ one logical posting; existing source/version machinery already prevents observation inflation

same employer + materially same vacancy + new source_job_id
→ possible repost/duplicate relationship
→ preserve both advertisements
→ count according to explicit approved unique-demand-unit policy

uncertain near-duplicate
→ do not destructively merge
→ preserve uncertainty and denominator impact explicitly
```

Do not test or implement a magic global similarity threshold as authority.

---

## 6. P1.6 acceptance-throughput test requirement

The prior orchestration/persistence research identified a Market-scale bottleneck: fresh English P1.6 v20 artifacts are intentionally `pending` until semantic review, while strong Market statistics should consume accepted/current P1.6 only.

The first Market slice must therefore test separate counts for:

```text
qualified source jobs
qualified jobs with accepted-current P1.6
qualified jobs with pending P1.6
qualified jobs missing P1.6
```

Required invariant:

> A pending P1.6 artifact may improve the processing ledger, but it may not silently increase the accepted semantic denominator.

Do not weaken the existing review boundary merely to make Market processing look complete.

The later formal investigation must decide how Market-scale acceptance throughput is made usable operationally.

---

## 7. Semantic-test philosophy

Semantic/model behavior should use three classes of assertion.

### 7.1 Hard semantic boundary assertions

Examples:

- model references evidence/jobs that were never supplied;
- model fabricates employer facts;
- model places a deterministic excluded job into core membership;
- model turns `preferred` evidence into required fact;
- model presents candidate subfamily as promoted/canonical;
- model-generated numeric prevalence conflicts with deterministic aggregate data.

These should fail acceptance.

### 7.2 Bounded behavioral assertions

Examples:

- clearly unrelated keyword false-positive should not become confident core;
- clear core work should not be excluded solely because title wording differs;
- hybrid job may use overlapping membership;
- ambiguous evidence may return uncertain.

These should tolerate equivalent safe outputs rather than require exact labels/prose.

### 7.3 Informational variation

Differences in:

- concise wording;
- candidate label wording;
- ordering of equally supported observations;
- non-authoritative rationale phrasing;

should not reopen the contract unless they cause a real authority/usefulness defect.

---

## 8. First-slice acceptance criteria

The first deterministic Market vertical slice should not be called accepted until all of the following hold.

### Repository acceptance

1. Target identity + immutable definition-version persistence is repeat-safe.
2. Run/membership/snapshot/aggregate relationships enforce exact dependency identity.
3. Historical snapshots remain unchanged after newer source or target versions exist.
4. Currentness/affected-work selection does not rerun unaffected model stages.
5. Primary aggregate counts are deterministic and expose explicit denominators.
6. Accepted-only semantic sections exclude pending/rejected/stale P1.6.
7. Raw advertisement and approved unique-demand-unit semantics are not conflated.
8. Partial failures preserve successful durable state and expose stage-specific failures.
9. Re-running unchanged inputs is idempotent/reuse-heavy rather than creating duplicate authority.
10. Existing Phase-1/P2.1/P2.2A/current Market behavior remains green unless an explicitly approved compatibility change is necessary.
11. No Market state is published to `corpus/` without a separate publication decision.
12. No candidate role/responsibility interpretation is silently promoted.

### Product acceptance

13. A user can see what target was analyzed and what definition version produced the result.
14. A user can see candidate, qualified, accepted-semantic, unique-demand-unit, and employer counts without guessing the denominator.
15. A user can drill from a reported demand item to exact supporting jobs/source evidence.
16. A partial run is visibly partial, not displayed as complete market truth.
17. An unchanged rerun visibly benefits from reuse.
18. The first report is useful without requiring Capability/Work artifacts for every job unless the formal audit proves such dependency necessary.

### Semantic acceptance when relevance qualification is included

19. Representative clear core/adjacent/false-positive/ambiguous cases behave within the approved disposition boundary.
20. No dangerous authority strengthening/fabrication is observed in the bounded acceptance set.
21. Ambiguous cases may remain uncertain rather than being forced to pass as core/excluded.

---

## 9. Explicit stop lines for the first vertical slice

Do not expand acceptance into these responsibilities merely because they are future Market goals:

```text
no semantic executive report generation yet unless separately authorized
no stable role-archetype promotion
no responsibility-family promotion merely for reporting
no Market → You personal readiness/scoring
no salary benchmarking without adequate source coverage
no forecasting
no generic second-source/plugin architecture
no graph/vector infrastructure
no exhaustive canonical mapping of every claim
no automatic P1.6 acceptance
no trend claim until at least two comparable frozen snapshots exist
no `emerging` label until longitudinal evidence and policy exist
no public corpus/repository export of Market state without privacy/publication review
```

A vertical slice is successful when it proves the smallest trustworthy market substrate, not when it prematurely implements the entire product vision.

---

## 10. Suggested implementation-test order later

After B1 closure and the formal Market foundation investigation, a sensible first implementation order is:

```text
1. target + definition-version models/store/tests
2. run + membership persistence/tests
3. snapshot immutability/currentness tests
4. deterministic aggregate profile/tests
5. affected-work/reuse planner tests
6. partial-success orchestration tests with fakes
7. minimal CLI inspection
8. minimal browser target/report view
9. bounded real local acceptance
10. only then decide whether semantic relevance qualification belongs in the same slice or the next one
```

If semantic relevance qualification is required to make the first target actually useful, include it as one bounded semantic component; otherwise keep the first slice deterministic and add qualification immediately afterward.

---

## 11. Recommended acceptance corpus strategy

Use three evidence tiers rather than one enormous test corpus.

```text
Tier 1 — synthetic deterministic mini-market
CI-safe; exact invariants/counts/currentness/idempotency

Tier 2 — curated repository-safe representative semantic cases
small; protects relevance/authority boundaries; no exact-prose oracle

Tier 3 — bounded real local target run
actual Jobinja/local LM Studio/runtime behavior; owner/local acceptance
```

Do not make Tier 3 a prerequisite for every ordinary CI run, and do not mistake Tier 1 synthetic success for proof of real semantic usefulness.

---

## 12. Design conclusions to carry into the formal post-B1 investigation

1. Preserve JobHunter's existing split between deterministic contract tests and semantic boundary evaluation.
2. The Market first slice needs strong tests for target-version identity, membership dependency identity, snapshot immutability, denominator correctness, and partial success.
3. Use a coherent 10-14-job synthetic mini-market rather than a huge fixture corpus.
4. Explicitly test accepted/pending/missing P1.6 coverage separately.
5. Pending/rejected/stale P1.6 must never enter accepted-only semantic prevalence.
6. Test affected-work invalidation so only genuinely stale dependencies are recomputed.
7. Preserve old snapshots after source/target changes.
8. Test duplicate/repost behavior only after its explicit policy is designed; never hide it behind an opaque threshold.
9. Semantic relevance tests should protect authority and obvious behavioral boundaries, not exact wording.
10. `uncertain` is a valid successful semantic outcome for ambiguous evidence.
11. CI should use fakes/stubs for network/model stages; real Jobinja/LM Studio acceptance remains a bounded local gate.
12. The first vertical slice should stop before report synthesis, trends, personal comparison, stable archetypes, or publication unless separately authorized.
13. Acceptance should prove repeated-use value and reuse/idempotency, not merely schema correctness.
14. The first report must expose its evidence coverage and denominators before presenting market conclusions.

---

## 13. Current state

```text
P2.2B-B1 local execution                     PAUSED UNTIL OWNER PC ACCESS
Market implementation                         NOT AUTHORIZED
Market research pass 1 — external references COMPLETE
Pass 2 — target/relevance/dedup/trends        COMPLETE
Pass 3 — report intelligence contract         COMPLETE
Pass 4 — incremental orchestration/reuse      COMPLETE
Pass 5 — persistence/snapshot model           COMPLETE
Pass 6 — first-slice acceptance/testing       COMPLETE
formal Market foundation audit                STILL QUEUED BEHIND B1
```

At this point the major first-slice design uncertainties are sufficiently bounded for pre-implementation planning. Further remote research should be selective rather than continuing indefinitely. The highest-value next remote-safe activity is a **consolidation audit of the six research records against the controlling Market plan**, identifying contradictions, unresolved decisions that truly need the post-B1 formal investigation, and anything already clear enough that it should not be researched again.
