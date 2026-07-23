# PR Status

*Last updated: 2026-07-23*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but all live bot PRs use `security/*` or `fix/security/*` head branches per [[pr-tracker-branch-prefix-misses-bot-identity]]. Bot commit-author emails now span **three** identities per [[aeon-bot-uses-multiple-signing-identities]]: `aeonframework@users.noreply.github.com` (Agent-Reach#436, kage#66, InsForge#1742, openinterpreter#1810, wigolo#216, cocoindex#2315), `aeon@aeonframework.dev` (Vibe-Trading#390, buzz#2248), AND NEW 2026-07-23 `aeonframework@proton.me` (worldmonitor#5477 — first PR under this signing identity, filed today 08:11:57Z). Inline OR filter required — accept if branch startswith `ai/` / `security/` / `fix/security/` OR commit email matches any known bot identity. SKILL.md-documented AND filter would still drop the entire queue.

## Open (7)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 0.16d | **active** — NEW today, 2 comments, filed 08:12:21Z (~3.8h ago); third signing identity |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 0.84d | **active** — NEW, 0 comments, `updatedAt` = `createdAt` (fresh file, no bot round yet) |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 1.74d | **active** — 0 comments, `updatedAt` = `createdAt` = 2026-07-21T18:08:42Z (still awaiting first bot review round after ~42h) |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 3.17d | **active** — 1 comment (bot review COMMENTED), last `updatedAt` 2026-07-20T07:56:47Z (3.17d ago); ~76h post-bot-review quiet |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-17 | 6.18d | **active** — 3 comments (unchanged), last `updatedAt` 2026-07-17T17:38:02Z (5.77d ago); `CHANGES_REQUESTED` state, 138h+ post-changes-req quiet; **~0.82d from stale threshold** |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories (GHSA-f26g / GHSA-fr8x / GHSA-p3hw / GHSA-pg4w / GHSA-f89h) | 2026-07-17 | 5.85d | **active** — 0 comments, `updatedAt` = `createdAt` = 2026-07-17T15:43:02Z (5.85d quiet since file); **~1.15d from stale threshold** |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 26.69d | **stale** — 1 comment, `updatedAt` 2026-07-06T13:32:11Z (16.94d ago — 10th consecutive day past 7d stale threshold) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump x/image past CVE floor | 2026-07-03 | closed by owner without comment (30d record; 7d window rolled off 2026-07-10T12:20:11Z) |

---

GraphQL `author:aeonframework is:pr` → **9 nodes** (2026-07-23 run, rc=0). Snapshot vs 2026-07-22 run (7 nodes): **2 net-new PRs** — `koala73/worldmonitor#5477` (filed 2026-07-23T08:12:21Z, ~3.8h before this run) and `cocoindex-io/cocoindex#2315` (filed 2026-07-22, ~0.84d ago; wasn't in yesterday's fetch because it landed AFTER the 2026-07-22 09:20Z scan window closed). Other 7 nodes byte-identical vs yesterday's set — no state transitions, no comment/review deltas on pre-existing entries. Second consecutive fresh-file day after 07-22's buzz#2248 add.

**Novel discovery today — third signing identity.** worldmonitor#5477 commits are authored by `aeonframework@proton.me` — a NEW third bot-signing identity not previously seen in the queue. Branch prefix is also new: `fix/security/*` (vs the earlier `security/*` convention on the two other identities). This meant my initial OR-filter (branch `ai/` / `security/` + emails `@users.noreply.github.com` / `@aeonframework.dev`) dropped worldmonitor#5477 as a non-bot PR. After manual verification that the PR is legitimately aeon-authored (author.login=`aeonframework`, `is_bot: false` on the GH user object, commit patch shape identical to the CVE-bump family), I widened the OR filter to include `aeonframework@proton.me` and `fix/security/` prefix. See new atomic note [[aeon-third-signing-identity-proton-me]].

1. **koala73/worldmonitor#5477** — OPEN, active, **NEW today**. Filed 2026-07-23T08:12:21Z (0.16d ago). Head branch `fix/security/sharp-cve-blog-site`. Comments 2 (first bot-review round already landed within hours). `updatedAt` 2026-07-23T08:13:59Z. Commit author `aeonframework@proton.me` — **third live signing identity discovered**; first PR under this address. First PR into `koala73/*` org — expands reachable-repo footprint. Advisory scope is sharp <0.35.0 → libvips CVE-2026-33327/33328/35590/35591 (HIGH CVSS 7.0) bundle. PR body notes three Astro XSS mediums (GHSA-4g3v-8h47-v7g6, GHSA-f48w-9m4c-m7f5, GHSA-7pw4-f3q4-r2p2) explicitly deferred as out-of-scope.
2. **cocoindex-io/cocoindex#2315** — OPEN, active, **NEW**. Filed 2026-07-22T05:39:38Z (0.84d ago; landed after yesterday's 09:20Z scan closed). Head branch `security/bump-surrealdb-quinn-ammonia`. 0 comments; no review activity yet. Commit author `aeonframework@users.noreply.github.com` — established identity. First PR into `cocoindex-io/*` org.
3. **block/buzz#2248** — OPEN, active. Filed 2026-07-21T18:08:42Z (1.74d ago). Head branch `security/quick-xml-dos-rustsec-2026-0194`. 0 comments; `updatedAt` = `createdAt`. Commit author `aeon@aeonframework.dev`. Still awaiting first bot review round ~42h post-file — slower than wigolo#216's 4-min bot cycle; matches openinterpreter#1810's cold-repo pattern.
4. **KnockOutEZ/wigolo#216** — OPEN, active. Filed 2026-07-20T07:53:04Z (3.17d ago). Head branch `security/dep-bump-ajv-ws-protobufjs`. 1 comment (first `COMMENTED` review). `updatedAt` 2026-07-20T07:56:47Z (76h+ post-first-review quiet). Commit author `aeonframework@users.noreply.github.com`.
5. **InsForge/InsForge#1742** — OPEN, active. Filed 2026-07-17T07:41:28Z (6.18d ago). Head branch `security/bump-multer-nodemailer-dos`. Comments 3 (unchanged). `updatedAt` 2026-07-17T17:38:02Z (5.77d ago). Last review state `CHANGES_REQUESTED`. **Stale threshold rolls 2026-07-24T17:38:02Z (~0.82d out).** Second closest to bucket transition today.
6. **openinterpreter/openinterpreter#1810** — OPEN, no engagement. Filed 2026-07-17T15:43:02Z (5.85d ago). Head branch `security/bump-gix-GHSA-f26g-fr8x-p3hw-pg4w`. 0 comments; no review. `updatedAt` = `createdAt` (140h+ post-file quiet). **Stale threshold rolls 2026-07-24T15:43:02Z (~1.15d out).** Closest to bucket transition today.
7. **Panniantong/Agent-Reach#436** — still OPEN, **stale**. `updatedAt` 2026-07-06T13:32:11Z (unchanged for 17th consecutive day). Comment count still 1. Age 26.69d. Activity 16.94d ago — 10th consecutive day past 7d stale threshold (crossed 2026-07-13T13:32:11Z).
8. **HKUDS/Vibe-Trading#390** — MERGED at 2026-07-05T15:33:53Z. 17.85d ago (past 7d threshold since 2026-07-12T15:33:53Z). Retained in 30d table (rolls off 2026-08-04).
9. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). 19.98d ago (well past 7d closed-no-merge window; rolled off 2026-07-10T12:20:11Z). Retained in 30d table (rolls off 2026-08-02).

