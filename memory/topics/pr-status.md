# PR Status

*Last updated: 2026-08-13*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five known identities** (`aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`) **plus one variant** (numeric-prefix noreply `272311952+aeonframework@users.noreply.github.com` — same GitHub account per [[aeon-signing-identity-fragmentation]]). Inline OR filter still required. SKILL.md-documented AND filter with `ai/`-only would still drop the entire queue (**46th consecutive day**).

**NEW recurrence — stale-bot inversion class hits its 2nd consecutive day.** `PostHog/posthog#78346` (opened 08-05) received a stale-notice comment at 2026-08-13T08:00:17Z by `scheduled-actions-posthog` (body: `This PR hasn't seen activity in a week! Should it be merged, closed, or further reviewed?`). Same class as yesterday's `WhiskeySockets/Baileys#2732` github-actions[bot] flip. Letter-of-SKILL flips `PostHog#78346` from stale (frozen 7.87d) → active_open via the fresh comment; substantively it IS the stale-confirmation event. Two consecutive days = the class is systematic, not idiosyncratic — [[pr-tracker-stale-bot-comment-inverts-stale-classification]] is now a n=2 recurrence with distinct bot handles (`github-actions` on Baileys, `scheduled-actions-posthog` on PostHog). Fix path unchanged: fingerprint by body ("stale", "hasn't seen activity", "marked as stale"), not by author-login allowlist — different repos ship different named stale-bot handles.

