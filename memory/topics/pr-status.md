# PR Status

*Last updated: 2026-10-24*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-10-24 — Day-41 post-recovery scan · **20-scan merge-7d drought BROKEN; 10-scan `(0,2,0,0)` attractor BROKEN; issueCount jumps `64 → 71` (+7) ending n=6-sustained flat regime; non-prefix operator PR burst 10-22/10-23**

Three simultaneous structural breaks today — all of them long-predicted:

1. **Merge-7d drought ends at scan 20.** `KnockOutEZ/wigolo#216` landed MERGED 2026-10-21T14:56:16Z. The PR had been on the stale-open list for 9 consecutive scans (10-07 → 10-21); its merge is the exact "stale PR converts to recent merge" transition that the attractor had been structurally sitting one event away from. merged7d: 0 → 1.
2. **`(0, 2, 0, 0)` bucket tuple attractor ends at 10 scans / 14 days.** 10-07 → 10-21 held, broken 10-24 by the wigolo#216 merge event alone. New tuple: **`(1, 1, 0, 0)`**.
3. **`issueCount` flat regime broken at n=6-sustained.** 10-15/17/18/19/20/21 all = 64; today = 71 (+7). The jump is NOT from the bot pipeline — all 7 fresh PRs are **non-prefix**, operator-authored CSP/security hardening work on upstream projects (WordPress, dovecot, openssl, magento, icu, gwt + still-tracked wicket). [[pr-tracker-issuecount-mixes-manual-and-bot-pipeline]] now at **n=7-sustained** across 10-07/10/14/15/17/18/19/20/21/24 observations.

