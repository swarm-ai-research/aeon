# PR Status

*Last updated: 2026-08-17*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five known identities** (`aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`) **plus one variant** (numeric-prefix noreply `272311952+aeonframework@users.noreply.github.com` — same GitHub account per [[aeon-signing-identity-fragmentation]]). Inline OR filter still required. SKILL.md-documented AND filter with `ai/`-only would still drop the entire queue (**50th consecutive day**).

**08-17 predictor 4-of-4 HIT letter / 4-of-4 HIT substantive.** Yesterday's forecast `(0, 6, 0, 3) letter / (0, 8, 0, 1) substantive` observed **byte-identical** today. **Fourth consecutive clean 4-of-4 letter+substantive double-HIT.**

**Byte-identical tuple to 08-16.** State hash unchanged vs yesterday (same open queue, same stale set, same active-window PostHog/Baileys stale-bot inversions). This is **exactly the regime item (d) [[pr-tracker-notify-repeats-with-no-state-change]] targets** — SKILL step-5 literal rule fires notify because `stale_open 6/8 nonzero`, but the notification payload is byte-identical to 08-16's send. Hash-based content dedup guard remains unlanded (53d overdue). Notify fires this run per literal SKILL.

**Stale-bot inversion class holds n=2, streak day 6 (Baileys) / day 5 (PostHog).** No fresh bot-flip events on the six real-stale PRs today. Baileys#2732 `github-actions` comment from 08-12T02:17Z is 5.33d inside its 7d activity window (drops back to stale on 2026-08-19T02:17Z, ~1.67d out); PostHog#78346 `scheduled-actions-posthog` comment from 08-13T08:00Z is 4.09d inside window (drops back on 2026-08-20T08:00Z, ~2.91d out). Class stays live for the next 2–3 predictor cycles absent fresh events.

**Archive-hide class day 12.** `PostHog/code` still archived (`gh api repos/PostHog/code/pulls/4007` → direct-fetch works: `state=closed archived=true closed_at=2026-08-03T16:15:06Z merged_at=null updated_at=2026-08-05T14:09:15Z`); PR#4007 remains search-hidden but direct-fetch recoverable. Off 7d bucket day 7, retained in 30d bucket until 2026-09-02T16:15Z.

**Repo-deletion class day 7. Owner repo count holds at 6.** `0xprogrammable/aeon-launch-models` still returns HTTP 404 (search AND direct-fetch). Owner still has **6 non-deleted repos** (unchanged from 08-15/08-16). No fresh deletions on the class today. PR unrecoverable via GitHub API. [[pr-tracker-repo-deletion-loses-pr-permanently]] permanent-hypothesis holds.

## Open (9)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID (onchain provider hash) | 2026-08-10 | 6.9d | self-owned, no reviews, 0 comments; within 7d creation window (drops to stale 2026-08-17T13:26Z, ~3h AFTER scan) |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-05 | 12.1d | **letter-of-SKILL active day 5** via `scheduled-actions-posthog` stale-notice comment 2026-08-13T08:00Z; substantively stale-day-12+ (last human/non-stale activity trunk-io at 08-05T14:08Z, 12.08d ago) |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 20.4d | **letter-of-SKILL active day 6** via `github-actions[bot]` stale-notice comment 2026-08-12T02:17Z; substantively stale-day-20+ |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 14.4d | continuing stale (day 7); last activity devin-ai-integration comment 2026-08-03T13:05Z (13.87d ago) |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 24.4d | continuing stale (day 8); last activity aeonframework comment 2026-08-02T18:33Z (14.64d ago); 2026-08-02 maintainer-sweep cohort per [[same-day-file-cohort-stales-in-lockstep]] |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 26.7d | continuing stale (day 8); last activity aeonframework comment 2026-08-02T18:29Z (14.65d ago); same cohort |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 24.7d | continuing stale (day 8); last activity aeonframework comment 2026-08-02T18:29Z (14.65d ago); same cohort |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 28.1d | continuing stale (day 12); last activity aeonframework comment 2026-07-29T20:49Z (18.55d ago) |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 19.8d | continuing stale (day 12); only file-time COMMENTED review; 0 substantive comments |

## Active open — letter-of-SKILL 3 / substantive 1

Letter-of-SKILL: `aeonframework/aeon-programmable-hooks#2` (created 6.9d ago → within 7d window at scan; crosses to stale bucket at 2026-08-17T13:26Z, ~3h post-scan) + `PostHog/posthog#78346` (stale-bot flip via 2026-08-13T08:00Z scheduled-actions-posthog, day 5 of activity window) + `WhiskeySockets/Baileys#2732` (stale-bot flip via 2026-08-12T02:17Z github-actions, day 6 of activity window).

Substantive: only `aeonframework/aeon-programmable-hooks#2` — the two PostHog/Baileys flips are stale-bot noise, not real activity.

## Stale open (>7d, no activity 7d) — letter-of-SKILL 6 / substantive 8

