# Market Target, Relevance, Deduplication, and Trend Research

**Date:** 2026-09-07  
**Status:** REMOTE EXTERNAL DESIGN RESEARCH / IMPLEMENTATION NOT AUTHORIZED  
**Branch:** `main`  
**Controlling future plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Current product gate:** P2.2B-B1 remains open and local-runtime execution is intentionally postponed until owner PC access returns

## 1. Purpose

This is the second bounded external-research pass for the future Market / Role-Family Intelligence responsibility.

It focuses only on four questions that materially affect the first future Market vertical slice:

```text
1. What should define a target market?
2. How should JobHunter decide whether a discovered posting genuinely belongs to it?
3. How should reposts / near-duplicates affect prevalence counts?
4. What trend claims are defensible from versioned online-job-ad snapshots?
```

This record is design input only. It does **not** start the formal post-B1 Market foundation investigation, change the B1 gate, create new runtime contracts, or authorize Market-v2 source implementation.

---

## 2. External evidence reviewed

Primary reference families:

### European Commission / ESCO

- ESCO occupation model and occupational profiles:
  - https://esco.ec.europa.eu/en/classification/occupation-main
  - https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/occupation
- ESCO multilingual mapping research:
  - https://esco.ec.europa.eu/en/about-esco/data-science-and-esco/machine-learning-assisted-mapping-multilingual-occupational-data-esco-part-1
- ESCO mapping platform / expert correspondence model:
  - https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/esco-mapping-platform
- 2026 ESCO skill-classifier evaluation:
  - https://esco.ec.europa.eu/en/about-esco/publications/publication/evaluating-esco-skill-classifiers

### European Commission JRC

- Skills intelligence from online job advertisements:
  - https://joint-research-centre.ec.europa.eu/scientific-activities/employment/skills-intelligence-online-job-advertisements_en
- Job tasks and work organisation:
  - https://joint-research-centre.ec.europa.eu/scientific-activities/employment/job-tasks-and-work-organisation_en

### Cedefop / Eurostat

- Current OJA methodology project and update cycle:
  - https://www.cedefop.europa.eu/en/projects/skills-online-job-advertisements
- Skills-OVATE time-series policy:
  - https://www.cedefop.europa.eu/en/tools/skills-online-vacancies
- Skill trend definition:
  - https://www.cedefop.europa.eu/en/tools/skills-online-vacancies/skills/trends
- 2026 exploratory labour-demand imbalance work:
  - https://www.cedefop.europa.eu/en/data-insights/utilising-online-job-advertisements-identify-labour-market-imbalances
- 2019 collection/classification methodology:
  - https://www.cedefop.europa.eu/files/4172_en.pdf
- 2025 ten-year methodology review:
  - https://www.cedefop.europa.eu/en/publications/5610

### International Labour Organization

- Methodological issues related to online labour-market data:
  - https://webapps.ilo.org/static/english/intserv/working-papers/wp068/index.html

### Lightcast methodology references

- 2026 Job Posting Analytics methodology:
  - https://kb.lightcast.io/en/articles/6957446-job-posting-analytics-jpa-methodology
- 2026 occupation classification methodology:
  - https://kb.lightcast.io/en/articles/7907688-occupations-classification-methodology
- Unique postings / posting intensity:
  - https://kb.lightcast.io/en/articles/7934208-unique-job-postings
  - https://kb.lightcast.io/en/articles/7934091-posting-intensity
- Active vs newly posted:
  - https://kb.lightcast.io/en/articles/6957675-job-posting-types-newly-posted-and-active

These are references for design patterns and methodological risks. JobHunter must not import proprietary rules or external taxonomy authority merely because another system uses them.

---

## 3. Finding A — target market must separate acquisition scope from membership meaning

The strongest external pattern is that a **job title is not an occupation and an occupation is not one exact job**.

ESCO defines an occupation as a grouping of jobs with similar tasks and required skill sets. Occupational concepts include labels, descriptions, scope notes, skills/knowledge and hierarchical relationships. ESCO also explicitly treats job-title/description mapping as a normalisation/classification problem rather than simple title equality.

Lightcast's current occupation classifier similarly uses title **plus description**, country and language, with role/responsibility/skill terminology contributing to classification.

### JobHunter implication

The future `TargetMarketDefinition` should contain two deliberately different parts:

