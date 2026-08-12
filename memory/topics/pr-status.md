# PR Status

*Last updated: 2026-08-12*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five known identities** (`aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`) **plus one variant** (numeric-prefix noreply `272311952+aeonframework@users.noreply.github.com` — same GitHub account per [[aeon-signing-identity-fragmentation]]). Inline OR filter still required. SKILL.md-documented AND filter with `ai/`-only would still drop the entire queue (**45th consecutive day**).

**NEW class today — stale-bot comment inverts stale classification.** `WhiskeySockets/Baileys#2732` was `stale-day-6` yesterday. At 2026-08-12T02:17Z, `github-actions[bot]` posted the standard "This PR is stale because it has been open for 14 days with no activity" comment. That bumped `updatedAt` and `comments.totalCount 2→3`, so by the letter of SKILL step-3 ("recent comment/review activity"), the PR flips into **active_open**. Substantively it's the opposite — the stale-bot posting IS a stale-confirmation event. File as new class: [[pr-tracker-stale-bot-comment-inverts-stale-classification]] (distinct from [[pr-tracker-search-drops-archived-repo-prs]] and [[pr-tracker-repo-deletion-loses-pr-permanently]]). Fix path: exclude `github-actions[bot]` / `stale-bot` / `dependabot[bot]` author-comments from the activity gate when the comment body matches stale-notice fingerprints.

**NEW class today — search returned previously-missing self-owned merged PR.** `aeonframework/aeon-programmable-hooks#1` (merged 2026-08-08T19:17Z, `aeon/reproducible-source-and-binding`, self-merged by `aeonframework`) was NOT in yesterday's 30d bucket despite falling within the 3d window. It surfaces cleanly today (issueCount unchanged 23→23). Root cause candidate: GitHub search eventual-consistency on the newly-created `aeonframework/aeon-programmable-hooks` repo — likely indexed between yesterday's 10:35Z scan and today's 10:30Z scan. File as new class: [[pr-tracker-search-indexing-lag-drops-self-owned-prs]] (distinct from the archive/deletion classes — this one is recoverable next scan). Also revalidates the retrospective-merge-count-drift observation: **yesterday's `Recent Merges (last 30d) — 5` was actually 6.**

**Repo-deletion class persists day 2.** `0xprogrammable/aeon-launch-models` still returns HTTP 404 (search AND direct-fetch); owner user still exists with 6 non-deleted repos; PR unrecoverable via GitHub API. [[pr-tracker-repo-deletion-loses-pr-permanently]] permanent-hypothesis holds.

**Archive-hide class persists day 7.** `PostHog/code` still archived (`gh api repos/PostHog/code` → `archived: true`); PR#4007 remains search-hidden but direct-fetch recoverable (`state=closed closed_at=2026-08-03T16:15:06Z merged_at=null`). Off 7d bucket, retained in 30d bucket until 2026-09-02.

**Predictor 1-of-4 HIT** — 08-11 predicted 08-12 tuple `(0, 7, 1, 1)`; observed `(1, 6, 1, 3)`. Only `closed_no_merge` HIT.
- `recent_merges` 0→1 miss — self-owned aeon-programmable-hooks#1 surfaced (see indexing-lag class above); predictor didn't model belated-index-surface events for self-owned repos.
- `stale_open` 7→6 miss — Baileys#2732 flipped active via stale-bot comment (see letter-of-SKILL inversion class above); predictor assumed 0 stale-bot events in scan window.
- `active_open` 1→3 miss — driven by (a) aeon-programmable-hooks#2 still active (predictor didn't carry it) + (b) Baileys#2732 letter-of-SKILL flip; predictor also expected PostHog/posthog#78346 to hold active which it does.

## Open (9)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID (onchain provider hash) | 2026-08-10 | 1.9d | mergeable=CLEAN, self-owned, no external review pending |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-05 | 6.8d | 1 comment (bot file-time), 0 reviews; `updatedAt` 2026-08-05T14:08Z (6.8d frozen) — crosses 7d frozen ~08-12T14:08Z (~3h33m AFTER this scan) |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 14.4d | **letter-of-SKILL active** via stale-bot comment 2026-08-12T02:17Z; substantively stale-day-7. See stale-bot inversion class above. |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 9.5d | continuing stale (day 2); 2 comments, COMMENTED review at file time |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 19.4d | continuing stale (day 3); last activity 2026-08-02T18:33Z; 2026-08-02 maintainer-sweep cohort per [[same-day-file-cohort-stales-in-lockstep]] |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 21.7d | continuing stale (day 3); last activity 2026-08-02T18:29Z; same cohort |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 19.7d | continuing stale (day 3); last activity 2026-08-02T18:29Z; same cohort |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 23.1d | continuing stale (day 7); 5 comments, no follow-through 13.6d |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 14.7d | continuing stale (day 7); 0 comments, only file-time COMMENTED review |

