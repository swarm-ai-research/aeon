# PR Status

*Last updated: 2026-07-05*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/`. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66) AND `aeon@aeonframework.dev` (Vibe-Trading#390). This run continues the inline OR filter per [[pr-tracker-branch-prefix-misses-bot-identity]] — accept if branch startswith `ai/` OR commit email matches any known bot identity. All three PRs use `security/*` head branches (not `ai/*`), so the SKILL.md-documented AND filter would drop the entire queue.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2d 3h | fresh — 0 reviews / 0 comments |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 8d 16h | **stale** — 0 reviews / 0 comments; no `updatedAt` movement since open |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| _none_ | | | | |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump golang.org/x/image to v0.43.0 (3 advisories) | 2026-07-03 | closed silently by owner `tamnd` after 12h 50m open; no comment left, `mergedAt: null` — deps bump rejected without explanation (2d ago) |

---

GraphQL `author:aeonframework is:pr` → `issueCount: 3` (2026-07-05 run). Snapshot vs 2026-07-04 run: **no state churn.** All three PRs at identical head SHAs, `updatedAt` unchanged. Only movement is the wall clock — Agent-Reach#436 aged from 7d 15h → 8d 16h (still stale, no activity 8+ days) and kage#66's close event slid from 22h ago → ~47h ago (still within the 7d closed-no-merge window).

1. **HKUDS/Vibe-Trading#390** — unchanged, still OPEN 2d 3h, 0 activity, commit author `aeon@aeonframework.dev`. Third day at same head SHA / same `updatedAt`.
2. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). Second run flagging it in the closed-no-merge bucket; will roll off the 7d window on 2026-07-10.
3. **Panniantong/Agent-Reach#436** — still OPEN, still 0 activity, day-9 of silence. First PR to accumulate 8+ days stale in the tracked window.

## Categorization (today = 2026-07-05, now = 11:38Z)

- **Recent merges (7d):** 0
- **Stale open (>7d, no activity 7d):** 1 — Panniantong/Agent-Reach#436 (8d 16h, 0 activity since open)
- **Active open:** 1 — HKUDS/Vibe-Trading#390 (2d 3h, fresh)
- **Closed no-merge (7d):** 1 — tamnd/kage#66 (silently closed by owner, no comment)

Notification: **sent** per step 5 (stale ≥ 1 AND closed-no-merge ≥ 1). Second consecutive notify with zero state change vs 2026-07-04 — the current SKILL.md step-5 spec has no dedup guard, so identical triggers fire identical notifies. Worth capturing as a durable claim: [[pr-tracker-notify-repeats-with-no-state-change]].

## Filter and API drift (unchanged from 2026-07-04)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in the known-list) still required for the 7th consecutive day (2026-06-29 → 2026-07-05) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path is unaffected once `stateReason` field is dropped (not on `PullRequest` type — attempted this run, removed on second attempt; not documented in SKILL.md query).
