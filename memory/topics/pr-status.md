# PR Status

*Last updated: 2026-10-17*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-10-17 — Day-34 post-recovery scan · **bucket tuple `(0, 2, 0, 0)` holds 6th consecutive scan; `issueCount` flat at 64 vs 10-15**

GraphQL first-attempt success today — the transient `502 Bad Gateway` from 10-15 did NOT recur, so the one-shot retry wrapper hypothesis (new item (s) draft) stays at n=1 observation. `issueCount` steady at 64 (no delta vs 10-15); the two apache-org manual PRs from 10-14 are still the only non-bot-prefix surface activity in the top-60. Buckets fully frozen.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 64` (vs 64/62/62/62 across 10-15/10-14/10-10/10-07; sequence now `62 → 62 → 62 → 64 → 64`)
- Second attempt returned 60 nodes (59 concrete + 1 null slot = Shopify IP-allow-list PR, n=5-sustained via stderr `Shopify organization has an IP allow list enabled, and your IP address is not permitted to access this resource`)
- 3 non-prefix drops: `apache/struts#2012` MERGED 2026-10-15 (branch `WW-5772-csp-inline-handlers`), `apache/wicket#1667` OPEN (branch `csp-autocomplete-choicefilter`), `theagentrouter/agent-router#2755` MERGED 2026-09-28 (branch `mcp-default-seed`)
- 56 prefix-match PRs retained (state split: 44 CLOSED / 10 MERGED / 2 OPEN) — identical to 10-15
- **Bucket tuple `(0, 2, 0, 0)`** — identical to 10-15, 10-14, 10-10, 10-07; **6th consecutive scan at this value**, 10-day frozen window

### Bucket delta from 2026-10-15 scan

