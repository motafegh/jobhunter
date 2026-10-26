# B2 closure and bounded capability comparison — 2026-10-26

**Status:** B2 CLOSED / ACCEPTED FOR SIX-CANDIDATE SCOPE; P2.3A-0 EVALUATION AND BOUNDED BROWSER SLICE AUTHORIZED
**Authority:** Following the independent project-state review, the owner explicitly approved all three recommended steps: reconcile B2 closure, evaluate existing composition options, and build/verify a bounded capability-understanding/comparison browser view.
**Predecessors:** the October 10 B2 direction decision, October 17 R3/R4–R6 decisions, and the post-B2 readiness and technical reuse audits.
**Scope:** Job-level, read-only understanding of existing accepted/current facts, optional current Capability-v9 organization, and reviewed Registry correspondences. No new inference, taxonomy promotion, persistent profile schema, or Market-v2 authority.

## 1. Proven B2 state

The local R3–R6 application already occurred on October 20. The October 26 review did not repeat a production mutation.

| Candidate | Concept suffix under `responsibility:` | Exact artifact claims | Mapping rows |
|---|---|---|---|
| R1 | design-implement-ai-agents | 50[0], 56[0] | 7, 8 |
| R2 | integrate-ai-systems-with-services | 50[2], 56[2] | 9, 10 |
| R3 | implement-llm-tool-calling | 50[3], 56[3] | 11, 12 |
| R4 | develop-rag-systems | 50[6], 56[4] | 13, 14 |
| R5 | design-develop-multi-step-ai-workflows | 50[7], 56[5] | 15, 16 |
| R6 | evaluate-improve-ai-system-performance | 50[8], 56[7] | 17, 18 |

Artifact 50 is `tvMm`; artifact 56 is `tNVe`. The accepted/current source and translation dependencies remain exact. All 35 selected responsibility claims were reconciled through the current Registry reader: **12 mapped, 23 pending**. Artifact 50 responsibility[9] and the broader R1/R2 boundaries remain pending. No R3–R6 aliases were added.

Local Registry totals are ten concepts, eighteen immutable claim decisions, and one pre-existing alias. The eighteen decisions include the original six P2.1 decisions, one of which is explicitly unmapped; they must not be described as eighteen mapped responsibilities.

## 2. Closure proof and limits

Comparison with the retained October 20 pre-R3–R6 SQLite backup proves:

- exactly four concepts and eight mappings were added; no prior Registry rows were removed or changed;
- only those Registry tables and SQLite sequence bookkeeping differ;
- source, translation, P1.6, Capability, Work, and all Market tables are unchanged;
- SQLite integrity is `ok`; foreign-key violations are empty;
- replaying all four concepts and eight decisions through the existing CLI on a fresh database copy changes no rows;
- rendered concept and responsibility-queue pages agree with the current reader and CLI on the exact source wording;
- public-corpus verification passes for all 420 jobs;
- production database and corpus hashes remain unchanged by the audit.

Browser proof here means rendered HTTP responses through TestClient over a copy of real local data. It is not an interactive visual review. The unchanged repository head passed 868 tests with warnings as errors, Ruff, and dependency consistency before closure.

Machine-local evidence remains ignored under `data/local-acceptance/project-state-2026-10-26/`: `summary.json`, `registry-cli.txt`, `corpus-verification.txt`, the audit script, and verification copies. They are neither public-corpus inputs nor committed database backups. The first audit harness comparison mixed SQLite row objects and tuples; that harness issue was corrected and the successful run used a fresh copy. It was not a product idempotency failure.

**Disposition:** B2 is closed and accepted for its six reviewed candidates. Reviewed correspondence is not a ResponsibilityFamily, stable role archetype, or prevalence claim. The 23 pending responsibilities are valid facts, not unfinished obligations to bulk-map.

## 3. P2.3A-0 execution and findings

The existing experiment was executed on the verified database copy, with zero model or source calls and no new durable profile state. Target jobs and older anchors were evaluated separately.

| Evidence set | Strategy A | Strategy B |
|---|---|---|
| Six snapshot-15 jobs | 175 exact claims; 175 buckets; 12 mapped responsibilities; 0/140 requirements mapped | Unavailable on all six: no eligible accepted public Capability-v9 artifact |
| Five accepted heterogeneous anchors | 108 exact claims; 108 buckets | 22 job-local groups cover 98 distinct claims; ten claims remain explicitly outside groups |

The anchor overlay contains 35 repeated memberships across groups. Consequently `exact_partition_ok` is false on all five anchors. The existing measurements are retained unchanged. Work-activity boundary checks pass, including the requirement-only anchors. The zero-availability target Strategy-B checks remain null, not passing.

This does not prove Strategy B wrong under the accepted Capability contract: a source claim may support several job-local capability areas. It does mean **the overlay is unsuitable as a disjoint partition or an additive demand denominator**. Group membership must not inflate distinct claim counts. No existing Capability artifact or evaluator threshold is rewritten to manufacture a pass.

