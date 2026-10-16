# Phase-2 semantic direction reconciliation decision

**Date:** 2026-10-10  
**Status:** DECISION COMPLETE / P2.2B-B2 AUTHORIZED / IMPLEMENTATION-SUBSYSTEM EXPANSION NOT REQUIRED  
**Execution update — 2026-10-16:** R1 and R2 owner approvals are applied: mappings #7/#8 for `responsibility:design-implement-ai-agents` and #9/#10 for `responsibility:integrate-ai-systems-with-services`, each over the exact approved artifact 50/56 claims. Four of the 35 selected responsibilities are mapped; 31 remain pending. Exact dependencies, idempotency, rendered browser/CLI agreement, integrity, and preservation checks pass. R3 owner review is next; B2 remains active.
**Entry gate:** `docs/working-memory/2026-10-10_PHASE2_SEMANTIC_DIRECTION_RECONCILIATION_ENTRY.md`  
**Predecessor closure:** `docs/working-memory/2026-10-10_MARKET_R4_FINAL_LOCAL_ACCEPTANCE.md`

## 1. Decision

Select **Direction A**, but do not jump to P2.2C responsibility-family promotion.

The next bounded Phase-2 responsibility is:

```text
P2.2B-B2 — snapshot-15 selective responsibility normalization

accepted/current P1.6 responsibility claims
→ bounded candidate cross-job correspondences
→ explicit human semantic review
→ existing P2.1 Canonical Registry responsibility concepts + immutable claim mappings
→ acceptance / no-promotion disposition
```

P2.2C responsibility families remain NOT AUTHORIZED. P2.2D stable role archetypes remain NOT AUTHORIZED. P2.3 capability requirement profiles are deferred until reviewed cross-job canonical correspondence coverage is stronger. P2.4 Market v2 remains downstream.

This tranche is primarily **semantic review and local registry promotion using existing accepted machinery**, not a new software subsystem. Do not add a new model, store, service, workflow framework, or review system unless execution exposes a concrete missing capability in the existing P2.1 Registry path.

## 2. Why old B1 no longer controls the prerequisite

B1 ended `NO-PROMOTION / DEFER` because the selected second job `ta9l` never produced an acceptable/current P1.6 artifact within the bounded recovery. Artifact 47 was materially incomplete and rejected; final rebuild attempt 101 failed; therefore no accepted second responsibility claim existed and no canonical correspondence could be promoted.

B1 explicitly did **not** semantically reject the proposed cross-job responsibility identity. Its blocker was factual-input authority.

The current Market state materially changes that prerequisite:

```text
snapshot 15 accepted-semantic core postings: 6
accepted P1.6 responsibility claims:          35
postings with direct responsibility claims:    4
postings with zero responsibilities:           2
```

The four direct-work postings are:

```text
tvMm  artifact 50  responsibilities 11
tmvA  artifact 61  responsibilities  7
tjgi  artifact 60  responsibilities  9
tNVe  artifact 56  responsibilities  8
```

`t7ck` and `t7Ay` remain valid accepted-semantic postings but contribute no direct responsibility evidence and must not be used to manufacture responsibility correspondences from requirements alone.

## 3. Why Direction A precedes Direction B

Capability v9 is a strong accepted per-job architecture. Deterministic reconciliation owns source coverage, requirement strength, source-explicit depth, source work links, and role-level constraints; optional model enrichment may be absent or filtered safely.

However, P2.3 is a **cross-job reusable relationship** program, not merely another per-job Capability run. Its current prerequisites are weaker than P2.2B-B2:

- the public corpus contains only five accepted/current Capability artifacts, from the heterogeneous Phase-1 anchor set;
- the current six-posting Market snapshot is P1.6-backed and does not establish reviewed Capability-profile correspondence across those six jobs;
- P2.1 canonical coverage is intentionally tiny: four concepts and six reviewed claim decisions in the original seed;
- requirement-side scale is much larger: 140 accepted P1.6 requirement claims in snapshot 15 versus 35 responsibility claims;
- building P2.3 now would either require a large mapping/profile tranche first or risk turning per-job grouping into cross-job canonical authority prematurely.

Direction B therefore remains a high-value future destination, but **cross-job reviewed normalization is the missing bridge**. P2.2B-B2 is smaller, better grounded, directly supported by the accepted P2.2A architecture, and creates reusable semantic substrate that later P2.2C/P2.3/P2.4 can consume.

## 4. Why Direction C remains downstream

