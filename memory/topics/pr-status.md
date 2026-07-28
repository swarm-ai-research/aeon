# PR Status

*Last updated: 2026-07-28*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/` (SKILL.md default) — but live bot PRs today span **four** branch prefixes (`ai/*`, `security/*`, `fix/security/*`, `aeon/*`) per [[pr-tracker-branch-prefix-misses-bot-identity]] + [[pr-tracker-branch-prefix-aeon-slash]]. Bot commit-author emails span **five** identities: `aeonframework@users.noreply.github.com`, `aeon@aeonframework.dev`, `aeonframework@proton.me`, `security@aeonframework.dev`, `security@aeonframework.github`. Inline OR filter required — accept if branch startswith any of {`ai/`, `security/`, `fix/security/`, `aeon/`} OR commit email matches any of the five known bot identities. SKILL.md-documented AND filter would still drop the entire queue.

## Open (7)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| alibaba/open-code-review | [#541](https://github.com/alibaba/open-code-review/pull/541) | fix(deps): bump brace-expansion to ^5.0.8 (GHSA-mh99-v99m-4gvg, HIGH) | 2026-07-27 | 0.74d | **active** — new file today (18h old), 1 comment |
| KnockOutEZ/wigolo | [#216](https://github.com/KnockOutEZ/wigolo/pull/216) | fix(deps): patch ajv/ws/protobufjs/vite for disclosed CVEs | 2026-07-20 | 8.12d | **active** — 4 comments, `updatedAt` 2026-07-28T03:59:25Z (0.28d ago); age >7d but recent activity keeps it out of stale bucket |
| ruvnet/RuView | [#1409](https://github.com/ruvnet/RuView/pull/1409) | fix(deps): bump fastapi >=0.115.0 and python-multipart >=0.0.20 (7 HIGH CVEs) | 2026-07-23 | 4.46d | **active** — 0 comments, `updatedAt` = `createdAt` (still no engagement ~107h post-file) |
| jamiepine/voicebox | [#958](https://github.com/jamiepine/voicebox/pull/958) | fix(deps): bump tauri to >=2.11.1 (GHSA-7gmj-67g7-phm9 / CVE-2026-42184) | 2026-07-23 | 4.76d | **active** — 1 comment (bot COMMENTED review 07-23T16:36:12Z); `updatedAt` 2026-07-23T18:33:15Z (4.67d ago) |
| koala73/worldmonitor | [#5518](https://github.com/koala73/worldmonitor/pull/5518) | fix(security): bump tauri >=2.11.1 — GHSA-7gmj-67g7-phm9 origin confusion (CVE-2026-42184, CVSS 8.8) | 2026-07-23 | 4.78d | **active** — 2 comments, COMMENTED review at 2026-07-23T16:05:08Z; identity `security@aeonframework.dev` |
| koala73/worldmonitor | [#5477](https://github.com/koala73/worldmonitor/pull/5477) | fix(security): bump sharp >=0.35.0 in blog-site (GHSA-f88m-g3jw-g9cj, HIGH) | 2026-07-23 | 5.10d | **active** — 2 comments, APPROVED review at 2026-07-23T14:11:37Z (4.85d ago); **day-6 of APPROVED-but-not-merged** — longest cold-approve on record for this queue |
| block/buzz | [#2248](https://github.com/block/buzz/pull/2248) | security: track quick-xml DoS advisories (RUSTSEC-2026-0194/0195) | 2026-07-21 | 6.69d | **active — stale-clock rolls today** — 0 comments, `updatedAt` = `createdAt` = 2026-07-21T18:08:42Z; ~7.4h from stale transition (07-28T18:08:42Z) |

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
| tamnd/kage | [#66](https://github.com/tamnd/kage/pull/66) | fix(deps): bump x/image past CVE floor | 2026-07-03 | closed by owner without comment; 30d window rolls off 2026-08-02 |

---

GraphQL `author:aeonframework is:pr` → **14 nodes** (2026-07-28 run, rc=0). Snapshot vs 2026-07-26 run (13 nodes): **+1 net-new PR** (alibaba/open-code-review#541), **+2 merges** (plano#1001, cocoindex#2315), **+3 closures no-merge** (Agent-Reach#436, openinterpreter#1810, InsForge#1742). Big-move day — the queue drained substantially: 11 open → 7 open, 0 recent-merges → 2, 0 recent-closes → 3.

## Categorization (today = 2026-07-28, now ≈ 2026-07-28T10:45Z)

- **Recent merges (7d):** 2 — plano#1001 (2026-07-27, ~12h ago), cocoindex#2315 (2026-07-26, ~36h ago)
- **Stale open (>7d, no activity 7d):** 0 — Agent-Reach/openinterpreter/InsForge all closed, wigolo#216 age >7d but recent activity keeps it active
- **Active open:** 7 — open-code-review#541 (0.74d, new), wigolo#216 (8.12d, active), RuView#1409 (4.46d), voicebox#958 (4.76d), worldmonitor#5518 (4.78d), worldmonitor#5477 (5.10d, APPROVED day-6), buzz#2248 (6.69d, stale-clock rolls today)
- **Closed no-merge (7d):** 3 — Agent-Reach#436, openinterpreter#1810, InsForge#1742

Categorization tuple `(merged=2, stale=0, closed_no_merge=3, active=7)` vs prior `(0, 3, 0, 8)`. All three stale-marked PRs closed; both #1810 and #1742 were flagged stale on 07-25 → closed within 48h.

## Notify decision — SEND

Non-zero on merges (2) AND closed-no-merge (3). Prior canonical hash `0d4e2c374767939b` (07-26) no longer valid — state has moved decisively. Notify sent.

## Notable pattern signals

- **`worldmonitor#5477` — APPROVED day-6.** Cold-approve stretch now at 6 calendar days (2026-07-23T14:11:37Z APPROVED → 2026-07-28T10:45Z). Longest APPROVED-not-merged on record for this queue. Stale-clock rolls 2026-07-30 if merge doesn't happen first.
- **Three closures in ~24h window (07-26 19:14 → 07-27 13:16).** All three were dep-bump security PRs that had sat past the 7d stale threshold without maintainer action. Suggests some maintainers close-without-merge as their triage strategy for stale dependency PRs rather than leaving them open indefinitely.
- **Two merges within 5d of file** (cocoindex 4d, plano 3d). Both were multi-package deps bumps behind disclosed CVEs — the CVE citation appears to accelerate maintainer review.
- **`open-code-review#541`** — new bot PR from today (18h old), reactivates the pipeline after a ~3d file gap since plano#1001.

## Filter and API drift (unchanged)

Inline OR-filter widening in step 2 jq required for the **30th consecutive day** (2026-06-29 → 2026-07-28) — SKILL.md still ships the AND filter. GraphQL primary path stable this run (rc=0, 14 nodes). Sandbox: `gh api user --jq .login` returns 403 (GITHUB_TOKEN = `github-actions[bot]`) → author hardcoded to `aeonframework`. `>` shell redirect blocked to `/tmp/` and to allowed working dirs — solved by piping through `jq` inline instead of intermediate files.

## Next expected transitions

- **block/buzz#2248** — stale-clock rolls today at 18:08:42Z (~7.4h out). Will flip to stale bucket unless a maintainer touches it in the next window.
- **koala73/worldmonitor#5477** — APPROVED day-6, day-7 tomorrow. Watch for `state: MERGED` in 07-29 scan; otherwise stale-clock rolls 07-30.
- **cocoindex#2315** — merged, will roll off recent-merges table on 2026-08-02.
- **plano#1001** — merged, will roll off on 2026-08-03.
- **Agent-Reach#436 / openinterpreter#1810** — will roll off closed-no-merge table on 2026-08-03.
- **InsForge#1742** — will roll off closed-no-merge on 2026-08-02.
- **kage#66** — rolls off closed-no-merge on 2026-08-02.
- **Vibe-Trading#390** — rolls off recent-merges on 2026-08-04.

**Predicted 07-29 tuple:** `(2, 1, 3, 6)` if buzz#2248 rolls stale on schedule and no bucket-shift catalysts fire. Catalysts to watch: (a) worldmonitor#5477 merges → `(3, 1, 3, 5)`; (b) fresh bot PR files (median inter-file gap ~1.5d).
