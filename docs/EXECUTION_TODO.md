# JobHunter Execution TODO

**Status:** Active working checklist  
**Date:** 2026-08-03  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, active phase plans, and `docs/ROADMAP.md`  
**Purpose:** Convert the roadmap into bounded next actions without turning the proposal library into an unbounded implementation backlog.

---

## 1. How to use this file

This file is the operational checklist for building JobHunter from the current state.

Rules:

- Do not skip a prerequisite gate because a later feature looks attractive.
- A checked implementation task is not automatically accepted; acceptance evidence is separate.
- Do not pull future proposal work forward unless the current phase explicitly promotes it.
- Keep tasks bounded enough that one task can be validated and reverted independently.
- Prefer one coherent vertical increment over framework work with no current user path.
- When a real defect changes a contract or exposes a new failure class, add a regression task before continuing.
- Keep proposal IDs as traceability references, not as ticket count.
- For job capability depth, prefer incomplete-but-defensible profiles over complete-looking technical curricula unsupported by vacancy evidence.

Status vocabulary:

```text
[ ] not started
[~] in progress / implementation exists but acceptance incomplete
[x] accepted or documentation task completed
[!] blocked / defect must be resolved before dependent work
[-] deliberately deferred
```

---

# A. Pre-building governance and consistency

## A0 — Roadmap and execution setup

- [x] A0.1 Create `docs/ROADMAP.md` from the current implementation, controlling plans, proposal library, and external design lessons.
- [x] A0.2 Create this `docs/EXECUTION_TODO.md`.
- [~] A0.3 Reconcile `docs/PRODUCT_SPECIFICATION.md` with the current implemented-pending-acceptance P1.6/Market/browser state.
- [~] A0.4 Reconcile `docs/ARCHITECTURE.md` with the current analysis/lifecycle/Market implementation.
- [x] A0.5 Reconcile README/current-status navigation after roadmap/governance activation on `main`.
- [x] A0.6 Add roadmap/TODO links to contributor reading/navigation without creating an authority conflict.
- [x] A0.7 Keep the 200-item proposal library non-controlling; no proposal is automatically moved into implementation scope.
- [x] A0.8 Formalize job-specific capability requirement/depth intelligence across product, domain, roadmap, implementation plan and this checklist without creating new proposal IDs or pulling Phase-2 code ahead of the Phase-1 gate.

**A0 done when:** the repository presents one consistent current-state model and future planning has one strategic roadmap plus one current checklist.

---

# B. Immediate Phase-1 stabilization and acceptance

The sequence below follows the controlling master/Phase-1 plans. Do not start Phase 2 until the Phase-1 gate passes.

## B1 — Deterministic baseline and migration safety

- [ ] B1.1 Pull/use the latest accepted `main` state and record the baseline commit for the acceptance run.
- [ ] B1.2 Run `ruff check .` and classify findings by root cause rather than fixing cascades independently.
- [ ] B1.3 Run the full `pytest` suite offline.
- [ ] B1.4 Run `pytest -W error`.
- [ ] B1.5 Confirm core schema migration executes before translation/analysis repositories query modern columns/tables.
- [ ] B1.6 Add/retain migration tests for legacy SQLite states used by real local data.
- [ ] B1.7 Verify migration preserves all source evidence, semantic versions, fetch observations and historical translation artifacts.

**Acceptance:** Ruff green, tests green, warnings-as-errors green, legacy migration tests green.

## B2 — Real database migration gate

- [ ] B2.1 Back up the real local SQLite/evidence workspace before opening it with the new schema.
- [ ] B2.2 Open/migrate the real database only after B1 is green.
- [ ] B2.3 Confirm historical v1 translation artifacts remain present.
- [ ] B2.4 Confirm v1 artifacts no longer resolve as current v2.
- [ ] B2.5 Verify discovered postings, versions, fetch observations, user triage and current source data counts remain plausible before/after migration.
- [ ] B2.6 Record any migration discrepancy as a blocking defect and regression fixture before proceeding.

**Acceptance:** real workspace migrates non-destructively and all expected historical/current state is explainable.

## B3 — Translation-v2 repair and quality gate

- [ ] B3.1 Repair one previously corrupted/affected job to `english-projection-v2`.
- [ ] B3.2 Manually inspect every translated field and source association.
- [ ] B3.3 Repair a second affected job with materially different text/structure.
- [ ] B3.4 Inspect the second job manually.
- [ ] B3.5 Expand repair to the wider parsed corpus in bounded batches.
- [ ] B3.6 Confirm source evidence/history never changes because translation succeeds/fails.
- [ ] B3.7 Confirm native-English strings produce identity projections without model calls.
- [ ] B3.8 Add a small reviewed Persian/mixed-language golden translation set if the current acceptance exposes model-quality ambiguity beyond deterministic integrity checks. `B011`.

**Acceptance:** current v2 projection is trustworthy for the accepted Phase-1 corpus scope; historical v1 remains historical.

## B4 — P1.6 one-job live semantic acceptance

