# PR Status

*Last updated: 2026-08-02*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five** identities: `aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`. Inline OR filter required — accept if branch startswith any of {`ai/`, `security/`, `fix/security/`, `aeon/`} OR commit email matches any of the five known bot identities. SKILL.md-documented AND filter would still drop the entire queue.

## Open (8)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 1.1d | **active** — 3 comments, COMMENTED review at 08:09Z (~2min post-file); no fresh engagement in the 27h since |
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | security: bump simple-git, tar, minimatch | 2026-07-30 | 2.9d | fresh — 1 comment, `updatedAt` = 2026-07-30T13:54:35Z (no engagement post-file; 3rd consecutive scan zero-move) |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 4.5d | active — 2 comments, COMMENTED review at 2026-07-28T23:45:34Z; no fresh engagement since |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 4.8d | active — 0 comments, COMMENTED review at 2026-07-28T16:18:46Z; no fresh engagement since |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 13.2d | **active** — 5 comments, `updatedAt` 2026-07-29T20:50:22Z (~3.6d ago); age >7d but recent-enough activity keeps out of stale bucket |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 9.8d | **stale day 3** — 1 comment (bot COMMENTED review 07-23T16:36:12Z); stale since 2026-07-30T16:34Z; 07-23 tauri cohort peer #5518 already closed no-merge |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 9.5d | **stale day 3** — 0 comments, 0 reviews (zero engagement 227h post-file); stale since 2026-07-30T23:41Z; highest close-no-merge risk per [[maintainer-close-without-merge-triage-pattern]] |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 11.7d | **stale day 5** — 0 comments, 0 reviews; `updatedAt` = `createdAt` = 2026-07-21T18:08:42Z; trending Agent-Reach-style long-tail close |

## Stale open (>7d, no activity 7d) — 3

Unchanged from 08-01 (voicebox#958 + RuView#1409 + buzz#2248 all held; each rolled +1 day). No new entries and no exits — the 3-way bucket stayed intact for the second consecutive scan. Zero-engagement stale queue (RuView + buzz, neither has surfaced any maintainer touch since file) grows to day 9.5 / day 11.7 respectively.

| Repo | PR | Title | Opened | Age | Notes |
|------|----|-------|--------|-----|-------|
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 | 2026-07-23 | 9.8d | 1 comment; stale-clock rolled 07-30T16:34Z; different maintainer surface than worldmonitor; 07-23 tauri cohort follow-through candidate after #5518 close |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi + python-multipart | 2026-07-23 | 9.5d | 0 comments, 0 reviews; stale-clock rolled 07-30T23:41Z; zero-engagement stale = highest close-no-merge risk; matches Agent-Reach#436's 31d-close and openinterpreter#1810's 10d-close trajectory |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS | 2026-07-21 | 11.7d | 0 comments, 0 reviews; stale day 5; long-tail close candidate; oldest zero-engagement stale in the queue |

## Recent Merges (last 30d) — 5

Unchanged from 08-01 — no fresh merges in the 24h since (predicted no merges → HIT).

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d) — 6

kage#66 predicted-to-roll-off today did NOT roll off at scan time — closedAt 2026-07-03T12:20:11Z + 30d = 2026-08-02T12:20:11Z, scan ran at 2026-08-02T11:16Z (~64min BEFORE rolloff). New tuple-predictor failure mode per [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]] (candidate) — the 07-31 calendar-boundary → next-scan-time fix does not cover the intra-day scan-vs-cutoff-hour axis. kage rolls off before tomorrow's 10:00Z scan (30d + 22h in the past by then).

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z after 8.6d, 3 comments (bot COMMENTED review at file, +1 new comment since) — first close on 07-23 tauri cohort |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z after 2.1d, 3 comments (1 bot COMMENTED review at file time) — no merge |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z after 31d stale, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z after 10d, 1 comment (bot-only) — no maintainer engagement before close |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z after 9d, 4 comments, CHANGES_REQUESTED at file time then closed without update — no merge |
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump golang.org/x/image to v0.43.0 (3 advisories) | 2026-07-03T12:20:11Z, 0 comments, closed by owner without review; 30d window rolls off 2026-08-02T12:20Z (~64min after this scan) |

---

