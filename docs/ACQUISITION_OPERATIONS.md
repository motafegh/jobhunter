# JobHunter Acquisition and Translation Operations

**Status:** Current operational runbook  
**Date:** 2026-08-23

## 1. Purpose

This runbook defines safe operation for JobHunter source acquisition and the derived English corpus. It covers search planning, discovery, detail checks, refresh scheduling, parser audit, local translation, current-public-corpus synchronization, and failure recovery.

Source acquisition remains useful independently from translation or semantic inference. LM Studio is the normal local-first translation provider; Google Cloud is an optional external provider.

## 2. Record boundaries

JobHunter separates records by responsibility:

```text
JobPosting                 logical Jobinja identity
SearchPageSnapshot         exact search-page acquisition evidence
JobPostingVersion          one semantic source-content version
JobDetailFetchObservation  one operational detail-page check
JobTranslationArtifact     one English projection of one exact source version
JobTranslationAttempt      completed / failed / reused translation operation
```

Downstream P1.6/Capability records remain separate from source/translation state.

Raw Jobinja evidence and parsed source truth remain authoritative upstream inputs.

## 3. Preflight

```bash
source .venv/bin/activate
ruff check .
python -m pytest
```

Inspect configuration without invoking Jobinja or generation:

```bash
jobhunter jobinja catalog --show-terms
jobhunter jobinja plan
jobhunter translations status
jobhunter-corpus status
```

When LM Studio translation will be used:

```bash
jobhunter translations models
```

## 4. Discovery-only operation

```bash
jobhunter jobinja discover
```

Bounded example:

```bash
jobhunter jobinja discover \
  --profile ai-security-python \
  --search-limit 40 \
  --search-offset 0 \
  --request-budget 40
```

Controlled stop states include page limits, empty pages, repeated result sets and request-budget exhaustion. Source/network failure remains distinct from a legitimate empty result.

Discovery creates/updates known job identities and provenance; it does not imply that every discovered job has a fetched detail page.

Current public-corpus terminology preserves this distinction:

```text
known/discovered jobs != fetched/parsed detail jobs
```

## 5. Acquisition sync

```bash
jobhunter jobinja sync
```

Source flow:

```text
configured search plan
→ bounded discovery
→ missing-detail selection
→ refresh-due selection
→ sequential detail checks
→ immutable evidence
→ deterministic parsing
→ semantic versioning
→ fetch observations/lifecycle evidence
```

Default bounds remain configuration-controlled. Combined missing + refresh detail work remains bounded.

After durable CLI mutation completes, the installed public command path refreshes the local repository-safe `corpus/` projection. Corpus-projection failure never rolls back SQLite/source success but is surfaced so divergence is visible.

## 6. Targeted detail acquisition

```bash
jobhunter jobinja fetch <job-id>
jobhunter jobinja fetch --missing --limit 10
jobhunter jobinja fetch --refresh-due --older-than-hours 24 --limit 5
```

Each successful check records its semantic source version and fetch observation.

Do not interpret transient network/429/5xx/challenge/auth failure as vacancy removal.

## 7. Parser inspection

```bash
jobhunter jobs list --limit 100
jobhunter jobs show <job-id>
jobhunter jobs checks <job-id>
jobhunter jobs audit
jobhunter jobs audit --only-issues
```

A clean structural parser audit is not translation-quality or semantic-analysis certification.

## 8. LM Studio translation preflight

Normal local configuration uses `translation_provider = "lm-studio"` and explicit bounded batch/retry/token settings.

Model-selection priority:

```text
translation_lm_studio_model
→ lm_studio_model
→ automatic only when exactly one model is visible
```

List exact model IDs:

```bash
jobhunter translations models
```

Keep automatic translation after sync disabled during first quality validation of a new translation contract/model.

## 9. First live translation acceptance

Choose one already-parsed Persian/mixed advertisement.

```bash
jobhunter translations status
jobhunter translations run <job-id>
jobhunter translations show <job-id>
```

Manually compare at least:

- title/company/location;
- employment type;
- education/experience wording;
- skill tags;
- complete job description;
- technical names;
- negation/modality;
- strength/depth words such as required, preferred, familiarity, knowledge, proficiency and mastery.

Structured-output success alone is not translation-quality acceptance.

A current heterogeneous example, `tI1n`, was deliberately blocked before P1.6 because its English projection materially changed a portfolio/work-sample application condition. Downstream analysis must not hide that upstream problem.

