# P1.6 semantic strictness and product-utility refinements — active discussion

**Opened:** 2026-09-24  
**Status:** ACTIVE DISCUSSION / FINDINGS AND PROPOSALS ONLY — NO IMPLEMENTATION APPROVAL  
**Scope:** Evaluate whether current P1.6 generation, validation, review, and whole-result acceptance reject useful source-backed intelligence because of conceptual overlap or disproportionate strictness. Accumulate issues and jointly settle refinements before planning code changes.  
**Working rule:** Record observations, source evidence, interpretations, options, decisions, and unresolved questions separately. Do not silently turn a discussion proposal into a controlling contract.

## Starting context and authority

- [Repository instructions](../../AGENTS.md): maximize useful, decision-relevant intelligence per user time; preserve source integrity; fail soft on interpretive uncertainty; scale strictness with authority and blast radius.
- [Utility/epistemic reasoning policy](../UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md): distinguish source facts from analytical interpretation and candidate output from reviewed/promoted authority; avoid both under-grounded and over-gated product behavior.
- [2026-09-24 v22 post-alias evaluation closure](2026-09-24_P16_V22_POST_ALIAS_EVALUATION_CLOSURE.md): the immediate concrete example, its review outcome, and unresolved preferred-proof-of-work coverage.
- [Rolling working memory](../WORKING_MEMORY.md) and [current-state reconciliation](../CURRENT_STATE_RECONCILIATION_2026-09-12.md): current operational status. This document is a subordinate discussion record and does not supersede them.

**Unchanged operational baseline:** English P1.6 public/current = `job-analysis-english-v21 / job-analysis-v5`; v22 remains an isolated unpromoted candidate; Market I7 remains HOLD. Accepted anchors, semantic promotion rules, Market history, and the stop line on further live generation remain unchanged. No implementation, model call, new acceptance, or authorization to relax an existing gate follows from opening this file.

## Issue R01 — Overlap among capability, practical experience, and proof of ability

### Concrete source/result

For `tvMm` (AI Agent Engineer), an employer expectation says the candidate should be able to **turn an Agent into a reliable system in a real product**. The v22 model produced the concept label `Agent reliability in real product experience`, initially typed as `experience`; v22 changed the ontology to `other` but preserved the phrase. The 2026-09-24 semantic review rejected this as an unsupported assertion of prior experience, and the follow-up guard rejects type-only abstention when experience wording survives. Separately, this source explicitly treats showing/explaining a previously built Agent and supplying a GitHub repository/sample project/demo as valued preferred evidence; the v22 result and requirement ledger omitted that preference. See the v22 closure for precise source/result and comparison-job evidence.

### User's concern / proposed interpretation

Ability to perform complex engineering work and hands-on experience are often closely related; capability, experience, and demonstrable work can legitimately overlap in a job description. A concise generated concept containing `experience` may be a reasonable shorthand for relevant practice rather than an assertion that the employer strictly requires having performed the identical work previously in paid production employment. Automatically treating all such overlap as a fatal error could discard useful information and contribute to repeated whole-analysis failures.

### Refinement identified in discussion (not an approved contract)

1. **Separate the claim from its representation and downstream use.** The source explicitly states a capability expectation. Prior hands-on experience may reasonably support that capability, but the precise requirement of prior professional delivery of that same system is not established by the quoted statement alone. Other parts of the same vacancy may independently state experience or preferred project proof.
2. **Allow non-exclusive concepts and bounded interpretation.** Capability, practice/experience, and evidence of ability need not be forced into a mutually exclusive taxonomy. A source-backed interpretation can describe their relationship if clearly distinguished from employer-authored facts.
3. **Assess semantic materiality and authority, not a keyword alone.** `Agent reliability in real product experience` is ambiguous as a standalone label; it is more consequential if rendered or consumed as a mandatory prior-production-employment condition than as reviewable shorthand. The presence of `experience` alone does not resolve which claim the user or downstream consumer receives.
4. **Prefer a precise source-fact representation plus an optional inference**, e.g. factual expectation: `Ability to turn an Agent into a reliable system in a real product`; associated interpretation: `Relevant hands-on agent/product engineering experience may demonstrate this ability`; preserve separately stated preferred prior-Agent project/demo evidence.
5. **Proportionate failure behavior is a design candidate.** Consider local clarification, lower-authority candidate output, uncertainty marking, or correction of the affected claim instead of rejecting an otherwise useful complete analysis for a non-material wording ambiguity. Do not automatically promote a genuinely unsupported mandatory employer requirement or let uncertain candidate claims silently enter authoritative Market prevalence or personal-readiness conclusions.

