# R05 Increment B — item-level review acceptance checklist

**Status:** ACTIVE ENGINEERING CHECKLIST / NOT A PROMOTION APPROVAL  
**Parent:** `2026-09-24_P16_R05_MINIMAL_RECORD_AND_DIAGNOSTIC_CAPTURE_DESIGN.md`.

An implementation is not complete merely because it stores comments. It must: retain the immutable original claim text and evidence; address a claim via exact artifact ID, collection, original ordinal and content digest; distinguish material semantic concern from benign uncertainty; represent source coverage gaps independently; preserve proposed corrections as review-only proposals, never overwrite source or claim; keep existing whole-artifact accept/reject decisions; refuse acceptance when a material recorded issue remains unresolved, including through CLI and browser; keep historical accepted artifacts and index-based Registry mappings unchanged; and prove absence of review/diagnostic sidecars from authoritative current queries and public corpus. Existing historical accepted artifacts without a newly started review workflow must not be mass-reopened.

The smallest implementation may initially expose review through the CLI, but complete user-facing B requires an integrated browser view, reviewer controls, and explicit coverage-checked completion. Do not promote corrected payloads until revision identity and downstream dependency migration have their own acceptance evidence. Maintain Market I7 HOLD independently.
