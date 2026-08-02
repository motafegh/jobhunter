# JobHunter Semantic Role, Taxonomy, and Requirement-Model Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B013-B030

---

## Purpose

This category expands JobHunter's semantic market model beyond a flat list of “skills.” The long-term goal is to understand what work employers expect, how requirements differ in strength and depth, how technologies relate to capabilities, and how inconsistent job titles map to evidence-derived role archetypes.

These ideas belong primarily to Phase 2 and should be designed from accepted P1.6 evidence rather than generic occupational assumptions.

---

## B013 — Model concepts beyond “skills”

**Intent:** Prevent heterogeneous employer expectations from being flattened into a single skills list.

**Proposal:** Expand the canonical semantic model to distinguish concept classes such as programming language, tool, framework, platform, protocol, applied skill, knowledge area, practice, domain, experience, education, credential, deliverable, and work context.

**Design direction:** P1.6 already has broad concept types. Phase 2 should review which distinctions are genuinely useful for aggregation and personal mapping before adding more classes. Each concept mention retains source context and requirement relationship.

**Guardrails:** Do not create taxonomy classes purely for theoretical completeness. A distinction belongs only if it changes analysis, comparison, or decision quality.

**Promotion signal:** During Phase-2 canonical concept-schema design.

---

## B014 — Deliverable intelligence

**Intent:** Capture what the employee is expected to produce, not only the technologies they should know.

**Proposal:** Extract and normalize deliverables such as ML models, APIs, security detections, incident reports, data pipelines, dashboards, automation scripts, architecture designs, deployment systems, or research prototypes.

**Design direction:** Link deliverables to responsibilities and supporting evidence. Aggregate them by role archetype and company where sample size permits. Later compare personal project outputs against market deliverables.

**Guardrails:** Do not infer a deliverable merely because a tool usually produces one. Employer text or well-supported responsibility interpretation is required.

**Promotion signal:** When Phase-2 responsibility normalization is designed.

---

## B015 — Responsibility intelligence

**Intent:** Answer “what work do employers repeatedly expect someone in this role to perform?”

**Proposal:** Normalize evidence-backed responsibility claims into reusable responsibility concepts such as designing ML pipelines, developing detection rules, investigating incidents, deploying models, automating operations, maintaining APIs, or operating infrastructure.

**Design direction:** Preserve original responsibility claims while mapping them to canonical responsibility concepts. Counts should distinguish number of postings and number of employers.

**Guardrails:** Canonical responsibility wording must not erase material differences in scope or seniority.

**Promotion signal:** Core Phase-2 candidate after reviewed P1.6 responsibility extraction exists.

---

## B016 — Responsibility families

**Intent:** Group detailed responsibilities into higher-order work families that make role structure understandable.

**Proposal:** Build reviewed families such as Detection Engineering, Incident Investigation, Security Automation, ML Development, ML Deployment, Data Engineering, Backend Development, Infrastructure Automation, Model Evaluation, and LLM Application Development.

**Design direction:** Families should emerge from the actual corpus. One responsibility may map to more than one family where justified. Role archetypes can later be represented by their responsibility-family composition.

**Guardrails:** Do not start with a fixed list and force every job into it. Maintain an `other/unmapped` path and review workflow.

**Promotion signal:** After canonical responsibilities are sufficiently populated.

---

## B017 — Role DNA

**Intent:** Describe the actual work composition of a job rather than trusting its title.

**Proposal:** Create a derived `RoleDNA` view showing the dominant responsibility families, deliverables, and capability clusters in a posting or archetype.

**Illustrative output:**

```text
Title: AI Security Engineer
Work composition:
- Security Automation: dominant
- Detection Engineering: strong
- ML Engineering: supporting
- Platform Engineering: supporting
```

The exact representation should avoid false numeric precision unless percentages can be defined defensibly.

**Guardrails:** Role DNA is a derived interpretation, not employer-authored truth. It must link to responsibility evidence.

**Promotion signal:** After responsibility families and archetypes are accepted.

---

## B018 — Title mismatch detector

**Intent:** Identify jobs whose title poorly describes their actual responsibilities.

**Proposal:** Compare the title/title-derived signals with the accepted responsibility and requirement profile. Flag cases where, for example, a `Data Scientist` role is dominated by backend/data engineering work or a `Security Engineer` role is primarily SOC monitoring.