```text
ACQUISITION ENVELOPE
How do we obtain useful recall?

MEMBERSHIP INTENT
What kind of work/role actually belongs in the market report?
```

A provisional target definition should therefore be capable of recording:

```text
identity / name / version

acquisition envelope:
- approved source(s)
- search profiles / packs / explicit terms / URLs
- page/request/detail budgets
- acquisition geography constraints where source search supports them

membership intent:
- human-readable role/market description
- include role/work hints
- explicit exclusion hints where useful
- geography
- remote/hybrid/on-site scope when material
- seniority/experience scope when material
- employment type when material
- freshness/time window
```

This preserves the existing permanent rule:

```text
search vocabulary
!= target-market relevance truth
!= canonical role taxonomy
```

### Important non-decision

Do **not** predeclare that every target must map to exactly one ESCO/ISCO/O*NET occupation. A user target such as `AI security engineering` may intentionally cut across several conventional occupations while still forming a coherent evidence-backed work market.

External taxonomies may later support:

- search expansion;
- alias discovery;
- optional crosswalk/display;
- external validation/comparison;

but should not silently decide membership.

---

## 4. Finding B — relevance should be staged, evidence-backed, and allowed to remain unresolved

External occupation-classification systems use more than title matching. ESCO mapping research reports better suggestion quality when title and description are combined, and ESCO's mapping workflows use model/software suggestions followed by expert validation for durable cross-classification correspondence. Lightcast also classifies from title + description and contextual fields.

The 2026 ESCO skill-classifier evaluation is an additional caution: large labour-market classifiers require explicit evaluation because taxonomy scale and class imbalance make naive accuracy assumptions unsafe.

### Recommended future JobHunter shape

Use a two-stage target-membership process.

#### Stage 1 — deterministic eligibility/filtering

Examples subject to formal investigation:

```text
approved source
source/currentness/lifecycle eligibility
explicit geography constraint
explicit employment-type constraint
explicit hard exclusion
required evidence/dependency availability
```

These are not semantic role judgments.

#### Stage 2 — semantic role/work relevance

Evaluate the actual role using the strongest currently available evidence, likely including:

```text
title
source description
accepted responsibilities
accepted requirements
role purpose when present
current Work/Capability interpretation only where authorized and useful
```

Work/responsibility evidence should outweigh superficial title similarity when they conflict.

Provisional dispositions remain sensible:

```text
core_match
adjacent_match
uncertain
excluded
```

Every non-trivial semantic disposition should preserve:

```text
target-definition version
posting/source-version identity
classification contract/model identity if applicable
disposition
short reason
supporting evidence references
review/correction state if later introduced
```

### Denominator implication

Do not automatically combine all four states into one prevalence denominator.

A strong first hypothesis is:

```text
primary prevalence denominator = approved core members
adjacent                      = reported separately
uncertain                     = reported separately / no forced decision
excluded                      = traceable but outside report denominator
```

The formal investigation must test whether some target types should admit reviewed adjacent members, but `uncertain` should never silently contaminate strong prevalence claims.

### Human review boundary

Human review should be proportional to blast radius:

- no need to manually approve every obvious low-risk core/excluded case if deterministic/model evidence is strong and the output remains candidate market interpretation;
- borderline membership should be correctable/reviewable;
- any mapping promoted into reusable canonical taxonomy requires a stronger review boundary than one report's candidate membership.

---

## 5. Finding C — JobHunter needs three distinct duplicate concepts

The external deduplication evidence makes an important distinction that JobHunter should preserve explicitly.

### C1. Same logical posting observed repeatedly

JobHunter already has strong source identity, observations, semantic source versions and lifecycle state.

Repeated checks of the same `source_job_id` must **not** create multiple demand units.

This problem is largely already handled by the current source model.

### C2. Repost / new source ID representing materially the same hiring demand

This is the important first Market-v2 dedup problem under the current single-source policy.

A future candidate duplicate/repost detector should investigate signals such as:

```text
same/normalized employer
same or near-equivalent title
same location / compatible remote scope
bounded temporal proximity
same or near-equivalent source description / semantic content
strong overlap in responsibilities / requirements
```

Do not choose final fields/thresholds until tested against real Jobinja examples.

### C3. Cross-source duplicate advertisement

This matters only after a second recurring source is actually approved.

