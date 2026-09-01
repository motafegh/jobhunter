# P2.2A Job Work Intelligence Representation Amendment

**Status:** APPROVED / IMPLEMENTED / REAL-LOCAL ACCEPTED
**Date:** 2026-09-01  
**Applies to:** `docs/P2_2_RESPONSIBILITY_WORK_ROLE_INTELLIGENCE_PLAN.md`  
**Scope:** P2.2A Job Work Intelligence representation, authority ownership, persistence contract, browser/CLI presentation, and post-redesign acceptance  
**Evidence checkpoint:** `docs/working-memory/2026-09-01_P2_2A_ACTION_AUTHORITY_TRIALS_AND_REPRESENTATION_REDESIGN_GATE.md`

This amendment resolves the P2.2A action-authority representation blocker. It is controlling where it is more specific than the base P2.2 plan. All unrelated P2.2 boundaries, non-goals, promotion rules, publication limits, and P2.2B/C/D sequencing remain unchanged. Its implementation and bounded post-implementation acceptance sequence are complete.

---

## 1. Decision summary

The repeated `tG9K` and `tmyX` trials established a stable boundary:

- local semantic reasoning is useful for grouping accepted work into coherent themes;
- model judgment is useful for relative emphasis, confidence, candidate role characterization, ambiguity, and bounded deliverable interpretation;
- free-form model prose is not reliable enough to carry factual action authority across heterogeneous jobs;
- stronger prompts, larger models, split generation/review protocols, and field-complete authority review improved some wording but did not reliably preserve action relationship and lifecycle endpoint;
- the 12B review route is additionally unsuitable for normal repeated-use latency.

Therefore P2.2A will no longer ask model prose to serve simultaneously as useful interpretation and factual work wording.

The approved architecture is:

```text
accepted/current English P1.6 direct-work statements
        ↓
model candidate grouping / emphasis / bounded interpretation
        ↓
deterministic reference + coverage validation
        ↓
deterministic assembly of exact accepted P1.6 work statements inside each theme
        ↓
persist one candidate Work Intelligence artifact with explicit fact/interpretation separation
        ↓
browser + CLI presentation
```

Permanent principle for this layer:

> **The model decides how accepted work is usefully organized; accepted P1.6 statements decide what factual work is actually asserted.**

---

## 2. Authority ownership

### 2.1 Accepted factual work

Factual action authority comes only from the exact accepted/current English P1.6 direct-work substrate:

```text
responsibilities[].statement
role_purpose[].statement
```

The final Work Intelligence artifact must carry those exact accepted statements through deterministic assembly. The model must not rewrite them into the factual portion of the artifact.

These are accepted P1.6 factual semantic statements, not necessarily literal original-language employer wording. Existing P1.6/source provenance remains the authority for recovering the underlying employer evidence.

### 2.2 Model-owned interpretation

The model may continue to own bounded candidate interpretation such as:

```text
theme identity and label
relative emphasis: primary | supporting | uncertain
field confidence: high | medium | low
supporting requirement references
candidate role label
candidate alternatives / limitations
bounded deliverable interpretation
optional explanatory interpretation / grouping rationale
ambiguity / unknown notes
```

These fields are **JobHunter interpretation**, not employer/P1.6 factual wording and not promoted canonical taxonomy.

### 2.3 Requirements remain supporting only

Requirements may support interpretation but still cannot independently create duties, stronger action verbs, ownership, autonomy, or lifecycle scope.

```text
requirement / technology mention alone
!=
direct work fact
```

No part of this amendment weakens that boundary.

---

## 3. Representation contract

### 3.1 Separate model candidate from persisted assembled artifact

The implementation should use two typed conceptual shapes rather than asking one model-returned document to own both interpretation and factual text.

#### Model candidate shape

The inference response should contain only the semantic decisions the model is actually allowed to make. At minimum:

