# P1.6 Stage A — passive source identity foundation and owner Pass A package

**Date:** 2026-11-13
**Status:** Stage A foundation mechanically approved for an INACTIVE merge; human semantic review remains pending.
**Candidate branch:** feature/p16-source-identity-foundation-2026-11-13
**Before-branch accepted main:** fd19e24c0550b98b819b80a282fac776b8956722
**Public P1.6 generation:** English v30/v5 unchanged. Original v9/v4 unchanged.
**Related research:** research/p16-original-source-evidence-spine-2026-11-13 (4035d7b) and experiment/p16-source-fidelity-2026-11-12 (03d6071).

## Decision

Safe, passive source-provenance infrastructure should not remain on a research branch indefinitely, but the experimental source-section parser and semantic classifications are NOT ready for production. Therefore this stage deliberately integrates a SMALL, stable subset of what the research established, with its own versioned contract. It does NOT cherry-pick or bulk merge the original research branch.

### Accepted passive modules

- `src/jobhunter/source_span_identity.py`: `jobhunter-source-span-identity-v1`, exact Unicode character and UTF-8 byte coordinates in the parsed original employer description, semantic source version and detail version binding, field/source text SHA-256, deterministic anchor ID, and strict verification of stale/tampered source anchors. No required/preferred/duty inference is performed.
- `jobhunter-legacy-field-alignment-v1`: checks a saved English projection v2's exact source dependency. For literal native-English descriptions, returns exact English offsets. For existing Persian-to-English whole-field translations, returns **translated_field_only_unaligned** with NO invented English item offsets or source equivalence.
- `scripts/build_owner_source_review_packet.py`: isolated snapshot-only offline review packet builder; no model invocation or DB mutation; displays original Persian source with structured board metadata separately; exports Pass A responses as an offline JSON download. Public original source URLs are explicitly restricted to Jobinja. Raw original content is not committed.
- `tests/test_source_span_identity.py` and `tests/test_owner_source_review_packet.py`: focused exact-identity, Unicode, stale dependency, false alignment, link sanitization, HTML escaping and manual-review blinding regressions.

The predecessor `source_lineage_v1.py` contains research-only heading heuristics and version-specific candidate item classifications. It is NOT part of this merge, as its section-boundary stability and semantic authority need independent review. The new passive source-anchor IDs are distinct from the prior research candidate IDs. A historical candidate source-span ID must never be silently used as a new anchor ID.

## Real-data verification

On preserved original parsed sources in the ignored November 12 isolated test database, the passive anchor builder was applied to every retained source offset recorded by the research `PRIVATE_REVIEW.json`:

| ID | Original exact spans verified |
| --- | ---: |
| tNhZ | 17 |
| tMps | 10 |
| tMqd | 3 |
| tNDx | 19 |
| tMjm | 4 |
| **Total** | **53 / 53** |

Every new exact anchor matched the preserved original text and UTF-8 offsets, and validation against the archived field-level English translation returned `translated_field_only_unaligned`. That verifies mechanical compatibility and honest uncertainty, not the semantic correctness of the 53 earlier research classifications.

No current P1.6 artifact, model completion, source version, translation, Capability, Work, Registry, Market, or corpus state was created, rewritten or promoted in this exercise.

## Owner manual review: first source-only package

The owner explicitly agreed to be an independent human reviewer and asked for prepared packages. First bounded packet: **JH-OWNER-A1-20261113**, four exposed diagnostic cases (`tNhZ`, `tMps`, `tNDx`, `tMjm`), chosen for distinct failure modes, not as a protected holdout.

- Public source-only review guide: `docs/review-packets/2026-11-13_JH_OWNER_A1_SOURCE_ONLY.md`.
- Private offline full-source page, manifest, README: `data/local-acceptance/owner-audit-2026-11-13/packet-a/`.
- Copied to owner's Windows Downloads: `JobHunter_Owner_Audit_A1_2026-11-13/PASS_A_SOURCE_ONLY.html` and corresponding ZIP.
- **Pass A is independent and unfinished.** The offline page provides eight separate free-text fields per job and a confidence selector; it produces `JH-OWNER-A1-20261113_PASS_A_RESPONSES.json` when Save is selected. Empty fields / cannot-determine are allowed.
- **Pass B is withheld** until the owner saves Pass A. The model answers are not embedded in the offline or public source-only guides. No reviewer outcome, acceptance or signed verdict is fabricated.
- Public GitHub contains only source URLs, frozen source hashes, and prompts, not the raw copied employer description, original/full translation, model output or personal review annotations.

The offline HTML/JS were checked for source-only content, escaping and response-download behavior. The packet source HTML hash and case metadata are kept in its local frozen manifest. Original-site content may have changed since November 12; the full-source offline snapshot is the comparison anchor.

The planned Pass B comparison inputs are independently sealed in ignored local data at data/local-acceptance/owner-audit-2026-11-13/packet-b-sealed/MODEL_COMPARISON_SEAL.json with SHA-256 112f7f10912a22560ef1073a13d0983d00d62bd7abc5db43f64fb8df26900c07. They have not been released to the owner, and no Pass B verdict is claimed.

## Compatibility and no-promotion gate

The stage is scoped to passive code and a review utility, without imports into the public P1.6 routing, model/translation service entrypoints, persistent storage, CLI, database migrations or UI templates. Existing v30/v9 analyzer behavior must remain byte-for-byte unchanged. No runtime calls to LM Studio are needed.

The next milestone, **Stage B**, is source-to-English item alignment with explicit review states and a model-versus-review comparison after the owner completes Pass A. A separate unseen verification cohort is still needed. Do not treat exposed diagnostic performance as general market reliability.

**Stage A verification:** 907 warnings-as-errors pytest tests passed; Ruff passed repository-wide, pip dependency consistency passed, git diff check passed. 23 new focused regressions passed and all 53 real source offsets matched; offline HTML review form, source-only blinding, JS download JSON simulation and privacy checks passed. Branch CI is verified separately after publication.

**Stage A merge criterion:** full warnings-as-errors suite, Ruff, dependency checks, real-source span identity verification, offline review packet/HTML integrity checks, review-output behavior test, privacy screening, clean working tree and branch review.

**Stop line:** Stage A is NOT a semantic promotion of source-lineage heuristics, a P1.6 v31 rollout, a new durable source-alignment database, or authorization for automatic skill requirements from structured Jobinja tags.
