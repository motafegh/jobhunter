# Market Incremental Orchestration and Reuse Research

**Date:** 2026-09-07  
**Status:** REMOTE DESIGN RESEARCH / IMPLEMENTATION NOT AUTHORIZED  
**Branch:** `main`  
**Controlling future plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Current product gate:** P2.2B-B1 remains open; local `ta9l` execution is intentionally postponed until owner PC access returns

## 1. Purpose

This is the fourth bounded research pass for the future Market / Role-Family Intelligence responsibility.

It focuses on one operational question:

> How should one target-market refresh reuse existing source, translation, accepted P1.6, Capability and Work artifacts instead of re-running expensive work across the whole corpus?

This record is design input only. It does **not** start the formal post-B1 Market investigation or authorize Market-v2 implementation.

---

## 2. Current JobHunter already has the core reuse primitives

The repository inspection shows that Market-v2 does not need a second cache/invalidation platform.

### 2.1 Source acquisition is already bounded and freshness-aware

`src/jobhunter/jobinja_sync.py` already distinguishes:

```text
missing detail jobs
refresh-due jobs
new semantic version
unchanged semantic content
failed checks
```

and bounds detail checks per run.

`src/jobhunter/job_detail_observations.py` separately records each fetch/check observation and can select refresh-due jobs by last-check age.

**Implication:** target-market orchestration should reuse this selection model and narrow it to the target acquisition envelope rather than refetch every known job.

### 2.2 Translation is already idempotent on explicit inputs

`src/jobhunter/translation_service.py` reuses an English projection when this identity matches:

```text
current job_detail_version_id
+ target language
+ provider
+ provider model
+ translation schema version
```

If the source semantic version is unchanged and the effective translation identity is unchanged, the translation is reused.

### 2.3 P1.6 already reuses exact dependency identity

`src/jobhunter/analysis_service_v20.py` looks for an existing artifact using:

```text
current job_detail_version_id
+ exact current translation_artifact_id
+ configured analysis model
+ P1.6 prompt version
+ P1.6 schema version
```

A matching artifact is recorded as `reused`; otherwise a new candidate is generated and persisted with semantic-review state `pending`.

### 2.4 Capability already depends on exact current accepted evidence

Current Capability v9 resolves:

```text
current source version
+ current English projection
+ exact semantically accepted current P1.6
```

and reuses a Capability artifact keyed by the exact source/translation/P1.6 dependencies plus capability model/prompt/schema identity.

### 2.5 Work Intelligence already follows the same pattern

P2.2A Work Intelligence requires exact accepted current P1.6 and stores immutable artifacts keyed by:

```text
analysis_artifact_id
+ model
+ prompt version
+ schema version
```

Requirement-only jobs can use the deterministic limited path with no model call.

### 2.6 Current Market is already read-only over accepted/current evidence

`src/jobhunter/market_insights.py` performs deterministic aggregation only. It selects current accepted English P1.6 artifacts and verifies the exact current translation dependency before counting them.

**Main architectural conclusion:**

```text
Market refresh should be a dependency-aware incremental planner
that composes existing currentness/reuse contracts.

It should NOT create a parallel cache, artifact store, or invalidation framework.
```

---

## 3. External design references

Two external patterns reinforce this direction without implying new infrastructure dependencies.

### Bazel remote-cache model

Official Bazel documentation describes build actions as explicit inputs + command/configuration + expected outputs. Reusable outputs are retrieved when the matching action identity already exists.

Reference:

- https://bazel.build/remote/caching

**Useful JobHunter analogy:** expensive derived artifacts should be reusable only when all material inputs/contract identities match. JobHunter already does this for translation/P1.6/Capability/Work.

Do not adopt Bazel itself; the useful principle is explicit dependency identity.

### dbt state-aware execution

Current dbt documentation describes state-aware orchestration as skipping unnecessary rebuilds when underlying logic/data have not materially changed.

