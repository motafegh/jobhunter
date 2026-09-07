# Local Runtime Pause and Remote Market Research

**Date:** 2026-09-07  
**Status:** LOCAL-RUNTIME WORK INTENTIONALLY POSTPONED / REMOTE-SAFE WORK CONTINUING  
**Branch:** `main`  
**Current product frontier:** P2.2B-B1 remains open at the `ta9l` English projection/P1.6 acceptance gate  
**Queued next product responsibility:** Market and Role-Family Intelligence foundation investigation after B1 closure

## 1. Owner decision

The owner currently does not have access to the machine-local JobHunter runtime and explicitly chose to postpone work that requires the local PC/runtime until access returns.

This is an **operational postponement**, not a product rejection, failed gate, or changed semantic decision.

Paused local-dependent work includes:

```text
P2.2B-B1
- ta9l current English projection
- ta9l English P1.6 v20/v5 generation
- ta9l semantic review/acceptance
- final correspondence review against tG9K
- possible one-concept/two-mapping registry mutation

Portfolio/release
- real local browser screenshots
- screenshot privacy review against the running local application
- any release action that depends on those screenshots/local verification
```

When local access returns, resume from the existing recorded `ta9l` preflight rather than repeating repository-side evidence selection.

## 2. Remote-safe work policy during the pause

While local runtime is unavailable:

- do not manufacture a B1 closure;
- do not create the tentative canonical responsibility concept before the accepted `ta9l` P1.6/final correspondence gate;
- do not start Market-v2 implementation while B1 remains open;
- do not start P2.2C/P2.2D merely to avoid waiting;
- do not perform redundant repository ceremony;
- do allow independent repository/release checks, bounded external research, design references, documentation reconciliation, and learning/review work that does not bypass active product gates.

## 3. Remote repository/release verification

Remote GitHub state checked on 2026-09-07:

```text
latest inspected main commit:
bd082de93a2f09de54cc18defd9c676d5884312c

latest CI run on that commit:
CI run 1119
status: completed
conclusion: success

repository visibility: public
license detected by GitHub: MIT
description: null
topics: []
homepage: null
```

The prepared portfolio package already recommends:

```text
description:
Local-first career intelligence from real job evidence, with provenance-preserving LLM analysis, semantic review, and auditable Python workflows.

topics:
python
fastapi
sqlite
llm
lm-studio
career-intelligence
job-market
provenance
local-first
pydantic

homepage:
leave blank until a real hosted destination exists
```

The current GitHub connector available in this work session can inspect repository metadata but does not expose repository-description/topic mutation. Therefore this concrete settings action remains pending rather than being falsely marked complete.

## 4. Bounded external research for future Market / Role-Family Intelligence

This research is **design input only**. It does not activate the formal Market implementation investigation or authorize source implementation while B1 remains open.

### 4.1 ESCO as an external reference vocabulary, not JobHunter authority

Current European Commission ESCO material shows that ESCO provides:

- a hierarchical occupation classification;
- occupation descriptions/profiles;
- preferred, non-preferred and hidden terms;
- linked skills/competences/knowledge;
- multilingual terminology;
- mappings to ISCO-08;
- machine-usable classifications and APIs.

Current version observed during research: ESCO v1.2.1, updated in December 2025.

Relevant sources:

- https://esco.ec.europa.eu/en/classification
- https://esco.ec.europa.eu/en/classification/occupation-main
- https://esco.ec.europa.eu/en/classification/skill-main
- https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/esco-v12

**JobHunter implication:**

ESCO may later be useful as an optional external reference/crosswalk source for aliases, occupation comparison and multilingual normalization. It should **not** replace JobHunter's evidence-derived Canonical Registry, silently decide target-market membership, or force every posting into a predefined ESCO occupation.

This aligns with the existing rule:

```text
search vocabulary
!= target-market relevance truth
!= canonical role taxonomy
```

### 4.2 O*NET supports keeping market dimensions separate

O*NET's Content Model explicitly separates worker requirements, knowledge, education, experience/training, work activities, work context and occupation-specific information.

Relevant sources:

- https://www.onetcenter.org/content.html
- https://www.onetcenter.org/competencyFrameworks.html
- https://www.onetcenter.org/dictionary/30.0/text/skills_to_work_activities.html

**JobHunter implication:**

This supports the current design direction of not flattening everything into one `skill` bucket. Market-v2 should continue to distinguish, where evidence permits:

```text
tools / technologies
skills / applied capabilities
knowledge
responsibilities / work activities
experience / seniority
education / credentials
work context
```

O*NET should be treated as a conceptual/reference framework, not copied wholesale into the internal domain model without a demonstrated use case.

### 4.3 Online job advertisements are not the whole labour market

European Commission JRC, Cedefop and ILO material consistently warns that online job advertisements are valuable high-frequency evidence but are not equivalent to all job vacancies or the whole labour market. Representation differs across occupation types and advertised skills can over/under-emphasize particular work characteristics.

Relevant sources:

