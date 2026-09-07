# Market Persistence, Snapshot, and Artifact Research

**Date:** 2026-09-07  
**Status:** REMOTE DESIGN RESEARCH / IMPLEMENTATION NOT AUTHORIZED  
**Branch:** `main`  
**Controlling future plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Current product gate:** P2.2B-B1 remains open; local `ta9l` execution is intentionally postponed until owner PC access returns

## 1. Purpose

This is the fifth bounded research pass for the future Market / Role-Family Intelligence responsibility.

It answers:

> What is the smallest durable persistence model that lets JobHunter run a target market repeatedly, reuse membership decisions, preserve point-in-time evidence, compare history honestly, and reproduce the exact report shown to the user?

This is design input only. It does **not** start the formal post-B1 Market foundation investigation and does not authorize Market-v2 implementation.

---

## 2. Existing JobHunter persistence pattern to preserve

The current repository already establishes several useful conventions.

### 2.1 Stable logical identity separate from semantic versions

`storage.py` separates:

```text
job_postings
→ stable logical source job

job_detail_versions
→ immutable semantic source versions

job_detail_fetch_observations
→ repeated checks/operational observations
```

A new fetch with unchanged semantic content does not create a new semantic source version.

### 2.2 Derived artifacts depend on exact upstream identities

Translation, P1.6, Capability and Work persist exact upstream artifact/version identities and reuse only when those inputs and their own contract identities match.

### 2.3 Reviewed reusable authority is explicit

The Canonical Registry persists reviewed concepts/mappings separately from source claims, and mappings point to exact P1.6 artifacts/claim indices.

### 2.4 Review snapshots preserve an exact chain

`review_snapshot.py` exports a deterministic point-in-time projection containing source version and exact derived artifact identities rather than only a prose summary.

**Market implication:**

Use the same architecture:

```text
stable target identity
→ immutable target definition version
→ operational run
→ reusable per-job membership decisions
→ immutable point-in-time corpus snapshot
→ deterministic aggregate artifact
→ persisted user-facing semantic report
```

Do not use one mutable `market_report` record as source, operation log, snapshot and interpretation simultaneously.

---

## 3. Refined minimal durable boundaries

The six provisional concepts in the controlling plan remain useful, but one needs a logical/version split.

Recommended conceptual model:

```text
TargetMarket
TargetMarketDefinitionVersion
MarketResearchRun
MarketJobMembership
MarketCorpusSnapshot (+ snapshot members)
MarketAggregateProfile
RoleFamilyIntelligenceReport
```

This is seven relational/domain boundaries but still the same six product responsibilities from the plan: `TargetMarketDefinition` becomes stable target identity + immutable definition versions.

Do not add more entities unless implementation evidence proves they are necessary.

---

## 4. `TargetMarket` + `TargetMarketDefinitionVersion`

### Purpose

Represent a user-recognizable market question that can evolve without rewriting history.

Example:

```text
stable target:
  ai-security-germany

v1:
  AI Security / ML Security
  Germany
  broad seniority
  search pack A

v2:
  same logical target
  Germany
  mid/senior only
  revised search vocabulary
```

### Why a stable target and immutable versions are both needed

If the target definition is updated in place, an old snapshot can no longer prove what scope produced it.

Therefore:

```text
TargetMarket
- stable target ID
- display name
- active/archive state
- created/updated timestamps

TargetMarketDefinitionVersion
- target ID
- monotonically increasing or immutable version ID
- canonical definition JSON
- semantic fingerprint/hash
- source/search scope
- geography/work arrangement/seniority/employment/freshness constraints
- request/page/detail bounds
- created_at
```

The exact fields remain for formal investigation.

### Store or recompute?

**Store.** The exact definition version is historical authority.

Do not infer an old target definition from today's settings.

---

## 5. `MarketResearchRun`

### Purpose

Represent one operational attempt to refresh/build a market view.

This is analogous to current `acquisition_runs`, but target-aware and multi-stage.

Candidate fields:

```text
run_id
target_definition_version_id
started_at
completed_at
status
requested bounds/budgets
effective contract identities
stage ledger / counts
failure summary
resulting snapshot_id when produced
```