- [ ] B4.1 Select one reviewed current v2 job with clear responsibilities and mixed requirement strengths.
- [ ] B4.2 Run P1.6 once.
- [ ] B4.3 Inspect every role-purpose claim.
- [ ] B4.4 Inspect every responsibility.
- [ ] B4.5 Inspect every requirement concept/type.
- [ ] B4.6 Verify every evidence excerpt is an exact authoritative source excerpt.
- [ ] B4.7 Verify preferred/contextual wording is not inflated to required.
- [ ] B4.8 Verify unsupported technologies/concepts are omitted/rejected.
- [ ] B4.9 Rerun and confirm exact artifact reuse under the same source/model/prompt/schema identity.
- [ ] B4.10 Change one analytical contract component in an isolated test and confirm historical artifact identity is not silently reused as current.

**Acceptance:** one complete real job is semantically acceptable and reproducible.

## B5 — Representative P1.6 batch acceptance (`B187`)

Do not simply analyze the next five IDs.

- [ ] B5.1 Define a deterministic/reviewed small-sample rule covering available variation in role family/title.
- [ ] B5.2 Include multiple companies where possible.
- [ ] B5.3 Include Persian/mixed/native-English variation where available.
- [ ] B5.4 Include both short and long descriptions.
- [ ] B5.5 Include jobs with different requirement density and strength wording.
- [ ] B5.6 Include at least one known/likely edge case plus some ordinary/random examples.
- [ ] B5.7 Analyze the bounded sample.
- [ ] B5.8 Record false positives, false negatives, evidence mismatch, type/strength mistakes and model failure classes.
- [ ] B5.9 Convert every repeatable failure class into an offline regression fixture.

**Acceptance:** reviewed sample supports bounded expansion or identifies a contract change that must be resolved first.

## B6 — Current Market truthfulness (`B087`, `B190`)

- [ ] B6.1 Show exact analyzed-current sample size.
- [ ] B6.2 Show source/filter scope.
- [ ] B6.3 Show current analysis contract identity where operationally useful.
- [ ] B6.4 Add deterministic small-sample warning when broad market conclusions are not justified.
- [ ] B6.5 Add concentration warning/visibility when the analyzed subset is dominated by too few employers/role patterns where feasible.
- [ ] B6.6 Keep required/preferred/contextual/inferred counts separate.
- [ ] B6.7 Confirm one requirement contributes at most once per job to job-prevalence counts unless the metric explicitly counts claims.
- [ ] B6.8 Add a compact corpus-health view if current navigation cannot otherwise explain discovered/detail/parsed/v2/analyzed coverage.

**Acceptance:** Market cannot be mistaken for complete-market truth and every metric has a defensible denominator.

## B7 — Source failure/lifecycle regression hardening (`B118`, `B120`)

Encode these as deterministic tests/fixtures where the current source boundary supports them:

- [ ] B7.1 Network failure -> operational failure, not `expired`/`removed`.
- [ ] B7.2 429 -> rate-limited/retryable policy, not empty result or removed job.
- [ ] B7.3 500 -> server error, not expired.
- [ ] B7.4 502 -> server error, not expired.
- [ ] B7.5 503 -> server error, not expired.
- [ ] B7.6 504 -> server error, not expired.
- [ ] B7.7 challenge/CAPTCHA-like content -> challenge, no blind retry.
- [ ] B7.8 auth redirect/login wall -> auth/access state, not missing vacancy.
- [ ] B7.9 first 404/410 -> `possibly_unavailable`, not immediate destructive removal.
- [ ] B7.10 repeated strong 404/410 evidence -> transition only under the defined lifecycle rule.
- [ ] B7.11 explicit employer expiry -> stronger than inferred unavailability.
- [ ] B7.12 provider/source exception -> failure result, not legitimate `0 jobs` result.
- [ ] B7.13 unexpected HTML/content type -> explicit unexpected/error class and inspectable evidence policy.

**Acceptance:** source uncertainty never silently becomes false market/lifecycle certainty.

## B8 — Unicode/identity regression hardening

- [ ] B8.1 Review source/search/company/title normalization for non-Latin text.
- [ ] B8.2 Add Persian/Arabic Unicode normalization fixtures relevant to JobHunter.
- [ ] B8.3 Verify normalization cannot collapse distinct non-Latin company/title identities to empty/generic identifiers.
- [ ] B8.4 Verify zero-width spacing normalization is limited to contexts where semantic identity remains safe.
- [ ] B8.5 Add property-based tests only if hand-written cases expose a wider normalization state space worth generating. `B119`.

## B9 — Model chaos and untrusted-content tests (`B121`, `B178`, `B179`)

- [ ] B9.1 Valid JSON + fabricated evidence excerpt -> reject.
- [ ] B9.2 Valid JSON + parser metadata used as employer evidence -> reject.
- [ ] B9.3 Valid JSON + unsupported new concept -> reject or omit under contract.
- [ ] B9.4 Inferred concept without rationale -> reject.
- [ ] B9.5 Extra fields/shape violations -> reject.
- [ ] B9.6 Truncated structured output -> explicit failure/recovery policy, no partial artifact.
- [ ] B9.7 Duplicate/contradictory claims -> define/test current allowed/rejected semantics.
- [ ] B9.8 Employer text containing `SYSTEM:`, `ignore previous instructions`, or similar prompt-injection strings remains inert source data.
- [ ] B9.9 Employer text instructing the model to mark the candidate qualified cannot create personal/readiness state.
- [ ] B9.10 Critical invariants are enforced by application validation/tests, not only by prompt wording.

