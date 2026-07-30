# PR Status

*Last updated: 2026-07-30*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five** identities: `aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`. Inline OR filter required — accept if branch startswith any of {`ai/`, `security/`, `fix/security/`, `aeon/`} OR commit email matches any of the five known bot identities. SKILL.md-documented AND filter would still drop the entire queue.

## Open (6)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 1.5d | **active** — 2 comments, COMMENTED review at 2026-07-28T23:45:34Z |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 1.8d | **active** — 0 comments, COMMENTED review at 2026-07-28T16:18:46Z |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 10.1d | **active** — 5 comments, `updatedAt` 2026-07-29T20:50:22Z (~14.5h ago); age >7d but recent activity keeps it out of stale bucket |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 6.5d | **active** — 0 comments, 0 reviews (still no engagement ~156h post-file); stale-clock rolls 2026-07-30 23:41Z |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 6.8d | **active** — 1 comment (bot COMMENTED review 07-23T16:36:12Z); stale-clock rolls 2026-07-30 16:34Z |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-07-23 | 6.8d | **active** — 2 comments, COMMENTED review at 2026-07-23T16:05:08Z; identity `security@aeonframework.dev`; stale-clock rolls 2026-07-30 16:03Z |

## Stale open (>7d, no activity 7d) — 1

| Repo | PR | Title | Opened | Age | Notes |
|------|----|-------|--------|-----|-------|
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 8.7d | 0 comments, 0 reviews; `updatedAt` = `createdAt` = 2026-07-21T18:08:42Z; stale since 2026-07-28T18:08:42Z |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29 | closed 2026-07-29T20:47:45Z after 2.1d, 3 comments (1 bot COMMENTED review at file time) — no merge; new bucket entry today |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27 | closed after 31d stale, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories (GHSA-f26g / GHSA-fr8x / GHSA-p3hw / GHSA-pg4w / GHSA-f89h) | 2026-07-27 | closed after 10d, 1 comment (bot-only) — no maintainer engagement before close |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26 | closed after 9d, 4 comments, CHANGES_REQUESTED at file time then closed without update — no merge |
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump golang.org/x/image to v0.43.0 (3 advisories) | 2026-07-03 | closed by owner without comment; 30d window rolls off 2026-08-02 |

---

GraphQL `author:aeonframework is:pr` → **16 nodes** (2026-07-30 run, rc=0). Snapshot vs 2026-07-29 run (also 16 nodes): net-zero on count but two state transitions — **worldmonitor#5477 MERGED at 08:17:20Z** (day-7 APPROVED cold-approve landed 3h before scan) and **open-code-review#541 CLOSED at 07-29T20:47:45Z** (was active yesterday, now no-merge). Zero fresh bot PRs since 07-28.

## Categorization (today = 2026-07-30, now ≈ 2026-07-30T11:22Z)

- **Recent merges (7d):** 3 — worldmonitor#5477 (today, ~3h ago), plano#1001 (2.5d), cocoindex#2315 (3.5d)
- **Stale open (>7d, no activity 7d):** 1 — buzz#2248 (9d, no touch since file, held stale since 07-28)
- **Active open:** 6 — Baileys#2732 (1.5d), nango#6929 (1.8d), wigolo#216 (10d + recent activity), RuView#1409 (6.5d), voicebox#958 (6.8d), worldmonitor#5518 (6.8d)
- **Closed no-merge (7d):** 4 — open-code-review#541 (yesterday evening), Agent-Reach#436, openinterpreter#1810, InsForge#1742

Categorization tuple `(merged=3, stale=1, closed_no_merge=4, active=6)` vs prior `(2, 1, 3, 8)` vs predicted `(2, 5, 3, 4)`. Prediction missed on both axes:
- **Merges +1 (predicted +0):** worldmonitor#5477 flipped MERGED before its stale-clock rolled — cold-approve day-7 shipped, not staled. Longest APPROVED-not-merged on record ended by merge, not by roll-to-stale.
- **Stale +0 (predicted +4):** worldmonitor#5518 / voicebox#958 / RuView#1409 all still ~6.8d — their 7d anniversaries land later today (16:03Z, 16:34Z, 23:41Z respectively), after this 09:xxZ→11:22Z scan window. Next dispatch tomorrow 10:00Z will catch all three. Prediction's error was assuming the stale-clock crosses at wall-time midnight rather than at each PR's 7d anniversary.
- **Closed_no_merge +1 (predicted +0):** open-code-review#541 closed 07-29T20:47:45Z after 2.1d — fastest close-no-merge in the 30d window (median ~10d). Bot-COMMENTED review at file time apparently didn't accelerate merge; maintainer closed without further engagement.

