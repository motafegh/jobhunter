# P2.3A read-only comparison overview — isolated prototype result (2026-11-11)

**Status:** EXPERIMENTAL IMPLEMENTATION; NOT OWNER-ACCEPTED OR MAIN-AUTHORIZED.
**Branch:** `experiment/p23a-compare-at-glance-2026-11-11`.
**Predecessor:** `2026-11-11_P23A_COMPARISON_FIRST_VIEW_PREDECISION.md`.
**Production boundary:** No change to `main`; neither Strategy-C inference nor persistent P2.3 profiles nor taxonomy promotion authorized.

## Question

Can existing factual data give a reader an earlier compact comparison of job qualifications versus direct work, while keeping the complete original evidence view and all unknowns available?

## Implementation

- Added an `At a glance` section **above the existing selection/filter controls**, only when jobs are selected.
- Each selected job shows *distinct exact-claim matches / all accepted claims*, number of matching qualifications, number of matching directly stated duties, and number of matched qualifications with explicit depth.
- Separate notices distinguish **no direct duties in the accepted analysis**, **existing duties with no wording match**, **accepted evidence unavailable**, and **no wording match is not no demand**.
- Headings explicitly prohibit interpreting raw claim counts as similarity, readiness, or demand scores.
- Each summary card links to its own existing evidence card; a global link jumps to detailed evidence. Original claim wording, source links, optional current Capability interpretation, and Market-origin handling remain unchanged.
- No new read model, SQL table, background job, taxonomy, remote source/model call, or persistent profile was added.

## Concrete browser checks

Chromium/Playwright used pre-existing local browser binaries, current project code, and a temporary SQLite copy bound to `127.0.0.1:8767`. The baseline was independently measured on the same machine against the original code at `127.0.0.1:8766`.

| Geometry for RAG three-job case | Original /compare | Experimental overview |
| --- | ---: | ---: |
| Desktop 1440px: first exact claim page Y | 822px | 1166px |
| Desktop: document height | 1851px | 2195px |
| Mobile 390px: overview begins | not present | 386px |
| Mobile: first summary job begins | not present | 557px |
| Mobile: first exact claim page Y | 1411px | 2233px |
| Mobile: document height | 4740px | 5562px |

These measurements are **not** user timing data. The overview puts cross-job requirement/duty counts and the requirement-only distinction earlier in the reading path, but it **lengthens the page**, pushing the original claim details downward. The links jump to job cards (tested on both widths) and can mitigate scrolling for targeted evidence inspection. Whether the net effect improves user comprehension or time remains unproven.

Engineering gates on the experimental branch: **879 strict-warning tests passed in 48.49s**, repository Ruff check passed, and Python dependency consistency check passed. The additional focused regression verifies exact distinct fact counts, no-direct-duty/no-wording-match distinctions, summary-to-evidence links, and no additional domain-state writes on repeated GETs.

Four scenarios × two viewport sizes rendered successfully, retaining baseline exact-claim counts `[3,4,3]` for RAG and `[2,2]` for Python; requirement-only direct duties `[0,0]`; no-match counts `[0,0]`. The evidence expanders and optional Capability grouping remained functional. Neither browser width had document-level horizontal overflow. The explicit anchor to the third job worked, with the target near 16px from viewport top. No page errors or off-origin requests occurred in the overview navigation probe.

Local screenshots, scripts, and temporary database snapshots remain under ignored `data/local-acceptance/` and are not public evidence.

## Interpretation and disposition

The candidate provides an **earlier fact-only summary**, not a newly reviewed capability model and not true semantic alignment. Raw requirement counts are affected by the wording/granularity of each posting, so they must not be ranked as job difficulty, fitness, or market prevalence.

The page-length tradeoff is real. Do not automatically adopt the prototype because it looks clearer in a screenshot. Owner repeated-use assessment against the original interface remains necessary. Further improvements, such as collapsing controls or exact reviewed-concept alignment, require an observed reason and separate bounded decision.

**Proposed gate:** Keep experimental branch isolated, review `/compare` directly with the same RAG/Python cases, and record whether at-a-glance facts reduce actual navigation/reading burden without hiding requirements, duties, evidence, or unknowns. Only then consider merging a bounded UX change to `main`.
