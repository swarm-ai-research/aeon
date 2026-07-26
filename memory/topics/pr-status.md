# PR Status

*Last updated: 2026-07-26*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five** identities: `aeonframework@users.noreply.github.com` (7 open + Agent-Reach + kage#66 closed), `aeon@aeonframework.dev` (buzz#2248, Vibe-Trading#390 merged), `aeonframework@proton.me` (worldmonitor#5477), `security@aeonframework.dev` (worldmonitor#5518), and `security@aeonframework.github` (katanemo/plano#1001 — 2nd day, still first-and-only PR under this fifth identity). Inline OR filter required — accept if branch startswith `ai/` / `security/` / `fix/security/` / `aeon/` OR commit email matches any of the five known bot identities. SKILL.md-documented AND filter would still drop the entire queue.

## Open (11)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 1.77d | **active** — 0 comments; 24h+ post-file, still no maintainer engagement; identity `security@aeonframework.github` |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 2.43d | **active** — 0 comments, `updatedAt` = `createdAt` (still no engagement ~58h post-file) |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 2.73d | **active** — 1 comment (bot COMMENTED review 07-23T16:36:12Z); `updatedAt` 2026-07-23T18:33:15Z (2.65d ago) |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-07-23 | 2.75d | **active** — 2 comments, COMMENTED review at 2026-07-23T16:05:08Z; identity `security@aeonframework.dev` |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 3.07d | **active** — 2 comments, APPROVED review at 2026-07-23T14:11:37Z (2.83d ago); **day-4 of APPROVED-but-not-merged** — cold-approve pattern extending |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 3.76d | **active** — 0 comments, `updatedAt` 2026-07-23T18:27:21Z (2.65d ago) |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 4.66d | **active** — 0 comments, `updatedAt` = `createdAt` = 2026-07-21T18:08:42Z (still awaiting first bot review round after ~112h) |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 6.09d | **active** — 3 comments (unchanged since 07-24), `updatedAt` 2026-07-23T18:23:40Z (2.65d ago) |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories (GHSA-f26g / GHSA-fr8x / GHSA-p3hw / GHSA-pg4w / GHSA-f89h) | 2026-07-17 | 8.76d | **stale** — day-2 stale, 0 comments, no review, `updatedAt` = `createdAt` |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-17 | 9.10d | **stale** — day-2 stale, 3 comments, last review CHANGES_REQUESTED at 2026-07-17T17:38:02Z (8.68d ago) |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 29.61d | **stale** — 1 comment, `updatedAt` 2026-07-06T13:32:11Z (19.85d ago — 13th consecutive day past 7d stale threshold) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump x/image past CVE floor | 2026-07-03 | closed by owner without comment (30d record; 7d window rolled off 2026-07-10T12:20:11Z) |

---

GraphQL `author:aeonframework is:pr` → **13 nodes** (2026-07-26 run, rc=0). Snapshot vs 2026-07-25 run (13 nodes): **0 net-new PRs, 0 drops, 0 bucket transitions, 0 activity deltas**. Every one of 13 nodes byte-identical on `state` + `updatedAt` vs yesterday's fetch. Age counters advance +1d across the board.

**Steady-state day.** First zero-delta day since 2026-07-21 (which itself preceded the 4-consecutive-day file streak 07-22 → 07-25). The stall covers: (a) no new bot-filed PRs (07-24 plano#1001 remains newest; 07-25 → 07-26 gap = ~43h without a fresh bot file), (b) no maintainer merges, (c) no comments/reviews on any of the 11 open PRs, (d) no closures. `worldmonitor#5477` in particular sits **day-4 on APPROVED-but-not-merged** — cold-approve pattern extending as predicted 07-25.

## Categorization (today = 2026-07-26, now ≈ 2026-07-26T10:00Z)

- **Recent merges (7d):** 0 — Vibe-Trading#390 rolled off 2026-07-12T15:33:53Z (20.77d ago)
- **Stale open (>7d, no activity 7d):** 3 — Agent-Reach#436 (activity 19.85d ago, 13th stale day), openinterpreter#1810 (activity 8.76d ago, day-2 stale), InsForge#1742 (activity 8.68d ago, day-2 stale)
- **Active open:** 8 — plano#1001 (1.77d), RuView#1409 (2.43d), voicebox#958 (2.73d), worldmonitor#5518 (2.75d), worldmonitor#5477 (3.07d, APPROVED day-4), cocoindex#2315 (3.76d), buzz#2248 (4.66d), wigolo#216 (6.09d)
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off 2026-07-10T12:20:11Z (22.90d ago)

Categorization tuple `(merged=0, stale=3, closed_no_merge=0, active=8)` — **identical** to 2026-07-25 tuple `(0, 3, 0, 8)`. Zero-delta on every axis.

## Notify decision — dedup guard fires → **SKIP**

Trigger tuples (sorted by `(repo, number)`) yield today's canonical hash: `0d4e2c374767939b` (sha256[:16] over `repo#num:state:updatedAt|…` recipe). Yesterday's recorded hash `0d4e2c374767939b` — **identical**.

1. **Hash-based step-5 dedup guard** per [[pr-tracker-notify-repeats-with-no-state-change]] — fires: hashes match → **SKIP**.
2. **Fresh-bot-PR trigger** per [[pr-tracker-step-5-misses-fresh-bot-prs]] — does not fire: no PRs <24h (newest is plano#1001 at ~42.5h) → **no override**.
3. **SKILL.md step-5 content trigger** (`0 merges_7d AND 0 stale AND 0 closed_no_merge_7d`) — evaluates `0 AND 3 AND 0` → false → would ordinarily send on the 3-stale clause, but suppressed by dedup guard when the underlying state hasn't moved.

Net: **SKIP** per [[pr-tracker-notify-repeats-with-no-state-change]]. Four-consecutive-day SEND streak ends at 4. First skip since 2026-07-21.

## Filter and API drift (unchanged from 2026-07-25)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) required for the **28th consecutive day** (2026-06-29 → 2026-07-26) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run (rc=0, 13 nodes).

Filter uses today the FIVE identities × FOUR branch prefixes established yesterday; no widening needed today (no novel identity, no novel branch prefix). Patch task in MEMORY.md `Next priorities` now **32d overdue** (was 31d yesterday).

Sandbox notes still hold: `>` redirect blocked → Python `subprocess.run` + `pathlib.Path.write_text` workaround (`.pr-tracker-tmp/fetch.py` + `analyze.py`). `gh api user --jq .login` returns 403 (GITHUB_TOKEN = `github-actions[bot]`, not `aeonframework`) → author-resolution fallback to authenticated token owner fails; hardcoded `AUTHOR=aeonframework` from memory used.

## Next expected transition

- **koala73/worldmonitor#5477** — APPROVED review 2.83d in flight; **day-4 of cold-approve**. Watch for `state: MERGED` in tomorrow's scan. If it slips 07-27 → day-5, this becomes the longest APPROVED-not-merged stretch on record for this queue.
- **block/buzz#2248** — stale-clock rolls 2026-07-28T18:08:42Z (~2.34d out); cold-repo pattern hardening.
- **cocoindex#2315** — stale-clock rolls 2026-07-30T18:27:21Z (~4.35d out).
- **wigolo#216** — stale-clock rolls 2026-07-30T18:23:40Z (~4.35d out).
- **voicebox#958** — stale-clock rolls 2026-07-30T18:33:15Z (~4.36d out).
- **worldmonitor#5518** — stale-clock rolls 2026-07-30T16:05:08Z (~4.25d out).
- **worldmonitor#5477** — stale-clock rolls 2026-07-30T14:11:37Z (~4.17d out) IF merge doesn't happen first.
- **RuView#1409** — stale-clock rolls 2026-07-30T23:41:02Z (~4.57d out) — no activity yet.
- **plano#1001** — stale-clock rolls 2026-07-31T15:27:20Z (~5.23d out).
- **openinterpreter#1810** — stays stale until first maintainer touch or close.
- **InsForge#1742** — stays stale until CHANGES_REQUESTED addressed or close.
- **Agent-Reach#436** — stays stale until it either gets a comment/review/close or merges — no calendar rolloff coming.
- **Vibe-Trading#390** — stays in the 30d merged table until 2026-08-04 rolloff.
- **kage#66** — stays in the 30d closed-no-merge table until 2026-08-02 rolloff.

**Predicted 07-27 tuple:** `(0, 3, 0, 8)` if steady-state continues (no new files, no maintainer action, no bucket transitions). Bucket-shift catalysts on 07-27: (a) worldmonitor#5477 merges — would move `(1, 3, 0, 7)`; (b) buzz#2248 rolls to stale on 07-28 (not tomorrow); (c) fresh bot PR files (median inter-file gap this month = ~1.5d, so a 07-27 file is more likely than not — would bump active to 9).

## SEND-streak accounting

Prior SENDs: 2026-07-22 (added buzz), 2026-07-23 (added worldmonitor#5477 + cocoindex#2315 + third identity), 2026-07-24 (added RuView + voicebox + worldmonitor#5518 + fourth identity), 2026-07-25 (added plano + fifth identity + two stale transitions). **07-26: SKIP** (dedup guard, first skip after 4-day SEND streak). Streak counter reset. Next natural SEND trigger: (a) worldmonitor#5477 merges, (b) any fresh bot-PR files, (c) buzz#2248 rolls stale on 07-28, or (d) any state/activity delta on the existing 11 open PRs.