### What is and is not established

**Established:** The source's reliable-product wording is a capability expectation; the generated concept is potentially ambiguous; capability and relevant experience can overlap; the observed v22 output lacked separately stated preferred proof-of-work evidence; v22 review rejected the full candidate and I7 remains HOLD.

**Not yet established:** Whether the generated phrase actually causes a harmful user-facing or downstream claim in present code; whether the v22 result could have been safely accepted under the current v5 factual-substrate contract; whether whole-analysis rejection is mandated by an invariant or is an over-broad review policy; whether a lexical guard can safely distinguish material false claims from benign shorthand; whether selective repair/provisional display is feasible without changing authority semantics.

### Questions to resolve before implementation

- Where is `concept` shown or consumed across job detail, review, Capability, and Market? Does `concept_type` change its meaning or downstream treatment?
- Which source-backed distinctions are required for P1.6 factual claims versus allowed only in an explicitly inferred/candidate analytical layer?
- What constitutes a **material** unsupported claim: false mandatory condition, unsupported prior-employment assertion, harmless compressed label, or uncertain implication? Which cases merit item correction, partial display, or whole-result rejection?
- Can one problematic item be isolated without silently losing source coverage, obligation strength, evidence, or accepted-current integrity? What does a useful non-promoted result look like?
- How should explicit preferred work-sample/project proof be covered without misclassifying later application-submission instructions as job qualifications?
- What representative cases, user-facing inspections, and non-regression checks are sufficient before any versioned design/implementation decision?

**Provisional direction:** Preserve explicit source truth and consequence-sensitive validation; revisit over-strict *classification, wording review, and whole-result failure granularity* rather than simply deleting guards. No particular code change, new contract, validator weakening, live generation, or I7 acceptance is decided here.

## Issue R02 — Why the concrete `tvMm` v22 failures happened (source-backed, not yet a repair decision)

### Primary evidence