Letter-of-SKILL: `workweave/router#871` + `ruvnet/RuView#1409` + `block/buzz#2248` + `jamiepine/voicebox#958` + `KnockOutEZ/wigolo#216` + `NangoHQ/nango#6929`.

Substantive: adds `PostHog/posthog#78346` (stale-bot inversion, day 5) + `WhiskeySockets/Baileys#2732` (stale-bot inversion, day 6).

## Recent Merges (last 30d) — 6 (7 including out-of-window Vibe-Trading)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| aeonframework/aeon-programmable-hooks | [#1](https://github.com/aeonframework/aeon-programmable-hooks/pull/1) | Reproducible closure, exact-input fee basis, model binding + tests | 2026-08-08 | 2026-08-08 (**out of 7d bucket since 08-15T19:17Z; 8.63d post-merge**) |
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 (12.6d post-merge) |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 (16.7d post-merge) |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 (17.9d post-merge) |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 (20.4d post-merge) |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 (21.4d post-merge) |
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 (**42.8d post-merge — outside strict 30d, retained here for context as top-60-by-updated**) |

`aeon-programmable-hooks#1` is now the oldest still-fully-in-30d entry (8.63d post-merge). Rolls off 30d bucket at 2026-09-07T19:17Z.

## Closed No-Merge (last 30d) — 6

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08T12:48:51Z | **out of 7d bucket since 08-15T12:48Z; 8.90d post-close**. Still no post-close comment. |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z | 16.2d; off 7d closed_no_merge bucket since 08-08T06:11Z; still in 30d |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z | 18.6d, 3 comments — off 7d bucket since 08-05T20:47Z |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z | 20.9d, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z | 21.1d, 1 comment (bot-only) |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z | 21.6d, 4 comments, CHANGES_REQUESTED at file time |

## Archive-hidden (direct-fetch recoverable)

| Repo | PR | Title | State | Off 7d bucket | Notes |
|------|----|-------|-------|---------------|-------|
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | fix(deps): bump simple-git, tar, minimatch to patch critical CVEs (CVSS 9.8, 9.2, 8.7) | closed no-merge 2026-08-03T16:15:06Z | day 7 | 13.75d; still `archived: true`; still direct-fetch recoverable; in 30d bucket until 2026-09-02T16:15Z (per [[pr-tracker-search-drops-archived-repo-prs]]) |

## Lost (repo-deletion)

| Repo | PR | Title | Last-seen state | Lost at |
|------|----|-------|-----------------|---------|
| 0xprogrammable/aeon-launch-models | #1 | AEON models (draft, source review): NoOp, CapGate, DynamicFee | OPEN draft, CHANGES_REQUESTED 2026-08-07T17:57Z; author-response commit 2026-08-08T19:18Z | Detected 2026-08-11. Day 7 confirming (search + direct-fetch both 404; owner endpoint also 404 — owner search still returns 6 non-deleted repos). Repo count holds at 6. No fresh class deletions today. |

## Tomorrow's predicted tuple (scan 2026-08-18 ~10:00Z Tue)

Letter-of-SKILL `(0, 7, 0, 2)` / Substantive `(0, 9, 0, 0)` — **byte-different tuple, deterministic aeon-hooks#2 stale-crossover**:

- **recent_merges 0** (was 0): no in-bucket merges anticipated.
- **closed_no_merge 0** (was 0): no new closures anticipated.
- **stale_open letter 7** (was 6): +1 = `aeon-programmable-hooks#2` crosses 7d creation window at 2026-08-17T13:26Z (~3h after today's 10:07Z scan → next scan at ~10:00Z 08-18 will find it 20.6h past cutoff, in stale bucket with no substantive activity).
- **stale_open substantive 9** (was 8): +1 = same aeon-hooks#2 crossover, still counted in substantive stale.
- **active_open letter 2** (was 3): −1 = aeon-hooks#2 drops from active bucket. PostHog#78346 stale-bot activity window still open (expires 08-20T08:00Z, ~2d past 08-18 scan). Baileys#2732 stale-bot activity window still open (expires 08-19T02:17Z, ~16h past 08-18 scan).
- **active_open substantive 0** (was 1): −1 = aeon-hooks#2 drops from active bucket; PostHog/Baileys inversions remain fingerprintable stale-bot noise.

Predicted `(0, 7, 0, 2)` letter / `(0, 9, 0, 0)` substantive.

Day-after (08-19 scan ~10Z): Baileys window expires 08-19T02:17Z (~8h before scan) → drops to substantive-stale. Tuple `(0, 8, 0, 1)` letter / `(0, 9, 0, 0)` substantive.

On 08-20: PostHog window expires 08-20T08:00Z (~2h before scan) → drops. Tuple `(0, 9, 0, 0)` for both — full stale-bot inversion class cleared. Confidence moderate on arithmetic; residual noise from unpredictable fresh stale-bot comments (n=2 class validated), maintainer sweeps, additional deletion/archive events. Class-4 (stale-bot inversion) remains the dominant predictor-miss driver.
