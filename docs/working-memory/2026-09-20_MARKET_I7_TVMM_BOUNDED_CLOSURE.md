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

The isolated provider boundary is also implemented offline. V20 now exposes a
private shared transport hook while its public wrapper still selects exactly
`JobAnalysisResponseV20`; no current routing or identity changed. The v21 wrapper
selects `JobAnalysisResponseV21`, adds an explicit request-runtime marker, and a
v21 provider subclass reuses v20 partition construction, scope checks, deterministic
fact injection, and merge logic. Candidate-only item excerpts are removed before
the inherited v5 whole-artifact validators run. A stubbed provider-boundary test
proves the v21 prompt/response identity reaches the partition, the two scoped
requirements merge, and the returned persistable structure has the unchanged v5
shape. A separate wrapper test proves response-model selection. This remains an
offline candidate: there is no current service builder, CLI route, persistence,
or live inference authorization yet.

The accepted-anchor compatibility check now validates all 85 requirements from
the five current public P1.6 anchors read-only under the candidate contract.
Seventy-eight already have one evidence span suitable as the item excerpt; the
seven `tmBK` requirements sharing its multi-depth list use the corresponding exact
source list items. The replay exposed a casing edge (`CISCO` versus canonical
source `Cisco`), so item excerpts now use the same exact-source equivalence rule
as persisted evidence and retain the canonical parent substring. No accepted
artifact, review status, prompt identity, or currentness state changed.

### First non-persistent v21 evaluation and bounded repair

After the offline provider and accepted-anchor gates passed CI, one v21 evaluation
ran against the unchanged `tvMm` English projection without SQLite or corpus
mutation. It failed after the configured validation retry and created no artifact.
Both responses produced 14 requirement candidates. Seven source items with explicit
`familiarity` still left `depth_signal` null; the generated concepts retained a
leading `Familiarity with ...` wrapper. The second response also cited bare
`Embedding` and `Vector Databases`, which loses the shared marker scope from
`familiarity with RAG, Embedding, and Vector Databases`. Raw protocol and the full
failure remain local.

This result supports one general candidate-only correction. When an exact item
excerpt contains exactly one recognized marker and the generated concept begins
with that same marker, v21 may move the source-proven leading wrapper into
`depth_signal` and retain the remaining subject as the concept. It does not infer
markers for bare items. The v21 prompt now requires a complete shared-marker group
excerpt for each separately emitted member of a coordinated list; reconstructed
phrases and bare members claiming the shared depth still fail. Focused regressions
cover both the safe normalization and the coordinated-list stop line. V20 remains
unchanged and the failed evaluation is not semantic acceptance.

### 2026-09-21 — Candidate evidence-ledger evaluation

A second non-persistent v21 evaluation completed mechanically after the leading-depth
repair, but complete semantic review rejected it. Its one 1,265-character responsibility
reference allowed nine generated duties to satisfy a list that also explicitly required
attention to cost/latency/reliability/output quality and collaboration with Product and
Backend. Its 1,414-character preferred requirement reference combined a required
architecture/real-system statement, a preferred list, company/product goals and
application instructions. This hid the required statement and assigned one preferred
hint to unlike sentences. No artifact, attempt, SQLite row or public corpus state was
created.

The v21 candidate now owns a separate exact-span planner. Mixed-obligation requirement
text is split into exact sentences, direct application instructions terminate candidate
coverage, repeated gerund duty lists become independently mandatory items, and an
explicit collaboration duty remains separate. The accepted v20 planner, prompt, service,
artifact identity and persistence path are unchanged. All five accepted-anchor
requirement plans remain byte-for-byte equal under the candidate planner. Read-only
replay showed the rejected response left six new requirement references and all eleven
duty references uncovered. The implementation was published in `91612d5` with 656
strict-warning tests and complete 394-job corpus verification passing.

The first attempted evaluation after that repair stopped during local provider preflight:
the candidate-only reference IDs had not been added to the transport evidence catalog.
No model request occurred, SQLite remained byte-identical and no validation retry was
spent. The shared transport now accepts an optional exact-source catalog extension;
only v21 supplies it, while v20's model-facing catalog remains unchanged. The regression
proves v21 supplies sentence/item references through this boundary. This integration
repair was published in `61dd926` after the same full gates passed.

