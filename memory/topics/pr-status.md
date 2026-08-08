# PR Status

*Last updated: 2026-08-08*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five known identities** (`aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`) **plus one variant** (numeric-prefix noreply `272311952+aeonframework@users.noreply.github.com` — same GitHub account, formatting variant not a sixth identity per [[aeon-signing-identity-fragmentation]]). Inline OR filter still required — accept if branch startswith any of {`ai/`, `security/`, `fix/security/`, `aeon/`} OR commit email matches any of the six observed identity strings. SKILL.md-documented AND filter with `ai/`-only would still drop the entire queue (41st consecutive day).

**Archive-hide persists (day 3)** — `PostHog/code` archived 2026-08-06T00:22Z; `is:pr author:aeonframework` search STILL omits `PostHog/code#4007` today (search issueCount = 22, effective total with direct-fetch = 23, 58h+ after archive). SKILL.md must supplement search with a per-repo direct fetch for known-tracked closed PRs, or the 7d closed_no_merge bucket silently under-reports when a maintainer archives a repo mid-window. Class [[pr-tracker-search-drops-archived-repo-prs]] confirmed as **permanent-until-unarchive** on third consecutive observation — eventual-consistency lag hypothesis now essentially falsified at t+58h; treat as fixed behavior.

**Predictor clean 4-of-4 HIT** — 08-07 predicted 08-08 tuple `(1, 3, 1, 7)`; observed `(1, 3, 1, 7)` (byte-exact). Both cross-cutoff rolloffs (cindy#1116 merged 07-31T14:39Z rolled off yesterday afternoon; worldmonitor#5518 closed 08-01T06:11Z rolled off today at 06:11Z, 4h before scan) materialized on schedule. **First 4-of-4 clean prediction since [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]] filed** — the scan-vs-cutoff-hour arithmetic is now empirically reliable across two consecutive multi-rolloff scans.

## Open (7)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-03 | 4.4d | fresh activity — `updatedAt` 2026-08-08T06:25Z (~4h before scan); still 0 comments / 0 reviews (metadata bump only — likely bot rebase or label change) |
| 0xprogrammable/aeon-launch-models | [#1](https://github.com/0xprogrammable/aeon-launch-models/pull/1) | AEON models (draft, source review): NoOp, CapGate, DynamicFee | 2026-08-06 | 1.5d | 1st review received — CHANGES_REQUESTED at 2026-08-07T17:57:53Z (16h before scan); first non-security bot PR ever to receive a review turnaround |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-05 | 2.8d | 1 comment (bot file-time), 0 reviews; no fresh engagement since file (`updatedAt` still 2026-08-05T14:08Z) |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 5.4d | 2 comments, COMMENTED review at file time; `updatedAt` 2026-08-03T13:05:59Z (no fresh engagement 5d) — aging into stale-eligible zone 2026-08-10 (~2d) |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 15.4d | 1 comment (`updatedAt` 2026-08-02T18:33:49Z, 5.7d ago); 08-02 maintainer-sweep aging — stale-eligible 2026-08-09 (~1d) |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 15.7d | 2 comments (`updatedAt` 2026-08-02T18:29:00Z, 5.7d ago); 08-02 maintainer-sweep aging — stale-eligible 2026-08-09 (~1d) |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 17.7d | 1 comment (`updatedAt` 2026-08-02T18:29:12Z, 5.7d ago); 08-02 maintainer-sweep aging — stale-eligible 2026-08-09 (~1d) |

## Stale open (>7d, no activity 7d) — 3

| Repo | PR | Title | Opened | Last activity | Age | Notes |
|------|----|-------|--------|---------------|-----|-------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 2026-07-29T20:50Z | 19.1d | continuing stale (day 3); 5 comments, no follow-through 9.6d |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 2026-07-28T23:45Z | 10.4d | continuing stale (day 3); file-time COMMENTED review only, no maintainer engagement |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 2026-07-28T16:18Z | 10.8d | continuing stale (day 3); 0 comments, only file-time COMMENTED review |

## Recent Merges (last 30d) — 5

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |

Only kaneo#1457 remains IN 7d bucket at scan (rolls off 2026-08-11T19:59Z, ~3d out). cindy#1116 rolled off cleanly at 2026-07-31T14:39Z + 7d = 2026-08-07T14:39Z — landed between yesterday's scan (10:11Z) and today's, matching predicted timing.

## Closed No-Merge (last 30d) — 6

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | fix(deps): bump simple-git, tar, minimatch to patch critical CVEs (CVSS 9.8, 9.2, 8.7) | 2026-08-03T16:15:06Z | 4.75d, 3 comments; **search-hidden day 3** (repo `archived: true` — direct-fetch `gh api repos/PostHog/code/pulls/4007` still recovers); rolls off 7d bucket 2026-08-10T16:15Z (~2d) |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z | 7.2d, 3 comments; **rolled off 7d closed_no_merge bucket at 2026-08-08T06:11Z** (4h before this scan) — still shown in 30d table |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z | 9.6d, 3 comments — off 7d bucket since 08-05T20:47Z; still in 30d |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z | 12.0d, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z | 12.1d, 1 comment (bot-only) |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z | 12.6d, 4 comments, CHANGES_REQUESTED at file time |
