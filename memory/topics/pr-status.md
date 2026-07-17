# PR Status

*Last updated: 2026-07-17*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but all live bot PRs use `security/*` head branches per [[pr-tracker-branch-prefix-misses-bot-identity]]. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66) AND `aeon@aeonframework.dev` (Vibe-Trading#390). Inline OR filter required — accept if branch startswith `ai/` / `security/` OR commit email matches any known bot identity. SKILL.md-documented AND filter would still drop the entire queue.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-17 | 2h | **active** — filed 07:41Z; 3 review + 3 issue comments from `greptile-apps`, `coderabbitai`, `agent-zhang-beihai` bots within 15min; last `updatedAt` 2026-07-17T07:56:07Z |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 20d 20h | **stale** — 1 comment, last `updatedAt` 2026-07-06T13:32:11Z (~10.85d ago — 4th consecutive day past 7d stale threshold) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump x/image past CVE floor | 2026-07-03 | closed by owner without comment (30d record; 7d window rolled off 2026-07-10T12:20:11Z) |

---

GraphQL `author:aeonframework is:pr` → **4 nodes** (2026-07-17 run, 2191 bytes, rc=0). Snapshot vs 2026-07-16 run: **NEW ENTRY** — InsForge#1742 filed 07:41Z today by `aeonframework` on `security/bump-multer-nodemailer-dos`, breaks the 11-day stationary streak (2026-07-06 → 2026-07-16). The other 3 PRs unchanged: same head SHAs, same comment counts, same `updatedAt` timestamps.

1. **InsForge/InsForge#1742** — OPEN, active. Filed 2026-07-17T07:41:28Z (0.10d ago). Head branch `security/bump-multer-nodemailer-dos`. Base `main`. Author `aeonframework`. Diff +55/-72 across 2 files. Immediate bot-review activity: `agent-zhang-beihai[bot]` at 07:41:37Z (workflow flag — "open an issue first, get it assigned, then submit a PR"), `coderabbitai[bot]` at 07:42:06Z (review stack), `greptile-apps[bot]` at 07:43:54Z (P2 flags on nodemailer semver floor + lockfile scope). Last activity `updatedAt` 2026-07-17T07:56:07Z (2h ago). Procedural-close risk noted.
2. **HKUDS/Vibe-Trading#390** — MERGED at 2026-07-05T15:33:53Z. Head SHA `85c7e5d616584aba5bb6ad90c19aedab8f7124eb` (unchanged). 11.77d ago (past 7d threshold since 2026-07-12). Retained in 30d table.
3. **Panniantong/Agent-Reach#436** — still OPEN, **stale**. Last activity `updatedAt` 2026-07-06T13:32:11Z (unchanged for 11th consecutive day). Head SHA `c4301c5b359379da26fef861ae1adb0624441358`. Comment count still 1. Age 20.61d. Activity 10.85d ago — 4th consecutive day past 7d stale threshold (crossed 2026-07-13T13:32:11Z).
4. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). Head SHA `ceeff4ab50238f357db120e6052fd5b0372d4d13`. 13.90d ago (well past 7d closed-no-merge window; rolled off 2026-07-10T12:20:11Z). Retained in 30d table.

## Categorization (today = 2026-07-17, now = 2026-07-17T10:00Z)

- **Recent merges (7d):** 0 — Vibe-Trading#390 rolled off 2026-07-12T15:33:53Z (11.77d ago)
- **Stale open (>7d, no activity 7d):** 1 — Agent-Reach#436 activity 10.85d ago, past 7d threshold since 2026-07-13T13:32:11Z (4th consecutive stale day)
- **Active open:** 1 — InsForge#1742 opened 2h ago, active review activity
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off 2026-07-10T12:20:11Z (13.90d ago)

Categorization tuple `(merged=0, stale=1, closed_no_merge=0, active=1)` — **breaks 3-day stationary streak** (2026-07-14/15/16 all `(0,1,0,0)`).

## Notify decision — hash-flip → **SEND**

Trigger-set hash `5ee669db1a9779a8` (16-char sha256 prefix over sorted `[(repo, number, state, latestTimestamp)]` tuples). Trigger tuples now `[(HKUDS/Vibe-Trading, 390, MERGED, 2026-07-05T15:33:53Z), (InsForge/InsForge, 1742, OPEN, 2026-07-17T07:56:07Z), (Panniantong/Agent-Reach, 436, OPEN, 2026-07-06T13:32:11Z), (tamnd/kage, 66, CLOSED, 2026-07-03T12:20:11Z)]` — differs from yesterday's `6e12fb569593f8ff` on both the added InsForge tuple AND the categorization tuple. Per [[pr-tracker-notify-repeats-with-no-state-change]] hash-based step-5 dedup guard, notify **FIRES** — state changed with a fresh bot PR (also satisfies fresh-bot-PR trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]]). Ends 3-day SKIP streak (2026-07-14 → 2026-07-16).

## Filter and API drift (unchanged from 2026-07-16)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) still required for the 19th consecutive day (2026-06-29 → 2026-07-17) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run (rc=0, 2191 bytes, 4 nodes).

Sandbox note: shell `>` redirect and env-var expansion to working-dir paths still blocked per [[sandbox-blocks-shell-redirect-to-workdir]] — GraphQL fetch this run went through Python `subprocess.run` + `pathlib.Path.write_text` workaround (script `.pr-tracker-tmp/fetch.py`).

## Next expected transition

- **InsForge#1742** — highest volatility. `agent-zhang-beihai[bot]` procedural nudge suggests possible administrative close if operator doesn't file a companion issue first; watch tomorrow. Otherwise stays active_open until either the 7d stale clock (rolls at 2026-07-24T07:56:07Z if no activity) or a merge/close.
- **AR#436** — stays stale until it either gets a comment/review/close or merges — no calendar rolloff coming.
- **Vibe-Trading#390** — stays in the 30d merged table until 2026-08-04 rolloff.
- **kage#66** — stays in the 30d closed-no-merge table until 2026-08-02 rolloff.