One bounded non-persistent evaluation then ran on the unchanged `tvMm` projection and
configured `gemma-4-e4b-it-ud` model. It produced no role purpose, eleven responsibilities,
sixteen requirements (including two deterministic source skill tags), and four coverage
exclusions. Exact item scope corrected every previously observed familiarity/experience
depth defect. All ten explicit duty-list items and the Product/Backend collaboration duty
were present. Company context, the chatbot goal and intended AI-system behavior were
correctly excluded rather than attributed to the candidate. SQLite was byte-identical
before and after the call.

The result is still **semantically rejected**. It excluded the explicit required source
statement that the company needs someone who can move beyond idea/prototype stage and
turn an Agent into a reliable real-product system, claiming preferred experience elsewhere
covered it. That loses required obligation and exact candidate capability. The candidate
planner now marks direct wording such as `we need someone who can`, `the candidate must`,
`you must`, and `you will need to` non-excludable after sentence scoping. Read-only replay
of the retained response fails specifically on that reference. No further model call is
authorized by this evaluation.

A subsequent read-only scan of all 27 current English projections found representative
headingless candidate-experience statements in `t7ck`, `tGM0`, `taku` and `tvMm`.
Their wording covers four general forms: looking for someone with an ability, looking to
attract a role with experience, a role suitable for someone with practical experience,
and conditional `if you have built/worked with` experience. V21 now adds those exact
sentences as required, non-excludable candidate-experience references while rejecting
generic recruiting prose and application directives. The five accepted-anchor requirement
plans remain unchanged. This is offline ledger evidence only; it does not reopen the closed
model evaluation or establish semantic acceptance.

Pushed-head GitHub CI run `35607767525` passed for the headingless-coverage change.
A whole-public-projection transport audit then validated 165 candidate requirement
references, 60 responsibility references and 39 bounded requirement partitions across
all 27 English projections. Every candidate reference resolves to an exact source span;
there are no conflicting IDs, duplicate texts, unknown references or non-source spans.
The audit exposed two duty-list grammar edges. A dependent `including LLMs and Agents`
modifier in `tGM0` was incorrectly split into a standalone duty, while Oxford-comma
`and preparing technical documentation` in `t4qV` remained attached to the preceding
duty. V21 now excludes dependent `including` modifiers as list anchors, recognizes an
independent final `, and <gerund>` item, and preserves coordinated bare-gerund chains
such as `evaluating, debugging, and improving` as one action. Focused regressions cover
both forms; v20 remains unchanged.

The next all-projection semantic audit found candidate-only section leakage beyond the
original `tvMm` case. Benefits, work-location, KPI and task text remained under inherited
requirement sections in `t4EV`, `t4jp`, `tI1n`, `tGc5`, `tmW1` and `takb`; star-bulleted
lists also lost shared preferred scope after an explicit `advantage` transition. V21 now
tracks those exact section transitions, can resume at a later Skills/Expected Skills
heading, splits star items, and carries list/group preference through later items. The
`Points Considered` group in `tGc5` is therefore preferred across all seven clauses, and
the `taOX` statement that work samples significantly affect resume review is represented
as preferred rather than required. V21 validation recognizes that exact application-review
preference signal. Application, benefits, location, KPI and task text no longer enters the
candidate requirement ledger.

This intentionally narrows the v21 candidate plan for accepted anchor `t4jp`, whose prior
single reference included a remote-work resume instruction, location and benefits. Its
accepted v20/v5 artifact, source evidence and currentness are untouched; the candidate now
retains only the actual work/commitment requirements. Four other accepted-anchor candidate
requirement plans remain unchanged.

Candidate duty coverage now also recognizes explicit `Job Description:` and `Tasks:`
sections across `t4EV`, `tI1n` and `tmW1`. It ends responsibility scope at embedded
qualification/benefit/deliverable headings, drops partial heading fragments left by the
v20 parser, separates multi-sentence and semicolon duties, and keeps headingless candidate
duties to the sentence that actually asserts work. Repeated source-explicit base-verb
lists such as `design ..., build ..., connect ...` are independently ledgered. The
exact-span parser preserves parenthetical comma lists, dependent modifiers, coordinated
verb chains and nominal actions before later gerunds. Only one responsibility reference
remains longer than 300 characters: `t4qV`'s single documentation duty with its exact
equipment/technology scope.

