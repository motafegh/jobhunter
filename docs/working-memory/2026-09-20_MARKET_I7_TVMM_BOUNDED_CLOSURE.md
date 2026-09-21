# Market I7 — tvMm bounded closure follow-up

**Date:** 2026-09-20 (Asia/Tehran; execution timestamps are UTC)  
**Status:** EXECUTED / HOLD  
**Baseline:** `6fc2a85110` on `main`

## Executed boundary

Fetched all remote branches with pruning and fast-forwarded the clean checkout from
`8c7fdb0` to `6fc2a85`. The latest handoff selected `tvMm`; operational inspection
confirmed no current English P1.6 candidate. Source detail 47 and English projection
41 were inspected against the public source/projection evidence.

After SQLite backup and clean integrity/foreign-key checks, executed exactly one
supported `jobs analyze tvMm` command with the existing configured model and v20/v5
contract. No acquisition, translation, model switch, or additional generation was run.
The normal runtime's bounded validation retry is part of this one command.

## Result

Attempt 106 failed with `InferenceResponseError`; no analysis artifact was persisted
or accepted. Final validation reported:

- a requirement retained familiarity depth wording in its concept instead of the
  required separate depth field;
- two model-authored requirements cited `field:skills:0` and `field:skills:1`, which
  were absent from the model-facing evidence catalog.

The latter exposed a concrete instruction/payload contradiction: v20 materializes
structured skill tags deterministically and removes them from model fields, but its
inherited v18 prompt still says those tags remain model-visible and require model
classification. The payload also lists their deterministic references. This does not
justify accepting invented references or relaxing evidence validation.

The former remains a model semantic-normalization failure. Fixing the instruction
contradiction alone cannot establish semantic acceptance or I7 PASS.

## Verification

- Full deterministic suite: **638 passed with warnings-as-errors**.
- Ruff and dependency consistency: passed.
- Pulled-head GitHub CI: run `35462865219`, success.
- Post-generation SQLite integrity: `ok`; foreign-key violations: none.
- Every Market table exactly matches the pre-generation backup, including historical
  snapshots, members, and profiles.
- Public corpus unchanged: 394 jobs, 27 English projections, 5 accepted English P1.6,
  and 5 Capability artifacts. Market-table/local-path privacy scan found no matches.
- Raw provider error/completion evidence and SQLite backup remain ignored local data.

## Bounded next work

Repair the general v20 structured-skill instruction/payload ownership contradiction
and protect it with an offline provider-boundary regression. Preserve historical
prompts, deterministic skill facts, and strict evidence/depth validation. Do not
rerun the selected case repeatedly or select another vacancy to manufacture PASS.

I7 remains HOLD: no accepted-semantic core artifact or new semantic snapshot/profile
was created, and live accepted-semantic CLI/browser drill-down remains unexercised.

## Completed bounded repair

The v20 prompt now replaces the inherited model-owned structured-skill instruction
with its actual deterministic ownership rule. Historical v18/v19 prompt values remain
unchanged. Deterministic requirement references remain in local request runtime
metadata but are omitted from model-facing input; they are not valid model evidence.

An offline provider-boundary regression exercises real v20 partition preparation and
merge validation with a stubbed inference call. It verifies that description
requirements remain extractable, exact structured skill facts are injected once,
deterministic IDs remain in runtime metadata, and invented skill references still
fail evidence validation. This is a general ownership correction, not a vacancy
rule, semantic validator change, or acceptance claim.

No second live generation was performed. The remaining depth-normalization failure
was not relaxed or treated as fixed. Before another live attempt, define a bounded
post-repair evaluation decision; do not blindly repeat the previous next command.

Repair validation: **639 tests passed normally and 639 with warnings-as-errors**;
Ruff passed. This establishes deterministic repair coverage, not post-repair
real-model accuracy or accepted-semantic product completion.

Published execution record: `4fe74d4`. Published repair: `94a14a1`.
GitHub CI run `35468478422` passed all gates on the repair, including installed
entrypoints, Ruff, normal tests and strict-warning tests. Public-corpus verification
also passed against all 394 known jobs. Current routing documents preserve HOLD and
the unexecuted post-repair real-model boundary.

## Bounded post-repair evaluation decision

The owner's continuation authorizes one post-repair `jobs analyze tvMm` command
against the unchanged source 47 / projection 41 and existing configured model and
v20/v5 contract. The only changed inference inputs are the published general
structured-skill ownership correction. Existing runtime validation bounds remain.