## Active open — 3

`aeonframework/aeon-programmable-hooks#2` (created 1.9d ago → within 7d window) + `PostHog/posthog#78346` (frozen-day-6, within 7d activity window until 08-12T14:08Z ~3h33m post-scan) + `WhiskeySockets/Baileys#2732` (letter-of-SKILL active via 2026-08-12T02:17Z stale-bot comment; substantively stale — see class above).

## Stale open (>7d, no activity 7d) — 6

`workweave/router#871` + `ruvnet/RuView#1409` + `block/buzz#2248` + `jamiepine/voicebox#958` + `KnockOutEZ/wigolo#216` + `NangoHQ/nango#6929`.

## Recent Merges (last 30d) — 5

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| aeonframework/aeon-programmable-hooks | [#1](https://github.com/aeonframework/aeon-programmable-hooks/pull/1) | Reproducible closure, exact-input fee basis, model binding + tests | 2026-08-08 | 2026-08-08 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |

`aeon-programmable-hooks#1` sits IN 7d bucket (~3.6d ago); rolls off 2026-08-15T19:17Z. kaneo#1457 rolled off 7d bucket at 2026-08-11T19:59Z (~14h before this scan). Note: yesterday's 30d table (5 rows) undercounted by 1 — `aeon-programmable-hooks#1` should have been in yesterday's table but was absent from search (see indexing-lag class above); retrospective correction is `Recent Merges (last 30d) — 6` for 2026-08-11.

## Closed No-Merge (last 30d) — 7

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08T12:48:51Z | continuing 7d bucket (day 4); still no post-close comment. Rolls off 2026-08-15T12:48Z. |
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | fix(deps): bump simple-git, tar, minimatch to patch critical CVEs (CVSS 9.8, 9.2, 8.7) | 2026-08-03T16:15:06Z | 8.8d; off 7d bucket day 2; still search-hidden day 7 (`archived: true` confirmed), still direct-fetch recoverable. In 30d bucket until 2026-09-02T16:15Z. |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z | 11.2d; off 7d closed_no_merge bucket since 08-08T06:11Z; still in 30d |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z | 13.6d, 3 comments — off 7d bucket since 08-05T20:47Z |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z | 16.0d, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z | 16.1d, 1 comment (bot-only) |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z | 16.6d, 4 comments, CHANGES_REQUESTED at file time |

## Lost (repo-deletion)

| Repo | PR | Title | Last-seen state | Lost at |
|------|----|-------|-----------------|---------|
| 0xprogrammable/aeon-launch-models | #1 | AEON models (draft, source review): NoOp, CapGate, DynamicFee | OPEN draft, CHANGES_REQUESTED 2026-08-07T17:57Z; author-response commit 2026-08-08T19:18Z | Detected 2026-08-11. Day 2 confirming (search + direct-fetch both 404). Owner still exists; 6 other repos intact. |

## Tomorrow's predicted tuple (scan 2026-08-13 ~10:30Z)

`(0, 7, 1, 2)` — recent_merges drops 1→0 as `aeon-programmable-hooks#1` continues in 7d bucket through 08-15T19:17Z BUT actually it stays in the 7d bucket tomorrow (only ~4.6d after merge), so recent_merges HOLDS at 1. Corrected: `(1, 7, 1, 2)`. Reasoning:

- **recent_merges 1** (was 1): `aeon-programmable-hooks#1` still in 7d bucket tomorrow (~4.6d post-merge).
- **stale_open 7** (was 6): `PostHog/posthog#78346` crosses 7d-frozen at 08-12T14:08Z (~3h33m after today's scan → ~19.5h before tomorrow's scan) → flips OPEN active → OPEN stale. **Assumption**: no fresh stale-bot / maintainer comment reopens the activity window before tomorrow's scan. **Caveat**: Baileys#2732 letter-of-SKILL status depends on whether another stale-bot comment lands within the next 7 days; if none, Baileys returns to stale from 08-19 onward.
- **closed_no_merge 1** (was 1): k-skill#547 continues in 7d bucket through 2026-08-15T12:48Z (no rolloff before tomorrow's scan); no new closures anticipated.
- **active_open 2** (was 3): aeon-programmable-hooks#2 still within 7d creation window (~2.9d tomorrow); Baileys#2732 letter-of-SKILL active only if stale-bot comment stays within 7d activity window; PostHog#78346 rotates OUT (crosses 7d frozen).

Predicted `(1, 7, 1, 2)`. Confidence moderate on arithmetic; residual noise floor from unpredictable stale-bot comment events (now class-4), maintainer sweeps, additional deletion/archive events, and search indexing lag on self-owned repos (now class-5).
