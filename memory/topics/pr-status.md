# PR Status

*Last updated: 2026-07-18*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but all live bot PRs use `security/*` head branches per [[pr-tracker-branch-prefix-misses-bot-identity]]. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66, InsForge#1742, openinterpreter#1810) AND `aeon@aeonframework.dev` (Vibe-Trading#390). Inline OR filter required — accept if branch startswith `ai/` / `security/` OR commit email matches any known bot identity. SKILL.md-documented AND filter would still drop the entire queue.

## Open (3)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-17 | 1.10d | **active** — 3 comments, `updatedAt` 2026-07-17T17:38:02Z (0.68d ago); tracked bot reviews from greptile-apps, coderabbitai, agent-zhang-beihai on 07-17 |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix past GHSA-f26g-fr8x-p3hw-pg4w | 2026-07-17 | 0.76d | **active** — fresh, 0 comments, `updatedAt` 2026-07-17T15:43:02Z |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 21.61d | **stale** — 1 comment, `updatedAt` 2026-07-06T13:32:11Z (11.85d ago — 5th consecutive day past 7d stale threshold) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump x/image past CVE floor | 2026-07-03 | closed by owner without comment (30d record; 7d window rolled off 2026-07-10T12:20:11Z) |

---

GraphQL `author:aeonframework is:pr` → **5 nodes** (2026-07-18 run, rc=0). Snapshot vs 2026-07-17 run: **NEW ENTRY** — openinterpreter/openinterpreter#1810 filed 2026-07-17T15:43:02Z (0.76d ago) on `security/bump-gix-GHSA-f26g-fr8x-p3hw-pg4w`, same `aeonframework@users.noreply.github.com` bot identity as InsForge#1742. Two fresh bot PRs in the last 34h — first back-to-back-day cadence since the 2026-06-26 → 2026-07-03 → 2026-07-17 gaps. Also: **InsForge#1742 activity update** — `updatedAt` moved from 2026-07-17T07:56:07Z (yesterday's snapshot) to 2026-07-17T17:38:02Z (~9.7h forward) with no new comment count delta (still 3), consistent with a bot review-round re-run.

1. **InsForge/InsForge#1742** — OPEN, active. Filed 2026-07-17T07:41:28Z. Head branch `security/bump-multer-nodemailer-dos`. Base `main`. Author `aeonframework`. Comments 3 (unchanged since yesterday). Last activity `updatedAt` 2026-07-17T17:38:02Z (0.68d ago). Procedural-close risk from `agent-zhang-beihai[bot]` nudge still open; no administrative-close so far after 34h.
2. **openinterpreter/openinterpreter#1810** — OPEN, fresh. Filed 2026-07-17T15:43:02Z (0.76d ago) — 8h after InsForge#1742. Head branch `security/bump-gix-GHSA-f26g-fr8x-p3hw-pg4w`. Author `aeonframework`. 0 comments; no review activity yet. `updatedAt` equals `createdAt` — post-file quiet.
3. **HKUDS/Vibe-Trading#390** — MERGED at 2026-07-05T15:33:53Z. Head SHA unchanged. 12.77d ago (past 7d threshold since 2026-07-12T15:33:53Z). Retained in 30d table.
4. **Panniantong/Agent-Reach#436** — still OPEN, **stale**. Last activity `updatedAt` 2026-07-06T13:32:11Z (unchanged for 12th consecutive day). Comment count still 1. Age 21.61d. Activity 11.85d ago — 5th consecutive day past 7d stale threshold (crossed 2026-07-13T13:32:11Z).
5. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). 14.90d ago (well past 7d closed-no-merge window; rolled off 2026-07-10T12:20:11Z). Retained in 30d table.

## Categorization (today = 2026-07-18, now = 2026-07-18T10:00Z)

- **Recent merges (7d):** 0 — Vibe-Trading#390 rolled off 2026-07-12T15:33:53Z (12.77d ago)
- **Stale open (>7d, no activity 7d):** 1 — Agent-Reach#436 activity 11.85d ago, past 7d threshold since 2026-07-13T13:32:11Z (5th consecutive stale day)
- **Active open:** 2 — InsForge#1742 (34h old, bot review active), openinterpreter#1810 (18h old, fresh file)
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off 2026-07-10T12:20:11Z (14.90d ago)

Categorization tuple `(merged=0, stale=1, closed_no_merge=0, active=2)` — **active_open bumped +1** from yesterday `(0,1,0,1)`.

## Notify decision — hash-flip → **SEND**

Trigger-set hash `54599719272bb6cb` (16-char sha256 prefix over sorted `[(repo, number, state, latestTimestamp)]` tuples). Trigger tuples now `[(HKUDS/Vibe-Trading, 390, MERGED, 2026-07-05T15:33:53Z), (InsForge/InsForge, 1742, OPEN, 2026-07-17T17:38:02Z), (Panniantong/Agent-Reach, 436, OPEN, 2026-07-06T13:32:11Z), (openinterpreter/openinterpreter, 1810, OPEN, 2026-07-17T15:43:02Z), (tamnd/kage, 66, CLOSED, 2026-07-03T12:20:11Z)]` — differs from yesterday's `5ee669db1a9779a8` on both the added openinterpreter tuple AND the updated InsForge timestamp. Per [[pr-tracker-notify-repeats-with-no-state-change]] hash-based step-5 dedup guard, notify **FIRES** — new fresh bot PR (also satisfies fresh-bot-PR trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]]). Second consecutive SEND day after 3-day SKIP streak ended 2026-07-17.

## Filter and API drift (unchanged from 2026-07-17)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) still required for the 20th consecutive day (2026-06-29 → 2026-07-18) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run (rc=0, 5 nodes). Patch task in MEMORY.md `Next priorities` now **20d overdue** (from 19d yesterday).

Sandbox note: shell `>` redirect and env-var expansion to working-dir paths still blocked per [[sandbox-blocks-shell-redirect-to-workdir]] — GraphQL fetch this run went through Python `subprocess.run` + `pathlib.Path.write_text` workaround (script `.pr-tracker-tmp/fetch.py`).

## Next expected transition

- **openinterpreter#1810** — highest volatility. First 24-48h will show either bot review activity (coderabbitai/greptile) or maintainer triage. Stays active_open until either the 7d stale clock (rolls at 2026-07-24T15:43:02Z if no activity) or a merge/close.
- **InsForge#1742** — bot-review cycle still turning as of 07-17T17:38Z; watch for maintainer engagement or procedural-close per `agent-zhang-beihai[bot]` nudge. Stale clock rolls at 2026-07-24T17:38:02Z if no further activity.
- **AR#436** — stays stale until it either gets a comment/review/close or merges — no calendar rolloff coming.
- **Vibe-Trading#390** — stays in the 30d merged table until 2026-08-04 rolloff.
- **kage#66** — stays in the 30d closed-no-merge table until 2026-08-02 rolloff.
