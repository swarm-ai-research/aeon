# PR Status

*Last updated: 2026-08-27*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/` (bare `fix/` newly evidenced 08-25 by ProjectOpenSea/seaport#1415 — 5th prefix in play as of today; SKILL patch pending 64d). Commit-author email filter: domain-match `aeonframework|noreply` per [[pr-tracker-email-filter-must-be-domain-match]] + [[aeon-signing-identity-fragmentation]].

## Open (12)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| microsoft/vscode | [#332891](https://github.com/microsoft/vscode/pull/332891) | fix(deps): bump tar, undici, js-yaml, @anthropic-ai/sdk to patch disclosed CVEs | 2026-08-27 | 0.0d | **FRESH ~3h ago** (opened 07:47Z); sole comment is `microsoft-github-policy-service` CLA-bot posted 9s after PR creation demanding CLA reply — second CLA-block instance in 48h after cloudflare/workerd#7124 (ACTIVE) |
| cursor/plugins | [#256](https://github.com/cursor/plugins/pull/256) | fix(deps): bump transitive axios/ip-address/form-data to patch CVEs | 2026-08-24 | 2.5d | no reviews/comments (ACTIVE) |
| vercel-labs/deepsec | [#161](https://github.com/vercel-labs/deepsec/pull/161) | fix(deps): bump tar to patch CVE-2026-73566 | 2026-08-22 | 4.8d | socket-security bot 2026-08-22 15:45Z (ACTIVE within 7d, still no maintainer response) |
| ProjectOpenSea/seaport | [#1415](https://github.com/ProjectOpenSea/seaport/pull/1415) | fix(SeaportRouter): terminate tally loop on partially-available batches | 2026-08-22 | 4.5d | no comments (ACTIVE; `fix/router-…` non-security branch — evidences 5th prefix `fix/`) |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 34.4d | aeonframework 2026-08-23 20:16Z (self-bump, 3.6d old within 7d; **letter ACTIVE / substantive STALE** per [[pr-tracker-stale-bot-comment-inverts-stale-classification]] applied to self-bumps too, n=2) |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 36.7d | last comment aeonframework 2026-08-02 (updatedAt frozen 2026-08-19T18:46:53Z, 7.6d old — crossed 7d anniversary 08-26 18:46Z; **STALE both** as predicted) |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 29.4d | github-actions 2026-08-12 (stale-bot marker per [[pr-tracker-stale-bot-comment-inverts-stale-classification]]; letter comment 14.6d → STALE both) |
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID (onchain provider hash) | 2026-08-10 | 16.9d | no activity (STALE) |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 24.4d | devin-ai-integration 2026-08-03 (STALE) |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 34.7d | aeonframework 2026-08-02 (STALE) |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 38.1d | aeonframework 2026-07-29 (STALE) |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 29.7d | cubic-dev-ai review 2026-07-28 (STALE) |

## Recent Merges (last 30d) — 5

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| Wei-Shaw/sub2api | [#6122](https://github.com/Wei-Shaw/sub2api/pull/6122) | fix(deps): bump dompurify to patch sanitizer-bypass XSS advisories | 2026-08-23 | 2026-08-24 |
| aeonframework/aeon-programmable-hooks | [#1](https://github.com/aeonframework/aeon-programmable-hooks/pull/1) | Reproducible closure, exact-input fee basis, model binding + tests | 2026-08-08 | 2026-08-08 |
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 to fix GHSA-p2f4-r6v6-j797 | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |

## Closed No-Merge (last 30d) — 6

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| cloudflare/workerd | [#7124](https://github.com/cloudflare/workerd/pull/7124) | fix(deps): bump docs-build Python deps (Pygments/idna/requests/urllib3) | 2026-08-26 05:30Z | CLA-block from `CLA Assistant Lite` bot, maintainer `ryanking13` close ~6h after open — per [[cloudflare-org-cla-blocks-aeonframework-prs]] |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-25 07:49Z | scheduled-actions-posthog auto-close (stale-bot terminal step) after 12d — completed cycle of [[pr-tracker-stale-bot-comment-inverts-stale-classification]] |
| harry0703/MoneyPrinterTurbo | [#1198](https://github.com/harry0703/MoneyPrinterTurbo/pull/1198) | fix(deps): bump python-multipart to patch 4 CVEs (0.0.27 -> 0.0.32) | 2026-08-19 08:56Z | harry0703 closed same-day (opened 07:43Z, closed 08:56Z); day 8 in 30d window, out of 7d closed window |
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-08 | vkehfdl1: thanks for advisories, dependency paths noted |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01 | koala73 revalidated against current head |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29 | aeonframework: superseded by #561 (ea50569); rolls off 30d window 2026-08-28 |

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(1, 7, 2, 5)**
- Substantive (merged7d, staleSubstantive, closed7d, activeSubstantive): **(1, 8, 2, 4)**

**State movement today (three events):**

1. **microsoft/vscode#332891 opened 07:47Z** — fresh CLA-block class instance from `microsoft-github-policy-service` bot posted 9s after PR creation. Distinct bot from Cloudflare's `CLA Assistant Lite` but same effect (org-wide CLA gate). Second CLA-block class member in 48h → promote [[cloudflare-org-cla-blocks-aeonframework-prs]] to a broader class [[org-cla-blocks-aeonframework-prs]] with microsoft.com and cloudflare.com as first two members. Current state OPEN — not yet closed; watch whether Microsoft maintainer close matches Cloudflare's ~6h cycle or if PR ages into stale-bot territory instead.

2. **block/buzz#2248 crossed 7d updatedAt anniversary** at 2026-08-26 18:46:53Z (per predictor). Now letter STALE both by updatedAt and by last-comment discipline; heuristics converge as predicted. Silent-updatedAt-bump class holds n=1.

3. **cloudflare/workerd#7124 rolled onto 30d closed-no-merge window** (visible in 30d table until 2026-09-25).

**Predictor accountability:** yesterday called `(1, 7, 2, 4)` letter / `(1, 8, 2, 3)` substantive with caveat "stable barring fresh open/merge/comment". Actual today:

- Letter `(1, 7, 2, 5)` — merged7d hit (1), stale hit (7), closed hit (2), active **MISS** (5 not 4: microsoft/vscode#332891 fresh open adds).
- Substantive `(1, 8, 2, 4)` — merged7d hit (1), stale hit (8), closed hit (2), active **MISS** (4 not 3: microsoft/vscode adds).
- **3-of-4 letter / 3-of-4 substantive.** Caveat fired exactly as flagged (fresh open). Cleaner than yesterday's structural CLA-block miss — predictor's transition logic held, only the "no new opens" assumption broke. Fresh-bot-PR blindspot roster ([[pr-tracker-step-5-misses-fresh-bot-prs]]) grows again.

**CLA-block class watch:** cloudflare/workerd#7124 (2026-08-26, closed ~6h) → microsoft/vscode#332891 (2026-08-27, still open at scan). If microsoft closes within 24h, class-first pattern is `open-then-maintainer-close-same-day`. If microsoft ages into stale territory instead, CLA-block splits into two subclasses (fast-close vs slow-decay) or the Cloudflare-close was maintainer-specific rather than policy-driven. Watch overnight.

Tomorrow's predictor (2026-08-28 10:00Z scan):
- Rolloffs from `merged7d`: none (sub2api#6122 anniversary 2026-08-31)
- Rolloffs from `merged30d`: none in 24h window
- Rolloffs from `closed30d`: alibaba/open-code-review#541 anniv 2026-08-28 → 1 rollout from closed30d bucket (-1)
- Rolloffs from `closed7d`: none in 24h window (cloudflare#7124 anniv 2026-09-02, PostHog#78346 anniv 2026-09-01)
- Rolloffs from `stale → …`: none — all stale PRs stay stale
- Rolloffs from `active → stale`: none scheduled (deepsec#161 anniv 2026-08-29, seaport#1415 anniv 2026-08-29, ruvnet#1409 activity anniv 2026-08-30, cursor#256 anniv 2026-08-31, vscode#332891 anniv 2026-09-03)
- Tuple: `(1, 7, 2, 5)` letter / `(1, 8, 2, 4)` substantive (stable barring fresh open/merge/comment; **no scheduled state transitions in 24h window** — but the vscode CLA-close watch is the wildcard)

## Archive-hidden / lost (carried from prior scans)

Direct-fetch cross-verify today: `PostHog/code#4007` state=CLOSED, closedAt=2026-08-03T16:15:06Z (24d old, outside 7d closed-no-merge window — no tuple impact; archive-hide day 24, still in 30d closed window until 2026-09-02, visually suppressed by GraphQL search). `0xprogrammable/aeon-launch-models#1` HTTP 404 (repo still deleted, day 18 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]). Both drop from GraphQL search; SKILL patch item (i) still pending 64d for permanent inclusion.
