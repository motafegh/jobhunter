# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-09-29  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Active branch:** `main`  
**Current product gate:** MARKET I1-I7 ACCEPTED / BOUNDED FIRST SLICE CLOSED  
**Current English P1.6:** `job-analysis-english-v30 / job-analysis-v5`; accepted v20/v21/v23/v28 v5 artifacts remain accepted-only compatibility inputs when exact dependencies match.  
**Current public corpus:** 420 jobs / 51 parsed details / 29 English projections / 11 accepted English P1.6 / 5 Capability artifacts.  
**LM Studio maintainer endpoint:** `http://127.0.0.1:18080/v1`; fresh-clone `Settings` default remains port 1234.  
**Active increment:** Market candidate interpretation V3.3 / contract v6. V5 completed safely but over-filtered all work/role candidates because declared internal `C*` citation syntax was treated as a semantic rejection. V6 deterministically normalizes declared compact citations while keeping undeclared compact refs and source/evidence mismatches as rejection conditions. One final snapshot-15 rerun remains before disposition.  
**Parallel portfolio:** MIT complete; GitHub metadata + screenshots + release + owner mastery pending.

This file is intentionally current-frontier oriented. Detailed historical execution belongs in dated records under `docs/working-memory/`.

## 1. Read this first

Authority and stable context:

1. `AGENTS.md`
2. `README.md`
3. `docs/PRODUCT_SPECIFICATION.md`
4. `docs/ARCHITECTURE.md`
5. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
6. `docs/SOURCE_POLICY.md`
7. `docs/UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md`
8. `docs/ROADMAP.md`
9. `docs/IMPLEMENTATION_PLAN.md`
10. `docs/CURRENT_STATE_RECONCILIATION_2026-09-12.md`
11. `docs/MARKET_ROLE_FAMILY_INTELLIGENCE_PLAN.md`
12. `docs/EXECUTION_TODO.md`

Current focused record:

`docs/working-memory/2026-09-29_MARKET_CANDIDATE_INTERPRETATION_V1.md`

Accepted Market closure records:

- `docs/working-memory/2026-09-26_MARKET_I7_FINAL_LOCAL_ACCEPTANCE.md`
- `docs/working-memory/2026-09-26_MARKET_I7_TARGET_COVERAGE_FOLLOWUP.md`

Do not follow older I7 HOLD, v20/v21/v22 retry, or open-B1 instructions when they conflict with current owners.

---

## 2. Current accepted product state

```text
Phase 1                              CLOSED / ACCEPTED
P2.1 Canonical Registry             CLOSED / ACCEPTED
P2.2A Job Work Intelligence         CLOSED / ACCEPTED
P2.2B-B1                            CLOSED / NO-PROMOTION / DEFER
Blueprint v6                        EXPERIMENTAL / NON-AUTHORITATIVE

Market foundation                   PASS / COMPLETE
Market I1                           ACCEPTED
Market I2                           ACCEPTED
Market I3                           ACCEPTED
Market I4                           ACCEPTED
Market I5                           ACCEPTED
Market I6                           ACCEPTED
Market I7                           PASS / CLOSED FOR BOUNDED SCOPE
Same-target coverage follow-up      COMPLETE
Candidate interpretation v6         ACTIVE FINAL RE-EVALUATION / NON-PROMOTIONAL
Market → You                        LATER / NOT AUTHORIZED
```

Current primary contracts:

```text
parser                         jobinja-detail-v2
translation                    lm-studio-translation-v2
English projection             english-projection-v2
English P1.6 generation         job-analysis-english-v30 / job-analysis-v5
Original P1.6                   job-analysis-original-v9 / job-analysis-v4
Capability                     job-capability-intelligence-v9 / job-capability-intelligence-v5
Canonical Registry             jobhunter-canonical-concept-registry-v1
Job Work Intelligence          job-work-intelligence-v2 / job-work-intelligence-v2.0
Market membership              market-membership-v1 / market-membership-v1.0
Market snapshot                market-corpus-snapshot-v1
Market aggregate               market-aggregate-profile-v1
Public Corpus                  jobhunter-public-corpus-v1
Candidate report               market-role-family-candidate-v6
```

