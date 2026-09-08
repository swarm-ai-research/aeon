# Plan — 2026-09-08

**Today's one thing:** Land the single bundled PR that adds `articles/.gitkeep` and flips `agi-tracker` to `enabled: false` at `aeon.yml:188`. Same rank-1 as 2026-09-07 — didn't land yesterday, so it carries into streak-2. This is the highest single-change leverage on the queue: cascade-closes 13 open `no_file_match` ISS tickets (ISS-002/005/008–018) once the next `skill-evals` scan confirms same-day file-match, AND kills the 11th silent-Mon fire before 2026-09-14T13:00Z.

## Ranked

1. **`articles/.gitkeep` + `agi-tracker: enabled: false` bundled PR** — cascade-closes 13 ISS + prevents 11th silent-Mon (Day-7 to next fire). Streak-2 (was streak-1 yesterday, no movement). Concrete unblock: open one PR from `fix/articles-gitkeep-agi-tracker-disable` with two file changes; branch is trivial. Serves `articles-dir-never-existed-in-git-history` + `agi-tracker-missing-skill-md-dispatches-no-op`. No skill dispatches this — it's an operator PR.
2. **ISS-006 status escalation `investigating → fixing` + interim slot migration** — 09-06 heartbeat surfaced Saturday 11Z + Sunday 06:30Z as new dead pockets outside the tracked 06:00Z weekday zone, both n=2 consecutive weeks. That widens the fix scope. Two concrete moves today: (a) edit `memory/issues/ISS-006.md` frontmatter `status: investigating → fixing` and note the weekend-pocket extension in the body; (b) migrate `planner` (`30 6 * * *`) and `compute-futures-eda` (`0 6 * * *`) in `aeon.yml` to a known-alive slot (proposed 07:30Z, adjacent to today's confirmed-alive 07:00Z pocket) until per-slot `messages.yml` cron rewrite lands. Interim mitigation only — the full rewrite covering coherent-late-pocket + decoupled-slow-slot + persistent-06:30Z-gap + Sat-11Z + Sun-06:30Z regimes stays queued behind this.
3. **Click merge on PR #26 OR install repo auto-merge policy for `dependabot` + `app/github-actions`** — Day-32 durability. Verified state:OPEN, updatedAt `2026-09-07T01:09:31Z` (no movement in ~26h). REST returns `mergeable: UNKNOWN` per known `gh-pr-view-mergestate-returns-unknown-after-graph-mutation`; last authoritative snapshot 5/5 CI SUCCESS. Prior top (streak-21 before demotion 09-07) — carrying streak-22 at rank-3 today. This is the load-bearing merge-flow proof for the aeon-repo queue.

## Holding / watching

- **watched-repos populate/disable** — streak-37, 6 dependents chronically no-op'd (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive). Trigger to unhold: ISS-006 status moves to `fixing` (rank-2 today satisfies).
- **pr-tracker SKILL.md patch batch (a)–(o)** — streak-68. 09-05 tuple `(1, 9, 1, 7)` was worst-in-series, root cause was scan-cadence break not model drift, so the code fix is not the emergency. Trigger to unhold: PR #26 lands (rank-3 today satisfies).
- **notegraph PR #61** — opened 09-05, 361n/2871h post-09-07 reflect run. Not blocked; watching.
- **workflow-security-audit PR #63** — opened 09-06, 153 findings. Rank-1's PR-flow proof pattern applies; wait for PR #26 to prove the auto-merge shape, then this becomes the second follow-through.
- **skill-repair** — nothing at `consecutive_failures >= 3`, so it stays quiet. Noted so we don't duplicate reactive coverage.
- **swarm-safety-eval ISS-005 close** — deferred; not touched by planner per detector-ownership convention.
- **ISS-001 residue close** — Day-82; deferred per action-queue rule until ISS-006 resolves.

## Fleet note

0 broken · 0 in-flight · 0 hard-failed · 38 DEGRADED (ISS-001 OAuth-denominator residue Day-82, hash `e27c0ac60367e7e5` on 69th steady-state day) · 4 HEALTHY · 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard`, never-dispatched Day-62). 21 open ISS (ISS-024 filed 09-06 for the 4th 48h-cadence batch outage). Both `gh` queries responded (26 open PRs; 0 open issues); PR #26 verified OPEN with 09-07 01:09Z timestamp unchanged.

## Sources

- Read: `memory/MEMORY.md`, `memory/cron-state.json`, `memory/issues/INDEX.md`, `memory/logs/2026-09-07.md`, `memory/logs/2026-09-06.md`, `memory/state/planner-state.json`.
- External: `gh pr list` OK (26 open), `gh issue list` OK (0 open), `gh pr view 26` OK (state:OPEN, updatedAt 2026-09-07T01:09:31Z).
- Soul: absent (`soul/` directory does not exist) — voice defaulted to first-person direct.
- Mode: `${var}` empty → plan-only; no dispatch. Reactive trigger did not fire (0 skills at `consecutive_failures >= 2`).
