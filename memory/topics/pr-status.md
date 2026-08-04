# PR Status

*Last updated: 2026-08-04*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five** identities: `aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`. Inline OR filter required — accept if branch startswith any of {`ai/`, `security/`, `fix/security/`, `aeon/`} OR commit email matches any of the five known bot identities. SKILL.md-documented AND filter would still drop the entire queue.

## Open (9)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-03 | 0.5d | **fresh** — 0 comments, 0 reviews (filed 23:44Z last night, no engagement yet) |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 1.5d | fresh — 2 comments, COMMENTED review at 2026-08-02T23:45:59Z (~2min post-file); `updatedAt` = 2026-08-03T13:05:59Z |
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 3.1d | active — 4 comments (+1 vs 08-02), `updatedAt` = 2026-08-02T16:31:07Z |
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 6.5d | active — 2 comments, COMMENTED review at 2026-07-28T23:45:34Z; no fresh engagement since |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 6.8d | active — 0 comments, COMMENTED review at 2026-07-28T16:18:46Z; no fresh engagement since |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 11.8d | **broke stale** — comments 1 → 2, `updatedAt` 2026-08-02T18:29:00Z (~1.7d ago); stale-3 held prior — comment landed 08-02 evening after that scan |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 11.5d | **broke stale** — comments 0 → 1, `updatedAt` 2026-08-02T18:33:49Z (~1.7d ago); first-ever engagement after 9.8d zero-touch stale |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 15.2d | active — 5 comments, `updatedAt` 2026-07-29T20:50:22Z (~5.6d ago); age >>7d but recent-enough activity keeps out of stale bucket |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 13.7d | **broke stale** — comments 0 → 1, `updatedAt` 2026-08-02T18:29:12Z (~1.7d ago); first-ever engagement after 11.7d zero-touch stale |

## Stale open (>7d, no activity 7d) — 0

**Bucket emptied.** All three prior stale entries (voicebox / RuView / buzz) received first fresh comments on 2026-08-02 evening in a ~4-minute window (18:29–18:33Z). Both zero-engagement stale entries (RuView day 9.8 + buzz day 11.7) broke the streak simultaneously with voicebox — pattern is a same-scan-day maintainer sweep rather than per-repo triage. Watch tomorrow: if none of the three converts to a review/merge/close, they'll re-enter stale on 2026-08-09 (7d after latest activity).

## Recent Merges (last 30d) — 5

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

Vibe-Trading#390 rolls off the 30d window at 2026-08-04T15:33Z (~4h after this scan) — kept in-table since scan time is before rolloff. Same intra-day scan-vs-cutoff-hour class as 08-02's kage miss per [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]].

## Closed No-Merge (last 30d) — 6

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | fix(deps): bump simple-git, tar, minimatch to patch critical CVEs (CVSS 9.8, 9.2, 8.7) | 2026-08-03T16:15:06Z | **NEW** — OPEN → CLOSED transition since 08-02 scan; 4.1d after file; 2 comments (no maintainer engagement post-review); shortest-lived closed-no-merge in queue |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z | 8.6d after file, 3 comments (bot COMMENTED at file, +1 new comment since) — first close on 07-23 tauri cohort |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z | 2.1d after file, 3 comments (1 bot COMMENTED review at file time) — no merge |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z | 31d stale, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z | 10d, 1 comment (bot-only) — no maintainer engagement before close |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z | 9d, 4 comments, CHANGES_REQUESTED at file time then closed without update — no merge |

**Roll-offs since 08-02 scan:** kage#66 rolled off at 2026-08-02T12:20Z (~64min after that scan — predictor miss per [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]], validated exactly as predicted).

---

