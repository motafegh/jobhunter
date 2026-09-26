# Market I7 target-coverage follow-up

**Date:** 2026-09-26

The bounded I7 first-slice PASS remains valid. The owner requested additional
coverage of the same target beyond that accepted sample. This record tracks the
new work without treating incomplete semantic coverage as zero demand or
silently enlarging the original acceptance claim.

Run 7 used the same five one-page searches, request budget 5, no source refresh,
translation budget 2, analysis budget 0 and membership budget 10. It qualified
both previously remaining source-ready postings. Snapshot/profile 7 froze ten
members: seven core, one adjacent, two excluded. One new English projection
completed; translation for `tNVe` timed out after LM Studio accepted the
request. The run retained the completed membership and translation work and
reported `completed_with_failures`. The semantic core denominator remains one
accepted P1.6 posting out of seven qualified core postings.

The configured LM Studio translation provider used its 30-second timeout for
the entire HTTP operation, including the model's response generation. The
loopback `/v1/models` health probe remained responsive. Translation now bounds
connection, write and pool waits while leaving the read wait unlimited only for
`chat/completions`; model listing keeps a bounded read. Provider identity and
translation prompt are unchanged. A focused transport regression covers the
timeout split. Corpus-wide offline planner tests now inspect every available
English projection rather than requiring the historical count of 27; run 7
added the 28th projection and exposed those brittle assertions.

Ruff passed, 742 tests passed with warnings as errors, and the public corpus
verified for 410 known jobs. The run's local ledger, snapshot and database
backup remain under ignored `data/local-acceptance/i7/`. Public corpus changes
contain only governed source observations and the completed English projection;
Market target, run, membership, snapshot and profile state remains local.

Next: retry only the missing `tNVe` translation through a bounded target run,
then review current core P1.6 candidates one at a time against exact source
evidence. Do not auto-accept model output or call this target semantically
complete while any core posting remains missing/pending/rejected.
