# JobHunter Market, Company, Geography, and Measurement Intelligence Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B031-B040, B155-B157, B162-B163, B188-B196

---

## Purpose

This family defines how accepted job-level evidence could become trustworthy market intelligence. The governing principle is that counts, prevalence, trends, and cohorts should be computed deterministically from an explicitly selected corpus and analysis/taxonomy contract. Model-generated prose may explain those facts later but must not manufacture them.

No proposal in this file authorizes broad “market truth” claims from a small, source-biased sample.

---

## B031 — Market Snapshot

**Intent:** Provide an answer-first view of the currently analyzed corpus.

**Proposal:** Create a snapshot page/report showing corpus size and important distributions such as required/preferred concepts, responsibility families, role archetypes, experience signals, work modes, and other accepted Phase-2 dimensions.

**Design direction:** Every metric shows its denominator and filter context. Snapshot identity should include date/time, source scope, current analysis contract, taxonomy version, and any target-role/geographic filters.

**Guardrails:** Do not label a Jobinja-only or otherwise bounded sample as the complete labor market. The UI should say what corpus the statement describes.

**Promotion signal:** A natural extension of the current Market page after canonical Phase-2 concepts exist.

---

## B032 — Period-over-period market change

**Intent:** Understand what changed, not only what is common now.

**Proposal:** Compare fixed market snapshots or time windows to identify changes in concept prevalence, responsibility patterns, role mix, seniority, location/work mode, and employer activity.

**Design direction:**

- compare like-for-like source/filter definitions;
- expose raw counts and percentages;
- retain denominator changes;
- distinguish new data coverage from genuine observed movement;
- require minimum sample thresholds for trend labels.

**Guardrails:** Period change is observational. Do not infer why demand moved unless separate evidence exists.

**Promotion signal:** After enough longitudinal corpus history and duplicate/lifecycle handling exists.

---

## B033 — Emerging-skill/capability detector

**Intent:** Surface concepts whose observed prevalence is increasing materially in the sampled market.

**Proposal:** Identify candidate emerging signals using recent versus historical windows, minimum job/employer counts, and stability checks.

**Design direction:** A finding should include historical prevalence, recent prevalence, sample sizes, number of distinct employers/role families, and whether the signal is new terminology or an existing concept becoming more common.

**Guardrails:** Avoid “trending” labels from one employer or tiny samples. An emerging signal is not automatically a learning recommendation.

**Promotion signal:** After snapshot comparison and canonical taxonomy are reliable.

---

## B034 — Market stability classification

**Intent:** Distinguish persistent foundations from volatile or niche technologies/practices.

**Proposal:** Classify observed concept demand over time into evidence-backed states such as `persistent foundation`, `stable specialization`, `emerging`, `volatile`, or `rare/niche`.

**Design direction:** Define transparent rules using prevalence, duration, employer diversity, and role-family distribution. Preserve the raw time series behind the label.

**Guardrails:** Do not treat `rare` as unimportant; a rare capability may be crucial for a specific target archetype.

**Promotion signal:** Requires meaningful longitudinal data across several periods.

---

## B035 — Company intelligence profile

**Intent:** Turn repeated postings from the same employer into a useful evidence-backed company view.

**Proposal:** Aggregate a company's observed hiring data: recurring role families, technologies/capabilities, seniority mix, locations, work modes, recurring vacancies, posting changes, and common requirements.

**Design direction:** Separate source-explicit company facts from observations derived only from JobHunter's collected postings. Always show the number/date range of postings supporting the profile.

**Guardrails:** Do not infer company-wide technology architecture or culture from a small hiring sample.

**Promotion signal:** After company identity normalization is dependable and enough employers have multiple postings.

---

## B036 — Company technology/work fingerprint

**Intent:** Summarize recurring capability and work patterns within one employer's observed jobs.

**Proposal:** Build a derived fingerprint showing concepts and responsibility families repeatedly present across that employer's postings, optionally segmented by role family.

**Design direction:** Use employer-weighted counts and time windows. Explain whether a signal appears across many jobs or only one recurring template.

**Guardrails:** A hiring fingerprint is not proof of the company's full production stack.

**Promotion signal:** As an extension of company profiles.

---

## B037 — Company role evolution

**Intent:** Observe how an employer's hiring focus changes over time.

**Proposal:** Compare company-level snapshots to detect shifts such as movement from traditional ML/data-science roles toward LLM application/platform roles, or increased infrastructure/security responsibility.

**Design direction:** Require enough postings and distinct time periods. Show the underlying role/responsibility evidence rather than only narrative interpretation.

**Guardrails:** Hiring changes do not prove internal strategy changes; present them as observed posting shifts.

**Promotion signal:** Only after longitudinal company coverage is meaningful.

---

## B038 — Geographic intelligence

**Intent:** Compare demand across locations relevant to the user.

**Proposal:** Normalize source-explicit location data and compare role availability, capabilities, seniority, language requirements, work mode, and compensation where reliable across cities/regions/countries.