### Status model

A run may be:

```text
running
completed
completed_with_failures
failed_before_snapshot
```

Exact vocabulary remains provisional.

A run is an operation record, not semantic market authority.

### Store or recompute?

**Store.** Operational history, partial success and failure state cannot be reconstructed safely from final artifacts alone.

The row may transition while the operation is running, then becomes historical after completion.

---

## 6. `MarketJobMembership`

### Purpose

Persist a reusable decision about whether one exact job evidence state belongs to one exact target definition.

This must not be a mutable flag on `job_postings`, because the same job can be:

```text
core for one target
adjacent for another
excluded for another
```

and a changed source version may justify a new decision.

### Candidate dependency identity

A semantic membership decision should identify at minimum:

```text
target_definition_version_id
source_job_id / job_posting_id
job_detail_version_id
membership policy/contract version
classification method
model/prompt/schema identity when model-assisted
exact semantic input artifact IDs used, such as P1.6 when applicable
```

### Candidate output

```text
disposition:
  core_match | adjacent_match | uncertain | excluded

reason / evidence references
qualitative confidence when useful
candidate/reviewed state only if the final policy needs a review boundary
created_at
```

### Deterministic exclusions

A deterministic hard exclusion can still be represented as a membership record with method such as:

```text
deterministic_policy
```

rather than inventing a fake model decision.

### Store or recompute?

**Store when the decision required semantic/model interpretation or represents the effective decision used by a snapshot.**

Cheap deterministic eligibility can be recomputed during planning, but the effective membership disposition selected for a historical snapshot must remain recoverable.

### Reuse rule

Reuse only when the exact relevant dependency identity still matches.

Changing target definition or source semantic version must not silently reuse an old semantic membership decision.

---

## 7. `MarketCorpusSnapshot`

### Purpose

This is the most important historical Market artifact.

It freezes the exact evidence corpus and denominator used for one market view.

A snapshot is **not** "all jobs currently matching a query." That answer changes as the database evolves.

### Snapshot header should preserve

At minimum:

```text
snapshot_id
target_definition_version_id
created_at
source scope
membership contract/version
dedup contract/version
aggregate input contract/version
raw candidate count
core / adjacent / uncertain / excluded counts
qualified unique-demand-unit count
distinct employer count
important coverage/warning state
```

### Snapshot-member rows should preserve exact identities

For every member/candidate relevant to the frozen snapshot, investigate storing:

```text
snapshot_id
job_posting_id / source_job_id
job_detail_version_id
membership_record_id
membership disposition used
translation_artifact_id if part of semantic evidence
accepted P1.6 artifact_id if part of the strong semantic denominator
duplicate/repost group or unique-demand-unit identity when applicable
inclusion role in primary denominator
```

Do not duplicate complete source/P1.6 payloads inside snapshot rows; exact foreign identities are enough because existing historical artifacts remain immutable.

### Which dispositions should be in the snapshot?

Prefer preserving more than only the final core denominator:

```text
core
adjacent
uncertain
excluded candidates that materially passed acquisition into qualification
```

This allows later audit of why a job did or did not count without rediscovering the whole run.

The report's primary denominator can still use only the approved qualified disposition/unit policy.

### Store or recompute?

**Store immutably.**

This is the point-in-time historical authority required for trustworthy trend comparison.

Never rebuild an old snapshot by querying today's current job state.

---

## 8. Duplicate/repost grouping inside snapshots

The previous research established that unique demand units and raw advertisements are different quantities.

Do not prematurely create a global permanent `DuplicateJob` ontology.

For the first single-source slice, the formal investigation should decide whether duplicate/repost disposition belongs as:

```text
A. a reusable job-pair/group artifact independent of snapshots
or
B. a versioned snapshot/membership-time grouping result
```

Minimum requirement regardless of representation:

- preserve every underlying source posting;
- preserve uncertain duplicate status;
- identify the unit counted in prevalence;
- preserve policy version;
- do not destructively merge source identities.

