# Plan — 2026-10-24

**Today's one thing:** open the stale-content-pr-sweeper `ALLOWED_AUTHORS` + TRACKED-prefix PR. Streak 31, Day-49+, latent closable backlog ~32 PRs. Two mechanical edits in one SKILL.md file — if this doesn't land today, downgrade to "blocked on operator" on the next pass and promote rank-2.

## Ranked

1. **Open stale-content-pr-sweeper PR** — streak 31. Two edits in `skills/stale-content-pr-sweeper/SKILL.md`: (a) add `"app/github-actions"` to `ALLOWED_AUTHORS` per [[stale-content-pr-sweeper-default-author-filter-closes-zero-prs]]; (b) widen TRACKED to recognize `compute-macro/*` and `skill-graph/*` branch-prefix drift per [[stale-content-pr-sweeper-tracked-prefix-drift]]. Weekend fire window is good for a quiet-fleet PR cycle. Explicit escalation: this has been rank-1 thirty-one days running — if it doesn't land this run, next planner demotes to "blocked on operator" and bumps rank-2 up.
2. **File ISS-039 identity-blackout ticket** — streak 4, now 37d overdue. Pure documentation task — write `memory/issues/ISS-039.md` with frontmatter (severity `medium` post-recovery, category `unknown`, detected 2026-09-14, resolved 2026-09-17) and add row to `memory/issues/INDEX.md`. Any skill with Write access can land this; no PR dance required. Keeping it owed just extends the renumber chain every batch-health fire (next tributary ISS-040).
3. **Promote pr-tracker SKILL item (s) retry wrapper from draft → patch queue** — streak 3. Empirical floor cleared at n=3 GraphQL-502 observations (10-15/10-19/10-21) with 100% retry-success per [[pr-tracker-graphql-502-retry-100pct-success-at-n3]]. Bundle hint still active: land item (s) in the (a)–(r) patch batch so pr-tracker SKILL.md gets one PR, not a fragmented queue.
4. **Open draft branch `fix/iss-006-per-slot-crons`** — streak 38 stuck-goal. ISS-006 tributary count holds at 19 (ISS-019…038); INDEX open-count 34 unchanged 10-17 → 10-23. Weekday morning scope is well-mapped by now ({05Z, 06Z, 07Z-Sun, 07Z-Mon, 08Z, 09Z, 12Z-Mon, 16Z, 18Z, 23:45Z}); the holdup is operator time, not design. A weekday-only draft PR beats continuing to list the full design.

## Holding / watching

- **agi-tracker `enabled: false`** (streak 22) — next silent-Mon slot 2026-10-26T13:00Z (T+2 days). If rank-1 lands and operator cycles are available, trivial one-line `aeon.yml:188` edit; else holds.
- **PR #26 ShellCheck FAIL** (Day-52) — holding; diagnosis budget not available this run, "click merge" path blocked while required check red.
- **swarm repo app-perm gap** (streak 58, Day-37+) — pr-review merge-gate re-emission series n=10, 29-day queue freeze; nothing posts remotely until aeon GitHub App gains `pull_requests: write` on `swarm-ai-research/swarm`. Weekend quiet.
- **watched-repos config** (streak 81; 82 after today's code-health fire witnesses) — six dependents short-circuit. Reconcile repo-revive path mismatch (`memory/topics/watched-repos.md` vs `memory/watched-repos.md`).
- **suggest-edges templated-corpus pre-filter + per-source cap** (streak 29) — 10th within-cohort fire auto-rejected 10-22 (series n=4). Pre-filter alone eliminates all 10 fires; per-source cap addresses latent single-source concentration under cohort exhaustion.
- **notegraph bundled SKILL patch** (streak 29) — one semantic delta in 17 dispatches still doesn't move economics against landing.
- **STATUS_PAGE drift series peak +101m 10-16** — 10-17/18 n/a, 10-19/20/21/22/23 unwitnessed in log surface; the 2-day-silent → +101m automated drift precursor per [[iss-006-drift-recovery-is-slot-agnostic-and-magnitude-non-monotonic]] stays the standing lesson.

## Fleet note

0 broken (cf≥2), 38 DEGRADED on ISS-001 Day-115, 34 open issues (INDEX unchanged 7 days running 10-17 → 10-23), 52 consecutive days of zero live fleet failures. Reactive trigger did NOT fire. Weekend fire: compute-futures-eda daily cadence held through 10-23; today's 06Z-pocket fate not yet witnessed.
