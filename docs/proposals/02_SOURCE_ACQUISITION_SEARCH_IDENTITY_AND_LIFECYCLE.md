# JobHunter Source Acquisition, Search, Identity, and Lifecycle Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B002-B006, B158, B161, B170

---

## Purpose

This file contains proposals for expanding how JobHunter discovers jobs, understands search effectiveness, preserves job identity across time, and detects change in source behavior. These proposals must remain subordinate to `docs/SOURCE_POLICY.md`: public-source boundaries, bounded requests, explicit adapters, evidence preservation, and cautious lifecycle interpretation remain permanent constraints.

---

## B002 — Multi-source acquisition ecosystem

**Intent:** Evolve JobHunter from a Jobinja-only collector into an adapter-based career-data acquisition system without turning it into an unrestricted crawler.

**Proposal:** Introduce additional approved public-source adapters over time. Candidate source types include public ATS/job-board APIs, selected company career boards, manually pasted supported job URLs, manually pasted vacancy text, local job documents, and user-controlled company watchlists.

**Design direction:**

- every source has an explicit adapter and source-policy contract;
- adapters declare supported operations such as discovery, detail fetch, lifecycle check, salary/location extraction, and stable identity;
- raw source evidence is preserved before normalization where acquisition permits it;
- common downstream services receive normalized records without pretending all source semantics are identical;
- unsupported arbitrary URLs remain rejected rather than routed through a generic scraper.

**Guardrails:** No CAPTCHA/access-control bypass, private authenticated platforms, rotating proxies, internet-wide crawling, or implicit browser automation. Manual text/document import should be clearly marked as user-supplied evidence rather than remotely verified source content.

**Promotion signal:** After the current Jobinja Phase-1 pipeline is accepted and a second source has a concrete repeated-use value that justifies the adapter abstraction.

---

## B003 — Search effectiveness and blind-spot intelligence

**Intent:** Learn whether JobHunter's acquisition vocabulary is actually productive.

**Proposal:** Track the downstream value of each search term, group, and pack through the acquisition funnel:

```text
search request
→ discoveries
→ unique contributions
→ duplicate overlap
→ detail acquisition
→ reviewed relevance
→ analyzable jobs
→ eventual target/opportunity value
```

A search can therefore be high-volume but low-value, or low-volume but uniquely productive.

**Design direction:**

- preserve deterministic counts from discovery provenance;
- distinguish unique contribution from total matches;
- later incorporate explicit human triage and accepted role intelligence;
- detect role titles/concepts appearing frequently in relevant jobs but missing from the configured search catalog;
- generate proposed search additions/removals/demotions for human review.

**Guardrails:** Search strategy suggestions never mutate the catalog silently. Search vocabulary remains acquisition recall, not career taxonomy or fit truth.

**Promotion signal:** Existing search-effectiveness views can grow incrementally once enough reviewed downstream outcomes exist.

---

## B004 — Repost and near-duplicate job identity

**Intent:** Prevent repeated advertisements from distorting lifecycle and market statistics while preserving exact source records.

**Proposal:** Add derived relationships that identify probable reposts, exact duplicates across source IDs, and near-duplicate advertisements with materially similar employer content.

**Possible entities:**

```text
DuplicateGroup
RepostChain
RelatedPostingGroup
```

**Design direction:**

- keep every source posting and evidence object intact;
- use deterministic identifiers where exact equivalence is provable;
- use reviewable similarity evidence where equivalence is probabilistic;
- distinguish “same logical vacancy reposted” from “same employer repeatedly hiring similar roles”;
- expose confidence and supporting fields such as company, title, location, content similarity, and publication timing.

**Guardrails:** Never merge or delete source history merely because titles/descriptions look similar. Model similarity may propose a relation but should not silently become canonical identity.

**Promotion signal:** Before trend analysis or duplicate-adjusted market statistics are treated as reliable.

---

## B005 — Semantic job-version diffing

**Intent:** Explain how an employer changed a job posting, not merely that its content hash changed.

**Proposal:** Build a derived `JobVersionDiff` over accepted source semantic versions. The system could identify changes such as:

- requirement added/removed;
- preferred wording strengthened to required or weakened in the opposite direction;
- responsibility added/removed;
- salary/location/work-mode change;
- experience/seniority change;
- substantial descriptive rewrite.

