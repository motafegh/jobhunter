# Market I3 — Membership Qualification

**Date:** 2026-09-17  
**Status:** REPOSITORY ACCEPTED / CLOSED FOR I3; real-model boundary evaluation recorded; I7 live workflow acceptance remains outstanding  
**Branch:** `main`  
**Implementation commit:** `0eaf04109a57846aa6d0a920d0563f89a4dfb535`  
**Controlling plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Foundation:** `docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`  
**Real-model evaluation:** `docs/experiments/2026-09-17_market-i3-real-model-acceptance/README.md`

## Scope and product contribution

I3 supplies one service that turns an I2 source-eligible target candidate into a reusable,
inspectable membership interpretation. It removes the need for a future target run to ask
the user to classify every posting manually or to wait for P1.6 acceptance before recognizing
source-level relevance. The complete repeated-use browser workflow remains I6/I7 scope.

Files:

- `src/jobhunter/market_membership_models.py`
- `src/jobhunter/market_membership_inference.py`
- `src/jobhunter/market_membership_service.py`
- `tests/test_market_membership.py`
- `tests/test_market_membership_inference.py`

No new persistence schema, cache, canonical taxonomy, or public-corpus contract was added.

## Contract and authority

```text
contract/schema: market-membership-v1
prompt:          market-membership-v1.0
provider:        lm-studio-membership-v1
constraints:     market-membership-constraints-v1
```

The typed output contains exactly one of `core_match`, `adjacent_match`, `uncertain`,
`excluded`, a short reason, bounded evidence references, and qualitative confidence.
It is JobHunter interpretation, not employer wording or promoted role taxonomy.

The evidence map uses exact source field keys, current English field keys, and optional
accepted-current P1.6 section/index keys. References must exist. A core decision must cite
substantive description or accepted work/requirement evidence; title/skills alone fail.
This reference check proves linkage, not semantic truth of the reason or classification.
The prompt separately requires role/work reasoning and preserves uncertainty.

The source-detail title is used; mutable discovery title observations cannot replace it.
Acquisition search profiles, packs, terms, and catalog identity are not model membership criteria.

## Staged execution

1. Recompute I2 eligibility for exactly the requested candidate, with all work budgets zero.
2. Inspect original current parsed evidence for deterministic constraints.
3. For an unambiguous structured full-time/part-time conflict, save an explicit exclusion
   without a model or derived-artifact dependency. Recognized English/Persian literals are
   field-value correspondences, not an action-verb or role-taxonomy equivalence system.
4. Missing, compound, unrecognized, geographic, seniority, and role constraints remain semantic.
   An alternative employment arrangement mentioned in the description also defers to reasoning.
5. Otherwise load current English when available and accepted-current P1.6 opportunistically.
   Pending P1.6 is neither consumed nor regenerated. Source-only Persian/English reasoning is
   supported when no projection exists; ambiguity remains `uncertain`, not fabricated meaning.
6. Look up exact reusable membership before calling the model.
7. Make one bounded structured reasoning operation; schema validation retries are bounded
   separately. `uncertain` needs no retry or human approval.
8. Validate references and recheck eligibility/consumed evidence before saving.

Input is limited to 32,000 serialized characters without silent truncation. Model output is
limited to 2,048 tokens with a 16,384-token configured context. Oversized/invalid inputs,
provider failures, ineligible source state, and changing dependencies fail visibly rather
than becoming stored uncertainty or an exclusion. The later coordinator owns batch failure
ledgers; this service handles one candidate per call and performs no acquisition.

The LM Studio adapter uses bounded connection/write/pool timeouts, no generation read timeout,
zero transport replay, and no model tools. Normal tests use fake providers or mock HTTP only.
No host URL, API token, machine-local path, or raw provider protocol is saved in classifier identity.

## Reuse and correction

`MarketStore` remains the owner of persistence and immutable history. Reuse names:

- target-definition version and source-detail version;
- classifier contract, method, and identity;
- model/provider, prompt/schema, prompt hash, and generation controls for semantic decisions;
- exact current English and accepted P1.6 artifact IDs actually supplied, if any.

Changed source/target/classifier/consumed artifacts yield distinct decisions. Deterministic
source-only decisions do not gain unrelated translation/P1.6 dependencies.

`correct()` requires an explicit review note, valid references, the same current evidence,
and the latest decision under those dependencies. It records a superseding row; it cannot
overwrite history. Subsequent identical qualifications reuse that correction without a model call.

The service rechecks state across long model calls within the application's existing single
mutable operation boundary. It does not claim new multiprocess/concurrent-writer guarantees.

## Service entry point

`build_market_membership_service(settings, membership_model=...)` composes the existing
I2/source/translation/P1.6 stores and currentness owners. The override is optional; the
configured effective analysis model is the default. The factory itself performs no network
or model calls. No new browser route or CLI command is claimed in I3.