```text
CandidateWorkTheme
- theme_id
- label
- emphasis
- confidence
- responsibility_indices[]
- role_purpose_indices[]
- optional supporting_requirement_indices[]
- optional interpretation / rationale

CandidateDeliverable
- label
- status: source_explicit | strongly_implied_by_work
- confidence
- responsibility_indices[]
- role_purpose_indices[]
- rationale when needed

CandidateRoleInterpretation
- label
- confidence
- supporting_theme_ids[]
- alternatives[]
- limitations[]

CandidateJobWorkIntelligence
- evidence_status
- work_themes[]
- deliverables[]
- optional role_interpretation
- limitations[]
```

The model candidate does **not** author accepted direct-work statements.

#### Persisted assembled shape

After candidate validation, application code resolves every accepted direct-work reference into a deterministic factual item.

Recommended factual item:

```text
AcceptedWorkItem
- kind: responsibility | role_purpose
- index
- statement          # exact accepted P1.6 statement
- confidence         # copied from P1.6 when available
```

A persisted work theme should therefore contain:

```text
WorkTheme
- theme_id
- label                         # JobHunter candidate interpretation
- emphasis                      # JobHunter candidate interpretation
- confidence                    # JobHunter candidate interpretation
- accepted_work_items[]         # deterministic exact P1.6 factual work
- optional supporting_requirement_indices[]
- optional interpretation / rationale
```

The same pattern applies to deliverables: supporting accepted work is injected deterministically and displayed beside the candidate deliverable interpretation.

### 3.2 Remove model prose from factual-action duty

The following current fields must not remain the primary factual description of work:

```text
JobWorkIntelligence.work_summary
WorkTheme.summary
CandidateRoleInterpretation.summary
DeliverableCandidate.summary
```

Approved disposition for the first redesigned contract:

- `work_summary`: remove from the model/persisted v2 representation rather than keeping an action-bearing headline;
- `WorkTheme.summary`: remove as the theme's factual description; an optional explicitly labeled interpretation/rationale may remain;
- `CandidateRoleInterpretation.summary`: remove from the required v2 shape; the candidate label + confidence + alternatives/limitations are sufficient initially;
- `DeliverableCandidate.summary`: remove from the required v2 shape; label/status/confidence/rationale + exact supporting work are sufficient initially.

Do not preserve redundant free-form prose merely for backward visual similarity.

If later product evidence shows one of these summaries materially improves comprehension, it may return only as an explicitly labeled candidate interpretation field, never as factual action wording.

### 3.3 Keep references recoverable

The model still reasons with zero-based P1.6 indices. The final artifact must keep the factual source kind/index recoverable through each injected `AcceptedWorkItem`.

Separate raw index arrays do not need to remain in the final persisted theme if `accepted_work_items[]` fully and deterministically preserves their identity. Avoid redundant persisted representations unless implementation simplicity clearly justifies them.

---

## 4. Versioning and history

This redesign materially changes the persisted semantic representation. It is not another `v1.3` prompt-only refinement.

Approved new identities:

```text
persisted Work Intelligence schema/contract: job-work-intelligence-v2
prompt/runtime identity:                     job-work-intelligence-v2.0
```

P2.2A remains the same product delivery increment; the `v2` identifier describes the corrected Work Intelligence artifact/representation contract.

Historical artifacts 2-11 and their attempt/request/raw-response records remain immutable under their original identities. Do not rewrite, migrate, or delete them.

The current SQLite table already keys artifact identity by accepted P1.6 dependency + model + prompt + schema. The representation redesign therefore should not require rewriting historical JSON. Add a database migration only if implementation reveals an actual table-level need; do not create one ceremonially.

---

## 5. Reasoning pipeline amendment

### 5.1 Approved v2 flow

```text
accepted/current P1.6
        ↓
deterministic compact indexed factual input
        ↓
one bounded model candidate-generation call
        ↓
deterministic schema/reference/coverage/currentness validation
        ↓
optional one bounded regeneration only when existing post-generation guards reject the candidate
        ↓
deterministic accepted-work injection / final artifact assembly
        ↓
persist candidate artifact
        ↓
browser / CLI
```

