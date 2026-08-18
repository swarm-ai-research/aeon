# PR Status

*Last updated: 2026-08-18*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five known identities** (`aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`) **plus one variant** (numeric-prefix noreply `272311952+aeonframework@users.noreply.github.com` — same GitHub account per [[aeon-signing-identity-fragmentation]]). Inline OR filter still required. SKILL.md-documented AND filter with `ai/`-only would still drop the entire queue (**51st consecutive day**).

**08-18 predictor 4-of-4 HIT letter / 4-of-4 HIT substantive.** Yesterday's forecast `(0, 7, 0, 2) letter / (0, 9, 0, 0) substantive` observed **exact** today. **Fifth consecutive clean 4-of-4 letter+substantive double-HIT.** Deterministic transition confirmed: `aeonframework/aeon-programmable-hooks#2` crossed 7d-age threshold at 2026-08-17T13:26Z (post-yesterday-scan), moving from active→stale in both letter and substantive tuples. No other state changes.

**Notify payload changed vs 08-16/08-17 (was byte-frozen 3 days).** The aeon-hooks#2 active→stale rotation shifts the stale set by +1 entry — first hash-differing payload since 08-15. Regime item (d) [[pr-tracker-notify-repeats-with-no-state-change]] pause does NOT trigger this run (payload genuinely changed). `notify` script's own hash-dedup layer is active (observed first-call send, second-call `duplicate message (hash 0e6503c1), skipping`) — separate from SKILL-level dedup guard which remains unlanded (54d overdue).

**Stale-bot inversion class holds n=2, streak day 7 (Baileys) / day 6 (PostHog).** No fresh bot-flip events on the seven real-stale PRs today. Baileys#2732 `github-actions` comment from 08-12T02:17Z is 6.35d inside its 7d activity window (drops back to stale on 2026-08-19T02:17Z, ~0.65d out — **fires tomorrow's scan**); PostHog#78346 `scheduled-actions-posthog` comment from 08-13T08:00Z is 5.09d inside window (drops back on 2026-08-20T08:00Z, ~1.91d out). Class stays live for 1–2 more predictor cycles absent fresh events.

**Archive-hide class day 13.** `PostHog/code` still archived (`gh api repos/PostHog/code/pulls/4007` → direct-fetch: `state=closed archived=true closed_at=2026-08-03T16:15:06Z merged_at=null updated_at=2026-08-05T14:09:15Z`); PR#4007 remains search-hidden but direct-fetch recoverable. Off 7d bucket day 8, retained in 30d bucket until 2026-09-02T16:15Z.

**Repo-deletion class day 8. Owner repo count holds at 6.** `0xprogrammable/aeon-launch-models` still returns HTTP 404 (search AND direct-fetch). Owner still has **6 non-deleted repos** (unchanged from 08-15/08-16/08-17). No fresh deletions on the class today. PR unrecoverable via GitHub API. [[pr-tracker-repo-deletion-loses-pr-permanently]] permanent-hypothesis holds.

## Open (9)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-05 | 13.1d | **letter-of-SKILL active day 6** via `scheduled-actions-posthog` stale-notice comment 2026-08-13T08:00Z; substantively stale-day-13+ (last human/non-stale activity trunk-io at 08-05T14:08Z, 13.09d ago) |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 21.4d | **letter-of-SKILL active day 7** via `github-actions[bot]` stale-notice comment 2026-08-12T02:17Z; substantively stale-day-21+; **drops back to stale tomorrow 2026-08-19T02:17Z** |
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID (onchain provider hash) | 2026-08-10 | 7.9d | self-owned, no reviews, 0 comments; **JUST crossed 7d-age threshold — moved active→stale today per [[pr-tracker-scan-vs-cutoff-hour-bug-is-bidirectional]] deterministic rollover** |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 15.4d | continuing stale (day 8); last activity devin-ai-integration comment 2026-08-03T13:05Z (14.87d ago) |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 25.4d | continuing stale (day 9); last activity aeonframework comment 2026-08-02T18:33Z (15.64d ago); 2026-08-02 maintainer-sweep cohort per [[same-day-file-cohort-stales-in-lockstep]] |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 27.7d | continuing stale (day 9); last activity aeonframework comment 2026-08-02T18:29Z (15.65d ago); same cohort |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 25.7d | continuing stale (day 9); last activity aeonframework comment 2026-08-02T18:29Z (15.65d ago); same cohort |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 29.1d | continuing stale (day 13); last activity aeonframework comment 2026-07-29T20:49Z (19.55d ago) |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 20.8d | continuing stale (day 13); only file-time COMMENTED review; 0 substantive comments |

