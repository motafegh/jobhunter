# Market I7 — Real Local Acceptance Result

**Date:** 2026-09-18  
**Status:** EXECUTED / HOLD — 2026-09-19 closure follow-up below
**Branch:** `main`  
**Repository head carrying local-work publication:** `d1d2a952e53d980e699348abe3d5bfc8177a60c1`  
**Final CI on that head:** run 1246 / 35386437630 — SUCCESS  
**Protocol:** `docs/working-memory/2026-09-18_MARKET_I7_LOCAL_ACCEPTANCE_PROTOCOL.md`

## Decision

```text
I7 RESULT: HOLD
FIRST MARKET VERTICAL SLICE: REMAINS OPEN
```

This is not an I1-I6 architecture rejection. The real-local runs validated the target-scoped coordinator,
bounded partial-success behavior, currentness/reuse mechanics, membership, source/semantic denominator
separation, browser workflow, and privacy/publication boundary. The remaining gap is acceptance evidence:
the live core snapshot had no accepted-current P1.6 member, so the accepted-semantic requirement/
responsibility drill-down could not be exercised end to end. The captured handoff also did not retain
the final post-rerun snapshot/profile identity + historical immutability comparison or a post-run SQLite
integrity/foreign-key result.

## Exact target and controls

Target:

```text
target id:      1
definition id:  1
slug:           applied-ai-ml-engineering
name:           Applied AI / ML Engineering
```

Membership intent preserved the I3 boundary: direct model/agent/retrieval/evaluation/AI-system work is
core; backend/platform work primarily enabling AI is adjacent; generic use of AI tools is outside.

Search envelope:

```text
AI Engineer
Machine Learning Engineer
RAG
AI Agent
MLOps
```

Each search was limited to one page.

Frozen controls:

```text
request_budget       5
search_limit         5
default_max_pages    1
missing_limit        4
refresh_limit        2
refresh_after_hours  168
translation_limit    4
analysis_limit       2
membership_limit     8
```

The exact definition fingerprint was not retained in the sanitized handoff. The immutable definition ID,
intent, terms and run controls were retained. This missing acceptance datum is one reason not to over-claim PASS.

## Preflight / deterministic baseline

Before the live run:

- local operational SQLite existed;
- pre-run SQLite integrity was reported clean and foreign-key checks were empty;
- direct LM Studio access worked after bypassing an environment proxy path that had produced a misleading 503;
- focused Market tests passed;
- the complete deterministic suite passed with warnings-as-errors;
- a pre-I7 SQLite backup was created under ignored local acceptance data.

No operational SQLite, tokens, raw provider protocol or local acceptance logs are published here.

## Run 1

Run 1 completed as `completed_with_failures`.

Observed product result:

```text
core source postings:             6
accepted-semantic core postings:  0
P1.6 failed attempts:             2
P1.6 missing analyses:            4
snapshot:                         created (snapshot 1)
aggregate profile:                created (profile 1)
```

The important behavior was correct: source-level Market membership remained useful while P1.6 failures
and missing semantic coverage stayed explicit. Missing semantic evidence did not become zero demand.

Browser inspection of the first result exposed bounded I6 presentation gaps:

- target/definition/run forms used weak/unhelpful controls;
- membership rows did not expose reason/evidence;
- aggregate rows did not expose the frozen claim evidence already stored in I5;
- warning objects were not rendered through their message field.

Those are presentation/inspection defects, not semantic-contract defects.

## Bounded I6 repair discovered by I7

The local agent repaired only the browser/evidence presentation boundary:

```text
src/jobhunter/web/static/app.css
src/jobhunter/web/templates/market_workspace.html
src/jobhunter/web/templates/market_snapshot.html
tests/test_market_aggregate_service.py
```

The repair:

- styles Market forms consistently;
- exposes membership reason/evidence/dependency identity;
- exposes immutable aggregate employer/source context;
- exposes frozen P1.6 claim evidence for requirement/responsibility rows;
- exposes all requirement-strength columns;
- renders warning messages rather than dictionary representations.

