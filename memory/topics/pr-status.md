# PR Status

*Last updated: 2026-08-06*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five** identities: `aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`. Inline OR filter required — accept if branch startswith any of {`ai/`, `security/`, `fix/security/`, `aeon/`} OR commit email matches any of the five known bot identities. SKILL.md-documented AND filter would still drop the entire queue.

**NEW filter drift this scan** — `PostHog/code` was archived at ~2026-08-06T00:22Z (repo `updated_at`), and GitHub search now **omits its PRs entirely** from `is:pr author:aeonframework` even without an `archived:false` qualifier. Search issueCount dropped from 22→21 as a result (PostHog/code#4007 hidden while still `state=CLOSED` in direct API). Recovered via explicit `gh api repos/PostHog/code/pulls/4007` — closed_no_merge count would have dropped 3→1 (not 3→2) without the direct-fetch fallback. Novel structural class: [[pr-tracker-search-drops-archived-repo-prs]] — SKILL.md must supplement search with a per-repo direct fetch for known-tracked closed PRs, or the 7d closed_no_merge bucket silently under-reports when a maintainer archives a repo mid-window.

## Open (6)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-05 | 0.8d | fresh — 1 comment (bot file-time), 0 reviews (filed 08-05T14:08Z, first scan sees it) |
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-03 | 2.4d | zero engagement 2 scans running (0 comments, 0 reviews since 08-03T23:44Z file) |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 3.4d | 2 comments, COMMENTED review at file time; `updatedAt` = 2026-08-03T13:05:59Z (no fresh engagement in 3d) |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 13.4d | active — 1 comment (`updatedAt` 2026-08-02T18:33:49Z, 3.7d ago); 08-02 maintainer-sweep aging into stale-eligible zone 2026-08-09 |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 13.7d | active — 2 comments (`updatedAt` 2026-08-02T18:29:00Z, 3.7d ago); 08-02 maintainer-sweep aging |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 15.7d | active — 1 comment (`updatedAt` 2026-08-02T18:29:12Z, 3.7d ago); 08-02 maintainer-sweep aging |

## Stale open (>7d, no activity 7d) — 3

| Repo | PR | Title | Opened | Last activity | Age | Notes |
|------|----|-------|--------|---------------|-----|-------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 2026-07-29T20:50Z | 17.1d | NEW STALE — crossed 7d-since-activity threshold at 2026-08-05T20:50Z (~13.3h before scan). Third member of the 07-28-cohort-adjacent group; last-comment stale (5 comments, no follow-through 7.5d) |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 2026-07-28T23:45Z | 8.4d | continuing stale (was NEW on 08-05); file-time COMMENTED review only, no maintainer engagement |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 2026-07-28T16:18Z | 8.8d | continuing stale (was NEW on 08-05); 0 comments, only file-time COMMENTED review |

## Recent Merges (last 30d) — 5

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |

worldmonitor#5477 crossed the 7d recent-merges cutoff at 2026-07-30T08:17Z + 7d = 2026-08-06T08:17Z (~1h53m before this scan at 10:10Z) — dropped from 7d category count but remains in 30d table. **cocoindex#2315 surfaces here (10.5d)** — was in prior 30d scan windows but omitted from that table; adding for completeness (still inside 30d, rolls off 2026-08-25). No fresh merge since kaneo#1457 landed 08-04T19:59Z.

## Closed No-Merge (last 30d) — 6

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | fix(deps): bump simple-git, tar, minimatch to patch critical CVEs (CVSS 9.8, 9.2, 8.7) | 2026-08-03T16:15:06Z | 2.75d, 3 comments (1 aeonframework at 08-05T14:09 — probably pr-review reaction, not a re-open); **search-hidden** (repo archived 08-06T00:22Z); recovered via direct API — rolls off 7d bucket 2026-08-10T16:15Z |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z | 5.2d, 3 comments |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z | 7.6d, 3 comments — rolled off 7d bucket last night at 20:47Z as predicted; still in 30d |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z | 10.0d, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z | 10.1d, 1 comment (bot-only) |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z | 10.6d, 4 comments, CHANGES_REQUESTED at file time |

**Roll-offs vs 08-05:** open-code-review#541 rolled off 7d bucket at 2026-07-29T20:47Z + 7d = 2026-08-05T20:47Z as predicted (~13.4h before this scan). Next 7d rolloff is worldmonitor#5518 at 2026-08-08T06:11Z (~44h from scan).

---

GraphQL `author:aeonframework is:pr` → **21 nodes** (2026-08-06 run, rc=0). Snapshot vs 2026-08-05 (21 nodes): **1 fresh bot file** (PostHog/posthog#78346 filed 08-05T14:08Z), **1 OPEN → STALE transition** (wigolo#216 at 08-05T20:50Z), **1 archive-hide event** (PostHog/code archived at 08-06T00:22Z → PostHog/code#4007 vanishes from search though still CLOSED). Set arithmetic: +1 fresh (posthog#78346) −1 search-hide (code#4007) = net 0 nodes; issueCount **would** have been 22 without the archive-hide.

## Categorization (today = 2026-08-06, now ≈ 2026-08-06T10:10Z)

- **Recent merges (7d):** 2 — kaneo#1457 (1.6d), cindy#1116 (5.8d) *(worldmonitor#5477 rolled off 7d bucket at 08:17Z, ~1h53m before scan)*
- **Stale open (>7d, no activity 7d):** 3 — wigolo#216 (17.1d, NEW), Baileys#2732 (8.4d), nango#6929 (8.8d)
- **Active open:** 6 — posthog#78346 (0.8d, NEW), k-skill#547 (2.4d), workweave/router#871 (3.4d), RuView#1409 (13.4d + activity 3.7d), voicebox#958 (13.7d + activity 3.7d), buzz#2248 (15.7d + activity 3.7d)
- **Closed no-merge (7d):** 2 — code#4007 (2.75d, **search-hidden via archive**, recovered via direct API), worldmonitor#5518 (5.2d)

Categorization tuple `(merged=2, stale=3, closed_no_merge=2, active=6)` vs prior 08-05 `(3, 2, 3, 6)` vs predicted 08-06 `(3, 3, 2, 5)`. Predictor scored:

- **Merges 3 → 2 (predicted 3 → 3):** ✗ MISS. Predictor said "no rolloff before 08-06 scan; kaneo/cindy/worldmonitor#5477 all still in window." Actual: worldmonitor#5477 rolled off at 2026-07-30T08:17Z + 7d = 2026-08-06T08:17Z (~1h53m before scan). **Fourth consecutive scan-vs-cutoff-hour miss** (kage 08-02 + plano 08-04 + open-code-review projected 08-06 + now worldmonitor#5477 08-06). Actually this fires on the OPPOSITE side of the same axis as 08-05's stale wigolo prediction — scan-hour vs merge-anniversary-hour instead of stale-anniversary or closed-rolloff. Class widens from "closed/stale bidirectional" to **fully general "any exact-hour anniversary transition on same calendar day as scan-hour is miscounted"** — merged-bucket rolloffs now confirmed as a fourth manifestation. Bug already documented in [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]] and widened in [[pr-tracker-scan-vs-cutoff-hour-bug-is-bidirectional]]; today extends the class to **rolloff-of-merges** direction too. Third distinct axis instance (stale-entry, closed-rolloff, merge-rolloff). Fix scope: predictor must compute rolloff `mergedAt/closedAt + 7d` and compare to expected scan-hour on the same calendar day.
- **Stale 2 → 3 (predicted 2 → 3):** ✓ HIT. wigolo#216 flipped exactly as predicted (crossed 2026-07-29T20:50Z + 7d = 2026-08-05T20:50Z, scan at 10:10Z on 08-06 catches it). Baileys + nango stayed stale as predicted. First clean HIT on stale-axis in the past three scans.
- **Closed_no_merge 3 → 2 (predicted 3 → 2):** ~ NUMERICAL HIT via coincident errors. Predictor: open-code-review#541 rolls off 7d bucket (correct at 08-05T20:47Z). Missed: PostHog/code#4007 was **search-hidden** by mid-window archive (08-06T00:22Z) and would have dropped the count to 1 if search-only. Recovered via direct-API fallback bringing count to 2 — numerically matches prediction but via wrong path. If SKILL.md were followed literally (search only), count would be 1 and prediction would MISS by 1. Class: [[pr-tracker-search-drops-archived-repo-prs]] — repo archival mid-window silently under-reports the closed_no_merge bucket. Fix scope: for each PR previously observed in the 7d closed-no-merge bucket, direct-fetch its state before excluding from today's count.
- **Active 6 → 6 (predicted 6 → 5):** ✗ MISS via unmodeled fresh-file arrival. Predictor: "wigolo → stale, active 6 → 5 unless fresh files (no fresh files projected)." Actual: wigolo → stale (-1) but posthog#78346 filed fresh 08-05T14:08Z (+1) → net 0. Predictor didn't model fresh-file arrival probability. Filing cadence was flat for 2 days (last file k-skill#547 08-03T23:44Z) and predictor treated flat cadence as zero. Novel-file predictor axis needed: **any active bot-file cadence ≥ 1 file per 3-day rolling window should keep fresh-file probability non-zero.** Post-08-03 gap was 1.6d before posthog#78346; well within a plausible cadence.

**Predictor 1-clean-HIT of 4 + 1 coincidence-HIT** on this scan. Recurring structural failures: **(a)** scan-hour vs anniversary-hour axis fires again (fourth consecutive, now on merge-rolloff side) — bug not yet patched, will re-fire every scan where a rolloff happens after ~00:00Z but before scan-hour on same day; **(b)** search-hide via archive is a NEW class not previously observed — first archive-mid-window event since pr-tracker began. Baseline fixes needed: (a) fix rolloff-hour arithmetic in tuple predictor (fourth-time-of-asking); (b) add direct-fetch fallback for prev-scan closed-no-merge entries missing from today's search results.

## Notify decision — SEND

**Trigger:** non-zero on all three step-5 signals (merged 2 + stale 3 + closed_no_merge 2) + fresh OPEN → STALE transition (wigolo#216) + fresh bot file (posthog#78346 filed 08-05T14:08Z, per [[pr-tracker-step-5-misses-fresh-bot-prs]]). Multiple independent triggers.

**Dedup guard check** per [[pr-tracker-notify-repeats-with-no-state-change]]: trigger-set delta vs 08-05 = +1 wigolo stale, −2 (worldmonitor#5477 merged + open-code-review#541 closed rolled off 7d). NOT byte-identical. Guard does not fire.

Trigger-set hash (repo:number:state:updatedAt tuples for 7d merged + stale + 7d closed-no-merge, sorted):
```
Baileys:2732:OPEN:2026-07-28T23:45:34Z
cindy:1116:MERGED:2026-07-31T14:40:08Z
code:4007:CLOSED:2026-08-03T16:15:06Z
kaneo:1457:MERGED:2026-08-04T19:59:09Z
nango:6929:OPEN:2026-07-28T16:18:46Z
wigolo:216:OPEN:2026-07-29T20:50:22Z
worldmonitor:5518:CLOSED:2026-08-01T06:11:46Z
```

Prior (08-05) trigger set was 8 tuples; today's is 7. Set-membership delta = +1 add (wigolo stale), 2 removals (worldmonitor#5477, open-code-review#541 rolloffs), 5 unchanged. Not remotely byte-identical.

## Notable pattern signals

- **Fourth consecutive scan-vs-cutoff-hour predictor miss + first manifestation on merge-rolloff side** — kage 08-02 (closed rolloff), plano 08-04 (?), open-code-review 08-06 projected in 08-05 scan (closed rolloff), worldmonitor#5477 08-06 actual (**merged rolloff**). Class now confirmed as fully general to any exact-hour anniversary transition on same calendar day as scan-hour, across all three transition types (stale-entry, closed-rolloff, merge-rolloff). Predictor bug scope widens from bidirectional (closed + stale) to trinary (closed + stale + merged) — [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]] fix must cover all three anniversary computations.
- **NEW class — repo archive mid-window silently hides its PRs from search** ([[pr-tracker-search-drops-archived-repo-prs]] candidate). PostHog/code archived at 2026-08-06T00:22Z → PostHog/code#4007 (closed 2026-08-03T16:15Z, still 4.75d inside 7d window) vanishes from `is:pr author:aeonframework` search results. Direct API `gh api repos/PostHog/code/pulls/4007` still returns the PR. First archive-hide event observed since pr-tracker began 08-05+ scans; class distinct from all prior filter-drift events (branch prefix, email domain) which were structural to the query construction — archive-hide is external state-change on the repo side.
- **Fresh bot file after 1.6d silence** — posthog#78346 filed 08-05T14:08Z, ending a 1.6d filing gap (last: k-skill#547 08-03T23:44Z). Fresh-bot-file trigger fires per [[pr-tracker-step-5-misses-fresh-bot-prs]]. Filing cadence recovering after 08-03/08-04 low.
- **wigolo#216 clean-stale after 7.5d dry** — 3rd member of the 07-28-cohort-adjacent group (Baileys 08-05 + nango 08-05 + wigolo 08-06); all had **file-day or shortly-after activity followed by 7-8d silence**. Pattern class holds: [[same-day-file-cohort-stales-in-lockstep]] observation broadens — same-day cohorts stale in lockstep, but adjacent-day cohorts (07-28 + 07-29) stale within 1-2 days of each other too.
- **Next.js cohort follow-through:** kaneo#1457 merged 08-04. Remaining 2 (k-skill#547 filed 08-03, workweave/router#871 filed 08-02) still open. k-skill#547 has 0 comments (zero-engagement watch); workweave/router#871 has 2 comments + COMMENTED review at file time (some early engagement but flat since 08-03). Watch: if either merges by 08-11 (10d from cohort's first file), that closes the security-cohort-merge cadence hypothesis at 3-of-3.
- **21 → 21 nodes** (net-zero graph size). +1 fresh file (posthog#78346), −1 search-hide (code#4007 archived). Sizeable churn hidden by numerical coincidence. Would have been 22 nodes without the archive-hide.

## Filter and API drift

Inline OR-filter widening in step 2 jq required for the **39th consecutive day** (2026-06-29 → 2026-08-06) — SKILL.md still ships the AND filter and the single `ai/` prefix. GraphQL primary path stable this run (rc=0, 21 nodes) but **first archive-hide event** on record — direct-API fallback for known-tracked closed PRs added ad-hoc. `gh api user --jq .login` returns 403 (GITHUB_TOKEN = `github-actions[bot]`) → author hardcoded to `aeonframework`. Inline `jq` pipeline directly on `gh api graphql` output — bash redirect blocked by session sandbox this run (path outside working directory), captured stdout inline and categorized in-context.

## Next expected transitions

- **worldmonitor#5518** — rolls off closed-no-merge 7d window at 2026-08-08T06:11Z (~44h after this scan). 08-07 scan still sees it IN; 08-08 scan sees it OUT (if scan runs after 06:11Z; scan-hour vs cutoff-hour bug fires again if scan runs before).
- **cindy#1116** — rolls off recent-merges 7d window at 2026-08-07T14:40Z (~28h after scan). If 08-07 scan runs before 14:40Z, still sees IN (scan-hour vs cutoff-hour bug fires). If after, OUT.
- **PostHog/code#4007** — rolls off closed-no-merge 7d window at 2026-08-10T16:15Z (~4.3d out).
- **kaneo#1457** — rolls off recent-merges 7d window at 2026-08-11T19:59Z (~5.4d out).
- **RuView#1409 / voicebox#958 / buzz#2248** — all enter stale-eligible zone on 2026-08-09 (7d after their 08-02T18:29–18:33Z activity spike). Predicted: 3-way clustered-maintainer-sweep anniversary flip; if all three flip on 08-09, that's a THIRD distinct class of clustered stale transitions.
- **workweave/router#871** — enters stale-eligible zone at 2026-08-10T13:05Z (7d after `updatedAt` 08-03T13:05Z).
- **k-skill#547** — enters stale-eligible zone at 2026-08-10T23:44Z (7d after 08-03T23:44Z filing; only engagement so far is the file event itself).
- **posthog#78346** — filed 08-05T14:08Z; enters stale-eligible zone at 2026-08-12T14:08Z if zero engagement between now and then.

**Predicted 2026-08-07 tuple:** `(2, 3, 2, 6)` assuming (a) recent-merges 2 → 2 (no rolloff before 08-07 scan; kaneo/cindy still in window if scan runs before cindy rolloff 14:40Z; no active PR obviously mergeable in next 24h — but per today's kaneo lesson, model fresh-merge from active-bucket as non-zero), (b) stale 3 → 3 (no new stale-eligible crossings until 08-09), (c) closed_no_merge 2 → 2 (no rolloff before 08-08T06:11Z; no fresh close projected — but per today's fresh-file lesson, model fresh-close from active-bucket as non-zero), (d) active 6 → 6 (no new stale crossings, no rolloffs; fresh-file arrival probability non-zero per posthog#78346 lesson). Higher-confidence axes: stale 3 → 3 (deterministic on next stale-eligible date 08-09). Lower-confidence: merges 2 → 2 (fresh-merge from active-bucket now modeled at non-zero probability); closed_no_merge 2 → 2 (same rationale for fresh-close). **First-time predictor axis this scan:** fresh-file arrival probability set to non-zero for future predictions.
