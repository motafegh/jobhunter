# JobHunter Proposal Library

**Status:** Proposal inventory — non-controlling  
**Created:** 2026-08-02  
**Scope:** Candidate product, intelligence, architecture, UX, reliability, privacy, learning, and career-workflow capabilities

---

## 1. Why this library exists

JobHunter now has a deliberately broad set of future ideas. Losing them would be wasteful; putting all of them directly into the implementation plan would be worse.

This library provides a middle layer:

```text
brainstorm / idea
        ↓
proposal library        ← this directory
        ↓ deliberate selection
approved product/architecture decision
        ↓
master implementation plan / phase plan
        ↓
bounded implementation increment
        ↓
acceptance evidence
```

A proposal can therefore be preserved and developed without becoming a commitment.

**Nothing in `docs/proposals/` authorizes implementation.** The repository's controlling product/specification/architecture/master-plan hierarchy remains unchanged.

---

## 2. Existing deep proposal retained outside this directory

The repository already contains:

- [`../AI_INTELLIGENCE_RAG_CONTINUAL_LEARNING_PROPOSAL.md`](../AI_INTELLIGENCE_RAG_CONTINUAL_LEARNING_PROPOSAL.md) — a deep proposal covering multi-provider inference, specialist agents, RAG, continual learning, AI Lab/evaluation, AI operations, privacy/safety, and future AI intelligence surfaces.

That proposal remains intact and is treated as a member of the wider proposal library. The B001-B200 category files reference it where relevant rather than attempting to replace it.

---

## 3. Proposal authority and lifecycle

Recommended proposal states:

```text
candidate            preserved idea; not selected
under_discussion     being actively analyzed/refined
selected_for_planning product direction accepted in principle; implementation not yet authorized
planned              incorporated into a controlling implementation/phase plan
implemented          code exists; acceptance status still stated separately
accepted             required acceptance evidence passed
rejected             deliberately not pursued under current assumptions
superseded           replaced by a newer proposal/decision
```

The category files currently remain **candidate proposals** unless another controlling artifact explicitly says otherwise.

### Promotion rule

Before promoting a proposal into implementation planning, answer at least:

1. What concrete user/system problem does it solve now?
2. What current evidence shows that the problem is real?
3. What existing capability/schema must exist first?
4. What is the smallest coherent vertical increment?
5. What are the privacy/security/provenance implications?
6. What would deterministic and live acceptance look like?
7. Does it require a new abstraction/dependency, and is that justified by a current use?
8. What explicitly remains out of scope?

A proposal should be rejected or deferred if the value is hypothetical while the complexity is immediate.

---

## 4. Categorization rules

- Every brainstorm item B001-B200 has exactly **one primary category** in this catalog.
- Cross-cutting proposals may reference other categories without changing their primary home.
- Numbering preserves traceability to the original brainstorming session; it is **not priority order**.
- File numbering is organizational; it is **not roadmap order**.
- Similar ideas are intentionally not merged away if they express meaningfully different product behavior.
- Later proposals may split or combine B-items, but the catalog should preserve a supersession/mapping trail so the original idea is never silently lost.

---

## 5. Category files

