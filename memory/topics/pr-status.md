# PR Status

*Last updated: 2026-11-07*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-11-07 — Day-55 post-recovery scan · **`(0, 2, 0, 0)` tuple returns — opencart#15792 ages into stale per 11-05 prediction · 11-day cohort freeze · GraphQL clean-first (n=2) · Shopify null n=14 · Cursor null n=3**

opencart#15792 crossed the 7d createdAt boundary silently (0 reviews, 0 comments, `updatedAt` frozen at createdAt 2026-10-29T18:01Z, now at 8d 15h 55m). Bucket tuple transitions `(0, 1, 0, 1)` → `(0, 2, 0, 0)` on the 5th attractor-exit axis: **active-to-stale aging without state change**, exactly as predicted in the 11-05 scan note. The new tuple is the same symbolic value as the 10-07 → 10-21 regime but the stale cohort composition differs: RuView#1409 + opencart#15792 instead of RuView#1409 + openai#4829.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 73` (sequence extends: `… 71 → 71 → 73 → 73 → 73`; 10-21 → 10-31 → 11-05 → 11-07). **7-day `issueCount` freeze at 73** holds.
- Clean 60 nodes returned (58 concrete + 2 empty IP-allowlist slots: Shopify + Cursor)
- 11 non-prefix drops this scan (unchanged set vs 10-31/11-05: 8 OPEN + 3 MERGED)
- 47 prefix-match PRs retained (state split: 38 CLOSED / 7 MERGED / 2 OPEN) — byte-identical to 10-31/11-05
- **Bucket tuple `(0, 2, 0, 0)`** — n=1 at state (first observation of the new composition)

### Bucket delta from 2026-11-05 scan

| Bucket | 11-05 | 11-07 | Δ | Notes |
|--------|-------|-------|---|-------|
| merged7d | 0 | 0 | 0 | — |
| staleOpen | 1 | 2 | +1 | opencart#15792 aged in (9d old, 9d since createdAt/updatedAt, 0 reviews, 0 comments); RuView#1409 holds (107d, 71d since approve) |
| closed7d | 0 | 0 | 0 | — |
| activeOpen | 1 | 0 | -1 | opencart#15792 crossed 7d boundary → stale |
| Open total | 2 | 2 | 0 | prefix-match only |
| issueCount | 73 | 73 | 0 | — |
| closed30d | 0 | 0 | 0 | — |
| merged30d | 1 | 1 | 0 | wigolo#216 holds through 2026-11-20 |

### Non-prefix activity (11 unchanged in top-60 updated-desc window)