## Repository verification

Implementation commit:

```text
0eaf04109a57846aa6d0a920d0563f89a4dfb535
```

GitHub Actions CI for that implementation:

```text
run 1172
package install                     PASS
pip dependency consistency          PASS
installed public entrypoint smoke   PASS
Ruff                                PASS
pytest                              PASS — 608 passed
pytest -W error                     PASS — 608 passed
CI conclusion                       SUCCESS
```

The suite includes 42 new I3 cases: the eight representative scripted role outcomes,
source-only and accepted/P1.6-pending paths, unknown references, title-only rejection,
deterministic/ambiguous constraints, eligibility failures, source/freshness/analysis changes
during inference, exact dependency invalidation/reuse, reviewed correction history, input
bounds, provider failure, and structured HTTP/runtime behavior.

The representative fixture outcomes are explicit paraphrase/scripted expectations based on
the foundation boundary cases (`ta9l`, `tG9K`, `tGM0`, `t4jp`, `tmBK`, `t4qV`, `tmyX`, and
one sparse uncertain case). They are not new employer quotations or real-model evaluations.
No Jobinja request, operational Market mutation, registry mutation, P1.6 acceptance, or corpus
publication was performed by the repository test suite.

## Real-model boundary evaluation

After repository acceptance, a bounded real-model semantic evaluation was run against an
isolated copy of operational SQLite using the configured `gemma-4-e4b-it-ud` membership model.
The exact preserved evidence is under:

`docs/experiments/2026-09-17_market-i3-real-model-acceptance/`

The evaluation used seven real historical postings plus one synthetic sparse case and an
explicit 90-day retrospective freshness window. It did not refresh the jobs or claim that they
remained open on the evaluation date.

### Baseline target

With the broad membership intent:

```text
Applied AI / ML engineering work
```

the model matched 7/8 expected outcomes overall (6/7 real vacancies). The sole disagreement
was `tGM0`, a backend/software-infrastructure role in an AI team, which was classified
`core_match` instead of expected `adjacent_match`.

The baseline still correctly demonstrated:

- `ta9l` can be recognized as core without accepted P1.6;
- `tG9K` can consume accepted P1.6 opportunistically;
- AI-content creation is excluded from an engineering target;
- generic backend work that merely uses AI tools is excluded;
- unrelated security roles are excluded;
- sparse evidence becomes `uncertain` rather than fabricated certainty;
- every immediate rerun reused the exact membership without another model call.

### Clarified-target comparison

A controlled follow-up kept the same model, prompt/schema, and vacancy evidence but made the
target meaning explicit:

```text
Applied AI / ML engineering where the primary work is developing, evaluating, or improving
AI/ML models, agents, retrieval, or AI system behavior. Backend/API/database/infrastructure
roles primarily enabling or integrating AI services are adjacent rather than core. Using AI
tools for general software or content production does not qualify for this target.
```

That comparison produced 8/8 expected outcomes, including `tGM0 -> adjacent_match`, while
preserving both clear AI-engineering cases as core.

This 8/8 is **not** an independent accuracy benchmark. The clarified definition was written
after observing the baseline miss, so it is post-hoc boundary calibration evidence. The correct
product conclusion is that a target definition must state the intended core-vs-adjacent boundary
when that distinction matters. It is not evidence that the I3 prompt should be patched around
`tGM0` specifically.

The immediate reuse checks prove persisted-decision reuse, not fresh-call model reproducibility.
No repeated fresh-call stability study or larger blinded semantic benchmark was performed.

## Target-definition lesson

For target-relative Market membership:

```text
membership quality
= target definition quality
+ source/derived evidence quality
+ classifier contract/model behavior
```

A short label such as `Applied AI / ML engineering work` can be semantically under-specified
for edge cases where backend/platform work enables AI systems. The immutable
`TargetMarketDefinitionVersion.membership_intent` should explicitly encode core-vs-adjacent and
other material inclusion boundaries rather than expecting the membership prompt to infer the
user's unstated market semantics.

This finding does not reopen I3 and does not promote any role taxonomy.

## Decision and next boundary

```text
I1-I3: REPOSITORY ACCEPTED / CLOSED
I3 REAL-MODEL BOUNDARY CHECK: RECORDED / SUPPORTIVE WITH TARGET-DEFINITION CAVEAT
NEXT: I4 immutable snapshot construction
I5-I7: sequentially gated
```

I4 should construct immutable snapshots from exact current memberships with explicit P1.6
coverage states, separate source/semantic denominators, and a core-only primary corpus.
I7 still owns the bounded repeated-use real target workflow and broader semantic/product
acceptance. Do not promote membership into P2.2C/P2.2D, add report/subfamily/trend/personal
claims, or publish Market state.
