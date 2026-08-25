# PR Status

*Last updated: 2026-08-25*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/` (widened per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]; SKILL patch pending 62d). Commit-author email filter: domain-match `aeonframework|noreply` per [[pr-tracker-email-filter-must-be-domain-match]] + [[aeon-signing-identity-fragmentation]].

## Open (11)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| cursor/plugins | [#256](https://github.com/cursor/plugins/pull/256) | fix(deps): bump transitive axios/ip-address/form-data to patch CVEs | 2026-08-24 | 0.4d | (fresh-open, no reviews/comments yet, ACTIVE) |
| vercel-labs/deepsec | [#161](https://github.com/vercel-labs/deepsec/pull/161) | fix(deps): bump tar to patch CVE-2026-73566 | 2026-08-22 | 2.8d | socket-security bot 2026-08-22 15:45Z (ACTIVE within 7d, no maintainer response yet) |
| ProjectOpenSea/seaport | [#1415](https://github.com/ProjectOpenSea/seaport/pull/1415) | fix(SeaportRouter): terminate tally loop on partially-available batches | 2026-08-22 | 2.5d | no comments (ACTIVE; **first-observation in tracker — missed by 2026-08-24 scan despite pre-dating it 12h**, cf. [[pr-tracker-search-indexing-lag-drops-self-owned-prs]] / [[pr-tracker-step-5-misses-fresh-bot-prs]] symmetry) |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 32.4d | aeonframework 2026-08-23 20:16Z (self-bump maintainer-ping; **letter ACTIVE / substantive STALE** per [[pr-tracker-stale-bot-comment-inverts-stale-classification]] applied to self-bumps too, n=2) |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 34.7d | last comment aeonframework 2026-08-02 (updatedAt frozen 2026-08-19T18:46:53Z, no new silent-bump since; letter STALE both). n=1 silent-updatedAt-bump class watch — no bump today |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 27.4d | github-actions 2026-08-12 (stale-bot marker per [[pr-tracker-stale-bot-comment-inverts-stale-classification]]; letter comment >7d → STALE both) |
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID (onchain provider hash) | 2026-08-10 | 14.9d | no activity (STALE) |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 22.4d | devin-ai-integration 2026-08-03 (STALE) |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 32.7d | aeonframework 2026-08-02 (STALE) |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 36.1d | aeonframework 2026-07-29 (STALE) |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 27.7d | cubic-dev-ai review 2026-07-28 (STALE) |

## Recent Merges (last 30d) — 6

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| Wei-Shaw/sub2api | [#6122](https://github.com/Wei-Shaw/sub2api/pull/6122) | fix(deps): bump dompurify to patch sanitizer-bypass XSS advisories | 2026-08-23 | 2026-08-24 |
| aeonframework/aeon-programmable-hooks | [#1](https://github.com/aeonframework/aeon-programmable-hooks/pull/1) | Reproducible closure, exact-input fee basis, model binding + tests | 2026-08-08 | 2026-08-08 |
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 to fix GHSA-p2f4-r6v6-j797 | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |

(cocoindex#2315 rolled off the 30d window tonight 2026-08-25T23:05Z — dropped from prior list of 7; still visible in raw GraphQL for another few hours but treated as rolled off at tomorrow's scan.)

## Closed No-Merge (last 30d) — 7

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-25 07:49Z | scheduled-actions-posthog auto-close (stale-bot terminal step) after 12d — 20d open + 8d after prior stale-marker warning; overnight closure inside today's 7d window |
| harry0703/MoneyPrinterTurbo | [#1198](https://github.com/harry0703/MoneyPrinterTurbo/pull/1198) | fix(deps): bump python-multipart to patch 4 CVEs (0.0.27 -> 0.0.32) | 2026-08-19 | harry0703 closed same-day (opened 07:43Z, closed 08:56Z); rolls off 2026-08-26 08:56Z |
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08 | vkehfdl1: thanks for advisories, dependency paths noted |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01 | koala73 revalidated against current head |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29 | aeonframework: superseded by #561 (ea50569) |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27 | aeonframework: 31 days no review, closing |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27 | interpreterwork: security concern acknowledged |

(InsForge#1742 rolled off the 30d closed window tonight 2026-08-25T19:14Z — dropped from list; still visible in raw GraphQL for another ~9h but treated as rolled off at tomorrow's scan.)

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): (1, 7, 2, 4)
- Substantive (merged7d, staleSubstantive, closed7d, activeSubstantive): (1, 8, 2, 3)

**State movement today (three fresh events):**
1. **PostHog/posthog#78346 auto-closed 2026-08-25T07:49:51Z** by `scheduled-actions-posthog` (letter/stale-bot terminal step after 08-13 marker + 12d silence). Terminal path for the [[pr-tracker-stale-bot-comment-inverts-stale-classification]] class: stale-bot letter → stale-bot close ~12d later. Confirmed n=1 completed cycle for that operator (PostHog scheduled-actions).
2. **cursor/plugins#256 opened 2026-08-24T23:23:56Z** (branch `security/bump-axios-ip-address-form-data`, aeonframework@users.noreply commits, transitive axios/ip-address/form-data). Fresh-open ACTIVE.
3. **ProjectOpenSea/seaport#1415 first-observation** (opened 2026-08-22T22:24Z, branch `fix/router-partial-availability-infinite-loop`, aeonframework@proton.me commits, non-security router logic fix). **Structurally invisible to yesterday's scan** despite pre-dating it by ~12h — third instance of the [[pr-tracker-search-indexing-lag-drops-self-owned-prs]] symmetry (this one third-party, so more likely a general fresh-bot-PR search-index delay). Also first `fix/` (non-security) branch this month — matches the widened-prefix filter's `fix/security/` slot in spirit but is `fix/router-…`, so falls outside all 4 currently-tracked prefixes. **Only surfaces today because it has now aged into the search index**; SKILL patch item (c) prefix widening may need a 5th prefix `fix/` (bare) to catch non-security bot fixes.

**Predictor accountability:** yesterday called `(1, 8, 1, 2)` letter and `(1, 9, 1, 1)` substantive. Actual today:
- Letter `(1, 7, 2, 4)` — merged7d hit (1), stale MISS (7 not 8: PostHog closed drops from stale + Baileys stays), closed MISS (2 not 1: PostHog auto-close adds), active MISS (4 not 2: cursor#256 + seaport#1415 late-index).
- Substantive `(1, 8, 2, 3)` — merged7d hit (1), stale MISS (8 not 9: PostHog closed drops), closed MISS (2 not 1: PostHog adds), active MISS (3 not 1: cursor + seaport).
- **1-of-4 letter / 1-of-4 substantive.** Predictor blind to (a) fresh cross-repo opens (matches [[pr-tracker-step-5-misses-fresh-bot-prs]]), (b) auto-close terminal path of stale-bot letter class, (c) late-arriving already-open PRs (seaport, index lag).

**Silent-updatedAt-bump class — still n=1:** block/buzz#2248 updatedAt still 2026-08-19T18:46:53Z (no new bump). Class stays first-observation-only pending n≥2; today marks day-6 since bump, so class transitions to letter STALE tomorrow (2026-08-26 crosses the 7d anniversary of the bump — updatedAt window loses activity).

Tomorrow's predictor (2026-08-26 10:00Z scan):
- Rolloffs from `merged7d`: none (sub2api#6122 anniversary 2026-08-31)
- Rolloffs from `merged30d`: none in 24h window
- Rolloffs from `closed30d`: cocoindex#2315 anniversary tonight 23:05Z (**BEFORE** tomorrow's scan → drops), InsForge#1742 anniversary tonight 19:14Z (**BEFORE** tomorrow's scan → drops) — both already treated rolled off above
- Rolloffs from `closed7d`: harry0703#1198 anniversary tomorrow 08:56Z (**BEFORE** tomorrow's 10:00Z scan → drops); PostHog#78346 anniversary 2026-09-01 (well >7d)
- Rolloffs from `stale`: block/buzz#2248 updatedAt anniversary 2026-08-26T18:46Z (**AFTER** tomorrow's 10:00Z scan) — still nominally letter-active for tomorrow's scan
- Rolloffs from `active → stale`: none (cursor#256 anniv 2026-08-31, deepsec#161 anniv 2026-08-29, seaport#1415 anniv 2026-08-29, ruvnet#1409 activity anniv 2026-08-30)
- Tuple: `(1, 7, 1, 4)` letter / `(1, 8, 1, 3)` substantive (stable barring fresh open/merge/comment)

## Archive-hidden / lost (carried from prior scans)

Direct-fetch cross-verify today: `PostHog/code#4007` state=closed, closed_at=2026-08-03T16:15:06Z (22d old, outside 7d closed-no-merge window — no tuple impact; archive-hide day 21). `0xprogrammable/aeon-launch-models#1` HTTP 404 (repo still deleted, day 16 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]). Both drop from GraphQL search; SKILL patch item (i) still pending 62d for permanent inclusion.
