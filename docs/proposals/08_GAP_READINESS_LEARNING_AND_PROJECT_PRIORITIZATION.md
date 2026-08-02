# JobHunter Gap, Readiness, Learning, and Project-Prioritization Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B049-B053, B055-B067, B130-B136

---

## Purpose

This family defines how JobHunter could translate market evidence and reviewed personal evidence into useful next actions without creating fake fit scores or false confidence. These proposals are blocked until the personal-evidence schema and Phase-2 market taxonomy are reviewed and accepted.

The key idea is that a “gap” is not synonymous with “skill absent.” It may be missing knowledge, insufficient depth, weak practice evidence, lack of production context, stale evidence, or simply an unknown state.

---

## B049 — Gap taxonomy

**Intent:** Represent why market demand and personal evidence differ.

**Proposal:** Define gap classes such as:

```text
knowledge_gap
practice_gap
depth_gap
integration_gap
production_evidence_gap
recency_gap
presentation/evidence_gap
experience_context_gap
credential_gap
unknown_evidence
```

**Design direction:** A gap assessment links one employer/market requirement to one or more personal capabilities/evidence records, with a rationale and severity/criticality context.

**Guardrails:** Do not create a gap when the personal state is merely unknown; preserve `unknown` separately unless the decision policy explicitly treats unknown as risk.

**Promotion signal:** Core Phase-3 gap-schema decision.

---

## B050 — Evidence-backed gap explanations

**Intent:** Make every gap answer “why does JobHunter believe this?”

**Proposal:** Gap detail should show the market evidence, requirement strength/depth, personal evidence found, limitations, and exactly what remains unsupported.

**Example:**

```text
Market: 17/28 target roles explicitly require Docker/container operation.
Personal: one guided Docker lab, no independent deployment evidence.
Gap: practice/depth gap, not a knowledge-absence claim.
```

**Guardrails:** Aggregate market evidence must expose sample size and scope. Personal evidence must be reviewed.

**Promotion signal:** Required for any gap UI.

---

## B051 — Gap severity without opaque readiness percentages

**Intent:** Prioritize meaningful gaps without generating a false `82% ready` score.

**Proposal:** Use categorical summaries such as:

```text
critical required gaps
partial required gaps
strong required matches
preferred gaps
unknown requirements
```

Severity depends on employer requirement strength, personal depth mismatch, and decision policy.

**Guardrails:** Avoid hidden weighted formulas. If weighting is later introduced, every factor remains visible.

**Promotion signal:** Before job readiness recommendations.

---

## B052 — “Can I apply now?” categorical decision support

**Intent:** Give practical application guidance while preserving uncertainty.

**Proposal:** Derive categories such as `apply now`, `reasonable to apply`, `targeted preparation recommended`, `major required gaps`, or `insufficient evidence` from explicit policies and requirement comparisons.

**Design direction:** The result must link to blocking requirements, strengths, constraints, and unknowns. Users may configure a policy or override the conclusion.

**Guardrails:** This is decision support, not prediction of recruiter behavior or interview success.

**Promotion signal:** Phase 4 after personal evidence and gap assessment are accepted.

---

## B053 — Requirement-by-requirement job comparison

**Intent:** Replace one aggregate fit number with inspectable evidence per employer requirement.

**Proposal:** Present a matrix such as:

```text
Requirement | Employer strength | Personal evidence | Assessment
Python      | required          | repeated project evidence | strong
Docker      | required          | guided practice           | partial
Kubernetes  | preferred         | introductory              | weak
SOC ops     | required          | none reviewed              | major gap
```

**Design direction:** Every row links to source evidence and personal evidence. Allow `unknown` and conflicting states.

**Guardrails:** Do not silently merge several employer requirements into one row when their depth/context differs.

**Promotion signal:** Core Phase-4 opportunity workflow.

---

## B055 — “Why am I not ready?” explanation

**Intent:** Replace generic advice with evidence-specific blockers.

**Proposal:** Summarize the few most consequential required gaps for a selected job/target archetype and explain their market prevalence and personal-evidence limitations.

**Design direction:** Prefer statements such as “networking is repeatedly required across this target cohort, while current evidence is introductory” over generic “improve cybersecurity.”

**Guardrails:** Lack of evidence is not proof of inability. Label it accurately.

**Promotion signal:** Built on gap explanations and role-target cohorts.

---

## B056 — “Why am I more ready than I think?” explanation

**Intent:** Surface strong evidence that may be hidden by unconventional background or job-title mismatch.

**Proposal:** Identify employer requirements for which reviewed project/technical evidence is stronger than a resume/title-based glance would suggest.

**Design direction:** Explain exact evidence and its limitations. Example: strong Python automation/local inference project evidence may support technical requirements even without prior tech-company employment.