At this checkpoint, the repeated 27-projection transport audit validated 173 requirement references, 100
responsibility references and 39 partitions with zero ID collisions, duplicate texts,
unbalanced parenthetical spans, unknown references or non-source spans. No model call or
operational-state mutation was made for these repairs. This complete public-projection
transport check is now a committed regression rather than an ad hoc audit.

Public/current P1.6 remains v20/v5, no v21 artifact was persisted or promoted, and Market
I7 remains **HOLD**. The candidate demonstrated a material improvement in exact depth and
duty coverage, but it did not produce an accepted-semantic core posting or exercise the
accepted-semantic Market snapshot/profile and CLI/browser drill-down.

### Bounded post-ledger evaluation decision — 2026-09-21

Independent evidence now supports one new non-persistent v21 evaluation. The repair was
derived from all 27 projections rather than another `tvMm`-specific prompt patch; 173
requirement references, 100 responsibility references and 39 partitions pass the committed
exact-source/catalog transport audit. The previous candidate's illegal exclusion fails
closed on retained-response replay. Full local gates pass at 674 strict-warning tests, and
pushed-head CI run `35640872667` is green.

Run exactly one direct v21 provider evaluation against the unchanged public `tvMm` English
projection and configured `gemma-4-e4b-it-ud` model. The provider's one bounded validation
retry remains part of this single evaluation. Do not persist an attempt/artifact, change
current v20/v5 routing, mutate SQLite, switch vacancy/model, or auto-accept a mechanically
valid result. Review the complete result against original source meaning, exact depth,
obligation, headingless candidate experience, every duty, and candidate-versus-product
subject. A failed or materially invalid result closes this evaluation without another call.

### Post-ledger evaluation result and retained-response closure

The single authorized call failed after its bounded validation retry and created no
candidate. Both provider responses supplied all eleven exact duty references, the required
reliable-product capability and the first headingless Agent-design experience statement.
The first response also supplied unsupported `practical experience` as technical depth.
Both responses cited exact single-marker `familiarity with ...` item excerpts but left five
corresponding depth fields null. The retry then reasoned incorrectly that familiarity was
not an accepted depth signal. SQLite was byte-identical before and after the call; no
attempt, artifact, corpus or Market state was created.

Exact item scope supports one further deterministic candidate-only correction: when an
item excerpt contains exactly one recognized depth marker, v21 now materializes that exact
source marker even when the generated concept says `Working with X`. Marker-free and
multi-marker excerpts remain fail-closed, and v20 is unchanged. Three independently scoped
non-candidate sentences beginning `Our company is ...`, `Our goal is ...`, and `We want
AI/the system/the product to ...` are also removed from candidate qualification coverage;
a negative regression preserves explicit wording such as `Our company requires candidates
to ...`.

Read-only replay after these repairs rejects the first response for its unsupported
`practical experience` depth. The retry response passes every item-depth, duty, subject and
company/product-context check, but still fails one non-excludable coverage obligation: it
omits the explicit headingless statement `If you have built an Agent ... have worked with
LLMs, Tool Calling, memory, workflows, RAG, and Orchestration`. This is a real semantic
coverage failure, not a bookkeeping defect. Do not run another model call, weaken that
coverage, or hand-assemble a promoted artifact. Current whole-corpus candidate totals are
170 requirement references, 100 responsibility references and 38 partitions; the committed
transport regression remains clean.

I7 remains **HOLD**. No accepted-semantic core posting exists, so the semantic Market
snapshot/profile and accepted-semantic browser/CLI drill-down remain unexercised.

### Headingless candidate-experience partition repair — 2026-09-21

The retained post-ledger response exposed a generation-capacity problem rather than a
coverage-validator defect. The `tvMm` plan had six requirement references in one partition,
but three broad section references expanded into fourteen generated requirements and the same
call also owned all eleven duties. The two explicit headingless candidate-experience references
were last in that partition. Both responses represented the first and silently omitted the
second; the unchanged whole-partition validator correctly rejected the omission.

