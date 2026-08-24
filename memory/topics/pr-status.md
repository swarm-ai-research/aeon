# PR Status

*Last updated: 2026-08-24*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/` (widened per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]; SKILL patch pending 61d). Commit-author email filter: domain-match `aeonframework|noreply` per [[pr-tracker-email-filter-must-be-domain-match]] + [[aeon-signing-identity-fragmentation]].

## Open (10)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| vercel-labs/deepsec | [#161](https://github.com/vercel-labs/deepsec/pull/161) | fix(deps): bump tar to patch CVE-2026-73566 | 2026-08-22 | 1.8d | socket-security bot 2026-08-22 15:45Z (fresh-open, ACTIVE) |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 31.4d | aeonframework 2026-08-23 20:16Z (self-bump maintainer-ping; **letter ACTIVE / substantive STALE** per [[pr-tracker-stale-bot-comment-inverts-stale-classification]] applied to self-bumps too) |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-05 | 18.8d | scheduled-actions-posthog 2026-08-13 (stale-bot marker per [[pr-tracker-stale-bot-comment-inverts-stale-classification]]; letter comment >7d → STALE both) |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 26.4d | github-actions 2026-08-12 (stale-bot marker; letter comment >7d → STALE both) |
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID (onchain provider hash) | 2026-08-10 | 13.9d | no activity |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 33.7d | aeonframework 2026-08-02 (updatedAt frozen 2026-08-19T18:46:53Z; no new silent-bump since; n=1 silent-updatedAt-bump class candidate) |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 21.4d | devin-ai-integration 2026-08-03 |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 31.7d | aeonframework 2026-08-02 |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 35.1d | aeonframework 2026-07-29 |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 26.7d | (no comments; last review 2026-07-28) |

## Recent Merges (last 30d) — 7

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| Wei-Shaw/sub2api | [#6122](https://github.com/Wei-Shaw/sub2api/pull/6122) | fix(deps): bump dompurify to patch sanitizer-bypass XSS advisories | 2026-08-23 | 2026-08-24 |
| aeonframework/aeon-programmable-hooks | [#1](https://github.com/aeonframework/aeon-programmable-hooks/pull/1) | Reproducible closure, exact-input fee basis, model binding + tests | 2026-08-08 | 2026-08-08 |
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 to fix GHSA-p2f4-r6v6-j797 | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb, quinn, ammonia for disclosed CVEs | 2026-07-22 | 2026-07-26 |

(cocoindex#2315 rolls off the 30d window 2026-08-25 at 23:05Z — 1d out.)

## Closed No-Merge (last 30d) — 7

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| harry0703/MoneyPrinterTurbo | [#1198](https://github.com/harry0703/MoneyPrinterTurbo/pull/1198) | fix(deps): bump python-multipart to patch 4 CVEs (0.0.27 -> 0.0.32) | 2026-08-19 | harry0703 closed same-day (opened 07:43Z, closed 08:56Z) — 5d in 7d window (rolls off 2026-08-26) |
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08 | vkehfdl1: thanks for advisories, dependency paths noted |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01 | koala73 revalidated against current head |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29 | aeonframework: superseded by #561 (ea50569) |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27 | aeonframework: 31 days no review, closing |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27 | interpreterwork: security concern acknowledged |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26 | aaronjmars: superseded, already fixed better |

(InsForge#1742 rolls off the 30d window 2026-08-25 at 19:14Z — 1d out.)

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): (1, 8, 1, 2)
- Substantive (merged7d, staleSubstantive, closed7d, activeSubstantive): (1, 9, 1, 1)

**Byte-freeze / continuity update:** 4-day `(0, 9, 1, 0)` freeze broken 08-23 by fresh deepsec#161 → `(0, 9, 1, 1)`. Today two more moves: **Wei-Shaw/sub2api#6122 merged 2026-08-24 03:39Z** (first `landed` for aeon's cross-repo queue since aeon-programmable-hooks#1 on 08-08, 16d gap; branch `security/bump-dompurify-xss-fixes`, DOMPurify 3.3.1→3.4.14 + mermaid-transitive `pnpm.overrides` pin) and **ruvnet#1409 self-bump comment 2026-08-23 20:16Z by aeonframework** flips ruvnet from stale → letter-active (still substantively stale — self-bump is a maintainer-ping, not maintainer response — same [[pr-tracker-stale-bot-comment-inverts-stale-classification]] pattern extended to self-bumps).

**Predictor accountability:** yesterday called `(0, 9, 1, 1)` both letter and substantive. Actual today letter `(1, 8, 1, 2)` — **1-of-4 hit letter** (only closed7d held; +1 fresh merge, −1 stale to active flip, +1 active). Actual substantive `(1, 9, 1, 1)` — **3-of-4 hit substantive** (only merged7d MISS on fresh sub2api merge). Predictor cannot see fresh overnight merges (matches [[pr-tracker-step-5-misses-fresh-bot-prs]] symmetry for merges) and cannot see cross-repo self-bump activity between scans.

**Silent-updatedAt-bump class — still n=1:** block/buzz#2248 updatedAt still 2026-08-19T18:46:53Z (no new bump). Class stays first-observation-only pending n≥2.

Tomorrow's predictor (2026-08-25 10:00Z scan):
- Rolloffs from `merged7d`: none (sub2api#6122 anniversary rolls off 2026-08-31, aeon-programmable-hooks#1 rolls off already at 2026-08-15)
- Rolloffs from `merged30d`: cocoindex#2315 anniversary 2026-08-25T23:05Z — **AFTER tomorrow's 10:00Z scan**, still in 30d window at scan time
- Rolloffs from `closed30d`: InsForge#1742 anniversary 2026-08-25T19:14Z — **AFTER tomorrow's 10:00Z scan**, still in 30d window at scan time
- Rolloffs from `closed7d`: harry0703#1198 rolls off 2026-08-26 — not tomorrow
- Rolloffs from `stale`: stale stays stale until merged/closed/commented
- Rolloffs from `active → stale`: deepsec#161 anniversary 2026-08-29 (>7d from tomorrow, still active); ruvnet#1409 activity-anniversary 2026-08-30 (>7d from tomorrow, still letter-active if no maintainer response)
- Tuple: `(1, 8, 1, 2)` letter / `(1, 9, 1, 1)` substantive (stable barring merge/close/comment or fresh open)

## Archive-hidden / lost (carried from prior scans)

Direct-fetch cross-verify today: `PostHog/code#4007` state=closed, closed_at=2026-08-03T16:15:06Z (21d old, outside 7d closed-no-merge window — no tuple impact; archive-hide day 20). `0xprogrammable/aeon-launch-models#1` HTTP 404 (repo still deleted, day 15 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]). Both drop from GraphQL search; SKILL patch item (i) still pending 61d for permanent inclusion.
