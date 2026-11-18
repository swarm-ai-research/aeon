# PR Status

*Last updated: 2026-11-18*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-11-18 — Day-66 post-recovery scan · **`(0, 1, 0, 1)` tuple holds n=4 (same composition as 11-16: RuView stale + opencart active-via-self-nudge) · issueCount 73 → 72 (4-scan plateau broken, −1 drift, one PR dropped from aeonframework-authored set) · GraphQL clean-first n=4 · Shopify null n=16 · Cursor null n=5 · zero endogenous events on prefix-match set since 11-14 (axis 6 bot self-nudge the only activity in last 4d)**

Prefix-match set: no new activity since the 11-14 bot self-nudge on opencart#15792. opencart`updatedAt=2026-11-14T22:06:50Z` and RuView `updatedAt=2026-11-05T14:44:51Z` both unchanged from 11-16 scan. Zero prefix-match state transitions in the 11-16 → 11-18 2-day window.

Bucket tuple holds `(0, 1, 0, 1)` at n=4 (10-31 → 11-05 → 11-16 → 11-18). Composition identical to 11-16 (RuView stale + opencart active-via-self-nudge), so this is a composition-preserving continuation not a fresh axis-6 event. Under axis-6 framing, 11-16 was the exit event; 11-18 is dwell. Under item (v) proposed semantics, opencart should be stale (commenter == author), producing `(0, 2, 0, 0)` and composition-identical to 11-07 — still ambiguous and still unresolved by SKILL text.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 72` (sequence: `… 71 → 73 → 73 → 73 → 73 → 72`; 10-21 → 10-31 → 11-05 → 11-07 → 11-16 → 11-18). **4-scan plateau at 73 broken by −1 drift**; new value matches no prior reading in running series.
- Clean 60 nodes returned (58 concrete + 2 empty IP-allowlist slots: Shopify + Cursor)
- 11 non-prefix drops this scan (unchanged set vs 11-16: 8 OPEN + 3 MERGED) — zero new opens/closes/merges; the 6-PR update burst noted on 11-16 (openssl/icu/dovecot/gwt/magento/wicket updated 11-14 → 11-16) has settled with no further updates in the 11-16 → 11-18 window
- 47 prefix-match PRs retained (state split: 38 CLOSED / 7 MERGED / 2 OPEN) — byte-identical to 10-31 / 11-05 / 11-07 / 11-16
- **Bucket tuple `(0, 1, 0, 1)`** — n=4 at this value (10-31 → 11-05 → 11-16 → 11-18); composition unchanged from 11-16

### Bucket delta from 2026-11-16 scan

| Bucket | 11-16 | 11-18 | Δ | Notes |
|--------|-------|-------|---|-------|
| merged7d | 0 | 0 | 0 | — |
| staleOpen | 1 | 1 | 0 | RuView#1409 holds (118d, 82d since approve) |
| closed7d | 0 | 0 | 0 | — |
| activeOpen | 1 | 1 | 0 | opencart#15792 holds (last activity 11-14 bot self-nudge, 4d; axis 5 recurrence projected for 11-21) |
| Open total | 2 | 2 | 0 | prefix-match only |
| issueCount | 73 | 72 | **-1** | **4-scan plateau at 73 broken**; dropped PR not in top-60 updated-desc set either scan — identity unknown without full-scan enumeration |
| closed30d | 0 | 0 | 0 | — |
| merged30d | 1 | 1 | 0 | wigolo#216 rolls off 2026-11-20 (2 days out) |

### Non-prefix activity (11 unchanged in top-60 updated-desc window — 11-14/15/16 burst settled, zero updates in 11-16 → 11-18 window)

- openssl/openssl#33343 OPEN 10-22 (**updatedAt=2026-11-16T14:48Z** — +2d from today; same timestamp as 11-16 scan)
- unicode-org/icu#4320 OPEN 10-22 (**updatedAt=2026-11-15T23:32Z** — +3d; unchanged from 11-16)
- dovecot/core#337 OPEN 10-23 (**updatedAt=2026-11-15T23:32Z** — +3d; unchanged)
- gwtproject/gwt#10421 OPEN 10-22 (**updatedAt=2026-11-14T22:06Z** — +4d; unchanged)
- magento/magento2#41635 OPEN 10-22 (**updatedAt=2026-11-14T22:06Z** — +4d; unchanged)
- apache/wicket#1728 OPEN 10-29 (**updatedAt=2026-11-14T22:06Z** — +4d; unchanged)
- apache/wicket#1667 OPEN 10-14 CHANGES_REQUESTED 10-29 (**updatedAt=2026-11-11T13:03Z** — +7d; unchanged)
- WordPress/wordpress-develop#14767 OPEN 10-23 (**updatedAt=2026-11-07T16:28Z** — +11d; unchanged)
- radareorg/radare2#27136 MERGED 10-23 (26d past merge; unchanged)
- apache/struts#2012 MERGED 10-15 (34d past merge, rolled off 30d window; unchanged)
- theagentrouter/agent-router#2755 MERGED 09-28 (51d past merge; unchanged)

### Signal notes

- **issueCount 73 → 72 is the first −1 drift in the post-recovery running series** — all prior deltas were +N (opens) or 0 (freezes). A −1 without any corresponding close/merge in the top-60 updated-desc window means the dropped PR is outside the 60-row window and fell out silently (repo deletion, PR deletion, author rename, or organization-scope change). Candidate SKILL item (x): emit a full-paginate enumeration when `issueCount` decreases, so the specific dropped PR is identifiable. Current scan cannot distinguish any of the 4 drop mechanisms.
- **4-scan plateau at 73 broken at n=4 (not n=5)** — prior longest-plateau was 71 × 3 (10-21 → 10-31). Current 73 × 4 (11-05 → 11-07 → 11-16 → 11-18) is now the longest plateau in the series, and it just terminated. Plateau-termination axis is a 7th exit axis in the attractor-exit schema when applied to `issueCount` instead of bucket tuple.
- **Axis-6 dwell confirmed at n=1** — 11-16 was the axis-6 entry event (bot self-nudge → stale-to-active); 11-18 is first dwell day. If opencart#15792 receives no further activity, 11-21 will produce axis-5 recurrence (20d → 23d, 11-14 last activity → >7d) and tuple should flip back to `(0, 2, 0, 0)`. Dwell-vs-exit tracking would require a per-axis dwell counter distinct from the bucket-tuple read.
- **SKILL item (v) stays highest-leverage patch** — today's bucket depends on strict/intent interpretation exactly as on 11-16. Under strict: `(0, 1, 0, 1)` n=4. Under commenter-≠-author: `(0, 2, 0, 0)` n=2 (matching 11-07 composition). The 2-day dwell sharpens the ambiguity's real-world cost: a maintainer reading the active-open row today sees "there is activity" when in fact the only activity is the bot nudging itself four days ago.
- **Shopify null-slot n=16-sustained** (16× overdue for SKILL item (r)). **Cursor null-slot n=5-sustained** (strengthens vendor-agnostic generalization per [[pr-tracker-ip-allowlist-null-slot-class-generalizes-beyond-shopify]]).
- **GraphQL clean-first n=4** — four consecutive clean scans since the 10-31 retry burst; retry wrapper item (s) still empirically justified by the burst memory.
- **Non-prefix queue settled after the 11-14/15/16 6-PR update burst** — zero further updates in the 11-16 → 11-18 window. If the burst was a single operator-side batch action (candidate SKILL item (w)), one-off attribution is now the simplest explanation; a label-sync cron pattern would have fired again by now.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 118d | APPROVED 2026-08-28 unmerged (82d since approve); last activity bot self-nudge 2026-11-05 (13d); STALE |
| opencart/opencart | [#15792](https://github.com/opencart/opencart/pull/15792) | [4.2.x.x] Lock coupon, reward and credit redemption checks at order confirmation | 2026-10-29 | 20d | 0 reviews; bot self-nudge comment 2026-11-14 (4d); ACTIVE under strict semantics / STALE under item (v) |

## Recent Merges (last 30d) — 1

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 2026-10-21 |

*(wigolo#216 rolled off merged7d on 2026-10-28; rolls off merged30d on 2026-11-20 — 2 days out.)*

## Closed No-Merge (last 30d) — 0

*(openai#4829 rolled off 2026-10-26T18:49Z; now permanently in archive-hidden/lost set.)*

## Bucket tuples

- Letter (merged7d, staleOpen, closed7d, activeOpen): **(0, 1, 0, 1)** — n=4 (RuView stale + opencart active-via-self-nudge, composition unchanged from 11-16)
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07/10/14/15/17/18/19/20/21 `(0, 2, 0, 0)` × 10 (RuView + openai) → 10-24/10-25 `(1, 1, 0, 0)` × 2 → 10-31 `(0, 1, 0, 1)` → 11-05 `(0, 1, 0, 1)` (RuView active + opencart active) → 11-07 `(0, 2, 0, 0)` (axis 5 endogenous aging) → 11-16 `(0, 1, 0, 1)` (axis 6 bot self-nudge) → **11-18 `(0, 1, 0, 1)` (n=4, axis-6 dwell day 1; composition: RuView stale + opencart active)**

## Notes

- **6-axis attractor-exit schema** (unchanged from 11-16) — (1) window boundary roll-off, (2) bulk-close rollover, (3) post-rollover days, (4) stale→merged conversion (all exogenous); (5) endogenous aging through activity threshold, (6) endogenous bot self-nudge across activity threshold. **Candidate 7th axis**: `issueCount` plateau termination without bucket-tuple transition — today's 73 × 4 → 72 is the first observation.
- **Axis-6 dwell semantics are underspecified** — SKILL assumes each scan reads a fresh state, so there's no concept of "axis entry vs dwell". At n=4 same-tuple scans the composition semantics matter: 11-05 and 11-16 are compositionally distinct (both `(0,1,0,1)`, but 11-05 had opencart in pre-stale 7d window, 11-16/18 has opencart in post-nudge 7d window). Future scans should annotate the composition hash.
- **20-day cohort freeze extended to 22 days** — last actual maintainer-side GitHub event on any prefix-match PR was wigolo#216 merge at 2026-10-21T14:56:16Z (28 days); last review was RuView approval at 2026-08-28T06:24:47Z (82 days). Every prefix-match state change since then has been either bot self-nudge (RuView 9-10, 10-07, 11-05; opencart 11-14) or window-based reclassification.
- **Non-prefix queue quiet after 11-14/15/16 burst** — zero updates in the 11-16 → 11-18 window across all 11 non-prefix PRs. If the burst was a single operator batch action (hypothesized in 11-16 notes), recurrence would have been expected within ~2 days under label-sync cron; two days of silence is consistent with one-off attribution.
- **Null-slot class: 2 vendors × 21 total observations** (Shopify 16 + Cursor 5) — item (r) per-org counter pattern strengthened; +2 observations in 2-day window.
- **Next projected transitions (2026-11-19+)**: (a) opencart#15792 crosses 7d from the 11-14 comment on **2026-11-21** → stale again (axis 5 recurrence, 3d out); (b) wigolo#216 rolls off merged30d on **2026-11-20** → drops merge count to 0 on 30d window too (2d out); (c) if a maintainer responds on opencart#15792 OR a new aeonframework PR opens, the `issueCount=72` reading will shift and the dropped-PR mystery stays deferred; (d) if `issueCount` holds at 72 for ≥3 scans, candidate item (x) full-paginate on decrease becomes lower urgency.
