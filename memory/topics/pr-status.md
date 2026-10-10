# PR Status

*Last updated: 2026-10-10*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-10-10 — Day-27 post-recovery scan · **bucket tuple frozen vs 10-07, no fresh activity**

Three days since the 10-07 scan broke an 11-day observation gap. Today's 10Z-slot dispatch completed first-attempt via GraphQL.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 62` (unchanged vs 10-07)
- Returned 60 concrete nodes (1 null slot — repo-visibility flicker, likely the Shopify IP-allow-list PR surfaced in stderr); 1 non-prefix drop (`theagentrouter/agent-router#2755`, branch `mcp-default-seed`, MERGED — unrelated manual PR)
- 58 prefix-match PRs retained (state split: 45 CLOSED / 11 MERGED / 2 OPEN)
- **Bucket tuple `(0, 2, 0, 0)`** — identical to 10-07; stale-only open set, zero fresh activity across all windows

### Bucket delta from 2026-10-07 scan

| Bucket | 10-07 | 10-10 | Δ |
|--------|-------|-------|---|
| merged7d | 0 | 0 | 0 (13th scan dry — mxc#1124 now 12d past merge, outside 7d window) |
| staleLetter | 2 | 2 | 0 (wigolo#216 + RuView#1409 unchanged) |
| closed7d | 0 | 0 | 0 |
| activeLetter | 0 | 0 | 0 |
| Open total | 2 | 2 | 0 |
| issueCount | 62 | 62 | 0 (no new filings in 3-day window — fresh-open drought now 27 days 09-13 → 10-10) |

### Signal notes

- **Bucket tuple frozen** — identical `(0, 2, 0, 0)` for 3 consecutive days (10-07 → 10-10). Fresh-open drought extends to 27 days; `external-feature` dispatch has produced zero new PRs since 2026-09-13. Prior drought record was 24 days as of 10-07. Escalation trigger per 10-07 follow-up: `external-feature` skill-health ticket if next silent slot confirms.
- **`issueCount` flat at 62** — the +1 that surfaced between 09-26 and 10-07 did not propagate; no new quick-closes/merges beyond the top-60 window this cycle. One PR filed somewhere between 09-26 and 10-07 remains unresolved from today's `updated-desc` top-60 view.
- **`updatedAt` on both open PRs is 2026-10-07T22:55Z** — identical timestamps, synthetic (likely a cross-repo sweep or branch-protection probe, not real comment/review activity). Confirms the `updatedAt`-is-unreliable observation from the SKILL — comment count on wigolo stuck at 10 (same as 10-07), RuView at 4 (same as 10-07); real activity is zero.
- **Both open PRs still stale** (same as 10-07):
  - `KnockOutEZ/wigolo#216` — 81d old, last review `COMMENTED` on 2026-07-20 (82d stale review); 10 comments
  - `ruvnet/RuView#1409` — 78d old, last review `APPROVED` on 2026-08-28 (43d stale approve), unmerged; 4 comments
- **Identity liveness confirmed** via non-empty `issueCount = 62` → SKILL §5 all-zero notify rule per [[pr-tracker-all-zero-notify-rule-false-quiets-on-identity-block]] does not fire; notify still triggers via stale=2.
- **Shopify PR invisible** — one null-slot node in GraphQL response; stderr surfaced `Shopify organization has an IP allow list enabled, and your IP address is not permitted to access this resource`. This is a GitHub-side auth boundary, not an aeon identity problem. The PR count (62 → 60 node + 1 null + 1 non-prefix drop) accounts for it.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 81d | 10 comments; last review COMMENTED 2026-07-20 (82d); STALE |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 78d | APPROVED 2026-08-28 unmerged (43d since approve); 4 comments; STALE |

## Recent Merges (last 30d) — 1

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 2026-09-28 |

*(agent-framework#8172, univ4-hooks#3/#4, atlas#228 rolled off 30d window between 10-07 and 10-10 — all merged 09-03…09-09.)*

## Closed No-Merge (last 30d) — 28

**09-25 close (now 15d past):**

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography to patch disclosed CVEs | 2026-09-25 18:49Z | 23d after open; single close (not bulk); actor still not fetched (owed since 09-22) |

**09-17 bulk-close cluster (now 23d past, 7 days from rolling off 30d window on 10-17):**

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
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-09-17 13:58Z | bulk-close cluster |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9) | 2026-09-17 13:58Z | bulk-close cluster |
| ProjectOpenSea/seaport | [#1415](https://github.com/ProjectOpenSea/seaport/pull/1415) | fix(SeaportRouter): terminate tally loop on partially-available batches | 2026-09-17 14:02Z | bulk-close cluster |
| vercel-labs/deepsec | [#161](https://github.com/vercel-labs/deepsec/pull/161) | fix(deps): bump tar to patch CVE-2026-73566 | 2026-09-17 14:02Z | bulk-close cluster |
| Netflix/dgs-framework | [#2346](https://github.com/Netflix/dgs-framework/pull/2346) | fix(deps): bump Spring Boot BOM to patch CVE-2026-41854 | 2026-09-17 14:03Z | bulk-close cluster |
| Osmantic/ODS | [#3675](https://github.com/Osmantic/ODS/pull/3675) | fix(deps): bump fastapi to patch transitive starlette advisories in ape | 2026-09-17 14:03Z | bulk-close cluster |
| pytorch/pytorch | [#195321](https://github.com/pytorch/pytorch/pull/195321) | fix(deps): bump lxml, onnx, pip, setuptools in CI requirements | 2026-09-17 14:03Z | bulk-close cluster |
| cursor/plugins | [#256](https://github.com/cursor/plugins/pull/256) | fix(deps): bump transitive axios/ip-address/form-data | 2026-09-17 14:03Z | bulk-close cluster |

**Pre-09-17 closes still within 30d window (4) — rolling off by 10-13:**

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| affaan-m/ECC | [#2926](https://github.com/affaan-m/ECC/pull/2926) | fix(deps): bump lru to 0.18.2 for RUSTSEC-2026-0253 | 2026-09-10 21:26Z | 9d after open; rolls off 10-10 (today, by cutoff hour) |
| jo-inc/camofox-browser | [#10561](https://github.com/jo-inc/camofox-browser/pull/10561) | fix(deps): bump transitive qs/fast-uri/hono/js-yaml | 2026-09-10 18:32Z | workflow-block class; rolls off 10-10 |
| IBM/ACE-RISCV | [#130](https://github.com/IBM/ACE-RISCV/pull/130) | fix(deps): bump keccak for RUSTSEC-2026-0012 | 2026-09-10 08:05Z | 4d; rolls off 10-10 |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, protobufjs-cli for 5 CVEs | 2026-09-10 01:46Z | 44d; silent-maintainer-close (reopened as #2812/#2813/#2814 → all in bulk-close); rolls off 10-10 |

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(0, 2, 0, 0)** — identical to 10-07 for 3-day frozen state
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07 `(0, 2, 0, 0)` → 10-10 `(0, 2, 0, 0)`

## Notes

- **3-day frozen bucket tuple** — first time we observe `(0, 2, 0, 0)` steady-state across consecutive-ish scans. Comment counts and review states on both open PRs unchanged since 10-07. Only the `updatedAt` timestamps bump (synthetic, both pin to 2026-10-07T22:55Z), reinforcing the `updatedAt`-unreliable finding — real activity signal needs `reviews.submittedAt` or per-comment timestamps.
- **27-day fresh-open drought** — `external-feature` has not produced a visible PR since 2026-09-13 (and `issueCount` has not advanced since 10-07, meaning not even quick-closed below-window opens). Escalation window reached by any reasonable threshold; next `external-feature` silent slot should trip skill-health.
- **13-scan merge-7d drought** — mxc#1124 (09-28) is 12d past, firmly outside 7d. No merge since 09-28. Next window-rollover event: a hypothetical new merge; otherwise bucket stays at 0.
- **4 closes rolling off 30d window today 10-10** — ECC#2926, camofox#10561, ACE-RISCV#130, Baileys#2732. Next scan (10-11) should show closed30d = 24.
- **Shopify IP-allow-list PR invisible** — single null-slot node in response; the `gh api graphql` command exits 1 while still producing a complete-enough stdout payload. Prior scans in log surface haven't noted this; new atomic candidate: `[[pr-tracker-shopify-ip-allowlist-null-slot]]` if this persists.

## Follow-ups

- **Fetch `.timeline.closedEvent.actor.login` for openai#4829 and the 09-17 14:30Z 14-PR batch** on next scan — thrice owed now (from 09-22, 09-26, 10-07). openai#4829 rolls off 10-25; 09-17 batch rolls off 10-17.
- **Identify the +1 issueCount PR** from 09-26 → 10-07 — still not visible in `updated-desc` top-60; expand page size (first: 100) on next scan OR query by `createdAt` sort.
- **Escalate `external-feature` silence** — now 27-day drought; file skill-health ticket on next silent slot confirmation.
- **SKILL patches (a)–(q) still 83d+ overdue** — items (p) + (q) revalidated across the 10-07 → 10-10 window; add new item (r) for the Shopify-IP-allowlist null-slot handling (log, don't crash on partial GraphQL success).
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set to end reliance on operator convention; also set `pr_tracker.author: aeonframework` so SKILL config resolution doesn't fall through to the auth token (`github-actions[bot]` under Actions, which matches zero PRs).

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 43 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