- https://joint-research-centre.ec.europa.eu/scientific-activities/employment/skills-intelligence-online-job-advertisements_en
- https://www.cedefop.europa.eu/en/tools/skills-intelligence/trend-focus/skills-online-job-advertisements
- https://www.cedefop.europa.eu/de/publications/5610
- https://www.ilo.org/publications/methodological-issues-related-use-online-labour-market-data

**JobHunter implication:**

The planned Market report should never claim that a qualified Jobinja snapshot is `the market` without scope qualification. Preserve:

- source scope;
- search/target scope;
- sample size;
- analyzed/qualified coverage;
- distinct-employer support;
- concentration warnings;
- missing/incomplete processing;
- explicit statement that online postings are recruitment-advertising evidence, not a census of vacancies/employment.

This strengthens the existing plan's sample/concentration and evidence-limit sections rather than adding a new subsystem.

### 4.4 Duplicate/repost treatment is a real analytical requirement

Lightcast's current Job Posting Analytics methodology uses a two-stage deduplication concept:

1. source-level filtering to avoid recollecting the same advertisement from one source;
2. cross-source comparison using normalized fields such as title, company and location across a bounded time window.

Lightcast also distinguishes total postings from unique/deduplicated postings and exposes posting intensity separately.

Relevant sources:

- https://kb.lightcast.io/en/articles/6957446-job-posting-analytics-jpa-methodology
- https://kb.lightcast.io/en/articles/6957661-how-does-lightcast-handle-duplicate-postings
- https://kb.lightcast.io/en/articles/7934208-unique-job-postings
- https://kb.lightcast.io/en/articles/7934091-posting-intensity

**JobHunter implication:**

Do not copy Lightcast's proprietary/fixed rules mechanically. The useful design pattern is:

```text
preserve every source observation/posting
→ identify candidate duplicate/repost groups
→ assign explicit duplicate relationship/disposition
→ aggregate prevalence on the approved unique-posting denominator
→ optionally expose raw advertising intensity separately
```

For JobHunter's first single-source implementation, source identity/version logic already eliminates some same-posting re-observation inflation. The formal investigation should focus on same-employer repost/new-ID cases before worrying about cross-source duplicates that cannot yet exist under current source policy.

No opaque semantic-similarity threshold should silently delete evidence.

### 4.5 Point-in-time snapshots are required for defensible trends

Current Lightcast documentation explicitly recommends point-in-time exports for reproducible longitudinal work because enrichment/classification can change over time. Cedefop/JRC similarly emphasize processing/classification methodology when interpreting OJA trends.

Relevant source:

- https://docs.lightcast.io/lightcast-api/docs/investment-support

**JobHunter implication:**

The existing Market plan is correct to preserve versioned snapshots instead of recomputing old periods with today's classification and calling the difference a historical trend.

A future comparable snapshot should preserve at minimum:

```text
target-definition identity/version
snapshot/run time
source scope
membership-policy version
deduplication-policy version
aggregate-contract version
qualified member identities/source versions
denominator semantics
```

`emerging` remains a longitudinal conclusion only when comparable snapshots support it.

## 5. Research conclusions worth carrying into the formal investigation

The external research does **not** justify a major architecture change. It reinforces the current plan and suggests the following investigation hypotheses:

1. keep JobHunter's internal evidence-derived model primary;
2. evaluate ESCO later as an optional external crosswalk/reference vocabulary, not authority;
3. preserve separate dimensions for work, skills/capabilities, knowledge, tools, experience, education and context;
4. explicitly label OJA scope/representativeness limitations in every market report;
5. make unique/deduplicated postings the strong prevalence denominator once the duplicate policy is accepted;
6. preserve raw total/repost intensity separately if it becomes useful rather than conflating it with demand;
7. begin duplicate work with same-source repost/new-ID cases because Jobinja is currently the only approved recurring source;
8. preserve point-in-time snapshots and contract versions for trends;
9. do not force ESCO/O*NET role taxonomies into JobHunter's candidate role-family reasoning;
10. do not add new external taxonomy infrastructure before the first Market vertical slice proves a concrete need.

## 6. Current remote-work state

```text
P2.2B-B1 local execution          PAUSED BY OWNER UNTIL PC ACCESS
B1 repository-side preparation   COMPLETE
Market plan activation           QUEUED BEHIND B1
Market source implementation     NOT AUTHORIZED
Market external research         FIRST BOUNDED PASS COMPLETE
latest main CI                    GREEN
GitHub description/topics        CONFIRMED PENDING
real browser screenshots         PAUSED UNTIL LOCAL ACCESS
release tag/release               NOT YET AUTHORIZED
```

## 7. Sensible next remote-safe work

Without changing product gates, useful follow-on work can be chosen from:

```text
A. bounded deeper Market research only where a specific design question remains;
B. inspect repository/public documentation for stale release metadata/version claims;
C. owner-learning / architecture review using current source and real accepted examples;
D. inspect whether any remote-only PR9 blocker can be completed with available GitHub capabilities;
```

Do not create additional work merely to fill the local-runtime pause.