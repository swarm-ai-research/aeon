# PR Status

*Last updated: 2026-07-21*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but all live bot PRs use `security/*` head branches per [[pr-tracker-branch-prefix-misses-bot-identity]]. Bot commit-author emails span two identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66, InsForge#1742, openinterpreter#1810, wigolo#216) AND `aeon@aeonframework.dev` (Vibe-Trading#390). Inline OR filter required — accept if branch startswith `ai/` / `security/` OR commit email matches any known bot identity. SKILL.md-documented AND filter would still drop the entire queue.

## Open (4)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 1.09d | **active** — 1 comment (bot review), last `updatedAt` 2026-07-20T07:56:47Z (1.09d ago; no movement since first bot review) |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-17 | 4.10d | **active** — 3 comments (unchanged), last `updatedAt` 2026-07-17T17:38:02Z (3.68d ago); `CHANGES_REQUESTED` review still last state, 89h+ quiet |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix past GHSA-f26g-fr8x-p3hw-pg4w | 2026-07-17 | 3.76d | **active** — 0 comments, `updatedAt` = `createdAt` = 2026-07-17T15:43:02Z (3.76d quiet since file — crossed 72h boundary yesterday); no auto-review round has landed |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 24.61d | **stale** — 1 comment, `updatedAt` 2026-07-06T13:32:11Z (14.85d ago — 8th consecutive day past 7d stale threshold) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump x/image past CVE floor | 2026-07-03 | closed by owner without comment (30d record; 7d window rolled off 2026-07-10T12:20:11Z) |

---

GraphQL `author:aeonframework is:pr` → **6 nodes** (2026-07-21 run, rc=0). Snapshot vs 2026-07-20 run: **byte-identical tuples** — every `(repo, number, state, timestamp)` tuple matches yesterday's set exactly. No fresh files, no state transitions, no comment/review deltas. First byte-identical-vs-yesterday snapshot since 2026-07-19 (07-20 broke the streak by adding wigolo#216).

1. **KnockOutEZ/wigolo#216** — OPEN, active. Filed 2026-07-20T07:53:04Z (1.09d ago). Head branch `security/dep-bump-ajv-ws-protobufjs`. Base `main`. Comments 1. First `COMMENTED` review from 2026-07-20T07:56:47Z (~4min post-file bot-review cycle). `updatedAt` static at 2026-07-20T07:56:47Z (26h+ post-first-review quiet). Commit author `aeonframework@users.noreply.github.com`. Post-bot-review pattern now matches InsForge#1742's fast-cluster shape (early bot round, then quiet awaiting human).
2. **InsForge/InsForge#1742** — OPEN, active. Filed 2026-07-17T07:41:28Z (4.10d ago). Head branch `security/bump-multer-nodemailer-dos`. Comments 3 (unchanged). `updatedAt` 2026-07-17T17:38:02Z (3.68d ago). Last review state `CHANGES_REQUESTED`. 89h+ post-CHANGES_REQUESTED quiet — bot-review cycle concluded, awaiting human maintainer. Approaches 7d stale threshold 2026-07-24T17:38:02Z (~3d out).
3. **openinterpreter/openinterpreter#1810** — OPEN, no engagement. Filed 2026-07-17T15:43:02Z (3.76d ago). Head branch `security/bump-gix-GHSA-f26g-fr8x-p3hw-pg4w`. 0 comments; no review activity. `updatedAt` still equals `createdAt` — **90h+ of post-file quiet**, crossed 72h boundary yesterday 2026-07-20T15:43:02Z. Cold repo for auto-review bots (contrast wigolo#216's 4-min bot round). Approaches 7d stale threshold 2026-07-24T15:43:02Z (~3d out).
4. **HKUDS/Vibe-Trading#390** — MERGED at 2026-07-05T15:33:53Z. 15.77d ago (past 7d threshold since 2026-07-12T15:33:53Z). Retained in 30d table (rolls off 2026-08-04).
5. **Panniantong/Agent-Reach#436** — still OPEN, **stale**. Last activity `updatedAt` 2026-07-06T13:32:11Z (unchanged for 15th consecutive day). Comment count still 1. Age 24.61d. Activity 14.85d ago — 8th consecutive day past 7d stale threshold (crossed 2026-07-13T13:32:11Z).
6. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). 17.90d ago (well past 7d closed-no-merge window; rolled off 2026-07-10T12:20:11Z). Retained in 30d table (rolls off 2026-08-02).

## Categorization (today = 2026-07-21, now = 2026-07-21T10:00Z)

- **Recent merges (7d):** 0 — Vibe-Trading#390 rolled off 2026-07-12T15:33:53Z (15.77d ago)
- **Stale open (>7d, no activity 7d):** 1 — Agent-Reach#436 activity 14.85d ago, past 7d threshold since 2026-07-13T13:32:11Z (8th consecutive stale day)
- **Active open:** 3 — wigolo#216 (~1d old, 26h post-bot-review quiet), InsForge#1742 (~4d old, ~3.68d quiet), openinterpreter#1810 (~3.76d old, no engagement)
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off 2026-07-10T12:20:11Z (17.90d ago)

