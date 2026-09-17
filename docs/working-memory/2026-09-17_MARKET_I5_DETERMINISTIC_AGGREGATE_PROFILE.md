# Market I5 — Deterministic Aggregate Profile

**Date:** 2026-09-17  
**Status:** ACCEPTED / CLOSED FOR I5  
**Branch:** `main`  
**Implementation:** `src/jobhunter/market_aggregate_service.py`  
**Tests:** `tests/test_market_aggregate_service.py`  
**Controlling plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**I4 snapshot authority:** `docs/working-memory/2026-09-17_MARKET_I4_IMMUTABLE_SNAPSHOT_CONSTRUCTION.md`

## 1. Scope

I5 builds and persists one deterministic Market aggregate profile from one exact immutable I4 snapshot.

It does **not** reconstruct the corpus from current source state, call any model, infer membership, refresh sources, perform repost collapsing, create semantic role families, forecast trends, score personal fit, render the browser/CLI workflow, or publish Market state.

The service entry point is:

```text
MarketAggregateService.build_profile(snapshot_id)
```

The existing immutable `market_aggregate_profiles` store remains persistence authority under:

```text
market-aggregate-profile-v1
```

## 2. Historical authority

I5 reads only identities already frozen by I4:

- target-definition version;
- run and snapshot identity/time;
- exact snapshot membership IDs;
- exact source-detail version IDs;
- exact translation/P1.6 IDs for semantic-covered members;
- frozen disposition and semantic-coverage state.

The aggregate never asks which source/P1.6 artifact is current *today*.

Employer and source-context facts are read from the exact immutable `job_detail_versions.fields_json` referenced by each snapshot member. Employer breadth therefore does not depend on mutable discovery metadata such as a later `job_postings.company_slug` update.

If an exact source-detail artifact has no employer field, I5 records an unknown-employer posting rather than fabricating employer identity.

## 3. Explicit denominator layers

I5 preserves two distinct denominator layers.

### Source-level Market denominator

```text
qualified core source postings
```

Only snapshot members marked `included_in_primary_corpus=true` may contribute.
I5 integrity-checks that every such member is actually `core_match`.

### Accepted-semantic denominator

```text
core postings with accepted snapshot P1.6 coverage
```

Only those postings may contribute requirement/responsibility semantic prevalence.

The profile records:

```text
raw snapshot members
core / adjacent / uncertain / excluded counts
primary core postings
accepted / pending / missing / failed / rejected core semantic coverage
accepted semantic core postings
accepted semantic coverage numerator / denominator / share
denominator_language = qualified source postings
repost_adjustment = not_implemented
```

Pending/missing/failed/rejected semantic coverage never enters accepted-semantic prevalence and never becomes zero demand.

## 4. Employer and source-context profile

For core postings I5 deterministically calculates:

- distinct known employers;
- unknown-employer postings;
- largest-employer posting count;
- largest-employer share of the core source denominator;
- postings by employer;
- location distribution;
- employment-type distribution;
- minimum-experience distribution;
- education distribution;
- source job-category distribution;
- frozen lifecycle distribution;
- frozen source-warning counts.

String grouping uses deterministic normalized text only. It does not claim employer-entity resolution across materially different names.

## 5. Requirement aggregation

Requirement statistics are calculated only from exact accepted P1.6 artifacts frozen in core snapshot members.

Each claim may be enriched by an existing reviewed Canonical Registry mapping only when that mapping's `reviewed_at` is **no later than the snapshot timestamp**.

This as-of-snapshot cutoff prevents a later Registry review from silently changing historical aggregate replay.

Normalization behavior:

```text
reviewed mapped claim
→ canonical:<concept_id>

no qualifying mapping
→ raw:<claim-kind>:<concept-type>:<normalized raw concept>
```

Reviewed-unmapped/rejected-mapping states remain explicit rather than being forced into canonical concepts.

For each normalized requirement concept, the profile includes:

- support posting count;
- share of accepted-semantic core postings;
- distinct known employers;
- unknown-employer posting count;
- explicit per-posting strength support for `required / preferred / contextual / inferred`;
- depth-signal posting counts;
- normalization/mapping state;
- exact evidence drill-down containing source job ID, analysis artifact ID and claim indexes.

One posting contributes at most once to the concept-support count even if the same concept appears repeatedly in that posting. The same posting may still legitimately contribute to multiple strength categories when its accepted P1.6 contains distinct claims with different strengths.

## 6. Responsibility aggregation

Responsibility support follows the same point-in-time Registry rule and exact accepted-semantic denominator.

No semantic family equivalence is invented. Unmapped responsibility statements remain exact normalized raw statements.

One posting contributes at most once to one normalized responsibility support count, while drill-down retains all matching claim indexes/statements from that posting.

This is deterministic evidence aggregation, not P2.2C responsibility-family promotion.

## 7. Warnings and limitations

The deterministic profile emits bounded warnings where applicable:

```text
repost_adjustment_missing
small_core_sample
small_semantic_sample
incomplete_semantic_coverage
employer_concentration
unknown_employer_evidence
```

Current thresholds retain existing first-slice semantics:

- small sample warning below 20 postings;
- employer-concentration warning when the core sample is at least 5 and one employer contributes at least 50%.

The profile explicitly states that:

- repost/new-ID/cross-source dedup is not implemented;
- semantic statistics use accepted-P1.6 core postings only;
- Registry enrichment is point-in-time bounded;
- no role-subfamily, trend, forecast, personal-fit or model-authored numeric score is present.

## 8. Deterministic persistence and replay

`MarketStore.record_aggregate_profile()` remains the immutable persistence boundary.

Canonical JSON is hashed. Rebuilding the same snapshot/profile returns the same aggregate artifact. Conflicting deterministic content for the same immutable snapshot + aggregate contract remains an integrity failure.

No model writes counts, shares, percentages, denominators or warnings.

## 9. Focused regression coverage

`tests/test_market_aggregate_service.py` adds five I5 tests covering:

1. explicit source vs accepted-semantic denominators, adjacent exclusion, employer breadth, one-posting-at-most-once concept/responsibility support, strength/depth counts and evidence drill-down;
2. exact historical source-detail/employer authority after a later source semantic version exists;
3. Canonical Registry enrichment only as-of snapshot time, including deterministic replay after a later mapping is reviewed;
4. pending/non-accepted semantic members never contributing requirement/responsibility counts;
5. unknown employer remaining explicit rather than being fabricated.

The existing Market store tests continue to protect conflicting deterministic profile replay.

## 10. Quality evidence

Final I5 code/test head before state-document reconciliation:

```text
5defb23cb769a4be7a6b0d13ea7762d35ec0f4ba
```

GitHub Actions:

```text
run 1189 / 35250174702
package install                     PASS
pip dependency consistency          PASS
installed public entrypoint smoke   PASS
Ruff                                PASS
pytest                              PASS — 622 passed
pytest -W error                     PASS — 622 passed
CI conclusion                       SUCCESS
```

Earlier I5 pushes failed only the repository Ruff gate because of two long limitation strings. Those formatting defects were repaired before acceptance; no I5 semantic test failed or was waived.

## 11. Non-claims

I5 does not yet establish:

- a user-facing browser/CLI Market workflow;
- a complete target-run coordinator from acquisition through snapshot/profile;
- a real local operational Market report;
- real repeated-run reuse at product level;
- repost-adjusted demand units;
- trends/emerging signals;
- role subfamilies/archetypes;
- personal Market→You scoring.

Those remain I6/I7 or later explicitly gated work.

## 12. Decision

```text
MARKET I5: ACCEPTED / CLOSED
NEXT: I6 — THIN BROWSER + CLI MARKET WORKFLOW
```

I6 should expose the accepted Market target/run/snapshot/profile workflow through the existing FastAPI/Jinja browser and CLI surfaces, using the same services/state. It must remain thin: no duplicate business logic, no new semantic contracts, no publication, and no model-generated report layer.
