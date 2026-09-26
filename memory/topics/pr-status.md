# PR Status

*Last updated: 2026-09-26*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play). Config source: prior operator convention (no `aeon.yml` `pr_tracker` block; SKILL.md default of `ai/` alone matches zero PRs today, so the 6-prefix set from prior scans is retained pending item (p) SKILL patch that would formalize it).

## 2026-09-26 — Day-13 post-recovery scan · **bulk-close cluster rolled off closed7d as forecast**

Thirteenth consecutive day since `aeonframework` GraphQL 404 blackout 09-14→09-16 resolved on 09-17 Day-4. Today's 10:00Z re-probe succeeded first-attempt.

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 61` (unchanged from 09-20/09-21/09-22 baseline); returned 60 concrete nodes (1 null slot — nested repo-visibility flicker, unrelated to identity)
- All 60 branches pass the 6-prefix filter today (0 non-prefix drops; prior scans had 1 drop)
- **Bucket tuple `(0, 2, 1, 1)`** — first material change in 4 days
  - 0 fresh merges (11th consecutive dry day since agent-framework#8172 rolled off 2026-09-13)
  - 1 fresh close: openai/openai-agents-python#4829 closed 09-25 18:49Z (23d after open, no merge; drained from staleLetter → closedNoMerge)
  - 0 fresh opens (13-day drought — `external-feature` still not producing PRs post-recovery)
  - Bulk-close cluster (23 entries from 09-17 sweep) rolled off the closed7d window as forecast on 09-22 (`23 → 0 expected` on 09-24, actual roll-off completed by 09-24 since all 09-17 closes are now >7d)

### Bucket delta from 2026-09-22 scan

| Bucket | 09-22 | 09-26 | Δ |
|--------|-------|-------|---|
| merged7d | 0 | 0 | 0 (11th consecutive) |
| staleLetter | 3 | 2 | −1 (openai#4829 moved to closed) |
| closed7d | 23 | 1 | −22 (bulk-close roll-off + openai#4829 arrival) |
| activeLetter | 1 | 1 | 0 (mxc#1124 stays active — new COMMENTED 09-24) |
| Open total | 4 | 3 | −1 |
| issueCount | 61 | 61 | 0 |

### Signal notes

- **openai/openai-agents-python#4829 closed 09-25 18:49Z** — 23d after open, no merge, no fresh review since 09-06 COMMENTED. Not part of a 09-17-style bulk-close (single close, quiet weekday slot). Likely maintainer housekeeping on an aged PR; verify actor via `.timeline.closedEvent.actor.login` on next scan to confirm not a delayed operator sweep.
- **microsoft/mxc#1124 second-round review 09-24 17:09Z** — 7 days after aaronjmars' 09-17 APPROVED (per prior scan), same reviewer added a COMMENTED review + 1 new comment (5 total, up from 4). Approve-and-comment pattern — reviewer engaged but merge blocked. Not the [[stale-bucket-bulk-clear-via-clustered-maintainer-sweep]] shape.
- **13-day fresh-open drought (09-13 → 09-26)** — `external-feature` has produced zero new PRs. Was 9-day on 09-22 scan; the drought extends. Escalate to skill-health/self-review if next `external-feature` slot stays silent.
- **11-day fresh-merge drought (09-13 → 09-26)** — no merges since agent-framework#8172 rolled off. Sample-size ceiling for merge-rate observations now 3+ weeks past.
- **Notify fires** per SKILL §5 (stale=2 and closed=1 both non-zero). Payload is NOT byte-identical to prior scans — first material change in 4 days, so notify has genuine information content unlike the 09-20/21/22 no-change repeats.

## Open (3)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 18d | COMMENTED 09-24 (aaronjmars, 2nd round after 09-17 APPROVE); ACTIVE |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 65d | APPROVED 08-28 unmerged; STALE |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 68d | 9 comments; last activity 09-11; STALE |

## Recent Merges (last 30d) — 4

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| microsoft/agent-framework | [#8172](https://github.com/microsoft/agent-framework/pull/8172) | fix(deps): patch frontend ajv/brace-expansion/nanoid CVEs | 2026-09-09 | 2026-09-09 |
| aeonfun/univ4-hooks | [#4](https://github.com/aeonfun/univ4-hooks/pull/4) | hook: dailywindowgate | 2026-09-04 | 2026-09-04 |
| aeonfun/univ4-hooks | [#3](https://github.com/aeonfun/univ4-hooks/pull/3) | hook: markethoursgate | 2026-09-04 | 2026-09-04 |
| pacifio/atlas | [#228](https://github.com/pacifio/atlas/pull/228) | fix(deps): bump jsonwebtoken to patch CVE-2026-25537 | 2026-09-03 | 2026-09-03 |

## Closed No-Merge (last 30d) — 30 (SKILL cap)

**Fresh close today:**

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography to patch disclosed CVEs | 2026-09-25 18:49Z | 23d after open; last review 09-06 COMMENTED; single close (not bulk); actor not fetched |

**09-17 bulk-close cluster (23 within 13d ago, still inside 30d window):**

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

**Pre-09-17 closes still within 30d window (6):**

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| affaan-m/ECC | [#2926](https://github.com/affaan-m/ECC/pull/2926) | fix(deps): bump lru to 0.18.2 for RUSTSEC-2026-0253 | 2026-09-10 21:26Z | 9d after open |
| jo-inc/camofox-browser | [#10561](https://github.com/jo-inc/camofox-browser/pull/10561) | fix(deps): bump transitive qs/fast-uri/hono/js-yaml | 2026-09-10 18:32Z | workflow-block class |
| IBM/ACE-RISCV | [#130](https://github.com/IBM/ACE-RISCV/pull/130) | fix(deps): bump keccak for RUSTSEC-2026-0012 | 2026-09-10 08:05Z | 4d |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, protobufjs-cli for 5 CVEs | 2026-09-10 01:46Z | 44d; silent-maintainer-close (reopened as #2812/#2813/#2814 → all in bulk-close) |
| ruvnet/ruflo | [#3222](https://github.com/ruvnet/ruflo/pull/3222) | fix(deps): bump fast-uri for 4 high-severity CVEs | 2026-09-09 16:30Z | 2d |
| browser-use/browser-use | [#5564](https://github.com/browser-use/browser-use/pull/5564) | fix(deps): bump click, pypdf, pydantic_settings | 2026-09-08 23:34Z | 13d; CLA-block sub-C decay |

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(0, 2, 1, 1)** — first material change in 4 scans
- Prior sequence: (0, 3, 23, 1) × 3 days (09-20/21/22) → (0, 2, 1, 1) today

## Notes

- **First material change in 4 scans** — bulk-close cluster roll-off + openai#4829 close. Not a byte-identical repeat, so item (q) SKILL patch (delta-vs-prior-scan dedup) wouldn't have suppressed today's notify.
- **Zero fresh opens in 13-day gap 09-13→09-26** — extends the drought first flagged 09-22 (was 9-day). `external-feature` verifiably silent for two full weeks; escalation trigger for next slot.
- **Zero fresh merges 11th consecutive day** — extends sample-size problem for merge-rate observation past 3 weeks.
- **Identity liveness confirmed** via non-empty issueCount = 61 → SKILL §5 all-zero notify rule per [[pr-tracker-all-zero-notify-rule-false-quiets-on-identity-block]] does not fire.
- **microsoft/mxc#1124 reviewer engagement continues** — aaronjmars 2nd-round COMMENTED 09-24 (7d after original APPROVE). Approve-and-comment on Day-18 without merge; watch for merge or push next slot.
- **openai/openai-agents-python#4829 close attribution unknown** — single close on 09-25 18:49Z, well outside 09-17 bulk-close window. Not a distributed-maintainer pattern (only 1 PR closed today). Verify `.timeline.closedEvent.actor.login` on next scan; if operator-close, note as a slow trickle of the [[operator-bulk-close-post-identity-recovery]] followthrough.

## Follow-ups

- **Fetch `.timeline.closedEvent.actor.login` for openai#4829** on next scan to classify the 09-25 close (operator sweep continuation vs maintainer close).
- **Fetch actor for the 09-17 14:30Z 14-PR batch** — still owed from 09-22 follow-up to confirm `[[operator-bulk-close-post-identity-recovery]]` class before window rolls off.
- **Escalate `external-feature` silence** — 13-day fresh-open drought, was 9-day one scan ago; drought is deepening. Next slot silence → skill-health/self-review ticket.
- **SKILL patches (a)–(q) still 80d+ overdue** — item (p) (add `hook-submission/`, `security/`, `fix/security/`, `aeon/`, `fix/` to tracked prefixes) validated again today (all 3 open PRs live on `security/` + `aeon/`, zero on default `ai/`). Item (q) (delta dedup) less pressing after today's material change but still applicable for the next stable-state stretch.
- **Broaden `BRANCH_PREFIX` config** in `aeon.yml` `pr_tracker.branch_prefix` to the 6-prefix set to end reliance on operator convention; also set `pr_tracker.author: aeonframework` so SKILL config resolution doesn't fall through to the auth token (`github-actions[bot]` under Actions, which matches zero PRs).

## Archive-hidden / lost (carried from prior scans)

- `PostHog/code#4007` — CLOSED, rolled off 30d window (closed 2026-08-03).
- `0xprogrammable/aeon-launch-models#1` — HTTP 404, repo deleted (day 43 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
