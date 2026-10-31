# PR Status

*Last updated: 2026-10-31*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-10-31 — Day-48 post-recovery scan · **`(0, 1, 0, 1)` tuple break on 2 axes · wigolo rolls off 7d-merge window · `fix/` fresh-open ends 42-day drought at Day-48 · GraphQL 502 retry n=4 · Cursor null-slot new**

Two-axis structural event day — the `(1, 1, 0, 0)` tuple attractor sustained for 2 scans (10-24 → 10-25) breaks on 2026-10-31 due to:

1. **merge7d bucket roll-off:** wigolo#216 (merged 2026-10-21) crossed the 7d-window boundary on 2026-10-28T14:56Z. Expected per [[pr-tracker-bucket-tuple-attractor-terminates-on-stale-to-merged-conversion]]'s window-boundary axis.
2. **activeOpen bucket entry:** opencart/opencart#15792 (branch `fix/lock-redemption-checks`) opened 2026-10-29T18:01Z — first fresh prefix-match open since 2026-09-13, **ending the 42-day bot-pipeline fresh-open drought on Day-48** (longest in observed series).

**NEW null-slot:** `Cursor organization has an IP allow list enabled` surfaced today alongside the standing `Shopify` null — null-slot count 1 → 2. Shopify n=12-sustained; Cursor n=1 (first observation). Second IP-allowlist org extends the class previously thought Shopify-specific.

**GraphQL 502 retry n=4 at 100% retry-success** — first-attempt nginx 502 today after n=2 clean-first scans on 10-24/10-25 (502 rate drifted 3/9 → re-engages at 4/11). Single 3s-backoff retry cleared. Item (s) empirical-success rate holds 4/4 across 10-15/10-19/10-21/10-31 fires.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 73` (sequence: `62 → 62 → 62 → 64 → 64 → 64 → 64 → 64 → 64 → 71 → 71 → 73`; 10-07 → 10-31)
- Clean 60 nodes returned (58 concrete + 2 empty slots: Shopify + Cursor IP-allow-list)
- 11 non-prefix drops this scan (10-25's 10 non-prefix set + 1 new `apache/wicket#1728` 10.x backport opened 2026-10-29)
- 47 prefix-match PRs retained (state split: 38 CLOSED / 7 MERGED / 2 OPEN) — down 2 vs 10-25 (49) because 2 oldest prefix PRs rolled out of top-60 updated-desc window as 2 new 10-29 opens bumped them off
- **Bucket tuple `(0, 1, 0, 1)`** — breaks `(1, 1, 0, 0)` × 2-scan attractor; n=1 at new state

### Bucket delta from 2026-10-25 scan