Evaluate two separate questions: whether absent structured-skill citations recur,
and whether the complete result is valid enough for semantic review. A candidate
must still pass source coverage, optionality, depth and qualification/duty review.
A failed attempt ends this evaluation without another generation or vacancy switch.
No acquisition, translation, model change, validator relaxation or automatic
acceptance is included. Back up SQLite first; verify historical state, integrity
and public-corpus privacy afterward.

## Post-repair result and semantic review

Attempt 107 completed and created pending artifact 49 with 10 responsibilities,
15 requirements and no role-purpose claim. The absent structured-skill citation
failure did not recur in this one case. Exact `Ai` and `Engineer` tags were injected
by the application. This is bounded repair evidence, not general model accuracy.

Complete source/projection/artifact review rejected artifact 49:

1. Seven experience requirements incorrectly acquired `familiarity` depth:
   LLM/API experience, Agent/workflow building, production Agents, Multi-Agent work,
   real database/API integration, Docker/cloud experience, and AI product building.
   The raw model response had null depth for all of them. Deterministic validation
   inserted the first neighboring marker because all markers in each broad evidence
   span had the same spelling. Repeated identical markers do not establish one
   shared subject or scope.
2. Requirement 12 turns the intended AI system's task execution/accounting-system
   interaction into a required candidate skill. The source subject is the AI system;
   the candidate's separate requirement is to build a reliable product Agent.

The 10 responsibility statements are supported by the explicit duty passage;
preferred experience remained preferred. These positive findings do not offset the
material requirement/depth defects or establish complete requirement coverage.

Rejection used the supported review command. Artifact 49 is archived as rejection 8
and excluded from current reuse/export. Its raw response and persisted payload were
also retained locally for diagnosis. No accepted semantic artifact, membership,
snapshot or profile was created. Every Market table matches the pre-evaluation
backup; SQLite integrity is `ok` and foreign-key checks are empty. The public corpus
remains unchanged at 5 accepted English P1.6 artifacts.

### Next bounded repair

The repeated-identical-marker case belongs to v20 deterministic depth validation.
Reject ambiguous automatic depth filling when multiple source markers occur, even
when their spelling is identical. Preserve explicit model-supplied item-specific
depth handling and historical validators. Cover the failure with offline regressions
and replay the retained raw artifact without model calls. This does not resolve the
separate semantic subject error. No further live generation belongs to this evaluation.

## Deterministic depth repair and current stop line

V20 no longer auto-fills null depth from an evidence span containing multiple
depth markers, even when every marker uses the same word. The model must supply
a source-exact item-specific phrase for an explicit depth claim. Historical v19
and earlier validators are untouched. A focused regression covers repeated-marker
rejection and preservation of a supplied scoped phrase.

Read-only replay of artifact 49's retained raw model response found that all 12
model-authored requirements cited broad spans with repeated markers while carrying
null depth; all now fail before borrowing depth. This is fail-closed diagnostic
evidence, not proof the model can generate a valid replacement. Read-only checks
over the five accepted public anchors found no new validation failures. One
historical `more than six years` result retains its existing separate lower-bound
preservation behavior.

Artifact 49 remains rejected. Its separate subject-attribution error is not fixed
by this depth change. I7 remains HOLD with no accepted-semantic core posting.
Further model attempts or a different vacancy require a new bounded evidence
decision; this closure work stops at the reviewed rejection and deterministic repair.

Repair gate: **640 passed with warnings-as-errors**, Ruff and dependency checks
passed, and public-corpus verification passed for all 394 known jobs. Post-mutation
SQLite integrity and foreign-key checks passed; every Market table still matches
the pre-evaluation backup, and the corpus privacy scan found no Market or local
host/path leakage. These checks do not change the I7 HOLD decision.

## 2026-09-20 — Remaining subject error investigation

Read-only inspection of artifact 49 and current evidence preparation located the
remaining semantic error. The `Required skills` heading carries forward into one
long translated section containing preferred qualifications, company/product goals
and application instructions. Semicolon splitting yields a third candidate coverage
span that begins with intended AI-system behavior. It has `allow_exclusion=True`:
the model was allowed to say this span is not a candidate qualification, but instead
turned system behavior into a candidate skill. The persisted review boundary caught
the claim; the normal validator cannot establish the intended subject from exact
text matching alone.

A read-only scan of all 27 current English projections found four requirement
coverage spans with company-goal or application transitions: two in `tvMm` and two
in `tGc5`. This shows section-scope leakage can recur, but the observed text does
not support one safe deterministic cutoff. For example, a company-goal sentence
can still state a real candidate expectation, while application instructions
usually do not. Cutting at one phrase or adding a vacancy-specific prompt would
silently discard valid requirements in other postings.

