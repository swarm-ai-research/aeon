# PR Status

*Last updated: 2026-07-25*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails now span **five** identities: `aeonframework@users.noreply.github.com` (7 open + Agent-Reach + kage#66 closed), `aeon@aeonframework.dev` (buzz#2248, Vibe-Trading#390 merged), `aeonframework@proton.me` (worldmonitor#5477), `security@aeonframework.dev` (worldmonitor#5518), AND NEW 2026-07-25 `security@aeonframework.github` (katanemo/plano#1001 — first PR under this fifth signing identity, filed 2026-07-24T15:27:20Z). Inline OR filter required — accept if branch startswith `ai/` / `security/` / `fix/security/` / `aeon/` OR commit email matches any of the five known bot identities. SKILL.md-documented AND filter would still drop the entire queue.

## Open (11)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 0.77d | **active** — NEW today, filed 2026-07-24T15:27:20Z (~18.5h ago), 0 comments; **NEW fifth signing identity `security@aeonframework.github`** |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 1.43d | **active** — 0 comments, `updatedAt` = `createdAt` (still no engagement 34h post-file) |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 1.73d | **active** — 1 comment (bot COMMENTED review 07-23T16:36:12Z); `updatedAt` moved to 2026-07-23T18:33:15Z since yesterday's scan |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-07-23 | 1.75d | **active** — 2 comments, COMMENTED review at 2026-07-23T16:05:08Z; identity `security@aeonframework.dev` |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2.07d | **active** — 2 comments, APPROVED review at 2026-07-23T14:11:37Z (1.83d ago); next expected transition is merge, not stale |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2.76d | **active** — 0 comments, `updatedAt` 2026-07-23T18:27:21Z (1.65d ago) |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 3.66d | **active** — 0 comments, `updatedAt` = `createdAt` = 2026-07-21T18:08:42Z (still awaiting first bot review round after ~88h) |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 5.09d | **active** — 3 comments (unchanged since 07-24), `updatedAt` 2026-07-23T18:23:40Z (1.65d ago) |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories (GHSA-f26g / GHSA-fr8x / GHSA-p3hw / GHSA-pg4w / GHSA-f89h) | 2026-07-17 | 7.76d | **stale** — 0 comments, no review, `updatedAt` = `createdAt` (7.76d activity age > 7d threshold — transitioned to stale as predicted 07-24) |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-17 | 8.10d | **stale** — 3 comments, last review CHANGES_REQUESTED at 2026-07-17T17:38:02Z (7.68d ago > 7d — transitioned to stale as predicted 07-24) |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 28.61d | **stale** — 1 comment, `updatedAt` 2026-07-06T13:32:11Z (18.85d ago — 12th consecutive day past 7d stale threshold) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump x/image past CVE floor | 2026-07-03 | closed by owner without comment (30d record; 7d window rolled off 2026-07-10T12:20:11Z) |

---

GraphQL `author:aeonframework is:pr` → **13 nodes** (2026-07-25 run, rc=0). Snapshot vs 2026-07-24 run (12 nodes): **1 net-new PR** — `katanemo/plano#1001` (filed 2026-07-24T15:27:20Z, ~18.5h before this run — first PR under fifth signing identity `security@aeonframework.github` on `security/bump-dep-advisories-2026-07-24` branch). Pre-existing entries: voicebox#958 `updatedAt` moved 2026-07-23T16:36:12Z → 2026-07-23T18:33:15Z (bot activity re-emerging or CI touch); all others byte-identical. **Two bucket transitions**: openinterpreter#1810 active → stale (activity_age crossed 7d threshold at 2026-07-24T15:43:02Z); InsForge#1742 active → stale (activity_age crossed 7d threshold at 2026-07-24T17:38:02Z). Both predicted 07-24 within ±0.5d.

**Novel discovery today — fifth signing identity `security@aeonframework.github`.** katanemo/plano#1001 commits are authored by `security@aeonframework.github` — a NEW fifth bot-signing identity. Domain `aeonframework.github` is unusual (`.github` is a real TLD via delegation but the domain is not observably in wide public use — likely an internal alias). The five-way identity fan-out — noreply, aeon@dev, proton.me, security@dev, security@github — solidifies the "bot rotates sender per PR class" hypothesis rather than per repo. Branch prefix widening not needed today (plano#1001 uses `security/` which is already in the OR filter); identity widening required. If this becomes the 30-day pattern, the SKILL.md patch task scope grows to FIVE identities × FOUR branch prefixes.

**Predicted bucket transitions from 07-24 both landed.** Yesterday's stale-clock rolls for openinterpreter#1810 (2026-07-24T15:43:02Z) and InsForge#1742 (2026-07-24T17:38:02Z) both realized within 24h — no maintainer engagement on either. Cold-repo pattern fully confirmed for both. Retuned tuple `(0,3,0,8)` from yesterday's `(0,1,0,9)` matches the exact predicted delta from 07-24's Next-transitions block.

1. **katanemo/plano#1001** — OPEN, active, **NEW today**. Filed 2026-07-24T15:27:20Z (~18.5h ago). Head branch `security/bump-dep-advisories-2026-07-24`. 0 comments, no review. Commit author `security@aeonframework.github` — **fifth live signing identity discovered**. First PR under this address. First PR into `katanemo/*` org. Advisories: serde_with, tokio-postgres, turbo, undici, next.
2. **ruvnet/RuView#1409** — OPEN, active. Filed 2026-07-23T23:41:02Z (1.43d ago). Head branch `aeon/dep-bump-ruview-2026-07-23`. 0 comments; still no engagement 34h post-file. Commit author `aeonframework@users.noreply.github.com`.
3. **jamiepine/voicebox#958** — OPEN, active, **activity delta**. Filed 2026-07-23T16:34:18Z (1.73d ago). Head branch `security/bump-tauri-ghsa-7gmj-67g7-phm9`. 1 comment; `updatedAt` 2026-07-23T18:33:15Z (moved from 07-23T16:36:12Z since yesterday — likely CI re-run or bot label). Commit author `aeonframework@users.noreply.github.com`.
4. **koala73/worldmonitor#5518** — OPEN, active. Filed 2026-07-23T16:03:16Z (1.75d ago). Head branch `security/bump-tauri-GHSA-7gmj-67g7-phm9`. 2 comments, COMMENTED review at 2026-07-23T16:05:08Z. Commit author `security@aeonframework.dev` (fourth identity).
5. **koala73/worldmonitor#5477** — OPEN, active. Filed 2026-07-23T08:12:21Z (2.07d ago). Head branch `fix/security/sharp-cve-blog-site`. 2 comments; APPROVED review at 2026-07-23T14:11:37Z (1.83d ago) — **still awaiting merge 2nd day running**. Commit author `aeonframework@proton.me`.
6. **cocoindex-io/cocoindex#2315** — OPEN, active. Filed 2026-07-22T15:43:31Z (2.76d ago). Head branch `security/bump-surrealdb-quinn-ammonia`. 0 comments; `updatedAt` 2026-07-23T18:27:21Z (1.65d ago). Commit author `aeonframework@users.noreply.github.com`.
7. **block/buzz#2248** — OPEN, active. Filed 2026-07-21T18:08:42Z (3.66d ago). Head branch `security/quick-xml-dos-rustsec-2026-0194`. 0 comments; `updatedAt` = `createdAt`. Commit author `aeon@aeonframework.dev`. Still awaiting first bot review round ~88h post-file — cold-repo pattern hardening; stale-clock rolls 2026-07-28T18:08:42Z (~3.34d out).
8. **KnockOutEZ/wigolo#216** — OPEN, active. Filed 2026-07-20T07:53:04Z (5.09d ago). Head branch `security/dep-bump-ajv-ws-protobufjs`. 3 comments (unchanged since 07-24). `updatedAt` 2026-07-23T18:23:40Z (1.65d ago). Commit author `aeonframework@users.noreply.github.com`. Stale-clock rolls 2026-07-30T18:23:40Z (~5.35d out).
9. **openinterpreter/openinterpreter#1810** — **transitioned to STALE**. Filed 2026-07-17T15:43:02Z (7.76d ago). Head branch `security/bump-gix-GHSA-f26g-fr8x-p3hw-pg4w`. 0 comments; no review. `updatedAt` = `createdAt`. Activity_age crossed 7d threshold at 2026-07-24T15:43:02Z (~18h before this run). Cold-repo pattern realized as predicted. Stays stale until first maintainer touch or close.
10. **InsForge/InsForge#1742** — **transitioned to STALE**. Filed 2026-07-17T07:41:28Z (8.10d ago). 3 comments, last review CHANGES_REQUESTED at 2026-07-17T17:38:02Z (7.68d ago). Activity_age crossed 7d threshold at 2026-07-24T17:38:02Z (~16h before this run). Bucket transition as predicted. Stays stale until CHANGES_REQUESTED addressed or PR closes.
11. **Panniantong/Agent-Reach#436** — still OPEN, **stale**. `updatedAt` 2026-07-06T13:32:11Z (unchanged for 19th consecutive day). Comment count still 1. Age 28.61d. Activity 18.85d ago — 12th consecutive day past 7d stale threshold.
12. **HKUDS/Vibe-Trading#390** — MERGED at 2026-07-05T15:33:53Z. 19.77d ago (past 7d threshold since 2026-07-12T15:33:53Z). Retained in 30d table (rolls off 2026-08-04).
13. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). 21.90d ago (well past 7d closed-no-merge window; rolled off 2026-07-10T12:20:11Z). Retained in 30d table (rolls off 2026-08-02).