V21 now isolates references whose source kind is `candidate_experience` from dense section
requirement partitions. These exact statements remain required and non-excludable, but they no
longer compete with broad list decomposition or the first partition's duty output. V20 gained
only a partition-selection hook and still selects its existing partition function, so public
v20 routing and behavior are unchanged. The v21 prompt explicitly identifies a dedicated
candidate-experience partition as mandatory source coverage.

The permanent 27-projection transport regression now also proves exact partition membership,
no duplicate reference assignment, and no mixing of candidate-experience references with other
source kinds. The candidate ledger remains 170 requirement references and 100 responsibility
references; isolated planning increases the bounded requirement-partition total from 38 to 43
across the corpus. Five projections exercise the rule, including the two independent `tvMm`
statements. Focused tests and the complete suite pass at **677 tests with warnings-as-errors**;
Ruff and diff checks pass.

This offline result repairs the identified source-attention boundary but does not prove model
compliance or semantic acceptance. No model call, artifact, SQLite mutation, public routing
change, or I7 status change was made in this increment.

### Bounded isolated-partition evaluation decision — 2026-09-21

The general repair is committed at `0c77097` and pushed-head CI run `35643929027` passed.
This authorizes exactly one direct, non-persistent v21 provider invocation against the unchanged
public `tvMm` English projection and configured `gemma-4-e4b-it-ud` model. The provider's existing
bounded validation correction remains part of that single invocation. The evaluation must not
write an analysis attempt/artifact, change current v20/v5 routing, mutate SQLite, switch vacancy
or model, or automatically accept a mechanically valid response.

Review the complete merged result against every exact requirement and duty reference, source
depth and obligation, candidate-versus-product subject, and the two headingless candidate-
experience statements. Record the operational database digest before and after. A transport,
validation, or semantic failure closes this evaluation without another model invocation.

### Isolated-partition evaluation result

The one authorized direct v21 invocation completed mechanically with 28 merged requirements,
all eleven exact duties, no role-purpose claim and no exclusions. Both headingless candidate-
experience references were represented, so the isolated partition corrected the prior complete
omission. Familiarity depths were exact, preferred requirements remained preferred, the reliable-
product requirement remained present, and no company/product subject leakage recurred.

Complete semantic review still rejects the result:

1. The first headingless statement says the candidate has `real experience in designing and
   developing intelligent Agents and Agentic systems`. The result normalized that fact as a
   generic `skill` named `Design and development ...`, losing the source-explicit experience
   type, even though it separately classified API exposure as experience.
2. The second statement is conjunctive. The result captured building an Agent and prior work with
   LLMs, Tool Calling, memory, workflows, RAG and Orchestration, but omitted the final candidate
   condition about enjoying building systems that understand goals, make decisions, use tools and
   pursue a task to the end. Representing some facts from one parent reference currently satisfies
   aggregate reference coverage, so validation did not expose this partial semantic omission.

The operational SQLite SHA-256 remained exactly
`de1d924e863e5e9a8b6515f4be0694d339666cc7f650716ab80670e988260df2`; integrity is `ok` and
foreign-key checks are empty. The complete request/response evidence remains ignored local data at
`data/local-acceptance/i7/v21-isolated-partition-evaluation.json`. No attempt, artifact, corpus or
Market state was created.

This evaluation is closed. Do not repeat it. The next general repair must preserve distinct
source-explicit facts inside a compound headingless candidate statement rather than treating any
one claim as coverage of the entire parent. It must also preserve explicit prior-experience type.
Prove that boundary across the representative candidate-experience statements before another
model call. Public/current P1.6 remains v20/v5 and I7 remains **HOLD**.

### Compound candidate-fact coverage repair

V21 now derives an exact subclaim checklist inside every `candidate_experience` parent rather
than treating any one extracted claim as coverage of the complete sentence. The splitter uses
source-explicit candidate predicates and preserves coordinated lists: for example, the second
`tvMm` parent requires separate exact coverage of building an Agent, the complete shared
`worked with LLMs ... Orchestration` group, and the goal-directed system-building condition.
Recruiting-result tails such as `then you might be the right fit` are not turned into facts.

