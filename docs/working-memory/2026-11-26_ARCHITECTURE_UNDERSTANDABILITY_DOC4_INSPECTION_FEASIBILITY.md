# Architecture understandability — DOC.4 code-derived inspection feasibility

**Date:** 2026-11-26. **Inspected revision:** `ab5dca798e60283eb32fed366fe516b7f833e557` (main; inspected source unchanged). **Disposition:** retain a bounded, optional developer prototype, not a production feature, whole-system architecture generator or new acceptance authority. Prior DOC.3 [CI 45860931648](https://github.com/motafegh/jobhunter/actions/runs/45860931648) passed. Controls: [DOC.2 verified map](2026-11-25_ARCHITECTURE_UNDERSTANDABILITY_DOC2_P16_RUNTIME_BASELINE.md), [DOC.3 profiles](2026-11-26_ARCHITECTURE_UNDERSTANDABILITY_DOC3_COMPONENT_PROFILES.md), [component standard](../COMPONENT_PROFILE_STANDARD.md). No change to selected E2.5 experimental design, 47-cell matrix, scoring, model selection or authority boundaries.

## 1. Decision and utility

Implement [scripts/inspect_p16_architecture.py](../../scripts/inspect_p16_architecture.py) as an optional read-only inspection aid. Repeated manual reconstruction of inherited method ownership, validator sets and file identities is error-prone and comparatively mechanical. A curated report makes these facts reproducible and exposes drift without pretending to infer the system's meaning. This is intentionally scoped to P1.6 and its immediate dependency/consumer seams, not an automatic call graph, generalized scanner, service, CI gate or documentation authority. No new third-party dependencies; Python standard library for the default static mode, existing installed JobHunter/Pydantic stack only for optional class inspection. Tests run in the existing development suite.

## 2. How to use

From repo root (activated existing virtual environment):

```bash
python scripts/inspect_p16_architecture.py
python scripts/inspect_p16_architecture.py --runtime --format markdown
python scripts/inspect_p16_architecture.py --runtime --frozen-schema-db \
  data/local-acceptance/p16-doc4-2026-11-26/closed-schema-inspection-copy.sqlite3
```

JSON is the default, Markdown is optional. Output to stdout only; redirect to an ignored local path when desired. Static mode reads a fixed source-file allowlist, hashes bytes, parses AST and identifies lexical definitions, internal module imports and call expressions in four selected methods. Git revision and inspected-source dirty flag identify scope; the flag is not a whole-tree/closure cleanliness claim. No source modules imported in default mode. Git reads use GIT_OPTIONAL_LOCKS=0. Runtime flag starts an isolated Python child with -I -B, minimal environment, 30s timeout and a reviewed class/method allowlist; resolves effective owners, MROs, fields, required fields, schema digests and Pydantic decorators without constructing services or invoking inference. Audit hook denies selected file writes, sockets, SQLite opens, subprocesses and other side-effect events. This is defense in depth for trusted repository code, not an OS sandbox or arbitrary untrusted Python inspection. If optional inspection fails, use static/manual fallback; do not weaken safeguards.

Schema flag requires an explicitly closed frozen SQLite copy below data/local-acceptance, not a live configured database. Resolves path, rejects sidecars, uses mode=ro and immutable=1 (caller must guarantee snapshot is closed), query_only and a restrictive SQLite authorizer: only schema metadata SELECT/allowed table_info and foreign_key_list PRAGMAs, no application-row reads or DML. No raw DDL, defaults or row values in output; table/column/type/PK/FK and trigger names only. File size/mtime/inode and absence of sidecars rechecked after inspection; this is not a guarantee against concurrent writers. No production store initialization. Snapshot presence/absence is not a statement about today's database. No provider credentials, model weights, prompts, raw source or external network requests needed.

## 3. Observed comparison against verified P1.6 documentation

| Inspection | Actual result | Comparison / boundary |
| --- | --- | --- |
| AST inventory | 44 curated files, 456 lexical definitions, 281 distinct file/internal-import pairs | All 31 prior DOC.2/DOC.3 source fingerprints and 65 named symbols/line locations matched. Additional files cover selected inheritance seams; not transitive closure. |
| Method resolution | 10 effective methods, 4 class MROs | All match DOC.3 receipt. Resolves V30 requested provider complete_structured to V16 and _run_once to V27; service persistence to V28. Not evidence of which branch executed for a job. |
| Pydantic | Requirement 8 fields, 13 model validators; response 4 fields, 4 model validators | Consistent with DOC.2 counts; schema hashes, field/required names and decorator owners inspectable. Not exact serialized Instructor request, validator behavior or semantic correctness. |
| SQLite | 7 selected table names; 5 present, 2 absent; 6 FK constraints, no selected trigger rows | Historical B0 frozen schema matches core source -> translation -> analysis/attempt links. Review sessions/events absent in this snapshot, not missing from current source implementation. |
| Reproducibility | Two complete JSON reports byte-identical | Same inspected revision, files, local dependency environment and closed copy; not cross-environment equivalence. Generated Markdown is [retained safe sample](2026-11-26_doc4_inspection/GENERATED_P16_INSPECTION.md). |

Concrete misleading/missing edges if automation is interpreted as execution:

- V30 provider imports V29, yet complete_structured resolves to V16; V29 import is not a call to V29.complete_structured. The V16 lexical call self._attempt does not resolve its conditional V15 super path or establish the nested recovery count. The V15 self._run_once call does not resolve V27/V25/V23/V21/V20 chain merely from syntax. DOC.2 owner map and offline replay remain necessary.
- A lexical reference to complete_analysis_partition_with_instructor_v24 is real syntax in V30._complete_partition, not proof a model request occurred. _filter_unassigned_partition_claims is in the same method, but order/failure/coverage semantics must be read and tested. Schema field names/validator count cannot establish the observed false-duty or depth failures.
- Historical SQLite FKs show structural relationships, not accepted/current selectors or authorization. The item-review acceptance-fence trigger exists in current source (analysis_item_review.py initialize), but absent B0 tables cannot prove today's trigger is installed or absent; inspect code and relevant isolated tests. Foreign keys alone do not prove pending artifacts blocked by Capability or semantic acceptance.
- Scope explicitly omits exhaustive acquisition, UI, market/personal and historical code. Imports can be conditional, type-only or indirect, alias resolution and dynamic dispatch incomplete. No automatic deletion decisions or complete architecture graph derived from import inventory.

The generated Markdown uses a small dashed-arrow Mermaid graph labeled **imports**, not calls; rendering not verified here. No automatic runtime sequence emitted. Retain manually verified maps and profiles as primary narrative; generated reports are supporting evidence, not replacements.

## 4. Safety, validation and maintenance

The first schema attempt correctly refused the old frozen B0 file because WAL/SHM sidecars existed. Did not remove them. Verified source SHA against the retained frozen baseline (693c054338cdd2a4e6652f3d78129d24b4ae6c29d6ea35413ab08986eba8ac7c), observed zero-length WAL before/after byte copy into ignored private local-acceptance directory, and verified source/copy digests match. No application rows queried or published; copy is existing private evidence, not new source acquisition. Inspected only closed copy with no sidecars and verified unchanged digest. Immutable inspection is only safe on a closed snapshot. Synthetic SQLite fixture exercises absent table reporting, FK, trigger name, denied private row reads and mutation; sidecar and outside-acceptance path rejection tested. Tests exercise actual curated runtime introspection and audit-hook guard function (not a comprehensive OS security proof), deterministic reports and lexical import/call separation.

One initial test expected a narrower wording of the graph disclaimer; corrected the assertion to match the existing truthful limitation, not runtime behavior. Final focused suite: **40 passed with warnings as errors**, including 12 new developer-tool tests. Ruff passed for changed Python. Protected-state reconciliation and safe report comparison in [receipt](2026-11-26_doc4_inspection/SAFE_DOC4_INSPECTION_VERIFICATION.json). No inference, model load, acquisition, production migration or accepted-state changes.

Maintenance cost: a single 420-line developer script and 130-line test module, fixed P1.6 scope, no configuration framework, new dependency, public entrypoint or automatic publishing. Scope/owner lists are curated and require changes when contracts move. Prefer this limited prototype over a generic import crawler/whole-system analyzer; if optional runtime dependencies or future audit restrictions fail, static extraction and manual DOC.2/DOC.3 inspection remain sufficient. DOC.7 decides proportionate drift practice and demonstrates it, not an immediate mandatory CI architecture gate. DOC.6 may extend only when concrete need justifies cost.

**Next:** DOC.7 orientation/currentness practice, DOC.5 selected architecture map, then E2.6 requirements freeze. DOC.4 complete as bounded feasibility/prototype, not proof of semantic quality or full architecture coverage.
