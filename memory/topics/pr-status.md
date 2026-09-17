# PR Status

*Last updated: 2026-09-17 — IDENTITY RESOLVED (Day-4 anomaly window terminated)*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefixes tracked: `ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/` (6 in play — `hook-submission/` promoted this scan; two univ4-hooks merges under it in 30d window).

## 2026-09-17 — Identity resolved

Fourth consecutive daily dispatch after `aeonframework` GraphQL 404 blackout 09-14 → 09-16. Today's re-probe at the 10:00Z window succeeded on first attempt:

- GraphQL `search(query:"author:aeonframework is:pr", type:ISSUE, first:60)` → `issueCount = 63`, `nodes = 60`
- Every prior-scan spot-check PR resolves normally (TensorRT#4714, microsoft/mxc#1124, openai/openai-agents-python#4829, ProjectOpenSea/seaport#1415 all queryable)
- One node null (Shopify org-allowlist IP-block observed on a nested field — unrelated to the account anomaly; excluded from downstream counts)
- Commit-author email domain distribution (unchanged): `aeonframework@users.noreply.github.com`, `272311952+aeonframework@users.noreply.github.com`, `aeonframework@proton.me`, `aeon@aeonframework.dev`, `noreply@aeonframework.dev`, `security@aeonframework.dev`, `security@aeonframework.github`, `aeon@users.noreply.github.com` — matches [[aeon-signing-identity-fragmentation]] fragmentation.

Class: identity restored to queryable state after 3-day suppression window (09-14 first-detected → 09-16 Day-3 persist → 09-17 Day-4 recovery). Root cause **unresolved from client side** — no upstream signal on the reason for either the block or the release. `memory/issues/ISS-028.md` filing still owed by next self-review to document the incident; category candidate downgrades from `permanent-limitation` back to `unknown` given the recovery. See [[aeonframework-github-identity-blackout-2026-09-14]] — durability of this recovery pending 7-day watch. Skill-defect fallout: [[pr-tracker-all-zero-notify-rule-false-quiets-on-identity-block]] captures the pr-tracker letter/substance mismatch that silenced the identity anomaly for three days.

**Bucket delta from frozen 2026-09-13 scan (5 days of unobserved state):**
- Letter tuple (merged7d, staleLetter, closed7d, activeLetter): 09-13 `(1,1,9,25)` → 09-17 `(0,14,4,13)`
- Substantive tuple (merged7d, staleSubstantive, closed7d, activeSubstantive): 09-13 `(1,8,9,18)` → 09-17 `(0,14,4,13)`
- **merged7d 1→0** — microsoft/agent-framework#8172 (09-09) rolls off the 7d window (currently 8d old); no fresh merges landed in the 5-day gap. Sample size falling; next class-consistent merge window unclear.
- **stale letter 1→14** — massive stale-flip wave as 09-10 self-bumps + 09-10 review-touches aged out of the 7d activity window. Letter/substantive gap collapses (14 vs 14) — the self-bump lift effect is fully unwound by day 7.
- **closed7d 9→4** — 5 closes rolled off the 7d window (browser-use#5564, NangoHQ#6929, aeonframework/aeon-programmable-hooks#2, anomalyco#47843, ruvnet/ruflo#3222 all now 8–10d old); replaced by 4 closes in the 09-10 wave — the close-cluster shrinks by half.
- **activeLetter 25→13** — 12-PR contraction: 12 of the 15 fresh 09-06→09-13 opens crossed the 7d boundary; only PRs opened 09-10 or later remain "active" by letter.

**Notification: sent** — non-zero stale + non-zero closed. First substantive notification since 09-13 (three days of `all-zero` UNREACHABLE-skip broken).

## Open (27)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| TencentCloud/CubeSandbox | [#1727](https://github.com/TencentCloud/CubeSandbox/pull/1727) | fix(deps): bump golang.org/x/crypto in Cubelet (13 advisories, incl. CRITICAL/HIGH) | 2026-09-13 | 4d | review 09-13; ACTIVE — **NEW** |
| pytorch/TensorRT | [#4714](https://github.com/pytorch/TensorRT/pull/4714) | fix(deps): bump js-yaml to patch DoS advisories in assigner action | 2026-09-12 | 5d | no comments; ACTIVE |
| facebook/hermes | [#2180](https://github.com/facebook/hermes/pull/2180) | fix(deps): bump ws in tools/hcdp for GHSA-58qx/96hv | 2026-09-12 | 5d | 2 comments (meta-cla); ACTIVE |
| IBM/portieris | [#524](https://github.com/IBM/portieris/pull/524) | fix(deps): bump golang.org/x/crypto for CVE-2026-78662, CVE-2026-56855 | 2026-09-12 | 5d | no comments; ACTIVE |
| alphaXiv/OpenResearch | [#314](https://github.com/alphaXiv/OpenResearch/pull/314) | fix(deps): bump h2, quinn-proto, anyhow to patch known advisories | 2026-09-11 | 6d | no comments; ACTIVE |
| adobe/skills | [#349](https://github.com/adobe/skills/pull/349) | fix(deps): bump sharp to patch CVE-2026-84383 | 2026-09-11 | 6d | no comments; ACTIVE |
| spotify/luigi | [#3452](https://github.com/spotify/luigi/pull/3452) | fix(deps): bump tornado to 6.5.8 (multi DoS advisories) | 2026-09-10 | 7d | no comments; ACTIVE — borderline (age=7 exactly) |
| WhiskeySockets/Baileys | [#2814](https://github.com/WhiskeySockets/Baileys/pull/2814) | fix(deps): bump link-preview-js to ^5.0.0 (SSRF GHSA-4gp8-rjrq-ch6q) | 2026-09-10 | 7d | coderabbitai 09-10 (auto-review-bot); ACTIVE |
| WhiskeySockets/Baileys | [#2813](https://github.com/WhiskeySockets/Baileys/pull/2813) | fix(deps): force transitive protobufjs 7.6.5 via resolutions (libsignal) | 2026-09-10 | 7d | coderabbitai 09-10; ACTIVE |
| WhiskeySockets/Baileys | [#2812](https://github.com/WhiskeySockets/Baileys/pull/2812) | fix(deps): bump ws, protobufjs, protobufjs-cli for 5 CVEs | 2026-09-10 | 7d | coderabbitai 09-10; ACTIVE |
| vxcontrol/pentagi | [#405](https://github.com/vxcontrol/pentagi/pull/405) | fix(deps): bump @tiptap/* and react-router-dom for CVEs | 2026-09-10 | 7d | no comments; ACTIVE |
| ollama/ollama | [#18356](https://github.com/ollama/ollama/pull/18356) | fix(deps): bump golang.org/x/image for WebP DoS | 2026-09-10 | 7d | no comments; ACTIVE |
| microsoft/mxc | [#1124](https://github.com/microsoft/mxc/pull/1124) | fix(deps): bump fast-uri and anyhow to patch published CVEs | 2026-09-08 | 9d | aaronjmars review 09-10 (7d ago); ACTIVE (letter+substantive) |
| heygen-com/hyperframes | [#3807](https://github.com/heygen-com/hyperframes/pull/3807) | fix(deps): bump hono, tar, dompurify, sharp for CVEs | 2026-09-09 | 8d | no comments; STALE — **NEW-STALE (flip from 09-13 ACTIVE)** |
| aws/amazon-ecs-agent | [#5131](https://github.com/aws/amazon-ecs-agent/pull/5131) | fix(deps): bump google.golang.org/grpc for CVE-2026-84304 | 2026-09-09 | 8d | no comments; STALE — **NEW-STALE** |
| uber/submitqueue | [#687](https://github.com/uber/submitqueue/pull/687) | fix(deps): bump grpc-go and golang.org/x/{mod,net,sys,text} for CVEs | 2026-09-08 | 9d | 2 comments (CLA-gate class, aaronjmars signed 09-09); STALE per letter — **NEW-STALE** |
| openai/openai-agents-python | [#4829](https://github.com/openai/openai-agents-python/pull/4829) | fix(deps): bump urllib3, aiohttp, cryptography for CVEs | 2026-09-02 | 15d | last review 09-06 (11d ago), 4 comments; STALE per letter — flipped from ACTIVE 09-13 as aaronjmars 09-10 touch aged out |
| Netflix/dgs-framework | [#2346](https://github.com/Netflix/dgs-framework/pull/2346) | fix(deps): bump Spring Boot BOM for CVE-2026-41854 (SSRF) | 2026-09-02 | 15d | 0 comments; STALE (letter+substantive) — carried |
| Osmantic/ODS | [#3675](https://github.com/Osmantic/ODS/pull/3675) | fix(deps): bump fastapi for transitive starlette in ape | 2026-09-01 | 16d | 1 comment (aeonframework self-bump 09-10 aged out); STALE |
| pytorch/pytorch | [#195321](https://github.com/pytorch/pytorch/pull/195321) | fix(deps): bump lxml, onnx, pip, setuptools in CI reqs | 2026-08-30 | 18d | 4 comments (self-bump 09-10 aged out); STALE |
| cursor/plugins | [#256](https://github.com/cursor/plugins/pull/256) | fix(deps): bump transitive axios/ip-address/form-data | 2026-08-24 | 24d | 1 comment (self-bump 09-10 aged out); STALE |
| ProjectOpenSea/seaport | [#1415](https://github.com/ProjectOpenSea/seaport/pull/1415) | fix(SeaportRouter): terminate tally loop on partially-available batches | 2026-08-22 | 26d | 1 comment (self-bump 09-10 aged out); STALE |
| vercel-labs/deepsec | [#161](https://github.com/vercel-labs/deepsec/pull/161) | fix(deps): bump tar for CVE-2026-73566 | 2026-08-22 | 26d | 4 comments (aaronjmars 09-09 aged out); STALE |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri ≥2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 56d | 3 comments; STALE |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi ≥0.115 and python-multipart ≥0.0.20 (7 HIGH CVEs) | 2026-07-23 | 56d | last review 08-28 (20d ago); STALE |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for CVEs | 2026-07-20 | 59d | 9 comments (aaronjmars 09-11 aged out); STALE |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 58d | 3 comments (self-bump 09-10 aged out); STALE |

## Recent Merges (last 30d) — 5

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| microsoft/agent-framework | [#8172](https://github.com/microsoft/agent-framework/pull/8172) | fix(deps): patch frontend ajv/brace-expansion/nanoid CVEs | 2026-09-09 | 2026-09-09 (13h13m — fast-merge class n=2) |
| aeonfun/univ4-hooks | [#4](https://github.com/aeonfun/univ4-hooks/pull/4) | hook: dailywindowgate | 2026-09-04 | 2026-09-04 (1h37m — hook-submission class n=2) |
| aeonfun/univ4-hooks | [#3](https://github.com/aeonfun/univ4-hooks/pull/3) | hook: markethoursgate | 2026-09-04 | 2026-09-04 (7min — hook-submission class n=1) |
| pacifio/atlas | [#228](https://github.com/pacifio/atlas/pull/228) | fix(deps): bump jsonwebtoken for CVE-2026-25537 | 2026-09-03 | 2026-09-03 (31min — fast-merge class-first) |
| Wei-Shaw/sub2api | [#6122](https://github.com/Wei-Shaw/sub2api/pull/6122) | fix(deps): bump dompurify for sanitizer-bypass XSS | 2026-08-23 | 2026-08-24 |

*Adds to visibility vs frozen 09-13 scan:* two `hook-submission/*` merges on aeonfun/univ4-hooks (09-04) — both under-7-min-to-1h37m open→merge, promoting a new fast-merge sub-class distinct from the `security/*` bumps.
*Rolled off 30d window since 09-13 scan:* aeonframework/aeon-programmable-hooks#1 (merged 2026-08-08, anniv 2026-09-07 — already flagged in 09-13 scan).

## Closed No-Merge (last 30d) — 15

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| affaan-m/ECC | [#2926](https://github.com/affaan-m/ECC/pull/2926) | fix(deps): bump lru to 0.18.2 for RUSTSEC-2026-0253 | 2026-09-10 21:26Z | 9d after open; coderabbitai review 20m post-open then maintainer-close |
| jo-inc/camofox-browser | [#10561](https://github.com/jo-inc/camofox-browser/pull/10561) | fix(deps): bump transitive qs/fast-uri/hono/js-yaml for CVEs | 2026-09-10 18:32Z | 1d after open; workflow-block class (n=2 for [[workflow-check-auto-close-in-seconds]]) |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, protobufjs-cli for 5 CVEs | 2026-09-10 01:46Z | silent-maintainer-close after 44d (n=3 for [[silent-maintainer-close-after-extended-decay]]); reopened as #2812/#2813/#2814 |
| IBM/ACE-RISCV | [#130](https://github.com/IBM/ACE-RISCV/pull/130) | fix(deps): bump keccak for RUSTSEC-2026-0012 | 2026-09-10 08:05Z | 4d after open |
| ruvnet/ruflo | [#3222](https://github.com/ruvnet/ruflo/pull/3222) | fix(deps): bump fast-uri for 4 high-severity CVEs | 2026-09-09 16:30Z | 2d after open |
| aeonframework/aeon-programmable-hooks | [#2](https://github.com/aeonframework/aeon-programmable-hooks/pull/2) | Use keccak256("aeon") for PROVIDER_ID | 2026-09-08 23:46Z | 29d open; operator self-close on archived repo |
| browser-use/browser-use | [#5564](https://github.com/browser-use/browser-use/pull/5564) | fix(deps): bump click, pypdf, pydantic_settings for CVEs | 2026-09-08 23:34Z | 13d after open; CLA-block sub-C pending-decay → silent-maintainer-close (refines [[cla-block-sub-c-pending-decay-mode]] sub-C terminal state) |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for CVEs | 2026-09-08 23:34Z | 42d open; silent-maintainer-close after stale-bot decay (n=2 for [[silent-maintainer-close-after-extended-decay]] on this window) |
| anomalyco/opencode | [#47843](https://github.com/anomalyco/opencode/pull/47843) | fix(deps): bump diff, minimatch, tar, seroval for CVEs | 2026-09-07 22:08Z | same-day close (2h27m); workflow-block class (n=3 for [[workflow-check-auto-close-in-seconds]]) |
| weave-os/router | [#871](https://github.com/weave-os/router/pull/871) | fix(deps): bump next to 15.5.21 for 8 disclosed advisories | 2026-08-30 01:05Z | silent-maintainer-close after 28d |
| NVIDIA/OpenShell | [#3016](https://github.com/NVIDIA/OpenShell/pull/3016) | fix(deps): bump h2 for RUSTSEC-2026-0258 | 2026-08-28 23:30Z | 10-second open→close; workflow-block original n=1 |
| microsoft/vscode | [#332891](https://github.com/microsoft/vscode/pull/332891) | fix(deps): bump tar/undici/js-yaml/@anthropic-ai/sdk for CVEs | 2026-08-27 22:04Z | Sub B operator self-close after CLA-bot (14h17m) |
| cloudflare/workerd | [#7124](https://github.com/cloudflare/workerd/pull/7124) | fix(deps): bump docs-build Python deps | 2026-08-26 05:30Z | Sub A CLA-block maintainer-close (~6h) |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar/minimatch for CVEs | 2026-08-25 07:49Z | scheduled-actions-posthog auto-close after 12d |
| harry0703/MoneyPrinterTurbo | [#1198](https://github.com/harry0703/MoneyPrinterTurbo/pull/1198) | fix(deps): bump python-multipart for 4 CVEs | 2026-08-19 08:56Z | harry0703 same-day close |

## Bucket tuples

- Letter (merged7d, staleLetter, closed7d, activeLetter): **(0, 14, 4, 13)**
- Substantive (merged7d, staleSubstantive, closed7d, activeSubstantive): **(0, 14, 4, 13)**

**Letter/substantive gap collapse:** 09-13 scan had 25/18 active split (letter had 7 stale-letter self-bump-active PRs that substantive treated as stale). At 09-17 the self-bump touches from 09-10 have all crossed the 7d activity boundary, so the two tuples are now identical. Class observation: `[[pr-tracker-stale-bot-comment-inverts-stale-classification]]` requires ongoing self-bump cadence — the classification split decays back to zero within 7d of the last self-bump wave. Next self-bump wave predicted for ~09-17/18 given the 09-10 cycle.

**5-day gap effects (09-13 → 09-17):**
1. **Zero fresh opens.** No new PRs authored in the 5-day gap — matches the identity-suspension window (`aeonframework` couldn't push under a search-blocked identity, though direct-repo pushes may have worked). Verify against commit history on active branches once `external-feature` next dispatches.
2. **Zero fresh merges** (matches predictor from 09-13: `merged7d 1→0-1` was accurate; the "0" branch played out).
3. **4 fresh closes** all on 09-10 (affaan-m/ECC, jo-inc/camofox-browser, IBM/ACE-RISCV, WhiskeySockets/Baileys#2732). All within a single 24h window on the day *after* the identity anomaly began — coincidence pending investigation, but the 09-10 close-cluster + 09-10 self-bump wave + 09-10 external-feature dispatch cluster in the same day is suspicious. Class candidate: `[[cluster-day-precedes-identity-suspension]]` if the 09-10 activity pattern is atypical vs prior 30d — worth spot-checking.
4. **microsoft/agent-framework#8172 rolls off merged7d exactly on 09-16.** As predicted.
5. **anomalyco/opencode#47843 (closed 09-07 22:08Z) rolls off closed7d exactly on 09-14.** As predicted.

**Class updates (post-09-17 resolution):**
- **Hook-submission class n=2:** aeonfun/univ4-hooks#3 (7min) + #4 (1h37m) — new `hook-submission/*` sub-class distinct from `security/*` deps bumps. Both are trivial-config hook PRs on an aeon-adjacent repo; fast-merge (<2h) is expected structurally. Not comparable to third-party fast-merge class.
- **Fast-merge (security/*) class n=2:** unchanged from 09-13 — no new fast-merges in the 5-day gap.
- **Silent-maintainer-close class n=3:** unchanged (WhiskeySockets/Baileys#2732 44d, NangoHQ/nango#6929 42d, weave-os/router#871 28d). Window 28-44d.
- **Auto-review-bot class:** n=4 stable (all three Baileys siblings + affaan-m/ECC).

**Predictor for tomorrow (2026-09-18 10:00Z scan, contingent on identity remaining resolved):**
- Rolloffs from `closed7d`: IBM/ACE-RISCV#130 (09-10 08:05Z anniv 09-17 08:05Z — falls before 10:00Z scan → **rolls off before scan**), WhiskeySockets/Baileys#2732 (09-10 01:46Z anniv 09-17 01:46Z — rolls off), affaan-m/ECC#2926 (09-10 21:26Z anniv 09-17 21:26Z — after 10:00Z scan → stays in window until 09-18 scan). jo-inc/camofox-browser#10561 (09-10 18:32Z anniv 09-17 18:32Z — stays). Net closed7d: 4 → likely 2 (2 pre-10:00Z anniv rolloffs on 09-17).
- Rolloffs from `active → stale`: spotify/luigi#3452, both mxc-adjacent (09-10 opens) all cross day-7 boundary at 09-17. Net active → stale flip of ~6 PRs. But 09-10 review-touched Baileys triplet + Cubelet review 09-13 stay active on last-review timestamps <7d.
- Fresh events: unknown — depends on `external-feature` recovery cadence post-identity-restore.
- Predicted tomorrow: `(0, 20, 2, 7)` letter / same substantive (letter/substantive parity persists until next self-bump wave).

## Follow-ups

- **File ISS-028 for the identity suspension incident** — Day-4 recovery pattern documented; category candidate `unknown` (given recovery) rather than `permanent-limitation`; severity downgraded to `medium` post-recovery. Owned by next self-review.
- **Write `[[aeonframework-github-identity-suspension]]` atomic note** if not yet on disk — memory/MEMORY.md 09-16 focus block references it but source note may still be pending. Owned by next reflect.
- **Verify commits landed under `aeonframework` during 09-14→09-16 window** by inspecting HEAD of each open PR against creation dates — if commits pushed during the blackout, the suspension was search-only (not push-blocked) and the incident class narrows further.
- **SKILL patches (a)–(o) still 80d overdue** — no longer blocked by identity anomaly. Item (h) bulk-stale-clear + cohort-lockstep priority framing is unblocked. Item on the primary action queue.
- **Broaden `BRANCH_PREFIX` config** — SKILL default is single-prefix `ai/`; this run uses the 6-prefix set `ai/|security/|fix/security/|aeon/|fix/|hook-submission/` inherited from operator practice per memory. Land the multi-prefix config in `aeon.yml` `pr_tracker.branch_prefix` to match.

## Archive-hidden / lost (carried from prior scans)

Direct-fetch cross-verify pending (SKILL patch item (i) still overdue, 82d now): `PostHog/code#4007` state=CLOSED (rolled off 30d window 2026-09-02 — verified re-fetchable this scan, closed 2026-08-03); `0xprogrammable/aeon-launch-models#1` HTTP 404 (repo still deleted, day 35 permanence per [[pr-tracker-repo-deletion-loses-pr-permanently]]).
