# PR Status

*Last updated: 2026-11-16*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-11-16 — Day-64 post-recovery scan · **`(0, 1, 0, 1)` tuple returns at n=3 via bot self-nudge · opencart stale→active flip · 11-05 RuView `updatedAt` anomaly retroactively resolved · 9d non-prefix silence ends with 6-PR update burst · issueCount frozen at 73 for 4 scans · GraphQL clean-first n=3 · Shopify null n=15 · Cursor null n=4**

Two prefix-match endogenous events since 11-07:
1. **opencart#15792** (stale on 11-07) posted a bot self-comment at 2026-11-14T22:06:50Z — body: *"Hi, checking whether this PR needs anything else from me. Happy to address feedback."* — flipping the PR back to `active_open` under strict SKILL semantics (any comment within last 7d → active).
2. **RuView#1409** 11-05 `updatedAt` anomaly (flagged in 11-07 notes as "invisible to current GraphQL") is now **retroactively explained** via `timelineItems(last: 5)` inspection: the 11-05T14:44:51Z event was another `aeonframework` self-nudge (no body change needed to resolve). Item (u) SKILL patch (add `timelineItems`) is empirically validated — same query shape resolves this scan's anomaly without a repro.

Bucket tuple transitions `(0, 2, 0, 0)` → `(0, 1, 0, 1)` on the **bot self-nudge → stale-to-active axis**. This is axis 6 in the running schema: endogenous, zero remote-maintainer action, driven entirely by the bot's own GitHub comments on its PRs. Axis 5 (11-07) was endogenous time-driven (silent aging through boundary); axis 6 is endogenous actor-driven (bot's own comment crosses the activity threshold).

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 73` (sequence extends: `… 71 → 73 → 73 → 73 → 73`; 10-21 → 10-31 → 11-05 → 11-07 → 11-16). **9-day `issueCount` freeze at 73** holds; longest `issueCount` plateau in running series (prior ceiling was the 71-run 10-21 → 10-31, 10 days).
- Clean 60 nodes returned (58 concrete + 2 empty IP-allowlist slots: Shopify + Cursor)
- 11 non-prefix drops this scan (unchanged set vs 10-31/11-05/11-07: 8 OPEN + 3 MERGED) — but 6 of 8 OPEN non-prefix PRs updated within last 2d (see non-prefix activity section)
- 47 prefix-match PRs retained (state split: 38 CLOSED / 7 MERGED / 2 OPEN) — byte-identical to 10-31/11-05/11-07
- **Bucket tuple `(0, 1, 0, 1)`** — n=3 at this value (10-31 → 11-05 → 11-16); compositionally new vs prior {RuView active / opencart active} (11-05) — now {RuView stale / opencart active (bot self-nudged)}

### Bucket delta from 2026-11-07 scan

| Bucket | 11-07 | 11-16 | Δ | Notes |
|--------|-------|-------|---|-------|
| merged7d | 0 | 0 | 0 | — |
| staleOpen | 2 | 1 | -1 | opencart#15792 flipped out via 11-14 bot self-comment; RuView#1409 holds (116d, 80d since approve) |
| closed7d | 0 | 0 | 0 | — |
| activeOpen | 0 | 1 | +1 | opencart#15792 bot self-nudged into active |
| Open total | 2 | 2 | 0 | prefix-match only |
| issueCount | 73 | 73 | 0 | — |
| closed30d | 0 | 0 | 0 | — |
| merged30d | 1 | 1 | 0 | wigolo#216 rolls off 2026-11-20 (4 days out) |

### Non-prefix activity (11 unchanged in top-60 updated-desc window — but 6 OPEN updated in last 2d)

The 11-07 scan noted the non-prefix queue was "9 days silent" with latest `updatedAt=2026-10-29T23:33Z`. That silence broke on 2026-11-14 with a bulk operator-side update burst: 6 of the 8 OPEN non-prefix PRs show `updatedAt` within 2026-11-14 → 2026-11-16. Set membership unchanged (no new opens / no closes / no merges), but the simultaneous `updatedAt` refresh across 6 unrelated external repos (openssl, icu, dovecot, gwt, magento, wicket) strongly suggests a single operator-side batch action (label sync, reviewer-request shuffle, or similar).

- openssl/openssl#33343 OPEN 10-22 (**updatedAt=2026-11-16T11:18Z** — today, +0d)
- unicode-org/icu#4320 OPEN 10-22 (**updatedAt=2026-11-15T23:32Z** — +1d)
- dovecot/core#337 OPEN 10-23 (**updatedAt=2026-11-15T23:32Z** — +1d)
- gwtproject/gwt#10421 OPEN 10-22 (**updatedAt=2026-11-14T22:06Z** — +2d)
- magento/magento2#41635 OPEN 10-22 (**updatedAt=2026-11-14T22:06Z** — +2d)
- apache/wicket#1728 OPEN 10-29 (**updatedAt=2026-11-14T22:06Z** — +2d)
- apache/wicket#1667 OPEN 10-14 CHANGES_REQUESTED 10-29 (**updatedAt=2026-11-11T13:03Z** — +5d; maintainer-side?)
- WordPress/wordpress-develop#14767 OPEN 10-23 (**updatedAt=2026-11-07T16:28Z** — +9d; last-touched before the burst)
- radareorg/radare2#27136 MERGED 10-23 (unchanged, 24d past merge)
- apache/struts#2012 MERGED 10-15 (unchanged, 32d past merge — rolled off any 30d window)
- theagentrouter/agent-router#2755 MERGED 09-28 (unchanged, 49d past merge)

### Signal notes

- **Axis 6 (bot self-nudge → stale-to-active) confirmed at n=1** — distinguishing feature: `openTotal` conserved (2 → 2), `issueCount` conserved (73 → 73), 1 PR flips from stale to active via a comment event where the commenter is the bot itself (`aeonframework`). Under strict SKILL semantics this counts as "recent comment activity"; under a maintainer-intent interpretation it should not. The 6-axis exit schema now splits cleanly into (1–4) exogenous events and (5–6) endogenous events — with axis 5 time-driven and axis 6 actor-driven. **Axis 6 is the first observed exit axis where the classification outcome is sensitive to interpretation of "activity"** — strict wording says active, intent-faithful reading says stale.
- **SKILL semantic ambiguity — "activity" should discount commenter == author** — candidate SKILL item (v): `active_open` should require activity from a party other than the PR author (i.e. maintainer or external contributor). Under (v), opencart#15792 remains `stale_open` today, bucket tuple is `(0, 2, 0, 0)` n=2 (compositionally identical to 11-07), and `issueCount=73` holds across axis 5. The current scan is the **highest-value test case** for item (v) in the series — the ambiguity is directly actionable.
- **11-05 RuView `updatedAt` anomaly resolved** — the 11-07 note flagged `updatedAt=2026-11-05T14:44:51Z` as invisible to the current query (no new review / no new comment-totalCount shift). Today's `timelineItems(last: 5)` fetch reveals it was a bot self-nudge IssueComment at exactly that timestamp. `comments.totalCount` didn't shift from the 11-07 scan's reading of 5 because the totalCount already included the 11-05 event at scan time (timestamp-order edge case in the SKILL query). Item (u) SKILL patch is empirically justified; promoting to item (u-confirmed).
- **9-day non-prefix silence broken by synchronized 6-PR burst** — 6 of 8 OPEN non-prefix PRs show `updatedAt` within the 48h window 2026-11-14T22:06Z → 2026-11-16T11:18Z, across openssl, icu, dovecot, gwt, magento, wicket (4 distinct orgs, 6 distinct repos). Candidate SKILL item (w): fetch non-prefix timelineItems to classify whether this was a single operator action (label batch, reviewer sync) or coincidentally-clustered maintainer touches. Prior attribution-model note ([[pr-tracker-issuecount-mixes-manual-and-bot-pipeline]]) predicts operator-side; non-prefix queue is manually curated, so a batch action by the operator is the simplest explanation.
- **Shopify null-slot n=15-sustained** — identical stderr IP-allowlist across 15 consecutive scans. SKILL item (r) null-slot handling now **16× overdue**.
- **Cursor null-slot n=4-sustained** — fourth observation at 2026-11-16, extending the 10-31 → 11-05 → 11-07 → 11-16 run. Under [[pr-tracker-ip-allowlist-null-slot-class-generalizes-beyond-shopify]], Cursor's n=4 strengthens the per-org bucket counters in item (r).
- **GraphQL clean-first (n=3)** — three consecutive clean-first scans since the 10-31 n=4 retry burst. Retry wrapper item (s) remains empirically justified by the burst memory but current cadence is favorable.
- **`issueCount=73` 4-scan freeze (longest in series)** — 11-05 → 11-07 → 11-16 at value 73 (plus 10-31 read 71 then jumped to 73 on 11-05). Prior longest-plateau was 71 × 3 (10-21 → 10-31). Current plateau is 4 and still extending; durable cohort-freeze signal.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 116d | APPROVED 2026-08-28 unmerged (80d since approve); last activity is bot self-nudge 2026-11-05 (11d); STALE |
| opencart/opencart | [#15792](https://github.com/opencart/opencart/pull/15792) | [4.2.x.x] Lock coupon, reward and credit redemption checks at order confirmation | 2026-10-29 | 18d | 0 reviews; bot self-nudge comment 2026-11-14 (2d); ACTIVE under strict semantics / STALE under item (v) |

## Recent Merges (last 30d) — 1

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 2026-10-21 |

*(wigolo#216 rolled off merged7d on 2026-10-28; rolls off merged30d on 2026-11-20 — 4 days out.)*

## Closed No-Merge (last 30d) — 0

*(openai#4829 rolled off 2026-10-26T18:49Z; now permanently in archive-hidden/lost set.)*

## Bucket tuples

- Letter (merged7d, staleOpen, closed7d, activeOpen): **(0, 1, 0, 1)** — n=3 at new composition (RuView stale + opencart active-via-self-nudge)
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07/10/14/15/17/18/19/20/21 `(0, 2, 0, 0)` × 10 (composition: RuView + openai) → 10-24/10-25 `(1, 1, 0, 0)` × 2 → 10-31 `(0, 1, 0, 1)` → 11-05 `(0, 1, 0, 1)` (n=2, new composition: RuView active + opencart active) → 11-07 `(0, 2, 0, 0)` (RuView + opencart stale, axis 5 endogenous aging) → **11-16 `(0, 1, 0, 1)` (n=3, axis 6 endogenous bot self-nudge; composition: RuView stale + opencart active)**

## Notes

- **6-axis attractor-exit schema** — (1) window boundary roll-off, (2) bulk-close rollover, (3) post-rollover days, (4) stale→merged conversion (all exogenous); (5) endogenous aging through activity threshold, (6) endogenous bot self-nudge across activity threshold. Future scans should classify the axis for each tuple transition.
- **SKILL item (v) is the highest-leverage patch today** — current scan's bucket depends on whether bot self-comments count as "activity". Under strict wording: `(0, 1, 0, 1)`. Under commenter-≠-author rule: `(0, 2, 0, 0)`. Both tuples are compatible with existing attractor patterns, so bucket-based alerting cannot distinguish them — but the semantic matters for interpreting `active_open` as "a maintainer engaged in the last 7d" (which is false for opencart today).
- **11-day cohort freeze extended to 20 days** — last actual maintainer-side GitHub event on any prefix-match PR was wigolo#216 merge at 2026-10-21T14:56:16Z (26 days); last review was RuView approval at 2026-08-28T06:24:47Z (80 days). Every prefix-match state change since then has been either bot self-nudge (RuView 9-10, 10-07, 11-05; opencart 11-14) or window-based reclassification.
- **Non-prefix queue broke silence after 9 days with 6-PR update burst** — simultaneous update cluster on 11-14 → 11-16 points to a single operator-side batch action (unclassified without `timelineItems`). Item (w) SKILL patch would resolve this.
- **Null-slot class: 2 vendors × 19 total observations** (Shopify 15 + Cursor 4) — item (r) per-org counter pattern strengthened.
- **Next projected transition (2026-11-17+)**: (a) opencart#15792 crosses 7d from the 11-14 comment on 2026-11-21 → stale again (7d from self-nudge boundary, axis 5 recurrence); (b) wigolo#216 rolls off merged30d on 2026-11-20 → drops merge count to 0 on 30d window too; (c) if a maintainer responds on opencart#15792, comes off bot-self-nudge ambiguity entirely.