## B10 — Rich operation result and partial-success semantics (`B102`, `B104`)

For every multi-stage browser/CLI workflow, define and expose at least:

```text
requested
attempted
completed
reused
skipped intentionally
failed
remaining eligible
```

- [ ] B10.1 Ensure a stage with partial failures cannot be summarized as simple success.
- [ ] B10.2 Ensure successful immutable work is retained when later stages fail.
- [ ] B10.3 Link operation results to affected/failed jobs where practical.
- [ ] B10.4 Distinguish `no eligible work` from `attempt failed`.
- [ ] B10.5 Keep browser result semantics consistent with CLI/service summaries.
- [ ] B10.6 Add tests for mixed success/failure workflow summaries.

## B11 — Finish P1.3/P1.5 acceptance

- [ ] B11.1 Complete representative source-response classification fixtures/live examples.
- [ ] B11.2 Add/verify last-successful-check summary.
- [ ] B11.3 Add/verify consecutive-failure summary.
- [ ] B11.4 Validate lifecycle UI states against real source history.
- [ ] B11.5 Validate user triage remains separate from source truth.
- [ ] B11.6 Validate missing-detail priority is never presented as personal fit/readiness.
- [ ] B11.7 Keep repost/near-duplicate handling deferred until enough corpus evidence exists, unless current statistics require it before acceptance.

## B12 — Finish P1.7 complete run/reporting

- [ ] B12.1 Finalize per-job analysis/report view with source/English/model provenance.
- [ ] B12.2 Add operation result links to newly fetched/transformed/analyzed jobs.
- [ ] B12.3 Build bounded ready-job analysis queue.
- [ ] B12.4 Build combined current-corpus Phase-1 report.
- [ ] B12.5 Implement final bounded `jobhunter run` orchestration.
- [ ] B12.6 Implement browser equivalent using the same services.
- [ ] B12.7 Report source/translation/analysis partial failures without hiding successful durable work.
- [ ] B12.8 Prove rerun/idempotency behavior.
- [ ] B12.9 Run deterministic end-to-end acceptance.
- [ ] B12.10 Run bounded live end-to-end acceptance.

## B13 — Phase-1 closure

- [ ] B13.1 Write/refresh an acceptance summary with exact accepted corpus/sample/bounds.
- [ ] B13.2 Update README/product/architecture/current-status docs to accepted Phase-1 reality.
- [ ] B13.3 Mark remaining non-capabilities explicitly.
- [ ] B13.4 Freeze/identify the accepted P1.6 contract used as the starting Phase-2 evidence source.
- [ ] B13.5 Do not begin Phase 2 until all blocking Phase-1 acceptance defects are resolved.

---

# C. Phase 2 — Canonical market intelligence

## C1 — Phase-2 design slice

- [ ] C1.1 Define the minimum canonical concept schema actually needed for queries/aggregation and job capability profiles.
- [ ] C1.2 Define stable IDs, type, display name, aliases, status and history.
- [ ] C1.3 Define broad/narrow capability and sub-capability relations separately from aliases.
- [ ] C1.4 Define prerequisite relations separately from market co-occurrence.
- [ ] C1.5 Define mapping provenance/review/supersession.
- [ ] C1.6 Define unknown/unmapped handling.
- [ ] C1.7 Define taxonomy version/current-resolution semantics.
- [ ] C1.8 Define acceptance examples before bulk migration/mapping.

## C2 — Canonical responsibilities and deliverables

- [ ] C2.1 Preserve original P1.6 responsibility claims.
- [ ] C2.2 Map reviewed claims to canonical responsibilities.
- [ ] C2.3 Add responsibility families only after examples demonstrate useful grouping.
- [ ] C2.4 Add deliverables where employer evidence supports them.
- [ ] C2.5 Preserve responsibility action/object/context/outcome where useful for capability inference.
- [ ] C2.6 Link responsibilities/deliverables to canonical capabilities only with reviewable provenance.
- [ ] C2.7 Count postings and distinct employers separately.

## C3 — Job capability requirement and depth intelligence

This is the first-class Phase-2 capability that answers not merely `Docker/Python/ML required?`, but **what the employee must know, understand and be able to do with that capability for this job**.

### C3.1 Contract and identity

- [ ] C3.1.1 Define/version `JobCapabilityRequirementProfile` identity by job source semantic version + taxonomy/profile contract.
- [ ] C3.1.2 Preserve canonical capability and exact employer wording separately.
- [ ] C3.1.3 Preserve required/preferred/contextual/inferred strength exactly from accepted source analysis.
- [ ] C3.1.4 Define immutable/history behavior when the profile contract changes.
- [ ] C3.1.5 Do not reuse the Phase-3 personal 0–7 scale as the job requirement schema.

### C3.2 Evidence-qualified technical scope

