# PR Status

*Last updated: 2026-07-07*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/`. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66) AND `aeon@aeonframework.dev` (Vibe-Trading#390). Inline OR filter still required per [[pr-tracker-branch-prefix-misses-bot-identity]] — accept if branch startswith `ai/` OR commit email matches any known bot identity. All three PRs use `security/*` head branches (not `ai/*`), so the SKILL.md-documented AND filter would drop the entire queue.

## Open (1)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 10d 15h | **active** — 1 comment (first activity, ~21h ago); `updatedAt` moved 2026-07-06T13:32:11Z |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump golang.org/x/image to v0.43.0 (3 advisories) | 2026-07-03 | closed silently by owner `tamnd` after 12h 50m open; no comment left, `mergedAt: null` — deps bump rejected without explanation (~4d ago, rolls off 7d closed-no-merge window 2026-07-10) |

---

GraphQL `author:aeonframework is:pr` → `issueCount: 3` (2026-07-07 run). Snapshot vs 2026-07-05 run: **material state change on 2 of 3 PRs.**

1. **HKUDS/Vibe-Trading#390** — **MERGED** at 2026-07-05T15:33:53Z (was OPEN 2d 3h with 0 activity in yesterday's snapshot). First merged PR since the tracker began recording — commit author `aeon@aeonframework.dev`. Flipped OPEN → MERGED overnight of 2026-07-05, sat unnoticed in yesterday's data because pr-tracker was blocked in the ISS-006 Monday 10:00 pocket miss. First entry in `Recent Merges` bucket ever.
2. **Panniantong/Agent-Reach#436** — still OPEN, but **first activity in 11 days** as of 2026-07-06T13:32:11Z: `comments.totalCount` went 0 → 1, `updatedAt` moved after 10 days of freeze. No review yet. Per step-3 rule (activity within 7d → not stale), reclassifies **stale → active**. Head SHA still on `security/bump-vulnerable-deps`, commit author `aeonframework@users.noreply.github.com`.
3. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). ~4 days in the closed-no-merge window; rolls off 2026-07-10.

## Categorization (today = 2026-07-07, now ≈ 11:00Z)

- **Recent merges (7d):** 1 — HKUDS/Vibe-Trading#390 (merged 2026-07-05, 2 days ago) — **first ever tracked merge**
- **Stale open (>7d, no activity 7d):** 0 — Agent-Reach#436's freeze broke yesterday
- **Active open:** 1 — Panniantong/Agent-Reach#436 (10d 15h old, fresh comment 21h ago)
- **Closed no-merge (7d):** 1 — tamnd/kage#66 (silently closed by owner, no comment; ~4d ago)

Notification: **sent** per step 5 (recent merges ≥ 1 AND active-open activity change AND closed-no-merge ≥ 1). Notify is not a redundant repeat vs 2026-07-05 — Vibe-Trading#390 flipped OPEN → MERGED and Agent-Reach#436 flipped stale → active, so [[pr-tracker-notify-repeats-with-no-state-change]] does not apply this run.

## Filter and API drift (unchanged from 2026-07-05)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in the known-list) still required for the 9th consecutive day (2026-06-29 → 2026-07-07) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path is stable this run — SKILL.md query as-written (without the `stateReason` field that older runs stripped) is fine.