### 5.2 Remove the dedicated second model authority-review pass

The current v1.3 `generation → authority-review` design was an evidence-gathering response to action inflation. Cross-job trials demonstrated that another free-form model pass cannot reliably establish factual action authority.

For v2:

- remove the dedicated semantic authority-review model call from the active successful path;
- do not replace it with a larger-model review, multi-model vote, verb-equivalence table, or additional review ceremony;
- preserve raw generation request/response identity for reproducibility;
- retain at most the already-bounded regeneration path for a candidate that fails deterministic post-generation guards.

This both strengthens the authority model and reduces normal repeated-use latency.

### 5.3 Deterministic validation retained

Keep the existing strong deterministic responsibilities:

- exact accepted/current P1.6 dependency validation;
- reference bounds validation;
- every accepted responsibility/role-purpose covered by at least one theme for `sufficient` results;
- each theme owns direct work evidence;
- each deliverable owns direct work evidence;
- candidate role interpretation references valid theme IDs;
- schema validity;
- artifact currentness/reuse identity;
- no publication side effect.

The existing unsupported scope-intensifier guard may remain for clearly misleading candidate prose such as unsupported `end-to-end` or `full lifecycle` claims. It must not grow into deterministic semantic paraphrase machinery.

### 5.4 No deterministic verb equivalence system

This amendment explicitly rejects machinery such as:

```text
develop/provide -> allowed verbs table
partner toward production -> allowed lifecycle verbs table
```

The system does not need to prove every paraphrase equivalent once factual action wording is carried by exact accepted P1.6 statements.

---

## 6. Limited-work behavior

`tmBK` remains the intentional negative anchor.

When accepted P1.6 has no responsibility or role-purpose evidence:

```text
evidence_status = limited
work_themes = []
deliverables = []
role_interpretation = none
explicit limitation explaining that qualifications are not converted into duties
```

No model call is required for this path. The redesign must not create a factual-work container populated from requirements.

---

## 7. Browser and CLI presentation

### 7.1 Browser hierarchy

The normal browser view must make the authority split visible through structure, not only explanatory footer text.

Recommended theme presentation:

```text
Production readiness & engineering collaboration
PRIMARY · HIGH CONFIDENCE
JobHunter candidate theme

Accepted work
- Partner with the semiconductor technical lead and engineering to move models toward production.
  P1.6 responsibility 6

JobHunter interpretation              # only when useful
- optional grouping rationale / explanation
```

The exact accepted work statements are therefore visible at the point where the user evaluates each theme. Raw index lists alone are insufficient as the factual presentation.

### 7.2 Top-level presentation

The redesigned page should prioritize:

1. candidate work-theme structure;
2. exact accepted work inside each theme;
3. optional clearly marked JobHunter interpretation;
4. candidate deliverables;
5. candidate role interpretation;
6. limitations/unknowns;
7. artifact/dependency metadata.

Do not lead with a free-form model-generated action summary.

### 7.3 Provenance wording

Use labels such as:

```text
Accepted P1.6 work
JobHunter interpretation
Candidate role interpretation
Unknown / limited
```

Do not label translated/derived English P1.6 statements as literal employer-authored English. The underlying source evidence remains recoverable through the accepted P1.6 dependency.

### 7.4 CLI

CLI output must use the same assembled artifact and authority distinction as the browser. It must not reconstruct a different semantic data model.

---

## 8. Implementation scope

The smallest expected implementation surface is:

```text
src/jobhunter/work_intelligence_models.py
src/jobhunter/work_intelligence_service.py
src/jobhunter/web/work_intelligence.py              # only if context assembly changes
src/jobhunter/web/templates/work_intelligence.html
CLI formatter/entrypoint where current fields are rendered
focused Work Intelligence tests
```

