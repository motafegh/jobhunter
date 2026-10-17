# JobHunter Current-State Reconciliation — 2026-10-10

**Status:** CURRENT / CONTROLLING STATUS-ONLY OVERLAY  
**Date:** 2026-10-10
**Last reconciled:** 2026-10-17
**Branch:** `main`  
**Scope:** Present-tense project state and execution routing.  
**Supersedes for current-state reading:** `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`

This file changes present-tense status/routing only. It does not replace durable product, domain, source, architecture, roadmap, implementation-plan, or phase-plan semantics.

## 1. Current operating state

```text
Phase 1                              CLOSED / ACCEPTED
P2.1 Canonical Registry             CLOSED / ACCEPTED
P2.2A Job Work Intelligence         CLOSED / ACCEPTED
P2.2B-B1                            CLOSED / NO-PROMOTION / DEFER
P2.2B-B2 selective normalization    ACTIVE / AUTHORIZED
P2.2C responsibility families       NOT AUTHORIZED
P2.2D stable role archetypes        NOT AUTHORIZED
P2.3 capability profiles            DEFERRED / NOT AUTHORIZED
P2.4 Market v2                      DOWNSTREAM / NOT AUTHORIZED
Blueprint v6                        EXPERIMENTAL / NON-AUTHORITATIVE

Market foundation                   PASS / COMPLETE
Market I1-I7                        ACCEPTED / CLOSED FOR BOUNDED SCOPE
Same-target coverage follow-up      COMPLETE
Candidate interpretation v6         ACCEPTED / CLOSED FOR BOUNDED REPORTING
RoleFamilyIntelligenceReport R1-R4  ACCEPTED / CLOSED
Market → You                        LATER / NOT AUTHORIZED

Portfolio / release                 PARALLEL
MIT license                         COMPLETE
metadata/screenshots/release/mastery PENDING
```

Current committed public-corpus baseline after the 2026-10-17 `tNpG` publication:

```text
known/discovered Jobinja jobs       420
fetched/parsed detail jobs           52
current English projections          30
accepted/current English P1.6        11
accepted/current Capability            5
```

The `tNpG` publication adds current source/detail and English-projection material only. It does not add accepted P1.6, Capability, Registry mappings, or Market authority.

## 2. Current exact semantic decision

Controlling direction decision:

`docs/working-memory/2026-10-10_PHASE2_SEMANTIC_DIRECTION_RECONCILIATION_DECISION.md`

Bounded semantic-decision records:

- `docs/working-memory/2026-10-17_P2_2B_B2_R3_SEMANTIC_DECISION.md`
- `docs/working-memory/2026-10-17_P2_2B_B2_R4_R6_SEMANTIC_DECISIONS.md`

Direction result:

```text
Direction A — responsibilities/correspondence     SELECTED
Direction B — capability profiles                 DEFERRED, NOT REJECTED
Direction C — Market v2                           DOWNSTREAM
```

The current bounded tranche is **P2.2B-B2 snapshot-15 selective responsibility normalization**.

B2 is not P2.2C. It creates only reviewed normalized responsibility correspondences through the existing P2.1 Canonical Registry when exact accepted/current P1.6 claims survive semantic review.

## 3. Evidence change since B1

B1 did not prove the proposed responsibility correspondence invalid. It stopped because the selected second job lacked an acceptable/current P1.6 artifact.

Snapshot 15 supplies:

```text
accepted-semantic core postings       6
accepted responsibility claims       35
postings with direct responsibilities 4
postings with zero responsibilities   2
```

Direct-work accepted artifacts:

```text
tvMm  artifact 50  11 responsibilities
tmvA  artifact 61   7 responsibilities
tjgi  artifact 60   9 responsibilities
tNVe  artifact 56   8 responsibilities
```

`t7ck` and `t7Ay` remain valid accepted-semantic Market evidence but have no direct responsibilities and cannot create responsibility facts from requirement-only evidence.

## 4. B2 candidate review state

The bounded R1-R6 semantic review is now complete. Review does not itself prove local Registry application.

```text
R1  AI-agent design / implementation
    ACCEPTED / APPLIED / VERIFIED 2026-10-16
    concept: responsibility:design-implement-ai-agents
    mappings: artifact 50 responsibility[0], artifact 56 responsibility[0]

R2  AI-system integration with APIs / databases / services
    ACCEPTED / APPLIED / VERIFIED 2026-10-16
    concept: responsibility:integrate-ai-systems-with-services
    mappings: artifact 50 responsibility[2], artifact 56 responsibility[2]

R3  LLM Tool / Function Calling implementation
    ACCEPTED 2026-10-17 / LOCAL APPLICATION + VERIFICATION PENDING
    concept: responsibility:implement-llm-tool-calling
    approved mappings: artifact 50 responsibility[3], artifact 56 responsibility[3]

R4  RAG development
    ACCEPTED 2026-10-17 / LOCAL APPLICATION + VERIFICATION PENDING
    concept: responsibility:develop-rag-systems
    approved mappings: artifact 50 responsibility[6], artifact 56 responsibility[4]

R5  multi-step AI workflow design/development
    ACCEPTED 2026-10-17 / LOCAL APPLICATION + VERIFICATION PENDING
    concept: responsibility:design-develop-multi-step-ai-workflows
    approved mappings: artifact 50 responsibility[7], artifact 56 responsibility[5]

R6  AI-system performance evaluation/improvement
    ACCEPTED 2026-10-17 / LOCAL APPLICATION + VERIFICATION PENDING
    concept: responsibility:evaluate-improve-ai-system-performance
    approved mappings: artifact 50 responsibility[8], artifact 56 responsibility[7]
```