GraphQL `author:aeonframework is:pr` → **21 nodes** (2026-08-04 run, rc=0). Snapshot vs 2026-08-02 run (19 nodes): **+2 fresh bot files** (k-skill#547 filed 08-03T23:44Z + workweave/router#871 filed 08-02T23:44Z) and **1 OPEN → CLOSED transition** (PostHog/code#4007 closed 08-03T16:15Z after 3.9d). Ends 08-02's 0-transition scan with a **3-transition scan + 3-comment landing** (RuView + buzz + voicebox all received first fresh comments in a 4-minute window on 08-02T18:29–18:33Z). Note: no 08-03 scan ran — 10:00Z slot was inside the ISS-020 morning-batch outage cluster; two-day gap since the 08-02 baseline.

## Categorization (today = 2026-08-04, now ≈ 2026-08-04T11:41Z)

- **Recent merges (7d):** 2 — cindy#1116 (3.9d), worldmonitor#5477 (5.1d)
- **Stale open (>7d, no activity 7d):** 0 — bucket emptied (3-way maintainer-sweep on 08-02 evening broke voicebox + RuView + buzz simultaneously)
- **Active open:** 9 — k-skill#547 (0.5d, NEW), workweave/router#871 (1.5d, NEW), kaneo#1457 (3.1d), Baileys#2732 (6.5d), nango#6929 (6.8d), voicebox#958 (11.8d + fresh 1.7d), RuView#1409 (11.5d + fresh 1.7d), wigolo#216 (15.2d + activity 5.6d), buzz#2248 (13.7d + fresh 1.7d)
- **Closed no-merge (7d):** 3 — code#4007 (0.8d, NEW), worldmonitor#5518 (3.2d), open-code-review#541 (5.6d)

Categorization tuple `(merged=2, stale=0, closed_no_merge=3, active=9)` vs prior 08-02 `(4, 3, 5, 5)` vs predicted 08-03 `(3, 3, 2, 5)`. Predictor validation deferred by two days (no 08-03 scan). Post-hoc against 08-04 actual:

- **Merges 4 → 2 (predicted 4 → 3):** ✗ MISS. Both cocoindex and plano rolled off between 08-02 scan (11:16Z) and 08-04 scan (11:41Z). Predictor tracked cocoindex rolloff (08-02T23:05) but treated the 7d window as calendar-based rather than exact-hour-based for plano (07-27T22:36 + 7d = 08-03T22:36Z, out at 08-04 scan). Same intra-day scan-vs-cutoff-hour class as [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]]. **Second consecutive same-axis miss** — the 07-31 calendar-boundary fix + the 08-02 lesson do not cover this predictor axis at all yet.
- **Stale 3 → 0 (predicted 3 → 3):** ✗ MISS. Predictor assumed 3-way bucket would hold; actual was a same-scan-evening maintainer sweep on 08-02 (18:29–18:33Z) that broke all three in a 4-minute window. Novel class: **stale-bucket bulk-clear via clustered maintainer sweep**, distinct from the per-PR close-follow-through pattern the predictor was watching for. First observed instance — file as lesson candidate [[stale-bucket-bulk-clear-via-clustered-maintainer-sweep]].
- **Closed_no_merge 5 → 3 (predicted 5 → 2):** ✗ MISS. Rolloffs happened as predicted (kage 08-02T12:20 + InsForge 08-02T19:14 + openinterpreter 08-03T08:59 + Agent-Reach 08-03T13:16, all past — all four rolled off 7d window), but predictor missed the **+1 fresh OPEN → CLOSED** (PostHog/code#4007 closed 08-03T16:15Z). Delta = 5 − 4 rolloffs + 1 new = 2 → predictor got the rolloff arithmetic right but under-weighted the fresh-close probability from the active-open bucket. Predicted trajectory of 5 → 2, actual 5 → 3.
- **Active 5 → 9 (predicted 5 → 5):** ✗ MISS. Two fresh bot files (k-skill#547 + workweave/router#871) plus three OPEN → OPEN transitions (voicebox / RuView / buzz activity absorbed them back into active from stale). Predictor's zero-fresh-file assumption from 08-02 (post-cadence-pause hypothesis) proved false — bot filing resumed within the pause window.

**Predictor 0-of-4 on this two-day-gap scan.** Distinct failure modes from 08-02's 1-of-4 miss — this run's misses concentrate on (a) unmodeled bulk-stale-clear via clustered maintainer sweep, (b) same intra-day scan-vs-cutoff-hour axis as 08-02 (now second consecutive miss on this class), (c) fresh-close from active-bucket underweighted, (d) fresh-file cadence resumption from pause. The two-day gap compounds error — normally predictor gets to observe intermediate state at 08-03 scan.

## Notify decision — SEND

**Trigger:** non-zero on all three step-5 signals (merged 2 + closed_no_merge 3) + explicit fresh-bot-file trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]] (k-skill#547 + workweave/router#871 both new since last scan) + stale-bucket bulk-clear event (3 comments landed simultaneously) + 1 fresh OPEN → CLOSED transition (PostHog/code#4007).

**Dedup guard check** per [[pr-tracker-notify-repeats-with-no-state-change]]: today's trigger set is **NOT** byte-identical to prior — every single trigger element has changed. Guard does not fire. Notification proceeds.

Trigger-set hash (repo:number:state:updatedAt tuples for 7d merged + stale + 7d closed-no-merge, sorted):
```
cindy:1116:MERGED:2026-07-31T14:40:08Z
code:4007:CLOSED:2026-08-03T16:15:06Z
open-code-review:541:CLOSED:2026-07-29T20:47:45Z
worldmonitor:5477:MERGED:2026-07-30T08:17:20Z
worldmonitor:5518:CLOSED:2026-08-01T06:11:46Z
```

Prior (08-02) trigger set had 12 tuples across 4 merged + 3 stale + 5 closed. Today's set is 5 tuples — set-membership delta of 12 (7 removed via rolloff/bucket-change + 0 unchanged core + 5 present today, of which 3 are shared with prior). Not remotely byte-identical.

Fresh-bot-file trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]]: k-skill#547 (filed 08-03T23:44Z, first appearance) + workweave/router#871 (filed 08-02T23:44Z, missed prior scan by 12h33m). Fresh-bot trigger fires additively.

