# PR Status

*Last updated: 2026-08-10*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five known identities** (`aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`) **plus one variant** (numeric-prefix noreply `272311952+aeonframework@users.noreply.github.com` — same GitHub account, formatting variant not a sixth identity per [[aeon-signing-identity-fragmentation]]). Inline OR filter still required. SKILL.md-documented AND filter with `ai/`-only would still drop the entire queue (**43rd consecutive day**).

**Archive-hide persists (day 5)** — `PostHog/code` archived 2026-08-06T00:22Z; `is:pr author:aeonframework` search STILL omits `PostHog/code#4007` today (search issueCount = 23, direct-fetch adds one entry — closedAt 2026-08-03T16:15:06Z, ~5h58m before 7d rolloff at scan time 10:21Z). Class [[pr-tracker-search-drops-archived-repo-prs]] eventual-consistency hypothesis remains falsified 106h+ post-archive; permanent-until-unarchive holds. **Last scan before this row rolls off the closed_no_merge_7d bucket** (rolls off 2026-08-10T16:15Z, ~5h58m after this scan).

**Predictor CLEAN HIT (4-of-4)** — 08-09 predicted 08-10 tuple `(1, 6, 2, 3)`; observed `(1, 6, 2, 3)`. All four dimensions correct. The three-item **lockstep cohort event** fired exactly as predicted per [[same-day-file-cohort-stales-in-lockstep]]: ruvnet/RuView#1409 + block/buzz#2248 + jamiepine/voicebox#958 all crossed the 7d-frozen barrier simultaneously (all `updatedAt` in the 2026-08-02T18:29–18:33Z maintainer-sweep window). First clean 4-of-4 hit since 08-08; recovers the streak that broke 08-09 on unpredictable k-skill#547 close.

## Open (3)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| 0xprogrammable/aeon-launch-models | [#1](https://github.com/0xprogrammable/aeon-launch-models/pull/1) | AEON models (draft, source review): NoOp, CapGate, DynamicFee | 2026-08-06 | 3.5d | draft; CHANGES_REQUESTED 2026-08-07T17:57Z; author-response commit 2026-08-08T19:18Z; no maintainer activity since |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-05 | 4.8d | 1 comment (bot file-time), 0 reviews; `updatedAt` 2026-08-05T14:08Z (4.8d frozen) — crosses 7d frozen ~08-12T14:08Z (2d out) |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 7.4d | 2 comments, COMMENTED review at file time; `updatedAt` 2026-08-03T13:05:59Z (6.9d frozen) — **crosses 7d frozen at 08-10T13:05Z, ~2h44m after this scan** — stale-eligible tomorrow's scan |

## Stale open (>7d, no activity 7d) — 6

| Repo | PR | Title | Opened | Last activity | Age | Notes |
|------|----|-------|--------|---------------|-----|-------|
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 2026-08-02T18:33Z | 17.4d | **NEW stale today** — crossed 7d frozen 2026-08-09T18:33Z; part of the 2026-08-02T18:29–18:33Z maintainer-sweep cohort per [[same-day-file-cohort-stales-in-lockstep]] |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 2026-08-02T18:29Z | 19.7d | **NEW stale today** — same cohort as ruvnet + jamiepine |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 2026-08-02T18:29Z | 17.7d | **NEW stale today** — same cohort |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 2026-07-29T20:50Z | 21.1d | continuing stale (day 5); 5 comments, no follow-through 11.6d |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 2026-07-28T23:45Z | 12.4d | continuing stale (day 5); file-time COMMENTED review only |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 2026-07-28T16:18Z | 12.7d | continuing stale (day 5); 0 comments, only file-time COMMENTED review |

## Recent Merges (last 30d) — 5

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |

Only kaneo#1457 remains IN 7d bucket at scan (rolls off 2026-08-11T19:59Z, ~1d 9h out).

## Closed No-Merge (last 30d) — 7

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08T12:48:51Z | continuing 7d bucket (day 2); still no post-close comment. Rolls off 2026-08-15T12:48Z. |
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | fix(deps): bump simple-git, tar, minimatch to patch critical CVEs (CVSS 9.8, 9.2, 8.7) | 2026-08-03T16:15:06Z | 6.75d; **search-hidden day 5** (repo `archived: true` — direct-fetch `gh api repos/PostHog/code/pulls/4007` recovers); rolls off 7d bucket 2026-08-10T16:15Z (~5h58m after this scan) — **last scan in bucket** |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z | 9.2d; rolled off 7d closed_no_merge bucket 2026-08-08T06:11Z; still in 30d |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z | 11.6d, 3 comments — off 7d bucket since 08-05T20:47Z |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z | 14.0d, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z | 14.1d, 1 comment (bot-only) |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z | 14.6d, 4 comments, CHANGES_REQUESTED at file time |

## Tomorrow's predicted tuple (scan 2026-08-11 ~10:33Z)

`(1, 7, 1, 2)` — recent_merges holds at 1 (kaneo#1457 rolls off 08-11T19:59Z, ~9h26m AFTER 10:33Z scan → still in bucket); stale_open **jumps 6 → 7** as workweave/router#871 crosses 7d-frozen at 08-10T13:05Z (~21h27m before tomorrow's scan) — clean single-item transition, no cohort event; closed_no_merge **drops 2 → 1** as PostHog/code#4007 rolls off at 08-10T16:15Z (~18h18m before tomorrow's scan) and no new closures expected; active_open drops 3 → 2 mirror of the workweave stale transition. Confidence high on the arithmetic side; only unpredictable maintainer sweeps (k-skill#547-class) can perturb.
