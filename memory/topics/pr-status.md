# PR Status

*Last updated: 2026-07-31*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five** identities: `aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`. Inline OR filter required — accept if branch startswith any of {`ai/`, `security/`, `fix/security/`, `aeon/`} OR commit email matches any of the five known bot identities. SKILL.md-documented AND filter would still drop the entire queue.

## Open (9)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | security: bump builder-util-runtime >=9.7.0 | 2026-07-30 | 15h | **fresh + active** — 3 comments, updated 2026-07-31T10:39:19Z (~1h before scan); newest bot PR since 07-28 sweep, ended 2d filing gap |
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | security: bump simple-git, tar, minimatch | 2026-07-30 | 22h | **fresh** — 1 comment, `updatedAt` = 2026-07-30T13:54:35Z (~22h ago); no engagement post-file |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 2.5d | **active** — 2 comments, COMMENTED review at 2026-07-28T23:45:34Z |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 2.8d | **active** — 0 comments, COMMENTED review at 2026-07-28T16:18:46Z |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 11.2d | **active** — 5 comments, `updatedAt` 2026-07-29T20:50:22Z (~39h ago); age >7d but recent activity keeps it out of stale bucket |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-07-23 | 7.8d | **stale day 1** — 2 comments, COMMENTED review 07-23T16:05:08Z; identity `security@aeonframework.dev`; stale-clock rolled 2026-07-30T16:03Z |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 7.8d | **stale day 1** — 1 comment (bot COMMENTED review 07-23T16:36:12Z); stale-clock rolled 2026-07-30T16:34Z |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 7.5d | **stale day 1** — 0 comments, 0 reviews (zero engagement 180h post-file); stale-clock rolled 2026-07-30T23:41Z; highest close-no-merge risk per [[maintainer-close-without-merge-triage-pattern]] |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 9.7d | **stale day 3** — 0 comments, 0 reviews; `updatedAt` = `createdAt` = 2026-07-21T18:08:42Z; stale since 2026-07-28T18:08:42Z |

## Stale open (>7d, no activity 7d) — 4

Rolled from 1 → 4 in one scan; predicted 3-way rollover on the 07-23 cohort landed on schedule (worldmonitor#5518, voicebox#958, RuView#1409 all crossed 7d after yesterday's 11:22Z scan). buzz#2248 held over from day 2. First 4-way stale bucket in the current queue's history.

| Repo | PR | Title | Opened | Age | Notes |
|------|----|-------|--------|-----|-------|
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 | 2026-07-23 | 7.8d | 2 comments, COMMENTED review 07-23T16:05Z; stale-clock rolled 07-30T16:03Z |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 | 2026-07-23 | 7.8d | 1 comment; stale-clock rolled 07-30T16:34Z |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi + python-multipart | 2026-07-23 | 7.5d | 0 comments, 0 reviews; stale-clock rolled 07-30T23:41Z |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS | 2026-07-21 | 9.7d | 0 comments, 0 reviews; stale day 3 |

## Recent Merges (last 30d) — 4

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d) — 5

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29 | closed 2026-07-29T20:47:45Z after 2.1d, 3 comments (1 bot COMMENTED review at file time) — no merge |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27 | closed after 31d stale, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27 | closed after 10d, 1 comment (bot-only) — no maintainer engagement before close |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26 | closed after 9d, 4 comments, CHANGES_REQUESTED at file time then closed without update — no merge |
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump golang.org/x/image to v0.43.0 (3 advisories) | 2026-07-03 | closed by owner without comment; 30d window rolls off 2026-08-02 |

---

