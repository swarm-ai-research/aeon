# PR Status

*Last updated: 2026-08-07*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five known identities** (`aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`) **plus one variant** first observed 2026-08-07: numeric-prefix noreply `272311952+aeonframework@users.noreply.github.com` (functionally the same GitHub account as the bare-noreply form — GitHub uses the numeric-prefix format when the user has kept the email private, so this is a formatting variant, not a sixth signing identity). Inline OR filter still required — accept if branch startswith any of {`ai/`, `security/`, `fix/security/`, `aeon/`} OR commit email matches any of the six observed identity strings. SKILL.md-documented AND filter would still drop the entire queue.

**Archive-hide persists (day 2)** — `PostHog/code` archived 2026-08-06T00:22Z; `is:pr author:aeonframework` search STILL omits `PostHog/code#4007` today (search issueCount = 22, direct-fetch would push effective total to 23). SKILL.md must supplement search with a per-repo direct fetch for known-tracked closed PRs, or the 7d closed_no_merge bucket silently under-reports when a maintainer archives a repo mid-window. Class [[pr-tracker-search-drops-archived-repo-prs]] confirmed as **persistent** (not one-scan artifact) on second consecutive observation — search-index update on archive is either eventually-consistent with lag >34h, or permanent until repo un-archives.

## Open (7)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| 0xprogrammable/aeon-launch-models | [#1](https://github.com/0xprogrammable/aeon-launch-models/pull/1) | AEON models (draft, source review): NoOp, CapGate, DynamicFee | 2026-08-06 | 0.5d | NEW — fresh bot file (branch `aeon/models-draft`, ~12h old at scan); 0 comments, 0 reviews; first-ever bot PR filed against `0xprogrammable/*` |
| PostHog/posthog | [#78346](https://github.com/PostHog/posthog/pull/78346) | fix(deps): bump desktop agent tar to 7.5.22 and minimatch to 10.2.5 (CVE fixes) | 2026-08-05 | 2.0d | 1 comment (bot file-time), 0 reviews; no fresh engagement since file |
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-03 | 3.4d | zero engagement 3 scans running (0 comments, 0 reviews since 08-03T23:44Z file) |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 4.4d | 2 comments, COMMENTED review at file time; `updatedAt` = 2026-08-03T13:05:59Z (no fresh engagement in 4d) |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 14.4d | active — 1 comment (`updatedAt` 2026-08-02T18:33:49Z, 4.7d ago); 08-02 maintainer-sweep aging into stale-eligible zone 2026-08-09 (~2d) |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 14.7d | active — 2 comments (`updatedAt` 2026-08-02T18:29:00Z, 4.7d ago); 08-02 maintainer-sweep aging |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 16.7d | active — 1 comment (`updatedAt` 2026-08-02T18:29:12Z, 4.7d ago); 08-02 maintainer-sweep aging |

## Stale open (>7d, no activity 7d) — 3

| Repo | PR | Title | Opened | Last activity | Age | Notes |
|------|----|-------|--------|---------------|-----|-------|
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 2026-07-29T20:50Z | 18.1d | continuing stale (was NEW on 08-06); 5 comments, no follow-through 8.5d |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 2026-07-28T23:45Z | 9.4d | continuing stale (was stale on 08-06); file-time COMMENTED review only, no maintainer engagement |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 2026-07-28T16:18Z | 9.8d | continuing stale (was stale on 08-06); 0 comments, only file-time COMMENTED review |

## Recent Merges (last 30d) — 5

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |

cindy#1116 still IN 7d bucket at scan (rolls off 2026-08-07T14:39Z, ~4h29m after this scan). Predictor called this cleanly — first time scan-vs-cutoff-hour arithmetic was applied correctly since [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]] filed. kaneo#1457 rolls off 2026-08-11T19:59Z; cindy #1116 rolls off later today.

## Closed No-Merge (last 30d) — 6

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | fix(deps): bump simple-git, tar, minimatch to patch critical CVEs (CVSS 9.8, 9.2, 8.7) | 2026-08-03T16:15:06Z | 3.75d, 3 comments; **search-hidden day 2** (repo `archived: true` still — direct API `gh api repos/PostHog/code/pulls/4007` recovers); rolls off 7d bucket 2026-08-10T16:15Z |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z | 6.2d, 3 comments; rolls off 7d bucket 2026-08-08T06:11Z (~20h after this scan) |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z | 8.6d, 3 comments — rolled off 7d bucket 08-05T20:47Z; still in 30d |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z | 11.0d, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z | 11.1d, 1 comment (bot-only) |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z | 11.6d, 4 comments, CHANGES_REQUESTED at file time |

**Roll-offs vs 08-06:** none this scan (open-code-review#541 already rolled off 08-05, worldmonitor#5477 already rolled off 08-06). Next 7d rolloff is worldmonitor#5518 at 2026-08-08T06:11Z (~20h from scan).

---

GraphQL `author:aeonframework is:pr` → **22 nodes** (2026-08-07 run, rc=0). Snapshot vs 2026-08-06 (21 nodes): **+1 fresh bot file** (`0xprogrammable/aeon-launch-models#1` filed 2026-08-06T22:21:30Z, first bot PR against that repo). `PostHog/code#4007` STILL search-hidden (would push effective total to 23 with direct-fetch). Net +1 node vs 08-06 search count; +1 vs effective-count. Zero state transitions on any prior-scan PR — all 21 prior-scan PRs return identical `state`/`updatedAt` values today.

## Categorization (today = 2026-08-07, now ≈ 2026-08-07T10:11Z)

- **Recent merges (7d):** 2 — kaneo#1457 (2.6d), cindy#1116 (6.8d) *(cindy rolls off 2026-08-07T14:39Z, ~4h29m after scan)*
- **Stale open (>7d, no activity 7d):** 3 — wigolo#216 (18.1d), Baileys#2732 (9.4d), nango#6929 (9.8d)
- **Active open:** 7 — 0xprogrammable/aeon-launch-models#1 (0.5d, NEW), posthog#78346 (2.0d), k-skill#547 (3.4d), workweave/router#871 (4.4d), RuView#1409 (14.4d + activity 4.7d), voicebox#958 (14.7d + activity 4.7d), buzz#2248 (16.7d + activity 4.7d)
- **Closed no-merge (7d):** 2 — code#4007 (3.75d, **search-hidden day 2**, recovered via direct API), worldmonitor#5518 (6.2d)

Categorization tuple `(merged=2, stale=3, closed_no_merge=2, active=7)` vs prior 08-06 `(2, 3, 2, 6)` vs predicted 08-07 `(2, 3, 2, 6)`. Predictor scored:

- **Merges 2 → 2 (predicted 2 → 2):** ✓ HIT. Predictor correctly reasoned cindy#1116 rolloff 2026-08-07T14:39Z is AFTER a ~10Z scan on 08-07. **First clean scan-vs-cutoff-hour HIT since [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]] was filed** — the arithmetic was applied correctly on the merged-bucket side, four scans after the class was documented. Bug documented but predictor now demonstrating fix-in-reasoning: **the axis is fixable by discipline alone even before SKILL.md is patched** (though patch is still needed for automation).
- **Stale 2 → 3 (predicted 2 → 3):** Wait — actual prior stale on 08-06 was 3 (wigolo + Baileys + nango). Stale 3 → 3 (predicted 3 → 3): ✓ HIT. All three stale entries carry over; no new stale-eligible crossings this window (next is 2026-08-09 cohort). Predictor's deterministic-when-no-anniversary-in-window claim holds.
- **Closed_no_merge 2 → 2 (predicted 2 → 2):** ✓ HIT (again via coincident errors). Predictor: worldmonitor#5518 stays IN (rolls off 08-08T06:11Z, after scan), no fresh close projected. Correct. **BUT** search-hidden code#4007 required direct-fetch recovery for the SECOND consecutive scan — if SKILL.md were followed literally (search only), count would be 1 and prediction would MISS by 1. Second-observation-day for [[pr-tracker-search-drops-archived-repo-prs]] class; still requires ad-hoc recovery.
- **Active 6 → 7 (predicted 6 → 6):** ✗ MISS via unmodeled fresh-file arrival. Predictor: "no new stale crossings, no rolloffs; fresh-file arrival probability non-zero (posthog#78346 lesson) but not scaled to expected count." Actual: `0xprogrammable/aeon-launch-models#1` filed 08-06T22:21Z, adding to active bucket. Second fresh-file arrival in 3 days (posthog#78346 on 08-05, aeon-launch-models#1 on 08-06). Predictor recognized non-zero probability but didn't incorporate into point estimate. **Refinement:** if filing cadence stayed ≥1-per-3d over the prior rolling window (which it did — 08-03 → 08-05 → 08-06), point estimate should tick active +1.

**Predictor 3-clean-HITs of 4 + 1 unmodeled-fresh-file MISS** on this scan. **Best predictor showing in the past week** (08-05: 1-of-4 partial; 08-06: 1-clean + 1-coincidence + 2-misses). Recurring structural failures: **(a)** archive-hide of PostHog/code#4007 persists day 2 — direct-fetch fallback is now a permanent maintenance action, not a one-scan artifact; **(b)** active-bucket point estimate still not incorporating filing-cadence into fresh-file arrival. Baseline fixes needed unchanged: (a) SKILL.md direct-fetch fallback for prev-scan closed-no-merge entries missing from today's search results; (b) predictor add filing-cadence multiplier on active-bucket point estimate.

**NEW OBSERVATION 08-07:** first non-security PR of the queue — `0xprogrammable/aeon-launch-models#1` is a **draft model spec** (title: "AEON models (draft, source review): NoOp, CapGate, DynamicFee"), not a `fix(deps)` bump. All 21 prior-scan PRs are security patches; this is the first substantive-content PR. Class widens: bot files span **security-patch queue AND spec/draft queue**. Cadence and follow-through patterns may differ — needs separate tracking (spec PRs likely age slower, engage different reviewers).

## Notify decision — SEND

**Trigger:** non-zero on all three step-5 signals (merged 2 + stale 3 + closed_no_merge 2) + fresh bot file (`0xprogrammable/aeon-launch-models#1` filed 08-06T22:21Z, per [[pr-tracker-step-5-misses-fresh-bot-prs]]). No fresh OPEN → STALE transition this scan.

**Dedup guard check** per [[pr-tracker-notify-repeats-with-no-state-change]]: trigger-set is **byte-identical** to 08-06 (same 7 tuples with same updatedAt values). Guard-per-hash would fire and suppress.

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

**However**, fresh-bot-PR trigger fires independently ([[pr-tracker-step-5-misses-fresh-bot-prs]] — 0xprogrammable#1 filed ~12h ago). The fresh-file trigger sits OUTSIDE the trigger-set hash, so dedup-per-hash doesn't cover it. **Sending notify** — dedup guard applies only to the closed 7-tuple set, not to fresh arrivals on the active bucket.

**Guard-firing note:** this is the **first byte-identical trigger set** observed across two consecutive scans since dedup guard came online. Confirms guard's steady-state suppression path is exercised. Notify still fires today via the fresh-file exception; without fresh 0xprogrammable#1 arrival, this would have been the first suppressed scan.

## Notable pattern signals

- **First clean scan-vs-cutoff-hour predictor HIT** — cindy#1116 rolloff correctly deferred to post-scan hour (14:39Z > 10:11Z scan). Predictor arithmetic bug is fixable-in-reasoning today; SKILL.md patch still overdue but discipline substitutes.
- **Archive-hide is persistent (day 2)** — PostHog/code#4007 continues to be omitted from `is:pr author:aeonframework` search results 34h+ after archive event. Class [[pr-tracker-search-drops-archived-repo-prs]] is not one-scan lag; direct-fetch fallback becomes permanent maintenance action. Would drop closed_no_merge count from 2 → 1 if search-only path were used.
- **First non-security bot PR** — `0xprogrammable/aeon-launch-models#1` is a substantive spec/draft, not a dep bump. All 21 prior-scan PRs were security patches. Bot queue widens to two content classes; may need separate tracking cadence.
- **Six identity variants now observed** — bare-noreply `aeonframework@users.noreply.github.com` and numeric-prefix noreply `272311952+aeonframework@users.noreply.github.com` are logically the same GitHub account (numeric-prefix format = private-email variant of same identity), so this is **not** a sixth signing identity per [[aeon-signing-identity-fragmentation]] but a formatting variant of the existing noreply identity. Filter must accept both string forms.
- **Byte-identical trigger set (first observation)** — steady-state 08-06 → 08-07 across all 7 trigger tuples. Dedup guard's suppression path would fire today except for the orthogonal fresh-file trigger. First empirical confirmation that stable-week windows will trigger dedup suppression.
- **Filing cadence continues** — 08-03 (k-skill) → 08-05 (posthog) → 08-06 (0xprogrammable). 3 files in 3 days. Predictor must scale active-bucket fresh-file arrival by this recent-cadence multiplier.
- **RuView / voicebox / buzz stale-crossing prediction holds** — all 3 still active via 08-02 maintainer-sweep 4.7d ago. Stale-eligible date 2026-08-09. If all 3 cross on same day, that's the predicted third distinct clustered-stale class from [[same-day-file-cohort-stales-in-lockstep]] (this cohort is `08-02` cluster, not same-day-file per se — 08-02T18:29-18:33Z was a maintainer-sweep timestamp, not a filing timestamp).

## Filter and API drift

Inline OR-filter widening in step 2 jq required for the **40th consecutive day** (2026-06-29 → 2026-08-07) — SKILL.md still ships the AND filter and the single `ai/` prefix. GraphQL primary path stable this run (rc=0, 22 nodes). Archive-hide direct-API fallback needed second consecutive scan. `gh api user --jq .login` returns 403 (GITHUB_TOKEN = `github-actions[bot]`) → author hardcoded to `aeonframework`. Inline `jq` pipeline directly on `gh api graphql` output — sandbox blocked writes to `/tmp` AND to `.cache-pr-tracker/` (unclear why the latter under working directory failed) — captured stdout inline and categorized in-context.

## Next expected transitions

- **cindy#1116** — rolls off recent-merges 7d window at 2026-08-07T14:39Z (~4h29m after this scan; before end of today). Tomorrow's 08-08 scan will see it OUT.
- **worldmonitor#5518** — rolls off closed-no-merge 7d window at 2026-08-08T06:11Z (~20h after scan). 08-08 scan at ~10Z catches it OUT (assuming morning-slot scan).
- **PostHog/code#4007** — rolls off closed-no-merge 7d window at 2026-08-10T16:15Z (~3.3d out).
- **kaneo#1457** — rolls off recent-merges 7d window at 2026-08-11T19:59Z (~4.4d out).
- **RuView#1409 / voicebox#958 / buzz#2248** — all enter stale-eligible zone on 2026-08-09 (7d after their 08-02T18:29–18:33Z activity spike). Predicted: 3-way clustered-maintainer-sweep anniversary flip (2 days out).
- **workweave/router#871** — enters stale-eligible zone at 2026-08-10T13:05Z (7d after `updatedAt` 08-03T13:05Z).
- **k-skill#547** — enters stale-eligible zone at 2026-08-10T23:44Z (7d after 08-03T23:44Z filing; only engagement so far is the file event itself).
- **posthog#78346** — filed 08-05T14:08Z; enters stale-eligible zone at 2026-08-12T14:08Z if zero engagement between now and then.
- **0xprogrammable/aeon-launch-models#1** — filed 08-06T22:21Z; enters stale-eligible zone at 2026-08-13T22:21Z if zero engagement. First spec/draft PR — may age differently from dep bumps.

**Predicted 2026-08-08 tuple:** `(1, 3, 1, 7)` assuming (a) recent-merges 2 → 1 (cindy#1116 rolls off at 14:39Z on 08-07; no fresh merge projected), (b) stale 3 → 3 (no new stale-eligible crossings until 08-09), (c) closed_no_merge 2 → 1 (worldmonitor#5518 rolls off 08-08T06:11Z — if 08-08 scan runs after this, count drops to 1; if scan-hour vs cutoff-hour bug fires again, may hold at 2), (d) active 7 → 7 (no crossings, no rolloffs; filing cadence justifies non-zero fresh-file prob, but not scaled to +1). Higher-confidence: stale 3 → 3 (deterministic on 08-09). Lower-confidence: merges 2 → 1 (assumes scan runs at typical morning hour, so cindy rolloff at 14:39Z on 08-07 is behind the 08-08 morning scan).
