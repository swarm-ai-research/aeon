# PR Status

*Last updated: 2026-08-11*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five known identities** (`aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`) **plus one variant** (numeric-prefix noreply `272311952+aeonframework@users.noreply.github.com` — same GitHub account, formatting variant not a sixth identity per [[aeon-signing-identity-fragmentation]]). Inline OR filter still required. SKILL.md-documented AND filter with `ai/`-only would still drop the entire queue (**44th consecutive day**).

**NEW CLASS today — repo-deletion PR loss** — `0xprogrammable/aeon-launch-models` returns HTTP 404 today (yesterday: OPEN draft #1 with CHANGES_REQUESTED verdict + author-response commit chain). Owner still exists (`gh api users/0xprogrammable/repos` returns 6 repos: `0xprogrammable`, `developers`, `hookbuilder`, `programmable`, `submit-launch`, `submit-template`) but the `aeon-launch-models` repo is **absent** — no rename target visible. Distinct from [[pr-tracker-search-drops-archived-repo-prs]] (archived: PR recoverable via direct-fetch on `gh api repos/{owner}/{repo}/pulls/{n}`) — deletion returns 404 even on direct-fetch (`gh api repos/0xprogrammable/aeon-launch-models/pulls/1` → 404 Not Found). PR is unrecoverable via GitHub API. Search `issueCount` dropped 23 → 23 vs yesterday (self-owned aeon-programmable-hooks#2 opened 2026-08-10T13:26Z filled the slot vacated by the deletion). File as new class: [[pr-tracker-repo-deletion-loses-pr-permanently]].

**Archive-hide rolled off 7d bucket** — `PostHog/code#4007` (archived 2026-08-06T00:22Z) closedAt 2026-08-03T16:15:06Z crossed the 7d rolloff at 2026-08-10T16:15Z (~18h before this scan). Still search-hidden (`gh api repos/PostHog/code` confirms `archived: true` day 6); still recoverable via direct-fetch — but no longer needed for 7d closed_no_merge bucket. Retained in 30d closed table via direct-fetch (fades naturally over next 22d). Class [[pr-tracker-search-drops-archived-repo-prs]] permanent-until-unarchive hypothesis unaltered — day 6 confirming.

**Predictor 3-of-4 HIT** — 08-10 predicted 08-11 tuple `(1, 7, 1, 2)`; observed `(1, 7, 1, 1)`. Three dimensions correct (recent_merges, stale_open, closed_no_merge). The MISS is `active_open` (predicted 2, observed 1): predictor did not model the **repo-deletion class** — expected 0xprogrammable/aeon-launch-models#1 to remain OPEN today for -1 delta driven by workweave/router#871's stale-transition mirror, but the source PR is gone entirely (repo 404). Recovers as clean 3-of-4 (arithmetic side clean; new class unmodeled). Streak breaks 4-of-4 chain at length-1 (yesterday's 08-09→08-10 clean hit).

## Open (8)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-05 | 5.9d | 1 comment (bot file-time), 0 reviews; `updatedAt` 2026-08-05T14:08Z (5.8d frozen) — crosses 7d frozen ~08-12T14:08Z (~1.1d out) |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 8.5d | **NEW stale today** — crossed 7d frozen 2026-08-10T13:05:59Z (~21h30m before this scan); 2 comments, COMMENTED review |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 18.4d | continuing stale (day 2); last activity 2026-08-02T18:33Z; 2026-08-02 maintainer-sweep cohort per [[same-day-file-cohort-stales-in-lockstep]] |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 20.7d | continuing stale (day 2); last activity 2026-08-02T18:29Z; same cohort |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 18.7d | continuing stale (day 2); last activity 2026-08-02T18:29Z; same cohort |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 22.1d | continuing stale (day 6); 5 comments, no follow-through 12.6d |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 13.4d | continuing stale (day 6); file-time COMMENTED review only |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 13.7d | continuing stale (day 6); 0 comments, only file-time COMMENTED review |

## Active open — 1

`PostHog/posthog#78346` (created 5.9d ago → within 7d activity window).

## Stale open (>7d, no activity 7d) — 7

`workweave/router#871` (**newly stale today**) + `ruvnet/RuView#1409` + `block/buzz#2248` + `jamiepine/voicebox#958` + `KnockOutEZ/wigolo#216` + `WhiskeySockets/Baileys#2732` + `NangoHQ/nango#6929`.

## Recent Merges (last 30d) — 5

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |

Only kaneo#1457 remains IN 7d bucket at scan (rolls off 2026-08-11T19:59Z, ~9h22m AFTER this scan).

## Closed No-Merge (last 30d) — 7

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08T12:48:51Z | continuing 7d bucket (day 3); still no post-close comment. Rolls off 2026-08-15T12:48Z. |
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | fix(deps): bump simple-git, tar, minimatch to patch critical CVEs (CVSS 9.8, 9.2, 8.7) | 2026-08-03T16:15:06Z | 7.8d; **rolled OFF 7d bucket at 08-10T16:15Z** (~18h before scan); still search-hidden day 6 (`archived: true` confirmed), still direct-fetch recoverable. Stays in 30d bucket until 2026-09-02T16:15Z. |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z | 10.2d; off 7d closed_no_merge bucket since 08-08T06:11Z; still in 30d |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z | 12.6d, 3 comments — off 7d bucket since 08-05T20:47Z |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z | 15.0d, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z | 15.1d, 1 comment (bot-only) |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z | 15.6d, 4 comments, CHANGES_REQUESTED at file time |

## Lost (repo-deletion)

| Repo | PR | Title | Last-seen state | Lost at |
|------|----|-------|-----------------|---------|
| 0xprogrammable/aeon-launch-models | #1 | AEON models (draft, source review): NoOp, CapGate, DynamicFee | OPEN draft, CHANGES_REQUESTED 2026-08-07T17:57Z; author-response commit 2026-08-08T19:18Z | Detected 2026-08-11 (repo 404). Owner still exists; repo absent from user's repo list. Direct-fetch confirms 404. |

## Tomorrow's predicted tuple (scan 2026-08-12 ~10:35Z)

`(0, 7, 1, 1)` — recent_merges drops **1 → 0** as kaneo#1457 rolls off 2026-08-11T19:59Z (~14h36m before tomorrow's scan) and no new merges expected; stale_open holds at 7 (no PR crosses 7d-frozen barrier tomorrow — next candidate is PostHog/posthog#78346 crossing at 2026-08-12T14:08Z, ~3h33m AFTER tomorrow's scan → still in active bucket); closed_no_merge holds at 1 (k-skill#547 continues in 7d bucket, no new closures anticipated); active_open holds at 1 (PostHog/posthog#78346 unless a new bot PR files). Confidence high on the arithmetic; residual noise floor from unpredictable maintainer sweeps + additional repo-deletion events (now class-3 confirmed) + bot-side new PRs.