**Design direction:** Store a categorical mismatch reason and evidence-derived alternate role family suggestions.

**Guardrails:** Titles are employer choices and may intentionally be broad. Report mismatch as an analytical observation, not a correction of the employer.

**Promotion signal:** After role archetype classification is mature enough to make comparison meaningful.

---

## B019 — Evidence-derived role archetype discovery

**Intent:** Discover stable work patterns across inconsistent titles.

**Proposal:** Build role archetypes from accepted responsibility, requirement, deliverable, and concept patterns. Candidate archetypes may include Applied ML Engineer, LLM/Application Engineer, AI Platform Engineer, Security Automation Engineer, Detection Engineer, or AI Security Engineer, but the corpus must determine what actually exists.

**Design direction:** Use clustering or model proposals only as candidate-generation tools. Canonical archetypes require review, definitions, representative jobs, and boundaries.

**Guardrails:** Do not equate unsupervised clusters with career truth. Preserve jobs that are genuinely hybrid or do not fit established archetypes.

**Promotion signal:** Major Phase-2 milestone after sufficient analyzed corpus coverage.

---

## B020 — Requirement-strength intelligence

**Intent:** Preserve whether a concept is actually required, preferred, contextual, or merely inferred.

**Proposal:** Extend current P1.6 strength classes into canonical market aggregation without collapsing them. A concept's market signal should show separate counts for explicit required, preferred, contextual, and inferred mentions.

**Design direction:** Strength remains claim-level and evidence-backed. Canonical concept mapping should not alter strength. Market views can offer multiple interpretations but always expose underlying counts.

**Guardrails:** Never turn a preferred technology into a required skill because it is common.

**Promotion signal:** Immediate design rule for Phase-2 aggregation.

---

## B021 — Requirement depth signals

**Intent:** Distinguish a mention of a technology from evidence that deep independent capability is expected.

**Proposal:** Extract or derive depth signals such as familiarity, basic knowledge, working knowledge, experience, proficiency, strong proficiency, expertise, and design/leadership ownership.

**Design direction:** Prefer source-language patterns and explicit wording. Model interpretation should retain exact evidence and uncertainty. Store depth as categorical/ordinal semantics, not a fake continuous score.

**Guardrails:** Do not infer high proficiency from years alone or from the mere presence of a tool in responsibilities.

**Promotion signal:** After P1.6 requirement-strength acceptance; likely a later schema revision because it changes analysis contracts.

---

## B022 — Experience intelligence

**Intent:** Separate distinct types of experience expectations that are currently easy to conflate.

**Proposal:** Model at least:

- explicit years of experience;
- professional/general experience;
- domain experience;
- production/operational experience;
- leadership/mentoring experience;
- independent ownership;
- project/academic experience when explicitly allowed.

**Design direction:** Preserve numeric ranges and units separately from qualitative context. Later personal comparison can match experience type, not only duration.

**Guardrails:** Do not convert all experience language into one years number.

**Promotion signal:** Phase-2 requirement normalization.

---

## B023 — Seniority inference from work signals

**Intent:** Estimate practical seniority when title labels are inconsistent.

**Proposal:** Derive a seniority signal from evidence such as years, architecture ownership, ambiguity handling, production operations, mentoring, cross-team responsibility, and strategy/leadership expectations.

**Design direction:** Keep explicit employer seniority labels and inferred seniority separate. Possible output should be categorical with supporting signals and uncertainty.

**Guardrails:** No universal years-to-seniority rule. Different companies and domains use titles differently.

**Promotion signal:** After experience and responsibility-depth semantics are stable.

---

## B024 — Technology relationship graph

**Intent:** Understand which technologies/capabilities appear together rather than viewing each frequency independently.

**Proposal:** Build deterministic co-occurrence relations across accepted canonical concepts, for example Python ↔ FastAPI, Docker ↔ Kubernetes, SIEM ↔ Detection Engineering, or RAG ↔ LLM application development.

**Design direction:** Store counts by posting and employer, expose sample size, and later compare by role archetype. A graph UI is optional; relational tables are sufficient.

**Guardrails:** Co-occurrence does not imply prerequisite, substitution, or causation.

**Promotion signal:** Once canonical concept mapping reaches enough coverage for meaningful aggregation.

---

## B025 — Capability bundle intelligence

**Intent:** Identify recurring combinations that define practical role expectations.

