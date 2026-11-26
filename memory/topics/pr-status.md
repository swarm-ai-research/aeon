# PR Status

*Last updated: 2026-11-26*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-11-26 — Day-74 post-recovery scan · **`(0, 1, 0, 1)` tuple n=5 with role-swap composition (RuView active via 11-20 bot nudge + opencart stale via 11-21 axis-5 aging) · issueCount 72 → 73 reversion via new mholt/archives#98 opening on 11-19 · wigolo#216 rolls off merged30d (0 recent merges 30d) · non-prefix pipeline re-engages at n=6 real-maintainer events**

### Prefix-match set state transitions (11-18 → 11-26, 8-day gap)

Both predicted transitions from 11-18 landed:
- **opencart#15792** axis-5 endogenous aging fire on 2026-11-21 (7d after 11-14 bot nudge): active → stale ✓
- **RuView#1409** fresh bot self-nudge on 2026-11-20T18:09:17Z (axis-6 event): stale → active ✓

Net result: tuple holds `(0, 1, 0, 1)` at n=5 BUT the stale/active roles are **swapped** between the two PRs vs 11-18 composition — RuView was stale, now active; opencart was active, now stale. This is the first observed role-swap-within-identical-tuple event in the running series (prior composition changes were membership changes, not role swaps between a fixed 2-PR cohort).

