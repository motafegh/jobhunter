# B5 third source failure, DOM recovery, and fourth prospective freeze

**Date:** 2026-11-22. **Branch:** main.
**Status:** B5 acceptance OPEN. Third truly new cohort FAILED with frozen B2v3; B2v4 is a non-production successor tested retrospectively on exposed sources. No B6 authorization.

## Third cohort: prospective failure

The third source cohort was selected exclusively from existing source-search metadata after freezing candidate B2v3 at commit `27aacda`, excluding the first two exposed cohorts. Eight public Jobinja details were fetched using the approved adapter and stored in isolated SQLite. The assistant sealed 85 exact original-language assertions, with quote positions and SHA identity, **before inspecting B2v3 results**. This is selected, source-first assistant review, not independent blind human certification or an exhaustive denominator.

Unchanged B2v3 failed the source gate: 78 role-comparable anchors, **48 role matches, 25 role mismatches, 12 missed explicit duties, 3 false required qualifications, 4 jobs missing explicit alternative scope**; 7/8 jobs flagged structurally. No translation, B4, unchanged v30 or native v9 analysis calls followed. The cohort is now EXPOSED and cannot be reused as a fresh independent check.

Private, ignored originals and first verdict: `data/local-acceptance/p16-stage-b5-2026-11-22/third-source-cohort-v1/`. Public safe counts and hashes: `docs/working-memory/2026-11-22_p16_b5_fourth_preflight/SAFE_THIRD_GATE_FAILURE_AND_B2V4_EXPOSED_METRICS.json`.

## Root cause and frozen next candidate

Original Jobinja `JobPosting.description` HTML preserved list, block and heading boundaries that the accepted `jobinja-detail-v2` parser collapses into a flat string. Across all 24 previously EXPOSED original pages, structural text-node reconstruction reproduced the exact same normalized source description, retaining original character/UTF-8 offsets and SHA identities.

Versioned, opt-in `src/jobhunter/source_item_candidate_b2_v4_dom.py` requires original raw HTML bytes and SHA, reparses source JSON-LD, rejects changed original text, and uses original block/list/heading boundaries to suggest evidence-grounded category and preference scope. It preserves unresolved option scope rather than inventing validated Boolean eligibility. Previously supported B2v3 alternatives/duties are not silently dropped. It never creates accepted employer facts or changes the accepted production parser or v30/v9 analyzers.

Retrospective comparison against source-only checks of the first, second and third now-EXPOSED cohorts yielded **80/86, 83/85 and 77/78** correctly matched role-comparable anchors, respectively. On these selected anchors: **zero missed explicit-duty assertions, zero false required qualifications and zero omitted alternative-scope jobs**. These are *assistant-selected diagnostic anchors*, not whole-ad accuracy percentages. Some historical qualification/heading overlaps remain unresolved. Twenty-four B1 candidate bundles, 24 source text reconstructions, and 15 focused B2v4 tests passed. Offline B3 planning predicted 69, 79, and 76 bounded translation batches respectively; **no new translation runs** followed those cohort failures. Prior three-case local model item relabeling degraded selected exposed original-source category accuracy (28/28 B2v3 to 25/28 model); it is not selected for prospective use.

**B2v4 candidate implementation and this protocol are frozen on main before the fourth cohort's original descriptions are accessed.** No candidate code changes after acquisition are allowed to count as fresh-cohort acceptance.

## Fourth independent source-first gate

Use the approved Jobinja source adapter and the *metadata-only* previously frozen discovery catalog. Exclude all 485 known B0 source IDs, the public corpus and every primary/reserve source identity and prior employer company from all three previous B5 cohorts. Predeclare exactly two backend/software, three AI/ML/agents and three security/network cases, with one reserve in each stratum. Freeze that selection BEFORE original descriptions. Maximum eleven first-try public source page requests, normal access restrictions, no bypass. Capture original HTML, source semantic SHA, isolated SQLite and immutable manifest, then seal original-language-only assistant review (exact original text, offsets, obligation, alternatives, unknowns) BEFORE B2v4 interpretation. Independently blind human review is not implied.

One evaluation with the unmodified B2v4 contract follows. **Critical source error means STOP**: source mismatch, unsupported mandatory skill, omitted unambiguous assigned duty, false preferred/negated strength, misleading OR/AND, invented tasks, missing original text or stale accepted evidence. The fourth cohort becomes exposed upon that comparison, whether successful or failed. No favorable post-hoc tuning can turn it back into an unseen result.

Only after an upstream source gate passes may B3 translation be attempted with a separate maximum **80 actual local HTTP attempts and 7,200 active seconds** across sessions, each guarded at <=8 attempts and <=900 seconds, preserving missing/deferred fragments as unresolved. Review original-language technical terms, optionality, negative scope and years. The unchanged English v30/v5 and original v9/v4 baseline should be compared against the same frozen job sources with separately bounded up-to-80 analysis requests and six-hour active B5 window, preserving original/current authority and measurable usefulness. Never regenerate accepted rows or imply independent human certification.

B5 PASS requires source and translation fidelity, no critical claim/alternative regression, old accepted source/chain stability, and demonstrably safer or more useful same-source evidence than unchanged v30. If any gate fails, report **B5 NOT ESTABLISHED**, not successful B5 completion. B6 rollout requires its own explicit promotion decision, backups and rollback even after B5 qualifies. Full descriptions, model payloads and source-first review text remain ignored private files.
