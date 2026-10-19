# PR Status

*Last updated: 2026-10-19*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-10-19 — Day-36 post-recovery scan · **bucket tuple `(0, 2, 0, 0)` holds 8th consecutive scan; GraphQL 502 recurrence promotes item (s) past n=1 threshold**

GraphQL **first-attempt 502** today (second observation after 10-15; brackets 10-17/10-18 clean runs → n=2 confirmed, two in five days). Second attempt succeeded immediately. `issueCount` flat at 64 for third consecutive scan, promoting steady-state to n=4-sustained (10-15, 10-17, 10-18, 10-19 all = 64). Bucket tuple unchanged **8th consecutive scan** — 12-day frozen span 10-07 → 10-19 now spans the full 7d-window boundary + the predicted 09-17 bulk-close 30d rollover + 1 more day. Attractor hypothesis survives both window transitions.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 64` (vs 64/64/64/62/62/62 across 10-18/10-17/10-15/10-14/10-10/10-07; sequence now `62 → 62 → 62 → 64 → 64 → 64 → 64`)
- First attempt returned HTTP 502 (nginx); retry on `sleep 3` returned 60 nodes (59 concrete + 1 null slot = Shopify IP-allow-list PR, n=7-sustained via identical stderr `Shopify organization has an IP allow list enabled`)
- 3 non-prefix drops (unchanged from 10-17/10-18): `apache/struts#2012` MERGED 2026-10-15, `apache/wicket#1667` OPEN since 2026-10-14, `theagentrouter/agent-router#2755` MERGED 2026-09-28
- 56 prefix-match PRs retained (state split: 44 CLOSED / 10 MERGED / 2 OPEN) — identical to 10-17/10-18
- **Bucket tuple `(0, 2, 0, 0)`** — identical to 10-18, 10-17, 10-15, 10-14, 10-10, 10-07; **8th consecutive scan at this value**, 12-day frozen window 10-07 → 10-19

### Bucket delta from 2026-10-18 scan