**Proposal:** Detect and review bundles such as `Python + APIs + retrieval + evaluation` for LLM applications or `SIEM + Python + Linux + networking + incident response` for detection/security automation.

**Design direction:** Generate candidate bundles from co-occurrence and role-specific patterns; validate stability across employers and time. Bundles should list supporting jobs and prevalence.

**Guardrails:** Avoid inventing mandatory bundles from a few correlated postings.

**Promotion signal:** After technology relationship analytics and archetypes are available.

---

## B026 — Prerequisite graph

**Intent:** Represent learning/knowledge dependencies separately from market co-occurrence.

**Proposal:** Build a reviewed prerequisite relation for concepts where technical dependency is meaningful, for example networking fundamentals → TCP/IP → traffic analysis → IDS/detection concepts.

**Design direction:** Market evidence may motivate which dependencies matter, but prerequisite edges require technical reasoning/review and may come from curated knowledge references. Distinguish `prerequisite`, `commonly co-occurs`, and `helpful background` relations.

**Guardrails:** Never infer prerequisites directly from job co-occurrence statistics.

**Promotion signal:** Before dependency-aware learning recommendations become authoritative.

---

## B027 — Technology substitution/family patterns

**Intent:** Distinguish a capability family from employer-specific product choices.

**Proposal:** Model relations such as cloud-platform alternatives, SIEM families, deep-learning frameworks, or container tooling where employers often accept experience with one of several alternatives.

**Design direction:** Preserve exact employer-requested product while mapping it to a broader capability family and optional substitution group. Aggregate both exact and family-level demand.

**Guardrails:** Substitutability is context-dependent. Do not claim Azure experience satisfies an explicit AWS requirement unless employer wording or decision policy supports that interpretation.

**Promotion signal:** Phase-2 taxonomy refinement after enough examples reveal repeated alternative families.

---

## B028 — Tool versus underlying capability intelligence

**Intent:** Prevent learning recommendations from blindly chasing product names.

**Proposal:** Link specific tools to the broader work capability they often represent. Example: Splunk may support SIEM querying, security telemetry investigation, and detection-rule development.

**Design direction:** Tool→capability relations are reviewed taxonomy knowledge, while employer evidence still records the exact tool requested. Gap analysis can then show both `specific tool gap` and `underlying capability evidence`.

**Guardrails:** Tool and capability are not interchangeable. A person can understand the capability but still lack product-specific experience that an employer explicitly requires.

**Promotion signal:** Before personal gap recommendations become tool-heavy.

---

## B029 — Canonical market taxonomy

**Intent:** Create a stable reviewed vocabulary for aggregation across source wording, languages, and aliases.

**Proposal:** Introduce canonical entities and aliases for technologies, skills, practices, domains, responsibilities, deliverables, and other meaningful concepts.

**Design direction:**

- every canonical concept has stable ID, type, display name, aliases, status, and version/history;
- raw/source wording is always preserved;
- mappings are reviewable and reversible;
- ambiguous aliases can remain unresolved;
- aggregation chooses an explicit taxonomy version.

**Guardrails:** Taxonomy must serve actual queries and decisions. Avoid building an encyclopedic ontology unrelated to JobHunter's corpus.

**Promotion signal:** Core Phase-2 foundation.

---

## B030 — External taxonomy comparison (ESCO/O*NET or similar)

**Intent:** Reuse established occupational/skills reference systems where they add value without making them JobHunter's source of truth.

**Proposal:** Allow canonical JobHunter concepts/role archetypes to map optionally to external reference-taxonomy identifiers. Uses may include terminology normalization, occupation comparison, discovering missing aliases, or providing broader context.

**Design direction:** Store mappings with mapping type, confidence/review status, external version, and notes. JobHunter's observed market evidence remains primary for local conclusions.

**Guardrails:** Do not force the corpus into an external taxonomy when the local market contains newer/hybrid work patterns. External schemas change and must be versioned.

**Promotion signal:** After JobHunter's own canonical taxonomy and role model have real data to compare.

---

## Category-level recommendation

The likely Phase-2 backbone is: canonical responsibilities and concepts → requirement strength/depth → role archetypes → co-occurrence/bundles → optional external mappings. Role DNA, title mismatch, prerequisite graphs, and substitution intelligence should build on that backbone rather than becoming independent AI features.