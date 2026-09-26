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

Run 8 retried only the missing `tNVe` translation under the repaired transport.
It completed with no stage failures, no source refresh or P1.6 generation, and
ten of ten source-ready target postings now have current English projections.
Membership again completed for all ten with seven core, one adjacent and two
excluded. The new immutable snapshot/profile 8 retains one accepted-semantic
core posting out of seven. The public corpus now has 29 current English
projections; no Market-local state was published.

Run 8 discovered one additional public source identity, bringing the corpus to
411 known jobs, 51 parsed details, 29 current English projections, six accepted
English P1.6 artifacts and five accepted Capability artifacts. Corpus
verification passed at this checkpoint.

Next: review current core P1.6 candidates one at a time against exact source
evidence. Do not auto-accept model output or call this target semantically
complete while any core posting remains missing/pending/rejected.

2026-09-27 continuation: the first normal v23 `tmvA` P1.6 attempt 112 failed
closed with no artifact. Retained diagnostic responses cited exact qualification
items, while the runtime also demanded the same broad sentence references in
a different partition. The distinct v24 candidate and bounded evaluation
decision are recorded at
`docs/working-memory/2026-09-27_MARKET_I7_V24_QUALIFICATION_OWNERSHIP_DECISION.md`.
Public v23 remains current pending real semantic review.

The same-target source review also corrected `taOX` membership from
high-confidence core (record 4) to medium-confidence adjacent (new immutable
record 15). Its principal duties deploy AI tools across departments, automate
internal work, train staff, and improve content, sales, support and
administration; custom assistant setup is one task. Against definition 1's
primary AI-system-development intent, adjacent is the bounded interpretation.
The repository correction service passed a private-copy dry run, then wrote
record 15 with exact English and original-source description references.
Snapshot/profile 9 froze ten members as six core, two adjacent and two
excluded, with one accepted-semantic core, one failed v23 core attempt and four
missing core analyses. Snapshot 8 remained byte-identical after correction;
SQLite integrity and foreign keys passed. This correction does not erase the
historical core classification from snapshots 1-8.
Run 9 discovery raised the repository-safe known identity count to 412;
public-corpus verification passed with 51 details, 29 English projections,
six accepted English P1.6 artifacts and five accepted Capability artifacts.
