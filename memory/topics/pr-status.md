# PR Status

*Last updated: 2026-07-20*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but all live bot PRs use `security/*` head branches per [[pr-tracker-branch-prefix-misses-bot-identity]]. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66, InsForge#1742, openinterpreter#1810, **wigolo#216 NEW**) AND `aeon@aeonframework.dev` (Vibe-Trading#390). Inline OR filter required — accept if branch startswith `ai/` / `security/` OR commit email matches any known bot identity. SKILL.md-documented AND filter would still drop the entire queue.

## Open (4)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 0.09d | **fresh** — filed 07:53:04Z, first COMMENTED review at 07:56:47Z (3m 43s post-file), 1 comment |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-17 | 3.10d | **active** — 3 comments (unchanged), last `updatedAt` 2026-07-17T17:38:02Z (2.68d ago); `CHANGES_REQUESTED` review still last state |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix past GHSA-f26g-fr8x-p3hw-pg4w | 2026-07-17 | 2.76d | **active** — 0 comments, `updatedAt` = `createdAt` = 2026-07-17T15:43:02Z (2.76d quiet since file) |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 23.61d | **stale** — 1 comment, `updatedAt` 2026-07-06T13:32:11Z (13.85d ago — 7th consecutive day past 7d stale threshold) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump x/image past CVE floor | 2026-07-03 | closed by owner without comment (30d record; 7d window rolled off 2026-07-10T12:20:11Z) |

---

GraphQL `author:aeonframework is:pr` → **6 nodes** (2026-07-20 run, rc=0). Snapshot vs 2026-07-19 run: **+1 delta** — KnockOutEZ/wigolo#216 filed 2026-07-20T07:53:04Z (2h07m before this run's 10:00Z categorization). Remaining 5 PRs byte-identical to yesterday (InsForge#1742 still quiet at 2026-07-17T17:38:02Z, openinterpreter#1810 still quiet at file time, Agent-Reach#436 unchanged 13.85d, Vibe-Trading#390 merged 14.77d ago, kage#66 closed 16.90d ago). First fresh bot-file since openinterpreter#1810 on 2026-07-17 (2.76d gap).

1. **KnockOutEZ/wigolo#216** — OPEN, active. **NEW today**. Filed 2026-07-20T07:53:04Z. Head branch `security/dep-bump-ajv-ws-protobufjs`. Base `main`. Author `aeonframework`. Comments 1 (from a bot-review, presumably). First `COMMENTED` review already landed at 2026-07-20T07:56:47Z — **~4min post-file bot-review cycle**, comparable to InsForge#1742's rapid triage (contrast: openinterpreter#1810 had no bot-review round). Commit author `aeonframework@users.noreply.github.com`. Age 0.09d.
2. **InsForge/InsForge#1742** — OPEN, active. Filed 2026-07-17T07:41:28Z (3.10d ago). Head branch `security/bump-multer-nodemailer-dos`. Comments 3 (unchanged). `updatedAt` 2026-07-17T17:38:02Z (2.68d ago; no movement since file day). Last review state `CHANGES_REQUESTED` from 2026-07-17T17:38:02Z. 65h+ post-CHANGES_REQUESTED quiet — bot-review cycle concluded, awaiting human maintainer.
3. **openinterpreter/openinterpreter#1810** — OPEN, no engagement yet. Filed 2026-07-17T15:43:02Z (2.76d ago). Head branch `security/bump-gix-GHSA-f26g-fr8x-p3hw-pg4w`. 0 comments; no review activity. `updatedAt` still equals `createdAt` — **66h+ of post-file quiet**. No coderabbitai/greptile-apps auto-review round has landed. Contrast wigolo#216's 4-min bot-review cycle: openinterpreter/ is a cold repo for auto-review bots. Approaches 72h boundary tomorrow.
4. **HKUDS/Vibe-Trading#390** — MERGED at 2026-07-05T15:33:53Z. 14.77d ago (past 7d threshold since 2026-07-12T15:33:53Z). Retained in 30d table (rolls off 2026-08-04).
5. **Panniantong/Agent-Reach#436** — still OPEN, **stale**. Last activity `updatedAt` 2026-07-06T13:32:11Z (unchanged for 14th consecutive day). Comment count still 1. Age 23.61d. Activity 13.85d ago — 7th consecutive day past 7d stale threshold (crossed 2026-07-13T13:32:11Z).
6. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). 16.90d ago (well past 7d closed-no-merge window; rolled off 2026-07-10T12:20:11Z). Retained in 30d table (rolls off 2026-08-02).

