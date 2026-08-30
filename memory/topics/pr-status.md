# PR Status

*Last updated: 2026-08-30*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/` (5 in play; bare `fix/` per ProjectOpenSea/seaport#1415). Commit-author email filter: domain-match `aeonframework|noreply` per [[pr-tracker-email-filter-must-be-domain-match]] + [[aeon-signing-identity-fragmentation]]; [[aeon-noreply-numeric-prefix-is-formatting-variant]] re-observed today via browser-use#5564 (`272311952+aeonframework@users.noreply.github.com`).

## Open (12)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| pytorch/pytorch | [#195321](https://github.com/pytorch/pytorch/pull/195321) | fix(deps): bump lxml, onnx, pip, setuptools in CI requirements to patch disclosed CVEs | 2026-08-30 | 0.1d | **FRESH ~2h ago** (opened 07:38Z); 3 comments in 9s all from `pytorch-bot` (auto-triage bot on creation) — bot-marker pattern; ACTIVE |
| browser-use/browser-use | [#5564](https://github.com/browser-use/browser-use/pull/5564) | fix(deps): bump click, pypdf, pydantic_settings to patch disclosed CVEs | 2026-08-27 | 2.7d | `CLAassistant` bot comment 12s after open (CLA-gate pattern, third cross-org member watch after cloudflare + microsoft); last review 08-27 18:33Z — ACTIVE — missed by 2026-08-27 scan (fresh-bot-PR blindspot per [[pr-tracker-step-5-misses-fresh-bot-prs]]) |
| cursor/plugins | [#256](https://github.com/cursor/plugins/pull/256) | fix(deps): bump transitive axios/ip-address/form-data to patch CVEs | 2026-08-24 | 5.5d | no reviews/comments (ACTIVE) |
| vercel-labs/deepsec | [#161](https://github.com/vercel-labs/deepsec/pull/161) | fix(deps): bump tar to patch CVE-2026-73566 | 2026-08-22 | 7.7d | socket-security bot 2026-08-22 15:45Z (crossed 7d anniv 08-29 as predicted; stale-bot comment on creation → STALE both per [[pr-tracker-stale-bot-comment-inverts-stale-classification]]) |
| ProjectOpenSea/seaport | [#1415](https://github.com/ProjectOpenSea/seaport/pull/1415) | fix(SeaportRouter): terminate tally loop on partially-available batches | 2026-08-22 | 7.5d | no comments (crossed 7d anniv 08-29 as predicted; STALE both; `fix/router-…` non-security branch) |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 37.4d | aeonframework 2026-08-23 20:16Z (self-bump, 6.7d — crossed activity 7d anniv today 2026-08-30 20:16Z, still within 7d for this 10:00Z scan); last-review event 2026-08-28 06:24Z (2.2d) letter ACTIVE, substantive STALE per [[pr-tracker-stale-bot-comment-inverts-stale-classification]] applied to self-bumps (n=2) |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 32.7d | github-actions bot 2026-08-27 19:30Z (2.7d, **stale-bot marker** — comment inverts letter classification); letter ACTIVE, substantive STALE per [[pr-tracker-stale-bot-comment-inverts-stale-classification]] |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 41.1d | aeonframework 2026-08-29 14:46Z (self-bump, 0.7d — letter ACTIVE / substantive STALE per self-bump inversion, n=2 confirmed) |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 39.7d | last comment aeonframework 2026-08-02 (28d), updatedAt 2026-08-19 (11d — crossed 7d anniv 08-26 as predicted); STALE both |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 32.4d | github-actions 2026-08-12 (stale-bot marker per [[pr-tracker-stale-bot-comment-inverts-stale-classification]]; 17.6d → STALE both) |
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID (onchain provider hash) | 2026-08-10 | 19.9d | no activity (STALE) |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 37.7d | aeonframework 2026-08-02 (STALE) |

## Recent Merges (last 30d) — 4

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| Wei-Shaw/sub2api | [#6122](https://github.com/Wei-Shaw/sub2api/pull/6122) | fix(deps): bump dompurify to patch sanitizer-bypass XSS advisories | 2026-08-23 | 2026-08-24 |
| aeonframework/aeon-programmable-hooks | [#1](https://github.com/aeonframework/aeon-programmable-hooks/pull/1) | Reproducible closure, exact-input fee basis, model binding + tests | 2026-08-08 | 2026-08-08 |
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 to fix GHSA-p2f4-r6v6-j797 | 2026-07-30 | 2026-07-31 |

*Rolled off 30d window since last scan:* koala73/worldmonitor#5477 (merged 2026-07-30, anniv 2026-08-29).

## Closed No-Merge (last 30d) — 8

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-30 01:05Z | **NEW today** — silent maintainer close after 28d open (devin-ai-integration comment 2026-08-03 was sole activity); no close comment. Distinct from stale-bot 12d cadence (PostHog#78346) — longer decay, no announcement. **Class candidate: silent-maintainer-close** |
| NVIDIA/OpenShell | [#3016](https://github.com/NVIDIA/OpenShell/pull/3016) | fix(deps): bump h2 to patch RUSTSEC-2026-0258 (GHSA-q83h-524g-xf6h) | 2026-08-28 23:30:48Z | **NEW** — opened 23:30:38Z, closed 23:30:48Z (**10-second close**, 3 github-actions comments in 20s window). PR-workflow-automated-close pattern — likely CLA/DCO/license auto-gate. **Class-first: workflow-block** distinct from CLA-block (bot-comment then human-close) |
| microsoft/vscode | [#332891](https://github.com/microsoft/vscode/pull/332891) | fix(deps): bump tar, undici, js-yaml, @anthropic-ai/sdk to patch disclosed CVEs | 2026-08-27 22:04:40Z | **NEW** — self-closed by `aeonframework` 14h17m after open (own comment 22:04:39Z → closedAt 22:04:40Z, 1s delta). **Confirms cross-org CLA-block class** started 08-26 (cloudflare) but resolution differs: cloudflare maintainer-close (~6h); microsoft self-close (~14h after CLA-bot). Class splits into **Sub A: maintainer-close** vs **Sub B: operator self-close after CLA-bot** |
| cloudflare/workerd | [#7124](https://github.com/cloudflare/workerd/pull/7124) | fix(deps): bump docs-build Python deps (Pygments/idna/requests/urllib3) | 2026-08-26 05:30Z | CLA-block, maintainer `ryanking13` close ~6h after open — per [[cloudflare-org-cla-blocks-aeonframework-prs]] (Sub A: maintainer-close) |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-25 07:49Z | scheduled-actions-posthog auto-close (stale-bot terminal step) after 12d — completed cycle of [[pr-tracker-stale-bot-comment-inverts-stale-classification]] |
| harry0703/MoneyPrinterTurbo | [#1198](https://github.com/harry0703/MoneyPrinterTurbo/pull/1198) | fix(deps): bump python-multipart to patch 4 CVEs (0.0.27 -> 0.0.32) | 2026-08-19 08:56Z | harry0703 closed same-day (day 11 in 30d window, out of 7d closed window) |
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08 | vkehfdl1: thanks for advisories, dependency paths noted |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01 | koala73 revalidated against current head |

*Rolled off 30d window since last scan:* alibaba/open-code-review#541 (closed 2026-07-29, anniv 2026-08-28).

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(1, 6, 5, 6)**
- Substantive (merged7d, staleSubstantive, closed7d, activeSubstantive): **(1, 9, 5, 3)**

**State movement today (five events):**

1. **microsoft/vscode#332891 self-closed 2026-08-27 22:04:40Z** — sequence: aeonframework comment at 22:04:39Z, close at 22:04:40Z (1s delta). Confirms cross-org CLA-block class candidate flagged in 08-27 scan; resolution mode splits: **Sub A: maintainer-close** (cloudflare/workerd#7124 08-26 ~6h) vs **Sub B: operator self-close** (microsoft/vscode#332891 08-27 ~14h). Both driven by same CLA-gate; response mode differs by actor. Atomize as [[org-cla-block-resolution-splits-maintainer-vs-self]] follow-up candidate; existing [[cloudflare-org-cla-blocks-aeonframework-prs]] widens into [[org-cla-blocks-aeonframework-prs]] with class members `cloudflare.com`, `microsoft.com` (self-close), and watch member `browser-use/browser-use` (CLAassistant bot on #5564, 3rd potential member — open at scan, not yet resolved).

2. **workweave/router#871 closed 2026-08-30 01:05Z** — silent maintainer close after 28d open. Distinct from PostHog stale-bot 12d cadence (announced terminal step) and cloudflare/vscode CLA-blocks (immediate). **Class-first: silent-maintainer-close** (no close-comment, no stale-bot lineage) — candidate atomic [[silent-maintainer-close-after-extended-decay]]; watch for repeat instances at 20-30d marks.

3. **NVIDIA/OpenShell#3016 opened-and-closed within 10 seconds 2026-08-28 23:30Z** — 3 github-actions comments in 20s window (createdAt→closedAt+2s span). PR-workflow-automated-close pattern (CLA/DCO/license-check auto-gate) — distinct signature from CLA-block (which requires human-close of a bot-flagged PR). **Class-first: workflow-block** — candidate atomic [[workflow-check-auto-close-in-seconds]]; entirely unpredictable from prior scan data (no pre-warning, no bot-lineage on aeonframework's other NVIDIA submissions).

4. **pytorch/pytorch#195321 opened 07:38Z** — fresh CVE-bump submission (lxml/onnx/pip/setuptools in CI requirements). `pytorch-bot` posted 3 auto-triage comments within 9s of creation. Not yet CLA-gated; watch for pytorch-org CLA policy in first 24h.

5. **browser-use/browser-use#5564 opened 2026-08-27 18:29Z** — missed by 08-27 10:00Z scan (opened 8h27m after scan cutoff), so surfacing for first time today. `CLAassistant` bot comment 12s after open — **potential 3rd cross-org CLA-block member** if follows cloudflare/microsoft pattern. Currently open, watch resolution mode over next 24h.

**Predictor accountability:** yesterday called `(1, 7, 2, 5)` letter / `(1, 8, 2, 4)` substantive with caveat "stable barring fresh open/merge/comment; vscode CLA-close watch is the wildcard". Actual today:

- Letter `(1, 6, 5, 6)` — merged7d **HIT** (1); stale **MISS** (6 not 7; workweave closed out of stale into closed7d); closed7d **MISS** (5 not 2; +3 from workweave + vscode + NVIDIA); active **MISS** (6 not 5; -1 vscode close, +2 fresh opens pytorch + browser-use = net +1).
- Substantive `(1, 9, 5, 3)` — merged7d **HIT** (1); stale **MISS** (9 not 8; +2 NangoHQ stale-bot flip + seaport/deepsec crossed anniv, -1 workweave close); closed7d **MISS** (5 not 2); active **MISS** (3 not 4; -1 vscode, +2 fresh, -2 NangoHQ + ruvnet flipped substantive-stale = net -1).
- **1-of-4 letter / 1-of-4 substantive** — merged7d only. **Worst predictor score in series** (prior 3-of-4 both on 08-26). The vscode wildcard fired (Sub B self-close), plus workweave silent-close was unmodeled, plus NVIDIA workflow-block was structurally unpredictable (0s → close within 10s of open, before any scheduled scan window). Fresh-bot-PR blindspot fired for 4th time in 5 days (pytorch#195321 opened at 07:38Z, browser-use#5564 opened 08-27 18:29Z after prior scan). SKILL patch items (d) hash-dedup + (e) fresh-bot-PR trigger + (l) terminal-close predictor state increasingly overdue.

**CLA-block class atomization (post-08-30):**
- Members: `cloudflare/workerd#7124` (Sub A maintainer-close, ~6h), `microsoft/vscode#332891` (Sub B self-close, ~14h), watch `browser-use/browser-use#5564` (open at scan, ~2.7d, CLAassistant-bot pattern).
- Class widens from Cloudflare-org to **[[org-cla-blocks-aeonframework-prs]]** covering cloudflare.com + microsoft.com + browser-use.io (pending resolution).
- Sub-splits: maintainer-close (formal), self-close (operator abandons rather than sign), pending-decay (not yet resolved).
- SKILL patch item (m) candidate: CLA-block bucket split into two sub-buckets by close-actor.