P2.4 Market v2 is defined to aggregate reviewed/current canonical mappings/profiles.

Today that reviewed canonical substrate is too sparse. Implementing Market v2 now would mostly repackage the existing deterministic Market profile plus bounded analytical report while adding little new reusable semantic authority.

Therefore:

```text
P2.2B-B2 reviewed correspondences
→ later P2.2C/P2.3 decision
→ later P2.4 Market v2
```

No automatic authorization is implied between these stages.

## 5. Reuse the accepted architecture

P2.2B-B2 uses existing owners:

```text
accepted/current English P1.6
→ CanonicalRegistryReviewReader
→ CanonicalRegistryService / CanonicalRegistryStore
→ reviewed responsibility concept
→ immutable exact claim mapping
```

Existing CLI already supports the required operations:

```text
jobhunter-registry claims list
jobhunter-registry concepts add
jobhunter-registry claims decide
jobhunter-registry concepts show
```

The CLI deliberately has no model-driven concept/alias acceptance path. The browser/CLI registry surfaces share the same underlying contract.

The accepted `RoleFamilyIntelligenceReport` and Work Intelligence may help identify **candidate** correspondences, but they are not promotion authority. Promotion evidence is the exact accepted/current P1.6 responsibility claim plus explicit human semantic review.

## 6. B2 evidence set

Use snapshot 15 only as the bounded **selection frame**. Canonical responsibility identity remains independent of the snapshot after review; every mapping still points to its exact P1.6 artifact/claim.

Review all 35 direct responsibility claims for boundary awareness, but begin with six high-evidence candidate correspondences that are already visible in exact accepted facts.

### Candidate R1 — design / implement AI agents

Strict initial pair:

```text
tvMm artifact 50 responsibility[0]
Designing and developing usable AI Agents in the product

tNVe artifact 56 responsibility[0]
include designing and implementing AI Agents and related workflows
```

Tentative canonical identity:

```text
responsibility:design-implement-ai-agents
preferred label: Design and implement AI agents
```

Boundary tests, not automatic members:

```text
tjgi responsibility[2]  Building applications, AI-based tools, and AI Agents
tmvA responsibility[3]  Design intelligent agents to perform various tasks across departments.
```

These broader claims must be reviewed independently; do not pull them into R1 merely because they mention agents.

### Candidate R2 — integrate AI systems with APIs / databases / internal services

Strict initial pair:

```text
tvMm responsibility[2]
Connecting Agents to tools, APIs, databases, and internal services

tNVe responsibility[2]
connecting LLMs to APIs, databases, and internal services
```

Tentative canonical identity:

```text
responsibility:integrate-ai-systems-with-services
preferred label: Integrate AI systems with APIs, data stores, and services
```

Boundary tests, not automatic members:

```text
tjgi responsibility[3]  Connecting AI models and services via API
tmvA responsibility[2]  Connect AI tools to CRM, email, and internal systems.
```

Preserve the difference between Agent/LLM/model/tool subject, generic API connection, and business-system integration.

### Candidate R3 — implement LLM Tool / Function Calling

```text
tvMm responsibility[3]
Implementing Tool Calling / Function Calling with LLMs

tNVe responsibility[3]
implementing Tool / Function Calling and Structured Output
```

Tentative canonical identity:

```text
responsibility:implement-llm-tool-calling
preferred label: Implement LLM tool/function calling
```

`Structured Output` is source-specific additional scope in `tNVe`; the canonical identity must not imply that every mapped claim includes structured output.

### Candidate R4 — develop RAG / knowledge retrieval systems

```text
tvMm responsibility[6]
Developing RAG and Knowledge-based systems

tNVe responsibility[4]
developing RAG and Knowledge Retrieval
```

Tentative canonical identity:

```text
responsibility:develop-rag-knowledge-retrieval
preferred label: Develop RAG and knowledge-retrieval systems
```

Do not silently equate all knowledge-based systems with RAG; preserve each exact claim.

### Candidate R5 — design / develop multi-step AI workflows

```text
tvMm responsibility[7]
Designing multi-step and reliable workflows

tNVe responsibility[5]
developing multi-step workflows, and if necessary, Multi-Agent Integration with Email, Ticketing, and other system modules
```

Tentative canonical identity:

```text
responsibility:design-develop-multi-step-ai-workflows
preferred label: Design and develop multi-step AI workflows
```

`reliable`, Multi-Agent integration, Email/Ticketing, and module-integration scope remain source-specific. They are not promoted into the canonical definition unless the reviewed reusable core truly requires them.