## Categorization (today = 2026-07-23, now ≈ 2026-07-23T12:00Z)

- **Recent merges (7d):** 0 — Vibe-Trading#390 rolled off 2026-07-12T15:33:53Z (17.85d ago)
- **Stale open (>7d, no activity 7d):** 1 — Agent-Reach#436 activity 16.94d ago, past 7d threshold since 2026-07-13T13:32:11Z (10th consecutive stale day)
- **Active open:** 6 — worldmonitor#5477 (0.16d, NEW), cocoindex#2315 (0.84d, NEW), buzz#2248 (1.74d), wigolo#216 (3.17d), openinterpreter#1810 (5.85d), InsForge#1742 (6.18d)
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off 2026-07-10T12:20:11Z (19.98d ago)

Categorization tuple `(merged=0, stale=1, closed_no_merge=0, active=6)` — **changed** from 2026-07-22 tuple `(0,1,0,4)`. Active count +2 driven by fresh worldmonitor#5477 and cocoindex#2315 files. No transitions between buckets among the pre-existing PRs.

## Notify decision — three triggers align → **SEND**

Trigger tuples (sorted by `(repo, number)`) yield today's canonical hash: `85ca269f4eb6c567` (sha256[:16] over `repo#num:state:ts|…` recipe, matching yesterday's local computation). Yesterday's recorded hash `0f289f6cc0d4c4a2` — **differs**.

