# Skill Freshness — 2026-07-23

**Verdict:** ✅ FRESHNESS_OK — 1 cross-skill dependency checked, all within freshness window.

*Audited 44 enabled skills · 1 dependency checked · 0 flagged*

## Flagged dependencies

*(none — fleet is silent-staleness-free)*

## What this means per consumer

All enabled consumers whose upstream file dependencies could be scored are reading fresh data. No action required.

## Healthy consumers

- pr-tracker — 1 dep (`memory/topics/pr-status.md`, topics class, ~2.5h old, threshold 168h).
- planner — no auditable cross-skill deps (self-state only).
- batch-health — no auditable cross-skill deps.
- notegraph — no auditable cross-skill deps (self-state only).
- heartbeat — no auditable cross-skill deps (token-report disabled, file never produced).
- surplus-pulse — no auditable cross-skill deps (self-state only).
- compute-futures-eda — no auditable cross-skill deps (self-state only).
- reflect — no auditable cross-skill deps (broad articles/ pattern, no specific named ref).

+ 36 more all-fresh consumers (no auditable non-self dependencies found).

## Source status

- `aeon.yml`: ~90 total entries, 44 enabled
- Implicit references discovered (surviving all filters): 1
- Explicit `chains: consume:` edges: 0 (chains block fully commented out in aeon.yml)
- Files not yet on disk (skipped — implicit references that never existed): 13

Skipped implicit never-existed refs: `memory/topics/pr-review-rules.md` (pr-review), `memory/topics/watched-repos.md` + `memory/topics/stale-models.md` (repo-revive), `memory/topics/compute-tokens.md` (compute-pulse), `memory/topics/projects.md` (surplus-pulse), `memory/topics/framework-watch-state.json` (ai-framework-watch), `memory/topics/compute-futures-macro-correlations.md` (compute-macro-correlate — on branch, not merged), `.outputs/github-trending.md` (vuln-scanner — github-trending is disabled), `memory/state/skill-repair-history.json` (skill-repair), `memory/state/fleet-control-state.json` (fleet-control), `memory/state/suggest-edges.json` (suggest-edges), `memory/topics/skill-graph-state.json` (skill-graph), `memory/topics/skills-history.md` (memory-flush).

## Structural note — GHA mtime blind spot

Per [[skill-freshness-mtime-blind-in-gha]], all on-disk files carry the same git log timestamp (`2026-07-23T07:27:27Z`, from a single initial bulk commit). The `git log -1 --format=%ct` fix recommended in MEMORY.md returns the same value for every file in this shallow clone, so per-file producer freshness cannot be individually distinguished from git timestamps alone.

Cross-referencing `memory/cron-state.json` (informational only — scoring uses on-disk timestamps per spec):

| Skill | last\_success | Age | Topic file | Note |
|-------|-------------|-----|------------|------|
| compute-pulse | 2026-07-18T12:05Z | ~5.9d | `memory/topics/compute-pulse.md` | Approaching 7d topics threshold; self-state only, no cross-skill consumer — no flag |
| notegraph | 2026-07-22T06:21Z | ~27.6h | `memory/state/notegraph.json` | Self-state, within threshold |
| heartbeat | 2026-07-22T09:14Z | ~24.7h | *(no topic file)* | No cross-skill deps |
| surplus-pulse | 2026-07-22T16:46Z | ~17.2h | `memory/topics/surplus-pulse.md` | Self-state, well within threshold |
| pr-tracker | 2026-07-22T11:24Z | ~22.6h | `memory/topics/pr-status.md` | **Only cross-skill dep audited** — within 168h threshold |

`compute-pulse` is the one to watch: at ~5.9 days since last run, the compute-pulse.md topic file will cross the 7-day WARN threshold if compute-pulse misses its next Saturday (2026-07-26) run. No enabled skill reads it cross-skill today, so no flag fires — but if a future skill adds a cross-skill reference to `memory/topics/compute-pulse.md`, it would immediately score WARN.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
