# JobHunter Personal Capability, Evidence, and Portfolio Intelligence Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B041-B048, B054, B164-B166, B177, B197-B199

---

## Purpose

This family defines how JobHunter could eventually represent the user without turning conversational assumptions, repository keywords, course completion, or AI-generated code into unjustified claims of mastery.

`AGENTS.md` currently prohibits implementation of personal capability gaps/readiness/recommendations until a reviewed personal-evidence schema exists with depth, recency, evidence references, and confidence. These proposals are therefore intentionally future-facing.

---

## B041 — Personal Evidence Ledger

**Intent:** Replace a generic “skills profile” with an inspectable record of what the user can actually support with evidence.

**Proposal:** Introduce a durable `PersonalCapability` + `CapabilityEvidence` model. A capability record describes the current interpreted capability state, while evidence records point to concrete artifacts/events such as project work, professional experience, assessments, technical explanations, debugging, deployment, repeated practice, or reviewed self-report.

**Design direction:**

```text
Capability
- canonical concept
- depth state
- confidence
- recency / last evidence
- limitations
- review status

Evidence
- type
- source/reference
- date
- AI-assistance context where relevant
- what it demonstrates
- strength / limitations
```

**Guardrails:** No capability is created from memory/chat context without explicit user-provided evidence and review.

**Promotion signal:** This is the prerequisite foundation for Phase 3.

---

## B042 — Personal evidence-type taxonomy

**Intent:** Distinguish evidence sources that support different levels of confidence and independence.

**Proposal:** Define evidence types such as professional work, personal project implementation, source-code contribution, tests, architecture decisions, debugging incidents, deployment/operation, technical explanation, assessment, course/lab, repeated practice, and reviewed self-report.

**Design direction:** Evidence type is not automatically evidence strength. A small but independently debugged project may demonstrate something different from a large AI-assisted codebase. Store type plus explicit demonstrated behavior.

**Guardrails:** Avoid rigid universal rankings of evidence types. Context matters, and professional work should not automatically imply mastery of every technology present.

**Promotion signal:** During Phase-3 schema design.

---

## B043 — GitHub/project evidence importer

**Intent:** Reduce manual evidence entry while refusing naive “repository contains X therefore user knows X” inference.

**Proposal:** Allow the user to select repositories/projects for evidence inspection. JobHunter could collect observable project facts such as files, technologies, tests, commits, architecture docs, deployment configs, issue/PR work, and user-reviewed explanations.

**Design direction:** The importer creates **evidence candidates**, not capabilities. Stronger evidence may require user confirmation such as “I designed this,” “I debugged this failure,” or an assessment/explanation workflow.

**Guardrails:** Do not scan private repositories without explicit connection/selection. Do not infer independent proficiency from generated code or dependency declarations.

**Promotion signal:** After manual Personal Evidence Ledger workflows prove the schema.

---

## B044 — Capability depth states

**Intent:** Represent progression without binary `knows / does not know` labels.

**Proposal:** Adopt a reviewed ordinal/categorical depth model aligned with the existing domain concept, for example:

```text
0 Unassessed
1 Awareness
2 Introductory understanding
3 Guided practice
4 Independent bounded execution
5 Integrated application
6 Repeated independent evidence
7 Production / production-like operation
```

Exact labels may be refined before implementation.

**Design direction:** Depth changes require evidence. Store the evidence supporting the current depth and retain previous assessments.

**Guardrails:** Depth is capability-specific and context-specific; do not claim professional production depth from personal projects merely because they are complex.

**Promotion signal:** Core Phase-3 schema decision.

---

## B045 — Capability confidence separate from depth

**Intent:** Distinguish “how deep the evidence suggests” from “how certain JobHunter is about that assessment.”

**Proposal:** Store confidence independently from capability depth. Example: a capability may appear to be at guided-practice depth with high confidence, while another appears potentially independent but has only one ambiguous evidence item and therefore low confidence.

**Design direction:** Confidence should be categorical initially and linked to evidence quantity/quality/review, not an arbitrary model probability.

**Guardrails:** Do not let high confidence make a low depth look stronger, or vice versa.

**Promotion signal:** Alongside capability depth.

---

## B046 — Capability recency

**Intent:** Recognize that technical evidence ages and capabilities can become stale.

**Proposal:** Track dates of supporting evidence and optionally derive recency states such as active/recent/stale/unknown for capabilities where recency matters.

**Design direction:** Preserve all historical evidence. Recency affects current confidence/readiness interpretation but never deletes prior achievements.

**Guardrails:** Avoid arbitrary expiration rules. Some foundational knowledge decays differently from fast-moving tool familiarity.

**Promotion signal:** Phase-3 evidence model, especially once evidence accumulates longitudinally.

---

## B047 — Capability independence / AI-assistance context

**Intent:** Represent AI-assisted engineering honestly without either dismissing it or treating generated work as fully independent mastery.

**Proposal:** Add evidence attributes describing how work was produced and what the user demonstrated, for example:

```text
AI-generated with limited user understanding
AI-assisted with user explanation
AI-assisted with user architecture/decision ownership
user independently modified/debugged
user independently reproduced
repeated independent evidence
```

**Design direction:** Independence is evidence metadata, not moral judgment. Different capabilities within one project can have different independence evidence.

**Guardrails:** Do not attempt to infer AI usage from code style. Record only explicit/observable evidence.

**Promotion signal:** Required before repositories/projects become major personal capability evidence.

---

## B048 — Market-concept ↔ personal-capability mapping

**Intent:** Compare employer requirements with personal evidence even when wording and granularity differ.

**Proposal:** Map market canonical concepts/capabilities to personal capability records, supporting exact, broader/narrower, and partial relations.

