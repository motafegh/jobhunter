# P1.6 v20 — First Live Partition Correction

**Date:** 2026-08-14  
**Status:** correction implemented; deterministic CI passed; dense live rerun pending  
**Candidate:** `job-analysis-english-v20` / `job-analysis-v5`  
**Branch:** `agent/p16-v20-source-led-partitioning`  
**Draft PR:** #8

## 1. Live result

The first dense `tG9K` v20 run did not persist an artifact. V20 reached partition 1 and failed inside typed requirement validation before later partitions could run.

Both bounded Instructor generations represented:

- the dense duty coverage;
- `Solid` statistics/signal-processing;
- validation/reproducibility/documentation discipline;
- MATLAB as preferred with `depth_signal=null`;
- C/C++ as preferred from `some C / C++ helpful`.

The remaining blocking item was C/C++:

```text
concept:          C / C++
requirement_type: preferred
depth_signal:     some
evidence:         some C / C++ helpful
```

The shared strict depth validator rejected `some` because JobHunter's accepted technical-depth / experience-extent vocabulary is intentionally bounded to explicit signals such as expert/proficient/mastery/familiarity/strong/solid/hands-on/comfort/years. The retry reproduced the same representation.

This is not a partitioning failure and does not justify increasing retries. It is an inherited item-normalization gap exposed by the new bounded partition.

## 2. Semantic decision

The exact source phrase contains two different kinds of information:

```text
some C / C++ helpful
^^^^               vague quantity/extent
             ^^^^^^^ explicit preference/optionality
```

For JobHunter's structured contract:

- `helpful` correctly establishes `requirement_type=preferred`;
- `some` is preserved in exact evidence but is too vague to become one of the accepted technical-depth values;
- therefore `depth_signal=null` is the conservative normalized representation unless the same evidence contains an independently accepted depth/experience-extent phrase.

The source information is not discarded because exact evidence remains durable and reviewable.

## 3. Correction

V20 now defines `AnalysisRequirementV20` / `JobAnalysisResponseV20` for partition calls.

Before inherited strict validation, `depth_signal="some"` is cleared only when all are true:

1. `requirement_type == "preferred"`;
2. the proposed depth is exactly the vague quantifier `some`;
3. the exact cited evidence itself contains `some`;
4. the exact cited evidence contains explicit English optionality/preference wording;
5. the exact cited evidence contains no independently accepted JobHunter depth or experience-extent marker.

This is deliberately narrow. It does not add `some` to the global depth vocabulary and does not affect required/contextual claims.

A source such as:

```text
Strong C / C++ preferred
```

still preserves `depth_signal=Strong`.

A non-preferred source such as:

```text
some C / C++
```

is not silently repaired and remains fail-closed under the inherited depth validator.

## 4. Role-purpose signal observed in the same live output

The first v20 partition also placed source segment 0 in `responsibilities` and returned `role_purpose=[]`, whereas the prior dense baseline treated the high-level statement as role purpose and kept the concrete duty surfaces separate.

No tG9K-specific deterministic rewrite was added. That distinction remains semantic/model-owned. The v20 prompt now explicitly reminds the model:

- high-level role mission belongs in `role_purpose`;
- concrete work belongs in `responsibilities`;
- sharing one responsibility coverage ledger does not mean every covered span must be emitted as a responsibility.

This remains an explicit dense semantic acceptance check after persistence.

## 5. Regression coverage

`tests/test_analysis_v20_candidate.py` now proves:

- exact live shape `some C / C++ helpful` + model `depth_signal="some"` canonicalizes to preferred + null depth while preserving exact evidence;
- real preferred technical depth (`Strong C / C++ preferred`) remains `Strong`;
- `some` without explicit preference evidence is not silently cleared and still fails strict validation;
- v20 prompt contains the role-purpose/responsibility distinction;
- all existing partition coverage/merge/leakage tests remain active.

## 6. Deterministic verification

Implementation CI after this correction:

```text
run 753
Ruff: PASS
full pytest: PASS
pytest -W error: PASS
```

A final CI pass is still required after documentation reconciliation.

## 7. Acceptance boundary

Public/accepted truth remains unchanged:

```text
job-analysis-english-v9 / job-analysis-v4
tG9K P1.6 artifact 29
Capability v7 artifact 9 derived from artifact 29
```

No v20 artifact has persisted yet. Do not run sparse `t4jp`, rebuild Capability, advance heterogeneous-role review, promote P1.6, or merge candidate PRs.

## 8. Next live action

After pulling the reconciled v20 branch:

```bash
python scripts/run_p16_v20_candidate.py --job-id tG9K
```

If an artifact persists, perform the full dense semantic review before authorizing sparse non-regression.