Do not build multi-source duplicate infrastructure now merely because commercial systems require it.

### Preservation rule

Deduplication must never mean deleting evidence.

Preferred conceptual flow:

```text
all source advertisements/identities preserved
→ candidate duplicate/repost relationships
→ explicit group/disposition
→ one approved demand representative for prevalence denominator
→ all members remain drill-down evidence
```

Ambiguous relationships should remain unresolved rather than silently collapsed.

### Metrics rule

The external distinction between total postings and unique postings is useful.

JobHunter should eventually be able to report separately:

```text
raw advertisements / posting identities seen
approved unique demand units
candidate/confirmed repost groups
```

If useful later:

```text
advertising intensity = raw advertisements / unique demand units
```

But advertising intensity is **not** equivalent to skill/role demand and should never replace the deduplicated prevalence denominator.

---

## 6. Finding D — trend analysis must separate market stock from market flow

Lightcast distinguishes:

```text
NEWLY POSTED
postings first appearing during the period

ACTIVE
postings live at any point during the period
```

This distinction is highly relevant to JobHunter because its current source model already records first/last-seen and lifecycle evidence.

### JobHunter implication

A future Market report should avoid one ambiguous `job count over time` metric.

Candidate temporal measures:

```text
new unique postings in period       → hiring-advertising flow
active unique postings in snapshot  → currently visible/open advertising stock
```

The exact semantics must match JobHunter's cautious lifecycle model; a failed refresh cannot become proof that a posting stopped being active.

---

## 7. Finding E — time-series comparability is stricter than snapshot persistence

Cedefop's current Skills-OVATE policy explicitly excludes job-ad portals that do not provide a stable feed over time from its comparable time-series dashboards. That is a stronger lesson than merely saving old reports.

Cedefop also presents recent trends over four-quarter windows and commonly compares the latest quarter against the same quarter of the previous year, which reduces seasonal distortion. ILO methodology notes that online-labour-data fluctuations can contain trend/cycle, seasonal and irregular components.

### JobHunter implication

Before comparing two snapshots, validate at least:

```text
target-definition identity/version
source/search scope
source-coverage/feed comparability
membership-policy version
dedup-policy version
aggregate-contract version
concept-normalization contract where relevant
denominator semantics
minimum evidence/support
```

A stored old snapshot is necessary but not sufficient for a valid trend.

If a major acquisition/classification/dedup contract changes, the system should say:

```text
NOT DIRECTLY COMPARABLE
```

rather than calculate a polished but misleading delta.

---

## 8. Finding F — first trend metrics should be simple and inspectable

JobHunter does not need a forecasting/time-series platform for its first historical Market slice.

A professional initial comparison can remain deterministic and transparent.

For each sufficiently supported concept/work pattern, candidate outputs are:

```text
previous unique-posting support
current unique-posting support
absolute count delta
previous prevalence share
current prevalence share
percentage-point prevalence delta
distinct-employer support change
```

Potential relative percentage change can be shown only when the previous denominator/support makes it meaningful; avoid explosive percentage claims from tiny baselines.

### Same-quarter year-over-year

When JobHunter eventually has enough history, same-quarter previous-year comparison is a useful option for seasonal robustness, consistent with Cedefop's public trend presentation.

Before one year of comparable history exists, JobHunter should use explicit adjacent-window/snapshot comparison and state the limitation rather than pretend it is seasonally adjusted.

### Do not add yet

No current evidence justifies implementing:

- ARIMA/Prophet/forecast models;
- automatic seasonal adjustment;
- trend prediction;
- labour-shortage inference from posting counts alone;
- a composite `market heat` score.

---

## 9. Finding G — `emerging` needs a multi-condition evidence rule

Current external methodology reinforces the existing JobHunter decision that `emerging` cannot mean `rare today`.

A future `emerging` disposition should require evidence across **comparable historical windows**.

Provisional evidence conditions for investigation:

```text
1. more than one comparable historical interval;
2. sufficient absolute unique-posting support;
3. increase is not caused only by a denominator collapse;
4. increase is not dominated by one employer/repost group;
5. support appears across more than one employer when the sample permits;
6. direction is sustained enough to distinguish it from one-window noise;
7. classification/normalization contract is comparable across windows.
```

