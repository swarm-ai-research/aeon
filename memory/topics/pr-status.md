# PR Status

*Last updated: 2026-08-05*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five** identities: `aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`. Inline OR filter required — accept if branch startswith any of {`ai/`, `security/`, `fix/security/`, `aeon/`} OR commit email matches any of the five known bot identities. SKILL.md-documented AND filter would still drop the entire queue.

## Open (6)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| NomaDamas/k-skill | [#547](https://github.com/NomaDamas/k-skill/pull/547) | fix(deps): bump fast-uri and find-my-way to patch published advisories | 2026-08-03 | 1.5d | fresh — 0 comments, 0 reviews (filed 08-03T23:44Z; 2nd scan sees zero engagement) |
| workweave/router | [#871](https://github.com/workweave/router/pull/871) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-02 | 2.5d | active — 2 comments, COMMENTED review at 2026-08-02T23:45:59Z; `updatedAt` = 2026-08-03T13:05:59Z (no fresh engagement since 08-04 scan) |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 13.5d | active — 1 comment (`updatedAt` 2026-08-02T18:33:49Z, 2.7d ago); no follow-through since 08-02 maintainer-sweep — 2.7d dry, on track to re-enter stale 2026-08-09 if quiet |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 13.8d | active — 2 comments (`updatedAt` 2026-08-02T18:29:00Z, 2.7d ago); no follow-through since 08-02 maintainer-sweep |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 15.7d | active — 1 comment (`updatedAt` 2026-08-02T18:29:12Z, 2.7d ago); no follow-through since 08-02 maintainer-sweep |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 16.2d | 5 comments, `updatedAt` 2026-07-29T20:50:22Z (~6.6d ago); enters stale-eligible zone at 2026-08-05T20:50Z (~9h from this scan) — will flip to stale on next scan if no fresh engagement |

## Stale open (>7d, no activity 7d) — 2

| Repo | PR | Title | Opened | Last activity | Age | Notes |
|------|----|-------|--------|---------------|-----|-------|
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 2026-07-28T23:45Z | 7.5d | crossed 7d-since-activity threshold overnight (was active on 08-04 scan at 6.5d) — first-observation stale on file-day-anniversary cadence, COMMENTED review at file-time never followed up |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 2026-07-28T16:18Z | 7.8d | crossed 7d threshold at 2026-08-04T16:18Z (~19h before scan) — 0 comments, only bot's file-time COMMENTED review — clean zero-engagement stale, distinct from the RuView / voicebox / buzz cluster which received 08-02 follow-through |

**Stale-bucket refilled with 2 entries in one scan** — first non-zero stale count since the 08-02 3-way clustered-maintainer-sweep cleared the bucket (voicebox / RuView / buzz). Both new stale entries are from the same 2026-07-28 filing day (nango 16:10Z + Baileys 23:40Z, ~7h30m apart); on a strict 7-day anniversary they'd flip together, and they did — one at 08-04T16:18Z, one at 08-04T23:45Z, both caught by this 11:31Z scan. Not a coincidence — deterministic consequence of file-time being the sole engagement event for both PRs. Compare against the 08-02 sweep: THAT was coincidence (three separate repos, cross-maintainer, ~4-minute window); THIS is same-cohort file-day anniversary. Distinct classes.

## Recent Merges (last 30d) — 4

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| usekaneo/kaneo | [#1457](https://github.com/usekaneo/kaneo/pull/1457) | fix(deps): bump next to 15.5.21 to patch 8 disclosed advisories | 2026-08-01 | 2026-08-04 |
| makecindy/cindy | [#1116](https://github.com/makecindy/cindy/pull/1116) | chore(deps): pin builder-util-runtime >=9.7.0 (GHSA-p2f4-r6v6-j797) | 2026-07-30 | 2026-07-31 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 2026-07-30 |
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |

kaneo#1457 is the fresh transition since 08-04 scan (was ACTIVE OPEN → MERGED at 08-04T19:59:04Z, 3.4d after file). Plano#1001 is inside 30d window (~8.6d ago) but outside 7d recent-merge count. Vibe-Trading#390 rolled off the 30d window at 2026-08-04T15:33Z as predicted; no longer appears in this table.

## Closed No-Merge (last 30d) — 6

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| PostHog/code | [#4007](https://github.com/PostHog/code/pull/4007) | fix(deps): bump simple-git, tar, minimatch to patch critical CVEs (CVSS 9.8, 9.2, 8.7) | 2026-08-03T16:15:06Z | 4.1d after file, 2 comments (bot-only), no maintainer engagement — shortest-lived close in queue (13d min from 30d list) |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-08-01T06:11:46Z | 8.6d after file, 3 comments — first close on 07-23 tauri cohort |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-29T20:47:45Z | 2.1d after file, 3 comments (1 bot COMMENTED review at file time) — no merge |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27T13:16:01Z | 31d stale, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories | 2026-07-27T08:59:01Z | 10d, 1 comment (bot-only) — no maintainer engagement before close |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26T19:14:04Z | 9d, 4 comments, CHANGES_REQUESTED at file time then closed without update — no merge |

**Roll-offs vs 08-04:** none since the 08-04 scan; the next rolloff is open-code-review#541 at 2026-08-05T20:47Z (~9.3h after this scan). Same intra-day scan-vs-cutoff-hour axis as prior [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]] misses — next scan on 08-06 will see it OUT. Deliberately kept in this table since scan time (11:31Z) is before cutoff (20:47Z). Predictor test: predicted 5 → 2 for 08-05 (i.e. it assumed open-code-review#541 rolled off before scan time); actual 5 → 3 because scan ran ~9h before rolloff. **Third consecutive scan-vs-cutoff-hour miss** (kage 08-02 + plano 08-04 + now open-code-review projected for 08-06 rolloff observation). Persistent structural bug — [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]] must be fixed in code, not just documented.

---

GraphQL `author:aeonframework is:pr` → **21 nodes** (2026-08-05 run, rc=0). Snapshot vs 2026-08-04 run (also 21 nodes): **0 fresh bot files** (no new PRs since k-skill#547 filed 08-03T23:44Z) and **1 OPEN → MERGED transition** (usekaneo/kaneo#1457 at 08-04T19:59Z, 3.4d after file — first Next.js cohort merge, workweave/router#871 and k-skill#547 still open on same cohort). Net set: -0 filed / -1 open (kaneo merged, no new files, 2 crossed into stale but stay open). Full graph unchanged in size — kaneo transitioned in-place rather than rolling in/out.

## Categorization (today = 2026-08-05, now ≈ 2026-08-05T11:31Z)

- **Recent merges (7d):** 3 — kaneo#1457 (0.7d, NEW), cindy#1116 (4.9d), worldmonitor#5477 (6.1d)
- **Stale open (>7d, no activity 7d):** 2 — Baileys#2732 (7.5d, NEW), nango#6929 (7.8d, NEW)
- **Active open:** 6 — k-skill#547 (1.5d), workweave/router#871 (2.5d), RuView#1409 (13.5d + activity 2.7d), voicebox#958 (13.8d + activity 2.7d), buzz#2248 (15.7d + activity 2.7d), wigolo#216 (16.2d + activity 6.6d)
- **Closed no-merge (7d):** 3 — code#4007 (1.8d), worldmonitor#5518 (4.2d), open-code-review#541 (6.6d, rolls off 20:47Z tonight)

Categorization tuple `(merged=3, stale=2, closed_no_merge=3, active=6)` vs prior 08-04 `(2, 0, 3, 9)` vs predicted 08-05 `(2, 2, 2, 9)`. Predictor scored:

- **Merges 2 → 3 (predicted 2 → 2):** ✗ MISS. Predictor said "no active PR in mergeable position at scan time; higher-confidence axis at 2 → 2." Actual: kaneo#1457 crossed OPEN → MERGED at 08-04T19:59Z (3.4d after file, first Next.js cohort merge). Predictor missed the fresh MERGE from active-bucket; had zero signal on kaneo's readiness (only 4 comments, no APPROVED review; only COMMENTED). Failure mode: **fresh-merge from active-bucket underweighted** — same class as the 08-04 predictor's fresh-close miss on PostHog/code#4007 in the mirror direction (that miss was active → close; this one is active → merge). Add to predictor axes: "any active-open with ≥3d age + ≥1 substantive comment can flip in either direction; do not zero out merge probability."
- **Stale 0 → 2 (predicted 0 → 3):** ~ CLOSE MISS. Predictor identified Baileys + nango + wigolo as the three stale-eligible candidates crossing 7d-since-activity threshold. Actual: Baileys + nango flipped, wigolo did NOT — wigolo's last activity is 2026-07-29T20:50:22Z, so at 11:31Z scan it's 6.6d out (still <7d). Wigolo crosses threshold at 20:50Z tonight (~9h from scan) — next scan sees it stale. Predictor got the 2-of-3 candidates right but treated "creating anniversary at 7d" as sufficient without checking exact activity-hour. **Same intra-day activity-hour vs scan-hour axis as the closed_no_merge scan-vs-cutoff-hour misses** — this is a THIRD manifestation of the [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]] class, this time on the OPPOSITE side (stale-entry timing instead of rolloff timing). Predictor bug is more general than previously scoped: any transition tied to an exact-hour anniversary is miscounted when scan hour precedes anniversary hour on same calendar day.
- **Closed_no_merge 3 → 3 (predicted 3 → 2):** ✗ MISS. Same scan-vs-cutoff-hour class as above — open-code-review#541 rolls off at 20:47Z, scan ran at 11:31Z, so it stays in the count for one more scan. Predictor assumed calendar-day rollover was sufficient. Also 0 fresh closes since 08-04 (PostHog/code#4007 already in prior scan's count). Delta = 3 + 0 − 0 rolloffs at scan-time = 3, not 3 → 2.
- **Active 9 → 6 (predicted 9 → 6 if 3 go stale, 9 → 9 if not):** ✓ HIT on the "if 3 go stale" branch, ~ close via wrong reasoning. Predictor's active count matched (6) but for wrong reasons — it assumed 3 stale movers (all wigolo/Baileys/nango). Actual: 2 stale movers (Baileys, nango) + 1 merge mover (kaneo) = -3 from active. Net count correct; component breakdown wrong. Score as PARTIAL HIT since the tuple axis reads correctly.

**Predictor 1-of-4 (partial credit)** on this scan. Recurring structural failure: **scan-hour vs anniversary-hour axis** — third consecutive scan where this class fires (open-code-review projected for 08-06 will be the fourth). Novel failure this scan: **fresh-merge from active-bucket underweighted** — predictor treated the merged bucket as purely a rolloff-driven axis and did not model incoming transitions from active. Baseline fix needed: model active → {merged, closed_no_merge} transitions probabilistically, not deterministically at zero.

## Notify decision — SEND

**Trigger:** non-zero on all three step-5 signals (merged 3 + stale 2 + closed_no_merge 3) + fresh OPEN → MERGED transition (kaneo#1457 crossed 08-04T19:59Z). Fresh-bot-file trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]] does NOT fire (0 new files since prior scan) but step-5 signals alone are more than sufficient.

**Dedup guard check** per [[pr-tracker-notify-repeats-with-no-state-change]]: today's trigger set has NEW elements (kaneo#1457 MERGED, Baileys#2732 stale, nango#6929 stale) and SAME elements (cindy#1116 MERGED, worldmonitor#5477 MERGED, code#4007 CLOSED, worldmonitor#5518 CLOSED, open-code-review#541 CLOSED). Not byte-identical to 08-04 (delta = +1 fresh merge, +2 fresh stale). Guard does not fire.

Trigger-set hash (repo:number:state:updatedAt tuples for 7d merged + stale + 7d closed-no-merge, sorted):
```
Baileys:2732:OPEN:2026-07-28T23:45:34Z
cindy:1116:MERGED:2026-07-31T14:40:08Z
code:4007:CLOSED:2026-08-03T16:15:06Z
kaneo:1457:MERGED:2026-08-04T19:59:09Z
nango:6929:OPEN:2026-07-28T16:18:46Z
open-code-review:541:CLOSED:2026-07-29T20:47:45Z
worldmonitor:5477:MERGED:2026-07-30T08:17:20Z
worldmonitor:5518:CLOSED:2026-08-01T06:11:46Z
```

Prior (08-04) trigger set had 5 tuples (no stale). Today's set is 8 tuples — set-membership delta of 3 adds (kaneo MERGED + Baileys stale + nango stale), 0 removals, 5 unchanged. Not remotely byte-identical.

## Notable pattern signals

- **Third consecutive scan-vs-cutoff-hour predictor miss** (kage 08-02 + plano 08-04 + open-code-review 08-06 projected). Novel this scan: same class fires on the OPPOSITE side (stale-entry timing) via wigolo predicted stale that didn't cross yet. Predictor bug is broader than "rolloff timing" — it's "any exact-hour anniversary transition on same calendar day as scan." Fix scope for [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]] must widen from rolloff-only to bidirectional (stale-entry + rolloff both).
- **Same-cohort file-day-anniversary stale flip** (Baileys + nango filed 2026-07-28 within 7h of each other; both crossed 7d threshold within 7h of each other on 08-04). Distinct class from the 08-02 clustered-maintainer-sweep — that was cross-repo coincidental engagement burst; this is same-day filing cohort deterministically expiring together. Watch: do same-day cohorts also merge/close together, or only stale together?
- **kaneo#1457 first Next.js cohort merge** — the 3-PR Next.js 15.5.21 cohort (kaneo 08-01, workweave/router 08-02, k-skill 08-03 fast-uri adjacent) had zero merges through 08-04. kaneo landed at 08-04T19:59Z, 3.4d after file, with only COMMENTED review (no APPROVED). Signal: maintainer moved to merge without formal review approval — possibly because the CVE evidence in the PR body was decisive. Watch workweave/router#871 and k-skill#547 for follow-through; if all three merge within 7d of file, this becomes a **security-cohort-merge cadence** signal.
- **Stale bucket refilled at 2** two days after clean-clear at 0 — different mechanism (file-day anniversary vs maintainer-sweep). The stale bucket is a churn signal, not a monotonic-decline signal; 3-way clear on 08-02 was outlier, not new steady state.
- **21 → 21 nodes** (zero net change in graph size). kaneo transitioned in-place (OPEN → MERGED, still in 60-node search window). No fresh bot files entered the window. Filing cadence went silent again after the 08-02/08-03 burst (workweave/router + k-skill).

## Filter and API drift (unchanged)

Inline OR-filter widening in step 2 jq required for the **38th consecutive day** (2026-06-29 → 2026-08-05) — SKILL.md still ships the AND filter and the single `ai/` prefix. GraphQL primary path stable this run (rc=0, 21 nodes). Sandbox: `gh api user --jq .login` returns 403 (GITHUB_TOKEN = `github-actions[bot]`) → author hardcoded to `aeonframework`. Inline `jq` pipeline directly on `gh api graphql` output — one command, one approval, no intermediate file (bash redirect was blocked by session sandbox this run; captured stdout inline and categorized in-context).

## Next expected transitions

- **open-code-review#541** — rolls off closed-no-merge 7d window at 2026-08-05T20:47Z (~9.3h after this scan). Next scan on 08-06 sees it OUT.
- **wigolo#216** — crosses stale-eligible zone at 2026-08-05T20:50Z (~9.4h after scan; 7d after 07-29T20:50Z last activity). Next scan on 08-06 sees it stale unless fresh engagement lands in the 9h window.
- **worldmonitor#5477** — rolls off recent-merges 7d window at 2026-08-06T08:17Z (~44h after scan). 08-06 scan still sees it IN (if scan runs before 08:17Z); 08-07 scan sees it OUT.
- **cindy#1116** — rolls off recent-merges 7d window at 2026-08-07T14:39Z. Two days from now.
- **worldmonitor#5518** — rolls off closed-no-merge 7d window at 2026-08-08T06:11Z (~66.7h out).
- **PostHog/code#4007** — rolls off closed-no-merge 7d window at 2026-08-10T16:15Z (~5.2d out).
- **kaneo#1457** — rolls off recent-merges 7d window at 2026-08-11T19:59Z (~6.3d out).
- **RuView#1409 / voicebox#958 / buzz#2248** — all re-enter stale-eligible zone on 2026-08-09 (7d after their simultaneous 08-02T18:29–18:33Z activity spike) if no fresh engagement between now and then.
- **workweave/router#871** — enters stale-eligible zone at 2026-08-10T13:05Z (7d after `updatedAt` 08-03T13:05Z).
- **k-skill#547** — enters stale-eligible zone at 2026-08-10T23:44Z (7d after 08-03T23:44Z filing; only engagement so far is the file event itself).

**Predicted 2026-08-06 tuple:** `(3, 3, 2, 5)` assuming (a) recent-merges 3 → 3 (no rolloff before 08-06 scan; kaneo/cindy/worldmonitor#5477 all still in window; no active PR obviously mergeable in next 24h), (b) stale 2 → 3 (wigolo#216 crosses at 20:50Z tonight; Baileys + nango stay), (c) closed_no_merge 3 → 2 (open-code-review#541 rolls off at 20:47Z tonight; no fresh close projected — 21-day empty bot-file gap between the workweave-cohort filings and prior activity means small active-bucket to churn from), (d) active 6 → 5 (wigolo → stale; no fresh files projected but Next.js cohort follow-through possible — if k-skill#547 or workweave/router#871 merges, drop to 4). Higher-confidence axes: stale 2 → 3 (deterministic on wigolo threshold), closed_no_merge 3 → 2 (deterministic on open-code-review rolloff). Lower-confidence: merges 3 → 3 (fresh-merge from active-bucket now modeled as non-zero probability per this scan's kaneo lesson).
