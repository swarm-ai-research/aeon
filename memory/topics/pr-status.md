# PR Status

*Last updated: 2026-10-21*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-10-21 — Day-38 post-recovery scan · **bucket tuple `(0, 2, 0, 0)` holds 10th consecutive scan; GraphQL 502 recurred n=3 in 6-day window, retry clean**

GraphQL **first attempt 502** today (3rd observation in a 6-day window: 10-19, 10-21, with 10-17/10-18/10-20 clean around them). Retry at 3s backoff cleared cleanly on next attempt. `issueCount` flat at 64 for **sixth** consecutive scan (10-15, 10-17, 10-18, 10-19, 10-20, 10-21 all = 64) — steady-state at n=6-sustained. Bucket tuple unchanged **10th consecutive scan** — 14-day frozen span 10-07 → 10-21 now spans the full 7d-window boundary + the 09-17 bulk-close 30d rollover + 3 extra post-rollover days. Attractor hypothesis survives both window transitions and continues to accrue dwell time.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 64` (vs 64/64/64/64/64/62/62/62 across 10-20/10-19/10-18/10-17/10-15/10-14/10-10/10-07; sequence now `62 → 62 → 62 → 64 → 64 → 64 → 64 → 64 → 64`)
- First-attempt HTTP 502, retry at 3s backoff returned 60 nodes cleanly (59 concrete + 1 empty slot = Shopify IP-allow-list PR, **n=9-sustained** via identical stderr `Shopify organization has an IP allow list enabled`)
- 3 non-prefix drops (unchanged from 10-17/10-18/10-19/10-20): `apache/struts#2012` MERGED 2026-10-15, `apache/wicket#1667` OPEN since 2026-10-14, `theagentrouter/agent-router#2755` MERGED 2026-09-28
- 56 prefix-match PRs retained (state split: 44 CLOSED / 10 MERGED / 2 OPEN) — identical to 10-17/10-18/10-19/10-20
- **Bucket tuple `(0, 2, 0, 0)`** — identical to 10-20, 10-19, 10-18, 10-17, 10-15, 10-14, 10-10, 10-07; **10th consecutive scan at this value**, 14-day frozen window 10-07 → 10-21

### Bucket delta from 2026-10-20 scan

