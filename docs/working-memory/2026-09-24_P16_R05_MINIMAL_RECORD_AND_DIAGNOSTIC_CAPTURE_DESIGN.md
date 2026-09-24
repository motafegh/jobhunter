# R05 — Minimal review/revision identities and diagnostic capture design

**Date:** 2026-09-24  
**Status:** EVIDENCE-BACKED DESIGN DRAFT / NOT A SCHEMA, IMPLEMENTATION, OR ACCEPTANCE APPROVAL  
**Parent decisions:** [R05 item review and diagnostic preservation](2026-09-24_P16_R05_ITEM_LEVEL_REVIEW_DIRECTION.md); [R05 corrections, lifecycles and proportional guards](2026-09-24_P16_R05_CORRECTION_LIFECYCLE_AND_PROPORTIONAL_GUARDS.md); [active R01–R04 discussion](2026-09-24_P16_SEMANTIC_STRICTNESS_AND_UTILITY_REFINEMENT_ACTIVE.md). Subordinate to AGENTS.md and controlling product/domain/source/architecture/reasoning policies.

## Observed current owners and constraints

- `src/jobhunter/analysis_runtime_v21.py` uses the existing v20 partition orchestration and shared Instructor transport (`analysis_runtime_v20.py`, `inference/instructor_lm_studio_v20.py`, `inference/instructor_lm_studio_v21.py`). Instructor returns a validated partition plus request/raw response on success; it raises on unsuccessful transport/structured validation. The caller retains preceding successful partitions only in memory until the whole-result checks complete. Do **not** presume an exception always exposes the failed raw response.
- `analysis_service_v20.py` and `analysis_store.py` persist mechanically validated output as a pending artifact. Failed generation/validation is an attempt with an error, not a pending analysis. `job_analysis_attempts` records `(job_detail_version_id, attempted_at, model, prompt_version, schema_version, outcome, artifact_id?, error_type?, error_message?)`, with outcomes `completed/failed/reused`; it does not currently express partitions, retries, original failed responses or detailed failure stages. Capture must not casually persist provider exception strings that could include sensitive data.
- `analysis_store.py` reviews an entire artifact, and the unique indexes permit at most one *non-rejected* current artifact per applicable detail/translation/model/prompt/schema contract. Historical snapshot references and Capability artifacts impose further immutable-dependency limits. A repaired revision must **not** reuse the prompt/schema fields as fictitious revision identifiers, bypass existing indexes, overwrite an accepted payload, or mutate historical snapshots. Current read/reuse selection would need deliberate revision-aware behavior before any new promoted revision is supported.
- `web/templates/job_detail.html` already permits clearly labelled inspection of a pending candidate. Capability and Market semantic aggregations require accepted analysis; current public English P1.6 remains v21/v5, isolated v22 is not promoted, and Market I7 remains HOLD.

## Proposed minimum logical records (storage layout intentionally undecided)

| Logical record | Stable identity / link | Minimum information | Authority |
| --- | --- | --- | --- |
| Generation attempt | Existing attempt identity plus a stable correlation identifier if needed **before** invocation; exact source-detail, projection, model, prompt/schema identities | Outcome, stage, timestamp, bounded nonsecret error, available partition/retry references. Reuse existing attempt ledger as canonical attempt history. | Operational only. |
| Diagnostic capture | Attempt link + capture identifier; partition index/total and retry number when known | Failure stage, validation issue paths/codes, availability/truncation flags, bounded privately retained original response or fragment **only if actually obtained**, reference to relevant nonsecret input/coverage/contract identities, and what validation succeeded before failure. | Non-authoritative; not a candidate. |
| Original candidate | Existing immutable analysis artifact ID + current source/projection/contract identity | Original persisted factual claims/evidence; generation attempt link where known; original raw response provenance. | Pending until reviewed. |
| Item/coverage review event | Review event ID + candidate/revision ID + item anchor **or** source-coverage anchor | Finding (supported / needs clarification / unsupported / missing coverage), cited evidence, materiality, human/rule provenance, reason, optional proposed action. Item anchor should include collection and original ordinal/digest; do not use normalized label as identity. Coverage gaps point to source evidence and are not fabricated candidate items. | Annotation only. |
| Correction proposal | Proposal ID + originating review event and original item (or coverage gap) | Proposed add/replace/remove/clarify operation, original versus proposed wording, exact source proof, obligation/depth/scope implications, reviewer disposition; no in-place rewrite. | Proposal, not promoted fact. |
| Revised candidate | New immutable revision identity + parent candidate/revision + approved change-set | Full inspectable revised claim set and preserved parent/original lineage; versioned validation result and item/coverage review disposition. Explicit old-to-new item mapping for inserts/deletions/reorder. | Candidate pending separate promotion decision. |
| Whole-artifact promotion decision | Exact revision identity + decision event + reviewing authority and time | Completeness and material-issue resolution assessment, source/dependency verification, exact accepted payload identity, downstream publication status. | Only fully reviewed and valid exact payload may become accepted P1.6. |

