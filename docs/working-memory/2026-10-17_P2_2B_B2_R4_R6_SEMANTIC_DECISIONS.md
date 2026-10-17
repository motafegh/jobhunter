# P2.2B-B2 R4-R6 Semantic Decisions — 2026-10-17

**Status:** SEMANTIC REVIEW COMPLETE / R4-R6 ACCEPTED / LOCAL APPLICATION PENDING  
**Scope:** Remaining B2 candidates R4-R6, plus the combined local application boundary for accepted-but-unapplied R3-R6.  
**Authority:** The owner delegated continuation of the remaining semantic gates to the assistant on 2026-10-17. This record closes semantic review only; it does not claim local SQLite rows that have not been executed and verified.

## 1. Decision summary

```text
R1  ACCEPTED / APPLIED / VERIFIED
R2  ACCEPTED / APPLIED / VERIFIED
R3  ACCEPTED / LOCAL APPLICATION PENDING
R4  ACCEPTED / LOCAL APPLICATION PENDING
R5  ACCEPTED / LOCAL APPLICATION PENDING
R6  ACCEPTED / LOCAL APPLICATION PENDING
```

The semantic-review stage of the bounded six-candidate B2 tranche is therefore complete. The current proven local Registry state remains the R1/R2 state until the accepted R3-R6 mappings are actually applied and verified on the maintainer SQLite database.

No R4-R6 alias is authorized.

---

## 2. R4 — develop RAG systems

### Decision

**ACCEPT**, with a narrower identity than the original tentative proposal.

Canonical concept:

```text
ID:          responsibility:develop-rag-systems
Label:       Develop RAG systems
Definition:  Developing retrieval-augmented generation (RAG) systems.
Category:    responsibility
```

Approved exact mappings:

```text
tvMm  artifact 50  responsibility[6]
→ Developing RAG and Knowledge-based systems

tNVe  artifact 56  responsibility[4]
→ developing RAG and Knowledge Retrieval
```

### Why the tentative identity was narrowed

The original candidate proposed `responsibility:develop-rag-knowledge-retrieval`. Both claims clearly share **RAG development**, but `Knowledge-based systems` and `Knowledge Retrieval` are not equivalent concepts. Promoting both phrases into the normalized identity would silently collapse that distinction.

The accepted reusable core is therefore only **develop RAG systems**. The additional source wording remains recoverable in each immutable claim:

- `Knowledge-based systems` stays specific to `tvMm`;
- `Knowledge Retrieval` stays specific to `tNVe`.

This is a stronger normalization boundary than the tentative proposal because it retains only the semantic intersection actually supported by both claims.

This concept does not infer vector databases, embeddings, chunking, re-ranking, evaluation, production deployment, source attribution, or any specific RAG architecture unless an exact mapped source claim separately states those facts.

---

## 3. R5 — multi-step AI workflows

### Decision

**ACCEPT**.

Canonical concept:

```text
ID:          responsibility:design-develop-multi-step-ai-workflows
Label:       Design/develop multi-step AI workflows
Definition:  Designing or developing multi-step workflows for AI or agent-based systems.
Category:    responsibility
```

Approved exact mappings:

```text
tvMm  artifact 50  responsibility[7]
→ Designing multi-step and reliable workflows

tNVe  artifact 56  responsibility[5]
→ developing multi-step workflows, and if necessary, Multi-Agent Integration with Email, Ticketing, and other system modules
```

The common reusable responsibility is creating multi-step workflow behavior in the AI/agent-system context of the two accepted postings. The normalized definition uses **designing or developing** so that it does not falsely assert that every mapped source claim explicitly owns both lifecycle verbs.

Source-specific scope is intentionally retained rather than normalized:

- `reliable` is additional scope in `tvMm`;
- Multi-Agent integration is additional conditional scope in `tNVe`;
- Email, Ticketing, and other-module integration are additional `tNVe` context;
- no shared orchestration framework, persistence mechanism, permissions model, human-approval model, or production guarantee is inferred.

---

## 4. R6 — evaluate and improve AI-system performance

### Decision

**ACCEPT**.

Canonical concept:

```text
ID:          responsibility:evaluate-improve-ai-system-performance
Label:       Evaluate and improve AI-system performance
Definition:  Evaluating and improving how AI or agent-based systems perform.
Category:    responsibility
```

Approved exact mappings:

```text
tvMm  artifact 50  responsibility[8]
→ Evaluating, debugging, and improving Agent performance

tNVe  artifact 56  responsibility[7]
→ evaluating and improving the quality, reliability, latency, and cost of AI systems.
```