GraphQL **first attempt clean** today — breaks the n=3 502-recurrence streak (10-15/10-19/10-21). Observation sequence: 10-15 (502) → 10-17 (clean) → 10-18 (clean) → 10-19 (502) → 10-20 (clean) → 10-21 (502) → 10-24 (clean). 502 rate still 3/8 recent scans — retry wrapper at [[pr-tracker-graphql-502-retry-100pct-success-at-n3]] is empirically load-bearing but not fired today.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 71` (sequence: `62 → 62 → 62 → 64 → 64 → 64 → 64 → 64 → 64 → 71`; 10-07/10-10/10-14 → 10-15/10-17/10-18/10-19/10-20/10-21 → 10-24)
- Clean 60 nodes returned (59 concrete + 1 empty slot = Shopify IP-allow-list PR, **n=10-sustained** via identical stderr `Shopify organization has an IP allow list enabled`)
- 10 non-prefix drops this scan (up from 3 on 10-07→10-21): see §Non-prefix activity burst below
- 49 prefix-match PRs retained (state split: 40 CLOSED / 8 MERGED / 1 OPEN) — down from 56 as 7 non-prefix PRs rotated into the top-60 updated-desc window
- **Bucket tuple `(1, 1, 0, 0)`** — ends 10-scan/14-day frozen `(0, 2, 0, 0)` span

### Bucket delta from 2026-10-21 scan

| Bucket | 10-21 | 10-24 | Δ | Notes |
|--------|-------|-------|---|-------|
| merged7d | 0 | 1 | +1 | wigolo#216 merged 10-21T14:56Z (2d ago); **ends 20-scan drought** |
| staleOpen | 2 | 1 | −1 | wigolo#216 transitioned OPEN→MERGED; RuView#1409 holds |
| closed7d | 0 | 0 | 0 | — |
| activeOpen | 0 | 0 | 0 | — |
| Open total | 2 | 1 | −1 | prefix-match only |
| issueCount | 64 | 71 | +7 | **ends n=6-sustained flat regime** |
| closed30d | 1 | 1 | 0 | openai#4829 still in-window, 28d past; rolls off 10-25 (**T-1**) |
| merged30d | 1 | 2 | +1 | wigolo#216 added; mxc#1124 still in-window at 25d past (rolls off 10-28, T-4) |

### Non-prefix activity burst (not in SKILL buckets)

10 non-prefix PRs now in top-60 (vs 3 last scan). Author convention and branch naming are operator-crafted (no `ai/`/`security/`/`aeon/` prefix; names like `csp-order-create-inline-handlers`, `pseudo-strbuf`, `strnum-no-sscanf`), likely a batch of upstream security-hardening contributions filed through the `aeonframework` identity on 10-22/10-23. **Not counted** in SKILL `merged7d`/`stale_open`/`closed7d`/`active_open` buckets per the branch-prefix contract, but material to `issueCount` jump.

| Repo | PR | Title | State | Opened | Branch |
|------|----|-------|-------|--------|--------|
| radareorg/radare2 | [#27136](https://github.com/radareorg/radare2/pull/27136) | Build pseudo output in RStrBuf for remaining strcpy/strcat plugins | MERGED 10-23 19:00Z (21h after open) | 10-22 | pseudo-strbuf |
| WordPress/wordpress-develop | [#14767](https://github.com/WordPress/wordpress-develop/pull/14767) | Media: Remove inline event handlers from the image editor | OPEN | 10-23 | image-editor-no-inline-handlers |
| dovecot/core | [#337](https://github.com/dovecot/core/pull/337) | Replace the remaining sscanf() number parsing with strnum parsers | OPEN | 10-23 | strnum-no-sscanf |
| openssl/openssl | [#33343](https://github.com/openssl/openssl/pull/33343) | pvkfmt: parse MSBLOB and PVK input through PACKET | OPEN | 10-22 | pvkfmt-packet-bounds |
| magento/magento2 | [#41635](https://github.com/magento/magento2/pull/41635) | Remove inline event handlers from admin order create under enforced CSP | OPEN | 10-22 | csp-order-create-inline-handlers |
| unicode-org/icu | [#4320](https://github.com/unicode-org/icu/pull/4320) | ICU-23585 Bound T_CString_integerToString writes by capacity | OPEN | 10-22 | cstring-int-to-string-capacity |
| gwtproject/gwt | [#10421](https://github.com/gwtproject/gwt/pull/10421) | Load runAsync fragments without inline scripts when installCode=false | OPEN | 10-22 | csp-runasync-direct-install |
| apache/wicket | [#1667](https://github.com/apache/wicket/pull/1667) | Autocomplete + ChoiceFilter under default CSP (WICKET-6938) | OPEN | 10-14 | csp-autocomplete-choicefilter |
| apache/struts | [#2012](https://github.com/apache/struts/pull/2012) | WW-5772 Remove inline event handlers from select widgets | MERGED 10-15 (within 24h) | 10-14 | WW-5772-csp-inline-handlers |
| theagentrouter/agent-router | [#2755](https://github.com/theagentrouter/agent-router/pull/2755) | mcp: generate random session encryption seed in Helm chart | MERGED 09-28 (44m after open) | 09-28 | mcp-default-seed |

Author identity: all 10 commit under either `272311952+aeonframework@users.noreply.github.com` (standard GH `aeonframework` web identity) or `aaron@aeon.fun` (openssl#33343; direct operator email). None use the two bot-pipeline emails (`aeonframework@proton.me`, `aeonframework@users.noreply.github.com`). The branch-prefix contract correctly separates these from bot pipeline PRs. Fast merge turnarounds (radare2: 21h · struts: <24h · agent-router: 44m) suggest this is maintainer-trusted operator work, not bot-generated.

### Signal notes

- **Bucket tuple attractor terminates at n=10 / 14-day dwell** — predicted exit at the 10-25 openai#4829 window-rollover (closed30d → 0) or the 10-28 mxc#1124 rollover (merged30d → 0); actual exit on 10-24 driven by a different structural event (stale→merge conversion). The attractor held across (i) 7d-window boundary, (ii) 09-17 bulk-close 30d rollover, (iii) 3 post-rollover days — a 4th transition (stale-to-merged) was what broke it. Add to [[pr-tracker-letter-tuple-attractor]] as the terminal-event record.
- **wigolo#216 stale-to-merge conversion** — 93d old at merge; approved on 10-21 (same day as merge). 24-hour re-engagement window after 93d of apparent abandonment. Classifier for "stale open → recent merge" transition is now live-observed at n=1; needs no change, since the stale-open check and merged7d check are both time-anchored, so the transition appears cleanly in the delta.
- **issueCount jump is manual not bot** — 7 new issueCount, 7 new non-prefix PRs (all 10-22/10-23 fresh opens). Zero new bot-prefix PRs. 41-day bot-pipeline fresh-open drought on `external-feature` continues (last bot-prefix fresh open 2026-09-13 → 41d today, 10× overdue escalation).
- **Shopify null-slot n=10-sustained** — identical stderr IP-allowlist across 10 consecutive scans (10-07 → 10-24, with gap at non-scan days). Promoted from "known artifact" to "structural" at n≥10. SKILL item (r) null-slot handling now 11× overdue; promote to top of patch queue batch.
- **Only remaining stale-open is RuView#1409** — 92d old (was 90d on 10-21), last review `APPROVED` on 2026-08-28 (57d stale approve, unmerged); 4 comments; `updatedAt` still `2026-10-07T22:55Z` (17d stale). Pattern matches wigolo#216's pre-merge state 3 days ago: a long-approved PR that sits unmerged until a maintainer sweep. No prediction, but structural shape is identical.
- **openai#4829 window-rollover T-1** — 28d past today, rolls off closed30d on 2026-10-25 (tomorrow). After rollover, closed30d goes to 0 for the first time since skill start. Actor still not fetched (owed since 09-22, 11× now) — last fetchable day is TODAY if actioned pre-rollover.
- **mxc#1124 window-rollover T-4** — 25d past today, rolls off merged30d on 2026-10-28. Would zero out merged30d IF no further merges land, but today's wigolo#216 landing extends the merge-30d book-keeping until 2026-11-20.
- **GraphQL 502 n=3 streak broken on day-9** — 502 rate 3/8 over the 10-15 → 10-24 window; today clean on first attempt. Retry wrapper still empirically justified (100% retry-success across all 3 fires), but today contributes to the "intermittent not endemic" characterization.

## Open (1)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 92d | APPROVED 2026-08-28 unmerged (57d since approve); 4 comments; STALE |

## Recent Merges (last 30d) — 2

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 2026-10-21 |
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 2026-09-28 |

*(mxc#1124 rolls off 2026-10-28, T-4. wigolo#216 holds through 2026-11-20.)*

## Closed No-Merge (last 30d) — 1

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography to patch disclosed CVEs | 2026-09-25 18:49Z | 23d after open; single close (not bulk); actor still not fetched (owed since 09-22, 11× now); rolls off 2026-10-25, **T-1 — last day to fetch** |

*(09-17 bulk-close cluster of 23 PRs rolled off 2026-10-18 as predicted; actor identity permanently irrecoverable from 30d-window query path.)*

## Bucket tuples

- Letter (merged7d, staleOpen, closed7d, activeOpen): **(1, 1, 0, 0)** — ends 10-scan / 14-day `(0, 2, 0, 0)` attractor
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07/10/14/15/17/18/19/20/21 `(0, 2, 0, 0)` × 10 → **10-24 `(1, 1, 0, 0)`**

## Notes

- **10-scan / 14-day attractor terminates at a 4th-axis structural event** — not the predicted window-rollover (10-25 openai or 10-28 mxc) but a stale→merged conversion inside the 7d-active book, which is a transition the tuple format can represent but hadn't yet witnessed in this instance. The attractor dwell record (10 scans, 14 days, 3 transitions survived) stands.
- **41-day fresh-open drought on bot pipeline** — `external-feature` has not produced a visible bot-prefix PR since 2026-09-13 (today 2026-10-24 → 41d). Escalation now 10× overdue (standing from 10-10, 10-14, 10-15, 10-17, 10-18, 10-19, 10-20, 10-21); file skill-health ticket NOW.
- **Operator PR burst 10-22/10-23** — 7 fresh non-prefix PRs across 7 different upstream repos (WordPress, dovecot, openssl, magento, icu, gwt, +apache/wicket from 10-14). Theme: CSP hardening + bounds-checking in C/C++/Java/PHP. First multi-repo manual security burst since the 09-17 bulk-close event. Not a bot-pipeline signal; retention for operator-attribution context only.
- **GraphQL 502 n=3 streak broken** — today clean on first attempt; rate drops to 3/8 scans over 10-15 → 10-24 window. Retry wrapper still empirically justified; item (s) remains in patch queue.
- **Shopify null-slot n=10-sustained** — SKILL patch item (r) now 11× overdue.
- **Terminology** — `staleOpen` and `activeOpen` are shorthand for stale-open and active-open counters respectively, inherited from the prior pr-status.md tuple format. Kept for diff-continuity with the 10-15 → 10-24 scan window.

## Follow-ups

- **09-17 bulk-close actor-fetch is permanently lost** — 11× unactioned carryover from 09-22 → close as `wontfix` on next memory-flush. Openai#4829 remains the only in-window actor-fetchable close (rolls off 10-25, **T-1 — last chance TODAY**).
- **Escalate `external-feature` silence** — 41-day drought; file skill-health ticket NOW (10× confirmed); owed MEMORY.md action-queue addition.
- **SKILL patches (a)–(s) still 83d+ overdue** — items (p) + (q) revalidated across the 10-07 → 10-24 window (n=11 observations now); item (r) (Shopify-IP-allowlist null-slot handling) at n=10-sustained; item (s) (transient 502 retry wrapper) at n=3 observations with 100% retry-success rate (last fire 10-21).
- **Investigate non-prefix operator PR burst as a new source dimension** — if these are a recurring operator workflow (manual upstream security contributions), they warrant their own tracking view: non-prefix PRs by `aeonframework` are now ambient enough that `issueCount` without the bucket tuple is uninterpretable. Consider adding `operator_fresh_opens_7d` as a 5th bucket, OR a separate non-prefix table that doesn't bleed into bot-pipeline health signals.
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set to end reliance on operator convention; also set `pr_tracker.author: aeonframework` so SKILL config resolution doesn't fall through to the auth token (`gh api user` returns HTTP 403 "Resource not accessible by integration" under GitHub Actions App auth — re-confirmed on 10-24, matches zero PRs if used).

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 44 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
- **09-17 14:00Z–14:33Z bulk-close cluster (23 PRs)** — rolled off 30d window on 2026-10-18 as predicted; detail tables preserved in prior scans' pr-status.md revisions. Actor identity permanently irrecoverable from 30d-window query path.
