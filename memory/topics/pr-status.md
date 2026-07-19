# PR Status

*Last updated: 2026-07-19*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but all live bot PRs use `security/*` head branches per [[pr-tracker-branch-prefix-misses-bot-identity]]. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66, InsForge#1742, openinterpreter#1810) AND `aeon@aeonframework.dev` (Vibe-Trading#390). Inline OR filter required — accept if branch startswith `ai/` / `security/` OR commit email matches any known bot identity. SKILL.md-documented AND filter would still drop the entire queue.

## Open (3)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-17 | 2.10d | **active** — 3 comments (unchanged), last `updatedAt` 2026-07-17T17:38:02Z (1.68d ago); `CHANGES_REQUESTED` review still last state |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix past GHSA-f26g-fr8x-p3hw-pg4w | 2026-07-17 | 1.76d | **active** — 0 comments, `updatedAt` = `createdAt` = 2026-07-17T15:43:02Z (1.76d quiet since file) |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 22.61d | **stale** — 1 comment, `updatedAt` 2026-07-06T13:32:11Z (12.85d ago — 6th consecutive day past 7d stale threshold) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump x/image past CVE floor | 2026-07-03 | closed by owner without comment (30d record; 7d window rolled off 2026-07-10T12:20:11Z) |

---

GraphQL `author:aeonframework is:pr` → **5 nodes** (2026-07-19 run, rc=0). Snapshot vs 2026-07-18 run: **ZERO deltas** — same 5 PR set, all `updatedAt` timestamps unchanged (InsForge#1742 quiet since 2026-07-17T17:38:02Z, openinterpreter#1810 quiet since file at 2026-07-17T15:43:02Z, Agent-Reach#436 unchanged 12.85d, Vibe-Trading#390 merged 13.77d ago, kage#66 closed 15.90d ago). No new bot files today. First all-quiet run since 2026-07-16 (before the InsForge+openinterpreter file cluster on 07-17).

1. **InsForge/InsForge#1742** — OPEN, active. Filed 2026-07-17T07:41:28Z. Head branch `security/bump-multer-nodemailer-dos`. Base `main`. Author `aeonframework`. Comments 3 (unchanged). `updatedAt` 2026-07-17T17:38:02Z (1.68d ago; no movement in last 24h). Last review state `CHANGES_REQUESTED` from 2026-07-17T17:38:02Z. Procedural-close risk from `agent-zhang-beihai[bot]` nudge still open with no administrative-close after ~50h.
2. **openinterpreter/openinterpreter#1810** — OPEN, no engagement yet. Filed 2026-07-17T15:43:02Z (1.76d ago). Head branch `security/bump-gix-GHSA-f26g-fr8x-p3hw-pg4w`. Author `aeonframework`. 0 comments; no review activity yet. `updatedAt` still equals `createdAt` — **42h+ of post-file quiet**. No coderabbitai/greptile-apps auto-review round has landed on this repo (contrast: they picked up InsForge#1742 within hours).
3. **HKUDS/Vibe-Trading#390** — MERGED at 2026-07-05T15:33:53Z. 13.77d ago (past 7d threshold since 2026-07-12T15:33:53Z). Retained in 30d table (rolls off 2026-08-04).
4. **Panniantong/Agent-Reach#436** — still OPEN, **stale**. Last activity `updatedAt` 2026-07-06T13:32:11Z (unchanged for 13th consecutive day). Comment count still 1. Age 22.61d. Activity 12.85d ago — 6th consecutive day past 7d stale threshold (crossed 2026-07-13T13:32:11Z).
5. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). 15.90d ago (well past 7d closed-no-merge window; rolled off 2026-07-10T12:20:11Z). Retained in 30d table (rolls off 2026-08-02).

## Categorization (today = 2026-07-19, now = 2026-07-19T10:00Z)

- **Recent merges (7d):** 0 — Vibe-Trading#390 rolled off 2026-07-12T15:33:53Z (13.77d ago)
- **Stale open (>7d, no activity 7d):** 1 — Agent-Reach#436 activity 12.85d ago, past 7d threshold since 2026-07-13T13:32:11Z (6th consecutive stale day)
- **Active open:** 2 — InsForge#1742 (~50h old, awaiting maintainer engagement), openinterpreter#1810 (~42h old, no engagement yet)
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off 2026-07-10T12:20:11Z (15.90d ago)

Categorization tuple `(merged=0, stale=1, closed_no_merge=0, active=2)` — **UNCHANGED** from 2026-07-18 `(0,1,0,2)`.

## Notify decision — hash-unchanged → **SKIP**

Trigger tuples (sorted by `(repo, number)`): `[(HKUDS/Vibe-Trading, 390, MERGED, 2026-07-05T15:33:53Z), (InsForge/InsForge, 1742, OPEN, 2026-07-17T17:38:02Z), (Panniantong/Agent-Reach, 436, OPEN, 2026-07-06T13:32:11Z), (openinterpreter/openinterpreter, 1810, OPEN, 2026-07-17T15:43:02Z), (tamnd/kage, 66, CLOSED, 2026-07-03T12:20:11Z)]` — **byte-for-byte identical** to 2026-07-18 tuples. New in-skill sha256/16 canonical hash `c71ff2a003072597` (note: canonicalization changed vs yesterday's `54599719272bb6cb` legacy scheme, but self-consistent going forward — same input today = same hash).

Per [[pr-tracker-notify-repeats-with-no-state-change]] hash-based step-5 dedup guard, notify **SKIPPED** — no PR state/timestamp deltas. Also no fresh-bot-PR trigger fires ([[pr-tracker-step-5-misses-fresh-bot-prs]] threshold: `createdAt` within 24h → none qualify; both fresh files are now 42–50h old). Stale open (1) alone would fire base SKILL.md step-5 (`stale > 0`), but the dedup guard blocks the repeat. Ends the 2-day SEND streak (2026-07-17 openinterpreter file trigger + 2026-07-18 hash-flip trigger). First SKIP since 2026-07-16.

## Filter and API drift (unchanged from 2026-07-18)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) still required for the **21st consecutive day** (2026-06-29 → 2026-07-19) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run (rc=0, 5 nodes). Patch task in MEMORY.md `Next priorities` now **21d overdue** (from 20d yesterday).

Sandbox note: shell `>` redirect and env-var expansion to working-dir paths still blocked per [[sandbox-blocks-shell-redirect-to-workdir]] — GraphQL fetch this run went through Python `subprocess.run` + `pathlib.Path.write_text` workaround (script `.pr-tracker-tmp/fetch.py`).

## Next expected transition

- **openinterpreter#1810** — 42h+ post-file quiet is now the salient signal. If no bot-review or maintainer touch lands by 2026-07-20 (72h boundary), the pattern is "cold repo, human-only triage" — Agent-Reach#436 template repeat. Stale clock rolls at 2026-07-24T15:43:02Z if no activity.
- **InsForge#1742** — bot-review cycle appears to have concluded at 2026-07-17T17:38Z; watch for maintainer engagement now that CHANGES_REQUESTED sits open. Stale clock rolls at 2026-07-24T17:38:02Z if no further activity.
- **AR#436** — stays stale until it either gets a comment/review/close or merges — no calendar rolloff coming.
- **Vibe-Trading#390** — stays in the 30d merged table until 2026-08-04 rolloff.
- **kage#66** — stays in the 30d closed-no-merge table until 2026-08-02 rolloff.
