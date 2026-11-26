# Component profile standard

**Optional inspection aid (DOC.4):** [Feasibility and commands](working-memory/2026-11-26_ARCHITECTURE_UNDERSTANDABILITY_DOC4_INSPECTION_FEASIBILITY.md) describe the curated read-only developer script and its limitations. Generated AST/import/schema/MRO reports supplement, not replace, verified runtime narratives and authority checks.

**Status:** adopted supporting engineering documentation (DOC.3, 2026-11-26). Subordinate to [AGENTS](../AGENTS.md), [Architecture](ARCHITECTURE.md), [Domain](DOMAIN_AND_ANALYSIS_MODEL.md), [Source policy](SOURCE_POLICY.md) and [Reasoning/authority policy](UTILITY_EPISTEMIC_AUTHORITY_AND_REASONING_POLICY.md). This is a description standard, not a new runtime contract or acceptance gate.

## 1. Purpose and reading routes

Document meaningful components and workflows, not every Python file. A component is a coherent responsibility with an entry boundary, contract, dependencies and observable effects; it may span inherited implementations. Prefer a compact overview and one verified profile per responsibility, linking detailed code/decisions rather than repeating them. Use [Current runtime](CURRENT_RUNTIME_AND_VERSIONED_CODE.md) as the index of active owners and [DOC.2 P1.6 walkthrough](working-memory/2026-11-25_ARCHITECTURE_UNDERSTANDABILITY_DOC2_P16_RUNTIME_BASELINE.md) for concrete calls, data and authority. [Worked profiles](working-memory/2026-11-26_ARCHITECTURE_UNDERSTANDABILITY_DOC3_COMPONENT_PROFILES.md) illustrate the standard.

| Reader / goal | Progression |
| --- | --- |
| Owner / learning | Product purpose -> architecture overview -> one worked profile -> success/failure example -> actual owner function and one relevant test -> limitations. Start from what happens to a job, not a long import list. |
| New developer | Governance -> runtime index -> affected component profile -> entrypoint and resolved implementation -> contracts/state, consumers and tests -> relevant decision/replay. |
| Reviewer | Change scope -> verified revision/authority -> input identity and data flow -> failure/currentness -> tests and observed evidence -> unresolved risk. |
| AI assistant | AGENTS and controlling docs -> current task ledger -> affected profile/actual owners -> transitive dependencies and consumer contracts -> tests/unknowns. Profile is a guide, never a substitute for inspecting actual code. |

The paths are progressive, not compulsory exhaustive history reading. For a narrow change inspect the affected slice and boundaries; for broad orientation extend systematically. [DOC.7 practice](working-memory/2026-11-26_ARCHITECTURE_UNDERSTANDABILITY_DOC7_ORIENTATION_CURRENTNESS.md) defines and demonstrates the permanent change/orientation procedure; use AGENTS §13.1.

## 2. Profile template

Use the following headings (tables or brief bullets are fine). Mark not applicable explicitly with reason. For a routine component aim for roughly one or two screens of overview and linked details, not a separate design book. Split genuinely independent responsibilities. Profile ID stable across revisions; use canonical repository-relative paths and qualified symbols instead of line numbers alone.

| Field | Required content |
| --- | --- |
| Header | Stable component ID/name; status and scope; verified code revision/date; responsible role; related controlling contract. |
| Purpose / non-goals | User/engineering problem solved; what it does not establish. |
| Entry boundary | Actual CLI/HTTP/factory/function (or explicit research entry), caller, active transitive owner(s); distinguish public facade and historical implementations. |
| Inputs / outputs / contracts | Input types, version/identity and validation prerequisites; returned/persisted shapes, contract versions, what result means and does not mean. |
| Responsibilities / dependencies | Deterministic preparation, model task if any, validation/semantic judgment separation; direct calls, data/authority dependencies, optional paths; shared/inherited code and external runtime. |
| Persistence / side effects | Reads/writes, key tables/files, exact dependency identity, network/model calls, cache/reuse, transaction limits, privacy/export boundary. No private rows or credentials in docs. |
| Lifecycle / failures | Normal, reuse, partial, failed, stale/rejected transitions where applicable; retries/limits, recovery owner, what remains available; explicit unknowns. |
| Authority / consumers | Evidence vs interpretation vs accepted authority, currentness selectors, allowed/blocked consumers and review/promotion. |
| Tests / evidence | Exact test files and relevant cases; static owner inspection, observed receipt or offline replay, verified revision/commands and limits. Test pass is not semantic approval. |
| Limits / decisions / change guidance | Known gaps, uncertainty, rejected/deferred options and linked records; which profile/contracts/tests/consumers need recheck on change. |

