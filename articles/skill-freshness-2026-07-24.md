# Skill Freshness — 2026-07-24

**Verdict:** ✅ FRESHNESS_OK — all reachable cross-skill dependencies are within freshness thresholds

*Audited 44 enabled skills · 10 cross-skill dependencies discovered · 0 flagged*

## Flagged dependencies

*(None — every discovered dependency is either within its freshness window, sourced from a disabled/on-demand producer (implicit skip), or an implicit reference to a file that has never existed on disk (not flagged per policy).)*

## What this means per consumer

All enabled consumers are operating with fresh or gracefully-absent upstream data. No staleness action is required.

Three structural notes surfaced during this run (informational only — not freshness flags):

> **vuln-scanner** — reads `.outputs/github-trending.md` as an optional auto-select source. The file is absent because `github-trending` is `enabled: false` (on-demand cadence). `vuln-scanner` degrades gracefully with `if [ -s .outputs/github-trending.md ]`. Not a freshness violation; no action unless the operator wants trending-assisted targeting.

> **heartbeat / weekly-shiplog** — reference `articles/token-report-*.md` and `articles/push-recap-*.md` respectively. Both producers are disabled; the `articles/` directory does not yet exist on disk. Both consumers handle absence gracefully (heartbeat omits the Token Pulse section; weekly-shiplog skips the push-recap context pass). Not flagged.

> **repo-revive, pr-review, surplus-pulse, compute-pulse** — reference operator-configured files (`memory/topics/watched-repos.md`, `memory/topics/pr-review-rules.md`, `memory/topics/projects.md`, `memory/topics/compute-tokens.md`) that have never been created. These are implicit references to files that simply never existed; policy excludes them from MISSING scoring. All four skills degrade gracefully on cold-start.

## Healthy consumers

- planner — 0 checkable cross-skill deps, all fresh.
- heartbeat — 0 checkable cross-skill deps (token-report disabled, articles/ absent), all fresh.
- skill-health — 0 checkable cross-skill deps, all fresh.
- reflect — 0 checkable cross-skill deps (articles/ absent, directory-scan reference skipped), all fresh.
- vuln-scanner — 0 checkable cross-skill deps (github-trending disabled, .outputs file absent), all fresh.
- compute-futures-eda — 0 checkable cross-skill deps, all fresh.
- goal-tracker — 0 checkable cross-skill deps, all fresh.
- skill-freshness — 0 checkable cross-skill deps (own state file is a self-read, filtered), all fresh.
+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 130+ skill entries, 44 enabled (on_demand/reactive skills excluded from consumer audit)
- Implicit cross-skill references discovered: 10
- Explicit `chains: consume:` edges: 0 (all chains currently commented out in `aeon.yml`)
- Files not yet on disk (skipped — implicit references that never existed or from disabled/on-demand producers): 10

### Notes on this run

- **`articles/` directory absent** — no enabled daily or weekly producer's article was expected as an explicit canonical dependency today. Created the directory as a side-effect of writing this report.
- **Single-commit repo** — git log timestamps (`git log -1 --format=%ct`) are uniform across all files (2026-07-24 07:26:04 UTC, ~2h before this run). All thresholds: `.outputs/` 4h, `memory/topics/` 7d, `memory/state/` 30d — every extant file is well within its window. Per [[skill-freshness-mtime-blind-in-gha]], the `git log` approach is the correct one in GHA; mtime is cloned-at time and would be equally uniform.
- **`skill-freshness` self-note** — the fix to use `git log -1 --format=%ct` instead of `stat --format=%Y` is flagged in MEMORY.md as a pending structural fix. This run applied that approach.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk git commit timestamps — this skill measures nothing it does not also report.*
