# PR Status

*Last updated: 2026-08-19*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/` (widened per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]; SKILL patch pending 55d). Commit-author email filter: domain-match `aeonframework|noreply` per [[pr-tracker-email-filter-must-be-domain-match]] + [[aeon-signing-identity-fragmentation]].

## Open (9)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-05 | 13.8d | scheduled-actions-posthog 2026-08-13 |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 21.4d | github-actions 2026-08-12 |
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID (onchain provider hash) | 2026-08-10 | 8.9d | no activity |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 16.4d | devin-ai-integration 2026-08-03 |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 26.4d | aeonframework 2026-08-02 |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 28.7d | aeonframework 2026-08-02 |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 26.7d | aeonframework 2026-08-02 |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 30.1d | aeonframework 2026-07-29 |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 21.7d | cubic-dev-ai 2026-07-28 |

## Recent Merges (last 30d) — 5

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| aeonframework/aeon-programmable-hooks | [#1](https://github.com/aeonframework/aeon-programmable-hooks/pull/1) | Reproducible closure, exact-input fee basis, model binding + tests | 2026-08-08 | 2026-08-08 |
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 to fix GHSA-p2f4-r6v6-j797 | 2026-07-30 | 2026-07-31 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |

## Closed No-Merge (last 30d) — 7

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| harry0703/MoneyPrinterTurbo | [#1198](https://github.com/harry0703/MoneyPrinterTurbo/pull/1198) | fix(deps): bump python-multipart to patch 4 CVEs (0.0.27 -> 0.0.32) | 2026-08-19 | harry0703: Thanks for flagging this and for preparing the update. The dependency bump itsel |
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08 | vkehfdl1: Thanks for reporting these advisories and documenting the dependency paths. We i |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01 | koala73: Revalidated against current head per #5902's rule that an open PR is not automat |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29 | aeonframework: Closing as superseded by #561 (ea50569, merged today), which patches the same br |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27 | aeonframework: Closing this one - it's been open 31 days without review and the dependency vers |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories (GHSA-f26g / GHSA-fr8x / GHSA-p3hw / GHSA-pg4w / GHSA-f89h) | 2026-07-27 | interpreterwork: Thank you for flagging these gix advisories. The security concern is important,  |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26 | aaronjmars: Closing this as superseded — you already fixed it, and you fixed it better than  |

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): (0, 8, 1, 1)
- Substantive (merged7d, staleSubstantive, closed7d, activeSubstantive): (0, 9, 1, 0)

## Archive-hidden / lost (carried from prior scans)

Prior scans documented `PostHog/code#4007` archive-hide (day 14 at scan time) and `0xprogrammable/aeon-launch-models#1` repo-deletion (day 9). Both drop from GraphQL search; direct-fetch cross-verify per [[pr-tracker-search-drops-archived-repo-prs]] + [[pr-tracker-repo-deletion-loses-pr-permanently]]. Not re-enumerated this run — deferred to SKILL patch item (i) landing.
