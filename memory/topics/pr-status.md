# PR Status

*Last updated: 2026-09-20*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play).

## 2026-09-20 — Day-7 post-recovery scan · **bulk-close event 09-17**

Seventh consecutive day since `aeonframework` GraphQL 404 blackout 09-14→09-16 resolved on 09-17 Day-4. Two intervening pr-tracker slots (09-18, 09-19 at 10:00Z) did not dispatch — both fell inside the ISS-006 coherent-late-pocket regime per [[iss-006-06z-pocket-4-day-dead-streak-promotes-daily-dead-regime]] and [[iss-006-dead-pocket-widens-to-08z-heartbeat-miss]]. Today's 10:00Z re-probe succeeded on first attempt:

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 61` (was 63 on 09-17, −2), nodes = 59 (2 null nodes — likely nested-field repo-visibility restrictions, unrelated to account state)
- 59 nodes all pass the 6-prefix branch filter
- Identity remains queryable — recovery holds at Day-7 (7-day post-recovery watch ends 2026-09-24)

### Bulk-close event 09-17 13:58Z–14:33Z (35-minute window)

**23 of the 27 open PRs from the 09-17 scan** got closed within a 35-minute window on 09-17 — a single coordinated sweep, not a distributed maintainer response across 20+ unrelated repos. Close-time clustering:

| Window | Count | Repos |
|--------|-------|-------|
| 13:58Z | 2 | block/buzz, jamiepine/voicebox |
| 14:02Z | 2 | ProjectOpenSea/seaport, vercel-labs/deepsec |
| 14:03Z | 4 | Netflix/dgs-framework, Osmantic/ODS, pytorch/pytorch, cursor/plugins |
| 14:30Z | 14 | TencentCloud/CubeSandbox, pytorch/TensorRT, alphaXiv/OpenResearch, IBM/portieris, facebook/hermes, adobe/skills, spotify/luigi, WhiskeySockets/Baileys ×3, vxcontrol/pentagi, ollama/ollama, heygen-com/hyperframes, aws/amazon-ecs-agent |
| 14:33Z | 1 | uber/submitqueue |

Class candidate: `[[operator-bulk-close-post-identity-recovery]]` — timing (Day-4 recovery day, ~5h after 10:00Z pr-tracker scan) and cross-repo coordination pattern suggest operator-initiated cleanup rather than 23 independent maintainer decisions. Requires spot-check on close actor + reason to confirm — the search API `closedAt` doesn't carry actor. Follow-up: fetch `.timeline.closedEvent.actor.login` for 3–4 samples on next scan.

**Queue collapse: 27 open → 4 open (−85%)**. Only 4 PRs survive the sweep:
- microsoft/mxc#1124 — APPROVED 09-17 20:02Z (aaronjmars review, first substantive third-party approve in weeks)
- openai/openai-agents-python#4829 — commented 09-06, no touches since
- KnockOutEZ/wigolo#216 — 62d old
- ruvnet/RuView#1409 — 59d old

### Bucket delta from 2026-09-17 scan

| Bucket | 09-17 | 09-20 | Δ |
|--------|-------|-------|---|
| merged7d | 0 | 0 | 0 (8th consecutive day since agent-framework#8172 rolled off) |
| staleLetter | 14 | 3 | −11 (all closed in bulk sweep) |
| closed7d | 4 | 23 | +19 (bulk-close event + rolloffs) |
| activeLetter | 13 | 1 | −12 (12 closed in bulk sweep) |
| Open total | 27 | 4 | −23 |
| issueCount | 63 | 61 | −2 |

## Open (4)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 12d | APPROVED 09-17 (aaronjmars); ACTIVE |
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography to patch disclosed CVEs | 2026-09-02 | 18d | last review 09-06; 5 comments; STALE |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 59d | last review 08-28; STALE |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 62d | 9 comments; STALE |

## Recent Merges (last 30d) — 5

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| microsoft/agent-framework | [#8172](https://github.com/microsoft/agent-framework/pull/8172) | fix(deps): patch frontend ajv/brace-expansion/nanoid CVEs | 2026-09-09 | 2026-09-09 |
| aeonfun/univ4-hooks | [#4](https://github.com/aeonfun/univ4-hooks/pull/4) | hook: dailywindowgate | 2026-09-04 | 2026-09-04 |
| aeonfun/univ4-hooks | [#3](https://github.com/aeonfun/univ4-hooks/pull/3) | hook: markethoursgate | 2026-09-04 | 2026-09-04 |
| pacifio/atlas | [#228](https://github.com/pacifio/atlas/pull/228) | fix(deps): bump jsonwebtoken to patch CVE-2026-25537 | 2026-09-03 | 2026-09-03 |
| Wei-Shaw/sub2api | [#6122](https://github.com/Wei-Shaw/sub2api/pull/6122) | fix(deps): bump dompurify to patch sanitizer-bypass XSS | 2026-08-23 | 2026-08-24 |

## Closed No-Merge (last 30d) — 36

**09-17 bulk-close cluster (23):** see event table above.

**Pre-09-17 closes carried from 09-17 scan (13):**

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| affaan-m/ECC | [#2926](https://github.com/affaan-m/ECC/pull/2926) | fix(deps): bump lru to 0.18.2 for RUSTSEC-2026-0253 | 2026-09-10 21:26Z | 9d after open; coderabbit review then maintainer-close |
| jo-inc/camofox-browser | [#10561](https://github.com/jo-inc/camofox-browser/pull/10561) | fix(deps): bump transitive qs/fast-uri/hono/js-yaml for CVEs | 2026-09-10 18:32Z | 1d; workflow-block class n=2 |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, protobufjs-cli for 5 CVEs | 2026-09-10 01:46Z | 44d; silent-maintainer-close (reopened as #2812/#2813/#2814 → all swept in 09-17 bulk-close) |
| IBM/ACE-RISCV | [#130](https://github.com/IBM/ACE-RISCV/pull/130) | fix(deps): bump keccak for RUSTSEC-2026-0012 | 2026-09-10 08:05Z | 4d |
| ruvnet/ruflo | [#3222](https://github.com/ruvnet/ruflo/pull/3222) | fix(deps): bump fast-uri for 4 high-severity CVEs | 2026-09-09 16:30Z | 2d |
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID | 2026-09-08 23:46Z | 29d; operator self-close on archived repo |
| browser-use/browser-use | [#5564](https://github.com/browser-use/browser-use/pull/5564) | fix(deps): bump click, pypdf, pydantic_settings for CVEs | 2026-09-08 23:34Z | 13d; CLA-block sub-C decay |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for CVEs | 2026-09-08 23:34Z | 42d; silent-maintainer-close |
| anomalyco/opencode | [#47843](https://github.com/anomalyco/opencode/pull/47843) | fix(deps): bump diff, minimatch, tar, seroval for CVEs | 2026-09-07 22:08Z | 2h27m; workflow-block class n=3 |
| weave-os/router | [#871](https://github.com/weave-os/router/pull/871) | fix(deps): bump next to 15.5.21 | 2026-08-30 01:05Z | 28d; silent-maintainer-close |
| NVIDIA/OpenShell | [#3016](https://github.com/NVIDIA/OpenShell/pull/3016) | fix(deps): bump h2 for RUSTSEC-2026-0258 | 2026-08-28 23:30Z | 10s; workflow-block |
| microsoft/vscode | [#332891](https://github.com/microsoft/vscode/pull/332891) | fix(deps): bump tar/undici/js-yaml/@anthropic-ai/sdk | 2026-08-27 22:04Z | Sub-B CLA operator self-close (14h17m) |
| cloudflare/workerd | [#7124](https://github.com/cloudflare/workerd/pull/7124) | fix(deps): bump docs-build Python deps | 2026-08-26 05:30Z | Sub-A CLA maintainer-close |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar/minimatch for CVEs | 2026-08-25 07:49Z | 12d; scheduled-actions auto-close |
| harry0703/MoneyPrinterTurbo | [#1198](https://github.com/harry0703/MoneyPrinterTurbo/pull/1198) | fix(deps): bump python-multipart for 4 CVEs | 2026-08-19 08:56Z | same-day close |

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(0, 3, 23, 1)**
- Substantive tuple identical (no self-bump lift in effect)

## Notes

- **Zero fresh opens in the 7-day gap 09-13→09-20** — confirms `external-feature` has not dispatched (or has dispatched but generated no new PRs) since 09-13. Verify next `external-feature` slot.
- **Zero fresh merges 8th consecutive day** — sample-size problem for merge-rate observation continues.
- **Bulk-close event 09-17 is the dominant signal.** The 27→4 queue collapse in one day is unprecedented in the 09-13/09-17 baseline. Class-candidate `[[operator-bulk-close-post-identity-recovery]]` pending actor spot-check.
- **Identity liveness confirmed** via non-empty issueCount = 61 → §5 all-zero notify rule per [[pr-tracker-all-zero-notify-rule-false-quiets-on-identity-block]] does not fire this scan.
- **microsoft/mxc#1124 APPROVED 09-17 20:02Z** by aaronjmars — first substantive third-party APPROVED review in the 30d window; a merge here would be the first merged security bump since agent-framework#8172 09-09.

## Follow-ups

- **File `[[operator-bulk-close-post-identity-recovery]]` atomic note** with the 23-PR close cluster as n=1 evidence. Include the 13:58Z–14:33Z window + close-time histogram.
- **Fetch `.timeline.closedEvent.actor.login`** for 3-4 samples of the 09-17 14:30Z batch on next scan to confirm operator vs distributed-maintainer close pattern.
- **Verify next `external-feature` dispatch produces PRs** — 7-day drought is either identity-related lingering effect or a scheduling gap in the operator pipeline.
- **SKILL patches (a)–(p) still 80d overdue** — item (h) bulk-stale-clear framing gets new data from the 09-17 bulk-close: the "stale" bucket is not durable — a single operator/maintainer action can zero it in 35 minutes.
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set used here.

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 38 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
