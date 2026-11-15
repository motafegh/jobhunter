# P1.6 B2 — source-item / board-reconciliation diagnostic slice, full gate OPEN

**Date:** 2026-11-15
**Branch:** `feature/p16-b2-source-items-metadata-2026-11-15`
**Parent accepted main:** `5d4a5e0a64e1dc1da64bc9f28848b4357895aa7e`
**Disposition:** B2 **first engineering diagnostic increment**, not full B2 acceptance or production activation.
**Governing plan:** `docs/P16_STAGE_B_SOURCE_GROUNDED_BILINGUAL_IMPLEMENTATION_PLAN.md`
**B1 contract:** `jobhunter-stage-b1-source-evidence-bundle-draft-v1` remains unchanged.

## Delivered

- `src/jobhunter/source_item_candidate_b2.py`: read-only, source-version-bound original item candidates using the accepted Stage A exact description anchors; bounded headings, obvious bullets, sentence boundaries, and conservative cues where the provider flattened natural list structure. Ambiguity stays unresolved rather than becoming employer truth.
- Separately references structured Jobinja board values with typed paths and canonical JSON hashes (no synthetic employer obligation). Flags possible copied-section contamination within board `skills`, optional-prose / board-skill disagreement, board employment-mode scope narrowing and board experience-range compression of alternative tracks. **Flags mean inspect, not established logical contradiction.**
- Retains candidate alternative-group references for Middle/Senior tracks, explicit "one of" technical domains and certificate-or-equivalent-knowledge clauses; these do NOT yet prove a complete nested AND/OR graph.
- Optional `strongly_implied_by_work_candidate` links for directly mentioned broad concepts on actual work duties. These are relevance suggestions, **not** employer-required previous professional experience or claimed mandatory named frameworks. Qualification-only cases are not turned into invented duties.
- `scripts/diagnose_stage_b2_candidate.py`: backs up an explicit frozen SQLite input to a private temporary copy, runs four read-only candidate analyses, maps their conservative subset into the accepted B1 design shape, invokes B1 structural/source validator, and writes **private full examples** only to ignored local acceptance files alongside a **source-safe aggregate metrics** file. No model, scraper, production database, corpus or downstream write.
- `tests/test_source_item_candidate_b2.py`: generalized counterexamples and source-exact exposed-case checks, nonmandatory-vs-preferred distinction, optional work-capability links, board-hash tampering, no false work-duty inference, privacy/output-path checks, B1 structural compatibility and alternative preservation.

## Frozen real-source diagnostics (exposed, not independent holdout)

Input (private): `data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3`

Input database SHA-256 (unchanged before/after):
`bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe`

Output (private, ignored): `data/local-acceptance/p16-stage-b2-2026-11-15/verified-first-slice/`

| Case | Candidate source items | Important observed behavior |
| --- | ---: | --- |
| `tNhZ` | 22 | Six separate duties, LLM duty-to-capability hint, prior LLM familiarity preferred/nonmandatory, board LLM tag non-authoritative, full-time board possibly narrower than prose |
| `tMps` | 19 | Work-duty candidates, two source-owned seniority tracks, one-of-domain clause retained, copied-section warnings in board skills; nested within-track AND/OR decomposition **pending** |
| `tNDx` | 19 | Five explicit EDR duties, teamwork preferred, bare Kaspersky credentials and government-customer experience strength unresolved, credential-or-equivalent clause retained but not yet expanded as validated graph |
| `tMjm` | 18 | Qualification-only description not transformed into duties, remote-work possibility an arrangement, conscientiousness a behavioral trait, salary lower bound retained |

Across four exposed cases: **78 original-source item candidates**, **53 separately owned board values**, **10 optional broad work-capability hints**, **3 non-authoritative alternative-group candidates**. The structural projection of each diagnostic candidate validated under the accepted B1 draft with exact private source objects, **no accepted review events**, **zero promoted employer facts** and **zero source-bound translation item claims**.

A separate comparison against four **already exposed, assistant-reviewed** B1 reference fixtures located **30/30** saved original-source references in at least one overlapping B2 item with the same proposed category/strength; only **24/30** were contained in a single B2 item. This is a diagnostic continuity check, **not an independent semantic accuracy score**, a new success denominator, or evidence of reliable future-job analysis.

**Full output SHA-256 (private):** `cf4329ece2f4f244d5ed0c293cd4d4afdfead14b6a06e44294b282e01ea304fc`

**Source-safe public report SHA-256:** `22d149429fa3a69d06f0d68169b692527cdf2abcc93a4d1042b3a2a630a26ef1`

**Publication:** Safe metrics only at `docs/working-memory/2026-11-15_p16_b2/SAFE_FIRST_SLICE_METRICS.json`. No raw description, employer HTML, source-bound translation, private output or owner annotation is committed.

## Acceptance boundary

**Engineering verification:** 20 focused B2 tests passed, 966 full warnings-as-errors repository tests passed, and Ruff/dependency consistency pass locally. Public GitHub CI requires separate review before any promotion.  self-contained tests pass, source anchors verify exact character/UTF-8 offsets and source SHA, structured board refs verify selected canonical JSON values, and the B1 validator accepts the non-authoritative candidate projection. Public v30 English/v9 original analyzer routing and accepted P1.6/Capability/Work/Registry/Market data remain unchanged.

**Full B2 gate remains OPEN.** This deterministic first slice deliberately **does not prove**:
1. General Persian semantic correctness for unseen advertisements, all low-structure text or source-heading completeness.
2. A complete, independently validated **nested** AND/OR eligibility graph for the Middle/Senior conditions and the certificate-or-knowledge options. The original exact clauses and explicit candidate alternatives are preserved; do not derive automated applicant eligibility from the incomplete graph.
3. Whether a small bounded local model interpretation improves meaning coverage and the correct duty-capability overlap *without* causing more unsupported mandatory claims, lost contextual relationships, prompt failure or compute cost.
4. Source-to-English item semantic fidelity (B3), useful user-facing brief (B4), unseen cohort generalization (B5), production promotion (B6).

**Next B2 increment:** inspect disputed/undercovered exact spans and nested alternatives; compare the simple deterministic candidate against at most one bounded source-context semantic approach only where it adds value. Evaluate false mandatory claims **and** useful context lost, keep source-first ambiguity unresolved, and avoid making all possible capability links mandatory. Add only generalized repairs with negative counterexamples. Rerun complete B2 acceptance before marking the gate PASS. No external source calls, cloud model, migrations or public route changes are authorized by this first slice.

This increment is **safe to preserve on its feature branch for review**, but the complete B2 gate must not be reported passed or be treated as permission to activate its heuristic classification in production.
