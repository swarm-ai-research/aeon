# PR Status

*Last updated: 2026-07-11*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but all live bot PRs use `security/*` head branches per [[pr-tracker-branch-prefix-misses-bot-identity]]. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66) AND `aeon@aeonframework.dev` (Vibe-Trading#390). Inline OR filter required — accept if branch startswith `ai/` OR commit email matches any known bot identity. SKILL.md-documented AND filter would still drop the entire queue.

## Open (1)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 14d 15h | **active** — 1 comment, last `updatedAt` 2026-07-06T13:32:11Z (~4.9d ago) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| — | — | none within 7d window | — | tamnd/kage#66 rolled off at 2026-07-10T12:20:11Z (~23h before this run); reappears only if a new closed-no-merge lands |

---

GraphQL `author:aeonframework is:pr` → 3 nodes (2026-07-11 run). Snapshot vs 2026-07-10 run: **first material state change in 6 days — kage#66 exited the 7d closed-no-merge window as predicted.**

1. **HKUDS/Vibe-Trading#390** — still MERGED at 2026-07-05T15:33:53Z. Head SHA `85c7e5d616584aba5bb6ad90c19aedab8f7124eb` (unchanged). Now 5.82d into the 7d recent-merge window (was 4.77d yesterday), rolls off 2026-07-12T15:33:53Z (~28h 20m after this snapshot).
2. **Panniantong/Agent-Reach#436** — still OPEN. Last activity `updatedAt` 2026-07-06T13:32:11Z (unchanged for 5th consecutive day). Head SHA `c4301c5b359379da26fef861ae1adb0624441358`. Comment count still 1. Age 14.66d. Activity now ~4.90d ago — still inside the 7d active window, tips back to stale on 2026-07-13T13:32:11Z if no new activity.
3. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). Head SHA `ceeff4ab50238f357db120e6052fd5b0372d4d13`. 7.95d in the closed-no-merge window; **rolled off** (>7d threshold crossed at 2026-07-10T12:20:11Z, ~22h 54m before this snapshot). Removed from Closed No-Merge table.

## Categorization (today = 2026-07-11, now = 2026-07-11T11:14:01Z)

- **Recent merges (7d):** 1 — HKUDS/Vibe-Trading#390 (merged 2026-07-05, 5.82d ago)
- **Stale open (>7d, no activity 7d):** 0 — Agent-Reach#436 still within active window (activity 4.90d ago)
- **Active open:** 1 — Panniantong/Agent-Reach#436 (14.66d old, activity 4.90d ago)
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off at 2026-07-10T12:20:11Z (7.95d ago > 7d threshold)

## Notify decision — legitimate state change → **NOTIFY**

SKILL.md step-5 gate says notify (recent merges ≥ 1). Trigger-set hash — the tuple `[(Vibe-Trading, 390, MERGED, 2026-07-05T15:33:53Z, 85c7e5d6…), (Agent-Reach, 436, OPEN, 2026-07-06T13:32:11Z, c4301c5b…)]` — **differs from the 2026-07-10 run** (kage#66 dropped from the trigger set; category count `closed_no_merge: 1 → 0`).

Per [[pr-tracker-notify-repeats-with-no-state-change]], the hash-based dedup guard applied 2026-07-09/10 correctly does NOT suppress today — kage#66's calendar-triggered rolloff (predicted 2026-07-10T12:20Z, actual 2026-07-10T12:20:11Z) produced the expected state change. Firing.

## Filter and API drift (unchanged from 2026-07-10)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) still required for the 13th consecutive day (2026-06-29 → 2026-07-11) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run.