GraphQL `author:aeonframework is:pr` → **19 nodes** (2026-08-02 run, rc=0). Snapshot vs 2026-08-01 run (19 nodes): **zero deltas** on both node count and per-PR state. First truly stationary scan since the 07-30 → 07-31 pause window (07-31 introduced cindy#1116; 08-01 introduced kaneo#1457 + 3 state transitions on existing set; 08-02 introduces nothing). Ends 08-01's record 3-transition scan with a 0-transition scan.

## Categorization (today = 2026-08-02, now ≈ 2026-08-02T11:16Z)

- **Recent merges (7d):** 4 — cindy#1116 (1.9d), worldmonitor#5477 (3.1d), plano#1001 (5.5d), cocoindex#2315 (6.5d)
- **Stale open (>7d, no activity 7d):** 3 — voicebox#958 (9.8d), RuView#1409 (9.5d), buzz#2248 (11.7d)
- **Active open:** 5 — kaneo#1457 (1.1d), code#4007 (2.9d), Baileys#2732 (4.5d), nango#6929 (4.8d), wigolo#216 (13.2d + recent activity)
- **Closed no-merge (7d):** 5 — worldmonitor#5518 (1.2d), open-code-review#541 (3.6d), Agent-Reach#436 (5.9d), openinterpreter#1810 (6.1d), InsForge#1742 (6.7d)

Categorization tuple `(merged=4, stale=3, closed_no_merge=5, active=5)` vs prior `(4, 3, 5, 5)` vs predicted `(4, 3, 4, 5)`. Prediction hit 3 of 4 axes:

- **Merges +0 (predicted +0):** ✓ EXACT — no fresh merges. Prior scan's fast-merge signal (cindy#1116 landed in 18h) was a one-off, not a trend.
- **Stale +0 (predicted +0):** ✓ EXACT — 3-way bucket held for 2nd consecutive scan; no OPEN → stale transitions, no stale exits. voicebox / RuView / buzz all rolled +1 day.
- **Closed_no_merge +0 (predicted −1):** ✗ MISS — expected kage#66 rolloff, actual rolloff time (12:20Z) is 64min after scan time (11:16Z). Predictor treated the calendar day as the boundary instead of the exact hour-of-close + 30d. Root cause = new mode of the same class as [[pr-tracker-tuple-predictor-calendar-day-boundary-bug]] (calendar-day thinking vs. actual-hour thinking); the 07-31 fix addressed one axis, this is a second axis. Second consecutive scan with predictor miss (08-01 hit 0 of 4 axes; 08-02 hits 3 of 4 — predictor accuracy recovered dramatically once OPEN set went stationary).
- **Active +0 (predicted +0):** ✓ EXACT — no bucket transitions, no fresh files.

## Notify decision — SKIP (dedup guard)

Per [[pr-tracker-notify-repeats-with-no-state-change]] hash-based dedup guard: today's notify-trigger set (union of 7d merged + stale + 7d closed-no-merge) is **byte-identical** to yesterday's set — same 12 PRs, same states, same `updatedAt` timestamps on the 3 OPEN stale entries (by definition of stale). SKILL step-5 gate would fire (non-zero on all three signals) but the guard suppresses because there is no state advance to communicate. This is the **guard's 5th validated in-skill application** (prior: 07-09, 07-10, 07-14, 07-15, 07-16 per note history).

Trigger-set hash (repo:number:state:updatedAt tuples, sorted, sha1):
```
cindy:1116:MERGED:2026-07-31T14:40:08Z
cocoindex:2315:MERGED:2026-07-26T23:05:36Z
plano:1001:MERGED:2026-07-27T22:36:12Z
worldmonitor:5477:MERGED:2026-07-30T08:17:20Z
buzz:2248:OPEN:2026-07-21T18:08:42Z
RuView:1409:OPEN:2026-07-23T23:41:02Z
voicebox:958:OPEN:2026-07-23T18:33:15Z
Agent-Reach:436:CLOSED:2026-07-27T13:16:01Z
InsForge:1742:CLOSED:2026-07-26T19:14:04Z
open-code-review:541:CLOSED:2026-07-29T20:47:45Z
openinterpreter:1810:CLOSED:2026-07-27T08:59:01Z
worldmonitor:5518:CLOSED:2026-08-01T06:11:46Z
```

Also per [[pr-tracker-step-5-misses-fresh-bot-prs]] fresh-bot-file trigger: no new bot PRs since prior scan (last new was kaneo#1457 filed 08-01T08:08Z, already tracked). Fresh-bot trigger does not fire.

## Notable pattern signals

- **First fully stationary scan since 07-30.** Zero deltas on GraphQL result set, zero state transitions, zero fresh bot files, zero rolloffs at scan time. The queue paused. Prior stationary streaks: 07-04 through 07-08 (5 days, drove the original dedup-guard lesson), 07-14 through 07-16 (3 days), 07-25 (1 day). Watch tomorrow: if kage#66 rolls off (it will, at 12:20Z today, hitting tomorrow's scan) and no other transitions land, predictor scores 4/4 and stationarity extends to 2 scans.
- **Predictor recovery — 3/4 hit vs 0/4 yesterday.** Once the OPEN set stopped moving (no fresh files, no cross-bucket transitions), predictor accuracy recovered from record low. Confirms predictor error concentrates on OPEN-set volatility axes (fresh files, active engagement flipping stale→active, cold-approve merges) rather than mechanical rolloffs. The 1-of-4 miss today is the intra-day scan-vs-cutoff-hour class — a distinct predictor failure mode from yesterday's cohort-inversion misses.
- **Zero-engagement stale queue holds at 2 (RuView#1409 + buzz#2248) — bucket ages roll +1 day.** RuView day 9.5, buzz day 11.7. Neither has surfaced any maintainer touch since file. RuView remains the closest analog to just-closed worldmonitor#5518 (day 8.6 close). Watch for close-no-merge follow-through in the 9–14 day range.
- **Zero fresh bot files today.** Prior 3 days had at least 1 fresh file per day (07-30 code#4007, 07-31 cindy#1116, 08-01 kaneo#1457). First zero-file scan since the 07-25 → 07-27 pause. Filing cadence pause is either (a) surge-then-rest natural rhythm or (b) upstream vuln-scanner blocked by [[github-actions-cannot-create-prs]] carryover (talivia bundle from 08-01 sits in `.pending-disclosure/` unblocked). Cannot distinguish without probing.
- **Cindy fast-merge (18h) had no follow-through today.** Yesterday's speculation that "aeonframework@proton.me identity ships fast" needs more data — today no fresh proton.me-signed PRs filed to test the hypothesis.

## Filter and API drift (unchanged)

Inline OR-filter widening in step 2 jq required for the **35th consecutive day** (2026-06-29 → 2026-08-02) — SKILL.md still ships the AND filter and the single `ai/` prefix. GraphQL primary path stable this run (rc=0, 19 nodes). Sandbox: `gh api user --jq .login` returns 403 (GITHUB_TOKEN = `github-actions[bot]`) → author hardcoded to `aeonframework`. `>` shell redirect blocked in prior scans; today used inline `jq` pipeline directly on `gh api graphql` output — one command, one approval, no intermediate file. Bash multi-op approval friction not hit today (single-command graphql-to-jq pipeline path is now the working default).

## Next expected transitions

- **kage#66** — rolls off closed-no-merge at 2026-08-02T12:20Z (~1h after this scan); definitely gone from tomorrow's 10:00Z scan; predicted tuple contribution: closed_no_merge 5 → 4.
- **cocoindex#2315** — rolls off recent-merges at 2026-08-02T23:05Z (later today); merged 5 → 4 for tomorrow.
- **plano#1001** — rolls off recent-merges at 2026-08-03T22:36Z (tomorrow late); merged 4 → 3 for scan on 2026-08-04.
- **jamiepine/voicebox#958** — day 10 stale on 2026-08-03; 07-23 tauri cohort peer of just-closed #5518; watch for close-no-merge follow-through as cohort-repeat evidence.
- **ruvnet/RuView#1409** — day 10 zero-engagement stale on 2026-08-03; still tracks Agent-Reach#436's 31d-close and openinterpreter#1810's 10d-close trajectories. Zero-engagement + close-cohort-signal from #5518 raises close-no-merge probability further.
- **block/buzz#2248** — day 12 stale on 2026-08-03; trending toward Agent-Reach-style long-tail close.
- **InsForge#1742** — rolls off closed-no-merge at 2026-08-02T19:14Z (later today); closed 5 → 4 for tomorrow. Combined with kage rolloff: closed_no_merge 5 → 3 by tomorrow's scan.
- **Agent-Reach#436 / openinterpreter#1810** — roll off closed-no-merge on 2026-08-03T13:16Z / 08:59Z; both hit tomorrow's 10:00Z scan cleanly if scan runs at/after 13:16Z (or 08:59Z for openinterpreter). openinterpreter rolls off just before nominal 10:00Z scan tomorrow → closed 4 → 3 by then; Agent-Reach rolls off ~3h after nominal scan → closed 3 → 2 by 2026-08-04. Same intra-day scan-vs-cutoff-hour predictor axis as today's kage miss applies.
- **Vibe-Trading#390** — rolls off recent-merges on 2026-08-04T15:33Z.
- **worldmonitor#5477** — rolls off recent-merges on 2026-08-06T08:17Z.
- **open-code-review#541** — rolls off closed-no-merge on 2026-08-28T20:47Z.
- **worldmonitor#5518** — rolls off closed-no-merge on 2026-08-31T06:11Z.
- **cindy#1116** — rolls off recent-merges on 2026-08-07T14:39Z.

**Predicted 2026-08-03 tuple:** `(3, 3, 3, 5)` assuming (a) no OPEN-set transitions, (b) tomorrow's scan runs at ~10:00Z: cocoindex rolls out of merged 5 → 4 (actually merged is at 4 today — after cocoindex rolls off tonight, merged becomes 3), kage + InsForge + openinterpreter all roll out of closed_no_merge (5 → 2). Adjusted from the raw rollover count: merged 4 → 3, stale 3 → 3, closed_no_merge 5 → 2, active 5 → 5. Predicted `(3, 3, 2, 5)`. Catalysts to watch: (a) voicebox#958/RuView#1409 cohort-trajectory test (does close-signal propagate to remaining tauri PRs?); (b) buzz#2248 continued dormancy vs late close; (c) fresh bot files (cadence paused today, watch for resumption); (d) predictor validation of the intra-day scan-vs-cutoff-hour axis (openinterpreter rolls off at 08:59Z, before 10:00Z scan — should be OUT; Agent-Reach rolls off at 13:16Z, after 10:00Z scan — should be IN).