**Design direction:** Keep source location text, normalized geographic entity, and uncertainty separate. Support geographic filters in market snapshots and role comparisons.

**Guardrails:** Job-source coverage may differ radically by geography. Every comparison must expose source/sample coverage.

**Promotion signal:** After additional sources or enough geographic diversity makes the comparison useful.

---

## B039 — Remote/hybrid/work-mode intelligence

**Intent:** Treat work location requirements as structured job conditions.

**Proposal:** Normalize explicit states such as onsite, hybrid, fully remote, remote-country-limited, remote-region-limited, and unspecified, plus supporting conditions such as office frequency, travel, on-call, or timezone constraints when explicitly stated.

**Design direction:** Preserve exact employer language and use derived normalized categories for filtering/comparison.

**Guardrails:** `Remote` must not be interpreted as globally remote without location constraints being checked.

**Promotion signal:** Phase-2/3 candidate because work mode affects both market analytics and personal constraints.

---

## B040 — Compensation intelligence with strict provenance

**Intent:** Use salary/compensation data where it is explicitly available without manufacturing comparable numbers from unclear inputs.

**Proposal:** Model compensation with currency, period, min/max, gross/net/unknown state, explicit versus estimated provenance, and source text. Later aggregate only compatible/normalized records under documented assumptions.

**Design direction:** Any normalization to monthly/annual or cross-currency views records the conversion assumptions and date/rate source.

**Guardrails:** Do not infer salary for postings that do not state it. Do not compare gross and net values as equivalent. Avoid salary prediction until data quality/volume justifies it.

**Promotion signal:** When actual source coverage proves sufficient.

---

## B155 — Internal product metrics

**Intent:** Measure whether JobHunter's workflows are healthy and useful without relying on vanity metrics.

**Proposal:** Track operational/product measures such as jobs discovered, details acquired, parse coverage, translation acceptance, analysis acceptance, review activity, taxonomy uncertainty, search unique contribution, and application-workflow usage.

**Design direction:** Metrics have definitions, denominators, and source queries. Separate system-health KPIs from career-market statistics.

**Guardrails:** More jobs or more model calls are not automatically better. Metrics should support decisions or reliability work.

**Promotion signal:** Incrementally as repeated-use workflows stabilize.

---

## B156 — Intelligence-quality metrics

**Intent:** Measure correctness/grounding of derived intelligence rather than only pipeline throughput.

**Proposal:** Candidate metrics include evidence-grounding rate, unsupported-claim rate, requirement-strength accuracy on reviewed samples, translation fidelity, taxonomy mapping accuracy, human correction rate, and retrieval evidence coverage.

**Design direction:** Define each metric against a reviewed reference set. Track by contract/model/version, not only globally.

**Guardrails:** Avoid composite “AI quality score” unless every component and weighting is justified.

**Promotion signal:** Core capability for model/taxonomy promotion decisions.

---

## B157 — Human review cost

**Intent:** Include operator effort in model/contract evaluation.

**Proposal:** Measure review burden per batch or 100 claims/jobs: time spent, number of corrections, unresolved items, and review actions needed.

**Design direction:** Use lightweight timing/interaction telemetry only if it does not make the UI intrusive. Even simple correction counts can reveal that a faster model creates more downstream work.

**Guardrails:** Review time is noisy and user-dependent; use it as an operational signal, not a productivity judgment.

**Promotion signal:** When comparing multiple analysis/taxonomy approaches.

---

## B162 — Career-market drift relative to personal evidence

**Intent:** Detect when the observed target market is moving in a way that changes the relevance of the user's evidence portfolio.

**Proposal:** Compare market trend snapshots with the user's current evidence map. Example: target roles increasingly request platform/networking responsibility while personal evidence remains concentrated in application-level AI.

**Design direction:** Show which market requirements changed and which personal-evidence states remain unchanged. Keep this separate from generic market drift.

**Guardrails:** Do not create urgency from small/noisy samples or imply that the user must chase every new technology.

**Promotion signal:** Requires accepted market trends plus personal capability mapping.

---

## B163 — “What did the market teach us?” periodic summary

**Intent:** Turn longitudinal observations into a concise evidence-backed review.

**Proposal:** Produce a monthly or user-triggered summary of new role families, changed requirement patterns, emerging concepts, fading search productivity, unexpected adjacent roles, and notable source/company changes.

**Design direction:** Deterministic metrics first; optional model synthesis second. Every narrative claim links to the supporting snapshot/change table.

**Guardrails:** If the sample is too small or unchanged, say so rather than inventing insights.

**Promotion signal:** After time-series market views exist.

---

## B188 — Outlier explorer

**Intent:** Find unusual postings that may reveal parser/model problems or genuinely novel market combinations.

**Proposal:** Surface jobs with unusual characteristics such as very high requirement counts, rare technologies, unusual role-family combinations, atypical seniority signals, new concepts, or extreme text structure.

**Design direction:** Explain which metric made the job an outlier and compare it with the corpus distribution.

**Guardrails:** Outlier does not mean bad or erroneous. It is a review/research category.