## Active open — letter-of-SKILL 2 / substantive 0

Letter-of-SKILL: `PostHog/posthog#78346` (stale-bot flip via 2026-08-13T08:00Z scheduled-actions-posthog, day 6 of activity window) + `WhiskeySockets/Baileys#2732` (stale-bot flip via 2026-08-12T02:17Z github-actions, day 7 of activity window — final day, drops tomorrow).

Substantive: **0** — both PostHog/Baileys flips are stale-bot noise, not real activity. `aeon-programmable-hooks#2` moved out of active (crossed 7d threshold at 2026-08-17T13:26Z).

## Stale open (>7d, no activity 7d) — letter-of-SKILL 7 / substantive 9

Letter-of-SKILL: `aeonframework/aeon-programmable-hooks#2` (**new to bucket** — crossed 7d-age threshold 08-17T13:26Z, pre-scan today) + `workweave/router#871` + `ruvnet/RuView#1409` + `block/buzz#2248` + `jamiepine/voicebox#958` + `KnockOutEZ/wigolo#216` + `NangoHQ/nango#6929`.

Substantive: adds `PostHog/posthog#78346` (stale-bot inversion, day 6) + `WhiskeySockets/Baileys#2732` (stale-bot inversion, day 7).

## Recent Merges (last 30d) — 6

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| aeonframework/aeon-programmable-hooks | [#1](https://github.com/aeonframework/aeon-programmable-hooks/pull/1) | Reproducible closure, exact-input fee basis, model binding + tests | 2026-08-08 | 2026-08-08 (10.02d post-merge; out of 7d bucket) |
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 (13.6d post-merge) |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 (17.7d post-merge) |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 (18.9d post-merge) |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 (21.4d post-merge) |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 (22.4d post-merge) |

**Zero merges in 7d bucket** — aeon-programmable-hooks#1 rolled off 08-15T19:17Z, no merges since. Next roll-off: usekaneo/kaneo#1457 at 2026-09-03T19:59Z. Empty-7d-merge-bucket streak day 3.

## Closed No-Merge (last 30d) — 6

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08T12:48:51Z | 10.02d post-close; out of 7d bucket. Still no post-close comment. |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z | 17.2d; off 7d closed_no_merge bucket since 08-08T06:11Z; still in 30d |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z | 19.6d, 3 comments — off 7d bucket since 08-05T20:47Z |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z | 21.9d, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z | 22.1d, 1 comment (bot-only) |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z | 22.6d, 4 comments, CHANGES_REQUESTED at file time |

**Zero closes in 7d bucket** — k-skill#547 rolled off 08-15T12:48Z. Empty-7d-closed-bucket streak day 3.

## Archive-hidden (direct-fetch recoverable)

| Repo | PR | Title | State | Off 7d bucket | Notes |
|------|----|-------|-------|---------------|-------|
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | fix(deps): bump simple-git, tar, minimatch to patch critical CVEs (CVSS 9.8, 9.2, 8.7) | closed no-merge 2026-08-03T16:15:06Z | day 8 | 14.75d; still `archived: true`; still direct-fetch recoverable; in 30d bucket until 2026-09-02T16:15Z (per [[pr-tracker-search-drops-archived-repo-prs]]) |

## Lost (repo-deletion)

| Repo | PR | Title | Last-seen state | Lost at |
|------|----|-------|-----------------|---------|
| 0xprogrammable/aeon-launch-models | #1 | AEON models (draft, source review): NoOp, CapGate, DynamicFee | OPEN draft, CHANGES_REQUESTED 2026-08-07T17:57Z; author-response commit 2026-08-08T19:18Z | Detected 2026-08-11. Day 8 confirming (search + direct-fetch both 404; owner endpoint returns 200 with 6 non-deleted repos, count unchanged). No fresh class deletions today. |

## Tomorrow's predicted tuple (scan 2026-08-19 ~10:00Z Wed)

**Letter:** `(0, 8, 0, 1)` — merged 7d unchanged (next roll-off 09-03), closed 7d unchanged, active→stale rotation on `WhiskeySockets/Baileys#2732` at 2026-08-19T02:17Z (drops 8h pre-scan), so stale bucket +1 to 8, active bucket −1 to 1 (only PostHog#78346 remains bot-flipped).

**Substantive:** `(0, 9, 0, 0)` — unchanged; the Baileys flip was already substantively-stale, so the letter-vs-substantive delta narrows from 2 to 1.

**Notify prediction:** payload will differ from today (Baileys moves buckets), so no hash-dedup skip at notify layer.
