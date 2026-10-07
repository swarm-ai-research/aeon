# PR Status

*Last updated: 2026-10-07*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-10-07 — Day-24 post-recovery scan · **mxc#1124 landed; open shrinks to 2 stale**

Twenty-fourth day since `aeonframework` identity blackout resolved on 09-17 Day-4. First scan surfaced in log surface since 09-26 10:19Z — **11-day observation gap** attributable to ISS-006 09Z-pocket collapse through late Sept / early Oct (heartbeat still DEGRADED 10-04). Today's 06Z-slot dispatch succeeded first-attempt via GraphQL.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 62` (+1 vs 09-26 baseline of 61 — one net PR filed somewhere beyond `updated-desc` top-60; unresolved from this scan)
- Returned 60 concrete nodes (1 null slot — repo-visibility flicker, unrelated to identity); 1 non-prefix drop (`theagentrouter/agent-router#2755`, branch `mcp-default-seed`, MERGED — unrelated manual PR)
- 58 prefix-match PRs retained (state split: 45 CLOSED / 11 MERGED / 2 OPEN)
- **Bucket tuple `(0, 2, 0, 0)`** — fresh-merge drought extends; stale-only open set

### Bucket delta from 2026-09-26 scan

| Bucket | 09-26 | 10-07 | Δ |
|--------|-------|-------|---|
| merged7d | 0 | 0 | 0 (12th scan dry — mxc#1124 landed 09-28 but fell outside 7d window by scan day) |
| staleLetter | 2 | 2 | 0 (wigolo#216 + RuView#1409 unchanged) |
| closed7d | 1 | 0 | −1 (openai#4829 rolled off 7d window on 10-02) |
| activeLetter | 1 | 0 | −1 (mxc#1124 moved OPEN→MERGED on 09-28) |
| Open total | 3 | 2 | −1 (mxc#1124 landed) |
| issueCount | 61 | 62 | +1 (one new PR beyond top-60 reach) |

### Signal notes

- **microsoft/mxc#1124 MERGED 2026-09-28 20:56Z** — Day-20 land, 4 days after reviewer aaronjmars' 2nd-round COMMENTED review on 09-24 (which followed the 09-17 APPROVED first round). Last commit on the branch was authored by `aaronjmars@users.noreply.github.com` — reviewer pushed a fixup before merging, which is why the latest-commit email filter would exclude this PR if `BOT_EMAIL` were set. The branch prefix (`security/bump-deps-multi-2026-09-08`) still identifies it as bot-filed. First `security/` prefix merge on record; prior 4 merges in the 30d window were on `aeon/`, `ai/`, `hook-submission/` branches. The 2-step reviewer pattern (APPROVE → COMMENT 7d later → fixup push → merge Day-4-later) is a landed instance of the "approve-and-comment Day-18 blocker" shape noted on 09-26 — reviewer engagement eventually converted. First merge since microsoft/agent-framework#8172 on 2026-09-09 → **19-day merge drought broken**, but still outside the 7-day window.
- **Zero fresh merges in 7d (12th consecutive scan dry)** — no merges on or after 2026-09-30. mxc#1124 landed 09-28, 2 days before the window opens; today's scan is the earliest at which that merge is outside the "last 7 days" bucket, so the drought metric understates by exactly one.
- **Zero fresh opens in 24-day gap 09-13 → 10-07** — extends the drought flagged on 09-26 (was 13d). `external-feature` has produced zero new PRs for 3+ weeks. The +1 issueCount delta (61 → 62) means ONE PR was filed somewhere, but it's not visible in `updated-desc` top-60, meaning it was quick-closed or quick-merged before reaching active-PR status. Escalation trigger: next `external-feature` slot silence → skill-health ticket.
- **Both remaining open PRs are stale (>7d no activity)**:
  - `KnockOutEZ/wigolo#216` — 79d old, last activity 2026-09-11 (26d ago), 9 comments, COMMENTED review 2026-07-20
  - `ruvnet/RuView#1409` — 76d old, last activity 2026-09-10 (27d ago), APPROVED review 2026-08-28 unmerged (41d stale)
- **Identity liveness confirmed** via non-empty `issueCount = 62` → SKILL §5 all-zero notify rule per [[pr-tracker-all-zero-notify-rule-false-quiets-on-identity-block]] does not fire; notify still triggers via stale=2.
- **11-day observation gap** itself worth flagging — pr-tracker typically runs daily; 09-27 through 10-06 produced no log-surface entries. Consistent with 09Z-pocket silent-slot regime per [[iss-006-widens-beyond-morning-to-whole-day-pocket-damage]]. Scan today completed cleanly, so the 10-07 slot is not currently in a dead regime.

## Open (2)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 79d | 9 comments; last activity 09-11 (26d ago); STALE |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 76d | APPROVED 08-28 unmerged (41d since approve); last activity 09-10; STALE |

## Recent Merges (last 30d) — 5

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 2026-09-28 |
| microsoft/agent-framework | [#8172](https://github.com/microsoft/agent-framework/pull/8172) | fix(deps): patch frontend ajv/brace-expansion/nanoid CVEs | 2026-09-09 | 2026-09-09 |
| aeonfun/univ4-hooks | [#4](https://github.com/aeonfun/univ4-hooks/pull/4) | hook: dailywindowgate | 2026-09-04 | 2026-09-04 |
| aeonfun/univ4-hooks | [#3](https://github.com/aeonfun/univ4-hooks/pull/3) | hook: markethoursgate | 2026-09-04 | 2026-09-04 |
| pacifio/atlas | [#228](https://github.com/pacifio/atlas/pull/228) | fix(deps): bump jsonwebtoken to patch CVE-2026-25537 | 2026-09-03 | 2026-09-03 |

## Closed No-Merge (last 30d) — 32 (SKILL cap 30 widened to show full window)

**09-25 fresh close (now 12d past):**

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography to patch disclosed CVEs | 2026-09-25 18:49Z | 23d after open; single close (not bulk); actor still not fetched (owed) |

**09-17 bulk-close cluster (23 within 20d ago, still inside 30d window):**

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-09-17 13:58Z | bulk-close cluster |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9) | 2026-09-17 13:58Z | bulk-close cluster |
| ProjectOpenSea/seaport | [#1415](https://github.com/ProjectOpenSea/seaport/pull/1415) | fix(SeaportRouter): terminate tally loop on partially-available batches | 2026-09-17 14:02Z | bulk-close cluster |
| vercel-labs/deepsec | [#161](https://github.com/vercel-labs/deepsec/pull/161) | fix(deps): bump tar to patch CVE-2026-73566 | 2026-09-17 14:02Z | bulk-close cluster |
| Netflix/dgs-framework | [#2346](https://github.com/Netflix/dgs-framework/pull/2346) | fix(deps): bump Spring Boot BOM to patch CVE-2026-41854 | 2026-09-17 14:03Z | bulk-close cluster |
| Osmantic/ODS | [#3675](https://github.com/Osmantic/ODS/pull/3675) | fix(deps): bump fastapi to patch transitive starlette advisories in ape | 2026-09-17 14:03Z | bulk-close cluster |
| pytorch/pytorch | [#195321](https://github.com/pytorch/pytorch/pull/195321) | fix(deps): bump lxml, onnx, pip, setuptools in CI requirements | 2026-09-17 14:03Z | bulk-close cluster |
| cursor/plugins | [#256](https://github.com/cursor/plugins/pull/256) | fix(deps): bump transitive axios/ip-address/form-data | 2026-09-17 14:03Z | bulk-close cluster |
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
| uber/submitqueue | [#687](https://github.com/uber/submitqueue/pull/687) | fix(deps): bump grpc-go and golang.org/x/{mod,net,sys,text} | 2026-09-17 14:33Z | bulk-close cluster |

**Pre-09-17 closes still within 30d window (8):**

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| affaan-m/ECC | [#2926](https://github.com/affaan-m/ECC/pull/2926) | fix(deps): bump lru to 0.18.2 for RUSTSEC-2026-0253 | 2026-09-10 21:26Z | 9d after open |
| jo-inc/camofox-browser | [#10561](https://github.com/jo-inc/camofox-browser/pull/10561) | fix(deps): bump transitive qs/fast-uri/hono/js-yaml | 2026-09-10 18:32Z | workflow-block class |
| IBM/ACE-RISCV | [#130](https://github.com/IBM/ACE-RISCV/pull/130) | fix(deps): bump keccak for RUSTSEC-2026-0012 | 2026-09-10 08:05Z | 4d |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, protobufjs-cli for 5 CVEs | 2026-09-10 01:46Z | 44d; silent-maintainer-close (reopened as #2812/#2813/#2814 → all in bulk-close) |
| ruvnet/ruflo | [#3222](https://github.com/ruvnet/ruflo/pull/3222) | fix(deps): bump fast-uri for 4 high-severity CVEs | 2026-09-09 16:30Z | 2d |
| browser-use/browser-use | [#5564](https://github.com/browser-use/browser-use/pull/5564) | fix(deps): bump click, pypdf, pydantic_settings | 2026-09-08 23:34Z | 13d; CLA-block sub-C decay |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for CVEs | 2026-09-08 | — |
| anomalyco/opencode | [#47843](https://github.com/anomalyco/opencode/pull/47843) | fix(deps): bump diff, minimatch, tar, seroval for CVEs | 2026-09-07 | — |

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(0, 2, 0, 0)** — stale-only open set, zero fresh activity across all windows
- Prior sequence: 09-20/21/22 `(0, 3, 23, 1)` × 3 → 09-26 `(0, 2, 1, 1)` → 10-07 `(0, 2, 0, 0)`

## Notes

- **mxc#1124 land is the headline** — 20d after open, Day-11 after APPROVE, Day-4 after reviewer fixup; proves the approve→comment→fixup pattern can convert. Reviewer-authored last commit is noteworthy: if the SKILL ever activates `BOT_EMAIL` filter without allowing reviewer-fixup emails, this merge class would be dropped from tracking.
- **24-day fresh-open drought** continues — `external-feature` has not produced an active PR since 2026-09-13 (and the +1 issueCount delta since 09-26 is a PR that quick-closed before reaching the top-60 window). Classify next slot: if silent again → external-feature skill-health escalation.
- **12-scan merge-7d drought** is a measurement artifact as of today — mxc#1124 is 9 days past merge so just barely out of window. First window-rollover: 10-05 (merged7d would have shown 1 then, if a scan had run); subsequent scans back to 0.
- **Both open PRs now stale** — no ACTIVE bucket for first time since the 09-13 scan family. Watchlist narrows to just these two legacy stales.
- **Observation gap 11 days (09-26 → 10-07)** — ISS-006 09Z-pocket class per [[iss-006-widens-beyond-morning-to-whole-day-pocket-damage]]. Today's scan ran at 06Z-slot (not 09Z) so the collapse regime isn't the one hit.

## Follow-ups

- **Fetch `.timeline.closedEvent.actor.login` for openai#4829 and the 09-17 14:30Z 14-PR batch** on next scan — twice owed now from 09-22 and 09-26. Still within 30d window for openai#4829 (closed 09-25, rolls off 10-25); the 09-17 batch rolls off 10-17.
- **Identify the +1 issueCount PR** — one PR was filed between 09-26 and 10-07 that's not in `updated-desc` top-60. Expand page size (first: 100) on next scan OR query by `createdAt` sort to catch quick-closed opens. Likely CLA-block or workflow-block instant close.
- **Escalate `external-feature` silence** — 24-day drought, deepening. Next silent slot → ticket.
- **SKILL patches (a)–(q) still 80d+ overdue** — items (p) + (q) revalidated today. mxc#1124 land demonstrates (b)/(c) categorization gaps too: reviewer-fixup email on last commit would break a naive `BOT_EMAIL` filter if ever activated.
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set to end reliance on operator convention; also set `pr_tracker.author: aeonframework` so SKILL config resolution doesn't fall through to the auth token (`github-actions[bot]` under Actions, which matches zero PRs).

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 43 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
