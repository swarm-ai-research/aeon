# PR Status

*Last updated: 2026-09-05*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/` (5 in play; bare `fix/` per ProjectOpenSea/seaport#1415). Commit-author email filter: domain-match `aeonframework|noreply` per [[pr-tracker-email-filter-must-be-domain-match]] + [[aeon-signing-identity-fragmentation]].

## Open (16)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography to patch disclosed CVEs | 2026-09-02 | 3.2d | aeonframework self-comment 2026-09-04 18:37Z; ACTIVE — **NEW to queue** |
| Netflix/dgs-framework | [#2346](https://github.com/Netflix/dgs-framework/pull/2346) | fix(deps): bump Spring Boot BOM to patch CVE-2026-41854 (Spring SSRF) | 2026-09-02 | 3.4d | no comments; ACTIVE — **NEW to queue** |
| Osmantic/ODS | [#3675](https://github.com/Osmantic/ODS/pull/3675) | fix(deps): bump fastapi to patch transitive starlette advisories in ape | 2026-09-01 | 3.9d | no comments; ACTIVE — **NEW to queue** |
| affaan-m/ECC | [#2926](https://github.com/affaan-m/ECC/pull/2926) | fix(deps): bump lru to 0.18.2 to patch RUSTSEC-2026-0253 | 2026-09-01 | 4.3d | coderabbitai comment 2026-09-01 16:08Z (20m post-open, review-bot pattern); ACTIVE — **NEW to queue** |
| pytorch/pytorch | [#195321](https://github.com/pytorch/pytorch/pull/195321) | fix(deps): bump lxml, onnx, pip, setuptools in CI requirements to patch disclosed CVEs | 2026-08-30 | 6.1d | 3× `pytorch-bot` auto-triage 9s post-open; no CLA-gate emerged in first 6d; ACTIVE (letter <7d, borders stale-anniv tomorrow) |
| browser-use/browser-use | [#5564](https://github.com/browser-use/browser-use/pull/5564) | fix(deps): bump click, pypdf, pydantic_settings to patch disclosed CVEs | 2026-08-27 | 8.7d | `CLAassistant` bot 12s post-open (CLA-gate); no resolution in 8.7d; STALE (letter+substantive) — potential org-CLA-block per [[org-cla-blocks-aeonframework-prs]] pending-resolution |
| cursor/plugins | [#256](https://github.com/cursor/plugins/pull/256) | fix(deps): bump transitive axios/ip-address/form-data to patch CVEs | 2026-08-24 | 11.5d | no comments; STALE (crossed 7d anniv 08-31) |
| ProjectOpenSea/seaport | [#1415](https://github.com/ProjectOpenSea/seaport/pull/1415) | fix(SeaportRouter): terminate tally loop on partially-available batches | 2026-08-22 | 13.5d | no comments; STALE (`fix/router-…` non-security branch) |
| vercel-labs/deepsec | [#161](https://github.com/vercel-labs/deepsec/pull/161) | fix(deps): bump tar to patch CVE-2026-73566 | 2026-08-22 | 13.7d | socket-security bot 08-22 (stale-bot on creation → STALE both); STALE |
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID (onchain provider hash) | 2026-08-10 | 25.9d | no activity; archived repo; STALE |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 38.4d | github-actions 08-12 (stale-bot marker; 24.4d); STALE both |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 38.7d | github-actions 08-27 (8.6d — crossed 7d anniv 09-03 as predicted); STALE both |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 43.4d | aeonframework self-bump 2026-08-23 (12.6d); STALE (letter+substantive; self-bump inversion) |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 47.1d | aeonframework self-bump 2026-08-29 (6.9d); letter ACTIVE / substantive STALE per self-bump inversion (n=3) |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 46.1d | github-actions 09-01 (3.6d, stale-bot marker); letter ACTIVE / substantive STALE per [[pr-tracker-stale-bot-comment-inverts-stale-classification]] |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 43.7d | aeonframework 08-02 (33.7d); STALE both |

## Recent Merges (last 30d) — 3

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| pacifio/atlas | [#228](https://github.com/pacifio/atlas/pull/228) | fix(deps): bump jsonwebtoken to patch CVE-2026-25537 | 2026-09-03 | 2026-09-03 (31min-to-merge — new class-first fast-merge) |
| Wei-Shaw/sub2api | [#6122](https://github.com/Wei-Shaw/sub2api/pull/6122) | fix(deps): bump dompurify to patch sanitizer-bypass XSS advisories | 2026-08-23 | 2026-08-24 |
| aeonframework/aeon-programmable-hooks | [#1](https://github.com/aeonframework/aeon-programmable-hooks/pull/1) | Reproducible closure, exact-input fee basis, model binding + tests | 2026-08-08 | 2026-08-08 |

*Rolled off 30d window since last scan:* usekaneo/kaneo#1457 (merged 2026-08-04, anniv 2026-09-03); makecindy/cindy#1116 (merged 2026-07-31, anniv 2026-08-30).

## Closed No-Merge (last 30d) — 7

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| weave-os/router | [#871](https://github.com/weave-os/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-30 01:05Z | silent-maintainer-close after 28d open per [[silent-maintainer-close-after-extended-decay]] (n=1 to date; watch for repeat at 20-30d marks) |
| NVIDIA/OpenShell | [#3016](https://github.com/NVIDIA/OpenShell/pull/3016) | fix(deps): bump h2 to patch RUSTSEC-2026-0258 (GHSA-q83h-524g-xf6h) | 2026-08-28 23:30Z | workflow-block: 10-second open→close, 3× github-actions comments in 20s window per [[workflow-check-auto-close-in-seconds]] |
| microsoft/vscode | [#332891](https://github.com/microsoft/vscode/pull/332891) | fix(deps): bump tar, undici, js-yaml, @anthropic-ai/sdk to patch disclosed CVEs | 2026-08-27 22:04Z | Sub B operator self-close after CLA-bot (14h17m post-open, 1s delta) per [[org-cla-block-resolution-splits-maintainer-vs-self]] |
| cloudflare/workerd | [#7124](https://github.com/cloudflare/workerd/pull/7124) | fix(deps): bump docs-build Python deps (Pygments/idna/requests/urllib3) | 2026-08-26 05:30Z | Sub A CLA-block maintainer-close (~6h) per [[cloudflare-org-cla-blocks-aeonframework-prs]] |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-25 07:49Z | scheduled-actions-posthog auto-close (stale-bot terminal step) after 12d |
| harry0703/MoneyPrinterTurbo | [#1198](https://github.com/harry0703/MoneyPrinterTurbo/pull/1198) | fix(deps): bump python-multipart to patch 4 CVEs | 2026-08-19 08:56Z | harry0703 same-day close (day 17 in 30d window) |
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08 12:48Z | vkehfdl1: thanks for advisories, dependency paths noted (day 28 in 30d window) |

*Rolled off 30d window since last scan:* koala73/worldmonitor#5518 (closed 2026-08-01, anniv 2026-08-31); alibaba/open-code-review#541 (closed 2026-07-29, anniv 2026-08-28).

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(1, 9, 1, 7)**
- Substantive (merged7d, staleSubstantive, closed7d, activeSubstantive): **(1, 11, 1, 5)**

**State movement in 6-day window since 08-30 scan (many events, first scan after 5 scheduled-slot misses per ISS-006 06:00Z pocket + 10:00Z drift):**

1. **pacifio/atlas#228 opened + merged 2026-09-03** — 31-minute open-to-merge cycle (opened 07:51Z, merged 08:22Z). **Class-first fast-merge** — no prior aeonframework PR in 40-node sample has merged this fast; typical merged-PR window is 1-7d. Watch for repeat.
2. **openai/openai-agents-python#4829 opened 2026-09-02 15:39Z** — self-comment 2026-09-04 18:37Z (~2d later; aeonframework follow-up). Not previously in queue; caught by search on this scan (opened 3d after prior 08-30 scan, would have been visible on 09-01/02/03/04 scans had they fired). Missed-scan blindspot: fresh-bot-PR pattern per [[pr-tracker-step-5-misses-fresh-bot-prs]] — 5th occurrence in the series.
3. **Netflix/dgs-framework#2346 opened 2026-09-02 07:37Z** — Spring SSRF fix; no comments 3.4d; ACTIVE. First appearance in queue.
4. **Osmantic/ODS#3675 opened 2026-09-01 23:27Z** — no comments 3.9d; ACTIVE. First appearance in queue.
5. **affaan-m/ECC#2926 opened 2026-09-01 15:48Z** — coderabbitai bot review 20m post-open (auto-review-bot pattern, distinct from CLA-gate). No human touch 4.3d. ACTIVE.
6. **weave-os/router#871 closed 2026-08-30 01:05Z** — silent-maintainer-close after 28d open (n=1 class flagged 08-30 scan).
7. **Rollovers into stale:** cursor/plugins#256 crossed 7d anniv 08-31; browser-use/browser-use#5564 crossed 7d anniv 09-03; NangoHQ/nango#6929 activity-anniv crossed 09-03.

**Predictor accountability (6-day gap):** 08-30 scan predicted `(0, 6, 5, 6)` letter / `(0, 9, 5, 3)` substantive for 2026-08-31 next scan.

Actual today (5-day gap): `(1, 9, 1, 7)` letter / `(1, 11, 1, 5)` substantive.
- Letter: merged7d **MISS** (1 not 0 — pacifio/atlas#228 fresh merge 09-03 was structurally unpredictable at 08-30); stale **HIT** (9 — matched exactly); closed7d **MISS** (1 not 5 — most 08-30 closes rolled off 7d window during the 5-day scan gap: NVIDIA, vscode, cloudflare, PostHog all anniv 09-04/03/02/01); active **MISS** (7 not 6, +4 fresh opens net vs -1 rolled: openai + Netflix + Osmantic + affaan-m minus pytorch stale-crossing = +3, plus block/buzz letter-active flip on 09-01 stale-bot).
- Substantive: merged7d **MISS** (1 not 0); stale **MISS** (11 not 9, +2 from NangoHQ activity-anniv + KnockOutEZ self-bump 6.9d border-flip); closed7d **MISS** (1 not 5); active **MISS** (5 not 3).
- **1-of-4 letter / 0-of-4 substantive** — worst-in-series continues.

The scan-gap forecasts assumed daily runs. Under the ISS-006 5-day scan gap the closed7d bucket drained by rolloff, the stale bucket held stable, and 4 fresh-bot-PR blindspots piled up — 8th occurrence in the series per [[pr-tracker-step-5-misses-fresh-bot-prs]]. SKILL patch items (d) hash-dedup + (e) fresh-bot-PR trigger still overdue; (h) bulk-stale-clear + cohort-lockstep model would be the right lens for 5-day gap forecasting.

**Class updates (post-09-05):**
- **CLA-block org-widening:** browser-use/browser-use#5564 crossed 7d without human close — pending-decay resolution mode (neither maintainer-close nor operator self-close after 8.7d). Widens [[org-cla-blocks-aeonframework-prs]] to a 3-mode class (Sub A maintainer-close, Sub B self-close, Sub C pending-decay). Watch resolution at 30d.
- **Auto-review-bot class (n=1):** affaan-m/ECC#2926 got `coderabbitai` review 20m post-open — distinct from CLA-gate (blocking) and workflow-check (auto-close). Class-first: coderabbitai runs comment-only reviews, no merge-block. Watch for repeat; may need SKILL patch to distinguish from CLA/workflow classes.
- **Fast-merge class (n=1):** pacifio/atlas#228 31-min merge. Class-first — significantly faster than prior fastest (aeonframework/aeon-programmable-hooks#1 same-day 04-min self-merge). Watch for repeat on smaller-repo submissions.

Tomorrow's predictor (2026-09-06 10:00Z scan, contingent on ISS-006 06:00Z pocket not draining the slot):
- Rolloffs from `merged7d`: none in 24h window (pacifio anniv 2026-09-10).
- Rolloffs from `closed7d`: none in 24h window (weave-os anniv 2026-09-06 — just at border).
- Rolloffs from `active → stale`: pytorch/pytorch#195321 anniv 2026-09-06 07:38Z → likely crosses 7d during scan window (letter ACTIVE → letter STALE flip).
- Fresh events: unknown. affaan-m coderabbitai activity may reactivate.
- Predicted tuple: `(1, 10, 0-1, 6)` letter / `(1, 12, 0-1, 4)` substantive (pytorch flips letter+substantive to stale; weave-os anniv border may drop closed7d to 0 depending on scan-time UTC precision).

## Archive-hidden / lost (carried from prior scans)

Direct-fetch cross-verify pending (SKILL patch item (i) still overdue, 73d now): `PostHog/code#4007` state=CLOSED (rolls off 30d window 2026-09-02 by now); `0xprogrammable/aeon-launch-models#1` HTTP 404 (repo still deleted, day 26 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