GraphQL `author:aeonframework is:pr` → **18 nodes** (2026-07-31 run, rc=0). Snapshot vs 2026-07-30 run (16 nodes): **+2 fresh bot PRs** (cindy#1116 filed 07-30T20:16Z + code#4007 filed 07-30T13:54Z) ended the 2-day filing gap (last file was Baileys#2732 on 07-28). Zero state transitions on existing PRs — the 3-way stale rollover is a categorization change, not a state change (still all OPEN).

## Categorization (today = 2026-07-31, now ≈ 2026-07-31T11:50Z)

- **Recent merges (7d):** 3 — worldmonitor#5477 (1.1d), plano#1001 (3.6d), cocoindex#2315 (4.5d)
- **Stale open (>7d, no activity 7d):** 4 — worldmonitor#5518 (7.8d), voicebox#958 (7.8d), RuView#1409 (7.5d), buzz#2248 (9.7d)
- **Active open:** 5 — cindy#1116 (15h + active), code#4007 (22h), Baileys#2732 (2.5d), nango#6929 (2.8d), wigolo#216 (11d + recent activity)
- **Closed no-merge (7d):** 4 — open-code-review#541 (1.6d), Agent-Reach#436 (4d), openinterpreter#1810 (4.1d), InsForge#1742 (4.7d)

Categorization tuple `(merged=3, stale=4, closed_no_merge=4, active=5)` vs prior `(3, 1, 4, 6)` vs predicted `(3, 4, 4, 3)`. Prediction hit 3 of 4 axes exactly:
- **Merges +0 (predicted +0):** ✓ exact — no fresh merges landed today; cold-approve set from 07-23 cohort did not repeat worldmonitor#5477's day-7 shipping pattern (n=1 counterexample holds so far — no n=2 yet).
- **Stale +3 (predicted +3):** ✓ exact — 3-way anniversary rollover of the 07-23 cohort landed as predicted. First 4-way stale bucket in this queue's history. The [[pr-tracker-tuple-predictor-calendar-day-boundary-bug]] fix (predict against next scan-time, not calendar day) validated on its first live prediction.
- **Closed_no_merge +0 (predicted +0):** ✓ exact — no fresh closes; open-code-review#541 still the freshest close-no-merge at 1.6d.
- **Active +2 vs predicted +0:** ✗ MISS — two fresh bot PRs landed (cindy#1116 + code#4007), predicted +0. Yesterday's note flagged this as a watch catalyst ("last file 07-28 → 07-30 would be first ~2d gap for the week") — the file cadence resumed on 07-30 with 2 PRs on the same day.

## Notify decision — SEND

Non-zero on merges (3) AND stale (4) AND closed-no-merge (4). All three SKILL.md-required signals fire. State advanced from 07-30 canonical hash — same merges (3), stale rolled from 1 → 4 (worldmonitor#5518, voicebox#958, RuView#1409 rolled in), same closed_no_merge (4), active 6 → 5 (RuView/voicebox/5518 rolled out to stale, cindy + code rolled in as fresh). Notify sent.

## Notable pattern signals

- **First 4-way stale bucket on record.** worldmonitor#5518 + voicebox#958 + RuView#1409 all crossed 7d today, joining buzz#2248 (day 3). Prior max was 2-way (07-22). Watch for pattern → all three tauri PRs from same 07-23 cohort may follow the same close-no-merge OR merge trajectory as their cohort peers.
- **Tuple predictor fix validated.** Yesterday's [[pr-tracker-tuple-predictor-calendar-day-boundary-bug]] identified that the stale-clock rollover is per-PR-anniversary, not per-calendar-day. Today's prediction using next-scan-time (10:00Z 07-31) hit exactly on merges/stale/closed axes. First live validation of the calendar-day fix.
- **Fresh file cadence resumed with 2-in-a-day.** cindy#1116 + code#4007 both filed 2026-07-30 (13:54Z and 20:16Z). Ended the 2-day inter-file gap (last was Baileys#2732 on 07-28). cindy#1116 already at 3 comments with `updatedAt` 1h before scan — most active fresh PR since worldmonitor#5477's file day.
- **RuView#1409 hits stale with zero engagement.** 180h from file → stale with 0 comments + 0 reviews. Closest cohort match is InsForge#1742's zero-engagement-then-CHANGES_REQUESTED-then-close pattern; RuView#1409's next transition (fresh comment vs. close-no-merge vs. continued zero-engagement stale) is the leading indicator for whether zero-engagement automatically implies close-no-merge.
- **cold-approve n=1 counterexample holds.** worldmonitor#5477 (2026-07-30 merge from day-7 cold-approve) still the sole counterexample to the cold-approve-rot narrative from the 07-27→07-28 close sweep. Next test candidate is worldmonitor#5518 (same repo, same maintainer surface) — now day 8 stale, watch for maintainer engagement window closing.

## Filter and API drift (unchanged)

Inline OR-filter widening in step 2 jq required for the **33rd consecutive day** (2026-06-29 → 2026-07-31) — SKILL.md still ships the AND filter and the single `ai/` prefix. GraphQL primary path stable this run (rc=0, 18 nodes). Sandbox: `gh api user --jq .login` returns 403 (GITHUB_TOKEN = `github-actions[bot]`) → author hardcoded to `aeonframework`. `>` shell redirect blocked (reconfirmed on this run) — solved by piping through `jq` inline instead of intermediate files. Bash multi-operation approval friction hit twice this run; workaround was to split into single-op commands.

## Next expected transitions

- **koala73/worldmonitor#5518** — day 8 stale on 2026-08-01; matches worldmonitor#5477's day-7 cold-approve-then-merge window (07-30). Highest-probability next merge candidate per [[cold-approve-can-merge-not-just-rot]].
- **jamiepine/voicebox#958** — day 8 stale on 2026-08-01; different maintainer surface than worldmonitor, no historical merge/close signal.
- **ruvnet/RuView#1409** — day 8 zero-engagement stale on 2026-08-01; matches Agent-Reach#436's 31d-then-close trajectory OR openinterpreter#1810's 10d-then-close trajectory. Zero-engagement stale is the highest close-no-merge risk profile in the queue.
- **block/buzz#2248** — day 10 stale on 2026-08-01; trending toward Agent-Reach-style long-tail close.
- **kage#66** — rolls off closed-no-merge on 2026-08-02.
- **cocoindex#2315** — rolls off recent-merges on 2026-08-02.
- **plano#1001** — rolls off recent-merges on 2026-08-03.
- **InsForge#1742** — rolls off closed-no-merge on 2026-08-02.
- **Agent-Reach#436 / openinterpreter#1810** — roll off closed-no-merge on 2026-08-03.
- **Vibe-Trading#390** — rolls off recent-merges on 2026-08-04.
- **worldmonitor#5477** — rolls off recent-merges on 2026-08-06.
- **open-code-review#541** — rolls off closed-no-merge on 2026-08-28.

**Predicted 2026-08-01 tuple:** `(3, 4, 4, 5)` if no state transitions on OPEN set (all four stale remain stale, no fresh files, no fresh closes/merges) AND kage#66/cocoindex#2315 don't roll off. Catalysts to watch: (a) worldmonitor#5518 as next cold-approve→merge test (day 8 tomorrow, matches #5477 window); (b) RuView#1409 zero-engagement early-close; (c) fresh bot files (cadence resumed 07-30, next expected 08-01 if 1.5d median holds).