A regression test proves a historical Market snapshot continues to render its frozen P1.6/employer
evidence after a later source version changes. HTML escaping is also covered.

The pushed head passed CI 1246.

## Run 2 — unchanged definition and controls

Run 2 completed at 2026-09-18T19:27:14Z as `completed_with_failures`.

Discovery:

```text
searches attempted: 5
requests attempted: 5
pages fetched:      5
candidate jobs:     52
known jobs:         52
new jobs:           0
discovery failures: 0
```

Source execution:

```text
attempted:     6
succeeded:     6
new versions:  5
unchanged:     1
failures:      0
```

This is consistent with bounded progression through remaining target-scoped missing/refresh work rather
than a global backlog spill. The final affected-work plan still reported 39 missing and one refresh
remaining, proving the run did not pretend target completion.

Translation:

```text
attempted: 4
completed: 2
failed:    2
stage-level reused: 0
final affected-work current/reused translations: 9
remaining: 3
```

The two failures were LM Studio timeouts. They remained explicit and did not roll back successful source
or translation work. The final affected-work state demonstrates that already-current translations were
recognized/reused rather than regenerated.

P1.6:

```text
attempted:              2
completed-or-reused:    1
failed:                 1
current accepted:       0
current pending review: 1
remaining:              8
```

The failure was an existing P1.6 v20 validation failure around dense source accounting/depth semantics.
The validator failed closed. No validator weakening, vacancy-specific prompt patch or automatic semantic
acceptance was introduced.

Membership:

```text
eligible:  12
selected:   8
remaining:  4
succeeded:  8
failed:     0

core_match:      6
adjacent_match:  1
excluded:        1
```

The membership service reuses exact dependency identities before model inference. The rerun ledger counts
successful selected memberships but does not separately expose completed-vs-reused membership counts.

## Browser / CLI

Local browser inspection confirmed:

- `/market/targets` was reachable;
- repaired forms were usable at desktop and narrow viewport;
- membership reason/evidence became visible;
- snapshot 1 rendered the source/core and semantic-coverage state;
- source drill-down to a job page worked.

The first live snapshot had zero accepted-semantic core postings, so the newly repaired requirement/
responsibility claim-evidence rows could only be regression-tested with deterministic fixtures, not
demonstrated against accepted semantic evidence in the real I7 target.

## Public corpus / privacy

The governed upstream public projection legitimately advanced during the real Market work:

```text
known/discovered jobs:       394
fetched/parsed details:       51
current English projections: 27
accepted English P1.6:         5
accepted Capability:           5
```

Repository audit after publication found no occurrences under `corpus/` of:

```text
market_targets
market_research_runs
market_job_memberships
market_corpus_snapshots
market_aggregate_profiles
127.0.0.1
/home/motafeq
configured local model identity
```

Market target/run/membership/snapshot/profile state therefore remains local/private.

## Why HOLD instead of PASS

PASS requires the complete real repeated-use path to be demonstrated.

The following remain incomplete in the preserved evidence:

1. accepted-semantic core denominator was zero, so live requirement/responsibility prevalence and frozen
   P1.6 evidence drill-down were not exercised end to end;
2. run 2 was terminal, but the sanitized handoff did not capture the second snapshot/profile identity
   and a post-rerun comparison proving snapshot/profile 1 remained byte/identity-stable;
3. pre-run SQLite integrity was clean, but the post-run integrity/foreign-key output was not retained;
4. the immutable definition fingerprint was not retained in the sanitized handoff.

These are acceptance-evidence gaps, not permission to weaken P1.6 or rebuild Market architecture.

## Exact next responsibility

Do only the remaining I7 closure work:

```text
review the one current pending P1.6 artifact using the normal semantic-review boundary
→ accept only if genuinely valid; otherwise reject/preserve evidence
→ obtain at least one accepted-current P1.6 core member without auto-acceptance or validator weakening
→ inspect the resulting live requirement/responsibility aggregate + frozen evidence drill-down
→ inspect run-2 snapshot/profile and prove run-1 snapshot/profile historical immutability
→ run post-execution SQLite integrity + foreign-key check
→ repeat privacy/publication check
→ record PASS only if all remaining checks succeed
```

If a valid accepted-semantic core member cannot be obtained under the bounded target/provider conditions,
preserve HOLD rather than manufacturing acceptance.

## Stop lines

While I7 is HOLD, do not start:

- semantic role-subfamily synthesis;
- trends/emerging/forecasting;
- Market → You;
- P2.2C/P2.2D promotion;
- P1.6 auto-acceptance or validator weakening;
- Capability/Work as mandatory Market gates;
- repost-dedup authority;
- Market-state public export;
- new workflow/currentness/persistence infrastructure.


## 2026-09-19 — Takeover, recovered closure evidence, and bounded review repair

Fetched all remote refs/tags and fast-forwarded `main` from `d1d2a95` to
`977af11f419dc0ef2540b2fadc121f5038321875`. No submodules were configured. The
operational database was present; the existing default configuration selected it.
The protocol's example `config/local.toml` was absent, so no replacement config was created.

### Recovered operational evidence

- Target 1 / definition 1 / version 1 fingerprint:
  `4f77e7966b68cae9c4d2545212269f7b85482458ce30e51bee435bdd65400d9f`.
- Run 1 → snapshot 1 → profile 1, profile SHA-256:
  `99fef4bd178c854ba3397674a57b663610d1e5ff69d507f255abea75ece649df`.
- Run 2 → snapshot 2 → profile 2, profile SHA-256:
  `11ccfeffa8eb858b87436d749d13488c6a860557e1901a8e292e43417e22d9eb`.
- Snapshot 1, all members, and profile 1 exactly match both retained pre-rerun
  structured JSON captures. This closes the missing historical comparison; it is
  comparison of parsed JSON values, not a claim about JSON whitespace bytes.
- Snapshot 2 has 6 core, 1 adjacent and 1 excluded member. Its core semantic
  coverage is 0 accepted, 1 pending, 4 missing and 1 failed.
- Post-run operational SQLite: `integrity_check = ok`; `foreign_key_check = []`.
- Public corpus scan found no Market table names, loopback address or local home
  path. No corpus changes were made during this follow-up.

These checks close the preserved-evidence gaps for definition identity, rerun
snapshot/profile existence, snapshot-1 immutability and post-run SQLite integrity.
They do not close the accepted-semantic drill-down gate.

### Pending candidate review — do not accept

The one pending candidate is `t7ck`, P1.6 artifact 48, source detail 48, English
projection 42, with 18 requirements and 7 asserted responsibilities. Its source
and translation were inspected directly. Review found material issues:

1. Required GPU coverage and preferred familiarity with Whisper, wav2vec2, XTTS
   and Chatterbox are absent from requirements.
2. Streaming Audio, Real-Time Voice, VAD and Voice Cloning are asserted as required
   even though the complete source sentence describes that experience as an
   advantage. Latency reduction is marked contextual; the shared optionality is
   not preserved across the sentence.
3. Practical experience and ability statements are converted into seven factual
   duties, contrary to the qualification-versus-duty boundary.

Recommendation: reject this candidate; never promote it to manufacture I7 PASS.
Operational artifact 48 remains pending until the owner's explicit review decision.
No model regeneration, model change, source reacquisition or semantic-validator
weakening was performed in this follow-up.

### Reproduced lifecycle defect and bounded repair

On a temporary SQLite backup, the normal rejection service failed with
`IntegrityError: FOREIGN KEY constraint failed`: snapshot 2 member 8 references
pending artifact 48, while the old rejection implementation deleted that artifact.
The failed transaction rolled back, preserving the candidate and snapshot.

