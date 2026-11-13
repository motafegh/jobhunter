# Erratum: EDR teamwork source-obligation interpretation

**Recorded:** 2026-11-13
**Applies to:** 2026-11-12 independent real-job evaluation, job `tNDx`.
**Disposition:** Correct the earlier semantic assessment without modifying frozen source/checklist/model evidence.

## Verified original-source fact

- Original source semantic SHA-256:
  `dd524eff809a4f628c1915fa2a52e1d70b1f91c2159cd218f1ce008700dc4963`.
- Exact original Persian source span:
  `روحیه کار تیمی و پذیرش ساختار مدیریتی مشخص مزیت محسوب می‌شود`.
- Evidence span identity: `d6b09e236c88e964dc5c886608e54c5f`.
- The explicit cue `مزیت محسوب می‌شود` states an **advantage**, not a mandatory condition.
- The English translation also describes this as an advantage. No translation-induced requirement-strength error is established for this item.

## Superseded prior interpretation

The original `2026-11-12_FRESH_SOURCE_INDEPENDENT_PRODUCT_EVALUATION_RESULT.md`
Section 3 described teamwork as required and criticized the original-language
candidate for classifying it as preferred. The frozen
`2026-11-12_fresh_source_cohort/INDEPENDENT_ADJUDICATION.json` includes the
same mistaken assertion; it is retained unchanged for audit integrity and
MUST be read with this erratum.

The subsequent v31 experiment also initially diagnosed this item as a
mistranslation; that diagnosis was corrected on its separate experiment branch
at commit `03d6071`. This erratum is consistent with that correction.

## Unchanged conclusions

- EDR acquisition and translation succeeded in the November 12 test.
- English P1.6 failed to produce a valid result; original-language mechanical
  acceptance does not prove independent semantic correctness.
- Other observed extraction issues, including missing or misfiled direct EDR
  duties, remain independently relevant.
- The independent audit's **zero approved English candidates** and
  **no-promotion** decision remain unchanged.
- This correction to human adjudication does not automatically approve the
  original-language candidate or establish general semantic reliability.
