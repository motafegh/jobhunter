# Market and Role-Family Intelligence — Planning Decision

**Date:** 2026-09-06  
**Status:** OWNER INTENT CONFIRMED / PLAN RECORDED / IMPLEMENTATION GATED  
**Branch:** `main`  
**Controlling future-focused plan:** `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`

## 1. Owner intent

The owner wants JobHunter to support a repeated-use workflow in which the user defines a target job category / role family / market slice and JobHunter:

```text
defines the target
→ updates/discovers current relevant job advertisements
→ fetches/refreshes required details
→ performs/reuses the required analysis/extraction
→ determines which postings genuinely belong to the requested market
→ aggregates the evidence across the qualified corpus
→ produces ONE current market/role-family intelligence report
```

The desired output is explicitly **not one generated report per vacancy**. Individual vacancies remain supporting evidence and drill-down material for one aggregate report.

The report should help answer, across the target market:

- what responsibilities recur;
- what requirements recur;
- what is required versus preferred/contextual/inferred;
- which skills/capabilities, tools/platforms, practices and knowledge areas recur;
- what experience/seniority/education/credential patterns appear;
- what role subfamilies or work patterns appear across inconsistent titles;
- what is common versus specialized;
- later, what actually changes over time;
- later, how the objective market compares with reviewed personal evidence.

## 2. Agreed product refinements

The planning discussion added the following professional refinements to the original feature idea:

1. use an aggregate **Role-Family Intelligence Report** / Market Brief rather than generic per-job summaries;
2. preserve raw posting counts/shares and requirement-strength distribution;
3. distinguish tools from applied capabilities where evidence permits;
4. distinguish exact source responsibilities from normalized/promoted responsibilities and candidate analytical work families;
5. support candidate role subfamilies based primarily on recurring work/responsibilities/capability expectations rather than titles alone;
6. expose distinct-employer support and employer-concentration warnings;
7. address repost/near-duplicate inflation before making strong prevalence/trend claims;
8. preserve a versioned target/corpus/report snapshot for historical comparison;
9. treat `emerging` as a longitudinal signal, not merely a rare current item;
10. build the objective market report first and keep later `Market → You` comparison as a separate personal-evidence-dependent layer.

## 3. Initial architecture mapping

The desired capability fits the existing modular monolith and should extend existing foundations rather than create a parallel analysis stack.

Relevant existing owners include:

```text
Acquisition / update
- src/jobhunter/search_registry.py
- src/jobhunter/jobinja_discovery.py
- src/jobhunter/jobinja_sync.py
- src/jobhunter/jobinja_batch.py
- src/jobhunter/phase1_run.py

Factual semantic substrate
- English projection v2
- English P1.6 v20/v5
- src/jobhunter/analysis_store.py

Per-job interpretation
- Capability Intelligence v9
- Job Work Intelligence v2

Reviewed normalization
- Canonical Registry v1

Current aggregate/report
- src/jobhunter/market_insights.py
- src/jobhunter/phase1_report.py
- browser Market/report surfaces
```

Current Market already deterministically aggregates accepted/current P1.6 requirement concepts and requirement strength, reports analyzed sample size/distinct-employer concentration, and discloses its source/filter/duplicate scope.

Important known limitation to investigate later:

```text
repost / cross-post near-duplicate adjustment is not implemented
```

## 4. Authority decisions

The new capability must retain the existing authority ladder:

```text
SOURCE FACT
→ NORMALIZED CORRESPONDENCE
→ ANALYTICAL INTERPRETATION
→ RECOMMENDATION / DECISION SYNTHESIS
```

Agreed consequences:

- source/job/version/currentness and numeric aggregation remain deterministic;
- model reasoning may help with relevance qualification, candidate work grouping, candidate role subfamilies and narrative synthesis;
- model output must not manufacture prevalence/counts;
- candidate role/work interpretation does not require automatic canonical promotion;
- reusable stable families/archetypes/canonical Market authority require the appropriate stronger promotion boundary;
- personal evidence is not mixed into the objective market report.

## 5. Current gate interaction

The repository's current product frontier remains P2.2B-B1.

Current exact next product action is still:

```text
ta9l current English projection
→ ta9l English P1.6 v20 generation + semantic review
→ exact responsibility-shape report
→ comparison with tG9K P1.6 36 responsibility[5]
→ possible one-concept/two-mapping registry mutation
→ B1 closure decision
```

Existing governance explicitly says not to start Market v2 during B1.

Therefore this planning decision authorizes:

- recording the product intent;
- recording the focused plan;
- recording future investigation requirements;
- recording rolling state pointers.

It does **not** authorize:

- Market-v2 source implementation;
- responsibility-family/archetype implementation;
- corpus-wide Market experiments that bypass B1;
- personal readiness/gap/scoring;
- speculative new infrastructure.

## 6. Formal investigation queued after activation

After B1 closes and the owner explicitly activates this plan, perform the bounded investigation defined in `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md` before source implementation.

The investigation must resolve at minimum:

```text
target-market definition
acquisition/orchestration reuse
corpus currentness/membership
semantic relevance qualification
P1.6 sufficiency
Capability reuse boundary
Work Intelligence reuse boundary
Canonical Registry dependency
responsibility-family/archetype dependency
repost/near-duplicate handling
sample/employer-concentration policy
temporal snapshot comparability
persistence/artifact model
browser/CLI workflow
incremental/model-call budget
publication/privacy boundary
representative test/acceptance corpus
```

Do not pre-decide these contracts merely to begin coding faster. Also do not over-investigate them beyond what is needed to authorize the first useful vertical slice.

## 7. Progressive documentation rule

For this responsibility:

```text
focused durable decisions
→ update docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md when needed

current handoff state
→ update docs/WORKING_MEMORY.md

currently authorized executable tasks
→ update docs/EXECUTION_TODO.md

meaningful evidence/decision transitions
→ add dated docs/working-memory/... record

bounded semantic/model experiments
→ docs/experiments/ when preservation is useful
```

Do not broad-rewrite master product/architecture/roadmap documents until an implemented/accepted durable contract actually changes them.

## 8. Exact current state

```text
feature intent             CONFIRMED
focused plan               RECORDED
initial architecture fit   CONFIRMED
formal implementation audit QUEUED / NOT STARTED
source implementation      NOT AUTHORIZED
current product frontier   P2.2B-B1 / ta9l P1.6 gate
```

## 9. Exact next action for this track

```text
wait for P2.2B-B1 closure
→ owner explicitly activates Market/role-family plan
→ perform the plan's foundation investigation
→ write a dated investigation/decision record
→ amend plan if evidence requires it
→ authorize first bounded implementation slice
```