## Notable pattern signals

- **Stale-bucket bulk-clear via clustered maintainer sweep** — first-ever observation of this class. All three stale entries (voicebox / RuView / buzz) received first fresh comments in a 4-minute window on 08-02T18:29–18:33Z. Cross-repo (3 different repos, 3 different maintainer surfaces) simultaneous within seconds is beyond coincidence; hypothesis is **shared upstream signal** — likely a security advisory feed refresh or vulnerability aggregator update that hit all three maintainers' notification pipelines at the same time. Both zero-engagement long-tail stale entries broke; voicebox's prior 1-comment stale broke too. Watch: does the pattern repeat on a 24h / 7d / advisory-publication cadence?
- **Predictor 0-of-4 on two-day-gap scan.** Second consecutive intra-day scan-vs-cutoff-hour miss (plano this run, kage 08-02); confirms [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]] is a persistent structural bug that needs an actual fix (not just documentation). Novel class today: bulk-stale-clear via clustered maintainer sweep — file as new lesson.
- **PostHog/code#4007 shortest-lived closed-no-merge in queue** — closed 3.9d after file, no maintainer engagement post-file (2 bot comments only). Distinct from the 8-31d cluster; may indicate PostHog has a policy of closing security-dep bumps quickly if they don't fit existing dependency management workflow.
- **Fresh bot filing cadence resumed** — 08-02 zero-file scan was interrupted by 2 fresh files within ~24h (workweave/router 08-02T23:44Z ≈ 12h33m after prior scan, k-skill 08-03T23:44Z). Both use `security/` prefix + `aeonframework@users.noreply.github.com` (default GitHub-actions bot identity, not the fragmented signing identities). Both target the `bump next to 15.5.21` (workweave) and adjacent Node ecosystem work (k-skill fast-uri/find-my-way) — parallel with kaneo#1457's `next 15.5.21` from 08-01, so this looks like a **Next.js/Node advisory cohort filing burst** rather than a repo-picker cadence recovery.
- **19 → 21 nodes in two days.** GraphQL result set grew by 2 (both new bot files); no PRs left the 60-node search window in the interval.

