# JobHunter Working Memory / Handoff

**Status:** Rolling non-authoritative handoff  
**Date:** 2026-08-08  
**Repository:** `https://github.com/motafegh/jobhunter`  
**Reconciled repository state through:** current 2026-08-08 B1/SQ-0 working-tree tranche
**Purpose:** Let a new conversation resume from the real current state without reconstructing the recent semantic-quality journey from chat history.

This file is **not** a controlling specification. If it conflicts with a higher-authority document, the higher-authority document wins.

---

## 1. Read this first in a new conversation

Before material work, read:

1. `README.md`
2. `AGENTS.md`
3. `docs/PRODUCT_SPECIFICATION.md`
4. `docs/ARCHITECTURE.md`
5. `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
6. `docs/SOURCE_POLICY.md`
7. `docs/ROADMAP.md`
8. `docs/IMPLEMENTATION_PLAN.md`
9. `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`
10. `docs/EXECUTION_TODO.md`
11. `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`
12. this file
13. task-specific docs such as:
    - `docs/SEMANTIC_ANALYSIS.md`
    - `docs/PHASE_2_CAPABILITY_INTELLIGENCE_PLAN.md`
    - `docs/ROLE_CAPABILITY_BLUEPRINT_PLAN.md`
    - `review-snapshots/README.md`

Authority remains:

```text
product/domain/source/architecture
→ roadmap
→ master implementation plan
→ active Phase-1 / focused plans
→ execution TODO
→ implementation/tests/live evidence
```

Do not use this handoff to override those documents.

---

## 2. Project identity

JobHunter is a local-first personal career-intelligence application.

Target mature loop:

```text
MARKET
→ ROLE / CAPABILITY INTELLIGENCE
→ REVIEWED PERSONAL EVIDENCE
→ GAPS / CONSTRAINTS
→ LEARN / PRACTISE / BUILD / VERIFY
→ APPLICATION DECISION
→ OUTCOME
→ UPDATED EVIDENCE AND DECISIONS
↺
```

Job acquisition is an input subsystem, not the final product.

Current architecture remains:

- local Python modular monolith;
- SQLite canonical structured state;
- immutable raw source evidence;
- FastAPI/Uvicorn/Jinja2/local static assets;
- browser primary, CLI advanced/debug/automation;
- source/model processing bounded and inspectable;
- local-first LM Studio;
- no Node/npm/React/vector DB/RAG/agent platform without demonstrated need.

---

## 3. Current active contracts

```text
source parser:                 jobinja-detail-v2
translation provider:         lm-studio-translation-v2
English projection:            english-projection-v2

English P1.6 prompt/runtime:   job-analysis-english-v9
Original P1.6 prompt/runtime:  job-analysis-original-v9
P1.6 persisted schema:         job-analysis-v4

Capability prompt/runtime:     job-capability-intelligence-v4
Capability persisted schema:   job-capability-intelligence-v2

Blueprint prompt/runtime:      role-capability-blueprint-v2
Blueprint persisted schema:    role-capability-blueprint-v1

Review Snapshot schema:        job-review-snapshot-v1
```

Do not call older P1.6/Capability/Blueprint prompt versions current. Historical incident/lesson documents may correctly mention them as history.

---

## 4. Current semantic layering

```text
original Jobinja source
        ↓ authoritative
English projection v2
        ↓ derived convenience
P1.6 strict factual extraction
        ↓ factual substrate
Capability Intelligence v4
        ↓ auditable reasoning
Role Capability Blueprint v2
        ↓ human-facing professional interpretation
Review Snapshot v1
        ↓ selected repository review artifact