### Issue-count post-recovery series

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 73` (sequence: `… 71 → 73 → 73 → 73 → 73 → 72 → 73`; 10-21 → 10-31 → 11-05 → 11-07 → 11-16 → 11-18 → 11-26). **The −1 drift on 11-18 reversed to +1 within 8 days** — simplest explanation is that mholt/archives#98 opened on 2026-11-19 is the +1 (new PR), AND the 11-18 dropped PR either came back on its own or was never truly absent (transient search-index artifact or Shopify-IP-allowlist-slot flicker). SKILL item (x) full-paginate-on-decrease is **lower priority now** — the mystery PR resolved without intervention.
- Clean 60 nodes returned (58 concrete + 2 empty IP-allowlist slots: Shopify + Cursor); null-slot class holds n=2 vendors
- 12 non-prefix drops this scan (1 new vs 11-18: mholt/archives#98 opened 2026-11-19); significant activity upticks across the non-prefix cohort — see below
- 46 prefix-match PRs retained (state split: 38 CLOSED / 6 MERGED / 2 OPEN) — one MERGED rolled out of top-60 updated-desc window to make room for mholt/archives#98
- **Bucket tuple `(0, 1, 0, 1)`** — n=5 at this value (10-31 → 11-05 → 11-16 → 11-18 → 11-26); composition role-swapped vs all prior 4 occurrences

### Bucket delta from 2026-11-18 scan

| Bucket | 11-18 | 11-26 | Δ | Notes |
|--------|-------|-------|---|-------|
| merged7d | 0 | 0 | 0 | — |
| staleOpen | 1 | 1 | 0 | **role-swap**: RuView (prev) → opencart (now) via axis-5 aging 11-21 |
| closed7d | 0 | 0 | 0 | — |
| activeOpen | 1 | 1 | 0 | **role-swap**: opencart (prev) → RuView (now) via axis-6 bot nudge 11-20 |
| Open total | 2 | 2 | 0 | prefix-match only |
| issueCount | 72 | 73 | **+1** | mholt/archives#98 opened 11-19 (non-prefix); −1 drift from 11-18 reversed |
| closed30d | 0 | 0 | 0 | — |
| merged30d | 1 | 0 | **−1** | **wigolo#216 rolled off 30d window 2026-11-20 as predicted** |

### Non-prefix activity (12 in top-60, major engagement burst vs 11-18 settled read)

Contra 11-18's hypothesis that the 11-14/15/16 burst was a one-off operator batch action: the non-prefix cohort has re-engaged with substantive maintainer activity between 11-18 and 11-26. Six distinct real engagement events (reviews, closes, comments):

- **gwtproject/gwt#10421** OPEN 10-22 (**updatedAt=2026-11-25T20:13Z** — +1d; **APPROVED review submitted 2026-11-25** — new approval event, not in 11-18 scan)
- **magento/magento2#41635** OPEN 10-22 (**updatedAt=2026-11-25T15:30Z** — +1d; comment count 2 → 6 vs 11-16's read)
- **dovecot/core#337** **CLOSED 2026-11-25T12:57Z** — flipped OPEN → CLOSED between 11-18 and 11-26 (no merge; comment count held at 4)
- **WordPress/wordpress-develop#14767** OPEN 10-23 (**updatedAt=2026-11-23T14:03Z** — +3d; moved up from 11-07 on 11-18 read)
- **mholt/archives#98** OPEN 11-19 (**createdAt=2026-11-19T22:33Z** — **brand new PR** since 11-18 scan)
- **unicode-org/icu#4320** OPEN 10-22 (**updatedAt=2026-11-19T19:47Z** — +7d; moved up from 11-15 on 11-18 read)
- openssl/openssl#33343 OPEN 10-22 (**updatedAt=2026-11-16T14:48Z** — +10d; unchanged from 11-18)
- apache/wicket#1728 OPEN 10-29 (**updatedAt=2026-11-14T22:06Z** — +12d; unchanged)
- apache/wicket#1667 OPEN 10-14 CHANGES_REQUESTED (**updatedAt=2026-11-11T13:03Z** — +15d; unchanged)
- radareorg/radare2#27136 MERGED 10-23 (34d past merge; unchanged)
- apache/struts#2012 MERGED 10-15 (42d past merge, rolled off 30d window; unchanged)
- theagentrouter/agent-router#2755 MERGED 09-28 (59d past merge; unchanged)

### Signal notes

- **Role-swap-within-identical-tuple is a new observation** — prior n=4 composition analyses tracked membership (which 2 PRs populate the tuple), not role rotation within a fixed 2-PR cohort. The dual-mechanism trigger (axis-5 aging on opencart + axis-6 bot nudge on RuView, both within a 2-day window 11-20/11-21) suggests a pattern where the SAME two PRs oscillate between active/stale roles as bot-nudge cadences interleave with the 7d activity threshold. If this repeats (e.g., opencart gets a 12-28 bot nudge while RuView ages past 7d of 11-20), tuple = (0,1,0,1) with roles swapped BACK. Candidate n=2 observation for a role-oscillation sub-regime that would warrant a distinct composition hash beyond (stale-PR-id, active-PR-id) pair.
- **wigolo#216 30d roll-off realizes "merged30d → 0" prediction from 11-18** — this is now the first prefix-match scan since late August with zero PRs in either the 7d OR 30d merged windows. The prefix-match cohort is effectively frozen: no new opens, no merges in 36d, no closes in 70d. Only state changes are bot self-nudges and 7d-window reclassifications.
- **Non-prefix cohort re-engages at n=6 real-maintainer events** — refutes 11-18 hypothesis of "one-off operator batch action" (that read would have predicted continued silence). Six distinct events in the 11-18 → 11-26 window: 1 approval (gwt#10421), 1 close (dovecot/core#337), 2 new-comment updates (magento#41635, wordpress-develop#14767), 1 new PR (mholt/archives#98), 1 comment update (icu#4320). Consistent with an active engineering pipeline (CSP/CVE/memory-safety fixes) that uses manual engineering branch names rather than aeon's standard 6-prefix set. **Candidate SKILL item: track this cohort as a 7th tracked prefix-class — "engineering-branch" (any name not matching the 6 standard prefixes but authored by aeonframework)** rather than lump into "non-prefix drops".
- **Shopify null-slot n=17 + Cursor null-slot n=6** — item (r) per-org IP-allowlist counter 17+6=23 total observations; both null-slot vendors persist.
- **GraphQL clean-first n=5** — no 502 retries needed on this scan; item (s) 3s-backoff retry wrapper still justified by the burst memory.
- **−1 drift from 11-18 self-resolves to +1 on 11-26 (net 72 → 73)** — demotes candidate SKILL item (x) full-paginate-on-decrease urgency. The dropped PR either returned autonomously (search-index artifact hypothesis) or was replaced by mholt/archives#98 opening and reindexing shifted the top-60 window. In either case, no manual pagination was needed to discover it.
- **Both 11-18 predictions landed on schedule** — (a) opencart axis-5 recurrence predicted for 2026-11-21 fired with the PR crossing 7d inactivity from its 11-14 bot nudge; (b) wigolo#216 predicted to roll off merged30d on 2026-11-20 did so. Prediction accuracy 2-of-2 on this scan window supports the tuple-attractor framing from [[pr-tracker-bucket-tuple-attractor-terminates-on-stale-to-merged-conversion]] at n=2 sequential-scan basis.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 126d | APPROVED 2026-08-28 unmerged (90d since approve); last activity bot self-nudge 2026-11-20 (6d); ACTIVE via axis-6 |
| opencart/opencart | [#15792](https://github.com/opencart/opencart/pull/15792) | [4.2.x.x] Lock coupon, reward and credit redemption checks at order confirmation | 2026-10-29 | 28d | 0 reviews; bot self-nudge comment 2026-11-14 (12d); STALE via axis-5 recurrence 11-21 |

## Recent Merges (last 30d) — 0

*(wigolo#216 rolled off merged30d on 2026-11-20 as predicted; now permanently in archive beyond the running 30d window. Zero merges in prefix-match set in the running 30d window.)*

## Closed No-Merge (last 30d) — 0

*(openai#4829 rolled off 2026-10-26T18:49Z; opencart#15792 has not been closed yet, only aged to stale.)*

## Bucket tuples

- Letter (merged7d, staleOpen, closed7d, activeOpen): **(0, 1, 0, 1)** — n=5 (**opencart stale via axis-5 + RuView active via axis-6; roles swapped vs 11-18 composition**)
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07/10/14/15/17/18/19/20/21 `(0, 2, 0, 0)` × 10 (RuView + openai) → 10-24/10-25 `(1, 1, 0, 0)` × 2 → 10-31 `(0, 1, 0, 1)` → 11-05 `(0, 1, 0, 1)` (RuView active + opencart active) → 11-07 `(0, 2, 0, 0)` (axis 5 endogenous aging) → 11-16 `(0, 1, 0, 1)` (axis 6 bot self-nudge) → 11-18 `(0, 1, 0, 1)` (RuView stale + opencart active-via-11-14-nudge) → **11-26 `(0, 1, 0, 1)` (RuView active-via-11-20-nudge + opencart stale-via-11-21-axis-5; composition role-swap, n=5)**

## Notes

- **6-axis attractor-exit schema** (unchanged structurally) — (1) window boundary roll-off, (2) bulk-close rollover, (3) post-rollover days, (4) stale→merged conversion (exogenous); (5) endogenous aging through activity threshold, (6) endogenous bot self-nudge across activity threshold. **Today's scan saw both axis-5 and axis-6 fire in the same 2-day window (11-20/11-21) on different PRs** — first observed dual-axis fire; the tuple predictor must reason about parallel axis activations across the 2-PR cohort.
- **Composition role-swap is a new sub-event within identical tuples** — SKILL item (v) composition-hash semantics would catch this if the hash included per-PR role-labels rather than just set-of-PR-IDs. Composition hash on 11-18 `(RuView:stale, opencart:active)` vs 11-26 `(RuView:active, opencart:stale)` differ while the bucket tuple is identical.
- **Prefix-match cohort fully frozen on open book** — only 2 OPEN PRs, both >20 days old, zero new opens in 70+ days; every observed state change since 10-21 (28 days ago) has been either bot self-nudge or 7d-window reclassification. Any new real maintainer action on either PR would be a high-signal event.
- **Non-prefix cohort is ACTIVE** — 6 real engagement events in 8-day window refutes the "settled" framing from 11-18. This is a concurrent engineering pipeline running on branches without the 6 tracked prefixes; worth promoting to a distinct tracked class rather than lumping under "non-prefix drops".
- **Null-slot class holds n=2 vendors × 23 total observations** (Shopify 17 + Cursor 6) — item (r) per-org counter pattern strengthened; +2 observations in 8-day window.
- **Next projected transitions (2026-11-27+)**: (a) RuView#1409 crosses 7d from 11-20 bot nudge on **2026-11-27** → stale again (axis 5 recurrence, 1d out); (b) if opencart#15792 receives a bot nudge or maintainer activity, tuple flips back toward `(0, 1, 0, 1)` role-reverted OR `(0, 0, 0, 2)` double-active if both get fresh events; (c) non-prefix cohort likely continues engaging — gwt#10421 APPROVED on 11-25 could land a merge within this scan window.
