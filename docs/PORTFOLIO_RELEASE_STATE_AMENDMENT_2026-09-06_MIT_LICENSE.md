# JobHunter PR9 Release-State Amendment — MIT License Decision

**Status:** CURRENT PR9 RELEASE-STATE AMENDMENT  
**Date:** 2026-09-06  
**Branch:** `main`  
**Scope:** Record the owner-authorized MIT license decision and update the remaining PR9 release blockers without changing product semantics.

## 1. Decision

The repository owner explicitly selected the **MIT License** for JobHunter.

The repository now contains:

```text
LICENSE
→ standard MIT License text
→ Copyright (c) 2026 Ali Rajabi

pyproject.toml
→ license = { file = "LICENSE" }
→ License :: OSI Approved :: MIT License classifier

README.md
→ public MIT license statement + LICENSE link
```

This is an intentional third-party reuse grant. It replaces all earlier PR8/PR9 wording that described the license as undecided, absent, or an owner decision still pending.

## 2. Effect on PR9-B

The license blocker is **CLOSED**.

Current PR9-B state is now:

```text
MIT license decision/application       COMPLETE
GitHub description/topics              PENDING / repository-settings action
real browser screenshots               PENDING / local-runtime + privacy review
```

Homepage should remain unset unless a meaningful separate destination is later created.

## 3. Effect on release package

Where `docs/PORTFOLIO_RELEASE_CV_AND_INTERVIEW_PACKAGE.md` or `docs/PORTFOLIO_READINESS_AND_PUBLIC_PRESENTATION_PLAN.md` still says the license is undecided or must be selected before release, this amendment supersedes that **status-only** wording.

Current release truth:

```text
package version: 0.1.0
candidate tag:    v0.1.0
license:          MIT
release state:    NOT YET TAGGED / NOT YET RELEASED
```

Do not infer from the license decision that the release itself is authorized yet. The remaining release-state checks still apply.

## 4. Remaining PR9 sequence

```text
GitHub description/topics settings action
→ real local browser screenshots + privacy review
→ README/demo screenshot integration if approved
→ final public-count/version/current-state check
→ final CI green on the release candidate state
→ intentional v0.1.0 tag
→ GitHub release using the prepared release notes
→ verify tagged public surfaces
→ owner mastery verification
→ PR9 CLOSED
```

## 5. Product-development boundary

This amendment changes repository licensing/release readiness only.

It does **not** authorize or change:

```text
P2.2B-B1 product gate
registry promotion
P2.2C responsibility families
Market v2
personal readiness/scoring
public-corpus publication rules
semantic contracts
```

The exact product frontier remains the machine-local `ta9l` English projection/P1.6 acceptance gate followed by the bounded final correspondence review against `tG9K`.