**Guardrails:** Do not convert project evidence into professional-production experience if it is not that.

**Promotion signal:** Alongside negative-gap explanations to keep assessment balanced.

---

## B057 — Career direction comparison

**Intent:** Compare target paths using collected market and personal evidence rather than generic internet career advice.

**Proposal:** Compare role families on observed vacancy volume, responsibility mix, required concepts/depth, personal evidence overlap, major gaps, constraints, and evidence-building burden.

**Guardrails:** Market coverage/source bias and personal unknowns must be visible. Do not rank a career path by salary or popularity alone.

**Promotion signal:** After role archetypes and personal evidence mapping exist.

---

## B058 — Adjacent-role discovery

**Intent:** Prevent over-fixation on one title when similar work exists under neighboring role families.

**Proposal:** Use responsibility/capability overlap to identify adjacent archetypes and show how they differ in required work, depth, and personal gaps.

**Guardrails:** Adjacency is analytical similarity, not a claim that the user wants that role.

**Promotion signal:** After role archetype and similarity structures exist.

---

## B059 — Career graph

**Intent:** Represent possible transitions among role archetypes through capability/responsibility relationships.

**Proposal:** Build a reviewed graph where nodes are role archetypes and edges describe why one role may be adjacent or a plausible progression based on shared responsibilities and incremental capability requirements.

**Guardrails:** Do not treat the graph as a deterministic career ladder. Employers and individual paths vary.

**Promotion signal:** Later Phase 4 after archetypes and gap mappings are mature.

---

## B060 — Relative path cost

**Intent:** Compare how much additional evidence/preparation different target paths appear to require.

**Proposal:** Derive transparent components such as missing prerequisite count, depth gaps, required project evidence, production-context gaps, and hard personal constraints. Present a qualitative/relative cost rather than “six weeks to mastery.”

**Guardrails:** Time-to-learn estimates are highly individual; do not fabricate precision.

**Promotion signal:** After gap taxonomy and prerequisite relationships exist.

---

## B061 — Learning priority engine

**Intent:** Prioritize learning based on career evidence, not topic popularity.

**Proposal:** Combine transparent factors such as market prevalence, requirement strength, target-role relevance, personal gap magnitude, prerequisite importance, and evidence-building opportunity.

**Design direction:** Show each factor and allow the user to change target scope. A simple ordered rule set may be preferable to a numeric formula initially.

**Guardrails:** The system recommends priorities, not mandatory study. Emerging hype should not overpower foundational dependencies.

**Promotion signal:** Phase 4 after market/personal/gap layers are accepted.

---

## B062 — “What should I learn next?” evidence answer

**Intent:** Convert the learning priority engine into a concise next-action explanation.

**Proposal:** For each recommended topic, show:

- why it matters in the selected market;
- which role responsibilities depend on it;
- current personal evidence depth;
- what depth is needed now versus later;
- what evidence could demonstrate progress.

**Guardrails:** Avoid giant roadmaps when one prerequisite is the actual bottleneck.

**Promotion signal:** First user-facing learning surface after the priority engine.

---

## B063 — Learning dependency planner

**Intent:** Respect prerequisite order so JobHunter does not recommend advanced tools before foundations.

**Proposal:** Use the reviewed prerequisite graph to sequence learning. If Kubernetes demand is high but container fundamentals are weak, recommend the dependency first and explain why.

**Guardrails:** Dependencies are not always strict. Distinguish required prerequisite from helpful background.

**Promotion signal:** After prerequisite graph + personal depth model.

---

## B064 — Gap-to-project generator

**Intent:** Turn important gaps into bounded practical learning/building opportunities.

**Proposal:** Generate project concepts specifically targeted at a small set of capability/evidence gaps. Example: a network-event ingestion/detection lab could target Python networking, telemetry handling, Docker, and detection reasoning.

**Design direction:** Project suggestions include targeted capabilities, intended evidence, scope stop-lines, and prerequisites. AI may propose options; the user approves.

**Guardrails:** Do not generate oversized flagship projects for every gap. Prefer the smallest project that can produce credible evidence.

**Promotion signal:** After learning priorities and evidence contracts exist.

---

## B065 — Project Evidence Planner

**Intent:** Define what a project should demonstrate before building begins.

**Proposal:** Attach an evidence plan to a learning project:

```text
capabilities targeted
expected depth
observable deliverables
required tests/debugging/explanation evidence
AI-assistance context to record
stop line
```

After completion, compare intended versus actual evidence.

**Guardrails:** Planned evidence is not awarded automatically.

**Promotion signal:** Companion to gap-to-project generation.

---

## B066 — Portfolio coverage analysis

**Intent:** Show which target-market capabilities are repeatedly demonstrated across projects and which are barely represented.

**Proposal:** Build a capability × project evidence matrix, with depth/recency/independence rather than checkmarks.

