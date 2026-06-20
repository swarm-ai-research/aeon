# Plan — 2026-06-20

**Today's one thing:** Diagnose the fleet-wide zero-token failure. Every skill in `memory/cron-state.json` is at 100% failure with the same truncated error pattern (`"total_cost_usd":0,"input_tokens":0,"output_tokens":0`), and `skill-repair` is among the dead — so nothing in the fleet can self-heal until an operator pulls the runner logs and finds the root cause.

## Ranked

1. **Pull a real runner log and identify why every skill exits at zero tokens.** All `last_failed` timestamps cluster at 2026-06-20T01:50–01:53Z, suggesting a single batch sweep or a uniform harness-level failure (bad/expired API key, runner script aborting before invoking `claude`, or the status-writer incorrectly marking every run as `failed`). Start with `gh run view <id> --log` on one of the currently-queued runs, not the cron-state file — that file only shows symptoms. Manual operator action; nothing the fleet can do for itself right now.
2. **Confirm `skill-repair` is actually dead, not just gated.** It's at 161/161 failures, but per `aeon.yml` it's also reactive and supposed to handle `consecutive_failures >= 3`. If its workflow runs but no-ops, the wake-up wiring is broken; if it never fires, the trigger is broken. This is the difference between "fix one bug" and "fix two systems."
3. **Bootstrap missing memory scaffolding.** `memory/MEMORY.md`, `memory/issues/INDEX.md`, and `memory/state/` were absent at the start of this run (I just created `state/`). The planner spec assumes these exist for goals and stuck-task escalation. Once the runner is fixed, a single low-cost run that seeds `MEMORY.md` with current goals and opens an issue for the fleet outage would let every downstream skill resume with the context it expects.

## Holding / watching

- **All content/digest/triage/research work.** Pointless to dispatch anything until the runner returns non-zero tokens. Trigger to resume: one successful skill run in `cron-state.json` with `total_successes >= 1`.
- **Dispatching from this plan.** Mode is plan-only by design — `var` is empty, and a fleet-wide degradation must never cascade into a dispatch storm. Trigger to dispatch: operator re-runs planner with `var=dispatch` after the runner is confirmed healthy.
- **`agi-tracker` follow-ups from 2026-06-10.** The `generate-skills-json` newline bug and the 161-vs-173 skills.json drift noted in the last log are still real and unfiled; deferring until memory scaffolding exists so the issue has somewhere to live.

## Fleet note
- Red across the board: 38/38 tracked skills failing, 0% success rate, zero tokens consumed per run. This is not a degradation — it's an outage, and skill-repair is in it.

## Sources
- `memory/cron-state.json` (read)
- `memory/logs/2026-06-10.md` (only recent log; no entries 06-11 → 06-20)
- `memory/triaged-prs.json`, `memory/triaged-issues.json` (read)
- `aeon.yml` (enabled-skill list, planner spec)
- `gh pr list` / `gh issue list` — returned empty (queries ran, no open items)
- `gh run list` — current cron just queued ~38 runs at 06:06Z; will land in the same failure mode unless the runner is fixed
- `memory/MEMORY.md` — **absent** (no goals file to read; flagged above)
- `memory/state/planner-state.json` — **absent** (no prior plan to compare against; first run)