Decision for this bounded I7 continuation: no source or validator patch, no new
model run and no replacement vacancy chosen for PASS. Artifact 49 stays rejected.
The next material step needs a separate, source-backed design for section scope and
subject attribution with representative positive and negative cases, or naturally
available valid accepted-semantic evidence inside the same target workflow. Until
then, the first Market slice remains I7 HOLD. The existing source-level Market view
and honest missing-semantic denominator remain useful and correct within their
declared authority.

## 2026-09-20 — Source-backed evidence-span repair

The requested continuation supplied enough evidence for two narrow grammatical
boundaries, without creating a general subject classifier. A dependent infinitive
after a semicolon retains the preceding clause's subject and exact source spacing.
An explicit `How to Apply:` heading ends the active requirement section; a later
requirement heading can start a new section. Both rules operate on evidence spans,
not extracted semantic claims, and preserve the complete source description.

Representative cases were the `tvMm` product-intent sentence (`We want AI ...;
to examine ...`) and `tGc5` application heading. Before the repair, `tvMm` placed
the infinitive continuation in a separate required coverage reference and `tGc5`
treated application instructions as requirement coverage. After the repair,
`tvMm` retains the AI subject in one exact span (three requirement references
become two), while `tGc5` removes the application segment from the requirement
plan (22 references become 21). Synthetic regressions also cover independent
semicolon qualifications, exact whitespace, application-section exclusion and
re-entry through a later required-skills heading.

Read-only before/after comparisons found identical requirement and responsibility
plans for all five accepted public anchors. Every new plan text was checked as an
exact substring of its source description. This reduces a repeatable source-scope
failure, but it does not prove that a model will correctly assign every product
goal or produce an acceptable P1.6 artifact. Artifact 49 remains rejected; I7
remains HOLD, and no further live generation was used to manufacture a PASS.

Verification: **642 tests passed with warnings-as-errors**, Ruff and dependency
checks passed, and the complete 394-job public corpus verified. No operational
SQLite or public-corpus state was changed by this evidence-span repair.

## Bounded live check after the source-span repair

The source-span repair changes the exact evidence the existing model sees. One
targeted `tvMm` generation is therefore authorized as validation of that change,
not as a model/prompt matrix or a search for an easy passing vacancy. Use the
unchanged source 47, English projection 41, configured model and v20/v5 contract.
Back up SQLite before the command. The normal bounded validation retry belongs to
this one command. Inspect any candidate against the complete original source and
English projection, including depth, optionality, duties and the product-versus-
candidate subject. Accept only if valid. A failed or materially invalid result
ends this check; preserve HOLD and do not switch vacancy/model or keep retrying.

### Result — 2026-09-20

Operational SQLite was backed up before execution. The unchanged targeted command
ran against source detail 47 and English projection 41 as analysis attempt 108. It
failed after the configured one validation retry; no candidate or accepted artifact
was created. The first provider response had three depth-field validation errors;
the retry had twelve. In the latter, requirement items cited broad evidence spans
with multiple explicit experience/depth markers but supplied no item-specific
`depth_signal`. The v20 guard refused to borrow a marker from another subject in
the span. This was a validation failure; the later exact-scope diagnosis below
separates model omissions from the broad-reference contract limitation. It is not
evidence that the source-span repair is wrong or a reason to relax the guard. Raw provider protocol
and the full error log remain local and are not publication material.

Post-run SQLite `integrity_check` is `ok` and `foreign_key_check` is empty. Exact
row-content digests for all seven `market_%` tables match the pre-run backup,
including both historical snapshots, their members, and profiles. I7 remains
**HOLD**: there is still no accepted-semantic core posting, so the semantic
snapshot/profile and CLI/browser drill-down cannot be claimed. This bounded live
check is closed. Do not repeat `tvMm`, switch vacancies/models, auto-accept, or
weaken depth validation merely to obtain PASS. The next decision needs independent
representative evidence of a generalizable semantic/evidence improvement or a
naturally available valid accepted-current core artifact.

### Offline depth-scope audit after attempt 108

The source-span hypothesis was checked against all 27 current public English
projections using the existing requirement coverage planner and v20 depth-marker
recognizer. The planner emitted 111 requirement references. Fourteen references
across 13 jobs contain multiple recognized depth markers; all fourteen are longer
than 300 characters. `tvMm` contributes two such references (420 and 1,414
characters), with repeated `familiarity` markers. Other shapes include hyphenated
lists, period-delimited sentences, and comma-separated prose, so a single length
cutoff or punctuation split would change evidence scope without proving the right
subject for each marker.