| File | Proposal family | Primary B-items |
|---|---|---|
| [`01_PRODUCT_VISION_DECISION_INTELLIGENCE_AND_CAREER_LOOP.md`](01_PRODUCT_VISION_DECISION_INTELLIGENCE_AND_CAREER_LOOP.md) | Product identity, career decisions, scenarios, explainability, provenance loop | B001, B137-B145, B147, B200 |
| [`02_SOURCE_ACQUISITION_SEARCH_IDENTITY_AND_LIFECYCLE.md`](02_SOURCE_ACQUISITION_SEARCH_IDENTITY_AND_LIFECYCLE.md) | Sources, search strategy, job identity/version/lifecycle, source/search drift | B002-B006, B158, B161, B170 |
| [`03_EVIDENCE_PROVENANCE_REVIEW_AND_TRUST.md`](03_EVIDENCE_PROVENANCE_REVIEW_AND_TRUST.md) | Claim provenance, evidence inspection, review, uncertainty, contradictions, reversibility | B007-B010, B086-B092, B184 |
| [`04_AI_MODELS_EVALUATION_RETRIEVAL_AND_EXPERIMENTATION.md`](04_AI_MODELS_EVALUATION_RETRIEVAL_AND_EXPERIMENTATION.md) | Translation/model evaluation, routing, retrieval, experiments, benchmark corpora | B011-B012, B116, B121, B123-B129, B159-B160, B167-B169, B185-B187 |
| [`05_SEMANTIC_ROLE_TAXONOMY_AND_REQUIREMENT_MODEL.md`](05_SEMANTIC_ROLE_TAXONOMY_AND_REQUIREMENT_MODEL.md) | Responsibilities, deliverables, role DNA/archetypes, requirement semantics, taxonomy | B013-B030 |
| [`06_MARKET_COMPANY_GEOGRAPHY_AND_MEASUREMENT_INTELLIGENCE.md`](06_MARKET_COMPANY_GEOGRAPHY_AND_MEASUREMENT_INTELLIGENCE.md) | Market/company/location intelligence, metrics, drift, corpus statistics | B031-B040, B155-B157, B162-B163, B188-B196 |
| [`07_PERSONAL_CAPABILITY_EVIDENCE_AND_PORTFOLIO_INTELLIGENCE.md`](07_PERSONAL_CAPABILITY_EVIDENCE_AND_PORTFOLIO_INTELLIGENCE.md) | Personal evidence ledger, capability depth/confidence/recency, portfolio intelligence | B041-B048, B054, B164-B166, B177, B197-B199 |
| [`08_GAP_READINESS_LEARNING_AND_PROJECT_PRIORITIZATION.md`](08_GAP_READINESS_LEARNING_AND_PROJECT_PRIORITIZATION.md) | Gap taxonomy, readiness, learning priority, evidence-building projects, counterfactuals/ROI | B049-B053, B055-B067, B130-B136 |
| [`09_APPLICATION_INTERVIEW_AND_OPPORTUNITY_WORKFLOW.md`](09_APPLICATION_INTERVIEW_AND_OPPORTUNITY_WORKFLOW.md) | Interview preparation, application evidence, resume targeting, application outcomes | B068-B076 |
| [`10_PRODUCT_UX_COCKPIT_REVIEW_AND_VISUALIZATION.md`](10_PRODUCT_UX_COCKPIT_REVIEW_AND_VISUALIZATION.md) | Repeated-use UX, comparisons, visualizations, cockpit/review/operations surfaces | B077-B085, B099-B102 |
| [`11_RAG_QUERY_REPORTING_AND_CAREER_ASSISTANT.md`](11_RAG_QUERY_REPORTING_AND_CAREER_ASSISTANT.md) | Natural-language queries, evidence-backed assistant, reports/charts/briefings | B093-B098 |
| [`12_OPERATIONS_RELIABILITY_TESTING_AND_OBSERVABILITY.md`](12_OPERATIONS_RELIABILITY_TESTING_AND_OBSERVABILITY.md) | Durable workflows, partial success, scheduling, snapshots, tests, observability | B103-B107, B114-B115, B117-B120, B122 |
| [`13_PRIVACY_SECURITY_BACKUP_PORTABILITY_AND_LOCAL_APP.md`](13_PRIVACY_SECURITY_BACKUP_PORTABILITY_AND_LOCAL_APP.md) | Privacy/egress, personal-data boundary, backup/export, packaging, security hardening | B108-B113, B174-B176, B178-B183 |
| [`14_ARCHITECTURE_PLATFORM_AND_DEVELOPER_KNOWLEDGE.md`](14_ARCHITECTURE_PLATFORM_AND_DEVELOPER_KNOWLEDGE.md) | Logical knowledge graph, developer learning/diagnostics, ADR/incidents, architecture constraints | B146, B148-B154, B171-B173 |

