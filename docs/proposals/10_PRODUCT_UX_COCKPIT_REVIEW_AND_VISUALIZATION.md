# JobHunter Product UX, Cockpit, Review, and Visualization Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B077-B085, B099-B102

---

## Purpose

This family describes how increasingly rich JobHunter intelligence could remain usable in a local browser application. The goal is not to add dashboards for their own sake; each surface should shorten a real workflow, preserve evidence visibility, and avoid hiding uncertainty behind polished UI.

The existing server-rendered Python web architecture remains preferred while it remains sufficient.

---

## B077 — “What changed since I last opened JobHunter?”

**Intent:** Make repeated use immediately useful without requiring the user to inspect every page.

**Proposal:** Show a bounded change summary since the user's previous acknowledged/opened checkpoint, for example new jobs, jobs removed/changed, new current translations/analyses, market-snapshot changes, and review items created.

**Design direction:** Changes should derive from durable timestamps/version events and a local user checkpoint. The user can drill into each category.

**Guardrails:** Do not overwhelm the dashboard with every operation detail. Highlight user-relevant state change, while operational failures remain accessible in Operations/System.

**Promotion signal:** Near-term UX enhancement once current full workflow stabilizes.

---

## B078 — Saved views

**Intent:** Let the user return to useful filters without rebuilding them manually.

**Proposal:** Save named query/view definitions such as `AI Security`, `Remote Germany`, `Needs review`, `New this week`, or later `Few major gaps`.

**Design direction:** Store filters/sort/view options, not duplicate result sets. Each saved view resolves against current data and displays its active filters.

**Guardrails:** Avoid turning saved views into an unbounded rule/automation engine. Advanced persistent configuration may remain TOML until safe UI writes are justified.

**Promotion signal:** When job/market filters become complex enough to repeat.

---

## B079 — Multi-job comparison

**Intent:** Compare 2-5 concrete opportunities without switching among detail pages.

**Proposal:** A comparison table could show responsibilities, required/preferred concepts, seniority, location/work mode, compensation where explicit, lifecycle/freshness, and later personal evidence/gaps.

**Design direction:** Preserve per-job source links and allow expanding exact evidence for a comparison row.

**Guardrails:** Do not compress incomparable source fields into misleading numbers. Keep unknown values explicit.

**Promotion signal:** After job analysis is accepted and detail surfaces are stable.

---

## B080 — Role comparison

**Intent:** Compare evidence-derived role archetypes rather than individual postings.

**Proposal:** Show differences in responsibility families, common required/preferred concepts, experience/seniority signals, observed market volume, geographic/work-mode patterns, and later personal gaps.

**Design direction:** Every metric uses the same market snapshot/filter scope and shows sample size.

**Guardrails:** Archetypes are derived and may evolve; comparison views must reference taxonomy/archetype version.

**Promotion signal:** Phase 2 after role archetypes exist.

---

## B081 — Company comparison

**Intent:** Compare selected employers using observed hiring evidence.

**Proposal:** Display company-level role mix, recurring capabilities, work modes, locations, compensation coverage, posting frequency, and change patterns.

**Design direction:** Separate observed posting data from any future externally sourced company information.

**Guardrails:** Do not present a small hiring sample as a full assessment of company culture or technology stack.

**Promotion signal:** After company intelligence profiles have enough coverage.

---

## B082 — Market heatmaps

**Intent:** Make high-dimensional aggregate relationships easier to inspect.

**Proposal:** Candidate matrices include concept × role archetype, concept × company, concept × seniority, concept × location, responsibility × archetype, and requirement-strength × concept.

**Design direction:** Cells show count/share and denominator on hover/click, with filters and minimum-sample suppression.

**Guardrails:** Heatmap intensity must not hide sample-size differences or imply causation.

**Promotion signal:** When canonical Phase-2 matrices exist and a chart genuinely improves interpretation over a table.

---

## B083 — Co-occurrence network visualization

**Intent:** Explore capability/technology relationships interactively.

**Proposal:** Render a filtered network where nodes are canonical concepts and edges represent deterministic co-occurrence strength; clicking an edge reveals supporting jobs/employers/role families.

**Design direction:** Keep graph computation independent from visualization. Provide threshold/top-N controls to avoid unreadable “hairball” graphs.