```

The current Market layer still aggregates accepted/current **English P1.6**, not Capability or Blueprint.

---

## 5. Where the project stands

Approximate current state:

| Area | Current state |
|---|---|
| Jobinja acquisition/provenance | strong foundation |
| Source semantic versions/check separation | strong foundation |
| Parser v2 | strong foundation |
| Translation v2 architecture | strong/currently used |
| P1.6 mechanics/evidence grounding | strong |
| P1.6 semantic coverage/optionality/depth | acceptance work open |
| Capability architecture/evidence mechanics | strong |
| Capability semantic calibration | CI-3 open |
| Blueprint product structure | strong/useful |
| Blueprint expert-judgment calibration | acceptance open |
| Independent reasoning model roles | implemented |
| Review Snapshot concept | implemented and proven useful |
| Integrated snapshot model routing | accepted; deterministic and live snapshot evidence green |
| Market truthfulness acceptance | still pending Phase-1 closure |
| Source/lifecycle acceptance | still pending Phase-1 closure |
| Final P1.7 run/report/browser acceptance | still pending |
| Phase 1 overall | active, not closed |
| Corpus-wide Phase 2 | gated |

Do not interpret the successful `tG9K` reasoning chain as Phase-1 completion.

---

## 6. Current live semantic acceptance anchors

### `t4jp` — sparse/ambiguous posting

Use this case to test conservative behavior when the employer supplies little technical detail.

Important lesson:

> A shallow result is not automatically a defect when the source is shallow.

Observed overreach classes from earlier review:

- child-health context was treated as proof of a highly regulated/clinical workflow;
- `the work is teachable` was interpreted as teaching other staff;
- `website design` was expanded too confidently into CMS/backend/deployment;
- AI-assisted content work was reframed too strongly as AI pipeline engineering.

Correct principle:

```text
sparse evidence
→ modest strong conclusions
→ more unknowns
→ limited architecture/tool speculation
```

### `tG9K` — rich semiconductor / industrial-ML posting

This is the main current dense technical acceptance case.

Current selected review artifact:

```text
review-snapshots/jobs/tG9K.json
```

The complete current chain successfully ran:

```text
English P1.6 v4
→ Capability v4
→ Blueprint v2
```

The snapshot records current-chain dependency flags as true.

Known artifact IDs in the first pushed snapshot:

```text
English projection artifact: 33
English analysis artifact:    25
Capability artifact:           6
Blueprint artifact:            4
model: gemma-4-e2b-it
```

These IDs are local-database artifact IDs and may change if regenerated under new contracts; use dependency identity rather than assuming IDs stay forever.

---

## 7. What `tG9K` proved

### Infrastructure/contract wins

- long dense postings can now complete P1.6 instead of silently producing 0/0;
- production P1.6 uses evidence-reference IDs rather than model quotation transcription;
- long-description evidence is heading/segment/clause-addressable;
- Capability references resolve back to exact source text;
- bad extra evidence references no longer kill a grounded supported claim;
- supported invalid-only evidence still fails closed;
- invalid-only evidence on `unknown_or_unsupported` normalizes to `[]` instead of wasting a full retry;
- long local P1.6/Capability/Blueprint reads have no arbitrary read timeout after successful connection;
- Capability and Blueprint can use dedicated local model roles;
- Review Snapshots allow complete GitHub-side quality review without manual browser copy/paste.

### Remaining P1.6 quality issues

The reviewed `tG9K` P1.6 responsibilities are good, but factual requirement coverage is incomplete.

Explicit source families that were not fully represented include examples such as:

- Data & statistics: pandas / NumPy / SciPy / statsmodels / PCA / PLS;
- Industrial statistics: SPC / DOE / capability analysis / Bayesian methods;
- Fab systems: MES / SECS-GEM / equipment/metrology/trace;
- cloud providers / edge wording;
- `MATLAB a plus`;
- `some C/C++ helpful`;
- structured 3–6 years experience / Master's degree where semantically appropriate.

Depth/optionality issue:

```text
Python (expert)
```

is explicit for Python only. It must not become `expert` for every listed ML framework.

Global wording:

```text
We don't expect every single item — depth in the core stack matters most.
```

must not become either:

```text
every stack item required
```

or:

```text
every stack item preferred
```

The current P1.6 enum is still:

```text
required
preferred
contextual
inferred
```

Evaluate `mixed` / `unspecified` only if reviewed examples prove the current contract cannot truthfully encode the source.

### Remaining Capability issues

- `depth_signals` were empty even though the source contains explicit depth/experience signals;
- requirement strength can still be over-inflated from a broad stack list;
- optional edge/cloud wording can become high-confidence operational context;
- unrelated uncertainty/context can leak into the wrong capability area;
- upstream P1.6 depth mistakes can be amplified downstream.

### Remaining Blueprint issues

The product structure is useful, but the first `tG9K` Blueprint still showed model-judgment overreach:

- named technologies were assembled into one `highly_likely` architecture;
- a real-time anomaly-detection flow was `highly_likely` while latency was also an explicit unknown;
- optional edge deployment was too strong;
- tools were assigned specific runtime roles not established by the vacancy;
- plausible domain ideas became more specific/certain than the source justified.

Permanent lesson:

> A technology list is not an architecture specification.

Do not fix these by accumulating semiconductor-specific prompt patches.

---

## 8. Evidence-density principle

One central acceptance rule now controls semantic review:

> Intelligence depth should scale with evidence density.

```text
poor advertisement
→ limited strong conclusions
→ explicit unknowns

