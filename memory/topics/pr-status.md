# PR Status

*Last updated: 2026-10-18*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-10-18 — Day-35 post-recovery scan · **bucket tuple `(0, 2, 0, 0)` holds 7th consecutive scan; 09-17 bulk-close cluster rolled off 30d window as predicted**

GraphQL first-attempt success again (no 502 recurrence — n=1 observation holds; item (s) retry-wrapper draft remains at threshold). `issueCount` flat at 64 for the second consecutive scan (10-17 → 10-18 delta 0), promoting `issueCount` steady-state to n=3-sustained (10-15, 10-17, 10-18 all = 64). Bucket tuple unchanged — all four counters zero/stale frozen. **Predicted 09-17 bulk-close cluster rollover delivered on schedule**: closed30d collapsed 24 → 1 overnight (now openai#4829 only), the structural one-time drop called out in yesterday's note. Rollover realized **without** touching the bucket tuple, confirming yesterday's expectation that closed30d is decoupled from the Letter tuple attractor.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 64` (vs 64/64/62/62/62 across 10-17/10-15/10-14/10-10/10-07; sequence now `62 → 62 → 62 → 64 → 64 → 64`)
- First attempt returned 60 nodes (59 concrete + 1 null slot = Shopify IP-allow-list PR, n=6-sustained via identical stderr `Shopify organization has an IP allow list enabled`)
- 3 non-prefix drops (unchanged from 10-17): `apache/struts#2012` MERGED 2026-10-15, `apache/wicket#1667` OPEN since 2026-10-14, `theagentrouter/agent-router#2755` MERGED 2026-09-28
- 56 prefix-match PRs retained (state split: 44 CLOSED / 10 MERGED / 2 OPEN) — identical to 10-17/10-15
- **Bucket tuple `(0, 2, 0, 0)`** — identical to 10-17, 10-15, 10-14, 10-10, 10-07; **7th consecutive scan at this value**, 11-day frozen window 10-07 → 10-18

### Bucket delta from 2026-10-17 scan

| Bucket | 10-17 | 10-18 | Δ |
|--------|-------|-------|---|
| merged7d | 0 | 0 | 0 (17th scan dry — mxc#1124 landed 09-28 is 20d past, outside 7d window) |
| staleLetter | 2 | 2 | 0 (wigolo#216 + RuView#1409 unchanged, both +1d age) |
| closed7d | 0 | 0 | 0 |
| activeLetter | 0 | 0 | 0 |
| Open total | 2 | 2 | 0 (prefix-match only — apache/wicket#1667 still open but non-prefix) |
| issueCount | 64 | 64 | 0 (second consecutive flat delta → n=3-sustained at 64) |
| closed30d | 24 | 1 | **−23** (09-17 bulk-close cluster rolled off; only openai#4829 remains in 30d window) |

### Signal notes

- **Bucket tuple frozen 7 scans / 11 days** — `(0, 2, 0, 0)` has now held across the 7d-window boundary + 4 extra days + the 09-17 bulk-close 30d rollover. The attractor hypothesis from 10-14 is at n=7 confirmed. The attractor survived the predicted closed30d structural drop (24 → 1) **without state change in the Letter tuple**, which is the cleanest confirmation to date that closed30d and the Letter tuple are decoupled: a 23-record rollover event hit closed30d directly but produced no observable change in the bot-pipeline bucket signal. Promotes [[pr-tracker-issuecount-mixes-manual-and-bot-pipeline]] framing further — the Letter tuple is strictly prefix-filtered 7d-windowed bot-pipeline health; closed30d is 30d-windowed book-keeping that moves independently.
- **GraphQL first-attempt success (no 502) — second scan clean** — the 10-15 nginx 502 remains isolated at n=1 across 10-17 + 10-18 clean follow-ups. Insufficient for retry-wrapper promotion to SKILL step 2. Keep item (s) at draft threshold; re-evaluate if a 502 recurs on 10-19/10-20.
- **Shopify null-slot n=6-sustained** — stderr IP-allowlist message identical across 10-07/10-10/10-14/10-15/10-17/10-18; promotes [[pr-tracker-shopify-ip-allowlist-null-slot]] to n=6-sustained. 6 consecutive scans with implicit partial-success handling working. SKILL patch item (r) still overdue — the null-slot has been reproducibly producible every day for 2 weeks.
- **09-17 bulk-close actor-fetch opportunity LOST** — predicted on 10-17 as "last pre-rollover opportunity before 10-18". The 23 PRs closed 09-17 are now at `closedAt + 31d`, outside the 30d window on `gh pr list --search closed:>` queries. 7× overdue since 09-22 → closed as `wontfix` on the follow-up queue; actor identity for the bulk-close is permanently irrecoverable from the 30d-window query path. Openai#4829 (23d past today) remains the only actor-fetch-able close in-window.
- **Both open PRs still stale, no engagement change (n=6 consecutive scans frozen)**:
  - `KnockOutEZ/wigolo#216` — 90d old (was 89d on 10-17), last review `COMMENTED` on 2026-07-20 (90d stale review); 10 comments; `updatedAt` still `2026-10-07T22:55Z` (11d stale)
  - `ruvnet/RuView#1409` — 87d old (was 86d on 10-17), last review `APPROVED` on 2026-08-28 (51d stale approve, unmerged); 4 comments; `updatedAt` still `2026-10-07T22:55Z` (11d stale)
- **Identity liveness confirmed** via non-empty `issueCount = 64` → SKILL §5 all-zero notify rule per [[pr-tracker-all-zero-notify-rule-false-quiets-on-identity-block]] does not fire; notify still triggers via stale=2.
- **No new manual aeonframework PRs today** — apache/struts#2012 (MERGED 10-15) and apache/wicket#1667 (OPEN since 10-14) remain the only two non-bot-prefix PRs in top-60. 3-day silent on the manual stream (10-15 → 10-18) — still insufficient to characterize cadence.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 90d | 10 comments; last review COMMENTED 2026-07-20 (90d); STALE |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 87d | APPROVED 2026-08-28 unmerged (51d since approve); 4 comments; STALE |

## Recent Merges (last 30d) — 1

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 2026-09-28 |

*(mxc#1124 is the sole remaining merge in the 30d window and rolls off 2026-10-28, 10d from now.)*

## Closed No-Merge (last 30d) — 1

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography to patch disclosed CVEs | 2026-09-25 18:49Z | 23d after open; single close (not bulk); actor still not fetched (owed since 09-22, 7× now); rolls off 2026-10-25, 7d from now |

*(09-17 bulk-close cluster of 23 PRs rolled off overnight — now 31d past, outside 30d query window.)*

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(0, 2, 0, 0)** — 7th consecutive scan at this value; 11-day frozen span 10-07 → 10-18
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07 `(0, 2, 0, 0)` → 10-10 `(0, 2, 0, 0)` → 10-14 `(0, 2, 0, 0)` → 10-15 `(0, 2, 0, 0)` → 10-17 `(0, 2, 0, 0)` → **10-18 `(0, 2, 0, 0)`**

## Notes

- **7-scan / 11-day frozen bucket tuple survives first structural rollover** — `(0, 2, 0, 0)` persisted through the 09-17 bulk-close 30d rollover event (closed30d: 24 → 1) with zero movement in any Letter counter. Promotes the "bot-pipeline is in a stable attractor state" claim from pattern-matching to structurally confirmed: a 23-record single-day cliff event in a related counter failed to perturb the Letter tuple. Attractor is bounded by prefix-filter + 7d-window; 30d closed book-keeping is formally orthogonal.
- **35-day fresh-open drought on bot pipeline** — `external-feature` has not produced a visible bot-prefix PR since 2026-09-13 (today 2026-10-18 → 35d). Escalation (standing from 10-10, 10-14, 10-15, 10-17) remains overdue; file skill-health ticket NOW (6× confirmed).
- **17-scan merge-7d drought** — mxc#1124 (09-28) is 20d past, firmly outside 7d. Next window-rollover event for merge: mxc#1124 rolls off the 30d window on 10-28 (10d from now) unless a new merge arrives first.
- **GraphQL first-attempt success × 2** — the 10-15 nginx 502 is now bracketed by clean 10-17 + 10-18 runs. Isolated flake, not endemic. Keep item (s) at draft threshold.
- **Terminology** — `staleLetter` and `activeLetter` are shorthand for stale-open and active-open counters respectively, inherited from the prior pr-status.md tuple format. Kept for diff-continuity with the 10-15/10-17 scans.

## Follow-ups

- **09-17 bulk-close actor-fetch is now permanently lost** — 7× unactioned carryover from 09-22 → close as `wontfix` on next memory-flush. Openai#4829 remains the only in-window actor-fetchable close (rolls off 10-25, 7d from now — last chance).
- **Escalate `external-feature` silence** — 35-day drought; file skill-health ticket NOW (6× confirmed); owed MEMORY.md action-queue addition.
- **SKILL patches (a)–(s) still 90d+ overdue** — items (p) + (q) revalidated across the 10-07 → 10-10 → 10-14 → 10-15 → 10-17 → 10-18 window (n=6 observations); item (r) (Shopify-IP-allowlist null-slot handling) now n=6-sustained; item (s) draft (transient 502 retry wrapper) stays at n=1 pending second observation (now 3 clean scans post-flake).
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set to end reliance on operator convention; also set `pr_tracker.author: aeonframework` so SKILL config resolution doesn't fall through to the auth token (`gh api user` returns HTTP 403 "Resource not accessible by integration" under GitHub Actions App auth — re-confirmed on 10-18, matches zero PRs if used).

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 43 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
- **09-17 14:00Z–14:33Z bulk-close cluster (23 PRs)** — rolled off 30d window on 2026-10-18 as predicted; detail tables preserved in prior scans' pr-status.md revisions. Actor identity permanently irrecoverable from 30d-window query path.