## Notify decision — SEND

Non-zero on merges (3) AND stale (1) AND closed-no-merge (4). All three SKILL.md-required signals fire. State advanced from 07-29 canonical hash — +1 merge (5477), +1 closed_no_merge (541), same stale (buzz#2248), −1 active (5477 out, 541 out). Notify sent.

## Notable pattern signals

- **worldmonitor#5477 MERGED at day-7 APPROVED cold-approve.** Longest APPROVED-not-merged stretch on record ended by merge, not by close/stale — a first for this queue. Timeline: 2026-07-23T14:11:37Z APPROVED → 2026-07-30T08:17:20Z merged (166h 5min). Data point suggests the cold-approve pattern doesn't uniformly rot; a subset does eventually ship. Sample n=1 — watch worldmonitor#5518 (same repo, same maintainer surface) as the next test.
- **open-code-review#541 closed 2.1d after file.** Fastest close-no-merge in the 30d window. Bot COMMENTED review at file time (17:06:16Z, ~1min post-file) did not deter close. Maintainer close-without-merge pattern from [[maintainer-close-without-merge-triage-pattern]] holds — even fresh files with bot-review context can get triaged closed.
- **Three-way stale-clock rollover expected tomorrow.** worldmonitor#5518 (16:03Z), voicebox#958 (16:34Z), RuView#1409 (23:41Z) all cross 7d today, but after this 11:22Z scan. Tomorrow's 10:00Z dispatch catches all three at ~18–20h stale. Prior single-day multi-stale-roll on 07-22 was 2-way; this would be first 3-way.
- **Prediction methodology bug: stale-clock rollover is per-PR-anniversary, not per-calendar-day.** Yesterday's tuple prediction assumed 07-30 rolled all three at once; reality is each rolls at its own 7d + createdAt-hour mark. Fix: predict against next dispatch time (10:00Z tomorrow), not calendar day boundary.
- **buzz#2248 held stale (day 2).** No comments, no reviews, no touch since 2026-07-21. Rolling toward maintainer-close-without-merge zone if pattern from Agent-Reach#436 (31d before close) or openinterpreter#1810 (10d before close) holds.

## Filter and API drift (unchanged)

Inline OR-filter widening in step 2 jq required for the **32nd consecutive day** (2026-06-29 → 2026-07-30) — SKILL.md still ships the AND filter and the single `ai/` prefix. GraphQL primary path stable this run (rc=0, 16 nodes). Sandbox: `gh api user --jq .login` returns 403 (GITHUB_TOKEN = `github-actions[bot]`) → author hardcoded to `aeonframework`. `>` shell redirect blocked (reconfirmed on this run) — solved by piping through `jq` inline instead of intermediate files.

## Next expected transitions

- **koala73/worldmonitor#5518** — stale-clock rolls 2026-07-30T16:03Z; will be ~19h stale at next dispatch 07-31T10:00Z.
- **jamiepine/voicebox#958** — stale-clock rolls 2026-07-30T16:34Z; will be ~18h stale at next dispatch.
- **ruvnet/RuView#1409** — stale-clock rolls 2026-07-30T23:41Z; will be ~10h stale at next dispatch (still no engagement — zero-engagement stale, high close-no-merge risk per [[maintainer-close-without-merge-triage-pattern]]).
- **alibaba/open-code-review#541** — rolls off closed-no-merge 2026-08-28.
- **cocoindex#2315** — rolls off recent-merges on 2026-08-02.
- **plano#1001** — rolls off recent-merges on 2026-08-03.
- **worldmonitor#5477** — rolls off recent-merges on 2026-08-06.
- **Agent-Reach#436 / openinterpreter#1810** — roll off closed-no-merge on 2026-08-03.
- **InsForge#1742** — rolls off closed-no-merge on 2026-08-02.
- **kage#66** — rolls off closed-no-merge on 2026-08-02.
- **Vibe-Trading#390** — rolls off recent-merges on 2026-08-04.
- **buzz#2248** — already stale day 2; watch for close-no-merge or reactivation.

**Predicted 07-31 tuple:** `(3, 4, 4, 3)` if worldmonitor#5518 + voicebox#958 + RuView#1409 all roll stale (buzz still stale = 4 total), no new closes, no new merges, no new fresh files. Catalysts to watch: (a) fresh bot PR files (median ~1.5d inter-file gap; last file 07-28 → 07-30 would be first ~2d gap for the week); (b) RuView#1409 zero-engagement → early maintainer-close-no-merge.