## Filter and API drift (unchanged)

Inline OR-filter widening in step 2 jq required for the **37th consecutive day** (2026-06-29 → 2026-08-04) — SKILL.md still ships the AND filter and the single `ai/` prefix. GraphQL primary path stable this run (rc=0, 21 nodes). Sandbox: `gh api user --jq .login` returns 403 (GITHUB_TOKEN = `github-actions[bot]`) → author hardcoded to `aeonframework`. Inline `jq` pipeline directly on `gh api graphql` output — one command, one approval, no intermediate file.

## Next expected transitions

- **Vibe-Trading#390** — rolls off recent-merges 30d window at 2026-08-04T15:33Z (~4h after this scan). Next scan sees it OUT.
- **worldmonitor#5477** — rolls off recent-merges 7d window at 2026-08-06T08:17Z (2.9d out); next daily scan on 2026-08-05 still sees it IN, 2026-08-06 scan drops it.
- **cindy#1116** — rolls off recent-merges 7d window at 2026-08-07T14:39Z. Two days from now.
- **PostHog/code#4007** — rolls off closed-no-merge 7d window at 2026-08-10T16:15Z (6.2d out).
- **worldmonitor#5518** — rolls off closed-no-merge 7d window at 2026-08-08T06:11Z (3.8d out).
- **open-code-review#541** — rolls off closed-no-merge 7d window at 2026-08-05T20:47Z (1.4d out); next daily scan on 2026-08-05 still sees it IN if scan runs before 20:47Z (nominal 10:00Z scan ✓); intra-day scan-vs-cutoff-hour axis does not apply next scan (14h+ margin).
- **kaneo#1457** — enters stale-eligible zone on 2026-08-09 (7d after 08-02T16:31Z last activity) if no fresh engagement.
- **voicebox#958 / RuView#1409 / buzz#2248** — all re-enter stale-eligible zone on 2026-08-09 (7d after their simultaneous 08-02T18:29–18:33Z activity spike) if no fresh engagement. Watch whether the maintainer-sweep signal produces follow-through (reviews, merges, closes) within 7d or peters out to re-stale.
- **wigolo#216** — enters stale-eligible zone on 2026-08-05 (7d after 07-29T20:50Z last activity) if no fresh engagement. Tomorrow's scan candidate.
- **Baileys#2732** — enters stale-eligible zone on 2026-08-05 (7d after 07-28T23:45Z file+review) if no fresh engagement. Same tomorrow.
- **nango#6929** — enters stale-eligible zone on 2026-08-04T16:18Z (~4.6h from this scan, on 7d + 5min anniversary of file); realistically re-scanned tomorrow.

**Predicted 2026-08-05 tuple:** `(2, 2, 2, 9)` assuming (a) Vibe-Trading rolls off recent-30d table but 7d already had it OUT (unchanged tuple axis), (b) no fresh merges (post-Next.js-cohort quiet window), (c) wigolo + Baileys + nango all cross 7d-since-activity threshold → stale bucket 0 → 3 (unless fresh engagement), (d) open-code-review#541 stays in closed_no_merge (rolls off 08-05T20:47Z, next scan expected before that), (e) 5→3 rolloff on closed_no_merge partially offset by one speculative new close, (f) active bucket stationary at 9 unless one of the 3 wigolo/Baileys/nango moves stale (would drop active 9 → 6). Two-scenario prediction depending on whether the 08-02 maintainer-sweep signal produces follow-through. Higher-confidence axis: recent merges 2 → 2 (no active PR in mergeable position at scan time).
