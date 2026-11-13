# Original-source bilingual lineage, version 1 — implementation and acceptance

**Date:** 2026-11-13
**Branch:** research/p16-original-source-evidence-spine-2026-11-13
**Base:** main 74ffec25533c5cd4b1afa90b0c3bc76ee023e7aa
**Disposition:** Isolated, inspectable source-first research; NO PUBLIC P1.6 PROMOTION.
**Accepted baseline:** English P1.6 v30/v5; Original P1.6 v9/v4; English projection v2.

## The product problem

The current translation v2 proves association between the original and English DESCRIPTION FIELD, not each duty, preference or eligibility item inside that field. Once a long Persian vacancy has been translated into a flattened English paragraph, source-heading and obligation interpretation can be unreliable.

The preceding v31 English-only candidate revealed a concrete issue. Its first EDR explanation was wrong: the Persian original itself says teamwork is an advantage (مزیت محسوب می‌شود), and the English translation agrees. The v31 planner incorrectly called it required. This was explicitly corrected in the preceding experimental branch at commit 03d6071. No existing run outcome or hash was rewritten.

Another real problem remains: for tNhZ, the structured Jobinja skill tag LLM coexists with employer prose explicitly saying LLM familiarity is not mandatory. Current deterministic skill materialization must not be assumed to be authoritative employer obligation.

## What we built

1. **Original source spine:** src/jobhunter/source_lineage_v1.py. Versioned immutable identifiers derived from the precise parsed source detail version, original field SHA-256, original Unicode/UTF-8 offsets, and exact source text hash. Handles common Persian and English original headings, bullets, and sentence separators. Candidate labels explicitly distinguish contextual text, work, qualifications, advantages, employment arrangements and alternative Middle/Senior tracks. A broad duty heading is not allowed to override item-local preference wording. All heuristic qualifications remain unreviewed; they are not asserted required.
2. **Legacy translation alignment:** the same module checks exact current source version, field hash, translation artifact identity, English projection version and field provenance. Native-English identity spans can align exactly. A translated English projection v2 receives an explicit UNALIGNED per-item status; it is not permitted to claim correspondence based on position or similar wording.
3. **New source-bound translation candidate:** src/jobhunter/source_bound_translation_v1.py. Calls the existing translation provider once per exact original span. Provider v2 validates its single content ID. A new candidate retains exact original version and span hashes, local provider/model identity, translated output SHA and semantic review flags. Loss of explicit not-required/preferred modality is flagged. All translated candidates remain source-bound but semantically unreviewed.
4. **Structured-tag advisory warnings:** src/jobhunter/source_obligation_audit_v1.py. A literal structured source skill tag that appears inside an original-language explicitly non-mandatory preference becomes a review warning, not a silently demoted or accepted skill.
5. **Reproducible privacy separation:** scripts/audit_p16_source_lineage_v1.py generates repository-safe count/hash-only audit JSON and local-only raw bilingual review data using a verified SQLite online backup. scripts/translate_p16_original_span_v1.py runs one exact source span against loopback-only LM Studio, with private results and no database writes. scripts/summarize_p16_source_bound_trials_v1.py independently verifies the local source-bound trial records and exports only hashes and counts. Both generated public reports are under docs/working-memory/2026-11-13_p16_source_lineage.

## Five real diagnostic jobs — deterministic result

| Job ID | Exact original spans | Main source observations |
| --- | ---: | --- |
| tNhZ | 17 | 1 duty-group candidate; 1 explicit optional qualification; optional LLM versus board-tag warning; application and arrangement kept separate |
| tMps | 10 | Separate Middle and Senior eligibility tracks, both unresolved alternatives; required versus preferred headings separated |
| tMqd | 3 | Separate duty, qualification and preferred groups |
| tNDx | 19 | 5 work-duty candidates, 6 qualification candidates, 1 explicit preferred teamwork item, 3 benefit items |
| tMjm | 4 | Job-heading introduction is not mistaken for an explicit duty; specialist/general qualifications and salary context separated |
| **Total** | **53** | All exact original offsets and hashes checked |

For all 53 original spans, the existing translated English projection remains ONLY FIELD-ASSOCIATED, not item-aligned. The system reported zero confirmed native identity links on this Persian/mixed cohort and did not invent alignment.

The public audit recorded ONE structured skill/nonmandatory warning, for tNhZ LLM, with the exact source span ID. None of the 53 items or five jobs was promoted into accepted P1.6 authority.

## Source-bound local translation trial

Two source-specific, deliberately exposed diagnostic clauses were sent to LOCAL LM Studio on 127.0.0.1:18080 using gemma-4-e4b-it-ud (no cloud provider). They were each bound to an exact original source span, with content-derived identity, a structured single-item response, and an immutable candidate hash.

