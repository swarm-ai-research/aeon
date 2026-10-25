# PR Status

*Last updated: 2026-10-25*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-10-25 — Day-42 post-recovery scan · **`(1, 1, 0, 0)` tuple + `issueCount=71` reaffirmed at n=2-sustained; openai#4829 last in-window day; Shopify null-slot n=11; GraphQL first-attempt clean n=2**

Quiet consolidation day — yesterday's three structural breaks (merge-7d drought ending at scan 20, 10-scan `(0,2,0,0)` attractor termination, `issueCount` n=6-sustained flat regime breaking to 71) all hold their new values at n=2 observations. No new structural event today.

GraphQL **first attempt clean** on both 10-24 and 10-25 — n=2-sustained post-502-streak. 502 rate drifts to 3/9 over the 10-15 → 10-25 window. Retry wrapper (item (s)) still empirically justified by past 3 fires but has had zero use the past two scans.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 71` (sequence: `62 → 62 → 62 → 64 → 64 → 64 → 64 → 64 → 64 → 71 → 71`; 10-07/10-10/10-14 → 10-15/10-17/10-18/10-19/10-20/10-21 → 10-24/10-25)
- Clean 60 nodes returned (59 concrete + 1 empty slot = Shopify IP-allow-list PR, **n=11-sustained** via identical stderr `Shopify organization has an IP allow list enabled`)
- 10 non-prefix drops this scan (same 10 as 10-24; no new non-prefix PRs in top-60 updated-desc window)
- 49 prefix-match PRs retained (state split: 40 CLOSED / 8 MERGED / 1 OPEN) — byte-identical to 10-24
- **Bucket tuple `(1, 1, 0, 0)`** — n=2-sustained

### Bucket delta from 2026-10-24 scan

| Bucket | 10-24 | 10-25 | Δ | Notes |
|--------|-------|-------|---|-------|
| merged7 | 1 | 1 | 0 | wigolo#216 (3d ago, still in-window) |
| staleOpen | 1 | 1 | 0 | RuView#1409 (now 93d old, +1d) |
| closed7d | 0 | 0 | 0 | — |
| activeOpen | 0 | 0 | 0 | — |
| Open total | 1 | 1 | 0 | prefix-match only |
| issueCount | 71 | 71 | 0 | n=2-sustained at new regime |
| closed30d | 1 | 1 | 0 | openai#4829 at 29d past (18:49Z close); **rolls off 10-26 at 18:49Z — T-0 last in-window day** |
| merged30d | 2 | 2 | 0 | wigolo#216 (3d) + mxc#1124 (26d, rolls off 10-28, T-3) |

### Non-prefix activity (no delta)

Same 10 non-prefix PRs as 10-24. No new operator-authored fresh opens today. The 10-22/10-23 CSP-hardening burst has stabilized at 10 nodes in the top-60 updated-desc window.

- radareorg/radare2#27136 MERGED 10-23 (unchanged)
- apache/struts#2012 MERGED 10-15 (unchanged)
- theagentrouter/agent-router#2755 MERGED 09-28 (unchanged)
- 7 still OPEN: WordPress#14767, dovecot#337, openssl#33343, magento#41635, icu#4320, gwt#10421, wicket#1667 (unchanged)

### Signal notes

- **Tuple `(1, 1, 0, 0)` dwell starts at n=2** — no structural events today; openai#4829 window-rollover T-0 (last in-window day — rolls off tomorrow 10-26 at 18:49Z); mxc#1124 window-rollover T-3; wigolo#216 window-rollover T+17. Next predicted exit on 10-29 (closed30d → 0 after openai rollover, leaving tuple unchanged but closed30d count drops) OR 10-28 (merged30d drops from 2 → 1 at mxc rollover). The merge7d bucket vacates independently on 10-29 (7d past wigolo merge of 10-21).
- **RuView#1409 holds its stale-approve shape** — now 93d old, 58d since the 2026-08-28 APPROVED review, 18d since last `updatedAt`. Still structurally identical to wigolo#216's pre-merge state 4 days before its 10-21 merge event. No new reviews, comments, or commits visible on this scan. The "long-approved PR converts to merge on a maintainer sweep" classifier is live-observed at n=1 (wigolo); RuView is the next candidate.
- **openai#4829 window-rollover T-0** — closes 29d 5h ago; still in-window today, rolls off at 2026-10-26T18:49Z. Actor identity still not fetched (owed since 09-22, **12× now**). This is the final day the 30d-window query returns this PR; after rollover it joins the archive-hidden/lost set per [[pr-tracker-repo-deletion-loses-pr-permanently]]'s sibling class [[pr-tracker-closer-identity-lost-after-30d-window]].
- **Shopify null-slot n=11-sustained** — identical stderr IP-allowlist across 11 consecutive scans (10-07 → 10-25 with gaps at non-scan days). SKILL item (r) null-slot handling now **12× overdue**.
- **42-day fresh-open drought on bot pipeline** — `external-feature` has not produced a visible bot-prefix PR since 2026-09-13 (today 2026-10-25 → 42d). Escalation now **11× overdue** (standing from 10-10, 10-14, 10-15, 10-17, 10-18, 10-19, 10-20, 10-21, 10-24). skill-health ticket still owed from yesterday.
- **GraphQL 502 streak broken n=2** — today clean on first attempt (no retry fired). Rate drops to 3/9 scans over 10-15 → 10-25 window. The item (s) retry wrapper has had zero fires the past two scans but 3-for-3 success on the earlier fires; keep empirically justified.
- **No notegraph churn signal in PR space** — notegraph PR #97 (yesterday's +2n/+12e delta) landed on swarm-ai-research/aeon (internal), not visible in cross-repo author queue. The daily notegraph cadence is orthogonal to the pr-tracker author pipeline.

## Open (1)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 93d | APPROVED 2026-08-28 unmerged (58d since approve); 4 comments; STALE |

## Recent Merges (last 30d) — 2

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 2026-10-21 |
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 2026-09-28 |

*(mxc#1124 rolls off 2026-10-28, T-3. wigolo#216 holds through 2026-11-20.)*

## Closed No-Merge (last 30d) — 1

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography to patch disclosed CVEs | 2026-09-25 18:49Z | 29d after open; single close (not bulk); actor still not fetched (owed since 09-22, **12× now**); rolls off 2026-10-26 18:49Z, **T-0 — last in-window day TODAY** |

*(09-17 bulk-close cluster of 23 PRs rolled off 2026-10-18 as predicted; actor identity permanently irrecoverable from 30d-window query path.)*

## Bucket tuples

- Letter (merged7d, staleOpen, closed7d, activeOpen): **(1, 1, 0, 0)** — n=2-sustained (10-24 → 10-25)
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07/10/14/15/17/18/19/20/21 `(0, 2, 0, 0)` × 10 → **10-24/10-25 `(1, 1, 0, 0)` × 2**

## Notes

- **Quiet consolidation day** — both the new tuple state and the new issueCount regime at 71 reaffirm at n=2. No structural events; the attractor-exit event classifier set from yesterday (window-boundary, bulk-close rollover, post-rollover days, stale→merged conversion) stands at 4 axes with no new candidate axis today.
- **42-day fresh-open drought on bot pipeline** — `external-feature` silence standing from 2026-09-13 → today 42d; 11× overdue escalation; skill-health ticket still owed from yesterday.
- **Operator PR burst stabilized** — 10 non-prefix PRs in top-60 window, identical to 10-24. No new operator fresh opens 10-24 → 10-25 (window boundary not yet rolled). The non-prefix 10-29 window boundary (apache/struts#2012 opened 2026-10-14; rolls off updated-desc eligibility if a 61st newer PR appears) is a next watch point.
- **GraphQL 502 streak broken n=2** — today clean on first attempt; rate 3/9 over 10-15 → 10-25 window. Retry wrapper still justified by past 100% retry-success at n=3.
- **Shopify null-slot n=11-sustained** — SKILL patch item (r) now 12× overdue.
- **Terminology** — `staleOpen` and `activeOpen` are shorthand for stale-open and active-open counters respectively, inherited from the prior pr-status.md tuple format. Kept for diff-continuity with the 10-15 → 10-25 scan window.

## Follow-ups

- **09-17 bulk-close actor-fetch is permanently lost** — 12× unactioned carryover from 09-22 → close as `wontfix` on next memory-flush. Openai#4829 remains the only in-window actor-fetchable close (rolls off 10-26 18:49Z, **T-0 — last chance TODAY**).
- **Escalate `external-feature` silence** — 42-day drought; file skill-health ticket (now 11× confirmed); owed MEMORY.md action-queue addition.
- **SKILL patches (a)–(t) still 84d+ overdue** — all patch-queue items revalidated across the 10-07 → 10-25 window; item (r) (Shopify-IP-allowlist null-slot handling) now n=11-sustained; item (s) (transient 502 retry wrapper) remains at n=3 fires with 100% retry-success rate (last fire 10-21, two clean scans since); item (t) (4-axis attractor-exit tuple predictor) still at n=1 observation for the stale→merged conversion axis.
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set to end reliance on operator convention; also set `pr_tracker.author: aeonframework` so SKILL config resolution doesn't fall through to the auth token (`gh api user` returns HTTP 403 "Resource not accessible by integration" under GitHub Actions App auth — re-confirmed on 10-25, matches zero PRs if used).

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 45 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
- **09-17 14:00Z–14:33Z bulk-close cluster (23 PRs)** — rolled off 30d window on 2026-10-18 as predicted; detail tables preserved in prior scans' pr-status.md revisions. Actor identity permanently irrecoverable from 30d-window query path.
- **openai/openai-agents-python#4829** — rolls off 2026-10-26 18:49Z, joining this list.
