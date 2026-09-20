# Plan — 2026-09-20

**Today's one thing:** Land `enabled: false` on `aeon.yml:188` for `agi-tracker` — the 12th silent-Monday fires **tomorrow** (2026-09-21T13:00Z, T-1) if I don't ship a one-line PR today.

## Ranked

1. **agi-tracker: `enabled: false` PR (or restore `skills/agi-tracker/SKILL.md`)** — T-1 to the 12th consecutive silent-Mon dispatch. The workflow has fired eleven times against a missing skill directory, produced no output, and burned a dispatch slot each time per [[agi-tracker-missing-skill-md-dispatches-no-op]]. Priority-streak 16 without action; that's a stuck goal — escalate today rather than restate. One-line PR is the cheapest fix; author `SKILL.md` if we still want the signal. This maps to no runnable skill in the fleet (it's a repo edit), so plan-only mode will emit the PR by hand on the next opportunity.

2. **ISS-006 messages.yml multi-pocket rewrite (streak-32, stuck-goal escalated)** — Today (Sun DOM=20 even) is the predicted weekend-compounded batch-outage slot. Planner itself just fired inside/near the 06:30Z pocket, so we have live evidence one way or the other; batch-health will resolve at 08:00Z scheduled (likely ~09:30Z coherent-late-pocket). If the 4-skill tuple `{planner, memory-flush, memory-structural-dedupe, compute-futures-eda}` misses, that's ISS-006 tributary #10 and the case for the rewrite hardens further. Serve this by drafting the per-slot cron rewrite in a branch (multi-pocket model: coherent-late-pocket, decoupled-slow-slot, dead-06:00Z, dead-06:30Z Sun, dead-08:00Z widening) — 10 tributaries is enough evidence; a 33rd priority-streak day without a branch is the actual bottleneck now.

3. **PR #26 ShellCheck FAIL diagnose + patch (Day-42)** — Regression from 5/5 SUCCESS to 4/5 UNSTABLE after the 2026-09-14T01:07:51Z dependabot force-rebase. The "click-merge" path per [[pr-creation-toggle-is-distinct-from-merge-capability]] is stale until ShellCheck is green. Pull the failing check log, patch, push. Small, unblocks a merge that's otherwise ready.

## Holding / watching

- **pr-tracker patch batch (a)–(q)** — streak-69 and 80d overdue. Held today because agi-tracker is time-critical and the pr-tracker patch is a larger multi-item edit. Trigger to move: any pr-tracker slot fires and the §5 all-zero notify rule quiets a real signal again.
- **watched-repos config populate-or-disable (streak-49)** — held pending operator input on which 6 dependents to keep; unilaterally seeding the file races that decision. Trigger: operator names a repo list, or authorizes bulk-disable.
- **stale-content-pr-sweeper allow-list patch** — held; the ~19 stale content PRs (notegraph/, suggest-edges/, skill-graph/, compute-macro/) are noise, not risk. Trigger: operator asks for a queue clean-up or the queue exceeds 50.
- **ISS-001 close** — deferred until ISS-006 stabilizes per MEMORY.md. Not touching.
- **swarm PR queue** — 4th consecutive full-skip cycle at n=3 dedup saturation; only exogenous events (operator click-merge, force-push, new PR) can turn it over. Nothing to do until then.

## Fleet note

0 broken (cf≥2), 38 DEGRADED (ISS-001 residue Day-91, all `last_status=success`), 4 HEALTHY, 2 NO_DATA (ai-framework-watch + run-frequency-guard, Day-67 never-dispatched). Notable stales: skill-repair 86d (reactive; only wakes on cf≥3, so silence is correct), agi-tracker 13d + 11 silent Mons (item #1 above), memory-flush/memory-structural-dedupe 12d (ISS-006 06:00Z pocket), skillpacks/compute-macro-correlate 28d (weekly-Sun 06:00–06:30Z pocket, weekend-compounded regime).

## Source footer

- Read: `memory/MEMORY.md`, `memory/state/planner-state.json`, `memory/logs/2026-09-19.md`, `memory/logs/2026-09-18.md`, `memory/issues/INDEX.md`, `memory/cron-state.json` (42 skills).
- `gh pr list` responded — 31 open PRs on this repo, dominated by `notegraph/*` + `suggest-edges/*` + `skill-graph/*` cohorts. Head: #73.
- `gh issue list` was not re-queried this run — MEMORY.md action queue is the authoritative issue-shaped state.
- Soul directory absent → default first-person direct voice.