rich advertisement
→ deeper work-linked decomposition
→ richer supported interpretation
```

If sparse and rich ads both produce elaborate architectures, the system is over-inferencing.

If both remain shallow, the system is under-reasoning or losing source information.

---

## 9. Completed current tranche — integrated Review Snapshot routing

**Integrated Review Snapshot effective-model routing is accepted.**

The normal command:

```bash
jobhunter jobs snapshot <id>
```

now passes:

```text
effective_analysis_lm_studio_model()
effective_capability_lm_studio_model()
effective_blueprint_lm_studio_model()
```

The first historical `tG9K` snapshot contained:

```json
"configured_models": {
  "analysis": null,
  "capability": null,
  "blueprint": null
}
```

although the artifacts correctly recorded `gemma-4-e2b-it`. B1 first regenerated a complete E2B chain. After B2 acceptance, the selected snapshot records `gemma-4-e4b-it-ud` for analysis and E2B for downstream roles.

Accepted evidence:

- integrated routing tests assert all three model arguments;
- focused routing/snapshot tests passed 7 tests;
- Ruff passed;
- normal full pytest passed 269 tests;
- warnings-as-errors passed 269 tests;
- regenerated `tG9K` selects accepted P1.6 artifact 29, includes dependency-current Capability artifact 7 for negative review, and omits the older Blueprint chain;
- snapshot exclusions remain intact.

No semantic prompt/schema/model generation changed in this tranche.

---

## 10. Exact next implementation sequence

With snapshot routing accepted:

### Completed — deterministic gate

```bash
ruff check .
python -m pytest
python -m pytest -W error
```

Observed on the user's environment: Ruff green; both full pytest runs passed 269 tests.

### Completed — P1.6 factual quality

Accepted artifact 29 now provides:

- explicit requirement coverage;
- optionality/obligation preservation;
- explicit depth preservation;
- structured experience/education participation;
- no depth spreading across technologies.

No arbitrary minimum claim count was introduced. The selected Review Snapshot exposes accepted P1.6 artifact 29, reviewed-but-unaccepted Capability artifact 7, and no stale Blueprint.

### Current next — Capability calibration

Against accepted P1.6 artifact 29:

- use `depth_signals` when evidence supports them;
- preserve upstream requirement strength;
- keep optional edge/cloud context appropriately uncertain;
- improve capability grouping coherence;
- retain current deterministic evidence-resilience rules.

The first artifact-29 rebuild completed as Capability artifact 7 under v4 but failed semantic review: explicit depth was omitted and contextual stack/ownership claims were overstated. A generic v5 depth-coverage experiment passed 21 focused tests but failed live after its bounded retry exhausted `max_tokens`; no v5 artifact persisted and the experiment was reverted. Full evidence and the later remediation route are in `docs/incidents/2026-08-09_MODEL_EVALUATION_AND_CAPABILITY_CALIBRATION_FAILURES.md`.

Current role configuration:

```text
analysis:   gemma-4-e4b-it-ud
capability: gemma-4-e2b-it
blueprint:  gemma-4-e2b-it
```

The analysis choice is evidence-based: E4B completed the accepted v9/v4 contract in 76 seconds. Gemma 12B was operationally too slow on the 8 GB GPU. OpenCode free candidates either failed semantic validation, exhausted the completion budget, or hit the free-tier limit. NVIDIA Inkling Low nearly matched E4B latency but still failed depth validation after its bounded retry; NVIDIA DeepSeek Flash Non-think was slower and also failed depth validation, while Think-High was operationally too slow. NVIDIA Gemma 31B and Nemotron Super were operationally rejected. No hosted candidate produced an accepted artifact.

### Step 3 — Blueprint calibration

General principles only:

- technology list != architecture;
- `highly_likely` cannot contradict unresolved unknown;
- examples stay examples;
- source optionality survives downstream;
- tool/metric/protocol semantics remain technically correct;
- scenario detail scales with evidence.

### Step 4 — controlled stronger-model comparison if needed

Keep fixed:

```text
source semantic version
English projection
accepted P1.6
prompt/schema contract
review rubric
```

Change only the Capability/Blueprint model.

Compare technical correctness/calibration, not eloquence.

Do not build multi-model voting.

### Step 5 — complete CI-3 heterogeneous review

Current anchors:

```text
t4jp  sparse/ambiguous
tG9K  rich AI/ML
```

Add:

- Python/software;
- network/security;
- operations/platform/DevOps.

Use Review Snapshots for selected acceptance examples.

### Step 6 — stop semantic expansion when accepted

Then return to Phase-1 closure:

```text
Market truthfulness/sampling
→ source failure/lifecycle acceptance
→ partial-success operation semantics
→ P1.7 report/run/browser acceptance
→ Phase-1 closure
```

### Step 7 — only after Phase-1 closure

Start corpus-wide Phase 2:

```text
canonical concepts
→ reviewed aliases/mappings
→ responsibilities/deliverables
→ corpus-scale capability requirement profiles
→ role archetypes
→ Market v2
→ later personal evidence/gaps
```

---

## 11. Review Snapshot workflow

After locally rebuilding a selected review job:

```bash
jobhunter jobs snapshot <JOB_ID>
git diff -- review-snapshots/jobs/<JOB_ID>.json
git add review-snapshots/jobs/<JOB_ID>.json
git commit -m "review: update <JOB_ID> intelligence snapshot"
git push origin main
```

Then a new conversation can simply be told:

> Check the latest `<JOB_ID>` Review Snapshot and analyze the full chain.

Do not commit the live SQLite DB.

Do not automatically commit the entire analyzed corpus; snapshots are selected review/acceptance artifacts.

---

## 12. Current independent model configuration

```toml
analysis_lm_studio_model = "..."
capability_lm_studio_model = "..."
blueprint_lm_studio_model = "..."
```

Fallback:

```text
Analysis
→ dedicated analysis
→ general model
→ explicit translation model