---

# 6. Complete B001-B200 catalog

The table below is the completeness ledger. Every original brainstorm item appears once with its primary proposal file.

| ID | Proposal | Primary file |
|---|---|---|
| B001 | Career-intelligence system as the product identity | 01 |
| B002 | Multi-source acquisition ecosystem | 02 |
| B003 | Search effectiveness and blind-spot intelligence | 02 |
| B004 | Repost and near-duplicate job identity | 02 |
| B005 | Semantic job-version diffing | 02 |
| B006 | Rich lifecycle intelligence | 02 |
| B007 | Field-level provenance | 03 |
| B008 | Evidence Inspector | 03 |
| B009 | Claim-level analysis quality review | 03 |
| B010 | Active-learning review queue | 03 |
| B011 | Translation golden corpus and quality evaluation | 04 |
| B012 | JobHunter model laboratory | 04 |
| B013 | Model concepts beyond “skills” | 05 |
| B014 | Deliverable intelligence | 05 |
| B015 | Responsibility intelligence | 05 |
| B016 | Responsibility families | 05 |
| B017 | Role DNA | 05 |
| B018 | Title mismatch detector | 05 |
| B019 | Evidence-derived role archetype discovery | 05 |
| B020 | Requirement-strength intelligence | 05 |
| B021 | Requirement depth signals | 05 |
| B022 | Experience intelligence | 05 |
| B023 | Seniority inference from work signals | 05 |
| B024 | Technology relationship graph | 05 |
| B025 | Capability bundle intelligence | 05 |
| B026 | Prerequisite graph | 05 |
| B027 | Technology substitution/family patterns | 05 |
| B028 | Tool versus underlying capability intelligence | 05 |
| B029 | Canonical market taxonomy | 05 |
| B030 | External taxonomy comparison | 05 |
| B031 | Market Snapshot | 06 |
| B032 | Period-over-period market change | 06 |
| B033 | Emerging-skill/capability detector | 06 |
| B034 | Market stability classification | 06 |
| B035 | Company intelligence profile | 06 |
| B036 | Company technology/work fingerprint | 06 |
| B037 | Company role evolution | 06 |
| B038 | Geographic intelligence | 06 |
| B039 | Remote/hybrid/work-mode intelligence | 06 |
| B040 | Compensation intelligence with strict provenance | 06 |
| B041 | Personal Evidence Ledger | 07 |
| B042 | Personal evidence-type taxonomy | 07 |
| B043 | GitHub/project evidence importer | 07 |
| B044 | Capability depth states | 07 |
| B045 | Capability confidence separate from depth | 07 |
| B046 | Capability recency | 07 |
| B047 | Capability independence / AI-assistance context | 07 |
| B048 | Market-concept ↔ personal-capability mapping | 07 |
| B049 | Gap taxonomy | 08 |
| B050 | Evidence-backed gap explanations | 08 |
| B051 | Gap severity without opaque readiness percentages | 08 |
| B052 | “Can I apply now?” categorical decision support | 08 |
| B053 | Requirement-by-requirement job comparison | 08 |
| B054 | Evidence portability across jobs | 07 |
| B055 | “Why am I not ready?” explanation | 08 |
| B056 | “Why am I more ready than I think?” explanation | 08 |
| B057 | Career direction comparison | 08 |
| B058 | Adjacent-role discovery | 08 |
| B059 | Career graph | 08 |
| B060 | Relative path cost | 08 |
| B061 | Learning priority engine | 08 |
| B062 | “What should I learn next?” evidence answer | 08 |
| B063 | Learning dependency planner | 08 |
| B064 | Gap-to-project generator | 08 |
| B065 | Project Evidence Planner | 08 |
| B066 | Portfolio coverage analysis | 08 |
| B067 | Evidence-building recommendation | 08 |
| B068 | Interview-domain intelligence | 09 |
| B069 | Interview preparation matrix | 09 |
| B070 | Project story builder | 09 |
| B071 | Application Evidence Pack | 09 |
| B072 | Evidence-constrained resume targeting | 09 |
| B073 | Application tracker | 09 |
| B074 | Opportunity decision journal | 09 |
| B075 | Rejection/outcome learning with causal restraint | 09 |
| B076 | Opportunity watch | 09 |
| B077 | “What changed since I last opened JobHunter?” | 10 |
| B078 | Saved views | 10 |
| B079 | Multi-job comparison | 10 |
| B080 | Role comparison | 10 |
| B081 | Company comparison | 10 |
| B082 | Market heatmaps | 10 |
| B083 | Co-occurrence network visualization | 10 |
| B084 | Role-family map | 10 |
| B085 | Job timeline | 10 |
| B086 | Data Quality Cockpit | 03 |
| B087 | Corpus health summary | 03 |
| B088 | Provenance coverage metric | 03 |
| B089 | Uncertainty-first UI vocabulary | 03 |
| B090 | Cross-field contradiction detection | 03 |
| B091 | Requirement contradiction detector | 03 |
| B092 | Suspicious-posting risk indicators | 03 |
| B093 | Natural-language market queries | 11 |
| B094 | Evidence-backed career chat | 11 |
| B095 | Query reproducibility | 11 |
| B096 | On-demand generated charts | 11 |
| B097 | Versioned report builder | 11 |
| B098 | Weekly career-intelligence briefing | 11 |
| B099 | Personal Career Cockpit | 10 |
| B100 | Unified Review Inbox | 10 |
| B101 | Command palette | 10 |
| B102 | Rich operation result pages | 10 |
| B103 | Durable workflow runs | 12 |
| B104 | Partial-success semantics | 12 |
| B105 | Resume after crash/interruption | 12 |
| B106 | Scheduled operation policies | 12 |
| B107 | Actionable notifications | 12 |
| B108 | Privacy dashboard | 13 |
| B109 | External egress ledger | 13 |
| B110 | Explicit market-data / personal-data boundary | 13 |
| B111 | Sensitive evidence controls | 13 |
| B112 | Tested backup and restore | 13 |
| B113 | Structured data export | 13 |
| B114 | Reproducible market/data snapshots | 12 |
| B115 | Migration Inspector | 12 |
| B116 | Model/prompt/analysis contract registry | 04 |
| B117 | Artifact-staleness explanation | 12 |
| B118 | Regression corpus | 12 |
| B119 | Property-based tests for deterministic invariants | 12 |
| B120 | Fault-simulation suite | 12 |
| B121 | Model chaos testing | 04 |
| B122 | Performance and capacity observability | 12 |
| B123 | Task-specific local model routing | 04 |
| B124 | Cheap-first / deterministic-first analysis | 04 |
| B125 | Model disagreement review | 04 |
| B126 | Semantic search over JobHunter evidence | 04 |
| B127 | Similar-job explorer with explicit similarity dimensions | 04 |
| B128 | “Show me jobs like this but easier” | 04 |
| B129 | Bridge-role discovery | 04 |
| B130 | Counterfactual capability analysis | 08 |
| B131 | Skill/capability ROI simulator | 08 |
| B132 | Project ROI simulator | 08 |
| B133 | Opportunity-cost intelligence | 08 |
| B134 | Explicit “ignore for now” recommendation | 08 |
| B135 | Requirement criticality | 08 |
| B136 | User-defined application threshold policy | 08 |
| B137 | Career hypothesis testing | 01 |
| B138 | Explicit Target Role Specification | 01 |
| B139 | Multiple career scenarios | 01 |
| B140 | Personal constraints as a separate decision layer | 01 |
| B141 | Preference strength model | 01 |
| B142 | Decision explanation contract | 01 |
| B143 | Recommendation challenge mode | 01 |
| B144 | “What would change the conclusion?” | 01 |
| B145 | End-to-end data provenance graph | 01 |
| B146 | Career knowledge graph as a logical model | 14 |
| B147 | Career Digital Twin as a conceptual model | 01 |
| B148 | Developer/learning mode | 14 |
| B149 | Trace one job end-to-end | 14 |
| B150 | Architecture diagnostics page | 14 |
| B151 | Data-flow visualizer | 14 |
| B152 | “Why does this code exist?” engineering context | 14 |
| B153 | Lightweight Architecture Decision Records (ADRs) | 14 |
| B154 | Engineering incident history | 14 |
| B155 | Internal product metrics | 06 |
| B156 | Intelligence-quality metrics | 06 |
| B157 | Human review cost | 06 |
| B158 | Source/parser data-drift detection | 02 |
| B159 | Analysis drift detection | 04 |
| B160 | Taxonomy drift and new-concept discovery | 04 |
| B161 | Search drift detection | 02 |
| B162 | Career-market drift relative to personal evidence | 06 |
| B163 | “What did the market teach us?” periodic summary | 06 |
| B164 | Personal longitudinal progress report | 07 |
| B165 | Explicit protection against false progress | 07 |
| B166 | Career experiment evidence | 07 |
| B167 | Local experimentation sandbox | 04 |
| B168 | Branching analytical contracts | 04 |
| B169 | Historical reproducibility across AI upgrades | 04 |
| B170 | Plugin-style source adapter contract | 02 |
| B171 | Generic external-processing provider boundary | 14 |
| B172 | Preserve modular-monolith discipline | 14 |
| B173 | Keep SQLite until evidence requires replacement | 14 |
| B174 | Local desktop packaging | 13 |
| B175 | Offline analytical mode | 13 |
| B176 | Workspace import/export portability | 13 |
| B177 | Multiple personal/career profiles or scenarios | 07 |
| B178 | Red-team untrusted acquired content | 13 |
| B179 | Evidence-poisoning tests | 13 |
| B180 | HTML sanitization and safe rendering | 13 |
| B181 | Network-exposure hardening if loopback is expanded | 13 |
| B182 | Secret management improvement | 13 |
| B183 | Strict local/privacy mode | 13 |
| B184 | Reversible intelligence and correction history | 03 |
| B185 | Human annotation workspace | 04 |
| B186 | Gold-job benchmark collection | 04 |
| B187 | Representative review sampling | 04 |
| B188 | Outlier explorer | 06 |
| B189 | Corpus diversity dashboard | 06 |
| B190 | Sampling warnings | 06 |
| B191 | Statistical confidence / uncertainty | 06 |
| B192 | Duplicate-adjusted statistics | 06 |
| B193 | Employer-weighted market views | 06 |
| B194 | Role-weighted market views | 06 |
| B195 | Foundational versus differentiating capabilities | 06 |
| B196 | Skill/capability scarcity relative to the user's portfolio | 06 |
| B197 | Personal specialization detector | 07 |
| B198 | Career narrative consistency | 07 |
| B199 | Missing portfolio evidence analysis | 07 |
| B200 | Market → Gap → Learn → Build → Evidence → Apply loop | 01 |

---

## 7. How to use the library during future work

When a new product discussion touches one of these ideas:

1. open its category file;
2. inspect related current implementation/specification constraints;
3. update/refine the proposal if the idea has materially evolved;
4. decide whether it remains a candidate, should be rejected, or is ready for planning;
5. only if selected, create/update the appropriate controlling product/implementation artifact;
6. define the bounded implementation increment and acceptance separately.

Do not copy the entire proposal family into the master implementation plan. The plan should contain only selected work and link back to the proposal for broader context.

---

## 8. Current strategic reading

The library intentionally contains far more ideas than JobHunter should build in the near term. The strongest long-term differentiator is not feature count; it is the combination of:

```text
high-quality market evidence
+ semantic understanding of actual work
+ explicit personal capability evidence
+ explainable gaps and decisions
+ learning/project evidence creation
+ longitudinal outcomes
```

The proposal library exists so JobHunter can preserve ambitious possibilities while continuing to implement conservatively, testably, and in coherent vertical increments.