If the same duplicate relationship is expensive to infer and reusable across targets, a small reusable duplicate-group artifact may be justified later. Do not assume it now.

---

## 9. `MarketAggregateProfile`

### Purpose

Persist the deterministic quantitative/structured result over one exact snapshot.

Candidate dependency identity:

```text
snapshot_id
aggregate contract version
normalization/registry policy version or effective identity
```

Candidate contents:

```text
evidence-quality metrics
market-shape counts
requirement demand rows
responsibility/work demand rows
experience/seniority/education/context distributions
employer breadth/concentration
bounded co-occurrence/bundles
warnings
```

### Why persist if deterministic?

In theory it can be recomputed from the immutable snapshot and exact historical artifacts.

Persisting it is still useful because:

1. report rendering becomes fast and stable;
2. the exact quantitative state shown to the user is recoverable;
3. aggregation contracts may evolve;
4. historical code need not be executed merely to inspect an old report;
5. a checksum/fingerprint can prove report dependency.

### Store or recompute?

**Persist as an immutable derived artifact, while keeping it reproducible from the snapshot.**

This is a cache-like optimization only in performance terms; authority still comes from the snapshot + referenced evidence + contract identity.

Do not allow aggregate JSON to become an alternative source database.

---

## 10. `RoleFamilyIntelligenceReport`

### Purpose

Persist the exact user-facing report/synthesis built from one aggregate profile and snapshot.

This matters especially because semantic synthesis may not be byte-for-byte reproducible on a later model call.

Candidate dependency identity:

```text
market_aggregate_profile_id
snapshot_id
report contract/schema version
synthesis model/prompt/schema identity when used
```

Candidate contents:

```text
executive synthesis
candidate role subfamilies
bounded interpretations / notable combinations
trend interpretation when a comparable prior snapshot exists
explicit limitations/warnings
structured references back to aggregate rows/evidence
```

Numeric counts should be injected from deterministic aggregate data, not authored freely by the model.

### Candidate authority

The report may contain analytical interpretation, but it does not promote:

- candidate subfamilies into canonical archetypes;
- candidate responsibility groupings into canonical families;
- narrative into source fact.

### Store or recompute?

**Store immutably.**

The exact report shown to the user is a durable product artifact and semantic generation may be nondeterministic.

A later report against the same snapshot but a materially changed report contract/model should be a new artifact, not an overwrite.

---

## 11. What should NOT be copied into Market persistence

Avoid redundant payload duplication.

Do not copy complete versions of:

```text
raw source HTML
parsed source JSON
English projection payload
P1.6 payload
Capability payload
Work payload
canonical-registry content
```

into every snapshot/report.

Reference exact existing durable identities instead.

The snapshot may denormalize a small amount of display/audit metadata where useful, but upstream artifact IDs remain authority.

---

## 12. Store-vs-recompute summary

```text
Target stable identity                 STORE
Target definition version              STORE IMMUTABLY
Market run / stage ledger               STORE
Cheap deterministic eligibility         RECOMPUTE for planning
Effective semantic membership decision  STORE/REUSE by exact dependencies
Historical snapshot member set          STORE IMMUTABLY
Duplicate/repost relationship            INVESTIGATE smallest reusable boundary
Aggregate quantitative profile          STORE IMMUTABLE DERIVED + RECOMPUTABLE
User-facing semantic report             STORE IMMUTABLY
Current/latest report pointer/view       COMPUTE or maintain as convenience only
Trend metrics                           COMPUTE from comparable immutable snapshots/profiles,
                                        optionally persist in report artifact
```

---

## 13. Currentness and history rules

### 13.1 Never mutate history because a job changes

If a job gets a new semantic source version:

- old snapshot continues pointing to the old exact source/P1.6 evidence used at that time;
- a new market refresh may use the new source version;
- historical trend remains auditable.

### 13.2 Current report is a view, not destructive replacement

A target can have many snapshots/reports.

`latest/current` should mean the newest applicable completed report for the current target definition, not the only surviving artifact.

### 13.3 Contract changes create new derived artifacts

If aggregate/report contract changes materially, preserve old profile/report and create new artifacts when rebuilt.