Reference:

- https://docs.getdbt.com/

**Useful JobHunter analogy:** determine affected work first, then execute only missing/stale stages.

Again, this is a design analogy, not a reason to add dbt or another orchestrator.

---

## 4. Proposed target-market refresh planner

A strong first-slice orchestration hypothesis is:

```text
A. resolve target definition
→ B. bounded discovery / source refresh
→ C. cheap deterministic eligibility screen
→ D. compute per-job dependency state
→ E. process only missing/stale prerequisites
→ F. qualify target membership
→ G. resolve duplicate/repost units
→ H. freeze qualified snapshot
→ I. deterministic aggregate profile
→ J. optional bounded semantic synthesis
→ K. save report + run ledger
```

### 4.1 A — Target definition

Resolve the target definition/version first so every later decision is traceable to one exact target scope.

Changing a target definition should **not** automatically invalidate source/translation/P1.6 artifacts. Those are job evidence, independent from a user's market question.

### 4.2 B — Bounded acquisition first

Reuse existing discovery and sync behavior:

- discover using the target acquisition/search envelope;
- fetch missing details first;
- refresh only due/currently relevant details within configured bounds;
- preserve failures as observations, not disappearance;
- prioritize newly discovered or recently changed target candidates.

Acquisition must remain useful even when model providers are unavailable.

### 4.3 C — Cheap deterministic screen before model work

Before expensive translation/analysis, remove only obviously ineligible candidates using high-confidence deterministic facts where available, for example:

- source not in approved source scope;
- explicit geography outside a strict target geography;
- explicit employment-type exclusion;
- explicit freshness/date boundary;
- lifecycle state that is validly removed/expired under current source policy;
- owner-defined hard exclusions that are directly observable.

This stage should be deliberately conservative. Do not reject a semantically relevant role merely because its title does not contain the search phrase.

### 4.4 D — Compute a dependency-state ledger per plausible candidate

For each still-plausible candidate, inspect rather than blindly execute:

```text
source current?
translation current?
matching P1.6 artifact exists?
P1.6 semantic state accepted/pending/rejected/missing?
target-membership decision current for this target + source/semantic inputs?
duplicate/repost disposition current?
Capability current if a requested report section actually needs it?
Work current if a requested report section actually needs it?
```

This ledger should drive the work queues.

### 4.5 E — Execute only the lowest missing prerequisite

A job should move through only the stages it actually needs.

Examples:

```text
current source + current translation + accepted current P1.6
→ no translation call
→ no P1.6 call
→ proceed to/reuse membership

current source + current translation + missing P1.6
→ no translation call
→ generate P1.6 candidate only

new semantic source version
→ old downstream artifacts remain historical
→ create/reuse translation for new source
→ P1.6 for exact new translation
→ downstream currentness follows from exact dependencies
```

Do not run Capability or Work merely because they exist as available product layers.

---

## 5. Invalidation / affected-work matrix

The formal investigation should test this dependency model.

### Source semantic version changes

Expected affected work:

```text
translation currentness
P1.6 currentness
Capability currentness
Work currentness
membership when membership uses semantic/source content
dedup relation if content identity materially affects it
snapshot / aggregate / report
```

Historical artifacts remain preserved.

### Translation provider/model/schema identity changes

Expected affected work:

```text
translation
P1.6 that depends on exact translation artifact
Capability / Work downstream of that P1.6
membership only if it consumes translated/P1.6 evidence
snapshot / aggregate / report as needed
```

Source evidence itself is unaffected.

### P1.6 model/prompt/schema changes

Expected affected work:

```text
P1.6
Capability / Work tied to exact P1.6
membership if membership consumes P1.6 semantics
snapshot / aggregate / report
```

Source and translation need not be rebuilt when still current.

### Target-market definition changes

Expected affected work:

```text
membership
dedup/snapshot only where target scope changes relevant units
aggregate
report
```

