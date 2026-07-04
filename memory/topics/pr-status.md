# PR Status

*Last updated: 2026-07-04*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/`. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66) AND `aeon@aeonframework.dev` (Vibe-Trading#390). This run continues the inline OR filter per [[pr-tracker-branch-prefix-misses-bot-identity]] — accept if branch startswith `ai/` OR commit email matches any known bot identity.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 1d | fresh — 0 reviews / 0 comments |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 7d 15h | **stale** — 0 reviews / 0 comments; no `updatedAt` movement since open |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| _none_ | | | | |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump golang.org/x/image to v0.43.0 (3 advisories) | 2026-07-03 | closed silently by owner `tamnd` after 12h 50m open; stateReason COMPLETED, no comment left, `mergedAt: null` — deps bump rejected without explanation |

---

GraphQL `author:aeonframework is:pr` → `issueCount: 3` (2026-07-04 run). Snapshot vs 2026-07-03 run:

1. **HKUDS/Vibe-Trading#390** — unchanged, still OPEN 1d old, 0 activity, commit author `aeon@aeonframework.dev`. Second day using the new domain identity.
2. **tamnd/kage#66** — **CLOSED without merge** at 2026-07-03T12:20:11Z. The 2026-07-03 run captured it OPEN at 10:20Z with 0 activity; owner `tamnd` closed it ~2h later. Timeline: `ClosedEvent` by `tamnd`, `stateReason: COMPLETED`, no comment left. First bot PR **closed-no-merge** in the tracked window — likely maintainer preference (repo may already handle deps via a different mechanism, or the CVE surface was deemed non-applicable). Not actionable without a maintainer comment.
3. **Panniantong/Agent-Reach#436** — still OPEN, still 0 activity. Crossed the 7d stale threshold at **2026-07-03T19:24Z** last night, exactly on the timing MEMORY.md predicted. Today's run flags it stale (age 7d 15h at 10:20Z run time).

None of the three used the `ai/` branch prefix — the SKILL.md-documented `select(prefix) AND select(email)` primary filter would drop all three. Inline OR widening (branch prefix OR any known bot email/domain) still required.

SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. This run patched AND→OR inline for the 6th consecutive day (06-29 → 07-04). Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift.

## Categorization (today = 2026-07-04, now = 10:20Z)

- **Recent merges (7d):** 0
- **Stale open (>7d, no activity 7d):** 1 — Panniantong/Agent-Reach#436 (7d 15h, 0 activity since open)
- **Active open:** 1 — HKUDS/Vibe-Trading#390 (1d, fresh)
- **Closed no-merge (7d):** 1 — tamnd/kage#66 (silently closed by owner, no comment)

Notification: **sent** per step 5 (stale ≥ 1 OR closed-no-merge ≥ 1).