**Design direction:** Deterministic field-level diffs should be used where fields are structured. Model-supported semantic comparison may be added for free text, but must cite both source versions and remain derived. Diffs should be versioned by comparison contract.

**Guardrails:** Never overwrite history. A semantic diff is an interpretation of two immutable versions, not a replacement for either version.

**Promotion signal:** After enough real postings have multiple meaningful source versions to justify the capability.

---

## B006 — Rich lifecycle intelligence

**Intent:** Extend the cautious source-availability lifecycle into a more useful longitudinal view without weakening evidence standards.

**Proposal:** Future lifecycle/state interpretation could distinguish states such as `new`, `active`, `recently_updated`, `stable`, `stale`, `possibly_unavailable`, `expired`, `removed`, `returned`, and `probable_repost`.

**Design direction:**

- preserve the current conservative HTTP/source evidence rules;
- derive richer labels from sequences of observations rather than single failures;
- make every transition explainable from observations/version changes;
- keep explicit employer expiry stronger than inferred staleness;
- allow a timeline view per posting.

**Guardrails:** Transient network, rate-limit, access, or challenge failures do not prove removal. `stale` or `probably filled` must never be presented as authoritative employer state unless evidence supports it.

**Promotion signal:** Incrementally after current lifecycle acceptance is complete.

---

## B158 — Source/parser data-drift detection

**Intent:** Detect when an external source changes structure before silent parser degradation corrupts the corpus.

**Proposal:** Monitor deterministic acquisition/parser health over time for signals such as sudden drops in field completion, unexpected content-type changes, large shifts in description length, new unknown structures, or unusual error-class distributions.

**Design direction:**

- compute health metrics from actual parser/acquisition records;
- compare against recent accepted baselines;
- surface warnings in System/Data Quality rather than automatically changing parser logic;
- retain representative failing evidence for regression tests;
- allow per-source drift rules because source structures differ.

**Guardrails:** Drift detection should not become an opaque anomaly model unless simpler thresholds prove insufficient. Alerts must show the metric that changed.

**Promotion signal:** When multiple live acquisition runs provide enough baseline history to make trend monitoring useful.

---

## B161 — Search drift detection

**Intent:** Identify search vocabulary that has stopped contributing useful or unique jobs, and discover search areas whose value is changing.

**Proposal:** Track search effectiveness longitudinally. Example findings:

```text
"machine learning engineer" produced zero unique jobs in 10 recent bounded runs
"detection engineer" unique contribution increased materially
```

**Design direction:**

- use deterministic acquisition provenance first;
- optionally layer reviewed relevance/target outcomes later;
- compare fixed windows or market snapshots;
- distinguish temporary source scarcity from persistent degradation;
- create review proposals such as `keep`, `investigate`, `demote`, or `expand`.

**Guardrails:** Never auto-delete search terms based on one period. Market seasonality and source coverage can create misleading movement.

**Promotion signal:** Once repeated scheduled/manual acquisition creates a meaningful time series.

---

## B170 — Plugin-style source adapter contract

**Intent:** Give multiple sources a clean architectural boundary without prematurely building a generic plugin platform.

**Proposal:** After at least a second source demonstrates the need, define a minimal source-adapter protocol around operations such as:

```text
discover()
fetch_detail()
classify_response()
canonicalize_identity()
source_capabilities()
```

Adapters would reuse shared evidence, lifecycle, operation, and downstream processing infrastructure while preserving source-specific rules.

**Design direction:**

- keep source-specific normalization close to the adapter;
- define explicit capability flags rather than no-op methods;
- use one common source registry/configuration layer;
- require deterministic tests and source-policy review for every adapter;
- avoid dynamic third-party plugin loading initially.

**Guardrails:** Do not abstract Jobinja prematurely merely to satisfy an imagined future interface. Extract the contract from two or more real adapters.

**Promotion signal:** When a concrete second source is selected and implementation differences are understood.

---

## Category-level recommendation

The highest-value ideas in this family are a second policy-compliant source, improved search-effectiveness feedback, and identity/lifecycle quality needed for trustworthy longitudinal market analysis. The adapter abstraction should emerge from those real needs rather than lead them.