- [ ] C3.2.1 Extract/link expected work activities from accepted responsibilities.
- [ ] C3.2.2 Extract/link expected deliverables where supported.
- [ ] C3.2.3 Represent technical sub-capabilities/features required to perform those activities.
- [ ] C3.2.4 Represent underlying knowledge/practices where they are explicit or defensibly inferred prerequisites.
- [ ] C3.2.5 Preserve broad-to-narrow capability relationships without confusing them with aliases.
- [ ] C3.2.6 Preserve tool-versus-underlying-capability relations. `B028`.
- [ ] C3.2.7 Keep prerequisite relations distinct from co-occurrence. `B024-B028`.

### C3.3 Depth dimensions

- [ ] C3.3.1 Preserve employer-stated depth wording (`familiarity`, `strong`, `expert`, etc.) without treating it as precise technical truth. `B021`.
- [ ] C3.3.2 Derive work-implied scope/depth from responsibilities and deliverables where evidence supports it.
- [ ] C3.3.3 Represent expected independence/ownership separately from knowledge depth.
- [ ] C3.3.4 Represent complexity/operational/production context separately.
- [ ] C3.3.5 Separate explicit years from experience type/context. `B022`.
- [ ] C3.3.6 Keep employer seniority labels separate from inferred work-seniority signals. `B023`.
- [ ] C3.3.7 Add a single summary depth category only if reviewed examples prove it stable/useful; the multidimensional profile remains primary.

### C3.4 Evidence status and uncertainty

For every fine-grained expectation preserve one of:

```text
source_explicit
strongly_implied_by_work
model_inferred_prerequisite
unknown_or_unsupported
```

- [ ] C3.4.1 Define deterministic persistence/validation for these states.
- [ ] C3.4.2 Require evidence + rationale for every model-inferred prerequisite.
- [ ] C3.4.3 Never display work-implied/inferred sub-capabilities as direct employer wording.
- [ ] C3.4.4 Preserve `unknown_or_unsupported` rather than filling gaps from generic model knowledge.
- [ ] C3.4.5 Keep confidence field-specific rather than assigning one confidence to the whole job/profile.

### C3.5 Company/product/team context

- [ ] C3.5.1 Use company/product/team context only when present in source or approved reviewed evidence.
- [ ] C3.5.2 Link context to the specific capability interpretation it supports.
- [ ] C3.5.3 Add explicit regression cases preventing stereotypes such as `startup -> must own everything` from manufacturing requirements.

### C3.6 Representative reviewed examples

Build the first acceptance set intentionally rather than selecting adjacent jobs only:

- [ ] C3.6.1 Broad programming language example such as Python.
- [ ] C3.6.2 Operational tool/platform example such as Docker or Linux.
- [ ] C3.6.3 Broad knowledge domain example such as Machine Learning.
- [ ] C3.6.4 Library/framework example such as NumPy or FastAPI.
- [ ] C3.6.5 Vague technology-only requirement where correct output contains substantial unknown scope.
- [ ] C3.6.6 Responsibility-rich vacancy where work evidence adds technical scope absent from the skill list.
- [ ] C3.6.7 Multiple employers/role patterns.
- [ ] C3.6.8 Persian/mixed/native-English variation where available.

### C3.7 Quality review and regression

For each reviewed profile record:

- [ ] C3.7.1 missed required activities;
- [ ] C3.7.2 unsupported sub-capabilities;
- [ ] C3.7.3 inflated/understated depth;
- [ ] C3.7.4 incorrect independence/ownership;
- [ ] C3.7.5 incorrect production/complexity context;
- [ ] C3.7.6 company-context overreach;
- [ ] C3.7.7 prerequisite overreach;
- [ ] C3.7.8 evidence-status mistakes;
- [ ] C3.7.9 unknown scope incorrectly filled;
- [ ] C3.7.10 convert every repeatable failure into an offline regression/model-chaos fixture.

### C3.8 Job-level capability profile UX

- [ ] C3.8.1 Show capability + employer strength/wording.
- [ ] C3.8.2 Show supported activities/sub-capabilities.
- [ ] C3.8.3 Show expected independence/context where supported.
- [ ] C3.8.4 Show explicit/work-implied/inferred badges distinctly.
- [ ] C3.8.5 Show unknown/unsupported technical scope explicitly.
- [ ] C3.8.6 Link every material expectation to supporting responsibility/deliverable/source evidence.
- [ ] C3.8.7 Keep JobHunter interpretation visually separate from employer wording.

**C3 acceptance:** JobHunter can describe what selected jobs actually require a person to do with important capabilities without inventing a universal technology curriculum or hiding uncertainty.

## C4 — Role archetypes

- [ ] C4.1 Generate candidate archetypes from accepted responsibilities/requirements/capability profiles, not title alone.
- [ ] C4.2 Review archetype definitions and boundaries manually.
- [ ] C4.3 Attach representative jobs.
- [ ] C4.4 Preserve hybrid/unmapped jobs.
- [ ] C4.5 Use recurring activity/depth patterns only after C3 profiles are credible.
- [ ] C4.6 Add Role DNA/title mismatch only after archetype quality is credible. `B017`, `B018`.

## C5 — Market matrices and quality

