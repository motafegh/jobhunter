# P1.6 — real-ad source-first repairs and remaining semantic gates

**Date:** 2026-11-23
**Scope:** bounded engineering remediation following the 2026-11-23 original-source manual audit. Work directly on `main`.
**Disposition:** SOURCE-FIRST REPAIRS VERIFIED ON EXPOSED REGRESSIONS; ORIGINAL-LANGUAGE NEW-ARTIFACT ACCEPTANCE GUARDED; CURRENT ENGLISH v30 AND TRANSLATION SEMANTIC GATES REMAIN OPEN. **Not B5 or B6 acceptance.**

## Origin and authorized engineering scope

The separate original-source manual E2E audit `docs/working-memory/2026-11-23_P16_LIVE_REAL_AD_END_TO_END_SOURCE_FIRST_AUDIT.md` found 3/3 original-source acquisitions and 3/3 English translations succeeded mechanically, but current English v30 failed 3/3. Experimental B2v6 missed seven explicit backend duty passages and all five true AI must-have requirement strengths; an original-language v9 artifact was automatically accepted despite an unsupported experience requirement. CLI discovery with a non-default SQLite path unexpectedly rewrote the tracked public corpus, restored during the trial. Three source descriptions duplicated older evaluation cases, including one new job ID with identical original content.

All three live case descriptions and all four older B5 cohorts are **EXPOSED**; this remediation cannot be counted as unseen success.

## Implemented: conservative B2v7 source-section candidate

`src/jobhunter/source_item_candidate_b2_v7_dom.py` adds opt-in **B2v7**, a versioned candidate on top of preserved B2v6. It recognizes standalone, non-list original DOM section headings; headings control interpretation but do not themselves become requirements. It retains exact original-source offsets, UTF-8 source spans, SHA identity and B1 validation. New headings support "What You'll Work On", "Must Have", "Nice to Have", employer-offering sections and work arrangements.

The first broad relabeling attempt **regressed prior source cohorts** (including missed duties and false mandatory items) and was rejected. The corrected implementation is conservative: it leaves previously sound source categories and explicit preferred/negative strength intact; upgrades uncertain/contaminated labels only under unambiguous standalone headings; recovers plainly stated working conditions when they appear inside benefits. Work assignments are not transformed into prior paid experience. This is intentionally narrower than a general semantic parser.

| Exact source-only diagnostic | Prior B2v6 | B2v7 exposed |
| --- | ---: | ---: |
| Backend explicitly assigned duty passages represented as work duties | 8/15 | **15/15** |
| AI "Must Have" substantive qualifications labeled required | 0/5 | **5/5** |
| Separate AI "Must Have" heading treated as requirement | 1 false item | **0** |
| Persian security duty passages retained as duties | 6/6 | **6/6** |
| Recognized explicit working-hours/arrangement candidate | inconsistent | **available in all affected live cases** |

A second, broader regression replay on **32 previously exposed cohort jobs** (4 sets × 8) validates all B1 bundles and preserves B2v6's selected role scores: first 83/86, second 84/85, third 78/78, fourth 73/73. Across these frozen selected assertions the conservative B2v7 adds **zero newly missed duties, false mandatory claims or critical classification mismatches**. The first cohort **still has one material wrong-category assertion**, and earlier alternatives/other source coverage remain uncertain. Neither test is independent or statistically representative.

**No original B2v4/B2v5/B2v6 evidence or test scorecard has been rewritten.** The accepted v30 pipeline and production feature gates remain unchanged.

## Implemented: independent, usable source-first fallback

New explicit read-only CLI entry:

```bash
jobhunter --config jobhunter.toml jobs source-brief JOB_ID
jobhunter --config jobhunter.toml jobs source-brief JOB_ID --all
jobhunter --config jobhunter.toml jobs source-brief JOB_ID --json
```

`src/jobhunter/source_brief_cli.py` reads the **currently parsed exact original job** from SQLite in read-only mode, verifies the HTML SHA, and uses B2v7 for an original-language-only evidence first view. It separates duties, required candidate qualifications, preferred candidate qualifications, uncertain qualifications, working arrangements, employer benefits and unresolved source items. At most three evidence excerpts appear initially per section; `--all` supplies full source drilldown. It prints exact original board metadata separately so source contradictions are not silently resolved.

