# Market I7: isolated MiMo 9B comparison

**Date:** 2026-09-27  
**Disposition:** useful candidate evidence; no model promotion

The owner supplied `MiMo-V2.6-Distill-Qwen-9B-Q4_K_L` for a bounded
comparison. LM Studio indexed it as `mimo-v2.6-distill-qwen-9b`; a 16K context
estimate was 7.18 GiB, and the model loaded successfully. The evaluation used
the current v23/v5 P1.6 contract and a SQLite backup under ignored
`data/local-acceptance/i7/`. It bypassed the public-corpus synchronization
wrapper. Live accepted artifacts, Market state and tracked corpus were not
changed by either model run.

On `tjgi`, MiMo persisted pending artifact 58 in the isolated copy with nine
duties and 23 requirements. It preserved the source alternative `GitHub or an
online demo` that configured Gemma artifact 57 had collapsed. Source review
also noticed that explicit `Experience using Claude Code, Codex, Cursor, or
similar tools` was labeled `concept_type=tool` while retaining the experience
wording in its concept. This is an ontology concern for downstream use.
Artifact 58 remains **pending in the isolated copy**, with no acceptance or
runtime authority.

The first isolated `t7Ay` request did not reach inference because the LM
Studio server had stopped between calls. The server was restarted on the
configured loopback port `18080`, and MiMo was reloaded. The subsequent
bounded `t7Ay` attempt 130 failed validation after its allowed correction:
both responses supplied coverage exclusions for IDs outside the active
partition. No artifact was persisted. This is model contract nonadherence,
not evidence that the source requirement is absent. The failed connection
and the model validation failure are distinct outcomes.

The configured Gemma model was restored after the comparison. These two cases
show one useful semantic improvement and one material protocol failure. They
do not justify changing the public analysis model, invalidating existing
accepted artifacts, or treating pending MiMo output as accepted Market
coverage. Future model comparison should remain isolated and be judged by
whole-artifact source review and exact dependency identity.