- [ ] C5.1 Concept demand by posting count.
- [ ] C5.2 Concept demand by distinct-employer count. `B193`.
- [ ] C5.3 Required/preferred/contextual/inferred distribution.
- [ ] C5.4 Responsibility-family prevalence.
- [ ] C5.5 Role/archetype segmentation.
- [ ] C5.6 Recurring work activities per capability.
- [ ] C5.7 Recurring sub-capabilities only with explicit minimum support/coverage.
- [ ] C5.8 Employer-stated vs work-implied depth patterns kept separate.
- [ ] C5.9 Independence/ownership and operational-context distributions only where evidence coverage is adequate.
- [ ] C5.10 Explicit/work-implied/inferred distributions for fine-grained capability expectations.
- [ ] C5.11 Co-occurrence with explicit sample sizes. `B024`.
- [ ] C5.12 Capability-bundle candidate generation only with minimum support thresholds. `B025`.
- [ ] C5.13 Duplicate-adjusted statistics only after duplicate identity is reliable. `B192`.
- [ ] C5.14 Sampling warnings remain visible for every filtered view. `B190`.
- [ ] C5.15 Add outlier/corpus-diversity views only if they improve quality review or acquisition decisions. `B188`, `B189`.

## C6 — Review, lineage and reversibility

- [ ] C6.1 Decide whether P1.6 claim correction is needed based on real correction frequency. `B009`.
- [ ] C6.2 If yes, preserve original model output and append reviewed correction.
- [ ] C6.3 Add taxonomy mapping review.
- [ ] C6.4 Add capability-profile review for individual activities/sub-capabilities/evidence status/depth/context without rewriting source/P1.6 history.
- [ ] C6.5 Keep every market aggregate drillable to supporting jobs/claims/profile expectations.
- [ ] C6.6 Implement lineage identifiers sufficient for later Evidence Inspector/Trace views. `B007`, `B008`, `B145`, `B149`.
- [ ] C6.7 Avoid building a graph database for lineage.

## C7 — Phase-2 quality gate

- [ ] C7.1 Canonical mappings reviewed on representative examples.
- [ ] C7.2 Aggregate counts reproducible from accepted artifacts.
- [ ] C7.3 Alias mapping does not double-count jobs.
- [ ] C7.4 Role archetypes have reviewed boundaries/examples.
- [ ] C7.5 Every market metric exposes sample/source/filter scope.
- [ ] C7.6 Job-level evidence drill-down remains intact.
- [ ] C7.7 Capability requirement/depth profiles have reviewed examples across broad languages, tools/platforms, knowledge domains and libraries/frameworks.
- [ ] C7.8 Fine-grained technical scope is evidence-supported rather than generic model knowledge.
- [ ] C7.9 Explicit/work-implied/inferred/unknown boundaries remain inspectable.
- [ ] C7.10 Vague employer adjectives do not become fake exact depth.
- [ ] C7.11 Unknown technical scope remains unknown.
- [ ] C7.12 Job-side depth model remains distinct from personal evidence depth.

---

# D. Multi-source expansion

## D1 — Select second source

- [ ] D1.1 Write one-page source value/policy note.
- [ ] D1.2 Prefer official API/feed/public ATS.
- [ ] D1.3 Define exact hosts/paths, bounds and permission assumptions.
- [ ] D1.4 Define stable identity and source-specific lifecycle semantics.
- [ ] D1.5 Define fields that cannot be normalized without loss.

## D2 — Implement second source vertically

- [ ] D2.1 Discovery.
- [ ] D2.2 Raw evidence.
- [ ] D2.3 Stable identity.
- [ ] D2.4 Detail acquisition.
- [ ] D2.5 Failure classification.
- [ ] D2.6 Parsing/normalization.
- [ ] D2.7 Semantic versioning.
- [ ] D2.8 English/analysis downstream compatibility where required.
- [ ] D2.9 Deterministic tests.
- [ ] D2.10 Bounded live acceptance.

## D3 — Extract minimal source adapter contract (`B170`)

- [ ] D3.1 Compare actual Jobinja and second-source differences.
- [ ] D3.2 Define common capability flags/operations only for shared real needs.
- [ ] D3.3 Keep source-specific logic close to its adapter.
- [ ] D3.4 Do not implement dynamic third-party plugin loading yet.

## D4 — Source/search effectiveness

- [ ] D4.1 Track unique contribution by search/source.
- [ ] D4.2 Track acquisition failure separately from zero results.
- [ ] D4.3 Track downstream analyzed/reviewed relevance when available.
- [ ] D4.4 Generate catalog/source suggestions for human review; never auto-mutate search strategy.
- [ ] D4.5 Add parser/source drift warnings from measured baselines when enough history exists. `B158`, `B161`.

---

# E. Phase 3 — Personal Evidence Platform

## E1 — Data ownership/privacy entry gate

- [ ] E1.1 Define system/public/user-workflow/personal/private/secret/rebuildable data classes.
- [ ] E1.2 Define which stores are canonical.
- [ ] E1.3 Define local vs remote AI processing policy per class.
- [ ] E1.4 Define export policy.
- [ ] E1.5 Define retention/deletion policy.
- [ ] E1.6 Implement/test backup/restore before storing irreplaceable personal evidence.

## E2 — Manual Personal Evidence Ledger