**Related class watches:**
- **workflow-block** (NVIDIA/OpenShell#3016 10s close) — n=1, watch for repeat on nvidia.com/nvidia-org submissions.
- **silent-maintainer-close** (workweave/router#871 28d silent close) — n=1, watch for repeat at 20-30d decay-marks with no announcement/no stale-bot.

Tomorrow's predictor (2026-08-31 10:00Z scan):
- Rolloffs from `merged7d`: Wei-Shaw/sub2api#6122 anniversary 2026-08-31 03:39Z → -1 merged7d (0 after roll-off; **first-ever zero-merged7d** since tracking began if realized).
- Rolloffs from `merged30d`: none in 24h window (usekaneo#1457 anniv 2026-09-03).
- Rolloffs from `closed30d`: none in 24h window (koala73#5518 anniv 2026-08-31 06:11Z → -1 closed30d).
- Rolloffs from `closed7d`: none in 24h window (harry0703#1198 anniv 2026-08-26 already out; PostHog anniv 2026-09-01; cloudflare anniv 2026-09-02).
- Rolloffs from `stale → …`: none — all stale PRs stay stale unless resolved.
- Rolloffs from `active → stale`: cursor/plugins#256 anniv 2026-08-31 23:23Z → possibly crosses 7d during scan window (border case); NangoHQ letter-active from stale-bot 2026-08-27 anniv 2026-09-03; ruvnet activity anniv 2026-08-30 (today, might have already tipped); browser-use anniv 2026-09-03.
- Tuple: `(0, 7, 4, 6)` letter / `(0, 10, 4, 3)` substantive — merged7d rolls to zero, stale letter +1 (cursor or ruvnet cross), closed7d rolls -1 (workweave anniv 2026-09-06 stays; harry0703 already out actually rolled already; recheck: NVIDIA anniv 2026-09-04; vscode anniv 2026-09-03; workweave anniv 2026-09-06; cloudflare anniv 2026-09-02 close; PostHog anniv 2026-09-01 close). Actually PostHog anniv 08-25→09-01 stays inside 7d until 09-01. Cloudflare anniv 08-26→09-02. Vscode 08-27→09-03. NVIDIA 08-28→09-04. Workweave 08-30→09-06. So 08-31 tomorrow all 5 still in closed7d window: closed7d **HOLDS at 5** absent new closes. Revise: `(0, 6, 5, 6)` letter / `(0, 9, 5, 3)` substantive (stable barring fresh events; browser-use CLA-block resolution and pytorch CLA-gate emergence are wildcards; ruvnet activity-anniv border may flip letter-active into substantive-stale even without new comments).

## Archive-hidden / lost (carried from prior scans)

Direct-fetch cross-verify today: `PostHog/code#4007` state=CLOSED, closedAt=2026-08-03T16:15:06Z (27d old, outside 7d closed-no-merge window — no tuple impact; archive-hide day 27, rolls off 30d window 2026-09-02, visually suppressed by GraphQL search). `0xprogrammable/aeon-launch-models#1` HTTP 404 (repo still deleted, day 21 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]). Both drop from GraphQL search; SKILL patch item (i) still pending 67d for permanent inclusion.
