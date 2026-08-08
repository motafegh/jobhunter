# JobHunter Semantic Quality Acceptance Plan

**Status:** Active bounded acceptance plan  
**Date:** 2026-08-08  
**Scope:** P1.6 strict extraction, Capability Intelligence, Role Capability Blueprint, model-role comparison, and repository review snapshots  
**Authority:** Subordinate to `docs/IMPLEMENTATION_PLAN.md`, `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`, `docs/ROADMAP.md`, and the product/domain/source/architecture constraints.

This plan does **not** authorize corpus-wide Phase-2 taxonomy/Market-v2 work. It exists to finish the semantic-quality evidence needed by the current Phase-1/P1.6 acceptance gate and the bounded per-job capability slice.

---

## 1. Why this plan exists

Recent live work proved that the architecture can complete the full reviewed chain:

```text
Jobinja source
→ English projection v2
→ strict P1.6 factual extraction
→ Capability Intelligence
→ Role Capability Blueprint
→ repository Review Snapshot
```

The remaining problems are no longer primarily transport, persistence, timeout, quotation-copy, or artifact-reuse failures. They are mostly **semantic coverage, optionality/depth preservation, capability calibration, expert-judgment precision, and model adequacy**.

Two live cases established the acceptance shape:

### Sparse case — `t4jp`

The source itself contains little technical detail. Correct behavior is conservative:

```text
sparse evidence
→ modest analysis
→ explicit unknowns
→ limited tool/architecture speculation
```

A shallow result is not automatically a defect when the employer supplied little evidence.

### Rich case — `tG9K`

The source contains dense semiconductor/industrial-ML responsibilities and technical-stack details. The current chain now runs end to end and is reviewable at:

```text
review-snapshots/jobs/tG9K.json
```

The snapshot proved that rich evidence produces richer intelligence, but also exposed remaining semantic defects:

- P1.6 still misses some explicit requirement families on long postings;
- global stack optionality can still collapse into overly strong `required` conclusions;
- explicit depth such as `Python (expert)` is not always kept separate from broader stack depth;
- Capability Intelligence underuses `depth_signals` and can overstate edge/deployment context;
- Blueprint can assemble a list of named technologies into an architecture the employer never specified;
- `highly_likely` scenarios can conflict with explicit unknowns;
- technically plausible prose can still misuse tools/metrics or assign them overly specific roles.

These are quality-calibration problems, not reasons to collapse the current layer separation.

---

## 2. Current active contracts

As of this plan:

```text
source parser:                 jobinja-detail-v2
English projection:            english-projection-v2
translation provider contract: lm-studio-translation-v2

English P1.6 prompt/runtime:   job-analysis-english-v4
Original P1.6 prompt/runtime:  job-analysis-original-v4
P1.6 persisted schema:         job-analysis-v2

Capability prompt/runtime:     job-capability-intelligence-v4
Capability persisted schema:   job-capability-intelligence-v2

Blueprint prompt/runtime:      role-capability-blueprint-v2
Blueprint persisted schema:    role-capability-blueprint-v1

Review Snapshot schema:        job-review-snapshot-v1
```

Historical prompt/runtime versions remain historical and must not be silently reused as current artifacts.

---

## 3. Permanent layer contract

Do not collapse these responsibilities:

```text
P1.6
→ factual substrate
→ what the employer/source explicitly supports
→ strict evidence and conservative classification

Capability Intelligence
→ auditable machine reasoning
→ work-linked decomposition, prerequisites, depth/context, unknown scope

Role Capability Blueprint
→ human-facing professional interpretation
→ useful likely scope, work products, failure modes, examples, scenarios
```

The quality of a downstream layer never upgrades an incorrect upstream factual claim into truth.

---

## 4. Acceptance principle: intelligence depth follows evidence density

Required behavior:

```text
poor advertisement
→ limited strong conclusions
→ more unknowns

rich advertisement
→ deeper work-linked decomposition
→ more precise capability/depth/context conclusions
```

Failure modes:

```text
similar elaborate output for sparse and rich jobs
→ likely over-inference

similar shallow output for sparse and rich jobs
→ likely under-reasoning / extraction loss
```

`t4jp` and `tG9K` are retained as opposite ends of this acceptance spectrum.

---

## 5. Tranche SQ-0 — Review Snapshot correctness

The Review Snapshot workflow is now the normal repository-native live-quality review mechanism.

Normal command:

```bash
jobhunter jobs snapshot <job-id>
```

Default output:

```text
review-snapshots/jobs/<job-id>.json
```

The live SQLite database remains local and ignored.

### Known blocking defect

The standalone snapshot entry point passes effective analysis/capability/blueprint model roles into the exporter. The integrated `jobhunter jobs snapshot` path currently does not. That caused the first pushed `tG9K` snapshot to contain:

```json
"configured_models": {
  "analysis": null,
  "capability": null,
  "blueprint": null
}
```

while the persisted artifacts themselves correctly recorded `gemma-4-e2b-it`.

This happened to select the correct chain because only one relevant model was present. It is **not safe for controlled multi-model comparison**.

### SQ-0 required work

- pass `effective_analysis_lm_studio_model()` into `write_review_snapshot()`;
- pass `effective_capability_lm_studio_model()`;
- pass `effective_blueprint_lm_studio_model()`;
- update CLI routing tests;
- regenerate `tG9K` and confirm `configured_models` records the effective roles;
- confirm current-chain flags remain correct;
- keep raw responses/prompts/SQLite/private user data excluded.

**Gate:** Do not begin model comparison until SQ-0 is green.

---

## 6. Tranche SQ-1 — P1.6 factual coverage and obligation/depth preservation

P1.6 is the highest semantic priority because downstream layers depend on it.

### Already improved in v4

- heading-aware long-description evidence references;
- clause-level references for semicolon-delimited mixed-strength lines;
- rich-source 0/0 extraction guard;
- evidence-reference generation instead of quotation transcription;
- deterministic atomic optionality guard;
- `preferred` claims require source preference/advantage wording;
- long local analysis generation has no arbitrary read-time ceiling.

### Remaining observed defects

The accepted `tG9K` v4 artifact captured responsibilities well but omitted explicit source families including examples such as:

- Data & statistics: pandas / NumPy / SciPy / statsmodels / PCA / PLS;
- Industrial statistics: SPC / DOE / capability analysis / Bayesian methods;
- Fab data systems: MES / SECS-GEM / equipment/metrology/trace;
- Cloud providers / edge wording;
- `MATLAB a plus`;
- `some C/C++ helpful`;
- structured education/experience signals where they should participate in job requirements.

It also over-strengthened some stack entries even though the employer states that not every technical-stack item is expected.

### SQ-1 design rules

1. **Coverage accounting, not forced claim count.**
   - meaningful requirement-bearing source segments should be extracted, explicitly classified as non-requirement/context, or otherwise explainably excluded;
   - do not solve recall by inventing a minimum number of claims.

2. **Obligation strength and technical depth stay separate.**
   - `Python (expert)` → employer-stated depth = expert;
   - `MATLAB a plus` → optional/preference signal;
   - `C/C++ helpful` → optional/helpful signal;
   - `we don't expect every single item` → individual stack obligation may be mixed/unspecified/contextual rather than automatically required or preferred.

3. **Do not spread one depth adjective across neighboring tools.**
   - `Python (expert)` does not prove expert PyTorch/TensorFlow/XGBoost/LightGBM.

4. **Structured source fields remain available where semantically relevant.**
   - explicit minimum experience and education must not disappear merely because the long free-text description is dense.

### Contract decision to evaluate

The current P1.6 requirement enum is:

```text
required
preferred
contextual
inferred
```

