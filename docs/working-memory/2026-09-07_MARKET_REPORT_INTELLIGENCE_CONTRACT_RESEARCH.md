# Market Report Intelligence Contract Research

**Date:** 2026-09-07  
**Status:** REMOTE EXTERNAL DESIGN RESEARCH / IMPLEMENTATION NOT AUTHORIZED  
**Branch:** `main`  
**Controlling future plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`  
**Current product gate:** P2.2B-B1 remains open; local `ta9l` execution is intentionally postponed until owner PC access returns

## 1. Purpose

This is the third bounded external-research pass for the future Market / Role-Family Intelligence responsibility.

It focuses on the report itself:

```text
1. What should one Role-Family Intelligence Report contain?
2. Which market metrics are defensible and useful?
3. How should responsibilities, tools, skills, knowledge, experience and context remain distinct?
4. How should candidate role subfamilies be generated and presented without becoming fake taxonomy?
```

This record is design input only. It does **not** start the formal post-B1 Market investigation, change current semantic contracts, or authorize Market-v2 implementation.

---

## 2. External evidence reviewed

Primary references:

### Cedefop / European labour-market intelligence

- Skills in online job advertisements:
  - https://www.cedefop.europa.eu/en/projects/skills-online-job-advertisements
- Occupation focus dashboard:
  - https://www.cedefop.europa.eu/en/tools/skills-online-vacancies/occupations/focus
- Skills trends dashboard:
  - https://www.cedefop.europa.eu/en/tools/skills-online-vacancies/skills/trends
- Sectors, skills and occupations:
  - https://www.cedefop.europa.eu/en/tools/skills-online-vacancies/sectors/skills-occupations
- Delivering evidence from online job advertisements (2025):
  - https://www.cedefop.europa.eu/en/publications/5610

### ESCO

- Current classification:
  - https://esco.ec.europa.eu/en/classification
- Occupation profiles:
  - https://esco.ec.europa.eu/en/classification/occupation-main
- Skills/knowledge hierarchy:
  - https://esco.ec.europa.eu/en/classification/skill-main
- Essential / optional semantics:
  - https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/essential
  - https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/optional

### O*NET

- Content Model:
  - https://www.onetcenter.org/content.html
- Database / work activities / technology skills / knowledge / work context:
  - https://www.onetcenter.org/database.html
- Occupation report structure:
  - https://services.onetcenter.org/reference/online/occupation

### OECD

- Skills for the Digital Transition — online job postings methodology:
  - https://www.oecd.org/en/publications/skills-for-the-digital-transition_38c36777-en/full-report/component-5.html
- Occupation-cluster concept:
  - https://www.oecd.org/en/publications/skills-for-the-digital-transition_38c36777-en/full-report/component-9.html
- Human capital behind AI — skill bundles:
  - https://www.oecd.org/en/publications/the-human-capital-behind-ai_2e278150-en.html
- Speaking the same language — skill classification:
  - https://www.oecd.org/en/publications/speaking-the-same-language_adb03746-en.html

---

## 3. Main conclusion: the report should be layered, not one ranked list

External labour-market systems repeatedly separate dimensions that are materially different:

```text
what the worker must know
what the worker must be able to do
what work/tasks/activities are performed
which technologies/tools are used
what education/experience is expected
what context the work occurs in
```

O*NET explicitly separates Skills, Knowledge, Education/Experience, Work Activities, Tasks, Technology Skills and Work Context. ESCO distinguishes knowledge from skill/competence concepts and links those to occupations. Cedefop analyses skills together with occupations, sectors and other vacancy attributes.

**JobHunter implication:**

Do not produce one flattened `Top skills` ranking that mixes Python, threat modelling, communication, MSc, five years of experience and monitoring responsibilities.

The report should preserve separate semantic sections and only provide cross-section synthesis where it is analytically justified.

---

## 4. Proposed report structure for the later formal investigation

The following is a strong design hypothesis, not yet a runtime contract.

### 4.1 Evidence / corpus quality header

Every report should start with the evidence boundary before interpretation:

```text
target name / definition version
snapshot/run time
source scope
candidate postings discovered
current source postings available
core / adjacent / uncertain / excluded membership counts
qualified unique-demand units
raw advertisements/observations
repost/duplicate adjustments
distinct employers
largest-employer share
current English/P1.6 coverage
important missing/stale processing
sampling / concentration / comparability warnings
```

This makes the denominator and evidence quality visible before the user reads any percentage.

### 4.2 Market shape

Useful factual context may include:

- unique qualified postings;
- newly-posted versus active-market counts when the temporal contract supports both;
- distinct employers;
- geography distribution;
- remote/hybrid/on-site distribution when explicitly available;
- seniority/experience distribution;
- employment type;
- sector/company distribution where available and useful.

Do not interpret missing fields as negative evidence.

### 4.3 Responsibilities / work demanded

This should answer:

> What do employers actually expect people in this target market to do?

For each responsibility/work pattern preserve:

```text
candidate/promoted identity and label
unique-posting count + share
distinct-employer support
representative exact responsibility wording
evidence drill-down
candidate/promoted/uncertain status
important source-specific details deliberately not normalized away
```

Accepted P1.6 responsibilities remain the factual substrate. Work Intelligence or later candidate family synthesis may organize them, but model prose must not replace the accepted source work.

### 4.4 Requirements by semantic type

Keep separate sections for at least:

```text
technologies / tools / platforms / languages
applied technical skills / capabilities
knowledge areas
practices / methods
professional / transversal capabilities
language requirements
education / credentials
experience / seniority
```

This is especially important because OECD explicitly notes that many items commonly pooled under the word `skills` are actually knowledge areas, technologies/tools or abilities.

### 4.5 Requirement rows: minimum useful metrics

For each normalized/canonical concept, investigate preserving:

```text
concept label
concept type
normalization state: reviewed canonical / bounded normalized / unmapped
unique-posting count
unique-posting share
distinct-employer count
required / preferred / contextual / inferred distribution
explicit source-depth distribution where supported
representative source wording / aliases
source job drill-down
coverage / concentration warnings
```

Do not create a composite opaque `importance score` merely to sort everything.

A simple deterministic order such as unique-posting prevalence with visible employer breadth is preferable initially.

### 4.6 Employer strength is not ESCO essentiality

ESCO distinguishes `essential` versus `optional` knowledge/skills/competences at the **occupation-profile** level:

- essential = usually required for the occupation independent of employer/context;
- optional = may be required depending on employer/context/country.

JobHunter's current P1.6 strength is vacancy-specific:

```text
required
preferred
contextual
inferred
```

These are different semantics.

**Rule:** do not translate JobHunter `required` into ESCO `essential`, or ESCO `optional` into JobHunter `preferred`.

ESCO may later provide an external occupation reference/crosswalk only.

### 4.7 Technology/tool demand is not capability demand

A tool mention should stay a tool/technology signal unless evidence supports a broader applied capability.

Example:

```text
Kubernetes          → technology/platform demand
container orchestration / platform operations → broader capability/work interpretation
```

The report may connect them, but should not silently substitute one for the other.

### 4.8 Knowledge is not the same as applied skill

Preserve source distinctions such as:

```text
knowledge of networking principles
vs
configure / troubleshoot networks
```

The first is knowledge; the second is applied capability/work evidence.

This aligns with both ESCO and O*NET's explicit separation of knowledge from skills/work activities.

### 4.9 Experience / seniority / education

Aggregate source-explicit signals separately:

- years/duration;
- junior/mid/senior wording;
- prior-domain experience;
- education level/field;
- certifications/credentials;
- management/leadership/ownership only when explicitly supported.

Do not mechanically turn years of experience into technical depth.

---

## 5. Market demand labels: raw evidence first

The current future plan considers human-readable bands such as `core`, `common`, or `specialized`.

The research supports **not** locking those thresholds prematurely.

Initial report output should prefer transparent evidence:

```text
Python
42 / 60 unique qualified postings = 70%
31 distinct employers
required 28 | preferred 9 | contextual 5
```

rather than:

```text
Python → CORE → score 94
```

If later demand bands are useful, the formal investigation should define them from:

- unique-posting share;
- employer breadth;
- minimum denominator/support;
- concentration effects;
- target-specific semantics;
- stability across representative snapshots.

Do not invent a universal threshold before evidence shows it is useful.

---

## 6. Co-occurrence and bundles

OECD labour-market work uses skill bundles and occupation similarity because combinations can reveal structure that individual frequencies miss.

JobHunter can eventually show useful combinations such as:

```text
Python + SQL
Kubernetes + cloud platform
LLM evaluation + observability
threat analysis + security automation
```

But the first contract should keep this bounded:

- count each unique demand unit at most once per combination;
- require enough support to avoid one-posting curiosities;
- expose distinct-employer support;
- avoid combinations dominated by one employer;
- do not interpret co-occurrence as prerequisite, causation, substitution or hierarchy;
- do not build a graph platform merely to display useful pairs/bundles.

Pairwise/bounded bundle tables are enough for the first useful slice.

---

## 7. Candidate role subfamilies

The most useful report-level interpretation is likely not a forced occupation taxonomy but a small number of **candidate work-composition subfamilies**.

OECD occupation-cluster work demonstrates that occupations can be grouped through similarity in underlying demanded skills. JobHunter has a richer evidence boundary because accepted responsibilities/work are available in addition to skills.

### 7.1 Proposed semantic basis

Candidate subfamily reasoning should weight approximately in this order:

```text
accepted recurring responsibilities / work
→ capability / requirement bundles
→ tools / knowledge / context
→ title wording as supporting evidence
```

Titles alone should not control subfamily membership.

### 7.2 Do not require a partition

The model should not be forced to assign every posting to exactly one subfamily.

Allow:

```text
primary candidate membership
secondary/overlapping membership when materially real
uncertain / mixed role
no useful subfamily assignment
```

A hybrid role is evidence, not a classification failure.

### 7.3 Candidate subfamily card

For each displayed candidate subfamily, investigate showing:

```text
candidate label
short evidence-qualified description
supporting unique postings
supporting distinct employers
recurring work/responsibility patterns
distinguishing requirements/capabilities
typical technologies/knowledge where supported
representative source titles
representative jobs/evidence
uncertainty / overlap notes
candidate vs promoted authority label
```

### 7.4 No automatic canonical promotion

A report-level candidate subfamily is analytical interpretation.

It does not automatically become:

- a canonical responsibility family;
- a stable role archetype;
- a permanent career taxonomy;
- a personal recommendation category.

Repeated support across snapshots/employers may later justify a separate promotion decision.

---

## 8. Trend section: changes should use multiple transparent measures

When comparable historical snapshots exist, one metric is not enough.

For a concept/work pattern investigate showing:

```text
current unique-posting count
previous comparable count
current share
previous share
percentage-point share change
relative percentage change when denominator/base is sufficient
current vs previous distinct-employer support
newly-posted vs active-market interpretation where relevant
```

Why both absolute and relative movement matter:

```text
1 → 3 postings = +200%
```

looks dramatic despite weak support. Cedefop explicitly warns that growth rates can be distorted by small base values.

Therefore:

- show absolute support alongside relative change;
- suppress or strongly warn on tiny bases;
- preserve employer breadth;
- require comparable snapshot contracts;
- keep `emerging` stricter than `increased this period`.

---

## 9. Proposed report reading order

A useful browser/report reading order is now:

```text
1. Target + Evidence Quality
2. Executive Market Summary
3. Market Shape
4. Responsibilities / Work Demand
5. Technologies / Tools
6. Applied Skills / Capabilities
7. Knowledge / Practices
8. Professional / Transversal Capabilities
9. Experience / Seniority / Education / Credentials
10. Work Context / Geography / Arrangement
11. Useful Co-occurrence / Bundles
12. Candidate Role Subfamilies
13. Changes Since Comparable Snapshot (when valid)
14. Evidence Drill-down + Method / Limitations
```

The executive summary should synthesize these deterministic/qualified sections; it should not invent additional unsupported market facts.

---

## 10. Recommended first-slice exclusions

Do **not** add these merely because market-intelligence products sometimes have them:

```text
one overall market score
one job-fit/readiness score
salary benchmarks before source coverage is adequate
forecasting future hiring from a tiny local corpus
causal claims about why demand changed
network/graph UI before bounded co-occurrence proves insufficient
automatic ESCO/O*NET occupation assignment as authority
a universal core/common/niche threshold
a forced exhaustive role-subfamily taxonomy
personal recommendations before reviewed personal evidence exists
```

---

## 11. Design decisions/hypotheses to carry into the formal post-B1 investigation

1. Put evidence quality and denominator semantics at the top of every report.
2. Keep responsibilities/work, technologies, applied skills, knowledge, experience, education and context as separate analytical dimensions.
3. Use exact unique-posting prevalence and distinct-employer breadth before any synthetic demand score.
4. Preserve vacancy-specific `required/preferred/contextual/inferred`; do not reuse ESCO `essential/optional` terminology for employer-strength evidence.
5. Treat tools as tools unless broader capability/work evidence exists.
6. Aggregate accepted P1.6 responsibilities as the factual work substrate.
7. Allow Work Intelligence/model reasoning to organize work, not manufacture it.
8. Start co-occurrence with bounded pairs/bundles rather than new graph infrastructure.
9. Generate candidate role subfamilies mainly from recurring work + requirement/capability composition; titles remain supporting evidence.
10. Allow overlapping, mixed and uncertain subfamily membership instead of forcing a partition.
11. Keep candidate subfamilies explicitly non-canonical until a separate evidence/promotion decision.
12. Trend rows should show absolute counts, shares, percentage-point movement, relative movement when safe, and employer breadth.
13. Small-base changes require warnings/suppression; `emerging` remains a stronger longitudinal conclusion.
14. External ESCO/O*NET/OECD structures are useful design/reference inputs, not JobHunter source truth.

---

## 12. Current state

```text
P2.2B-B1 local execution             PAUSED UNTIL OWNER PC ACCESS
Market implementation                NOT AUTHORIZED
Market external research pass 1      COMPLETE
Market target/relevance/dedup pass 2 COMPLETE
Market report-contract pass 3        COMPLETE
formal Market foundation audit       STILL QUEUED BEHIND B1
```

The next remote-safe investigation, if further work is useful before local access returns, should focus on **incremental orchestration and cost/model-call strategy**: how a target refresh can reuse current JobHunter source/English/P1.6/Capability/Work artifacts instead of processing the entire discovered corpus every time.
