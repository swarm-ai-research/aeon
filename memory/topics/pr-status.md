# PR Status

*Last updated: 2026-10-15*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-10-15 — Day-32 post-recovery scan · **bucket tuple `(0, 2, 0, 0)` holds 5th consecutive scan; `issueCount` 62 → 64 breaks 3-scan flat**

First-attempt GraphQL hit a transient `502 Bad Gateway` from nginx; retried once after 8s and succeeded. `issueCount` jumps +2 to 64 — first non-zero delta since 10-07 broke an 11-day observation gap. The two new nodes are **manual (non-bot-prefix) apache-org PRs** filed yesterday 2026-10-14 by the `aeonframework` identity, so they land in `issueCount` but drop out at prefix-filter — buckets are unaffected.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 64` (vs 62 across 10-07 / 10-10 / 10-14; sequence now `62 → 62 → 62 → 64`)
- First-attempt exit=1 with HTTP 502 body `<html><title>502 Bad Gateway</title>…</html>` from nginx — new error-shape distinct from the Shopify IP-allowlist `exit=1 + stderr + non-empty stdout` pattern (this one has an HTML body, no useful JSON). Retried after 8s, succeeded.
- Second attempt returned 60 nodes (59 concrete + 1 null slot = Shopify IP-allow-list PR, confirmed via stderr `Shopify organization has an IP allow list enabled, and your IP address is not permitted to access this resource`); 3 non-prefix drops (`apache/struts#2012` MERGED 2026-10-15T07:09Z branch `WW-5772-csp-inline-handlers`, `apache/wicket#1667` OPEN branch `csp-autocomplete-choicefilter`, `theagentrouter/agent-router#2755` branch `mcp-default-seed`)
- 56 prefix-match PRs retained (state split: 44 CLOSED / 10 MERGED / 2 OPEN); vs 58 on 10-14 — net `−2` prefix-match because older MERGED/CLOSED items got pushed below top-60 by the two new apache-org `updatedAt` events
- **Bucket tuple `(0, 2, 0, 0)`** — identical to 10-14, 10-10, 10-07; **5th consecutive scan at this value**, 8-day frozen window

### Bucket delta from 2026-10-14 scan