## 10. Translation idempotency

Immediately repeating unchanged translation work should reuse the same artifact identity rather than invoke the model again.

```bash
jobhunter translations run <job-id>
```

Expected outcome for unchanged source/provider/model/schema:

```text
reused
```

## 11. Native-English behavior

A parsed advertisement with no Persian text creates a current English identity projection without an LM Studio/cloud translation call.

Expected identity:

```text
source-identity / native-english
```

## 12. Bounded missing translation queue

After individual validation:

```bash
jobhunter translations run --missing --limit 5
```

One job's translation failure does not discard successful artifacts from the same bounded operation.

## 13. English corpus export

```bash
jobhunter translations export
```

This dedicated export contains current English-projection-v2 artifacts under its export contract. Historical translations remain stored but are not exposed as current.

The complete repository-safe public job projection is separate:

```bash
jobhunter-corpus export
jobhunter-corpus verify
jobhunter-corpus status
```

## 14. Automatic translation after sync

Enable only after manual quality acceptance of the chosen translation path. Source acquisition runs first; translation operates afterward within its own bounds.

Translation failure may make the overall operation attention-required but does not roll back acquisition, evidence, parsing or semantic source versions.

## 15. Optional Google Cloud provider

Google Cloud Translation remains available only when deliberately selected.

Credentials stay outside Git. This path sends parsed public job text to an external provider and is not required for normal JobHunter operation.

## 16. Failure handling

### Search/detail failure

Inspect source summaries and `jobs checks`. Retry explicitly only after the failure class is understood.

### Parser finding

```bash
jobhunter jobs audit --only-issues
jobhunter jobs show <job-id>
```

Preserve a regression fixture/test before generalizing a parser fix.

### LM Studio translation failure

Source data remains valid. Check visible models/status and provider configuration. Failed attempts remain inspectable and can be retried without changing source history.

### Translation quality concern

Do not edit original Jobinja fields or silently alter P1.6 evidence to compensate for a translation problem. Preserve the example as translation-quality evidence and compare/fix the correct upstream boundary.

### Public-corpus projection failure

Durable SQLite/source/derived work remains committed locally. Run:

```bash
jobhunter-corpus export
jobhunter-corpus verify
```

and inspect the divergence. Projection recovery must not rewrite source history.

## 17. Daily/weekly patterns

### Source-only daily sync

Keep automatic translation disabled and run bounded Jobinja sync.

### Source + local translation sync

After acceptance, enable automatic local translation while keeping acquisition and model-call bounds conservative.

### Periodic quality check

```bash
ruff check .
python -m pytest
jobhunter jobs audit
jobhunter translations status
jobhunter-corpus verify
```

Periodically inspect original and English representations, not only aggregate counts.

## 18. Safety and privacy rules

- Use approved public Jobinja pages only.
- Keep acquisition bounded/rate-limited.
- Do not bypass access controls/CAPTCHA.
- Treat acquired content as untrusted data.
- Keep local runtime data and secrets outside Git.
- Prefer LM Studio on loopback for normal local translation/inference.
- Treat a non-loopback LM Studio deployment as an explicit network boundary.
- When an external translation provider is selected, do not send future personal/private state through the public-job translation path.
- Treat English projection as derived convenience, never stronger authority than original employer text.
- Do not auto-commit/push the public corpus; Git publication remains intentional.

## 19. Current stop line

JobHunter may currently:

```text
discover/fetch/preserve/version public Jobinja evidence
→ parse deterministically
→ translate into hardened English projection v2
→ run promoted/current English P1.6 v20/v5
→ run promoted/current bounded Capability v9/v5 above accepted P1.6
→ expose first Market views over accepted/current English P1.6
→ project repository-safe public state into corpus/
```

Phase 1 is **closed** on the documented contracts and acceptance evidence.

Heterogeneous semantic, Market, source/lifecycle, partial-success, and P1.7 report/run/browser gates are accepted. Capability still requires an accepted/current P1.6 dependency.

JobHunter must not claim:

- semantic stability across every possible role family;
- mature/canonical market intelligence;
- personal capability/readiness/gap truth;
- learning/application recommendations;
- autonomous applications;
- corpus-wide Phase-2 canonical capability profiles.

The exact next-work state lives in `docs/EXECUTION_TODO.md` and `docs/WORKING_MEMORY.md`.