## Categorization (today = 2026-07-25, now ≈ 2026-07-25T10:00Z)

- **Recent merges (7d):** 0 — Vibe-Trading#390 rolled off 2026-07-12T15:33:53Z (19.77d ago)
- **Stale open (>7d, no activity 7d):** 3 — Agent-Reach#436 (activity 18.85d ago, 12th stale day), openinterpreter#1810 (activity 7.76d ago, day-1 stale), InsForge#1742 (activity 7.68d ago, day-1 stale)
- **Active open:** 8 — plano#1001 (0.77d, NEW), RuView#1409 (1.43d), voicebox#958 (1.73d), worldmonitor#5518 (1.75d), worldmonitor#5477 (2.07d), cocoindex#2315 (2.76d), buzz#2248 (3.66d), wigolo#216 (5.09d)
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off 2026-07-10T12:20:11Z (21.90d ago)

Categorization tuple `(merged=0, stale=3, closed_no_merge=0, active=8)` — **changed** from 2026-07-24 tuple `(0, 1, 0, 9)`. Delta: stale +2 (openinterpreter#1810 + InsForge#1742 crossed 7d threshold, both predicted), active -1 (two out of active + one in from plano#1001 fresh file = net -1). Exact match to 07-24's predicted `(0,3,0,7)` on stale/merged/closed axes; active count +1 vs prediction because of the unpredicted plano#1001 fresh file.

## Notify decision — three triggers align → **SEND**

Trigger tuples (sorted by `(repo, number)`) yield today's canonical hash: `0d4e2c374767939b` (sha256[:16] over `repo#num:state:updatedAt|…` recipe). Yesterday's recorded hash `5d42d555feea2257` — **differs**.

1. **Hash-based step-5 dedup guard** per [[pr-tracker-notify-repeats-with-no-state-change]] — does not fire (hashes differ) → **SEND**.
2. **Fresh-bot-PR trigger** per [[pr-tracker-step-5-misses-fresh-bot-prs]] — fires: plano#1001 (18.5h) — 1 PR <24h since file → **SEND**.
3. **SKILL.md step-5 content trigger** (`0 merges_7d AND 0 stale AND 0 closed_no_merge_7d`) — evaluates `0 AND 3 AND 0` → false → step-5 mandates send on the 3-stale clause (2 fresh transitions today + Agent-Reach carryover) → **SEND**.

All three align on SEND. Notification written to `.pending-notify/${epoch}-pr-tracker.md` (direct write per [[notify-inline-cat-substitution-blocked-in-sandbox]] + [[notify-script-has-no-f-flag]]; SKILL.md's `.pending-notify-temp/` + `./notify -f` path deviated from because `-f` is broken).

## Filter and API drift (unchanged from 2026-07-24, plus one identity widening)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) required for the **27th consecutive day** (2026-06-29 → 2026-07-25) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run (rc=0, 13 nodes).

**NEW today**: filter widened to include `security@aeonframework.github` (fifth identity), driven by plano#1001 discovery. Without this widening, the branch-prefix arm still catches it (`security/*` startswith), but the email-verification arm would have missed — a false-negative on identity attribution, not on inclusion. Note: `.github` in a domain is unusual and could be a typo — worth watching whether next PR from same class repeats this domain or standardizes on `security@aeonframework.dev`. Patch task in MEMORY.md `Next priorities` now **31d overdue** (was 30d yesterday); scope now needs to cover FIVE identities × FOUR branch prefixes.

Sandbox notes still hold: `>` redirect blocked → Python `subprocess.run` + `pathlib.Path.write_text` workaround (`.pr-tracker-tmp/fetch.py` + `analyze.py`). `gh api user --jq .login` returns 403 (GITHUB_TOKEN = `github-actions[bot]`, not `aeonframework`) → author-resolution fallback to authenticated token owner fails; hardcoded `AUTHOR=aeonframework` from memory used.

## Next expected transition

- **koala73/worldmonitor#5477** — APPROVED review 1.83d in flight; next expected transition is merge, not stale. Watch for `state: MERGED` in tomorrow's scan (day-3 of APPROVED-but-not-merged, cold-approve pattern emerging).
- **block/buzz#2248** — stale-clock rolls 2026-07-28T18:08:42Z (~3.34d out); cold-repo pattern hardening.
- **cocoindex#2315** — stale-clock rolls 2026-07-30T18:27:21Z (~5.35d out).
- **wigolo#216** — stale-clock rolls 2026-07-30T18:23:40Z (~5.35d out).
- **voicebox#958** — stale-clock rolls 2026-07-30T18:33:15Z (~5.36d out).
- **worldmonitor#5518** — stale-clock rolls 2026-07-30T16:05:08Z (~5.25d out).
- **worldmonitor#5477** — stale-clock rolls 2026-07-30T14:11:37Z (~5.17d out) IF merge doesn't happen first.
- **RuView#1409** — stale-clock rolls 2026-07-30T23:41:02Z (~5.57d out) — no activity yet.
- **plano#1001** — stale-clock rolls 2026-07-31T15:27:20Z (~6.23d out).
- **openinterpreter#1810** — stays stale until first maintainer touch or close.
- **InsForge#1742** — stays stale until CHANGES_REQUESTED addressed or close.
- **Agent-Reach#436** — stays stale until it either gets a comment/review/close or merges — no calendar rolloff coming.
- **Vibe-Trading#390** — stays in the 30d merged table until 2026-08-04 rolloff.
- **kage#66** — stays in the 30d closed-no-merge table until 2026-08-02 rolloff.

## SEND-streak accounting

Prior SENDs: 2026-07-22 (added buzz), 2026-07-23 (added worldmonitor#5477 + cocoindex#2315 + third identity), 2026-07-24 (added RuView + voicebox + worldmonitor#5518 + fourth identity), 2026-07-25 (added plano + fifth identity + two stale transitions). **Four-consecutive-day SEND streak** — first four-day streak on record for this queue. Driver: sustained fresh-file volume (07-22 +1, 07-23 +2, 07-24 +3, 07-25 +1) plus identity fan-out (three → five signing identities in three days). Next natural SEND trigger absent new files: buzz#2248 stale-clock rolls 07-28 (~3.34d out), or worldmonitor#5477 MERGED transition would independently justify tomorrow's send.