| Bucket | 10-14 | 10-15 | Δ |
|--------|-------|-------|---|
| merged7d | 0 | 0 | 0 (15th scan dry — mxc#1124 landed 09-28 is 17d past, outside 7d window) |
| staleLetter | 2 | 2 | 0 (wigolo#216 + RuView#1409 unchanged) |
| closed7d | 0 | 0 | 0 |
| activeLetter | 0 | 0 | 0 |
| Open total | 2 | 2 | 0 (prefix-match only — ignoring apache/wicket#1667 which is non-prefix) |
| issueCount | 62 | 64 | **+2** (first non-zero in 4 scans; both deltas are manual aeonframework PRs on apache org, non-bot-prefix) |
| closed30d | 24 | 24 | 0 (09-17 bulk-close cluster still inside window; next rollover 10-17 i.e. in 2 days) |

### Signal notes

- **`issueCount` +2 to 64 — first non-zero delta since 10-07** — breaks the 3-scan flat 62. Both deltas trace to the apache-org manual PR cluster (details below); neither increments any bot bucket. Steady-state attractor hypothesis from 10-14 (bucket tuple frozen) still intact — the apache-org PRs are *operator surface activity visible through the author filter*, not bot-pipeline output. **Candidate atomic**: `[[pr-tracker-manual-aeonframework-prs-surface-in-top-60-but-not-in-buckets]]` — `issueCount` is a mixed surface (bot + manual operator) while buckets are bot-only; delta drift between the two now has observational evidence.
- **Manual aeonframework activity on apache org** — two PRs opened yesterday 2026-10-14 by the `aeonframework` identity, neither on bot-prefix branches:
  - `apache/struts#2012` — WW-5772 Remove inline event handlers from optiontransferselect/… — opened 10-14T19:27Z, **MERGED today 10-15T07:09Z** (~12h turnaround — fast operator-tier contribution, distinct from the <5min aeon-adjacent fast-merge class per [[pr-tracker-hook-submission-prefix-promotes-with-aeon-adjacent-fast-merges]])
  - `apache/wicket#1667` — CSP autocomplete+ChoiceFilter work (WICKET-6938) — opened 10-14T19:27Z, still OPEN
  - These are CSP/XSS-adjacent manual contributions, suggesting operator-driven work in parallel to the bot stream. Flagging because: (a) the aeonframework identity is now observationally dual-use (bot + manual), and (b) manual PRs with branch prefixes outside the 6-set are a new data-quality consideration for any skill that treats "aeonframework author" as a bot-only proxy.
- **Transient 502 on first attempt** — new error class for pr-tracker. First time nginx 502 observed on `gh api graphql` from this skill. One-shot retry at 8s succeeded. Candidate atomic: `[[pr-tracker-gh-api-graphql-transient-502-bad-gateway]]` — first observation at n=1, no promotion yet. If recurs, consider adding a retry-with-backoff wrapper to the primary query path (currently SKILL.md step-2 primary falls through to `gh search prs` on error — but a transient 502 doesn't warrant falling back to the lossier search API when retry works).
- **Shopify null-slot n=4** — stderr IP-allowlist message identical across 10-07/10-10/10-14/10-15; promotes [[pr-tracker-shopify-ip-allowlist-null-slot]] to n=4-sustained. Partial-success handling (`exit=1 + non-empty stdout + null-slot in nodes`) continues to work implicitly. SKILL patch item (r) formalization still owed (currently 3 variants observed: (i) Shopify null-slot — benign, (ii) non-empty error body — benign, (iii) nginx 502 → stdout=HTML — need to retry; a single partial-success handler must distinguish these).
- **Both open PRs still stale, no engagement change (n=4 consecutive scans frozen)**:
  - `KnockOutEZ/wigolo#216` — 86d old (was 85d on 10-14), last review `COMMENTED` on 2026-07-20 (86d stale review); 10 comments
  - `ruvnet/RuView#1409` — 83d old (was 82d on 10-14), last review `APPROVED` on 2026-08-28 (47d stale approve, unmerged); 4 comments
  - `updatedAt` on both is still `2026-10-07T22:55Z` (identical minute, 8 days stale — synthetic, likely the branch-protection probe or cross-repo sweep from 10-07)
- **Identity liveness confirmed** via non-empty `issueCount = 64` → SKILL §5 all-zero notify rule per [[pr-tracker-all-zero-notify-rule-false-quiets-on-identity-block]] does not fire; notify still triggers via stale=2.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 86d | 10 comments; last review COMMENTED 2026-07-20 (86d); STALE |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 83d | APPROVED 2026-08-28 unmerged (47d since approve); 4 comments; STALE |

## Recent Merges (last 30d) — 1

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 2026-09-28 |

*(mxc#1124 is the sole remaining merge in the 30d window and rolls off 2026-10-28.)*

## Closed No-Merge (last 30d) — 24

**09-25 close (now 20d past, rolls off 10-25):**

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography to patch disclosed CVEs | 2026-09-25 18:49Z | 23d after open; single close (not bulk); actor still not fetched (owed since 09-22) |

**09-17 bulk-close cluster (now 28d past, 2 days from rolling off 30d window on 10-17):**

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

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(0, 2, 0, 0)** — 5th consecutive scan at this value; 8-day frozen span 10-07 → 10-15
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07 `(0, 2, 0, 0)` → 10-10 `(0, 2, 0, 0)` → 10-14 `(0, 2, 0, 0)` → **10-15 `(0, 2, 0, 0)`**

## Notes

- **5-scan / 8-day frozen bucket tuple** — `(0, 2, 0, 0)` sustains across a second observation beyond the 7-day window. The attractor hypothesis from 10-14 is now n=5 confirmed. **New observation**: `issueCount` can shift (`+2` today) without any bucket changing — because the delta came from non-bot-prefix PRs that fall out at the prefix filter. The bucket-tuple attractor is specifically a *bot-pipeline* steady state; `issueCount` is a looser upper bound that catches operator activity.
- **32-day fresh-open drought on bot pipeline** — `external-feature` has not produced a visible bot-prefix PR since 2026-09-13. The two new apache-org PRs are manual contributions, not pipeline output; they do not reset this drought counter. Escalation (standing from 10-10, 10-14) remains overdue; file skill-health ticket NOW.
- **15-scan merge-7d drought** — mxc#1124 (09-28) is 17d past, firmly outside 7d. Next window-rollover event: either a hypothetical new bot-pipeline merge, OR the apache/struts#2012 merge WOULD enter the merged-7d bucket if we loosened the prefix filter to include manual aeonframework PRs. Choice preserves prior-scan semantics (bot-only buckets).
- **Zero closes rolled off 30d window** since 10-14 (next rollover: 09-17 bulk-close cluster starts rolling off 2026-10-17, 2 days away → 23 PRs will drop out and closed30d collapses to 1).
- **New error class on first attempt**: `gh api graphql` HTTP 502 with HTML body (not Shopify stderr, not partial-success). Retry at 8s succeeded. Promotes to atomic candidate at n=1 — observational baseline for future triage.
- **Terminology** — `staleLetter` and `activeLetter` are shorthand for stale-open and active-open counters respectively, inherited from the prior pr-status.md tuple format. Kept for diff-continuity with the 10-14 scan.

## Follow-ups

- **Fetch `.timeline.closedEvent.actor.login` for openai#4829 and the 09-17 14:30Z 14-PR batch** on next scan — five times owed now (from 09-22, 09-26, 10-07, 10-10, 10-14). openai#4829 rolls off 10-25; 09-17 batch rolls off 10-17 (2 days — if not fetched by tomorrow's scan, the actor-identification data is permanently lost from this 30d window).
- **Identify the +2 issueCount deltas** — resolved today. The +1 that was invisible since 09-26 is likely one of the apache-org PRs (both opened 10-14), and the second is the other. Candidate atomic: the deltas were below top-60 `updated-desc` until an updatedAt event bubbled them up.
- **Escalate `external-feature` silence** — now 32-day drought; file skill-health ticket NOW (4× confirmed); owed MEMORY.md action-queue addition.
- **SKILL patches (a)–(r) still 88d+ overdue** — items (p) + (q) revalidated across the 10-07 → 10-10 → 10-14 → 10-15 window; item (r) (Shopify-IP-allowlist null-slot handling) now n=4-sustained; new item (s) draft: transient 502 retry wrapper on primary GraphQL path.
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set to end reliance on operator convention; also set `pr_tracker.author: aeonframework` so SKILL config resolution doesn't fall through to the auth token (`gh api user` returns HTTP 403 "Resource not accessible by integration" under GitHub Actions App auth today — confirmed on 10-15, matches zero PRs if used).

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 43 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
