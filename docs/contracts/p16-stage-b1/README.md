# Stage B1 source evidence candidate — design-only contract

**Status:** B1 design artifacts only. No new production P1.6 analysis, schema migration, model calls, source acquisition, UI, or accepted employer facts.
**Contract:** `jobhunter-stage-b1-source-evidence-bundle-draft-v1`.
**Authoritative ADR:** `../../working-memory/2026-11-14_P16_B1_SOURCE_ITEM_BILINGUAL_CONTRACT_ARCHITECTURE_DECISION.md`.

The JSON Schema `source_evidence_bundle.schema.json` describes an isolated, original-source-owned interpretation candidate. It deliberately separates exact original description anchors, typed board metadata references, semantic categories, conditional obligation strength, eligibility logic, English translation association, review events and read-only candidate brief limits.

The four fixtures in `fixtures/` are from previously exposed, retained job advertisements. They store **only source-version IDs, hashes, character offsets, proposed categories and reviewer provenance**. Full Persian original descriptions, source HTML, translation text, human responses and model outputs remain under ignored local `data/local-acceptance/` and are not supplied through this public contract. These fixtures are not an independently blinded holdout and are not accepted P1.6 artifacts.

The B1 draft uses `legacy_field_only_unaligned` for the status that Stage A calls `translated_field_only_unaligned`; this is a named mapping, **not** a new claim of original-to-English item correspondence. Synthetic source-bound target relations can represent associations, but do not prove meaning equivalence. Source semantic and translation review are separate.

The pure design validator is `scripts/validate_stage_b1_design.py`; the source-safe fixtures can be checked with:

```bash
PYTHONPATH=.:src python scripts/validate_stage_b1_design.py \
  docs/contracts/p16-stage-b1/fixtures/*_source_safe_design.json
python -m pytest -q -W error tests/test_p16_stage_b1_contract_design.py
```

When the private frozen B0 SQLite evidence is present, the focused tests reverify the exact original text and English v2 field provenance on an isolated **copy**. CI without private files tests structure and references only; neither mode certifies semantic quality or makes a production acceptance decision.

**Next:** B2 original-language source item interpretation and board-metadata conflict handling, separately gated. B3 bilingual meaning verification, B4 useful view, B5 unseen evaluation, and B6 controlled promotion remain ahead.


The review-state validator requires a review event in the **semantic_classification**
dimension before an item can claim assistant or independent semantic checking.
A source-integrity check or translation-association check does not count.
Structured-board JSON Pointers follow RFC 6901 escape rules and canonical
decimal array indexing. These restrictions are draft-contract mechanical fences,
not semantic truth or downstream acceptance.