| Job | Source span ID | Observed model result | Runtime |
| --- | --- | --- | ---: |
| tNDx | d6b09e236c88e964dc5c886608e54c5f | English still presents teamwork and acceptance of defined management structure as an advantage | 26 s |
| tNhZ | 9324c3cb16fd7ed6120b3a2fce42beba | English still presents financial-markets/Backtest/technical-analysis/LLM familiarity as nonmandatory | 10 s |

Both candidate outputs passed source-identity checks; zero automatic modality warning flags. A focused assistant inspection of these two exact clauses found their stated optionality preserved, but this is NOT an independent blind semantic review. Candidate status is source_bound_unreviewed, and neither is a persistent English projection v3 or accepted P1.6 claim.

This result supports one-to-one TRANSLATION ASSOCIATION only. It does not establish complete linguistic fidelity, all alternatives/depth, full-job coverage, user-value improvement, or model-independent performance.

## Mechanical verification

- 903 warnings-as-errors tests passed in the complete repository suite; 19 targeted lineage/translation regression tests passed.
- Ruff passed across the repository; pip dependency consistency passed; Bash wrapper passed syntax validation.
- Both repository-safe audit reports were checked against ignored private records, local model outputs and exact source versions. Source and local-corpus integrity passed; the production database still has no v31 candidates, and corpus files were unchanged.
- These checks validate machinery and provenance only; they do not constitute independent translation or downstream semantic acceptance.

## Evidence files and privacy

Repository-safe reports:
- docs/working-memory/2026-11-13_p16_source_lineage/COHORT_AUDIT.json
- docs/working-memory/2026-11-13_p16_source_lineage/BOUND_TRANSLATION_TRIAL.json

Local-only, ignored, private original source, translated candidate text, trial status and logs:
- data/local-acceptance/current-real-ads-2026-11-12/
- data/local-acceptance/p16-source-lineage-2026-11-13/

The public report contains only source job IDs, hashes, source span IDs, status, counts and timings. No employer description text, translated candidate text, local database, model raw response or personal information is committed. The provider does not currently export the full wire request/response for these candidate trials; that additional audit trail remains a future acceptance requirement.

## Run/reproduce (from the repository root, current research branch)

1. Activate the existing Python virtual environment. Do not reinitialize or modify the production database.
2. Run the source audit on the isolated current real-ad database:

    python scripts/audit_p16_source_lineage_v1.py --database data/local-acceptance/current-real-ads-2026-11-12/data/current-cohort.sqlite3 --jobs tNhZ tMps tMqd tNDx tMjm --report docs/working-memory/NEW_AUDIT_PATH.json --private data/local-acceptance/p16-source-lineage-new/PRIVATE_REVIEW.json

3. Run the bounded wrapper against a NEW ignored local output folder. It automatically captures the model completion, failure/timeout status, duration and private logs. The model must already be accessible on local port 18080:

    bash scripts/run_p16_source_bound_trial_v1.sh data/local-acceptance/current-real-ads-2026-11-12/data/current-cohort.sqlite3 tNDx d6b09e236c88e964dc5c886608e54c5f gemma-4-e4b-it-ud data/local-acceptance/p16-source-lineage-new

4. Once successful local status/log files exist, generate a **new** safe public metrics file using the preserved local evidence:

    python scripts/summarize_p16_source_bound_trials_v1.py --database data/local-acceptance/current-real-ads-2026-11-12/data/current-cohort.sqlite3 --private-dir data/local-acceptance/p16-source-lineage-new --jobs tNDx --report docs/working-memory/NEW_BOUND_TRANSLATION_REPORT.json

5. Run warnings-as-errors pytest, Ruff, dependency check, Git diff check, SQLite integrity, and verify corpus hashes and production data have not changed.

Because the script refuses to overwrite output evidence, do not reuse the already committed audit filename on a subsequent run. Do not git-add local acceptance files.

## Promotion decision and next engineering gate

**No promotion to English P1.6 v30, original P1.6 v9, translation v2, Capability, Registry or Market.** This work establishes the original-source spine and per-item provider association as reusable research code, not as accepted career facts.

Next, implement an explicit evidence review/qualification boundary for one-to-one original/English source items and original modality. Use a fresh unseen verification cohort, include semantic counterexamples and cross-language failure categories, preserve existing historical accepted artifact IDs, and gate any new P1.6 candidate against source-grounded duties, obligation, exact evidence and complete exclusions. Do not interpret missing generated claims as zero demand and do not bypass source review by trusting deterministic metadata or a model's own confidence.

Only after an independently reviewed useful candidate passes should JobHunter consider wiring this contract into the public pipeline or resuming durable P2.3 capability-expectation profiles.