Do **not** invalidate generic job source/translation/P1.6 simply because the user changed from `AI Security` to `Applied AI`.

### Membership-policy/model changes

Expected affected work:

```text
membership
snapshot
aggregate
report
```

Generic job semantic artifacts remain reusable.

### Duplicate/repost-policy changes

Expected affected work:

```text
duplicate dispositions / unique-demand units
snapshot denominator
aggregate metrics
historical comparability
report
```

Do not rerun P1.6 for a dedup-policy change.

### Aggregate/report contract changes

Expected affected work:

```text
aggregate/report only
```

Existing qualified evidence should be reusable when its contracts still satisfy the new report.

### Candidate synthesis prompt/model changes

Expected affected work:

```text
candidate role-subfamily / narrative synthesis only
```

Deterministic counts and snapshot membership must not be regenerated merely because model prose changes.

---

## 6. Strong first-slice cost/model-call policy

Local LM Studio removes API billing but not cost. Latency, GPU/CPU time, memory, energy, user waiting time and model-failure exposure remain real operational costs.

### 6.1 Translation

Call translation only when:

```text
candidate remains plausibly in target scope
AND
current effective English projection is missing
AND
source content actually requires translation
```

Native-English source identity already supports a no-provider path.

### 6.2 P1.6

Generate P1.6 only when:

```text
candidate survives cheap eligibility
AND
current English projection exists
AND
no matching current P1.6 artifact exists
```

Do not regenerate an exact matching artifact.

### 6.3 Capability

Capability should **not** be a mandatory prerequisite for the first useful Market report.

Strong baseline market facts—requirements, strength, depth, responsibilities and exact evidence—already come from accepted P1.6.

Use existing current Capability opportunistically where it adds value. Generate missing Capability only if a concrete report section proves it materially useful.

### 6.4 Work Intelligence

Similarly, Work Intelligence should not gate the core report.

Accepted P1.6 responsibilities can feed deterministic responsibility demand directly. Existing Work artifacts may enrich candidate work-composition synthesis.

Do not generate Work for every qualified job by default until the formal investigation proves the value outweighs model-call cost.

### 6.5 Report-level semantic synthesis

Prefer:

```text
deterministic aggregate computation
+ bounded candidate synthesis over structured aggregates and selected evidence
```

rather than one model call per job to generate a narrative and then another model call to summarize those narratives.

The first report should avoid N-jobs × many-model-stages multiplication where direct accepted evidence already supports the question.

---

## 7. Important newly identified bottleneck: P1.6 acceptance throughput

This research found a more important scaling question than raw inference cost.

Current P1.6 v20 behavior is intentionally:

```text
new artifact
→ semantic_review_status = pending
→ explicit acceptance/rejection boundary
```

Current Market selects accepted-only current P1.6 artifacts.

Therefore a future target refresh cannot safely do:

```text
generate 100 P1.6 candidates
→ silently count all 100 as market truth
```

That would bypass an accepted authority boundary.

### Formal investigation question

Before a large Market corpus is treated as strong semantic evidence, determine a scalable acceptance strategy without weakening truthfulness.

Candidate directions to evaluate later include:

1. **accepted-only first slice** — report strong semantic aggregates only over already accepted current P1.6 and explicitly show the pending-review backlog;
2. **bounded batch-review workflow** — improve owner review throughput without changing what `accepted` means;
3. **separate exploratory candidate view** — allow lower-authority candidate statistics only if unmistakably separated from accepted market truth and never mixed into the primary denominator;
4. only if strong evidence later justifies it, reconsider whether some P1.6 outputs can become safely auto-promoted under a new explicit policy—but do not assume or implement that now.

Do **not** solve the throughput problem by quietly changing `pending` into `accepted`.

This question belongs in the formal post-B1 Market foundation investigation because it materially affects corpus size, UX and processing economics.

---

## 8. Recommended queue priority