- [ ] E2.1 PersonalCapability schema.
- [ ] E2.2 CapabilityEvidence schema.
- [ ] E2.3 Depth state.
- [ ] E2.4 Confidence separate from depth.
- [ ] E2.5 Recency/freshness.
- [ ] E2.6 Limitations/context.
- [ ] E2.7 Review state/history.
- [ ] E2.8 AI-assistance/independence evidence metadata.
- [ ] E2.9 Manual create/edit/review UI.
- [ ] E2.10 Provenance and backup tests.

## E3 — Evidence interpretation discipline

- [ ] E3.1 No capability from chat memory alone.
- [ ] E3.2 No capability from repository dependency names alone.
- [ ] E3.3 No automatic mastery from project completion.
- [ ] E3.4 No automatic independent execution from AI-assisted implementation.
- [ ] E3.5 Preserve explicit `unassessed/unknown`.
- [ ] E3.6 Preserve evidence limitations visibly.

## E4 — GitHub/project evidence candidates (`B043`)

Only after manual schema proves itself:

- [ ] E4.1 User explicitly selects repositories/projects.
- [ ] E4.2 Import observable facts, not proficiency claims.
- [ ] E4.3 Generate evidence candidates.
- [ ] E4.4 Require user review/confirmation for ownership/decisions/debugging/independence claims.
- [ ] E4.5 Keep private-repo access explicit and minimized.

## E5 — Market-to-person mapping

- [ ] E5.1 Exact concept mapping.
- [ ] E5.2 Broader/narrower/partial mapping types.
- [ ] E5.3 Map personal evidence to job-required activities/sub-capabilities where justified.
- [ ] E5.4 Preserve the distinction between general technology evidence and evidence for one job-specific activity.
- [ ] E5.5 Review corrections.
- [ ] E5.6 Evidence reuse across jobs without universalizing job-specific sufficiency. `B054`.

## E6 — Phase-3 gate

- [ ] E6.1 No personal claim without evidence.
- [ ] E6.2 Depth/confidence/recency preserved.
- [ ] E6.3 AI-assistance context representable.
- [ ] E6.4 Backup/restore proven.
- [ ] E6.5 Market-person mappings reviewable.
- [ ] E6.6 Broad concept matches do not silently satisfy every job-specific activity/sub-capability.
- [ ] E6.7 No gap/readiness output yet claims more than the evidence supports.

---

# F. Phase 4 — Gap, readiness, learning and action intelligence

## F1 — Gap model

- [ ] F1.1 Knowledge gap.
- [ ] F1.2 Practice gap.
- [ ] F1.3 Depth gap.
- [ ] F1.4 Integration gap.
- [ ] F1.5 Production-evidence gap.
- [ ] F1.6 Recency gap.
- [ ] F1.7 Presentation/evidence gap.
- [ ] F1.8 Experience-context gap.
- [ ] F1.9 Constraint mismatch.
- [ ] F1.10 Unknown evidence state distinct from confirmed gap.

## F2 — Requirement-by-requirement and activity-by-activity comparison

- [ ] F2.1 Link each employer requirement to source evidence.
- [ ] F2.2 Link each supported job-required activity/sub-capability to its capability-profile evidence/status.
- [ ] F2.3 Link candidate personal evidence.
- [ ] F2.4 Preserve required/preferred/criticality.
- [ ] F2.5 Preserve required work scope, independence and operational context where known.
- [ ] F2.6 Produce explicit match/partial/gap/unknown state at capability and relevant activity/sub-capability level.
- [ ] F2.7 Allow strong general technology evidence plus a specific missing activity to coexist without contradiction.
- [ ] F2.8 Make every conclusion inspectable.

## F3 — Categorical readiness policy

- [ ] F3.1 Define readable policy rules.
- [ ] F3.2 Support `apply now` / `reasonable` / `prepare` / `major gaps` / `insufficient evidence`.
- [ ] F3.3 Show exactly which rule passed/failed.
- [ ] F3.4 Allow user override without rewriting underlying evidence.
- [ ] F3.5 Do not introduce a global percentage score without calibration evidence.

## F4 — Learning/action priorities

- [ ] F4.1 Market relevance.
- [ ] F4.2 Requirement strength.
- [ ] F4.3 Job-specific activity/sub-capability gap.
- [ ] F4.4 Personal depth/evidence gap.
- [ ] F4.5 Prerequisite dependencies.
- [ ] F4.6 Evidence-building opportunity.
- [ ] F4.7 Prefer targeted missing activities over unnecessary relearning of an entire broad technology.
- [ ] F4.8 `ignore for now` with rationale.
- [ ] F4.9 Explain why the recommendation exists.

## F5 — Gap-to-project/evidence planning

- [ ] F5.1 Generate small bounded project options, not giant flagships by default.
- [ ] F5.2 State targeted capabilities and specific missing activities/sub-capabilities.
- [ ] F5.3 State intended evidence.
- [ ] F5.4 State prerequisites.
- [ ] F5.5 State stop line.
- [ ] F5.6 After completion, compare planned versus actually demonstrated evidence.

## F6 — Career scenarios/constraints

- [ ] F6.1 Target Role Specification.
- [ ] F6.2 Adjacent/excluded roles.
- [ ] F6.3 Geography/work-mode constraints.
- [ ] F6.4 Hard/strong/soft preference strength.
- [ ] F6.5 Multiple scenarios over one evidence base.