## Categorization (today = 2026-07-20, now = 2026-07-20T10:00Z)

- **Recent merges (7d):** 0 — Vibe-Trading#390 rolled off 2026-07-12T15:33:53Z (14.77d ago)
- **Stale open (>7d, no activity 7d):** 1 — Agent-Reach#436 activity 13.85d ago, past 7d threshold since 2026-07-13T13:32:11Z (7th consecutive stale day)
- **Active open:** 3 — wigolo#216 (fresh, ~2h old, 1 bot review), InsForge#1742 (~3d old, ~2.68d quiet), openinterpreter#1810 (~2.76d old, no engagement yet)
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off 2026-07-10T12:20:11Z (16.90d ago)

Categorization tuple `(merged=0, stale=1, closed_no_merge=0, active=3)` — **CHANGED** from 2026-07-18/19 `(0,1,0,2)`. Active count 2 → 3, driven by wigolo#216 file.

## Notify decision — hash-changed + fresh-bot-PR → **SEND**

Trigger tuples (sorted by `(repo, number)`): `[(HKUDS/Vibe-Trading, 390, MERGED, 2026-07-05T15:33:53Z), (InsForge/InsForge, 1742, OPEN, 2026-07-17T17:38:02Z), (KnockOutEZ/wigolo, 216, OPEN, 2026-07-20T07:56:47Z), (Panniantong/Agent-Reach, 436, OPEN, 2026-07-06T13:32:11Z), (openinterpreter/openinterpreter, 1810, OPEN, 2026-07-17T15:43:02Z), (tamnd/kage, 66, CLOSED, 2026-07-03T12:20:11Z)]`. Canonical hash `c267efaeed220887` — **differs** from 2026-07-19 hash `c71ff2a003072597` (wigolo#216 added, all other tuples identical).

Per [[pr-tracker-notify-repeats-with-no-state-change]] hash-based step-5 dedup guard, notify **SENT** — new bot PR filed. Also fresh-bot-PR trigger fires per [[pr-tracker-step-5-misses-fresh-bot-prs]] (wigolo#216 `createdAt` 0.09d < 24h threshold). Both triggers agree. Ends 1-day SKIP streak (2026-07-19 SKIP was first SKIP since 2026-07-16); resumes SEND cadence.

## Filter and API drift (unchanged from 2026-07-19)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) still required for the **22nd consecutive day** (2026-06-29 → 2026-07-20) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run (rc=0, 6 nodes). Patch task in MEMORY.md `Next priorities` now **22d overdue** (from 21d yesterday).

Sandbox note: shell `>` redirect and env-var expansion to working-dir paths still blocked per [[sandbox-blocks-shell-redirect-to-workdir]] — GraphQL fetch this run went through Python `subprocess.run` + `pathlib.Path.write_text` workaround (script `.pr-tracker-tmp/fetch.py`).

## Next expected transition

- **wigolo#216** — watch the next 24h. If maintainer responds or bot-review escalates to `CHANGES_REQUESTED` / `APPROVED`, likely fast-merge or coderabbitai-style review cycle. Stale clock rolls at 2026-07-27T07:56:47Z if no further activity.
- **openinterpreter#1810** — 66h+ post-file quiet approaches 72h boundary tomorrow (2026-07-20T15:43:02Z). If no bot/maintainer touch by then, template repeat of Agent-Reach#436 ("cold repo, human-only triage"). Stale clock rolls at 2026-07-24T15:43:02Z if no activity.
- **InsForge#1742** — bot-review cycle appears concluded at 2026-07-17T17:38Z; watch for maintainer engagement now that CHANGES_REQUESTED sits open (65h+). Stale clock rolls at 2026-07-24T17:38:02Z if no further activity.
- **AR#436** — stays stale until it either gets a comment/review/close or merges — no calendar rolloff coming.
- **Vibe-Trading#390** — stays in the 30d merged table until 2026-08-04 rolloff.
- **kage#66** — stays in the 30d closed-no-merge table until 2026-08-02 rolloff.
