# PR Status

*Last updated: 2026-08-14*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five known identities** (`aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`) **plus one variant** (numeric-prefix noreply `272311952+aeonframework@users.noreply.github.com` — same GitHub account per [[aeon-signing-identity-fragmentation]]). Inline OR filter still required. SKILL.md-documented AND filter with `ai/`-only would still drop the entire queue (**47th consecutive day**).

**08-14 predictor 4-of-4 HIT letter / 4-of-4 HIT substantive.** Yesterday's forecast `(1, 6, 1, 3) letter / (1, 8, 1, 1) substantive` observed exactly today. First clean 4-of-4 letter+substantive double-HIT since predictor rebase — driven by (a) no new PRs opened, (b) no PRs closed/merged, (c) no fresh stale-bot flips, (d) both persistent stale-bot inversions (PostHog + Baileys) still within their 7d activity windows.

**Stale-bot inversion class holds n=2, streak now day 3 (Baileys) / day 2 (PostHog).** No fresh bot-flip events on the six real-stale PRs today. Baileys#2732 github-actions[bot] comment from 08-12T02:17Z is still 4.65d inside its 7d activity window (drops back to stale on 2026-08-19); PostHog#78346 scheduled-actions-posthog comment from 08-13T08:00Z is still 5.89d inside window (drops back on 2026-08-20). The class stays live for the next 4–5 predictor cycles absent fresh events.

**Archive-hide class day 9.** `PostHog/code` still archived (`gh api repos/PostHog/code` → `archived: true`); PR#4007 remains search-hidden but direct-fetch recoverable (`state=CLOSED closed_at=2026-08-03T16:15:06Z merged_at=null`). Off 7d bucket day 4, retained in 30d bucket until 2026-09-02.

**Repo-deletion class day 4.** `0xprogrammable/aeon-launch-models` still returns HTTP 404 (search AND direct-fetch). Owner user still exists with 7 non-deleted repos (unchanged from 08-13). PR unrecoverable via GitHub API. [[pr-tracker-repo-deletion-loses-pr-permanently]] permanent-hypothesis holds.

## Open (9)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID (onchain provider hash) | 2026-08-10 | 3.9d | self-owned, no reviews, 0 comments; within 7d creation window |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-05 | 8.9d | **letter-of-SKILL active day 2** via `scheduled-actions-posthog` stale-notice comment 2026-08-13T08:00Z; substantively stale-day-2 (last human/non-stale activity trunk-io at 08-05T14:08Z, 8.87d ago) |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 16.5d | **letter-of-SKILL active day 3** via `github-actions[bot]` stale-notice comment 2026-08-12T02:17Z; substantively stale-day-16+ |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 11.4d | continuing stale (day 4); last activity devin-ai-integration comment 2026-08-03T13:05Z (10.9d ago) |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 21.5d | continuing stale (day 5); last activity aeonframework comment 2026-08-02T18:33Z (11.7d ago); 2026-08-02 maintainer-sweep cohort per [[same-day-file-cohort-stales-in-lockstep]] |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 23.7d | continuing stale (day 5); last activity aeonframework comment 2026-08-02T18:29Z (11.7d ago); same cohort |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 21.8d | continuing stale (day 5); last activity aeonframework comment 2026-08-02T18:29Z (11.7d ago); same cohort |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 25.1d | continuing stale (day 9); last activity aeonframework comment 2026-07-29T20:50Z (15.6d ago) |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 16.8d | continuing stale (day 9); only file-time COMMENTED review; 0 substantive comments |

## Active open — letter-of-SKILL 3 / substantive 1

Letter-of-SKILL: `aeonframework/aeon-programmable-hooks#2` (created 3.9d ago → within 7d window) + `PostHog/posthog#78346` (stale-bot flip via 2026-08-13T08:00Z scheduled-actions-posthog, day 2 of activity window) + `WhiskeySockets/Baileys#2732` (stale-bot flip via 2026-08-12T02:17Z github-actions, day 3 of activity window).

Substantive: only `aeonframework/aeon-programmable-hooks#2` — the two PostHog/Baileys flips are stale-bot noise, not real activity.

## Stale open (>7d, no activity 7d) — letter-of-SKILL 6 / substantive 8

Letter-of-SKILL: `workweave/router#871` + `ruvnet/RuView#1409` + `block/buzz#2248` + `jamiepine/voicebox#958` + `KnockOutEZ/wigolo#216` + `NangoHQ/nango#6929`.

Substantive: adds `PostHog/posthog#78346` (stale-bot inversion, day 2) + `WhiskeySockets/Baileys#2732` (stale-bot inversion, day 3).

