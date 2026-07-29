# PR Status

*Last updated: 2026-07-29*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five** identities: `aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`. Inline OR filter required — accept if branch startswith any of {`ai/`, `security/`, `fix/security/`, `aeon/`} OR commit email matches any of the five known bot identities. SKILL.md-documented AND filter would still drop the entire queue.

## Open (8)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| WhiskeySockets/Baileys | [#2732](https://github.com/WhiskeySockets/Baileys/pull/2732) | fix(deps): bump ws, protobufjs, and protobufjs-cli for 5 disclosed CVEs | 2026-07-28 | 0.9d | **active** — fresh today, 2 comments, COMMENTED review at 2026-07-28T23:45:34Z |
| NangoHQ/nango | [#6929](https://github.com/NangoHQ/nango/pull/6929) | fix(deps): bump qs, fast-xml-parser, postcss for disclosed CVEs | 2026-07-28 | 1.1d | **active** — fresh today, 0 comments, COMMENTED review at 2026-07-28T16:18:46Z |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 9.1d | **active** — 4 comments, `updatedAt` 2026-07-28 (~1d ago); age >7d but recent activity keeps it out of stale bucket |
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-27 | 1.7d | **active** — 1 comment, COMMENTED review at 2026-07-27T17:06:16Z |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 5.5d | **active** — 0 comments, 0 reviews (still no engagement ~132h post-file) |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 5.8d | **active** — 1 comment (bot COMMENTED review 07-23T16:36:12Z); stale-clock rolls 07-30 |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-07-23 | 5.8d | **active** — 2 comments, COMMENTED review at 2026-07-23T16:05:08Z; identity `security@aeonframework.dev`; stale-clock rolls 07-30 |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 6.1d | **active** — 2 comments, APPROVED review at 2026-07-23T14:11:37Z; **day-7 of APPROVED-but-not-merged** — extends longest cold-approve on record; stale-clock rolls 07-30 |

## Stale open (>7d, no activity 7d) — 1

| Repo | PR | Title | Opened | Age | Notes |
|------|----|-------|--------|-----|-------|
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 8.0d | 0 comments, 0 reviews; `updatedAt` = `createdAt` = 2026-07-21T18:08:42Z; **stale as of 2026-07-28T18:08:42Z** (yesterday's prediction hit on schedule) |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| katanemo/plano | [#1001](https://github.com/katanemo/plano/pull/1001) | fix(deps): patch serde_with, tokio-postgres, turbo, undici, next for disclosed CVEs | 2026-07-24 | 2026-07-27 |
| cocoindex-io/cocoindex | [#2315](https://github.com/cocoindex-io/cocoindex/pull/2315) | fix(deps): bump surrealdb >=3.2.3 to patch quinn-proto DoS (CVSS 7.5) and ammonia XSS | 2026-07-22 | 2026-07-26 |
| HKUDS/Vibe-Trading | [#390](https://github.com/HKUDS/Vibe-Trading/pull/390) | fix(deps): bump Pillow and langchain floors past disclosed CVEs | 2026-07-03 | 2026-07-05 |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-07-27 | closed after 31d stale, 3 comments — no merge |
| openinterpreter/openinterpreter | [#1810](https://github.com/openinterpreter/openinterpreter/pull/1810) | fix(deps): bump gix to 0.83 to patch 5 security advisories (GHSA-f26g / GHSA-fr8x / GHSA-p3hw / GHSA-pg4w / GHSA-f89h) | 2026-07-27 | closed after 10d, 1 comment (bot-only) — no maintainer engagement before close |
| InsForge/InsForge | [#1742](https://github.com/InsForge/InsForge/pull/1742) | fix(deps): bump multer to 2.2.0 and nodemailer to 8.0.11 to patch disclosed DoS/CRLF advisories | 2026-07-26 | closed after 9d, 3 comments, CHANGES_REQUESTED at file time then closed without update — no merge |
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump golang.org/x/image to v0.43.0 (3 advisories) | 2026-07-03 | closed by owner without comment; 30d window rolls off 2026-08-02 |

---

GraphQL `author:aeonframework is:pr` → **16 nodes** (2026-07-29 run, rc=0). Snapshot vs 2026-07-28 run (14 nodes): **+2 net-new PRs** (Baileys#2732 + nango#6929), no merges, no closures. Yesterday's prediction `(2, 1, 3, 6)` came in `(2, 1, 3, 8)` — stale-clock prediction on buzz#2248 hit on schedule, and the +2 fresh files exceeded the median 1.5d inter-file gap.

## Categorization (today = 2026-07-29, now ≈ 2026-07-29T09:30Z)

- **Recent merges (7d):** 2 — plano#1001 (2026-07-27, ~2d ago), cocoindex#2315 (2026-07-26, ~3d ago)
- **Stale open (>7d, no activity 7d):** 1 — buzz#2248 (opened 2026-07-21, no touch since, rolled stale on schedule)
- **Active open:** 8 — Baileys#2732 (fresh), nango#6929 (fresh), wigolo#216 (9d + recent activity), open-code-review#541 (2d), RuView#1409 (5.5d, zero-engagement), voicebox#958 (5.8d), worldmonitor#5518 (5.8d), worldmonitor#5477 (APPROVED day-7)
- **Closed no-merge (7d):** 3 — Agent-Reach#436, openinterpreter#1810, InsForge#1742

Categorization tuple `(merged=2, stale=1, closed_no_merge=3, active=8)` vs prior `(2, 0, 3, 7)`. The +2 fresh files (Baileys + nango, both 2026-07-28, both bot COMMENTED reviews at file time) drove active_open 7→8 and pool 14→16 nodes.

## Notify decision — SEND

Non-zero on merges (2) AND stale (1) AND closed-no-merge (3). All three SKILL.md-required signals fire. Prior canonical hash (07-28's SEND) no longer valid — state has advanced (new stale bucket entry + 2 fresh PRs). Notify sent.

## Notable pattern signals

- **`worldmonitor#5477` — APPROVED day-7.** Cold-approve stretch extends to 7 calendar days (2026-07-23T14:11:37Z APPROVED → 2026-07-29T09:30Z). Extends longest APPROVED-not-merged on record. Stale-clock rolls tomorrow (2026-07-30) if merge doesn't happen first.
- **buzz#2248 rolled stale on schedule.** Yesterday's prediction: "stale-clock rolls today at 18:08:42Z." Confirmed — 8d old, zero comments, zero reviews, no touch since file. First same-day stale-clock prediction hit for this queue.
- **Two fresh bot PRs in one day** (Baileys#2732 + nango#6929, both filed 2026-07-28). Filing rate briefly elevated above the ~1.5d median inter-file gap. Both are multi-package dep-bumps citing CVEs — the pattern that appears to accelerate maintainer review per prior merges.
- **worldmonitor#5518** (tauri) and **worldmonitor#5477** (sharp) both hit their 7d stale-clock threshold tomorrow (2026-07-30). Same repo, same maintainer surface — a coincident stale-transition day is likely.
- **voicebox#958** also hits 7d stale threshold 2026-07-30. Three-way stale-transition candidate day.

## Filter and API drift (unchanged)

Inline OR-filter widening in step 2 jq required for the **31st consecutive day** (2026-06-29 → 2026-07-29) — SKILL.md still ships the AND filter. GraphQL primary path stable this run (rc=0, 16 nodes). Sandbox: `gh api user --jq .login` returns 403 (GITHUB_TOKEN = `github-actions[bot]`) → author hardcoded to `aeonframework`. `>` shell redirect blocked to `/tmp/` and to allowed working dirs — solved by piping through `jq` inline instead of intermediate files (blocked in this run too — reconfirmed as structural sandbox behavior).

## Next expected transitions

- **koala73/worldmonitor#5477** — APPROVED day-7 today. Watch for `state: MERGED` in 07-30 scan; otherwise stale-clock rolls 2026-07-30.
- **koala73/worldmonitor#5518** — stale-clock rolls 2026-07-30.
- **jamiepine/voicebox#958** — stale-clock rolls 2026-07-30.
- **ruvnet/RuView#1409** — stale-clock rolls 2026-07-30 (no engagement, will pop straight to stale).
- **alibaba/open-code-review#541** — stale-clock rolls 2026-08-03.
- **cocoindex#2315** — merged, will roll off recent-merges table on 2026-08-02.
- **plano#1001** — merged, will roll off on 2026-08-03.
- **Agent-Reach#436 / openinterpreter#1810** — will roll off closed-no-merge table on 2026-08-03.
- **InsForge#1742** — will roll off closed-no-merge on 2026-08-02.
- **kage#66** — rolls off closed-no-merge on 2026-08-02.
- **Vibe-Trading#390** — rolls off recent-merges on 2026-08-04.
- **buzz#2248** — already stale; watch for close-no-merge or reactivation.

**Predicted 07-30 tuple:** `(2, 5, 3, 4)` if worldmonitor#5518 + worldmonitor#5477 + voicebox#958 + RuView#1409 all roll stale on schedule (buzz#2248 still stale = 5 total). Catalysts to watch: (a) worldmonitor#5477 merges before stale-clock → `(3, 4, 3, 4)`; (b) fresh bot PR files at median 1.5d cadence.
