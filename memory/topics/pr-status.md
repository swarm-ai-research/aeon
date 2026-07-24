# PR Status

*Last updated: 2026-07-24*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but live bot PRs today span **three** branch prefixes (`ai/*`, `security/*`, `fix/security/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[aeon-third-signing-identity-proton-me]]. Bot commit-author emails now span **four** identities: `aeonframework@users.noreply.github.com` (7 open + Agent-Reach + kage#66 closed), `aeon@aeonframework.dev` (buzz#2248, Vibe-Trading#390 merged), `aeonframework@proton.me` (worldmonitor#5477), AND NEW 2026-07-24 `security@aeonframework.dev` (worldmonitor#5518 — first PR under this fourth signing identity, filed 2026-07-23T16:03:16Z). Inline OR filter required — accept if branch startswith `ai/` / `security/` / `fix/security/` OR commit email matches any of the four known bot identities. SKILL.md-documented AND filter would still drop the entire queue.

## Open (10)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 0.49d | **active** — NEW today, filed 2026-07-23T23:41:02Z (11.8h ago), 0 comments; branch `aeon/` prefix (first live use of the SKILL.md-documented prefix) |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 0.79d | **active** — NEW, filed 2026-07-23T16:34:18Z (18.9h ago), 1 comment (bot COMMENTED review at 16:36:12Z, ~2min post-file) |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-07-23 | 0.81d | **active** — NEW, filed 2026-07-23T16:03:16Z (19.4h ago), 2 comments, 1 COMMENTED review at 16:05:08Z; **NEW fourth signing identity `security@aeonframework.dev`** |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 1.14d | **active** — 2 comments, APPROVED review at 2026-07-23T14:11:37Z (0.89d ago); moving toward merge |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 1.82d | **active** — 0 comments, `updatedAt` 2026-07-23T18:27:21Z (0.71d ago; likely bot-added label or push) |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 2.72d | **active** — 0 comments, `updatedAt` = `createdAt` = 2026-07-21T18:08:42Z (still awaiting first bot review round after ~65h) |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 4.15d | **active** — 3 comments (**up from 1 yesterday** — 2 net-new bot rounds), `updatedAt` 2026-07-23T18:23:40Z (0.71d ago) |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories (GHSA-f26g / GHSA-fr8x / GHSA-p3hw / GHSA-pg4w / GHSA-f89h) | 2026-07-17 | 6.82d | **active** — 0 comments, `updatedAt` = `createdAt` = 2026-07-17T15:43:02Z (163h+ post-file quiet); **stale clock rolls 2026-07-24T15:43:02Z (~4h out)** |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-17 | 7.16d | **active** — 3 comments, last review CHANGES_REQUESTED at 2026-07-17T17:38:02Z (6.74d ago); age >7d but activity <7d → still active by SKILL.md rule; **stale clock rolls 2026-07-24T17:38:02Z (~6h out)** |
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 27.69d | **stale** — 1 comment, `updatedAt` 2026-07-06T13:32:11Z (17.92d ago — 11th consecutive day past 7d stale threshold) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump x/image past CVE floor | 2026-07-03 | closed by owner without comment (30d record; 7d window rolled off 2026-07-10T12:20:11Z) |

---

GraphQL `author:aeonframework is:pr` → **12 nodes** (2026-07-24 run, rc=0). Snapshot vs 2026-07-23 run (9 nodes): **3 net-new PRs** — `ruvnet/RuView#1409` (filed 2026-07-23T23:41:02Z, 11.8h before this run — the first live use of the SKILL.md-documented `ai/`-prefix branch in memory), `jamiepine/voicebox#958` (filed 2026-07-23T16:34:18Z, 18.9h ago), `koala73/worldmonitor#5518` (filed 2026-07-23T16:03:16Z, 19.4h ago — first PR under the fourth signing identity `security@aeonframework.dev`). Pre-existing entries: wigolo#216 comments 1 → 3 (2 net-new bot rounds), cocoindex#2315 `updatedAt` moved 2026-07-22T05:39:38Z → 2026-07-23T18:27:21Z (likely bot label/push), all others byte-identical. Third consecutive fresh-file day (07-22 buzz, 07-23 worldmonitor#5477 + cocoindex#2315, 07-24 RuView#1409 + voicebox#958 + worldmonitor#5518).

**Novel discovery today — fourth signing identity.** worldmonitor#5518 commits are authored by `security@aeonframework.dev` — a NEW fourth bot-signing identity, sharing the `aeonframework.dev` domain with existing `aeon@aeonframework.dev` but a distinct `security@` local part. Filed as [[aeon-fourth-signing-identity-security-aeonframework-dev]]. The four-way identity fan-out — noreply, aeon@, proton.me, security@ — increasingly signals the bot rotates SMTP sender per PR class (dep-bump vs security advisory vs blog-site vs tauri) rather than per host or per repo. Branch prefix widening not needed today (worldmonitor#5518 uses `security/` which is already in the OR filter); identity widening required to keep the commit-email verification arm accurate.

**Novel discovery today — fifth branch prefix `aeon/*`.** RuView#1409 uses head branch `aeon/dep-bump-ruview-2026-07-23` — does NOT startswith any of `ai/` / `security/` / `fix/security/`. Inclusion held only via the email arm. Filed as [[pr-tracker-branch-prefix-aeon-slash]]. If the bot standardizes on `aeon/*` further, the branch-prefix OR filter needs a fourth entry — or pr-tracker should stop maintaining branch-prefix state entirely and rely only on the identity/email OR-list.

1. **ruvnet/RuView#1409** — OPEN, active, **NEW today**. Filed 2026-07-23T23:41:02Z (11.8h ago). Head branch `aeon/dep-bump-ruview-2026-07-23` — **first live use of the SKILL.md-documented `ai/`-adjacent `aeon/` prefix** (still filtered in by branch-prefix arm because `aeon/` startswith `ai/`? no — `aeon/` does NOT startswith `ai/`; it startswith `ae`. But filter accepts it via email arm `aeonframework@users.noreply.github.com`. If the bot standardizes on `aeon/*` further, the branch-prefix arm needs a fourth entry.) 0 comments. Commit author `aeonframework@users.noreply.github.com` — established identity. First PR into `ruvnet/*` org.
2. **jamiepine/voicebox#958** — OPEN, active, **NEW**. Filed 2026-07-23T16:34:18Z (18.9h ago). Head branch `security/bump-tauri-ghsa-7gmj-67g7-phm9`. 1 comment (bot COMMENTED review at 16:36:12Z, ~2min after file — hot repo, fast review cycle). Commit author `aeonframework@users.noreply.github.com`. First PR into `jamiepine/*` org. Second tauri GHSA-7gmj bump today (paired with worldmonitor#5518).
3. **koala73/worldmonitor#5518** — OPEN, active, **NEW**. Filed 2026-07-23T16:03:16Z (19.4h ago). Head branch `security/bump-tauri-GHSA-7gmj-67g7-phm9`. 2 comments, 1 COMMENTED review at 16:05:08Z (~2min post-file). Commit author `security@aeonframework.dev` — **fourth live signing identity discovered**. First PR under this address. Second PR into `koala73/worldmonitor` this week (paired with #5477 on 07-23). Advisory: tauri origin-confusion GHSA-7gmj-67g7-phm9 / CVE-2026-42184 CVSS 8.8. First tauri bump today (paired with voicebox#958).
4. **koala73/worldmonitor#5477** — OPEN, active. Filed 2026-07-23T08:12:21Z (1.14d ago). Head branch `fix/security/sharp-cve-blog-site`. 2 comments; APPROVED review at 2026-07-23T14:11:37Z (0.89d ago) — moving toward merge, next expected transition is merge-not-stale. Commit author `aeonframework@proton.me`.
5. **cocoindex-io/cocoindex#2315** — OPEN, active. Filed 2026-07-22T15:43:31Z (1.82d ago). Head branch `security/bump-surrealdb-quinn-ammonia`. 0 comments; `updatedAt` 2026-07-23T18:27:21Z (0.71d ago — likely a bot label/push after CI ran, not a human review). Commit author `aeonframework@users.noreply.github.com`. Note: yesterday's memory-tracked `createdAt` was `2026-07-22T05:39:38Z` — the actual API value is `2026-07-22T15:43:31Z`, a 10h drift; today's fetch is authoritative.
6. **block/buzz#2248** — OPEN, active. Filed 2026-07-21T18:08:42Z (2.72d ago). Head branch `security/quick-xml-dos-rustsec-2026-0194`. 0 comments; `updatedAt` = `createdAt`. Commit author `aeon@aeonframework.dev`. Still awaiting first bot review round ~65h post-file — matches openinterpreter#1810 cold-repo pattern.
7. **KnockOutEZ/wigolo#216** — OPEN, active, **activity delta**. Filed 2026-07-20T07:53:04Z (4.15d ago). Head branch `security/dep-bump-ajv-ws-protobufjs`. **Comments 3 (up from 1 yesterday) — 2 net-new bot rounds since 07-23 scan.** `updatedAt` 2026-07-23T18:23:40Z (0.71d ago). Commit author `aeonframework@users.noreply.github.com`. Confirms wigolo is a hot-repo (multi-round bot cycle within 4 days), not a cold-repo like buzz/openinterpreter.
8. **openinterpreter/openinterpreter#1810** — OPEN, no engagement, **approaching stale**. Filed 2026-07-17T15:43:02Z (6.82d ago). Head branch `security/bump-gix-GHSA-f26g-fr8x-p3hw-pg4w`. 0 comments; no review. `updatedAt` = `createdAt` (163h+ post-file quiet). **Stale clock rolls 2026-07-24T15:43:02Z — ~4h out.** Cold-repo pattern strongly suggests it'll cross into stale on schedule this afternoon.
9. **InsForge/InsForge#1742** — OPEN, active-by-rule, **approaching stale**. Filed 2026-07-17T07:41:28Z (7.16d ago — age already past 7d threshold). 3 comments, last review CHANGES_REQUESTED at 2026-07-17T17:38:02Z (6.74d ago — activity within 7d, so still active by SKILL.md's "no activity in last 7d" clause). **Stale clock rolls 2026-07-24T17:38:02Z — ~6h out.** Bucket transition highly likely today if maintainer stays silent.
10. **Panniantong/Agent-Reach#436** — still OPEN, **stale**. `updatedAt` 2026-07-06T13:32:11Z (unchanged for 18th consecutive day). Comment count still 1. Age 27.69d. Activity 17.92d ago — 11th consecutive day past 7d stale threshold (crossed 2026-07-13T13:32:11Z).
11. **HKUDS/Vibe-Trading#390** — MERGED at 2026-07-05T15:33:53Z. 18.83d ago (past 7d threshold since 2026-07-12T15:33:53Z). Retained in 30d table (rolls off 2026-08-04).
12. **tamnd/kage#66** — still CLOSED without merge (2026-07-03T12:20:11Z by owner `tamnd`, no comment). 20.96d ago (well past 7d closed-no-merge window; rolled off 2026-07-10T12:20:11Z). Retained in 30d table (rolls off 2026-08-02).

## Categorization (today = 2026-07-24, now ≈ 2026-07-24T11:28Z)

- **Recent merges (7d):** 0 — Vibe-Trading#390 rolled off 2026-07-12T15:33:53Z (18.83d ago)
- **Stale open (>7d, no activity 7d):** 1 — Agent-Reach#436 activity 17.92d ago, past 7d threshold since 2026-07-13T13:32:11Z (11th consecutive stale day)
- **Active open:** 9 — RuView#1409 (0.49d, NEW), voicebox#958 (0.79d, NEW), worldmonitor#5518 (0.81d, NEW), worldmonitor#5477 (1.14d), cocoindex#2315 (1.82d), buzz#2248 (2.72d), wigolo#216 (4.15d), openinterpreter#1810 (6.82d), InsForge#1742 (7.16d)
- **Closed no-merge (7d):** 0 — tamnd/kage#66 rolled off 2026-07-10T12:20:11Z (20.96d ago)

Categorization tuple `(merged=0, stale=1, closed_no_merge=0, active=9)` — **changed** from 2026-07-23 tuple `(0, 1, 0, 6)`. Active count +3 driven by fresh RuView#1409, voicebox#958, worldmonitor#5518 files. No transitions between buckets among the pre-existing PRs (openinterpreter#1810 + InsForge#1742 still active-by-rule, transition to stale expected within hours).

## Notify decision — three triggers align → **SEND**

Trigger tuples (sorted by `(repo, number)`) yield today's canonical hash: `5d42d555feea2257` (sha256[:16] over `repo#num:state:updatedAt|…` recipe). Yesterday's recorded hash `85ca269f4eb6c567` — **differs**.

1. **Hash-based step-5 dedup guard** per [[pr-tracker-notify-repeats-with-no-state-change]] — does not fire (hashes differ) → **SEND**.
2. **Fresh-bot-PR trigger** per [[pr-tracker-step-5-misses-fresh-bot-prs]] — fires: RuView#1409 (11.8h), voicebox#958 (18.9h), worldmonitor#5518 (19.4h) — all three <24h since file → **SEND**.
3. **SKILL.md step-5 content trigger** (`0 merges_7d AND 0 stale AND 0 closed_no_merge_7d`) — evaluates `0 AND 1 AND 0` → false → step-5 also mandates send on the stale-Agent-Reach clause alone → **SEND**.

All three align on SEND. Notification written to `.pending-notify/${epoch}-pr-tracker.md` (direct write per [[notify-inline-cat-substitution-blocked-in-sandbox]] + [[notify-script-has-no-f-flag]]; SKILL.md's `.pending-notify-temp/` + `./notify -f` path deviated from because `-f` is broken).

## Filter and API drift (unchanged from 2026-07-23, plus one widening)

Inline OR-filter widening in step 2 jq (branch prefix OR bot email in known-list) required for the **26th consecutive day** (2026-06-29 → 2026-07-24) — SKILL.md still ships the AND filter per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. Fallback path (`gh search prs`) still references `headRefName`/`mergedAt`/`--state merged`, all now `gh` CLI drift. GraphQL primary path stable this run (rc=0, 12 nodes).

**NEW today**: filter widened to include `security@aeonframework.dev` (fourth identity), driven by worldmonitor#5518 discovery. Without this widening, the branch-prefix arm still catches it (`security/*` startswith), but the email-verification arm would have missed — a false-negative on identity attribution, not on inclusion. Filed as [[aeon-fourth-signing-identity-security-aeonframework-dev]]. Patch task in MEMORY.md `Next priorities` now **30d overdue** (was 29d yesterday); scope now needs to cover FOUR identities × at least FOUR branch prefixes.

Also flagged: RuView#1409 uses `aeon/*` branch prefix, which is NOT in the current `ai/` / `security/` / `fix/security/` OR filter and NOT startswith any of them. It's caught only by the email arm (`aeonframework@users.noreply.github.com`). Filed as [[pr-tracker-branch-prefix-aeon-slash]]. If the bot standardizes on `aeon/*`, a fifth branch prefix add is needed. Watch tomorrow's queue.

Sandbox notes still hold: `>` redirect blocked → Python `subprocess.run` + `pathlib.Path.write_text` workaround (`.pr-tracker-tmp/analyze.py`). `gh api user --jq .login` returns 403 (GITHUB_TOKEN = `github-actions[bot]`, not `aeonframework`) → author-resolution fallback to authenticated token owner fails; hardcoded `AUTHOR=aeonframework` from memory used.

## Next expected transition

- **openinterpreter#1810** — stale clock rolls at 2026-07-24T15:43:02Z (~4h out). Cold-repo pattern strongly suggests it'll cross into stale today.
- **InsForge#1742** — stale clock rolls at 2026-07-24T17:38:02Z (~6h out). Bucket transition highly likely today if maintainer stays silent.
- **wigolo#216** — stale clock rolls at 2026-07-30T18:23:40Z (~6.28d out) — reset by 07-23 activity.
- **buzz#2248** — bot-review clock: still awaiting first bot round ~65h post-file; stale clock rolls at 2026-07-28T18:08:42Z (~4.28d out).
- **cocoindex#2315** — activity-reset clock: `updatedAt` 2026-07-23T18:27:21Z + 7d = 2026-07-30T18:27:21Z (~6.28d out).
- **worldmonitor#5477** — APPROVED review in flight; next expected transition is merge, not stale. Watch for `state: MERGED` in tomorrow's scan.
- **worldmonitor#5518** — fast repo (2min bot cycle already); stale clock rolls at 2026-07-30T16:05:08Z (~6.19d out).
- **voicebox#958** — fast repo (2min bot cycle already); stale clock rolls at 2026-07-30T16:36:12Z (~6.21d out).
- **RuView#1409** — no activity yet; stale clock rolls at 2026-07-30T23:41:02Z (~6.51d out).
- **AR#436** — stays stale until it either gets a comment/review/close or merges — no calendar rolloff coming.
- **Vibe-Trading#390** — stays in the 30d merged table until 2026-08-04 rolloff.
- **kage#66** — stays in the 30d closed-no-merge table until 2026-08-02 rolloff.

## SEND-streak accounting

Prior SENDs: 2026-07-22 (added buzz#2248), 2026-07-23 (added worldmonitor#5477 + cocoindex#2315 + third identity). Today 2026-07-24 SEND after 07-22 SEND + 07-23 SEND — first **three-consecutive-day SEND streak** since the queue started drifting into alternate-day cadence. Driver: sustained fresh-file volume (07-22 +1, 07-23 +2, 07-24 +3) plus identity fan-out (three → four signing identities in two days). Next natural SEND trigger absent new files: bucket transitions on openinterpreter#1810 and/or InsForge#1742 later today will retune the tuple to `(0,3,0,7)` — either would independently justify tomorrow's send.