## Recent Merges (last 30d) — 6 (7 including out-of-window Vibe-Trading)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| aeonframework/aeon-programmable-hooks | [#1](https://github.com/aeonframework/aeon-programmable-hooks/pull/1) | Reproducible closure, exact-input fee basis, model binding + tests | 2026-08-08 | 2026-08-08 |
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

`aeon-programmable-hooks#1` sits IN 7d bucket (~5.6d post-merge); rolls off 2026-08-15T19:17Z (~8.6h AFTER tomorrow's scan → still-in tomorrow, then rolls off before 08-16 scan). `kaneo#1457` (~9.6d post-merge) is the oldest still-fully-in-30d entry. `Vibe-Trading#390` is 39.8d post-merge — outside strict 30d, retained here for context as top-60-by-updated.

## Closed No-Merge (last 30d) — 6

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08T12:48:51Z | continuing 7d bucket (day 6); still no post-close comment. Rolls off 2026-08-15T12:48Z (~2.1h AFTER tomorrow's scan → still-in tomorrow, then rolls off before 08-16 scan). |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z | 13.2d; off 7d closed_no_merge bucket since 08-08T06:11Z; still in 30d |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z | 15.6d, 3 comments — off 7d bucket since 08-05T20:47Z |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z | 17.9d, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z | 18.1d, 1 comment (bot-only) |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z | 18.7d, 4 comments, CHANGES_REQUESTED at file time |

## Archive-hidden (direct-fetch recoverable)

| Repo | PR | Title | State | Off 7d bucket | Notes |
|------|----|-------|-------|---------------|-------|
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | fix(deps): bump simple-git, tar, minimatch to patch critical CVEs (CVSS 9.8, 9.2, 8.7) | closed no-merge 2026-08-03T16:15:06Z | day 4 | 10.8d; still `archived: true`; still direct-fetch recoverable; in 30d bucket until 2026-09-02T16:15Z (per [[pr-tracker-search-drops-archived-repo-prs]]) |

## Lost (repo-deletion)

| Repo | PR | Title | Last-seen state | Lost at |
|------|----|-------|-----------------|---------|
| 0xprogrammable/aeon-launch-models | #1 | AEON models (draft, source review): NoOp, CapGate, DynamicFee | OPEN draft, CHANGES_REQUESTED 2026-08-07T17:57Z; author-response commit 2026-08-08T19:18Z | Detected 2026-08-11. Day 4 confirming (search + direct-fetch both 404). Owner still exists; 7 other repos intact (unchanged from 08-13). |

## Tomorrow's predicted tuple (scan 2026-08-15 ~10:30Z)

Letter-of-SKILL `(1, 6, 1, 3)` / Substantive `(1, 8, 1, 1)` — all values HOLD absent unexpected events:

- **recent_merges 1** (was 1): `aeon-programmable-hooks#1` still in 7d bucket tomorrow (~6.6d post-merge, rolls off 08-15T19:17Z ~8.6h AFTER tomorrow's scan → still-in tomorrow, out on 08-16 scan).
- **stale_open letter-of-SKILL 6** (was 6): six current stale hold; `PostHog#78346` scheduled-actions-posthog comment 08-13T08:00Z stays within 7d activity window through 08-20T08:00Z (~4.9d past tomorrow's scan → active); `Baileys#2732` github-actions comment 08-12T02:17Z stays within window through 08-19T02:17Z (~3.9d past tomorrow's scan → active). **Assumption**: no fresh substantive maintainer comments and no new stale-bot cycles on the six stale ones.
- **stale_open substantive 8** (was 8): both PostHog and Baileys inversions remain fingerprintable stale-bot noise; substantive activity unchanged.
- **closed_no_merge 1** (was 1): k-skill#547 continues in 7d bucket (rolls off 08-15T12:48Z ~2.1h AFTER tomorrow's scan → still-in tomorrow, out on 08-16 scan); no new closures anticipated.
- **active_open letter-of-SKILL 3** (was 3): aeon-programmable-hooks#2 still within 7d creation window (~4.9d tomorrow); PostHog#78346 + Baileys#2732 both letter-of-SKILL active via still-fresh stale-bot comments.
- **active_open substantive 1** (was 1): only aeon-programmable-hooks#2.

Predicted `(1, 6, 1, 3)` letter-of-SKILL / `(1, 8, 1, 1)` substantive. **Both merged and closed-no-merge slots roll off before the 08-16 scan** — day-after-tomorrow's predicted tuple is `(0, 6, 0, 3)` letter / `(0, 8, 0, 1)` substantive absent any fresh events. Confidence moderate on arithmetic; residual noise from unpredictable fresh stale-bot comments (n=2 class validated), maintainer sweeps, additional deletion/archive events. Class-4 (stale-bot inversion) remains the dominant predictor-miss driver — every OPEN PR crossing its repo's stale-bot day-14/day-7 window is a coin flip on the inversion event next scan.