Capability
→ dedicated capability
→ effective analysis

Blueprint
→ dedicated Blueprint
→ effective Capability
```

Current reviewed artifacts used `gemma-4-e2b-it` because no dedicated stronger role model was configured in that run.

---

## 13. Runtime policy for long local reasoning

For P1.6/Capability/Blueprint local Instructor/OpenAI-compatible calls:

```text
connect timeout: bounded
read timeout after connection: none
write/pool: bounded
transport replay: disabled
max tokens: bounded
validation retry: bounded separately
```

This was deliberately chosen after legitimate long local generations were killed by arbitrary read deadlines.

Tradeoff: if LM Studio hangs after connection, a non-streaming request can wait until the user cancels/stops the operation.

---

## 14. Known technical debt — do not hide it inside the next semantic fix

Current `job_analysis_artifacts` uniqueness semantics do not directly include `translation_artifact_id`.

The accepted English analysis artifact **stores** its exact translation dependency. Capability/Blueprint correctly follow that exact ID instead of guessing from the latest translation row.

Any future migration that changes P1.6 identity to include translation artifact directly must be:

- explicitly designed;
- migration-tested;
- non-destructive;
- independently versioned/reconciled.

Do not opportunistically fold this schema migration into semantic-quality work.

---

## 15. Test/runtime truth at handoff

Do not claim the current documentation head is code-tested merely because these edits are documentation-only.

Observed earlier during the semantic tranche:

- a full suite reached **250 passed** with one stale assertion failure;
- the assertion was fixed;
- a Ruff E501 line-length failure was fixed;
- Review Snapshot tests exposed missing `TranslationStore.artifact_by_id()` and it was implemented;
- Capability unknown-evidence behavior exposed the `p1:requirements:19` failure and was fixed/tested;
- after those fixes, the user successfully generated both Capability and Blueprint for `tG9K` and created/pushed the snapshot.

The B1/SQ-0 code tranche ran:

```bash
ruff check .
python -m pytest
python -m pytest -W error
```

Observed result: Ruff green; focused snapshot/model-routing tests 7 passed; full pytest 269 passed; full warnings-as-errors 269 passed.

---

## 16. Documentation audit completed on 2026-08-08

Reconciled current/entry-point docs include:

- `README.md`
- `AGENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/PHASE_1_JOBINJA_AUTOMATION_PLAN.md`
- `docs/EXECUTION_TODO.md`
- `docs/SEMANTIC_ANALYSIS.md`
- `docs/PHASE_2_CAPABILITY_INTELLIGENCE_PLAN.md`
- `docs/ROLE_CAPABILITY_BLUEPRINT_PLAN.md`
- `docs/decisions/2026-08-06_REVIEW_SNAPSHOT_AND_REASONING_MODEL_ROLES.md`
- `review-snapshots/README.md`
- new `docs/SEMANTIC_QUALITY_ACCEPTANCE_PLAN.md`
- this `docs/WORKING_MEMORY.md`

Audited and intentionally left unchanged because their strategic/product invariants remain valid:

- `docs/PRODUCT_SPECIFICATION.md`
- `docs/DOMAIN_AND_ANALYSIS_MODEL.md`
- `docs/SOURCE_POLICY.md`
- `docs/ROADMAP.md`

Those higher-level documents do not control exact prompt/runtime version numbers; the master/phase/focused plans now carry the current implementation state.

Historical incident/lesson documents may retain older version names when they describe historical events. Do not erase useful history merely to make a string search empty.

---

## 17. Important non-goals / stop lines

Do not:

- commit live SQLite/WAL/SHM;
- start corpus-wide Phase 2 before Phase-1 closure;
- auto-grow taxonomy from model output;
- add multi-model voting;
- build RAG/vector DB because semantic reasoning is imperfect;
- add domain-specific prompt patches for every `tG9K` technical mistake;
- infer personal readiness/gaps before reviewed personal evidence exists;
- automate applications/messages;
- bypass Jobinja/source-policy access limits;
- reinterpret coverage count as semantic-quality certification;
- silently call old prompt artifacts current;
- restart the obsolete August-3 execution checklist.

---

## 18. When this handoff should be updated

Update this file when one of these materially changes:

- active prompt/schema identities;
- current accepted/live examples;
- the exact next blocking task;
- acceptance state of P1.6/Capability/Blueprint;
- Phase-1 closure status;
- major architecture/persistence/source-policy decisions;
- model-role selection after a controlled comparison.

Do not update it for every small commit. It is a session/conversation handoff, not a changelog.