The accepted/current `tmBK` P1.6 is a counterexample to treating a broad span as
inherently unworkable: its 305-character source list has seven recognized markers,
and its reviewed artifact preserves the corresponding item-specific `Mastery`,
`Familiarity`, and `Sufficient knowledge` values. This audit supports retaining the
fail-closed validator and rejects a length-only splitter. It does not establish a
safe general parser change or make attempt 108 semantically valid. No new model
call or operational-state mutation was made for this audit; I7 remains HOLD.

### Explicit repeated-marker integrity repair

A separate v20 validator gap remained after the null-signal repair: an explicitly
supplied `depth_signal` containing two equal marker words could pass because the
validator counted distinct spellings rather than occurrences. For example,
`familiarity with tool calling, familiarity with retrieval` identifies two
subjects even though both markers read `familiarity`. V20 now requires exactly one
recognized marker occurrence in an explicit signal. It still accepts an exact
single-marker subject-scoped excerpt. The regression covers both cases.

This is a fail-closed source-integrity correction, not a solution for attempt
108's missing item signals. All 85 requirements in the five accepted/current
public English P1.6 anchors validated read-only under the new guard. The full
strict-warning suite passed 642 tests, and Ruff passed. No accepted artifact was
regenerated or re-reviewed, no live model call was made, and I7 remains HOLD.

### Exact-scope diagnosis for the remaining I7 blocker

Read-only inspection of the retained attempt-108 responses and exact public
projection found two distinct causes. The model omitted applicable `familiarity`
for Tool Calling, RAG and Agentic Frameworks in the required list, and for
Observability and Backend architecture in the preferred list. The model also
returned null or non-depth `experience` phrases for concepts whose exact source
wording expresses prior experience but no recognized technical-depth level. The
v20 validator cannot distinguish these cases when every item cites the same
420- or 1,414-character coverage reference. For example, `practical experience
with LLMs and language model APIs in Python and/or TypeScript` validates with
null depth as an exact item excerpt; citing its 420-character parent fails because
that parent also contains three unrelated `familiarity` markers. Conversely, an
exact `familiarity with Tool Calling / Function Calling` excerpt exposes the
applicable depth. This diagnostic only evaluated existing source excerpts; it
did not assemble or accept an artifact.

Eight of the fourteen multi-marker references in the 27-projection audit also
carry a preferred-obligation signal in their parent span. Narrowing those items
to exact source excerpts often drops the shared preference phrase: in `tvMm`,
`experience building Production-grade Agents` has no `advantage` wording by itself,
while its parent says `It is an advantage if ...`. An item-level repair therefore
needs both an exact claim excerpt for depth/subject scope and an independently
traceable parent context for obligation and coverage. A punctuation or length
split, or simply allowing null on a broad citation, cannot prove both.

Next implementation decision: design a **versioned candidate** representation
that keeps a parent coverage reference and a contiguous exact item excerpt as
separate evidence, validates item depth only within the latter, and proves any
inherited preferred strength from the former. Preserve the full coverage ledger,
public v20/v5 artifacts, review promotion, and Market history. Test the same
mixed-depth case, the accepted `tmBK` counterexample, preferred shared-context
cases, and subject changes before a bounded live evaluation. Do not run the
unchanged v20 `tvMm` command again; it cannot express this distinction. I7 HOLD
remains the honest product result.

### V21 isolated scoped-evidence contract

The first offline implementation of that boundary is now isolated in
`AnalysisRequirementV21`; it is not routed to the current service or provider.
Each candidate requirement retains the parent `evidence` used by the coverage
ledger and adds one mandatory `item_excerpt` that must be an exact contiguous
subspan. English depth validation runs against the item excerpt, while requirement
strength may be proven either by explicit item wording or by the matching parent
coverage hint plus its exact optionality wording. Missing applicable item depth,
an excerpt outside its parent, and a required claim under preferred parent context
all fail closed.

Six focused tests cover the attempt-108 mixed experience/familiarity shape, omitted
item depth, shared preferred context, invalid subject/excerpt scope, the accepted
`tmBK` multi-depth list shape, and removal of candidate-only `item_excerpt` before
the unchanged v5 persistence shape. This proves the representation can express the
needed distinction offline. It does not yet prove provider behavior, whole-artifact
semantic quality, or authorize a live call. Public/current remains v20/v5 and I7
remains HOLD.