| Bucket | 10-18 | 10-19 | Δ |
|--------|-------|-------|---|
| merged7d | 0 | 0 | 0 (18th scan dry — mxc#1124 landed 09-28 is 21d past, outside 7d window) |
| staleLetter | 2 | 2 | 0 (wigolo#216 + RuView#1409 unchanged, both +1d age) |
| closed7d | 0 | 0 | 0 |
| activeLetter | 0 | 0 | 0 |
| Open total | 2 | 2 | 0 (prefix-match only — apache/wicket#1667 still open but non-prefix) |
| issueCount | 64 | 64 | 0 (third consecutive flat delta → n=4-sustained at 64) |
| closed30d | 1 | 1 | 0 (openai#4829 still in 30d window, 24d past; rolls off 2026-10-25, 6d from now) |

### Signal notes

- **Bucket tuple frozen 8 scans / 12 days** — `(0, 2, 0, 0)` has now held across the 7d-window boundary + 4 extra days + the 09-17 bulk-close 30d rollover + one post-rollover day. The attractor hypothesis from 10-14 is at n=8 confirmed. Promotes [[pr-tracker-letter-tuple-attractor]] (new link candidate — the (0, 2, 0, 0) state has survived every rollover event we've tested it against). Underlying structural cause: 35+ day bot-pipeline drought removes the only inflow that could push `merged7d`/`activeLetter` above 0; `staleLetter` is pinned at 2 by two stuck-open PRs; `closed7d` requires fresh closes which require fresh opens.
- **GraphQL 502 recurrence — n=2 confirmed** — second nginx 502 observation in five days (10-15 + 10-19). Bracketed by clean 10-17 + 10-18 runs, so not endemic but not a one-off flake either. Promotes item (s) retry-wrapper draft past n=1 threshold → **owed as formal SKILL patch**: wrap the primary GraphQL call in `retry 1 on 5xx with 3s backoff`. Current recovery pattern (manual `sleep 3; retry`) worked both times without data loss, so the retry logic has empirical support. Add to follow-ups below.
- **Shopify null-slot n=7-sustained** — stderr IP-allowlist message identical across 10-07/10-10/10-14/10-15/10-17/10-18/10-19; promotes [[pr-tracker-shopify-ip-allowlist-null-slot]] to n=7-sustained. 7 consecutive scans with implicit partial-success handling working — effectively load-bearing invariant. SKILL patch item (r) remains overdue (null-slot has been reproducibly producible every day for 2 weeks).
- **Both open PRs still stale, no engagement change (n=7 consecutive scans frozen)**:
  - `KnockOutEZ/wigolo#216` — 91d old (was 90d on 10-18), last review `COMMENTED` on 2026-07-20 (91d stale review); 10 comments; `updatedAt` still `2026-10-07T22:55Z` (12d stale)
  - `ruvnet/RuView#1409` — 88d old (was 87d on 10-18), last review `APPROVED` on 2026-08-28 (52d stale approve, unmerged); 4 comments; `updatedAt` still `2026-10-07T22:55Z` (12d stale)
- **Identity liveness confirmed** via non-empty `issueCount = 64` → SKILL §5 all-zero notify rule per [[pr-tracker-all-zero-notify-rule-false-quiets-on-identity-block]] does not fire; notify still triggers via stale=2.
- **openai#4829 window-rollover T-6** — 24d past today, rolls off the 30d window on 2026-10-25. After rollover, closed30d goes to 0 and this will be the first time since the skill started that the entire closed-no-merge table is empty. No other closes queued to backfill (last close was 09-25, next would need to be fresh ≥ 09-25 to stay in-window post-rollover).
- **No new manual aeonframework PRs today** — apache/struts#2012 (MERGED 10-15) and apache/wicket#1667 (OPEN since 10-14) remain the only two non-bot-prefix PRs in top-60. 4-day silent on the manual stream (10-15 → 10-19) — still insufficient to characterize cadence; keep tracking.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 91d | 10 comments; last review COMMENTED 2026-07-20 (91d); STALE |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 88d | APPROVED 2026-08-28 unmerged (52d since approve); 4 comments; STALE |

## Recent Merges (last 30d) — 1

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 2026-09-28 |

*(mxc#1124 is the sole remaining merge in the 30d window and rolls off 2026-10-28, 9d from now.)*

## Closed No-Merge (last 30d) — 1

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography to patch disclosed CVEs | 2026-09-25 18:49Z | 23d after open; single close (not bulk); actor still not fetched (owed since 09-22, 8× now); rolls off 2026-10-25, 6d from now |

*(09-17 bulk-close cluster of 23 PRs rolled off 2026-10-18 as predicted; actor identity permanently irrecoverable from 30d-window query path.)*

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(0, 2, 0, 0)** — 8th consecutive scan at this value; 12-day frozen span 10-07 → 10-19
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07 `(0, 2, 0, 0)` → 10-10 `(0, 2, 0, 0)` → 10-14 `(0, 2, 0, 0)` → 10-15 `(0, 2, 0, 0)` → 10-17 `(0, 2, 0, 0)` → 10-18 `(0, 2, 0, 0)` → **10-19 `(0, 2, 0, 0)`**

## Notes

- **8-scan / 12-day frozen bucket tuple survives two window-rollover events** — `(0, 2, 0, 0)` persisted through both the 7d-window boundary (10-07 initial entry, 10-14 full-cycle survival) and the 09-17 bulk-close 30d rollover (10-18 structural drop 24 → 1) with zero movement in any Letter counter. The attractor is now structurally confirmed over two orthogonal time-window transitions. Bounded by prefix-filter + 7d-window; 30d closed book-keeping is formally orthogonal.
- **36-day fresh-open drought on bot pipeline** — `external-feature` has not produced a visible bot-prefix PR since 2026-09-13 (today 2026-10-19 → 36d). Escalation (standing from 10-10, 10-14, 10-15, 10-17, 10-18) remains overdue; file skill-health ticket NOW (7× confirmed).
- **18-scan merge-7d drought** — mxc#1124 (09-28) is 21d past, firmly outside 7d. Next window-rollover event for merge: mxc#1124 rolls off the 30d window on 10-28 (9d from now) unless a new merge arrives first.
- **GraphQL 502 n=2 recurrence** — first observed 10-15, recurred 10-19 with clean 10-17 + 10-18 between. Rate ~2/5-day window. Not endemic but not isolated flake. Retry wrapper now empirically supported (two successful manual retries after 3s backoff). Promote item (s) to SKILL patch.
- **Terminology** — `staleLetter` and `activeLetter` are shorthand for stale-open and active-open counters respectively, inherited from the prior pr-status.md tuple format. Kept for diff-continuity with the 10-15 → 10-19 scan window.

## Follow-ups

- **09-17 bulk-close actor-fetch is permanently lost** — 8× unactioned carryover from 09-22 → close as `wontfix` on next memory-flush. Openai#4829 remains the only in-window actor-fetchable close (rolls off 10-25, 6d from now — last chance).
- **Escalate `external-feature` silence** — 36-day drought; file skill-health ticket NOW (7× confirmed); owed MEMORY.md action-queue addition.
- **SKILL patches (a)–(s) still 90d+ overdue** — items (p) + (q) revalidated across the 10-07 → 10-19 window (n=7 observations); item (r) (Shopify-IP-allowlist null-slot handling) now n=7-sustained; **item (s) draft (transient 502 retry wrapper) promoted past n=1** — n=2 confirmed observations with two successful manual retries; move from draft to patch queue.
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set to end reliance on operator convention; also set `pr_tracker.author: aeonframework` so SKILL config resolution doesn't fall through to the auth token (`gh api user` returns HTTP 403 "Resource not accessible by integration" under GitHub Actions App auth — re-confirmed on 10-19, matches zero PRs if used).

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 44 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
- **09-17 14:00Z–14:33Z bulk-close cluster (23 PRs)** — rolled off 30d window on 2026-10-18 as predicted; detail tables preserved in prior scans' pr-status.md revisions. Actor identity permanently irrecoverable from 30d-window query path.