## F7 — Challenge/counterfactual later increment

- [ ] F7.1 Challenge optimistic conclusions.
- [ ] F7.2 Challenge overly negative conclusions.
- [ ] F7.3 Show what evidence would change the result.
- [ ] F7.4 Counterfactual capability simulation clearly marked hypothetical.
- [ ] F7.5 Skill/project ROI based on affected gaps, not fake hiring probabilities.

---

# G. Phase 5 — Application and interview workspace

## G1 — Application Evidence Pack

- [ ] G1.1 Freeze job/source/analysis/capability-profile identity.
- [ ] G1.2 Include employer requirements/responsibilities.
- [ ] G1.3 Include job-specific required activities/sub-capabilities/depth context where accepted.
- [ ] G1.4 Include strongest personal evidence.
- [ ] G1.5 Include critical/partial/unknown gaps.
- [ ] G1.6 Include constraints.
- [ ] G1.7 Include relevant projects/examples.
- [ ] G1.8 Include interview-preparation topics.
- [ ] G1.9 Mark pack stale when source/profile/personal evidence changes.

## G2 — Resume targeting

- [ ] G2.1 Every material claim maps to personal evidence.
- [ ] G2.2 No fabricated ownership, metrics, scale, years or technologies.
- [ ] G2.3 AI-assistance/independence limitations remain representable.
- [ ] G2.4 User final approval required.

## G3 — Interview preparation

- [ ] G3.1 Requirement/activity-to-concept matrix.
- [ ] G3.2 Use accepted job capability profiles to identify the technical scope most likely worth preparing, without inventing the employer's hidden interview rubric.
- [ ] G3.3 Best personal example/story components.
- [ ] G3.4 Missing preparation.
- [ ] G3.5 Synthetic self-test questions labelled synthetic.
- [ ] G3.6 No invented company interview process.

## G4 — Application tracker

- [ ] G4.1 Neutral user-owned application states.
- [ ] G4.2 Dates/notes/contacts only as explicitly provided.
- [ ] G4.3 Source lifecycle remains independent.
- [ ] G4.4 Evidence-pack version linked where useful.

## G5 — Outcome learning

- [ ] G5.1 Store outcome.
- [ ] G5.2 Store explicit feedback separately.
- [ ] G5.3 Use `reason unknown` when no reason is supplied.
- [ ] G5.4 Never infer rejection cause from a coincident gap.
- [ ] G5.5 Later aggregate outcome patterns only with explicit causal restraint.

## G6 — Opportunity watch

- [ ] G6.1 Explicit user watch criteria.
- [ ] G6.2 New/changed high-relevance jobs only after accepted comparison model.
- [ ] G6.3 Explain why surfaced.
- [ ] G6.4 User-controlled cadence/noise.

**Permanent:** no autonomous application submission or recruiter messaging.

---

# H. Phase 6 — Sustained repeated operation

## H1 — Durable workflow runs if needed

- [ ] H1.1 Add only if ephemeral operation history is insufficient across restarts.
- [ ] H1.2 Store orchestration state, not duplicate domain truth.
- [ ] H1.3 Preserve partial-success states.
- [ ] H1.4 Resume naturally from durable artifact eligibility.

## H2 — Snapshots and trends

- [ ] H2.1 Snapshot manifests including taxonomy/capability-profile contract identity where applicable.
- [ ] H2.2 Like-for-like period comparison.
- [ ] H2.3 Duplicate/lifecycle-adjusted views.
- [ ] H2.4 Emerging/stable/volatile labels only with transparent thresholds.
- [ ] H2.5 Company/location/work-mode trends only with adequate sample coverage.
- [ ] H2.6 Recurring activity/sub-capability/depth trends only with sufficient like-for-like evidence coverage.
- [ ] H2.7 Career-market drift relative to personal evidence only after both sides are mature.

## H3 — Scheduling

- [ ] H3.1 Schedule only already-idempotent bounded services.
- [ ] H3.2 Respect source/model/privacy limits.
- [ ] H3.3 One clear run history.
- [ ] H3.4 No silent catch-up explosion after downtime/config change.

## H4 — Notifications and briefings

- [ ] H4.1 In-app change summary first.
- [ ] H4.2 Notify only actionable conditions.
- [ ] H4.3 Weekly/monthly briefing from deterministic change sets first, optional synthesis second.
- [ ] H4.4 If nothing meaningful changed, say so.

## H5 — Backup/restore/portability

- [ ] H5.1 Tested backup.
- [ ] H5.2 Tested restore to a clean destination.
- [ ] H5.3 Schema/app version manifest.
- [ ] H5.4 Personal/private data handling.
- [ ] H5.5 Workspace move/import without silent overwrite.
- [ ] H5.6 Desktop packaging only if installation friction becomes a measured usability problem.

---

# I. Advanced AI, retrieval and experimentation — trigger-based only

## I1 — Evaluation Lab foundation