### Candidate R6 — evaluate and improve AI-system performance

Strict initial pair:

```text
tvMm responsibility[8]
Evaluating, debugging, and improving Agent performance

tNVe responsibility[7]
evaluating and improving the quality, reliability, latency, and cost of AI systems.
```

Tentative canonical identity:

```text
responsibility:evaluate-improve-ai-system-performance
preferred label: Evaluate and improve AI-system performance
```

Boundary case:

```text
tvMm responsibility[9]
Paying attention to cost, Latency, Reliability, and output quality.
```

Do not automatically map responsibility[9]. It expresses attention/quality concerns rather than the same explicit evaluate/improve action and is useful as a boundary test.

## 7. Promotion rule

A canonical responsibility in B2 may be created only when semantic review concludes that at least two exact accepted/current responsibility claims from distinct postings share the same reusable responsibility core strongly enough to justify one normalized correspondence.

This is a **normalization threshold**, not a market-prevalence threshold.

Review must preserve:

- exact source/P1.6 wording;
- exact artifact + responsibility index;
- source-specific object, technology, operating context and lifecycle scope;
- differences such as architecture vs implementation, evaluation vs monitoring, API integration vs broader internal-system integration;
- uncertainty when the reusable core is not clean.

Do not promote a concept merely because two claims share nouns such as `AI`, `Agent`, `API`, `RAG`, or `workflow`.

No universal quota requires all six candidates to pass. A valid B2 result may accept a subset or none.

## 8. Mapping semantics

For an accepted candidate:

```text
create/reuse canonical responsibility concept
→ map each explicitly reviewed exact responsibility claim
→ keep original P1.6 claim immutable and recoverable
```

Do not add aliases merely to duplicate claim wording. Add a reviewed alias only if it has independent lexical reuse value under the existing Registry contract.

Claims outside an accepted correspondence remain pending unless there is a specific reason to record `unmapped` or `rejected`. Do not mass-decide the remaining 35 claims for checklist completeness.

## 9. Deterministic versus semantic ownership

Human semantic review owns:

- whether two exact responsibilities represent the same normalized responsibility;
- canonical preferred label/definition/boundary;
- which exact claims map to the concept.

Deterministic application code owns:

- accepted/current claim eligibility;
- exact artifact/kind/index identity;
- concept/category validity;
- immutable mapping history;
- stale/current behavior;
- idempotent reuse;
- browser/CLI persistence views;
- SQLite integrity and public-corpus non-publication.

No LM call is required for B2 promotion. Model/report output may be consultation evidence only.

## 10. Execution sequence

### B2.1 — read-only evidence confirmation

On the maintainer database:

1. pull current `main`;
2. back up SQLite;
3. verify `PRAGMA integrity_check` / `foreign_key_check`;
4. list the exact current responsibility claims for `tvMm`, `tNVe`, `tjgi`, and `tmvA`;
5. confirm artifact IDs 50 / 56 / 60 / 61 and mapping states;
6. verify the existing Registry concept/mapping baseline before mutation.

If any selected P1.6 claim is no longer accepted/current, stop and re-evaluate that candidate. Do not silently substitute a newer/different claim.

### B2.2 — semantic review before mutation

Review R1-R6 one at a time.

For each candidate decide:

```text
ACCEPT correspondence
HOLD / too broad or ambiguous
REJECT candidate identity
```

Record why, especially for held/rejected boundary members.

### B2.3 — local Registry application

For ACCEPT only:

- create/reuse the reviewed `responsibility:*` concept using `jobhunter-registry concepts add`;
- map only the explicitly approved claims using `jobhunter-registry claims decide ... mapped`;
- add no unrelated concepts or mappings.

### B2.4 — verification

Prove:

- concept/mapping rows are exactly those approved;
- rerunning the same concept/mapping commands is idempotent;
- CLI current-claim views resolve the same exact mappings;
- browser Registry views show the same concepts, mappings and source wording;
- SQLite integrity is `ok` and foreign-key check empty;
- accepted P1.6 / Market snapshot artifacts are unchanged;
- `corpus/` remains unchanged because Registry publication remains unauthorized.

No new CI run is required solely for machine-local semantic data mutation if repository code is unchanged. If a real product/contract defect requires code changes, add the narrowest regression and run normal CI before continuing.

### B2.5 — disposition

Record a final B2 acceptance document containing:

- accepted concepts + exact mapped claims;
- held/rejected candidate correspondences and boundary reasons;
- local row IDs where useful;
- idempotency/integrity/browser/CLI evidence;
- explicit statement that B2 promotion is normalized correspondence, not a responsibility family or prevalence claim.

Then STOP and make a separate P2.2C/P2.3 readiness decision.

## 11. Acceptance gate

B2 passes for its bounded scope when:

```text
exact accepted-current inputs verified             PASS
semantic review precedes mutation                  PASS
only accepted correspondences promoted             PASS
exact source/P1.6 claims remain recoverable         PASS
canonical concept/mapping provenance correct        PASS
repeat application idempotent                       PASS
CLI/browser agree on reviewed state                 PASS
SQLite integrity/foreign keys                       PASS
Market/P1.6/public-corpus non-mutation              PASS
family/archetype/prevalence overclaim absent        PASS
```

There is no minimum number of accepted concepts required to force PASS. If no candidate correspondence survives review, close B2 as `NO-PROMOTION / DEFER` and preserve the evidence. Do not create another model/prompt retry loop merely to obtain mappings.

## 12. Stop lines

B2 does **not** authorize:

- P2.2C `ResponsibilityFamily` creation;
- P2.2D stable `RoleArchetype` creation;
- automatic promotion from Work Intelligence or RoleFamilyIntelligenceReport labels;
- bulk mapping of the 35 snapshot responsibilities;
- requirement canonicalization under this tranche;
- P2.3 capability-profile generation;
- P2.4 Market v2;
- Blueprint authority;
- personal readiness/gap/scoring;
- Registry/Work/Market publication to `corpus/`;
- a new semantic model or second review model;
- graph/vector/RAG/agent infrastructure.

## 13. Final direction disposition

```text
Direction A — SELECTED
  next: P2.2B-B2 selective responsibility normalization

Direction B — DEFERRED, NOT REJECTED
  reason: strong per-job Capability architecture but insufficient reviewed cross-job canonical relationship coverage for P2.3 authority

Direction C — DOWNSTREAM
  reason: Market v2 should aggregate reviewed canonical mappings/profiles rather than repackage current bounded interpretation

P2.2C responsibility families — NOT AUTHORIZED
P2.2D stable role archetypes — NOT AUTHORIZED
```

The next execution is B2.2 owner semantic review of R3-R6, following the approved and applied R1/R2 dispositions below. Reconfirm the baseline if dependencies/state change before mutation. No repository feature implementation should begin before that review exposes a concrete tooling gap.


## 14. R1 owner decision and execution repair — 2026-10-16

The owner approved `responsibility:design-implement-ai-agents`, label **Design and
implement AI agents**, definition **Designing AI agents and implementing their
behavior for use in an application or system.** Only `tvMm` artifact 50
responsibility[0] and `tNVe` artifact 56 responsibility[0] are approved mappings.
The broader `tjgi`/`tmvA` cases remain pending, with their original claims intact.

Before mutation, a SQLite-copy reproduction exposed a concrete Registry defect:
the current-artifact service selects accepted v23/v5 correctly, but the store's
write validator rejects it as not v30. The narrow repair admits the same accepted
v20/v21/v23/v28 compatibility contracts as the current P1.6 boundary, preserves
original artifact identity, and retains acceptance, schema, translation, exact
current dependency, category, and immutable review checks. No artifacts are
regenerated or automatically accepted. Regression coverage exercises every
compatible version across model identity, exact identity/idempotency, and
unsupported version/schema/pending rejection. Normal CI must pass before live R1
application. This is the tooling-gap exception authorized by B2, not a new layer.


### R1 application evidence and next review