Every role, strength and alternative is visibly **candidate-only / not employer-verified**. No model, translation, remote fetch, accepted artifact, target English claim, or production synchronization is performed; the original SQLite SHA was unchanged before and after a real CLI source-brief run. This creates a useful way to read source evidence when English v30 cannot deliver an artifact. It is NOT integrated as an automatic browser fallback or a promoted replacement for semantic analysis.

## Implemented: prevent new unreviewed original-language acceptance

`src/jobhunter/analysis_service.py` now stores newly generated `job-analysis-original-v9` artifacts as **pending** semantic review rather than automatically `accepted`. The accepted English route is not changed. Existing review and rejection workflows remain available.

The regression suite tests a new original v9 result as pending and invisible to accepted-only selectors. A further **actual LM Studio v9 run on a cloned copy of the live Persian-source database** completed in 27.2 seconds and returned **pending**; `accepted_only=True` returned no artifact. The original historical, manually problematic v9 artifact remains in the sealed trial database as originally recorded; this fix does not silently relabel historical accepted v9 artifacts or claim semantic correctness.

## Implemented: source duplication and isolated corpus boundaries

- `src/jobhunter/source_novelty.py` compares exact original-description SHA-256 fingerprints in current and archive **read-only** SQLite source versions, including matching source descriptions across different Jobinja IDs. The utility never claims that a unique fingerprint relative to supplied archives is newly posted or independent of every possible previous source; it does not suppress unrelated active job listings automatically. Verified on actual archived original-source snapshots and synthetic source-changing/cross-ID cases.
- `src/jobhunter/public_corpus.py` provides `automatic_corpus_destination`: canonical `data/jobhunter.sqlite3` retains the established tracked `corpus/` projection; a different (research/test) SQLite database exports automatically only beside its own database, into a private `public-corpus/` directory. Both CLI automatic synchronization and local-browser post-operation synchronization now respect this boundary. Explicit `jobhunter-corpus export --output-dir` remains under its own user-specified destination. Synthetic tests verify both paths; real production corpus and DB hashes unchanged.

## Independent English v30 and translation: what was not repaired

The original live E4B English P1.6 v30 had **0/3 accepted artifacts**, with two depth/concept schema failures and one dense source-duty coverage failure. These validators are currently protective and were **not relaxed** to manufacture success. A separate **v31 guidance-only diagnostic** was run on a cloned isolated AI source against the same strict v30 response model. It **failed** again after ~92.6 seconds because the model still emitted depth wording inside a requirement concept. That changed prompt was NOT shipped and did NOT become accepted v30 or B5 evidence.

The native English-v2 source-text translator's original meaning defects (proper-name drift, merged distinct work duties, fragmented performance benefit) are **not** fully solved by these changes. The new source-first command avoids treating such unverified English as employer truth; independent bilingual alignment, unambiguous quote-level verification and a new bounded semantic/translation improvement remain necessary.

The automatic capability pipeline still requires a qualified, current accepted English analysis; a source-first CLI brief cannot fabricate that prerequisite. No changes to the existing capability promotion boundary or accepted employer facts were made.

## Verification, reproducibility, remaining gates

Regression tests include `tests/test_source_item_candidate_b2_v7_dom.py`, `tests/test_source_brief_cli.py`, `tests/test_isolated_corpus_destination.py`, `tests/test_source_novelty.py`, and updated original-v9 tests in `tests/test_analysis_service.py`. Private exposed case replay and old-cohort source-evaluator replays were executed offline; their raw employer texts, original model responses and archival personal data remain private ignored local evidence. All 32 older selected B1 bundles validated without new critical regressions.

The full Python 3.12 local suite passed **1,274 tests with warnings as errors**; Ruff and local pip dependency checks passed. Production database, public corpus and old frozen evaluation evidence were not modified. GitHub CI result must be checked on the exact published commit before claiming its independent pass.

**Next engineering gate:** a separate versioned and budgeted model-depth/coverage reliability experiment, paired with original-source assertion/child alignment and independent translation assessment. Explicitly distinguish (a) failure to produce structured artifacts, (b) correct rejection of unsupported evidence, and (c) acceptance of semantically correct outputs. Do not turn an adjective like "strong interest" into required paid experience, flatten formal alternatives, claim no duties based on empty candidate extract, or infer validation success from a local prompt tweak.

**B5 unseen generalization: NOT accepted. B6 production rollout: NOT authorized.** User-facing time savings and semantic accuracy still need evidence.