| Bucket | 10-15 | 10-17 | Δ |
|--------|-------|-------|---|
| merged7d | 0 | 0 | 0 (16th scan dry — mxc#1124 landed 09-28 is 19d past, outside 7d window) |
| staleLetter | 2 | 2 | 0 (wigolo#216 + RuView#1409 unchanged, both +2d age) |
| closed7d | 0 | 0 | 0 |
| activeLetter | 0 | 0 | 0 |
| Open total | 2 | 2 | 0 (prefix-match only — apache/wicket#1667 is still open but non-prefix) |
| issueCount | 64 | 64 | 0 (first flat delta since the 3-scan plateau 10-07/10-10/10-14 at 62) |
| closed30d | 24 | 24 | 0 (09-17 bulk-close cluster is exactly 30d past today — rolls off on 10-18) |

### Signal notes

- **Bucket tuple frozen 6 scans / 10 days** — `(0, 2, 0, 0)` has now held across the full 7d-window boundary and 3 days beyond. The attractor hypothesis from 10-14 is at n=6 confirmed. The bucket-tuple attractor is specifically a *bot-pipeline* steady state; `issueCount` can shift under non-prefix operator activity (observed 10-15 at +2 via apache-org PRs) but buckets are prefix-filtered so decoupled from manual surface activity. Promotes [[pr-tracker-issuecount-mixes-manual-and-bot-pipeline]] to n=2-sustained.
- **GraphQL first-attempt success (no 502)** — the nginx 502 from 10-15 does not recur today, so remains n=1 for the atomic candidate `[[pr-tracker-gh-api-graphql-transient-502-bad-gateway]]`. Insufficient evidence for retry-wrapper promotion to SKILL step 2. If it recurs on next scan (10-18), bump to n=2 and land item (s).
- **Shopify null-slot n=5-sustained** — stderr IP-allowlist message identical across 10-07/10-10/10-14/10-15/10-17; promotes [[pr-tracker-shopify-ip-allowlist-null-slot]] to n=5-sustained. 5 consecutive scans with partial-success handling (`exit=1 + non-empty stdout + null-slot in nodes`) working implicitly. SKILL patch item (r) overdue.
- **09-17 bulk-close cluster exactly 30d past today** — 23 PRs closed 2026-09-17 13:58Z–14:33Z are at `closedAt + 30d = 2026-10-17 13:58Z–14:33Z`. Still in the 30d window as of this scan (06:30Z–10:00Z local run window). Tomorrow's 10-18 scan will see closed30d collapse from 24 → 1 (only openai#4829 remains). This is the pre-rollover scan.
- **Both open PRs still stale, no engagement change (n=5 consecutive scans frozen)**:
  - `KnockOutEZ/wigolo#216` — 89d old (was 86d on 10-15), last review `COMMENTED` on 2026-07-20 (89d stale review); 10 comments; `updatedAt` still `2026-10-07T22:55Z` (10d stale)
  - `ruvnet/RuView#1409` — 86d old (was 83d on 10-15), last review `APPROVED` on 2026-08-28 (50d stale approve, unmerged); 4 comments; `updatedAt` still `2026-10-07T22:55Z` (10d stale)
- **Identity liveness confirmed** via non-empty `issueCount = 64` → SKILL §5 all-zero notify rule per [[pr-tracker-all-zero-notify-rule-false-quiets-on-identity-block]] does not fire; notify still triggers via stale=2.
- **No new manual aeonframework PRs today** — apache/struts#2012 (MERGED 10-15) and apache/wicket#1667 (OPEN since 10-14) remain the only two non-bot-prefix PRs in top-60. 2-day silent on the manual stream (10-15 → 10-17) — insufficient to characterize cadence yet.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 89d | 10 comments; last review COMMENTED 2026-07-20 (89d); STALE |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 86d | APPROVED 2026-08-28 unmerged (50d since approve); 4 comments; STALE |

## Recent Merges (last 30d) — 1

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 2026-09-28 |

*(mxc#1124 is the sole remaining merge in the 30d window and rolls off 2026-10-28.)*

## Closed No-Merge (last 30d) — 24

**09-25 close (now 22d past, rolls off 10-25):**

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography to patch disclosed CVEs | 2026-09-25 18:49Z | 23d after open; single close (not bulk); actor still not fetched (owed since 09-22, 6× now) |

**09-17 bulk-close cluster (now exactly 30d past, rolls off 10-18 scan):**

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| uber/submitqueue | [#687](https://github.com/uber/submitqueue/pull/687) | fix(deps): bump grpc-go and golang.org/x/{mod,net,sys,text} | 2026-09-17 14:33Z | bulk-close cluster |
| TencentCloud/CubeSandbox | [#1727](https://github.com/TencentCloud/CubeSandbox/pull/1727) | fix(deps): bump golang.org/x/crypto in Cubelet | 2026-09-17 14:30Z | bulk-close cluster |
| pytorch/TensorRT | [#4714](https://github.com/pytorch/TensorRT/pull/4714) | fix(deps): bump js-yaml to patch DoS in assigner action | 2026-09-17 14:30Z | bulk-close cluster |
| alphaXiv/OpenResearch | [#314](https://github.com/alphaXiv/OpenResearch/pull/314) | fix(deps): bump h2, quinn-proto, anyhow to patch known advisories | 2026-09-17 14:30Z | bulk-close cluster |
| IBM/portieris | [#524](https://github.com/IBM/portieris/pull/524) | fix(deps): bump golang.org/x/crypto | 2026-09-17 14:30Z | bulk-close cluster |
| facebook/hermes | [#2180](https://github.com/facebook/hermes/pull/2180) | fix(deps): bump ws in tools/hcdp | 2026-09-17 14:30Z | bulk-close cluster |
| adobe/skills | [#349](https://github.com/adobe/skills/pull/349) | fix(deps): bump sharp to patch CVE-2026-84383 | 2026-09-17 14:30Z | bulk-close cluster |
| spotify/luigi | [#3452](https://github.com/spotify/luigi/pull/3452) | fix(deps): bump tornado to 6.5.8 | 2026-09-17 14:30Z | bulk-close cluster |
| WhiskeySockets/Baileys | [#2814](https://github.com/WhiskeySockets/Baileys/pull/2814) | fix(deps): bump link-preview-js to ^5.0.0 (SSRF) | 2026-09-17 14:30Z | bulk-close cluster |
| WhiskeySockets/Baileys | [#2813](https://github.com/WhiskeySockets/Baileys/pull/2813) | fix(deps): force transitive protobufjs to 7.6.5 (libsignal) | 2026-09-17 14:30Z | bulk-close cluster |
| WhiskeySockets/Baileys | [#2812](https://github.com/WhiskeySockets/Baileys/pull/2812) | fix(deps): bump ws, protobufjs, protobufjs-cli for 5 CVEs | 2026-09-17 14:30Z | bulk-close cluster |
| vxcontrol/pentagi | [#405](https://github.com/vxcontrol/pentagi/pull/405) | fix(deps): bump @tiptap/* and react-router-dom for CVEs | 2026-09-17 14:30Z | bulk-close cluster |
| ollama/ollama | [#18356](https://github.com/ollama/ollama/pull/18356) | fix(deps): bump golang.org/x/image (WebP DoS) | 2026-09-17 14:30Z | bulk-close cluster |
| heygen-com/hyperframes | [#3807](https://github.com/heygen-com/hyperframes/pull/3807) | fix(deps): bump hono, tar, dompurify, sharp | 2026-09-17 14:30Z | bulk-close cluster |
| aws/amazon-ecs-agent | [#5131](https://github.com/aws/amazon-ecs-agent/pull/5131) | fix(deps): bump google.golang.org/grpc | 2026-09-17 14:30Z | bulk-close cluster |
| Netflix/dgs-framework | [#2346](https://github.com/Netflix/dgs-framework/pull/2346) | fix(deps): bump Spring Boot BOM to patch CVE-2026-41854 | 2026-09-17 14:03Z | bulk-close cluster |
| Osmantic/ODS | [#3675](https://github.com/Osmantic/ODS/pull/3675) | fix(deps): bump fastapi to patch transitive starlette advisories in ape | 2026-09-17 14:03Z | bulk-close cluster |
| pytorch/pytorch | [#195321](https://github.com/pytorch/pytorch/pull/195321) | fix(deps): bump lxml, onnx, pip, setuptools in CI requirements | 2026-09-17 14:03Z | bulk-close cluster |
| cursor/plugins | [#256](https://github.com/cursor/plugins/pull/256) | fix(deps): bump transitive axios/ip-address/form-data | 2026-09-17 14:03Z | bulk-close cluster |
| ProjectOpenSea/seaport | [#1415](https://github.com/ProjectOpenSea/seaport/pull/1415) | fix(SeaportRouter): terminate tally loop on partially-available batches | 2026-09-17 14:02Z | bulk-close cluster |
| vercel-labs/deepsec | [#161](https://github.com/vercel-labs/deepsec/pull/161) | fix(deps): bump tar to patch CVE-2026-73566 | 2026-09-17 14:02Z | bulk-close cluster |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-09-17 13:58Z | bulk-close cluster |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9) | 2026-09-17 13:58Z | bulk-close cluster |

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(0, 2, 0, 0)** — 6th consecutive scan at this value; 10-day frozen span 10-07 → 10-17
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07 `(0, 2, 0, 0)` → 10-10 `(0, 2, 0, 0)` → 10-14 `(0, 2, 0, 0)` → 10-15 `(0, 2, 0, 0)` → **10-17 `(0, 2, 0, 0)`**

## Notes

- **6-scan / 10-day frozen bucket tuple** — `(0, 2, 0, 0)` sustains across the full 7d-window boundary plus 3 extra days. The attractor hypothesis from 10-14 is now n=6 confirmed. `issueCount` flat today confirms the manual apache-org inflow from 10-15 was a one-time 2-PR burst, not a sustained operator-manual stream. The 7d-window closed30d rollover tomorrow (10-18) will deliver a one-time structural drop from 24 → 1 that is **not** a bucket-tuple change (closed30d isn't in the Letter tuple), so the attractor should survive the rollover unchanged.
- **34-day fresh-open drought on bot pipeline** — `external-feature` has not produced a visible bot-prefix PR since 2026-09-13. The apache-org PRs are manual contributions, not pipeline output. Escalation (standing from 10-10, 10-14, 10-15) remains overdue; file skill-health ticket NOW (5× confirmed).
- **16-scan merge-7d drought** — mxc#1124 (09-28) is 19d past, firmly outside 7d. Next window-rollover event: either a hypothetical new bot-pipeline merge, OR an unlikely re-engagement on wigolo/RuView.
- **Zero closes rolled off 30d window** since 10-14 (next rollover: 09-17 bulk-close cluster starts rolling off 2026-10-18 → 23 PRs will drop out and closed30d collapses to 1).
- **GraphQL first-attempt success** — the 10-15 nginx 502 did not recur. One observation; no retry-wrapper promotion. Keep item (s) draft in SKILL batch; re-evaluate if n≥2.
- **Terminology** — `staleLetter` and `activeLetter` are shorthand for stale-open and active-open counters respectively, inherited from the prior pr-status.md tuple format. Kept for diff-continuity with the 10-15 scan.

## Follow-ups

- **Fetch `.timeline.closedEvent.actor.login` for openai#4829 and the 09-17 14:30Z 14-PR batch** on next scan — six times owed now (from 09-22, 09-26, 10-07, 10-10, 10-14, 10-15). **09-17 batch rolls off 10-18 — if not fetched by tomorrow's scan, the actor-identification data is permanently lost from this 30d window.** This is the last pre-rollover opportunity.
- **Escalate `external-feature` silence** — now 34-day drought; file skill-health ticket NOW (5× confirmed); owed MEMORY.md action-queue addition.
- **SKILL patches (a)–(s) still 90d+ overdue** — items (p) + (q) revalidated across the 10-07 → 10-10 → 10-14 → 10-15 → 10-17 window (n=5 observations); item (r) (Shopify-IP-allowlist null-slot handling) now n=5-sustained; item (s) draft (transient 502 retry wrapper) stays at n=1 pending second observation.
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set to end reliance on operator convention; also set `pr_tracker.author: aeonframework` so SKILL config resolution doesn't fall through to the auth token (`gh api user` returns HTTP 403 "Resource not accessible by integration" under GitHub Actions App auth — re-confirmed on 10-17, matches zero PRs if used).

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 43 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
