# P2.3A comparison — independent local engineering review

**Run date:** 2026-11-11
**Source:** Local WSL checkout of `review/p23a-compare-usefulness-2026-11-06` on base main `21f9d03`.
**Scope:** Technical checks only; no owner usability acceptance or claims of time savings.
**Privacy:** TestClient probes and deterministic counts against temporary SQLite copies. Only aggregate metrics and fixed public job IDs are published.

## Automated evidence

The read-only capture script produced `AUTO_METRICS.json`; all four cases were `evaluated`.
The SQLite snapshot integrity check returned `ok` and zero foreign-key violations.
No acquisition, translation, or model calls were made by the capture.

| Scenario | Accepted matching claims | Direct matching responsibilities | Important boundary |
| --- | --- | --- | --- |
| RAG: tvMm / tNVe / t7Ay | 3 / 4 / 3 | 1 / 1 / 0 | t7Ay has requirements, no direct duties |
| Python: tG9K / tmBK | 2 / 2 | 0 / 0 | Both have optional current Capability groups, whose memberships overlap |
| Requirement-only: t7ck / t7Ay | 18 / 26 | 0 / 0 | No fabricated work from qualifications |
| No-match: tvMm / tNVe | 0 / 0 | 0 / 0 | No match does not establish absent demand |

## Browser HTTP rendering probes

The existing `build_runtime_app` was exercised with Starlette TestClient against a separate temporary snapshot of the populated local SQLite database. No interactive browser or visual usability session was claimed.

| Probe | Result |
| --- | --- |
| RAG comparison | HTTP 200; three job cards, ten expandable evidence sections and ten source drill-down links; requirement-only warning present |
| Python comparison | HTTP 200; two job cards, four evidence/drill-down links; existing job-local capability-group presentation present |
| Requirement-only comparison | HTTP 200; two job cards, 44 evidence/drill-down links; no-direct-responsibilities warning present |
| No-match comparison | HTTP 200; explicit no-match notice; zero matching evidence/drill-down links |
| Four repeated job parameters | HTTP 422, above the bounded three-job limit |
| Temporary database copy | Same byte length before and after TestClient reads; this size observation alone does not prove bytewise identity |

These are structural/rendering observations, not proof of usefulness, accessibility conformance, equivalence of Python/RAG concepts, or user effort reduction. A real browser assessment, including navigation friction and comprehension, remains an independent gate.

## Engineering disposition

- Local script compiled and Ruff passed.
- Focused `tests/test_job_comparison.py`: 10 tests passed with warnings as errors.
- Dependency consistency: no broken requirements.
- Full-project strict-warning test suite: **878 passed in 47.68s**.
- Full repository Ruff check passed; dependency consistency check passed.

**Decision:** Automated technical evidence is consistent with the intended bounded factual comparison contract. This review does **not** accept P2.3 profiles, promote a canonical taxonomy, establish measured time savings, or substitute for the owner repeated-use review.

**Next gate:** Owner manually evaluates scenarios and records genuine experience in `OWNER_REVIEW.md`, then the team chooses a bounded follow-on increment. The unfilled owner template must not be treated as acceptance.
