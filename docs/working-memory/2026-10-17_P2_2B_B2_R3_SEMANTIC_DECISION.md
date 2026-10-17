# P2.2B-B2 R3 Semantic Decision — 2026-10-17

**Status:** ACCEPTED SEMANTIC CORRESPONDENCE / LOCAL APPLICATION PENDING  
**Scope:** R3 only — implement LLM Tool / Function Calling.  
**Authority:** owner delegated the remaining R3 semantic gate to the assistant on 2026-10-17. This record closes that semantic gate but does not claim a local SQLite mutation that has not been executed.

## Decision

R3 is **ACCEPTED**.

Canonical concept:

```text
ID:          responsibility:implement-llm-tool-calling
Label:       Implement LLM tool/function calling
Definition:  Implementing tool calling or function calling for language-model-based systems.
Category:    responsibility
```

Approved exact mappings:

```text
tvMm  artifact 50  responsibility[3]
→ Implementing Tool Calling / Function Calling with LLMs

tNVe  artifact 56  responsibility[3]
→ implementing Tool / Function Calling and Structured Output
```

The shared reusable responsibility core is direct: both accepted/current source-backed responsibility claims assert implementation of Tool/Function Calling in an LLM-based system. `Structured Output` is additional source-specific scope in `tNVe`; it is preserved in the original claim and deliberately excluded from the normalized definition.

This correspondence does **not** infer a shared framework, autonomous execution model, permissions model, deployment responsibility, orchestration architecture, production guarantee, or Structured Output responsibility across both jobs. R2 service/API integration remains a separate canonical responsibility.

No alias is justified for this application.

## Evidence boundary

The accepted source-backed P1.6 responsibilities are:

- `tvMm` artifact 50 responsibility[3]: `Implementing Tool Calling / Function Calling with LLMs`.
- `tNVe` artifact 56 responsibility[3]: `implementing Tool / Function Calling and Structured Output`.

Both claims were already recorded as accepted/current and pending Registry review under the B2 decision. The repository CI at head `e1b21e29` passed dependency checks, installed-entrypoint smoke, Ruff, normal pytest, and pytest with warnings as errors before this decision was recorded.

## Exact local application protocol

Runtime authority remains the maintainer's local SQLite database. It is intentionally not stored in GitHub, so this repository-side decision cannot honestly claim the Registry rows already exist.

Before mutation, pull current `main`, back up the configured database, and reconfirm the exact two claims are still accepted/current and pending. Then apply only the approved concept and mappings through the existing manual Registry CLI:

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
out = Path('data/local-acceptance/b2-review-2026-10-17/pre-r3-live.sqlite3')
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
```

## Required verification after application

The application is complete only after all of the following are demonstrated:

```text
concept creation/reuse is idempotent
both mapping commands are idempotent
exact artifact/source/translation/claim identities are preserved
Registry CLI shows the two approved mappings and original wording
browser Registry views agree with CLI/source identity
SQLite integrity_check = ok
foreign_key_check = []
R1/R2 and all pre-existing Registry rows are unchanged
accepted P1.6 / Market snapshot identities are unchanged
public corpus files are unchanged by Registry mutation
```

Until those checks are executed against the local runtime database, status is **semantic ACCEPT / application pending**, not applied/verified.

## Next semantic gate

After R3 application and verification, continue to R4 (`develop RAG / knowledge retrieval`) under the same ACCEPT | HOLD | REJECT boundary. This decision does not pre-authorize R4-R6, P2.2C families, P2.2D archetypes, P2.3 profiles, P2.4 Market v2, or personal scoring.
