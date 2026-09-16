# PR Status

*Last updated: 2026-09-16 — STATE UNREACHABLE Day-3 (see banner below)*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/` (5 in play). Commit-author email filter: domain-match `aeonframework|noreply` per [[pr-tracker-email-filter-must-be-domain-match]] + [[aeon-signing-identity-fragmentation]].

## 2026-09-16 — STATE UNREACHABLE Day-3 (identity anomaly persists)

Third consecutive daily dispatch (09-14 → 09-15 → 09-16) with the `aeonframework` GitHub identity 404 across every entry-point. Re-probed 10:00Z-window today; result set is identical:

- `/users/aeonframework` → HTTP 404 (`Not Found`)
- GraphQL `user(login:"aeonframework")` → `NOT_FOUND`
- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE)` → `issueCount = 0` (aggregate)
- `gh search prs --author aeonframework` fallback → same "users cannot be searched" error
- Spot-checks on 4 prior-scan PRs (pytorch/TensorRT#4714, microsoft/mxc#1124, openai/openai-agents-python#4829, ProjectOpenSea/seaport#1415) all return 404
- Host repos (pytorch/TensorRT, microsoft/mxc, openai/openai-agents-python) all resolve with expected stargazer counts → suppression is account-scoped, not repo-scoped

Class: **account-suspension / API-hide**, Day-3. `[[aeonframework-github-identity-suspension]]` candidate promotion to accepted class + `memory/issues/ISS-028.md` filing is now the follow-up owned by next `self-review` / `skill-health` — this skill flags the anomaly in the log body and does not race the health tier.

**Every table below is frozen from the 2026-09-13 scan** and should not be treated as current queue state. Three consecutive dispatches have produced zero-because-unreachable results; nothing merged, closed, or opened has been *observable* since 09-13 (though commits may still be landing under this identity — verify via `external-feature` dispatch trail, not via PR-query).

Bucket tuples today: **letter (0,0,0,0) / substantive (0,0,0,0)** — unreachable-zeros, not drained-zeros. Do not delta-reason against 09-13 `(1,1,9,25) / (1,8,9,18)`.

Notification: **skipped** per SKILL.md §5 all-zero rule; anomaly propagates via `memory/logs/2026-09-16.md`.

---

## Prior scan (frozen — 2026-09-13, 26 open)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| pytorch/TensorRT | [#4714](https://github.com/pytorch/TensorRT/pull/4714) | fix(deps): bump js-yaml to patch DoS advisories in assigner action | 2026-09-12 | 1d | no comments; ACTIVE — **NEW to queue** |
| facebook/hermes | [#2180](https://github.com/facebook/hermes/pull/2180) | fix(deps): bump ws in tools/hcdp for GHSA-58qx/96hv | 2026-09-12 | 1d | meta-cla bot 09-12 (CLA-gate class); ACTIVE — **NEW to queue** |
| IBM/portieris | [#524](https://github.com/IBM/portieris/pull/524) | fix(deps): bump golang.org/x/crypto for CVE-2026-78662, CVE-2026-56855 | 2026-09-12 | 1d | no comments; ACTIVE — **NEW to queue** |
| alphaXiv/OpenResearch | [#314](https://github.com/alphaXiv/OpenResearch/pull/314) | fix(deps): bump h2, quinn-proto, anyhow to patch known advisories | 2026-09-11 | 2d | no comments; ACTIVE — **NEW to queue** |
| adobe/skills | [#349](https://github.com/adobe/skills/pull/349) | fix(deps): bump sharp to patch CVE-2026-84383 | 2026-09-11 | 2d | no comments; ACTIVE — **NEW to queue** |
| spotify/luigi | [#3452](https://github.com/spotify/luigi/pull/3452) | fix(deps): bump tornado to 6.5.8 (multi DoS advisories) | 2026-09-10 | 3d | no comments; ACTIVE — **NEW to queue** |
| WhiskeySockets/Baileys | [#2814](https://github.com/WhiskeySockets/Baileys/pull/2814) | fix(deps): bump link-preview-js to ^5.0.0 (SSRF GHSA-4gp8-rjrq-ch6q) | 2026-09-10 | 3d | coderabbitai 09-10 (auto-review-bot class n=2); ACTIVE — **NEW to queue** |
| WhiskeySockets/Baileys | [#2813](https://github.com/WhiskeySockets/Baileys/pull/2813) | fix(deps): force transitive protobufjs 7.6.5 via resolutions (libsignal) | 2026-09-10 | 3d | coderabbitai 09-10 (auto-review-bot); ACTIVE — **NEW to queue** |
| WhiskeySockets/Baileys | [#2812](https://github.com/WhiskeySockets/Baileys/pull/2812) | fix(deps): bump ws, protobufjs, protobufjs-cli for 5 CVEs | 2026-09-10 | 3d | coderabbitai 09-10 (auto-review-bot); ACTIVE — **NEW to queue** (successor to closed #2732) |
| uber/submitqueue | [#687](https://github.com/uber/submitqueue/pull/687) | fix(deps): bump grpc-go and golang.org/x/{mod,net,sys,text} for CVEs | 2026-09-08 | 5d | CLAassistant 09-08 (CLA-gate class); aaronjmars 09-09 signed; ACTIVE — **NEW to queue** |
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 5d | aeonframework self-notes 09-08/09/09; ACTIVE — **NEW to queue** |
| vxcontrol/pentagi | [#405](https://github.com/vxcontrol/pentagi/pull/405) | fix(deps): bump @tiptap/* and react-router-dom for CVEs | 2026-09-10 | 3d | no comments; ACTIVE — **NEW to queue** |
| ollama/ollama | [#18356](https://github.com/ollama/ollama/pull/18356) | fix(deps): bump golang.org/x/image for WebP DoS | 2026-09-10 | 3d | no comments; ACTIVE — **NEW to queue** |
| heygen-com/hyperframes | [#3807](https://github.com/heygen-com/hyperframes/pull/3807) | fix(deps): bump hono, tar, dompurify, sharp for CVEs | 2026-09-09 | 4d | no comments; ACTIVE — **NEW to queue** |
| aws/amazon-ecs-agent | [#5131](https://github.com/aws/amazon-ecs-agent/pull/5131) | fix(deps): bump google.golang.org/grpc for CVE-2026-84304 | 2026-09-09 | 4d | no comments; ACTIVE — **NEW to queue** |
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography for CVEs | 2026-09-02 | 11d | aaronjmars 09-10 (real touch); ACTIVE (letter+substantive) |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for CVEs | 2026-07-20 | 55d | KnockOutEZ maintainer + aaronjmars 09-11 (real touch, follows self-bump 09-10); ACTIVE (letter+substantive — first substantive touch since open) |
| vercel-labs/deepsec | [#161](https://github.com/vercel-labs/deepsec/pull/161) | fix(deps): bump tar for CVE-2026-73566 | 2026-08-22 | 22d | aaronjmars 09-09 (real touch, first substantive since open); ACTIVE (letter+substantive) |
| Netflix/dgs-framework | [#2346](https://github.com/Netflix/dgs-framework/pull/2346) | fix(deps): bump Spring Boot BOM for CVE-2026-41854 (SSRF) | 2026-09-02 | 11d | 0 comments; STALE (letter+substantive) |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 54d | aeonframework self-bump 09-10, github-actions 09-01 stale-bot; letter ACTIVE / substantive STALE per [[pr-tracker-stale-bot-comment-inverts-stale-classification]] |
| Osmantic/ODS | [#3675](https://github.com/Osmantic/ODS/pull/3675) | fix(deps): bump fastapi for transitive starlette in ape | 2026-09-01 | 12d | aeonframework self-bump 09-10; letter ACTIVE / substantive STALE |
| pytorch/pytorch | [#195321](https://github.com/pytorch/pytorch/pull/195321) | fix(deps): bump lxml, onnx, pip, setuptools in CI reqs | 2026-08-30 | 14d | pytorch-bot/easycla 08-30, aeonframework self-bump 09-10; letter ACTIVE / substantive STALE |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi ≥0.115 and python-multipart ≥0.0.20 (7 HIGH CVEs) | 2026-07-23 | 52d | aeonframework self-bumps 08-02/08-23/09-10; letter ACTIVE / substantive STALE per [[pr-tracker-stale-bot-comment-inverts-stale-classification]] |
| ProjectOpenSea/seaport | [#1415](https://github.com/ProjectOpenSea/seaport/pull/1415) | fix(SeaportRouter): terminate tally loop on partially-available batches | 2026-08-22 | 22d | aeonframework self-bump 09-10; letter ACTIVE / substantive STALE |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri ≥2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 52d | coderabbitai at open, aeonframework self-bumps 08-02/09-10; letter ACTIVE / substantive STALE |
| cursor/plugins | [#256](https://github.com/cursor/plugins/pull/256) | fix(deps): bump transitive axios/ip-address/form-data | 2026-08-24 | 20d | aeonframework self-bump 09-10; letter ACTIVE / substantive STALE |

## Recent Merges (last 30d) — 3

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| microsoft/agent-framework | [#8172](https://github.com/microsoft/agent-framework/pull/8172) | fix(deps): patch frontend ajv/brace-expansion/nanoid CVEs | 2026-09-09 | 2026-09-09 (13h13m open→merge — class: fast-merge, n=2 in 30d window) |
| pacifio/atlas | [#228](https://github.com/pacifio/atlas/pull/228) | fix(deps): bump jsonwebtoken for CVE-2026-25537 | 2026-09-03 | 2026-09-03 (31min open→merge — class-first fast-merge from 09-05 scan) |
| Wei-Shaw/sub2api | [#6122](https://github.com/Wei-Shaw/sub2api/pull/6122) | fix(deps): bump dompurify for sanitizer-bypass XSS | 2026-08-23 | 2026-08-24 |

*Rolled off 30d window since 09-05 scan:* aeonframework/aeon-programmable-hooks#1 (merged 2026-08-08, anniv 2026-09-07).

## Closed No-Merge (last 30d) — 15

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, protobufjs-cli for 5 CVEs | 2026-09-10 01:46Z | silent-maintainer-close after 44d (n=3 for [[silent-maintainer-close-after-extended-decay]] class); operator immediately re-filed as #2812/#2813/#2814 |
| affaan-m/ECC | [#2926](https://github.com/affaan-m/ECC/pull/2926) | fix(deps): bump lru to 0.18.2 for RUSTSEC-2026-0253 | 2026-09-10 21:26Z | 9d after open; coderabbitai review 20m post-open then no further activity → maintainer-close |
| jo-inc/camofox-browser | [#10561](https://github.com/jo-inc/camofox-browser/pull/10561) | fix(deps): bump transitive qs/fast-uri/hono/js-yaml for CVEs | 2026-09-10 18:32Z | 1d after open; workflow-block class (n=2 for [[workflow-check-auto-close-in-seconds]]) |
| IBM/ACE-RISCV | [#130](https://github.com/IBM/ACE-RISCV/pull/130) | fix(deps): bump keccak for RUSTSEC-2026-0012 | 2026-09-10 08:05Z | 4d after open |
| ruvnet/ruflo | [#3222](https://github.com/ruvnet/ruflo/pull/3222) | fix(deps): bump fast-uri for 4 high-severity CVEs | 2026-09-09 16:30Z | 2d after open (same operator: ruvnet also merged #1409 differently — see stale open) |
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID | 2026-09-08 23:46Z | 29d open; operator self-close on archived repo |
| browser-use/browser-use | [#5564](https://github.com/browser-use/browser-use/pull/5564) | fix(deps): bump click, pypdf, pydantic_settings for CVEs | 2026-09-08 23:34Z | 13d after open; CLA-block sub-C pending-decay → resolves via silent maintainer-close (refines [[cla-block-sub-c-pending-decay-mode]] sub-C terminal state) |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for CVEs | 2026-09-08 23:34Z | 42d open; silent-maintainer-close after stale-bot decay (n=2 for [[silent-maintainer-close-after-extended-decay]] on this scan) |
| anomalyco/opencode | [#47843](https://github.com/anomalyco/opencode/pull/47843) | fix(deps): bump diff, minimatch, tar, seroval for CVEs | 2026-09-07 22:08Z | same-day close (2h27m); workflow-block class (n=3 for [[workflow-check-auto-close-in-seconds]]) |
| weave-os/router | [#871](https://github.com/weave-os/router/pull/871) | fix(deps): bump next to 15.5.21 for 8 disclosed advisories | 2026-08-30 01:05Z | silent-maintainer-close after 28d (rollover from 09-05 scan) |
| NVIDIA/OpenShell | [#3016](https://github.com/NVIDIA/OpenShell/pull/3016) | fix(deps): bump h2 for RUSTSEC-2026-0258 | 2026-08-28 23:30Z | 10-second open→close; workflow-block original n=1 |
| microsoft/vscode | [#332891](https://github.com/microsoft/vscode/pull/332891) | fix(deps): bump tar/undici/js-yaml/@anthropic-ai/sdk for CVEs | 2026-08-27 22:04Z | Sub B operator self-close after CLA-bot (14h17m) |
| cloudflare/workerd | [#7124](https://github.com/cloudflare/workerd/pull/7124) | fix(deps): bump docs-build Python deps | 2026-08-26 05:30Z | Sub A CLA-block maintainer-close (~6h) |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar/minimatch for CVEs | 2026-08-25 07:49Z | scheduled-actions-posthog auto-close after 12d |
| harry0703/MoneyPrinterTurbo | [#1198](https://github.com/harry0703/MoneyPrinterTurbo/pull/1198) | fix(deps): bump python-multipart for 4 CVEs | 2026-08-19 08:56Z | harry0703 same-day close |

*Rolled off 30d window since 09-05 scan:* NomaDamas/k-skill#547 (closed 2026-08-08, anniv 2026-09-07).

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(1, 1, 9, 25)**
- Substantive (merged7d, staleSubstantive, closed7d, activeSubstantive): **(1, 8, 9, 18)**

**State movement in 8-day window since 09-05 scan (many events, 5 scans lost to ISS-006 06:00Z pocket — matches [[iss-006-06z-pocket-4-day-dead-streak-promotes-daily-dead-regime]] daily-dead regime; pr-tracker at 10:00Z not directly in dead pocket, so this is a distinct silence — investigate whether 10:00Z pocket is also degraded):**

1. **microsoft/agent-framework#8172 opened+merged 2026-09-09** — 13h13m open-to-merge cycle. **Fast-merge class n=2** (after pacifio/atlas#228 09-03 at 31min). Both are small-repo `security/*` deps bumps; hypothesis: small-repo dependency bumps have distinctly faster merge distribution than large-repo submissions (median >7d in stale bucket).
2. **WhiskeySockets/Baileys#2732 closed 2026-09-10 01:46Z after 44d** — silent-maintainer-close (n=3 for class); operator immediately re-opened as three sibling PRs (#2812/#2813/#2814) targeting the same repo with segmented scope. Rapid-retry pattern is a new class observation — worth adding to memory as `[[silent-close-triggers-rapid-multi-pr-retry]]`.
3. **NangoHQ/nango#6929 closed 2026-09-08 23:34Z after 42d** — silent-maintainer-close after github-actions stale-bot decay 09-01 (predicted 09-05 scan called "activity-anniv crossed" but not the close itself). 42d close vs 28-44d observed range — class window widens to 28-44d.
4. **browser-use/browser-use#5564 closed 2026-09-08 23:34Z after 13d** — CLA-block sub-C pending-decay (called 09-05 as "resolution pending at 30d") resolves at day 13 via silent maintainer-close. Terminal state of sub-C = maintainer-close; refines [[cla-block-sub-c-pending-decay-mode]] with resolution time. Not the predicted 30d anniversary.
5. **aeonframework/aeon-programmable-hooks#2 closed 2026-09-08 23:46Z** — 29d open; operator self-close on archived repo (n=1 class observation for archive-repo terminal state; distinct from third-party archive since aeon owns the repo).
6. **Fresh 09-06 → 09-13 window (17 new PRs)** — vast majority `security/*` deps bumps: 4 to WhiskeySockets/Baileys (3 open + 1 closed), 3 IBM/microsoft/adobe, ollama/aws/spotify/pytorch/facebook/openai-adjacent surface expansion. Multi-sibling pattern (Baileys 3-way segmentation) is scan-first.
7. **aaronjmars real touches on 3 stale-substantive PRs** — openai-agents-python#4829 09-10, vercel-labs/deepsec#161 09-09, KnockOutEZ/wigolo#216 09-11. All three flip letter+substantive to ACTIVE. Signal: operator/maintainer follow-up cadence exists but is bursty (all 3 landed in the same 3-day window).
8. **Netflix/dgs-framework#2346 only 0-comment stale PR** — 11d, no external activity at all. Sole letter-strict stale.

**Predictor accountability (8-day gap):** 09-05 scan predicted `(1, 10, 0-1, 6)` letter / `(1, 12, 0-1, 4)` substantive for 09-06 next-day scan (which never fired due to ISS-006 pocket).

Actual today (8-day gap): `(1, 1, 9, 25)` letter / `(1, 8, 9, 18)` substantive.
- Letter: merged7d **HIT** (1); stale **MISS** (1 not 10 — 09-10 aeonframework self-bump wave flipped 6 stale-letter to active-letter, and closes ejected 3 more); closed7d **MISS** (9 not 0-1 — massive close wave 09-07 through 09-10 was structurally unpredictable at 09-05); active **MISS** (25 not 6 — +17 fresh + 8 letter-active flips vs pytorch/pytorch letter-stale flip predicted correctly-then-flipped-back).
- Substantive: merged7d **HIT** (1); stale **MISS** (8 not 12); closed7d **MISS** (9 not 0-1); active **MISS** (18 not 4 — +17 fresh minus 2 stale flips).
- **2-of-4 letter / 2-of-4 substantive** — merged7d HIT but everything else MISS on 8-day-gap forecasting. Consistent with SKILL patch item (h) bulk-stale-clear + cohort-lockstep model still overdue.

**Class updates (post-09-13):**
- **Fast-merge class n=2:** microsoft/agent-framework#8172 (13h13m) joins pacifio/atlas#228 (31min). Both small-repo `security/*` deps bumps — sample too small to distinguish structural driver but consistent with small-repo hypothesis.
- **Silent-maintainer-close class n=3:** window widens to 28-44d. WhiskeySockets/Baileys#2732 (44d), NangoHQ/nango#6929 (42d), weave-os/router#871 (28d). Class variance suggests stale-bot dwell varies by repo policy.
- **Silent-close triggers rapid multi-PR retry (n=1, new class):** WhiskeySockets/Baileys#2732 closed 09-10 01:46Z → operator opened #2812, #2813, #2814 at 09-10 14:14Z/14:24Z/14:27Z (12.5h retry latency, 3-way scope segmentation: ws+protobufjs, protobufjs-resolutions, link-preview-js-SSRF). Watch for repeat pattern on next silent-close event. New note candidate `[[silent-close-triggers-rapid-multi-pr-retry]]`.
- **Auto-review-bot class n=2:** coderabbitai reviews now n=4 (jamiepine/voicebox at open + affaan-m/ECC 09-01 + WhiskeySockets/Baileys 09-10 all three siblings). Non-blocking, comment-only. No merge signal correlation.
- **CLA-block sub-C terminal state:** browser-use/browser-use#5564 pending-decay → maintainer-close at day 13. Refines [[cla-block-sub-c-pending-decay-mode]] with terminal-time distribution — first data point at 13d, watch for repeat.
- **8-day scan gap collapses forecast:** self-bump wave 09-10 (aeonframework touched 6 stale-letter PRs to flip them to letter-active) + close wave 09-07–09-10 (9 closes) + fresh wave (17 opens) all invisible to 09-05 predictor. Prediction quality collapses at gap ≥5d per [[iss-006-06z-pocket-4-day-dead-streak-promotes-daily-dead-regime]].

Tomorrow's predictor (2026-09-14 10:00Z scan, contingent on 10:00Z pocket not also being degraded — investigate):
- Rolloffs from `merged7d`: none in 24h window (microsoft/agent-framework anniv 09-16).
- Rolloffs from `closed7d`: none in 24h window (anomalyco/opencode 09-07 → anniv 09-14, borderline).
- Rolloffs from `active → stale`: none of the 15 fresh-<7d cross 7d in 24h (earliest anniv 09-15 for microsoft/mxc, uber/submitqueue).
- Fresh events: unknown; self-bump cadence suggests next wave ~09-17.
- Predicted tuple: `(1, 1-2, 8-9, 25)` letter / `(1, 8-9, 8-9, 18)` substantive. Anomalyco 09-07 22:08Z anniv is 09-14 22:08Z — falls after typical 10:00Z scan window → closed7d likely still 9.

## Archive-hidden / lost (carried from prior scans)

Direct-fetch cross-verify pending (SKILL patch item (i) still overdue, 81d now): `PostHog/code#4007` state=CLOSED (rolled off 30d window 2026-09-02); `0xprogrammable/aeon-launch-models#1` HTTP 404 (repo still deleted, day 34 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