Accepted-only historical P1.6 compatibility does not relabel old artifacts. Exact prompt/schema/dependency identity remains visible.

---

## 3. Frozen Market first-slice rules

```text
source = Jobinja only
search/acquisition envelope != target membership truth
membership = core_match | adjacent_match | uncertain | excluded
primary source corpus = core_match only
accepted P1.6 is not required for source-level membership
accepted-current P1.6 is required for strong semantic prevalence
pending/missing/failed/rejected P1.6 != zero demand
Capability/Work optional, not gates
repost/new-ID collapse deferred
use "qualified source postings", not "unique demand units"
Market state local/private by default
```

Accepted sequence:

```text
I1 domain + persistence
→ I2 target-scoped affected work
→ I3 membership qualification
→ I4 immutable snapshot
→ I5 deterministic aggregate profile
→ I6 shared browser/CLI workflow
→ I7 bounded real-local acceptance
→ same-target coverage follow-up
```

Snapshots 14-15 contain ten qualified members, six core postings and six accepted-semantic core postings. The unchanged rerun reused the same member and analysis identities.

---

## 4. Active increment — Market candidate interpretation V3.3 / contract v6

Purpose:

Turn one frozen Market snapshot into a bounded, evidence-linked interpretation of recurring work and possible role subfamilies without converting model prose into employer fact or promoted taxonomy.

Implementation:

- `src/jobhunter/market_candidate_report.py`
- `src/jobhunter/market_cli.py`
- `src/jobhunter/web/market_workspace.py`
- `src/jobhunter/web/templates/market_candidate_report.html`

Authority boundary:

```text
accepted exact P1.6 evidence
→ model proposes bounded interpretation
→ application validates citations and computes counts
→ user reviews usefulness
→ no taxonomy promotion from generation alone
```

Snapshot 15 input:

```text
accepted-semantic core postings: 6
responsibility claims:            35
requirement claims:              140
```

The v6 report:

- consumes only included core members with accepted exact-identity P1.6;
- treats responsibilities as primary work evidence and requirements as specialty/qualification context rather than inferred duties;
- requires every overall observation, interpretation point, and alternative to carry exact supplied evidence refs;
- never renders internal compact `C*` IDs: IDs already declared by the same item's `evidence_refs` are normalized away before presentation;
- rejects an undeclared compact ID as a semantic citation inconsistency;
- rejects a source-alias mention when that same interpretation does not cite evidence from the source;
- omits only genuinely unsafe generated elements and records a path/code integrity diagnostic; if no safe interpretation survives, the whole report fails;
- withholds employer names and job titles from model input;
- derives distinct support, available-vs-cited evidence counts, confidence caps, and responsibility/requirement evidence basis in application code;
- separates one-posting role candidates into specialty/outlier candidates instead of presenting them as multi-posting subfamilies;
- keeps jobs with no extracted responsibilities visible as a coverage limitation;
- resolves internal source aliases before user presentation;
- remains ephemeral in CLI/browser memory and does not create Market/report tables or corpus artifacts.

Real bounded evidence:

- Gemma completed in about 1m29s and produced a conservative report.
- MiMo completed in about 8m45s, surfaced additional niche/speech-audio interpretation, but also emitted unsupported caveats.
- Browser rendering completed successfully with source/evidence drill-down.
- These outputs remain candidate evidence only.

Current acceptance state:

1. owner usefulness review of the captured v3 report is complete: the synthesis was useful, but v3 was not strong enough to persist;
2. V4 real-model rerun on 2026-09-30 failed safely on `source_alias_without_matching_evidence`; no report was cached;
3. V5 real-model rerun completed and was captured, but 17 declared-compact-citation violations removed every work cluster and role-subfamily candidate;
4. V3.3 is implemented under new v6/prompt-v6 identities with deterministic normalization of declared compact citations and rejection of undeclared ones;
5. dedicated regression coverage is present in `tests/test_market_candidate_report.py`;
6. CI run `37139118186` passed Ruff, 817 tests, and 817 warnings-as-errors tests;
7. one final real-model/browser snapshot-15 rerun under v6 is required before report disposition;
8. no decision has been made to persist/version reports;
9. no responsibility family or role subfamily is promoted from this sample.

---

## 5. Exact continuation sequence

```text
A. Pull/restart current main on the maintainer machine

B. Regenerate snapshot 15 under candidate v6
   - same accepted snapshot input
   - default Gemma analysis model
   - browser route must render successfully

C. Capture the v4 rendered report as review evidence

D. Compare directly with the recorded v3 defects
   - no duplicate overall support display
   - available evidence != cited evidence is labeled correctly
   - no internal C* IDs in prose
   - every source-specific observation has source-bound evidence
   - alternatives are evidence-bound
   - requirement-only specialty is explicit, not inferred work
   - one-posting role candidates are not shown as reusable subfamilies
   - role-subfamily section adds value beyond renamed work clusters

E. Make explicit disposition
   - keep ephemeral; or
   - authorize a separately versioned persisted RoleFamilyIntelligenceReport

F. Then continue broader Phase-2 semantics
   - representative responsibility families / role archetypes
   - JobCapabilityRequirementProfile
```

Do not skip directly from one six-posting candidate report to promoted taxonomy.

---

## 6. Current stop lines

Do not currently:

- reopen B1 or accepted Market I1-I7 without a repeatable contradiction;
- regenerate accepted anchors merely because v30 is current;
- auto-accept P1.6;
- make Capability or Work mandatory Market gates;
- claim broad-market prevalence or trends from snapshot 15;
- promote responsibility families / stable role archetypes from the current candidate report;
- implement automatic repost/new-ID collapse without evidence;
- begin Market → You / readiness scoring before reviewed personal evidence exists;
- publish private Market state into `corpus/`;
- add graph/vector/RAG/agent infrastructure without demonstrated need.

Interpretive uncertainty should fail soft; integrity/provenance violations should fail hard.

---

## 7. Historical records

Historical detail remains available in dated working-memory and experiment records rather than this rolling handoff.

Important historical pointers:

- B1 closure: `docs/working-memory/2026-09-14_P2_2B_B1_EXTRACTION_RECOVERY.md`
- Market foundation: `docs/working-memory/2026-09-14_MARKET_ROLE_FAMILY_FOUNDATION_INVESTIGATION_DECISION.md`
- I6 implementation: `docs/working-memory/2026-09-17_MARKET_I6_BROWSER_CLI_WORKFLOW_IMPLEMENTATION.md`
- I7 protocol: `docs/working-memory/2026-09-18_MARKET_I7_LOCAL_ACCEPTANCE_PROTOCOL.md`
- historical I7 HOLD: `docs/working-memory/2026-09-18_MARKET_I7_REAL_LOCAL_ACCEPTANCE_HOLD.md`
- final I7 PASS: `docs/working-memory/2026-09-26_MARKET_I7_FINAL_LOCAL_ACCEPTANCE.md`
- coverage follow-up: `docs/working-memory/2026-09-26_MARKET_I7_TARGET_COVERAGE_FOLLOWUP.md`
- candidate interpretation: `docs/working-memory/2026-09-29_MARKET_CANDIDATE_INTERPRETATION_V1.md`

Historical HOLD-era wording is evidence, not current routing.

---

## 8. Parallel portfolio/release

Still pending:

```text
GitHub description/topics
real browser screenshots + privacy review
intentional v0.1.0 tag/release
owner mastery verification
```

These do not alter the active Market interpretation acceptance boundary.