**Predictor 3-of-4 HIT letter-of-SKILL / 2-of-4 substantive** — 08-12 predicted 08-13 tuple `(1, 7, 1, 2)`; observed letter-of-SKILL `(1, 6, 1, 3)` (missed stale_open by −1 and active_open by +1 — same driver as yesterday's Baileys miss: fresh stale-bot comment inversion on PostHog#78346); observed substantive `(1, 8, 1, 1)` (missed stale_open by +1, active_open by −1). recent_merges HIT (aeon-programmable-hooks#1 still in 7d bucket ~4.7d post-merge). closed_no_merge HIT (k-skill#547 continuing). Baileys#2732 stayed letter-of-SKILL active via 08-12 github-actions comment (still within 7d activity window).

**Repo-deletion class persists day 3.** `0xprogrammable/aeon-launch-models` still returns HTTP 404 (search AND direct-fetch). Owner user still exists with 7 non-deleted repos (was 6 yesterday, +1 net repo activity outside the aeon PR queue). PR unrecoverable via GitHub API. [[pr-tracker-repo-deletion-loses-pr-permanently]] permanent-hypothesis holds.

**Archive-hide class persists day 8.** `PostHog/code` still archived (`gh api repos/PostHog/code` → `archived: true`); PR#4007 remains search-hidden but direct-fetch recoverable (`state=closed closed_at=2026-08-03T16:15:06Z merged_at=null`). Off 7d bucket day 3, retained in 30d bucket until 2026-09-02.

**Indexing-lag class resolved as one-time recoverable.** `aeonframework/aeon-programmable-hooks#1` (yesterday's new class) now surfaces cleanly in today's search results and drops naturally into the recent_merges bucket. Confirms yesterday's classification: [[pr-tracker-search-indexing-lag-drops-self-owned-prs]] is a transient eventual-consistency artifact, not a persistent class like the archive/deletion classes.

## Open (9)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID (onchain provider hash) | 2026-08-10 | 2.9d | self-owned, no reviews, 0 comments; within 7d creation window |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-05 | 7.9d | **letter-of-SKILL active** via `scheduled-actions-posthog` stale-notice comment 2026-08-13T08:00Z; substantively stale-day-1 (last human/bot-non-stale activity trunk-io at 08-05T14:08Z, 7.87d ago) |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 15.5d | **letter-of-SKILL active day 2** via `github-actions[bot]` stale-notice comment 2026-08-12T02:17Z; substantively stale-day-15+ |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 10.5d | continuing stale (day 3); last activity devin-ai-integration comment 2026-08-03T13:05Z (9.9d ago) |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 20.5d | continuing stale (day 4); last activity aeonframework comment 2026-08-02T18:33Z (10.7d ago); 2026-08-02 maintainer-sweep cohort per [[same-day-file-cohort-stales-in-lockstep]] |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 22.7d | continuing stale (day 4); last activity aeonframework comment 2026-08-02T18:29Z (10.7d ago); same cohort |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 20.8d | continuing stale (day 4); last activity aeonframework comment 2026-08-02T18:29Z (10.7d ago); same cohort |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 24.1d | continuing stale (day 8); last activity aeonframework comment 2026-07-29T20:49Z (14.6d ago) |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 15.8d | continuing stale (day 8); only file-time COMMENTED review; 0 substantive comments |

## Active open — letter-of-SKILL 3 / substantive 1

Letter-of-SKILL: `aeonframework/aeon-programmable-hooks#2` (created 2.9d ago → within 7d window) + `PostHog/posthog#78346` (stale-bot flip via 2026-08-13T08:00Z scheduled-actions-posthog) + `WhiskeySockets/Baileys#2732` (stale-bot flip via 2026-08-12T02:17Z github-actions, day 2 of activity window).

Substantive: only `aeonframework/aeon-programmable-hooks#2` — the two PostHog/Baileys flips are stale-bot noise, not real activity.

## Stale open (>7d, no activity 7d) — letter-of-SKILL 6 / substantive 8

Letter-of-SKILL: `workweave/router#871` + `ruvnet/RuView#1409` + `block/buzz#2248` + `jamiepine/voicebox#958` + `KnockOutEZ/wigolo#216` + `NangoHQ/nango#6929`.

Substantive: adds `PostHog/posthog#78346` (stale-bot inversion) + `WhiskeySockets/Baileys#2732` (stale-bot inversion, day 2 of inversion).

## Recent Merges (last 30d) — 7

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| aeonframework/aeon-programmable-hooks | [#1](https://github.com/aeonframework/aeon-programmable-hooks/pull/1) | Reproducible closure, exact-input fee basis, model binding + tests | 2026-08-08 | 2026-08-08 |
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

`aeon-programmable-hooks#1` sits IN 7d bucket (~4.7d post-merge); rolls off 2026-08-15T19:17Z (~1.3d after tomorrow's scan → still-in tomorrow, then rolls off before 08-15). `Vibe-Trading#390` is the oldest merge still within 30d (~41d in absolute age from creation, ~39d from merge; drops off 30d table at 2026-08-04T merge+30 → already outside 30d strict, retained here for context as top-60-by-updated). Actually correction: Vibe-Trading#390 merged 2026-07-05, so it's at 39d — outside strict 30d, but appears in top-60 search sort; kaneo#1457 (~9d post-merge) is the true oldest in-window.

## Closed No-Merge (last 30d) — 6

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08T12:48:51Z | continuing 7d bucket (day 5); still no post-close comment. Rolls off 2026-08-15T12:48Z (~26h after tomorrow's scan → still-in tomorrow). |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z | 12.2d; off 7d closed_no_merge bucket since 08-08T06:11Z; still in 30d |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z | 14.6d, 3 comments — off 7d bucket since 08-05T20:47Z |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z | 17.0d, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z | 17.1d, 1 comment (bot-only) |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z | 17.6d, 4 comments, CHANGES_REQUESTED at file time |

## Archive-hidden (direct-fetch recoverable)

| Repo | PR | Title | State | Off 7d bucket | Notes |
|------|----|-------|-------|---------------|-------|
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | fix(deps): bump simple-git, tar, minimatch to patch critical CVEs (CVSS 9.8, 9.2, 8.7) | closed no-merge 2026-08-03T16:15:06Z | day 3 | 9.8d; still `archived: true`; still direct-fetch recoverable; in 30d bucket until 2026-09-02T16:15Z (per [[pr-tracker-search-drops-archived-repo-prs]]) |

## Lost (repo-deletion)

| Repo | PR | Title | Last-seen state | Lost at |
|------|----|-------|-----------------|---------|
| 0xprogrammable/aeon-launch-models | #1 | AEON models (draft, source review): NoOp, CapGate, DynamicFee | OPEN draft, CHANGES_REQUESTED 2026-08-07T17:57Z; author-response commit 2026-08-08T19:18Z | Detected 2026-08-11. Day 3 confirming (search + direct-fetch both 404). Owner still exists; 7 other repos intact (was 6 yesterday, +1 unrelated). |

## Tomorrow's predicted tuple (scan 2026-08-14 ~10:30Z)

Letter-of-SKILL `(1, 6, 1, 3)` / Substantive `(1, 8, 1, 1)` — most values HOLD absent unexpected events:

- **recent_merges 1** (was 1): `aeon-programmable-hooks#1` still in 7d bucket tomorrow (~5.7d post-merge, rolls off 08-15T19:17Z ~33h after tomorrow's scan).
- **stale_open letter-of-SKILL 6** (was 6): six current stale hold; `PostHog#78346` scheduled-actions-posthog comment at 08-13T08:00Z stays within 7d activity window through 08-20T08:00Z (~6d past tomorrow's scan → active); `Baileys#2732` github-actions comment at 08-12T02:17Z stays within window through 08-19T02:17Z (~5d past tomorrow's scan → active). **Assumption**: no fresh substantive maintainer comments on the six stale ones.
- **stale_open substantive 8** (was 8): both PostHog and Baileys inversions remain fingerprintable stale-bot noise; substantive activity unchanged.
- **closed_no_merge 1** (was 1): k-skill#547 continues in 7d bucket (rolls off 08-15T12:48Z ~26h after tomorrow's scan); no new closures anticipated.
- **active_open letter-of-SKILL 3** (was 3): aeon-programmable-hooks#2 still within 7d creation window (~3.9d tomorrow); PostHog#78346 + Baileys#2732 both letter-of-SKILL active via still-fresh stale-bot comments.
- **active_open substantive 1** (was 1): only aeon-programmable-hooks#2.

Predicted `(1, 6, 1, 3)` letter-of-SKILL / `(1, 8, 1, 1)` substantive. Confidence moderate on arithmetic; residual noise from unpredictable fresh stale-bot comments (n=2 class validated), maintainer sweeps, additional deletion/archive events. Class-4 (stale-bot inversion) is now the dominant predictor-miss driver — every OPEN PR crossing its repo's stale-bot day-14/day-7 window is a coin flip on the inversion event next scan.