- [Existing v22 evaluation JSON, fixed commit 0c656fb](https://github.com/motafegh/jobhunter/blob/0c656fba8fe65b8ec6fa38a317a62c5301e7ed54/docs/experiments/2026-09-24_p16-v22-tvmm-case-evidence/evaluation-original.json): the `result.structured` output, both actual `request_body.partition_requests` including evidence catalogs/checklists, and both `raw_response.partitions` are embedded. `result.structured` is the validated/normalized provider result, **not** the untouched raw model result. The 27 validated requirements include 25 model-generated items and two deterministically added source skill tags (`Ai`, `Engineer`); eleven responsibilities are model-generated.
- [Runner at that commit](https://github.com/motafegh/jobhunter/blob/0c656fba8fe65b8ec6fa38a317a62c5301e7ed54/docs/experiments/2026-09-24_p16-v22-tvmm-case-evidence/evaluation-runner.py): one direct evaluation; no persisted analysis artifact or Market mutation.
- [Exact English posting](https://github.com/motafegh/jobhunter/blob/main/corpus/jobs/tvMm/english-projection.json), [v21 evidence planner as executed at effa861](https://github.com/motafegh/jobhunter/blob/effa8616af03f2c11674317e8daade654ac19c5f/src/jobhunter/evidence_refs_v21.py), [v22 prompt](https://github.com/motafegh/jobhunter/blob/effa8616af03f2c11674317e8daade654ac19c5f/src/jobhunter/analysis_service_v22.py), and [v22 normalization](https://github.com/motafegh/jobhunter/blob/effa8616af03f2c11674317e8daade654ac19c5f/src/jobhunter/inference/instructor_lm_studio_v22.py).

### A. Disputed reliable-product experience label: separate model, normalization, and review causes

**Observed:** The source says the person should be able to turn an Agent into a reliable system in a real product. The raw model wrote `Agent reliability in real product experience`, with `concept_type=experience`; validated v22 result changed the type to `other` without changing the wording or `required` strength. Source elsewhere explicitly seeks actual experience designing/building Agents and separately prefers production-grade Agents and demonstrable past work.

**Mechanism:** The v22 prompt explicitly says ontology abstention changes *only* the label and to preserve `concept`. Its Python `mode=before` validator only changes `concept_type`, so any questionable implication in `concept` necessarily survives. The semantic reviewer interpreted the wording as asserting prior experience delivering that exact product-system result and rejected the complete candidate; user and assistant are reopening whether that short label is materially misleading rather than acceptable practical shorthand. The original model's internal reason for choosing the phrase cannot be established from a single output. A later lexical guard against preserving `experience` under type abstention catches this exact pattern but is not evidence that every such label is materially false.

### B. Omitted preferred previous-Agent demonstration / GitHub-project-demo proof: upstream coverage gap

**Observed:** The source says it would be a huge plus to show/explain a previously built Agent and values a real GitHub repository/sample project/demo. Both actual `requirement_coverage` partition lists omit this preference. Partition 2 carries the wording within the *broad, background* `field:description:segment:1` evidence text, but neither partition exposes a requirement-coverage reference for that particular preference. The v22 model therefore had access to the text in background evidence but was not directed to account for it as a candidate qualification; the final requirements omit it. Do not conflate the separate later `To apply ... please send ...` instruction with the earlier preferred proof-of-work qualification.

**Code mechanism identified:** `build_requirement_coverage_plan_v21` extends base coverage by a narrow additional search requiring the same sentence to match both `_CANDIDATE_SUBJECT_RE` and `_CANDIDATE_QUALIFICATION_RE`. Neither `It would be a huge plus if you could show and explain...` nor `A real GitHub repository, sample project, or Demo is very valuable` matches that particular conjunction; the preference appears in the broad duties/intro description area rather than a recognized requirements checklist. This accounts for the absence from v21/v22 requirement planning in this recorded case. It does *not* prove a universal new detection rule is safe. Distinguish prior-work preference from mere application submission instructions across comparison jobs.

### C. Overlapping entries: distinct source assertions and partitioning versus user-facing deduplication

**Observed:** #1 (practical LLM/API experience) overlaps with #16/#19 (prior model-API/LLM exposure); #2 overlaps with #17/#18 (Agent design/building); #3 overlaps with #20 (tool calling familiarity versus having worked with it). The first group comes from the explicit skills/qualification passage in partition 1; the latter comes from introductory candidate sentences in partition 2, with distinct provenance and sometimes distinct strength/type/depth nuances. The two structured skill tags are extra deterministic entries. Source-led extraction and bounded partition accounting explain why multiple distinct records survive. They are not automatically identical or erroneous; no claim of an aggregate double-counting defect is established without inspecting its current deduplication logic.

**Design question:** Can the job-facing experience group and higher-level synthesis consolidate overlapping concepts **while preserving separate source/evidence assertions, optionality and expertise distinctions**, without losing genuine different signals or inflating a count of independent expectations?

### D. Why the whole candidate did not become accepted Market evidence

**Observed:** The provider returned `validated_pending_semantic_review` after passing mechanical validation. The post-hoc semantic review rejected the full candidate for the contested wording, recording the separate preference coverage omission. This direct evaluation never persisted a P1.6 artifact. I7 requires a genuinely valid accepted-current core artifact and complete real semantic drill-down. It does not follow that every generated item was wrong or should be hidden from a clearly labeled candidate-level view.

**Open policy question:** Which of these problems merits item correction, whole-artifact promotion rejection, or candidate-level warning/partial display? This is not solved by changing `concept_type` alone, weakening a validator, or rerunning a model. No broad model-capability conclusion follows from this one case.

## Issue R03 — Source-preserving consolidation of overlapping qualifications

**Discussion decision (2026-09-24):** User agreed with the proposed representation direction. Preserve separately extracted, source-backed statements and their inspectable evidence, but do not force the main job-analysis view to present every statement as an independent qualification. Present related statements in a smaller, intelligible set of qualification groups; expose their underlying evidence and preserve material distinctions, including required versus preferred, familiarity versus applied experience, specific tools/languages and broader scope. A user should be able to expand a group to inspect source statements and qualifiers.

**Concrete `tvMm` examples:** Requirements #1/#16/#19 concern LLMs and model APIs but #1 names Python and/or TypeScript; #2/#17/#18 concern building and designing Agents at different levels of specificity; #3/#20 share tool-calling subject matter but distinguish familiarity from previous use. Grouping these subjects is a presentation/synthesis direction, **not** a claim that their contents, sources or depths are identical. Refer to the fixed [v22 evidence result](https://github.com/motafegh/jobhunter/blob/0c656fba8fe65b8ec6fa38a317a62c5301e7ed54/docs/experiments/2026-09-24_p16-v22-tvmm-case-evidence/evaluation-original.json).

**Counting intent to investigate:** Separate prevalence across *qualified source postings* from the number of extracted statements within a single posting. Repeated employer wording must not, by itself, inflate the number of distinct market demands. Inspect the existing I5 per-posting concept deduplication and Registry/Capability treatment before claiming a counting defect or changing accepted Market semantics.

**Not yet decided:** Whether groups are a derived read model, candidate semantic interpretation, or reviewed/promoted mapping; what grouping confidence, naming, materiality and lifecycle rules apply; whether and how an imperfect candidate analysis can be displayed; grouping versus canonical identity across postings; which existing feature already provides similar functionality; whether any P1.6 schema, acceptance, Market, Capability or UI code changes are warranted. Review existing owners and actual consumers before writing an implementation plan. No automatic merging of evidence records, source loss, obligation/depth weakening, or current acceptance-policy change is authorized.

## Issue R04 — Preserve explicit preferred proof of ability independently from application instructions

**Discussion decision (2026-09-24):** User agreed to recognize explicit employer preferences for demonstrating ability as first-class career intelligence regardless of whether they occur under a formal requirements heading. Keep three distinct meanings: (1) substantive required or preferred qualification, (2) preferred evidence of that qualification or prior work, and (3) directions for submitting an application. Link related evidence preferences to the relevant qualification/group without treating them as mandatory tools, credentials, platforms, or production-employment requirements.

**Concrete `tvMm` case:** The source asks for actual experience designing/building agents; separately says it would be a *huge plus* to show and explain an agent the candidate previously built, and values a real GitHub repository, sample project or demo; later instructs applicants to send a resume and optionally a project or explanation. The first is a substantive qualification, the second is a preferred demonstration/proof-of-ability signal, and the third is application guidance. The recorded v22 result omitted the second because its source passage had no requirement-coverage checklist entry, although it appeared in broad background evidence. See the [English source](https://github.com/motafegh/jobhunter/blob/main/corpus/jobs/tvMm/english-projection.json), [fixed evaluation input and output](https://github.com/motafegh/jobhunter/blob/0c656fba8fe65b8ec6fa38a317a62c5301e7ed54/docs/experiments/2026-09-24_p16-v22-tvmm-case-evidence/evaluation-original.json), and R02 for the observed planner mechanism.

**Representation intent:** Convey both what work the employer expects and how it prefers a candidate to substantiate that work. A project, repository, demo, oral explanation or another expressly stated form of proof must retain its source optionality and alternatives; the existence of a preferred demonstration does not by itself require a public GitHub repository or previous paid production role. Application submission instructions remain separately reviewable and can inform application preparation without becoming additional technical skills or requirements. This can be displayed within an R03 qualification group while retaining separate underlying evidence statements.

**Still open:** Inspect existing product models, source planner, user-facing surfaces, Registry/Capability and Market consumers before selecting a new field, category, grouping relationship, extraction heuristic, or model prompt. Validate the distinction against varied real postings: preferred work samples, mandatory portfolios if explicitly stated, generic submission logistics, and descriptions mentioning projects without a candidate preference. Do not equate every occurrence of `GitHub`, `portfolio`, `project`, `demo`, or `plus` with a proof-of-ability qualification. No code, schema, validator, test, accepted artifact, Market status or new model-run authorization is changed by this discussion decision.

## Discussion ledger

| ID | Topic | Status | Next discussion |
| --- | --- | --- | --- |
| R01 | Capability ↔ experience ↔ demonstrable work overlap; ambiguous concept-label materiality; whole-analysis rejection | First discussion recorded; refinement proposals OPEN | Determine actual downstream consequences and the right claim/authority boundary |
| R02 | `tvMm` source/result/planner/model/normalizer/review failure-layer diagnosis; omitted preference and overlapping entries | Evidence-backed findings recorded; refinements OPEN | Decide proportional treatment and whether source-backed preference coverage must be redesigned |
| R03 | Source-preserving grouping of related qualifications for the job-facing view | **User agreed on design direction**; mechanism and implementation OPEN | Inspect existing grouping/consumers, then specify safe display and counting boundaries |
| R04 | Preferred proof-of-ability evidence versus required qualification and application instructions | **User agreed on design direction**; extraction/representation implementation OPEN | Inspect current schema/consumer ownership; evaluate representative real-posting counterexamples |
| R05+ | Other strictness, failure, coverage, model, and utility issues | NOT YET DISCUSSED | Add separate source-backed entries as discussion continues |

## Change authorization boundary

Keep this file as the active place to append discussion findings and explicit decisions. Do not modify prompts, source, tests, validators, accepted artifacts, Market state, controlling governance/plans, or run the model solely on this record's proposals. When we finish issue review, separately agree on prioritized refinements, owning layers, versioning, tests, and any bounded evaluation authorization under the controlling repository rules.