The repair is owned by `AnalysisStore`:

- archive the rejected candidate and retain its exact payload/ID when a historical
  pending Market snapshot references it;
- mark the retained row rejected and exclude it from current/reuse queries;
- permit a replacement under the same source/translation/model/contract identity;
- preserve frozen snapshot/member/profile state and retained attempt linkage;
- keep accepted Market and Capability downstream rejection protection;
- migrate the prior two-state schema with foreign-key validation and preserve the
  autoincrement high-water mark so archived IDs cannot be reused.

Unreferenced rejections retain the existing archive/delete behavior. This changes
review lifecycle persistence only; it does not alter P1.6 extraction or acceptance
semantics, nor I5 aggregate semantics.

Validation:

- focused baseline before repair: 35 passed with warnings-as-errors;
- regression coverage exercises fresh and legacy schema, pending → rejected →
  replacement, immutable old snapshot/profile, new rejected coverage, accepted
  downstream protection, and foreign-key integrity;
- repaired rejection replay on a copy of the real operational database passed;
  every row in both historical snapshots, their members and profiles was unchanged;
- full suite: **636 passed** normally and **636 passed** with warnings-as-errors;
- Ruff and dependency consistency checks passed.

The operational SQLite was not migrated or semantically mutated by these repair
replays; all migration/rejection replays used temporary copies. Changes remain
local/uncommitted, with no commit, push or publication performed.

### Remaining exact work

Owner review decision for artifact 48 → apply the supported rejection if confirmed
→ obtain a genuinely valid accepted-current core P1.6 artifact through bounded
normal generation/review → build a new point-in-time snapshot/profile → inspect
live accepted-semantic requirement/responsibility evidence through CLI and browser
→ recheck integrity/privacy after those mutations. Keep I7 HOLD until that path passes.


## 2026-09-19 — Incremental publication and operational rejection

The owner authorized continued building/fixing and progressive commits/pushes.
The history-preserving rejection repair and recovered evidence were published as
`d761a4f` before starting the next coherent repair batch.

After a local SQLite backup, the reviewed rejection of `t7ck` artifact 48 was
applied through `AnalysisStore.review_current`. The archive preserves the semantic
review reasons and original model evidence. The retained historical artifact is
`rejected`; it is absent from current/reuse selection. Every row of both snapshots,
their members and aggregate profiles remains unchanged. SQLite integrity is `ok`
and foreign-key checks are empty. No semantic artifact was accepted.

### Bounded evidence-preparation repair

Replaying the exact projection exposed two deterministic contributing defects:

- residual qualification accounting only covered decomposed recognized headings
  and the tail after the last list. Headingless prose lost material between lists;
- the pre-heading duty detector matched `to` within hyphenated text or crossed
  sentence boundaries to candidate ability wording, imposing a spurious duty ledger.

The owning helpers now preserve exact uncovered text from each detected list's
sentence and restrict implicit duty detection to a same-sentence infinitive,
excluding ability/capacity/experience qualification prefixes. No employer text is
rewritten and no vacancy-specific prompt or technology list is introduced.

For projection 42 the missing GPU/model-familiarity sentence remainder is now
addressable and the false whole-paragraph duty checklist is absent. This is not a
claim that all semantic issues are solved: shared optionality, complete semantic
coverage and qualification-versus-duty assertions still require normal review.

Focused regressions: 23 passed. Full strict-warning suite: 638 passed. Ruff and
dependency checks passed. Read-only before/after helper comparisons on all five
accepted public anchors found identical residual and duty plans; no anchors were
regenerated or their review state changed.

Next bounded live step: one current target-core posting with missing P1.6, using
the existing configured model/contract, then inspect the candidate without auto-
acceptance. No full acquisition rerun is needed for this evidence step. The provider
models endpoint is reachable and lists the configured analysis model.
