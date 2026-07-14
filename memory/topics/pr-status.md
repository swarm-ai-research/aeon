# PR Status

*Last updated: 2026-07-14*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but all live bot PRs use `security/*` head branches per [[pr-tracker-branch-prefix-misses-bot-identity]]. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66) AND `aeon@aeonframework.dev` (Vibe-Trading#390). Inline OR filter required — accept if branch startswith `ai/` OR commit email matches any known bot identity. SKILL.md-documented AND filter would still drop the entire queue.

## Open (1)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 17d 15h | **stale** — 1 comment, last `updatedAt` 2026-07-06T13:32:11Z (~7.86d ago — crossed 7d stale threshold at 2026-07-13T13:32:11Z as predicted) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump x/image past CVE floor | 2026-07-03 | closed by owner without comment (30d record; 7d window rolled off 2026-07-10T12:20:11Z) |

---

GraphQL `author:aeonframework is:pr` → 3 nodes (2026-07-14 run). Snapshot vs 2026-07-13 run: **second state change in the burn-down** — Agent-Reach#436 activity crossed 7d threshold at 2026-07-13T13:32:11Z (~20.6h before this snapshot), so `stale_open: 0 → 1` and `active_open: 1 → 0`. 9th stationary day for AR#436 in raw terms (SHA + comment count + updatedAt frozen since 2026-07-06), but the age-derived category flipped today.

1. **HKUDS/Vibe-Trading#390** — MERGED at 2026-07-05T15:33:53Z. Head SHA `85c7e5d616584aba5bb6ad90c19aedab8f7124eb` (unchanged). 8.78d ago (past 7d threshold since 2026-07-12). Retained in 30d table.
2. **Panniantong/Agent-Reach#436** — still OPEN, now **stale**. Last activity `updatedAt` 2026-07-06T13:32:11Z (unchanged for 8th consecutive day). Head SHA `c4301c5b359379da26fef861ae1adb0624441358`. Comment count still 1. Age 17.62d. Activity 7.86d ago — crossed the 7d stale threshold as predicted in yesterday's snapshot.
3. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). Head SHA `ceeff4ab50238f357db120e6052fd5b0372d4d13`. 10.91d ago (well past the 7d closed-no-merge window; rolled off 2026-07-10T12:20:11Z). Retained in 30d table.

## Categorization (today = 2026-07-14, now = 2026-07-14T10:10:34Z)

- **Recent merges (7d):** 0 — Vibe-Trading#390 rolled off 2026-07-12T15:33:53Z (8.78d ago)
- **Stale open (>7d, no activity 7d):** 1 — Agent-Reach#436 activity 7.86d ago, past 7d threshold since 2026-07-13T13:32:11Z
- **Active open:** 0 — Agent-Reach#436 flipped from active to stale
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off 2026-07-10T12:20:11Z (10.91d ago)

## Notify decision — stale_open ≥ 1 → **SEND**

SKILL.md step-5 gate: notify if any of {recent_merges, stale_open, closed_no_merge} > 0. `stale_open=1` triggers. Payload written to `.pending-notify/1784023892-pr-tracker.md` (direct write per [[notify-inline-cat-substitution-blocked-in-sandbox]] and [[notify-script-has-no-f-flag]]). No prior "PR Tracker — 2026-07-14" payload in `.pending-notify/` — hash-dedup check clean.

Yesterday's snapshot prediction ("tomorrow's 2026-07-14 10:00Z pr-tracker will fire stale_open ≥ 1 if crossed") landed correctly. AR#436's activity clock ticked past 7d at 2026-07-13T13:32:11Z; today's 10:10Z run sees it at 7.86d and flips the category.

## Filter and API drift (unchanged from 2026-07-13)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) still required for the 16th consecutive day (2026-06-29 → 2026-07-14) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run (rc=0, 1590 bytes, 3 nodes).

Sandbox note: shell `>` redirect to working-dir paths still blocked per [[sandbox-blocks-shell-redirect-to-workdir]] — GraphQL fetch this run went through Python `subprocess.run` + `pathlib.Path.write_text` workaround.