Direct inspection supports a narrower design choice: accepted Capability labels help navigate already-reviewed anchor evidence, while Strategy A supplies complete exact facts. Neither result establishes measured user time savings, six-target-job semantic grouping, canonical capability equivalence, or readiness for persistent P2.3 profiles.

Retained local outputs: `p23-target-six.json` and `p23-anchor-five.json`. They contain different evidence sets; they must not be presented as a matched A/B comparison across the six target jobs.

## 4. Authorized browser increment

Implement a small current-evidence comparison view for up to three selected jobs:

1. Show role/company and the availability of accepted/current English P1.6.
2. Let the user find capability wording across the selected jobs without manually navigating separate complete documents.
3. Keep requirements, obligation, explicit depth, and actual responsibilities separate; preserve exact excerpts and evidence on demand.
4. Attach reviewed Registry correspondence only to the exact mapped claims. Unmapped claims remain usable.
5. Reuse existing current Capability-v9 organization opportunistically, with exact dependency validation and job-local interpretation labels. Keep overlapping support visible and count each factual claim once.
6. Preserve a complete factual fallback when Capability is absent. A lexical match is a reading aid, never a canonical equivalence claim.
7. Expose no-match, missing/pending/stale accepted analysis, requirement-only, and unknown scope honestly.
8. Provide local navigation into source evidence and preserve validated originating Market context when supplied.

Runtime data comes from SQLite through existing owners. The browser must not start reading `corpus/` as a runtime database. Any shared extraction from the experimental composer is limited to the concrete second consumer and keeps the original public experiment available for replay.

## 5. Verification and stop lines

Prove currentness, exact dependencies, factual recovery, no duty fabrication, no count inflation from overlapping groups, read-only GET behavior, escaping, bounded selection, and safe origin handling. Exercise real local evidence at desktop and narrow width, keyboard navigation, and source drill-down. Run normal engineering gates after implementation.

Record observed comprehension improvements as structural/navigation observations unless the owner actually measures repeated-use effort. Do not invent timing, semantic acceptance, or product acceptance from green tests.

This authorization does not include Strategy-C model generation, Capability regeneration, persistent P2.3 profile tables, bulk canonicalization, P2.2C/P2.2D promotion, Market v2, personal scoring, or public projection of Registry/Market/Work state.

## 6. Delivery result

The browser slice is implemented at `/compare`, reachable from primary navigation,
the Jobs page, and a job's comparison action. It uses a shared application read model
and SQLite Capability selection rather than the public-corpus files. The experimental
public overlay remains available unchanged in meaning; both inputs reuse the same
exact dependency and grouping checks.

Real-data inspection exposed a pre-existing reader omission: P1.6 v5 stores obligation
in `requirement_type`, while the Registry reader checked only `strength` and
`requirement_strength`. The reader now prefers the v5 field and retains the older
fallbacks. A regression proves required/preferred survival. This is a presentation
repair, not a factual artifact, review, or mapping mutation. Original evaluation
outputs are retained; separately named post-repair outputs have identical mechanical
summaries and corrected strength metadata.

The first browser draft also searched complete evidence spans. Broad shared spans
caused a RAG query to include neighboring Python, Git, and backend qualifications.
The final primary filter searches accepted claim wording only. Complete evidence is
still expandable. The earlier draft screenshots were replaced by final-view screenshots;
the behavior and reason for that revision are retained here.

Real-data Chromium checks exercised RAG across `tvMm`, `tNVe`, and `t7Ay`: the final
view shows 3/36, 4/32, and 3/26 matching exact claims respectively. It exposes required
versus preferred wording, familiarity where explicit, direct RAG work where present,
the reviewed RAG correspondence on the two exact duties, and the absence of direct
duties in `t7Ay`. The Python comparison over `tG9K` and `tmBK` presents two matching
claims in each job and optional existing job-local groups without count inflation.

Browser checks passed for expandable evidence, navigation to the accepted analysis,
report #2 / snapshot 15 / `work-1` return context through form submission, no-match
wording, 390px layout without horizontal page overflow, keyboard skip-to-content, no
page errors, and no external browser requests. Desktop and narrow screenshots were
visually inspected. Evidence remains local in `browser-summary.json`,
`comparison-desktop.png`, `comparison-mobile.png`, and `comparison-grouping.png`.

These are implementation, evidence-integrity, and navigation observations. They do
not establish measured time savings, owner repeated-use acceptance, semantic grouping
over the six target jobs, or mature P2.3 profile acceptance. Owner repeated-use
assessment remains the next product-evidence boundary. No new model/source call,
Registry mutation, profile persistence, or public-corpus publication was needed.

Final local engineering gates: **878 tests passed with warnings as errors**, Ruff passed, dependency consistency passed. The regression set covers the v5 obligation field, literal search versus broad evidence, currentness/acceptance, exact Capability dependencies, shared memberships with distinct factual counts, requirement-only behavior, escaping, bounded input and read-only rendering.