### 13.4 Target edits create new definition versions

Do not rewrite snapshots to point at a modified target definition.

---

## 14. Comparability contract

Trend comparison should occur only when the two snapshots satisfy explicit compatibility checks.

Candidate checks:

```text
same logical target
compatible target-definition semantics
same/compatible source scope
same/compatible membership policy
same/compatible dedup policy
same/compatible denominator semantics
same/compatible aggregate metric definition
sufficient temporal/window interpretation
```

A target definition may change in harmless ways while remaining comparable, but that judgment needs an explicit versioned compatibility rule rather than string equality alone.

If comparability is uncertain, store/display the warning rather than compute a confident trend.

---

## 15. P1.6 acceptance-throughput implication for snapshots

Pass 4 identified P1.6 acceptance throughput as a potential Market scaling bottleneck.

Persistence must make that limitation visible rather than hiding it.

A snapshot/report should be able to distinguish:

```text
qualified source candidates
qualified jobs with accepted-current P1.6
qualified jobs with pending P1.6
qualified jobs missing P1.6
```

If strong semantic prevalence uses accepted-only P1.6, store the exact accepted semantic denominator separately from broader source-level qualified corpus counts.

Do not let `60 qualified jobs` silently become `60 semantically analyzed jobs` when only 18 are accepted.

This likely means one snapshot can preserve source-level market membership while aggregate sections declare their own evidence-eligible denominator.

That is preferable to creating a separate snapshot for every semantic-processing stage.

---

## 16. Suggested first implementation vertical slice, later

When B1 closes and the formal investigation authorizes implementation, the smallest useful persistence slice likely needs only:

```text
1. target + immutable definition version
2. market run
3. membership records
4. immutable snapshot + member rows
5. deterministic aggregate profile
```

Then render a deterministic first report view from the aggregate.

Persist a model-generated `RoleFamilyIntelligenceReport` artifact only when semantic report synthesis/subfamily interpretation is introduced in the next bounded increment.

This keeps the first implementation vertical without prematurely requiring every future artifact at once.

---

## 17. Design hypotheses to carry into formal post-B1 investigation

1. Split stable target identity from immutable target-definition versions.
2. Keep operation/run state separate from semantic snapshot authority.
3. Persist membership per exact target/source/semantic dependency identity; never as a global job flag.
4. Treat `MarketCorpusSnapshot` as the historical point-in-time authority for denominator membership.
5. Snapshot rows should reference exact existing artifacts instead of copying their complete payloads.
6. Preserve core/adjacent/uncertain/excluded qualification evidence sufficiently for audit, not only final included rows.
7. Preserve raw-advertisement and unique-demand-unit semantics separately.
8. Persist aggregate profiles as immutable derived artifacts even though they are deterministically reproducible.
9. Persist semantic reports because exact model synthesis may not be reproducible later.
10. Keep candidate report/subfamily interpretation non-canonical.
11. `latest/current` should be a view over preserved history, never destructive overwrite.
12. Trend comparison requires explicit snapshot-contract compatibility checks.
13. A snapshot should preserve both broad qualified source scope and the narrower accepted-P1.6 semantic denominator used by strong aggregate sections.
14. Do not create new storage engines or duplicate upstream artifact payloads.
15. Implement persistence incrementally; the first vertical slice does not need every future report artifact.

---

## 18. Current state

```text
P2.2B-B1 local execution                    PAUSED UNTIL OWNER PC ACCESS
Market implementation                       NOT AUTHORIZED
Market research pass 1                      COMPLETE
Market target/relevance/dedup pass 2        COMPLETE
Market report-contract pass 3               COMPLETE
Market incremental/reuse pass 4             COMPLETE
Market persistence/snapshot pass 5          COMPLETE
formal Market foundation audit              STILL QUEUED BEHIND B1
```

The most useful remaining remote-safe design pass is now **acceptance and testing strategy for the first Market vertical slice**: define representative fixture classes, deterministic invariants, semantic acceptance cases, failure/partial-success cases, and explicit stop lines—without writing implementation tests yet.