Within one target-market run, prioritize work approximately as:

```text
1. newly discovered target candidates with no detail
2. target candidates whose source refresh is due
3. changed/new semantic source versions
4. plausible candidates missing current translation
5. plausible candidates missing current P1.6
6. pending P1.6 items requiring review/decision
7. missing/recomputed membership decisions
8. uncertain duplicate/repost cases needed for denominator integrity
9. optional Capability/Work only when needed for report value
10. report-level synthesis
```

The exact ordering should remain configurable/bounded rather than becoming an unbounded background crawler.

---

## 9. Run ledger / partial-success semantics

One Market run should expose what happened rather than one generic success boolean.

Investigate a ledger containing at least:

```text
discovery requested / completed / failed
missing details selected
refresh-due details selected
new semantic versions
unchanged source checks
source failures
deterministically excluded candidates
translation reused / completed / failed
P1.6 reused / generated / failed
P1.6 accepted / pending / rejected counts relevant to snapshot
membership reused / classified / uncertain / excluded
duplicate groups resolved / uncertain
qualified unique-demand units
snapshot members
Capability reused / generated / skipped
Work reused / generated / deterministic-limited / skipped
synthesis calls / failures
remaining eligible backlog
```

A model failure should degrade the relevant stage, not erase already durable source/translation/P1.6 results.

---

## 10. Why no new orchestration framework is justified

Current JobHunter already has:

- bounded source synchronization;
- explicit source observations;
- semantic source versions;
- idempotent translation;
- exact dependency-bound P1.6;
- accepted/current routing;
- exact downstream Capability/Work dependencies;
- attempt histories with `completed / failed / reused`;
- partial-success orchestration in `phase1_run.py`;
- deterministic Market read models.

The missing capability is a **target-aware dependency planner and run/snapshot model**, not Airflow/Dagster/dbt/Bazel integration.

Stay with the Python modular monolith and SQLite until measured operational complexity proves otherwise.

---

## 11. Design hypotheses to carry into the formal post-B1 investigation

1. Reuse the existing source → translation → accepted P1.6 dependency chain as the core Market processing substrate.
2. Build Market orchestration as affected-work planning, not full-corpus reruns.
3. Keep target-definition/membership invalidation separate from generic job-evidence invalidation.
4. Perform conservative deterministic screening before expensive semantic processing.
5. Reuse exact current artifacts before making any model call.
6. Keep Capability and Work optional for the first core aggregate rather than mandatory corpus-wide prerequisites.
7. Prefer deterministic aggregate calculation plus a small bounded report-level semantic synthesis.
8. Persist a run ledger with reused/completed/failed/pending/remaining counts.
9. Preserve partial success and never interpret provider failure as evidence disappearance.
10. Treat P1.6 acceptance throughput as a first-class Market scaling problem.
11. Do not auto-accept P1.6 merely to increase market sample size.
12. Investigate a scalable review/candidate-vs-accepted presentation strategy before claiming strong corpus-wide semantic statistics.
13. Do not add a new workflow/orchestration/cache framework before current service composition proves inadequate.

---

## 12. Current state

```text
P2.2B-B1 local execution                    PAUSED UNTIL OWNER PC ACCESS
Market implementation                       NOT AUTHORIZED
Market external/general research pass 1      COMPLETE
Market target/relevance/dedup/trend pass 2  COMPLETE
Market report-contract pass 3               COMPLETE
Market incremental/reuse pass 4             COMPLETE
formal Market foundation audit              STILL QUEUED BEHIND B1
```

A sensible next remote-safe pass, if useful, is now **persistence and snapshot/run artifact design**: determine the smallest durable `TargetMarketDefinition / MarketResearchRun / MarketJobMembership / MarketCorpusSnapshot / MarketAggregateProfile / RoleFamilyIntelligenceReport` boundaries and what must be stored versus recomputed—without implementing them yet.
