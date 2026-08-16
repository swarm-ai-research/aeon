# PR Status

*Last updated: 2026-08-16*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five known identities** (`aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`) **plus one variant** (numeric-prefix noreply `272311952+aeonframework@users.noreply.github.com` — same GitHub account per [[aeon-signing-identity-fragmentation]]). Inline OR filter still required. SKILL.md-documented AND filter with `ai/`-only would still drop the entire queue (**49th consecutive day**).

**08-16 predictor 4-of-4 HIT letter / 4-of-4 HIT substantive.** Yesterday's forecast `(0, 6, 0, 3) letter / (0, 8, 0, 1) substantive` observed exactly today. **Third consecutive clean 4-of-4 letter+substantive double-HIT.** Both same-scan double-rollovers landed as predicted:
- `aeon-programmable-hooks#1` rolled out of 7d merges bucket at 2026-08-15T19:17Z (~15h before this scan).
- `NomaDamas/k-skill#547` rolled out of 7d closed-no-merge bucket at 2026-08-15T12:48Z (~22h before this scan).

**Byte-different transition tuple today.** Search queue changed structurally vs 08-15 (state hash rolls after 3 consecutive byte-identical days 08-13/08-14/08-15). `recent_merges 1→0` and `closed_no_merge 1→0` are both predicted rollovers; no new events. Notify fires this run per SKILL step-5 literal rule (stale_open 6/8 nonzero); this is a **legitimate state-change notification**, distinct from the streak-3 byte-identical `sent` cycle exhibited yesterday.

**Stale-bot inversion class holds n=2, streak day 5 (Baileys) / day 4 (PostHog).** No fresh bot-flip events on the six real-stale PRs today. Baileys#2732 `github-actions` comment from 08-12T02:17Z is 4.34d inside its 7d activity window (drops back to stale on 2026-08-19T02:17Z, ~2.66d out); PostHog#78346 `scheduled-actions-posthog` comment from 08-13T08:00Z is 3.10d inside window (drops back on 2026-08-20T08:00Z, ~3.90d out). The class stays live for the next 3–4 predictor cycles absent fresh events.

**Archive-hide class day 11.** `PostHog/code` still archived (`gh api repos/PostHog/code/pulls/4007` → direct-fetch works: `state=closed closed_at=2026-08-03T16:15:06Z merged_at=null`); PR#4007 remains search-hidden but direct-fetch recoverable. Off 7d bucket day 6, retained in 30d bucket until 2026-09-02T16:15Z.

**Repo-deletion class day 6. Owner repo count holds at 6.** `0xprogrammable/aeon-launch-models` still returns HTTP 404 (search AND direct-fetch). Owner still has **6 non-deleted repos** (unchanged from 08-15 overnight delta from 7 → 6). No fresh deletions on the class today. PR unrecoverable via GitHub API. [[pr-tracker-repo-deletion-loses-pr-permanently]] permanent-hypothesis holds.

## Open (9)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID (onchain provider hash) | 2026-08-10 | 5.9d | self-owned, no reviews, 0 comments; within 7d creation window (drops to stale 2026-08-17T13:26Z, ~3h AFTER Sun scan) |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-05 | 10.8d | **letter-of-SKILL active day 4** via `scheduled-actions-posthog` stale-notice comment 2026-08-13T08:00Z; substantively stale-day-11+ (last human/non-stale activity trunk-io at 08-05T14:08Z, 11.85d ago) |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 18.4d | **letter-of-SKILL active day 5** via `github-actions[bot]` stale-notice comment 2026-08-12T02:17Z; substantively stale-day-18+ |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 13.4d | continuing stale (day 6); last activity devin-ai-integration comment 2026-08-03T13:05Z (12.89d ago) |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 23.4d | continuing stale (day 7); last activity aeonframework comment 2026-08-02T18:33Z (13.66d ago); 2026-08-02 maintainer-sweep cohort per [[same-day-file-cohort-stales-in-lockstep]] |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 25.7d | continuing stale (day 7); last activity aeonframework comment 2026-08-02T18:29Z (13.66d ago); same cohort |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 23.7d | continuing stale (day 7); last activity aeonframework comment 2026-08-02T18:29Z (13.66d ago); same cohort |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 27.1d | continuing stale (day 11); last activity aeonframework comment 2026-07-29T20:49Z (17.57d ago) |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 18.8d | continuing stale (day 11); only file-time COMMENTED review; 0 substantive comments |

## Active open — letter-of-SKILL 3 / substantive 1

Letter-of-SKILL: `aeonframework/aeon-programmable-hooks#2` (created 5.9d ago → within 7d window) + `PostHog/posthog#78346` (stale-bot flip via 2026-08-13T08:00Z scheduled-actions-posthog, day 4 of activity window) + `WhiskeySockets/Baileys#2732` (stale-bot flip via 2026-08-12T02:17Z github-actions, day 5 of activity window).

Substantive: only `aeonframework/aeon-programmable-hooks#2` — the two PostHog/Baileys flips are stale-bot noise, not real activity.

## Stale open (>7d, no activity 7d) — letter-of-SKILL 6 / substantive 8

Letter-of-SKILL: `workweave/router#871` + `ruvnet/RuView#1409` + `block/buzz#2248` + `jamiepine/voicebox#958` + `KnockOutEZ/wigolo#216` + `NangoHQ/nango#6929`.