- [ ] I1.1 Translation gold set.
- [ ] I1.2 Gold-job semantic-analysis set.
- [ ] I1.3 After Phase-2 implementation begins, reviewed job capability requirement/depth gold examples spanning broad and narrow capabilities.
- [ ] I1.4 Human annotation format.
- [ ] I1.5 Candidate vs baseline contract runner.
- [ ] I1.6 Metrics for capability profiles: unsupported sub-capabilities, missed activities, depth inflation, evidence-status error, independence/context error, unknown-scope overfill.
- [ ] I1.7 General metrics: unsupported claims, missed claims, strength errors, evidence-validation failures, latency/truncation/cost where relevant.
- [ ] I1.8 Promotion/rollback decision record.

## I2 — Multi-provider/task routing

**Trigger:** a second provider/model has demonstrated measured value.

- [ ] I2.1 Capability-oriented provider boundary.
- [ ] I2.2 Task-specific configuration.
- [ ] I2.3 Persist actual executing provider/model.
- [ ] I2.4 Privacy/data-class routing.
- [ ] I2.5 Fallback policy does not hide provenance.

## I3 — Natural-language structured query

**Trigger:** predefined filters/reports become cumbersome for real analytical questions.

- [ ] I3.1 Bounded intent/query plan.
- [ ] I3.2 Approved read-only query layer.
- [ ] I3.3 Deterministic data result.
- [ ] I3.4 Optional grounded synthesis.
- [ ] I3.5 Query reproducibility for saved/durable decisions.

## I4 — Semantic retrieval/RAG

**Trigger:** reviewed queries demonstrate structured/keyword retrieval is insufficient.

- [ ] I4.1 Build reviewed retrieval test set first.
- [ ] I4.2 Choose chunk/index strategy.
- [ ] I4.3 Keep index derived/rebuildable.
- [ ] I4.4 Version embedding/chunking/retrieval/reranker contracts.
- [ ] I4.5 Evaluate recall/precision before assistant dependence.
- [ ] I4.6 Do not require a separate vector database unless measured need justifies it.

## I5 — Evidence-backed assistant

- [ ] I5.1 Answers about JobHunter use retrieved local evidence.
- [ ] I5.2 Clearly separate JobHunter evidence from generic model explanation.
- [ ] I5.3 Cite/link supporting local records.
- [ ] I5.4 Conversational memory never becomes durable personal truth.
- [ ] I5.5 `insufficient evidence` is valid output.

## I6 — Specialist bounded workers

- [ ] I6.1 Narrow allowed inputs.
- [ ] I6.2 Narrow tools.
- [ ] I6.3 Versioned model/prompt/schema.
- [ ] I6.4 Explicit budget.
- [ ] I6.5 Deterministic validators.
- [ ] I6.6 Human review at authority transitions.
- [ ] I6.7 No unrestricted shell/filesystem/browser/network tools.

---

# J. Explicit non-TODO / rejected-by-default work

Do not create tasks for the following unless a future decision explicitly changes the constraint:

- [-] authenticated LinkedIn/private-platform scraping;
- [-] CAPTCHA/access-control bypass;
- [-] proxy/identity rotation to defeat limits;
- [-] autonomous application submission;
- [-] automatic recruiter messaging;
- [-] cloud accounts/multi-user SaaS architecture;
- [-] microservices/message brokers/Kubernetes for portfolio decoration;
- [-] React/Node rewrite while server-rendered Python remains sufficient;
- [-] graph database because the domain can be drawn as a graph;
- [-] vector database before evaluated retrieval need;
- [-] opaque holistic readiness percentage;
- [-] universal Docker/Python/ML/etc. curricula generated from a single vacancy keyword;
- [-] fake exact job depth derived from words such as `expert`/`strong` without supporting work evidence;
- [-] personal capability from chat memory alone;
- [-] repository technology names treated as proficiency;
- [-] self-training on unverified model generations;
- [-] dozens of source adapters before one second source proves the contract;
- [-] elaborate plugin framework before real extensions require it;
- [-] mobile/native rewrite without a demonstrated repeated-use requirement.

---

# K. Current exact next actions

The current building sequence remains Phase 1; the new capability-depth work is now fully planned but **does not bypass this gate**:

```text
1. Establish deterministic baseline: Ruff + pytest + warnings-as-errors.
2. Resolve any remaining migration-order or schema-compatibility defects.
3. Migrate/inspect the real workspace only after deterministic green.
4. Repair and inspect translation-v2 on affected real jobs.
5. Run and manually inspect one real P1.6 job.
6. Build/select a representative small P1.6 review sample (B187).
7. Convert discovered semantic/model/source failure classes into regression/chaos fixtures.
8. Add/verify Market sampling warnings and corpus coverage truthfulness (B190/B087).
9. Harden source failure/lifecycle cases, especially transient 5xx != expiry.
10. Make full-workflow result semantics explicit for partial success (B102/B104).
11. Finish remaining P1.3/P1.5 acceptance.
12. Finish P1.7 final run/report/browser equivalent.
13. Close Phase 1 with accepted evidence and reconciled docs.
14. Only then start Phase 2 with canonical concepts/responsibilities/deliverables, followed by the reviewed job capability requirement/depth profile slice before using that information for personal gap intelligence.
15. Select/implement one second source under its own roadmap gate; do not let source expansion weaken the Phase-2 semantic model.
```

This sequence is the current working priority. Future sections in this file are not permission to skip it.
