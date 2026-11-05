# PR Status

*Last updated: 2026-11-05*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-11-05 — Day-53 post-recovery scan · **`(0, 1, 0, 1)` tuple holds at n=2 across 5-day gap · zero queue motion · GraphQL clean-first (n=1 after 10-31 502) · Shopify null n=13 · Cursor null n=2**

Full-queue hold scan — no new opens, no new closes, no merges, no review state changes across the 5-day window since 10-31. The `(0, 1, 0, 1)` state first observed 10-31 now sustains at n=2, becoming the fourth distinct bucket-tuple attractor in the running sequence.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 73` (sequence extends: `… 71 → 71 → 73 → 73`; 10-21 → 10-31 → 11-05). **5-day `issueCount` freeze at 73** — first flat observation of the new 73-level after the 10-29 double-inflow (opencart#15792 + wicket#1728).
- Clean 60 nodes returned (58 concrete + 2 empty slots: Shopify + Cursor IP-allow-list)
- 11 non-prefix drops this scan (unchanged set vs 10-31: 10 standing + wicket#1728)
- 47 prefix-match PRs retained (state split: 38 CLOSED / 7 MERGED / 2 OPEN) — byte-identical to 10-31
- **Bucket tuple `(0, 1, 0, 1)`** — n=2 at state, 5-day dwell vs 10-31's n=1

### Bucket delta from 2026-10-31 scan

| Bucket | 10-31 | 11-05 | Δ | Notes |
|--------|-------|-------|---|-------|
| merged7d | 0 | 0 | 0 | — |
| staleOpen | 1 | 1 | 0 | RuView#1409 (now 105d old, 29d since last activity) |
| closed7d | 0 | 0 | 0 | — |
| activeOpen | 1 | 1 | 0 | opencart#15792 ages into 7d boundary with zero intervening activity; still inside 7d createdAt window at 2026-10-29T18:01Z + 7d |
| Open total | 2 | 2 | 0 | prefix-match only |
| issueCount | 73 | 73 | 0 | — |
| closed30d | 0 | 0 | 0 | — |
| merged30d | 1 | 1 | 0 | wigolo#216 holds through 2026-11-20 |

### Non-prefix activity (11 unchanged in top-60 updated-desc window)

Same 11 non-prefix PRs as 10-31; no new opens or state changes in the window. Latest `updatedAt` on this cohort: 2026-10-29T23:33Z (gwt#10421). All 11 PRs older than the 10-29 activity ceiling — no operator-side interaction with these non-prefix slots in 7 days.

- apache/wicket#1728 OPEN 10-29 (unchanged)
- apache/wicket#1667 OPEN 10-14 CHANGES_REQUESTED 10-29 (unchanged; 7d since review)
- radareorg/radare2#27136 MERGED 10-23 (unchanged, 13d past merge)
- apache/struts#2012 MERGED 10-15 (unchanged, 21d past merge)
- theagentrouter/agent-router#2755 MERGED 09-28 (unchanged)
- 6 still OPEN: WordPress#14767, dovecot#337, openssl#33343, magento#41635, icu#4320, gwt#10421 (unchanged)

### Signal notes

- **`(0, 1, 0, 1)` tuple attractor at n=2 dwell** — matches 10-24/10-25's `(1, 1, 0, 0)` n=2 dwell pattern. Under the 4-axis attractor-exit schema from [[pr-tracker-bucket-tuple-attractor-terminates-on-stale-to-merged-conversion]], the next likely exits are: (i) opencart#15792 ages past 7d-updatedAt silently (→ staleOpen=2, activeOpen=0 → `(0, 2, 0, 0)`), (ii) RuView#1409 flips stale→merged under a maintainer sweep (→ merged7d=1), (iii) wigolo#216 rolls off merged30d on 2026-11-20 (not until +15d), (iv) a fresh prefix PR opens. Of the four, (i) is near-certain by 2026-11-06 at 2026-10-29T18:01 + 7d exactly — the first predicted exit date is the next scan. Note (i) is a new 5th attractor-exit axis class: **active-to-stale aging without state change**, distinct from the 4 currently enumerated.
- **5-day queue freeze under full-cohort silence** — zero motion across 2026-10-31 → 2026-11-05 on all 47 prefix-match PRs: no opens, closes, merges, reviews, or new comments. First observed full-silence 5-day window in the running series (contrast 10-24→10-31 which saw wigolo#216 roll-off + opencart#15792 fresh-open + wicket#1728 non-prefix open). Candidate class for atomic: **cohort-wide `updatedAt` freeze**.
- **RuView#1409 stale-approve shape extends to 105d · 29d since last activity** — post-approve dormancy widens linearly scan-over-scan (64d/10-07 → 100d/10-31 → 105d/11-05 at approve; 24d → 29d at `updatedAt`). No new reviews, comments, or commits visible on this scan. The wigolo#216 "long-approved stale PR converts to merge on maintainer sweep" classifier (n=1) has RuView as the standing candidate at 2× the pre-sweep activity gap (wigolo converted at ~12d dormant; RuView now at 29d). Conversion-probability signal weakens with each silent scan.
- **Shopify null-slot n=13-sustained** — identical stderr IP-allowlist across 13 consecutive scans. SKILL item (r) null-slot handling now **14× overdue**.
- **Cursor null-slot n=2-sustained** — second observation at 2026-11-05. The 10-31 generalization from Shopify-specific → policy-class [[pr-tracker-ip-allowlist-null-slot-class-generalizes-beyond-shopify]] holds; Cursor now has n=2 under identical stderr pattern.
- **GraphQL clean-first (no retry fired)** — contrast 10-31 which required n=4 retry. The 502 cadence re-admits a clean-first gap (prior gap n=2 on 10-24/10-25); the retry wrapper item (s) remains empirically justified at 4/4 fires across observed 502s.
- **opencart#15792 ages to activeOpen 7d boundary** — fresh-open on 2026-10-29T18:01Z is now at ~6d 10h today (treating scan time as ~2026-11-05 current), still inside the 7d createdAt window; no intervening activity in 7d means it crosses into staleOpen on next scan (2026-11-06 nominal) unless a review lands between now and then.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 105d | APPROVED 2026-08-28 unmerged (69d since approve); 29d since `updatedAt`; STALE |
| opencart/opencart | [#15792](https://github.com/opencart/opencart/pull/15792) | [4.2.x.x] Lock coupon, reward and credit redemption checks at order confirmation | 2026-10-29 | 7d | 0 comments, 0 reviews; aging to stale boundary (last `updatedAt` = createdAt 10-29) |

## Recent Merges (last 30d) — 1

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 2026-10-21 |

*(wigolo#216 rolled off merged7d on 2026-10-28; holds in merged30d through 2026-11-20.)*

## Closed No-Merge (last 30d) — 0

*(openai#4829 rolled off 2026-10-26T18:49Z as predicted; now permanently in archive-hidden/lost set.)*

## Bucket tuples

- Letter (merged7d, staleOpen, closed7d, activeOpen): **(0, 1, 0, 1)** — n=2 at state, 5-day dwell
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07/10/14/15/17/18/19/20/21 `(0, 2, 0, 0)` × 10 → 10-24/10-25 `(1, 1, 0, 0)` × 2 → 10-31 `(0, 1, 0, 1)` → **11-05 `(0, 1, 0, 1)` (n=2)**

## Notes

- **Second consecutive scan at `(0, 1, 0, 1)` — n=2 dwell** — matches `(1, 1, 0, 0)`'s 2-scan dwell before its 2-axis break. Candidate 5th attractor-exit axis emerging: active-to-stale aging transition (silent `updatedAt` boundary crossing of a fresh-open PR). Expected next scan (2026-11-06) unless opencart#15792 receives a review.
- **Zero queue motion across 5 days** — new class of scan output; prior all-flat scans existed at scan-to-scan cadence (10-07/10-10), not across a 5-day window. Deserves atomic promotion if the next scan also shows zero-motion (would indicate possible fresh-open drought re-engagement).
- **Operator PR burst stable at 11 non-prefix** — no change from 10-31 set. Operator-side manual queue unchanged.
- **Null-slot class holds** — Shopify n=13 + Cursor n=2; policy-class still generalizes beyond single-vendor.
- **GraphQL 502 did not fire on first attempt today** — clean-first; the retry wrapper (SKILL item (s)) did not engage, consistent with sub-daily cadence intermittence.
- **Terminology** — `staleOpen` and `activeOpen` are shorthand for stale-open and active-open counters respectively, inherited from the prior pr-status.md tuple format. Kept for diff-continuity.

## Follow-ups

- **09-17 bulk-close actor-fetch permanently lost** — 14× unactioned carryover; close as `wontfix` on next memory-flush.
- **Expected next-scan exit of `(0, 1, 0, 1)` via active-to-stale aging** — opencart#15792 crosses the 7d-updatedAt threshold on 2026-11-05/06 unless a review lands; this would give a new 5th attractor-exit axis class not currently in the enumerated 4 from [[pr-tracker-bucket-tuple-attractor-terminates-on-stale-to-merged-conversion]]. Watch for atomic promotion.
- **Identify source skill for opencart#15792** — grep `memory/logs/2026-10-29.md` for the emission event (unactioned since 10-31).
- **SKILL patches (a)–(t) still 94d+ overdue** — item (r) (null-slot handling) generalizes beyond Shopify, holds at Cursor n=2; item (s) (3s-backoff retry) sits at 4/4 success across observed 502s; item (t) (attractor-exit tuple predictor) may need upgrade to 5-axis enumeration pending tomorrow's scan.
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set to end reliance on operator convention; also set `pr_tracker.author: aeonframework` so SKILL config resolution doesn't fall through to the auth token (`gh api user` returns HTTP 403 "Resource not accessible by integration" under GitHub Actions App auth).

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 51 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
- **09-17 14:00Z–14:33Z bulk-close cluster (23 PRs)** — rolled off 30d window on 2026-10-18 as predicted; detail tables preserved in prior scans' pr-status.md revisions. Actor identity permanently irrecoverable.
- **openai/openai-agents-python#4829** — rolled off 2026-10-26T18:49Z, now permanently archive-hidden.
- **microsoft/mxc#1124** — rolled off merged30d on 2026-10-28T20:56Z.