**Open architectural choice:** A sidecar revision store, an extended artifact identity/current selector, and a reviewed export into the existing accepted-artifact shape have different migration and foreign-key consequences. Do not select one before inspecting all live `find_artifact`/`latest_current`/Market snapshot/Capability and Registry consumers. Revisions must never cause an existing accepted anchor to disappear, become rejected merely to free a uniqueness slot, or change historical dependency meanings.

## Diagnostic capture boundaries

1. **Pre-inference/transport failure:** record the available stage and sanitized operational error; mark response `unavailable`. No inferred response or fragment.
2. **Response received but Instructor parsing/schema/item validation fails:** capture original response only through an explicitly reviewed, bounded provider capture interface, where actually available; retain failed validation path/code, partition/retry context and the exact contract. Do not assume existing exceptions reliably contain original bytes or that their string representation is safe to persist. Keep failed raw output outside the regular analysis-artifact table.
3. **Validated partition followed by scope failure:** retain the already returned validated partition and its raw/request references as *partition-scoped diagnostic evidence*, together with the scope failure; not a whole-job candidate.
4. **Later partition fails after earlier success:** record which earlier partitions succeeded and failed without treating the union as complete, independently validated full analysis.
5. **Merge/global source-coverage/postprocessing/persistence failure:** capture the available assembled structured result, valid partition identities and the failing stage, under the same non-authoritative diagnostic boundary. A persistence/identity-integrity exception must not be reframed as a recoverable semantic problem.

Protect confidentiality by storing locally by default; excluding credentials, authorization headers, private configuration, arbitrary exception dumps and public-corpus export; bounding response size, diagnostic count, retention and access; explicitly marking missing/truncated/unavailable content. Preserve exact available original content in a protected payload only when safe; any redacted display copy must be labelled a derivative, not the original bytes. Confirm actual SDK/provider access to failed completions before promising lossless capture.

## Proportional guard decision table (draft)

| Problem | Preserve useful evidence | Do not relax |
| --- | --- | --- |
| Ambiguous standalone concept label but source-grounded capability exists | Candidate-level item finding and source-backed correction proposal; unaffected claims inspectable | No unsupported employer history/strength in accepted facts |
| Wrongly borrowed depth or source obligation | Item-scoped diagnostic/review finding; target the affected claim | Do not promote a false required/preferred or expertise assertion |
| One failed partition after other valid partitions | Preserve completed partitions and failures as diagnostic evidence | No incomplete union promoted as complete analysis |
| Missing explicit preferred proof-of-work statement | Record source-coverage gap and proposed separately evidenced addition | Do not infer completeness from absence of detected gaps or make optional proof mandatory |
| Invalid dependency/provenance, corrupt state or privacy breach | Retain only securely available operational evidence | Hard stop; no candidate or promotion bypass |

## Verification and stop lines before implementation

Use synthetic/local fixtures first: no response, failed response with/without raw access, invalid item, successful first partition then failure, successful partitions then merged validation failure, ambiguous concept plus otherwise supported claims, exact source-backed correction, missing preferred proof, stale source/projection, existing accepted anchor with durable Capability/Market references. Check no diagnostic/review record is returned by accepted-current queries or contaminates Market/Capability/public corpus; check source/dependency identity, privacy, bounded retention, complete audit lineage, before/after evidence, and accepted/historical snapshot immutability. Do not run further live model evaluation or modify existing validators/acceptance to manufacture I7 PASS.

**Next:** inspect all revision/currentness and durable consumer references, and verify provider failure-response availability and privacy policy against actual SDK behavior. Then decide the smallest storage/read model and phased implementation, with explicit authorization before code, migrations or new model runs.
