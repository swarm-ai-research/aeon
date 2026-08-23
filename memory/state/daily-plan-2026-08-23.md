# Plan — 2026-08-23

**Today's one thing:** post `gh pr comment 26 -b "@dependabot rebase"` on PR #26 — day-6 stuck-goal escalation. The single ShellCheck FAILURE (SC2164 on `tmp-skill-graph/fingerprint.sh` line 2, job `95256043957`, 2026-08-17T01:09:55Z) is still stale: `tmp-skill-graph/` was removed from main after PR #26 was created, but PR #26's head still carries it. A rebase drops the file, checks clear, and #26 becomes the textbook `app/github-actions`+`app/dependabot` merge-flow proof at ~389h+ since last aeon-repo merge (#8, 2026-08-07T01:36Z). Zero movement overnight — status rollup on #26 byte-identical to 08-21/08-22 snapshots.

## Ranked

1. **Comment `@dependabot rebase` on PR #26** (streak 14 → 15, day-6 escalation) — one-liner from the operator or a dispatched runner. Blocks rank-2 and the entire 25-deep queue. Path collapse held: this is now literally a single `gh pr comment` call; no diagnosis remains. Fallback: `gh pr close 26 --delete-branch` and dependabot re-opens against fresh main.

2. **Open `agi-tracker: enabled: false` PR against `aeon.yml:188`** (streak 7 → 8) — deadline is **tomorrow, Mon 2026-08-24T13:00Z** (8th silent-Mon fire). Depends on rank-1 clearing so the PR can ride the same freshly-proved merge path. If rank-1 doesn't clear today, the PR sits in the queue for the 24th consecutive `app/github-actions`-authored PR with no merge — the deadline slips into the "already been silent 8 weeks" bucket. Alt path (restore `skills/agi-tracker/SKILL.md`) is higher-friction and doesn't unblock the queue.

3. **Patch `stale-content-pr-sweeper` SKILL.md** (streak 16 → 17) — add `"app/github-actions"` to `ALLOWED_AUTHORS` and align TRACKED prefixes per [[stale-content-pr-sweeper-tracked-prefix-drift]]. Under a patched allowlist, today's 5 open notegraph/suggest-edges chain PRs (#38/#40/#42/#43/#44) become sweep candidates on the next daily fire. 08-21 operator-invocation already proved the SKILL works when the allowlist is widened (5 PRs closed). Rebuild-safe against rank-1 status; can land in parallel.

## Holding / watching

- **Populate `memory/watched-repos.md`** (streak-18 chronic) — 6 skills silently no-op every fire; today's 09:00Z cluster will extend by another 3. Promote when the queue-merge unblock lands or when a same-day cluster hits 6/6.
- **pr-tracker SKILL.md patch batch (a)–(k)** — 60d overdue as of 2026-08-23. Queue-level `notify` hash-dedup partially masks item (d), but the underlying identical `.pending-notify/` writes and log churn still happen. Promote when today's or tomorrow's pr-tracker scan changes tuple state (breaks the current 3-day `(0, 9, 1, 0)` freeze).
- **docs/status.md snapshot-rebase gate** — 37d past urgency threshold; 08-22 heartbeat regenerated wholesale for the 25th consecutive time. Promote when it becomes the top-3 slot's occupant (currently blocked by higher-severity queue items).
- **ISS-006 messages.yml multi-pocket rewrite** — Day-21. Fix path viable; merge path pending durability from rank-1. Reactive triggers (`skill-repair` for `cf ≥ 3`) still cover the P0 case.
- **swarm-repo app-perm gap** ([[aeon-app-no-write-on-swarm-repo]]) — Day-42. 57 pr-review + 40 pr-triage = 97 combined operator invocations with zero writes attempted; gap remains unexercised. Promote if a swarm PR actually needs an autonomous write.
- **compute-futures 2.5000× multiplier at n=5 — rename threshold hit** — per [[compute-futures-multiplier-invalidated-at-n-7]] cadence, today's 08-22 CSV pushed n=4 → n=5 (rename threshold). Promote to a class-anchor atomic note `[[compute-futures-basket-synth-2.5x-multiplier]]` in tomorrow's reflect pass, not a planner top-3 item.
- **milestone-tracker Mon 2026-08-24T12:00Z fire** — ms-01 stalled-6, ms-02 47/50 (agi-tracker `enabled: false` would pull ms-02 to 46/50). Watching, not acting.
- **cost-report Mon 2026-08-24T07:00Z fire** — last week $396.85 / +50.8% WoW; watching for whether notegraph/pr-review/sweeper spike sustains.

## Fleet note

Fleet: 0 broken, 0 in-flight (4th consecutive clean morning after today's notegraph silent-no-change + suggest-edges/compute-futures-eda successes), 38 DEGRADED (ISS-001 Day-65 chronic residue, all `last_status: success` + `cf: 0`), 4 truly healthy, 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard`, 47th silent day). 25 open aeon-repo PRs. 0 open GH issues. 17 open ISS (INDEX unchanged since 08-22).