**Guardrails:** The matrix reflects recorded evidence only, not the user's entire knowledge.

**Promotion signal:** After project evidence import/ledger are mature.

---

## B067 — Evidence-building recommendation

**Intent:** Distinguish cases where the user needs more learning from cases where the main problem is lack of demonstrable evidence.

**Proposal:** Recommend action types such as:

```text
learn concept
practice independently
integrate with another capability
build a small artifact
document/explain existing work
obtain production-like operational evidence
assess current knowledge
```

**Guardrails:** Do not recommend another course when the gap is clearly evidence or practice rather than knowledge.

**Promotion signal:** Phase 4 action intelligence.

---

## B130 — Counterfactual capability analysis

**Intent:** Answer “what would change if I gained evidence for X?” without pretending that evidence already exists.

**Proposal:** Recalculate gap/readiness outcomes under a hypothetical capability state and compare with the current real state.

**Design direction:** Hypothetical states are isolated and clearly marked. Outputs show which jobs/roles would lose critical gaps and which blockers would remain.

**Guardrails:** Counterfactual improvement is not a prediction of hiring success.

**Promotion signal:** After deterministic gap assessment exists.

---

## B131 — Skill/capability ROI simulator

**Intent:** Compare which potential capability improvements affect the largest number of important target gaps.

**Proposal:** For candidate capabilities, calculate how many required/preferred gaps would be reduced under explicit hypothetical depth/evidence assumptions.

**Design direction:** Include target-role weighting, requirement strength, prerequisites, and remaining blockers. Show raw affected-job counts rather than only a single ROI number.

**Guardrails:** Market coverage is not the only value of learning; user interest and long-term strategy remain human decisions.

**Promotion signal:** Built on counterfactual analysis.

---

## B132 — Project ROI simulator

**Intent:** Compare candidate projects by the meaningful evidence they could create.

**Proposal:** Given project evidence plans, estimate which market gaps each project could address if successfully completed and verified.

**Design direction:** Separate `planned evidence coverage` from actual evidence after completion. Consider prerequisites and project scope/cost qualitatively.

**Guardrails:** A project that touches many technologies is not automatically high ROI; depth and verifiability matter.

**Promotion signal:** After Project Evidence Planner + counterfactual capability analysis.

---

## B133 — Opportunity-cost intelligence

**Intent:** Help avoid technology rabbit holes that are weakly aligned with the selected target market.

**Proposal:** Compare the observed target-market relevance of competing learning directions and show what important work is displaced by a lower-alignment choice.

**Design direction:** Example: a niche technology appears in few target roles while networking fundamentals recur across many security-automation responsibilities.

**Guardrails:** Do not turn market prevalence into a command. Personal motivation, experimentation, and long-term optionality can justify lower-market-alignment work.

**Promotion signal:** After learning priority evidence is mature.

---

## B134 — Explicit “ignore for now” recommendation

**Intent:** Recognize that not every observed gap deserves action.

**Proposal:** Support action states such as `learn`, `practice`, `build evidence`, `assess`, `monitor`, and `ignore for now`. A gap may be real but low priority because it is preferred-only, niche, redundant, blocked by more basic prerequisites, or outside the current target.

**Guardrails:** `Ignore for now` must include rationale and be revisitable when market/target state changes.

**Promotion signal:** Part of action-intelligence policy.

---

## B135 — Requirement criticality

**Intent:** Distinguish true blockers from soft requirements inside one job.

**Proposal:** Refine employer requirement interpretation into criticality states such as explicit must-have, strong required, soft required, preferred, and contextual where evidence supports the distinction.

**Design direction:** Criticality should derive from source wording and role context, not from the user's personal profile.

**Guardrails:** Do not overfit nuanced employer prose into more categories than can be reliably distinguished.

**Promotion signal:** Requires analysis-schema evaluation beyond current required/preferred/contextual/inferred.

---

## B136 — User-defined application threshold policy

**Intent:** Let readiness decisions follow an explicit policy instead of a hidden fit percentage.

**Proposal:** Support rules such as:

```text
reasonable_to_apply when:
- no more than one major required gap
- primary responsibility has supporting evidence
- no hard personal constraint is violated
```

**Design direction:** Policies are readable, editable, and scenario-specific. JobHunter explains which rule passed/failed.

**Guardrails:** The policy does not predict recruiter behavior and should not be presented as an industry standard.

**Promotion signal:** Before application-readiness categorization becomes actionable.

---

## Category-level recommendation

The core sequence should be: reviewed personal evidence → explicit gap taxonomy → requirement-by-requirement comparison → explainable categorical readiness → learning priorities → bounded evidence-building projects → counterfactual/ROI tools. The system should never jump directly from job text to a generic roadmap or numeric fit score.