**Promotion signal:** Useful after normalized metrics exist and can help quality review as well as market research.

---

## B189 — Corpus diversity dashboard

**Intent:** Expose whether JobHunter's analytical sample is concentrated in too few companies, roles, locations, languages, or source types.

**Proposal:** Measure distributions across employer, role archetype, location, language, source, posting age, and other meaningful dimensions.

**Design direction:** Show concentration as counts/shares and allow filtering. Use this to qualify market claims and guide acquisition/search expansion.

**Guardrails:** Diversity is descriptive, not inherently a target to maximize. A deliberately narrow target-role corpus may correctly be concentrated.

**Promotion signal:** Before broad trend claims become a core feature.

---

## B190 — Sampling warnings

**Intent:** Prevent strong conclusions from tiny or unrepresentative analyzed subsets.

**Proposal:** Define explicit warning policies based on analyzed job count, employer count, role diversity, source coverage, and contract coverage.

**Example:** `Only 7 current analyzed jobs match this view; broad market conclusions are not supported.`

**Design direction:** Warnings should be deterministic and context-specific. A sample can be sufficient for inspecting individual requirements but insufficient for market prevalence.

**Guardrails:** Avoid arbitrary universal thresholds; define them per analytical claim type where possible.

**Promotion signal:** Near-term requirement for any expanding Market surface.

---

## B191 — Statistical confidence / uncertainty

**Intent:** Show uncertainty around proportions/trends when statistical treatment is justified.

**Proposal:** For sufficiently defined samples, expose intervals or uncertainty measures alongside percentages, especially when comparing periods or groups.

**Design direction:** Use simple, documented methods and preserve raw counts. Prefer understandable intervals to sophisticated models that the product cannot explain.

**Guardrails:** Statistical intervals address sampling variation under assumptions; they do not correct source-selection bias or duplicate jobs.

**Promotion signal:** After corpus definitions and duplicate adjustments are mature enough that formal uncertainty is meaningful.

---

## B192 — Duplicate-adjusted statistics

**Intent:** Prevent reposts and duplicate advertisements from inflating observed demand.

**Proposal:** Offer views that count logical/repost groups separately from raw postings once duplicate/repost identity is reliable.

**Design direction:** Preserve both measures:

```text
raw posting count
unique/repost-adjusted vacancy signals
```

Explain the grouping method and uncertain groups.

**Guardrails:** Do not deduplicate aggressively when identity confidence is low.

**Promotion signal:** Before longitudinal/prevalence statistics are treated as mature.

---

## B193 — Employer-weighted market views

**Intent:** Prevent one employer with many similar openings from dominating concept prevalence.

**Proposal:** Offer at least two complementary measures: posting frequency and distinct-employer frequency for concepts/responsibilities/archetypes.

**Design direction:** Show both rather than selecting one universal “correct” weighting. For company-specific research, raw posting volume may itself be meaningful.

**Guardrails:** Employer weighting cannot fix every source bias; it addresses only concentration by employer.

**Promotion signal:** Core consideration for Phase-2 aggregate design.

---

## B194 — Role-weighted market views

**Intent:** Show whether a capability is broadly useful across role families or concentrated in one archetype.

**Proposal:** Report the number/share of role archetypes in which a concept appears above a defined threshold, alongside raw posting prevalence.

**Design direction:** Example interpretation: Python may be broad across many archetypes; threat hunting may be concentrated but strong inside Detection/SOC families.

**Guardrails:** Role archetypes must already be reviewed/stable; otherwise weighting magnifies taxonomy noise.

**Promotion signal:** After archetype acceptance.

---

## B195 — Foundational versus differentiating capabilities

**Intent:** Distinguish broadly expected foundations from capabilities that specialize a role family.

**Proposal:** Derive categories from cross-role prevalence and within-role concentration. A foundation appears broadly across relevant archetypes; a differentiator is strongly associated with a narrower target area.

**Design direction:** Show the underlying breadth/concentration metrics and sample sizes. Allow a concept to be foundational in one target scope and differentiating in another.

**Guardrails:** `Differentiating` does not mean rare globally or valuable by itself.

**Promotion signal:** After role-weighted market views exist.

---

## B196 — Skill/capability scarcity relative to the user's portfolio

**Intent:** Identify unusual combinations in the user's evidence that overlap meaningful target-market demand.

**Proposal:** Compare personal demonstrated capability bundles against market bundle prevalence to surface strengths that may be relatively uncommon within the user's own portfolio context.

**Design direction:** This is not workforce-supply estimation. The system can only state that a personal evidence combination is distinctive relative to observed target requirements, not that the labor market lacks candidates.

**Guardrails:** Never claim general talent scarcity without external supply data.

**Promotion signal:** After personal evidence and market capability bundles are both accepted.

---

## Category-level recommendation

The first mature market-intelligence layer should prioritize transparent counts, sample warnings, employer/duplicate-aware views, and stable snapshots before sophisticated trend labels. The system becomes more valuable when it can say not only “X appears often,” but also how many jobs, how many employers, in which role families, under what time/source scope, and with what uncertainty.