R3 preserves `Structured Output` as source-specific extra scope rather than part of the normalized definition.

R4 deliberately narrows the original tentative identity: both claims explicitly share **RAG development**, while `Knowledge-based systems` and `Knowledge Retrieval` are not equivalent. The accepted concept is therefore `responsibility:develop-rag-systems`; each source-specific knowledge phrase remains exact in its original claim.

R5 normalizes only multi-step AI/agent workflow design/development. `reliable` remains specific to `tvMm`; Multi-Agent, Email, Ticketing, and module-integration scope remains specific to `tNVe`.

R6 normalizes explicit evaluation/improvement of AI/agent-system performance. `debugging` remains specific to `tvMm`; quality/reliability/latency/cost remain explicit `tNVe` dimensions. `tvMm` artifact 50 responsibility[9] remains pending because “paying attention to” those qualities is not the same evaluate/improve action.

Four of the 35 selected responsibilities are currently proven mapped in the local Registry from R1/R2; 31 remain pending until R3-R6 are actually applied to the maintainer SQLite database. If all eight approved R3-R6 claims remain accepted/current and pending, successful application would be expected to produce 12/35 mapped and 23 pending. That expected state is not current authority until local verification proves it.

## 5. Current architecture rule

Reuse existing accepted owners:

```text
accepted/current P1.6 factual responsibility
→ explicit semantic correspondence review
→ jobhunter-canonical-concept-registry-v1
→ reviewed responsibility concept
→ immutable exact claim mapping
```

Do not create another canonical concept system or model-driven promotion path.

Work Intelligence / RoleFamilyIntelligenceReport may identify candidate patterns but remain analytical interpretation; they do not authorize canonical mappings.

The R1 execution exposed one narrow Registry write-validator defect: accepted-compatible historical English P1.6 artifacts selected by the currentness policy could be rejected by persistence. Commit `dafdb05` aligned Registry persistence with the accepted v20/v21/v23/v28/v30 v5 compatibility boundary while preserving exact artifact identity, semantic acceptance, source/translation dependencies, schema checks, and immutable review behavior. This repair is complete; it did not create a new semantic layer.

## 6. B2 exact execution sequence

```text
B2.1 read-only local baseline COMPLETE (2026-10-15)
  → backup / integrity / foreign keys
  → exact current tvMm/tNVe/tjgi/tmvA responsibility claims confirmed
  → Registry baseline confirmed

B2.2 semantic review COMPLETE
  → R1-R6 reviewed individually
  → R1/R2 accepted/applied/verified
  → R3-R6 accepted semantically; local application/verification pending

B2.3 local application ACTIVE
  → pull current main and back up SQLite
  → reconfirm all eight R3-R6 claims are still accepted/current and pending
  → create/reuse only the four accepted R3-R6 responsibility concepts
  → map only the eight explicitly approved exact claims
  → add no aliases
  → leave tvMm 50[9] and broader R1/R2 boundaries pending

B2.4 proof
  → rerun/idempotency
  → CLI/browser same reviewed state
  → SQLite integrity / foreign keys
  → R1/R2 and unrelated Registry rows unchanged
  → accepted P1.6 and Market identities unchanged
  → Registry remains local/private; public-corpus publication remains separate

B2.5 disposition
  → record exact applied row identities + held/pending boundaries
  → close B2 for the bounded six-candidate tranche
  → STOP
  → separate P2.2C vs P2.3 readiness decision
```

## 7. Current non-authorizations

Do not during B2:

- create `ResponsibilityFamily` entities;
- create stable `RoleArchetype` entities;
- auto-promote Work/report labels;
- bulk-map all snapshot claims;
- canonicalize requirements in this tranche;
- build P2.3 profiles;
- build P2.4 Market v2;
- use Blueprint as authority;
- start personal readiness/gap/scoring;
- publish Registry/Market/Work private state into `corpus/`;
- add new semantic models or model-review loops merely to obtain promotion.

## 8. Current exact next action

```text
R1/R2 applied and verified
R3-R6 semantic correspondences accepted
→ semantic review stage COMPLETE
→ apply the accepted R3-R6 batch to the maintainer local SQLite database
→ exact concepts/mappings/commands are fixed in the 2026-10-17 R4-R6 decision record
→ prove idempotency, CLI/browser agreement, integrity/FK and preservation boundaries
→ record final B2 disposition
→ STOP and make a separate P2.2C-vs-P2.3 readiness decision
```

The exact combined application commands and verification boundary are fixed in `docs/working-memory/2026-10-17_P2_2B_B2_R4_R6_SEMANTIC_DECISIONS.md`. This repository session cannot claim the local Registry rows exist because the runtime SQLite database is intentionally local and excluded from GitHub.

The latest repository also intentionally publishes the previously local `tNpG` source/detail + English projection. That corpus publication is independent of B2 and does not change the local Registry application boundary.
