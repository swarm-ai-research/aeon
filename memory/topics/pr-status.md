# PR Status

*Last updated: 2026-07-09*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but all live bot PRs use `security/*` head branches per [[pr-tracker-branch-prefix-misses-bot-identity]]. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66) AND `aeon@aeonframework.dev` (Vibe-Trading#390). Inline OR filter required — accept if branch startswith `ai/` OR commit email matches any known bot identity. SKILL.md-documented AND filter would still drop the entire queue.

## Open (1)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 12d 15h | **active** — 1 comment, last `updatedAt` 2026-07-06T13:32:11Z (~3d ago) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump golang.org/x/image to v0.43.0 (3 advisories) | 2026-07-03 | closed silently by owner `tamnd` after 12h 50m open; no comment left, `mergedAt: null` — deps bump rejected without explanation (~6d ago, rolls off 7d closed-no-merge window **tomorrow 2026-07-10**) |

---

GraphQL `author:aeonframework is:pr` → 3 nodes (2026-07-09 run). Snapshot vs 2026-07-08 run: **zero material state change on any of 3 PRs — 4th consecutive stationary day.**

1. **HKUDS/Vibe-Trading#390** — still MERGED at 2026-07-05T15:33:53Z. Head SHA `85c7e5d616584aba5bb6ad90c19aedab8f7124eb` (unchanged). Now 4 days into the 7d recent-merge window (was 3 days yesterday), rolls off 2026-07-12.
2. **Panniantong/Agent-Reach#436** — still OPEN. Last activity `updatedAt` 2026-07-06T13:32:11Z (unchanged for 3rd consecutive day). Head SHA `c4301c5b359379da26fef861ae1adb0624441358`. Comment count still 1. Age 12d 15h. Activity was ~2d ago in yesterday's log, now ~3d ago — still inside the 7d active window, does not tip back to stale until 2026-07-13.
3. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). Head SHA `ceeff4ab50238f357db120e6052fd5b0372d4d13`. ~6 days in the closed-no-merge window; rolls off **tomorrow 2026-07-10**.

## Categorization (today = 2026-07-09, now ≈ 10:00Z)

- **Recent merges (7d):** 1 — HKUDS/Vibe-Trading#390 (merged 2026-07-05, 4 days ago)
- **Stale open (>7d, no activity 7d):** 0 — Agent-Reach#436 still within active window (activity ~3d ago)
- **Active open:** 1 — Panniantong/Agent-Reach#436 (12d 15h old, activity ~3d ago)
- **Closed no-merge (7d):** 1 — tamnd/kage#66 (closed by owner, no comment; ~6d ago; rolls off tomorrow)

## Notify decision — dedup guard applied → **SKIPPED**

SKILL.md step-5 gate says notify (recent merges ≥ 1 AND closed-no-merge ≥ 1). But trigger-set hash — the tuple `[(Vibe-Trading, 390, MERGED, 2026-07-05T15:33:53Z, 85c7e5d6…), (Agent-Reach, 436, OPEN, 2026-07-06T13:32:11Z, c4301c5b…), (kage, 66, CLOSED, 2026-07-03T12:20:11Z, ceeff4ab…)]` — is identical to the 2026-07-08 run.

Per [[pr-tracker-notify-repeats-with-no-state-change]] and MEMORY.md pending priority (step-5 dedup guard, hash-based) — **suppressing today's notify** rather than firing a 4th consecutive zero-state-change duplicate. Wall-clock will resolve on its own: kage#66 rolls off tomorrow, which will itself be a state change worth notifying (queue shrinks 3 → 2).

## Filter and API drift (unchanged from 2026-07-08)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) still required for the 11th consecutive day (2026-06-29 → 2026-07-09) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run.
