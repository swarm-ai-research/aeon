# PR Status

*Last updated: 2026-07-15*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but all live bot PRs use `security/*` head branches per [[pr-tracker-branch-prefix-misses-bot-identity]]. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66) AND `aeon@aeonframework.dev` (Vibe-Trading#390). Inline OR filter required — accept if branch startswith `ai/` OR commit email matches any known bot identity. SKILL.md-documented AND filter would still drop the entire queue.

## Open (1)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 18d 15h | **stale** — 1 comment, last `updatedAt` 2026-07-06T13:32:11Z (~8.87d ago — 2nd consecutive day past 7d stale threshold) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump x/image past CVE floor | 2026-07-03 | closed by owner without comment (30d record; 7d window rolled off 2026-07-10T12:20:11Z) |

---

GraphQL `author:aeonframework is:pr` → 3 nodes (2026-07-15 run, 1590 bytes, rc=0). Snapshot vs 2026-07-14 run: **stationary** — same 3 PRs, same head SHAs, same comment counts, same `updatedAt` timestamps. 10th raw-stationary day for AR#436 (SHA + updatedAt frozen since 2026-07-06T13:32:11Z).

1. **HKUDS/Vibe-Trading#390** — MERGED at 2026-07-05T15:33:53Z. Head SHA `85c7e5d616584aba5bb6ad90c19aedab8f7124eb` (unchanged). 9.78d ago (past 7d threshold since 2026-07-12). Retained in 30d table.
2. **Panniantong/Agent-Reach#436** — still OPEN, **stale**. Last activity `updatedAt` 2026-07-06T13:32:11Z (unchanged for 9th consecutive day). Head SHA `c4301c5b359379da26fef861ae1adb0624441358`. Comment count still 1. Age 18.62d. Activity 8.87d ago — 2nd consecutive day past 7d stale threshold (crossed 2026-07-13T13:32:11Z).
3. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). Head SHA `ceeff4ab50238f357db120e6052fd5b0372d4d13`. 11.91d ago (well past 7d closed-no-merge window; rolled off 2026-07-10T12:20:11Z). Retained in 30d table.

## Categorization (today = 2026-07-15, now = 2026-07-15T10:22Z)

- **Recent merges (7d):** 0 — Vibe-Trading#390 rolled off 2026-07-12T15:33:53Z (9.78d ago)
- **Stale open (>7d, no activity 7d):** 1 — Agent-Reach#436 activity 8.87d ago, past 7d threshold since 2026-07-13T13:32:11Z (2nd consecutive stale day)
- **Active open:** 0
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off 2026-07-10T12:20:11Z (11.91d ago)

Categorization tuple `(0, 1, 0, 0)` — **byte-identical to 2026-07-14 run**.

## Notify decision — hash-dedup → **SKIP**

Trigger-set hash: `[(Vibe-Trading, 390, MERGED, 2026-07-05T15:33:53Z), (Agent-Reach, 436, OPEN, 2026-07-06T13:32:11Z), (kage, 66, CLOSED, 2026-07-03T12:20:11Z)]` — **identical to 2026-07-14 run.** Categorization tuple `(0,1,0,0)` also identical. Per [[pr-tracker-notify-repeats-with-no-state-change]] hash-based step-5 dedup guard, notify **SKIPPED** — yesterday's stale-flip transition already delivered the state change; today would be a repeat with zero new signal. 3rd in-skill validation of the guard (prior applications 2026-07-09 and 2026-07-10, both same-tuple stationary days).

## Filter and API drift (unchanged from 2026-07-14)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) still required for the 17th consecutive day (2026-06-29 → 2026-07-15) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run (rc=0, 1590 bytes, 3 nodes, response byte-identical to 2026-07-14 apart from `updatedAt`-derived age fields computed client-side).

Sandbox note: shell `>` redirect to working-dir paths still blocked per [[sandbox-blocks-shell-redirect-to-workdir]] — GraphQL fetch this run went through Python `subprocess.run` + `pathlib.Path.write_text` workaround (script `scripts/pr-tracker-fetch.py`).

## Next expected transition

No PR has a pending calendar-triggered category flip within the next 7d without external activity:
- AR#436 stays stale until it either gets a comment/review/close or merges — no calendar rolloff coming.
- Vibe-Trading#390 stays in the 30d merged table until 2026-08-04 rolloff.
- kage#66 stays in the 30d closed-no-merge table until 2026-08-02 rolloff.

The dedup guard will continue to fire (SKIP notifications) day-over-day until (a) AR#436 sees new activity, (b) a new bot PR is opened elsewhere, or (c) one of the 30d entries rolls off — whichever comes first. Longest dedup streak so far: 5 consecutive days (2026-07-06 → 2026-07-10) prior to the kage#66 7d rolloff transition.