Do not freeze numeric thresholds now. Cedefop's 2026 imbalance experiment, for example, excludes occupations without minimum data coverage and in one analysis requires at least 50 OJAs plus broad country coverage; those thresholds fit its EU-scale statistical purpose and should **not** be copied into a personal JobHunter corpus.

JobHunter should derive its own minimum-support/warning rules from real corpus behavior during the formal investigation.

---

## 10. Finding H — prevalence counts need exact denominator semantics

A posting can contain many skills/requirements. Summing concept rows therefore exceeds the number of postings and is not an error.

The useful question is:

```text
How many qualified unique postings mention this concept/work pattern?
```

not:

```text
What share of all extracted mentions belongs to this concept?
```

### Recommended aggregate invariant

For each aggregate concept/group:

```text
one qualified unique demand unit contributes at most 1 to posting-support count
```

while retaining separate internal counts for strength/category/evidence where needed.

Report examples should expose:

```text
Python — 44 / 63 qualified unique postings (70%)
required: 31 postings
preferred: 8 postings
contextual: 5 postings
```

Strength categories may be non-exclusive if a posting legitimately contains multiple claims of different strengths for the same concept; the exact semantic rule must be inherited from accepted P1.6/Market behavior and documented rather than forced to add up deceptively.

---

## 11. Refined design hypotheses for the formal post-B1 investigation

Carry these forward as **hypotheses to verify**, not frozen implementation contracts:

1. `TargetMarketDefinition` separates acquisition envelope from membership intent.
2. Target membership uses deterministic eligibility first, semantic work/role relevance second.
3. Role relevance uses title + description + accepted work/requirements; title alone is insufficient.
4. `core_match / adjacent_match / uncertain / excluded` remains the leading membership-state design.
5. Primary prevalence initially uses approved core members; adjacent/uncertain are visible separately.
6. External ESCO/O*NET mappings, if introduced, are optional references/crosswalks rather than JobHunter authority.
7. First dedup scope is same-source repost/new-ID detection; cross-source dedup waits for a real second source.
8. Dedup groups evidence; it never deletes source records.
9. Strong prevalence uses unique demand units; raw posting/advertising intensity is separate.
10. Temporal reporting distinguishes newly-posted flow from active-market stock.
11. Snapshot comparison requires contract/source/feed comparability, not just two timestamps.
12. First trend metrics remain counts, shares, percentage-point deltas and employer breadth—not forecasting.
13. `emerging` requires sustained comparable evidence, minimum support and employer/repost safeguards.
14. Tiny-sample trend claims should be suppressed or explicitly marked insufficient rather than assigned arbitrary significance.
15. Concept prevalence counts postings, not raw mention frequency.

---

## 12. Acceptance questions to preserve for the later formal investigation

When B1 closes and the formal Market foundation investigation begins, answer these with real repository/runtime evidence:

### Target contract

- What is the smallest target definition that supports both acquisition recall and membership intent without duplicating search-registry state?
- Which target dimensions are hard filters versus semantic hints?
- How is target versioning/fingerprinting handled?

### Membership

- Can current English/P1.6 substrate classify core/adjacent/uncertain/excluded without a new semantic layer?
- Is source description needed before P1.6 exists to avoid expensive analysis of obviously irrelevant jobs?
- What is the cheapest reliable staged classifier flow?
- Which ambiguous cases deserve owner correction/review?

### Dedup/reposts

- How many real same-employer/title/new-ID repost examples exist in current Jobinja evidence?
- Which deterministic fields are reliable enough for candidate grouping?
- Is semantic content similarity needed, and if so at what stage?
- What false-positive cases would make collapse dangerous?

### Trends

- Which current source observations reliably support `newly posted` versus `active` semantics?
- What refresh cadence makes two snapshots meaningfully comparable?
- What contract changes invalidate comparison?
- What minimum sample/employer support is needed for prevalence and for `emerging`?

---

## 13. Current boundary after research

```text
P2.2B-B1 local execution          PAUSED UNTIL OWNER PC ACCESS
Market owner activation           GIVEN / QUEUED BEHIND B1
Market formal foundation audit    NOT STARTED
Market implementation             NOT AUTHORIZED
External Market research          SECOND FOCUSED PASS COMPLETE
```

This research reduces uncertainty for the later formal investigation but does not replace that investigation because the real answers must be reconciled with JobHunter's current services, SQLite schema, corpus behavior, accepted artifacts and representative real cases at activation time.