`tG9K` shows that some employer wording may genuinely require a distinct representation such as `mixed` and/or `unspecified`. Do not add the enum merely because it sounds useful; implement it only if reviewed examples demonstrate that the current four-way contract cannot truthfully encode the source without distortion.

**Gate:** Before downstream retuning, P1.6 must preserve factual coverage, obligation, and explicit depth on `tG9K` without inventing certainty.

---

## 7. Tranche SQ-2 — Capability Intelligence calibration

Current contract:

```text
job-capability-intelligence-v4
schema: job-capability-intelligence-v2
```

### Already working

- stable evidence-reference catalog;
- exact source resolution before persistence;
- invalid additional references are discarded only when valid grounding remains;
- invalid-only evidence still fails supported claims;
- invalid-only evidence for `unknown_or_unsupported` normalizes to `[]` rather than consuming another full model retry;
- long local generation has no arbitrary read-time ceiling;
- dedicated capability model role is configurable;
- current source/translation/P1.6 dependency identity is preserved.

### Remaining acceptance problems

- `depth_signals` can remain empty even when the posting has strong explicit depth/seniority evidence;
- source stack optionality can be converted into overly strong capability `required` conclusions;
- one capability area can absorb unrelated uncertainty/context that belongs to another area;
- optional edge/cloud wording can become a high-confidence operational-context conclusion;
- downstream reasoning can amplify an upstream P1.6 depth mistake.

### SQ-2 rules

- explicit depth/seniority/experience evidence should populate `depth_signals` when material;
- `requirement_strength` must not silently become stronger than the factual substrate;
- unknown scope stays explicit;
- capability grouping should be coherent enough that unrelated MLOps/deployment uncertainty is not attached to a time-series feature-engineering capability without a real reason;
- deterministic bookkeeping repairs remain deterministic;
- do not add domain-specific semiconductor validators.

**Gate:** Capability Intelligence should be materially more useful than P1.6 while remaining auditable and correctly calibrated.

---

## 8. Tranche SQ-3 — Blueprint calibration and expert-judgment quality

Current contract:

```text
role-capability-blueprint-v2
schema: role-capability-blueprint-v1
```

### Product shape is accepted as useful

The human-facing structure is valuable:

- role read / likely role shape;
- capability areas;
- likely depth;
- likely subskills;
- source-named / likely / possible tools/examples;
- work products;
- operational concerns/failure modes;
- hidden requirements;
- end-to-end scenarios;
- probable non-requirements;
- important unknowns;
- bottom line.

### Remaining observed failure classes

The first `tG9K` snapshot showed examples of overconfident synthesis:

- many independently listed technologies were assembled into one `highly_likely` architecture;
- a real-time scenario was labeled highly likely while latency remained an explicit unknown;
- optional edge deployment wording was treated too strongly;
- individual tools were assigned overly specific runtime roles;
- technically plausible statements could become more specific than the vacancy evidence justified.

### SQ-3 general rules

Do **not** accumulate one-off rules such as `never use Airflow for X` or semiconductor-specific prompt patches.

Instead enforce/review these general principles:

1. A technology list is **not** an architecture specification.
2. A plausible example remains an example; it must not be described as employer-required.
3. `highly_likely` requires strong supporting evidence and must not contradict an explicit unknown.
4. Source optionality must survive into scenarios and hidden requirements.
5. Tool/framework/protocol/metric names retain their normal technical meaning.
6. Company-domain context may support reasoning but must not manufacture regulation, scale, architecture, or proprietary systems.
7. Scenario detail should scale with evidence density.
8. Prefer useful narrowing (`probably not required`) over generic curriculum dumping.

**Gate:** Blueprint must be professionally useful without presenting one reasonable architecture as the employer's likely architecture when the evidence only supports a family of possibilities.

---

## 9. Tranche SQ-4 — Controlled model-role comparison

JobHunter now supports independent local models:

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

Fallback:

```text
Capability → dedicated capability model → effective analysis model
Blueprint  → dedicated blueprint model  → effective capability model
```

### Comparison protocol

Do not change source, translation, P1.6 evidence, prompt contract, and model at the same time.

For one reviewed job such as `tG9K`:

```text
same source semantic version
same English projection
same accepted P1.6 artifact
same Capability/Blueprint prompt+schema
        ↓
model A
vs
model B
```

Compare:

- factual/technical correctness;
- evidence-status calibration;
- obligation/depth preservation;
- useful decomposition;
- unsupported inference rate;
- domain/tool correctness;
- scenario realism;
- uncertainty calibration;
- generic-curriculum tendency;
- output usefulness per token/time.

Do not introduce multi-model voting or ensemble consensus. The purpose is to select an adequate role-specific model, not build another architecture layer.

---

## 10. Tranche SQ-5 — CI-3 representative live acceptance

Capability CI-3 is not passed by one strong technical example.

Review at least five materially different jobs where the corpus allows:

1. sparse/ambiguous posting — `t4jp` is the existing first case;
2. rich AI/ML/industrial role — `tG9K` is the existing first case;
3. Python/software role;
4. network/security role;
5. operations/platform/DevOps role.

Prefer multiple companies and varied description length, language mix, requirement density, and optionality wording.

For each job, regenerate a repository Review Snapshot and review the complete chain:

```text
source
→ English projection
→ P1.6
→ Capability Intelligence
→ Role Capability Blueprint
```

Record at least:

- P1.6 false positives/false negatives;
- requirement obligation/depth mistakes;
- evidence mismatch;
- Capability status/decomposition mistakes;
- unsupported prerequisites;
- missing unknown boundaries;
- Blueprint technical mistakes;
- over/under-inference;
- model-specific limitations.

Repeatable deterministic failures become regression fixtures. Non-deterministic/model-capability limitations are documented and used in model selection rather than patched endlessly.

---

## 11. Promotion / stop decision

After SQ-0 through SQ-5:

### Accept the bounded semantic slice when

- deterministic Ruff/pytest/warnings gates are green on the user's environment;
- current artifacts are dependency-correct and reviewable through snapshots;
- P1.6 factual coverage/strength/depth is acceptable across the representative sample;
- Capability adds useful auditable reasoning without systematic over-strengthening;
- Blueprint adds useful professional interpretation without systematic architecture invention;
- a dedicated stronger model is selected if Gemma remains inadequate;
- important repeatable failures have regression coverage;
- known model limitations are explicit.

### Then stop expanding this slice

Do not spend indefinite time polishing Blueprint. Return to remaining Phase-1 closure work:

```text
Market truthfulness / sampling
→ source failure + lifecycle acceptance
→ partial-success operation semantics
→ remaining P1.3/P1.5 acceptance
→ final P1.7 run/report/browser-equivalent acceptance
→ Phase-1 closure
```

Only after Phase-1 closure should corpus-wide Phase-2 canonical mapping, Market-v2 capability aggregation, role archetypes, and personal gap/readiness work become controlling implementation scope.

---

## 12. Non-goals

This plan does not authorize:

- universal technology curricula;
- automatic taxonomy growth;
- corpus-wide Capability/Blueprint generation;
- multi-model voting;
- vector/RAG infrastructure;
- personal readiness scoring;
- learning-plan generation;
- application ranking;
- autonomous application submission;
- domain-specific prompt rule accumulation.

---

## 13. Review Snapshot workflow

After a reviewed local run:

```bash
jobhunter jobs snapshot <job-id>
git diff -- review-snapshots/jobs/<job-id>.json
git add review-snapshots/jobs/<job-id>.json
git commit -m "review: update <job-id> intelligence snapshot"
git push origin main
```

The reviewer/AI can then inspect the repository snapshot directly. Manual browser copy/paste is no longer the normal review path.
