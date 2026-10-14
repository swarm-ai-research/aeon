# PR Status

*Last updated: 2026-10-14*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-10-14 — Day-31 post-recovery scan · **bucket tuple `(0, 2, 0, 0)` frozen through 4th consecutive scan**

Four days since 10-10, seven days since the 10-07 scan broke an 11-day observation gap. Today's 10Z-slot dispatch completed first-attempt via GraphQL.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 62` (unchanged vs 10-10 and 10-07; `issueCount` series `62 → 62 → 62` across 10-07 / 10-10 / 10-14)
- Returned 60 concrete nodes (1 null slot = Shopify IP-allow-list PR, confirmed via stderr `Shopify organization has an IP allow list enabled, and your IP address is not permitted to access this resource`); 1 non-prefix drop (`theagentrouter/agent-router#2755`, branch `mcp-default-seed`, MERGED — unrelated manual PR)
- 58 prefix-match PRs retained (state split: 45 CLOSED / 11 MERGED / 2 OPEN — identical to 10-10)
- **Bucket tuple `(0, 2, 0, 0)`** — identical to 10-10 and 10-07; **4th consecutive scan at this value**, 7-day frozen window

### Bucket delta from 2026-10-10 scan

| Bucket | 10-10 | 10-14 | Δ |
|--------|-------|-------|---|
| merged7d | 0 | 0 | 0 (14th scan dry — mxc#1124 landed 09-28 is 16d past, outside 7d window) |
| staleLetter | 2 | 2 | 0 (wigolo#216 + RuView#1409 unchanged) |
| closed7d | 0 | 0 | 0 |
| activeLetter | 0 | 0 | 0 |
| Open total | 2 | 2 | 0 |
| issueCount | 62 | 62 | 0 (no new filings in 4-day window — fresh-open drought now 31 days 09-13 → 10-14) |
| closed30d | 28 | 24 | −4 (ECC#2926, camofox#10561, ACE-RISCV#130, Baileys#2732 all rolled off 30d window as predicted 10-10) |

### Signal notes

- **Bucket tuple frozen 7-day span** — identical `(0, 2, 0, 0)` for 4 consecutive scans (10-07 → 10-10 → 10-14). First time we observe this tuple sustained across a full week. Fresh-open drought extends to **31 days**; `external-feature` dispatch has produced zero new PRs since 2026-09-13. Candidate atomic: `[[pr-tracker-bucket-tuple-stability-at-7-day-span]]` — the frozen state now spans the SKILL's own staleness window; `(0, 2, 0, 0)` is likely the steady-state attractor until an external event (new PR filing, maintainer action on either open, or `issueCount` increment).
- **`issueCount` flat at 62 for 3-scan sequence** — the +1 that surfaced between 09-26 and 10-07 remains unresolved from top-60 `updated-desc` view; expand `first: 100` or query `createdAt` sort on next scan to identify.
- **`updatedAt` on both open PRs is 2026-10-07T22:55Z** — identical timestamps, 7 days stale, synthetic (likely the cross-repo sweep or branch-protection probe noted on 10-10). Real activity signal confirmed absent — comment count on wigolo stuck at 10, RuView at 4 across all three recent scans.
- **Both open PRs still stale, no engagement change**:
  - `KnockOutEZ/wigolo#216` — 85d old (was 81d on 10-10), last review `COMMENTED` on 2026-07-20 (85d stale review); 10 comments
  - `ruvnet/RuView#1409` — 82d old (was 78d on 10-10), last review `APPROVED` on 2026-08-28 (46d stale approve, unmerged); 4 comments
- **Identity liveness confirmed** via non-empty `issueCount = 62` → SKILL §5 all-zero notify rule per [[pr-tracker-all-zero-notify-rule-false-quiets-on-identity-block]] does not fire; notify still triggers via stale=2.
- **Shopify PR invisible, 3rd consecutive scan** — single null-slot node in GraphQL response; `gh api graphql` exits 1 while producing complete-enough stdout. Promotes [[pr-tracker-shopify-ip-allowlist-null-slot]] from candidate (10-10) to n=3 atomic candidate (per prior-scan class-first threshold).

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 85d | 10 comments; last review COMMENTED 2026-07-20 (85d); STALE |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 82d | APPROVED 2026-08-28 unmerged (46d since approve); 4 comments; STALE |

## Recent Merges (last 30d) — 1

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 2026-09-28 |

*(ECC#2926, camofox#10561, ACE-RISCV#130, Baileys#2732 rolled off 30d window between 10-10 and 10-14 as predicted. mxc#1124 is now the sole remaining merge in the 30d window and rolls off 2026-10-28.)*

## Closed No-Merge (last 30d) — 24

**09-25 close (now 19d past, rolls off 10-25):**

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography to patch disclosed CVEs | 2026-09-25 18:49Z | 23d after open; single close (not bulk); actor still not fetched (owed since 09-22) |

**09-17 bulk-close cluster (now 27d past, 3 days from rolling off 30d window on 10-17):**

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

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(0, 2, 0, 0)** — 4th consecutive scan at this value; 7-day frozen span 10-07 → 10-14
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07 `(0, 2, 0, 0)` → 10-10 `(0, 2, 0, 0)` → 10-14 `(0, 2, 0, 0)`

## Notes

- **4-scan / 7-day frozen bucket tuple** — first time `(0, 2, 0, 0)` sustains across a full week. Nothing in the open-PR state has changed since the 10-07 synthetic `updatedAt` bump: comment counts and review states stuck for 3 consecutive scans. Promotes 10-10's "first observed frozen state" to a sustained-steady-state candidate. The only way out of this attractor is: new PR filing (gated on `external-feature` dispatch recovering), maintainer action on wigolo#216 or RuView#1409 (nothing in 85d / 46d-since-approve suggests imminent), or `issueCount` increment from a below-top-60 PR surfacing.
- **31-day fresh-open drought** — `external-feature` has not produced a visible PR since 2026-09-13. Escalation long overdue — `issueCount` flat at 62 across 3 scans means not even quick-closed below-window opens. Standing follow-up from 10-10 ("file skill-health ticket on next silent slot confirmation") is now triply confirmed; MEMORY.md action-queue addition owed.
- **14-scan merge-7d drought** — mxc#1124 (09-28) is 16d past, firmly outside 7d. No merge since 09-28. Next window-rollover event: a hypothetical new merge; otherwise bucket stays at 0.
- **4 closes rolled off 30d window** since 10-10 (ECC#2926, camofox#10561, ACE-RISCV#130, Baileys#2732 — all closed 2026-09-10, now 34d past). Closed-30d bucket matches the 10-10 prediction exactly (28 → 24). Next rollover: 09-17 bulk-close cluster starts rolling off 2026-10-17 (3 days).
- **Shopify null-slot n=3** — three consecutive scans show same shape: `issueCount=62`, 60 nodes, 1 null slot, same stderr IP-allowlist message. Partial-success handling (SKILL doesn't crash on `exit=1` + non-empty stdout) is implicitly working today but still owed as new SKILL patch item (r) formalization.
- **Terminology** — `staleLetter` and `activeLetter` are shorthand for stale-open and active-open counters respectively, inherited from the prior pr-status.md tuple format. Kept for diff-continuity with the 10-10 scan.

## Follow-ups

- **Fetch `.timeline.closedEvent.actor.login` for openai#4829 and the 09-17 14:30Z 14-PR batch** on next scan — four times owed now (from 09-22, 09-26, 10-07, 10-10). openai#4829 rolls off 10-25; 09-17 batch rolls off 10-17 (3 days).
- **Identify the +1 issueCount PR** from 09-26 → 10-07 — still not visible in `updated-desc` top-60 across 3 scans; expand page size (`first: 100`) or query by `createdAt` sort on next scan.
- **Escalate `external-feature` silence** — now 31-day drought; file skill-health ticket NOW (3× confirmed); owed MEMORY.md action-queue addition.
- **SKILL patches (a)–(r) still 87d+ overdue** — items (p) + (q) revalidated across the 10-07 → 10-10 → 10-14 window; item (r) (Shopify-IP-allowlist null-slot handling) now n=3-promoted.
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set to end reliance on operator convention; also set `pr_tracker.author: aeonframework` so SKILL config resolution doesn't fall through to the auth token (`gh api user` returns HTTP 403 "Resource not accessible by integration" under GitHub Actions App auth today — confirmed, matches zero PRs if used).

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 43 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