The shared reusable action is explicit in both claims: evaluate and improve the behavior/performance of an AI or agent system.

Source-specific scope remains exact:

- `debugging` is additional scope in `tvMm`;
- quality, reliability, latency, and cost are explicit performance dimensions in `tNVe`;
- the normalized concept does not imply that every mapped claim covers every one of those dimensions.

Boundary claim:

```text
tvMm artifact 50 responsibility[9]
→ Paying attention to cost, Latency, Reliability, and output quality.
```

This claim remains **pending**. It expresses attention to operational qualities but does not assert the same explicit evaluate/improve action. Shared nouns are not enough to map it into R6.

---

## 5. Semantic review closure

The six-candidate review now has four accepted-but-unapplied concepts after R1/R2:

```text
R3  responsibility:implement-llm-tool-calling
R4  responsibility:develop-rag-systems
R5  responsibility:design-develop-multi-step-ai-workflows
R6  responsibility:evaluate-improve-ai-system-performance
```

Approved exact pending application set:

```text
R3  tvMm 50[3]  ↔ tNVe 56[3]
R4  tvMm 50[6]  ↔ tNVe 56[4]
R5  tvMm 50[7]  ↔ tNVe 56[5]
R6  tvMm 50[8]  ↔ tNVe 56[7]
```

If all eight accepted claims remain accepted/current and pending at application time, successful R3-R6 application would move the selected snapshot set from the currently proven **4/35 mapped** state to an expected **12/35 mapped** state, leaving 23 selected responsibilities pending. This is an expected postcondition only; it must not be represented as current state before local execution proves it.

Reviewed canonical correspondence remains distinct from `ResponsibilityFamily`, role archetype, market prevalence, or personal-readiness authority.

---

## 6. Combined local application protocol for R3-R6

Runtime authority is the maintainer local SQLite database and is intentionally absent from GitHub. Apply only after pulling current `main`, backing up the configured database, and reconfirming all eight exact claims are still accepted/current and pending.

