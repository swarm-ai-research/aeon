# Plan — 2026-08-24

**Today's one thing:** merge PR #26 — the 15-day queue-merge blocker cleared overnight. `gh pr view 26` returns `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`, `updatedAt: 2026-08-24T01:08:19Z`, and all 5 checks (ShellCheck + 3 TypeScript + compute-futures tests) are SUCCESS. The single ShellCheck FAILURE that anchored this slot since 08-17 is gone — checks re-ran overnight (updatedAt jumped 08-17 → 08-24 01:08Z) and flipped green. Whether the `@dependabot rebase` comment landed or a workflow-file change on main invalidated the stale failure, the effect is the same: **this PR is a one-click merge from the operator now**, and clicking it proves the `app/github-actions` + `app/dependabot` merge path at ~432h+ since the last aeon-repo merge (#8, 2026-08-07T01:36Z).

## Ranked

1. **Merge PR #26** (streak 15 → 16, blocker resolved, one-click) — the entire 23-deep queue behind this (21 `app/github-actions` + 1 dependabot + 1 freebuff-web) has been waiting on the same proof-of-flow. Plan-only can't click merge; operator action needed. On merge, this slot renames from "escalation" to "queue drain" and rank-2 immediately gets a proven landing path.

2. **Open `agi-tracker: enabled: false` PR against `aeon.yml:188`** (streak 8 → 9) — **deadline is TODAY, Mon 2026-08-24T13:00Z (~5.5h out)**, the 8th silent-Mon fire. Should be opened regardless of rank-1 status — even if #26 sits in review for a beat, the agi-tracker PR can queue behind it and ride the freshly-proved path the moment it lands. If rank-1 clears in the next 5 hours, this rides in behind on the same merge motion. If it doesn't, the PR is at least authored before the 13:00Z window opens and the failure mode compresses from "silent no-op" to "silent no-op with pending fix in the queue".

3. **Patch `stale-content-pr-sweeper` SKILL.md** (streak 17 → 18) — add `"app/github-actions"` to `ALLOWED_AUTHORS` and align TRACKED prefixes per [[stale-content-pr-sweeper-tracked-prefix-drift]]. Today's 00:02Z operator-invocation swept 2 more (`#41` + `#44`) under applied intent — the second proof-of-concept run after 08-21's 5-close run. The live 5 chain PRs (`#42/#43/#45/#48/#49`, notegraph + suggest-edges) will keep growing net +1/day; a code-fix under a widened cron allowlist lets the daily cron do this without operator intent-application on each fire.

## Holding / watching

- **Populate `memory/watched-repos.md`** (streak-18 chronic) — no fresh same-day cluster fires yet today (Monday morning); most watched-repos-dependent skills fire Sun-only or Wed-only. Promote to top-3 when a same-day cluster hits 6/6 or when the queue-merge unblock frees a slot.
- **pr-tracker SKILL.md patch batch (a)–(k)** — 62d overdue. Item (e) fresh-bot-PR trigger got another exercise 08-23 when `deepsec#161` landed 5h after the daily scan and was structurally invisible to the anniversary-only predictor. Promote when today's or tomorrow's pr-tracker scan changes tuple state (breaks the fresh `(0, 9, 1, 1)` freeze).
- **docs/status.md snapshot-rebase gate** — 38d past urgency threshold; 26th consecutive rebase-clobber-then-regen as of 08-23 heartbeat. Promote when it becomes the top-3 slot's occupant.
- **ISS-006 messages.yml multi-pocket rewrite** — Day-22. Fix path viable; three regimes to model (coherent-late-pocket, decoupled-slow-slot, 06:30 gap). Reactive triggers still cover the P0 case.
- **swarm-repo app-perm gap** ([[aeon-app-no-write-on-swarm-repo]]) — Day-43. 59 pr-review + 40 pr-triage = 99 combined operator invocations with zero writes attempted. Promote if a swarm PR actually needs an autonomous write.
- **compute-futures `[[compute-futures-basket-synth-2.5x-multiplier]]`** — promoted at n=5 rename threshold via 08-23 reflect/memory-flush notes; watching for n=6 durability on today's or tomorrow's 08-23 CSV run.
- **milestone-tracker Mon 2026-08-24T12:00Z fire (~4h out)** — ms-01 stalled-6, ms-02 47/50 (agi-tracker `enabled: false` pulls ms-02 → 46/50, opposite direction). Watching, not acting.
- **cost-report Mon 2026-08-24T07:00Z** — fired ~36 min ago; watching for whether last week's $396.85 / +50.8% WoW spike sustains.
- **Notegraph fingerprint-pipeline sandbox friction n=2** — flagged for reflect to promote to `[[notegraph-fingerprint-pipeline-blocked-by-sandbox]]` at n≥3.

## Fleet note

Fleet: 0 broken · 0 in-flight · 0 failed (**5th consecutive clean morning**: 00:02Z sweeper closed 2 stale, 05:38Z suggest-edges PR #49 open, 05:40Z notegraph PR #48 open with +5 notes wired in, 06:25Z memory-structural-dedupe, 06:32Z memory-flush, 06:33Z compute-futures-eda success) · 38 DEGRADED (ISS-001 Day-66 residue, all `last_status: success` + `cf: 0`) · 4 truly healthy · 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard`, **48th silent day**) · 17 open issues (INDEX.md unchanged since 08-22) · **23 open aeon PRs** (21 `app/github-actions` + 1 dependabot + 1 freebuff-web) · 0 open GH issues.
