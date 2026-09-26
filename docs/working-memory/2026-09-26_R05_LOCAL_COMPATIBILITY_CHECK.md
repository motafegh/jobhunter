# R05 local compatibility check — 2026-09-26

**Status:** bounded local compatibility verified; real candidate review and Market I7 remain outstanding.
**Repository head at check:** `59643b4` on `main` (equal to `origin/main` after fetch and fast-forward pull).

The existing `data/jobhunter.sqlite3` was inspected read-only. SQLite integrity returned `ok`, foreign-key check returned no violations, and the database contained 41 analysis artifacts, 109 analysis attempts, and two immutable Market snapshots. It contained no pending English v21 analysis, and neither R05 sidecar table had yet been initialized. Historical failed attempts cannot retroactively supply unavailable provider completions.

The SQLite backup API copied the operational database to a temporary private file. Initializing the A2 diagnostic and B item-review stores on that copy added the intended sidecar tables and acceptance trigger. Analysis artifact, attempt, snapshot, and snapshot-member row counts were unchanged. The copied database still returned `ok` for integrity and no foreign-key violations. The operational database was not migrated or mutated by this check.

The installed local Instructor version is 1.15.4. Its `InstructorRetryException` exposes `failed_attempts`; each `FailedAttempt` exposes `attempt_number` and `completion`. A regression now constructs these actual installed classes and proves the private diagnostic store captures available completion message text with the retry number. This is an installed-library shape check without an LM Studio call; it does not prove a real provider failure will include a usable completion.

Verification at this increment: 13 focused R05 tests passed; the full warnings-as-errors suite passed 726 tests; Ruff passed on the changed test.

There is no current pending v21 candidate on which to perform an honest real reviewer session, and the prior `tvMm`/v22 stop line forbids a model retry merely to manufacture one. Browser/CLI reviewer usability on representative live evidence, actual failure capture, corrected-revision identity, and accepted-semantic Market drill-down remain unverified. Preserve Market I7 HOLD and the public v21/v5 contract.