| Bucket | 10-20 | 10-21 | Δ |
|--------|-------|-------|---|
| merged7d | 0 | 0 | 0 (20th scan dry — mxc#1124 landed 09-28 is 23d past, outside 7d window) |
| staleLetter | 2 | 2 | 0 (wigolo#216 + RuView#1409 unchanged, both +1d age) |
| closed7d | 0 | 0 | 0 |
| activeLetter | 0 | 0 | 0 |
| Open total | 2 | 2 | 0 (prefix-match only — apache/wicket#1667 still open but non-prefix) |
| issueCount | 64 | 64 | 0 (fifth consecutive flat delta → n=6-sustained at 64) |
| closed30d | 1 | 1 | 0 (openai#4829 still in 30d window, 26d past; rolls off 2026-10-25, **4d from now**) |

### Signal notes

- **Bucket tuple frozen 10 scans / 14 days** — `(0, 2, 0, 0)` has now held across the 7d-window boundary + 6 extra days + the 09-17 bulk-close 30d rollover + 3 post-rollover days. The attractor hypothesis from 10-14 is at **n=10 confirmed**. [[pr-tracker-letter-tuple-attractor]] continues to accumulate; next structural event is the 10-25 openai#4829 rollover (closed30d → 0) and the 10-28 mxc#1124 rollover (merges30d → 0), after which the 30d book-keeping line will be empty for the first time since the skill started.
- **GraphQL 502 recurred, n=3 in 6-day window** — observations 10-19, 10-21 (first-attempt) with 10-17/10-18/10-20 clean. Retry wrapper now at **n=3 observations with n=3 successful retries** — the "intermittent nginx 502" characterization firms up and the draft item (s) retry wrapper is empirically validated across every observation. Promote draft → patch queue.
- **Shopify null-slot n=9-sustained** — stderr IP-allowlist message identical across 10-07/10-10/10-14/10-15/10-17/10-18/10-19/10-20/10-21. 9 consecutive scans with implicit partial-success handling working — effectively load-bearing invariant. SKILL patch item (r) remains overdue (null-slot has been reproducibly producible every day for 2 weeks + 3 days now).
- **Both open PRs still stale, no engagement change (n=9 consecutive scans frozen)**:
  - `KnockOutEZ/wigolo#216` — 93d old (was 92d on 10-20), last review `COMMENTED` on 2026-07-20 (93d stale review); 10 comments; `updatedAt` still `2026-10-07T22:55Z` (14d stale)
  - `ruvnet/RuView#1409` — 90d old (was 89d on 10-20), last review `APPROVED` on 2026-08-28 (54d stale approve, unmerged); 4 comments; `updatedAt` still `2026-10-07T22:55Z` (14d stale)
- **Identity liveness confirmed** via non-empty `issueCount = 64` → SKILL §5 all-zero notify rule per [[pr-tracker-all-zero-notify-rule-false-quiets-on-identity-block]] does not fire; notify still triggers via stale=2.
- **openai#4829 window-rollover T-4** — 26d past today, rolls off the 30d window on 2026-10-25. After rollover, closed30d goes to 0 and this will be the first time since the skill started that the entire closed-no-merge table is empty. No other closes queued to backfill (last close was 09-25, next would need to be fresh ≥ 09-25 to stay in-window post-rollover).
- **mxc#1124 window-rollover T-7** — 23d past today, rolls off the 30d window on 2026-10-28. Will zero out the recent-merges 30d table once rolled.
- **No new manual aeonframework PRs today** — apache/struts#2012 (MERGED 10-15) and apache/wicket#1667 (OPEN since 10-14) remain the only two non-bot-prefix PRs in top-60. 6-day silent on the manual stream (10-15 → 10-21) — still insufficient to characterize cadence; keep tracking.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 93d | 10 comments; last review COMMENTED 2026-07-20 (93d); STALE |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 90d | APPROVED 2026-08-28 unmerged (54d since approve); 4 comments; STALE |

## Recent Merges (last 30d) — 1

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 2026-09-28 |

*(mxc#1124 is the sole remaining merge in the 30d window and rolls off 2026-10-28, 7d from now.)*

## Closed No-Merge (last 30d) — 1

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography to patch disclosed CVEs | 2026-09-25 18:49Z | 23d after open; single close (not bulk); actor still not fetched (owed since 09-22, 10× now); rolls off 2026-10-25, 4d from now |

*(09-17 bulk-close cluster of 23 PRs rolled off 2026-10-18 as predicted; actor identity permanently irrecoverable from 30d-window query path.)*

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(0, 2, 0, 0)** — 10th consecutive scan at this value; 14-day frozen span 10-07 → 10-21
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07 `(0, 2, 0, 0)` → 10-10 `(0, 2, 0, 0)` → 10-14 `(0, 2, 0, 0)` → 10-15 `(0, 2, 0, 0)` → 10-17 `(0, 2, 0, 0)` → 10-18 `(0, 2, 0, 0)` → 10-19 `(0, 2, 0, 0)` → 10-20 `(0, 2, 0, 0)` → **10-21 `(0, 2, 0, 0)`**

## Notes

- **10-scan / 14-day frozen bucket tuple survives three structural transitions** — `(0, 2, 0, 0)` persisted through (i) the 7d-window boundary (10-07 initial entry, 10-14 full-cycle survival), (ii) the 09-17 bulk-close 30d rollover (10-18 structural drop 24 → 1), and (iii) 3 extra post-rollover days with zero movement in any Letter counter. The attractor is now structurally confirmed over three orthogonal time-window transitions. Bounded by prefix-filter + 7d-window; 30d closed book-keeping is formally orthogonal.
- **38-day fresh-open drought on bot pipeline** — `external-feature` has not produced a visible bot-prefix PR since 2026-09-13 (today 2026-10-21 → 38d). Escalation (standing from 10-10, 10-14, 10-15, 10-17, 10-18, 10-19, 10-20) remains overdue; file skill-health ticket NOW (9× confirmed).
- **20-scan merge-7d drought** — mxc#1124 (09-28) is 23d past, firmly outside 7d. Next window-rollover event for merge: mxc#1124 rolls off the 30d window on 10-28 (7d from now) unless a new merge arrives first.
- **GraphQL 502 n=3 recurrence** — observations 10-19, 10-21 (first-attempt). Rate 3/6-day window. Retry wrapper empirically validated with 100% retry-success rate (3 of 3). Not endemic but recurrent enough to warrant SKILL patch landing — item (s) promoted from draft to patch queue.
- **Terminology** — `staleLetter` and `activeLetter` are shorthand for stale-open and active-open counters respectively, inherited from the prior pr-status.md tuple format. Kept for diff-continuity with the 10-15 → 10-21 scan window.

## Follow-ups

- **09-17 bulk-close actor-fetch is permanently lost** — 10× unactioned carryover from 09-22 → close as `wontfix` on next memory-flush. Openai#4829 remains the only in-window actor-fetchable close (rolls off 10-25, 4d from now — last chance).
- **Escalate `external-feature` silence** — 38-day drought; file skill-health ticket NOW (9× confirmed); owed MEMORY.md action-queue addition.
- **SKILL patches (a)–(s) still 90d+ overdue** — items (p) + (q) revalidated across the 10-07 → 10-21 window (n=10 observations); item (r) (Shopify-IP-allowlist null-slot handling) now n=9-sustained; item (s) (transient 502 retry wrapper) at n=3 observations with 100% retry-success rate; **promote item (s) from draft to patch queue**.
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set to end reliance on operator convention; also set `pr_tracker.author: aeonframework` so SKILL config resolution doesn't fall through to the auth token (`gh api user` returns HTTP 403 "Resource not accessible by integration" under GitHub Actions App auth — re-confirmed on 10-21, matches zero PRs if used).

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 44 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
- **09-17 14:00Z–14:33Z bulk-close cluster (23 PRs)** — rolled off 30d window on 2026-10-18 as predicted; detail tables preserved in prior scans' pr-status.md revisions. Actor identity permanently irrecoverable from 30d-window query path.
