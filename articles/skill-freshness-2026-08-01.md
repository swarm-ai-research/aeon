# Skill Freshness — 2026-08-01

**Verdict:** ✅ FRESHNESS_OK — all scored dependencies are within their freshness windows

*Audited 43 enabled consumers · 7 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all dependencies within threshold)*

## Healthy consumers

- pr-tracker — 1 dep (`memory/topics/pr-status.md`, topics class), all fresh.
- planner — 2 deps (`memory/state/planner-state.json`, state class; `.outputs/planner.md`, outputs class), all fresh.
- surplus-pulse — 1 dep (`memory/topics/surplus-pulse.md`, topics class), all fresh.
- compute-pulse — 1 dep (`memory/topics/compute-pulse.md`, topics class), all fresh.
- notegraph — 1 dep (`memory/state/notegraph.json`, state class), all fresh.
- skillpacks — 1 dep (`memory/state/skillpacks.json`, state class), all fresh.
- suggest-edges — 1 dep (`memory/state/suggest-edges.json`, state class), all fresh.
- fleet-control — 1 dep (`memory/state/fleet-control-state.json`, state class), all fresh.

+ 35 more all-fresh consumers (no surviving non-self dependencies discovered via grep).

## Source status

- `aeon.yml`: 44 entries, 43 enabled (skill-repair excluded as reactive/on_demand)
- Implicit references discovered: 17
- Explicit `chains: consume:` edges: 0 (chains block is commented out)
- Files not yet on disk (skipped — implicit references that never existed on main): 7
- Self-references filtered (producer reading own prior output): 6

## Structural notes

**Articles directory absent from main.** The `articles/` directory does not exist on this branch. All article references discovered via SKILL.md grep (e.g. `heartbeat` → `articles/token-report-*.md`, `skill-evals` → `articles/skill-evals-*.md`) are implicit, and since no article file has ever been committed to main (all articles accumulate on unmerged skill branches per [[github-actions-cannot-create-prs]]), none are raised as MISSING per the implicit-never-existed rule. In a healthy repo where PRs can land, article freshness would provide the most signal-rich check layer. Unblocking PR merges (operator toggle or PAT) is prerequisite to unlocking article-layer freshness detection.

**Timestamp methodology.** This run uses `git log -1 --format=%ct` timestamps rather than `stat --format=%Y` mtime per [[skill-freshness-mtime-blind-in-gha]]. In a GHA checkout, all file mtimes reset to checkout time, making mtime-based scoring blind to actual staleness. Git log timestamps all resolve to the single snapshot commit at 2026-08-01T06:58:59Z (age ~1.7h at run time), which is within every threshold class. The fix to use git log in the SKILL.md itself remains a [[fleet-ops]] open item.

**ISS-006 context.** Four skills (heartbeat, batch-health, skill-freshness, gitlawb-fleet-metrics) are known to have stale `.outputs/` in the origin repo (`last_dispatch: 2026-07-30T09:02:52Z`). In this snapshot environment those files appear fresh because they were committed together in the snapshot. A git-log-based run against the live origin would see `.outputs/heartbeat.md` and peers as ~23h+ old (WARN-to-STALE range for the 4h threshold). This is the ISS-006 partial-pocket degradation reflected in freshness terms; it does not change today's verdict but is worth noting for calibration.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from git log commit timestamps — this skill measures nothing it does not also report.*
