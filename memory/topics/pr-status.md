# PR Status

*Last updated: 2026-07-13*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but all live bot PRs use `security/*` head branches per [[pr-tracker-branch-prefix-misses-bot-identity]]. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66) AND `aeon@aeonframework.dev` (Vibe-Trading#390). Inline OR filter required — accept if branch startswith `ai/` OR commit email matches any known bot identity. SKILL.md-documented AND filter would still drop the entire queue.

## Open (1)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 16d 21h | **active** — 1 comment, last `updatedAt` 2026-07-06T13:32:11Z (~6.92d ago — tips stale at ~13:32Z today) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump x/image past CVE floor | 2026-07-03 | closed by owner without comment (30d record; 7d window rolled off 2026-07-10T12:20:11Z) |

---

GraphQL `author:aeonframework is:pr` → 3 nodes (2026-07-13 run). Snapshot vs 2026-07-12 run: **first state change in 8 days** — Vibe-Trading#390 crossed the 7d recent-merge threshold at 2026-07-12T15:33:53Z (~19.98h before this snapshot), so `recent_merges: 1 → 0`. 8th stationary day for Agent-Reach#436 (activity `updatedAt` frozen at 2026-07-06T13:32:11Z since 2026-07-06 — but ~2h from stale-tip at 13:32Z today if no comment lands).

1. **HKUDS/Vibe-Trading#390** — MERGED at 2026-07-05T15:33:53Z. Head SHA `85c7e5d616584aba5bb6ad90c19aedab8f7124eb` (unchanged). 7.83d ago (**past 7d threshold** — dropped out of "recent merges" bucket at 2026-07-12T15:33:53Z, ~20h before this snapshot). Retained in 30d table.
2. **Panniantong/Agent-Reach#436** — still OPEN. Last activity `updatedAt` 2026-07-06T13:32:11Z (unchanged for 7th consecutive day). Head SHA `c4301c5b359379da26fef861ae1adb0624441358`. Comment count still 1. Age 16.92d. Activity 6.92d ago — **~2h under the 7d threshold**, tips stale at 2026-07-13T13:32:11Z if no new activity. Next pr-tracker run (2026-07-14 10:00Z) will re-classify unless a comment/review lands.
3. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). Head SHA `ceeff4ab50238f357db120e6052fd5b0372d4d13`. 9.97d ago (well past the 7d closed-no-merge window; rolled off 2026-07-10T12:20:11Z). Retained in 30d table.

## Categorization (today = 2026-07-13, now = 2026-07-13T11:31:44Z)

- **Recent merges (7d):** 0 — Vibe-Trading#390 rolled off 2026-07-12T15:33:53Z (7.83d ago)
- **Stale open (>7d, no activity 7d):** 0 — Agent-Reach#436 activity 6.92d ago, still under 7d threshold by ~1.7h
- **Active open:** 1 — Panniantong/Agent-Reach#436 (16.92d old, activity 6.92d ago)
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off 2026-07-10T12:20:11Z (9.97d ago)

## Notify decision — all three trigger categories zero → **SKIP**

SKILL.md step-5 gate: "Skip notification if: zero recent merges (7d) AND zero stale open (>7d) AND zero closed-no-merge (7d)." All three are zero, so notification is skipped by the SKILL.md rule directly — no need to invoke the hash-based dedup guard from [[pr-tracker-notify-repeats-with-no-state-change]] this run.

Note: the memory-flush 2026-07-11 prediction ("2026-07-13 snapshot fires on rollover") was **partially wrong** — the rollover happened as predicted, but the rollover *reduces* trigger counts to zero rather than triggering a fresh notification. The correct read is: SKILL.md only fires on **presence** of merges / stale / closed-no-merge, not on transitions in either direction. Silent runs are the norm when the queue is quiet.

Next expected notification: (a) if Agent-Reach#436 crosses stale threshold at 2026-07-13T13:32:11Z **without** a new comment landing, tomorrow's 2026-07-14 10:00Z pr-tracker will fire (stale_open ≥ 1); or (b) if a fresh bot-PR lands per [[pr-tracker-step-5-misses-fresh-bot-prs]] (SKILL.md's current step-5 doesn't gate on fresh-bot-PR count — but the ledger notes it as a known miss).

## Filter and API drift (unchanged from 2026-07-12)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) still required for the 15th consecutive day (2026-06-29 → 2026-07-13) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run.
