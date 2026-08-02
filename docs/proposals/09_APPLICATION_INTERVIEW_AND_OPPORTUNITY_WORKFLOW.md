# JobHunter Application, Interview, and Opportunity Workflow Proposals

**Status:** Proposed — discussion/design inventory only  
**Authority:** Non-controlling; inclusion here does not authorize implementation  
**Date:** 2026-08-02  
**Primary brainstorm items:** B068-B076

---

## Purpose

This family covers the stage after JobHunter has enough evidence to support a real opportunity decision: preparing for interviews, selecting supporting project evidence, tracking applications, recording outcomes, and learning from explicit feedback. These capabilities remain downstream of the market, personal-evidence, and gap layers.

The permanent product non-goal remains: JobHunter does not autonomously submit applications.

---

## B068 — Interview-domain intelligence

**Intent:** Convert a selected job's evidence into a focused interview-preparation scope.

**Proposal:** Derive likely technical preparation domains from the posting's accepted responsibilities, requirements, technologies, and seniority signals.

**Design direction:** Output should distinguish:

- employer-explicit topics;
- likely discussion areas derived from responsibilities;
- personal evidence that can support each area;
- known gaps/unknowns requiring preparation.

**Guardrails:** Do not fabricate company-specific interview questions or claim knowledge of the employer's interview process unless sourced separately.

**Promotion signal:** After requirement-by-requirement personal comparison exists.

---

## B069 — Interview preparation matrix

**Intent:** Connect each important employer requirement to what the user should be ready to explain and demonstrate.

**Proposal:** Build a matrix:

```text
Requirement
→ source evidence / importance
→ concepts to explain
→ strongest personal evidence/example
→ missing preparation
→ candidate questions to self-test
```

**Design direction:** Generated practice questions should be clearly synthetic and grounded in the requirement, while factual claims about the user's experience come only from reviewed evidence.

**Guardrails:** Avoid endless question generation. Prioritize major responsibilities and critical requirements.

**Promotion signal:** Phase 4 application-preparation surface.

---

## B070 — Project story builder

**Intent:** Help select and structure the strongest real project examples for a specific opportunity.

**Proposal:** Given reviewed project/capability evidence, identify which projects best support requirements such as Python automation, system design, debugging, security reasoning, or ML integration.

**Design direction:** Initially output evidence mappings and story components:

```text
situation/context
problem
user-owned decisions/actions
evidence/result
limitations / AI-assistance context
```

Full prose can be generated later from these reviewed facts.

**Guardrails:** Never invent metrics, ownership, impact, or independence. AI-assisted work must be represented according to the evidence record.

**Promotion signal:** After portfolio evidence is reviewable.

---

## B071 — Application Evidence Pack

**Intent:** Create one inspectable preparation bundle for a selected job.

**Proposal:** Generate a versioned package containing:

- employer requirements and responsibilities;
- personal matching evidence;
- strongest relevant projects;
- critical/partial gaps;
- constraints/unknowns;
- interview-preparation topics;
- source links and artifact versions.

**Design direction:** The pack becomes a source for later resume tailoring, cover-letter assistance, interview prep, and manual application decisions.

**Guardrails:** The package is derived from current evidence and should become stale if the source job or personal evidence changes.

**Promotion signal:** Strong Phase-4 integration feature.

---

## B072 — Evidence-constrained resume targeting

**Intent:** Tailor resume emphasis to a job without inventing claims.

**Proposal:** Select and order only evidence-backed capabilities, projects, responsibilities, and outcomes that are relevant to the employer's requirements. Generated wording must remain traceable to personal evidence.

**Design direction:** Add a claim-validation layer: every material resume claim maps to one or more approved evidence records. The user remains final editor/approver.

**Guardrails:** No invented years, job titles, production scale, metrics, independent ownership, or technologies. Do not submit applications automatically.

**Promotion signal:** After Application Evidence Packs and personal evidence provenance are stable.

---

## B073 — Application tracker

**Intent:** Keep opportunity state separate from job-source lifecycle and local interest triage.

**Proposal:** Add application states such as:

```text
considering
preparing
applied
screening
technical_interview
final_interview
rejected
withdrawn
offer
closed_unknown
```

**Design direction:** Store dates, notes, contacts where the user explicitly provides them, linked Application Evidence Pack version, and known feedback/outcomes. Source job may become removed while the application remains active.

**Guardrails:** Do not infer application state from source lifecycle. Do not store sensitive contact data unnecessarily.

**Promotion signal:** When JobHunter begins supporting actual application preparation rather than only research.

---

## B074 — Opportunity decision journal

**Intent:** Preserve why an opportunity was pursued or skipped so later reflection uses actual decisions rather than memory.

**Proposal:** For significant jobs, allow a lightweight journal entry with why the user applied/skipped, attractive responsibilities, major gaps, constraints, expectations, and later outcome/reflection.

**Design direction:** Keep narrative notes separate from authoritative market/personal evidence. The journal may be intentionally subjective.

**Guardrails:** Do not let subjective journal text silently mutate capability or market records.

**Promotion signal:** Useful once application tracking exists; should remain optional and lightweight.

---

## B075 — Rejection/outcome learning with causal restraint

**Intent:** Learn from explicit application outcomes without inventing reasons for rejection.

**Proposal:** Record known recruiter/interviewer feedback separately from the outcome. If feedback explicitly states a missing capability, that becomes evidence relevant to career decisions; if no reason is provided, store `reason unknown`.

**Design direction:** Later reports can correlate outcomes with known gap states but must separate correlation from explicit causal feedback.

**Guardrails:** Never infer “rejected because Kubernetes” merely because Kubernetes was a gap. Do not use one rejection as proof a career path is impossible.

**Promotion signal:** Alongside application tracking.

---

## B076 — Opportunity watch

**Intent:** Surface newly acquired jobs that materially affect the user's active opportunity set.

**Proposal:** A future watch process could highlight new postings in selected role archetypes, jobs with unusually strong reviewed evidence overlap, target companies posting new relevant roles, or important changes to already-interesting jobs.

**Design direction:** Notifications are based on explicit target/watch settings and accepted analysis. The product should show why an item was surfaced.

**Guardrails:** Avoid compulsive high-frequency alerting and generic “new job” noise. User controls cadence and watch criteria.

**Promotion signal:** After repeated acquisition, target-role specifications, and job-level comparison are stable.

---

## Category-level recommendation

The strongest application architecture is evidence pack first, prose second. JobHunter should build a trustworthy bundle of employer evidence, personal evidence, gaps, and preparation topics; resume/interview assistance can then operate over that bundle without inventing facts.