**Guardrails:** Co-occurrence is not prerequisite or causation. A graph library/SPA rewrite is not justified solely for this feature.

**Promotion signal:** After co-occurrence analytics prove useful in tabular form.

---

## B084 — Role-family map

**Intent:** Visualize relationships among role archetypes based on actual responsibility/capability overlap.

**Proposal:** Present a 2D/graph-style map or structured adjacency view showing which role families are close, hybrid, or distinct and why.

**Design direction:** A selected edge displays shared/differentiating responsibilities and supporting sample sizes.

**Guardrails:** Dimensionality-reduction coordinates are not meaningful distances by themselves; explanations must use underlying features.

**Promotion signal:** After role archetype similarity is stable.

---

## B085 — Job timeline

**Intent:** Put a job's acquisition, version, analysis, user, and application history in one understandable sequence.

**Proposal:** Timeline events may include discovered, detail fetched, source changed, lifecycle transition, translation created/failed, analysis created/reviewed, triage changed, application created, and source removed.

**Design direction:** Derive timeline from durable events/artifacts rather than duplicating another event store unless needed.

**Guardrails:** Operational retry noise should be collapsible so the timeline remains useful.

**Promotion signal:** Useful when enough layers exist that a job detail page becomes difficult to reason about chronologically.

---

## B099 — Personal Career Cockpit

**Intent:** Organize the mature product around user goals rather than internal database modules.

**Proposal:** A future top-level information architecture could include:

```text
Market        what employers demand
Jobs          individual opportunities
Roles         archetypes/comparisons
Me            personal capability/evidence
Gaps          market ↔ personal differences
Learning      next learning/building actions
Applications  active opportunity workflow
Research      trends/experiments
System        operations/data/model health
```

**Design direction:** These are product domains, not necessarily separate backend services. Reuse shared application services and stores.

**Guardrails:** Do not expose empty future navigation before the capability is real. Add sections only when they support repeated use.

**Promotion signal:** Use as a future navigation model as Phases 2-5 mature.

---

## B100 — Unified Review Inbox

**Intent:** Centralize human decisions that currently could be scattered across analysis, taxonomy, translation, duplicate, and personal-evidence pages.

**Proposal:** A Review Inbox could aggregate review tasks with types such as analysis uncertainty, taxonomy mapping, translation suspicion, duplicate/repost relation, personal evidence candidate, or recommendation challenge.

**Design direction:** Each item links to its specialized review page and records resolution. Priority can use deterministic quality impact and age.

**Guardrails:** The inbox should reference domain-owned records rather than becoming a second truth store. Avoid creating review tasks for routine successful processing.

**Promotion signal:** When at least three independent review workflows exist.

---

## B101 — Command palette

**Intent:** Speed up navigation/actions for frequent local use without removing normal UI controls.

**Proposal:** A `Ctrl/Cmd+K` palette could search jobs/pages and invoke safe commands such as open job, add supported URL, run bounded sync, open Market, compare roles, or export an allowed artifact.

**Design direction:** Mutating commands must obey the same CSRF/operation bounds/confirmation rules as ordinary forms.

**Guardrails:** The palette is convenience, not an unrestricted command shell. No arbitrary Python/shell/database commands.

**Promotion signal:** Low-priority UX enhancement after common actions stabilize.

---

## B102 — Rich operation result pages

**Intent:** Make completed browser operations tell the user what actually happened and what to do next.

**Proposal:** Operation results should summarize what ran, what changed, successes/failures, affected jobs, created artifacts, limits reached, and relevant next actions/links.

**Design direction:** Example full-workflow result:

```text
40 search requests succeeded
12 new postings
8 detail fetches completed
7 English-v2 current
6 analyses current
1 analysis failed → inspect
Market updated from 6 accepted current analyses
```

**Guardrails:** Do not hide partial failure behind a green “completed” state. Link to detailed logs/errors without dumping raw internals into normal UI.

**Promotion signal:** Near-term improvement for the newly implemented full browser workflow.

---

## Category-level recommendation

The best near-term UX value is clearer operation results, change summaries, saved views, and job comparisons. Rich graphs and a full Career Cockpit should follow actual semantic/personal capabilities rather than being built as empty navigation or visualization infrastructure.