```bash
cd ~/projects/jobhunter
git pull --ff-only
source .venv/bin/activate

python - <<'PY'
from pathlib import Path
import sqlite3
from jobhunter.config import Settings

settings = Settings.load('jobhunter.toml')
source = sqlite3.connect(settings.database_path)
out = Path('data/local-acceptance/b2-review-2026-10-17/pre-r3-r6-live.sqlite3')
out.parent.mkdir(parents=True, exist_ok=True)
dest = sqlite3.connect(out)
source.backup(dest)
dest.close()
print('backup=', out)
print('integrity=', source.execute('PRAGMA integrity_check').fetchone()[0])
print('foreign_keys=', source.execute('PRAGMA foreign_key_check').fetchall())
source.close()
PY

jobhunter-registry --config jobhunter.toml claims list \
  --job-id tvMm --kind responsibility --state pending
jobhunter-registry --config jobhunter.toml claims list \
  --job-id tNVe --kind responsibility --state pending

# R3
jobhunter-registry --config jobhunter.toml concepts add \
  responsibility:implement-llm-tool-calling \
  --category responsibility \
  --label "Implement LLM tool/function calling" \
  --description "Implementing tool calling or function calling for language-model-based systems." \
  --reason "B2 R3 accepted 2026-10-17: exact accepted/current tvMm[3] and tNVe[3] share implementation of Tool/Function Calling for LLM-based systems; Structured Output remains source-specific extra scope."

jobhunter-registry --config jobhunter.toml claims decide \
  tvMm responsibility 3 mapped \
  --concept responsibility:implement-llm-tool-calling \
  --reason "B2 R3 accepted exact correspondence: implementing Tool/Function Calling with LLMs."

jobhunter-registry --config jobhunter.toml claims decide \
  tNVe responsibility 3 mapped \
  --concept responsibility:implement-llm-tool-calling \
  --reason "B2 R3 accepted exact correspondence: implementing Tool/Function Calling; Structured Output remains additional source-specific scope."

# R4
jobhunter-registry --config jobhunter.toml concepts add \
  responsibility:develop-rag-systems \
  --category responsibility \
  --label "Develop RAG systems" \
  --description "Developing retrieval-augmented generation (RAG) systems." \
  --reason "B2 R4 accepted 2026-10-17: exact accepted/current tvMm[6] and tNVe[4] share RAG development; knowledge-based systems versus knowledge retrieval remain source-specific rather than normalized."

jobhunter-registry --config jobhunter.toml claims decide \
  tvMm responsibility 6 mapped \
  --concept responsibility:develop-rag-systems \
  --reason "B2 R4 accepted exact correspondence: developing RAG systems; Knowledge-based systems remains additional source-specific scope."

jobhunter-registry --config jobhunter.toml claims decide \
  tNVe responsibility 4 mapped \
  --concept responsibility:develop-rag-systems \
  --reason "B2 R4 accepted exact correspondence: developing RAG systems; Knowledge Retrieval remains additional source-specific scope."

# R5
jobhunter-registry --config jobhunter.toml concepts add \
  responsibility:design-develop-multi-step-ai-workflows \
  --category responsibility \
  --label "Design/develop multi-step AI workflows" \
  --description "Designing or developing multi-step workflows for AI or agent-based systems." \
  --reason "B2 R5 accepted 2026-10-17: exact accepted/current tvMm[7] and tNVe[5] share multi-step AI/agent workflow creation; reliability and multi-agent/business-system integration remain source-specific."

jobhunter-registry --config jobhunter.toml claims decide \
  tvMm responsibility 7 mapped \
  --concept responsibility:design-develop-multi-step-ai-workflows \
  --reason "B2 R5 accepted exact correspondence: designing multi-step AI/agent workflows; reliability remains source-specific."

jobhunter-registry --config jobhunter.toml claims decide \
  tNVe responsibility 5 mapped \
  --concept responsibility:design-develop-multi-step-ai-workflows \
  --reason "B2 R5 accepted exact correspondence: developing multi-step AI/agent workflows; Multi-Agent/Email/Ticketing/module integration remains additional source-specific scope."

# R6
jobhunter-registry --config jobhunter.toml concepts add \
  responsibility:evaluate-improve-ai-system-performance \
  --category responsibility \
  --label "Evaluate and improve AI-system performance" \
  --description "Evaluating and improving how AI or agent-based systems perform." \
  --reason "B2 R6 accepted 2026-10-17: exact accepted/current tvMm[8] and tNVe[7] share explicit evaluation and improvement of AI/agent-system performance; debugging and specific quality/reliability/latency/cost dimensions remain source-specific."

jobhunter-registry --config jobhunter.toml claims decide \
  tvMm responsibility 8 mapped \
  --concept responsibility:evaluate-improve-ai-system-performance \
  --reason "B2 R6 accepted exact correspondence: evaluating and improving Agent performance; debugging remains additional source-specific scope."

jobhunter-registry --config jobhunter.toml claims decide \
  tNVe responsibility 7 mapped \
  --concept responsibility:evaluate-improve-ai-system-performance \
  --reason "B2 R6 accepted exact correspondence: evaluating and improving AI-system performance; quality/reliability/latency/cost remain exact source-specific dimensions."
```

Do not map `tvMm` responsibility[9] during this batch.

---

## 7. Required application verification

After the first application, rerun the same concept/mapping commands and prove idempotent reuse. Then verify:

```text
all four accepted concepts exist exactly once
all eight approved R3-R6 claim mappings exist exactly once
exact artifact/source/translation/claim identities are preserved
original source/P1.6 wording remains recoverable
R1/R2 and all unrelated Registry rows are unchanged
CLI views show the same approved state
browser Registry views agree with CLI/source identity
SQLite integrity_check = ok
foreign_key_check = []
accepted P1.6 identities are unchanged
Market snapshot identities are unchanged
public corpus file hashes are unchanged by Registry mutation
no R4-R6 aliases were added
tvMm 50[9] remains pending
```

If the current local state has changed materially, stop and reconcile rather than silently substituting a claim or widening a concept.

No repository code/test change is required merely because these local semantic rows are applied. If application exposes a real product/contract defect, repair only that defect with focused regression evidence and normal CI before continuing.

---

## 8. Next gate after verified application

After R3-R6 are applied and verified, B2 should move to bounded closure/disposition:

1. record exact concept and mapping row identities plus idempotency/integrity/browser/CLI evidence;
2. record boundary claims left pending, including the R1/R2 broader cases and `tvMm` 50[9];
3. state explicitly that canonical correspondence is not `ResponsibilityFamily` or prevalence authority;
4. close B2 for the bounded six-candidate tranche;
5. **STOP** and make a separate P2.2C-vs-P2.3 readiness decision.

This record does not authorize P2.2C families, P2.2D archetypes, P2.3 profiles, P2.4 Market v2, bulk mapping, requirement canonicalization, or personal scoring.