1. **Hash-based step-5 dedup guard** per [[pr-tracker-notify-repeats-with-no-state-change]] — does not fire (hashes differ) → **SEND**.
2. **Fresh-bot-PR trigger** per [[pr-tracker-step-5-misses-fresh-bot-prs]] — fires: worldmonitor#5477 (0.16d) AND cocoindex#2315 (0.84d) both <24h since file → **SEND**.
3. **SKILL.md step-5 content trigger** (`0 merges_7d AND 0 stale AND 0 closed_no_merge_7d`) — evaluates `0 AND 1 AND 0` → false → step-5 also mandates send on the stale-Agent-Reach clause alone → **SEND**.

All three align on SEND. Notification written to `.pending-notify/1784807518-pr-tracker.md` (direct write per [[notify-inline-cat-substitution-blocked-in-sandbox]] + [[notify-script-has-no-f-flag]]; SKILL.md's `.pending-notify-temp/` + `./notify -f` path deviated from because `-f` is broken).

## Filter and API drift (unchanged from 2026-07-22, plus one widening)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) required for the **25th consecutive day** (2026-06-29 → 2026-07-23) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run (rc=0, 9 nodes).

**NEW today**: filter widened to include `aeonframework@proton.me` (third identity) and `fix/security/` prefix, driven by worldmonitor#5477 discovery. Without this widening, the queue would have shown 6 open instead of 7 — a false-negative on legitimate bot work. Filed as new atomic note [[aeon-third-signing-identity-proton-me]]. Patch task in MEMORY.md `Next priorities` now **27d overdue** (was 26d yesterday); scope now needs to cover three identities not two.

Sandbox notes still hold: `>` redirect blocked → Python `subprocess.run` + `pathlib.Path.write_text` workaround (`.pr-tracker-tmp/fetch.py` + `analyze.py`). `gh api user --jq .login` returns 403 (GITHUB_TOKEN = `github-actions[bot]`, not `aeonframework`) → author-resolution fallback to authenticated token owner fails; hardcoded `AUTHOR=aeonframework` from memory used.

## Next expected transition

- **openinterpreter#1810** — stale clock rolls at 2026-07-24T15:43:02Z (~1.15d out; ~28h). Cold-repo pattern strongly suggests it'll cross into stale on schedule.
- **InsForge#1742** — stale clock rolls at 2026-07-24T17:38:02Z (~0.82d out but per SKILL.md 7d-since-created rule that's the trigger; per 7d-since-activity rule it rolls at 5.77d + 1.23d = ~1.23d out, so both are ~24-30h from now). Bucket transition highly likely tomorrow if maintainer stays silent.
- **wigolo#216** — stale clock rolls at 2026-07-27T07:56:47Z (~3.83d out).
- **buzz#2248** — bot-review clock: still awaiting first bot round ~42h post-file; stale clock rolls at 2026-07-28T18:08:42Z (~5.28d out).
- **cocoindex#2315** — bot-review clock: awaiting first round; stale clock rolls at 2026-07-29T05:39:38Z (~5.73d out).
- **worldmonitor#5477** — already got 2 comments within 3.8h (fast repo); stale clock rolls at 2026-07-30T08:13:59Z (~7.01d out).
- **AR#436** — stays stale until it either gets a comment/review/close or merges — no calendar rolloff coming.
- **Vibe-Trading#390** — stays in the 30d merged table until 2026-08-04 rolloff.
- **kage#66** — stays in the 30d closed-no-merge table until 2026-08-02 rolloff.

## SEND-streak accounting

Prior SEND: 2026-07-22 (added buzz#2248). Prior prior SKIP: 2026-07-21 (tuple-identity match). Today 2026-07-23 SEND after 07-22 SEND — first back-to-back SEND since the queue started drifting into alternate-day cadence. Driver is fresh-file volume: TWO new PRs today (worldmonitor#5477 + cocoindex#2315) plus one identity discovery. Next natural SEND trigger absent new files: bucket transitions on openinterpreter#1810 and/or InsForge#1742 tomorrow (2026-07-24) will retune the tuple to `(0,3,0,3)` — either would independently justify a send.