The repair is committed at `dafdb05`; Ruff and **843 warnings-as-errors tests**
passed locally. Normal CI [38893557722](https://github.com/motafegh/jobhunter/actions/runs/38893557722)
passed before live mutation. A copy-only full rehearsal also passed.

Live R1 application used the existing `jobhunter-registry` CLI after a fresh
backup at `data/local-acceptance/b2-review-2026-10-16/pre-r1-live.sqlite3`.
Mapping #7 preserves artifact 50 / source version 47 / translation 41 / claim 0;
mapping #8 preserves artifact 56 / source version 56 / translation 48 / claim 0.
The Registry now contains five concepts and eight mappings; no alias was added.
Reapplying all three commands returned the identical concept/mapping rows,
including review metadata. Every table except `canonical_concepts`,
`job_claim_canonical_mappings`, and `sqlite_sequence` matched the pre-run rows.
Existing Registry rows were preserved. SQLite integrity is `ok`, foreign-key
violations are empty, and all corpus file hashes are unchanged.

The normal rendered concept and claim pages were checked through the browser
application on a post-update database copy and agreed with CLI/source identities.
This is rendered-route acceptance, not a new visual usability study. No network
acquisition or model generation occurred. Local backups/results remain ignored.

R1 boundary claims `tjgi` artifact 60 responsibility[2] and `tmvA` artifact 61
responsibility[3] remain pending. This is not whole-B2 closure or family authority.

**R2 proposal reviewed and approved by the owner on 2026-10-16; application evidence in §15:**

- ID: `responsibility:integrate-ai-systems-with-services`.
- Label: **Integrate AI systems with APIs, data stores, and services**.
- Definition: **Connecting AI agents or language models to APIs, databases, and internal services.**
- Exact proposed mappings: artifact 50 responsibility[2], “Connecting Agents to tools, APIs, databases, and internal services”; artifact 56 responsibility[2], “connecting LLMs to APIs, databases, and internal services”.
- Rationale: both explicitly connect an AI component to the same API/database/internal-service interfaces. Agent versus LLM subject remains visible in the original claim; tools are additional scope in the first claim.
- No authentication, deployment, architecture, ownership, or production guarantees are inferred.
- Boundary claims artifact 60 responsibility[3] (“Connecting AI models and services via API”) and artifact 61 responsibility[2] (“Connect AI tools to CRM, email, and internal systems.”) remain pending: neither asserts the complete shared interface scope of the proposed pair.

All four R2 claims were reconfirmed accepted/current and pending on 2026-10-16.
The owner subsequently approved this exact R2 proposal; §15 records its application.
R1 approval was not used as authorization for R2.


## 15. R2 approved application and R3 review — 2026-10-16

The owner approved the R2 proposal above. Applied through the existing Registry
CLI after rechecking exact current source/translation/artifact identities and
source wording. Fresh backup:
`data/local-acceptance/b2-review-2026-10-16/pre-r2-live.sqlite3`.

- Concept: `responsibility:integrate-ai-systems-with-services`.
- Label: **Integrate AI systems with APIs, data stores, and services**.
- Definition: **Connecting AI agents or language models to APIs, databases, and internal services.**
- Mapping #9: `tvMm` artifact 50 / source version 47 / translation 41 / responsibility[2].
- Mapping #10: `tNVe` artifact 56 / source version 56 / translation 48 / responsibility[2].

Registry totals are six concepts and ten mappings. Reapplying the concept and
both mappings preserved all rows and review metadata exactly. Only
`canonical_concepts`, `job_claim_canonical_mappings`, and their SQLite sequence
counters changed; all pre-existing Registry rows, every other table, and every
corpus file hash were preserved. No aliases were added. Integrity is `ok` and
foreign-key violations are empty. Rendered browser Registry concept/claim pages
on a post-update database copy agree with the CLI and original source wording.
Local result: `data/local-acceptance/b2-review-2026-10-16/r2-live-result.json`.

R2 boundary claims `tjgi` artifact 60 responsibility[3] and `tmvA` artifact 61
responsibility[2] remain pending. Four of the 35 snapshot-selected responsibility
claims are now mapped, and 31 remain pending. No source fetch, model generation,
code change, or full-suite rerun was needed for this data-only application.
Historical engineering evidence remains the 843 passing tests and successful CI
recorded in §14; these are not represented as newly executed R2 tests.

**R3 proposal, pending owner semantic review:**

- ID: `responsibility:implement-llm-tool-calling`.
- Label: **Implement LLM tool/function calling**.
- Definition: **Implementing tool calling or function calling for language-model-based systems.**
- Proposed pair: `tvMm` artifact 50 responsibility[3], “Implementing Tool Calling / Function Calling with LLMs”; `tNVe` artifact 56 responsibility[3], “implementing Tool / Function Calling and Structured Output”.
- Both assert implementation of tool/function calling. The second posting's title and description establish its LLM application context; the original claim remains exact. Structured Output is additional scope only in `tNVe` and is not part of the shared definition.
- This correspondence does not assert a shared framework, autonomous execution, permission model, or deployment responsibility. R2's general service integration remains a separate correspondence.

Both R3 claims were reconfirmed accepted/current and pending, with exact source
versions 47/56 and translations 41/48. No R3 concept or mappings have been
created. Owner review of this exact proposal is the next promotion gate.