### Status and evidence notation

Status: **C** public/current route; **T** active transitive owner; **K** accepted-only compatibility; **R** research/candidate/opt-in; **H** historical-only; **D** deferred/proposed (not implemented). A profile may combine statuses with explicit subpaths. Version suffix alone never establishes status. Evidence: **S** static code/identity inspection; **O** observed retained execution/receipt; **X** executed offline replay or test; **I** illustrative walkthrough; **P** proposed design. Distinguish a test with stubs from a live trace. Record missing evidence as unknown/not established; no invented call edges, authority or coverage.

For diagrams use solid arrows for direct calls or labeled concrete sequence, dashed arrows for data/authority dependencies or optional composition. Label edge meanings and scope; if several paths are possible, show conditions. MRO and import graphs are separate views, not runtime call graphs. Verify actual method resolution when inheritance/decorators/factories matter. Prefer a simple text trace if a diagram adds no value.

## 3. Verification and maintenance

At creation or affected change, verify symbols, resolved owners, contract IDs, actual read/write paths and consumer currentness against source at recorded revision; link tests/replays, not just file names where substantive claim requires evidence. Use read-only inspection of frozen data, no production initialization merely for documentation. Compare known prior fingerprints when reusing a dated map; a match only establishes identical inspected bytes, not correctness of uninspected dependencies. Record revision, file digest and check output in a safe receipt if useful. Do not claim full dynamic coverage from AST, schema or MRO. Use exact code links and concise known gaps.

Keep primary living references at existing stable paths; dated profile receipts and decision records remain historical evidence. Change author owns affected profile/map update, reviewer checks actual code/authority/limitations, product owner retains substantive policy decisions. If implementation is not yet written, use a separate proposed design profile (P/D), not a current profile. If changed behavior makes a dated record obsolete, link a new version and mark scope superseded rather than rewriting history. DOC.4 delivered optional inspection tooling; DOC.6 expands component coverage in bounded slices; DOC.7 established permanent orientation and on-demand drift checks. No new documentation bureaucracy, generator or CI obligation implied by this standard.

## 4. Worked P1.6 profiles and next steps

- [P1.6 current English analysis orchestration and execution](working-memory/2026-11-26_ARCHITECTURE_UNDERSTANDABILITY_DOC3_COMPONENT_PROFILES.md#p16-english-analysis) — model/deterministic boundaries, inherited owners, source/projection reuse, candidate persistence and failure.
- [P1.6 source brief](working-memory/2026-11-26_ARCHITECTURE_UNDERSTANDABILITY_DOC3_COMPONENT_PROFILES.md#p16-source-brief) — contrasting deterministic, read-only candidate route.
- [Review and consumer boundary](working-memory/2026-11-26_ARCHITECTURE_UNDERSTANDABILITY_DOC3_COMPONENT_PROFILES.md#p16-review-and-consumers) — separate authority profile.
- [Selected research design](working-memory/2026-11-25_P16_EVOLUTION_E2_ARCHITECTURE_DECISION.md) remains proposed; [DOC.5 implementation-facing profiles](working-memory/2026-11-26_ARCHITECTURE_UNDERSTANDABILITY_DOC5_SELECTED_DESIGN.md) document it separately before E3. Reconcile as-built after implementation.

The standard covers this P1.6 pilot; whole-system profile completeness is not established. Use the tracker for completion and next steps.