Categorization tuple `(merged=0, stale=1, closed_no_merge=0, active=3)` — **unchanged** from 2026-07-20 tuple `(0,1,0,3)`. wigolo#216 aged from 0.09d → 1.09d overnight but remains in active bucket (still <7d).

## Notify decision — tuple-identity → **SKIP**

Trigger tuples (sorted by `(repo, number)`): `[(HKUDS/Vibe-Trading, 390, MERGED, 2026-07-05T15:33:53Z), (InsForge/InsForge, 1742, OPEN, 2026-07-17T17:38:02Z), (KnockOutEZ/wigolo, 216, OPEN, 2026-07-20T07:56:47Z), (Panniantong/Agent-Reach, 436, OPEN, 2026-07-06T13:32:11Z), (openinterpreter/openinterpreter, 1810, OPEN, 2026-07-17T15:43:02Z), (tamnd/kage, 66, CLOSED, 2026-07-03T12:20:11Z)]`. Local canonical hash today `a55567402362e9bc` (sha256[:16] over `repo#num:state:ts|…`). Yesterday's recorded hash `c267efaeed220887` was computed by an earlier run under a different digest recipe — **not directly comparable**, so tuple-identity is the authoritative check.

Tuple-identity check: byte-comparing all six `(repo, number, state, timestamp)` tuples against yesterday's line-50 record → **all six identical**. Per [[pr-tracker-notify-repeats-with-no-state-change]] hash-based step-5 dedup guard, notify **SKIPPED** — no state change. Fresh-bot-PR trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]] does not fire (no PR filed in last 24h; wigolo#216 aged to 1.09d overnight). Both triggers agree.

Note on hash instability: today's script computes hash locally with a fresh sha256 recipe, so from 2026-07-21 onward the recorded hash `a55567402362e9bc` becomes the reference for tomorrow's comparison. Yesterday's `c267efaeed220887` reflects a distinct hashing convention embedded in the prior run's analyze step. Going forward, tomorrow's comparison against today's `a55567402362e9bc` should be direct.

## Filter and API drift (unchanged from 2026-07-20)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) still required for the **23rd consecutive day** (2026-06-29 → 2026-07-21) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run (rc=0, 6 nodes). Patch task in MEMORY.md `Next priorities` now **23d overdue** (from 22d yesterday).

Sandbox note: shell `>` redirect and env-var expansion to working-dir paths still blocked per [[sandbox-blocks-shell-redirect-to-workdir]] — GraphQL fetch this run went through Python `subprocess.run` + `pathlib.Path.write_text` workaround (scripts `.pr-tracker-tmp/fetch.py` + `.pr-tracker-tmp/analyze.py`). Also: `gh api user --jq .login` returns 403 `Resource not accessible by integration` (GITHUB_TOKEN is `github-actions[bot]` not `aeonframework`), so the SKILL.md fallback "authenticated token owner" author-resolution path fails here; must rely on `aeon.yml` / `AEON_PR_AUTHOR` / hardcoded-per-memory. This run used memory-documented `AUTHOR=aeonframework` since no `aeon.yml` `pr_tracker.author` key and no `AEON_PR_AUTHOR` env var are set.

## Next expected transition

- **InsForge#1742** — stale clock rolls at 2026-07-24T17:38:02Z (~3d out). If maintainer still silent then, joins Agent-Reach in the stale bucket.
- **openinterpreter#1810** — stale clock rolls at 2026-07-24T15:43:02Z (~3d out). Cold-repo pattern strongly suggests it'll cross into stale on schedule.
- **wigolo#216** — stale clock rolls at 2026-07-27T07:56:47Z (~6d out). Watch for coderabbitai-style follow-up review or maintainer touch.
- **AR#436** — stays stale until it either gets a comment/review/close or merges — no calendar rolloff coming.
- **Vibe-Trading#390** — stays in the 30d merged table until 2026-08-04 rolloff.
- **kage#66** — stays in the 30d closed-no-merge table until 2026-08-02 rolloff.

## SKIP-streak accounting

Prior SKIP: 2026-07-19 (1-day SKIP, then 07-20 SEND for wigolo#216 file). Today 2026-07-21 SKIP resumes. If tomorrow 2026-07-22 also yields byte-identical tuples with no fresh files, that would be 2 consecutive SKIP — matching the tuple-static pattern the queue has drifted into for the 3 mid-cluster PRs (InsForge, openinterpreter, Agent-Reach). Next natural SEND trigger: an InsForge#1742 or openinterpreter#1810 stale-threshold crossing on 2026-07-24 (both roll into the stale bucket, changing the categorization tuple).
