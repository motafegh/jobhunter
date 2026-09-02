# Portfolio PR3 — Documentation Information Architecture

**Status:** COMPLETE / ACCEPTED REPOSITORY-QUALITY INCREMENT  
**Date:** 2026-09-02  
**Track:** `docs/PORTFOLIO_READINESS_AND_PUBLIC_PRESENTATION_PLAN.md`  
**Product boundary:** No product semantics, accepted artifacts, P2.2 authority, runtime behavior, or source/test code changed.

## Objective

Make JobHunter's deep documentation understandable to an external reviewer without destroying the governance/reference structure that the repository actually uses.

## Evidence and decision

The `docs/` root already had useful history collections:

```text
decisions/
experiments/
incidents/
proposals/
working-memory/
```

The primary problem was therefore not a missing folder hierarchy. It was the absence of a clear documentation landing page/lifecycle map while stable controlling documents, active plans, closed plans, amendments, and historical records appeared together in the root.

`AGENTS.md` also explicitly routes contributors through stable root paths such as:

```text
docs/PRODUCT_SPECIFICATION.md
docs/ARCHITECTURE.md
docs/DOMAIN_AND_ANALYSIS_MODEL.md
docs/SOURCE_POLICY.md
docs/ROADMAP.md
docs/IMPLEMENTATION_PLAN.md
docs/EXECUTION_TODO.md
docs/WORKING_MEMORY.md
```

Mass-moving those files would create broad link/reference churn without improving product architecture.

## Implemented

1. Added `docs/README.md` as the documentation landing page and lifecycle/status map.
2. Defined an external-reviewer route from product → architecture → domain/source policy → current execution → deep history.
3. Classified current controlling documents separately from supporting subsystem guides.
4. Identified the active P2.2/P2.2B execution route separately from closed Phase-1/P2.1 plans.
5. Classified amendments, rolling state, closed/accepted records, experiments, proposals, incidents, decisions, and working memory explicitly.
6. Added future document-placement rules so new experiment/proposal/working-memory material does not return to a flat ambiguous root.
7. Kept widely referenced controlling filenames stable rather than moving files for cosmetic tidiness.
8. Rewrote `review-snapshots/README.md` to remove stale Phase-1 framing and reconcile the public corpus baseline to:

```text
Known/discovered jobs:       353
Fetched/parsed job details:   43
Current English projections:  20
English P1.6:                  5
Original P1.6:                 0
Capabilities:                  5
```

## Explicit non-actions

PR3 did **not**:

- move controlling product/architecture/policy files;
- mass-archive closed plans;
- delete historical documentation;
- rewrite Git history;
- create duplicate current-state owners;
- convert proposals/experiments into authority;
- change P2.2B product execution;
- fix historical document headers merely to make old records look current.

Some closed historical documents still contain wording such as `Active` from the period when they controlled work. `docs/README.md` now makes their current lifecycle unambiguous. Rewriting large historical plans solely to modernize old header wording would weaken their value as historical records and create unnecessary churn.

## Current documentation model

```text
README.md
  ↓
docs/README.md                         documentation navigation/lifecycle
  ↓
current stable authority
  PRODUCT_SPECIFICATION
  ARCHITECTURE
  DOMAIN_AND_ANALYSIS_MODEL
  SOURCE_POLICY
  UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY
  ROADMAP
  IMPLEMENTATION_PLAN
  ↓
current execution
  active P2.2 / P2.2B plans
  EXECUTION_TODO
  WORKING_MEMORY
  ↓
subsystem references / closed plans
  ↓
decisions / proposals / experiments / incidents / working-memory history
```

## Acceptance judgment

PR3 resolves the portfolio audit's main documentation-navigation problem without paying the cost/risk of a repository-wide file migration.

The public/current path is now explicit, while detailed engineering history remains available for deeper review.

## Next portfolio increment

Proceed to **PR4 — historical/versioned source disposition**.

PR4 must build an evidence-backed dependency/reference map before moving, archiving, or removing any versioned semantic source/test/script family. The presence of `v10`, `v11`, ..., `v20` filenames is not evidence that those files are dead.
