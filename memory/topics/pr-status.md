# PR Status

*Last updated: 2026-07-08*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/`. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66) AND `aeon@aeonframework.dev` (Vibe-Trading#390). Inline OR filter still required per [[pr-tracker-branch-prefix-misses-bot-identity]] — accept if branch startswith `ai/` OR commit email matches any known bot identity. All three PRs use `security/*` head branches (not `ai/*`), so the SKILL.md-documented AND filter would drop the entire queue.

## Open (1)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 11d 15h | **active** — 1 comment, last `updatedAt` 2026-07-06T13:32:11Z (~2d ago) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump golang.org/x/image to v0.43.0 (3 advisories) | 2026-07-03 | closed silently by owner `tamnd` after 12h 50m open; no comment left, `mergedAt: null` — deps bump rejected without explanation (~5d ago, rolls off 7d closed-no-merge window 2026-07-10) |

---

GraphQL `author:aeonframework is:pr` → `issueCount: 3` (2026-07-08 run). Snapshot vs 2026-07-07 run: **zero material state change on any of 3 PRs.**

1. **HKUDS/Vibe-Trading#390** — still MERGED at 2026-07-05T15:33:53Z. Same `mergedAt`, same head SHA. Now 3 days into the 7d recent-merge window (was 2 days yesterday), rolls off 2026-07-12.
2. **Panniantong/Agent-Reach#436** — still OPEN. Last activity `updatedAt` 2026-07-06T13:32:11Z (unchanged from yesterday's snapshot). Comment count still 1. Age 11d 15h. Activity was 21h ago in yesterday's log, now ~2 days ago — still inside the 7d active window, does not tip back to stale until 2026-07-13.
3. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). ~5 days in the closed-no-merge window; rolls off 2026-07-10.

## Categorization (today = 2026-07-08, now ≈ 10:00Z)

- **Recent merges (7d):** 1 — HKUDS/Vibe-Trading#390 (merged 2026-07-05, 3 days ago)
- **Stale open (>7d, no activity 7d):** 0 — Agent-Reach#436 still within active window (activity ~2d ago)
- **Active open:** 1 — Panniantong/Agent-Reach#436 (11d 15h old, activity ~2d ago)
- **Closed no-merge (7d):** 1 — tamnd/kage#66 (closed by owner, no comment; ~5d ago)

Notification: **sent** per step 5 gate (recent merges ≥ 1 AND closed-no-merge ≥ 1). SKILL.md still has no dedup guard, so this is another zero-state-change repeat vs 2026-07-07 per [[pr-tracker-notify-repeats-with-no-state-change]] — same 3 PRs, same buckets, same head SHAs, same `updatedAt`, same triggers. Notify fires because the SKILL.md-as-written gate does not check for state change.

## Filter and API drift (unchanged from 2026-07-07)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in the known-list) still required for the 10th consecutive day (2026-06-29 → 2026-07-08) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path is stable this run — SKILL.md query as-written (without the `stateReason` field that older runs stripped) is fine.