`work_intelligence_inference.py` should only change if needed for the new candidate response model or removal of the second review call. Do not redesign generic inference infrastructure.

`work_intelligence_store.py` should remain structurally unchanged unless an actual persistence need is discovered; JSON schema identity already separates v1 and v2 artifacts.

Do not modify P1.6, Capability v9, Canonical Registry, Market, public corpus publication, or Blueprint as part of this repair.

---

## 9. Required regression evidence

Add focused deterministic tests proving the representation boundary by construction.

At minimum:

- exact P1.6 responsibility/role-purpose statements are copied unchanged into final theme `accepted_work_items`;
- source kind/index and statement cannot disagree;
- model candidate output cannot replace an accepted statement with stronger wording;
- a candidate may use an interpretive label while factual work remains exact;
- all accepted direct work remains covered across themes;
- invalid references still fail;
- requirement-only evidence still cannot create work;
- valid direct-work generation uses one model call in the normal path rather than generation + authority review;
- bounded regeneration remains bounded when deterministic candidate validation rejects a draft;
- historical v1 artifacts remain readable/historical and are not reused as current v2 artifacts;
- current v2 artifact reuse remains idempotent;
- browser and CLI visibly distinguish accepted work from JobHunter interpretation;
- Work Intelligence remains excluded from public-corpus publication.

Use the known relationships as regression examples where useful:

```text
tG9K:
"Partner with the semiconductor technical lead and engineering to move models toward production."
must remain exactly that factual work statement even if candidate interpretation contains stronger wording.

tmyX:
"...develop and provide security requirements, Best Practices, and hardening solutions."
must not become factual direct hardening execution through Work Intelligence representation.
```

These are regression fixtures/authority examples, not authorization for another sequence of live model trials.

---

## 10. Post-implementation acceptance sequence

Do **not** rerun the completed v1.3-v1.7 model/action-authority trial matrix.

After deterministic v2 implementation quality is green:

```text
1. t4qV — generate/review one redesigned real direct-work artifact
2. tmBK — verify deterministic limited-work behavior
3. unchanged current v2 job — verify artifact reuse
4. browser — inspect authority separation and user comprehension on real artifacts
5. CLI — confirm same final representation semantics
6. decide P2.2A semantic/product acceptance
7. only then decide whether P2.2B should begin
```

`tG9K` and `tmyX` already provide the cross-job evidence that justified this redesign. They may be used as deterministic fixtures and historical semantic evidence; do not require more live action-authority model trials merely to prove the same failure again.

P2.2A acceptance should answer:

> Does the redesigned view materially reduce manual responsibility synthesis while making the exact accepted work immediately recoverable and preventing candidate prose from silently becoming factual action authority?

---

## 11. Stop lines

This amendment and the completed P2.2A acceptance do **not** authorize:

- P2.2B/C/D implementation without a separate next-stage decision;
- deterministic action-verb equivalence machinery;
- another prompt-only/model-only action-authority experiment series;
- 12B authority-review routing for ordinary Work Intelligence;
- multi-model voting;
- fixed primary-theme quotas;
- bulk responsibility canonicalization;
- public-corpus publication of Work Intelligence;
- P2.3 capability requirement profiles;
- Market v2;
- personal readiness/gap/recommendation/scoring;
- P1.6/Capability reopening without new material upstream evidence.

---

## 12. Acceptance outcome and exact next action

The representation decision is approved, implemented, and accepted on:

```text
job-work-intelligence-v2 / job-work-intelligence-v2.0
```

The real-local `t4qV → tmBK → reuse → browser → CLI` sequence passed. Evidence and the final
P2.2A decision are recorded in:

`docs/working-memory/2026-09-01_P2_2A_V2_REAL_LOCAL_ACCEPTANCE.md`

```text
P2.2A ACCEPTED / CLOSED
→ STOP
→ P2.2B decision NOT STARTED
```

No further representation-design or prompt/model action-authority trial is required. P2.2B work
requires a separate focused decision.