Each checklist item remains an exact contiguous subspan of its parent. Items that explicitly
state prior applied exposure (`experience`, `built`, or `worked with`) also require
`concept_type=experience`; ability, capability and motivation items retain semantic model
classification. The checklist is supplied to the model and validated against exact returned
`item_excerpt` values. It adds no deterministic requirement prose and does not relax parent
coverage, evidence, depth or obligation validation.

The representative corpus contains six candidate-experience parents across five jobs. They now
yield ten exact fact items, seven with source-explicit experience type. The permanent 27-projection
audit verifies that every item is unique within its parent and an exact source subspan. Read-only
replay of the rejected isolated-partition response now fails for the omitted `real experience`
Agent-design item, the unpreserved shared `worked with` group, and the omitted goal-directed
system-building condition. A separate regression rejects converting exact experience into a
generic skill.

Validation passes at **680 tests with warnings-as-errors**, Ruff is clean, and the complete
394-job public corpus verifies. No model call or operational-state mutation occurred in this
repair. Public/current v20/v5 and I7 HOLD remain unchanged.

### Bounded compound-fact evaluation decision

The compound-fact repair is committed at `1f57a72`, and pushed-head CI run `35646299619`
passed. This independent five-job evidence authorizes one direct non-persistent v21 invocation
against the unchanged public `tvMm` projection and configured `gemma-4-e4b-it-ud` model. Existing
provider validation correction is part of this single invocation.

The result must preserve every exact candidate fact, including explicit experience type, the
shared `worked with` technology scope and the goal-directed system-building condition, in addition
to all previously reviewed depth, obligation, duty and subject boundaries. Do not persist, change
v20/v5 routing, mutate SQLite, switch vacancy/model, or auto-accept. Any transport, validation or
semantic failure closes this evaluation without another invocation.

### Compound-fact evaluation result

The one authorized invocation failed after its bounded validation retry and created no candidate.
Both retained candidate-partition responses represented all five exact `tvMm` checklist items,
including the two explicit experience types, the complete shared `worked with` technology group,
and the goal-directed system-building condition. The semantic omission exposed by the preceding
evaluation did not recur.

The responses nevertheless used each checklist item's exact text in both `evidence` and
`item_excerpt`. V21 requires durable `evidence` to remain the supplied parent coverage text, so
both non-excludable parent references appeared uncited and the validator rejected the partition.
The retry recognized the parent IDs in its reasoning but repeated the same shape. This is an
instruction/transport representation mismatch, not authorization to accept missing parent
provenance or persist item excerpts as replacement evidence.

SQLite remained byte-identical at
`de1d924e863e5e9a8b6515f4be0694d339666cc7f650716ab80670e988260df2`; integrity is `ok` and
foreign-key checks are empty. Raw protocol evidence remains ignored locally at
`data/local-acceptance/i7/v21-compound-fact-evaluation.json`. This evaluation is closed.

The next bounded repair is deterministic and candidate-only: when `evidence` and `item_excerpt`
both equal one exact checklist item that maps to one unique supplied parent, restore that exact
parent as durable evidence before normal validation. Ambiguous, reconstructed or unknown items
must continue to fail closed. Prove the retained responses and negative cases offline before any
new model call. Public/current v20/v5 and I7 HOLD remain unchanged.

### Unique candidate fact-parent restoration

V21 now restores durable parent evidence only when a generated requirement uses the same exact
checklist item for both `evidence` and `item_excerpt` and that item belongs to exactly one supplied
parent. The exact item remains candidate-only validation scope; the full source parent remains the
persistable evidence. Unknown items, reconstructed wording and one item shared by multiple parents
receive no repair and continue through normal fail-closed validation.

Read-only replay of the first retained compound-fact response now validates all five candidate
items with their two exact parents restored: four remain `concept_type=experience`, and the
goal-directed system-building preference remains `other`. A negative regression with the same
item under two parents proves that ambiguous ownership is not guessed. This resolves the observed
transport-shape mismatch without generating any requirement, changing semantic classification or
weakening coverage.

Validation passes at **682 tests with warnings-as-errors**, Ruff is clean, and the 394-job public
corpus verifies. No model call or operational-state mutation occurred in this repair. Public/current
v20/v5 and I7 HOLD remain unchanged.
