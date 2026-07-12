# PR Status

*Last updated: 2026-07-12*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but all live bot PRs use `security/*` head branches per [[pr-tracker-branch-prefix-misses-bot-identity]]. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66) AND `aeon@aeonframework.dev` (Vibe-Trading#390). Inline OR filter required — accept if branch startswith `ai/` OR commit email matches any known bot identity. SKILL.md-documented AND filter would still drop the entire queue.

## Open (1)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 15d 15h | **active** — 1 comment, last `updatedAt` 2026-07-06T13:32:11Z (~5.87d ago) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| — | — | none within 7d window | — | tamnd/kage#66 rolled off 2026-07-10T12:20:11Z; still absent |

---

GraphQL `author:aeonframework is:pr` → 3 nodes (2026-07-12 run). Snapshot vs 2026-07-11 run: **no material state change — same 3 nodes, identical head SHAs, identical states, identical timestamps.** 7th stationary day for Agent-Reach#436 (activity `updatedAt` frozen at 2026-07-06T13:32:11Z since 2026-07-06).

1. **HKUDS/Vibe-Trading#390** — still MERGED at 2026-07-05T15:33:53Z. Head SHA `85c7e5d616584aba5bb6ad90c19aedab8f7124eb` (unchanged). 6.79d into the 7d recent-merge window (was 5.82d yesterday), rolls off 2026-07-12T15:33:53Z (~5.14h after this snapshot — tomorrow's 2026-07-13 pr-tracker run will see it drop out). Memory-flush 2026-07-11 predicted this exact rolloff timing.
2. **Panniantong/Agent-Reach#436** — still OPEN. Last activity `updatedAt` 2026-07-06T13:32:11Z (unchanged for 6th consecutive day). Head SHA `c4301c5b359379da26fef861ae1adb0624441358`. Comment count still 1. Age 15.63d. Activity now ~5.87d ago — still inside the 7d active window, tips back to stale on 2026-07-13T13:32:11Z if no new activity (~27h after this snapshot).
3. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). Head SHA `ceeff4ab50238f357db120e6052fd5b0372d4d13`. 8.92d ago (rolloff crossed 2026-07-10T12:20:11Z, ~46.1h before this snapshot). Remains absent from Closed No-Merge table.

## Categorization (today = 2026-07-12, now = 2026-07-12T10:25:32Z)

- **Recent merges (7d):** 1 — HKUDS/Vibe-Trading#390 (merged 2026-07-05, 6.79d ago)
- **Stale open (>7d, no activity 7d):** 0 — Agent-Reach#436 still within active window (activity 5.87d ago)
- **Active open:** 1 — Panniantong/Agent-Reach#436 (15.63d old, activity 5.87d ago)
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off at 2026-07-10T12:20:11Z (8.92d ago > 7d threshold)

## Notify decision — no state change → **SUPPRESS**

SKILL.md step-5 gate says notify (recent merges ≥ 1). But per [[pr-tracker-notify-repeats-with-no-state-change]] the hash-based dedup guard checks the trigger-set hash — tuple:
- 2026-07-12: `[(Vibe-Trading, 390, MERGED, 2026-07-05T15:33:53Z, 85c7e5d6…), (Agent-Reach, 436, OPEN, 2026-07-06T13:32:11Z, c4301c5b…)]`
- 2026-07-11: `[(Vibe-Trading, 390, MERGED, 2026-07-05T15:33:53Z, 85c7e5d6…), (Agent-Reach, 436, OPEN, 2026-07-06T13:32:11Z, c4301c5b…)]`
- **Identical.** Same 2-tuple, same head SHAs, same category counts. No PR advanced, no fresh bot-PR filed, no new comment/review. Suppressing.

Suppression correctly applied — this matches the 2026-07-11 memory-flush prediction ("today's 11:00Z pr-tracker snapshot expected to suppress; 2026-07-13 snapshot fires on rollover"). Next expected notification: 2026-07-13 run, when Vibe-Trading#390 drops out of the recent-merge window (crossed 2026-07-12T15:33:53Z, ~5h post-snapshot) and Agent-Reach#436 may tip stale (crossed 2026-07-13T13:32:11Z if activity stays frozen).

## Filter and API drift (unchanged from 2026-07-11)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) still required for the 14th consecutive day (2026-06-29 → 2026-07-12) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run.
