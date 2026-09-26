# R03/R04 offline source and consumer audit — 2026-09-26

**Status:** evidence for the active discussion; no extraction, grouping, schema, acceptance, or model contract change.
**Parent:** `2026-09-24_P16_SEMANTIC_STRICTNESS_AND_UTILITY_REFINEMENT_ACTIVE.md`.

## Current consumers and counting

The job-detail browser renders each P1.6 requirement independently with its concept, strength, type, depth and evidence (`src/jobhunter/web/templates/job_detail.html`). The new R05 item-review page likewise addresses exact original items. Capability v9 already groups **accepted** P1.6 facts, preserving their source indexes; it is not a grouping surface for a pending candidate. Thus R03's compact, expandable job-level presentation is not yet provided for pending P1.6.

I5's target Market requirement profile (`src/jobhunter/market_aggregate_service.py::_requirement_profile`) builds one support entry per normalized key *within each posting* before adding the posting to cross-job sets. It retains the supporting claim indexes, strengths, depth signals, and evidence. Repeated claims with the same normalized key therefore do not inflate the posting count. Semantically related but differently worded, unmapped keys can still appear as separate rows; this audit does not establish a counting defect or authorize a taxonomy merge. Any later job-facing group must remain distinct from Market's accepted-current denominator and Registry identity.

## Five public-projection comparison cases

These are **derived English projection** excerpts in `corpus/jobs/<id>/english-projection.json`, not claims that the employer authored this exact English wording. The full projection and original source remain the review authority.

| Job | Observed source distinction | Implication for R04 |
| --- | --- | --- |
| `tvMm` | A statement says it would be a “huge plus” to show and explain a previously built Agent; a repository, sample project **or** demo is valued. Later “To apply” wording asks for a resume and optionally a sample or explanation. | Preferred proof of prior work and application submission are separate; alternatives and optionality matter. |
| `tjgi` | “Having at least one real-world sample” appears in desired qualities; a later scoring section values deployed projects with GitHub or an online demo; the final paragraph asks applicants to send links and project details. | A substantive sample preference can coexist with later submission instructions in one posting. |
| `tI1n` | The requirements heading itself says to submit a resume with Python project samples, while another sentence says the resume/portfolio will be reviewed. | Heading alone cannot turn a submission instruction into a technical qualification. |
| `takb` | The only portfolio mention in the description is a request to send a resume and portfolio after skills and KPI sections. | A portfolio keyword alone is insufficient proof of a preferred prior project requirement. |
| `tm4I` | Skills wording allows experience **or samples** in thermal-product design; the closing sentence requests a resume and related portfolio samples. | Keep qualification alternatives distinct from the act of submitting evidence. |

The examples support a three-way source-backed distinction: substantive capability/experience, expressly preferred demonstration of ability, and application logistics. A keyword or heading heuristic cannot safely encode it by itself. The observed `tvMm` omission is especially consequential because its preferred demonstration appears before a formal skills list; the later application request is a separate passage.

## Bounded next design gate

Use the exact source spans above plus at least one negative case in an offline proposal for item-scoped proof-of-ability coverage. The proposal must keep strength, alternatives, exact source linkage, and the qualification-versus-submission distinction visible, and show where a candidate interpretation would sit before acceptance. For R03, first prototype a source-index-preserving **presentation** grouping against retained candidate/accepted artifacts, without changing P1.6 claim arrays, Capability assignments, Registry mappings or I5 keys/counts. Review the prototype for lost required/preferred, familiarity/experience, and tool/language distinctions before choosing persistence or contract changes.

No new model run or `tvMm` retry follows from this audit. Market I7 remains HOLD until genuinely accepted-current core evidence and real semantic drill-down exist.