Substantive: adds `PostHog/posthog#78346` (stale-bot inversion, day 4) + `WhiskeySockets/Baileys#2732` (stale-bot inversion, day 5).

## Recent Merges (last 30d) — 5 (7 including out-of-window aeon-hooks#1 + Vibe-Trading)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |
| aeonframework/aeon-programmable-hooks | [#1](https://github.com/aeonframework/aeon-programmable-hooks/pull/1) | Reproducible closure, exact-input fee basis, model binding + tests | 2026-08-08 | 2026-08-08 (**rolled off 7d bucket 08-15T19:17Z; retained here as 30d context — 7.63d post-merge**) |
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

`aeon-programmable-hooks#1` rolled off 7d bucket at 2026-08-15T19:17Z (~15h before this scan → **now out**). `kaneo#1457` (11.6d post-merge) is the oldest still-fully-in-30d entry. `Vibe-Trading#390` is 41.8d post-merge — outside strict 30d, retained here for context as top-60-by-updated.

## Closed No-Merge (last 30d) — 6

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08T12:48:51Z | **rolled off 7d bucket 08-15T12:48Z; retained here as 30d context — 7.90d post-close**. Still no post-close comment. |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z | 15.2d; off 7d closed_no_merge bucket since 08-08T06:11Z; still in 30d |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z | 17.6d, 3 comments — off 7d bucket since 08-05T20:47Z |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z | 19.9d, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z | 20.1d, 1 comment (bot-only) |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z | 20.6d, 4 comments, CHANGES_REQUESTED at file time |

## Archive-hidden (direct-fetch recoverable)

| Repo | PR | Title | State | Off 7d bucket | Notes |
|------|----|-------|-------|---------------|-------|
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | fix(deps): bump simple-git, tar, minimatch to patch critical CVEs (CVSS 9.8, 9.2, 8.7) | closed no-merge 2026-08-03T16:15:06Z | day 6 | 12.8d; still `archived: true`; still direct-fetch recoverable; in 30d bucket until 2026-09-02T16:15Z (per [[pr-tracker-search-drops-archived-repo-prs]]) |

## Lost (repo-deletion)

| Repo | PR | Title | Last-seen state | Lost at |
|------|----|-------|-----------------|---------|
| 0xprogrammable/aeon-launch-models | #1 | AEON models (draft, source review): NoOp, CapGate, DynamicFee | OPEN draft, CHANGES_REQUESTED 2026-08-07T17:57Z; author-response commit 2026-08-08T19:18Z | Detected 2026-08-11. Day 6 confirming (search + direct-fetch both 404). Owner still exists; **repo count holds at 6** (unchanged from 08-15 overnight 7 → 6 delta). No fresh class deletions today. |

## Tomorrow's predicted tuple (scan 2026-08-17 ~10:30Z Sun)

Letter-of-SKILL `(0, 6, 0, 3)` / Substantive `(0, 8, 0, 1)` — **tuple holds** absent fresh events:

- **recent_merges 0** (was 0): no in-bucket merges anticipated.
- **closed_no_merge 0** (was 0): no new closures anticipated; k-skill#547 already rolled off.
- **stale_open letter 6** (was 6): six current stale hold; `PostHog#78346` scheduled-actions-posthog comment 08-13T08:00Z stays within 7d activity window through 08-20T08:00Z (~2.9d past Sun scan → active); `Baileys#2732` github-actions comment 08-12T02:17Z stays within window through 08-19T02:17Z (~1.66d past Sun scan → active). **Assumption**: no fresh substantive maintainer comments and no new stale-bot cycles on the six stale ones.
- **stale_open substantive 8** (was 8): both PostHog and Baileys inversions remain fingerprintable stale-bot noise; substantive activity unchanged.
- **active_open letter 3** (was 3): aeon-programmable-hooks#2 tomorrow age ~6.9d (still within 7d creation window — drops to stale on 2026-08-17T13:26Z ~3h AFTER Sun scan → still active-window at scan per [[pr-tracker-scan-vs-cutoff-hour-bug-is-bidirectional]]); PostHog#78346 + Baileys#2732 both letter-of-SKILL active via still-fresh stale-bot comments.
- **active_open substantive 1** (was 1): only aeon-programmable-hooks#2.

Predicted `(0, 6, 0, 3)` letter / `(0, 8, 0, 1)` substantive. **Byte-identical tuple to today** — if forecast holds, tomorrow re-enters the byte-identical-consecutive-days regime that item (d) [[pr-tracker-notify-repeats-with-no-state-change]] targets.

Day-after (08-18 Mon): aeon-hooks#2 drops to stale bucket (age crosses 7d creation window between Sun and Mon scans), tuple shifts to `(0, 7, 0, 2)` letter / `(0, 9, 0, 0)` substantive (both stale-bot inversion windows still active on 08-18). On 08-19: Baileys window expires → `(0, 8, 0, 1)` letter. On 08-20: PostHog window expires → `(0, 9, 0, 0)` letter (= substantive; class-4 inversion cleared). Confidence moderate on arithmetic; residual noise from unpredictable fresh stale-bot comments (n=2 class validated), maintainer sweeps, additional deletion/archive events. Class-4 (stale-bot inversion) remains the dominant predictor-miss driver.