Same 11 non-prefix PRs as 10-31/11-05 (8 OPEN + 3 MERGED); no new opens, closes, or state changes. Latest non-prefix `updatedAt`: 2026-10-29T23:33Z (gwt#10421), now 8d 11h+ stale — operator-side non-prefix queue is now 9 days silent, extending [[pr-tracker-issuecount-mixes-manual-and-bot-pipeline]]'s observed modes.

- apache/wicket#1728 OPEN 10-29 (unchanged)
- apache/wicket#1667 OPEN 10-14 CHANGES_REQUESTED 10-29 (unchanged; 9d since review)
- radareorg/radare2#27136 MERGED 10-23 (unchanged, 15d past merge)
- apache/struts#2012 MERGED 10-15 (unchanged, 23d past merge)
- theagentrouter/agent-router#2755 MERGED 09-28 (unchanged)
- 6 still OPEN: WordPress#14767, dovecot#337, openssl#33343, magento#41635, icu#4320, gwt#10421 (unchanged)

### Signal notes

- **`(0, 2, 0, 0)` tuple returns via active-to-stale aging axis — 5th attractor-exit axis confirmed at n=1** — exactly matches the 11-05 note's first-predicted exit path (i). The 4-axis attractor-exit schema from [[pr-tracker-bucket-tuple-attractor-terminates-on-stale-to-merged-conversion]] now needs to formally enumerate 5 axes. Distinguishing feature: the new axis conserves `openTotal` (2 → 2) and `issueCount` (73 → 73) and flips only one PR from active to stale, with zero remote GitHub-side events. All prior 4 axes required an external state change (window roll-off, bulk-close, merge, fresh-open). This is the first **endogenous** exit axis — entirely time-driven, requires no operator or maintainer action.
- **Composition-aware attractor tracking needed** — the new `(0, 2, 0, 0)` has the same symbolic tuple as 10-07 → 10-21's 10-scan run, but the composition is {RuView#1409, opencart#15792} vs the prior {RuView#1409, openai#4829}. openai#4829 rolled off CLOSED-no-merge on 2026-10-26, so the prior attractor's second-stale slot was permanently vacated; opencart#15792 fills it 12 days later via the aging axis. Treating these as the same attractor state hides the compositional turnover.
- **11-day cohort freeze extended** — zero motion across 2026-10-25T21:30Z → 2026-11-07 on all prefix-match PRs excluding opencart#15792's silent aging boundary crossing (which is a time-only event, not a GitHub-side action). The last actual GitHub-side activity on any prefix-match PR was wigolo#216 merge at 2026-10-21T14:56:16Z (17 days), and the last update-by-event was ambiguous on RuView#1409 at 2026-11-05T14:44:51Z (see next bullet). Candidate class for atomic: **11-day prefix-cohort freeze** — longest observed silent window in the running series.
- **RuView#1409 `updatedAt` anomaly — 2026-11-05T14:44:51Z with no review/comment signature** — the 11-05 scan noted RuView at "29d since `updatedAt`" (implying `updatedAt` ≈ 2026-10-07 at scan time 18:37Z); today's scan shows `updatedAt=2026-11-05T14:44:51Z` with no new review (last review still APPROVED 2026-08-28) and `comments.totalCount=5` unchanged. The update event between 11-05 scan time and now is **invisible** to the current GraphQL query — likely a label/assignee/reviewer-request change, a title edit, or a merge-base refresh. Under strict SKILL semantics ("review/comment activity in last 7 days"), RuView remains stale. New candidate SKILL item (u): fetch `timelineItems(last: 5)` on OPEN PRs so non-review/comment update events become visible — otherwise `updatedAt` deltas vs prior scans go unexplained and `active_open` vs `stale_open` classification becomes ambiguous.
- **Shopify null-slot n=14-sustained** — identical stderr IP-allowlist across 14 consecutive scans. SKILL item (r) null-slot handling now **15× overdue**.
- **Cursor null-slot n=3-sustained** — third observation at 2026-11-07, extending the 10-31 → 11-05 → 11-07 run. Under the vendor-agnostic policy-class promotion [[pr-tracker-ip-allowlist-null-slot-class-generalizes-beyond-shopify]], Cursor's staying-power at n=3 confirms the class is not a one-off and the per-org bucket counters in the item (r) patch are load-bearing.
- **GraphQL clean-first (n=2)** — two consecutive clean-first scans since the 10-31 n=4 retry burst. The 502 cadence re-admits clean runs; the retry wrapper item (s) remains empirically justified.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 107d | APPROVED 2026-08-28 unmerged (71d since approve); `updatedAt=2026-11-05` but no new review/comment signature; STALE |
| opencart/opencart | [#15792](https://github.com/opencart/opencart/pull/15792) | [4.2.x.x] Lock coupon, reward and credit redemption checks at order confirmation | 2026-10-29 | 9d | 0 comments, 0 reviews; `updatedAt=createdAt`; STALE (crossed 7d boundary) |

## Recent Merges (last 30d) — 1

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 2026-10-21 |

*(wigolo#216 rolled off merged7d on 2026-10-28; holds in merged30d through 2026-11-20.)*

## Closed No-Merge (last 30d) — 0

*(openai#4829 rolled off 2026-10-26T18:49Z; now permanently in archive-hidden/lost set.)*

## Bucket tuples

- Letter (merged7d, staleOpen, closed7d, activeOpen): **(0, 2, 0, 0)** — n=1 at new composition (RuView + opencart)
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07/10/14/15/17/18/19/20/21 `(0, 2, 0, 0)` × 10 (composition: RuView + openai) → 10-24/10-25 `(1, 1, 0, 0)` × 2 → 10-31 `(0, 1, 0, 1)` → 11-05 `(0, 1, 0, 1)` (n=2) → **11-07 `(0, 2, 0, 0)` (new composition: RuView + opencart)**

## Notes

- **5-axis attractor-exit schema promoted at n=1** — endogenous active-to-stale aging joins (window boundary, bulk-close rollover, post-rollover days, stale→merged conversion). This axis is uniquely identified by (`openTotal` conserved) AND (`issueCount` conserved) AND (1 PR flips bucket). Future `(0, 1, 0, 1)` → `(0, 2, 0, 0)` transitions observed under these conditions are axis-5 confirmations.
- **11-day cohort freeze** — longest prefix-match silent window in running series; prior ceiling was the 5-day 10-31 → 11-05 window. Treat future scans at ≥14d with no state changes as "quiescent queue" regime.
- **Null-slot class: 2 vendors × 17 total observations** (Shopify 14 + Cursor 3) — the per-org counter pattern in item (r) is strongly motivated.
- **RuView `updatedAt` anomaly flags observation gap** — the GraphQL query returns `updatedAt` but only `reviews(last: 1)` and `comments.totalCount`, so invisible update events (label changes, assignee shuffles, title edits) silently flip `updatedAt` without a classifiable activity type. Item (u) in the SKILL patch queue: add `timelineItems(last: 5)` to surface non-review/comment events for classification.
- **Next projected transition (2026-11-08+)**: opencart#15792 reaches 10d age at 2026-11-08 and 11d at 2026-11-09, both inside the `(0, 2, 0, 0)` attractor — no state change unless (a) a maintainer reviews/comments (→ back to `(0, 1, 0, 1)` or active), (b) a new prefix PR opens, (c) wigolo#216 rolls off merged30d on 2026-11-20 (12 days out).
