# Plan — 2026-08-22

**Today's one thing:** Comment `@dependabot rebase` on PR #26 (or close + let dependabot re-open) — the ShellCheck FAILURE is stale, not substantive. `tmp-skill-graph/fingerprint.sh` (the file that trips `SC2164` on `Lint`/ShellCheck job `95256043957`) exists on PR #26's head tree but was deleted from `main` between when dependabot opened the PR and now, so a rebase will drop the offending file and every check should pass.

## Ranked

1. **Rebase PR #26 to clear the stale ShellCheck failure** — day-15 of the merge-flow-proof stuck goal, day-5 at the same escalated rank-1. Yesterday's planner isolated the single ShellCheck failure on workflow `Lint` (job `95256043957`, completed 2026-08-17T01:09:55Z) as the specific merge blocker. Today's escalation: I probed `git/trees` on both refs — `tmp-skill-graph/{fingerprint.sh, build-graph.mjs, debug*.mjs, result.json, skill-graph.md}` is present on PR #26 head (`2eeed9b`) but absent from `main`. The failing lint doesn't reflect anything the PR changes; it reflects a directory that was removed from `main` after this dependabot PR was created. Action is a one-liner: `gh pr comment 26 -b "@dependabot rebase"` (or `gh pr close 26 --delete-branch` — dependabot will re-open cleanly against fresh main). Serves the merge-flow-proof goal directly; if the rebase clears checks and merges, we finally have the textbook `app/github-actions` proof at ~370h+ silence.

2. **Land `enabled: false` on `aeon.yml:188` for `agi-tracker` via PR** — streak 6 → 7. **Deadline now 2 days out** (next silent-Mon fire 2026-08-24T13:00Z). This depends on rank-1 being cleared: without a working `app/github-actions` merge path, a PR opened today can't auto-merge by Mon. If rank-1 clears today (rebase wins), open the `enabled: false` PR immediately so it can ride the same fresh merge policy. Alt: restore/author `skills/agi-tracker/SKILL.md` matching the [[agi-tracker]] weekly frontier-agent scoring shape — higher-value but slower; the toggle is the deadline-safe move.

3. **Patch `stale-content-pr-sweeper` — `ALLOWED_AUTHORS` + TRACKED prefix aliases** — streak 15 → 16. 08-21 operator-invocation proof-of-concept closed 5 stale PRs when the intent was applied manually. Currently open under the same class: 3 notegraph (#39/#41/#43), 4 suggest-edges (#38/#40/#42/#44) — a patched sweeper would close ~5–6 of these superseded PRs the next weekly run without touching #26 (merge target) or the human-review PRs. Two-part patch: (a) add `"app/github-actions"` (or a broader bot-authored allowlist) to `ALLOWED_AUTHORS`; (b) fix TRACKED-prefix drift per [[stale-content-pr-sweeper-tracked-prefix-drift]] so `compute-macro/*` and `skill-graph/*` prefixes resolve to their skill names.

## Holding / watching

- **Populate `memory/watched-repos.md` OR disable the 6 dependent skills** — streak 17 chronic; 6 healthy-looking silent short-circuits per day. Trigger to promote: a same-day cluster of 4+ short-circuits (currently oscillating 3–4/day) or an operator green-light on the binary choice (populate vs disable).
- **`pr-tracker` patch batch (a–k)** — 59d overdue. Promote if `pr-tracker` produces a fourth consecutive identical-tuple day (currently at 3) or an operator ask; queue-level `notify` hash-dedup is masking day-to-day urgency but the SKILL-level guard is still the fix.
- **`docs/status.md` snapshot-rebase gate** — 36d past urgency; 24th consecutive clobber-regen. Promote if any status-page reader downstream (dashboards, digests) starts breaking, or if regen minutes measurably eat into the heartbeat budget.
- **ISS-006 pocket-slot cron rewrite** — Day-20. Today (even DOM 22, Saturday) expects 4 skills in 06:00–07:30Z (planner + compute-futures-eda + memory-flush + memory-structural-dedupe); batch-health will confirm shape. Promote if today's batch fails to land the expected 4, else keep in fix-viable-not-urgent state.
- **`suggest-edges` templated-corpus pre-filter** — day-14 recurrence with #44 today (5 consecutive PR-opening days on the same cluster). Promote once rank-1 clears and merge-flow proves; otherwise it's just another PR that can't merge.
- **`skill-repair` reactive at `consecutive_failures ≥ 3`** — not covered here (by design); watching only.

## Fleet note

Green surface. **0 broken · 0 hard-failed · 0 in-flight · 38 degraded** (chronic ISS-001 Day-64 residue — all `last_status: success`, `consecutive_failures: 0`) · **4 truly healthy** (`agi-tracker` HEALTHY-but-empty, `config-validator`, `swarm-safety-eval`, `weekly-shiplog`) · **2 NO_DATA** (`ai-framework-watch` + `run-frequency-guard`, **46th silent day**) · **18 open issues** · **24 open aeon PRs** (net +1 overnight: 23 → +#43/#44 opens, no closes) · **0 open GH issues**. Third consecutive clean morning.

## Source footer

Read: `memory/MEMORY.md` (65 lines, index-shape) · `memory/state/planner-state.json` (last_run 2026-08-21T06:30:00Z, top_priority `aeon-repo-queue-merge-escalation` streak-13, 9 tracked streaks) · `memory/cron-state.json` (42 tracked skills) · last 2 days of `memory/logs/` (08-21 full 380 lines + 08-22 through memory-flush) · `memory/issues/INDEX.md` (18 open + 2 resolved) · `gh pr list --state open` (24 rows) · `gh pr view 26 --json statusCheckRollup` (4/5 SUCCESS + 1 ShellCheck FAILURE, unchanged from 08-17) · `gh api repos/.../git/trees/{main,PR26 head}` (tmp-skill-graph/ present on PR26 head, absent on main — new signal). `soul/` absent → clear-direct first-person. `${var}` empty → plan-only, no dispatch.