**Example:** A market requirement for `SIEM query development` might be partially supported by personal evidence in log analysis and a specific SIEM lab, while still lacking production evidence.

**Design direction:** Mapping relations are explicit and reviewable. They do not automatically upgrade personal depth.

**Guardrails:** Do not use semantic similarity alone to declare equivalence.

**Promotion signal:** After both Phase-2 taxonomy and Phase-3 evidence schemas exist.

---

## B054 — Evidence portability across jobs

**Intent:** Avoid re-evaluating the same personal capability from scratch for every vacancy.

**Proposal:** Once a capability/evidence interpretation is reviewed, reuse it as a stable input to requirement comparisons across many jobs. Job-specific comparison stores only the relation/assessment, not a duplicate personal profile.

**Design direction:** Changes to capability evidence invalidate or refresh affected gap/readiness assessments through versioned dependencies.

**Guardrails:** Reuse the evidence, not a universal conclusion. The same capability can satisfy one employer requirement and be insufficient for another requiring greater depth/context.

**Promotion signal:** Foundational Phase-3 architecture rule.

---

## B164 — Personal longitudinal progress report

**Intent:** Show what actually changed in the user's evidence over time.

**Proposal:** Produce a periodic/user-triggered report covering new evidence, depth changes, confidence changes, gaps closed, newly demonstrated integrations, stale evidence, and target-market requirements newly covered.

**Design direction:** Every improvement statement links to evidence and previous assessment state. Distinguish `new evidence recorded` from `capability depth increased`.

**Guardrails:** Avoid motivational inflation. If no evidence changed, the report should say so.

**Promotion signal:** After sufficient personal evidence history exists.

---

## B165 — Explicit protection against false progress

**Intent:** Prevent learning trackers from implying mastery because a topic was mentioned or introduced.

**Proposal:** JobHunter should preserve depth semantics in every learning/progress surface. Reading an explanation or completing an introductory exercise may update a capability from `unassessed` to `awareness/introductory`, not to “complete.”

**Design direction:** Every progress transition specifies the evidence type and depth change. UI language should avoid checkmarks that imply full mastery unless the state actually means that.

**Guardrails:** Do not gamify capability evidence into completion percentages detached from depth.

**Promotion signal:** Permanent requirement for any learning/progress feature.

---

## B166 — Career experiment evidence

**Intent:** Let deliberate learning/building experiments produce measurable evidence changes.

**Proposal:** A user may define an experiment such as “build a bounded network-event pipeline to strengthen networking/security-telemetry evidence.” Before execution, specify targeted capabilities and expected evidence. After completion, record what was actually demonstrated and whether the original hypothesis was supported.

**Design direction:** Link experiment → project/work artifacts → capability evidence → affected gap assessments. A failed experiment can still create useful debugging/knowledge evidence.

**Guardrails:** Completing the project does not automatically grant the planned capability depth.

**Promotion signal:** After the evidence ledger and gap-to-project workflow exist.

---

## B177 — Multiple personal/career profiles or scenarios

**Intent:** Support legitimately different user contexts without contaminating one evidence base.

**Proposal:** If needed later, allow multiple user-controlled profile/scenario contexts, for example separate target-career configurations or public/private portfolio views, while keeping shared evidence reusable where appropriate.

**Design direction:** Prefer one evidence ledger with multiple views/targets over duplicating evidence. Only introduce truly separate profiles if different people or incompatible privacy domains become a real requirement.

**Guardrails:** JobHunter is currently a single-user personal application. Do not turn this into multi-user account architecture prematurely.

**Promotion signal:** Only when a concrete repeated-use need appears.

---

## B197 — Personal specialization detector

**Intent:** Identify coherent evidence clusters that may represent an emerging specialization.

**Proposal:** Analyze reviewed personal evidence across capabilities, projects, and repeated work patterns to surface clusters such as `Python + security automation + local AI integration + Linux`.

**Design direction:** Present as an observation: `Your strongest current evidence cluster is ...`, with links to supporting projects/evidence and missing adjacent depth.

**Guardrails:** Do not define the user's identity permanently or infer career preference from capability clustering alone.

**Promotion signal:** After enough reviewed evidence spans multiple projects/capabilities.

---

## B198 — Career narrative consistency

**Intent:** Help choose which projects/evidence collectively tell a coherent professional story.

**Proposal:** Compare selected portfolio projects against target-role responsibility/capability families and identify the recurring technical themes they demonstrate.

**Design direction:** Output supporting themes, gaps in the story, redundant evidence, and candidate project examples. Resume/social prose can be generated later only from reviewed evidence.

**Guardrails:** Narrative coherence must not erase legitimate breadth or invent intent that was never present.

**Promotion signal:** Useful once application/portfolio preparation is built.

---

## B199 — Missing portfolio evidence analysis

**Intent:** Detect target-market capabilities that are repeatedly required but poorly represented by inspectable personal projects/evidence.

**Proposal:** Compare the portfolio evidence matrix with target-role market requirements. Example finding: several AI-heavy projects demonstrate Python/LLM work, but there is little inspectable evidence for network telemetry, deployment, or observability.

**Design direction:** Distinguish true knowledge gaps from evidence/presentation gaps. Recommend a new project only when existing work cannot reasonably provide the missing evidence.

**Guardrails:** Do not conclude the user lacks a capability solely because GitHub does not show it; personal/professional evidence may exist elsewhere.

**Promotion signal:** After portfolio import and personal evidence mapping are mature.

---

## Category-level recommendation

Phase 3 should begin with the smallest credible evidence ledger: capability, depth, confidence, recency, evidence reference/type, and explicit limitations. Repository import, specialization detection, progress reports, and portfolio intelligence should be added only after manual evidence review proves the underlying model.