| Bucket | 10-25 | 10-31 | Δ | Notes |
|--------|-------|-------|---|-------|
| merged7d | 1 | 0 | −1 | wigolo#216 rolled off 7d-window on 10-28T14:56Z |
| staleOpen | 1 | 1 | 0 | RuView#1409 (now 100d old, 24d since last activity) |
| closed7d | 0 | 0 | 0 | — |
| activeOpen | 0 | 1 | +1 | opencart#15792 fresh-open 10-29 (`fix/` prefix); first bot-prefix fresh-open in 48d |
| Open total | 1 | 2 | +1 | prefix-match only |
| issueCount | 71 | 73 | +2 | +1 prefix (opencart) + 1 non-prefix (wicket#1728 10.x backport) |
| closed30d | 1 | 0 | −1 | openai#4829 rolled off 10-26T18:49Z as predicted |
| merged30d | 2 | 1 | −1 | mxc#1124 rolled off 10-28T20:56Z as predicted; only wigolo remains (10d past, holds through 11-20) |

### Non-prefix activity (+1 new)

Same 10 non-prefix PRs as 10-25, plus **wicket#1728** opened 2026-10-29T22:02Z (10.x backport of #1667). 11 non-prefix in top-60 updated-desc window now.

- apache/wicket#1728 OPEN 10-29 (new — 10.x backport of #1667 WICKET-6938 CSP fix)
- apache/wicket#1667 OPEN 10-14 last review CHANGES_REQUESTED 10-29
- radareorg/radare2#27136 MERGED 10-23 (unchanged, 8d past merge)
- apache/struts#2012 MERGED 10-15 (unchanged, 16d past merge)
- theagentrouter/agent-router#2755 MERGED 09-28 (unchanged)
- 6 still OPEN: WordPress#14767, dovecot#337, openssl#33343, magento#41635, icu#4320, gwt#10421 (unchanged)

### Signal notes

- **42-day bot-pipeline fresh-open drought ends at Day-48** — opencart#15792 is the first prefix-match fresh-open since 2026-09-13 (external-feature's last emission). Branch `fix/lock-redemption-checks` + title "Lock coupon, reward and credit redemption checks at order confirmation" suggest a race-condition fix rather than the typical `security/*` CVE-bump pattern. May indicate a different skill emitted (not `external-feature` — hypothesis: `pr-code-fix` or similar). skill-health ticket for the drought is now de-escalated from "11× overdue" to "resolved by fresh emission 2026-10-29"; still owed is **source-skill identification** — grep `memory/logs/2026-10-29.md` for emission event.
- **RuView#1409 extends stale-approve shape to 100d · 24d since last `updatedAt`** — still structurally identical to wigolo#216's pre-merge state. The "long-approved PR converts to merge on a maintainer sweep" classifier at n=1 (wigolo) still has RuView as the standing candidate; however the 24-day activity gap post-approval widens the hypothesis window and reduces conversion probability. No new reviews, comments, or commits visible on this scan.
- **openai#4829 window-rollover confirmed on 10-26T18:49Z** — now in archive-hidden/lost set per [[pr-tracker-closer-identity-lost-after-30d-window]]. Actor identity permanently irrecoverable (owed since 09-22, closed as `wontfix` category this scan at **13× unactioned**).
- **mxc#1124 window-rollover confirmed on 10-28T20:56Z** — joins merge-archive, no longer in 30d bucket.
- **wigolo#216 window-rollover T+10 for merged30d** — holds in merged30d bucket through 2026-11-20 (30d past merge). Already rolled off merged7d on 10-28T14:56Z as predicted.
- **Shopify null-slot n=12-sustained** — identical stderr IP-allowlist across 12 consecutive scans. SKILL item (r) null-slot handling now **13× overdue**.
- **Cursor null-slot n=1 NEW** — second IP-allowlist org observed; the regime previously thought Shopify-specific generalizes. Item (r) null-slot handler must be refactored from a per-org special-case to a generic `IP allow list enabled` stderr classifier.
- **GraphQL 502 retry wrapper fires again n=4 (4-for-4)** — single 3s-backoff retry cleared today's first-attempt nginx 502; the 10-24/25 clean-first streak (n=2) terminates. The retry wrapper (SKILL item (s)) remains empirically justified; the "502 drought ends after n=2 clean" is a lower-signal observation than the retry success rate because the retry pattern is cheap and the 502 fires with sub-daily cadence.
- **The `(1, 1, 0, 0)` attractor broke on 2 axes simultaneously at n=2 dwell** — distinct from the `(0, 2, 0, 0)` attractor's 10-scan dwell. Short-dwell attractors evaporate quickly under drought-recovery conditions.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 100d | APPROVED 2026-08-28 unmerged (64d since approve); 24d since `updatedAt`; STALE |
| opencart/opencart | [#15792](https://github.com/opencart/opencart/pull/15792) | [4.2.x.x] Lock coupon, reward and credit redemption checks at order confirmation | 2026-10-29 | 2d | 0 comments, 0 reviews; FRESH (`fix/` prefix); ends 42d bot-pipeline drought |

## Recent Merges (last 30d) — 1

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 2026-10-21 |

*(wigolo#216 rolled off merged7d on 2026-10-28; holds in merged30d through 2026-11-20.)*

## Closed No-Merge (last 30d) — 0

*(openai#4829 rolled off 2026-10-26T18:49Z as predicted; now permanently in archive-hidden/lost set.)*

## Bucket tuples

- Letter (merged7d, staleOpen, closed7d, activeOpen): **(0, 1, 0, 1)** — n=1 at new state
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07/10/14/15/17/18/19/20/21 `(0, 2, 0, 0)` × 10 → 10-24/10-25 `(1, 1, 0, 0)` × 2 → **10-31 `(0, 1, 0, 1)`**

## Notes

- **Two-axis attractor break day** — (1,1,0,0) sustained only n=2 before dual-axis exit. New state `(0, 1, 0, 1)` is unobserved in prior sequence; could be another transient or a new attractor — insufficient data at n=1.
- **48-day fresh-open drought ends** — opencart#15792 is first prefix-match fresh-open since 2026-09-13. Fresh branch is `fix/` not `security/*` — source skill TBD (likely not `external-feature`).
- **Operator PR burst stable at 10 non-prefix + 1 new 10.x backport** — wicket#1728 is the operator opening a 10.x backport of #1667 after the 10-29 CHANGES_REQUESTED review.
- **Null-slot class generalization** — Cursor joins Shopify in the IP-allowlist null-slot class. The item (r) handler must accept any org that returns the generic stderr pattern.
- **GraphQL 502 retry n=4 at 100%** — the empirical floor-clear for item (s) deepens.
- **Terminology** — `staleOpen` and `activeOpen` are shorthand for stale-open and active-open counters respectively, inherited from the prior pr-status.md tuple format. Kept for diff-continuity.

## Follow-ups

- **09-17 bulk-close actor-fetch permanently lost** — 13× unactioned carryover; close as `wontfix` on next memory-flush.
- **Identify source skill for opencart#15792** — grep `memory/logs/2026-10-29.md` for the emission event; was it `external-feature` (ending the drought) or a different pipeline?
- **SKILL patches (a)–(t) still 89d+ overdue** — item (r) (null-slot handling) now generalizes beyond Shopify (Cursor added today); item (s) (3s-backoff retry) deepens to n=4-for-4; item (t) (4-axis attractor-exit tuple predictor) still at n=1 observation for stale→merged axis plus today's standard window-boundary + drought-recovery activeOpen entry.
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set to end reliance on operator convention; also set `pr_tracker.author: aeonframework` so SKILL config resolution doesn't fall through to the auth token (`gh api user` returns HTTP 403 "Resource not accessible by integration" under GitHub Actions App auth).

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 51 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
- **09-17 14:00Z–14:33Z bulk-close cluster (23 PRs)** — rolled off 30d window on 2026-10-18 as predicted; detail tables preserved in prior scans' pr-status.md revisions. Actor identity permanently irrecoverable.
- **openai/openai-agents-python#4829** — rolled off 2026-10-26T18:49Z, now permanently archive-hidden.
- **microsoft/mxc#1124** — rolled off merged30d on 2026-10-28T20:56Z.
